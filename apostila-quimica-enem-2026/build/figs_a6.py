"""Bloco A · página 8 — bicamada fosfolipídica, fosfolipídio, sabão, detergente, micela."""
import math
import random

from registry import fig
from svglib import SVG, C, tw
from figlib import pol, chip_svg

INK = C["ink"]
HEAD_F, HEAD_S = "#8DBBF2", C["blue"]
TAIL = C["amber"]
BLUED, AMBD = C["blue_d"], C["amber_d"]


def _tail(s, x, y0, length, direction, kink=False, rnd=None, color=TAIL, sw=2.0):
    """Cauda hidrocarbônica ondulada saindo de (x,y0) na vertical (direction=+1 desce, -1 sobe)."""
    pts = []
    n = int(length / 4)
    shift = 0.0
    for i in range(n + 1):
        t = i / n
        y = y0 + direction * length * t
        amp = 1.5
        xo = amp * math.sin(i * 1.7 + (rnd.random() if rnd else 0) * 2)
        if kink and t > 0.5:
            shift = 4.2
        pts.append((x + xo + shift, y))
    s.poly(pts, stroke=color, sw=sw, close=False)


def _lipid(s, x, y, direction, rnd, head_r=7.4):
    """Fosfolipídio: cabeça em (x,y); caudas na direção vertical."""
    y_tail0 = y + direction * (head_r - 0.5)
    _tail(s, x - 3.4, y_tail0, 42, direction, False, rnd)
    _tail(s, x + 3.4, y_tail0, 42, direction, True, rnd)
    s.circle(x, y, head_r, fill=HEAD_F, stroke=HEAD_S, sw=1.4)


@fig("a_bicamada")
def _bicamada():
    W, H = 695, 276
    s = SVG(W, H, title="Bicamada fosfolipídica e permeabilidade da membrana")
    rnd = random.Random(21)
    xl, xr = 10, 524
    yt, yb = 86, 196
    # regiões aquosas
    s.rect(xl, 6, xr - xl, 64, fill=C["blue_l"], rx=8, opacity=0.8)
    s.rect(xl, 214, xr - xl, 56, fill=C["blue_l"], rx=8, opacity=0.8)
    for _ in range(46):
        s.circle(rnd.uniform(xl + 6, xr - 6), rnd.uniform(14, 66), 1.9, fill=C["blue_m"])
    for _ in range(40):
        s.circle(rnd.uniform(xl + 6, xr - 6), rnd.uniform(222, 264), 1.9, fill=C["blue_m"])
    s.text(xl + 8, 21, "MEIO EXTRACELULAR · aquoso (polar)", 10.4, "start", 800, BLUED)
    s.text(xl + 8, 262, "CITOPLASMA · aquoso (polar)", 10.4, "start", 800, BLUED)
    # núcleo hidrofóbico (faixa)
    s.rect(xl, 134, xr - xl, 12, fill=C["amber_l"], opacity=0.9)
    # lipídios
    excl = (364, 438)
    x = xl + 8
    k = 0
    while x < xr - 6:
        if not (excl[0] < x < excl[1]):
            jy = rnd.uniform(-1.5, 1.5)
            _lipid(s, x, yt + jy, +1, rnd)
            _lipid(s, x + 0.0, yb + rnd.uniform(-1.5, 1.5), -1, rnd)
        x += 17.6
        k += 1
    # proteína canal
    for (px0, px1) in ((366, 392), (410, 436)):
        s.rect(px0, 70, px1 - px0, 142, fill=C["slate_m"], stroke=C["slate"], sw=1.4, rx=9, opacity=0.95)
    for yy in range(84, 206, 12):
        s.line(370, yy, 388, yy + 4, "#CBD5E1", 1.2)
        s.line(414, yy, 432, yy + 4, "#CBD5E1", 1.2)
    s.text(401, 256, "proteína transportadora (canal)", 9.8, "middle", 700, C["slate"])
    # O2 atravessa
    def o2(cx, cy):
        s.circle(cx - 3.2, cy, 3.6, fill="#FFFFFF", stroke=C["amber_d"], sw=1.5)
        s.circle(cx + 3.2, cy, 3.6, fill="#FFFFFF", stroke=C["amber_d"], sw=1.5)
    xo = 79.6
    o2(xo, 40)
    s.arrow(xo, 48, xo, 224, TAIL, 2.2, 8, dash="5 3")
    o2(xo, 236)
    s.text(xo + 12, 44, "O_2, CO_2, hormônios", 10, "start", 700, AMBD, halo="#E6F0FD")
    s.text(xo + 12, 56, "esteroides: apolares", 10, "start", 700, AMBD, halo="#E6F0FD")
    s.text(xo + 12, 68, "→ atravessam", 10, "start", 700, AMBD, halo="#E6F0FD")
    # íon bloqueado
    def ion(cx, cy):
        s.circle(cx, cy, 6.4, fill="#B79DFB", stroke="#6D4BD0", sw=1.2)
        s.text(cx, cy + 3.6, "+", 10, "middle", 800, "#fff")
    xi = 255.6
    ion(xi, 40)
    s.arrow(xi, 48, xi, 128, C["slate"], 2, 7)
    s.line(xi - 8, 133, xi + 8, 149, C["red"], 3.2)
    s.line(xi + 8, 133, xi - 8, 149, C["red"], 3.2)
    s.text(xi + 12, 44, "Na^+ não atravessa", 10, "start", 700, C["red_d"], halo="#E6F0FD")
    s.text(xi + 12, 56, "o núcleo apolar", 10, "start", 700, C["red_d"], halo="#E6F0FD")
    # íon via canal
    ion(401, 40)
    s.arrow(401, 48, 401, 212, "#6D4BD0", 2.4, 8)
    ion(401, 224)
    s.text(414, 44, "íons e polares grandes", 10, "start", 700, "#4C2FA0", halo="#E6F0FD")
    s.text(414, 56, "usam proteínas", 10, "start", 700, "#4C2FA0", halo="#E6F0FD")
    # rótulos laterais
    lx = 548
    def lab(y, y_target, t1, t2, col, tcol):
        s.line(lx - 8, y, xr + 4, y_target, col, 1.2)
        s.text(lx, y - 1, t1, 11, "start", 800, tcol)
        s.text(lx, y + 12, t2, 10, "start", 400, C["muted"])
    lab(70, 84, "Cabeças polares", "hidrofílicas: voltadas", BLUED, BLUED)
    s.text(lx, 93, "para a água", 10, "start", 400, C["muted"])
    lab(112, 116, "Caudas apolares", "hidrofóbicas: escondidas", C["amber"], AMBD)
    s.text(lx, 135, "da água (interior)", 10, "start", 400, C["muted"])
    lab(168, 196, "Cabeças polares", "voltadas para o citoplasma", BLUED, BLUED)
    s.text(lx, 192 + 18, "", 8)
    s.text(lx, 224, "Espessura ≈ 7–8 nm", 10.4, "start", 700, C["slate"])
    s.text(lx, 237, "(duas folhas de lipídios)", 10, "start", 400, C["muted"])
    return s


@fig("a_fosfolipideo")
def _fosfolip():
    W, H = 330, 176
    s = SVG(W, H, title="Estrutura esquemática de um fosfolipídio")
    hx, hy = 62, 26
    s.circle(hx, hy, 17, fill=HEAD_F, stroke=HEAD_S, sw=1.6)
    s.text(hx, hy + 4.2, "P", 13, "middle", 800, BLUED)
    # glicerol
    s.line(hx, hy + 17, hx, hy + 38, "#6B7280", 3)
    s.line(hx, hy + 38, hx - 20, hy + 54, "#6B7280", 3)
    s.line(hx, hy + 38, hx + 20, hy + 54, "#6B7280", 3)
    # ésteres (roxo)
    for ex in (hx - 20, hx + 20):
        s.circle(ex, hy + 58, 8.5, fill=C["purple_l"], stroke=C["purple"], sw=1.5)
    # caudas
    def zig(x, y, n, kink=False):
        pts = [(x, y)]
        up = False
        for i in range(n):
            dx = 5.2 * (1 if i % 2 == 0 else -1)
            nx = pts[-1][0] + dx
            ny = pts[-1][1] + 9.4
            if kink and i == n // 2:
                nx += 7
            pts.append((nx, ny))
        s.poly(pts, stroke=TAIL, sw=2.4, close=False)
        return pts
    zig(hx - 20, hy + 66, 8)
    pr = zig(hx + 20, hy + 66, 8, kink=True)
    # rótulos com linhas-guia
    lx = 150
    def lab(y, ty, t1, t2, col, tcol, px, py):
        s.line(lx - 6, ty, px, py, col, 1.1)
        s.text(lx, ty - 1, t1, 10.8, "start", 800, tcol)
        s.text(lx, ty + 11, t2, 9.8, "start", 400, C["muted"])
    lab(0, 20, "cabeça polar", "fosfato + grupo polar (carga)", HEAD_S, BLUED, hx + 17, hy)
    lab(0, 54, "glicerol", "esqueleto de 3 carbonos", "#6B7280", INK, hx + 3, hy + 36)
    lab(0, 86, "2 ligações éster", "função orgânica (roxo)", C["purple"], C["purple_d"], hx + 28, hy + 58)
    lab(0, 124, "2 caudas apolares", "ácidos graxos (hidrocarbonetos)", TAIL, AMBD, pr[4][0] + 6, pr[4][1])
    lab(0, 160, "dupla cis na cauda", "faz a dobra: afasta as cadeias", C["red"], C["red_d"], pr[5][0] + 6, pr[5][1])
    return s


# ---------------------------------------------------------------------------- ícones comparativos
def _ico_head(s, x, y, r=8.4, sign=None, label=None):
    s.circle(x, y, r, fill=HEAD_F, stroke=HEAD_S, sw=1.4)
    if sign:
        s.text(x, y + 4, sign, 12, "middle", 800, BLUED)
    if label:
        s.text(x, y + 3, label, 7.6, "middle", 800, BLUED)


@fig("a_ico_fosfolipideo")
def _i1():
    s = SVG(110, 74)
    rnd = random.Random(3)
    _ico_head(s, 55, 14, 9.6)
    _tail(s, 51, 23, 44, +1, False, rnd, sw=2.2)
    _tail(s, 59.5, 23, 44, +1, True, rnd, sw=2.2)
    s.text(8, 20, "cabeça", 9.2, "start", 600, BLUED)
    s.text(8, 31, "polar", 9.2, "start", 600, BLUED)
    s.text(102, 56, "2 caudas", 9.2, "end", 600, AMBD)
    return s


@fig("a_ico_sabao")
def _i2():
    s = SVG(110, 74)
    rnd = random.Random(4)
    _ico_head(s, 55, 14, 9.6, "−")
    _tail(s, 55, 24, 46, +1, False, rnd, sw=2.4)
    s.text(70, 18, "COO^-  Na^+", 9, "start", 700, BLUED)
    s.text(70, 56, "1 cauda", 9.2, "start", 600, AMBD)
    return s


@fig("a_ico_detergente")
def _i3():
    s = SVG(110, 74)
    rnd = random.Random(5)
    _ico_head(s, 55, 14, 9.6, "−")
    # anel aromático esquemático entre cabeça e cauda
    cx, cy = 55, 36
    pts = [pol(cx, cy, 8.5, 90 + 60 * i) for i in range(6)]
    s.poly(pts, stroke=TAIL, sw=2, close=True)
    _tail(s, 55, 44.5, 24, +1, False, rnd, sw=2.4)
    s.text(70, 18, "SO_3^-  Na^+", 9, "start", 700, BLUED)
    s.text(70, 56, "1 cauda", 9.2, "start", 600, AMBD)
    return s


@fig("a_ico_micela")
def _i4():
    s = SVG(110, 74)
    rnd = random.Random(6)
    cx, cy = 55, 37
    s.circle(cx, cy, 13, fill=C["amber_m"], opacity=0.8)
    s.text(cx, cy + 3.4, "gordura", 7.8, "middle", 800, AMBD)
    n = 12
    for i in range(n):
        a = i * 360 / n
        x1, y1 = pol(cx, cy, 14.5, a)
        x2, y2 = pol(cx, cy, 25, a)
        s.line(x1, y1, x2, y2, TAIL, 2.2)
        hx, hy = pol(cx, cy, 29.5, a)
        s.circle(hx, hy, 4.9, fill=HEAD_F, stroke=HEAD_S, sw=1.1)
    return s


@fig("a_ico_bicamada")
def _i5():
    s = SVG(110, 74)
    rnd = random.Random(7)
    for i in range(5):
        x = 14 + i * 20.5
        s.circle(x, 10, 5.4, fill=HEAD_F, stroke=HEAD_S, sw=1.1)
        _tail(s, x - 2.2, 15, 21, +1, False, rnd, sw=1.6)
        _tail(s, x + 2.2, 15, 21, +1, True, rnd, sw=1.6)
        s.circle(x, 64, 5.4, fill=HEAD_F, stroke=HEAD_S, sw=1.1)
        _tail(s, x - 2.2, 59, 21, -1, False, rnd, sw=1.6)
        _tail(s, x + 2.2, 59, 21, -1, True, rnd, sw=1.6)
    return s
