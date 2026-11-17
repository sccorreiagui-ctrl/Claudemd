// Uso: node build.js [--pdf] [--check] [--png]
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const ROOT = __dirname;
const DIST = path.join(ROOT, 'dist');
const PDF = path.join(DIST, 'APOSTILA_HISTORIA_BRASIL_ENEM_PAS3_2026.pdf');
const args = process.argv.slice(2);

function buildHtml() {
  const H = require('./src/lib/h.js');
  const dir = path.join(ROOT, 'src', 'pages');
  const files = fs.readdirSync(dir).filter((f) => /^p\d\d\.js$/.test(f)).sort();
  const pages = files.map((f) => { delete require.cache[require.resolve(path.join(dir, f))]; return require(path.join(dir, f))(H); });
  const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Apostila Visual de História do Brasil — ENEM e PAS 3 (UnB) 2026</title>
<meta name="author" content="Apostila Visual de História do Brasil"><meta name="description" content="Era Vargas, República de 1946, Ditadura Militar e Nova República — revisão para ENEM e PAS 3/UnB">
<link rel="stylesheet" href="../src/styles.css"></head><body>${pages.join('\n')}</body></html>`;
  fs.mkdirSync(DIST, { recursive: true });
  fs.writeFileSync(path.join(DIST, 'apostila.html'), html);
  return { count: files.length, used: [...H.USED_IMAGES] };
}

async function run() {
  const info = buildHtml();
  console.log(`HTML gerado: ${info.count} páginas; imagens usadas: ${info.used.length}`);
  if (!args.includes('--pdf') && !args.includes('--check')) return;
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 } });
  const page = await ctx.newPage();
  await page.goto('file://' + path.join(DIST, 'apostila.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  if (args.includes('--check')) {
    const report = await page.evaluate(() => {
      const out = [];
      const MM = 96 / 25.4;
      document.querySelectorAll('.page').forEach((pg) => {
        const n = pg.dataset.n;
        const pr = pg.getBoundingClientRect();
        const pb = pg.querySelector('.pb').getBoundingClientRect();
        const limitB = pr.top + (297 - 13.0) * MM, limitR = pr.left + (210 - 12.5) * MM, limitL = pr.left + 12.5 * MM;
        let maxB = 0;
        pg.querySelectorAll('.pb *').forEach((el) => {
          if (el.closest('.cover-hero') && el.classList.contains('stripe')) return;
          const r = el.getBoundingClientRect();
          if (r.width === 0 && r.height === 0) return;
          maxB = Math.max(maxB, r.bottom);
          if (r.right > limitR + 1 && !el.closest('svg')) out.push(`p${n}: overflow direita <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal === undefined ? el.className : ''}"> ${el.textContent.trim().slice(0, 40)}`);
          if (r.left < limitL - 1 && !el.closest('svg')) out.push(`p${n}: overflow esquerda <${el.tagName.toLowerCase()} class="${el.className}"> ${el.textContent.trim().slice(0, 40)}`);
          const cs = getComputedStyle(el);
          if ((cs.overflow === 'hidden' || cs.overflowY === 'hidden') && el.scrollHeight > el.clientHeight + 1 && !el.classList.contains('page') && !el.classList.contains('cover-hero')) out.push(`p${n}: conteúdo cortado em <${el.tagName.toLowerCase()} class="${el.className}">`);
        });
        const pbScroll = pg.querySelector('.pb');
        const free = (limitB - maxB) / MM;
        out.push(`p${n}: espaço livre no rodapé = ${free.toFixed(1)} mm${free < 0 ? '  <<< ESTOURO' : ''}`);
        // sobreposição de rótulos de timeline
        pg.querySelectorAll('.tl').forEach((tl) => {
          const labs = [...tl.querySelectorAll('.lab .box')].map((b) => ({ r: b.getBoundingClientRect(), t: b.textContent.slice(0, 25), cls: b.parentElement.className }));
          for (let i = 0; i < labs.length; i++) for (let j = i + 1; j < labs.length; j++) {
            const a = labs[i], b = labs[j];
            if (a.cls.split(' ')[1] !== b.cls.split(' ')[1]) continue;
            const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
            const oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
            if (ox > 1 && oy > 1) out.push(`p${n}: SOBREPOSIÇÃO timeline "${a.t}" x "${b.t}"`);
          }
          // rótulo fora do bloco
          labs.forEach((a) => { if (a.r.left < limitL - 1 || a.r.right > limitR + 1) out.push(`p${n}: rótulo de timeline fora da margem "${a.t}"`); });
        });
      });
      return out;
    });
    fs.writeFileSync(path.join(DIST, 'check.txt'), report.join('\n'));
    console.log(report.join('\n'));
  }

  if (args.includes('--pdf')) {
    await page.pdf({ path: PDF, format: 'A4', printBackground: true, preferCSSPageSize: true, tagged: true, outline: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    console.log('PDF:', PDF);
  }
  await browser.close();
  if (args.includes('--png')) {
    const out = path.join(DIST, 'png');
    fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
    execSync(`pdftoppm -r ${process.env.DPI || 80} -png "${PDF}" "${out}/p"`);
    console.log('PNGs em', out);
  }
}
run().catch((e) => { console.error(e); process.exit(1); });
