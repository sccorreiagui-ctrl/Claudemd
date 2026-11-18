// pré-visualiza figuras: node figs/preview.cjs nome1 nome2 ...  -> qa/fig_<nome>.png
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const names = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  const css = fs.readFileSync(path.join(ROOT, 'build/style.css'), 'utf8');
  for (const n of names) {
    const svg = fs.readFileSync(path.join(ROOT, 'figs/svg', n + '.svg'), 'utf8');
    const html = `<!doctype html><link rel=stylesheet href="file://${ROOT}/assets/katex/katex.min.css"><style>${css} body{padding:6mm;width:max-content} .page{display:none}</style><body><div style="display:inline-block;border:1px dashed #ccc">${svg}</div></body>`;
    fs.writeFileSync(path.join(ROOT, 'qa/_prev.html'), html);
    await p.goto('file://' + path.join(ROOT, 'qa/_prev.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(ROOT, 'qa', 'fig_' + n + '.png'), fullPage: true });
  }
  await b.close();
})();
