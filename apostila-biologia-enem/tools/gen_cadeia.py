o=''
W=690
o+='<rect x="0" y="10" width="548" height="108" rx="8" class="l-sl"/><rect x="0" y="150" width="548" height="150" rx="8" class="l-la"/>'
o+='<text x="8" y="26" class="t9 xb tx-sl">ESPAÇO INTERMEMBRANAS — [H⁺] ALTA (pH baixo)</text><text x="8" y="294" class="t9 xb tx-la">MATRIZ — [H⁺] BAIXA</text>'
o+='<rect x="0" y="118" width="548" height="32" class="l-am"/>'
for x in range(6,548,11):
    o+=f'<circle cx="{x}" cy="121" r="3.6" class="f-az"/><circle cx="{x}" cy="147" r="3.6" class="f-az"/>'
o+='<text x="548" y="134" class="t7 b tx-am e" style="display:none"></text>'
def cx(x0,x1,y0,y1,lab,sub=None,fill='#dfe5ef'):
    r=f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="12" fill="{fill}" stroke="#475a73" stroke-width="1.8"/>'
    r+=f'<text x="{(x0+x1)/2}" y="{(y0+y1)/2+4}" class="t12 c xb" style="fill:#2c3b50">{lab}</text>'
    return r
o+=cx(56,112,100,170,'I')+cx(142,184,110,158,'II')+cx(246,302,100,170,'III')+cx(372,428,100,170,'IV')
# ubiquinona e citocromo c
o+='<circle cx="214" cy="134" r="9" class="f-la"/><text x="214" y="137" class="t8 c b w">Q</text>'
o+='<circle cx="338" cy="104" r="9" class="f-la"/><text x="338" y="107" class="t8 c b w">c</text>'
# elétrons
o+='<g class="nf s-la sw3 rc"><path d="M112 134 C130 128 160 124 204 132" marker-end="url(#ar-la)"/><path d="M184 134 H202" marker-end="url(#ar-la)" style="display:none"/><path d="M224 134 C236 134 240 134 244 134" marker-end="url(#ar-la)"/><path d="M302 126 C312 112 322 106 328 106" marker-end="url(#ar-la)"/><path d="M348 106 C360 108 366 112 372 118" marker-end="url(#ar-la)"/></g>'
o+='<path d="M184 146 C196 146 204 142 206 140" class="nf s-la sw2" marker-end="url(#ar-la)"/>'
# bombeamento de H+
for x in (84,274,400):
    o+=f'<path d="M{x} 118 V84" class="nf s-vm sw3" marker-end="url(#ar-vm)"/><circle cx="{x}" cy="62" r="8" class="f-vm"/><text x="{x}" y="65" class="t8 c b w">H⁺</text>'
# entradas
o+='<text x="34" y="214" class="t9 b tx-la">NADH</text><path d="M42 204 C48 190 60 180 70 172" class="nf s-la sw2" marker-end="url(#ar-la)"/><text x="34" y="226" class="t8 g">→ NAD⁺ + H⁺</text>'
o+='<text x="132" y="214" class="t9 b tx-la">FADH₂</text><path d="M158 202 V162" class="nf s-la sw2" marker-end="url(#ar-la)"/><text x="132" y="226" class="t8 g">→ FAD</text>'
o+='<text x="396" y="214" class="t9 b tx-az">½ O₂ + 2 e⁻ + 2 H⁺</text><path d="M400 202 V172" class="nf s-az sw2" marker-end="url(#ar-az)" style="display:none"/><text x="396" y="226" class="t9 b tx-az">→ H₂O</text>'
# ATP sintase
o+='<path d="M470 118 H520 V150 H470Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.8"/><text x="495" y="138" class="t9 c b" style="fill:#2c3b50">F₀</text>'
o+='<rect x="490" y="150" width="10" height="18" fill="#c3d0e6" stroke="#475a73" stroke-width="1.4"/><circle cx="495" cy="190" r="24" fill="#dfe5ef" stroke="#475a73" stroke-width="1.8"/><text x="495" y="194" class="t10 c xb" style="fill:#2c3b50">F₁</text>'
o+='<path d="M482 64 V112 M508 64 V112" class="nf s-vm sw3" style="display:none"/><path d="M495 52 V114" class="nf s-vm sw4" marker-end="url(#ar-vm)"/><circle cx="495" cy="44" r="8" class="f-vm"/><text x="495" y="47" class="t8 c b w">H⁺</text>'
o+='<path d="M470 168 a28 28 0 0 0 -2 36" class="nf s-la sw2" marker-end="url(#ar-la)" style="display:none"/><path d="M466 176 a30 30 0 0 0 4 28" class="nf s-ro sw2" style="display:none"/><path d="M458 184 C454 204 470 224 492 222" class="nf s-k sw15" marker-end="url(#ar-k)" style="display:none"/>'
o+='<text x="495" y="238" class="t9 c xb tx-la">ADP + Pi → ATP</text><text x="495" y="250" class="t8 c g">F₁ gira com o fluxo de H⁺</text>'
o+='<text x="495" y="20" class="t9 c xb tx-vm" style="display:none"></text>'
# nomes
o+='<text x="84" y="92" class="t8 c b tx-sl" style="display:none"></text>'
# inibidor
o+='<g><circle cx="400" cy="130" r="11" class="f-vm"/><text x="400" y="135" class="t14 c b w">✕</text></g>'
o+='<text x="440" y="184" class="t8 b tx-vm e">cianeto e CO</text><text x="440" y="194" class="t8 b tx-vm e">bloqueiam o IV</text>'
# vazamento
o+='<path d="M127 66 V172" class="nf s-vm sw3 dsh" marker-end="url(#ar-vm)"/><text x="196" y="40" class="t8 b tx-la c">DNP · termogenina:</text><text x="196" y="50" class="t8 g c">vazamento de H⁺ → calor</text><path d="M160 54 L131 72" class="nf s-g sw1"/>'
# legenda/ analogia usina
o+='<rect x="560" y="10" width="130" height="290" rx="8" class="f-w s-g sw1"/><text x="625" y="26" class="t9 c xb tx-la">ANALOGIA: USINA</text>'
o+='<rect x="572" y="36" width="106" height="52" rx="6" class="l-az s-az sw1"/><path d="M576 54 q8 -6 16 0 t16 0 t16 0 t16 0 t14 0" class="nf s-az sw2"/><text x="625" y="76" class="t8 c b tx-az">reservatório</text><text x="625" y="84" class="t7 c g" style="display:none"></text>'
o+='<path d="M625 90 V128" class="nf s-az sw4" marker-end="url(#ar-az)"/>'
o+='<circle cx="625" cy="148" r="20" class="f-sl"/><path d="M611 148 a14 14 0 1 1 6 12" class="nf s-w sw3" marker-end="url(#ar-w)"/><text x="625" y="152" class="t8 c b w" style="display:none"></text>'
o+='<path d="M625 170 V196" class="nf s-la sw4" marker-end="url(#ar-la)"/><text x="625" y="212" class="t10 c xb tx-la">⚡ ATP</text>'
o+='<g class="t8 c"><text x="625" y="232" class="b">gradiente de H⁺</text><text x="625" y="242" class="g">= água represada</text><text x="625" y="256" class="b">ATP sintase</text><text x="625" y="266" class="g">= turbina</text><text x="625" y="280" class="b">cianeto</text><text x="625" y="290" class="g">= tranca a comporta</text></g>'
open('src/svg/cadeia.svg','w').write(f'<svg viewBox="0 0 {W} 306">{o}</svg>')
