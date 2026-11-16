// Mede larguras de avanço (em unidades de em) dos fontes usados nas figuras SVG.
// Saída: src/lib/metrics.json  — usado pelo svgkit.py para posicionar rótulos com exatidão.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const html = `<!doctype html><meta charset="utf-8">
  <link rel="stylesheet" href="file://${ROOT}/src/fonts.css">
  <link rel="stylesheet" href="file://${ROOT}/assets/katex/katex.min.css">
  <body><span style="font-family:KaTeX_Main">a</span><span style="font-family:KaTeX_Math;font-style:italic">a</span><span style="font-family:'Source Sans 3'">a</span></body>`;
  fs.writeFileSync(path.join(ROOT, 'build', '_measure.html'), html);
  await page.goto('file://' + path.join(ROOT, 'build', '_measure.html'));
  const chars = [];
  for (let c = 32; c < 256; c++) chars.push(String.fromCharCode(c));
  for (let c = 0x391; c <= 0x3C9; c++) chars.push(String.fromCharCode(c));
  chars.push('−','·','×','±','°','µ','≈','→','∞','√','²','³','⁻','¹','⁰','⁴','⁵','⁶','⁷','⁸','⁹','∥','⊥');
  const fonts = {
    sans400: '400 100px "Source Sans 3"', sans600: '600 100px "Source Sans 3"', sans700: '700 100px "Source Sans 3"',
    sans400i: 'italic 400 100px "Source Sans 3"',
    math: 'italic 400 100px KaTeX_Math', main: '400 100px KaTeX_Main', mainb: '700 100px KaTeX_Main'
  };
  const out = await page.evaluate(async ({ fonts, chars }) => {
    const res = {};
    const cv = document.createElement('canvas'); const ctx = cv.getContext('2d');
    for (const [k, spec] of Object.entries(fonts)) {
      try { await document.fonts.load(spec, chars.join('')); } catch (e) {}
      ctx.font = spec; res[k] = {};
      for (const ch of chars) res[k][ch] = +(ctx.measureText(ch).width / 100).toFixed(4);
    }
    return res;
  }, { fonts, chars });
  fs.writeFileSync(path.join(ROOT, 'src', 'lib', 'metrics.json'), JSON.stringify(out));
  // sanity
  console.log('sans400 A,i,W,0:', out.sans400.A, out.sans400.i, out.sans400.W, out.sans400['0']);
  console.log('math F,R,I,ε:', out.math.F, out.math.R, out.math.I, out.math['ε']);
  console.log('main 0,Ω,=,(:', out.main['0'], out.main['Ω'], out.main['='], out.main['(']);
  await browser.close();
})();
