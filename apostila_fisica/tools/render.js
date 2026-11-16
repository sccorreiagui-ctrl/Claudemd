// Renderiza build/apostila.html → PDF (Chromium/Playwright) e mede preenchimento/overflow de cada página.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const html = path.join(ROOT, 'build', 'apostila.html');
const pdf = process.argv[2] || path.join(ROOT, 'build', 'apostila.pdf');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
  await page.emulateMedia({ media: 'print' });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
  await page.waitForTimeout(300);
  const rep = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('section.page').forEach((pg, i) => {
      const body = pg.querySelector('.body'), flow = pg.querySelector('.flow');
      if (!body || !flow) { out.push({ page: i + 1, special: true }); return; }
      const br = body.getBoundingClientRect();
      const bh = body.clientHeight;
      // altura natural do conteúdo = maior bottom entre filhos diretos
      let maxB = 0, maxR = 0, offender = null, wEl = null;
      flow.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        if (el.closest('.katex-mathml') || (el.closest('.katex') && el.tagName.toLowerCase() === 'path')) return;
        maxB = Math.max(maxB, r.bottom - br.top);
        if (r.right - br.left > maxR) { maxR = r.right - br.left; wEl = el.tagName + '.' + (el.getAttribute('class')||'') + ' «' + (el.textContent||'').trim().slice(0,30) + '»'; }
      });
      const kids = [...flow.children];
      for (const k of kids) { const r = k.getBoundingClientRect(); if (r.bottom - br.top > bh + 0.5) { offender = (k.className || k.tagName) + ': ' + k.textContent.trim().slice(0, 50); break; } }
      const katexErr = pg.querySelectorAll('.katex-error').length;
      const wide = [];
      pg.querySelectorAll('.katex-display, .calc, .eq, table, .gab, .cond').forEach(el => {
        const sw = el.scrollWidth, cw = el.clientWidth;
        if (cw > 0 && sw > cw + 1.5) wide.push(el.className + ' sw=' + sw + ' cw=' + cw + ' «' + (el.textContent||'').trim().slice(0, 40) + '»');
      });
      // KaTeX: elementos .base mais largos que o contêiner
      pg.querySelectorAll('.katex-display').forEach(d => {
        const dr = d.getBoundingClientRect(); let mx = 0;
        d.querySelectorAll('.base').forEach(b => { mx = Math.max(mx, b.getBoundingClientRect().right); });
        if (mx > dr.right + 1.5) wide.push('katex-display overflow +' + (mx - dr.right).toFixed(0) + 'px «' + (d.textContent||'').trim().slice(0, 40) + '»');
      });
      out.push({ page: i + 1, fill: +(maxB / bh).toFixed(3), over_px: +(maxB - bh).toFixed(1), over_w_px: +(maxR - body.clientWidth).toFixed(1), wEl, offender, katexErr, wide });
    });
    return out;
  });
  fs.writeFileSync(path.join(ROOT, 'build', 'layout_report.json'), JSON.stringify(rep, null, 1));
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, tagged: true, outline: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  const bad = rep.filter(r => !r.special && (r.over_px > 0.5 || r.over_w_px > 0.5 || r.katexErr || (r.wide && r.wide.length)));
  console.log('PDF:', pdf);
  console.log('páginas:', rep.length, '| com problema:', bad.length);
  rep.forEach(r => { if (!r.special) console.log(`p${String(r.page).padStart(2,'0')} fill=${(r.fill*100).toFixed(0).padStart(3)}%` + (r.over_px > 0.5 ? `  ⛔ OVERFLOW ${r.over_px}px → ${r.offender}` : '') + (r.over_w_px > 0.5 ? `  ↔ largura +${r.over_w_px}px → ${r.wEl}` : '') + (r.katexErr ? `  ✖ katex errors: ${r.katexErr}` : '') + ((r.wide && r.wide.length) ? '\n      ↔ ' + r.wide.join('\n      ↔ ') : '')); });
})();
