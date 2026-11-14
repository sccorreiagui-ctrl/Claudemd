# ---- cladograma de plantas
o=''
o+='<path d="M16 138 H640" class="nf s-ve sw4 rc"/>'
terms=[(190,'Briófitas','musgos',['sem vasos','gametófito dominante','água na fecundação']),(316,'Pteridófitas','samambaias',['com vasos','esporófito dominante','sem sementes']),(442,'Gimnospermas','pinheiros, araucária',['semente nua (pinhão)','cones; grão de pólen','sem flor e sem fruto']),(568,'Angiospermas','a maioria das plantas',['flor, fruto e semente','dupla fecundação','endosperma'])]
for x,n,ex,ls in terms:
    o+=f'<path d="M{x} 138 V84" class="nf s-ve sw3"/><circle cx="{x}" cy="78" r="7" class="f-ve"/>'
    o+=f'<text x="{x}" y="14" class="t10 c xb tx-ve">{n}</text><text x="{x}" y="25" class="t8 c g">{ex}</text>'
    for i,l in enumerate(ls): o+=f'<text x="{x}" y="{40+i*11}" class="t8 c" style="font-size:8px">{l}</text>'
inn=[(128,'embrião protegido','+ cutícula (terra firme)'),(253,'vasos condutores','xilema e floema; lignina'),(379,'semente','pólen: fecundação sem água'),(505,'flor e fruto','polinizadores; dispersão')]
for x,t1,t2 in inn:
    o+=f'<circle cx="{x}" cy="138" r="7" class="f-la"/><text x="{x}" y="141" class="t8 c b w">★</text><text x="{x}" y="158" class="t8 c xb tx-la">{t1}</text><text x="{x}" y="169" class="t8 c g" style="font-size:7.6px">{t2}</text>'
o+='<text x="4" y="128" class="t8 b tx-ve">algas verdes</text><text x="4" y="119" class="t7 g" style="display:none"></text>'
o+='<text x="4" y="182" class="t8 g">★ = inovação evolutiva (conquista do ambiente terrestre)</text>'
open('src/svg/cladoveg.svg','w').write(f'<svg viewBox="0 0 690 190">{o}</svg>')
# ---- planta e transporte
o=''
o+='<rect x="0" y="176" width="335" height="120" fill="#efe3d3"/><text x="8" y="290" class="t8 b tx-mr">solo</text>'
o+='<path d="M168 176 V80" stroke="#2f9e5a" stroke-width="14" stroke-linecap="round"/>'
o+='<path d="M168 130 C150 120 120 110 96 92 M168 108 C190 98 218 92 240 76" stroke="#2f9e5a" stroke-width="7" fill="none" stroke-linecap="round"/>'
for (cx,cy,rot) in ((86,86,-30),(250,70,30),(168,66,0)): o+=f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="14" fill="#7cc89a" stroke="#2f9e5a" stroke-width="1.6" transform="rotate({rot} {cx} {cy})"/>'
for dx in (-40,-24,-8,10,26,40): o+=f'<path d="M168 176 C{168+dx*.4} 210 {168+dx*.8} 236 {168+dx} 262" stroke="#8a5a2b" stroke-width="2.4" fill="none"/>'
# xilema (azul) subindo: dentro do caule, lado esquerdo
o+='<path d="M163 262 V84" class="nf s-az sw3 dsh" marker-end="url(#ar-az)"/><path d="M163 130 L112 98" class="nf s-az sw2 dsh" marker-end="url(#ar-az)"/>'
o+='<path d="M173 84 V250" class="nf s-la sw3" marker-end="url(#ar-la)"/><path d="M110 92 C130 108 150 120 170 134" class="nf s-la sw2" style="display:none"/>'
# vapor
o+='<path d="M96 66 q-6 -10 0 -20 M110 62 q-6 -10 0 -20 M240 50 q-6 -10 0 -20 M254 50 q-6 -10 0 -20" class="nf s-az sw1 rc dt"/>'
o+='<text x="60" y="28" class="t8 b tx-az">H₂O (vapor): transpiração</text><text x="198" y="20" class="t8 b tx-az">CO₂ entra pelos estômatos</text>'
o+='<text x="2" y="150" class="t9 xb tx-az">XILEMA</text><text x="2" y="161" class="t8">seiva bruta (água + sais)</text><text x="2" y="171" class="t8 g">raiz → folhas</text>'
o+='<text x="200" y="196" class="t9 xb tx-la">FLOEMA</text><text x="200" y="207" class="t8">seiva elaborada (açúcares)</text><text x="200" y="217" class="t8 g">das folhas aos drenos</text>'
o+='<text x="168" y="284" class="t8 c b tx-mr">raiz: absorve água e sais</text>'
open('src/svg/planta.svg','w').write(f'<svg viewBox="0 0 335 300">{o}</svg>')
# ---- flor
o=''
o+='<path d="M120 230 V150" stroke="#2f9e5a" stroke-width="8"/>'
o+='<path d="M96 156 C70 120 80 70 120 56 C160 70 170 120 144 156 Z" fill="#fbdcec" stroke="#d4287c" stroke-width="2" opacity=".9"/>'
o+='<path d="M100 164 C84 150 70 130 62 112 C80 120 100 138 112 156Z M140 164 C156 150 170 130 178 112 C160 120 140 138 128 156Z" fill="#fbdcec" stroke="#d4287c" stroke-width="1.6"/>'
o+='<path d="M96 160 L84 176 L108 170Z M144 160 L156 176 L132 170Z" fill="#7cc89a" stroke="#2f9e5a"/>'
o+='<path d="M120 154 V86" stroke="#2f9e5a" stroke-width="5"/><ellipse cx="120" cy="78" rx="8" ry="5" fill="#d4287c"/><ellipse cx="120" cy="136" rx="14" ry="12" fill="#cde8d6" stroke="#2f9e5a" stroke-width="1.6"/><circle cx="116" cy="134" r="3" class="f-ve"/><circle cx="125" cy="138" r="3" class="f-ve"/>'
for dx in (-28,28): o+=f'<path d="M{120+dx*0.5} 154 L{120+dx} 96" stroke="#d19a00" stroke-width="3"/><ellipse cx="{120+dx}" cy="92" rx="6" ry="9" fill="#f2b21b" stroke="#a8742d"/>'
o+='<g class="t8"><text x="190" y="36" class="b tx-rs">Pétalas (corola):</text><text x="190" y="47" class="g">atraem polinizadores</text><text x="190" y="80" class="b tx-am">Estame: antera</text><text x="190" y="91" class="g">(pólen) + filete</text><text x="190" y="116" class="b tx-ve">Pistilo: estigma,</text><text x="190" y="127" class="g">estilo e ovário (óvulos)</text><text x="190" y="170" class="b tx-ve">Sépalas (cálice)</text></g>'
o+='<path d="M186 38 L152 70 M186 78 L152 92 M186 110 L130 82 M186 168 L150 174" class="nf s-g sw1"/>'
o+='<rect x="190" y="190" width="140" height="70" rx="8" class="l-ve"/><text x="198" y="204" class="t8 b tx-ve">Dupla fecundação</text><text x="198" y="215" class="t7">gameta 1 + oosfera → zigoto 2n</text><text x="198" y="225" class="t7">gameta 2 + 2 polares → endosp. 3n</text><text x="198" y="238" class="t7 g">ovário → fruto · óvulo → semente</text>'
open('src/svg/flor.svg','w').write(f'<svg viewBox="0 0 335 266">{o}</svg>')
# ---- fototropismo
o=''
o+='<circle cx="20" cy="40" r="14" class="f-am"/><path d="M38 44 L68 60" class="nf s-am sw3" marker-end="url(#ar-am)"/><text x="6" y="70" class="t8 b tx-am">luz lateral</text>'
o+='<path d="M120 160 V60" stroke="#2f9e5a" stroke-width="12" stroke-linecap="round"/><ellipse cx="120" cy="54" rx="20" ry="8" fill="#7cc89a" stroke="#2f9e5a"/>'
o+='<rect x="126" y="70" width="6" height="80" fill="#d4287c" opacity=".35"/><text x="140" y="96" class="t8 b tx-rs">↑ auxina no lado</text><text x="140" y="107" class="t8 b tx-rs">sombreado</text><text x="140" y="118" class="t8 b tx-rs">→ cresce mais</text>'
o+='<path d="M250 160 V110 C250 80 230 66 214 62" stroke="#2f9e5a" stroke-width="12" stroke-linecap="round" fill="none"/><ellipse cx="206" cy="60" rx="20" ry="8" fill="#7cc89a" stroke="#2f9e5a" transform="rotate(-20 206 60)"/>'
o+='<text x="250" y="178" class="t8 c b tx-ve">curvatura em direção à luz</text><text x="120" y="178" class="t8 c b">antes</text>'
o+='<path d="M154 126 H220" class="nf s-k sw2" marker-end="url(#ar-k)" style="display:none"/>'
o+='<text x="6" y="140" class="t8 g" style="display:none"></text>'
open('src/svg/foto.svg','w').write(f'<svg viewBox="0 0 335 188">{o}</svg>')
print('ok')
