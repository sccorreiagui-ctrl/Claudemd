"""Acrescenta 'Item PAS comentado' e 'Treino rápido' a páginas com folga (executado uma vez; idempotente)."""
import os, re
PG = os.path.join(os.path.dirname(__file__), '..', 'content', 'pages')


def item(statements, gabarito, lv='N2', title='Itens PAS comentados'):
    st = '<br>'.join(f'<b>({chr(97+i)})</b> {s}' for i, s in enumerate(statements))
    return (f'<div class="exm xtra"><div class="eh"><span>{title}</span><span class="lv">{lv}</span><span class="fm ce">C/E</span><span class="r">autorais, no estilo da banca</span></div>'
            f'<div class="er"><div class="l">Julgue</div><div>{st}</div></div>'
            f'<div class="er res"><div class="l">Gabarito</div><div>{gabarito}</div></div></div>\n')


def treino(items):
    cells = ''.join(f'<div>{a} <b class="cg">→ {b}</b></div>' for a, b in items)
    return (f'<div class="box pre xtra"><div class="bt">Treino rápido · sem numeração · confira com a resposta ao lado</div>'
            f'<div class="g3 sm" style="gap:.8mm 4mm">{cells}</div></div>\n')


X = {}
X[2] = treino([('$i^{33}$', '$i$'), ('$i^{50}$', '$-1$'), ('$i^{2024}$', '$1$'), ('$i^{-2}$', '$-1$'), ('$i^5+i^6+i^7+i^8$', '$0$'), ('$(i^2)^3$', '$-1$')])
X[3] = item(['A parte imaginária de $z=4-7i$ é $-7i$.', 'O número $0$ é, ao mesmo tempo, real e imaginário puro.'],
            '<b>(a) Errado:</b> $\\Imp(z)=-7$ (um número real); o $i$ não faz parte dela. <b>(b) Errado:</b> $0$ é real; imaginário puro exige $a=0$ <b>e</b> $b\\neq0$.', 'N1') + \
       treino([('classe de $-2i$', 'imag. puro'), ('classe de $3+0i$', 'real'), ('classe de $1-i$', 'não real'), ('$\\Rep(-6+2i)$', '$-6$'), ('$\\Imp(5)$', '$0$'), ('$z$ real: $(k-1)+3i$?', 'impossível')])
X[4] = item(['Se $x,y\\in\\R$ e $x+yi=(2+i)^2$, então $x+y=7$.'],
            '<b>(a) Certo.</b> $(2+i)^2=4+4i+i^2=3+4i$, logo $x=3$, $y=4$ e $x+y=7$.', 'N2') + \
       treino([('$x+yi=3-5i$', '$x=3,\\,y=-5$'), ('$(2x-1)+(y+3)i=5$', '$x=3,\\,y=-3$'), ('$(x+y)+(x-y)i=6+2i$', '$x=4,\\,y=2$')])
X[5] = item(['Se $z_1=2+3i$ e $z_2=-2+5i$, então $z_1+z_2$ é imaginário puro.', 'A soma de dois números complexos não reais pode ser um número real.'],
            '<b>(a) Certo:</b> $z_1+z_2=0+8i$, com $a=0$ e $b=8\\ne0$. <b>(b) Certo:</b> $(1+i)+(1-i)=2$ (partes imaginárias opostas se cancelam).', 'N2') + \
       treino([('$(2+3i)+(4-i)$', '$6+2i$'), ('$(7-2i)-(5+3i)$', '$2-5i$'), ('$3(2-i)+2(1+4i)$', '$8+5i$'), ('$4i-(2-7i)$', '$-2+11i$'), ('$-(-3+i)$', '$3-i$'), ('$z+w,\\ z-w$ p/ $1+2i,\\ 3-i$', '$4+i;\\ -2+3i$')])
X[6] = item(['O número $(1+i)^{2026}$ é imaginário puro.'],
            '<b>(a) Certo.</b> $(1+i)^2=2i$, então $(1+i)^{2026}=(2i)^{1013}=2^{1013}\\,i^{1013}$; $\\ 1013=4\\cdot253+1\\Rightarrow i^{1013}=i$. Resultado: $2^{1013}i$ (parte real nula, parte imaginária não nula).', 'N3') + \
       treino([('$(2-i)(3+i)$', '$7-i$'), ('$(1+2i)^2$', '$-3+4i$'), ('$(4-3i)(4+3i)$', '$25$'), ('$i(1+i)^2$', '$-2$'), ('$(1-i)^4$', '$-4$'), ('$(2+i)(1-3i)$', '$5-5i$')])
X[7] = item(['Se $z\\cdot\\conj z=25$ e $\\Rep(z)=3$, então $\\Imp(z)=\\pm4$.'],
            '<b>(a) Certo.</b> $z\\conj z=a^2+b^2=25$ com $a=3$ ⟹ $b^2=16$ ⟹ $b=\\pm4$.', 'N2') + \
       treino([('$z=2-5i$: $z+\\conj z$', '$4$'), ('$z=2-5i$: $z\\conj z$', '$29$'), ('$\\conj{(1+i)(2-i)}$', '$3-i$')])
X[9] = ('<div class="box ok xtra"><div class="bt">Resumo geométrico das operações (MAT8)</div>'
        '<table class="t2" style="margin:0"><tr><th class="l">Operação</th><th class="l">Efeito sobre o afixo</th></tr>'
        '<tr><td class="l">$z+w_0$</td><td class="l"><b>translação</b> pelo vetor $w_0$</td></tr>'
        '<tr><td class="l">$k\\,z$ ($k$ real $>0$)</td><td class="l"><b>homotetia</b> de razão $k$ (centro na origem)</td></tr>'
        '<tr><td class="l">$-z$</td><td class="l">reflexão <b>pela origem</b> (giro de $180^\\circ$)</td></tr>'
        '<tr><td class="l">$\\conj z$</td><td class="l">reflexão <b>no eixo real</b></td></tr>'
        '<tr><td class="l">$iz$</td><td class="l">giro de $90^\\circ$ no sentido anti-horário (p. 15)</td></tr></table></div>\n') + \
       item(['Se $a\\neq0$ e $b\\ne0$, os afixos de $z=a+bi$, $\\conj z$ e $-z$ são vértices de um triângulo retângulo.'],
            '<b>(a) Certo.</b> Afixos $(a,b)$, $(a,-b)$, $(-a,-b)$. O lado de $\\conj z$ a $z$ é vertical e o de $\\conj z$ a $-z$ é horizontal: ângulo reto no afixo de $\\conj z$.', 'N2') + \
       treino([('afixo de $\\conj{(-3+4i)}$', '$(-3,-4)$'), ('afixo de $-(2-i)$', '$(-2,1)$'), ('quadrante de $-1+5i$', '2º')])
X[11] = item(['Se $|z|=1$, então $\\dfrac1z=\\conj z$.'],
             '<b>(a) Certo.</b> $z\\conj z=|z|^2=1$, logo $\\conj z=\\dfrac1z$. (Isso mostra que o inverso de um complexo de módulo $1$ é o seu conjugado.)', 'N2') + \
        treino([('$|-5+12i|$', '$13$'), ('$|(2+i)(2-i)|$', '$5$'), ('$\\left|\\dfrac1{3+4i}\\right|$', '$\\dfrac15$'), ('$|z|=3$: $z\\conj z$', '$9$'), ('$|i^{2026}|$', '$1$'), ('$|(1-i)^6|$', '$8$')])
X[12] = item(['$\\sen\\dfrac{7\\pi}6=-\\dfrac12$ e $\\cos\\dfrac{7\\pi}6=-\\dfrac{\\sqrt3}2$.'],
             '<b>(a) Certo.</b> $\\frac{7\\pi}6=210^\\circ$, 3º quadrante, ângulo de referência $30^\\circ$: seno e cosseno negativos, com $\\sen30^\\circ=\\frac12$ e $\\cos30^\\circ=\\frac{\\sqrt3}2$.', 'N2') + \
        treino([('$3\\pi/4$ em graus', '$135^\\circ$'), ('$240^\\circ$ em rad', '$4\\pi/3$'), ('$\\cos300^\\circ$', '$\\tfrac12$'), ('$\\sen330^\\circ$', '$-\\tfrac12$'), ('$\\sen3\\pi$', '$0$'), ('$\\tg225^\\circ$', '$1$')])
X[20] = item(['O conjunto dos complexos $z$ tais que $|z-1|=|z-i|$ é uma reta do plano de Argand-Gauss.'],
             '<b>(a) Certo.</b> É a mediatriz do segmento de afixos $1=(1,0)$ e $i=(0,1)$. Com $z=x+yi$: $(x-1)^2+y^2=x^2+(y-1)^2\\Rightarrow-2x=-2y\\Rightarrow y=x$.', 'N3')
X[22] = item(['O polinômio nulo, $P(x)=0$, tem grau $0$.', 'Se $P$ e $Q$ têm grau $3$, então $P+Q$ tem grau $3$.'],
             '<b>(a) Errado:</b> o grau do polinômio nulo não se define (não é $0$; o grau $0$ é das constantes não nulas). <b>(b) Errado:</b> $(x^3+1)+(-x^3+x)=x+1$ tem grau $1$; a soma pode ter grau menor.', 'N1') + \
        treino([('grau de $5x^2-x^4+3$', '$4$'), ('grau de $(x-1)(x+1)(x^2+1)$', '$4$'), ('grau de $(2x^3-x)-(2x^3+x^2)$', '$2$'), ('$k$: $(k^2-1)x^2+(k+1)x+3$ de grau 1', '$k=1$')])
X[24] = treino([('$ax+b\\equiv3x-2$', '$a=3,\\ b=-2$'), ('$(x+1)^2\\equiv x^2+px+q$', '$p=2,\\ q=1$'), ('$(m-2)x^2+3x+1\\equiv3x+1$', '$m=2$')])
X[25] = item(['$(x^2-x+1)(x^2+x+1)=x^4+x^2+1$.'],
             '<b>(a) Certo.</b> Com $A=x^2+1$: $(A-x)(A+x)=A^2-x^2=x^4+2x^2+1-x^2=x^4+x^2+1$.', 'N2') + \
        treino([('$(x+2)(x-2)$', '$x^2-4$'), ('$(2x-1)^2$', '$4x^2-4x+1$'), ('$(x-1)(x^2+x+1)$', '$x^3-1$'), ('$(x^2+1)(x^2-1)$', '$x^4-1$'), ('grau de $(x^2+1)^3$', '$6$'), ('$(3x^2-x)+(x^2+x)$', '$4x^2$')])
X[28] = item(['Na divisão de um polinômio por $D(x)=x^2+1$, o resto pode ser $R(x)=x^2+1$.'],
             '<b>(a) Errado.</b> Deve valer $R\\equiv0$ ou $\\operatorname{gr}(R)<\\operatorname{gr}(D)=2$. Um resto de grau $2$ indica que a divisão ainda não terminou: $x^2+1=D\\cdot1+0$.', 'N2') + \
        treino([('$(x^2-5x+6)\\div(x-2)$', '$Q=x-3,\\,R=0$'), ('$(x^3+1)\\div(x+1)$', '$Q=x^2-x+1,\\,R=0$'), ('$(x^2+1)\\div x$', '$Q=x,\\,R=1$')])

for n, html in X.items():
    f = os.path.join(PG, f'p{n:02d}.html')
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<div class="(?:exm|box (?:pre|ok)) xtra">.*?(?=\n<div class="(?:exm|box (?:pre|ok)) xtra">|\Z)', '', s, flags=re.S)  # idempotente
    s = s.rstrip('\n') + '\n' + html
    open(f, 'w', encoding='utf-8').write(s)
print('extras aplicados em', sorted(X))
