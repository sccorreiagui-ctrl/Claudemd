// folha de contato: node figs/sheet.cjs saida.png nome1 nome2 ...
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const [out, ...names] = process.argv.slice(2);
  const css = fs.readFileSync(path.join(ROOT, 'build/style.css'), 'utf8');
  const cells = names.map(n => `<div class="cell"><div class="nm">${n}</div>${fs.readFileSync(path.join(ROOT, 'figs/svg', n + '.svg'), 'utf8')}</div>`).join('');
  const html = `<!doctype html><link rel=stylesheet href="file://${ROOT}/assets/katex/katex.min.css"><style>${css}
   body{padding:4mm;width:380mm} .cell{display:inline-block;vertical-align:top;margin:2mm;border:1px dashed #ccc} .nm{font:7px monospace;color:#999}</style><body>${cells}</body>`;
  fs.writeFileSync(path.join(ROOT, 'qa/_sheet.html'), html);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + path.join(ROOT, 'qa/_sheet.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(ROOT, 'qa', out), fullPage: true }); await b.close();
})();
