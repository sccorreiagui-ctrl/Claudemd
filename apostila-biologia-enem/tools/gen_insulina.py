o=''
def panel(i,body,title):
    x=i*138
    return f'<g transform="translate({x} 0)"><rect x="0" y="0" width="130" height="150" rx="8" class="f-w s-g sw1"/>{body}</g>'
RO='#7b43b8'; ROD='#4d2580'; RS='#d4287c'
# 1 célula humana
b='<circle cx="62" cy="70" r="46" fill="#fff" stroke="#1f78c8" stroke-width="2"/><circle cx="52" cy="62" r="22" class="l-ro s-ro sw2"/>'
b+='<path d="M38 62 q6 -10 12 0 t12 0 t8 -4" class="nf s-ro sw2 rc"/><rect x="52" y="56" width="12" height="7" rx="2" fill="#d4287c"/>'
b+='<path d="M66 72 q8 4 14 0 t14 4" class="nf s-ro sw2" style="display:none"/><path d="M68 76 C78 86 86 86 92 92" class="nf s-ro sw2 rc" marker-end="url(#ar-ro)"/>'
b+='<text x="62" y="124" class="t8 c b tx-ro">mRNA maduro</text><text x="62" y="135" class="t8 c g">da insulina → cDNA</text>'
b+='<text x="62" y="12" class="t8 c xb">célula humana</text>'
o+=panel(0,b,'')
# 2 plasmídio cortado
b=f'<path d="M62 30 A38 38 0 1 0 90 40" class="nf s-ro sw4"/>'
b+='<path d="M90 40 l6 -4 l-2 8 l6 -4" class="nf s-vm sw2"/><path d="M62 30 l-6 -4 l2 8 l-6 -4" class="nf s-vm sw2"/>'
b+='<text x="104" y="62" class="t16 c em">✂️</text>'
b+='<text x="62" y="72" class="t9 c xb tx-ro">plasmídio</text><text x="62" y="83" class="t8 c g">DNA circular</text>'
b+='<text x="62" y="124" class="t8 c b tx-vm">enzima de restrição</text><text x="62" y="135" class="t8 c g">corta (pontas coesivas)</text><text x="62" y="12" class="t8 c xb">bactéria</text>'
o+=panel(1,b,'')
# 3 recombinante
b='<path d="M62 30 A38 38 0 1 0 100 58" class="nf s-ro sw4"/><path d="M100 58 A38 38 0 0 0 82 34" class="nf" style="display:none"/>'
b+='<path d="M82 31 A38 38 0 0 1 102 54" stroke="#d4287c" stroke-width="7" fill="none"/>'
b+='<text x="62" y="68" class="t9 c xb tx-ro">plasmídio</text><text x="62" y="79" class="t9 c xb tx-ro">recombinante</text><text x="108" y="30" class="t8 b tx-rs">gene</text>'
b+='<text x="62" y="124" class="t8 c b tx-ro">DNA ligase</text><text x="62" y="135" class="t8 c g">sela o inserto (cDNA)</text><text x="62" y="12" class="t8 c xb">inserção</text>'
o+=panel(2,b,'')
# 4 transformação
b='<rect x="22" y="40" width="86" height="44" rx="22" fill="#e8f5ec" stroke="#2f9e5a" stroke-width="2"/><circle cx="48" cy="62" r="11" class="nf s-ro sw3"/><path d="M58 56 a4 4 0 1 1 0.1 0" class="nf" style="display:none"/><rect x="45" y="52" width="6" height="6" fill="#d4287c"/><path d="M92 62 h10 M84 52 q6 -6 12 0" class="nf s-ve sw1"/>'
b+='<path d="M14 24 L40 50" class="nf s-ro sw2" marker-end="url(#ar-ro)"/><circle cx="12" cy="22" r="6" class="nf s-ro sw2"/>'
b+='<text x="62" y="102" class="t8 c b tx-ve">E. coli</text><text x="62" y="124" class="t8 c b tx-ve">transformação</text><text x="62" y="135" class="t8 c g">+ seleção por antibiótico</text><text x="62" y="12" class="t8 c xb">hospedeira</text>'
o+=panel(3,b,'')
# 5 biorreator
b='<rect x="30" y="26" width="70" height="78" rx="12" class="l-az s-az sw2"/>'
import random
random.seed(5)
for _ in range(12): b+=f'<ellipse cx="{random.uniform(40,90):.0f}" cy="{random.uniform(40,96):.0f}" rx="5" ry="2.6" fill="#2f9e5a"/>'
for _ in range(6): b+=f'<circle cx="{random.uniform(40,90):.0f}" cy="{random.uniform(36,96):.0f}" r="2" fill="#d4287c"/>'
b+='<path d="M52 104 v10 M78 104 v10" class="nf s-g sw2"/>'
b+='<text x="62" y="124" class="t8 c b tx-rs">insulina humana</text><text x="62" y="135" class="t8 c g">cultivo, extração, purificação</text><text x="62" y="12" class="t8 c xb">biorreator</text>'
o+=panel(4,b,'')
for i in range(4):
    cx=i*138+130+4
    o+=f'<path d="M{cx-1} 76 H{cx+7}" class="nf s-k sw2" marker-end="url(#ar-k)"/>'
open('src/svg/insulina.svg','w').write(f'<svg viewBox="0 0 690 152">{o}</svg>')
# sticky ends
o='<text x="0" y="12" class="t9 xb tx-ro">Exemplo: EcoRI reconhece GAATTC (palíndromo) e corta entre G e A em cada fita, em posições deslocadas</text>'
top=['···','N','G','A','A','T','T','C','N','···']; bot=['···','N','C','T','T','A','A','G','N','···']
def seq(t,x0,y,cut=None,gap=0,over=None):
    r=''
    for i,c in enumerate(t):
        x=x0+i*26+(gap if (cut is not None and i>=cut) else 0)
        col='#d4287c' if (over and i in over) else '#4d2580'
        r+=f'<text x="{x}" y="{y}" class="t12 c xb" style="fill:{col}">{c}</text>'
    return r
o+='<text x="2" y="38" class="t8 b tx-ro">5′</text><text x="2" y="62" class="t8 b tx-ro">3′</text>'
o+=seq(top,30,38)+seq(bot,30,62)
for i in range(2,8): o+=f'<line x1="{30+i*26}" y1="42" x2="{30+i*26}" y2="50" class="nf s-g sw1"/>'
o+='<line x1="{0}" y1="26" x2="{0}" y2="44" class="nf s-vm sw3"/>'.format(30+3*26-13)
o+='<line x1="{0}" y1="56" x2="{0}" y2="74" class="nf s-vm sw3"/>'.format(30+7*26-13)
o+='<text x="300" y="38" class="t8 b tx-ro">3′</text><text x="300" y="62" class="t8 b tx-ro">5′</text>'
o+='<path d="M312 50 H350" class="nf s-k sw3" marker-end="url(#ar-k)"/><text x="331" y="42" class="t8 c b tx-vm">corte</text>'
o+='<text x="364" y="38" class="t8 b tx-ro">5′</text><text x="364" y="62" class="t8 b tx-ro">3′</text>'
o+=seq(top,392,38,cut=3,gap=34,over={3,4,5,6})
# sobras coesivas: destacar AATT na parte direita superior e CTTAA... na esquerda inferior
o+=seq(bot,392,62,cut=7,gap=34,over={3,4,5,6})
o+='<text x="364" y="90" class="t8 b tx-rs">extremidades coesivas (AATT): pareiam com</text><text x="364" y="101" class="t8 b tx-rs">qualquer fragmento cortado pela mesma enzima</text>'
open('src/svg/ecori.svg','w').write(f'<svg viewBox="0 0 690 108">{o}</svg>')
print('ok')
