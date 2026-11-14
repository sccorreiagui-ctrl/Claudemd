import math
col={'A':'#d4287c','T':'#1f78c8','U':'#6bb3e8','C':'#2f9e5a','G':'#d19a00'}
comp={'A':'T','T':'A','C':'G','G':'C'}
o=''
# ---- DNA
o+='<text x="170" y="16" class="t12 c xb tx-ro">DNA</text><text x="170" y="28" class="t8 c g">dupla fita · desoxirribose · A, T, C, G</text>'
seq='ATCGA'
y0=48; step=34
for i,b in enumerate(seq):
    y=y0+i*step; xl=120; xr=220
    bb=comp[b]; hb=3 if b in 'CG' else 2
    o+=f'<rect x="{xl}" y="{y-8}" width="26" height="16" rx="3" fill="{col[b]}"/><text x="{xl+13}" y="{y+4}" class="t10 c b w">{b}</text>'
    o+=f'<rect x="{xr-26}" y="{y-8}" width="26" height="16" rx="3" fill="{col[bb]}"/><text x="{xr-13}" y="{y+4}" class="t10 c b w">{bb}</text>'
    for k in range(hb):
        o+=f'<line x1="{xl+28}" y1="{y-4+k*(8/(max(hb-1,1)))}" x2="{xr-28}" y2="{y-4+k*(8/(max(hb-1,1)))}" class="nf s-k sw1 dsh"/>' if hb>1 else ''
    # açúcar-fosfato
    o+=f'<circle cx="{xl-14}" cy="{y}" r="7" class="f-ro" opacity=".85"/><circle cx="{xr+14}" cy="{y}" r="7" class="f-ro" opacity=".85"/>'
o+=f'<path d="M106 {y0} V{y0+4*step}" class="nf s-ro sw3"/><path d="M234 {y0} V{y0+4*step}" class="nf s-ro sw3"/>'
o+=f'<text x="92" y="{y0-12}" class="t8 b tx-ro e">5′</text><text x="92" y="{y0+4*step+16}" class="t8 b tx-ro e">3′</text><text x="248" y="{y0-12}" class="t8 b tx-ro">3′</text><text x="248" y="{y0+4*step+16}" class="t8 b tx-ro">5′</text>'
o+='<text x="168" y="226" class="t8 c b">A=T (2 ligações de H) · C≡G (3)</text><text x="168" y="237" class="t8 c g">fitas antiparalelas e complementares</text>'
# ---- RNA
o+='<g transform="translate(350 0)"><text x="170" y="16" class="t12 c xb tx-ro">RNA</text><text x="170" y="28" class="t8 c g">fita simples · ribose · A, U, C, G</text>'
seq2='AUCGA'
for i,b in enumerate(seq2):
    y=y0+i*step; xl=150
    o+=f'<rect x="{xl}" y="{y-8}" width="26" height="16" rx="3" fill="{col[b]}"/><text x="{xl+13}" y="{y+4}" class="t10 c b w">{b}</text>'
    o+=f'<circle cx="{xl-14}" cy="{y}" r="7" class="f-ro" opacity=".85"/>'
o+=f'<path d="M136 {y0} V{y0+4*step}" class="nf s-ro sw3"/><text x="122" y="{y0-12}" class="t8 b tx-ro e">5′</text><text x="122" y="{y0+4*step+16}" class="t8 b tx-ro e">3′</text>'
o+='<text x="190" y="104" class="t8 b tx-ro">bases voltadas p/ fora:</text><text x="190" y="115" class="t8 g">pareiam com outras fitas</text><text x="190" y="126" class="t8 g">(códon–anticódon)</text>'
o+='<text x="168" y="226" class="t8 c b">U (uracila) no lugar de T</text><text x="168" y="237" class="t8 c g">muitas formas: mRNA, tRNA, rRNA</text></g>'
# legenda: nucleotídeo
o+='<g transform="translate(262 40)"><text x="0" y="0" class="t9 xb tx-ro">Nucleotídeo</text><circle cx="10" cy="22" r="8" class="f-ro" opacity=".85"/><text x="10" y="25" class="t7 c b w">P</text><polygon points="40,12 52,20 48,34 32,34 28,20" fill="#fff" stroke="#4d2580" stroke-width="1.6"/><rect x="62" y="14" width="26" height="16" rx="3" fill="#d4287c"/><text x="75" y="26" class="t9 c b w">base</text><path d="M18 22 H27 M52 24 H60" class="nf s-ro sw2"/><text x="0" y="52" class="t8">fosfato + pentose + base</text></g>'
open('src/svg/dnarna.svg','w').write(f'<svg viewBox="0 0 690 246">{o}</svg>')
print('ok')
