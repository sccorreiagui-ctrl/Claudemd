"""Figuras do Módulo II — Eletrostática (parte B: campo, potencial, blindagem, capacitores)."""
import math
from . import fig
from lib.circuit import *


def _Edip(px, py, charges):
    ex = ey = 0.0
    for cx, cy, q in charges:
        dx, dy = px - cx, py - cy
        r2 = dx * dx + dy * dy
        r3 = r2 * math.sqrt(r2)
        ex += q * dx / r3
        ey += q * dy / r3
    return ex, ey


@fig("campo_pontual")
def campo_pontual():
    f = Fig(332, 198, title="Linhas de campo de cargas puntiformes positiva e negativa")
    for cx, sgn, txt in ((84, +1, "$Q>0$: $\\vec E$ aponta para fora"), (248, -1, "$Q<0$: $\\vec E$ aponta para dentro")):
        cy = 80
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            f.line(cx + 14 * ca, cy - 14 * sa, cx + 72 * ca, cy - 72 * sa, EFD, 1.7, tag="bg")
            if sgn > 0:
                f.head(cx + 50 * ca, cy - 50 * sa, math.atan2(-sa, ca), EFD, 9.5, 0.4, "bg")
            else:
                f.head(cx + 38 * ca, cy - 38 * sa, math.atan2(sa, -ca), EFD, 9.5, 0.4, "bg")
        f.charge(cx, cy, sgn, 11)
        # carga de prova e força
        a = 22.5
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        tx, ty = cx + 60 * ca, cy - 60 * sa
        if sgn > 0:
            f.arrow(tx + 7 * ca, ty - 7 * sa * 1, tx + 36 * ca, ty - 36 * sa, INK, 2.6, 9)
        else:
            f.arrow(tx - 7 * ca, ty + 7 * sa, tx - 34 * ca, ty + 34 * sa, INK, 2.6, 9)
        f.circ(tx, ty, 6.5, POS_L, POS, 1.6, tag="bg")
        f.line(tx - 3, ty, tx + 3, ty, POS, 1.4, tag="bg")
        f.line(tx, ty - 3, tx, ty + 3, POS, 1.4, tag="bg")
        f.text(cx, 170, txt, 11.5, INK)
    f.text(166, 191, "carga de prova $q>0$ (a força $\\vec F$ tem o sentido de $\\vec E$)", 10.5, MUTED)
    return f


@fig("dipolo_E")
def dipolo_E():
    f = Fig(332, 196, title="Campo elétrico de um dipolo e vetor E em um ponto P")
    ch = [(96, 106, +1), (236, 106, -1)]
    field_lines(f, ch, (2, 2, 330, 194), n_per_unit=10, c=EFD, w=1.4, r0=13, stop_r=11, arrows=(0.45,))
    f.charge(96, 106, +1, 11)
    f.charge(236, 106, -1, 11)
    Px, Py = 166, 52
    ex, ey = _Edip(Px, Py, ch)
    n = math.hypot(ex, ey)
    L = 52
    f.arrow(Px, Py, Px + L * ex / n, Py + L * ey / n, EFD_D, 3.2, 12)
    f.circ(Px, Py, 3.4, "#fff", INK, 1.8, tag="bg")
    f.text(Px - 8, Py - 8, "P", 12.5, INK, anchor="end", halo=True)
    f.text(Px + L * ex / n / 2 + 8, Py + L * ey / n / 2 - 10, "$\\vec E_P$", 13, EFD_D, halo=True)
    return f


@fig("placas_E")
def placas_E():
    f = Fig(332, 202, title="Campo elétrico uniforme entre placas paralelas")
    x0, x1, yt, yb = 48, 284, 40, 158
    f.rect(x0, yt - 9, x1 - x0, 9, POS_L, POS, 1.8, tag="bg")
    f.rect(x0, yb, x1 - x0, 9, NEG_L, NEG, 1.8, tag="bg")
    for i in range(10):
        px = x0 + 12 + i * (x1 - x0 - 24) / 9
        f.line(px - 3.4, yt - 4.5, px + 3.4, yt - 4.5, POS_D, 1.5, tag="bg")
        f.line(px, yt - 8, px, yt - 1, POS_D, 1.5, tag="bg")
        f.line(px - 3.4, yb + 4.5, px + 3.4, yb + 4.5, NEG_D, 1.5, tag="bg")
    for i in range(9):
        px = x0 + 14 + i * (x1 - x0 - 28) / 8
        f.line(px, yt + 2, px, yb - 2, EFD, 1.6, tag="bg")
        f.head(px, yt + 58, math.pi / 2, EFD, 9, 0.4, "bg")
    # cargas de prova
    xq1, xq2 = 112, 218
    f.circ(xq1, 100, 8, POS_L, POS, 1.8, tag="bg")
    f.line(xq1 - 3.6, 100, xq1 + 3.6, 100, POS, 1.6, tag="bg")
    f.line(xq1, 96.4, xq1, 103.6, POS, 1.6, tag="bg")
    f.arrow(xq1, 110, xq1, 140, INK, 2.8, 10)
    f.text(xq1 + 11, 130, "$\\vec F$", 12.5, INK, anchor="start", halo=True)
    f.circ(xq2, 100, 8, NEG_L, NEG, 1.8, tag="bg")
    f.line(xq2 - 3.6, 100, xq2 + 3.6, 100, NEG, 1.6, tag="bg")
    f.arrow(xq2, 90, xq2, 60, INK, 2.8, 10)
    f.text(xq2 + 11, 74, "$\\vec F$", 12.5, INK, anchor="start", halo=True)
    f.text(xq1 - 12, 104, "$+q$", 12, POS_D, anchor="end", halo=True)
    f.text(xq2 - 12, 104, "$-q$", 12, NEG_D, anchor="end", halo=True)
    f.text(x0 - 6, 105, "$\\vec E$", 14, EFD_D, anchor="end")
    f.arrow(x1 + 20, yt, x1 + 20, yb, GRY, 1.2, 7, 0.4, both=True)
    f.text(x1 + 26, 104, "$d$", 12.5, INK, anchor="start")
    f.text(x0 + 8, 24, "placa  +", 11.5, POS_D, anchor="start", weight=600)
    f.text(x0 + 8, 190, "placa  −", 11.5, NEG_D, anchor="start", weight=600)
    return f


@fig("super_E")
def super_E():
    f = Fig(332, 204, title="Superposição de campos elétricos no ponto P")
    Q1, Q2, P = (56, 174), (276, 174), (166, 64)
    f.line(Q1[0], Q1[1], P[0], P[1], GRY_M, 1.1, "4 3", tag="bg")
    f.line(Q2[0], Q2[1], P[0], P[1], GRY_M, 1.1, "4 3", tag="bg")
    d1 = (P[0] - Q1[0], P[1] - Q1[1])
    n1 = math.hypot(*d1)
    e1 = (d1[0] / n1 * 70, d1[1] / n1 * 70)
    d2 = (Q2[0] - P[0], Q2[1] - P[1])
    n2 = math.hypot(*d2)
    e2 = (d2[0] / n2 * 70, d2[1] / n2 * 70)
    f.line(P[0] + e1[0], P[1] + e1[1], P[0] + e1[0] + e2[0], P[1] + e1[1] + e2[1], GRY, 1.1, "4 3", tag="bg")
    f.line(P[0] + e2[0], P[1] + e2[1], P[0] + e1[0] + e2[0], P[1] + e1[1] + e2[1], GRY, 1.1, "4 3", tag="bg")
    f.arrow(P[0], P[1], P[0] + e1[0], P[1] + e1[1], EFD, 2.8, 11)
    f.arrow(P[0], P[1], P[0] + e2[0], P[1] + e2[1], EFD, 2.8, 11)
    f.arrow(P[0], P[1], P[0] + e1[0] + e2[0], P[1] + e1[1] + e2[1], EFD_D, 3.8, 13)
    f.circ(P[0], P[1], 3.4, "#fff", INK, 1.8, tag="bg")
    f.text(P[0] - 8, P[1] - 6, "P", 12.5, INK, anchor="end", halo=True)
    f.text(P[0] + e1[0] * 0.5 - 8, P[1] + e1[1] * 0.5 - 2, "$\\vec E_1$", 13, EFD_D, anchor="end", halo=True)
    f.text(P[0] + e2[0] * 0.5 + 9, P[1] + e2[1] * 0.5 + 14, "$\\vec E_2$", 13, EFD_D, anchor="start", halo=True)
    f.text(P[0] + (e1[0] + e2[0]) * 0.62, P[1] + 17, "$\\vec E_R$", 13.5, EFD_D, anchor="middle", halo=True)
    f.text(166, 16, "$\\vec E_R=\\vec E_1+\\vec E_2$  (soma vetorial)", 12, INK, lint=False)
    f.charge(*Q1, +1, 11)
    f.charge(*Q2, -1, 11)
    f.text(Q1[0], 198, "$+Q$", 12, POS_D)
    f.text(Q2[0], 198, "$-Q$", 12, NEG_D)
    return f


@fig("equip_pontual")
def equip_pontual():
    f = Fig(332, 216, title="Superfícies equipotenciais de uma carga puntiforme positiva")
    cx, cy = 166, 100
    for a in range(0, 360, 45):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        f.line(cx + 13 * ca, cy - 13 * sa, cx + 96 * ca, cy - 96 * sa, EFD, 1.4, tag="bg")
        f.head(cx + 50 * ca, cy - 50 * sa, math.atan2(-sa, ca), EFD, 9, 0.4, "bg")
    for r, V in ((30, 900), (60, 450), (90, 300)):
        f.circ(cx, cy, r, "none", EFD_D, 1.9, dash="6 4", tag="bg")
        f.text(cx + r * 0.7071 + 3, cy - r * 0.7071 + 4, f"{V} V", 11.5, EFD_D, anchor="start", weight=700, halo=True)
    f.charge(cx, cy, +1, 11)
    for (x, nm) in ((cx + 30, "A"), (cx + 90, "B")):
        f.circ(x, cy, 3.6, "#fff", INK, 1.8, tag="bg")
        f.text(x, cy + 17, nm, 12.5, INK, weight=700, halo=True)
    f.text(166, 208, "$r$ = 0,10 m, 0,20 m e 0,30 m  ($Q=+10$ nC)", 11, MUTED)
    return f


@fig("placas_equip")
def placas_equip():
    f = Fig(332, 176, title="Placas paralelas com superfícies equipotenciais")
    x0, x1, yt, yb = 56, 244, 24, 126
    f.rect(x0, yt - 9, x1 - x0, 9, POS_L, POS, 1.8, tag="bg")
    f.rect(x0, yb, x1 - x0, 9, NEG_L, NEG, 1.8, tag="bg")
    for i in range(8):
        px = x0 + 12 + i * (x1 - x0 - 24) / 7
        f.line(px - 3.4, yt - 4.5, px + 3.4, yt - 4.5, POS_D, 1.5, tag="bg")
        f.line(px, yt - 8, px, yt - 1, POS_D, 1.5, tag="bg")
        f.line(px - 3.4, yb + 4.5, px + 3.4, yb + 4.5, NEG_D, 1.5, tag="bg")
    for i in range(7):
        px = x0 + 14 + i * (x1 - x0 - 28) / 6
        f.line(px, yt + 2, px, yb - 2, EFD, 1.3, tag="bg", op=0.8)
        f.head(px, yt + 56, math.pi / 2, EFD, 8.5, 0.4, "bg")
    for k, V in enumerate((100, 80, 60, 40, 20, 0)):
        y = yt + k * (yb - yt) / 5
        if 0 < k < 5:
            f.line(x0, y, x1, y, EFD_D, 1.6, "6 4", tag="bg")
        f.text(x1 + 8, y + 4, f"{V} V", 11.5, EFD_D if 0 < k < 5 else INK, anchor="start", weight=600)
    f.arrow(x0 - 14, yt, x0 - 14, yb, GRY, 1.2, 7, 0.4, both=True)
    f.text(x0 - 20, 70, "$d$", 12.5, INK, anchor="end")
    f.text(x0 - 20, 84, "10 cm", 10.5, MUTED, anchor="end")
    f.text(166, 166, "$E=U/d=100\\text{ V}/0{,}10\\text{ m}=1000$ V/m", 11.5, INK)
    return f


@fig("acel_eletron")
def acel_eletron():
    f = Fig(332, 178, title="Elétron acelerado por uma diferença de potencial")
    xa, xb, y0, y1 = 64, 252, 26, 142
    f.rect(xa - 8, y0, 8, y1 - y0, NEG_L, NEG, 1.8, tag="bg")
    f.rect(xb, y0, 8, 46, POS_L, POS, 1.8, tag="bg")
    f.rect(xb, y0 + 70, 8, y1 - y0 - 70, POS_L, POS, 1.8, tag="bg")
    for yy in (36, 54, 112, 130):
        f.arrow(xb - 3, yy, xa + 4, yy, EFD, 1.5, 8, 0.4)
    f.text(150, 104, "$\\vec E$", 12.5, EFD_D)
    f.charge(xa + 22, 84, -1, 9)
    f.arrow(xa + 35, 84, xb - 8, 84, INK, 2.6, 10)
    f.text(150, 76, "$\\vec F$", 12.5, INK)
    f.arrow(xb + 14, 84, xb + 58, 84, NEG_D, 2.8, 11)
    f.text(xb + 36, 74, "$\\vec v$", 13, NEG_D)
    f.arrow(xa - 8, 158, xb + 8, 158, GRY, 1.2, 7, 0.4, both=True)
    f.text((xa + xb) / 2, 173, "$d$   ·   $U = V_B - V_A = 400$ V", 11.5, INK)
    f.text(xa - 10, 16, "placa A: 0 V", 11, NEG_D, anchor="start", weight=600)
    f.text(xb + 8, 16, "placa B: +400 V", 11, POS_D, anchor="end", weight=600)
    return f


@fig("gaiola")
def gaiola():
    f = Fig(332, 206, title="Condutor oco em campo externo: campo nulo no interior")
    cx, cy, R = 166, 103, 46
    E0 = 1.0

    def Ef(x, y):
        dx, dy = x - cx, cy - y   # coordenadas físicas (y para cima)
        r2 = dx * dx + dy * dy
        r = math.sqrt(r2)
        k = R ** 3 / r ** 5
        ex = E0 * (1 + k * (3 * dx * dx - r2))
        ey = E0 * (k * 3 * dx * dy)
        return ex, -ey   # y de tela para baixo

    def trace(x, y, sgn=1, n=700, st=3.0):
        pts = [(x, y)]
        for _ in range(n):
            e = Ef(x, y)
            m = math.hypot(*e) + 1e-12
            k1 = (e[0] / m, e[1] / m)
            e2 = Ef(x + st * 0.5 * sgn * k1[0], y + st * 0.5 * sgn * k1[1])
            m2 = math.hypot(*e2) + 1e-12
            x += sgn * st * e2[0] / m2
            y += sgn * st * e2[1] / m2
            pts.append((x, y))
            if math.hypot(x - cx, y - cy) < R + 0.8:
                break
            if not (2 <= x <= 328 and 4 <= y <= 202):
                break
        return pts
    lines = []
    for y0 in (22, 44, 64, 84, 103, 122, 142, 162, 184):
        lines.append(trace(3, y0, +1))
    for a in (0, 20, -20, 40, -40, 60, -60, 75, -75):
        sx, sy = cx + (R + 1) * math.cos(math.radians(a)), cy - (R + 1) * math.sin(math.radians(a))
        lines.append(trace(sx, sy, +1))
    for pts in lines:
        f.pl(pts, EFD, 1.5, tag="bg")
        f.mid_head(pts, 0.42, EFD, 8.5, 0.4, tag="bg")
    f.circ(cx, cy, R, "#fff", GRY, 3.2, tag="bg")
    f.circ(cx, cy, R - 7, GRY_XL, None, 0, fop=0.0)
    f.circ(cx, cy, R - 7, "none", GRY_L, 1.2, dash="3 3", tag="bg")
    for a in (140, 160, 180, 200, 220):
        f.text(cx + (R - 5) * math.cos(math.radians(a)), cy - (R - 5) * math.sin(math.radians(a)) + 4.5, "−", 14, NEG_D, weight=700, lint=False)
    for a in (-40, -20, 0, 20, 40):
        f.text(cx + (R - 5) * math.cos(math.radians(a)), cy - (R - 5) * math.sin(math.radians(a)) + 5, "+", 14, POS_D, weight=700, lint=False)
    f.text(cx, cy + 5, "$E=0$", 14, INK, weight=700)
    return f


@fig("pontas")
def pontas():
    f = Fig(332, 178, title="Poder das pontas: maior densidade de carga e campo mais intenso perto da ponta")
    ox, oy = 120, 92
    path = (f"M{ox},{oy-52} A52,52 0 0 0 {ox},{oy+52} C{ox+50},{oy+52} {ox+95},{oy+10} {ox+120},{oy} "
            f"C{ox+95},{oy-10} {ox+50},{oy-52} {ox},{oy-52} Z")
    f.path(path, GRY, 2.6, GRY_XL)

    def bez(p0, p1, p2, p3, t):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
    top = [(ox, oy - 52), (ox + 50, oy - 52), (ox + 95, oy - 10), (ox + 120, oy)]
    bot = [(ox, oy + 52), (ox + 50, oy + 52), (ox + 95, oy + 10), (ox + 120, oy)]
    plus = []
    for t in (0.3, 0.52, 0.68, 0.8, 0.9, 0.965):
        plus.append(bez(*top, t))
        plus.append(bez(*bot, t))
    for a in (110, 145, 180, 215, 250):
        plus.append((ox + 44 * math.cos(math.radians(a)), oy - 44 * math.sin(math.radians(a))))
    for (px, py) in plus:
        f.text(px, py + 4.5, "+", 12.5, POS_D, weight=700, lint=False)
    # linhas de campo
    for (ax, ay, bx, by) in ((ox + 124, oy, ox + 176, oy), (ox + 118, oy - 8, ox + 166, oy - 28), (ox + 118, oy + 8, ox + 166, oy + 28),
                             (ox - 54, oy, ox - 90, oy), (ox - 40, oy - 36, ox - 66, oy - 62), (ox - 40, oy + 36, ox - 66, oy + 62)):
        f.arrow(ax, ay, bx, by, EFD, 2.0, 9, 0.4)
    f.text(ox + 150, oy + 54, "campo intenso", 11.5, EFD_D, weight=600, lint=False)
    f.text(30, 172, "campo mais fraco", 11, MUTED, anchor="start", lint=False)
    return f


@fig("capacitor")
def capacitor():
    f = Circ(332, 172, title="Capacitor de placas paralelas carregado")
    x0, x1, yt, yb = 100, 280, 48, 116
    f.rect(x0, yt - 8, x1 - x0, 8, POS_L, POS, 1.8, tag="bg")
    f.rect(x0, yb, x1 - x0, 8, NEG_L, NEG, 1.8, tag="bg")
    f.rect(x0 + 1, yt + 1, x1 - x0 - 2, yb - yt - 2, GRY_XL, None, 0, fop=0.35)
    for i in range(8):
        px = x0 + 12 + i * (x1 - x0 - 24) / 7
        f.line(px - 3.2, yt - 4, px + 3.2, yt - 4, POS_D, 1.5, tag="bg")
        f.line(px, yt - 7, px, yt - 1, POS_D, 1.5, tag="bg")
        f.line(px - 3.2, yb + 4, px + 3.2, yb + 4, NEG_D, 1.5, tag="bg")
        f.line(px, yt + 4, px, yb - 4, EFD, 1.3, tag="bg", op=0.9)
        f.head(px, yt + 34, math.pi / 2, EFD, 7.5, 0.4, "bg")
    f.text((x0 + x1) / 2, yt + 50, "dielétrico (isolante)", 10.5, MUTED, halo=True)
    f.text(x1, yt - 14, "$+Q$", 12.5, POS_D, anchor="end")
    f.text(x1, yb + 22, "$-Q$", 12.5, NEG_D, anchor="end")
    f.arrow(x1 + 18, yt, x1 + 18, yb, GRY, 1.2, 7, 0.4, both=True)
    f.text(x1 + 25, (yt + yb) / 2 + 4, "$d$", 12.5, INK, anchor="start")
    f.text((x0 + x1) / 2 - 20, yb + 38, "área $A$ de cada placa", 11.5, INK)
    f.wire([(x0, yt - 4), (46, yt - 4)])
    f.wire([(x0, yb + 4), (46, yb + 4)])
    f.bat((46, yb + 4), (46, yt - 4), pos="q", lab="w", signs=True, name="$U$", ww=2.0)
    f.text(166, 14, "$C=Q/U$  ·  carga líquida total: $(+Q)+(-Q)=0$", 11.5, INK)
    return f


@fig("cap_assoc")
def cap_assoc():
    f = Circ(680, 214, title="Associação de capacitores em série e em paralelo")
    f.text(190, 14, "Série", 13, INK, weight=700)
    f.text(515, 14, "Paralelo", 13, INK, weight=700)
    # série
    y1, y2 = 56, 150
    f.wire([(78, y1), (100, y1)])
    f.cap((100, y1), (176, y1), "$C_1$", "6 µF", lab="n", pos="p")
    f.cap((176, y1), (252, y1), "$C_2$", "3 µF", lab="n", pos="p")
    f.wire([(252, y1), (310, y1), (310, y2), (78, y2)])
    f.bat((78, y2), (78, y1), pos="q", lab="w", name="$U$", val="12 V", signs=True)
    f.node(176, y1)
    f.text(190, 186, "mesma carga: $Q_1=Q_2=Q$   ·   $U=U_1+U_2$", 12, INK)
    f.text(190, 204, "$1/C_{eq}=1/C_1+1/C_2$  (como resistores em paralelo)", 11.5, EFD_D)
    # paralelo
    xo = 360
    f.wire([(xo + 40, y1), (xo + 120, y1)])
    f.wire([(xo + 120, y1), (xo + 250, y1)])
    f.wire([(xo + 40, y2), (xo + 250, y2)])
    f.bat((xo + 40, y2), (xo + 40, y1), pos="q", lab="w", name="$U$", val="12 V", signs=True)
    f.cap((xo + 120, y1), (xo + 120, y2), "$C_1$", "6 µF", lab="w", pos="p")
    f.cap((xo + 250, y1), (xo + 250, y2), "$C_2$", "3 µF", lab="e", pos="p")
    f.node(xo + 120, y1)
    f.node(xo + 120, y2)
    f.text(xo + 165, 186, "mesma tensão: $U_1=U_2=U$   ·   $Q=Q_1+Q_2$", 12, INK)
    f.text(xo + 165, 204, "$C_{eq}=C_1+C_2$  (soma direta)", 11.5, EFD_D)
    return f


@fig("cap_QU")
def cap_QU():
    f = Fig(332, 172, title="Gráfico Q × U de um capacitor: a área é a energia armazenada")
    P = Plot(f, 52, 140, 230, 100, (0, 14), (0, 28), xticks=[(4, "4"), (8, "8"), (12, "12")],
             yticks=[(8, "8"), (16, "16"), (24, "24")], grid=True)
    P.axis_labels("$U$ (V)", "$Q$ (µC)", ydx=6)
    P.area([(0, 0), (12, 24)], 0, ENE, 0.30, None)
    f.pl([(P.X(0), P.Y(0)), (P.X(12), P.Y(24)), (P.X(12), P.Y(0))], None, 0, fill=ENE, close=True, fop=0.30)
    P.line([(0, 0), (13, 26)], INK, 2.6)
    P.guide(x=12, y=24, c=GRY_M)
    P.point(12, 24, INK, 3.6)
    f.text(P.X(8.2), P.Y(6.5), "$E=Q\\,U/2$", 13, ENE_D, weight=700, halo=True)
    f.text(P.X(0.6), P.Y(20.0), "inclinação $=C$", 12, INK, anchor="start")
    f.text(P.X(0.6), P.Y(16.6), "(2 µC/V = 2 µF)", 11, MUTED, anchor="start")
    return f


@fig("desfib")
def desfib():
    f = Circ(332, 186, title="Circuito simplificado de desfibrilador: carga e descarga de um capacitor")
    yt, yb = 40, 144
    f.wire([(34, yt), (60, yt)])
    f.sw((60, yt), (130, yt), closed=True, name="S₁", lab="n", length=36)
    f.wire([(130, yt), (166, yt)])
    f.cap((166, yt), (166, yb), "$C$", lab="e", pos="p")
    f.wire([(166, yt), (200, yt)])
    f.sw((200, yt), (254, yt), closed=False, name="S₂", lab="n", length=36, ang=32)
    f.wire([(254, yt), (296, yt)])
    f.wire([(254, yt), (296, yt), (296, 62)])
    f.res((296, 62), (296, 124), "$R$", lab="e", length=40)
    f.wire([(296, 124), (296, yb), (34, yb)])
    f.bat((34, yb), (34, yt), pos="q", lab="w", name="HV", signs=True)
    f.node(166, yt)
    f.node(166, yb)
    f.text(166, 172, "fase 1 (S₁ fechada): a fonte carrega $C$ até $U$", 11, MUTED)
    return f


@fig("ex_campo")
def ex_campo():
    f = Fig(332, 150, title="Exemplo 5: carga fonte, ponto P e força sobre a carga de prova")
    xq, xp, y = 44, 244, 56
    f.line(xq + 14, y, xp - 12, y, GRY_M, 1.1, "5 4", tag="bg")
    f.charge(xq, y, +1, 12)
    f.charge(xp, y, -1, 11)
    f.arrow(xp + 14, y - 22, xp + 14 + 45, y - 22, EFD_D, 3.0, 11)
    f.text(xp + 14 + 22, y - 32, "$\\vec E$", 13, EFD_D)
    f.arrow(xp - 14, y + 22, xp - 14 - 45, y + 22, INK, 3.0, 11)
    f.text(xp - 14 - 22, y + 40, "$\\vec F$", 13, INK)
    f.arrow(xq, y + 54, xp, y + 54, GRY, 1.1, 6, 0.4, both=True)
    f.text((xq + xp) / 2, y + 70, "$r=0{,}10$ m (ponto $P$)", 11.5, INK)
    f.text(xq, y - 22, "$Q=+5{,}0$ nC", 11.5, POS_D, weight=600)
    f.text(166, 144, "$E=4{,}5\\times10^{3}$ N/C  ·  $F=9{,}0\\times10^{-3}$ N", 11, MUTED)
    return f


@fig("dip_mid")
def dip_mid():
    f = Fig(332, 168, title="Exemplo 9: ponto médio de um dipolo, campo não nulo e potencial nulo")
    y = 78
    xq1, xm, xq2 = 52, 166, 280
    f.line(xm, 14, xm, 144, EFD_D, 1.8, "6 4", tag="bg")
    f.text(xm + 8, 24, "$V=0$ (mediatriz)", 11.5, EFD_D, anchor="start", weight=600)
    f.line(xq1 + 14, y, xq2 - 14, y, GRY_M, 1.1, "5 4", tag="bg")
    f.arrow(xm - 52, y - 22, xm + 56, y - 22, EFD_D, 3.4, 12)
    f.text(xm + 4, y - 32, "$\\vec E_M$", 13, EFD_D, halo=True)
    f.charge(xq1, y, +1, 12)
    f.charge(xq2, y, -1, 12)
    f.circ(xm, y, 3.8, "#fff", INK, 1.9, tag="bg")
    f.text(xm - 7, y + 18, "M", 12.5, INK, anchor="end", weight=700, halo=True)
    f.text(xq1, y + 28, "$+Q$", 12.5, POS_D)
    f.text(xq2, y + 28, "$-Q$", 12.5, NEG_D)
    f.arrow(xq1, 116, xm, 116, GRY, 1.1, 6, 0.4, both=True)
    f.arrow(xm, 116, xq2, 116, GRY, 1.1, 6, 0.4, both=True)
    f.text((xq1 + xm) / 2, 132, "0,30 m", 11.5, INK)
    f.text((xm + xq2) / 2, 132, "0,30 m", 11.5, INK)
    f.text(166, 160, "campo reforçado (mesmo sentido), potenciais se cancelam", 10.5, MUTED)
    return f
