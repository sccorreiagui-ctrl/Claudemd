RO='#7b43b8'; RL='#c9a6f0'
# ---------- CRISPR ----------
o=''
def strands(x0,x1,y,tgt=None,gap=None,pam=None):
    r=''
    def line(xa,xb,yy,col): return f'<path d="M{xa} {yy} H{xb}" stroke="{col}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
    if gap is None:
        r+=line(x0,x1,y,RO)+line(x0,x1,y+12,RO)
    else:
        a,b=gap
        r+=line(x0,a,y,RO)+line(b,x1,y,RO)+line(x0,a-6,y+12,RO)+line(b+6,x1,y+12,RO)
    return r
o+='<text x="0" y="12" class="t10 xb tx-ro">1. Reconhecimento</text>'
o+=strands(6,330,70)
o+='<rect x="96" y="63" width="118" height="22" rx="4" fill="none" stroke="#d4287c" stroke-width="2"/><text x="155" y="100" class="t8 c b tx-rs">sequência-alvo (≈ 20 nt)</text>'
o+='<rect x="218" y="63" width="34" height="22" rx="4" class="l-am s-am sw2"/><text x="235" y="100" class="t8 c b tx-am">PAM</text><text x="235" y="110" class="t7 c g">(NGG)</text>'
o+='<path d="M98 54 H214" stroke="#d4287c" stroke-width="4" fill="none"/><text x="156" y="46" class="t8 c b tx-rs">RNA-guia (complementar ao alvo)</text>'
o+='<ellipse cx="156" cy="72" rx="88" ry="38" class="nf s-sl sw2 dsh"/><text x="156" y="128" class="t9 c xb tx-sl">Cas9 (nuclease) + RNA-guia</text>'
o+='<text x="0" y="150" class="t8 g">O RNA-guia leva a Cas9 até a sequência complementar; o PAM adjacente é exigido.</text>'
o+='<g transform="translate(0 168)"><text x="0" y="0" class="t10 xb tx-ro">2. Corte nas duas fitas (quebra de fita dupla)</text>'
o+=strands(6,330,22,gap=(150,176))+'<text x="163" y="42" class="t14 c em">✂️</text><text x="163" y="68" class="t8 c b tx-vm">Cas9 corta a dupla-hélice</text></g>'
# painel direito
o+='<g transform="translate(360 0)"><text x="0" y="12" class="t10 xb tx-ro">3. A célula repara — e é aí que se edita</text>'
o+='<rect x="0" y="22" width="330" height="112" rx="8" class="l-vm s-vm sw1"/><text x="10" y="40" class="t9 xb tx-vm">a) Reparo sem molde (junção de extremidades)</text>'
o+=strands(10,320,56,gap=(150,174))
o+='<rect x="146" y="50" width="34" height="22" rx="3" fill="#fff" stroke="#d83a3a" stroke-width="1.6" stroke-dasharray="3 2"/><text x="163" y="64" class="t9 c b tx-vm">indel</text>'
o+='<text x="10" y="100" class="t8">Erros → pequenas inserções ou deleções → <tspan class="b tx-vm">gene inativado (knock-out)</tspan></text><text x="10" y="112" class="t8 g">útil para “desligar” um gene</text>'
o+='<rect x="0" y="142" width="330" height="112" rx="8" class="l-ve s-ve sw1"/><text x="10" y="160" class="t9 xb tx-ve">b) Reparo com molde de DNA fornecido</text>'
o+=strands(10,320,176)
o+='<rect x="140" y="170" width="46" height="22" rx="3" class="f-ve"/><text x="163" y="184" class="t8 c b w">novo trecho</text>'
o+='<text x="10" y="218" class="t8">Correção de uma mutação ou inserção de gene (<tspan class="b tx-ve">edição precisa</tspan>)</text><text x="10" y="230" class="t8 g">Ex.: terapia para anemia falciforme (p. 26)</text></g>'
open('src/svg/crispr.svg','w').write(f'<svg viewBox="0 0 690 262">{o}</svg>')
# ---------- antissentido ----------
o=''
o+='<text x="0" y="12" class="t9 xb tx-sl">Sem RNA antissentido</text>'
o+='<path d="M6 40 H320" stroke="#7b43b8" stroke-width="4.5" fill="none"/><text x="6" y="30" class="t8 b tx-ro">mRNA da poligalacturonase</text>'
o+='<ellipse cx="200" cy="30" rx="26" ry="8" class="f-sl"/><ellipse cx="200" cy="50" rx="18" ry="7" class="f-sl"/><text x="232" y="34" class="t8 b tx-sl">ribossomo</text><path d="M200 60 V68" class="nf s-la sw2" marker-end="url(#ar-la)"/><text x="6" y="78" class="t8 b tx-la">proteína (enzima) degrada a pectina da parede</text><text x="6" y="88" class="t8 b tx-la">→ fruto amolece e estraga</text>'
o+='<text x="0" y="102" class="t9 xb tx-rs">Com RNA antissentido (transgene invertido)</text>'
o+='<path d="M6 128 H320" stroke="#7b43b8" stroke-width="4.5" fill="none"/><path d="M6 138 H320" stroke="#d4287c" stroke-width="4.5" fill="none"/>'
o+='<text x="6" y="118" class="t8 b tx-ro">mRNA</text><text x="190" y="156" class="t8 b tx-rs">RNA antissentido (complementar)</text><text x="6" y="156" class="t8 b tx-ro">dupla fita de RNA</text>'
o+='<ellipse cx="200" cy="118" rx="26" ry="8" class="f-sl" opacity=".5"/><text x="258" y="106" class="t14 b tx-vm">✕</text><text x="244" y="118" class="t8 b tx-vm" style="display:none"></text>'
o+='<text x="6" y="176" class="t8 b tx-ve">tradução bloqueada → pouca enzima → fruto firme por mais tempo</text>'
open('src/svg/antissentido.svg','w').write(f'<svg viewBox="0 0 335 188">{o}</svg>')
# ---------- gel ----------
o=''
o+='<text x="2" y="12" class="t8 b tx-vm">− (cátodo)</text><text x="2" y="226" class="t8 b tx-az">+ (ânodo)</text>'
o+='<rect x="30" y="20" width="290" height="196" rx="6" fill="#e9eef5" stroke="#98a2b6" stroke-width="1.5"/>'
lanes=[('M',[50,76,102,128,154,180]),('Mãe',[76,128,180]),('Filho',[76,102,180]),('Pai 1',[102,154,180]),('Pai 2',[50,128,154])]
for i,(n,bands) in enumerate(lanes):
    x=56+i*54
    o+=f'<rect x="{x-14}" y="24" width="28" height="9" rx="2" fill="#475a73"/><text x="{x}" y="46" class="t8 c xb">{n}</text>'
    for y in bands:
        col='#1b2236' if n!='M' else '#7b8499'
        extra=''
        o+=f'<rect x="{x-13}" y="{y+8}" width="26" height="4" rx="1.5" fill="{col}"/>'
o+='<path d="M334 30 V210" class="nf s-az sw3" marker-end="url(#ar-az)"/>'
o+='<text x="336" y="100" class="t8 b tx-az" style="display:none"></text>'
# destaque banda do pai
o+='<rect x="{0}" y="{1}" width="170" height="12" rx="3" class="nf s-rs sw2" style="display:none"/>'.format(0,0)
o+='<rect x="{}" y="{}" width="30" height="10" rx="2" class="nf s-rs sw2"/>'.format(56+2*54-15,102+7)+'<rect x="{}" y="{}" width="30" height="10" rx="2" class="nf s-rs sw2"/>'.format(56+3*54-15,102+7)
o+='<text x="326" y="120" class="t8 b tx-rs e" style="display:none"></text>'
open('src/svg/gel.svg','w').write(f'<svg viewBox="0 0 350 232">{o}</svg>')
# ---------- mtDNA ----------
o=''
def sq(x,y,f): return f'<rect x="{x-11}" y="{y-11}" width="22" height="22" fill="{f}" stroke="#1b2236" stroke-width="1.6"/>'
def ci(x,y,f): return f'<circle cx="{x}" cy="{y}" r="11" fill="{f}" stroke="#1b2236" stroke-width="1.6"/>'
P='#7b43b8'; W='#fff'
o+=sq(110,30,W)+ci(170,30,P)+'<path d="M121 30 H159" class="nf s-k sw15"/>'
o+='<path d="M140 30 V56 M66 56 H214 M66 56 V74 M214 56 V74" class="nf s-k sw15"/>'
o+=ci(66,86,P)+sq(126,86,W)+'<path d="M77 86 H115" class="nf s-k sw15"/>'
o+=sq(214,86,P)+ci(274,86,W)+'<path d="M225 86 H263" class="nf s-k sw15"/>'
o+='<path d="M96 86 V112 M52 112 H112 M52 112 V128 M112 112 V128" class="nf s-k sw15"/>'
o+=ci(52,140,P)+sq(112,140,P)
o+='<path d="M244 86 V112 M200 112 H260 M200 112 V128 M260 112 V128" class="nf s-k sw15"/>'
o+=ci(200,140,W)+sq(260,140,W)
o+='<text x="8" y="24" class="t8 b tx-ro">avó</text><text x="8" y="90" class="t8 g">filha</text><text x="290" y="90" class="t8 g">filho</text><text x="150" y="178" class="t8 c b tx-ro">■ ● = carrega o mtDNA da avó materna</text>'
o+='<text x="82" y="168" class="t8 c b tx-ro">mãe → todos os filhos</text><text x="232" y="168" class="t8 c b tx-sl">pai → ninguém</text>'
open('src/svg/mtdna.svg','w').write(f'<svg viewBox="0 0 335 184">{o}</svg>')
print('ok')
