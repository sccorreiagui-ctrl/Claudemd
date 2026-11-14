import random
random.seed(3)
W=690;H=290
o=''
# fundo aquoso
o+=f'<rect x="0" y="0" width="470" height="{H}" rx="8" class="l-az"/>'
o+='<rect x="0" y="77" width="470" height="106" class="l-am" opacity=".85"/>'
o+='<text x="10" y="18" class="t9 xb tx-az">MEIO EXTRACELULAR (aquoso)</text><text x="10" y="278" class="t9 xb tx-az">CITOSOL (aquoso)</text>'
o+='<text x="350" y="134" class="t8 xb tx-am c">núcleo apolar</text><text x="350" y="144" class="t7 b tx-am c">(hidrofóbico)</text>'
skip=[(142,198),(238,308),(392,440)]
def inskip(x): return any(a-6<=x<=b+6 for a,b in skip)
def unit(x,top,kink):
    yh=72 if top else 188
    d=1 if top else -1
    g=f'<circle cx="{x}" cy="{yh}" r="5.6" class="f-az"/>'
    for dx in (-2.6,2.6):
        k = kink and dx>0
        y0=yh+d*5.6
        if k:
            path=f'M{x+dx} {y0} V{y0+d*16} L{x+dx+4} {y0+d*23} L{x+dx} {y0+d*30} V{y0+d*50}'
        else:
            path=f'M{x+dx} {y0} V{y0+d*50}'
        g+=f'<path d="{path}" class="nf s-am sw15 rc" stroke-width="1.8"/>'
    return g
xs=[x for x in range(30,462,13)]
for i,x in enumerate(xs):
    if not inskip(x): o+=unit(x,True,i%4==1)
for i,x in enumerate(xs):
    xx=x+6
    if not inskip(xx): o+=unit(xx,False,i%4==2)
# colesterol
def chol(x,top):
    y=100 if top else 160
    ytop=y-12
    return (f'<g><rect x="{x-3.5}" y="{ytop}" width="7" height="26" rx="3" fill="#f0cf6a" stroke="#7d5a00" stroke-width="1"/>'
            f'<circle cx="{x}" cy="{ytop if top else ytop+26}" r="2.6" class="f-az"/></g>')
for x in (60,112,214,330,372,452): o+=chol(x,True)
for x in (80,128,222,344,386,430): o+=chol(x,False)
# proteínas
def prot(x0,x1,fill='#dfe5ef',stroke='#475a73'):
    return f'<rect x="{x0}" y="62" width="{x1-x0}" height="136" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
# canal: duas metades com poro
o+=f'<path d="M142 62 H162 V198 H142 Q134 198 134 190 V70 Q134 62 142 62Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.6"/>'
o+=f'<path d="M178 62 H198 Q206 62 206 70 V190 Q206 198 198 198 H178Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.6"/>'
o+='<rect x="162" y="62" width="16" height="136" class="l-az"/>'
o+='<circle cx="170" cy="48" r="6" class="f-ro" opacity="0"/>'
o+='<g><circle cx="170" cy="40" r="7" fill="#fff" stroke="#1f78c8" stroke-width="1.4"/><text x="170" y="43" class="t7 c b tx-az">Na⁺</text></g><path d="M170 50 V212" class="nf s-az sw2 dsh" marker-end="url(#ar-az)"/>'
# carreadora integral
o+='<path d="M250 62 H296 Q306 62 306 72 V188 Q306 198 296 198 H250 Q240 198 240 188 V72 Q240 62 250 62Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.6"/>'
o+='<path d="M258 62 Q273 96 288 62" fill="#c3d0e6" stroke="#475a73" stroke-width="1.2"/><text x="273" y="136" class="t8 c b" style="fill:#2c3b50">integral</text><text x="273" y="147" class="t8 c" style="fill:#2c3b50">(transporte)</text>'
# periférica (face citoplasmática)
o+='<ellipse cx="342" cy="206" rx="26" ry="11" fill="#c3d0e6" stroke="#475a73" stroke-width="1.4"/><text x="342" y="209" class="t7 c b" style="fill:#2c3b50">periférica</text>'
# glicoproteína
o+='<path d="M398 62 H432 Q440 62 440 70 V190 Q440 198 432 198 H398 Q392 198 392 190 V70 Q392 62 398 62Z" fill="#dfe5ef" stroke="#475a73" stroke-width="1.6"/>'
o+='<path d="M414 62 V44 M414 44 L402 32 M414 44 L426 32 M414 50 L404 46" class="nf s-ro sw15 rc"/><g class="f-ro"><circle cx="402" cy="30" r="3.4"/><circle cx="426" cy="30" r="3.4"/><circle cx="404" cy="46" r="3"/><circle cx="414" cy="42" r="3"/></g>'
o+='<text x="414" y="120" class="t8 c b" style="fill:#2c3b50">glico-</text><text x="414" y="131" class="t8 c b" style="fill:#2c3b50">proteína</text>'
# O2 atravessando
o+='<g><circle cx="86" cy="38" r="7" class="f-la"/><text x="86" y="41" class="t7 c b w">O₂</text></g><path d="M86 48 V214" class="nf s-la sw2 dsh" marker-end="url(#ar-la)"/>'
o+='<g><circle cx="200" cy="228" r="6" fill="#fff" stroke="#475a73" stroke-width="1.2"/></g>'
# números
nums=[(452,58,'1'),(24,108,'2'),(30,100,''),(112,86,'3'),(170,230,'4'),(342,224,'5'),(414,214,'6'),(86,236,'7')]
def badge(x,y,t): return f'<circle cx="{x}" cy="{y}" r="8.5" class="f-vm"/><text x="{x}" y="{y+3.2}" class="t9 c b w">{t}</text>'
o+=badge(448,56,'1')+badge(20,118,'2')+badge(66,126,'3')+badge(170,236,'4')+badge(342,232,'5')+badge(414,214,'6')+badge(86,240,'7')+badge(274,170,'8')
# legenda
leg=[('1','Cabeça polar (fosfato): hidrofílica, voltada à água'),('2','Caudas de ácidos graxos: apolares, hidrofóbicas; a dobra (insaturação) aumenta a fluidez'),('3','Colesterol (célula animal): “amortecedor” térmico da fluidez'),('4','Proteína integral em canal: íons e moléculas polares'),('5','Proteína periférica (face interna): sinalização e ancoragem'),('6','Glicoproteína → glicocálix: reconhecimento celular'),('7','O₂, CO₂ e lipossolúveis: difusão simples pela bicamada'),('8','Proteína integral transportadora')]
y=20
for n,t in leg:
    o+=f'<circle cx="490" cy="{y}" r="8" class="f-vm"/><text x="490" y="{y+3.2}" class="t9 c b w">{n}</text>'
    words=t.split(' ');lines=[];cur=''
    for w in words:
        if len(cur)+len(w)+1>40: lines.append(cur);cur=w
        else: cur=(cur+' '+w).strip()
    lines.append(cur)
    for j,l in enumerate(lines): o+=f'<text x="506" y="{y+3+j*10.5}" class="t8">{l}</text>'
    y+=max(1,len(lines))*10.5+13
open('src/svg/bicamada.svg','w').write(f'<svg viewBox="0 0 {W} {H}">{o}</svg>')
