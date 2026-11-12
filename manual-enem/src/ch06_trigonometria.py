"""Capítulo 6 – Trigonometria (tópicos 29, 30, 31, 32)."""
import math
from lib import *
from svg import Fig, Plot

LABEL = 'CAP. 6 · TRIGONOMETRIA'
R2, R3 = math.sqrt(2), math.sqrt(3)


def fig_trig_tri():
    f = Fig(300, 168)
    B, C, A = (26, 132), (246, 132), (246, 38)
    f.poly([B, C, A], fill='lblue', stroke='navy', sw=2.2)
    f.rightangle(C[0], C[1], (-1, 0), (0, -1), 10)
    th = math.degrees(math.atan2(132 - 38, 246 - 26))
    f.arc(B[0], B[1], 32, 0, th, col='orange', sw=2.4)
    f.label(B[0] + 44, B[1] - 6, 'θ', size=13, col='orange', bold=True, anchor='start')
    f.label(136, 152, 'cateto ADJACENTE a θ', size=10.5, col='blue', bold=True)
    f.label(254, 88, 'cateto', size=10.5, col='purple', anchor='start', bold=True)
    f.label(254, 101, 'OPOSTO', size=10.5, col='purple', anchor='start', bold=True)
    f.label(254, 114, 'a θ', size=10.5, col='purple', anchor='start', bold=True)
    f.label(118, 70, 'HIPOTENUSA', size=10.5, col='navy', bold=True)
    f.text(118, 83, '(oposta ao ângulo reto)', size=9, col='grey')
    return f.svg()


def fig_metricas():
    f = Fig(300, 168)
    B, C = (14, 138), (286, 138)
    H = (14 + 3.6 / 10 * 272, 138)
    A = (H[0], 138 - 4.8 / 10 * 272 * 0.9)
    f.poly([A, B, C], fill='lblue', stroke='navy', sw=2.2)
    f.line(A[0], A[1], H[0], H[1], col='purple', w=2, dash='4 3')
    f.rightangle(H[0], H[1], (1, 0), (0, -1), 8)
    f.poly([B, A, H], fill='lgreen', stroke='navy', sw=1, op=.7)
    f.poly([C, A, H], fill='lorange', stroke='navy', sw=1, op=.7)
    f.poly([A, B, C], stroke='navy', sw=2.2)
    f.rightangle(A[0], A[1], (-0.5, 0.86), (0.5, 0.86), 9) if False else None
    for p, t, dx, dy in ((A, 'A', 0, -6), (B, 'B', -2, 14), (C, 'C', 2, 14), (H, 'H', 0, 14)):
        f.label(p[0] + dx, p[1] + dy, t, size=11, col='navy', bold=True)
    f.label((B[0] + A[0]) / 2 - 10, (B[1] + A[1]) / 2, '*c*', size=11.5, col='navy', anchor='end', bold=True)
    f.label((C[0] + A[0]) / 2 + 12, (C[1] + A[1]) / 2, '*b*', size=11.5, col='navy', anchor='start', bold=True)
    f.label(H[0] + 7, (A[1] + H[1]) / 2 + 4, '*h*', size=11.5, col='purple', anchor='start', bold=True)
    f.dim(B[0], 156, H[0], 156, '*n*', col='grey', text_dy=-3)
    f.dim(H[0], 156, C[0], 156, '*m*', col='grey', text_dy=-3)
    f.text(150, 166, '*a* = *m* + *n*', size=10, col='navy', bold=True)
    return f.svg()


def fig_notaveis():
    f = Fig(342, 150)
    u = 54
    # 45-45-90
    x0, y0 = 14, 100
    f.poly([(x0, y0), (x0 + u, y0), (x0, y0 - u)], fill='lblue', stroke='navy', sw=2)
    f.rightangle(x0, y0, (1, 0), (0, -1), 8)
    f.label(x0 + u / 2, y0 + 14, '1', size=11, col='blue', bold=True); f.label(x0 - 8, y0 - u / 2 + 4, '1', size=11, col='blue', anchor='end', bold=True)
    f.label(x0 + u / 2 + 14, y0 - u / 2 - 6, '√2', size=11, col='navy', bold=True)
    f.label(x0 + u - 20, y0 - 4, '45°', size=9.5, col='orange', bold=True); f.label(x0 + 4, y0 - u + 20, '45°', size=9.5, col='orange', anchor='start', bold=True)
    f.text(x0 + u / 2 + 6, 128, 'metade de um quadrado', size=9.4, col='grey')
    f.text(x0 + u / 2 + 6, 140, 'de lado 1', size=9.4, col='grey')
    # 30-60-90 (metade do equilátero de lado 2)
    x1, y1 = 172, 100
    L = R3 * u
    f.poly([(x1, y1), (x1 + L, y1), (x1, y1 - u)], fill='lgreen', stroke='navy', sw=2)
    f.rightangle(x1, y1, (1, 0), (0, -1), 8)
    f.label(x1 + L / 2, y1 + 14, '√3', size=11, col='blue', bold=True); f.label(x1 - 8, y1 - u / 2 + 4, '1', size=11, col='blue', anchor='end', bold=True)
    f.label(x1 + L / 2 + 14, y1 - u / 2 - 4, '2', size=11, col='navy', bold=True)
    f.label(x1 + L - 24, y1 - 4, '30°', size=9.5, col='orange', bold=True); f.label(x1 + 4, y1 - u + 22, '60°', size=9.5, col='orange', anchor='start', bold=True)
    f.text(x1 + L / 2 + 6, 128, 'metade de um triângulo', size=9.4, col='grey')
    f.text(x1 + L / 2 + 6, 140, 'equilátero de lado 2', size=9.4, col='grey')
    return f.svg()


def fig_torre():
    f = Fig(342, 172)
    gy = 140
    xt = 280; h = 20 * R3
    sc = 3.1
    ht = h * sc
    B = xt - ht / R3  # ponto B (60°)
    A = B - 40 * sc * 0.62  # 40 m reduzido na escala horizontal (aprox.)
    A = xt - ht * R3
    f.line(6, gy, 336, gy, col='ink', w=1.6)
    f.rect(xt - 6, gy - ht, 12, ht, fill='lgreen', stroke='navy', sw=1.6)
    f.line(xt, gy - ht, xt, gy, col='navy', w=1)
    # visadas
    f.line(A, gy, xt, gy - ht, col='orange', w=1.6, dash='4 3')
    f.line(B, gy, xt, gy - ht, col='purple', w=1.8, dash='4 3')
    f.dot(A, gy, 3.6, 'navy'); f.dot(B, gy, 3.6, 'navy')
    f.label(A, gy + 14, 'A', size=10.5, col='navy', bold=True); f.label(B, gy + 14, 'B', size=10.5, col='navy', bold=True)
    f.arc(A, gy, 28, 0, 30, col='orange', sw=2.2); f.label(A + 33, gy - 4, '30°', size=10, col='orange', anchor='start', bold=True)
    f.arc(B, gy, 22, 0, 60, col='purple', sw=2.2); f.label(B + 25, gy - 8, '60°', size=10, col='purple', anchor='start', bold=True)
    f.dim(A, gy + 24, B, gy + 24, '40 m', col='grey', text_dy=-4)
    f.line(xt + 14, gy - ht, xt + 14, gy, col='green', w=1.6, arrow=True, arrow0=True)
    f.label(xt + 20, gy - ht / 2, '*h*', size=11.5, col='green', anchor='start', bold=True)
    f.label(xt - 4, gy - ht - 6, 'topo', size=10, col='navy', anchor='end', bold=True)
    return f.svg()


def fig_triangulo():
    f = Fig(250, 150)
    A, B, C = (60, 18), (14, 128), (228, 118)
    f.poly([A, B, C], fill='lblue', stroke='navy', sw=2.2)
    for p, t, dx, dy in ((A, '*A*', 0, -6), (B, '*B*', -10, 12), (C, '*C*', 10, 12)):
        f.label(p[0] + dx, p[1] + dy, t, size=12, col='orange', bold=True)
    f.label((B[0] + C[0]) / 2, (B[1] + C[1]) / 2 + 16, '*a*', size=12, col='navy', bold=True)
    f.label((A[0] + C[0]) / 2 + 10, (A[1] + C[1]) / 2 - 4, '*b*', size=12, col='navy', anchor='start', bold=True)
    f.label((A[0] + B[0]) / 2 - 10, (A[1] + B[1]) / 2, '*c*', size=12, col='navy', anchor='end', bold=True)
    f.text(120, 90, 'cada lado é oposto', size=9.2, col='grey'); f.text(120, 102, 'ao ângulo de mesma letra', size=9.2, col='grey')
    return f.svg(width='100%')


def fig_circ_trig():
    f = Fig(250, 200)
    cx, cy, r = 112, 100, 72
    f.line(cx - r - 14, cy, cx + r + 22, cy, col='ink', w=1.2, arrow=True); f.line(cx, cy + r + 12, cx, cy - r - 20, col='ink', w=1.2, arrow=True)
    f.circ(cx, cy, r, fill='lblue', stroke='navy', sw=1.8, op=.9)
    th = 60
    px, py = cx + r * math.cos(math.radians(th)), cy - r * math.sin(math.radians(th))
    qx = cx - r * math.cos(math.radians(th))
    f.line(cx, cy, px, py, col='navy', w=2.2)
    f.line(px, py, px, cy, col='purple', w=2.4); f.line(cx, cy, px, cy, col='blue', w=2.4)
    f.line(cx, cy, qx, py, col='mgrey', w=1.6, dash='4 3'); f.line(qx, py, qx, cy, col='mgrey', w=1.4, dash='4 3')
    f.dot(px, py, 3.8, 'navy'); f.circ(qx, py, 3.6, fill='white', stroke='orange', sw=1.8)
    f.arc(cx, cy, 20, 0, th, col='orange', sw=2.2); f.label(cx + 26, cy - 8, 'θ', size=11, col='orange', anchor='start', bold=True)
    f.label(px + 6, (py + cy) / 2 + 4, 'sen θ', size=10, col='purple', anchor='start', bold=True)
    f.label(cx + 6 + (px - cx) / 2 - 22, cy + 14, 'cos θ', size=10, col='blue', bold=True)
    f.label(cx + 12, cy - r / 2 - 14, '1', size=10.5, col='navy', bold=True)
    f.label(qx - 6, py - 7, '120°', size=9.6, col='orange', anchor='end', bold=True)
    f.label(px + 6, py - 7, '60°', size=9.6, col='navy', anchor='start', bold=True)
    f.text(cx, 190, 'sen² θ + cos² θ = 1  (Pitágoras no raio 1)', size=10, col='green', bold=True)
    return f.svg(width='100%')


def fig_elevacao():
    f = Fig(350, 176)
    gy = 156
    f.line(6, gy, 344, gy, col='ink', w=1.6)
    # prédio
    f.rect(246, 42, 56, gy - 42, fill='lblue', stroke='navy', sw=1.8)
    for k in range(4):
        for j in range(2):
            f.rect(256 + j * 24, 56 + k * 22, 14, 12, fill='white', stroke='mblue', sw=1)
    # observador 1 (no chão) - olhos
    ex_, ey_ = 40, 118
    f.circ(ex_, ey_ - 8, 6, fill='white', stroke='navy', sw=1.6); f.line(ex_, ey_ - 2, ex_, gy, col='navy', w=2.4)
    f.line(ex_, ey_, 246, ey_, col='mgrey', w=1.4, dash='4 3')
    f.line(ex_, ey_, 246, 42, col='purple', w=2, dash='5 3')
    ang = math.degrees(math.atan2(ey_ - 42, 246 - ex_))
    f.arc(ex_, ey_, 40, 0, ang, col='purple', sw=2.4)
    f.label(ex_ + 46, ey_ - 6, 'α', size=12, col='purple', bold=True, anchor='start')
    f.text(110, 100, 'elevação', size=9.8, col='purple', bold=True)
    # carro (chão) + observador no topo
    cxx = 150
    f.rect(cxx - 12, gy - 9, 24, 9, fill='lorange', stroke='orange', sw=1.4, rx=2)
    f.line(246, 42, 120, 42, col='mgrey', w=1.4, dash='4 3')
    f.line(246, 42, cxx, gy - 9, col='orange', w=2, dash='5 3')
    beta = math.degrees(math.atan2(gy - 9 - 42, 246 - cxx))
    f.arc(246, 42, 44, 180 + 0, 180 + beta, col='orange', sw=2.4)
    f.label(246 - 54, 42 + 34, 'β', size=12, col='orange', bold=True)
    f.text(206, 70, 'depressão', size=9.8, col='orange', bold=True) if False else None
    f.label(196, 58, 'depressão', size=9.8, col='orange', bold=True)
    f.arc(cxx, gy - 9, 30, 0, beta, col='orange', sw=2.2)
    f.label(cxx + 36, gy - 14, 'β', size=11, col='orange', bold=True, anchor='start')
    f.text(176, 14, 'Ângulos medidos a partir da HORIZONTAL (tracejada cinza)', size=10, col='navy', bold=True)
    f.text(176, 28, 'depressão em cima = elevação embaixo (alternos internos)', size=9.4, col='grey')
    return f.svg()


def fig_circ_notaveis():
    f = Fig(250, 210)
    ox, oy, r = 34, 178, 150
    f.line(ox - 8, oy, ox + r + 14, oy, col='ink', w=1.3, arrow=True); f.line(ox, oy + 8, ox, oy - r - 12, col='ink', w=1.3, arrow=True)
    f.path(f'M{ox + r},{oy} A{r},{r} 0 0 0 {ox},{oy - r}', stroke='navy', sw=2, fill='none')
    f.sector(ox, oy, r, 0, 90, fill='lblue', stroke=None, op=.45)
    f.text(ox + r + 8, oy + 14, 'cos', size=9.5, col='blue', anchor='end', bold=True); f.text(ox - 4, oy - r - 4, 'sen', size=9.5, col='purple', anchor='end', bold=True)
    for ang, lab, col in ((30, '(√3/2 ; 1/2)', 'green'), (45, '(√2/2 ; √2/2)', 'blue'), (60, '(1/2 ; √3/2)', 'purple')):
        px, py = ox + r * math.cos(math.radians(ang)), oy - r * math.sin(math.radians(ang))
        f.line(ox, oy, px, py, col=col, w=1.8)
        f.line(px, py, px, oy, col='mgrey', w=1, dash='3 3'); f.line(px, py, ox, py, col='mgrey', w=1, dash='3 3')
        f.dot(px, py, 3.8, col)
        f.label(px + (6 if ang != 60 else 6), py - 6 if ang != 30 else py - 7, f'{ang}° {lab}', size=9.4, col=col, anchor='start', bold=True) if False else None
    f.label(ox + r * math.cos(math.radians(30)) - 4, oy - r * math.sin(math.radians(30)) - 8, '30°', size=10, col='green', anchor='end', bold=True)
    f.label(ox + r * math.cos(math.radians(45)) - 4, oy - r * math.sin(math.radians(45)) - 8, '45°', size=10, col='blue', anchor='end', bold=True)
    f.label(ox + r * math.cos(math.radians(60)) - 4, oy - r * math.sin(math.radians(60)) - 8, '60°', size=10, col='purple', anchor='end', bold=True)
    f.text(ox + r * math.cos(math.radians(30)) - 24, oy + 14, '√3/2', size=9, col='grey')
    f.text(ox + r * math.cos(math.radians(45)), oy + 14, '√2/2', size=9, col='grey')
    f.text(ox + r * math.cos(math.radians(60)), oy + 14, '1/2', size=9, col='grey')
    f.text(ox - 6, oy - r * math.sin(math.radians(30)) + 3, '1/2', size=9, col='grey', anchor='end')
    f.text(ox - 6, oy - r * math.sin(math.radians(45)) + 3, '√2/2', size=9, col='grey', anchor='end')
    f.text(ox - 6, oy - r * math.sin(math.radians(60)) + 3, '√3/2', size=9, col='grey', anchor='end')
    f.text(ox + 70, oy - r + 14, 'ponto = (cos θ , sen θ)', size=9.6, col='navy', bold=True, anchor='middle')
    return f.svg()


def fig_casos():
    f = Fig(350, 118)
    def tri(x0, title, sub, marks):
        A, B, C = (x0 + 54, 20), (x0 + 6, 82), (x0 + 106, 76)
        f.poly([A, B, C], fill='white', stroke='navy', sw=1.6)
        for kind, p, q in marks:
            if kind == 'side':
                f.line(*p, *q, col='green', w=3.4)
            elif kind == 'ang':
                f.circ(p[0], p[1], 8, fill='orange', op=.85)
        f.text(x0 + 56, 100, title, size=9.8, col='navy', bold=True)
        f.text(x0 + 56, 113, sub, size=8.8, col='grey')
    tri(0, 'Cossenos', '2 lados + ângulo entre eles', [('side', (54 + 0, 20), (6, 82)), ('side', (6, 82), (106, 76)), ('ang', (10, 80), None)])
    tri(117, 'Cossenos', '3 lados → ângulo', [('side', (117 + 54, 20), (117 + 6, 82)), ('side', (117 + 6, 82), (117 + 106, 76)), ('side', (117 + 106, 76), (117 + 54, 20))])
    tri(234, 'Senos', 'lado + ângulo oposto', [('side', (234 + 6, 82), (234 + 106, 76)), ('ang', (234 + 54, 24), None), ('ang', (234 + 12, 80), None)])
    return f.svg()


def fig_navios():
    f = Fig(260, 150)
    Pt = (30, 112)
    n1 = (Pt[0] + 30 * 6.2, Pt[1])
    n2 = (Pt[0] + 40 * 6.2 * math.cos(math.radians(60)), Pt[1] - 40 * 6.2 * math.sin(math.radians(60)))
    f.poly([Pt, n1, n2], fill='lblue', stroke='navy', sw=1.8)
    f.arc(Pt[0], Pt[1], 24, 0, 60, col='orange', sw=2.4)
    f.label(Pt[0] + 30, Pt[1] - 8, '60°', size=10, col='orange', anchor='start', bold=True)
    f.line(*n1, *n2, col='green', w=2.8, dash='5 3')
    f.dot(*Pt, 4, 'navy'); f.dot(*n1, 4, 'navy'); f.dot(*n2, 4, 'navy')
    f.label(Pt[0] - 4, Pt[1] + 16, 'porto', size=10, col='navy', anchor='middle', bold=True)
    f.label((Pt[0] + n1[0]) / 2, Pt[1] + 15, '30 km', size=10, col='navy', bold=True)
    f.label((Pt[0] + n2[0]) / 2 - 6, (Pt[1] + n2[1]) / 2 - 2, '40 km', size=10, col='navy', anchor='end', bold=True)
    f.label((n1[0] + n2[0]) / 2 + 8, (n1[1] + n2[1]) / 2 + 2, '*d* = ?', size=11, col='green', anchor='start', bold=True)
    f.text(130, 142, 'LAL → lei dos cossenos', size=9.6, col='grey')
    return f.svg()


def p_razoes():
    band = chapter_band(6, 'Trigonometria', 'tópicos 29 · 30 · 31 · 32')
    c29 = card('Razões trigonométricas no triângulo retângulo', 29, 'A', cols(
        stack(
            formula((r'\sen\theta=\dfrac{\text{cateto oposto}}{\text{hipotenusa}}', ''),
                    (r'\cos\theta=\dfrac{\text{cateto adjacente}}{\text{hipotenusa}}', ''),
                    (r'\tg\theta=\dfrac{\text{cateto oposto}}{\text{cateto adjacente}}=\dfrac{\sen\theta}{\cos\theta}', ''), label='SEN · COS · TG'),
            mem('<b>SOH – CAH – TOA</b>: <b>S</b>eno = <b>O</b>posto/<b>H</b>ipotenusa · <b>C</b>osseno = <b>A</b>djacente/<b>H</b>ipotenusa · <b>T</b>angente = <b>O</b>posto/<b>A</b>djacente. '
                'Para os dois ângulos agudos: \\(\\sen\\theta=\\cos(90^\\circ-\\theta)\\).'),
            gap='1.3mm'),
        fig(fig_trig_tri(), 'Oposto e adjacente dependem do ângulo escolhido (θ); a hipotenusa não muda.'),
        ratio='1fr 1.08fr', gap='3.5mm', align='center') +
        cols(when('Triângulo retângulo com <b>um ângulo agudo + um lado</b> conhecidos: altura de prédio/árvore/poste, <b>ângulo de elevação</b> (visada para cima) ou depressão, '
                  'inclinação de rampa e telhado (\\(\\tg\\theta=\\tfrac{\\text{altura}}{\\text{base}}\\)).'),
             err('Escolher as razões pelo lado “aparente” e não em relação a θ; deixar a calculadora em radianos; usar \\(\\sen\\) quando os dados (oposto e adjacente) pedem \\(\\tg\\). '
                 'Rampa de 30°: o ângulo é com a horizontal, não com a vertical.'), ratio='1.1fr 1fr', gap='3mm'))

    c30 = card('Relações métricas do triângulo retângulo', 30, 'B', cols(
        fig(fig_metricas(), 'Exemplo 6–8–10: h = 4,8 · m = 6,4 · n = 3,6.'),
        stack(
            formula((r'a^2=b^2+c^2', 'Pitágoras'),
                    (r'b^2=a\cdot m\qquad c^2=a\cdot n', 'cateto² = hipotenusa × projeção'),
                    (r'h^2=m\cdot n', 'altura² = produto das projeções'),
                    (r'b\cdot c=a\cdot h', 'catetos × = hipotenusa × altura'), label='RELAÇÕES MÉTRICAS'),
            when('<b>Altura relativa à hipotenusa</b> (a que “cai” do ângulo reto), projeções dos catetos, “semelhança de triângulos” em figuras retangulares. '
                 'A altura divide o triângulo em <b>dois triângulos semelhantes ao original</b>.'),
            gap='1.3mm'),
        ratio='1fr 1.05fr', gap='3.5mm', align='center'))
    el = card('Ângulo de elevação e de depressão', None, 'A', cols(
        fig(fig_elevacao(), None),
        stack(when('“<b>sob um ângulo de X°</b>”, “avista o topo”, “ângulo de visada”: monte o triângulo retângulo com a <u>horizontal</u> como um dos lados. '
                   'Some a <b>altura do observador</b> (olhos) à altura calculada, se houver.'),
              mini('Rampa de 8%:', 'tg θ = 0,08.', 'sobe 8 m a cada 100 m na horizontal; θ ≈ 4,6°.', ''),
              mini('Prédio:', 'a 30 m da base, olhos a 1,6 m, α = 60° (√3 ≈ 1,73).', r'\(h=30\tg60^\circ+1{,}6=51{,}9+1{,}6\)', '≈ 53,5 m.'), gap='1.4mm'),
        ratio='1.35fr 1fr', gap='3.5mm', align='center'))
    ap = cols(mini('Teste 6–8–10:', 'altura h pela relação b·c = a·h.', r'\(6\cdot8=10\cdot h\Rightarrow h=4{,}8\); \(h^2=m\cdot n:\ 4{,}8^2=6{,}4\cdot3{,}6=23{,}04\) ✔', ''),
              mini('Rampa:', 'sobe 1,5 m em 6 m de comprimento (inclinada).', r'\(\sen\theta=\tfrac{1{,}5}{6}=0{,}25\)', '→ θ ≈ 14,5°.'), gap='3mm')
    r = rec(('Hipotenusa 13 e cateto oposto 5: sen θ?', '5/13'),
            ('Cateto adjacente 8 e oposto 6: tg θ?', '6/8 = 0,75'),
            ('Em qual relação aparece h² (altura relativa)?', 'h² = m · n'))
    return band + c29 + el + c30 + ap + r


def p_notaveis():
    c31 = card('Ângulos notáveis: 30°, 45° e 60°', 31, 'A', cols(
        stack(
            tbl(['θ', 'sen', 'cos', 'tg'],
                [['0°', '0', '1', '0'],
                 ['30°', r'\(\tfrac12\)', r'\(\tfrac{\sqrt3}{2}\)', r'\(\tfrac{\sqrt3}{3}\)'],
                 ['45°', r'\(\tfrac{\sqrt2}{2}\)', r'\(\tfrac{\sqrt2}{2}\)', r'\(1\)'],
                 ['60°', r'\(\tfrac{\sqrt3}{2}\)', r'\(\tfrac12\)', r'\(\sqrt3\)'],
                 ['90°', '1', '0', '—']], cls='c'),
            mem('<b>Seno:</b> \\(\\tfrac{\\sqrt1}{2},\\tfrac{\\sqrt2}{2},\\tfrac{\\sqrt3}{2}\\) (30°, 45°, 60°) — <b>cosseno</b>: a mesma lista de trás para a frente. '
                '<b>tg = sen ÷ cos</b>. Aproximações: \\(\\sqrt2\\approx1{,}41\\) · \\(\\sqrt3\\approx1{,}73\\) · \\(\\tfrac{\\sqrt3}{3}\\approx0{,}58\\).'),
            when('Enunciado com ângulo de <b>30°, 45° ou 60°</b> sem tabela/calculadora. Se o ENEM dá outro ângulo, vem acompanhado de uma tabela (sen 20°, cos 20°…).'),
            gap='1.3mm'),
        stack(fig(fig_notaveis(), 'Os valores saem de duas figuras: a diagonal do quadrado (√2) e a altura do triângulo equilátero (√3).'),
              fig(fig_circ_notaveis(), 'No 1º quadrante o ponto da circunferência de raio 1 é (cos θ, sen θ).'), gap='1.6mm'),
        ratio='1fr 1.05fr', gap='3.5mm', align='start'))

    e11 = ex(11, 'Altura de uma torre com duas visadas',
             'Um topógrafo vê o topo de uma torre vertical, de um ponto A, sob um ângulo de elevação de 30°. Aproximando-se 40 m em direção à base, até o ponto B, '
             'passa a vê-lo sob 60°. Ignorando a altura do aparelho, qual é a altura da torre? (Use √3 ≈ 1,73.)',
             '<b>Dois triângulos retângulos</b> que compartilham a altura h; ângulos notáveis → \\(\\tg 30^\\circ=\\tfrac{\\sqrt3}{3}\\) e \\(\\tg 60^\\circ=\\sqrt3\\). A incógnita extra é a distância x de B à base.',
             r'Em B: \(\tg60^\circ=\dfrac{h}{x}\Rightarrow x=\dfrac{h}{\sqrt3}\). Em A: \(\tg30^\circ=\dfrac{h}{x+40}\Rightarrow x+40=h\sqrt3\).'
             r'<br>Substituindo: \(\dfrac{h}{\sqrt3}+40=h\sqrt3\Rightarrow 40=h\Big(\sqrt3-\dfrac{1}{\sqrt3}\Big)=h\cdot\dfrac{2}{\sqrt3}\Rightarrow h=20\sqrt3\).'
             r'<br>\(h=20\cdot1{,}73=34{,}6\).',
             r'Altura da torre ≈ <b>34,6 m</b> (e a distância de B à base é \(x=\tfrac{h}{\sqrt3}=20\) m).',
             shortcut=r'Confira: \(\tg30^\circ=\dfrac{34{,}6}{20+40}=0{,}577\approx0{,}58\) ✔. Atalho geral: entre as visadas de 30° e 60°, o triângulo ABtopo é <b>isósceles</b> (ângulo de 30° no topo), logo \(AB=B\text{topo}=40\) e \(h=40\cdot\sen60^\circ=20\sqrt3\).')
    ap = cols(
        mini('Sombra de poste:', 'sol a 45° e sombra de 8 m.', r'\(\tg45^\circ=\tfrac{h}{8}\Rightarrow h=8\cdot1\)', '= 8 m.'),
        mini('Escada:', '6 m de comprimento forma 60° com o chão.', r'\(h=6\sen60^\circ=6\cdot\tfrac{\sqrt3}{2}=3\sqrt3\)', '≈ 5,2 m de altura.'), gap='3mm')
    r = rec(('sen 30° · cos 60° · tg 45°?', '1/2 · 1/2 · 1'),
            ('Ângulo de elevação 45° e distância horizontal 12 m: altura?', '12 m (tg 45° = 1)'),
            ('Se sen θ = cos θ, quanto vale θ?', '45°'))
    return c31 + cols(e11, fig(fig_torre(), 'Duas visadas para o mesmo topo: A (30°) e B (60°), com AB = 40 m.'), ratio='1.55fr 1fr', gap='3mm', align='start') + ap + r


def p_leis():
    c32 = card('Lei dos senos, lei dos cossenos e relação fundamental', 32, 'B', cols(
        stack(
            formula((r'\dfrac{a}{\sen A}=\dfrac{b}{\sen B}=\dfrac{c}{\sen C}=2R', 'lei dos senos (R = raio do círculo circunscrito)'),
                    (r'a^2=b^2+c^2-2bc\cos A', 'lei dos cossenos'),
                    (r'\sen^2\theta+\cos^2\theta=1', 'relação fundamental'),
                    (r'A_{\triangle}=\tfrac12\,b\,c\,\sen A', 'área com dois lados e o ângulo entre eles'), label='TRIÂNGULO QUALQUER'),
            gap='1.2mm'),
        fig(fig_triangulo(), None), ratio='1.4fr 1fr', gap='3mm', align='center') +
        tbl(['O que o enunciado dá', 'Lei', 'Como pensar'],
            [['2 lados e o ângulo <b>entre</b> eles (LAL)', '<b class="g">Cossenos</b>', 'achar o 3º lado: \\(a^2=b^2+c^2-2bc\\cos A\\)'],
             ['3 lados (LLL) e quer um ângulo', '<b class="g">Cossenos</b>', 'isole \\(\\cos A=\\dfrac{b^2+c^2-a^2}{2bc}\\)'],
             ['1 lado + 2 ângulos, ou lado + ângulo <b>oposto</b> a ele', '<b class="bl">Senos</b>', 'razão lado ÷ seno do ângulo oposto é constante'],
             ['ângulo reto', 'Pitágoras / SOH-CAH-TOA', 'a lei dos cossenos com 90° vira Pitágoras (cos 90° = 0)']], widths=['38%', '20%', '42%']))

    cc = cols(
        stack(fig(fig_circ_trig(), None),
              ),
        stack(
            err('<b>Ângulos obtusos:</b> \\(\\sen120^\\circ=\\sen60^\\circ=\\tfrac{\\sqrt3}{2}\\), mas \\(\\cos120^\\circ=-\\cos60^\\circ=-\\tfrac12\\). Esquecer o sinal negativo na lei dos cossenos é o erro mais comum.'),
            mem('<b>Seno</b> = altura do ponto na circunferência de raio 1; <b>cosseno</b> = posição horizontal. '
                'Por isso \\(\\sen^2+\\cos^2=1\\) (Pitágoras) e ângulos suplementares têm <u>mesmo seno</u> e cossenos <u>opostos</u>.'),
            gap='1.4mm'),
        ratio='1fr 1.25fr', gap='3.5mm', align='center')
    nav = cols(fig(fig_navios(), None),
               stack(mini('Dois navios:', 'saem do mesmo porto em rotas de 60°; após 2 h estão a 30 km e 40 km do porto.',
                          r'\(d^2=30^2+40^2-2\cdot30\cdot40\cos60^\circ=2500-1200=1300\)', '→ d ≈ 36 km.'),
                     mini('Seno:', 'A = 45°, B = 60°, a = 10.', r'\(b=\dfrac{a\,\sen B}{\sen A}=\dfrac{10\cdot\frac{\sqrt3}{2}}{\frac{\sqrt2}{2}}=5\sqrt6\)', '≈ 12,2.'), gap='1.6mm'),
               ratio='1fr 1.3fr', gap='3.5mm', align='center')
    r = rec(('Triângulo com lados 5, 5 e ângulo entre eles de 60°: 3º lado?', 'a² = 25 + 25 − 50·½ = 25 → a = 5'),
            ('Se sen θ = 3/5 (θ agudo), cos θ?', '4/5 (3² + 4² = 5²)'),
            ('Área de triângulo com lados 6 e 8 e ângulo de 30° entre eles?', '½·6·8·½ = 12'))
    return c32 + cc + nav + r


def pages():
    return [p_razoes(), p_notaveis(), p_leis()]
