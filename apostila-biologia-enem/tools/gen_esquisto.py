o=''
o+='<rect x="190" y="0" width="300" height="236" rx="14" class="l-az"/><text x="340" y="14" class="t9 c xb tx-az">ÁGUA DOCE (lagoas, riachos, represas)</text>'
def node(x,y,w,h,emoji,t1,t2,col):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{col}" stroke-width="1.8"/>'
    s+=f'<text x="{x+26}" y="{y+h/2+10}" class="t26 c em">{emoji}</text><text x="{x+50}" y="{y+18}" class="t9 xb" style="fill:{col}">{t1}</text>'
    for i,l in enumerate(t2): s+=f'<text x="{x+50}" y="{y+30+i*10.5}" class="t8">{l}</text>'
    return s
o+=node(0,92,196,62,'🧍','Humano (hosp. definitivo)',['vermes adultos nas veias do','intestino/fígado: reprodução sexuada'],'#d83a3a')
o+=node(250,34,196,50,'🥚','Ovos → miracídios',['ovos saem nas fezes; eclodem na água;','larva ciliada nada'],'#2f9e5a')
o+=node(494,92,196,62,'🐌','Caramujo Biomphalaria',['hosp. intermediário: o parasita se','multiplica assexuadamente'],'#8a5a2b')
o+=node(250,170,196,56,'🏊','Cercárias',['larvas de cauda bifurcada saem do','caramujo e nadam'],'#7b43b8')
o+='<path d="M96 92 C120 60 200 56 248 56" class="nf s-ve sw3" marker-end="url(#ar-ve)"/><text x="116" y="62" class="t8 b tx-ve">① ovos</text>'
o+='<path d="M446 56 C500 56 560 70 590 90" class="nf s-ve sw3" marker-end="url(#ar-ve)"/><text x="510" y="58" class="t8 b tx-ve">② penetra no caramujo</text>'
o+='<path d="M590 156 C570 190 500 200 448 198" class="nf s-mr sw3" marker-end="url(#ar-mr)"/><text x="470" y="216" class="t8 b tx-mr">③ libera cercárias</text>'
o+='<path d="M250 200 C180 204 110 190 96 156" class="nf s-ro sw3" marker-end="url(#ar-ro)"/><text x="50" y="190" class="t8 b tx-ro">④ penetram a pele</text><text x="50" y="200" class="t8 g">ativamente (banho, lavagem)</text>'
open('src/svg/esquisto.svg','w').write(f'<svg viewBox="0 0 690 238">{o}</svg>')
print('ok')
