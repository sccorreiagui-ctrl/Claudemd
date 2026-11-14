import math,random
random.seed(8)
o=''
X=[56,196,336,476,616]
Y=64
# 1 zigoto
cx=X[0];o+=f'<circle cx="{cx}" cy="{Y}" r="30" fill="#fff" stroke="#d4287c" stroke-width="2.4"/><circle cx="{cx}" cy="{Y}" r="10" class="l-ro s-ro sw2"/>'
o+=f'<text x="{cx}" y="{Y+52}" class="t9 c xb tx-rs">Zigoto</text><text x="{cx}" y="{Y+63}" class="t8 c g">fecundação na tuba</text><text x="{cx}" y="{Y+73}" class="t8 c g">uterina</text>'
# 2 clivagem
cx=X[1]
for dx,dy in ((-14,-14),(14,-14),(-14,14),(14,14)): o+=f'<circle cx="{cx+dx}" cy="{Y+dy}" r="14" fill="#fff" stroke="#d4287c" stroke-width="2"/><circle cx="{cx+dx}" cy="{Y+dy}" r="4" class="f-ro" opacity=".6"/>'
o+=f'<text x="{cx}" y="{Y+52}" class="t9 c xb tx-rs">Clivagem</text><text x="{cx}" y="{Y+63}" class="t8 c g">mitoses sem crescimento:</text><text x="{cx}" y="{Y+73}" class="t8 c g">células cada vez menores</text>'
# 3 mórula
cx=X[2]
pts=[]
for i in range(16):
    a=random.uniform(0,6.28);r=random.uniform(0,22);pts.append((cx+r*math.cos(a),Y+r*math.sin(a)))
for x,y in pts: o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#fff" stroke="#d4287c" stroke-width="1.6"/>'
o+=f'<text x="{cx}" y="{Y+52}" class="t9 c xb tx-rs">Mórula</text><text x="{cx}" y="{Y+63}" class="t8 c g">bola maciça de células</text><text x="{cx}" y="{Y+73}" class="t8 c g">(≈ 3º–4º dia)</text>'
# 4 blastocisto
cx=X[3]
for k in range(16):
    a=2*math.pi*k/16; o+=f'<circle cx="{cx+28*math.cos(a):.1f}" cy="{Y+28*math.sin(a):.1f}" r="6.4" fill="#fbdcec" stroke="#d4287c" stroke-width="1.6"/>'
for (dx,dy) in ((-8,-10),(2,-14),(-12,2),(0,0),(10,-6)): o+=f'<circle cx="{cx+dx}" cy="{Y+dy-4}" r="6" fill="#d4287c" opacity=".85"/>'
o+=f'<text x="{cx}" y="{Y+52}" class="t9 c xb tx-rs">Blastocisto</text><text x="{cx}" y="{Y+63}" class="t8 c g">trofoblasto (placenta) +</text><text x="{cx}" y="{Y+73}" class="t8 c g">massa celular interna (embrião)</text>'
o+=f'<text x="{cx}" y="{Y-36}" class="t8 c b tx-vm">implanta no endométrio (6º–7º dia)</text>'
# 5 gástrula
cx=X[4]
o+=f'<path d="M{cx-30} {Y-6} A30 30 0 0 0 {cx+30} {Y-6}" fill="none" stroke="#1f78c8" stroke-width="7" stroke-linecap="round"/>'
o+=f'<path d="M{cx-22} {Y-6} A22 22 0 0 0 {cx+22} {Y-6}" fill="none" stroke="#d83a3a" stroke-width="7" stroke-linecap="round"/>'
o+=f'<path d="M{cx-14} {Y-6} A14 14 0 0 0 {cx+14} {Y-6}" fill="none" stroke="#d19a00" stroke-width="7" stroke-linecap="round"/>'
o+=f'<text x="{cx}" y="{Y+52}" class="t9 c xb tx-rs">Gástrula</text><text x="{cx}" y="{Y+63}" class="t8 c g">gastrulação: 3 folhetos</text><text x="{cx}" y="{Y+73}" class="t8 c g">(≈ 3ª semana)</text>'
for i in range(4):
    x=X[i]+46; o+=f'<path d="M{x} {Y} H{x+40}" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
open('src/svg/embrio.svg','w').write(f'<svg viewBox="0 0 690 150">{o}</svg>')
print('ok')
