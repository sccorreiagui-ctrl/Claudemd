V='#8c1f35'; VL='#f3d3da'; A='#d83a3a'; AL='#fbe0e0'
o=''
# pulmões
for cx in (110,580):
    o+=f'<ellipse cx="{cx}" cy="62" rx="62" ry="46" fill="#fde9ef" stroke="#c9778f" stroke-width="1.6"/>'
    for dx,dy in ((-18,-8),(2,-14),(20,-2),(-8,12),(14,16)):
        o+=f'<circle cx="{cx+dx}" cy="{62+dy}" r="9" fill="#fff" stroke="#c9778f" stroke-width="1"/>'
o+='<text x="110" y="124" class="t9 c xb">Pulmão direito</text><text x="580" y="124" class="t9 c xb">Pulmão esquerdo</text>'
o+='<text x="345" y="28" class="t10 c xb tx-rs" style="display:none"></text>'
# coração
o+=f'<path d="M345 206 C300 206 262 176 262 134 C262 108 282 94 306 96 C324 98 338 108 345 122 Z" fill="{VL}" stroke="{V}" stroke-width="3"/>'
o+=f'<path d="M345 206 C392 206 430 176 430 134 C430 108 410 94 386 96 C368 98 352 108 345 122 Z" fill="{AL}" stroke="{A}" stroke-width="4"/>'
o+='<path d="M345 122 V206" stroke="#1b2236" stroke-width="2"/><path d="M270 150 H345" stroke="#1b2236" stroke-width="1.4" stroke-dasharray="4 3"/><path d="M345 150 H424" stroke="#1b2236" stroke-width="1.4" stroke-dasharray="4 3"/>'
o+='<text x="304" y="130" class="t11 c xb" style="fill:#8c1f35">AD</text><text x="304" y="184" class="t11 c xb" style="fill:#8c1f35">VD</text><text x="388" y="130" class="t11 c xb tx-vm">AE</text><text x="388" y="184" class="t11 c xb tx-vm">VE</text>'
o+='<text x="345" y="226" class="t8 c g">AD/AE: átrios · VD/VE: ventrículos (a parede do VE é mais espessa)</text>'
# vasos e setas
# veias cavas -> AD
o+=f'<path d="M150 292 C170 190 260 140 290 128" class="nf sw3 rc" stroke="{V}" marker-end="url(#ar-v2)"/>'
o+='<text x="150" y="190" class="t9 b" style="fill:#8c1f35">veias cavas</text><text x="150" y="201" class="t8 g">sangue pobre em O₂</text>'
# VD -> pulmões (tronco pulmonar)
o+=f'<path d="M312 98 C300 70 220 70 168 82" class="nf sw3 rc" stroke="{V}" marker-end="url(#ar-v2)"/><path d="M322 96 C330 60 480 50 528 76" class="nf sw3 rc" stroke="{V}" marker-end="url(#ar-v2)"/>'
o+='<text x="255" y="62" class="t9 c b" style="fill:#8c1f35">artérias pulmonares</text><text x="255" y="73" class="t8 c g">(O₂ baixo)</text>'
# pulmões -> AE (veias pulmonares)
o+=f'<path d="M160 100 C220 134 320 112 366 100" class="nf sw3 rc" stroke="{A}" marker-end="url(#ar-vm)"/>'
o+=f'<path d="M520 96 C470 112 420 100 394 96" class="nf sw3 rc" stroke="{A}" marker-end="url(#ar-vm)"/><path d="M170 100 C220 100 330 80 372 94" class="nf sw3 rc" stroke="{A}" marker-end="url(#ar-vm)" style="display:none"/>'
o+='<text x="470" y="118" class="t9 c b tx-vm">veias pulmonares</text><text x="470" y="129" class="t8 c g">(O₂ alto)</text>'
# aorta -> corpo
o+=f'<path d="M404 100 C440 70 470 80 490 130 C506 176 520 240 520 280" class="nf sw3 rc" stroke="{A}" marker-end="url(#ar-vm)"/>'
o+='<text x="520" y="196" class="t9 b tx-vm">aorta e artérias</text><text x="520" y="207" class="t8 g">sangue rico em O₂</text>'
# corpo
o+='<rect x="160" y="282" width="400" height="44" rx="10" fill="#f6eecd" stroke="#cdbf8a" stroke-width="1.6"/><text x="360" y="300" class="t10 c xb">Tecidos do corpo (capilares sistêmicos)</text><text x="360" y="314" class="t8 c g">O₂ e nutrientes saem do sangue; CO₂ entra</text>'
o+='<text x="110" y="148" class="t8 c b" style="fill:#2c3b50">hematose:</text><text x="110" y="158" class="t8 c" style="fill:#2c3b50">O₂ entra, CO₂ sai</text>'
o+='<path d="M60 126 L60 126" class="nf"/>'
# legenda de cor
o+='<g transform="translate(0 232)"><rect x="0" y="0" width="14" height="10" rx="2" fill="#d83a3a"/><text x="20" y="9" class="t8">● O₂ alto</text><rect x="0" y="16" width="14" height="10" rx="2" fill="#8c1f35"/><text x="20" y="25" class="t8">◐ O₂ baixo</text><text x="0" y="44" class="t8 g">pequena circulação:</text><text x="0" y="54" class="t8 g">coração ↔ pulmões</text><text x="0" y="68" class="t8 g">grande circulação:</text><text x="0" y="78" class="t8 g">coração ↔ corpo</text></g>'
open('src/svg/circ.svg','w').write(f'<svg viewBox="0 0 690 334">{o}</svg>')
# ---- circulação comparada ----
o=''
def heart(x,title,sub,atr,vent,lines):
    g=f'<g transform="translate({x} 0)"><rect x="0" y="0" width="160" height="150" rx="8" class="f-w s-g sw1"/><text x="80" y="14" class="t10 c xb">{title}</text><text x="80" y="26" class="t8 c g">{sub}</text>'
    # átrios
    aw=60/len(atr) if len(atr)>0 else 60
    for i,c in enumerate(atr):
        g+=f'<rect x="{30+i*(60/len(atr))+(2 if len(atr)>1 else 0)}" y="36" width="{60/len(atr)-(4 if len(atr)>1 else 0)}" height="26" rx="6" fill="{c}" stroke="#1b2236" stroke-width="1.2"/>'
    for i,c in enumerate(vent):
        g+=f'<rect x="{30+i*(60/len(vent))+(2 if len(vent)>1 else 0)}" y="66" width="{60/len(vent)-(4 if len(vent)>1 else 0)}" height="34" rx="6" fill="{c}" stroke="#1b2236" stroke-width="1.2"/>'
    for i,l in enumerate(lines): g+=f'<text x="80" y="{116+i*10}" class="t8 c {"b" if i==0 else "g"}">{l}</text>'
    return g+'</g>'
R='#d83a3a'; W='#8c1f35'
MIX='url(#grad-mix)'
o+='<defs><linearGradient id="grad-mix" x1="0" x2="1"><stop offset="0" stop-color="#8c1f35"/><stop offset="1" stop-color="#d83a3a"/></linearGradient></defs>'
o+=heart(0,'Peixes','2 cavidades',[W],[W],['circulação simples','só sangue pobre em O₂ no coração','→ brânquias → corpo'])
o+=heart(176,'Anfíbios','3 cavidades',[W,R],[MIX],['dupla e incompleta','mistura no ventrículo','(pulmões e pele)'])
o+=heart(352,'Répteis*','3 + septo parcial',[W,R],[W,R],['dupla e incompleta','mistura reduzida','*crocodilianos: 4 cav.'])
o+=heart(528,'Aves e mamíferos','4 cavidades',[W,R],[W,R],['dupla e completa','sem mistura','→ metabolismo alto'])
o+='<text x="0" y="168" class="t8 g">Cor: vinho = O₂ baixo · vermelho = O₂ alto · degradê = mistura. Em peixes, sangue oxigenado das brânquias segue direto aos tecidos, sem voltar ao coração.</text>'
open('src/svg/circcomp.svg','w').write(f'<svg viewBox="0 0 688 174">{o}</svg>')
print('ok')
