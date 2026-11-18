// Monta build/book.html a partir de src/pages/*.html + build/figures/*.svg
//   node scripts/build.mjs
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import katex from 'katex';
import * as cheerio from 'cheerio';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const P = (...a) => path.join(root, ...a);
const meta = JSON.parse(fs.readFileSync(P('src/meta.json'), 'utf8'));
const TOTAL = meta.pages.length;

// ---------------------------------------------------------------- matemática (KaTeX no build)
const MACROS = {
  '\\vB': '\\vec{B}', '\\vv': '\\vec{v}', '\\vF': '\\vec{F}', '\\vE': '\\vec{E}', '\\vN': '\\hat{n}',
  '\\vI': '\\vec{I}', '\\vL': '\\vec{L}', '\\vA': '\\vec{A}',
  '\\mz': '\\mu_0',
  '\\un': '\\,\\mathrm{#1}',
  '\\tx': '\\times10^{#1}',
  '\\dd': '\\mathrm{d}',
  '\\sen': '\\operatorname{sen}',
  '\\emf': '\\varepsilon',
  '\\degC': '{}^{\\circ}\\mathrm{C}',
};
let mathCount = 0;
function renderMath(src, display) {
  const fixed = src.replace(/(\d),(\d)/g, '$1{,}$2'); // vírgula decimal sem espaço
  mathCount++;
  try {
    return katex.renderToString(fixed, {
      displayMode: display, throwOnError: true, output: 'html', strict: 'ignore', trust: false,
      macros: { ...MACROS },
    });
  } catch (e) {
    throw new Error(`KaTeX falhou em «${src}»: ${e.message}`);
  }
}
function processMath(text) {
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, g) => renderMath(g.trim(), true));
  text = text.replace(/\$([^$\n]+?)\$/g, (_, g) => renderMath(g.trim(), false));
  return text;
}

// ---------------------------------------------------------------- utilidades
const LV_TXT = { 1: 'Fundamental', 2: 'Intermediário', 3: 'Avançado PAS' };
const lvDots = (l) => `<span class="lv l${l}" title="${LV_TXT[l]}"><i></i><i></i><i></i></span>`;
const OK_ICON = '<span class="okmark"><svg viewBox="0 0 12 12"><path d="M1.5 6.6 4.6 9.7 10.6 2.6" fill="none" stroke="#14703A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>';
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

function readSvg(name, label) {
  const f = P('build/figures', name + '.svg');
  if (!fs.existsSync(f)) { warn(`figura ausente: ${name}`); return `<div class="todo">[figura: ${name}]</div>`; }
  let s = fs.readFileSync(f, 'utf8').replace(/<\?xml[^>]*\?>/g, '').replace(/<!DOCTYPE[^>]*>/g, '').trim();
  s = s.replace(/^<svg /, `<svg role="img" aria-label="${esc(label || name)}" `);
  return s;
}
const warnings = [];
function warn(m) { warnings.push(m); console.warn('  ! ' + m); }

// ---------------------------------------------------------------- transformação de uma página
function buildBody(n, raw) {
  const html = processMath(raw);
  const $ = cheerio.load(html, { xmlMode: false, decodeEntities: false }, false);
  let figNo = 0;
  const figMap = {};

  // 1ª passada: numerar figuras com legenda
  const capOf = ($e) => { const c = $e.children('cap'); return c.length ? c.html() : $e.attr('cap'); };
  $('x-fig').each((_, el) => {
    const name = $(el).attr('name');
    if (capOf($(el)) !== undefined) { figNo++; figMap[name] = `${n}.${figNo}`; }
  });

  // figuras
  $('x-fig').each((_, el) => {
    const $e = $(el); const name = $e.attr('name'); const cap = capOf($e);
    const cls = $e.attr('cls') || '';
    const svg = readSvg(name, cap ? cap.replace(/<[^>]+>/g, '') : name);
    const capHtml = cap !== undefined ? `<figcaption><b>Fig. ${figMap[name]}</b> ${cap}</figcaption>` : '';
    const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const wAttr = $e.attr('w');
    const style = wAttr ? `width:${wAttr};max-width:100%` : (vb ? `width:${(+vb[1] * 25.4 / 96).toFixed(1)}mm;max-width:100%` : '');
    $e.replaceWith(`<figure class="fig ${cls}" style="${style}"><div class="svgw">${svg}</div>${capHtml}</figure>`);
  });
  $('x-ref').each((_, el) => {
    const f = $(el).attr('f');
    if (!figMap[f]) warn(`p${n}: x-ref para figura sem legenda: ${f}`);
    $(el).replaceWith(`<b>Fig. ${figMap[f] || '?'}</b>`);
  });

  // linhas <p data-k="Rótulo">…</p> -> <dt>/<dd>
  const rows = ($root) => $root.children('p[data-k]').map((_, p) => {
    const k = $(p).attr('data-k'); const cl = $(p).attr('class') || '';
    const isVer = /^verifica/i.test(k); const isRes = /^resultado/i.test(k);
    return `<dt class="${isVer ? 'ver' : ''}">${k}</dt><dd class="${isVer ? 'ver' : ''} ${isRes ? 'res' : ''} ${cl}">${$(p).html()}</dd>`;
  }).get().join('');

  // exemplos resolvidos
  $('x-ex').each((_, el) => {
    const $e = $(el); const l = +($e.attr('l') || 1);
    let r = rows($e).replace(/<dt class="ver">/g, '<dt class="ver">').replace(/(<dt class="ver">)/g, '$1');
    r = r.replace(/<dt class="ver">Verificação/g, `<dt class="ver">Verificação`);
    $e.replaceWith(`<div class="ex"><div class="ex-h"><span>Exemplo ${$e.attr('n')}</span><span class="ttl">${$e.attr('t') || ''}</span>${lvDots(l)}<span class="lvt">${LV_TXT[l]}</span></div><dl>${r}</dl></div>`);
  });

  // cartões de fórmula
  $('x-fc').each((_, el) => {
    const $e = $(el);
    const eqs = ($e.attr('eq') || '').split(';;').map((s) => s.trim()).filter(Boolean)
      .map((s) => renderMath(s, true)).join('');
    const sub = $e.attr('s') || '';
    $e.replaceWith(`<div class="fc ${$e.attr('cls') || ''}"><div class="fc-h"><span>Fórmula · ${$e.attr('t') || ''}</span><span>${sub}</span></div><div class="eq">${eqs}</div><dl>${rows($e)}</dl></div>`);
  });

  // caixas
  $('x-box').each((_, el) => {
    const $e = $(el); const k = $e.attr('k') || ''; const t = $e.attr('t');
    $e.replaceWith(`<div class="box ${k}">${t ? `<div class="bt">${t}</div>` : ''}${$e.html()}</div>`);
  });

  // exercícios
  $('x-exe').each((_, el) => {
    const $e = $(el); const l = +($e.attr('l') || 1);
    $e.replaceWith(`<div class="exe"><div class="n">E${$e.attr('n')}${lvDots(l)}</div><div>${$e.html()}</div></div>`);
  });
  $('x-ans').each((_, el) => { $(el).replaceWith(`<div class="ans"><b>Respostas:</b> ${$(el).html()}</div>`); });
  $('x-exs').each((_, el) => {
    const $e = $(el);
    $e.replaceWith(`<div class="exs"><div class="exs-h"><span>${$e.attr('t') || 'Exercícios'}</span><span>${$e.attr('s') || `${lvDots(1)} fundamental · ${lvDots(2)} intermediário · ${lvDots(3)} avançado PAS · todos autorais`}</span></div>${$e.html()}</div>`);
  });
  $('x-ok').each((_, el) => { $(el).replaceWith(OK_ICON); });

  let out = $.html();
  // espaçador flexível antes dos exercícios (ou no fim)
  if (out.includes('class="exs"')) out = out.replace('<div class="exs">', '<div class="grow"></div><div class="exs">');
  else out += '<div class="grow"></div>';
  return out;
}

// ---------------------------------------------------------------- montagem
function modOf(n) { for (const [k, v] of Object.entries(meta.modules)) if (n >= v.pages[0] && n <= v.pages[1]) return [k, v]; }
const pad = (n) => String(n).padStart(2, '0');

let pagesHtml = '';
for (const pg of meta.pages) {
  const n = pg.n; const [mk, mv] = modOf(n);
  const f = P('src/pages', `p${pad(n)}.html`);
  let raw;
  if (fs.existsSync(f)) raw = fs.readFileSync(f, 'utf8');
  else { raw = `<p class="todo">[página ${pad(n)} — conteúdo pendente]</p>`; warn(`página ${pad(n)} sem arquivo (stub)`); }
  const body = buildBody(n, raw);
  const prog = Array.from({ length: TOTAL }, (_, i) => {
    const q = i + 1; const inMod = q >= mv.pages[0] && q <= mv.pages[1];
    return `<i class="${q === n ? 'cur' : inMod ? 'mod' : ''}"></i>`;
  }).join('');
  const tb = pg.cover ? '' : `<div class="tb"><div class="num">${pad(n)}</div><div class="ttl"><h1>${pg.title}</h1>${pg.lead ? `<div class="lead">${processMath(pg.lead)}</div>` : ''}</div></div>`;
  pagesHtml += `
<section class="page" id="p${pad(n)}" data-n="${n}">
  <div class="prog">${prog}</div>
  <div class="hdr"><div class="brand"><span class="logo">CTG</span><span>Física · Eletromagnetismo · PAS 3 / UnB</span></div><div><b>Módulo ${mk}</b> · ${mv.name}</div></div>
  <div class="body">${tb}${body}</div>
  <div class="ftr">CTG · FÍSICA · ELETROMAGNETISMO · ${pg.subject.toUpperCase()} · <b>${pad(n)}/${TOTAL}</b></div>
</section>`;
}

const doc = `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>${meta.title}</title>
<meta name="author" content="CTG">
<link rel="stylesheet" href="../assets/fonts/fonts.css">
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<link rel="stylesheet" href="../src/css/book.css">
</head>
<body>${pagesHtml}
</body>
</html>`;
fs.mkdirSync(P('build'), { recursive: true });
fs.writeFileSync(P('build/book.html'), doc);
console.log(`book.html: ${TOTAL} páginas, ${mathCount} expressões KaTeX, ${warnings.length} avisos`);
