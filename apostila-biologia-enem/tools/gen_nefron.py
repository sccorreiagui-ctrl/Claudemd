o=''
# fundo córtex / medula
o+='<rect x="0" y="0" width="480" height="140" rx="8" fill="#fbeedd"/><rect x="0" y="140" width="480" height="200" rx="8" fill="#f6d6c2"/>'
o+='<text x="8" y="14" class="t9 xb" style="fill:#a8603f">CÓRTEX RENAL</text><text x="8" y="330" class="t9 xb" style="fill:#8a4a2a">MEDULA RENAL (↑ osmolaridade para baixo)</text>'
# gradiente de osmolaridade
o+='<defs><linearGradient id="osm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6d6c2" stop-opacity="0"/><stop offset="1" stop-color="#c8896a" stop-opacity=".55"/></linearGradient></defs><rect x="0" y="140" width="480" height="200" rx="8" fill="url(#osm)"/>'
# capilares peritubulares
o+='<path d="M120 60 C150 70 160 90 150 120 M170 56 C200 76 210 110 200 134 M300 96 C320 110 324 132 316 150" class="nf s-v2 sw1 dt" style="display:none"/>'
# arteríolas
o+='<path d="M20 56 H60" stroke="#d83a3a" stroke-width="7" fill="none" stroke-linecap="round"/><text x="4" y="40" class="t8 b tx-vm">arteríola aferente</text>'
o+='<path d="M96 100 C96 118 70 130 30 130" stroke="#d83a3a" stroke-width="4" fill="none"/><text x="8" y="146" class="t8 b tx-vm">arteríola eferente</text>'
# glomérulo e cápsula
o+='<circle cx="82" cy="72" r="30" fill="#fff" stroke="#475a73" stroke-width="2.4"/><path d="M62 70 q8 -14 16 0 t14 0 t10 6 M66 82 q8 -12 14 0 t12 -2" stroke="#d83a3a" stroke-width="3" fill="none"/>'
o+='<text x="82" y="116" class="t8 c b" style="fill:#2c3b50">corpúsculo renal</text><text x="82" y="126" class="t8 c" style="fill:#5a6479">(glomérulo + cápsula)</text>'
# TCP
o+='<path d="M112 72 C130 56 150 56 156 72 C162 88 144 96 134 84 C124 72 148 66 168 80 C188 94 196 70 214 66" fill="none" stroke="#1f78c8" stroke-width="9" stroke-linecap="round"/>'
o+='<text x="196" y="40" class="t9 c xb tx-az">túbulo contorcido</text><text x="196" y="51" class="t9 c xb tx-az">proximal</text>'
# alça de Henle
o+='<path d="M222 70 H246 V250 C246 276 280 276 280 250 V92" fill="none" stroke="#475a73" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
o+='<path d="M246 92 V250 C246 276 280 276 280 250" fill="none" stroke="#98a2b6" stroke-width="3" style="display:none"/>'
o+='<text x="226" y="296" class="t9 c xb" style="fill:#2c3b50">alça de Henle</text>'
# TCD
o+='<path d="M280 92 C290 80 306 80 312 94 C318 108 300 112 296 100 C292 88 324 84 346 92 C362 98 372 84 392 82" fill="none" stroke="#2f9e5a" stroke-width="9" stroke-linecap="round"/>'
o+='<text x="340" y="134" class="t9 c xb tx-ve">túbulo contorcido</text><text x="340" y="145" class="t9 c xb tx-ve">distal</text>'
# ducto coletor
o+='<path d="M404 82 H420 V300" fill="none" stroke="#d19a00" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
o+='<text x="436" y="190" class="t9 xb tx-am">ducto</text><text x="436" y="201" class="t9 xb tx-am">coletor</text><path d="M420 304 V328" class="nf s-am sw3" marker-end="url(#ar-am)"/><text x="428" y="326" class="t8 b tx-am">urina → pelve renal</text>'
# setas F R S
o+='<path d="M60 58 H50" stroke="#1f78c8" stroke-width="3" style="display:none"/>'
def badge(x,y,t,c): return f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/><text x="{x}" y="{y+3.5}" class="t10 c b w">{t}</text>'
o+=badge(116,46,'F','#1f78c8')+'<path d="M82 50 V56" class="nf s-az sw2" style="display:none"/>'
o+='<path d="M140 100 L128 140" class="nf s-ve sw2" marker-end="url(#ar-ve)" style="display:none"/>'
o+=badge(176,98,'R','#2f9e5a')+badge(262,170,'R','#2f9e5a')+badge(304,70,'S','#d83a3a')+badge(328,70,'R','#2f9e5a')+badge(446,150,'R','#2f9e5a')
# setas reabsorção
o+='<path d="M170 92 L176 112" class="nf s-ve sw2" marker-end="url(#ar-ve)" style="display:none"/>'
# legenda direita
o+='<g transform="translate(496 0)">'
items=[('F','#1f78c8','FILTRAÇÃO','no glomérulo: pressão empurra água, íons, glicose, ureia e aminoácidos para a cápsula. Células e proteínas grandes ficam no sangue.'),
('R','#2f9e5a','REABSORÇÃO','TCP: ~100% da glicose e aminoácidos, grande parte da água e do Na⁺. Alça: concentra a medula. Coletor: água sob ADH.'),
('S','#d83a3a','SECREÇÃO','TCD: H⁺, K⁺, amônio e alguns fármacos passam do sangue ao túbulo.')]
y=14
for l,c,t,tx in items:
    o+=f'<circle cx="10" cy="{y}" r="9" fill="{c}"/><text x="10" y="{y+3.5}" class="t10 c b w">{l}</text><text x="26" y="{y+4}" class="t10 xb" style="fill:{c}">{t}</text>'
    words=tx.split(' ');cur='';ln=[]
    for w in words:
        if len(cur)+len(w)+1>34: ln.append(cur);cur=w
        else: cur=(cur+' '+w).strip()
    ln.append(cur)
    for i,l2 in enumerate(ln): o+=f'<text x="0" y="{y+20+i*10.5}" class="t8">{l2}</text>'
    y+=26+len(ln)*10.5+10
o+=f'<rect x="0" y="{y}" width="190" height="66" rx="6" class="l-sl"/><text x="8" y="{y+14}" class="t8 xb tx-sl">Urina = filtração − reabsorção + secreção</text><text x="8" y="{y+28}" class="t8">Sem ADH: urina volumosa e diluída.</text><text x="8" y="{y+39}" class="t8">Com ADH: reabsorve água → pouca</text><text x="8" y="{y+50}" class="t8">urina, concentrada.</text>'
o+='</g>'
open('src/svg/nefron.svg','w').write(f'<svg viewBox="0 0 690 342">{o}</svg>')
print('ok')
