"""Capítulo 5 – Geometria plana e polígonos (tópicos 18–28)."""
import math
from lib import *
from svg import Fig, Plot, polygon_pts

LABEL = 'CAP. 5 · GEOMETRIA PLANA E POLÍGONOS'
R3 = math.sqrt(3)


# ------------------------------------------------------------------ figuras
def fig_poli_soma():
    f = Fig(180, 132)
    V = [(14, 76), (40, 24), (94, 10), (150, 40), (136, 100), (70, 120)]
    cols_ = ['lblue', 'lpurple', 'lgreen', 'lorange']
    for k in range(4):
        f.poly([V[0], V[k + 1], V[k + 2]], fill=cols_[k], stroke='navy', sw=1.2)
    f.poly(V, stroke='navy', sw=2)
    cen = lambda *ps: (sum(p[0] for p in ps) / 3, sum(p[1] for p in ps) / 3 + 4)
    for k in range(4):
        x, y = cen(V[0], V[k + 1], V[k + 2])
        f.text(x, y, '180°', size=9.6, col='navy', bold=True)
    for v in V:
        f.dot(v[0], v[1], 2.8, 'navy')
    f.text(90, 134, '', size=1)
    return f.svg()


def fig_hexa():
    f = Fig(350, 176)
    r = 56
    cx, cy = 90, 92
    P = polygon_pts(6, cx, cy, r, rot=0)
    f.poly(P, fill='lblue', stroke='navy', sw=2)
    for p in P:
        f.line(cx, cy, p[0], p[1], col='mblue', w=1.2)
    V0 = P[0]
    ex_, ey_ = V0[0] + 34 * math.cos(math.radians(60)), V0[1] - 34 * math.sin(math.radians(60))
    f.line(V0[0], V0[1], ex_, ey_, col='orange', w=2, dash='4 3')
    f.arc(V0[0], V0[1], 15, 120, 240, col='green', sw=2.4)
    f.arc(V0[0], V0[1], 25, 60, 120, col='orange', sw=2.4)
    f.arc(cx, cy, 17, 0, 60, col='purple', sw=2.4)
    f.label(V0[0] - 19, V0[1] + 4, '120°', size=10, col='green', anchor='end', bold=True)
    f.label(V0[0] + 6, V0[1] - 33, '60°', size=10, col='orange', anchor='start', bold=True)
    f.label(cx + 18, cy - 13, '60°', size=10, col='purple', anchor='start', bold=True)
    f.text(cx, 14, 'interno · externo · central', size=10, col='navy', bold=True)
    f.text(cx, 168, 'regular, n = 6', size=9.5, col='grey')
    cx2 = 262
    P2 = polygon_pts(6, cx2, cy, r, rot=0)
    f.poly(P2, fill='white', stroke='navy', sw=2)
    for i in range(6):
        for j in range(i + 2, 6):
            if i == 0 and j == 5:
                continue
            if j - i == 3:
                f.line(P2[i][0], P2[i][1], P2[j][0], P2[j][1], col='green', w=2.6)
            else:
                f.line(P2[i][0], P2[i][1], P2[j][0], P2[j][1], col='mgrey', w=1.2, dash='3 3')
    f.circ(cx2, cy, 3.4, fill='green')
    for p in P2:
        f.dot(p[0], p[1], 2.8, 'navy')
    f.text(cx2, 14, 'diagonais: 9 no total', size=10, col='navy', bold=True)
    f.text(cx2, 168, '3 pelo centro (n/2) · 6 não passam', size=9.5, col='grey')
    return f.svg()


def sq_on(f, p, q, s, fill, stroke='navy', sw=1.4):
    dx, dy = q[0] - p[0], q[1] - p[1]
    nx, ny = -dy * s, dx * s
    pts = [p, q, (q[0] + nx, q[1] + ny), (p[0] + nx, p[1] + ny)]
    f.poly(pts, fill=fill, stroke=stroke, sw=sw)
    return (sum(x for x, _ in pts) / 4, sum(y for _, y in pts) / 4)


def fig_pit():
    f = Fig(230, 208)
    u = 16
    A = (70, 130); B = (A[0] + 4 * u, A[1]); C = (A[0], A[1] - 3 * u)
    f.poly([A, B, C], fill='white', stroke='navy', sw=2)
    c1 = sq_on(f, A, B, 1, 'lgreen'); c2 = sq_on(f, C, A, 1, 'lblue'); c3 = sq_on(f, B, C, 1, 'lpurple')
    f.poly([A, B, C], fill='white', stroke='navy', sw=2)
    f.rightangle(A[0], A[1], (1, 0), (0, -1), 9)
    f.text(c1[0], c1[1] + 5, '16 = 4²', size=12, col='green', bold=True)
    f.text(c2[0], c2[1] + 5, '9 = 3²', size=11, col='navy', bold=True)
    f.text(c3[0], c3[1] + 5, '25 = 5²', size=13, col='purple', bold=True)
    f.label((A[0] + B[0]) / 2 + 4, A[1] - 6, '*b* = 4', size=10, col='navy', bold=True)
    f.label(A[0] + 6, (A[1] + C[1]) / 2 + 4, '*c* = 3', size=10, col='navy', anchor='start', bold=True)
    f.label((B[0] + C[0]) / 2 - 8, (B[1] + C[1]) / 2 + 12, '*a* = 5', size=10.5, col='purple', anchor='end', bold=True)
    f.text(115, 200, '*a*² = *b*² + *c*²  →  25 = 16 + 9', size=11, col='green', bold=True)
    return f.svg()


def fig_areas():
    f = Fig(640, 168)
    S, W = 1.8, 128
    def T(i, x, y):
        return (i * W + 14 + x * S, 6 + (y - 16) * S)
    def Pp(i, pts):
        return [T(i, x, y) for x, y in pts]
    def lab(i, x, y, t, col='grey', anchor='middle'):
        px, py = T(i, x, y); f.label(px, py, t, size=10.5, col=col, anchor=anchor, bold=col != 'grey')
    # retângulo
    f.poly(Pp(0, [(2, 22), (56, 22), (56, 60), (2, 60)]), fill='lblue', stroke='navy', sw=1.8)
    lab(0, 29, 68, '*b*'); lab(0, -2, 43, '*h*', anchor='end')
    # paralelogramo
    f.poly(Pp(1, [(2, 60), (42, 60), (58, 22), (18, 22)]), fill='lblue', stroke='navy', sw=1.8)
    a, b = T(1, 18, 22), T(1, 18, 60); f.line(*a, *b, col='orange', w=1.8, dash='3 2'); f.rightangle(b[0], b[1], (1, 0), (0, -1), 7)
    lab(1, 22, 68, '*b*'); lab(1, 15, 43, '*h*', col='orange', anchor='end')
    # triângulo
    f.poly(Pp(2, [(2, 60), (56, 60), (36, 22)]), fill='lblue', stroke='navy', sw=1.8)
    a, b = T(2, 36, 22), T(2, 36, 60); f.line(*a, *b, col='orange', w=1.8, dash='3 2'); f.rightangle(b[0], b[1], (-1, 0), (0, -1), 7)
    lab(2, 20, 68, '*b*'); lab(2, 40, 43, '*h*', col='orange', anchor='start')
    # trapézio
    f.poly(Pp(3, [(2, 60), (58, 60), (44, 22), (16, 22)]), fill='lblue', stroke='navy', sw=1.8)
    a, b = T(3, 16, 22), T(3, 16, 60); f.line(*a, *b, col='orange', w=1.8, dash='3 2'); f.rightangle(b[0], b[1], (1, 0), (0, -1), 7)
    lab(3, 32, 68, '*B*'); lab(3, 30, 17, '*b*'); lab(3, 13, 43, '*h*', col='orange', anchor='end')
    # losango
    f.poly(Pp(4, [(30, 20), (56, 41), (30, 62), (4, 41)]), fill='lblue', stroke='navy', sw=1.8)
    a, b = T(4, 4, 41), T(4, 56, 41); f.line(*a, *b, col='orange', w=1.8, dash='3 2')
    a, b = T(4, 30, 20), T(4, 30, 62); f.line(*a, *b, col='orange', w=1.8, dash='3 2')
    lab(4, 44, 38, '*D*', col='orange'); lab(4, 34, 32, '*d*', col='orange', anchor='start')
    names = ['Retângulo', 'Paralelogramo', 'Triângulo', 'Trapézio', 'Losango']
    forms = ['*A* = *b*·*h*', '*A* = *b*·*h*', '*A* = *b*·*h* / 2', '*A* = (*B*+*b*)·*h* / 2', '*A* = *D*·*d* / 2']
    for i in range(5):
        f.text(i * W + 14 + 28 * S, 124, names[i], size=10.5, col='navy', bold=True)
        f.text(i * W + 14 + 28 * S, 140, forms[i], size=10, col='green', bold=True)
    f.text(320, 162, '*h* = altura PERPENDICULAR à base (tracejada) — nunca o lado inclinado', size=10, col='orange', bold=True)
    return f.svg()


def fig_circulo():
    f = Fig(250, 170)
    cx, cy, r = 80, 88, 66
    f.circ(cx, cy, r, fill='lblue', stroke='navy', sw=2.2)
    f.line(cx - r, cy, cx + r, cy, col='purple', w=2, dash='4 3')
    f.line(cx, cy, cx + r * math.cos(math.radians(40)), cy - r * math.sin(math.radians(40)), col='green', w=2.6)
    f.dot(cx, cy, 3.4, 'navy')
    f.label(cx + 34, cy - 24, '*r*', size=12, col='green', bold=True)
    f.label(cx - 28, cy + 17, '*d* = 2*r*', size=11, col='purple', bold=True)
    f.text(190, 52, '*C* = 2π*r*', size=11.5, col='green', bold=True)
    f.text(190, 67, 'comprimento (contorno)', size=8.8, col='grey')
    f.text(190, 104, '*A* = π*r*²', size=11.5, col='green', bold=True)
    f.text(190, 119, 'área (superfície)', size=8.8, col='grey')
    return f.svg()


def fig_coroa_setor_seg():
    f = Fig(640, 196)
    R, cy = 66, 80
    cx = 106
    f.circ(cx, cy, R, fill='lorange', stroke='navy', sw=2); f.circ(cx, cy, 38, fill='white', stroke='navy', sw=2)
    f.line(cx, cy, cx + R, cy, col='orange', w=2); f.line(cx, cy, cx - 38 * .7, cy - 38 * .7, col='navy', w=2)
    f.label(cx + 50, cy - 6, '*R*', size=11.5, col='orange', bold=True); f.label(cx - 16, cy - 6, '*r*', size=11.5, col='navy', bold=True, anchor='end')
    f.text(cx, 168, 'COROA', size=10.5, col='navy', bold=True)
    f.text(cx, 184, '*A* = π(*R*² − *r*²)', size=10.5, col='green', bold=True)
    cx = 320
    f.circ(cx, cy, R, fill='white', stroke='navy', sw=1.6)
    f.sector(cx, cy, R, 10, 80, fill='lpurple', stroke='purple', sw=2)
    f.arc(cx, cy, 24, 10, 80, col='purple', sw=2.2)
    f.label(cx + 24, cy - 30, 'θ', size=12, col='purple', bold=True, anchor='start')
    f.label(cx + 46, cy - 4, '*r*', size=11.5, col='navy', bold=True)
    f.text(cx, 168, 'SETOR', size=10.5, col='navy', bold=True)
    f.text(cx, 184, '*A* = (θ / 360°) · π*r*²', size=10.5, col='green', bold=True)
    cx = 534
    f.circ(cx, cy, R, fill='white', stroke='navy', sw=1.6)
    a0, a1 = 25, 155
    x0, y0 = cx + R * math.cos(math.radians(a0)), cy - R * math.sin(math.radians(a0))
    x1, y1 = cx + R * math.cos(math.radians(a1)), cy - R * math.sin(math.radians(a1))
    f.path(f'M{x0:.1f},{y0:.1f} A{R},{R} 0 0 0 {x1:.1f},{y1:.1f} Z', fill='lgreen', stroke='green', sw=2)
    f.poly([(cx, cy), (x0, y0), (x1, y1)], fill='lblue', stroke='navy', sw=1.4, op=.9)
    f.text(cx, 168, 'SEGMENTO', size=10.5, col='navy', bold=True)
    f.text(cx, 184, '*A* = setor − triângulo', size=10.5, col='green', bold=True)
    f.text(cx, cy - 6, 'triângulo', size=9.5, col='navy', bold=True)
    f.text(cx, cy - 40, 'segmento', size=9.8, col='green', bold=True)
    return f.svg()


def fig_especiais():
    f = Fig(640, 176)
    cx, cy, r = 110, 76, 62
    P = polygon_pts(6, cx, cy, r, rot=0)
    f.poly(P, fill='lblue', stroke='navy', sw=2)
    for p in P:
        f.line(cx, cy, p[0], p[1], col='navy', w=1.1)
    f.poly([(cx, cy), P[1], P[2]], fill='lpurple', stroke='navy', sw=1.2)
    f.label(cx, cy - 26, '*ℓ*', size=11.5, col='purple', bold=True)
    f.text(cx, 158, 'HEXÁGONO REGULAR = 6 triângulos equiláteros', size=10, col='navy', bold=True)
    x0, y0, s = 270, 12, 100
    f.rect(x0, y0, s, s, fill='lblue', stroke='navy', sw=2)
    f.line(x0, y0 + s, x0 + s, y0, col='orange', w=2.6)
    f.label(x0 + s / 2, y0 + s + 15, '*ℓ*', size=11.5, col='navy', bold=True)
    f.label(x0 + 38, y0 + 38, '*d* = *ℓ*√2', size=11, col='orange', bold=True, anchor='middle')
    f.text(x0 + s / 2, 158, 'QUADRADO: diagonal', size=10, col='navy', bold=True)
    xe = 520; hh = 100 * R3 / 2 * 1.0
    f.poly([(xe - 50, 112), (xe + 50, 112), (xe, 112 - hh)], fill='lgreen', stroke='navy', sw=2)
    f.line(xe, 112, xe, 112 - hh, col='orange', w=2, dash='3 2')
    f.rightangle(xe, 112, (1, 0), (0, -1), 8)
    f.label(xe + 5, 112 - hh / 2 + 4, '*h* = *ℓ*√3/2', size=10.5, col='orange', anchor='start', bold=True)
    f.label(xe - 30, 112 - hh / 2 - 6, '*ℓ*', size=11.5, col='navy', anchor='end', bold=True)
    f.text(xe, 158, 'TRIÂNGULO EQUILÁTERO', size=10, col='navy', bold=True)
    return f.svg()


def fig_semelhanca():
    f = Fig(190, 138)
    A, B, C = (96, 12), (14, 104), (178, 104)
    k = 0.45
    D = (A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k); E = (A[0] + (C[0] - A[0]) * k, A[1] + (C[1] - A[1]) * k)
    f.poly([A, B, C], fill='lblue', stroke='navy', sw=1.8)
    f.poly([A, D, E], fill='lpurple', stroke='purple', sw=1.8)
    for p, t, dx, dy in ((A, 'A', 0, -3), (B, 'B', -8, 12), (C, 'C', 8, 12), (D, 'D', -10, 4), (E, 'E', 10, 4)):
        f.label(p[0] + dx, p[1] + dy, t, size=10.5, col='navy', bold=True)
    f.text(96, 126, 'DE ∥ BC  →  AD/AB = AE/AC = DE/BC', size=9.6, col='green', bold=True)
    f.text(96, 138, '', size=1)
    return f.svg()


# ------------------------------------------------------------------ páginas
def poly_at(P, phi, n, L):
    """Vértices de um polígono regular de lado L com um vértice em P, primeiro lado na direção phi (graus), interior à esquerda."""
    pts = [P]
    x, y = P
    d = phi
    for _ in range(n - 1):
        x += L * math.cos(math.radians(d)); y -= L * math.sin(math.radians(d))
        pts.append((x, y))
        d += 360 / n
    return pts


def fig_tiling():
    f = Fig(350, 128)
    cases = [(3, 6, 32, 'lblue', '6 × 60° = 360°'), (4, 4, 30, 'lpurple', '4 × 90° = 360°'),
             (6, 3, 27, 'lgreen', '3 × 120° = 360°'), (5, 3, 30, 'lorange', '3 × 108° = 324°')]
    for i, (n, k, L, col, lab) in enumerate(cases):
        P = (44 + i * 88, 56)
        ai = (n - 2) * 180 / n
        for j in range(k):
            f.poly(poly_at(P, j * ai, n, L), fill=col, stroke='navy', sw=1.4)
        if n == 5:
            f.sector(P[0], P[1], 20, 3 * ai, 360, fill='white', stroke='orange', sw=1.6)
            f.text(P[0] + 8, P[1] + 4, '36°', size=8.5, col='orange', bold=True)
        f.dot(P[0], P[1], 3, 'navy')
        f.text(P[0], 112, lab, size=9, col='green' if n != 5 else 'orange', bold=True)
        f.text(P[0], 124, ['triângulos', 'quadrados', 'hexágonos', 'pentágonos: sobra!'][i], size=8.8, col='grey')
    return f.svg()


def fig_composta():
    f = Fig(350, 130)
    u = 8
    def Lshape(x0, y0):
        return [(x0, y0), (x0 + 10 * u, y0), (x0 + 10 * u, y0 + 2 * u), (x0 + 4 * u, y0 + 2 * u), (x0 + 4 * u, y0 + 6 * u), (x0, y0 + 6 * u)]
    # decomposição 1: soma de dois retângulos
    x0, y0 = 10, 20
    f.poly(Lshape(x0, y0), fill='lblue', stroke='navy', sw=1.8)
    f.line(x0 + 4 * u, y0, x0 + 4 * u, y0 + 2 * u, col='orange', w=1.6, dash='3 2')
    f.text(x0 + 7 * u, y0 + u + 4, '10 × 2', size=9.5, col='navy', bold=True)
    f.text(x0 + 2 * u, y0 + 4 * u + 4, '4 × 4', size=9.5, col='navy', bold=True)
    f.text(x0 + 5 * u, 14, 'SOMA: 20 + 16 = 36', size=10, col='green', bold=True)
    # decomposição 2: retângulo grande menos recorte
    x1 = 190
    f.rect(x1, y0, 10 * u, 6 * u, fill='white', stroke='navy', sw=1.2, dash='4 3')
    f.poly(Lshape(x1, y0), fill='lpurple', stroke='navy', sw=1.8)
    f.rect(x1 + 4 * u, y0 + 2 * u, 6 * u, 4 * u, fill='lorange', stroke='orange', sw=1.4, dash='4 3')
    f.text(x1 + 7 * u, y0 + 4 * u + 4, 'recorte 6 × 4', size=9.5, col='orange', bold=True)
    f.text(x1 + 5 * u, 14, 'SUBTRAÇÃO: 60 − 24 = 36', size=10, col='green', bold=True)
    f.text(175, 100, 'Figura em L (10 × 6 com recorte 6 × 4): decomponha de duas formas e confira.', size=9.5, col='grey')
    f.text(175, 116, '', size=1)
    return f.svg()


def fig_inscrito():
    f = Fig(250, 150)
    cx, cy, r = 70, 78, 56
    f.circ(cx, cy, r, fill='lblue', stroke='navy', sw=1.8)
    A = (cx + r * math.cos(math.radians(-35)), cy - r * math.sin(math.radians(-35)))
    B = (cx + r * math.cos(math.radians(55)), cy - r * math.sin(math.radians(55)))
    Pp = (cx + r * math.cos(math.radians(200)), cy - r * math.sin(math.radians(200)))
    f.path(f'M{A[0]:.1f},{A[1]:.1f} A{r},{r} 0 0 0 {B[0]:.1f},{B[1]:.1f}', stroke='orange', sw=3.2)
    f.line(cx, cy, *A, col='purple', w=1.8); f.line(cx, cy, *B, col='purple', w=1.8)
    f.line(*Pp, *A, col='green', w=1.8); f.line(*Pp, *B, col='green', w=1.8)
    f.arc(cx, cy, 15, -35, 55, col='purple', sw=2.2)
    f.arc(Pp[0], Pp[1], 20, -12, 18, col='green', sw=2.2) if False else None
    f.label(cx + 22, cy + 3, '2α', size=11, col='purple', bold=True, anchor='start')
    f.label(Pp[0] + 24, Pp[1] - 8, 'α', size=11, col='green', bold=True, anchor='start')
    f.dot(cx, cy, 3, 'navy'); f.dot(Pp[0], Pp[1], 3.2, 'green')
    f.text(190, 40, 'ângulo inscrito = ½ do', size=10, col='navy', bold=True)
    f.text(190, 54, 'ângulo central', size=10, col='navy', bold=True)
    f.text(190, 72, 'que enxerga o mesmo arco', size=9, col='grey')
    f.text(190, 104, 'θ (rad) = ℓ / *r*', size=11, col='green', bold=True)
    f.text(190, 120, 'π rad = 180°', size=11, col='green', bold=True)
    return f.svg()


def p_poligonos():
    band = chapter_band(5, 'Geometria plana e polígonos', 'tópicos 18 a 28')
    c = card('Polígonos: ângulos e diagonais', '18–23', 'B', cols(
        stack(
            formula((r'S_i=(n-2)\cdot180^\circ', 'soma dos ângulos internos'),
                    (r'a_i=\dfrac{(n-2)\cdot180^\circ}{n}', 'interno · regular'),
                    (r'a_e=\dfrac{360^\circ}{n}', 'externo · regular'),
                    (r'a_c=\dfrac{360^\circ}{n}', 'central · regular'),
                    (r'd=\dfrac{n\,(n-3)}{2}', 'diagonais'), label='POLÍGONOS (n LADOS)'),
            vars_('<b>a<sub>i</sub> + a<sub>e</sub> = 180°</b> em cada vértice. A soma dos externos de qualquer polígono convexo é <b>360°</b>. '
                  'Regular com n par: <b>n/2</b> diagonais passam pelo centro; as outras \\(d-\\tfrac n2\\) não passam.'),
            gap='1.2mm'),
        fig(fig_poli_soma(), 'De um vértice saem n − 3 diagonais, que dividem o polígono em <b>n − 2 triângulos</b> → S = (n−2)·180° (hexágono: 4 × 180° = 720°).'),
        ratio='1.05fr 1fr', gap='3.5mm', align='center') +
        cols(fig(fig_hexa(), None),
             tbl(['n', 'S<sub>i</sub>', 'a<sub>i</sub>', 'a<sub>e</sub> = a<sub>c</sub>', 'd'],
                 [['3', '180°', '60°', '120°', '0'], ['4', '360°', '90°', '90°', '2'], ['5', '540°', '108°', '72°', '5'],
                  ['6', '720°', '120°', '60°', '9'], ['8', '1080°', '135°', '45°', '20'], ['10', '1440°', '144°', '36°', '35'],
                  ['12', '1800°', '150°', '30°', '54']], cls='c'),
             ratio='1.15fr 1fr', gap='3mm', align='center'))
    q = cols(
        stack(when('“polígono regular”, “ângulo interno/externo de X°”, “quantos lados”, “quantas diagonais”, ladrilhamento do piso.'),
              err('Usar \\(n\\) em vez de \\(n-2\\) na soma interna; esquecer que a fórmula de \\(a_i\\) vale só para polígono <u>regular</u>.'), gap='1.4mm'),
        stack(mem('Piso <b>sem frestas</b>: os ângulos em torno de um vértice somam 360°. Só triângulo, quadrado e hexágono regulares ladrilham sozinhos.'),
              mini('Regular com ângulo interno 150°:', 'nº de diagonais?', r'\(a_e=30^\circ\Rightarrow n=12\Rightarrow d=\tfrac{12\cdot9}{2}\)', '= 54 (6 pelo centro).'), gap='1.4mm'),
        gap='3mm')
    til = fig(fig_tiling(), 'Ladrilhamento: em volta de um vértice a soma dos ângulos precisa dar exatamente 360° (o pentágono deixa um vazio de 36°).')
    r = rec(('Soma dos ângulos internos de um octógono?', '(8 − 2)·180° = 1080°'),
            ('Ângulo externo de um polígono regular de 20 lados?', '360°/20 = 18°'),
            ('Quantas diagonais tem um pentágono?', '5·2/2 = 5'))
    return band + c + q + til + r


def p_pit_areas():
    pit = card('Teorema de Pitágoras', 24, 'A', cols(
        stack(
            formula((r'a^2=b^2+c^2', 'a = hipotenusa (oposta ao ângulo reto)'),
                    (r'd=\sqrt{a^2+b^2}', 'diagonal do retângulo'), label='TRIÂNGULO RETÂNGULO'),
            when('Distância/altura/comprimento em figura com <b>ângulo reto</b>: rampa, escada na parede, diagonal de tela, trajeto em “L”, altura de telhado.'),
            mem('<b>Ternos pitagóricos:</b> 3-4-5 · 5-12-13 · 8-15-17 · 7-24-25 e seus múltiplos (6-8-10, 9-12-15…). Reconhecê-los evita raiz quadrada.'),
            err('Colocar um cateto como hipotenusa: ela é sempre o <u>maior</u> lado. Vale só para triângulo retângulo.'),
            gap='1.3mm'),
        stack(fig(fig_pit(), 'A área do quadrado da hipotenusa é a soma das áreas dos quadrados dos catetos.'),
              mini('Escada de 5 m', 'apoiada a 3 m da base da parede.', r'\(h=\sqrt{5^2-3^2}=\sqrt{16}\)', '= 4 m de altura.'), gap='1.2mm'),
        ratio='1.1fr 1fr', gap='3.5mm', align='center'))

    ar = card('Áreas e perímetros das principais figuras planas', 26, 'A',
              fig(fig_areas(), None, cls='wide') +
              cols(formula((r'P=\text{soma dos lados}', 'perímetro: contorno (cerca, rodapé, moldura)'),
                           (r'A_{\square}=\ell^2\quad P=4\ell', 'quadrado'),
                           (r'A_{\text{retângulo}}=b\cdot h\quad P=2(b+h)', ''), label='ÁREA × PERÍMETRO'),
                   stack(when('<b>Área</b> = superfície a cobrir (piso, tinta, grama) → unidade ao quadrado. <b>Perímetro</b> = contorno (cerca, rodapé) → unidade linear.'),
                         mem('Tudo é “base × altura”: triângulo = <b>metade</b> de um paralelogramo; trapézio = <b>base média</b> \\(\\tfrac{B+b}{2}\\) × altura. '
                             'Figuras de mesma área podem ter perímetros diferentes.'), gap='1.4mm'),
                   ratio='1fr 1.15fr', gap='3mm', align='start'))
    comp = cols(fig(fig_composta(), None),
                stack(mini('Área composta:', 'em “L”, some peças ou subtraia o recorte.', r'\(10\cdot6-6\cdot4\)', '= 36 m².'),
                      mini('Dobrando os lados:', 'quadrado de lado 5 → 10.', 'perímetro ×2 (20 → 40); área ×4 (25 → 100).', ''), gap='1.6mm'),
                ratio='1.25fr 1fr', gap='3mm', align='center')
    r = rec(('Hipotenusa de catetos 6 e 8?', '10 (terno 3-4-5 ×2)'),
            ('Área do trapézio B = 10, b = 6, h = 4?', '(10+6)·4/2 = 32'),
            ('Perímetro × área: quem muda com a unidade ao quadrado?', 'a área (m² → cm²: × 10 000)'))
    return pit + ar + comp + r


def p_circulo():
    ci = card('Círculo e circunferência', 25, 'A', cols(
        stack(
            formula((r'C=2\pi r=\pi d', 'comprimento da circunferência'), (r'A=\pi r^2', 'área do círculo'), label='CÍRCULO'),
            when('Roda, pista, canteiro, pizza, relógio, “volta completa”, tampa. Se o enunciado dá um valor de π (3, 3,14), <b>use-o</b>.'),
            err('Usar o <b>diâmetro</b> no lugar do raio em \\(\\pi r^2\\) (raio = d/2). Dobrar o raio <b>quadruplica</b> a área.'),
            gap='1.3mm'),
        fig(fig_circulo(), None), ratio='1.1fr 1fr', gap='3.5mm', align='center') +
        mini('Roda:', 'raio 30 cm; 100 voltas.', r'\(d=100\cdot2\pi\cdot0{,}3=60\pi\approx188{,}4\ \text{m}\ (\pi=3{,}14)\)', '≈ 188 m.'))

    cs = card('Coroa circular, setor circular e segmento circular', 27, 'B',
              fig(fig_coroa_setor_seg(), None) +
              cols(formula((r'A_{\text{coroa}}=\pi\,(R^2-r^2)', ''),
                           (r'\ell=\dfrac{\theta}{360^\circ}\,2\pi r\qquad A_{\text{setor}}=\dfrac{\theta}{360^\circ}\,\pi r^2', 'θ em graus'),
                           (r'A_{\text{seg}}=A_{\text{setor}}-A_{\triangle}\quad A_\triangle=\tfrac12\,r^2\sin\theta', ''), label='PARTES DO CÍRCULO'),
                   stack(when('<b>Coroa:</b> piscina com calçada, anel, aro. <b>Setor:</b> fatia de pizza, alcance de irrigador/antena/farol, ponteiro. '
                              '<b>Segmento:</b> região entre uma corda e o arco.'),
                         mem('Setor é <b>proporção do círculo</b>: θ/360° da área <u>e</u> do contorno. Segmento = “setor menos triângulo”.'),
                         gap='1.3mm'),
                   ratio='1.35fr 1fr', gap='3mm', align='start'))

    rad = card('Radiano, comprimento de arco e ângulo inscrito', None, 'B', cols(
        stack(
            formula((r'\ell=r\,\theta\quad(\theta\ \text{em rad})', 'comprimento do arco'),
                    (r'\pi\ \text{rad}=180^\circ', 'conversão'),
                    (r'\alpha_{\text{inscrito}}=\dfrac{\theta_{\text{central}}}{2}', 'mesmo arco'), label='ARCOS E ÂNGULOS'),
            when('Relógio, engrenagem, roda, curva em rodovia, setor de antena. Ex.: <b>60° = π/3 rad</b>; <b>90° = π/2</b>; <b>45° = π/4</b>.'),
            gap='1.4mm'),
        fig(fig_inscrito(), None), ratio='1.1fr 1fr', gap='3mm', align='center'))
    e10 = mini('Praça com coroa e setor:', 'raio 10 m, chafariz central de raio 6 m; gramar a coroa, exceto um setor de 90° (π = 3,14).',
               r'\(A_{\text{coroa}}=\pi(10^2-6^2)=64\pi\); sobra \(\tfrac34\) → \(48\pi\)', '≈ 150,7 m².')
    r = rec(('Comprimento de um arco de 90° em circunferência de raio 8?', '(90/360)·2π·8 = 4π'),
            ('Dobrando o raio de um círculo, a área…', 'fica 4 vezes maior'),
            ('Área de setor de 60° e raio 6 (π = 3)?', '(1/6)·3·36 = 18'))
    return ci + rad + cs + e10 + r


def p_especiais():
    es = card('Hexágono regular, diagonal do quadrado, triângulo equilátero', 28, 'B', fig(fig_especiais(), None) +
              cols(formula((r'd=\ell\sqrt2', 'diagonal do quadrado'),
                           (r'h=\dfrac{\ell\sqrt3}{2}\qquad A_{\triangle}=\dfrac{\ell^2\sqrt3}{4}', 'equilátero'),
                           (r'A_{\text{hexágono}}=6\cdot\dfrac{\ell^2\sqrt3}{4}=\dfrac{3\ell^2\sqrt3}{2}', ''), label='FÓRMULAS ESPECIAIS'),
                   stack(mem('O hexágono regular é <b>6 triângulos equiláteros</b> de lado ℓ: raio da circunferência circunscrita = ℓ; apótema (raio inscrito) = \\(\\tfrac{\\ell\\sqrt3}{2}\\).'),
                         err('Use as aproximações que o enunciado fornece (\\(\\sqrt2\\approx1{,}41\\); \\(\\sqrt3\\approx1{,}73\\)). A diagonal do quadrado é ℓ√2, <u>não</u> 2ℓ.', label='ATENÇÃO'),
                         gap='1.3mm'), ratio='1.3fr 1fr', gap='3mm', align='start'))
    se = card('Semelhança de triângulos e Teorema de Tales', None, 'A', cols(
        fig(fig_semelhanca(), None),
        stack(
            formula((r'\dfrac{\text{lado}}{\text{lado}'+r'\,'+r'\text{correspondente}}=k', 'razão de semelhança'),
                    (r'P\to k\qquad A\to k^2\qquad V\to k^3', 'perímetro · área · volume'), label='SEMELHANÇA'),
            when('<b>Sombras</b> (poste × pessoa), mapas/maquetes, reta paralela à base de um triângulo, feixe de paralelas cortadas por transversais, figuras “iguais em forma”.'),
            mini('Sombra:', 'pessoa de 1,8 m projeta sombra de 1,2 m; o poste, no mesmo instante, 4 m.', r'\(\tfrac{H}{4}=\tfrac{1{,}8}{1{,}2}\Rightarrow H=\tfrac{1{,}8\cdot4}{1{,}2}\)', '= 6 m.'),
            gap='1.3mm'),
        ratio='.9fr 1.3fr', gap='3.5mm', align='center'))
    e = ex(10, 'Área composta: hexágono com chafariz e custo da grama',
           'Uma praça tem a forma de um hexágono regular de lado 6 m. No centro será construída uma fonte circular de raio 2 m, e o restante será gramado ao custo de R$ 25,00 por m². '
           'Use √3 ≈ 1,7 e π ≈ 3,1. Qual o custo da grama?',
           '<b>Hexágono regular</b> = 6 triângulos equiláteros; subtrai-se a área do <b>círculo</b>; depois multiplica-se pelo preço por m² (unidade correta!).',
           r'\(A_{\text{hex}}=6\cdot\dfrac{6^2\sqrt3}{4}=6\cdot\dfrac{36\cdot1{,}7}{4}=6\cdot15{,}3=91{,}8\ \text{m}^2\).'
           r'<br>\(A_{\text{fonte}}=\pi r^2=3{,}1\cdot4=12{,}4\ \text{m}^2\ \Rightarrow\ A_{\text{grama}}=91{,}8-12{,}4=79{,}4\ \text{m}^2\).'
           r'<br>Custo \(=79{,}4\cdot25=1\,985\).',
           r'Custo da grama: <b>R$ 1.985,00</b> (área gramada ≈ 79,4 m²).',
           shortcut=r'Estimativa: hexágono ≈ 2,6·ℓ² = 2,6·36 ≈ 93 m² (confere com 91,8); menos ≈ 12 → ≈ 80 m² ✔.')
    r = rec(('Diagonal de um quadrado de lado 10?', '10√2 ≈ 14,1'),
            ('Altura de um triângulo equilátero de lado 8?', '8·√3/2 = 4√3 ≈ 6,9'),
            ('Lados dobram: a área do triângulo semelhante…', 'fica 4 vezes maior'))
    return es + se + e + r


def pages():
    return [p_poligonos(), p_pit_areas(), p_circulo(), p_especiais()]
