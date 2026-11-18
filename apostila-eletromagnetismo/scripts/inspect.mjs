// Lista a altura (mm) dos blocos de uma página: node scripts/inspect.mjs 3
import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const n = +process.argv[2] || 1;
const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
await page.emulateMedia({ media: 'print' });
await page.goto('file://' + path.join(root, 'build/book.html'), { waitUntil: 'load' });
await page.evaluate(async () => { await document.fonts.ready; });
const out = await page.evaluate((n) => {
  const mm = (px) => +(px * 25.4 / 96).toFixed(1);
  const body = document.querySelector(`#p${String(n).padStart(2, '0')} .body`);
  const rows = [];
  let y0 = body.getBoundingClientRect().top;
  for (const c of body.children) {
    const r = c.getBoundingClientRect();
    const cls = c.className || c.tagName;
    const item = { cls: String(cls).slice(0, 28), top: mm(r.top - y0), h: mm(r.height) };
    rows.push(item);
    if (/main/.test(cls)) for (const k of c.children) { const kr = k.getBoundingClientRect(); const it = { cls: '  ' + String(k.className || k.tagName).slice(0, 26), top: mm(kr.top - y0), h: mm(kr.height) }; if (/row/.test(k.className)) it.cols = [...k.children].map((q) => mm(q.getBoundingClientRect().height)); rows.push(it); }
  }
  return { avail: mm(body.clientHeight), rows };
}, n);
console.log('página', n, '— altura útil', out.avail, 'mm');
for (const r of out.rows) console.log(String(r.top).padStart(6), String(r.h).padStart(6), ' ', r.cls, r.cols ? '  colunas: ' + r.cols.join(' | ') : '');
await browser.close();
