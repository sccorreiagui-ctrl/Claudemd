import math
o=''
# membrana plasmática à direita
for y in range(10,224,9):
    o+=f'<circle cx="598" cy="{y}" r="3.6" class="f-az"/><circle cx="614" cy="{y}" r="3.6" class="f-az"/><path d="M598 {y+3} V{y+12} M614 {y+3} V{y+12}" class="nf s-am sw12" style="display:none"/>'
o+='<rect x="600" y="8" width="12" height="216" fill="#d19a00" opacity=".8"/>'
o+='<text x="606" y="236" class="t8 c b tx-az">membrana plasmática</text>'
o+='<text x="660" y="22" class="t8 c b g">meio</text><text x="660" y="32" class="t8 c b g">extracelular</text>'
# núcleo
o+='<circle cx="62" cy="116" r="50" class="nf s-ro sw1 dsh"/><circle cx="62" cy="116" r="46" class="l-ro s-ro sw2"/><circle cx="52" cy="124" r="9" class="f-ro" opacity=".55"/>'
o+='<path d="M30 104 q8 -14 16 0 t16 0 t16 0 t12 -8" class="nf s-ro sw2 rc"/>'
for a in (-60,-20,25,70):
    r=math.radians(a); o+=f'<circle cx="{62+46*math.cos(r):.1f}" cy="{116+46*math.sin(r):.1f}" r="2.6" class="f-w s-ro sw1"/>'
o+='<text x="62" y="186" class="t9 c xb tx-ro">Núcleo</text><text x="62" y="197" class="t8 c g">DNA → mRNA</text>'
# mRNA saindo
o+='<path d="M110 94 q6 -8 12 0 t12 0 t12 0 t12 0" class="nf s-ro sw2 rc" marker-end="url(#ar-ro)"/><text x="148" y="82" class="t8 b tx-ro">mRNA</text>'
# RER
for k,y in enumerate((66,88,110,132)):
    x0=140+ (0 if k<3 else 6)
    o+=f'<rect x="{x0}" y="{y}" width="{118-(x0-140)}" height="14" rx="7" class="l-sl s-sl sw12"/>'
    for x in range(x0+8,x0+110,12):
        o+=f'<circle cx="{x}" cy="{y-2.5}" r="2.2" class="f-k"/><circle cx="{x}" cy="{y+16.5}" r="2.2" class="f-k"/>'
o+='<path d="M108 120 C122 120 126 112 140 112" class="nf s-sl sw2"/>'
o+='<text x="198" y="176" class="t9 c xb tx-sl">Retículo endoplasmático rugoso</text><text x="198" y="187" class="t8 c g">ribossomos aderidos: proteínas para exportar,</text><text x="198" y="197" class="t8 c g">membrana ou lisossomos</text>'
# vesícula de transporte
o+='<circle cx="288" cy="102" r="9" fill="#fff" stroke="#1f78c8" stroke-width="2"/><circle cx="288" cy="102" r="3.5" class="f-rs"/>'
o+='<path d="M262 108 H276" class="nf s-k sw15" marker-end="url(#ar-k)"/><path d="M300 102 H322" class="nf s-k sw15" marker-end="url(#ar-k)"/>'
o+='<text x="288" y="80" class="t8 c b tx-az">vesícula de</text><text x="288" y="90" class="t8 c b tx-az">transporte</text>'
# Golgi
for k,y in enumerate((72,90,108,126,144)):
    o+=f'<path d="M332 {y} Q382 {y-16} 432 {y}" class="nf" stroke="#8aa0bd" stroke-width="8" stroke-linecap="round"/><path d="M332 {y} Q382 {y-16} 432 {y}" class="nf" stroke="#475a73" stroke-width="1.2" opacity=".6"/>'
o+='<text x="326" y="64" class="t8 b tx-sl">cis</text><text x="428" y="168" class="t8 b tx-sl">trans</text>'
o+='<text x="382" y="192" class="t9 c xb tx-sl">Complexo golgiense</text><text x="382" y="203" class="t8 c g">modifica (ex.: glicosilação),</text><text x="382" y="213" class="t8 c g">seleciona e empacota</text>'
# vesículas de secreção
o+='<circle cx="474" cy="104" r="10" fill="#fff" stroke="#1f78c8" stroke-width="2"/><g class="f-rs"><circle cx="471" cy="102" r="2.4"/><circle cx="478" cy="106" r="2.4"/><circle cx="473" cy="109" r="2"/></g>'
o+='<path d="M436 138 C452 138 462 122 468 114" class="nf s-k sw15" marker-end="url(#ar-k)"/>'
o+='<circle cx="520" cy="116" r="11" fill="#fff" stroke="#1f78c8" stroke-width="2"/><g class="f-rs"><circle cx="517" cy="114" r="2.4"/><circle cx="524" cy="118" r="2.4"/><circle cx="519" cy="121" r="2"/></g>'
o+='<path d="M486 108 H506" class="nf s-k sw15" marker-end="url(#ar-k)"/>'
o+='<text x="498" y="86" class="t8 c b tx-az">vesículas de</text><text x="498" y="96" class="t8 c b tx-az">secreção</text>'
# fusão
o+='<path d="M532 116 H586" class="nf s-k sw15" marker-end="url(#ar-k)"/>'
o+='<path d="M586 116 a12 12 0 0 1 14 -2" class="nf" style="display:none"/>'
o+='<g class="f-rs"><circle cx="630" cy="112" r="3"/><circle cx="640" cy="122" r="3"/><circle cx="652" cy="110" r="3"/><circle cx="662" cy="124" r="3"/><circle cx="636" cy="136" r="3"/></g>'
o+='<path d="M616 114 H626" class="nf s-rs sw2" marker-end="url(#ar-rs)"/>'
o+='<text x="650" y="158" class="t9 c xb tx-rs">exocitose</text><text x="650" y="169" class="t8 c g">(ex.: insulina)</text>'
# lisossomo
o+='<circle cx="528" cy="176" r="14" class="l-la s-la sw2"/><g class="f-la"><circle cx="523" cy="172" r="2"/><circle cx="532" cy="175" r="2"/><circle cx="526" cy="181" r="2"/></g><path d="M440 152 C470 160 496 168 510 174" class="nf s-k sw15" marker-end="url(#ar-k)"/>'
o+='<text x="540" y="202" class="t9 c xb tx-la">Lisossomo</text><text x="540" y="213" class="t8 c g">hidrolases ácidas (pH ≈ 5)</text>'
# badges
def bd(x,y,t): return f'<circle cx="{x}" cy="{y}" r="8.5" class="f-vm"/><text x="{x}" y="{y+3.2}" class="t9 c b w">{t}</text>'
o+=bd(24,70,'1')+bd(186,50,'2')+bd(128,150,'3')+bd(288,60,'4')+bd(380,44,'5')+bd(560,98,'6')
open('src/svg/secrecao.svg','w').write(f'<svg viewBox="0 0 690 246">{o}</svg>')
