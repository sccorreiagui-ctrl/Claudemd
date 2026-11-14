import math
# ---------- painéis de transporte ----------
PW=134;PG=5;PH=206
def band(x0,x1,yf,gaps=(),step=8):
    o=''
    pts=[(x,yf(x)) for x in range(x0,x1+1,2)]
    d='M'+' L'.join(f'{x} {y:.1f}' for x,y in pts)
    o+=f'<path d="{d}" class="nf" stroke="#d19a00" stroke-width="11" stroke-linecap="butt" opacity=".85"/>'
    for x in range(x0+4,x1,step):
        if any(a<=x<=b for a,b in gaps): continue
        y=yf(x)
        o+=f'<circle cx="{x}" cy="{y-8:.1f}" r="3.6" class="f-az"/><circle cx="{x}" cy="{y+8:.1f}" r="3.6" class="f-az"/>'
    return o
def dots(pts,cls,r=3.2,txt=None):
    o=''
    for (x,y) in pts:
        o+=f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>'
        if txt: o+=f'<text x="{x}" y="{y+2.6}" class="t6 c b w">{txt}</text>'
    return o
def sq(pts,cls,s=6):
    return ''.join(f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="1.2" class="{cls}"/>' for x,y in pts)
def panel(i,title,sub,body,foot1,foot2,foot3=None):
    x=i*(PW+PG)
    o=f'<g transform="translate({x} 0)"><rect x="0" y="0" width="{PW}" height="{PH}" rx="8" class="f-w s-g sw1"/>'
    o+=f'<text x="{PW/2}" y="14" class="t10 c xb tx-az">{title}</text><text x="{PW/2}" y="25" class="t8 c g">{sub}</text>'
    o+=body
    o+=f'<text x="{PW/2}" y="170" class="t8 c b">{foot1}</text><text x="{PW/2}" y="181" class="t8 c g">{foot2}</text>'
    if foot3: o+=f'<text x="{PW/2}" y="192" class="t8 c g">{foot3}</text>'
    return o+'</g>'
flat=lambda x:92
out=''
# 1 difusão simples
b=band(6,PW-6,flat)
b+=dots([(18,40),(34,58),(52,44),(70,60),(88,40),(104,56),(120,44),(44,72),(96,74)],'f-la',3.4)+dots([(30,128),(100,142)],'f-la',3.4)
b+='<path d="M64 62 V132" class="nf s-la sw2 dsh" marker-end="url(#ar-la)"/>'
b+='<text x="8" y="36" class="t7 g">fora: + conc.</text><text x="8" y="154" class="t7 g">dentro: − conc.</text>'
out+=panel(0,'Difusão simples','sem proteína',b,'a favor do gradiente','O₂, CO₂, lipossolúveis','sem gasto de ATP')
# 2 facilitada
gaps=[(40,68)]
b=band(6,PW-6,flat,gaps)
b+='<path d="M40 76 H52 V108 H40 Q36 108 36 104 V80 Q36 76 40 76Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.4"/><path d="M78 76 H66 V108 H78 Q82 108 82 104 V80 Q82 76 78 76Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.4"/><rect x="52" y="76" width="14" height="32" class="l-az"/>'
b+=sq([(16,42),(36,56),(52,40),(78,50),(100,42),(116,60),(24,70),(92,68),(60,60)],'f-ve',6)+sq([(34,134),(96,140)],'f-ve',6)
b+='<path d="M59 66 V132" class="nf s-ve sw2 dsh" marker-end="url(#ar-ve)"/>'
b+='<text x="100" y="104" class="t7 b" style="fill:#2c3b50">canal</text>'
out+=panel(1,'Difusão facilitada','canal ou carreadora',b,'a favor do gradiente','glicose, íons (hidrofílicos)','sem gasto de ATP')
# 3 osmose
b=band(6,PW-6,flat,[(52,66)])
b+='<path d="M52 78 H64 V106 H52 Q48 106 48 102 V82 Q48 78 52 78Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.2"/><path d="M80 78 H68 V106 H80 Q84 106 84 102 V82 Q84 78 80 78Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.2"/>'
b+=dots([(16,44),(34,60),(100,48),(118,64),(78,40),(22,72),(112,36)],'f-az',2.6)+sq([(54,50),(90,66)],'f-la',5)
b+=dots([(16,124),(34,140),(100,128),(118,144),(78,122),(22,152),(112,150)],'f-az',2.6)+sq([(24,112),(44,128),(62,118),(80,140),(98,112),(108,136),(54,148),(84,152),(14,138),(122,122)],'f-la',5)
b+='<path d="M58 66 V126" class="nf s-az sw3" marker-end="url(#ar-az)"/>'
b+='<text x="8" y="36" class="t7 b tx-az">hipotônico</text><text x="8" y="152" class="t7 b tx-la" style="display:none"></text>'
b+='<text x="PWX" y="118" class="t7 b tx-la" style="display:none"></text>'
out+=panel(2,'Osmose','só a água (solvente)',b.replace('PWX','0'),'do menos para o mais soluto','(hipo → hipertônico)','solutos não atravessam')
# 4 transporte ativo
b=band(6,PW-6,flat,[(46,86)])
b+='<path d="M46 74 H86 Q92 74 92 80 V104 Q92 110 86 110 H46 Q40 110 40 104 V80 Q40 74 46 74Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.4"/>'
b+='<path d="M52 74 Q66 94 80 74" fill="#c3d0e6" stroke="#475a73" stroke-width="1"/><text x="66" y="102" class="t7 c b" style="fill:#2c3b50">bomba</text>'
b+=dots([(14,42),(30,56),(104,40),(120,58),(18,70),(116,72)],'f-ro',5,'Na')+dots([(100,134),(118,146)],'f-rs',5,'K')
b+=dots([(20,130),(36,144),(14,148)],'f-ro',5,'Na')+dots([(34,150)],'f-rs',5,'K')
b+='<circle cx="106" cy="118" r="10" class="f-la"/><text x="106" y="121" class="t6 c b w">ATP</text>'
b+='<path d="M52 128 V92" class="nf s-ro sw2" marker-end="url(#ar-ro)"/><path d="M80 64 V128" class="nf s-rs sw2" marker-end="url(#ar-rs)"/>'
b+='<text x="48" y="142" class="t6 b tx-ro">3 Na⁺ ↑</text><text x="84" y="60" class="t6 b tx-rs">2 K⁺ ↓</text>'
out+=panel(3,'Transporte ativo','bomba Na⁺/K⁺ (ATPase)',b,'contra o gradiente','gasta ATP','mantém potencial de membrana')
# 5 endo/exocitose
def ypocket(x):
    return 92+22*math.exp(-((x-34)/12)**2)
b=band(6,PW-6,ypocket,[])
b+='<circle cx="34" cy="92" r="6" class="f-vm" style="display:none"/><circle cx="34" cy="74" r="7" class="f-vm"/><path d="M34 52 V66" class="nf s-vm sw2" marker-end="url(#ar-vm)"/>'
b+='<circle cx="34" cy="144" r="13" fill="#fff" stroke="#1f78c8" stroke-width="3"/><circle cx="34" cy="144" r="6" class="f-vm"/><text x="34" y="164" class="t7 c b tx-az" style="display:none"></text>'
b+='<circle cx="100" cy="132" r="13" fill="#fff" stroke="#1f78c8" stroke-width="3"/><g class="f-rs"><circle cx="97" cy="130" r="2.6"/><circle cx="104" cy="134" r="2.6"/><circle cx="99" cy="137" r="2.2"/></g>'
b+='<g class="f-rs"><circle cx="100" cy="68" r="2.4"/><circle cx="110" cy="62" r="2.4"/><circle cx="106" cy="76" r="2.4"/></g><path d="M100 108 V84" class="nf s-rs sw15" marker-end="url(#ar-rs)"/>'
b+='<text x="34" y="38" class="t7 c b tx-vm">endocitose</text><text x="100" y="44" class="t7 c b tx-rs">exocitose</text>'
out+=panel(4,'Endo/exocitose','vesículas (fagocitose, pinocitose)',b,'partículas e macromoléculas','ex.: macrófago; secreção de insulina','gasta ATP')
Wt=5*PW+4*PG
open('src/svg/transporte.svg','w').write(f'<svg viewBox="0 0 {Wt} {PH}">{out}</svg>')

# ---------- osmose em células animal/vegetal ----------
CW=223;CG=10
def medium(x,y,w,h,n,seed):
    import random
    random.seed(seed)
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="l-az"/>'
    for _ in range(n):
        o+=f'<rect x="{random.uniform(x+6,x+w-12):.1f}" y="{random.uniform(y+6,y+h-12):.1f}" width="5" height="5" rx="1" class="f-la"/>'
    return o
def arrows_in(cx,cy,r,n=4,inward=True,cls='s-az'):
    o=''
    for k in range(n):
        a=math.radians(45+90*k)
        x1=cx+(r+22)*math.cos(a);y1=cy+(r+22)*math.sin(a);x2=cx+(r+4)*math.cos(a);y2=cy+(r+4)*math.sin(a)
        if not inward: x1,y1,x2,y2=x2,y2,x1,y1
        o+=f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="nf {cls} sw2" marker-end="url(#ar-az)"/>'
    return o
def solutes(cx,cy,r,n):
    import random
    random.seed(n+int(cx))
    o=''
    for _ in range(n):
        a=random.uniform(0,6.28);d=random.uniform(0,r*0.7)
        o+=f'<rect x="{cx+d*math.cos(a)-2.5:.1f}" y="{cy+d*math.sin(a)-2.5:.1f}" width="5" height="5" rx="1" class="f-la"/>'
    return o
heads=[('HIPOTÔNICO','meio com MENOS soluto','água ENTRA'),('ISOTÔNICO','mesma concentração','entra = sai'),('HIPERTÔNICO','meio com MAIS soluto','água SAI')]
out=''
for i,(h,s,w) in enumerate(heads):
    x=i*(CW+CG)
    out+=f'<g transform="translate({x} 0)"><rect x="0" y="0" width="{CW}" height="30" rx="6" class="f-az"/><text x="{CW/2}" y="13" class="t10 c xb w">{h}</text><text x="{CW/2}" y="24" class="t8 c w">{s} → {w}</text></g>'
nm=[3,7,13]
# animal
for i in range(3):
    x=i*(CW+CG); cx=x+CW/2; cy=110
    out+=medium(x,36,CW,152,nm[i],10+i)
    if i==0:
        out+=f'<circle cx="{cx}" cy="{cy}" r="38" fill="#ffe3e3" stroke="#d83a3a" stroke-width="2.2" stroke-dasharray="5 3"/>'+solutes(cx,cy,38,7)+arrows_in(cx,cy,38)
        for k in range(8):
            a=math.radians(22+45*k);out+=f'<line x1="{cx+44*math.cos(a):.1f}" y1="{cy+44*math.sin(a):.1f}" x2="{cx+52*math.cos(a):.1f}" y2="{cy+52*math.sin(a):.1f}" class="nf s-vm sw15 rc" style="display:none"/>'
        out+=f'<text x="{cx}" y="{cy+66}" class="t9 c b tx-vm">inchada → lise (hemólise)</text>'
    elif i==1:
        out+=f'<circle cx="{cx}" cy="{cy}" r="30" fill="#ffe3e3" stroke="#d83a3a" stroke-width="2.2"/>'+solutes(cx,cy,30,7)
        out+=f'<line x1="{cx-48}" y1="{cy-30}" x2="{cx-34}" y2="{cy-22}" class="nf s-az sw2" marker-end="url(#ar-az)"/><line x1="{cx-34}" y1="{cy+22}" x2="{cx-48}" y2="{cy+30}" class="nf s-az sw2" marker-end="url(#ar-az)"/><line x1="{cx+48}" y1="{cy-30}" x2="{cx+34}" y2="{cy-22}" class="nf s-az sw2" marker-end="url(#ar-az)"/><line x1="{cx+34}" y1="{cy+22}" x2="{cx+48}" y2="{cy+30}" class="nf s-az sw2" marker-end="url(#ar-az)"/>'
        out+=f'<text x="{cx}" y="{cy+58}" class="t9 c b tx-ve">volume normal</text>'
    else:
        pts=[]
        for k in range(24):
            a=2*math.pi*k/24; r=22+(6 if k%2==0 else -2)
            pts.append(f'{cx+r*math.cos(a):.1f},{cy+r*math.sin(a):.1f}')
        out+=f'<polygon points="{" ".join(pts)}" fill="#ffe3e3" stroke="#d83a3a" stroke-width="2.2" stroke-linejoin="round"/>'+solutes(cx,cy,22,7)+arrows_in(cx,cy,30,4,False)
        out+=f'<text x="{cx}" y="{cy+56}" class="t9 c b tx-vm">encolhida → crenação</text>'
    out+=f'<text x="{x+8}" y="52" class="t8 b g" style="display:none"></text>'
# rótulo linha
# vegetal
oy=198
for i in range(3):
    x=i*(CW+CG); cx=x+CW/2; cy=oy+80
    out+=medium(x,oy,CW,160,nm[i],30+i)
    w=104;h=84
    wall=f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="6" fill="#e8f5ec" stroke="#13663a" stroke-width="5"/>'
    if i==0:
        out+=wall+f'<rect x="{cx-w/2+3}" y="{cy-h/2+3}" width="{w-6}" height="{h-6}" rx="4" fill="none" stroke="#1f78c8" stroke-width="1.4"/><rect x="{cx-w/2+13}" y="{cy-h/2+13}" width="{w-26}" height="{h-26}" rx="8" class="l-az s-az sw1"/>'
        out+=arrows_in(cx,cy,w/2-8,4)+f'<text x="{cx}" y="{cy+h/2+18}" class="t9 c b tx-ve">túrgida (parede resiste)</text>'
    elif i==1:
        out+=wall+f'<rect x="{cx-w/2+3}" y="{cy-h/2+3}" width="{w-6}" height="{h-6}" rx="4" fill="none" stroke="#1f78c8" stroke-width="1.4"/><rect x="{cx-w/2+22}" y="{cy-h/2+20}" width="{w-44}" height="{h-40}" rx="8" class="l-az s-az sw1"/>'
        out+=f'<text x="{cx}" y="{cy+h/2+18}" class="t9 c b tx-ve">flácida / estado normal</text>'
    else:
        out+=f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="6" fill="#d8ecfb" stroke="#13663a" stroke-width="5"/>'
        out+=f'<rect x="{cx-w/2+16}" y="{cy-h/2+14}" width="{w-32}" height="{h-28}" rx="10" fill="#e8f5ec" stroke="#1f78c8" stroke-width="1.6"/><rect x="{cx-w/2+30}" y="{cy-h/2+26}" width="{w-60}" height="{h-52}" rx="6" class="l-az s-az sw1"/>'
        out+=f'<text x="{cx}" y="{cy+h/2+18}" class="t9 c b tx-vm">plasmólise (membrana se solta)</text>'
    out+=f'<text x="{cx}" y="{cy-h/2-8}" class="t7 c g" style="display:none"></text>'
# legenda
out+='<g transform="translate(0 366)"><rect x="0" y="0" width="12" height="12" rx="2" class="l-az s-az sw1"/><text x="18" y="10" class="t8">meio aquoso / vacúolo</text><rect x="130" y="3" width="5" height="5" rx="1" class="f-la"/><text x="142" y="10" class="t8">soluto</text><line x1="190" y1="6" x2="214" y2="6" class="nf s-az sw2" marker-end="url(#ar-az)"/><text x="220" y="10" class="t8">fluxo de água</text><rect x="320" y="0" width="14" height="12" rx="2" fill="#e8f5ec" stroke="#13663a" stroke-width="3"/><text x="342" y="10" class="t8">parede de celulose (célula vegetal)</text></g>'
out+='<text x="8" y="219" class="t9 xb tx-sl" style="display:none"></text>'
# rótulos de linha
out+='<text x="6" y="52" class="t8 b tx-sl" style="display:none"></text>'
out+='<text x="8" y="50" class="t9 xb tx-sl">CÉLULA ANIMAL</text><text x="8" y="214" class="t9 xb tx-ve">CÉLULA VEGETAL</text>'
open('src/svg/osmose.svg','w').write(f'<svg viewBox="0 0 {3*CW+2*CG} 382">{out}</svg>')
print('ok')
