// Renderiza o HTML da apostila em PDF (Chromium/Playwright) e audita o layout de cada página.
// Uso: node render_pdf.js <html> <pdf> <relatorio.json>
const fs = require('fs');
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(path.join(process.env.NODE_PATH || '', 'playwright'))); }

(async () => {
  const [html, pdf, report] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  const audit = await page.evaluate(() => {
    const res = [];
    document.querySelectorAll('.page').forEach((pg, idx) => {
      const body = pg.querySelector('.pg-body');
      const r = { page: idx + 1, id: pg.id, over: 0, free: null, hover: [], clipped: [] };
      if (body) {
        const br = body.getBoundingClientRect();
        r.over = Math.max(0, Math.round((body.scrollHeight - body.clientHeight) * 10) / 10);
        let maxB = br.top;
        body.querySelectorAll('*').forEach(el => {
          if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
          const cs = getComputedStyle(el);
          if (cs.position === 'absolute') return;
          const b = el.getBoundingClientRect();
          if (b.width === 0 && b.height === 0) return;
          if (b.bottom > maxB) maxB = b.bottom;
          const pr = pg.getBoundingClientRect();
          if (b.right > pr.right - 8 || b.left < pr.left + 8) {
            if (r.hover.length < 4) r.hover.push(el.tagName.toLowerCase() + '.' + (el.className && el.className.baseVal === undefined ? el.className : '') + ' ' + Math.round(b.left - pr.left) + '-' + Math.round(b.right - pr.left));
          }
          if ((cs.overflow === 'hidden' || cs.overflowX === 'hidden') && el !== body && el.scrollWidth > el.clientWidth + 2) {
            if (r.clipped.length < 4) r.clipped.push('W:' + el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className : '') + ' ' + el.scrollWidth + '>' + el.clientWidth);
          }
          if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden') && el !== body && el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0) {
            if (r.clipped.length < 4) r.clipped.push('H:' + el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className : '') + ' ' + el.scrollHeight + '>' + el.clientHeight);
          }
        });
        r.free = Math.round((br.bottom - maxB) * 10) / 10;
      }
      res.push(r);
    });
    return res;
  });
  fs.writeFileSync(report, JSON.stringify(audit, null, 1));

  await page.pdf({
    path: pdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
