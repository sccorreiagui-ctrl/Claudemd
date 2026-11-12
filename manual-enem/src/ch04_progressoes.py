"""Capítulo 4 – Progressões aritméticas e geométricas (tópicos 10, 11, 12, 13, 14)."""
from lib import *
from svg import Fig, Plot, fmt

LABEL = 'CAP. 4 · PROGRESSÕES ARITMÉTICAS E GEOMÉTRICAS'

PA_TERMS = [2, 5, 8, 11, 14, 17]


def fig_pa_gauss():
    f = Fig(342, 178)
    n, w, gap, u = 6, 38, 6, 4.3
    x0, base = 8, 124
    tot = 19
    f.text(171, 12, 'Cada coluna soma a₁ + aₙ = 19', size=10.5, col='green', bold=True)
    for k in range(n):
        a = PA_TERMS[k]; b = tot - a
        x = x0 + k * (w + gap)
        f.rect(x, base - a * u, w, a * u, fill='lblue', stroke='navy', sw=1.3)
        f.rect(x, base - tot * u, w, b * u, fill='lpurple', stroke='purple', sw=1.3, dash='4 3')
        f.text(x + w / 2, base - a * u / 2 + 4, str(a), size=11, col='navy', bold=True)
        f.text(x + w / 2, base - tot * u + b * u / 2 + 4, str(b), size=11, col='purple', bold=True)
        f.text(x + w / 2, base + 14, f'*a*_{k + 1}', size=10, col='grey')
    f.text(171, 156, '6 colunas × 19 = 2·Sₙ   →   Sₙ = 6·19/2 = 57', size=10.5, col='green', bold=True)
    f.text(171, 172, 'azul = a PA · roxo = a mesma PA ao contrário', size=9, col='grey')
    return f.svg()


def fig_poste():
    f = Fig(342, 62)
    xs = [20 + k * 76 for k in range(5)]
    f.line(xs[0], 30, xs[-1], 30, col='mgrey', w=1.6)
    for k, x in enumerate(xs):
        f.circ(x, 30, 6, fill='lblue', stroke='navy', sw=1.6); f.text(x, 52, f'*a*_{k + 1}', size=10.5, col='navy', bold=True)
        if k < 4:
            f.path(f'M{x + 6},24 Q{x + 38},4 {x + 70},24', stroke='orange', sw=1.6, arrow=True)
            f.text(x + 38, 10, '+ *r*', size=10, col='orange', bold=True)
    f.text(xs[-1] + 4, 56, '', size=1)
    return f.svg()


def fig_pa_pg():
    p = Plot(330, 184, 0, 8.2, 0, 34, l=32, r=10, t=14, b=22)
    p.grid(1, 8)
    p.axes(xlab='n', ylab='aₙ', xticks=(1, 2, 3, 4, 5, 6), yticks=(8, 16, 24, 32), size=9.5)
    p.curve(lambda t: 1 + 2 * (t - 1), 1, 6, col='blue', w=2, dash='4 3')
    p.curve(lambda t: 2 ** (t - 1), 1, 6, col='purple', w=2, dash='4 3')
    for n in range(1, 7):
        p.pt(n, 1 + 2 * (n - 1), 'blue', 4); p.pt(n, 2 ** (n - 1), 'purple', 4)
    p.label(p.X(6) + 7, p.Y(11) + 4, 'PA (+2)', size=10.5, col='blue', anchor='start', bold=True)
    p.label(p.X(6) + 7, p.Y(32) + 4, 'PG (×2)', size=10.5, col='purple', anchor='start', bold=True)
    p.text(p.X(0.3), p.Y(31), 'PA: 1, 3, 5, 7, 9, 11', size=9.6, col='blue', anchor='start', bold=True)
    p.text(p.X(0.3), p.Y(27), 'PG: 1, 2, 4, 8, 16, 32', size=9.6, col='purple', anchor='start', bold=True)
    return p.svg()


def fig_quadrado_pg():
    f = Fig(190, 138)
    X0, Y0, S = 8, 8, 112
    # peças sucessivas de 1/2, 1/4, 1/8 ...
    pieces = []
    x, y, w, h = X0, Y0, S, S
    horizontal = False
    for k in range(7):
        if not horizontal:
            pieces.append((x, y, w / 2, h)); x += w / 2; w /= 2
        else:
            pieces.append((x, y, w, h / 2)); y += h / 2; h /= 2
        horizontal = not horizontal
    cols_ = ['lblue', 'lpurple', 'lgreen']
    labs = ['1/2', '1/4', '1/8', '1/16']
    for k, (px, py, pw, ph) in enumerate(pieces):
        f.rect(px, py, pw, ph, fill=cols_[k % 3], stroke='navy', sw=1.1)
        if k < 4:
            f.text(px + pw / 2, py + ph / 2 + 4, labs[k], size=11 if k < 3 else 8, col='navy', bold=True)
    f.rect(X0, Y0, S, S, stroke='navy', sw=2)
    f.text(X0 + S / 2, S + 22, '½ + ¼ + ⅛ + … = 1', size=11, col='green', bold=True)
    f.text(X0 + S / 2, S + 36, 'a₁ = ½, q = ½ → S∞ = ½ / (1 − ½) = 1', size=9.4, col='navy')
    return f.svg(width='100%')


def fig_bola():
    f = Fig(220, 110)
    gy, k = 96, 8.2
    f.line(6, gy, 214, gy, col='ink', w=1.6)
    f.line(24, gy - 10 * k, 24, gy, col='mgrey', w=1.2, dash='3 3')
    f.circ(24, gy - 10 * k, 4, fill='orange')
    f.text(30, 14, '10 m', size=10, col='navy', anchor='start', bold=True)
    x = 24
    heights = [6, 3.6, 2.16, 1.3, 0.78]
    widths = [66, 50, 38, 28, 20]
    for h, w in zip(heights, widths):
        top = h * k
        f.path(f'M{x},{gy} Q{x + w / 2},{gy - 2 * top} {x + w},{gy}', stroke='purple', sw=1.8)
        f.line(x + w / 2, gy - top, x + w / 2, gy, col='mpurple', w=1, dash='2 3')
        x += w
    f.text(24 + 33, gy - 6 * k - 7, '6', size=10, col='purple', bold=True)
    f.text(24 + 66 + 25, gy - 3.6 * k - 7, '3,6', size=10, col='purple', bold=True)
    f.text(24 + 116 + 19, gy - 2.16 * k - 7, '2,16', size=9.5, col='purple', bold=True)
    f.text(110, 108, 'alturas das subidas: PG de razão 0,6', size=9.5, col='grey')
    return f.svg()


def fig_impares():
    f = Fig(190, 150)
    s, x0, y0 = 22, 10, 6
    cols_ = ['lorange', 'lblue', 'lpurple', 'lgreen', 'lblue']
    for i in range(5):
        for j in range(5):
            k = max(i, j)
            f.rect(x0 + j * s, y0 + i * s, s, s, fill=cols_[k], stroke='white', sw=1.2)
    for k in range(5):
        # contorno em L de cada camada
        pts = [(x0, y0 + k * s), (x0 + (k + 1) * s, y0 + k * s), (x0 + (k + 1) * s, y0), (x0 + (k + 1) * s, y0)]
    for k, lab in enumerate(('1', '3', '5', '7', '9')):
        f.text(x0 + k * s + s / 2, y0 + k * s + s / 2 + 4, lab, size=10.5, col='navy', bold=True)
    f.rect(x0, y0, 5 * s, 5 * s, stroke='navy', sw=1.8)
    f.text(x0 + 55, 140, '1+3+5+7+9 = 25 = 5²', size=10.5, col='green', bold=True)
    return f.svg()


def p_pa():
    band = chapter_band(4, 'Progressões aritméticas e geométricas', 'tópicos 10 · 11 · 12 · 13 · 14')
    pa = card('Progressão aritmética (PA): termo geral e soma', '10 · 11', 'A', cols(
        stack(
            formula((r'a_n=a_1+(n-1)\,r', 'termo geral'),
                    (r'a_n=a_m+(n-m)\,r', 'a partir de qualquer termo'),
                    (r'S_n=\dfrac{n\,(a_1+a_n)}{2}', 'soma dos n primeiros'),
                    (r'a_k=\dfrac{a_{k-1}+a_{k+1}}{2}', 'termo médio'), label='PA — SOMA CONSTANTE r'),
            vars_('<b>r</b> razão = \\(a_{n+1}-a_n\\) · <b>n</b> nº de termos · <b>aₙ</b> n-ésimo termo. Uma PA é uma <b>função afim</b> definida só nos inteiros: pontos sobre uma reta.'),
            when('“<b>aumenta/diminui o mesmo valor</b> a cada dia/andar/fileira”, “somar de 1 até 100”, assentos em fileiras, parcelas que crescem linearmente.'),
            gap='1.4mm'),
        fig(fig_pa_gauss(), 'Truque de Gauss: some a PA com ela mesma ao contrário → n colunas iguais a a₁+aₙ; o total é o dobro da soma.'),
        ratio='1fr 1.12fr', gap='3.5mm', align='center') +
        cols(fig(fig_poste(), 'Do 1º ao 5º termo há 4 “passos” de razão r: por isso é (n − 1)·r.'),
             err('Usar \\(n\\cdot r\\) em vez de \\((n-1)\\,r\\). Contagem de termos entre dois valores: \\(n=\\dfrac{a_n-a_1}{r}+1\\) (o “+1” conta o primeiro termo).'),
             ratio='1.3fr 1fr', gap='3.5mm', align='center'))

    util = card('Propriedades úteis da PA', None, 'B', cols(
        stack('<p class="small" style="color:var(--ink)"><b>Termos equidistantes dos extremos</b> somam o mesmo valor: \\(a_1+a_n=a_2+a_{n-1}=\\dots\\) '
              '(é o que sustenta a soma de Gauss).</p>'
              '<p class="small" style="color:var(--ink)"><b>Interpolação:</b> para inserir \\(k\\) termos entre \\(a\\) e \\(b\\) em PA, \\(r=\\dfrac{b-a}{k+1}\\). '
              'Ex.: 3 termos entre 2 e 14 → \\(r=\\tfrac{12}{4}=3\\): 2, <b>5, 8, 11</b>, 14.</p>',
              mem('<b>Soma dos n primeiros ímpares = n²</b> (1+3+5+7+9 = 25). Soma de 1 a n: \\(\\tfrac{n(n+1)}{2}\\).'), gap='1.6mm'),
        fig(fig_impares(), None), ratio='1.35fr 1fr', gap='3mm', align='center'))

    e8 = ex(8, 'PA + equação do 2º grau: o plano de treino',
            'Um corredor faz 2 km no primeiro dia de treino e, a cada dia, corre 0,5 km a mais que no dia anterior. '
            'Em que dia o total acumulado chega a 36 km e quantos km ele corre nesse dia?',
            'Distâncias diárias crescem de forma constante → <b>PA</b> (a₁ = 2, r = 0,5). “Total acumulado” = <b>soma</b> Sₙ; a incógnita é n (resulta numa equação do 2º grau).',
            r'\(a_n=2+0{,}5\,(n-1)=1{,}5+0{,}5n\) \(\Rightarrow\) \(S_n=\dfrac{n\,(2+a_n)}{2}=\dfrac{n\,(3{,}5+0{,}5n)}{2}=\dfrac{n(n+7)}{4}\)'
            r'\[\dfrac{n(n+7)}{4}=36\ \Rightarrow\ n^2+7n-144=0\ \Rightarrow\ n=\dfrac{-7\pm\sqrt{49+576}}{2}=\dfrac{-7\pm25}{2}\ \Rightarrow\ n=9\]'
            r'(a raiz negativa não serve). No 9º dia: \(a_9=1{,}5+0{,}5\cdot9=6\) km.',
            r'O total chega a 36 km no <b>9º dia</b>, quando ele corre <b>6 km</b>.',
            shortcut=r'Confira: \(S_9=\dfrac{9\,(2+6)}{2}=36\) ✔.')
    r = rec(('PA 3, 7, 11, … : a₂₀ e S₂₀?', 'a₂₀ = 3 + 19·4 = 79 · S₂₀ = 20·82/2 = 820'),
            ('Quantos múltiplos de 7 entre 10 e 100?', '14, 21, …, 98 → n = (98 − 14)/7 + 1 = 13'),
            ('Soma 1 + 2 + … + 100?', '100·101/2 = 5 050'))
    return band + pa + util + e8 + r


def p_pg():
    pg = card('Progressão geométrica (PG): termo geral, soma finita e infinita', '12 · 13 · 14', 'A', cols(
        stack(
            formula((r'a_n=a_1\cdot q^{\,n-1}', 'termo geral'),
                    (r'S_n=\dfrac{a_1\,(q^n-1)}{q-1}\quad(q\neq1)', 'soma de n termos'),
                    (r'S_\infty=\dfrac{a_1}{1-q}\quad(-1\lt q\lt1)', 'soma infinita (só se |q| < 1)'),
                    (r'a_k^{\,2}=a_{k-1}\cdot a_{k+1}', 'termo médio (produto)'), label='PG — MULTIPLICA POR q'),
            vars_('<b>q</b> razão = \\(a_{n+1}\\div a_n\\). Uma PG é uma <b>função exponencial</b> nos inteiros. '
                  'Em porcentagem: crescer 8% a cada passo → <b>q = 1,08</b>; cair 20% → <b>q = 0,8</b>.'),
            gap='1.4mm'),
        fig(fig_pa_pg(), 'Crescimento aditivo (PA, +2) × multiplicativo (PG, ×2): a PG ultrapassa a PA e dispara.'),
        ratio='1fr 1.1fr', gap='3.5mm', align='center'))

    cmp_ = cols(
        tbl(['', 'PA', 'PG'],
            [['Passo', r'soma \(r\)', r'multiplica por \(q\)'], ['Gráfico', 'pontos de uma reta', 'pontos de exponencial'],
             ['Modelo', 'juros simples, degraus, parcelas', 'juros compostos, população, depreciação, meia-vida'],
             ['Termo geral', r'\(a_1+(n-1)r\)', r'\(a_1\,q^{n-1}\)'],
             ['Soma', r'\(\tfrac{n(a_1+a_n)}{2}\)', r'\(\tfrac{a_1(q^n-1)}{q-1}\)']], widths=['20%', '36%', '44%']),
        stack(when('<b>PG</b>: “aumenta/diminui <u>x%</u> a cada…”, “dobra/triplica/reduz à metade”, “repete-se indefinidamente com fração constante” (soma infinita).'),
              err('Usar PA em percentual (somar 10% várias vezes) ou aplicar \\(S_\\infty\\) com \\(|q|\\ge1\\) (a soma não converge).'), gap='1.4mm'),
        ratio='1.15fr 1fr', gap='3.5mm', align='start')

    e9 = ex(9, 'Soma infinita: a bola que quica',
            'Uma bola é solta de 10 m de altura. Após cada choque com o chão, ela sobe até 60% da altura da queda anterior. '
            'Admitindo que continue quicando indefinidamente, qual a distância total percorrida?',
            'Alturas formam <b>PG de razão 0,6</b>; como há infinitos quiques com \\(|q|\\lt1\\), use a <b>soma infinita</b>. Atenção: cada subida (exceto a queda inicial) é percorrida duas vezes (sobe e desce).',
            r'Alturas das subidas: \(6;\ 3{,}6;\ 2{,}16;\dots\) → \(a_1=6,\ q=0{,}6\)'
            r'\[S_\infty=\dfrac{6}{1-0{,}6}=\dfrac{6}{0{,}4}=15\ \text{m}\]'
            r'Distância \(=\) queda inicial \(+\) 2 × (soma das subidas) \(=10+2\cdot15\).',
            r'Distância total percorrida: <b>40 m</b>.',
            shortcut=r'Fórmula direta: \(d=h\cdot\dfrac{1+q}{1-q}=10\cdot\dfrac{1{,}6}{0{,}4}=40\) ✔.')
    r = rec(('PG 2, 6, 18, … : a₅?', '2 · 3⁴ = 162'),
            ('Soma infinita de 8 + 4 + 2 + 1 + …?', '8 ÷ (1 − ½) = 16'),
            ('Preço sobe 5% ao ano: razão da PG? E em 3 anos?', 'q = 1,05 · fator 1,05³ ≈ 1,158 (+15,8%)'))
    mins = cols(
        mini('População:', '+3% ao ano, 20 000 hab.', r'\(20000\cdot1{,}03^5\approx\)', '≈ 23 185 em 5 anos.'),
        mini('Depreciação:', 'carro de R$ 40 000 perde 10% ao ano.', r'\(40000\cdot0{,}9^3\)', '= R$ 29 160 em 3 anos.'),
        mini('Dois termos:', 'a₃ = 12 e a₆ = 96.', r'\(q^3=\tfrac{96}{12}=8\Rightarrow q=2\), \(a_1=\tfrac{12}{4}\)', '= 3.'), gap='2.4mm')
    return pg + cmp_ + cols(e9, stack(fig(fig_bola(), None), fig(fig_quadrado_pg(), 'Soma infinita = 1: preencher o quadrado por metades.'), gap='1mm'), ratio='1.5fr 1fr', gap='3mm', align='start') + mins + r


def pages():
    return [p_pa(), p_pg()]
