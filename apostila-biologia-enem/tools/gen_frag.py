W=220; G=15; H=214
def frag(x,y,w,h,r=8,ring=8):
    # anel de borda (verde claro) + núcleo (verde escuro)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#9fd4b0" stroke="#2f9e5a" stroke-width="1.2"/>'
            f'<rect x="{x+ring}" y="{y+ring}" width="{w-2*ring}" height="{h-2*ring}" rx="{max(r-3,2)}" fill="#2f9e5a" opacity=".9"/>')
def panel(i,kind):
    o=f'<g transform="translate({i*(W+G)} 0)">'
    titles={0:('A. Hábitat contínuo','grande área central, fluxo livre'),1:('B. Hábitat fragmentado','estrada e lavoura isolam os fragmentos'),2:('C. Fragmentos + corredores','faixas de mata e passagens de fauna')}
    t=titles[kind]
    o+=f'<text x="{W/2}" y="11" class="t9 xb c">{t[0]}</text><text x="{W/2}" y="22" class="t8 g c">{t[1]}</text>'
    o+=f'<rect x="0" y="28" width="{W}" height="{H-28}" rx="8" fill="#f6eecd" stroke="#cdbf8a" stroke-width="1"/>'
    if kind==0:
        o+=frag(10,36,W-20,H-46,10,16)
        o+='<text x="110" y="124" class="t30 c em">🐆</text>'
        o+='<g class="nf s-vm sw15 rc"><path d="M62 146 C80 168 110 168 150 146" marker-end="url(#ar-ve)" class="s-ve"/><path d="M158 82 C140 60 100 60 66 84" class="s-ve" marker-end="url(#ar-ve)"/></g>'
        o+='<text x="110" y="182" class="t8 c b w">núcleo (interior)</text><text x="110" y="48" class="t8 c b" style="fill:#14693a">borda</text>'
    else:
        # estradas
        o+='<path d="M0 110 H220" stroke="#6b7385" stroke-width="9"/><path d="M0 110 H220" stroke="#fff" stroke-width="1.2" stroke-dasharray="6 6"/><path d="M118 28 V110" stroke="#6b7385" stroke-width="9"/><path d="M118 28 V110" stroke="#fff" stroke-width="1.2" stroke-dasharray="6 6"/>'
        o+=frag(10,36,98,66,8,9)+frag(128,36,84,66,8,8)+frag(10,120,80,82,8,9)+frag(112,124,56,56,6,8)
        if kind==1:
            o+='<text x="58" y="76" class="t20 c em">🐆</text><text x="170" y="76" class="t20 c em">🐆</text>'
            o+='<g class="f-vm"><text x="118" y="107" class="t12 b c tx-vm">✕</text><text x="50" y="112" class="t12 b c tx-vm" style="display:none"></text></g>'
            o+='<text x="152" y="148" class="t8 c b w">pequeno:</text><text x="140" y="159" class="t8 c w b">só borda</text>'
            o+='<text x="108" y="206" class="t8 c b tx-vm" style="display:none"></text>'
        else:
            # corredores
            o+='<rect x="106" y="58" width="26" height="14" fill="#2f9e5a" opacity=".95"/><rect x="38" y="100" width="14" height="24" fill="#2f9e5a" opacity=".95"/><rect x="88" y="150" width="28" height="12" fill="#2f9e5a" opacity=".95"/><rect x="164" y="98" width="14" height="30" fill="#2f9e5a" opacity=".95"/>'
            o+='<path d="M74 112 H62" stroke="#fff" stroke-width="1" style="display:none"/>'
            o+='<text x="50" y="82" class="t20 c em">🐆</text>'
            o+='<g class="nf s-ve sw2 rc dsh"><path d="M70 66 H190" marker-end="url(#ar-ve)"/><path d="M44 90 V160" marker-end="url(#ar-ve)"/></g>'
            o+='<text x="110" y="204" class="t8 c b tx-ve">fluxo gênico restabelecido ✓</text>'
    o+='</g>'
    return o
out=''.join(panel(i,i) for i in range(3))
open('src/svg/frag.svg','w').write(f'<svg viewBox="0 0 {3*W+2*G} {H+2}">{out}</svg>')
