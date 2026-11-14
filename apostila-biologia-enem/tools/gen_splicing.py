RO='#7b43b8'; RL='#c9a6f0'
def box(x,y,w,h,fill,stroke,label='',dash=False,tc='#fff'):
    d=' stroke-dasharray="4 3"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{d}/><text x="{x+w/2}" y="{y+h/2+4}" class="t9 c xb" style="fill:{tc}">{label}</text>'
# ----- splicing -----
o=''
x0=150
segs=[('prom',46,'#98a2b6','#475a73','promotor','#fff'),('E1',58,RO,'#4d2580','éxon 1','#fff'),('I1',74,'#e9edf4','#98a2b6','íntron 1','#475a73'),('E2',58,RO,'#4d2580','éxon 2','#fff'),('I2',56,'#e9edf4','#98a2b6','íntron 2','#475a73'),('E3',58,RO,'#4d2580','éxon 3','#fff')]
def row(y,withprom,tag,label,sub):
    r=f'<text x="0" y="{y+14}" class="t9 xb tx-ro">{label}</text><text x="0" y="{y+26}" class="t8 g">{sub}</text>'
    x=x0
    for k,w,f,s,l,tc in segs:
        if k=='prom' and not withprom: x+=0; continue
        r+=box(x,y,w,22,f,s,l,dash=(k in ('I1','I2')),tc=tc); x+=w+4
    return r
o+=row(14,True,'dna','DNA do gene','(eucarionte)')
o+=f'<path d="M{x0+120} 42 V54" class="nf s-ro sw3" marker-end="url(#ar-ro)"/><text x="{x0+128}" y="52" class="t8 b tx-ro">transcrição</text>'
# pré-mRNA
y=78
o+=f'<text x="0" y="{y+14}" class="t9 xb tx-ro">pré-mRNA</text><text x="0" y="{y+26}" class="t8 g">núcleo: éxons + íntrons</text>'
o+=f'<circle cx="{x0-8}" cy="{y+11}" r="6" class="f-rs"/><text x="{x0-8}" y="{y+4}" class="t7 c b tx-rs" style="display:none"></text>'
x=x0
for k,w,f,s,l,tc in segs[1:]:
    o+=box(x,y,w,22,f,s,l,dash=(k in ('I1','I2')),tc=tc); x+=w+4
o+=f'<text x="{x+6}" y="{y+16}" class="t10 xb tx-ro">AAAA</text>'
o+=f'<path d="M{x0+120} 104 V118" class="nf s-ro sw3" marker-end="url(#ar-ro)"/><text x="{x0+128}" y="116" class="t8 b tx-ro">splicing: íntrons removidos, éxons unidos</text>'
# mRNA maduro
y=126
o+=f'<text x="0" y="{y+14}" class="t9 xb tx-ro">mRNA maduro</text><text x="0" y="{y+26}" class="t8 g">vai ao citoplasma</text>'
o+=f'<circle cx="{x0-8}" cy="{y+11}" r="6" class="f-rs"/>'
x=x0
for k,w,f,s,l,tc in (segs[1],segs[3],segs[5]):
    o+=box(x,y,w,22,f,s,l,tc=tc); x+=w+2
o+=f'<text x="{x+6}" y="{y+16}" class="t10 xb tx-ro">AAAA</text><text x="{x+60}" y="{y+16}" class="t8 b tx-rs">+ cap 5′ e cauda poli-A: protegem o mRNA</text>'
open('src/svg/splicing.svg','w').write(f'<svg viewBox="0 0 690 160">{o}</svg>')
# ----- cDNA -----
o=''
o+='<text x="0" y="12" class="t9 xb tx-ro">1. Primeira fita: transcriptase reversa (molde = mRNA)</text>'
o+=f'<circle cx="34" cy="38" r="6" class="f-rs"/><path d="M40 38 H430" class="nf s-ro sw4"/><text x="436" y="42" class="t10 xb tx-ro">AAAA</text><text x="60" y="28" class="t8 b tx-ro">mRNA maduro (só éxons)</text>'
o+='<path d="M430 48 H330" stroke="#c9a6f0" stroke-width="4" fill="none"/>'
o+='<path d="M430 54 H40" stroke="#c9a6f0" stroke-width="4" fill="none" stroke-dasharray="1 0" style="display:none"/>'
o+='<path d="M424 52 H60" stroke="#c9a6f0" stroke-width="4" fill="none" marker-end="url(#ar-ro)"/>'
o+='<text x="430" y="70" class="t8 b tx-rs">primer oligo-dT (TTTT)</text><text x="62" y="68" class="t8 b tx-ro">cDNA fita simples (complementar ao mRNA)</text>'
o+='<text x="560" y="40" class="t8 b tx-ro">Transcriptase reversa:</text><text x="560" y="51" class="t8 g">enzima de retrovírus (HIV)</text><text x="560" y="62" class="t8 g">RNA → DNA</text>'
o+='<text x="0" y="96" class="t9 xb tx-ro">2. Degrada-se o mRNA e DNA polimerase faz a segunda fita</text>'
o+='<path d="M60 114 H430" stroke="#c9a6f0" stroke-width="4" fill="none"/><path d="M60 124 H430" stroke="#7b43b8" stroke-width="4" fill="none"/>'
o+='<text x="436" y="120" class="t9 xb tx-ro">cDNA dupla-fita</text><text x="436" y="131" class="t8 g">sem íntrons · pronto para clonar no plasmídio</text>'
o+='<text x="0" y="148" class="t8 g">Para a clonagem do gene, o cDNA entra no plasmídio com enzimas de restrição e ligase (p. 24). A PCR pode amplificá-lo depois.</text>'
open('src/svg/cdna.svg','w').write(f'<svg viewBox="0 0 690 156">{o}</svg>')
# ----- PCR -----
o=''
def pan(i,title,temp,body):
    x=i*150
    return f'<g transform="translate({x} 0)"><rect x="0" y="0" width="142" height="130" rx="8" class="f-w s-g sw1"/><text x="71" y="14" class="t9 c xb tx-ro">{title}</text><text x="71" y="26" class="t8 c b tx-la">{temp}</text>{body}</g>'
b='<path d="M12 56 H130" class="nf s-ro sw4"/><path d="M12 70 H130" class="nf s-ro sw4"/><path d="M60 56 C70 56 76 44 90 40 H130" class="nf" style="display:none"/>'
b='<path d="M12 62 H58 Q68 62 76 48 L96 36 H130" class="nf s-ro sw4"/><path d="M12 72 H58 Q68 72 76 86 L96 98 H130" class="nf s-ro sw4"/><text x="71" y="118" class="t8 c g">fitas se separam</text>'
o+=pan(0,'1. Desnaturação','94–98 °C',b)
b='<path d="M12 40 H130" class="nf s-ro sw4"/><path d="M12 92 H130" class="nf s-ro sw4"/><rect x="26" y="48" width="24" height="7" rx="3" fill="#d4287c"/><rect x="92" y="78" width="24" height="7" rx="3" fill="#d4287c"/><text x="38" y="66" class="t7 c b tx-rs">primer</text><text x="104" y="74" class="t7 c b tx-rs" style="display:none"></text><text x="71" y="118" class="t8 c g">primers pareiam nas pontas</text>'
o+=pan(1,'2. Anelamento','50–65 °C',b)
b='<path d="M12 40 H130" class="nf s-ro sw4"/><path d="M12 92 H130" class="nf s-ro sw4"/><path d="M26 52 H124" stroke="#c9a6f0" stroke-width="4"/><path d="M16 80 H116" stroke="#c9a6f0" stroke-width="4"/><circle cx="84" cy="66" r="9" class="f-la"/><text x="84" y="69" class="t7 c b w">Taq</text><text x="71" y="118" class="t8 c g">polimerase estende (5′→3′)</text>'
o+=pan(2,'3. Extensão','72 °C',b)
# gráfico
o+='<g transform="translate(462 0)"><text x="0" y="12" class="t9 xb tx-ro">Amplificação exponencial</text>'
for n in range(6):
    h=4*2**n if n<5 else 4*2**n
    h=min(4*2**n,100)
    o+=f'<rect x="{n*30+4}" y="{118-h}" width="22" height="{h}" rx="2" fill="#7b43b8" opacity="{0.4+0.12*n:.2f}"/><text x="{n*30+15}" y="130" class="t8 c b">{n}</text><text x="{n*30+15}" y="{112-h}" class="t8 c b tx-ro">{2**n}</text>'
o+='<text x="190" y="144" class="t8 g e">nº de ciclos</text><text x="0" y="144" class="t8 g">cópias = 2ⁿ</text></g>'
open('src/svg/pcr.svg','w').write(f'<svg viewBox="0 0 690 150">{o}</svg>')
print('ok')
