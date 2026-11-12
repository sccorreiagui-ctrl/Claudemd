"""Capítulo 8 – Geometria analítica, potências, radicais, logaritmos e função exponencial (tópicos 38, 39 + exponencial)."""
import math
from lib import *
from svg import Fig, Plot

LABEL = 'CAP. 8 · GEOMETRIA ANALÍTICA, POTÊNCIAS E LOGARITMOS'


def fig_dist():
    p = Plot(262, 292, -0.8, 9.2, -0.8, 11.2, l=26, r=12, t=10, b=20)
    p.grid(1, 1)
    p.axes(xticks=(1, 3, 5, 7, 9), yticks=(2, 4, 6, 8, 10), size=9.5)
    p.seg(1, 2, 7, 10, col='blue', w=2.8)
    p.seg(1, 2, 7, 2, col='orange', w=1.8, dash='4 3'); p.seg(7, 2, 7, 10, col='orange', w=1.8, dash='4 3')
    p.pt(1, 2, 'navy', 4.4); p.pt(7, 10, 'navy', 4.4); p.pt(4, 6, 'green', 5)
    p.label(p.X(1) - 6, p.Y(2) + 14, 'A(1, 2)', size=10.5, col='navy', anchor='start', bold=True)
    p.label(p.X(7) - 6, p.Y(10) - 7, 'B(7, 10)', size=10.5, col='navy', anchor='end', bold=True)
    p.label(p.X(4) + 7, p.Y(6) + 14, 'M(4, 6)', size=10.5, col='green', anchor='start', bold=True)
    p.label(p.X(4), p.Y(2) + 14, 'Δ*x* = 6', size=10.5, col='orange', bold=True)
    p.label(p.X(7) + 7, p.Y(6) + 4, 'Δ*y* = 8', size=10.5, col='orange', anchor='start', bold=True)
    p.label(p.X(2.2) - 6, p.Y(5.2) - 2, '*d* = 10', size=11, col='blue', anchor='end', bold=True)
    return p.svg()


def fig_circ():
    p = Plot(311, 300, -3, 10.2, -1.8, 11, l=24, r=10, t=10, b=18)
    p.grid(1, 1)
    p.axes(xticks=(-2, 2, 4, 6, 8), yticks=(2, 4, 6, 8, 10), size=9.5)
    cxp, cyp = p.X(3), p.Y(5)
    rp = p.X(8) - p.X(3)
    p.circ(cxp, cyp, rp, fill='lblue', stroke='navy', sw=2.2, op=.75)
    p.seg(-1, 2, 7, 8, col='purple', w=2.2)
    p.pt(-1, 2, 'navy', 4.4); p.pt(7, 8, 'navy', 4.4); p.pt(3, 5, 'green', 5)
    p.pt(6, 9, 'orange', 4.8); p.pt(1, 1, 'purple', 4.8)
    p.label(p.X(-1) - 6, p.Y(2) + 14, 'A(−1, 2)', size=10.5, col='navy', anchor='start', bold=True)
    p.label(p.X(7) + 6, p.Y(8) + 14, 'B(7, 8)', size=10.5, col='navy', anchor='start', bold=True)
    p.label(p.X(3) - 6, p.Y(5) + 17, 'M(3, 5)', size=10.5, col='green', anchor='end', bold=True)
    p.label(p.X(6) - 8, p.Y(9) - 6, 'P(6, 9) sobre', size=10, col='orange', anchor='end', bold=True)
    p.label(p.X(1) - 6, p.Y(1) + 14, 'Q(1, 1) dentro', size=10, col='purple', anchor='start', bold=True)
    p.text(p.X(10.2) - 2, p.Y(-0.8), '(*x*−3)² + (*y*−5)² = 25', size=10.5, col='navy', anchor='end', bold=True)
    return p.svg()


def fig_exp_log():
    p = Plot(278, 280, -2.4, 9.4, -2.4, 9.4, l=26, r=10, t=10, b=18)
    p.grid(1, 1)
    p.axes(xticks=(-2, 2, 4, 6, 8), yticks=(-2, 2, 4, 6, 8), size=9.5)
    p.seg(-2, -2, 9, 9, col='mgrey', w=1.4, dash='5 4')
    p.curve(lambda x: 2 ** x, -2.4, 3.2, col='blue', w=2.8, ylim=(-2.4, 9.4))
    p.curve(lambda x: math.log2(x), 0.19, 9.3, col='purple', w=2.8, ylim=(-2.4, 9.4))
    p.curve(lambda x: 0.5 ** x, -2.4, 3.2, col='orange', w=2, dash='4 3', ylim=(-2.4, 9.4))
    for x, y, c_ in ((0, 1, 'blue'), (1, 2, 'blue'), (3, 8, 'blue'), (1, 0, 'purple'), (2, 1, 'purple'), (8, 3, 'purple')):
        p.pt(x, y, c_, 3.8)
    p.label(p.X(3.2) + 4, p.Y(8.6), '2ˣ', size=11.5, col='blue', anchor='start', bold=True)
    p.label(p.X(9.2) - 4, p.Y(3.3), 'log₂ *x*', size=11, col='purple', anchor='end', bold=True)
    p.label(p.X(-2.3) + 6, p.Y(5.2), '(½)ˣ', size=11, col='orange', anchor='start', bold=True)
    p.label(p.X(7.3), p.Y(8.1), '*y* = *x*', size=10, col='grey', anchor='start')
    p.label(p.X(0) + 7, p.Y(1) - 6, '(0, 1)', size=9.5, col='blue', anchor='start')
    p.label(p.X(1) + 5, p.Y(0) + 13, '(1, 0)', size=9.5, col='purple', anchor='start')
    return p.svg(width='100%')


def p_analitica():
    band = chapter_band(8, 'Geometria analítica, potências e logaritmos', 'tópicos 38 · 39 + função exponencial')
    c38 = card('Distância entre dois pontos, ponto médio e circunferência', 38, 'B', cols(
        stack(
            formula((r'd_{AB}=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}', 'Pitágoras no plano'),
                    (r'M=\Big(\dfrac{x_A+x_B}{2},\ \dfrac{y_A+y_B}{2}\Big)', 'ponto médio'),
                    (r'(x-a)^2+(y-b)^2=r^2', 'circunferência: centro (a, b), raio r'), label='PLANO CARTESIANO'),
            when('Mapas com coordenadas, localização de antenas/torres/postos, “alcance de sinal”, ponto equidistante, trajeto entre pontos. '
                 'Ponto P e circunferência: \\(d(P,C)\\lt r\\) dentro · \\(=r\\) sobre · \\(\\gt r\\) fora.'),
            err('Esquecer a <b>raiz</b> na distância, errar o sinal em \\((x-a)\\) (o centro de \\((x+2)^2\\) é <b>−2</b>) e confundir \\(r^2\\) com \\(r\\).'),
            gap='1.3mm'),
        stack(fig(fig_dist(), 'Distância = hipotenusa do triângulo retângulo de catetos Δx e Δy; o ponto médio é a média das coordenadas.'),),
        ratio='1.05fr 1fr', gap='3.5mm', align='center'))
    retas = card('Retas no plano (complemento)', None, 'B', cols(
        formula((r'm=\dfrac{\Delta y}{\Delta x}\qquad y-y_0=m\,(x-x_0)', 'declividade e reta por um ponto'),
                (r'm_1=m_2\ (\parallel)\qquad m_1\cdot m_2=-1\ (\perp)', 'paralelas · perpendiculares'), label='RETAS'),
        mini('Reta por (1, 2) e (7, 10):', '', r'\(m=\tfrac{8}{6}=\tfrac43\); perpendicular a ela tem \(m=-\tfrac34\)', '.'),
        ratio='1.35fr 1fr', gap='3mm', align='center'))
    e13 = ex(13, 'Cobertura circular com diâmetro AB',
             'Duas torres de transmissão estão nas posições A(−1, 2) e B(7, 8) de um mapa em quilômetros. Uma antena cobrirá a região circular que tem o segmento AB como diâmetro. '
             'Determine a equação da circunferência de cobertura e diga o que ocorre com as cidades P(6, 9) e Q(1, 1).',
             '<b>Ponto médio</b> (centro), <b>distância entre pontos</b> (diâmetro → raio) e <b>equação da circunferência</b>; depois compara-se a distância de cada cidade ao centro com o raio.',
             r'Centro: \(M=\Big(\dfrac{-1+7}{2},\dfrac{2+8}{2}\Big)=(3,5)\). Diâmetro: \(d_{AB}=\sqrt{8^2+6^2}=10\Rightarrow r=5\).'
             r'<br>Equação: \((x-3)^2+(y-5)^2=25\).'
             r'<br>P: \((6-3)^2+(9-5)^2=9+16=25\) → <b>sobre</b> a circunferência. Q: \((1-3)^2+(1-5)^2=4+16=20\lt25\) → <b>dentro</b>.',
             r'\((x-3)^2+(y-5)^2=25\); P está <b>no limite</b> da cobertura e Q <b>recebe sinal</b>.',
             shortcut=r'P(6, 9) e o centro (3, 5) formam um triângulo 3-4-5: distância 5 = raio, sem calcular raiz ✔.')
    r = rec(('Distância entre (0, 0) e (5, 12)?', '13'),
            ('Ponto médio de (2, −4) e (8, 6)?', '(5, 1)'),
            ('Centro e raio de (x + 1)² + (y − 2)² = 9?', 'C(−1, 2) · r = 3'))
    return band + c38 + cols(e13, fig(fig_circ(), None), ratio='1.25fr 1fr', gap='3mm', align='start') + retas + r


def p_log():
    pot = card('Propriedades de potenciação, radiciação e logaritmos', 39, 'B', cols(
        stack(
            tbl(['Potências', 'Radicais'],
                [[r'\(a^m\cdot a^n=a^{m+n}\)', r'\(\sqrt[n]{ab}=\sqrt[n]{a}\,\sqrt[n]{b}\)'],
                 [r'\(\dfrac{a^m}{a^n}=a^{m-n}\)', r'\(\sqrt[n]{\tfrac ab}=\tfrac{\sqrt[n]{a}}{\sqrt[n]{b}}\)'],
                 [r'\((a^m)^n=a^{mn}\)', r'\(\sqrt[n]{a^m}=a^{m/n}\)'],
                 [r'\((ab)^n=a^nb^n\)', r'\(\sqrt{a^2}=|a|\)'],
                 [r'\(a^{-n}=\dfrac1{a^n}\quad a^0=1\)', r'\(\dfrac{1}{\sqrt a}=\dfrac{\sqrt a}{a}\)']], widths=['50%', '50%']),
            err('\\((a+b)^2\\neq a^2+b^2\\) · \\(\\sqrt{a+b}\\neq\\sqrt a+\\sqrt b\\) · \\(-2^2=-4\\) mas \\((-2)^2=4\\) · \\(2^{3^2}=2^9\\) (não \\(8^2\\)) · \\(a^{-n}\\) <u>não</u> é negativo.'),
            gap='1.3mm'),
        stack(
            formula((r'\log_b a=x\iff b^x=a\quad(a\gt0,\ b\gt0,\ b\neq1)', ''),
                    (r'\log(ab)=\log a+\log b\qquad\log\tfrac ab=\log a-\log b', ''),
                    (r'\log a^n=n\log a\qquad\log_b a=\dfrac{\log_c a}{\log_c b}', 'mudança de base'),
                    (r'\log_b1=0\quad\log_bb=1\quad b^{\log_ba}=a', ''), label='LOGARITMOS'),
            tbl(['log 2', 'log 3', 'log 5', 'log 10'], [['≈ 0,30', '≈ 0,48', '1 − log 2 ≈ 0,70', '1']], cls='c'),
            gap='1.3mm'),
        ratio='1fr 1fr', gap='3.5mm', align='start') +
        cols(mem('<b>Logaritmo é o expoente</b>: “a que potência eleva-se b para chegar a a?”. \\(\\log_28=3\\) porque \\(2^3=8\\). “log” sem base = base 10. '
                 'Log <u>transforma produto em soma</u> e potência em produto — e resolve equações em que a incógnita está no expoente.'),
             mini('log 12:', 'dado log 2 = 0,30 e log 3 = 0,48.', r'\(\log12=\log(2^2\cdot3)=2(0{,}30)+0{,}48\)', '= 1,08.'), gap='3mm'))

    ex_ = card('Função exponencial e sua inversa, o logaritmo', None, 'B', cols(
        stack(
            formula((r'f(x)=a\cdot b^{x}\quad(b\gt0,\ b\neq1)', 'b > 1 cresce · 0 < b < 1 decresce'),
                    (r'b^{x}=c\ \Rightarrow\ x=\log_b c', 'resolve o expoente'), label='EXPONENCIAL'),
            when('<b>Incógnita no expoente</b>: crescimento populacional, juros compostos, decaimento radioativo (meia-vida), depreciação, resfriamento, dobra de valores. '
                 '<b>Modelo:</b> quantidade final = inicial × (fator)<sup>nº de períodos</sup>.'),
            mini('Meia-vida de 8 h, 80 g iniciais:', 'quando restam 5 g? E 10% (8 g)?', r'\(80\to5\): \(\tfrac{80}{5}=16=2^4\) → 4 meias-vidas = 32 h. \(10\%\): \(\left(\tfrac12\right)^{t/8}=0{,}1\Rightarrow\tfrac t8=\tfrac{1}{0{,}30}\)', '→ t ≈ 26,7 h.'),
            gap='1.3mm'),
        stack(fig(fig_exp_log(), 'Exponencial e logaritmo são <b>inversas</b>: gráficos espelhados na reta y = x. Ambos passam pelos “1”: (0, 1) e (1, 0).'), ),
        ratio='1.15fr 1fr', gap='3.5mm', align='center'))
    esc = card('Equações exponenciais e escalas logarítmicas', None, 'B', cols(
        stack(tbl(['Equação', 'Como resolver', 'x'],
                  [[r'\(2^x=32\)', 'mesma base: \\(32=2^5\\)', '5'], [r'\(3^{x+1}=27\)', '\\(27=3^3\\Rightarrow x+1=3\\)', '2'],
                   [r'\(4^x=8\)', '\\(2^{2x}=2^3\\Rightarrow 2x=3\\)', '3/2'], [r'\(1{,}1^x=2\)', 'não dá para igualar bases → logaritmo', r'\(\tfrac{\log2}{\log1{,}1}\)']],
                  cls='c', widths=['26%', '54%', '20%']),
              mini('Capital dobra a 5% a.m.?', '', r'\(1{,}05^t=2\Rightarrow t=\dfrac{\log2}{\log1{,}05}\)', 'dado log 1,05 ≈ 0,021 → t ≈ 14 meses.'), gap='1.3mm'),
        stack(formula((r'\mathrm{pH}=-\log[\mathrm{H}^+]\qquad \beta=10\log\dfrac{I}{I_0}', 'pH · nível sonoro (dB)'), label='ESCALAS LOGARÍTMICAS'),
              mem('Na escala logarítmica, <b>+1 unidade = ×10</b> na grandeza: pH 3 é 100× mais ácido que pH 5; +10 dB = intensidade ×10; +1 de magnitude (log) ≈ ×10 de amplitude.'), gap='1.3mm'),
        ratio='1.2fr 1fr', gap='3.5mm', align='start'))
    r = rec(('2⁵ · 2⁻² · 4?', '2⁵⁻²·2² = 2⁵ = 32'), ('log₃ 81?', '4 (3⁴ = 81)'),
            ('População dobra a cada 3 anos: fator em 9 anos?', '2³ = 8'))
    return pot + ex_ + esc + r


def pages():
    return [p_analitica(), p_log()]
