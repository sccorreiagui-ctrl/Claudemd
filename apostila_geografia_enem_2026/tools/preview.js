// Renderiza um ou mais SVGs (assets/figures/NAME.svg) em PNG para inspeção. Uso: node tools/preview.js out_dir name1 name2 ... [--w=710]
const path = require('path'); const fs = require('fs');
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const root = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const outDir = args[0]; const wArg = args.find(a => a.startsWith('--w=')); const W = wArg ? +wArg.split('=')[1] : 710;
const names = args.slice(1).filter(a => !a.startsWith('--'));
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: W + 20, height: 900 }, deviceScaleFactor: 2 });
  const css = fs.readFileSync(path.join(root, 'assets/css/fonts.css'), 'utf8').replace(/\.\.\/assets\/fonts/g, 'file://' + root + '/assets/fonts');
  for (const n of names) {
    const svg = fs.readFileSync(path.join(root, 'assets/figures', n + '.svg'), 'utf8');
    const page = await ctx.newPage();
    await page.setContent(`<html><head><style>${css} body{margin:10px;background:#fff;font-family:Inter} .w{width:${W}px;outline:1px dashed #ccc}</style></head><body><div class="w">${svg}</div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    const el = await page.$('.w'); await el.screenshot({ path: path.join(outDir, n + '.png') });
    await page.close();
  }
  await b.close();
})();
