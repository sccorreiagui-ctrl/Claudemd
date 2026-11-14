# painéis de eutrofização
import random
random.seed(7)
W=162; G=14; D=50; H=212+D
def gauge(frac, x=138):
    top=78; h=96+D
    f=h*frac
    return (f'<rect x="{x}" y="{top}" width="12" height="{h}" rx="3" class="f-w s-g sw1"/>'
            f'<rect x="{x+1}" y="{top+h-f:.1f}" width="10" height="{f:.1f}" rx="2" class="f-az"/>'
            f'<text x="{x+6}" y="{top-4}" class="t7 c b tx-az">O₂</text>')
def base(i,title1,title2):
    return (f'<text x="{W/2}" y="11" class="t9 xb c">{i}. {title1}</text><text x="{W/2}" y="22" class="t8 g c">{title2}</text>'
            f'<rect x="0" y="30" width="{W}" height="{H-30}" rx="8" class="f-w s-g sw1"/>'
            f'<rect x="1" y="66" width="{W-2}" height="{112+D}" class="l-az"/><rect x="1" y="{178+D}" width="{W-2}" height="{H-31-148-D}" rx="0" class="l-mr"/>'
            f'<path d="M1 {H-1} H{W-1}" class="nf"/>')
def dots(n,y0,y1,x0,x1,cls,r=3.2):
    o=''
    for _ in range(n):
        o+=f'<circle cx="{random.uniform(x0,x1):.1f}" cy="{random.uniform(y0,y1):.1f}" r="{r}" class="{cls}"/>'
    return o
def plants(op=1):
    o=''
    for x in (14,28,44,60,76,92,108):
        o+=f'<path d="M{x} {178+D} q-5 -22 2 -44 q4 -12 0 -26" class="nf s-ve sw2 rc" opacity="{op}"/>'
    return o
panels=[]
# 1
p=base(1,'Lago equilibrado','águas claras, luz chega ao fundo')
p+=''.join(f'<path d="M{x} 34 V{150+D}" class="nf s-am sw12 dsh" marker-end="url(#ar-am)"/>' for x in (30,70,110))
p+=dots(6,72,150+D,8,124,'f-ve',2.2)+plants(1)
p+=f'<text x="40" y="108" class="t20 c em">🐟</text><text x="92" y="{150+D}" class="t20 c em">🐟</text>'+gauge(.88)
p+='<text x="8" y="60" class="t7 b tx-am">luz</text>'
panels.append(p)
# 2
p=base(2,'Excesso de N e P','esgoto e fertilizantes entram')
p+='<path d="M0 54 H20" class="nf s-ro sw3" marker-end="url(#ar-ro)" style="display:none"/>'
p+='<rect x="-12" y="40" width="40" height="22" rx="4" class="l-la s-la sw1"/><text x="8" y="54" class="t8 c b tx-la">N · P</text><path d="M28 51 H52" class="nf s-la sw2" marker-end="url(#ar-la)"/>'
for i in range(20): p+=f'<circle cx="{10+i*6.2:.1f}" cy="{random.uniform(68,76):.1f}" r="4.2" class="f-ve"/>'
for i in range(14): p+=f'<circle cx="{14+i*8.2:.1f}" cy="{random.uniform(78,86):.1f}" r="3.6" class="f-ve" opacity=".8"/>'
p+=''.join(f'<path d="M{x} 34 V70" class="nf s-am sw12 dsh" marker-end="url(#ar-am)"/>' for x in (36,76,116))
p+=plants(.3)+'<text x="40" y="116" class="t20 c em">🐟</text><text x="78" y="62" class="t8 b c tx-ve" style="display:none"></text>'+gauge(.8)
p+=f'<text x="60" y="{190+D}" class="t7 c g">pouca luz no fundo</text><text x="6" y="94" class="t8 b tx-ve" style="display:none"></text>'
panels.append(p)
# 3
p=base(3,'Algas morrem','decomposição aeróbia consome O₂')
p+=dots(18,84,150+D,8,126,'f-mr',2.6)
p+=''.join( f'<path d="M{x} 92 V116" class="nf s-mr sw1 dt" marker-end="url(#ar-mr)"/>' for x in (24,60,96))
p+=dots(14,150+D,174+D,8,126,'f-vm',2.2)
p+=f'<text x="64" y="{140+D}" class="t8 c b tx-vm">bactérias aeróbias</text><text x="64" y="{152+D}" class="t7 c g">O₂ + matéria org. → CO₂</text>'
p+='<text x="52" y="116" class="t20 c em">🐟</text><text x="94" y="104" class="t10 b tx-vm">?</text>'+gauge(.32)
panels.append(p)
# 4
p=base(4,'Hipóxia / anoxia','mortandade de organismos aeróbios')
p+='<g transform="translate(46 80) rotate(180)"><text x="0" y="0" class="t20 c em">🐟</text></g><text x="46" y="82" class="t12 c b tx-vm" style="display:none"></text>'
p+='<g transform="translate(100 96) rotate(180)"><text x="0" y="0" class="t20 c em">🐟</text></g>'
p+='<text x="30" y="106" class="t12 b tx-vm">✕</text><text x="84" y="122" class="t12 b tx-vm">✕</text>'
p+=dots(9,92,170+D,8,124,'f-mr',2.4)
for (x,y,t) in ((24,160+D,'H₂S'),(64,150+D,'CH₄'),(100,162+D,'NH₃')):
    p+=f'<circle cx="{x}" cy="{y}" r="9" class="f-w s-g sw1"/><text x="{x}" y="{y+3}" class="t7 c b">{t}</text>'
p+='<path d="M80 176 C110 152 118 120 118 96" class="nf s-ro sw12 dsh" marker-end="url(#ar-ro)" style="display:none"/>'
p+=gauge(.06)
p+=f'<text x="64" y="{204+D}" class="t7 c g">ambiente anaeróbio no fundo</text>'
panels.append(p)
o=''
for i,pp in enumerate(panels):
    o+=f'<g transform="translate({i*(W+G)} 0)">{pp}</g>'
    if i<3:
        cx=i*(W+G)+W+G/2
        o+=f'<path d="M{cx-5} 100 L{cx+5} 120 L{cx-5} 140" class="nf s-sl sw3 rc" style="display:none"/><polygon points="{cx-6},108 {cx+6},120 {cx-6},132" class="f-sl"/>'
open('src/svg/lagos.svg','w').write(f'<svg viewBox="0 0 {4*W+3*G} {H+4}">{o}</svg>')
