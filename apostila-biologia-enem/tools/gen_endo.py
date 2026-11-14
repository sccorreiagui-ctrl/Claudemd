# ---- eixo tireoide ----
o=''
def bx(x,y,w,h,t1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="l-rs s-rs sw12"/><text x="{x+w/2}" y="{y+h/2+4}" class="t10 c xb tx-rs">{t1}</text>'
o+=bx(20,6,120,32,'Hipotálamo')+bx(20,70,120,32,'Adeno-hipófise')+bx(20,134,120,32,'Tireoide')
o+='<path d="M80 38 V68" class="nf s-rs sw3" marker-end="url(#ar-rs)"/><text x="88" y="58" class="t8 b tx-rs">TRH</text>'
o+='<path d="M80 102 V132" class="nf s-rs sw3" marker-end="url(#ar-rs)"/><text x="88" y="122" class="t8 b tx-rs">TSH</text>'
o+='<path d="M140 150 H196 V22 H144" class="nf s-vm sw2 dsh" marker-end="url(#ar-vm)"/><path d="M196 86 H144" class="nf s-vm sw2 dsh" marker-end="url(#ar-vm)"/>'
o+='<text x="206" y="60" class="t9 b tx-vm">T₃ e T₄ ↑</text><text x="206" y="72" class="t8">inibem (−) o</text><text x="206" y="82" class="t8">hipotálamo e</text><text x="206" y="92" class="t8">a hipófise</text>'
o+='<text x="206" y="130" class="t8 g">T₃/T₄ (iodo):</text><text x="206" y="140" class="t8 g">metabolismo basal</text><text x="80" y="184" class="t8 c b">retroalimentação negativa</text>'
open('src/svg/tireoide.svg','w').write(f'<svg viewBox="0 0 335 192">{o}</svg>')
# ---- glicemia ----
o=''
o+='<rect x="108" y="84" width="120" height="28" rx="14" fill="#fff" stroke="#475a73" stroke-width="2"/><text x="168" y="103" class="t10 c xb">glicemia</text>'
o+='<rect x="6" y="6" width="122" height="34" rx="8" class="l-az s-az sw12"/><text x="67" y="20" class="t8 c xb tx-az">células β (pâncreas)</text><text x="67" y="33" class="t10 c xb tx-az">INSULINA</text>'
o+='<rect x="206" y="152" width="124" height="34" rx="8" class="l-vm s-vm sw12"/><text x="268" y="166" class="t8 c xb tx-vm">células α (pâncreas)</text><text x="268" y="179" class="t10 c xb tx-vm">GLUCAGON</text>'
o+='<path d="M140 82 C120 70 100 58 88 44" class="nf s-rs sw3" marker-end="url(#ar-rs)"/><text x="132" y="62" class="t8 b tx-vm" transform="translate(0 0)">↑ glicemia</text>'
o+='<path d="M40 42 C20 80 40 104 104 100" class="nf s-az sw3" marker-end="url(#ar-az)"/>'
o+='<path d="M196 114 C214 128 236 138 250 150" class="nf s-rs sw3" marker-end="url(#ar-rs)"/><text x="206" y="136" class="t8 b tx-az">↓ glicemia</text>'
o+='<path d="M326 150 C336 112 290 96 232 98" class="nf s-vm sw3" marker-end="url(#ar-vm)"/>'
o+='<text x="6" y="124" class="t8 b tx-az">Insulina: células captam</text><text x="6" y="135" class="t8">glicose; fígado faz glicogênio</text><text x="6" y="146" class="t8 b tx-az">→ ↓ glicemia</text>'
o+='<text x="190" y="14" class="t8 b tx-vm">Glucagon: glicogenólise e</text><text x="190" y="25" class="t8">gliconeogênese no fígado</text><text x="190" y="36" class="t8 b tx-vm">→ ↑ glicemia</text>'
open('src/svg/glicemia.svg','w').write(f'<svg viewBox="0 0 335 192">{o}</svg>')
# ---- ciclo menstrual ----
o=''
o+='<line x1="30" y1="14" x2="30" y2="130" class="nf s-k sw12" marker-end="url(#ar-k)"/><line x1="30" y1="130" x2="326" y2="130" class="nf s-k sw12" marker-end="url(#ar-k)"/>'
for d in (1,7,14,21,28): o+=f'<text x="{30+d*10}" y="142" class="t8 c g">{d}</text><line x1="{30+d*10}" y1="130" x2="{30+d*10}" y2="134" class="nf s-k sw1"/>'
o+='<text x="326" y="154" class="t8 g e">dias do ciclo</text>'
o+='<path d="M40 112 C100 108 150 100 170 94 C190 100 230 110 310 114" class="nf s-ve sw2 rc" style="display:none"/>'
# estrogênio
o+='<path d="M40 104 C80 90 120 36 160 30 C190 34 200 70 220 62 C240 54 250 60 270 90 C285 108 300 110 316 112" class="nf s-rs sw3 rc"/>'
o+='<path d="M40 124 C100 124 180 122 190 120 C220 60 240 30 250 28 C270 36 280 100 300 120" class="nf s-vm sw3 rc" style="display:none"/>'
# progesterona
o+='<path d="M40 124 C120 124 170 124 190 118 C215 80 235 40 252 40 C270 44 280 100 300 122" class="nf s-ro sw3 rc"/>'
# LH
o+='<path d="M40 120 C100 118 140 116 150 100 C156 60 160 18 166 18 C172 18 176 70 182 108 C200 118 260 120 316 122" class="nf s-am sw3 rc"/>'
# FSH
o+='<path d="M40 100 C70 96 100 98 130 94 C150 80 160 70 166 70 C172 72 176 90 190 110 C210 120 260 122 316 122" class="nf s-az sw2 rc dsh"/>'
o+='<line x1="170" y1="14" x2="170" y2="130" class="nf s-g sw1 dt"/><text x="172" y="10" class="t8 b">ovulação</text>'
o+='<g class="t8 b"><text x="62" y="86" class="tx-rs">estrogênio</text><text x="252" y="34" class="tx-ro">progesterona</text><text x="136" y="30" class="tx-am e">LH</text><text x="92" y="108" class="tx-az">FSH</text></g>'
o+='<rect x="30" y="160" width="140" height="10" rx="3" fill="#f3d3da" stroke="#c9778f"/><text x="100" y="168" class="t7 c b tx-rs">menstruação / proliferação</text><rect x="170" y="160" width="156" height="10" rx="3" fill="#e1c9f0" stroke="#7b43b8"/><text x="248" y="168" class="t7 c b tx-ro">fase lútea (endométrio secretor)</text>'
open('src/svg/ciclo.svg','w').write(f'<svg viewBox="0 0 335 176">{o}</svg>')
print('ok')
