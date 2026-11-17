// Componentes de diagramação da apostila. Tudo devolve strings HTML/SVG (vetoriais).
const fs = require('fs');
const path = require('path');

const ASSETS = path.join(__dirname, '..', '..', 'assets', 'img');
let CREDITS = {};
try { CREDITS = JSON.parse(fs.readFileSync(path.join(ASSETS, 'credits.json'), 'utf8')); } catch (e) { CREDITS = {}; }
const USED_IMAGES = new Set();

const PERIODOS = {
  vargas: { nome: 'ERA VARGAS', cor: '#1e3a5f', idx: 0 },
  r46: { nome: 'REPÚBLICA DE 1946', cor: '#2a7a4b', idx: 1 },
  dit: { nome: 'DITADURA MILITAR', cor: '#b3261e', idx: 2 },
  nova: { nome: 'NOVA REPÚBLICA', cor: '#2a7a4b', idx: 3 },
  geral: { nome: 'VISÃO GERAL', cor: '#1e3a5f', idx: -1 },
};

function miniBar(idx) {
  const segs = [['#1e3a5f', 15], ['#2a7a4b', 19], ['#b3261e', 21], ['#2a7a4b', 25]];
  return '<span class="mb" style="display:inline-flex;gap:.5mm;vertical-align:middle;margin-left:3mm">' +
    segs.map(([c, w], i) => `<span style="display:inline-block;height:1.5mm;width:${w * 0.28}mm;border-radius:.4mm;background:${idx === -1 || i === idx ? c : '#dfe4ea'}"></span>`).join('') + '</span>';
}

function page(n, meta, body) {
  const P = PERIODOS[meta.per];
  const num = String(n).padStart(2, '0');
  return `
<section class="page" id="p${num}" data-n="${n}">
  <div class="ph"><span><span class="dot" style="background:${P.cor}"></span>HISTÓRIA DO BRASIL | <b>${P.nome}</b></span><span>ENEM · PAS 3/UnB ${miniBar(P.idx)}</span></div>
  <div class="pb">${body}</div>
  <div class="pf"><span><b style="color:${P.cor}">${P.nome}</b> · ${meta.assunto} · ${meta.intervalo}</span><span class="pn">${num} <small>/ 24</small></span></div>
</section>`;
}

const CHIPS = {
  dir: ['soc', 'Eleição direta'], ind: ['inst', 'Eleição indireta'], const: ['o-inst', 'Sucessão constitucional'],
  ren: ['cris', 'Renúncia'], dep: ['o-rep', 'Deposição'], golpe: ['rep', 'Golpe'], morte: ['gray', 'Morte / suicídio'],
  imp: ['cris', 'Impeachment'], junta: ['rep', 'Junta militar'], inter: ['gray', 'Interino'], ref: ['int', 'Referendo'],
};
const chip = (k, txt) => (CHIPS[k] ? `<span class="chip ${CHIPS[k][0]}">${txt || CHIPS[k][1]}</span>` : `<span class="chip ${k}">${txt}</span>`);

const sec = (title, kind, html, extra = '') => `<div class="sec k-${kind} ${extra}"><h3>${title}</h3>${html}</div>`;
const ul = (items, kind = '', cls = '') => `<ul class="l ${kind ? 'k-' + kind : ''} ${cls}">${items.map((i) => `<li>${i}</li>`).join('')}</ul>`;
const call = (kind, hd, html) => `<div class="call ${kind}"><b class="hd">${hd}</b>${html}</div>`;
const med = (rows) => `<div class="med">${rows.map(([k, kind, txt]) => `<div class="c lb ${kind}">${k}</div><div class="c tx">${txt}</div>`).join('')}</div>`;
const rev = (items, title = 'Revisão ativa') => `<div class="rev"><div class="hd">${title}</div>${items.map(([q, a]) => `<div class="q"><b>${q}</b></div><div class="a">${a}</div>`).join('')}</div>`;

// ---------- linha do tempo ----------
// start/end: {d, t, k}; events: [{d, t, k, pos}]
function tl({ start, end, events }) {
  const items = [{ ...start, role: 'start', k: start.k || 'soc' }, ...events, { ...end, role: 'end', k: end.k || 'cris' }];
  const N = items.length;
  let h = `<div class="tl" style="grid-template-columns:repeat(${N},1fr)"><div class="axis"></div>`;
  items.forEach((it, i) => {
    const pos = it.pos || (i % 2 === 0 ? 'up' : 'dn');
    const col = i + 1;
    const cls = i === 0 ? 'first' : i === N - 1 ? 'last' : '';
    h += `<div class="dot k-c-${it.k} ${it.role || ''}" style="grid-column:${col}"></div>`;
    h += `<div class="lab ${pos} ${cls} k-c-${it.k}" style="grid-column:${col}"><div class="box"><b>${it.d}</b>${it.t}</div></div>`;
  });
  return h + '</div>';
}

// ---------- linha do tempo vertical (colunas estreitas) ----------
function vtl({ start, end, events }) {
  const row = (it, cls) => `<div class="vi ${cls || ''} k-c-${it.k}"><b>${it.d}</b> ${it.t}</div>`;
  return `<div class="vtl">${row({ ...start, k: start.k || 'soc' }, 'start')}${events.map((e) => row(e)).join('')}${row({ ...end, k: end.k || 'cris' }, 'end')}</div>`;
}

// ---------- fluxograma ----------
const TAG = { causa: 'Causa', fato: 'Acontecimento', cons: 'Consequência' };
function flow(steps, opts = {}) {
  const parts = steps.map((s) => `<div class="st ${s.t} k-c-${s.k || 'inst'}" style="--c:var(--${s.k || 'inst'})"><span class="tag">${TAG[s.t]}</span>${s.h ? `<b>${s.h}${s.p ? ':' : ''}</b> ` : ''}${s.p || ''}</div>`);
  return `<div class="flow ${opts.h ? 'h' : ''}">${parts.join('<div class="ar"></div>')}</div>`;
}
const flowLegend = () => '<div class="legend"><span><i class="d"></i>causa</span><span><i></i>acontecimento</span><span><i class="t"></i>consequência</span></div>';

// ---------- mapa de sucessão ----------
function succ({ title = 'Mapa da sucessão', nodes, steps, one = false, tag }) {
  let chain = '';
  nodes.forEach((n, i) => {
    chain += `<div class="pn ${n.c || ''}"><b>${n.n}</b><span>${n.s || ''}</span></div>`;
    if (i < nodes.length - 1) chain += `<div class="link"><span class="n">${i + 1}</span></div>`;
  });
  const li = steps.map(([k, txt], i) => `<li><span class="n">${i + 1}</span><div>${chip(k)} ${txt}</div></li>`).join('');
  return `<div class="succ ${one ? 'one' : ''}"><div class="hd"><span>${title}</span><span>${tag || ''}</span></div><div class="chain">${chain}</div><ol>${li}</ol></div>`;
}

// ---------- fotos ----------
function findImg(slug) {
  for (const ext of ['jpg', 'jpeg', 'png', 'webp']) {
    if (fs.existsSync(path.join(ASSETS, `${slug}.${ext}`))) return `${slug}.${ext}`;
  }
  return null;
}
const SIL = `<svg class="sil" viewBox="0 0 100 125" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34557f"/><stop offset="1" stop-color="#27456b"/></linearGradient></defs><rect width="100" height="125" fill="url(#sg)"/><circle cx="50" cy="46" r="19" fill="#5f7ea6"/><path d="M12 125 C12 92 30 78 50 78 C70 78 88 92 88 125 Z" fill="#5f7ea6"/></svg>`;

// retrato dentro do cabeçalho de governo
function portrait(slug) {
  const f = slug && findImg(slug);
  if (!f) return SIL;
  USED_IMAGES.add(slug);
  const c = CREDITS[slug];
  return `<img src="../assets/img/${f}" alt="${c ? c.desc : slug}"/>${c ? `<span style="position:absolute;left:.8mm;bottom:.5mm;right:.8mm;font-size:4.6pt;line-height:1.1;color:#fff;text-shadow:0 0 .8mm #000,0 0 .8mm #000">${c.curto}</span>` : ''}`;
}

// foto de evento (retorna '' se não houver arquivo) — h em mm
function photo(slug, { h = 40, cap = '' } = {}) {
  const f = findImg(slug);
  if (!f) return '';
  USED_IMAGES.add(slug);
  const c = CREDITS[slug] || {};
  return `<div class="figwrap"><div class="fig" style="height:${h}mm"><img src="../assets/img/${f}" alt="${c.desc || cap}"/></div><div class="figcap">${cap}</div><div class="figcr">${c.curto ? 'Foto: ' + c.curto : ''}</div></div>`;
}

// ---------- cabeçalho de governo ----------
function gov({ kick = 'Governo', nome, anos, sub = '', foto, compact = false, c4 = false, c1 = false, ficha }) {
  const f = ficha;
  const head = compact
    ? `<div class="gov-h compact ${c1 ? 'stack' : ''}"><div class="txt"><div><div class="kick">${kick}</div><h2>${nome}</h2></div><div class="yrs">${anos}<span>${sub}</span></div></div></div>`
    : `<div class="gov-h"><div class="ph-slot">${portrait(foto)}</div><div class="txt"><div class="kick">${kick}</div><h2>${nome}</h2><div class="yrs">${anos}<span>${sub}</span></div></div></div>`;
  const cell = (cls, lb, txt) => (txt ? `<div class="f ${cls}"><b class="lb">${lb}</b>${txt}</div>` : '');
  const fich = `<div class="ficha ${c4 ? 'c4' : ''} ${c1 ? 'c1' : ''}">
    ${cell('', '1 · Como chegou ao poder', f.chegada)}
    ${cell('ctx', '2 · Situação encontrada', f.contexto)}
    ${cell('fmed', '3 · Medidas', f.medidas)}
    ${cell('cri', '4 · Crises e oposição', f.crises)}
    ${cell('end', '6 · Como terminou', f.termino)}
    ${cell('end', '7 · Sucessão', f.sucessao)}</div>`;
  return `<div class="gov">${head}${fich}</div>`;
}

// ---------- gráficos ----------
const fmtN = (v, d = 1) => String(Number(v).toFixed(d)).replace('.', ',');

function chartFrame(w, h, pad, ymin, ymax, ticks, ylab) {
  const yy = (v) => pad.t + (1 - (v - ymin) / (ymax - ymin)) * (h - pad.t - pad.b);
  let s = '';
  ticks.forEach((t) => {
    s += `<line x1="${pad.l}" x2="${w - pad.r}" y1="${yy(t)}" y2="${yy(t)}" stroke="${t === 0 ? '#8a95a5' : '#e3e8ee'}" stroke-width="${t === 0 ? 0.35 : 0.22}"/>`;
    s += `<text x="${pad.l - 1.2}" y="${yy(t) + 0.75}" text-anchor="end" font-size="2.1" fill="#586373">${t}${ylab}</text>`;
  });
  return { s, yy };
}

function barChart({ w = 180, h = 58, keys, vals, color = '#0b7a8a', colors = {}, ymin = 0, ymax, ticks, bands = [], labelEvery = 1, show = [], ylab = '', dec = 1, pad = { l: 8, r: 2, t: 8, b: 6.5 } }) {
  const n = keys.length;
  const step = (w - pad.l - pad.r) / n;
  const { s: frame, yy } = chartFrame(w, h, pad, ymin, ymax, ticks, ylab);
  let svg = `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">`;
  bands.forEach((b) => {
    const i0 = keys.indexOf(b.from), i1 = keys.indexOf(b.to);
    if (i0 < 0 || i1 < 0) return;
    const x0 = pad.l + i0 * step, x1 = pad.l + (i1 + 1) * step;
    svg += `<rect x="${x0}" y="${pad.t - 5.2}" width="${x1 - x0}" height="${h - pad.t - pad.b + 5.2}" fill="${b.color}" opacity=".13"/>`;
    svg += `<rect x="${x0}" y="${pad.t - 5.2}" width="${x1 - x0}" height=".7" fill="${b.color}"/>`;
    svg += `<text x="${(x0 + x1) / 2}" y="${pad.t - 1.6}" text-anchor="middle" font-size="2" font-weight="700" fill="${b.color}">${b.label}</text>`;
  });
  svg += frame;
  keys.forEach((k, i) => {
    const v = vals[i];
    const x = pad.l + i * step + step * 0.16;
    const bw = step * 0.68;
    const y0 = yy(0), y1 = yy(Math.min(v, ymax));
    const top = Math.min(y0, y1), hh = Math.abs(y0 - y1);
    svg += `<rect x="${x}" y="${top}" width="${bw}" height="${Math.max(hh, 0.2)}" fill="${colors[k] || color}" rx=".25"/>`;
    if (show.includes(k)) {
      const ty = v >= 0 ? top - 0.9 : top + hh + 2.3;
      svg += `<text x="${x + bw / 2}" y="${ty}" text-anchor="middle" font-size="2.05" font-weight="700" fill="#1b2430">${fmtN(v, dec)}</text>`;
    }
    if (i % labelEvery === 0) svg += `<text x="${x + bw / 2}" y="${h - pad.b + 3}" text-anchor="middle" font-size="2" fill="#586373">${String(k).length === 4 ? "'" + String(k).slice(2) : k}</text>`;
  });
  return svg + '</svg>';
}

function lineChart({ w = 90, h = 50, keys, vals, color = '#b3261e', ymin = 0, ymax, ticks, bands = [], show = [], ylab = '', dec = 1, pad = { l: 8, r: 3, t: 8, b: 6.5 }, labelEvery = 2 }) {
  const n = keys.length;
  const xs = (i) => pad.l + (i + 0.5) * ((w - pad.l - pad.r) / n);
  const { s: frame, yy } = chartFrame(w, h, pad, ymin, ymax, ticks, ylab);
  let svg = `<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">`;
  bands.forEach((b) => {
    const i0 = keys.indexOf(b.from), i1 = keys.indexOf(b.to);
    if (i0 < 0 || i1 < 0) return;
    const x0 = xs(i0) - (xs(1) - xs(0)) / 2, x1 = xs(i1) + (xs(1) - xs(0)) / 2;
    svg += `<rect x="${x0}" y="${pad.t - 5.2}" width="${x1 - x0}" height="${h - pad.t - pad.b + 5.2}" fill="${b.color}" opacity=".13"/><rect x="${x0}" y="${pad.t - 5.2}" width="${x1 - x0}" height=".7" fill="${b.color}"/>`;
    svg += `<text x="${(x0 + x1) / 2}" y="${pad.t - 1.6}" text-anchor="middle" font-size="2" font-weight="700" fill="${b.color}">${b.label}</text>`;
  });
  svg += frame;
  const pts = keys.map((k, i) => `${xs(i)},${yy(vals[i])}`);
  svg += `<polygon points="${xs(0)},${yy(0)} ${pts.join(' ')} ${xs(n - 1)},${yy(0)}" fill="${color}" opacity=".12"/>`;
  svg += `<polyline points="${pts.join(' ')}" fill="none" stroke="${color}" stroke-width=".7" stroke-linejoin="round"/>`;
  keys.forEach((k, i) => {
    if (show.includes(k)) {
      svg += `<circle cx="${xs(i)}" cy="${yy(vals[i])}" r=".9" fill="${color}" stroke="#fff" stroke-width=".3"/>`;
      svg += `<text x="${xs(i)}" y="${yy(vals[i]) - 1.7}" text-anchor="${i === n - 1 ? 'end' : 'middle'}" font-size="2.1" font-weight="700" fill="#1b2430">${fmtN(vals[i], dec)}</text>`;
    }
    if (i % labelEvery === 0) svg += `<text x="${xs(i)}" y="${h - pad.b + 3}" text-anchor="middle" font-size="2" fill="#586373">${String(k).length === 4 ? "'" + String(k).slice(2) : k}</text>`;
  });
  return svg + '</svg>';
}

// barras horizontais em HTML (resultados eleitorais)
function hbars(items, { color = 'var(--inst)', max = 60 } = {}) {
  return items.map(([lab, v, c, txt]) => `<div class="hb"><span class="lb">${lab}</span><span class="tr"><span class="bar" style="width:${(v / max) * 100}%;background:${c || color}"></span></span><b>${txt !== undefined ? txt : fmtN(v, 1) + '%'}</b></div>`).join('');
}

const chart = (title, sub, svg, extra = '') => `<div class="chart"><div class="ct">${title}</div><div class="cs">${sub}</div>${svg}${extra}</div>`;

module.exports = { page, chip, sec, ul, call, med, rev, tl, vtl, flow, flowLegend, succ, gov, photo, portrait, barChart, lineChart, hbars, chart, fmtN, USED_IMAGES, CREDITS, PERIODOS };
