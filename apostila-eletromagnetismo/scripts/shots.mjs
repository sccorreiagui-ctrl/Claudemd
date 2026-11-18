// Captura PNG das figuras SVG (mesmas fontes do livro) para inspeção visual.
//   node scripts/shots.mjs nome1 nome2 ...   (sem argumentos: todas)   [--scale=2]
import fs from 'fs'; import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const figDir = path.join(root, 'build/figures'); const shotDir = path.join(root, 'build/shots');
fs.mkdirSync(shotDir, { recursive: true });
const args = process.argv.slice(2);
const scale = +(args.find((a) => a.startsWith('--scale='))?.split('=')[1] || 1.6);
let names = args.filter((a) => !a.startsWith('--'));
if (!names.length) names = fs.readdirSync(figDir).filter((f) => f.endsWith('.svg')).map((f) => f.slice(0, -4));
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: scale, viewport: { width: 760, height: 900 } });
for (const n of names) {
  const f = path.join(figDir, n + '.svg'); if (!fs.existsSync(f)) { console.log('ausente', n); continue; }
  const svg = fs.readFileSync(f, 'utf8');
  const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const w = Math.round(+vb[1]), h = Math.round(+vb[2]);
  const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${root}/assets/fonts/fonts.css"><link rel="stylesheet" href="file://${root}/assets/katex/katex.min.css">
  <style>body{margin:0;background:#fff} .w{width:${w}px;height:${h}px;border:1px solid #e3e7ee;box-sizing:content-box} svg{display:block;width:${w}px;height:${h}px}</style></head><body><div class="w">${svg}</div></body></html>`;
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.locator('.w').screenshot({ path: path.join(shotDir, n + '.png') });
  console.log('shot', n, `${w}x${h}`);
}
await browser.close();
