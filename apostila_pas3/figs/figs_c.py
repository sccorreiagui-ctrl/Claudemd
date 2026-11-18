"""Figuras da Parte I — Números Complexos."""
import math
from svgkit import Fig, Plane, PAL, fmt

D2R = math.pi / 180


def cpt(r, deg):
    return r * math.cos(deg * D2R), r * math.sin(deg * D2R)


# ---------------------------------------------------------------- p01
def fig_sets():
    f = Fig(250, 238)
    cx, cy = 125, 121
    rings = [(112, 'purple_l', 'purple', '\\bb{C}'), (90, 'orange_l', 'orange', '\\bb{R}'),
             (68, 'yellow_l', 'yellow', '\\bb{Q}'), (47, 'blue_l', 'blue', '\\bb{Z}'), (26, 'green_l', 'green', '\\bb{N}')]
    for r, fl, st, lab in rings:
        f.circle(cx, cy, r, fl, st, 1.6)
    for r, fl, st, lab in rings:
        f.text(cx, cy - r + 14 if r > 30 else cy - r + 12, lab, 15, st, weight=700)
    # elementos
    f.text(cx - 6, cy + 2, '2', 10.5, 'green'); f.text(cx + 8, cy + 14, '0', 10.5, 'green')
    f.text(cx - 14, cy + 38, '−3', 10.5, 'blue'); f.text(cx + 14, cy + 38, '−10', 10, 'blue')
    f.text(cx - 14, cy + 58, '1/2', 10.5, '#8a6a00'); f.text(cx + 18, cy + 60, '−0,75', 9.5, '#8a6a00')
    f.text(cx - 28, cy + 69, '√2', 10.5, 'orange'); f.text(cx + 30, cy + 69, 'π', 11, 'orange')
    f.dot(cx - 38, cy + 92, 2.6, 'purple'); f.text(cx - 31, cy + 96, 'i', 12, 'purple', anchor='start', weight=700)
    f.dot(cx + 36, cy + 90, 2.6, 'purple'); f.text(cx + 43, cy + 94, '2+3i', 10.5, 'purple', anchor='start', weight=700)
    return f


# ---------------------------------------------------------------- p02
def fig_icycle():
    f = Fig(300, 240)
    pl = Plane(f, 150, 118, 64)
    f.circle(150, 118, 64, 'none', 'gray_m', 1.2, dash='3 3')
    pl.axes(-1.7, 1.7, -1.55, 1.55, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=False)
    pts = [(1, 0, 0), (0, 1, 90), (-1, 0, 180), (0, -1, 270)]
    cols = ['blue', 'purple', 'blue', 'purple']
    for (x, y, a), c in zip(pts, cols):
        pl.pt(x, y, c, 4.4)
    # rotações de 90° (setas laranja)
    for a in (0, 90, 180, 270):
        pl.arc(1.0, a + 14, a + 76, 'orange', 1.9, arrow=True) if False else None
    for a in (0, 90, 180, 270):
        r = 0.62
        pl.arc(r, a + 12, a + 78, 'orange', 1.9, arrow=True)
        mx, my = cpt(r + 0.22, a + 45)
        pl.text(mx, my, '×i', 10.5, 'orange', dy=3.5, weight=700)
    # rótulos dos nós (fora dos eixos)
    f.text(150 + 64 + 8, 118 - 7, '1', 15, 'blue', anchor='start', weight=700)
    f.text(150 + 64 + 8, 118 + 9, '= i^{0} = i^{4} = i^{8} …', 8.6, 'blue', anchor='start')
    f.text(150 + 9, 118 - 64 - 6, 'i', 15, 'purple', anchor='start', weight=700)
    f.text(150 + 9 + 12, 118 - 64 - 6, '= i^{1} = i^{5} = i^{9} …', 8.6, 'purple', anchor='start')
    f.text(150 - 64 - 8, 118 - 7, '−1', 15, 'blue', anchor='end', weight=700)
    f.text(150 - 64 - 8, 118 + 9, 'i^{2} = i^{6} = i^{10} …', 8.6, 'blue', anchor='end')
    f.text(150 + 9, 118 + 64 + 14, '−i', 15, 'purple', anchor='start', weight=700)
    f.text(150 + 9 + 20, 118 + 64 + 14, '= i^{3} = i^{7} = i^{11} …', 8.6, 'purple', anchor='start')
    return f


# ---------------------------------------------------------------- p03
def fig_anat_alg():
    f = Fig(372, 150)
    y = 42
    f.text(186, y, '«ink:z» = «blue:a» + «purple:b»«purple:i»', 30)
    # posições aproximadas dos glifos (30u): z=~123, a=~178, b=~213, i=~226
    # setas
    f.arrow(172, 56, 72, 92, 'blue', 1.5, 6)
    f.arrow(209, 56, 186, 92, 'purple', 1.5, 6)
    f.arrow(232, 56, 300, 92, 'purple', 1.5, 6)
    f.label_box(6, 94, 132, 50, '', 'blue_l', 'blue', rx=4)
    f.text(72, 110, '~Parte real', 9.5, 'blue', weight=700)
    f.text(72, 124, '\\r{Re}(z) = a', 12, 'blue')
    f.text(72, 138, '~(número real)', 8.2, 'gray')
    f.label_box(142, 94, 100, 50, '', 'purple_l', 'purple', rx=4)
    f.text(192, 110, '~Parte imaginária', 9.2, 'purple', weight=700)
    f.text(192, 124, '\\r{Im}(z) = b', 12, 'purple')
    f.text(192, 138, '~(também REAL!)', 8.2, 'red', weight=700)
    f.label_box(246, 94, 120, 50, '', 'gray_l', 'gray', rx=4)
    f.text(306, 110, '~Unidade imaginária', 9.2, 'purple', weight=700)
    f.text(306, 124, 'i^2 = −1', 12, 'ink')
    f.text(306, 138, '~(não é parte de b)', 8.2, 'gray')
    return f


# ---------------------------------------------------------------- p06
def fig_distrib():
    f = Fig(400, 142)
    f.add('<g transform="translate(14,0)">')
    ty = 60
    f.text(186, ty, '(«blue:2» + «purple:3i»)(«blue:3» − «orange:2i»)', 26)
    # x aproximados (26u): '(' 66 | 2 | + | 3i | ')' | '(' | 3 | − | 2i | ')'
    X = dict(a2=92, b3i=145, c3=206, d2i=265)
    def curve(x1, y1, x2, y2, cy, col):
        f.path(f'M{x1},{y1} Q{(x1 + x2) / 2},{cy} {x2},{y2}', stroke=col, w=1.7)
        # ponta
        f._head(x2, y2, math.atan2(y2 - cy, 0.001 + (x2 - (x1 + x2) / 2)) if False else (math.pi / 2 if y2 > cy else -math.pi / 2), 6, PAL[col])
    curve(X['a2'], ty - 24, X['c3'], ty - 24, 2, 'blue')
    curve(X['a2'] + 4, ty - 24, X['d2i'], ty - 24, -16, 'orange')
    curve(X['b3i'], ty + 9, X['c3'] + 4, ty + 9, ty + 34, 'purple')
    curve(X['b3i'] + 6, ty + 9, X['d2i'], ty + 9, ty + 44, 'red')
    # números dos produtos
    f.text(186, 112, '~Produtos parciais:', 8.5, 'gray', anchor='end', op=None) if False else None
    items = [('«blue:2·3» = 6', 'blue'), ('«blue:2»·(«orange:−2i») = −4i', 'orange'), ('«purple:3i»·«blue:3» = 9i', 'purple'), ('«purple:3i»·(«orange:−2i») = −6i^2 = «red:+6»', 'red')]
    xs = [40, 124, 224, 322]
    for (t, c), x in zip(items, xs):
        f.text(x, 108, t, 10.2, c)
    f.text(186, 132, '= 6 − 4i + 9i + 6 = «green:12 + 5i»', 13.5)
    f.add('</g>')
    return f


# ---------------------------------------------------------------- p07
def fig_conj():
    f = Fig(300, 200)
    pl = Plane(f, 150, 100, 28)
    pl.axes(-4.8, 4.8, -3.3, 3.3, ticks=True, step=1, tick_size=7.5, lab_size=9)
    # espelho
    pl.line(3, 2, 3, -2, 'green', 1.2, dash='4 3')
    pl.line(3, 2, -3, -2, 'orange', 1.2, dash='4 3')
    pl.vec(3, 2, 'purple', 1.8); pl.vec(3, -2, 'green', 1.8); pl.vec(-3, -2, 'orange', 1.8)
    for (x, y, c) in [(3, 2, 'purple'), (3, -2, 'green'), (-3, -2, 'orange')]:
        pl.pt(x, y, c, 3.2)
    pl.text(3.15, 2.1, 'z = 3 + 2i', 9.5, 'purple', anchor='start', dy=-3, weight=700, bg='white')
    pl.text(3.15, -2.1, '\\bar{z} = 3 − 2i', 9.5, 'green', anchor='start', dy=11, weight=700, bg='white')
    pl.text(-3.15, -2.1, '−z = −3 − 2i', 9.5, 'orange', anchor='start', dx=-14, dy=12, weight=700, bg='white')
    pl.text(3.12, 0.0, '~espelho: eixo real', 7.5, 'green', anchor='start', dy=-4, bg='white') if False else None
    f.text(190, 94, '~conjugado = reflexão no eixo real', 7.8, 'green', anchor='start', rot=None, bg='white') if False else None
    return f


# ---------------------------------------------------------------- p09
def fig_argand():
    f = Fig(384, 300)
    pl = Plane(f, 192, 152, 31)
    pl.axes(-5.7, 5.7, -4.4, 4.4, step=1, tick_size=8)
    # vetor e projeções de z1
    pl.line(3, 2, 3, 0, 'purple', 1.1, dash='3 3'); pl.line(3, 2, 0, 2, 'blue', 1.1, dash='3 3')
    pl.vec(3, 2, 'ink', 1.8)
    pts = [(3, 2, 'z_1 = 3 + 2i', 'blue', 'start', 1), (-2, 3, 'z_2 = −2 + 3i', 'purple', 'end', 1),
           (-3, -2, 'z_3 = −3 − 2i', 'ink', 'end', -1), (2, -3, 'z_4 = 2 − 3i', 'ink', 'start', -1),
           (-4.5, 0, 'z_5 = −4,5', 'blue', 'middle', -1), (0, -1.4, 'z_6 = −1,4i', 'purple', 'start', -1)]
    for x, y, lab, c, anc, sg in pts:
        pl.pt(x, y, 'ink' if c == 'ink' else c, 3.4)
        px, py = pl.P(x, y)
        dx = 7 if anc == 'start' else (-7 if anc == 'end' else 0)
        dy = -7 if sg == 1 else 15
        if lab.startswith('z_5'): dy = -9; dx = 0
        if lab.startswith('z_6'): dx = 7; dy = 4
        f.text(px + dx, py + dy, lab, 9.2, 'ink', anchor=anc, bg='white')
    pl.text(3, 0, '3', 8, 'blue', dy=11) if False else None
    for (x, y, txt) in [(4.4, 3.9, '1º quadrante'), (-4.4, 3.9, '2º quadrante'), (-4.4, -4.05, '3º quadrante'), (4.4, -4.05, '4º quadrante')]:
        pl.text(x, y, '~' + txt, 8.2, 'gray', weight=700)
    f.text(pl.P(3, 0)[0], pl.P(3, 0)[1] - 17 + 0, '', 8) if False else None
    pl.text(1.5, 2.0, '~vetor de posição', 7.6, 'ink', dy=-26, dx=-10, anchor='start') if False else None
    return f


# ---------------------------------------------------------------- p11
def fig_modulus():
    f = Fig(330, 215)
    pl = Plane(f, 40, 185, 38)
    pl.axes(-0.4, 7.4, -0.4, 4.9, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=True, lab_size=9)
    # triângulo
    f.poly([pl.P(0, 0), pl.P(3, 0), pl.P(3, 4)], 'green_l', 'none', 0, op=0.55)
    pl.line(0, 0, 3, 0, 'blue', 2.6); pl.line(3, 0, 3, 4, 'purple', 2.6); pl.vec(3, 4, 'green', 2.6)
    # ângulo reto
    x, y = pl.P(3, 0)
    f.poly([(x - 8, y), (x - 8, y - 8), (x, y - 8)], 'none', 'gray', 1.0, close=False)
    pl.pt(3, 4, 'ink', 3.6)
    pl.text(1.5, 0, 'a = 3', 11, 'blue', dy=17, weight=700)
    pl.text(3, 2, 'b = 4', 11, 'purple', dx=10, anchor='start', weight=700)
    pl.text(1.5, 2, 'ρ = |z| = 5', 11, 'green', dx=-14, dy=-6, anchor='end', weight=700)
    pl.text(3, 4, 'P(3, 4)  ↔  z = 3 + 4i', 9.6, 'ink', dx=8, dy=-4, anchor='start')
    pl.text(3.35, 0.55, '', 8)
    f.text(176, 127, 'ρ^2 = a^2 + b^2', 11, 'ink', anchor='start') if False else None
    f.text(166, 130, '~Pitágoras: ρ² = a² + b²', 9.3, 'gray', anchor='start')
    f.text(176, 166, '= 3² + 4² = 25  ⇒  ρ = 5', 9.6, 'green', anchor='start') if False else None
    f.text(166, 146, '~ρ² = 9 + 16 = 25  ⇒  ρ = 5', 9.3, 'green', anchor='start', weight=700)
    f.text(166, 162, '~catetos: números REAIS a e b', 8.6, 'red', anchor='start')
    f.text(166, 174, '~(nunca bi, com o i!)', 8.6, 'red', anchor='start')
    return f


# ---------------------------------------------------------------- p12
def fig_trigcircle():
    W, H = 500, 456
    f = Fig(W, H)
    cx, cy, R = 250, 228, 150
    pl = Plane(f, cx, cy, R)
    # quadrantes (sinais)
    for (qx, qy, t) in [(0.5, 0.5, '(+, +)'), (-0.5, 0.5, '(−, +)'), (-0.5, -0.5, '(−, −)'), (0.5, -0.5, '(+, −)')]:
        pl.text(qx, qy, t, 9.5, 'gray_m', dy=3)
    for (qx, qy, t) in [(0.5, 0.36, '1º Q'), (-0.5, 0.36, '2º Q'), (-0.5, -0.64, '3º Q'), (0.5, -0.64, '4º Q')]:
        pl.text(qx, qy, '~' + t, 8, 'gray_m', dy=3)
    pl.axes(-1.34, 1.34, -1.34, 1.34, xlab='~cos θ (Re)', ylab='~sen θ (Im)', grid=False, ticks=False, origin=False, lab_size=8.6)
    f.circle(cx, cy, R, 'none', 'cyan', 1.9)
    # rótulos 1, -1 nos eixos
    for (x, y, t, dx, dy) in [(1, 0, '1', -7, 13), (-1, 0, '−1', -7, 13), (0, 1, '1', 9, 3), (0, -1, '−1', 11, 3)]:
        px, py = pl.P(x, y); f.text(px + dx, py + dy, t, 8.4, 'gray', anchor='middle')
    # ângulos
    angs = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    rad = {0: '0', 30: 'π/6', 45: 'π/4', 60: 'π/3', 90: 'π/2', 120: '2π/3', 135: '3π/4', 150: '5π/6', 180: 'π', 210: '7π/6', 225: '5π/4', 240: '4π/3', 270: '3π/2', 300: '5π/3', 315: '7π/4', 330: '11π/6'}
    for a in angs:
        x, y = cpt(1, a)
        px, py = pl.P(x, y)
        f.dot(px, py, 2.9, 'cyan')
        if a == 0:
            f.text(px + 10, py + 14, '0° = 360°', 8.6, 'ink', anchor='start'); f.text(px + 10, py + 24, '0 = 2π', 8.4, 'orange', anchor='start')
            continue
        lx, ly = cpt(1.0, a)
        ox_, oy_ = pl.P(lx * 1.0, ly * 1.0)
        ux, uy = math.cos(a * D2R), -math.sin(a * D2R)
        tx, ty = ox_ + ux * 12, oy_ + uy * 12
        anc = 'start' if ux > 0.3 else ('end' if ux < -0.3 else 'middle')
        if a == 30:
            f.text(px - 16, py - 20, '30°', 8.6, 'ink', anchor='end'); f.text(px - 16, py - 10, 'π/6', 8.4, 'orange', anchor='end')
            continue
        if a in (90, 270):
            ty += (-4 if a == 90 else 9)
            f.text(tx, ty - 9, f'{a}°', 8.6, 'ink', anchor='middle') if a == 90 else f.text(tx, ty - 9, f'{a}°', 8.6, 'ink', anchor='middle')
            f.text(tx, ty + 1, rad[a], 8.4, 'orange', anchor='middle')
        else:
            f.text(tx, ty - 4 if uy < 0 else ty - 2, f'{a}°', 8.6, 'ink', anchor=anc)
            f.text(tx, ty + 6 if uy < 0 else ty + 8, rad[a], 8.4, 'orange', anchor=anc)
    # demonstração 30° : cos, sen, tg
    a = 30
    x, y = cpt(1, a)
    pl.line(0, 0, x, y, 'ink', 1.8)
    pl.line(0, 0, x, 0, 'blue', 3.2); pl.line(x, 0, x, y, 'purple', 3.2)
    pl.line(1, 0, 1, math.tan(a * D2R), 'gray', 2.0)
    pl.line(0, 0, 1, math.tan(a * D2R), 'gray', 1.0, dash='3 3')
    pl.arc(0.2, 0, 30, 'orange', 2.0)
    pl.text(x / 2, 0, 'cos θ', 8.6, 'blue', dy=19 if False else 17, weight=700)
    pl.text(x, y / 2, 'sen θ', 8.6, 'purple', dx=-5, dy=3, anchor='end', weight=700)
    pl.text(1, math.tan(a * D2R) / 2, 'tg θ', 8.4, 'gray', dx=-4, dy=4, anchor='end', weight=700) if False else pl.text(1, math.tan(a * D2R) * 0.52, '~tg θ', 8.4, 'gray', dx=5, dy=3, anchor='start', weight=700)
    pl.text(0.26, 0.04, 'θ', 9, 'orange', dy=-1, dx=1)
    return f


# ---------------------------------------------------------------- p13
def fig_quadrants():
    f = Fig(396, 300)
    pl = Plane(f, 198, 150, 52)
    # quadrantes sombreados levemente
    for (x0, y0) in [(0, 0), (-3.4, 0), (-3.4, -2.6), (0, -2.6)]:
        pass
    pl.axes(-3.7, 3.7, -2.75, 2.75, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=True, lab_size=9)
    items = [(math.sqrt(3), 1, 30, '√3 + i', 'θ = 30° = π/6', 'blue'),
             (-1, 1, 135, '−1 + i', 'θ = 135° = 3π/4', 'purple'),
             (-1, -1, 225, '−1 − i', 'θ = 225° = 5π/4', 'orange'),
             (1, -1, 315, '1 − i', 'θ = 315° = 7π/4', 'green')]
    for (x, y, a, zt, tt, c) in items:
        pl.vec(x, y, c, 2.0)
        pl.pt(x, y, c, 3.2)
        r = {30: 0.42, 135: 0.66, 225: 0.9, 315: 1.14}[a]
        pl.arc(r, 0, a, c, 1.7, arrow=True, head=6.5)
        # ângulo de referência
        px, py = pl.P(x, y)
    pl.text(math.sqrt(3), 1, 'z_1 = √3 + i', 9.2, 'blue', dx=7, dy=-5, anchor='start', weight=700, bg='white'); pl.text(math.sqrt(3), 1, '~θ = 30° = π/6', 8, 'blue', dx=7, dy=6, anchor='start')
    pl.text(-1, 1, 'z_2 = −1 + i', 9.2, 'purple', dx=-6, dy=-6, anchor='end', weight=700, bg='white'); pl.text(-1, 1, '~θ = 135° = 3π/4', 8, 'purple', dx=-6, dy=5, anchor='end')
    pl.text(-1, -1, 'z_3 = −1 − i', 9.2, 'orange', dx=-6, dy=14, anchor='end', weight=700, bg='white'); pl.text(-1, -1, '~θ = 225° = 5π/4', 8, 'orange', dx=-6, dy=25, anchor='end')
    pl.text(1, -1, 'z_4 = 1 − i', 9.2, 'green', dx=6, dy=14, anchor='start', weight=700, bg='white'); pl.text(1, -1, '~θ = 315° = 7π/4', 8, 'green', dx=6, dy=25, anchor='start')
    # ângulos
    pl.text(0.78, 0.34, '30°', 8.4, 'blue', anchor='start', dy=-4) if False else None
    pl.text(2.35, 0.42, '30°', 8.4, 'blue', anchor='start', dy=0) if False else None
    # texto dos quadrantes
    q = [(3.7, 2.62, 'end', '~1º Q: a > 0, b > 0', '~cos+, sen+  ·  θ = θ₀'), (-3.7, 2.62, 'start', '~2º Q: a < 0, b > 0', '~cos−, sen+  ·  θ = π − θ₀'),
         (-3.7, -2.18, 'start', '~3º Q: a < 0, b < 0', '~cos−, sen−  ·  θ = π + θ₀'), (3.7, -2.18, 'end', '~4º Q: a > 0, b < 0', '~cos+, sen−  ·  θ = 2π − θ₀')]
    for (x, y, anc, t1, t2) in q:
        px, py = pl.P(x, y)
        f.text(px, py - 4, t1, 8.6, 'ink', anchor=anc, weight=700)
        f.text(px, py + 7, t2, 8.0, 'gray', anchor=anc)
    return f


# ---------------------------------------------------------------- p14
def fig_polar():
    f = Fig(520, 304)
    ox, oy, s = 50, 250, 105
    pl = Plane(f, ox, oy, s)
    pl.axes(-0.2, 1.95, -0.2, 2.45, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=True, lab_size=9)
    a, b = 1.0, math.sqrt(3)
    f.poly([pl.P(0, 0), pl.P(a, 0), pl.P(a, b)], 'green_l', 'none', 0, op=0.5)
    pl.line(0, 0, a, 0, 'blue', 3.0); pl.line(a, 0, a, b, 'purple', 3.0)
    pl.vec(a, b, 'green', 2.8)
    pl.line(a, b, 0, b, 'purple', 1.0, dash='3 3')
    pl.pt(a, b, 'ink', 3.8)
    pl.arc(0.32, 0, 60, 'orange', 2.2)
    pl.text(0.5, 0, 'a = ρ cos θ = 1', 9.6, 'blue', dy=17, weight=700)
    pl.text(a, b / 2, 'b = ρ sen θ = √3', 9.6, 'purple', dx=8, anchor='start', weight=700)
    pl.text(0.5, 0.87, 'ρ = 2', 10, 'green', dx=-9, dy=-6, anchor='end', weight=700)
    pl.text(0.36, 0.1, 'θ = 60°', 9.4, 'orange', anchor='start', dx=3, dy=-8) if False else None
    pl.text(0.34, 0.12, 'θ', 10.5, 'orange', anchor='start', dx=4, dy=-3)
    px, py = pl.P(0, b)
    f.text(px - 6, py + 3, '√3', 8.6, 'purple', anchor='end')
    px, py = pl.P(a, 0)
    # painel das três representações
    X0 = 262
    f.text(X0 + 118, 22, '~O MESMO número, três representações', 9.6, 'ink', weight=700)
    f.label_box(X0, 34, 236, 56, '', 'blue_l', 'blue', rx=4)
    f.text(X0 + 8, 50, '~① Forma algébrica', 8.6, 'blue', anchor='start', weight=700)
    f.text(X0 + 8, 76, 'z = «blue:1» + «purple:√3»«purple:i»', 17, 'ink', anchor='start')
    f.label_box(X0, 98, 236, 56, '', 'gray_l', 'gray', rx=4)
    f.text(X0 + 8, 114, '~② Afixo no plano (ponto)', 8.6, 'gray', anchor='start', weight=700)
    f.text(X0 + 8, 140, 'P(«blue:1», «purple:√3»)', 17, 'ink', anchor='start')
    f.label_box(X0, 162, 236, 70, '', 'orange_l', 'orange', rx=4)
    f.text(X0 + 8, 178, '~③ Forma trigonométrica', 8.6, 'orange', anchor='start', weight=700)
    f.text(X0 + 8, 204, 'z = «green:2»(cos «orange:60°» + i sen «orange:60°»)', 14.5, 'ink', anchor='start')
    f.text(X0 + 8, 222, 'z = «green:2» cis «orange:π/3»', 12, 'ink', anchor='start')
    f.arrow(X0 + 118, 92, X0 + 118, 98, 'gray', 1.0, 4)
    f.text(X0 + 118, 252, '~ρ = |z| = √(1² + (√3)²) = 2   ·   cos θ = 1/2, sen θ = √3/2', 8, 'gray') if False else None
    f.text(X0 + 118, 256, '~cos θ = a/ρ = 1/2  ·  sen θ = b/ρ = √3/2', 8.4, 'gray')
    f.text(X0 + 118, 270, '~⇒ θ = 60° (1º quadrante)', 8.4, 'orange', weight=700)
    return f


# ---------------------------------------------------------------- p10 (três figuras)
def fig_sum():
    f = Fig(246, 178)
    pl = Plane(f, 24, 156, 27)
    pl.axes(-0.3, 8.0, -0.3, 5.6, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.5, origin=False, lab_size=8.6)
    z, w = (4, 3), (1, 2)
    s = (5, 5)
    pl.line(*z, *s, 'gray', 1.2, dash='4 3'); pl.line(*w, *s, 'gray', 1.2, dash='4 3')
    pl.vec(*z, 'blue', 2.0); pl.vec(*w, 'purple', 2.0); pl.vec(*s, 'green', 2.4)
    for p, c in [(z, 'blue'), (w, 'purple'), (s, 'green')]: pl.pt(*p, c, 3.2)
    pl.text(4, 3, 'z = 4 + 3i', 8.8, 'blue', dx=6, dy=11, anchor='start', weight=700, bg='white')
    pl.text(1, 2, 'w = 1 + 2i', 8.8, 'purple', dx=-6, dy=-6, anchor='start', weight=700, bg='white')
    pl.text(5, 5, 'z + w = 5 + 5i', 9.2, 'green', dx=7, dy=3, anchor='start', weight=700)
    return f


def fig_diff():
    f = Fig(246, 178)
    pl = Plane(f, 24, 156, 27)
    pl.axes(-0.3, 8.0, -0.3, 5.6, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.5, origin=False, lab_size=8.6)
    z, w = (4, 3), (1, 2)
    pl.vec(*z, 'blue', 1.5); pl.vec(*w, 'purple', 1.5)
    pl.vec(3, 1, 'green', 1.6, dash='4 3')      # translação para a origem
    pl.vec(*z, 'green', 2.6, x0=w[0], y0=w[1])  # w -> z
    for p, c in [(z, 'blue'), (w, 'purple')]: pl.pt(*p, c, 3.2)
    pl.pt(3, 1, 'green', 2.6)
    pl.text(4, 3, 'z', 10, 'blue', dx=6, dy=0, anchor='start', weight=700)
    pl.text(1, 2, 'w', 10, 'purple', dx=-7, dy=-3, anchor='end', weight=700)
    pl.text(2.6, 2.75, 'z − w', 9.4, 'green', dx=0, dy=-8, weight=700, bg='white')
    pl.text(3, 1, 'z − w = 3 + i', 8.6, 'green', dx=7, dy=12, anchor='start', bg='white')
    f.text(150, 40, '|z − w| = √(3² + 1²)', 9, 'green', anchor='start') if False else None
    f.text(138, 36, '~d = |z − w| = √10', 9.2, 'green', anchor='start', weight=700)
    f.text(138, 49, '~(distância entre os afixos)', 7.6, 'gray', anchor='start')
    return f


def fig_locus():
    f = Fig(246, 178)
    pl = Plane(f, 62, 118, 21)
    pl.axes(-2.7, 8.2, -3.8, 4.9, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.2, origin=False, lab_size=8.6)
    pl.circle(3, cx=2, cy=1, stroke='cyan', w=2.2, fill='cyan_l', op=0.55)
    pl.circle(3, cx=2, cy=1, stroke='cyan', w=2.2)
    pl.pt(2, 1, 'ink', 3.0)
    pl.line(2, 1, 5, 1, 'green', 1.8)
    pl.text(3.5, 1, 'r = 3', 8.8, 'green', dy=-4, weight=700, bg='white') if False else pl.text(3.5, 1, 'r = 3', 8.8, 'green', dy=-4, weight=700)
    zx, zy = 2 + 3 * math.cos(55 * D2R), 1 + 3 * math.sin(55 * D2R)
    pl.line(2, 1, zx, zy, 'orange', 1.3, dash='4 3')
    pl.pt(zx, zy, 'orange', 3.0)
    pl.text(zx, zy, 'z', 9.4, 'orange', dx=6, dy=-3, anchor='start', weight=700)
    pl.text(2, 1, 'z₀ = 2 + i', 8.6, 'ink', dx=-6, dy=13, anchor='end', bg='white') if False else pl.text(2, 1, 'z₀', 9.4, 'ink', dx=-6, dy=12, anchor='end', weight=700)
    f.text(118, 14, '~|z − z₀| = 3', 8.8, 'cyan', anchor='start', weight=700) if False else None
    f.text(238, 14, '~|z − (2 + i)| = 3', 8.8, 'cyan', anchor='end', weight=700)
    f.text(238, 26, '~círculo cheio: |z − z₀| ≤ 3', 7.6, 'cyan', anchor='end')
    return f


# ---------------------------------------------------------------- p15
def fig_rot():
    f = Fig(300, 276)
    pl = Plane(f, 150, 138, 40)
    pl.axes(-3.5, 3.5, -3.3, 3.3, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.5, origin=False, lab_size=9)
    P = {'z': (2, 1), 'iz': (-1, 2), 'mz': (-2, -1), 'miz': (1, -2)}
    pl.line(*P['z'], *P['iz'], 'gray', 1.0, dash='3 3'); pl.line(*P['iz'], *P['mz'], 'gray', 1.0, dash='3 3')
    pl.line(*P['mz'], *P['miz'], 'gray', 1.0, dash='3 3'); pl.line(*P['miz'], *P['z'], 'gray', 1.0, dash='3 3')
    # triângulo-modelo de z e de iz
    pl.line(2, 0, 2, 1, 'blue', 1.0, dash='2 2'); pl.line(-1, 0, -1, 2, 'orange', 1.0, dash='2 2')
    cols = {'z': 'blue', 'iz': 'orange', 'mz': 'gray', 'miz': 'gray'}
    for k, (x, y) in P.items():
        pl.vec(x, y, cols[k], 2.2)
        pl.pt(x, y, cols[k], 3.2)
    pl.arc(0.9, 26.57, 116.57, 'orange', 1.8, arrow=True)
    pl.arc(0.9, 116.57, 206.57, 'gray', 1.4, arrow=True)
    pl.arc(0.9, 206.57, 296.57, 'gray', 1.4, arrow=True)
    pl.arc(0.9, 296.57, 386.57, 'gray', 1.4, arrow=True)
    pl.text(2, 1, 'z = 2 + i', 9.4, 'blue', dx=6, dy=-3, anchor='start', weight=700, bg='white')
    pl.text(-1, 2, 'iz = −1 + 2i', 9.4, 'orange', dx=-6, dy=-5, anchor='end', weight=700, bg='white')
    pl.text(-2, -1, '−z = −2 − i', 9.4, 'gray', dx=-6, dy=14, anchor='end', weight=700, bg='white')
    pl.text(1, -2, '−iz = 1 − 2i', 9.4, 'gray', dx=7, dy=12, anchor='start', weight=700, bg='white')
    pl.text(0.2, 0.55, '90°', 8.6, 'orange', anchor='start', dx=0, dy=0) if False else None
    pl.text(0.0, 0.0, '', 8)
    f.text(150 - 26, 138 - 26, '×i', 9, 'orange', weight=700) if False else None
    return f


def fig_scale():
    f = Fig(230, 276)
    pl = Plane(f, 28, 236, 40)
    pl.axes(-0.4, 5.1, -0.4, 5.6, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.5, origin=False, lab_size=9)
    z = (2, 1); w = (1, 3)
    pl.vec(*z, 'blue', 2.0); pl.vec(*w, 'orange', 2.4)
    pl.pt(*z, 'blue', 3.2); pl.pt(*w, 'orange', 3.2)
    pl.arc(0.9, 26.57, 71.57, 'orange', 1.8, arrow=True)
    pl.text(*z, 'z = 2 + i', 9.2, 'blue', dx=6, dy=11, anchor='start', weight=700, bg='white')
    pl.text(*w, '(1+i)z = 1 + 3i', 9.2, 'orange', dx=7, dy=-1, anchor='start', weight=700, bg='white')
    pl.text(1.0, 0.45, '+45°', 8.6, 'orange', anchor='start', dx=9, dy=-12) if False else None
    pl.text(0.6, 0.55, '45°', 8.4, 'orange', anchor='start', dx=36, dy=-32) if False else None
    f.text(176, 100, '~|z| = √5', 8.4, 'blue', anchor='end', op=None) if False else None
    return f


# ---------------------------------------------------------------- p16
def fig_polarmult():
    f = Fig(290, 262)
    pl = Plane(f, 36, 224, 72)
    pl.axes(-0.3, 3.5, -0.25, 3.0, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=True, lab_size=9)
    Z = cpt(2, 30); W = cpt(math.sqrt(2), 45); ZW = cpt(2 * math.sqrt(2), 75)
    pl.circle(2.0, stroke='gray_m', w=0.9, dash='2 3') if False else None
    pl.vec(*Z, 'blue', 2.2); pl.vec(*W, 'purple', 2.2); pl.vec(*ZW, 'green', 2.8)
    for p, c in [(Z, 'blue'), (W, 'purple'), (ZW, 'green')]: pl.pt(*p, c, 3.2)
    pl.arc(1.55, 0, 30, 'blue', 1.5, arrow=True)
    pl.arc(1.0, 0, 45, 'purple', 1.5, arrow=True)
    pl.arc(2.15, 0, 75, 'orange', 2.0, arrow=True)
    pl.text(*Z, 'Z = 2 cis 30°', 9.2, 'blue', dx=8, dy=3, anchor='start', weight=700, bg='white')
    pl.text(*W, 'W = √2 cis 45°', 9.2, 'purple', dx=-8, dy=-6, anchor='end', weight=700, bg='white')
    pl.text(*ZW, 'ZW = 2√2 cis 75°', 9.4, 'green', dx=8, dy=-3, anchor='start', weight=700, bg='white')
    f.text(120, 238, '~30° + 45° = 75°   ·   2 · √2 = 2√2', 8.4, 'orange', weight=700) if False else None
    return f


# ---------------------------------------------------------------- p17
def fig_demoivre():
    f = Fig(400, 318)
    cx, cy, R = 200, 160, 112
    pl = Plane(f, cx, cy, R)
    pl.axes(-1.32, 1.32, -1.32, 1.32, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=False, lab_size=8.6)
    f.circle(cx, cy, R, 'none', 'gray_m', 1.2, dash='3 3')
    # polígono de 12 pontos e espiral de setas
    for n in range(12):
        a = 30 * n
        x, y = cpt(1, a)
        col = 'blue' if n in (0, 6) else ('purple' if n in (3, 9) else 'orange')
        f.line(cx, cy, *pl.P(x, y), stroke='#dde2e9', w=0.9)
    for n in range(12):
        a = 30 * n
        x, y = cpt(1, a)
        col = 'blue' if n in (0, 6) else ('purple' if n in (3, 9) else 'orange')
        pl.pt(x, y, col, 4.0 if n in (0, 3, 6, 9) else 3.0)
        ux, uy = math.cos(a * D2R), -math.sin(a * D2R)
        px, py = pl.P(x, y)
        lab = f'w^{{{n}}}'
        if n == 0: lab = 'w^{0} = w^{12} = 1'
        if n == 3: lab = 'w^{3} = i'
        if n == 6: lab = 'w^{6} = −1'
        if n == 9: lab = 'w^{9} = −i'
        anc = 'start' if ux > 0.2 else ('end' if ux < -0.2 else 'middle')
        dx, dy = ux * 10, uy * 11 + (4 if uy > 0.2 else (0 if abs(uy) < 0.2 else -1))
        if n == 0: dx, dy, anc = 9, -4, 'start'
        if n == 6: dx, dy, anc = -9, -4, 'end'
        f.text(px + dx, py + dy + (3 if abs(uy) < 0.2 else 0), lab, 9.2, col, anchor=anc, weight=700 if n % 3 == 0 else None)
    for n in range(0, 12, 1):
        pass
    pl.arc(0.28, 0, 30, 'orange', 1.8, arrow=True)
    pl.text(0.36, 0.06, '30°', 8.4, 'orange', anchor='start', dx=2, dy=3) if False else f.text(cx + 38, cy - 8, '30°', 8.2, 'orange', anchor='start')
    return f


# ---------------------------------------------------------------- p18
def _root_fig(n, rho, theta0, label_fn, s=60, size=(330, 296)):
    f = Fig(*size)
    cx, cy = size[0] / 2, size[1] / 2 + 12
    pl = Plane(f, cx, cy, s)
    lim = rho * 1.42
    pl.axes(-lim, lim, -lim * 0.86, lim * 0.86, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=False, lab_size=8.6)
    pl.circle(rho, stroke='gray_m', w=1.3, dash='3 3')
    pts = []
    for k in range(n):
        a = theta0 + 360 * k / n
        pts.append(cpt(rho, a))
    pl.f.poly([pl.P(*p) for p in pts], 'violet_l', 'violet', 1.5, op=0.35)
    for k, p in enumerate(pts):
        a = theta0 + 360 * k / n
        pl.line(0, 0, *p, 'gray', 0.9, dash='2 3')
        pl.pt(*p, 'purple' if k else 'green', 4.0)
        ux, uy = math.cos(a * D2R), -math.sin(a * D2R)
        px, py = pl.P(*p)
        anc = 'start' if ux > 0.2 else ('end' if ux < -0.2 else 'middle')
        lx_, ly_ = px + ux * 10, py + uy * 10 + (4 if uy > 0.3 else 0) + (3 if abs(uy) < 0.2 else 0)
        if ux < -0.9: anc, lx_, ly_ = 'start', px - 6, py - 11
        f.text(lx_, ly_, label_fn(k, a), 8.8, 'purple' if k else 'green', anchor=anc, weight=700, bg='white')
    # arcos: θ0 e passo
    pl.arc(0.34 * rho, 0, theta0, 'orange', 1.8, arrow=True)
    step = 360 / n
    pl.arc(0.55 * rho, theta0, theta0 + step, 'orange', 1.8, arrow=True)
    return f, pl


def fig_roots3():
    f, pl = _root_fig(3, 1.0, 60, lambda k, a: ['W₀ = cis 60°', 'W₁ = cis 180°', 'W₂ = cis 300°'][k], s=98, size=(330, 296))
    f.text(165, 12, '~∛(−1): módulo 1  ·  θ₀ = 60°  ·  passo 120°', 8.4, 'orange', weight=700)
    return f


def fig_roots4():
    f, pl = _root_fig(4, 2.0, 45, lambda k, a: ['W₀ = 2 cis 45°', 'W₁ = 2 cis 135°', 'W₂ = 2 cis 225°', 'W₃ = 2 cis 315°'][k], s=49, size=(330, 296))
    f.text(165, 12, '~⁴√(−16): módulo 2  ·  θ₀ = 45°  ·  passo 90°', 8.4, 'orange', weight=700)
    return f


# ---------------------------------------------------------------- p19
def fig_unity():
    f = Fig(640, 232)
    R = 70
    for (cx, n, title) in [(110, 3, 'z³ = 1 : triângulo'), (320, 4, 'z⁴ = 1 : quadrado'), (530, 6, 'z⁶ = 1 : hexágono')]:
        cy = 118
        pl = Plane(f, cx, cy, R)
        pl.axes(-1.3, 1.3, -1.25, 1.25, xlab=None, ylab=None, grid=False, ticks=False, origin=False)
        pl.circle(1.0, stroke='gray_m', w=1.1, dash='3 3')
        pts = [cpt(1, 360 * k / n) for k in range(n)]
        f.poly([pl.P(*p) for p in pts], 'violet_l', 'violet', 1.7, op=0.45)
        for k, p in enumerate(pts):
            pl.line(0, 0, *p, 'gray_m', 0.8, dash='2 3')
            pl.pt(*p, 'green' if k == 0 else 'purple', 3.8)
        pl.text(0, 0, '', 8)
        f.text(cx, 16, '~' + title, 9.2, 'violet', weight=700)
        # rótulos
        if n == 3:
            lab = [('1', 'start', 8, -6), ('−½ + (√3/2) i', 'end', -6, -6), ('−½ − (√3/2) i', 'end', -6, 14)]
        elif n == 4:
            lab = [('1', 'start', 8, -6), ('i', 'start', 8, -2), ('−1', 'end', -8, -6), ('−i', 'start', 8, 8)]
        else:
            lab = [('1', 'start', 8, -6), ('cis 60°', 'start', 6, -7), ('cis 120°', 'end', -6, -7), ('−1', 'end', -8, -6), ('cis 240°', 'end', -6, 14), ('cis 300°', 'start', 6, 14)]
        for p, (t, anc, dx, dy) in zip(pts, lab):
            px, py = pl.P(*p)
            f.text(px + dx, py + dy, t, 8.6, 'ink', anchor=anc, bg='white')
        f.text(cx, 226, '~passo angular = 360°/n = %d°' % (360 // n), 8.2, 'orange')
    return f


def fig_unity_r():
    f = Fig(300, 252)
    pl = Plane(f, 150, 128, 46)
    pl.axes(-3.0, 3.0, -2.65, 2.65, xlab='~Re', ylab='~Im', grid=False, ticks=False, origin=False, lab_size=8.6)
    pl.circle(1.0, stroke='gray_m', w=1.0, dash='2 3')
    pl.circle(2.0, stroke='violet', w=1.6)
    pts = [cpt(2, 120 * k) for k in range(3)]
    f.poly([pl.P(*p) for p in pts], 'violet_l', 'violet', 1.7, op=0.45)
    for k, p in enumerate(pts):
        pl.line(0, 0, *p, 'gray', 0.9, dash='2 3')
        pl.pt(*p, 'green' if k == 0 else 'purple', 3.8)
    pl.text(2, 0, '2', 9, 'green', dx=6, dy=-7, anchor='start', weight=700)
    pl.text(-1, math.sqrt(3), '−1 + i√3', 9, 'purple', dx=-6, dy=-6, anchor='end', weight=700, bg='white')
    pl.text(-1, -math.sqrt(3), '−1 − i√3', 9, 'purple', dx=-6, dy=13, anchor='end', weight=700, bg='white')
    pl.text(0.0, 0.0, '', 8)
    f.text(150, 244, '~z³ = 8: raio R = ∛8 = 2 (círculo tracejado = raio 1)', 8.2, 'gray')
    return f


ALL = [fig_sets, fig_icycle, fig_anat_alg, fig_distrib, fig_conj, fig_argand, fig_modulus, fig_trigcircle,
       fig_quadrants, fig_polar, fig_sum, fig_diff, fig_locus, fig_rot, fig_scale, fig_polarmult,
       fig_demoivre, fig_roots3, fig_roots4, fig_unity, fig_unity_r]
