// Renderiza build/manual.html -> PDF (Chromium) e imprime um relatório de qualidade por página.
//   node render.js build/manual.html out/arquivo.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  const errs = [];
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.goto('file://' + path.resolve(input));
  await page.waitForFunction(() => window.__done === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);

  const report = await page.evaluate(() => {
    const out = { pages: [], katexErrors: [] };
    document.querySelectorAll('.katex-error').forEach(e => out.katexErrors.push(e.textContent.slice(0, 80)));
    document.querySelectorAll('.page').forEach(pg => {
      const body = pg.querySelector('.body');
      const br = body.getBoundingClientRect();
      const kids = [...body.children];
      const cs = getComputedStyle(body);
      const gap = parseFloat(cs.rowGap) || 0;
      const used = kids.reduce((a, k) => a + k.getBoundingClientRect().height, 0) + gap * Math.max(0, kids.length - 1);
      const avail = body.clientHeight - parseFloat(cs.paddingTop);
      const pr = pg.getBoundingClientRect();
      // elementos que ultrapassam a margem direita/esquerda da página
      const wide = [];
      pg.querySelectorAll('.cb, .card, .example, .box, .formula, table, svg, .figbox').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.right > pr.right - 8 || r.left < pr.left + 8) wide.push(el.className.baseVal ?? el.className);
      });
      // cartões cujo conteúdo transborda (texto cortado dentro do cartão/caixa)
      const clipped = [];
      pg.querySelectorAll('.card, .cb, .example, .box, .formula, .figbox').forEach(el => {
        if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) clipped.push((el.className.baseVal ?? el.className) + ':' + (el.scrollHeight - el.clientHeight) + '/' + (el.scrollWidth - el.clientWidth));
      });
      out.pages.push({
        n: +pg.dataset.page,
        overflow: Math.max(Math.round(body.scrollHeight - body.clientHeight), Math.round(used - avail)),
        free: Math.round(avail - used),
        wide: [...new Set(wide)].slice(0, 5),
        clipped: [...new Set(clipped)].slice(0, 6),
      });
    });
    return out;
  });

  await page.pdf({ path: output, format: 'A4', printBackground: true, preferCSSPageSize: true, outline: true, tagged: true });
  await browser.close();
  console.log(JSON.stringify({ errs, ...report }));
})().catch(e => { console.error(e); process.exit(1); });
