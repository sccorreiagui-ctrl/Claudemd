import random
random.seed(11)
G='#98a2b6'; R='#d83a3a'
def dots(x0,y0,w,h,n,res,col2=R):
    o=''
    for i in range(n):
        c=col2 if i<res else G
        o+=f'<circle cx="{random.uniform(x0+6,x0+w-6):.1f}" cy="{random.uniform(y0+6,y0+h-6):.1f}" r="4.6" fill="{c}" stroke="#fff" stroke-width=".8"/>'
    return o
# ---- seleção natural (resistência a antibiótico)
o=''
pw=210
def panel(i,title,sub):
    return f'<g transform="translate({i*(pw+30)} 0)"><text x="{pw/2}" y="12" class="t10 c xb tx-sl">{title}</text><text x="{pw/2}" y="23" class="t8 c g">{sub}</text><rect x="0" y="30" width="{pw}" height="86" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>'
o+=panel(0,'1. Variação','mutações ao acaso: poucas bactérias resistentes')+dots(0,30,pw,86,26,3)+'</g>'
o+=panel(1,'2. Pressão seletiva','antibiótico mata as sensíveis')+dots(240,30,pw,86,26,3).replace('','')+'</g>'
# painel 2: sensíveis com X: refaz
o=''
def pn(i,title,sub,content):
    return f'<g transform="translate({i*(pw+30)} 0)"><text x="{pw/2}" y="12" class="t10 c xb tx-sl">{title}</text><text x="{pw/2}" y="23" class="t8 c g">{sub}</text><rect x="0" y="30" width="{pw}" height="86" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>{content}<text x="{pw/2}" y="132" class="t8 c g"></text></g>'
random.seed(4)
c1=dots(0,30,pw,86,26,3)
c2=''
random.seed(4)
pts=[(random.uniform(6,pw-6),random.uniform(36,110)) for _ in range(26)]
for i,(x,y) in enumerate(pts):
    if i<3: c2+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{R}" stroke="#fff"/>'
    else: c2+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{G}" opacity=".35"/><text x="{x:.1f}" y="{y+3:.1f}" class="t8 c b" style="fill:#475a73">✕</text>'
random.seed(9)
c3=dots(0,30,pw,86,40,40)
o+=pn(0,'1. Variação preexistente','mutações ao acaso: poucas resistentes',c1)
o+=pn(1,'2. Pressão seletiva','antibiótico elimina as sensíveis',c2)
o+=pn(2,'3. Reprodução diferencial','as resistentes se multiplicam',c3)
for i in range(2):
    x=i*(pw+30)+pw+4
    o+=f'<path d="M{x} 74 H{x+20}" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
o+='<g transform="translate(0 134)"><circle cx="6" cy="6" r="5" fill="#98a2b6"/><text x="16" y="10" class="t8">sensível</text><circle cx="76" cy="6" r="5" fill="#d83a3a"/><text x="86" y="10" class="t8">resistente (herdável)</text><text x="230" y="10" class="t8 g">O antibiótico não “cria” a resistência: seleciona a que já existia.</text></g>'
open('src/svg/selecao.svg','w').write(f'<svg viewBox="0 0 690 152">{o}</svg>')
# ---- deriva
random.seed(2)
o=''
cols=['#1f78c8','#f2691b']
o+='<rect x="0" y="22" width="120" height="100" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>'
for i in range(24): o+=f'<circle cx="{random.uniform(8,112):.1f}" cy="{random.uniform(30,114):.1f}" r="4.6" fill="{cols[i%2]}"/>'
o+='<path d="M124 72 L156 52 V92 Z" class="f-sl" opacity=".5"/><text x="140" y="112" class="t7 c g">evento</text><text x="140" y="121" class="t7 c g">casual</text>'
o+='<rect x="160" y="22" width="40" height="100" rx="8" fill="#f4f6fb" stroke="#cfd6e3"/>'
for (x,y) in ((172,50),(188,70),(176,92)): o+=f'<circle cx="{x}" cy="{y}" r="4.6" fill="{cols[1]}"/>'
o+='<path d="M206 72 H224" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
o+='<rect x="228" y="22" width="100" height="100" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>'
for i in range(18): o+=f'<circle cx="{random.uniform(236,320):.1f}" cy="{random.uniform(30,114):.1f}" r="4.6" fill="{cols[1]}"/>'
o+='<text x="168" y="138" class="t8 c b">sobreviventes por acaso</text><text x="278" y="138" class="t8 c b tx-la">alelo azul perdido</text><text x="60" y="138" class="t8 c b">população original</text><text x="0" y="154" class="t8 g">Efeito gargalo: acaso em populações pequenas; não é adaptação.</text><text x="0" y="165" class="t8 g">Efeito fundador: poucos indivíduos fundam uma nova população.</text>'
open('src/svg/deriva.svg','w').write(f'<svg viewBox="0 0 335 170">{o}</svg>')
# ---- especiação
random.seed(6)
o=''
o+='<rect x="0" y="22" width="100" height="84" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>'
for i in range(10): o+=f'<circle cx="{random.uniform(8,92):.1f}" cy="{random.uniform(30,98):.1f}" r="4.4" fill="#1f78c8"/>'
o+='<text x="50" y="120" class="t8 c b">1. população ancestral</text>'
o+='<path d="M106 64 H122" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
o+='<rect x="126" y="22" width="80" height="84" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/><path d="M166 22 L152 70 L170 106" class="nf" stroke="#8a5a2b" stroke-width="12" stroke-linecap="round" opacity=".75"/>'
for i in range(5): o+=f'<circle cx="{random.uniform(132,148):.1f}" cy="{random.uniform(32,96):.1f}" r="4.4" fill="#2f9e5a"/>'
for i in range(5): o+=f'<circle cx="{random.uniform(184,200):.1f}" cy="{random.uniform(32,96):.1f}" r="4.4" fill="#f2691b"/>'
o+='<text x="166" y="120" class="t8 c b">2. barreira geográfica</text><text x="166" y="130" class="t8 c g">e divergência</text>'
o+='<path d="M212 64 H228" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
o+='<rect x="232" y="22" width="100" height="84" rx="10" fill="#f4f6fb" stroke="#cfd6e3"/>'
for i in range(4): o+=f'<circle cx="{random.uniform(244,282):.1f}" cy="{random.uniform(34,94):.1f}" r="4.4" fill="#2f9e5a"/><circle cx="{random.uniform(286,322):.1f}" cy="{random.uniform(34,94):.1f}" r="4.4" fill="#f2691b"/>'
o+='<text x="284" y="68" class="t16 c b tx-vm">✕</text><text x="282" y="120" class="t8 c b">3. sem cruzamento</text><text x="282" y="130" class="t8 c g">= espécies distintas</text>'
open('src/svg/especiacao.svg','w').write(f'<svg viewBox="0 0 335 150">{o}</svg>')
# ---- homologia
o=''
def limb(x,name,sizes):
    g=f'<text x="{x+40}" y="122" class="t8 c b">{name}</text>'
    parts=[('úmero','#2f9e5a'),('rádio/ulna','#1f78c8'),('carpo','#7b43b8'),('metacarpos','#d19a00'),('falanges','#f2691b')]
    y=10
    for (n,c),h in zip(parts,sizes):
        g+=f'<rect x="{x+30}" y="{y}" width="20" height="{h}" rx="5" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
        y+=h+2
    return g
o+=limb(0,'humano',(26,28,8,16,18))+limb(104,'morcego',(14,22,6,22,28))+limb(208,'baleia',(12,14,8,10,10))
o+='<g transform="translate(262 22)" class="t7"></g>'
leg=[('úmero','#2f9e5a'),('rádio/ulna','#1f78c8'),('carpo','#7b43b8'),('metacarpos','#d19a00'),('falanges','#f2691b')]
for i,(n,c) in enumerate(leg): o+=f'<rect x="276" y="{14+i*13}" width="9" height="9" rx="2" fill="{c}"/><text x="289" y="{22+i*13}" class="t7">{n}</text>'
o+='<text x="0" y="138" class="t8 g">Mesmo plano ósseo, funções diferentes → ancestral comum.</text><text x="0" y="149" class="t8 g">Asa de ave × asa de inseto: análogas (mesma função).</text>'
open('src/svg/homologia.svg','w').write(f'<svg viewBox="0 0 335 156">{o}</svg>')
print('ok')
