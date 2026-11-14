import importlib.util,sys
spec=importlib.util.spec_from_file_location('gd','tools/gen_divisao.py')
src=open('tools/gen_divisao.py').read().split('LL,LS=24,15')[0]
ns={}
exec(src,ns)
chrom=ns['chrom'];cell=ns['cell'];MAT=ns['MAT'];PAT=ns['PAT']
def allele(x,y,t,col): return f'<text x="{x}" y="{y}" class="t9 c xb" style="fill:{col}">{t}</text>'
# ---------- crossing-over ----------
o=''
def chromatid(x,ytop,L,col,w=9):
    return f'<rect x="{x-w/2}" y="{ytop}" width="{w}" height="{L}" rx="4" fill="{col}" stroke="#2c1650" stroke-width=".8"/>'
L=96
# painel 1: antes
def panel1(ox):
    g=f'<g transform="translate({ox} 0)">'
    xs=[26,44,70,88]; cols=[MAT,MAT,PAT,PAT]
    for x,c in zip(xs,cols): g+=chromatid(x,30,L,c)
    g+='<circle cx="35" cy="78" r="4" fill="#fff" stroke="#2c1650"/><circle cx="79" cy="78" r="4" fill="#fff" stroke="#2c1650"/>'
    for x,c,(a,b) in zip(xs,cols,[('A','B')]*2+[('a','b')]*2):
        g+=f'<text x="{x}" y="46" class="t8 c b w">{a}</text><text x="{x}" y="124" class="t8 c b w">{b}</text>'
    g+='<text x="57" y="20" class="t9 c xb tx-ro">1. Pareamento</text><text x="57" y="156" class="t8 c g">homólogos formam</text><text x="57" y="166" class="t8 c g">um bivalente (tétrade)</text></g>'
    return g
def panel2(ox):
    g=f'<g transform="translate({ox} 0)">'
    g+=chromatid(26,30,L,MAT)+chromatid(44,30,L,MAT)+chromatid(70,30,L,PAT)+chromatid(88,30,L,PAT)
    g+='<path d="M44 96 C50 96 64 92 70 92" class="nf s-vm sw3"/><path d="M44 88 C52 88 62 96 70 96" class="nf s-vm sw3" style="display:none"/>'
    g+='<circle cx="57" cy="94" r="12" class="nf s-vm sw2 dsh"/><text x="57" y="132" class="t9 c xb tx-vm">quiasma</text>'
    g+='<text x="57" y="20" class="t9 c xb tx-ro">2. Crossing-over</text><text x="57" y="156" class="t8 c g">troca de segmentos entre</text><text x="57" y="166" class="t8 c g">cromátides NÃO-irmãs</text></g>'
    return g
def panel3(ox):
    g=f'<g transform="translate({ox} 0)">'
    # cromátides após: mat1 AB, mat2 (A top, b bottom), pat1 (a top, B bottom), pat2 ab
    xs=[26,44,70,88]
    g+=chromatid(26,30,L,MAT)
    g+=chromatid(44,30,48,MAT)+chromatid(44,78,48,PAT)
    g+=chromatid(70,30,48,PAT)+chromatid(70,78,48,MAT)
    g+=chromatid(88,30,L,PAT)
    labs=[('A','B'),('A','b'),('a','B'),('a','b')]
    for x,(a,b) in zip(xs,labs): g+=f'<text x="{x}" y="46" class="t8 c b w">{a}</text><text x="{x}" y="124" class="t8 c b" style="fill:{"#fff" if (x in (26,70)) else "#2c1650"}">{b}</text>'
    g+='<text x="57" y="20" class="t9 c xb tx-ro">3. Resultado</text><text x="26" y="142" class="t7 c b tx-ro">AB</text><text x="44" y="150" class="t7 c b tx-vm">Ab</text><text x="70" y="142" class="t7 c b tx-vm">aB</text><text x="88" y="150" class="t7 c b tx-ro">ab</text>'
    g+='<text x="57" y="166" class="t8 c g" style="font-size:7.5px">2 parentais · 2 recombinantes</text></g>'
    return g
o=panel1(0)+panel2(112)+panel3(224)
open('src/svg/crossing.svg','w').write(f'<svg viewBox="0 0 335 176">{o}</svg>')
# ---------- anáfase I x II ----------
o=''
def spind(cx,y,r):
    return f'<line x1="{cx-r}" y1="{y}" x2="{cx}" y2="{y-14}" stroke="#98a2b6" stroke-width=".9"/>'
y=100; r=62
# AI
cx=84
o+=cell(cx,y,r)
o+=f'<line x1="{cx-r+4}" y1="{y}" x2="{cx-34}" y2="{y-26}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx-r+4}" y1="{y}" x2="{cx-34}" y2="{y+24}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx+r-4}" y1="{y}" x2="{cx+34}" y2="{y-26}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx+r-4}" y1="{y}" x2="{cx+34}" y2="{y+24}" stroke="#98a2b6" stroke-width="1"/>'
o+=chrom(cx-30,y-26,44,MAT,True,90,patch=(1,PAT),w=8)+chrom(cx-30,y+24,28,PAT,True,90,w=8)
o+=chrom(cx+30,y-26,44,PAT,True,90,patch=(0,MAT),w=8)+chrom(cx+30,y+24,28,MAT,True,90,w=8)
o+=f'<path d="M{cx-10} {y} H{cx-22}" class="nf s-vm sw2" marker-end="url(#ar-vm)"/><path d="M{cx+10} {y} H{cx+22}" class="nf s-vm sw2" marker-end="url(#ar-vm)"/>'
o+=f'<text x="{cx}" y="16" class="t11 c xb tx-ro">ANÁFASE I</text><text x="{cx}" y="28" class="t8 c b tx-vm">separa HOMÓLOGOS</text>'
o+=f'<text x="{cx}" y="{y+r+16}" class="t8 c b">cada polo: 2 cromossomos</text><text x="{cx}" y="{y+r+27}" class="t8 c b">DUPLICADOS (4 cromátides)</text><text x="{cx}" y="{y+r+39}" class="t8 c g">célula-mãe 2n → n</text>'
# AII
cx=252
o+=cell(cx,y,r)
o+=f'<line x1="{cx-r+4}" y1="{y}" x2="{cx-30}" y2="{y-24}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx+r-4}" y1="{y}" x2="{cx+30}" y2="{y-24}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx-r+4}" y1="{y}" x2="{cx-30}" y2="{y+22}" stroke="#98a2b6" stroke-width="1"/><line x1="{cx+r-4}" y1="{y}" x2="{cx+30}" y2="{y+22}" stroke="#98a2b6" stroke-width="1"/>'
for sgn in (-1,1):
    o+=chrom(cx+sgn*30,y-24,44,MAT,False,90,w=8)+chrom(cx+sgn*30,y+22,28,PAT,False,90,w=8)
o+=f'<path d="M{cx-10} {y} H{cx-22}" class="nf s-vm sw2" marker-end="url(#ar-vm)"/><path d="M{cx+10} {y} H{cx+22}" class="nf s-vm sw2" marker-end="url(#ar-vm)"/>'
o+=f'<text x="{cx}" y="16" class="t11 c xb tx-ro">ANÁFASE II</text><text x="{cx}" y="28" class="t8 c b tx-vm">separa CROMÁTIDES-irmãs</text>'
o+=f'<text x="{cx}" y="{y+r+16}" class="t8 c b">cada polo: 2 cromossomos</text><text x="{cx}" y="{y+r+27}" class="t8 c b">SIMPLES (2 cromátides)</text><text x="{cx}" y="{y+r+39}" class="t8 c g">igual à anáfase da mitose (n)</text>'
open('src/svg/anafases.svg','w').write(f'<svg viewBox="0 0 335 232">{o}</svg>')
# ---------- segregação independente ----------
o=''
def icon(cx,y,orient):
    # orient 0: mat longo e mat curto do mesmo lado
    g=''
    cols=[(MAT,MAT),(MAT,PAT)][orient]
    # polo esquerdo: longo(mat) + curto(c0); direito: longo(pat) + curto(c1)
    top_left=MAT; 
    return g
def gam(cx,y,c1,c2):
    return cell(cx,y,14)+chrom(cx-4,y,16,c1,False,0,w=3.6)+chrom(cx+5,y+1,10,c2,False,0,w=3.6)
o+='<text x="0" y="12" class="t10 xb tx-ro">Orientação ao acaso → gametas diferentes</text>'
# orientação 1
o+=f'<text x="0" y="36" class="t9 b">Orientação 1:</text>'
o+=gam(120,32,MAT,MAT)+gam(150,32,PAT,PAT)+'<text x="176" y="36" class="t8">gametas A B  e  a b</text>'
o+=f'<text x="0" y="74" class="t9 b">Orientação 2:</text>'
o+=gam(120,70,MAT,PAT)+gam(150,70,PAT,MAT)+'<text x="176" y="74" class="t8">gametas A b  e  a B</text>'
o+='<text x="0" y="104" class="t8 g">Com n pares, há 2ⁿ combinações. Humano (n = 23): 2²³ ≈ 8,4 milhões</text><text x="0" y="115" class="t8 g">de gametas diferentes por pessoa — sem contar o crossing-over.</text>'
open('src/svg/indep.svg','w').write(f'<svg viewBox="0 0 335 124">{o}</svg>')
print('ok')
