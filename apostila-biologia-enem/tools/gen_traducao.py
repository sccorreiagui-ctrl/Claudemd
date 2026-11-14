o=''
# ---------- tradução ----------
cod=['AUG','GCU','UGG','AAA','UAA']
x0=118; sp=88; bw=76; y=150
o+=f'<text x="6" y="{y+4}" class="t9 xb tx-ro">mRNA</text><text x="6" y="{y+16}" class="t8 b tx-ro">5′</text><text x="{x0+5*sp+2}" y="{y+16}" class="t8 b tx-ro">3′</text>'
o+=f'<path d="M{x0-10} {y} H{x0+5*sp}" class="nf s-ro sw3"/>'
for i,c in enumerate(cod):
    x=x0+i*sp
    f='#f6dede' if c=='UAA' else '#ece0f8'
    o+=f'<rect x="{x}" y="{y-12}" width="{bw}" height="24" rx="5" fill="{f}" stroke="#4d2580" stroke-width="1.4"/>'
    for j,l in enumerate(c): o+=f'<text x="{x+14+j*24}" y="{y+5}" class="t12 c xb tx-ro">{l}</text>'
o+=f'<text x="{x0+4*sp+bw/2}" y="{y+28}" class="t8 c b tx-vm">códon de parada</text>'
o+=f'<text x="{x0+0*sp+bw/2}" y="{y+28}" class="t8 c b tx-ro">início (Met)</text>'
# ribossomo cobrindo códons 0..2
rx0=x0-8; rx1=x0+3*sp-12
o+=f'<path d="M{rx0} {y-30} Q{(rx0+rx1)/2} {y-110} {rx1} {y-30} Z" class="l-sl s-sl sw2" opacity=".95"/>'
o+=f'<path d="M{rx0+10} {y+22} Q{(rx0+rx1)/2} {y+66} {rx1-10} {y+22} Z" class="l-sl s-sl sw2" opacity=".95" style="display:none"/>'
o+=f'<text x="{rx1+6}" y="{y-60}" class="t9 xb tx-sl">subunidade maior</text><text x="{(rx0+rx1)/2}" y="{y+52}" class="t9 c xb tx-sl">subunidade menor</text>'
o+=f'<path d="M{rx0} {y+26} Q{(rx0+rx1)/2} {y+60} {rx1} {y+26}" class="nf s-sl sw3" />'
# sítios
for i,s in enumerate(['E','P','A']):
    xc=x0+i*sp+bw/2
    o+=f'<text x="{xc}" y="{y-34}" class="t9 c xb tx-sl">{s}</text>'
# tRNAs
def trna(i,anti,aa,col,label_aa,chain=None):
    xc=x0+i*sp+bw/2
    s=f'<rect x="{xc-6}" y="{y-86+30}" width="12" height="38" rx="3" fill="#dfe5ef" stroke="#475a73" stroke-width="1.4"/>'
    s+=f'<rect x="{xc-26}" y="{y-24}" width="52" height="16" rx="4" fill="#fff" stroke="#4d2580" stroke-width="1.4"/>'
    for j,l in enumerate(anti): s+=f'<text x="{xc-16+j*16}" y="{y-12}" class="t10 c xb tx-ro">{l}</text>'
    if aa:
        s+=f'<circle cx="{xc}" cy="{y-70}" r="11" fill="{col}"/><text x="{xc}" y="{y-67}" class="t8 c b w">{label_aa}</text>'
    return s
# E: tRNA-Met saindo (sem aa), anticódon UAC
o+=trna(0,'UAC',False,'','')
# P: Ala com cadeia Met
o+=trna(1,'CGA',True,'#f2691b','Ala')
xp=x0+1*sp+bw/2
o+=f'<circle cx="{xp-26}" cy="{y-92}" r="10" fill="#d4287c"/><text x="{xp-26}" y="{y-89}" class="t7 c b w">Met</text><path d="M{xp-16} {y-90} L{xp-10} {y-79}" class="nf s-k sw2"/>'
# A: Trp
o+=trna(2,'ACC',True,'#2f9e5a','Trp')
o+=f'<path d="M{x0+2*sp+bw/2-22} {y-104} q-20 -10 -30 -6" class="nf" style="display:none"/>'
# setas
o+=f'<path d="M{x0+2*sp+bw/2+34} {y-50} L{x0+2*sp+bw/2+60} {y-50}" class="nf s-ro sw2" marker-end="url(#ar-ro)" style="display:none"/>'
o+=f'<path d="M{x0+3*sp-4} {y+44} H{x0+4*sp+40}" class="nf s-ro sw3" marker-end="url(#ar-ro)"/><text x="{x0+3*sp+30}" y="{y+58}" class="t8 b tx-ro">o ribossomo avança 1 códon</text>'
# legenda
o+='<g transform="translate(520 20)"><text x="0" y="0" class="t9 xb tx-ro">Passo a passo</text>'
steps=['1. iniciação: AUG + Met','2. tRNA com anticódon','   complementar entra no sítio A','3. ligação peptídica:','   cadeia passa ao tRNA do A','4. translocação (E–P–A)','5. UAA/UAG/UGA: terminação']
for k,t in enumerate(steps): o+=f'<text x="0" y="{16+k*12}" class="t8">{t}</text>'
o+='</g>'
o+=f'<text x="6" y="14" class="t10 xb tx-ro">códon (mRNA)  ⟷  anticódon (tRNA): antiparalelos e complementares</text>'
open('src/svg/traducao.svg','w').write(f'<svg viewBox="0 0 690 232">{o}</svg>')

# ---------- mutações ----------
aa={'AUG':'Met','GCU':'Ala','GCC':'Ala','UGG':'Trp','AAA':'Lys','GAA':'Glu','UAA':'Pare','UGA':'Pare','CGC':'Arg','UUG':'Leu','AUA':'Ile'}
rows=[
 ('Normal',['AUG','GCU','UGG','AAA','UAA'],[],[],'proteína normal: Met–Ala–Trp–Lys','#475a73'),
 ('Silenciosa',['AUG','GCC','UGG','AAA','UAA'],[(1,2)],[],'mesmo aminoácido (código degenerado)','#2f9e5a'),
 ('Missense',['AUG','GCU','UGG','GAA','UAA'],[(3,0)],[3],'1 aminoácido trocado: efeito varia','#d19a00'),
 ('Nonsense',['AUG','GCU','UGA','AAA','UAA'],[(2,2)],[2],'parada precoce: proteína truncada','#d83a3a'),
 ('Frameshift',['AUG','CGC','UUG','GAA','AUA'],[(1,0)],[1,2,3,4],'inserção de 1 base: quadro de leitura muda','#d83a3a'),
]
o=''
o+='<text x="0" y="12" class="t9 xb tx-ro">Sequência: mRNA</text><text x="470" y="12" class="t9 xb tx-ro">Consequência</text>'
y=26
for name,codons,chg,hl,eff,colr in rows:
    o+=f'<rect x="0" y="{y}" width="690" height="38" rx="6" class="f-w s-g sw1"/><rect x="0" y="{y}" width="6" height="38" rx="3" fill="{colr}"/>'
    o+=f'<text x="14" y="{y+16}" class="t10 xb" style="fill:{colr}">{name}</text>'
    for i,c in enumerate(codons):
        x=118+i*68
        fill='#fbe0e0' if (i in hl) else '#ece0f8'
        o+=f'<rect x="{x}" y="{y+5}" width="62" height="19" rx="4" fill="{fill}" stroke="#4d2580" stroke-width="1"/>'
        for j,l in enumerate(c):
            red = any(ci==i and cj==j for ci,cj in chg)
            o+=f'<text x="{x+12+j*19}" y="{y+19}" class="t11 c xb" style="fill:{"#d83a3a" if red else "#4d2580"}">{l}</text>'
        o+=f'<text x="{x+31}" y="{y+34}" class="t8 c b" style="fill:{"#8e1c1c" if (i in hl) else "#2b3550"}">{aa.get(c,"…")}</text>'
    words=eff.split(' ');l1='';l2=''
    for w in words:
        if len(l1)+len(w)<34 and not l2: l1+=(' ' if l1 else '')+w
        else: l2+=(' ' if l2 else '')+w
    o+=f'<text x="470" y="{y+16}" class="t8 b">{l1}</text><text x="470" y="{y+28}" class="t8 b g">{l2}</text>'
    y+=44
o+=f'<text x="0" y="{y+4}" class="t8 g">Bases em vermelho = alteradas. No frameshift, todos os códons seguintes mudam (…Met–Arg–Leu–Glu–Ile…).</text>'
open('src/svg/mutacoes.svg','w').write(f'<svg viewBox="0 0 690 {y+10}">{o}</svg>')
print('ok')
