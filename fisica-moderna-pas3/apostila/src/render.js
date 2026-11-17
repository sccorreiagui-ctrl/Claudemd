// Renderiza apostila.html em PDF (A4): aplica KaTeX, ajusta a escala de cada página
// (preenche o A4 sem estourar) e produz um relatório de layout em out/layout_report.json.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ZMIN = 1.0, ZMAX = parseFloat(process.env.ZMAX || '1.22'), SLACK = 12; // px livres mínimos no rodapé do conteúdo
(async () => {
  const [, , html, pdf] = process.argv;
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.addScriptTag({ path: path.join(root, 'vendor/katex/katex.min.js') });
  const errs = await page.evaluate(() => {
    const e = [];
    document.querySelectorAll('m').forEach(el => {
      const src = el.textContent.trim();
      try { katex.render(src, el, { displayMode: el.classList.contains('d'), throwOnError: true, strict: 'ignore', output: 'html' }); }
      catch (err) { e.push(src + ' :: ' + err.message); }
    });
    return e;
  });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  // ajuste de escala por página (busca binária)
  const fit = await page.evaluate(async ({ ZMIN, ZMAX, SLACK }) => {
    const out = [];
    for (const pg of document.querySelectorAll('.page')) {
      const c = pg.querySelector('.content'), z = pg.querySelector('.zin');
      const H = c.getBoundingClientRect().height;
      const used = (zz) => { z.style.setProperty('--z', zz); return z.getBoundingClientRect().height; };
      let lo = ZMIN, hi = ZMAX;
      if (used(ZMIN) > H - SLACK) { out.push({ z: ZMIN, fits: false }); z.style.setProperty('--z', ZMIN); continue; }
      if (used(ZMAX) <= H - SLACK) { out.push({ z: ZMAX, fits: true, capped: true }); z.style.setProperty('--z', ZMAX); continue; }
      for (let i = 0; i < 14; i++) { const mid = (lo + hi) / 2; if (used(mid) <= H - SLACK) lo = mid; else hi = mid; }
      let zf = Math.floor(lo * 1000) / 1000;
      while (used(zf) > H - SLACK && zf > ZMIN) zf = Math.round((zf - 0.002) * 1000) / 1000; // não-monotonicidade por quebras de linha
      z.style.setProperty('--z', zf);
      out.push({ z: zf, fits: used(zf) <= H - SLACK });
    }
    return out;
  }, { ZMIN, ZMAX, SLACK });

  const rep = await page.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
    const c = pg.querySelector('.content'), z = pg.querySelector('.zin');
    const cr = c.getBoundingClientRect(), zr = z.getBoundingClientRect();
    let worst = null, maxR = 0;
    z.querySelectorAll('*').forEach(el => {
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return; // filhos de SVG são recortados pelo viewport
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.right > maxR) { maxR = r.right; worst = el.tagName + '.' + (el.className && el.className.baseVal === undefined ? el.className : '') ; }
    });
    return { page: i + 1, contentH: Math.round(cr.height), usedH: Math.round(zr.height), freePx: Math.round(cr.height - zr.height),
             overflowX: Math.round(maxR - cr.right), widest: worst, z: getComputedStyle(z).getPropertyValue('--z') };
  }));
  fs.writeFileSync(path.join(root, 'out', 'layout_report.json'), JSON.stringify({ katexErrors: errs, fit, pages: rep }, null, 1));
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  console.log('KaTeX errors:', errs.length); errs.forEach(e => console.log('  ', e));
  rep.forEach((r, i) => console.log(`p${r.page}: z=${(+r.z).toFixed(3)} usado ${r.usedH}/${r.contentH}px livre ${r.freePx}px overflowX ${r.overflowX}${r.overflowX > 2 ? ' <- ' + r.widest : ''}${fit[i].fits === false ? '  !! NÃO CABE' : ''}${fit[i].capped ? '  (z no teto)' : ''}`));
})();
