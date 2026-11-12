"""Capítulo 3 – Álgebra e funções (produtos notáveis, Δ, Bhaskara, função afim, função quadrática)."""
from lib import *
from svg import Fig, Plot, COL, fmt

LABEL = 'CAP. 3 · ÁLGEBRA E FUNÇÕES'


# =====================================================================  FIGURAS
def fig_parabola_up():
    """f(x)=x²-4x+3 : raízes 1 e 3, vértice (2,-1), c=3."""
    p = Plot(330, 238, -1.2, 5.2, -2, 5, l=26, r=12, t=14, b=20)
    f = lambda x: x * x - 4 * x + 3
    p.grid(1, 1)
    p.axes(xticks=(-1, 2, 4, 5), yticks=(-1, 1, 2, 4, 5))
    p.line(p.X(2), p.Y(-2), p.X(2), p.Y(5), col='purple', w=1.5, dash='5 3')
    p.label(p.X(2) - 5, p.Y(5) + 9, 'eixo de simetria  *x* = *x*_v', size=10, col='purple', anchor='end')
    p.curve(f, -0.45, 4.45, col='blue', w=2.6, ylim=(-2, 5))
    # simetria c=3
    p.seg(0, 3, 4, 3, col='mgrey', w=1.2, dash='2 3')
    p.dot(p.X(4), p.Y(3), 3.4, 'white'); p.circ(p.X(4), p.Y(3), 3.4, fill='white', stroke='blue', sw=1.6)
    p.pt(0, 3, 'blue'); p.label(p.X(0) + 7, p.Y(3) - 6, '(0, c) = (0, 3)', size=10, col='blue', anchor='start')
    # raízes
    p.pt(1, 0, 'green', 4); p.pt(3, 0, 'green', 4)
    p.label(p.X(1) + 5, p.Y(0) - 7, '*x*_1 = 1', size=10.5, col='green', anchor='start', bold=True)
    p.label(p.X(3) - 5, p.Y(0) - 7, '*x*_2 = 3', size=10.5, col='green', anchor='end', bold=True)
    # vértice
    p.seg(0, -1, 2, -1, col='purple', w=1.1, dash='2 3')
    p.pt(2, -1, 'purple', 4.6)
    p.label(p.X(2) + 9, p.Y(-1) + 4, 'V(2, −1) mínimo', size=10.5, col='purple', anchor='start', bold=True)
    p.label(p.X(2) + 9, p.Y(-1) + 17, '*y*_v = f(2) = −1', size=9.5, col='purple', anchor='start')
    p.text(p.X(5.2) - 2, p.Y(4.1), '*a* > 0', size=11, col='navy', anchor='end', bold=True)
    p.text(p.X(5.2) - 2, p.Y(3.55), 'boca ∪', size=9.5, col='grey', anchor='end')
    return p.svg()


def fig_parabola_down():
    """f(x)=-x²+2x+3 : raízes -1 e 3, vértice (1,4), c=3."""
    p = Plot(330, 222, -2, 4.4, -2.0, 5, l=26, r=12, t=14, b=20)
    f = lambda x: -x * x + 2 * x + 3
    p.grid(1, 1)
    p.axes(xticks=(), yticks=(1, 2, 3, 5))
    p.line(p.X(1), p.Y(-2.0), p.X(1), p.Y(5), col='purple', w=1.5, dash='5 3')
    p.curve(f, -1.45, 3.45, col='blue', w=2.6, ylim=(-2.0, 5))
    # raízes e ponto médio
    p.pt(-1, 0, 'green', 4); p.pt(3, 0, 'green', 4)
    p.label(p.X(-1) - 4, p.Y(0) + 14, '*x*_1 = −1', size=10.5, col='green', anchor='end', bold=True)
    p.label(p.X(3) + 4, p.Y(0) + 14, '*x*_2 = 3', size=10.5, col='green', anchor='start', bold=True)
    p.pt(1, 0, 'purple', 3.6)
    p.label(p.X(1) + 5, p.Y(0) + 28, '*x*_v = (−1+3)/2 = 1', size=9.5, col='purple', anchor='start')
    p.pt(1, 4, 'purple', 4.6)
    p.label(p.X(1) + 8, p.Y(4) - 6, 'V(1, 4) máximo', size=10.5, col='purple', anchor='start', bold=True)
    p.pt(0, 3, 'blue'); p.label(p.X(0) - 7, p.Y(3) + 3, '*c* = 3', size=10, col='blue', anchor='end')
    p.text(p.X(4.4) - 2, p.Y(4.4), '*a* < 0', size=11, col='navy', anchor='end', bold=True)
    p.text(p.X(4.4) - 2, p.Y(3.85), 'boca ∩', size=9.5, col='grey', anchor='end')
    return p.svg()


def fig_delta():
    """Δ>0, Δ=0, Δ<0 (a>0): três mini-parábolas lado a lado."""
    W, H = 180, 118
    out = []
    cases = [('Δ > 0', 'duas raízes reais distintas', lambda x: x ** 2 - 1, [-1, 1], 'green'),
             ('Δ = 0', 'uma raiz real (dupla)', lambda x: x ** 2, [0], 'blue'),
             ('Δ < 0', 'nenhuma raiz real', lambda x: x ** 2 + 1, [], 'orange')]
    for title, sub, f, roots, col in cases:
        p = Plot(W, H, -2.2, 2.2, -1.5, 2.3, l=8, r=8, t=26, b=8)
        p.line(p.X(-2.2), p.Y(0), p.X(2.2), p.Y(0), col='ink', w=1.2, arrow=True)
        p.line(p.X(0), p.Y(-1.5), p.X(0), p.Y(2.3), col='ink', w=1.2, arrow=True)
        p.text(p.X(2.2) - 1, p.Y(0) + 12, 'x', size=10.5, anchor='end')
        p.curve(f, -1.9, 1.9, col=col, w=2.6, ylim=(-1.5, 2.3))
        for r in roots:
            p.pt(r, 0, col, 4)
        p.text(W / 2, 12, title, size=12, col=col, bold=True)
        p.text(W / 2, 23, sub, size=9.2, col='grey')
        out.append(p.svg())
    return out


def fig_receita():
    p = Plot(330, 190, -12, 23, -1500, 10500, l=44, r=10, t=14, b=24)
    R = lambda x: -40 * x * x + 400 * x + 8000
    p.grid(5, 2000)
    p.axes(xlab='x', ylab='R(x)', xticks=(-10, 5, 20), yticks=(4000, 8000), yfmt=lambda v: f'{int(v):,}'.replace(',', '.'))
    p.curve(R, -10, 0, col='mblue', w=2, dash='4 3')
    p.curve(R, 0, 20, col='blue', w=2.8)
    p.pt(-10, 0, 'green', 3.8); p.pt(20, 0, 'green', 3.8)
    p.seg(5, 0, 5, 9000, col='purple', w=1.3, dash='4 3')
    p.pt(5, 9000, 'purple', 4.8)
    p.label(p.X(5) + 8, p.Y(9000) - 5, 'V(5; 9.000) → R$ 9.000', size=10.5, col='purple', anchor='start', bold=True)
    p.pt(0, 8000, 'blue', 3.6); p.label(p.X(0) - 6, p.Y(8000) - 6, 'hoje: 8.000', size=9.5, col='blue', anchor='end')
    p.label(p.X(-10), p.Y(0) - 7, '−10', size=9.5, col='green'); p.label(p.X(20), p.Y(0) - 7, '20', size=9.5, col='green')
    return p.svg()


def fig_bola():
    p = Plot(330, 190, -0.5, 4.8, -4, 24, l=34, r=10, t=14, b=24)
    h = lambda t: -5 * t * t + 20 * t
    p.grid(1, 5)
    p.axes(xlab='t (s)', ylab='h (m)', xticks=(1, 2, 3, 4), yticks=(5, 10, 15, 20))
    p.curve(h, 0, 4, col='blue', w=2.8)
    p.pt(0, 0, 'green', 3.8); p.pt(4, 0, 'green', 3.8)
    p.seg(2, 0, 2, 20, col='purple', w=1.3, dash='4 3')
    p.pt(2, 20, 'purple', 4.8)
    p.label(p.X(2) + 8, p.Y(20) - 5, 'V(2; 20) → 20 m', size=10.5, col='purple', anchor='start', bold=True)
    p.label(p.X(4) + 2, p.Y(0) - 8, 'solo', size=9.5, col='green', anchor='start')
    return p.svg()


def fig_sign():
    """Sinal de f(x)=x²-4x+3 (a>0): positivo fora das raízes, negativo entre elas."""
    p = Plot(250, 128, -0.2, 4.2, -1.5, 3.4, l=8, r=10, t=8, b=22)
    f = lambda x: x * x - 4 * x + 3
    p.curve(f, 0, 4, col='blue', w=2.4, ylim=(-1.6, 3.4))
    p.line(p.X(-0.2), p.Y(0), p.X(4.2), p.Y(0), col='ink', w=1.2, arrow=True)
    p.line(p.X(-0.2), p.Y(0), p.X(1), p.Y(0), col='green', w=5)
    p.line(p.X(3), p.Y(0), p.X(4.2), p.Y(0), col='green', w=5)
    p.line(p.X(1), p.Y(0), p.X(3), p.Y(0), col='orange', w=5)
    for r in (1, 3):
        p.pt(r, 0, 'ink', 3.8)
    p.text(p.X(1), p.Y(0) + 14, '1', size=10.5, col='ink'); p.text(p.X(3), p.Y(0) + 14, '3', size=10.5, col='ink')
    p.text(p.X(0.4), p.Y(2.6), '*f* > 0', size=11, col='green', bold=True)
    p.text(p.X(3.65), p.Y(2.6), '*f* > 0', size=11, col='green', bold=True)
    p.text(p.X(2), p.Y(0.55), '*f* < 0', size=11, col='orange', bold=True)
    return p.svg()


def fig_quadrado():
    """(a+b)² decomposto em a², ab, ab, b²."""
    f = Fig(210, 168)
    a, b = 82, 44
    x0, y0 = 30, 26
    f.rect(x0, y0, a, a, fill='lblue', stroke='navy', sw=1.6)
    f.rect(x0 + a, y0, b, a, fill='lpurple', stroke='navy', sw=1.6)
    f.rect(x0, y0 + a, a, b, fill='lpurple', stroke='navy', sw=1.6)
    f.rect(x0 + a, y0 + a, b, b, fill='lgreen', stroke='navy', sw=1.6)
    f.text(x0 + a / 2, y0 + a / 2 + 5, '*a*²', size=16, col='navy', bold=True)
    f.text(x0 + a + b / 2, y0 + a / 2 + 5, '*ab*', size=13, col='purple', bold=True)
    f.text(x0 + a / 2, y0 + a + b / 2 + 5, '*ab*', size=13, col='purple', bold=True)
    f.text(x0 + a + b / 2, y0 + a + b / 2 + 5, '*b*²', size=14, col='green', bold=True)
    f.dim(x0, y0 - 9, x0 + a, y0 - 9, '*a*', col='grey', text_dy=-4)
    f.dim(x0 + a, y0 - 9, x0 + a + b, y0 - 9, '*b*', col='grey', text_dy=-4)
    f.dim(x0 - 10, y0, x0 - 10, y0 + a, '', col='grey'); f.text(x0 - 17, y0 + a / 2 + 4, '*a*', size=10.5, col='grey')
    f.dim(x0 - 10, y0 + a, x0 - 10, y0 + a + b, '', col='grey'); f.text(x0 - 17, y0 + a + b / 2 + 4, '*b*', size=10.5, col='grey')
    f.text(105, 162, '(*a*+*b*)² = *a*² + 2*ab* + *b*²', size=11, col='navy', bold=True)
    return f.svg(width='100%')


def fig_passos():
    f = Fig(340, 96)
    def box(x, w, t1, t2, fill, col):
        f.rect(x, 20, w, 56, fill=fill, stroke=col, sw=1.6, rx=6)
        f.text(x + w / 2, 36, t1, size=9.8, col=col, bold=True)
        f.text(x + w / 2, 54, t2, size=10.5, col='ink')
    f.text(170, 11, 'Exemplo: 2x² − 7x + 3 = 0', size=10, col='navy', bold=True)
    box(2, 98, '1 · IDENTIFIQUE', '*a*=2, *b*=−7, *c*=3', 'lblue', 'blue')
    box(122, 96, '2 · CALCULE Δ', 'Δ = 49 − 24 = 25', 'lpurple', 'purple')
    box(240, 98, '3 · APLIQUE', '*x* = (7 ± 5)/4', 'lgreen', 'green')
    f.line(100, 48, 120, 48, col='navy', w=2, arrow=True); f.line(218, 48, 238, 48, col='navy', w=2, arrow=True)
    f.text(170, 92, 'raízes: x = 3  e  x = 1/2', size=10.5, col='green', bold=True)
    return f.svg()


def fig_sistema():
    p = Plot(250, 176, 0, 56, -10, 62, l=30, r=10, t=12, b=22)
    p.grid(10, 10)
    p.axes(xlab='x', ylab='y', xticks=(10, 20, 30, 40, 50), yticks=(20, 40, 60), size=9)
    p.seg(0, 50, 50, 0, col='blue', w=2.4)
    p.seg(0, 80, 40, 0, col='purple', w=2.4) if False else None
    p.curve(lambda x: 80 - 2 * x, 15, 40, col='purple', w=2.4, ylim=(-10, 62))
    p.pt(30, 20, 'green', 5)
    p.label(p.X(30) + 8, p.Y(20) - 6, '(30, 20)', size=10.5, col='green', anchor='start', bold=True)
    p.text(p.X(6), p.Y(54), '*x* + *y* = 50', size=10, col='blue', bold=True, anchor='start')
    p.text(p.X(30), p.Y(58), '2*x* + *y* = 80', size=10, col='purple', bold=True, anchor='start')
    return p.svg()


def fig_afim():
    """y=2x+1 com Δx, Δy, coef. linear e raiz."""
    p = Plot(330, 204, -1.4, 4.8, -2.0, 9.5, l=26, r=12, t=12, b=20)
    p.grid(1, 1)
    p.axes(xticks=(-1, 1, 2, 3, 4), yticks=(1, 3, 5, 7, 9))
    p.seg(-1.2, -1.4, 4.2, 9.4, col='blue', w=2.8)
    # pontos (1,3) e (3,7)
    p.seg(1, 3, 3, 3, col='orange', w=1.8, dash='4 3'); p.seg(3, 3, 3, 7, col='orange', w=1.8, dash='4 3')
    p.pt(1, 3, 'ink'); p.pt(3, 7, 'ink')
    p.label(p.X(2), p.Y(3) + 14, 'Δ*x* = 2', size=10.5, col='orange', bold=True)
    p.label(p.X(3) + 6, p.Y(5) + 4, 'Δ*y* = 4', size=10.5, col='orange', anchor='start', bold=True)
    p.label(p.X(1) - 6, p.Y(3) - 5, '(1, 3)', size=10, col='ink', anchor='end')
    p.label(p.X(3) - 6, p.Y(7) - 5, '(3, 7)', size=10, col='ink', anchor='end')
    p.pt(0, 1, 'purple', 4.4)
    p.label(p.X(0) + 9, p.Y(1) + 16, '*b* = 1  (corta o eixo *y*)', size=10, col='purple', anchor='start', bold=True)
    p.pt(-0.5, 0, 'green', 4.4)
    p.label(p.X(-0.5) - 4, p.Y(0) - 8, 'raiz −1/2', size=10, col='green', anchor='end', bold=True)
    p.text(p.X(4.8) - 2, p.Y(-0.9), '*a* = Δ*y*/Δ*x* = 4/2 = 2', size=10.5, col='navy', anchor='end', bold=True)
    p.text(p.X(4.8) - 2, p.Y(-1.6), '*f*(*x*) = 2*x* + 1', size=10.5, col='blue', anchor='end', bold=True)
    return p.svg()


def fig_sinais_a():
    p = Plot(330, 100, -3, 3, -3, 3, l=8, r=8, t=8, b=10)
    out = []
    for k, (txt, col, f) in enumerate((('*a* > 0 · crescente', 'green', lambda x: 0.9 * x), ('*a* = 0 · constante', 'blue', lambda x: 0.5), ('*a* < 0 · decrescente', 'orange', lambda x: -0.9 * x))):
        q = Plot(108, 100, -3, 3, -3, 3, l=8, r=8, t=22, b=8)
        q.line(q.X(-3), q.Y(0), q.X(3), q.Y(0), col='ink', w=1.1, arrow=True); q.line(q.X(0), q.Y(-3), q.X(0), q.Y(3), col='ink', w=1.1, arrow=True)
        q.curve(f, -2.6, 2.6, col=col, w=2.8, ylim=(-3, 3))
        q.text(54, 12, txt, size=9.5, col=col, bold=True)
        out.append(q)
    g = Fig(330, 100)
    for k, q in enumerate(out):
        g.group(q, k * 111, 0)
    return g.svg()


def fig_planos():
    p = Plot(330, 196, 0, 11, 0, 46, l=34, r=10, t=14, b=24)
    p.grid(1, 10)
    p.axes(xlab='km', ylab='R$', xticks=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), yticks=(10, 20, 30, 40), size=9.5)
    p.curve(lambda x: 7 + 3 * x, 0, 10, col='blue', w=2.6, ylim=(0, 46))
    p.curve(lambda x: 12 + 2 * x, 0, 10, col='purple', w=2.6, ylim=(0, 46))
    p.fill_between(lambda x: 7 + 3 * x, lambda x: 12 + 2 * x, 5, 10, fill='lgreen', op=.85)
    p.pt(5, 22, 'navy', 5)
    p.label(p.X(5) - 6, p.Y(22) - 8, '(5; 22): preços iguais', size=10.5, col='navy', anchor='end', bold=True)
    p.label(p.X(10) - 2, p.Y(37) - 7, 'A: 7 + 3x', size=10.5, col='blue', anchor='end', bold=True)
    p.label(p.X(10) - 2, p.Y(32) + 16, 'B: 12 + 2x', size=10.5, col='purple', anchor='end', bold=True)
    p.text(p.X(7.4), p.Y(26.5), 'B mais barata', size=9.5, col='green', bold=True)
    p.text(p.X(1.9), p.Y(8), 'A mais barata', size=9.5, col='blue', bold=True)
    return p.svg()


# =====================================================================  PÁGINAS
def p_prod():
    band = chapter_band(3, 'Álgebra e funções', 'tópicos 6 · 7 · 8 · 9 · 15 · 16 · 17')
    c6 = card('Produtos notáveis', 6, 'B', cols(
        fig(fig_quadrado()),
        stack(
            formula((r'(a+b)^2=a^2+2ab+b^2', ''), (r'(a-b)^2=a^2-2ab+b^2', ''), (r'(a+b)(a-b)=a^2-b^2', 'diferença de quadrados'),
                    (r'(a\pm b)^3=a^3\pm3a^2b+3ab^2\pm b^3', 'cubo'), label='PRODUTOS NOTÁVEIS'),
            when('Simplificar expressões, <b>fatorar</b>, cálculo mental (\\(99^2=(100-1)^2=9801\\); \\(51\\cdot49=50^2-1=2499\\)), '
                 'completar quadrados, relacionar \\(x+\\tfrac1x\\) com \\(x^2+\\tfrac1{x^2}\\).'),
            err('<b>(a + b)² ≠ a² + b²</b>: falta o termo do meio 2ab (as duas “faixas” roxas da figura).'),
            gap='1.4mm'),
        ratio='.82fr 1.18fr', gap='3.5mm', align='center'))

    ceq = card('Equações e sistemas simples', None, 'B', cols(
        stack(
            formula((r'ax+b=0\ \Rightarrow\ x=-\dfrac{b}{a}', 'equação do 1º grau'),
                    (r'\begin{cases}x+y=50\\[2pt]2x+y=80\end{cases}', 'sistema 2×2'), label='EQUAÇÃO · SISTEMA'),
            when('Duas incógnitas e duas informações (total de itens + total em dinheiro, idades, misturas). '
                 '<b>Substituição:</b> isole uma variável e substitua. <b>Adição:</b> some/subtraia as equações para cancelar uma incógnita.'),
            mini('Ingressos:', 'inteira R$ 20 e meia R$ 10; 50 ingressos somam R$ 800.', r'\(x+y=50\) e \(20x+10y=800\Rightarrow10x=300\)', 'x = 30 inteiras e y = 20 meias.'),
            gap='1.4mm'),
        stack(fig(fig_sistema(), 'Resolver o sistema = achar o ponto onde as retas se cruzam (exemplo: x + y = 50 e 2x + y = 80).'),),
        ratio='1.18fr .82fr', gap='3.5mm', align='center'))

    c78 = card('Discriminante e fórmula de Bhaskara', '7 · 8', 'A', cols(
        stack(
            formula((r'\Delta=b^2-4ac', ''), (r'x=\dfrac{-b\pm\sqrt{\Delta}}{2a}', 'para ax² + bx + c = 0 (a ≠ 0)'), label='DISCRIMINANTE E BHASKARA'),
            tbl(['Δ', 'Raízes reais'], [['Δ > 0', 'duas, distintas'], ['Δ = 0', 'uma (dupla): x = −b/2a'], ['Δ &lt; 0', 'nenhuma']], widths=['28%', '72%']),
            gap='1.4mm'),
        stack(
            when('<b>Atalhos antes de Bhaskara:</b> \\(c=0\\) → \\(x(ax+b)=0\\); \\(b=0\\) → \\(x^2=-\\tfrac ca\\); raízes inteiras → <b>soma e produto</b>.', label='ECONOMIZE TEMPO'),
            err('Esquecer que <b>b negativo</b> vira \\(-b\\) positivo; dividir só um termo por \\(2a\\) (o <u>2a</u> divide tudo); '
                'e escrever \\(\\sqrt{\\Delta}\\) com Δ negativo (não há raiz real).'),
            gap='1.4mm'),
        ratio='1fr 1.1fr', gap='3.5mm', align='start') + fig(fig_passos()) +
        '<div class="small tc">O número de raízes e a posição da parábola em relação ao eixo x estão na p. 10.</div>')
    r = rec(('(x − 3)² desenvolvido?', 'x² − 6x + 9'), ('x² − 5x + 6 = 0: soma e produto das raízes?', 'S = 5, P = 6 → 2 e 3'),
            ('x² − 6x + 9 = 0: Δ vale?', '36 − 36 = 0 → raiz dupla x = 3'))
    return band + c6 + ceq + c78 + r


def p_afim():
    c9 = card('Lei de formação da função do 1º grau', 9, 'A', cols(
        stack(
            formula((r'f(x)=ax+b', 'reta'),
                    (r'a=\dfrac{\Delta y}{\Delta x}=\dfrac{y_2-y_1}{x_2-x_1}', 'coeficiente angular (taxa de variação)'),
                    (r'b=f(0)', 'coeficiente linear (valor inicial)'),
                    (r'f(x)=0\ \Rightarrow\ x=-\dfrac{b}{a}', 'raiz'), label='FUNÇÃO AFIM'),
            when('<b>Valor fixo + valor variável</b> (táxi, plano, aluguel, salário com comissão), variação <u>constante</u> (“a cada km…”, “por hora…”). '
                 '<b>Dois pontos</b> dados → ache \\(a\\) e depois \\(b = y_1 - a x_1\\).'),
            gap='1.4mm'),
        fig(fig_afim(), 'f(x) = 2x + 1: passa por (1, 3) e (3, 7).'),
        ratio='1fr 1.2fr', gap='3.5mm', align='center'))

    c9b = cols(
        stack(fig(fig_sinais_a(), 'O sinal de <b>a</b> decide o comportamento; b só “sobe” ou “desce” a reta.'),
              mem('<b>a</b> = inclinação = “quanto y varia para cada 1 de x”. <b>b</b> = onde a reta nasce (x = 0). '
                  'Função <b>linear</b> (b = 0) é a proporcionalidade direta: passa pela origem.'), gap='1.4mm'),
        stack(err('Trocar <b>a</b> e <b>b</b>; calcular a inclinação com \\(\\tfrac{\\Delta x}{\\Delta y}\\); '
                  'e esquecer que a taxa precisa estar na <u>mesma unidade</u> do eixo (km, min, R$).'),
              mini('Taxa de variação:', 'temperatura sobe de 12 °C às 6 h para 24 °C às 10 h.', r'\(a=\tfrac{24-12}{10-6}\)', '= 3 °C/h → T(t) = 12 + 3(t − 6).'),
              gap='1.4mm'),
        ratio='1.2fr 1fr', gap='3.5mm', align='start')

    e6 = ex(6, 'Lei com dois pontos + comparação de planos',
            'A empresa A de táxi cobra uma bandeirada fixa mais um valor por km rodado: 5 km custam R$ 22 e 12 km custam R$ 43. A empresa B cobra '
            'R$ 12 fixos mais R$ 2 por km. A partir de quantos km a empresa B passa a ser mais barata?',
            'Custo = fixo + variável por km → <b>função afim</b>. Dois pontos dão a lei de A; comparar preços = <b>igualar as funções</b>.',
            r'\(a=\dfrac{43-22}{12-5}=3\); \(\ b=22-3\cdot5=7\ \Rightarrow\ A(x)=3x+7\); \(\ B(x)=2x+12\).'
            r'<br>Iguais quando \(3x+7=2x+12\Rightarrow x=5\). Para \(x\gt5\): \(A(x)-B(x)=x-5\gt0\) (A fica mais cara).',
            r'A bandeirada de A é <b>R$ 7</b> e cada km custa R$ 3. <b>Acima de 5 km</b> a empresa B é mais barata (empate em 5 km: R$ 22).',
            shortcut=r'Com 12 km: \(A=3\cdot12+7=43\) ✔ (confere o dado do enunciado); \(B=2\cdot12+12=36\lt43\) ✔.')
    r = rec(('Reta por (0, 5) e (2, 11): lei?', 'a = 3; f(x) = 3x + 5'),
            ('f(x) = −4x + 12: onde corta os eixos?', 'y: 12 · x: 3'),
            ('Retas y = 2x + 3 e y = 5x − 6 se cruzam em x?', '2x + 3 = 5x − 6 → x = 3'))
    reco = card('Reconhecendo a função afim no enunciado', None, 'A', tbl(
        ['Pista no texto', 'Modelo', 'Como achar a e b'],
        [['“taxa fixa + R$ … por unidade”', r'\(y=b+ax\)', 'b = valor fixo; a = valor por unidade'],
         ['“a cada … aumenta/diminui sempre o mesmo”', r'\(y=y_0\pm a\,x\)', 'a = variação por passo (sinal!); y₀ = valor inicial'],
         ['“proporcional a …” / sem taxa fixa', r'\(y=ax\)', 'a = y ÷ x (qualquer ponto não nulo)'],
         ['gráfico de reta com pontos marcados', r'\(y=ax+b\)', 'a = Δy/Δx e leia b onde cruza o eixo y']], widths=['34%', '16%', '50%']))
    return c9 + c9b + cols(e6, fig(fig_planos(), 'Gráfico do Exemplo 6: o ponto de cruzamento marca a troca da empresa mais barata.'),
                           ratio='1.35fr 1fr', gap='3mm', align='start') + reco + r


def p_quad1():
    c15 = card('Função quadrática: lei de formação e parábola', 15, 'A', cols(
        stack(
            formula(r'f(x)=ax^2+bx+c\quad (a\neq 0)',
                    (r'\Delta=b^2-4ac', 'discriminante'),
                    (r'x=\dfrac{-b\pm\sqrt{\Delta}}{2a}', 'raízes (Bhaskara)'), label='LEI DE FORMAÇÃO · RAÍZES'),
            vars_('<b>a</b> abre a parábola: <b>a&gt;0</b> sorri (∪, tem <i>mínimo</i>); <b>a&lt;0</b> fica triste (∩, tem <i>máximo</i>). '
                  '<b>c</b> = f(0): é onde a curva corta o eixo <i>y</i>. <b>Raízes</b> = onde corta o eixo <i>x</i> (f(x)=0).'),
            when('Fenômeno com <b>valor máximo ou mínimo</b> (lucro, área, altura, custo), trajetória parabólica, '
                 '“em que instante/valor…”, ou variação que <u>não é constante</u>.'),
            gap='1.8mm'),
        fig(fig_parabola_up(), '<b>Exemplo:</b> f(x) = x² − 4x + 3  →  Δ = 4, raízes 1 e 3, c = 3, vértice V(2, −1).'),
        ratio='1fr 1.12fr', gap='3.5mm', align='center'))

    c17 = card('Soma e produto das raízes · coordenadas do vértice', 17, 'A', cols(
        fig(fig_parabola_down(), '<b>Exemplo:</b> f(x) = −x² + 2x + 3  →  x<sub>v</sub> é a <b>média das raízes</b>; y<sub>v</sub> = f(x<sub>v</sub>) = 4.'),
        stack(
            formula((r'S=x_1+x_2=-\dfrac{b}{a}', 'soma'),
                    (r'P=x_1\cdot x_2=\dfrac{c}{a}', 'produto'),
                    (r'x_v=\dfrac{x_1+x_2}{2}=-\dfrac{b}{2a}', 'xᵥ: onde ocorre o extremo'),
                    (r'y_v=-\dfrac{\Delta}{4a}=f(x_v)', 'yᵥ: valor do extremo'), label='RAÍZES E VÉRTICE'),
            when('<b>Soma e produto</b> poupam Bhaskara quando as raízes são inteiras: procure dois números com soma '
                 '\\(S\\) e produto \\(P\\). Ex.: \\(x^2-5x+6=0\\): soma 5, produto 6 → <b>2 e 3</b>.'),
            err('<b>Valor máximo</b> (y<sub>v</sub>) ≠ <b>ponto de máximo</b> (x<sub>v</sub>). Leia o que a pergunta pede: '
                '“<i>em que preço</i>” → x<sub>v</sub>; “<i>qual o lucro máximo</i>” → y<sub>v</sub>. Cuidado: \\(x_v=-\\dfrac{b}{2a}\\), com o 2a no denominador.'),
            gap='1.8mm'),
        ratio='1fr 1.12fr', gap='3.5mm', align='center'))

    d1, d2, d3 = fig_delta()
    cdelta = card('O discriminante Δ decide quantas raízes a parábola tem', 7, 'A', cols(d1, d2, d3, gap='2mm') +
                  '<div class="small tc">Para a &lt; 0 a figura se inverte (∩); o número de raízes continua sendo decidido por Δ.</div>')

    memo = cols(
        mem('<b>xᵥ é o centro da simetria</b>: a parábola é um espelho em torno de x = xᵥ. Dois pontos de mesma altura (como '
            '<i>(0, c)</i> e <i>(2xᵥ, c)</i>) são simétricos. Por isso xᵥ = média das raízes.'),
        mem('<b>Atalho para yᵥ:</b> calcule xᵥ e <b>substitua na função</b>: yᵥ = f(xᵥ). Evita decorar −Δ/4a e reduz erro de sinal.'),
        gap='2.5mm')

    r = rec(('Qual o vértice de y = x² − 6x + 5?', 'xᵥ = 3; yᵥ = 9 − 18 + 5 = −4 → V(3, −4)'),
            ('Se Δ < 0 e a > 0, a parábola tem sinal…', 'sempre positivo (não toca o eixo x)'),
            ('Soma e produto de 2x² − 8x + 6 = 0?', 'S = 8/2 = 4; P = 6/2 = 3 (raízes 1 e 3)'))
    return card_wrap(c15, c17, cdelta, memo, r)


def card_wrap(*parts):
    return ''.join(parts)


def p_quad2():
    forms = card('Três formas da mesma função: escolha a que combina com os dados', 16, 'B', tbl(
        ['Forma', 'Expressão', 'Use quando o enunciado dá…'],
        [['<b>Geral</b>', r'\(f(x)=ax^2+bx+c\)', 'coeficientes, ou 3 pontos do gráfico (monte um sistema para a, b e c)'],
         ['<b class="g">Fatorada</b>', r'\(f(x)=a\,(x-x_1)(x-x_2)\)', 'as <b>raízes</b> (“corta o eixo x em…”) + mais 1 ponto para achar <i>a</i>'],
         ['<b class="p">Canônica</b>', r'\(f(x)=a\,(x-x_v)^2+y_v\)', 'o <b>vértice</b> (“altura máxima de … no instante …”) + mais 1 ponto para achar <i>a</i>']],
        widths=['17%', '31%', '52%']) +
        mini('Raízes 2 e −3, passa por (0, −6):', '', r'\(f(x)=a(x-2)(x+3)\); em \(x=0\): \(a\cdot(-2)(3)=-6\Rightarrow a=1\).',
             r'\(f(x)=x^2+x-6\)'))

    sign = card('Sinal da função e inequações do 2º grau', None, 'B', cols(
        fig(fig_sign()),
        stack(
            '<p><b>a &gt; 0:</b> f &gt; 0 <u>fora</u> das raízes e f &lt; 0 <u>entre</u> elas.<br><b>a &lt; 0:</b> o contrário (f &gt; 0 entre as raízes).</p>'
            '<p>Resolva a inequação <b>desenhando o esboço</b>: raízes + concavidade bastam.</p>',
            mem('Raízes 1 e 3, a &gt; 0: \\(f(x)\\lt 0\\) em \\(1\\lt x\\lt 3\\) · \\(f(x)\\ge 0\\) em \\(x\\le 1\\) ou \\(x\\ge 3\\).'),
            gap='1.4mm'),
        ratio='1fr 1fr', gap='3mm', align='center'))

    e7 = ex(7, 'Receita máxima: otimização com função quadrática',
            'Um teatro cobra R$ 40 por ingresso e vende, em média, 200 ingressos por sessão. Uma pesquisa indica que, '
            'a cada redução de R$ 2 no preço, são vendidos 20 ingressos a mais. Qual preço maximiza a receita e qual é essa receita máxima?',
            'Receita = preço × quantidade, com <b>dois fatores que variam linearmente</b> com a mesma variável → produto é uma <b>função quadrática</b>. '
            'Pergunta por “maior” valor → <b>vértice</b>.',
            r'Seja \(x\) o número de reduções de R$ 2. Preço \(=40-2x\); quantidade \(=200+20x\).'
            r'\[R(x)=(40-2x)(200+20x)=-40x^2+400x+8000\]'
            r'\[x_v=-\dfrac{b}{2a}=-\dfrac{400}{2(-40)}=5\quad\Rightarrow\quad \text{preço}=40-2\cdot5=30,\ \ \text{público}=200+20\cdot5=300\]'
            r'\[R_{\max}=R(5)=30\cdot 300=9\,000\]',
            r'Preço de <b>R$ 30,00</b> e receita máxima de <b>R$ 9.000,00</b> (a=−40&lt;0 garante que é máximo).',
            shortcut=r'As raízes são \(x=-10\) (público 0) e \(x=20\) (preço 0); o vértice fica no ponto médio: \(x_v=\dfrac{-10+20}{2}=5\) ✔.')

    graf = cols(fig(fig_receita(), 'Exemplo 7: R(x) = −40x² + 400x + 8000 (trecho útil x ≥ 0, linha cheia).'),
                fig(fig_bola(), 'Lançamento: h(t) = −5t² + 20t. Vértice = ponto mais alto; raízes = saída e chegada.'), gap='4mm')
    lanc = mini('Lançamento:', r'uma bola é lançada e sua altura (m) é \(h(t)=-5t^2+20t\), com \(t\) em segundos.',
                r'\(t_v=-\dfrac{20}{2(-5)}=2\) s; \(h(2)=-20+40=20\). Volta ao solo quando \(h=0\): \(t(-5t+20)=0\Rightarrow t=4\) s.',
                'Altura máxima 20 m (em 2 s); tempo de voo 4 s.')

    cerca = mini('Cerca com muro:', r'40 m de tela cercam 3 lados de um retângulo encostado em um muro (lados \(x\), \(x\) e \(y\)).',
                 r'\(2x+y=40\Rightarrow A=x(40-2x)=-2x^2+40x\); \(x_v=-\dfrac{40}{2(-2)}=10\), então \(y=20\) e \(A=10\cdot20\).',
                 'Área máxima 200 m².')
    r = rec(('f(x) = −2(x − 1)² + 8: qual o valor máximo e onde ocorre?', 'máximo 8, em x = 1 (forma canônica)'),
            ('Em que forma é mais fácil achar a função se dão as raízes?', 'fatorada: a(x − x₁)(x − x₂)'))
    return forms + sign + e7 + graf + lanc + cerca + r


def pages():
    return [p_prod(), p_afim(), p_quad1(), p_quad2()]
