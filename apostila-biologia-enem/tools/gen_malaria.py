o=''
def box(x,y,w,h,n,t1,t2,col):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="{col}" stroke-width="1.8"/>'
    s+=f'<circle cx="{x+14}" cy="{y+h/2}" r="10" fill="{col}"/><text x="{x+14}" y="{y+h/2+3.5}" class="t10 c b w">{n}</text>'
    s+=f'<text x="{x+32}" y="{y+16}" class="t9 xb" style="fill:{col}">{t1}</text><text x="{x+32}" y="{y+28}" class="t8">{t2}</text>'
    return s
# humano (direita)
o+='<rect x="350" y="0" width="340" height="318" rx="10" class="l-vm" opacity=".55"/><text x="520" y="16" class="t11 c xb tx-vm">HOSPEDEIRO HUMANO</text><text x="520" y="28" class="t8 c g">fase assexuada (multiplicação por divisão)</text>'
H=[('1','Picada: esporozoítos no sangue','vão rapidamente ao fígado'),('2','Fígado (hepatócitos)','esquizogonia: multiplicação assexuada → merozoítos'),('3','Merozoítos invadem hemácias','crescimento: trofozoíto → esquizonte'),('4','Ruptura sincrônica das hemácias','libera merozoítos e toxinas: FEBRE periódica, anemia'),('5','Alguns viram gametócitos','formas sexuadas, infectantes para o mosquito')]
y=40
for n,t1,t2 in H:
    o+=box(362,y,316,46,n,t1,t2,'#d83a3a'); 
    if n!='5': o+=f'<path d="M520 {y+46} V{y+55}" class="nf s-vm sw2" marker-end="url(#ar-vm)"/>'
    y+=56
# mosquito (esquerda)
o+='<rect x="0" y="0" width="340" height="318" rx="10" class="l-sl" opacity=".7"/><text x="170" y="16" class="t11 c xb tx-sl">MOSQUITO <tspan style="font-style:italic">Anopheles</tspan> (fêmea)</text><text x="170" y="28" class="t8 c g">hospedeiro definitivo: fase sexuada</text>'
M=[('6','Ingere gametócitos','ao picar uma pessoa infectada'),('7','Fecundação no intestino','gametas → zigoto → oocisto'),('8','Esporozoítos nas glândulas salivares','prontos para infectar o próximo humano')]
ys=[236,180,124]
for (n,t1,t2),yy in zip(M,[236,164,92]):
    o+=box(10,yy,316,46,n,t1,t2,'#475a73')
o+='<path d="M170 236 V220" class="nf s-sl sw2" marker-end="url(#ar-sl)"/><path d="M170 164 V148" class="nf s-sl sw2" marker-end="url(#ar-sl)"/>'
# conexões
o+='<path d="M520 310 V326 H170 V284" class="nf s-vm sw3" marker-end="url(#ar-vm)"/><text x="344" y="338" class="t8 c b tx-vm">mosquito pica pessoa com gametócitos</text>'
o+='<path d="M170 92 V50 H350 C356 50 360 56 362 62" class="nf s-sl sw3" marker-end="url(#ar-sl)" style="display:none"/>'
o+='<path d="M170 92 V46 H358" class="nf s-sl sw3" marker-end="url(#ar-sl)"/><text x="260" y="40" class="t8 c b tx-sl">picada transmite esporozoítos</text>'
open('src/svg/malaria.svg','w').write(f'<svg viewBox="0 0 690 344">{o}</svg>')
print('ok')
