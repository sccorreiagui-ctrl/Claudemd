/* Gera apostila.html e o PDF definitivo.
 *   node build/build.cjs            -> HTML + PDF + relatório de overflow
 *   node build/build.cjs --html     -> apenas HTML
 */
const fs = require('fs');
const path = require('path');
const katex = require('katex');

const ROOT = path.resolve(__dirname, '..');
const PAGES_DIR = path.join(ROOT, 'content', 'pages');
const FIG_DIR = path.join(ROOT, 'figs', 'svg');
const DIST = path.join(ROOT, 'dist');
const PDF_NAME = 'CTG_MATEMATICA_COMPLEXOS_POLINOMIOS_PAS3_2026.pdf';

// cores semânticas nas fórmulas
const C = { re: '1f5fbf', im: '7a3fc2', ok: '167a44', ang: 'd4690a', bad: 'c62828', gr: '5f6b7a' };
const macros = {
  '\\re': `\\textcolor{${C.re}}{#1}`,
  '\\im': `\\textcolor{${C.im}}{#1}`,
  '\\ok': `\\textcolor{${C.ok}}{#1}`,
  '\\ang': `\\textcolor{${C.ang}}{#1}`,
  '\\bad': `\\textcolor{${C.bad}}{#1}`,
  '\\gr': `\\textcolor{${C.gr}}{#1}`,
  '\\conj': '\\overline{#1}',
  '\\cis': '\\operatorname{cis}',
  '\\sen': '\\operatorname{sen}',
  '\\tg': '\\operatorname{tg}',
  '\\Rep': '\\operatorname{Re}',
  '\\Imp': '\\operatorname{Im}',
  '\\gr_': '\\operatorname{gr}',
  '\\C': '\\mathbb{C}', '\\R': '\\mathbb{R}', '\\Q': '\\mathbb{Q}', '\\Z': '\\mathbb{Z}', '\\N': '\\mathbb{N}',
  '\\mdc': '\\operatorname{mdc}',
};

function renderMath(src, file) {
  const mk = (tex, display) => {
    try {
      return katex.renderToString(tex.trim(), { displayMode: display, throwOnError: true, strict: 'ignore', output: 'html', macros: { ...macros }, trust: false });
    } catch (e) {
      console.error(`ERRO KaTeX em ${file}: ${e.message}\n  >> ${tex.slice(0, 120)}`);
      process.exitCode = 2;
      return `<span style="color:red">[ERRO MATH]</span>`;
    }
  };
  let out = src.replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => mk(t, true));
  out = out.replace(/\$([^$\n]+?)\$/g, (_, t) => mk(t, false));
  return out;
}

function inlineFig(name) {
  const f = path.join(FIG_DIR, name + '.svg');
  if (!fs.existsSync(f)) {
    console.error(`FIGURA AUSENTE: ${name}`);
    process.exitCode = 2;
    return `<div style="color:red">[fig ${name} ausente]</div>`;
  }
  let s = fs.readFileSync(f, 'utf8');
  s = s.replace(/<\?xml[\s\S]*?\?>/, '').replace(/<!DOCTYPE[\s\S]*?>/, '').replace(/<!--[\s\S]*?-->/g, '');
  // evita colisão de ids entre svgs inline
  s = s.replace(/\bid="([^"]+)"/g, (_, i) => `id="${name}_${i}"`)
       .replace(/url\(#([^)]+)\)/g, (_, i) => `url(#${name}_${i})`)
       .replace(/(xlink:href|href)="#([^"]+)"/g, (_, a, i) => `${a}="#${name}_${i}"`);
  return s.trim();
}

const MODS = { C: 'Números Complexos', P: 'Polinômios' };

function buildPage(n, raw) {
  const file = `p${String(n).padStart(2, '0')}.html`;
  let meta = { topic: '' };
  raw = raw.replace(/^\s*<!--META\s*([\s\S]*?)-->/, (_, j) => { meta = JSON.parse(j); return ''; });
  let body = renderMath(raw, file);
  body = body.replace(/\{\{fig:([a-z0-9_]+)\}\}/g, (_, nm) => inlineFig(nm));
  const mod = n <= 20 ? 'C' : 'P';
  const modName = MODS[mod];
  const partName = mod === 'C' ? 'Parte I' : 'Parte II';
  return `<section class="page mod-${mod}" id="p${n}" data-n="${n}">
<div class="ph"><span><span class="mk">CTG</span> &nbsp;MATEMÁTICA | PAS 3 / UNB</span><span>${partName} · ${modName}</span></div>
<div class="pc">
${body}
</div>
<div class="pf"><span>CTG · MATEMÁTICA · <b>${modName}</b> · ${meta.topic} · ${String(n).padStart(2, '0')}/40</span></div>
</section>`;
}

function buildHtml() {
  const pages = [];
  for (let n = 1; n <= 40; n++) {
    const f = path.join(PAGES_DIR, `p${String(n).padStart(2, '0')}.html`);
    if (!fs.existsSync(f)) {
      pages.push(`<section class="page mod-${n <= 20 ? 'C' : 'P'}" id="p${n}" data-n="${n}"><div class="pc">[página ${n} ausente]</div></section>`);
      console.error(`página ausente: ${n}`);
      continue;
    }
    pages.push(buildPage(n, fs.readFileSync(f, 'utf8')));
  }
  const css = fs.readFileSync(path.join(__dirname, 'style.css'), 'utf8');
  const html = `<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>CTG · Matemática · Números Complexos e Polinômios · PAS 3/UnB</title>
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<style>${css}</style></head>
<body>
${pages.join('\n')}
</body></html>`;
  fs.mkdirSync(DIST, { recursive: true });
  const out = path.join(DIST, 'apostila.html');
  fs.writeFileSync(out, html);
  return out;
}

async function toPdf(htmlPath) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const rep = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach(pg => {
      const pc = pg.querySelector('.pc');
      const pr = pc.getBoundingClientRect();
      let maxB = 0;
      pc.querySelectorAll(':scope > *').forEach(ch => { maxB = Math.max(maxB, ch.getBoundingClientRect().bottom); });
      const natural = pc.scrollHeight - pc.clientHeight; // >0: estouro
      // altura realmente usada pelos filhos (sem considerar margin-top:auto)
      let used = 0;
      pc.querySelectorAll(':scope > *').forEach(ch => {
        const cs = getComputedStyle(ch);
        used += ch.getBoundingClientRect().height + parseFloat(cs.marginBottom || 0) + (cs.marginTop === 'auto' ? 0 : parseFloat(cs.marginTop || 0));
      });
      // elementos internos que transbordam horizontalmente
      let hOver = 0;
      pc.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.right > pr.right + 1.5 && r.width > 0 && !e.closest('svg')) hOver++; });
      out.push({ n: +pg.dataset.n, overflowPx: Math.round(natural), usedPx: Math.round(used), availPx: Math.round(pr.height), slackPx: Math.round(pr.height - used), hOver });
    });
    return out;
  });
  fs.writeFileSync(path.join(DIST, 'layout_report.json'), JSON.stringify(rep, null, 1));
  const pdf = path.join(DIST, PDF_NAME);
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await browser.close();
  return rep;
}

(async () => {
  const html = buildHtml();
  if (process.argv.includes('--html')) return;
  const rep = await toPdf(html);
  const bad = rep.filter(r => r.overflowPx > 0 || r.hOver > 0);
  console.log('páginas medidas:', rep.length);
  rep.forEach(r => console.log(`p${String(r.n).padStart(2, '0')} folga=${String(r.slackPx).padStart(4)}px overflow=${r.overflowPx} hOver=${r.hOver}`));
  if (bad.length) { console.log('PÁGINAS COM ESTOURO:', bad.map(b => b.n).join(', ')); }
})();
