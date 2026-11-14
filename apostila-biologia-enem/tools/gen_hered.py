o=''
def sq(x,y,aff=False,lab=''):
    return f'<rect x="{x-12}" y="{y-12}" width="24" height="24" fill="{"#1b2236" if aff else "#fff"}" stroke="#1b2236" stroke-width="1.8"/><text x="{x}" y="{y+26}" class="t9 c b">{lab}</text>'
def ci(x,y,aff=False,lab=''):
    return f'<circle cx="{x}" cy="{y}" r="12" fill="{"#1b2236" if aff else "#fff"}" stroke="#1b2236" stroke-width="1.8"/><text x="{x}" y="{y+26}" class="t9 c b">{lab}</text>'
o+='<text x="2" y="38" class="t10 xb tx-ro">I</text><text x="2" y="124" class="t10 xb tx-ro">II</text>'
o+=sq(110,34,False,'Aa')+ci(220,34,False,'Aa')+'<path d="M122 34 H208" class="nf s-k sw2"/>'
o+='<path d="M165 34 V74 M60 74 H270 M60 74 V108 M165 74 V108 M270 74 V108" class="nf s-k sw2"/>'
o+=sq(60,120,True,'aa (afetado)')+ci(165,120,False,'A_')+sq(270,120,False,'A_')
o+='<text x="165" y="156" class="t8 c tx-vm b">P(Aa) = 2/3</text><text x="270" y="156" class="t8 c tx-vm b">P(Aa) = 2/3</text>'
o+='<g transform="translate(6 170)"><rect x="0" y="0" width="10" height="10" fill="#fff" stroke="#1b2236" stroke-width="1.4"/><text x="14" y="9" class="t8">homem</text><circle cx="62" cy="5" r="5.5" fill="#fff" stroke="#1b2236" stroke-width="1.4"/><text x="72" y="9" class="t8">mulher</text><rect x="116" y="0" width="10" height="10" fill="#1b2236"/><text x="130" y="9" class="t8">afetado</text><text x="180" y="9" class="t8">— casamento · | descendência</text></g>'
open('src/svg/hered.svg','w').write(f'<svg viewBox="0 0 335 186">{o}</svg>')
