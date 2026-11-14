o=''
# ---- órgãos ----
o+='<ellipse cx="345" cy="24" rx="28" ry="13" fill="#f3b6b6" stroke="#b34747" stroke-width="1.6"/><path d="M325 24 H365" stroke="#b34747" stroke-width="1.4"/>'
o+='<ellipse cx="300" cy="36" rx="9" ry="6" fill="#f6d28f" stroke="#a8742d"/><ellipse cx="390" cy="36" rx="9" ry="6" fill="#f6d28f" stroke="#a8742d"/>'
o+='<rect x="340" y="38" width="10" height="86" rx="5" fill="#e6a38a" stroke="#a8603f"/>'
o+='<path d="M338 124 C326 132 322 162 336 188 C354 218 412 214 422 184 C428 166 410 156 398 156 C388 156 380 162 374 152 C368 140 362 128 352 124 Z" fill="#f4a58a" stroke="#b5503a" stroke-width="1.8"/>'
o+='<path d="M222 134 C244 114 322 112 340 126 L336 176 C298 198 248 190 222 162 Z" fill="#a9503a" stroke="#6e2c1e" stroke-width="1.8" opacity=".92"/>'
o+='<ellipse cx="316" cy="192" rx="8" ry="15" fill="#5aa36f" stroke="#2f6e44" stroke-width="1.4"/><path d="M320 178 C324 190 326 200 330 208" class="nf s-ve sw2"/>'
o+='<path d="M328 216 C360 202 410 196 448 204 L446 218 C410 216 368 226 330 228 Z" fill="#e8c46a" stroke="#a8842d" stroke-width="1.6"/>'
o+='<path d="M344 206 C324 208 316 226 330 240" fill="none" stroke="#d9a57b" stroke-width="10" stroke-linecap="round"/>'
pts=[(330,240),(392,248),(300,260),(392,272),(300,284),(392,296),(300,308),(384,320)]
o+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#e3b98d" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
o+='<path d="M276 330 V234 H414 V324 C414 348 384 352 362 362 V388" fill="none" stroke="#9b6a4a" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
o+='<ellipse cx="268" cy="338" rx="4" ry="9" fill="#9b6a4a"/>'
# ---- rótulos ----
def lab(x,y,w,title,col,lines,anchor_x,anchor_y,side):
    s=f'<rect x="{x}" y="{y-12}" width="{w}" height="{14+11*len(lines)+4}" rx="5" fill="#fff" stroke="{col}" stroke-width="1.2"/>'
    s+=f'<text x="{x+6}" y="{y}" class="t9 xb" style="fill:{col}">{title}</text>'
    for i,l in enumerate(lines): s+=f'<text x="{x+6}" y="{y+12+i*11}" class="t8">{l}</text>'
    ex=x+w if side=='L' else x
    s+=f'<path d="M{ex} {y+6} L{anchor_x} {anchor_y}" class="nf s-g sw1"/><circle cx="{anchor_x}" cy="{anchor_y}" r="2.6" fill="{col}"/>'
    return s
o+=lab(0,22,206,'BOCA e glândulas salivares','#b34747',['mastigação (digestão mecânica)','amilase salivar (pitialina):','amido → maltose · pH ≈ 6,5–7'],318,24,'L')
o+=lab(0,118,206,'FÍGADO','#6e2c1e',['produz bile (SEM enzimas):','sais biliares emulsificam lipídios','metaboliza nutrientes, detoxifica'],250,148,'L')
o+=lab(0,198,206,'VESÍCULA BILIAR','#2f6e44',['armazena a bile e a libera no','duodeno (estímulo: colecistocinina)'],310,194,'L')
o+=lab(0,292,206,'INTESTINO GROSSO','#7a4f2f',['absorve água e sais; flora bacteriana','(vitamina K); forma as fezes','não digere nutrientes principais'],270,300,'L')
o+=lab(484,66,206,'ESÔFAGO','#a8603f',['peristaltismo: contrações','involuntárias; não digere'],350,80,'R')
o+=lab(484,122,206,'ESTÔMAGO','#b5503a',['HCl (células parietais; pH ≈ 2)','pepsinogênio → pepsina:','proteínas → peptídeos · quimo'],412,176,'R')
o+=lab(484,208,206,'PÂNCREAS (exócrino)','#a8842d',['suco pancreático: HCO₃⁻ (pH ≈ 8),','amilase, tripsina, quimotripsina,','lipase, nucleases'],440,210,'R')
o+=lab(484,290,206,'INTESTINO DELGADO','#a8742d',['suco entérico: maltase, sacarase,','lactase, peptidases · quilo','absorção: vilosidades e','microvilosidades'],396,284,'R')
open('src/svg/digestorio.svg','w').write(f'<svg viewBox="0 0 690 400">{o}</svg>')
# ---- emulsificação ----
import math
o=''
o+='<text x="0" y="12" class="t9 xb tx-am">Bile (tensoativo) + lipase</text>'
o+='<circle cx="44" cy="70" r="34" class="l-am s-am sw2"/><text x="44" y="74" class="t9 c xb tx-am">gordura</text><text x="44" y="118" class="t8 c g">gota grande:</text><text x="44" y="128" class="t8 c g">pouca superfície</text>'
o+='<path d="M84 70 H108" class="nf s-k sw2" marker-end="url(#ar-k)"/><text x="96" y="62" class="t8 c b tx-ve">bile</text>'
for (cx,cy) in [(138,50),(164,60),(146,82),(174,88),(136,106),(166,112)]:
    o+=f'<circle cx="{cx}" cy="{cy}" r="8" class="l-am s-am sw1"/>'
    for k in range(8):
        a_=2*math.pi*k/8; o+=f'<line x1="{cx+8*math.cos(a_):.1f}" y1="{cy+8*math.sin(a_):.1f}" x2="{cx+12*math.cos(a_):.1f}" y2="{cy+12*math.sin(a_):.1f}" stroke="#1f78c8" stroke-width="2"/>'
o+='<text x="152" y="130" class="t8 c g">gotículas: ↑ superfície</text>'
o+='<path d="M194 80 H218" class="nf s-k sw2" marker-end="url(#ar-k)"/><text x="206" y="72" class="t8 c b tx-la">lipase</text>'
o+='<text x="224" y="74" class="t8 b">ácidos graxos</text><text x="224" y="86" class="t8 b">+ glicerol</text><text x="224" y="98" class="t8 g">(absorvidos)</text>'
o+='<circle cx="10" cy="146" r="5" class="f-az"/><path d="M10 151 V160" stroke="#d19a00" stroke-width="2.4"/><text x="22" y="152" class="t8">sal biliar: cabeça polar (azul) + cauda apolar (âmbar)</text>'
open('src/svg/emulsif.svg','w').write(f'<svg viewBox="0 0 335 164">{o}</svg>')
print('ok')
