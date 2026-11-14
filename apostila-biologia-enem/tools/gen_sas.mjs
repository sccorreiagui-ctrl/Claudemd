import fs from 'fs';
const rows=[['Desequilíbrio ecossistêmico',64,'11,6','ve','p.7–10'],['Viroses',23,'4,2','vm','p.33'],['DNA e função dos genes',22,'4,0','ro','p.19–20'],['Bioquímica',18,'3,3','la','p.15–18'],['Biologia celular',18,'3,3','az','p.11–14'],['Ciclos biogeoquímicos',17,'3,1','ve','p.6'],['Relações ecológicas',16,'2,9','ve','p.5'],['Cadeias e teias alimentares',15,'2,7','ve','p.3–4'],['Protozooses',13,'2,4','vm','p.34'],['Bacterioses',12,'2,2','vm','p.33'],['Relações interespecíficas',12,'2,2','ve','p.5'],['Saúde',12,'2,2','sl','p.35']];
let o='',y=4;const x0=150,sc=1.9;
for(const [n,v,p,c,pg] of rows){o+=`<text x="0" y="${y+14}" class="t10 b">${n}</text><rect x="${x0}" y="${y}" width="${(v*sc).toFixed(0)}" height="19" rx="3" class="f-${c}"/><text x="${x0+v*sc+6}" y="${y+14}" class="t10 b">${v} · ${p}%</text><text x="400" y="${y+14}" class="t9 g e">${pg}</text>`;y+=27;}
o+=`<text x="0" y="${y+14}" class="t9 g">12 categorias = 242 itens (≈ 44% de 551).</text>`;
fs.writeFileSync('src/svg/sas.svg',`<svg viewBox="0 0 405 ${Math.round(y+16)}" preserveAspectRatio="xMidYMin meet">${o}</svg>`);
