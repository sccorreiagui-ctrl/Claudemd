"""Figuras do Módulo I — Fundamentos."""
import math
from . import fig
from lib.circuit import *


@fig("atomo")
def atomo():
    f = Fig(332, 190, title="Átomo: núcleo com prótons e nêutrons; elétrons na eletrosfera")
    cx, cy = 88, 92
    r1, r2 = 38, 72
    f.circ(cx, cy, r1, "none", GRY_M, 1.2, dash="3 3", tag="bg")
    f.circ(cx, cy, r2, "none", GRY_M, 1.2, dash="3 3", tag="bg")
    pos = [(-7, -8), (6, -9), (-12, 3), (0, 1), (11, 2), (-4, 12), (7, 12)]
    kinds = ["n", "p", "n", "p", "n", "n", "p"]
    for (dx, dy), k in zip(pos, kinds):
        if k == "p":
            f.circ(cx + dx, cy + dy, 6.6, POS_L, POS, 1.5, tag="bg")
            f.line(cx + dx - 3, cy + dy, cx + dx + 3, cy + dy, POS, 1.4, tag="bg")
            f.line(cx + dx, cy + dy - 3, cx + dx, cy + dy + 3, POS, 1.4, tag="bg")
        else:
            f.circ(cx + dx, cy + dy, 6.6, GRY_XL, GRY, 1.5, tag="bg")
    els = [(r1, 40), (r1, 220), (r2, 118)]
    for (rad, ang) in els:
        ex, ey = cx + rad * math.cos(math.radians(ang)), cy - rad * math.sin(math.radians(ang))
        f.circ(ex, ey, 6.8, NEG_L, NEG, 1.7, tag="bg")
        f.line(ex - 3.2, ey, ex + 3.2, ey, NEG, 1.5, tag="bg")
    # legendas
    ex, ey = cx + r1 * math.cos(math.radians(40)), cy - r1 * math.sin(math.radians(40))
    f.line(ex + 7, ey - 2, 178, 30, GRY_M, 0.9, tag="bg")
    f.text(182, 28, "elétron  (−)", 12, NEG_D, anchor="start", weight=600)
    f.text(182, 42, "carga −e · massa ≈ 9,1×10⁻³¹ kg", 10, MUTED, anchor="start")
    f.line(cx + 12, cy + 2, 178, 82, GRY_M, 0.9, tag="bg")
    f.text(182, 80, "próton  (+)", 12, POS_D, anchor="start", weight=600)
    f.text(182, 94, "carga +e · massa ≈ 1,67×10⁻²⁷ kg", 10, MUTED, anchor="start")
    f.line(cx - 12, cy + 4, 178, 134, GRY_M, 0.9, tag="bg")
    f.text(182, 132, "nêutron  (sem carga)", 12, GRY, anchor="start", weight=600)
    f.text(182, 146, "massa ≈ 1,67×10⁻²⁷ kg", 10, MUTED, anchor="start")
    f.text(166, 184, "eletrosfera ≈ 10⁻¹⁰ m  ·  núcleo ≈ 10⁻¹⁵ m", 10.5, MUTED)
    return f


@fig("vec_anatomia")
def vec_anatomia():
    f = Fig(332, 204, title="Módulo, direção e sentido de um vetor; componentes")
    ox, oy = 46, 182
    L, ang = 200, 30
    ex, ey = ox + L * math.cos(math.radians(ang)), oy - L * math.sin(math.radians(ang))
    f.line(ex, oy, ex, ey, GRY_M, 1.2, "4 3", tag="bg")
    f.line(ox, ey, ex, ey, GRY_M, 1.2, "4 3", tag="bg")
    f.arrow(ox, oy, ex, oy, GRY, 1.8, 8)
    f.arrow(ex, oy, ex, ey + 1, GRY, 1.8, 8)
    f.arrow(ox, oy, ex, ey, INK, 3.0, 12, 0.36)
    f.arc(ox, oy, 50, 0, ang, GRY, 1.4)
    f.text(ox + 66, oy - 9, "$\\theta$", 14, INK)
    f.text(126, 119, "$\\vec F$", 15, INK)
    f.text((ox + ex) / 2, oy + 17, "$F_x = F\\cos\\theta$", 12, GRY)
    f.text(ex + 8, (oy + ey) / 2 + 5, "$F_y = F\\,\\sen\\theta$", 12, GRY, anchor="start")
    for k, (a, b) in enumerate((("módulo", "comprimento da seta (em newtons)"), ("direção", "reta suporte (ângulo θ)"),
                               ("sentido", "para onde aponta a ponta"))):
        f.text(8, 15 + k * 30, a, 12, INK, anchor="start", weight=700)
        f.text(8, 29 + k * 30, b, 10.5, MUTED, anchor="start")
    return f


@fig("soma_vec")
def soma_vec():
    f = Fig(680, 150, title="Soma de vetores: mesmo sentido, sentidos opostos, perpendiculares")
    W = 213
    for k, tt in enumerate(("Mesma direção e sentido", "Mesma direção, sentidos opostos", "Direções perpendiculares")):
        x0 = k * (W + 20)
        f.text(x0 + W / 2, 13, tt, 12, INK, weight=700)
        f.line(x0, 21, x0 + W, 21, RULE, 1, tag="bg")
    # (a)
    x0 = 0
    f.arrow(x0 + 14, 52, x0 + 84, 52, INK, 2.4, 10)
    f.text(x0 + 49, 43, "$\\vec F_1$", 13, INK)
    f.arrow(x0 + 84, 52, x0 + 184, 52, INK, 2.4, 10)
    f.text(x0 + 134, 43, "$\\vec F_2$", 13, INK)
    f.arrow(x0 + 14, 90, x0 + 184, 90, INK, 3.6, 12)
    f.text(x0 + 99, 81, "$\\vec F_R$", 13, INK)
    f.text(x0 + W / 2, 128, "$F_R = F_1 + F_2$", 13, INK)
    # (b)
    x0 = W + 20
    f.arrow(x0 + 100, 50, x0 + 190, 50, INK, 2.4, 10)
    f.text(x0 + 145, 41, "$\\vec F_1$", 13, INK)
    f.arrow(x0 + 100, 68, x0 + 40, 68, INK, 2.4, 10)
    f.text(x0 + 70, 86, "$\\vec F_2$", 13, INK)
    f.arrow(x0 + 100, 100, x0 + 130, 100, INK, 3.6, 12)
    f.text(x0 + 148, 105, "$\\vec F_R$", 13, INK, anchor="start")
    f.line(x0 + 100, 44, x0 + 100, 106, GRY_M, 1, "3 3", tag="bg")
    f.text(x0 + W / 2, 128, "$F_R = F_1 - F_2$  (se $F_1 > F_2$)", 12.5, INK)
    # (c)
    x0 = 2 * (W + 20)
    ox, oy = x0 + 40, 92
    f.arrow(ox, oy, ox + 110, oy, INK, 2.4, 10)
    f.text(ox + 56, oy + 15, "$\\vec F_1$", 13, INK)
    f.arrow(ox, oy, ox, oy - 52, INK, 2.4, 10)
    f.text(ox - 8, oy - 24, "$\\vec F_2$", 13, INK, anchor="end")
    f.line(ox + 110, oy, ox + 110, oy - 52, GRY, 1.2, "4 3", tag="bg")
    f.line(ox, oy - 52, ox + 110, oy - 52, GRY, 1.2, "4 3", tag="bg")
    f.arrow(ox, oy, ox + 110, oy - 52, INK, 3.6, 12)
    f.text(ox + 30, oy - 44, "$\\vec F_R$", 13, INK, halo=True)
    f.text(x0 + W / 2, 128, "$F_R = \\sqrt{F_1^{\\,2} + F_2^{\\,2}}$", 13, INK, lint=False)
    f.text(x0 + W / 2, 145, "$\\tg\\,\\theta = F_2/F_1$", 12, INK, lint=False)
    return f


@fig("trig")
def trig():
    f = Fig(332, 150, title="Triângulo retângulo: cateto oposto, adjacente e hipotenusa")
    ax, ay = 40, 122
    bx, by = 250, 122
    cx, cy = 250, 30
    f.pl([(ax, ay), (bx, by), (cx, cy)], INK, 2.2, fill=SOFT, close=True)
    f.pl([(bx - 12, by), (bx - 12, by - 12), (bx, by - 12)], INK, 1.3)
    f.arc(ax, ay, 40, 0, math.degrees(math.atan2(ay - cy, bx - ax)), INK, 1.5)
    f.text(ax + 52, ay - 8, "$\\theta$", 14, INK)
    f.text((ax + bx) / 2, ay + 18, "cateto adjacente  ($c_a$)", 12, INK)
    f.text(bx + 10, (by + cy) / 2 + 4, "cateto", 12, INK, anchor="start")
    f.text(bx + 10, (by + cy) / 2 + 18, "oposto", 12, INK, anchor="start")
    f.text(bx + 10, (by + cy) / 2 + 32, "($c_o$)", 12, INK, anchor="start")
    f.text((ax + cx) / 2 - 12, (ay + cy) / 2 - 12, "hipotenusa ($h$)", 12, INK, anchor="end", halo=True)
    return f


@fig("prop4")
def prop4():
    f = Fig(680, 196, title="Proporcionalidades: direta, inversa, quadrática e inversa do quadrado")
    titles = [("Direta", "y = k·x", "U = R·I"), ("Inversa", "y = k/x", "I = U/R"),
              ("Quadrática", "y = k·x²", "P = U²/R"), ("Inversa do quadrado", "y = k/x²", "F = k·q₁q₂/r²")]
    rule = ["x ×2  →  y ×2", "x ×2  →  y ÷2", "x ×2  →  y ×4", "x ×2  →  y ÷4"]
    fns = [lambda x: x, lambda x: 1 / x, lambda x: x * x, lambda x: 1 / (x * x)]
    lims = [(2.4, 4.8), (2.4, 4.4), (2.4, 5.6), (2.4, 4.4)]
    ys_pts = [(1, 2), (1, 2), (1, 2), (1, 2)]
    for k in range(4):
        x0 = k * 172 + 12
        f.text(x0 + 70, 13, titles[k][0], 12, INK, weight=700)
        P = Plot(f, x0 + 14, 150, 120, 108, (0, lims[k][0]), (0, lims[k][1]), xticks=[(1, "1"), (2, "2")], yticks=[],
                 grid=False, arrows=True, tick_size=10)
        fn = fns[k]
        a = 0.32 if k in (1, 3) else 0.0
        if k == 1:
            a = 0.3
        if k == 3:
            a = 0.46
        P.curve(fn, a, lims[k][0] - 0.02, 90, c=EFD if k in (1, 3) else CUR, w=2.4)
        for xv in (1, 2):
            yv = fn(xv)
            P.guide(x=xv, y=yv, c=GRY_M)
            P.point(xv, yv, INK, 3.6)
        f.text(x0 + 14 + 120 + 10, 150 + 5, "x", 11, MUTED, anchor="start", lint=False)
        f.text(x0 + 14 - 9, 150 - 108 - 12, "y", 11, MUTED, anchor="middle", lint=False)
        f.text(x0 + 70, 176, rule[k], 11.5, INK, weight=600)
        f.text(x0 + 70, 191, titles[k][2], 11.5, MUTED)
    return f


@fig("dotcross")
def dotcross():
    f = Fig(332, 198, title="Convenção ⊙ (saindo do plano) e ⊗ (entrando no plano)")
    # setas 3D vistas de frente / de trás
    for k, kind in enumerate(("out", "in")):
        x0 = 6 + k * 168
        f.rect(x0, 8, 156, 54, SOFT, RULE, 1, rx=4, tag="bg")
        f.cross_dot(x0 + 28, 35, kind, 14, INK, 2.0)
        if kind == "out":
            f.text(x0 + 52, 31, "saindo do plano", 12, INK, anchor="start", weight=700)
            f.text(x0 + 52, 46, "(ponta da seta vista", 10.5, MUTED, anchor="start")
            f.text(x0 + 52, 58, "de frente)", 10.5, MUTED, anchor="start")
        else:
            f.text(x0 + 52, 31, "entrando no plano", 12, INK, anchor="start", weight=700)
            f.text(x0 + 52, 46, "(cauda da seta vista", 10.5, MUTED, anchor="start")
            f.text(x0 + 52, 58, "de trás)", 10.5, MUTED, anchor="start")
    # campos
    for k, kind in enumerate(("out", "in")):
        x0 = 6 + k * 168
        f.rect(x0, 74, 156, 100, "#fff", GRY_M, 1.3, rx=4)
        for i in range(4):
            for j in range(3):
                x, y = x0 + 26 + i * 34, 94 + j * 30
                if kind == "out":
                    f.circ(x, y, 7, "none", MAG, 1.5, tag="bg")
                    f.dot(x, y, 2.4, MAG)
                else:
                    f.circ(x, y, 7, "none", MAG, 1.5, tag="bg")
                    f.line(x - 4, y - 4, x + 4, y + 4, MAG, 1.5, tag="bg")
                    f.line(x - 4, y + 4, x + 4, y - 4, MAG, 1.5, tag="bg")
        f.text(x0 + 78, 193, "$\\vec B$ saindo" if kind == "out" else "$\\vec B$ entrando", 12, MAG_D, weight=600)
    return f


@fig("graf_leitura")
def graf_leitura():
    f = Fig(680, 212, title="Leitura de gráficos: inclinação e área")
    f.text(0, 13, "inclinação = $\\Delta U/\\Delta I$ = 6 V/A = 6 Ω", 12, INK, anchor="start", weight=600)
    P = Plot(f, 52, 176, 240, 112, (0, 2.5), (0, 15), xticks=[(0.5, "0,5"), (1, "1,0"), (1.5, "1,5"), (2, "2,0")],
             yticks=[(3, "3"), (6, "6"), (9, "9"), (12, "12")], grid=True)
    P.axis_labels("$I$ (A)", "$U$ (V)", ydx=2)
    P.line([(0, 0), (2.3, 13.8)], INK, 2.6)
    P.guide(x=0.5, y=3, c=GRY_M)
    P.guide(x=1.5, y=9, c=GRY_M)
    f.line(P.X(0.5), P.Y(3), P.X(1.5), P.Y(3), GRY, 1.4, "4 3", tag="bg")
    f.line(P.X(1.5), P.Y(3), P.X(1.5), P.Y(9), GRY, 1.4, "4 3", tag="bg")
    P.point(0.5, 3, INK, 3.4)
    P.point(1.5, 9, INK, 3.4)
    f.text(P.X(1.0) + 6, P.Y(3) + 15, "$\\Delta I = 1{,}0$ A", 11.5, INK, halo=True)
    f.text(P.X(1.5) + 8, P.Y(6) + 4, "$\\Delta U = 6$ V", 11.5, INK, anchor="start", halo=True)
    x2 = 372
    f.text(x2 - 20, 13, "área sob a curva = carga:  $Q = A_1 + A_2 = 16$ C", 12, INK, anchor="start", weight=600)
    P2 = Plot(f, x2 + 20, 176, 220, 112, (0, 6), (0, 5), xticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
              yticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], grid=True)
    P2.axis_labels("$t$ (s)", "$I$ (A)", ydx=2)
    P2.area([(0, 0), (2, 4), (2, 0)], 0, CUR, 0.30, None)
    P2.area([(2, 4), (5, 4), (5, 0), (2, 0)], 0, CUR, 0.14, None)
    P2.line([(0, 0), (2, 4), (5, 4), (5, 0)], CUR, 2.8)
    P2.guide(x=2, y=4, c=GRY_M)
    f.text(P2.X(1.62), P2.Y(0.7), "$A_1$", 11.5, INK, halo=True)
    f.text(P2.X(3.5), P2.Y(2.0), "$A_2$ = 12 C", 12, INK)
    return f


def _sym_cell(f, x, y, kind, name):
    p, q = (x - 34, y), (x + 34, y)
    if kind == "fio":
        f.wire([p, q])
    elif kind == "cruz":
        f.wire([(x - 34, y), (x - 8, y)])
        f.path(f"M{x - 8},{y} A8,8 0 0 1 {x + 8},{y}", INK, 2.0)
        f.wire([(x + 8, y), (x + 34, y)])
        f.wire([(x, y - 26), (x, y - 8)])
        f.wire([(x, y + 8), (x, y + 26)])
    elif kind == "conex":
        f.wire([(x - 34, y), (x + 34, y)])
        f.wire([(x, y - 26), (x, y + 26)])
        f.node(x, y, INK, 4.2)
    elif kind == "pilha":
        f.bat(p, q, "q", signs=True)
    elif kind == "res":
        f.res(p, q)
    elif kind == "lamp":
        f.lamp(p, q)
    elif kind == "sw0":
        f.sw(p, q, False)
    elif kind == "sw1":
        f.sw(p, q, True)
    elif kind == "cap":
        f.cap(p, q)
    elif kind == "amp":
        f.meter(p, q, "A")
    elif kind == "volt":
        f.meter(p, q, "V")
    elif kind == "gnd":
        f.wire([(x, y - 26), (x, y - 4)])
        f.ground(x, y - 4)
    elif kind == "fuse":
        f.fuse(p, q)
    elif kind == "led":
        f.led(p, q)
    elif kind == "motor":
        f.box(p, q, "M", circle=True, height=24)
    f.text(x, y + 38, name, 11.5, INK, lint=False)


@fig("sym_circ")
def sym_circ():
    f = Circ(680, 262, title="Símbolos usuais de circuitos elétricos")
    items = [("fio", "fio ideal (condutor)"), ("conex", "fios conectados (nó)"), ("cruz", "cruzamento sem conexão"),
             ("pilha", "pilha / bateria (fonte)"), ("res", "resistor"),
             ("lamp", "lâmpada"), ("sw0", "chave aberta"), ("sw1", "chave fechada"), ("cap", "capacitor"),
             ("fuse", "fusível"),
             ("amp", "amperímetro"), ("volt", "voltímetro"), ("gnd", "terra (referência)"), ("led", "LED (diodo emissor)"),
             ("motor", "motor")]
    for i, (k, n) in enumerate(items):
        r, c = divmod(i, 5)
        _sym_cell(f, 68 + c * 136, 36 + r * 86, k, n)
    return f
