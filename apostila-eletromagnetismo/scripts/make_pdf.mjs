// Gera o PDF com Chromium (Playwright) e mede ocupação/overflow de cada página.
//   node scripts/make_pdf.mjs [saida.pdf]
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.resolve(process.argv[2] || path.join(root, 'build/book.pdf'));

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.join(root, 'build/book.html'), { waitUntil: 'load' });
await page.evaluate(async () => { await document.fonts.ready; });

const rep = await page.evaluate(() => [...document.querySelectorAll('.page')].map((pg) => {
  const body = pg.querySelector('.body');
  const main = body.querySelector(':scope > .main');
  let slackPx = null;
  if (main) {
    let tot = 0;
    for (const c of main.children) { const cs = getComputedStyle(c); tot += c.getBoundingClientRect().height + parseFloat(cs.marginTop) + parseFloat(cs.marginBottom); }
    slackPx = main.getBoundingClientRect().height - tot;
  }
  const br = body.getBoundingClientRect();
  let maxR = 0, maxB = 0;
  body.querySelectorAll('*').forEach((el) => {
    if (el.closest('svg') && el.tagName !== 'svg') return; if (el.closest('.mast-art')) return;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    maxR = Math.max(maxR, r.right); maxB = Math.max(maxB, r.bottom);
  });
  const mm = (px) => +(px * 25.4 / 96).toFixed(1);
  return {
    n: +pg.dataset.n, avail: mm(body.clientHeight), slack: slackPx === null ? null : mm(slackPx),
    overY: mm(body.scrollHeight - body.clientHeight), overX: mm(body.scrollWidth - body.clientWidth),
    right: mm(maxR - br.right), bottom: mm(maxB - br.bottom),
  };
}));

let bad = 0;
console.log('pág  folga(mm)  overflowY  overflowX  extrapola(dir/baixo)');
for (const r of rep) {
  const flag = (r.overY > 0.8 || r.overX > 0.3 || r.right > 0.3 || r.bottom > 0.3 || (r.slack !== null && r.slack < 0)) ? '  <<< PROBLEMA' : '';
  if (flag) bad++;
  console.log(String(r.n).padStart(3), String(r.slack).padStart(9), String(r.overY).padStart(10), String(r.overX).padStart(10), `  ${r.right}/${r.bottom}${flag}`);
}
await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await browser.close();
fs.writeFileSync(path.join(root, 'build/layout_report.json'), JSON.stringify(rep, null, 1));
console.log(`PDF: ${out}  |  páginas com problema de layout: ${bad}`);
