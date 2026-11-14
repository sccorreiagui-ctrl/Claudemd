import math
R=21
nodes={'capim':(90,205,'🌾','ve','capim'),'sem':(245,205,'🌰','ve','sementes'),'gaf':(50,140,'🦗','sl','gafanhoto'),'rato':(205,140,'🐀','sl','rato'),
'sapo':(50,75,'🐸','sl','sapo'),'cobra':(255,75,'🐍','sl','cobra'),'gav':(150,24,'🦅','sl','gavião')}
edges=[('capim','gaf'),('capim','rato'),('sem','rato'),('gaf','sapo'),('rato','cobra'),('sapo','cobra'),('sapo','gav'),('cobra','gav'),('rato','gav')]
o=''
for a,b in edges:
    x1,y1=nodes[a][:2];x2,y2=nodes[b][:2];d=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/d,(y2-y1)/d
    o+=f'<line x1="{x1+ux*(R+2):.1f}" y1="{y1+uy*(R+2):.1f}" x2="{x2-ux*(R+5):.1f}" y2="{y2-uy*(R+5):.1f}" class="nf s-k sw15 rc" marker-end="url(#ar-k)"/>'
for k,(x,y,e,c,l) in nodes.items():
    o+=f'<circle cx="{x}" cy="{y}" r="{R}" class="f-w s-{c} sw3"/><text x="{x}" y="{y+9}" class="t20 c em">{e}</text>'
    if k=='gav': o+=f'<text x="{x+R+6}" y="{y+3}" class="t8 g">{l}</text>'
    else: o+=f'<text x="{x}" y="{y+R+11}" class="t8 c g">{l}</text>'
# legendas de nível
o+='<g class="t8 b"><text x="305" y="209" class="e tx-ve">produtores</text><text x="305" y="144" class="e g" style="display:none"></text></g>'
open('src/svg/teia.svg','w').write(f'<svg viewBox="0 0 332 246">{o}</svg>')
