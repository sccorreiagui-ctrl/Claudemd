// Gera build/apostila.html e o PDF final; faz auditoria automática de layout.
import fs from 'fs'; import path from 'path'; import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const src = path.join(root, 'src'), out = path.join(root, 'build');
const pdfOut = process.argv[2] || path.join(out, 'apostila.pdf');

const css = fs.readFileSync(path.join(src, 'style.css'), 'utf8');
const files = fs.readdirSync(path.join(src, 'pages')).filter(f => f.endsWith('.html')).sort();
const colors = { az:'#1f78c8', ve:'#2f9e5a', ro:'#7b43b8', la:'#f2691b', vm:'#d83a3a', rs:'#d4287c', am:'#d19a00', sl:'#475a73', k:'#1b2236', g:'#7b8499', mr:'#8a5a2b', v2:'#8c1f35', w:'#ffffff' };
let defs = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>';
for (const [n, c] of Object.entries(colors))
  defs += `<marker id="ar-${n}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0.8 L9,5 L0,9.2 Z" fill="${c}"/></marker>`;
defs += '</defs></svg>';

const modNames = { eco:'Ecologia e impactos ambientais', cit:'Citologia e membrana', met:'Bioquímica e metabolismo', gen:'Genética e biotecnologia', fis:'Fisiologia humana', imu:'Imunologia e doenças', evo:'Evolução e complementos', bot:'Fotossíntese e botânica', gui:'Guia de estudo', cap:'', fim:'Revisão e referências' };
let pagesHtml = '';
const meta = [];
files.forEach((f, i) => {
  let h = fs.readFileSync(path.join(src, 'pages', f), 'utf8');
  h = h.replace(/\{\{svg:([\w-]+)\}\}/g, (_, n) => fs.readFileSync(path.join(src, 'svg', n + '.svg'), 'utf8'));
  const n = i + 1;
  const m = /class="page m-(\w+)"/.exec(h); const mod = m ? m[1] : 'eco';
  const om = /data-origin="(\w)"/.exec(h); const org = om ? om[1] : 'm';
  const orgTxt = { v:'Base: inventário da videoaula (auditado)', m:'Base: inventário da videoaula + complementos', c:'Complemento ENEM (fora do inventário da videoaula)' }[org];
  const hf = `<div class="ph"><span><span class="dot"></span><b>${modNames[mod] || ''}</b></span><span>Apostila Visual · Biologia ENEM 2026</span></div><div class="pf"><span>${orgTxt}</span><span class="pn">${n}</span></div>`;
  h = h.replace('<!--HF-->', f.startsWith('p01') ? '' : hf);
  pagesHtml += h + '\n'; meta.push(f);
});
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Apostila Visual de Biologia para o ENEM 2026</title><style>${css}</style></head><body>${defs}${pagesHtml}</body></html>`;
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'apostila.html'), html);

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + path.join(out, 'apostila.html'));
await page.evaluate(() => document.fonts.ready);
const report = await page.evaluate(() => {
  const res = [];
  document.querySelectorAll('.page').forEach((pg, idx) => {
    const r = { page: idx + 1, issues: [] };
    const pb = pg.querySelector('.pb');
    if (pb) {
      const over = pb.scrollHeight - pb.clientHeight;
      if (over > 1) r.issues.push(`OVERFLOW vertical ${over}px`);
      if (pb.scrollWidth - pb.clientWidth > 1) r.issues.push(`OVERFLOW horizontal ${pb.scrollWidth - pb.clientWidth}px`);
      const kids = [...pb.children]; const last = kids[kids.length - 1];
      const pbR = pb.getBoundingClientRect();
      let maxB = 0; kids.forEach(k => { maxB = Math.max(maxB, k.getBoundingClientRect().bottom); });
      r.free = Math.round(pbR.bottom - maxB);
      // elementos filhos flex que estourem
      pb.querySelectorAll('.bx,.fig,table').forEach(el => {
        const b = el.getBoundingClientRect();
        if (b.bottom > pbR.bottom + 1 || b.right > pbR.right + 1) r.issues.push(`elemento fora da area: ${el.className || el.tagName} (${Math.round(b.bottom - pbR.bottom)}px)`);
        if (el.scrollHeight - el.clientHeight > 2 && getComputedStyle(el).overflow !== 'visible') r.issues.push(`conteudo cortado em ${el.className}`);
      });
    }
    pg.querySelectorAll('svg').forEach((svg, si) => {
      const vb = svg.viewBox && svg.viewBox.baseVal; if (!vb || !vb.width) return;
      const sr = svg.getBoundingClientRect(); if (sr.width < 5) return;
      const texts = [...svg.querySelectorAll('text')];
      const boxes = texts.map(t => ({ t, b: t.getBoundingClientRect() })).filter(o => o.b.width > 0);
      boxes.forEach(({ t, b }) => {
        if (b.left < sr.left - 1 || b.right > sr.right + 1 || b.top < sr.top - 1 || b.bottom > sr.bottom + 1)
          r.issues.push(`svg#${si} texto fora do viewBox: "${t.textContent.trim().slice(0, 30)}"`);
      });
      for (let a = 0; a < boxes.length; a++) for (let c = a + 1; c < boxes.length; c++) {
        const A = boxes[a].b, B = boxes[c].b;
        const ix = Math.min(A.right, B.right) - Math.max(A.left, B.left), iy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
        if (ix > 1.5 && iy > 2) {
          const inter = ix * iy, sm = Math.min(A.width * A.height, B.width * B.height);
          if (inter / sm > 0.12) r.issues.push(`svg#${si} textos sobrepostos: "${boxes[a].t.textContent.trim().slice(0, 22)}" x "${boxes[c].t.textContent.trim().slice(0, 22)}"`);
        }
      }
      // fonte efetiva muito pequena (<5.2pt)
      const scale = sr.width / vb.width;
      texts.forEach(t => { const fs = parseFloat(getComputedStyle(t).fontSize) * scale * 0.75; if (fs < 5.9 && t.textContent.trim()) r.issues.push(`fonte pequena ${fs.toFixed(1)}pt: "${t.textContent.trim().slice(0, 25)}"`); });
    });
    res.push(r);
  });
  return res;
});
await page.pdf({ path: pdfOut, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();
let bad = 0;
for (const r of report) {
  const flag = r.issues.length ? '!!' : 'ok';
  console.log(`p${String(r.page).padStart(2, '0')} ${meta[r.page - 1].padEnd(34)} livre=${String(r.free).padStart(4)}px ${flag}`);
  [...new Set(r.issues)].slice(0, 12).forEach(s => console.log('      - ' + s));
  if (r.issues.length) bad++;
}
console.log(`paginas: ${report.length}; com alertas: ${bad}; pdf: ${pdfOut}`);
