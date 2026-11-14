// Exporta html/apostila.html -> output/APOSTILA_GEOGRAFIA_ENEM_2026.pdf (A4) e gera relatório de overflow.
// Uso: node tools/export_pdf.js [html] [pdf]
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) {
  ({ chromium } = require(path.join(process.env.NODE_PATH || '/opt/node22/lib/node_modules', 'playwright')));
}
const root = path.resolve(__dirname, '..');
const htmlPath = path.resolve(process.argv[2] || path.join(root, 'html', 'apostila.html'));
const pdfPath = path.resolve(process.argv[3] || path.join(root, 'output', 'APOSTILA_GEOGRAFIA_ENEM_2026.pdf'));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
  const msgs = [];
  page.on('console', m => { if (['error', 'warning'].includes(m.type())) msgs.push(m.type() + ': ' + m.text()); });
  page.on('pageerror', e => msgs.push('pageerror: ' + e.message));
  await page.goto('file://' + htmlPath, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  // Verificação de overflow: elementos que ultrapassam o corpo (.pb) da página ou caixas com conteúdo cortado
  const report = await page.evaluate(() => {
    const out = [];
    const mm = 96 / 25.4;
    document.querySelectorAll('.page').forEach((pg, i) => {
      const pr = pg.getBoundingClientRect();
      const body = pg.querySelector('.pb');
      const issues = [];
      if (body) {
        const br = body.getBoundingClientRect();
        // conteúdo vertical excedente
        let maxBottom = 0;
        body.querySelectorAll('*').forEach(el => {
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) return;
          if (r.bottom > maxBottom) maxBottom = r.bottom;
          if (r.right > br.right + 2) issues.push({ t: 'right-overflow', el: el.tagName + '.' + (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className), over: +(r.right - br.right).toFixed(1) });
        });
        const free = (br.bottom - maxBottom) / mm;
        issues.push({ t: 'free-bottom-mm', v: +free.toFixed(1) });
        if (free < -0.5) issues.push({ t: 'BOTTOM-OVERFLOW', mm: +(-free).toFixed(1) });
        // elementos com texto cortado (scrollHeight > clientHeight) dentro de boxes
        body.querySelectorAll('.box,.q,.chain .c,td,th,.stat,.cap').forEach(el => {
          if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow !== 'visible') issues.push({ t: 'clipped', el: el.className });
        });
      }
      out.push({ page: i + 1, id: pg.id || '', issues });
    });
    return out;
  });
  fs.writeFileSync(path.join(root, 'output', 'overflow_report.json'), JSON.stringify({ messages: msgs, pages: report }, null, 1));
  await page.pdf({ path: pdfPath, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  const bad = report.filter(p => p.issues.some(x => x.t === 'BOTTOM-OVERFLOW' || x.t === 'right-overflow' || x.t === 'clipped'));
  console.log(`PDF: ${pdfPath}`);
  console.log(`Páginas no HTML: ${report.length}; com problemas: ${bad.length}`);
  report.forEach(p => {
    const free = p.issues.find(x => x.t === 'free-bottom-mm');
    const probs = p.issues.filter(x => x.t !== 'free-bottom-mm');
    console.log(`  p${String(p.page).padStart(2, '0')} livre=${free ? free.v : '?'}mm` + (probs.length ? '  ⚠ ' + JSON.stringify(probs.slice(0, 4)) : ''));
  });
  if (msgs.length) console.log('Mensagens do navegador:', msgs.slice(0, 10));
})();
