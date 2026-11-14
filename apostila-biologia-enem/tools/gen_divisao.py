import math
MAT='#5b2c91'; PAT='#b99be0'
def chrom(cx,cy,L,col,dup=False,rot=0,patch=None,w=5.4):
    g=f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot})">'
    offs=[-w*0.68,w*0.68] if dup else [0]
    for k,dx in enumerate(offs):
        c=col
        g+=f'<rect x="{dx-w/2}" y="{-L/2}" width="{w}" height="{L}" rx="2.6" fill="{c}" stroke="#2c1650" stroke-width=".7"/>'
        if patch and dup and patch[0]==k:
            g+=f'<rect x="{dx-w/2}" y="{0}" width="{w}" height="{L/2-1.5}" rx="2" fill="{patch[1]}" stroke="#2c1650" stroke-width=".7"/>'
    if dup: g+=f'<circle cx="0" cy="0" r="2" fill="#fff" stroke="#2c1650" stroke-width=".7"/>'
    return g+'</g>'
def cell(cx,cy,r=34,fill='#fff'):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="#4d2580" stroke-width="1.8"/>'
def lab(x,y,t1,t2=None,t3=None):
    s=f'<text x="{x}" y="{y}" class="t9 c xb tx-ro">{t1}</text>'
    if t2: s+=f'<text x="{x}" y="{y+11}" class="t8 c g">{t2}</text>'
    if t3: s+=f'<text x="{x}" y="{y+21}" class="t8 c g">{t3}</text>'
    return s
LL,LS=24,15
def wrap(o,S,cx,y,k=1.3): return o[:S]+f'<g transform="translate({cx} {y}) scale({k}) translate({-cx} {-y})">'+o[S:]+'</g>'
o=''
sp=115; X=[58+i*sp for i in range(6)]
# ---------- MITOSE ----------
y=74
o+='<text x="0" y="14" class="t11 xb tx-ro">MITOSE (2n → 2n): 1 célula → 2 células geneticamente idênticas</text>'
# M1 G1
S=len(o);cx=X[0];o+=cell(cx,y)
for (dx,dy,L,c,rot) in [(-11,-9,LL,MAT,15),(8,-10,LL,PAT,-10),(-9,13,LS,MAT,-20),(10,12,LS,PAT,25)]: o+=chrom(cx+dx,y+dy,L,c,False,rot)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'G1','4 cromossomos','4 cromátides')
# M2 G2
S=len(o);cx=X[1];o+=cell(cx,y)
for (dx,dy,L,c,rot) in [(-12,-9,LL,MAT,15),(10,-10,LL,PAT,-10),(-9,13,LS,MAT,-20),(11,12,LS,PAT,25)]: o+=chrom(cx+dx,y+dy,L,c,True,rot)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'G2 (após S)','4 cromossomos','8 cromátides')
# M3 metáfase
S=len(o);cx=X[2];o+=cell(cx,y)
for dy_,(L,c) in zip([-20,-7,7,20],[(LL,MAT),(LL,PAT),(LS,MAT),(LS,PAT)]):
    o+=f'<line x1="{cx-30}" y1="{y}" x2="{cx}" y2="{y+dy_}" stroke="#98a2b6" stroke-width=".8"/><line x1="{cx+30}" y1="{y}" x2="{cx}" y2="{y+dy_}" stroke="#98a2b6" stroke-width=".8"/>'
    o+=chrom(cx,y+dy_,L,c,True,90)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Metáfase','no equador','4 crom. · 8 cromát.')
# M4 anáfase
S=len(o);cx=X[3];o+=cell(cx,y)
for sgn in (-1,1):
    for dy_,(L,c) in zip([-20,-7,7,20],[(LL,MAT),(LL,PAT),(LS,MAT),(LS,PAT)]):
        o+=chrom(cx+sgn*15,y+dy_,L,c,False,90)
o+=f'<path d="M{cx-9} {y} H{cx-27}" class="nf s-ro sw15" marker-end="url(#ar-ro)"/><path d="M{cx+9} {y} H{cx+27}" class="nf s-ro sw15" marker-end="url(#ar-ro)"/>'
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Anáfase','cromátides se separam','8 cromossomos')
# M5 telófase
S=len(o);cx=X[4]
for sgn in (-1,1):
    o+=cell(cx+sgn*20,y,19)
    for (dx,dy,L,c,rot) in [(-4,-4,LL*.5,MAT,10),(4,-4,LL*.5,PAT,-10),(-3,7,LS*.5,MAT,-15),(4,7,LS*.5,PAT,15)]: o+=chrom(cx+sgn*20+dx,y+dy,L,c,False,rot,w=3.6)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'2 células','2n = 4','4 crom. cada')
# nota final
o+=f'<g transform="translate({X[5]-50} {74-28})"><rect x="0" y="0" width="100" height="62" rx="8" class="l-ro"/><text x="50" y="18" class="t9 c xb tx-ro">Resultado</text><text x="50" y="31" class="t8 c">2 células</text><text x="50" y="42" class="t8 c">2n idênticas</text><text x="50" y="54" class="t8 c g">(crescimento, reparo)</text></g>'
# ---------- MEIOSE ----------
y=270
o+='<text x="0" y="198" class="t11 xb tx-ro">MEIOSE (2n → n): 1 célula → 4 células haploides geneticamente diferentes</text>'
# I1 prófase I
S=len(o);cx=X[0];o+=cell(cx,y)
o+=chrom(cx-7,y-11,LL,MAT,True,0,patch=(1,PAT))+chrom(cx+7,y-11,LL,PAT,True,0,patch=(0,MAT))
o+=chrom(cx-7,y+14,LS,MAT,True,0)+chrom(cx+7,y+14,LS,PAT,True,0)
o+=f'<text x="{cx+22}" y="{y-4}" class="t8 b tx-vm">X</text>'
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Prófase I','pareamento e','crossing-over')
# I2 metáfase I
S=len(o);cx=X[1];o+=cell(cx,y)
o+=f'<line x1="{cx-30}" y1="{y}" x2="{cx-8}" y2="{y-12}" stroke="#98a2b6" stroke-width=".8"/><line x1="{cx+30}" y1="{y}" x2="{cx+8}" y2="{y-12}" stroke="#98a2b6" stroke-width=".8"/><line x1="{cx-30}" y1="{y}" x2="{cx-8}" y2="{y+13}" stroke="#98a2b6" stroke-width=".8"/><line x1="{cx+30}" y1="{y}" x2="{cx+8}" y2="{y+13}" stroke="#98a2b6" stroke-width=".8"/>'
o+=chrom(cx-9,y-12,LL,MAT,True,90,patch=(1,PAT))+chrom(cx+9,y-12,LL,PAT,True,90,patch=(0,MAT))
o+=chrom(cx-9,y+13,LS,MAT,True,90)+chrom(cx+9,y+13,LS,PAT,True,90)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Metáfase I','homólogos pareados','no equador')
# I3 anáfase I
S=len(o);cx=X[2];o+=cell(cx,y)
o+=chrom(cx-15,y-10,LL,MAT,True,90,patch=(1,PAT))+chrom(cx-15,y+12,LS,PAT,True,90)
o+=chrom(cx+15,y-10,LL,PAT,True,90,patch=(0,MAT))+chrom(cx+15,y+12,LS,MAT,True,90)
o+=f'<path d="M{cx-5} {y} H{cx-25}" class="nf s-vm sw15" marker-end="url(#ar-vm)" style="display:none"/>'
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Anáfase I','homólogos se separam','(ainda duplicados)')
# I4 2 células n
S=len(o);cx=X[3]
for sgn,(c1,c2,p1) in ((-1,(MAT,PAT,(1,PAT))),(1,(PAT,MAT,(0,MAT)))):
    o+=cell(cx+sgn*20,y,19)
    o+=chrom(cx+sgn*20-4,y-3,LL*.55,c1,True,0,patch=p1,w=3.4)+chrom(cx+sgn*20+6,y+4,LS*.55,c2,True,0,w=3.4)
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Fim da meiose I','2 células · n = 2','duplicados')
# I5 anáfase II
S=len(o);cx=X[4]
for sgn,(c1,c2,p1) in ((-1,(MAT,PAT,(1,PAT))),(1,(PAT,MAT,(0,MAT)))):
    ccx=cx+sgn*22
    o+=cell(ccx,y,20)
    o+=chrom(ccx-5,y-12,LL*.5,c1,False,0,w=3.4)+chrom(ccx-5,y+12,LL*.5,c1,False,0,w=3.4,patch=None)
    o+=chrom(ccx+6,y-8,LS*.5,c2,False,0,w=3.4)+chrom(ccx+6,y+8,LS*.5,c2,False,0,w=3.4)
o+=f'<path d="M{cx-22} {y-4} V{y-17}" class="nf" style="display:none"/>'
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'Anáfase II','cromátides se separam','(como na mitose)')
# I6 4 células
S=len(o);cx=X[5]
pos=[(-18,-18),(18,-18),(-18,18),(18,18)]
combos=[(MAT,PAT,PAT),(MAT,PAT,None),(PAT,MAT,MAT),(PAT,MAT,None)]
for (dx,dy),(a,b,pt) in zip(pos,combos):
    o+=cell(cx+dx,y+dy,15)
    o+=chrom(cx+dx-4,y+dy,LL*.42,a,False,0,w=3,patch=None)+chrom(cx+dx+5,y+dy+1,LS*.42,b,False,0,w=3)
    if pt: o+=f'<rect x="{cx+dx-5.5}" y="{y+dy}" width="3" height="{LL*.21-1}" rx="1" fill="{pt}" stroke="#2c1650" stroke-width=".5"/>'
o=wrap(o,S,cx,y);o+=lab(cx,y+66,'4 células','n = 2','1 cromátide cada')
o+='<g transform="translate(6 362)"><rect x="0" y="0" width="12" height="12" rx="3" fill="#5b2c91"/><text x="18" y="10" class="t8">cromossomo de origem materna</text><rect x="170" y="0" width="12" height="12" rx="3" fill="#b99be0" stroke="#2c1650" stroke-width=".7"/><text x="188" y="10" class="t8">de origem paterna</text><text x="300" y="10" class="t8">trechos de cor trocada = crossing-over · o tamanho identifica o par</text></g>'
open('src/svg/divisao.svg','w').write(f'<svg viewBox="0 0 690 380">{o}</svg>')
print('ok')
