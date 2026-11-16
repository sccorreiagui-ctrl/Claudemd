"""Figuras do Módulo IV — Magnetismo (parte B): força magnética, trajetórias, fio em campo, motor."""
import math
from . import fig
from lib.circuit import *
from .f40a_magn import Bmark, Bgrid, bez


def hand(f, x0, y0):
    """Mão direita espalmada, palma voltada para o leitor, dedos para cima, polegar para a direita."""
    fill, edge = GRY_XL, GRY
    # dedos (mindinho … indicador, da esquerda para a direita)
    for i, (h, dx) in enumerate(((42, 0), (54, 17.5), (60, 35), (50, 52.5))):
        f.rect(x0 + dx + 1, y0 - h, 15.5, h + 14, fill, edge, 1.5, rx=7.5, tag="bg")
    f.rect(x0, y0 - 2, 70, 64, fill, edge, 1.5, rx=10, tag="bg")
    for dx in (17.5, 35, 52.5):
        f.line(x0 + dx + 0.2, y0 - 2, x0 + dx + 0.2, y0 + 10, edge, 1.0, tag="bg")
    # polegar (à direita)
    f.rect(x0 + 58, y0 + 24, 56, 17, fill, edge, 1.5, rx=8.5, tag="bg")
    f.rect(x0 + 58, y0 + 22, 14, 21, fill, None, rx=4, tag="bg")
    f.line(x0 + 62, y0 + 22.7, x0 + 62, y0 + 42, fill, 3, tag="bg")


@fig("regra_mao")
def regra_mao():
    f = Fig(332, 246, title="Regra da mão direita (tapa) e sentido da força para cargas positivas e negativas")
    hx, hy = 22, 124
    f.text(96, 14, "mão direita, palma voltada para você", 10.5, MUTED)
    hand(f, hx, hy)
    f.arrow(hx + 114, hy + 33, hx + 150, hy + 33, CUR, 3.2, 12)
    f.text(hx + 150, hy + 20, "$\\vec v$ (ou $I$)", 11.5, CUR_D, anchor="end", weight=700, halo=True)
    f.arrow(hx + 34, hy - 68, hx + 34, hy - 98, MAG, 3.2, 12)
    f.text(hx + 44, hy - 80, "$\\vec B$", 12.5, MAG_D, anchor="start", weight=700, halo=True)
    f.cross_dot(hx + 36, hy + 32, "out", r=10, c=INK, w=2.0, fill=WHITE)
    f.text(hx + 36, hy + 80, "$\\vec F$ sai da palma (⊙)", 11, INK, weight=700, halo=True)
    f.text(14, 224, "polegar → $\\vec v$ (ou $I$);  dedos → $\\vec B$", 10.5, INK, anchor="start", weight=600)
    f.text(14, 238, "palma → $\\vec F$ (para carga $q>0$)", 10.5, INK, anchor="start", weight=600)
    # casos 2D
    for (y0, q, tit, c_v) in ((6, +1, "$q>0$: $\\vec F$ para cima", POS_D), (122, -1, "$q<0$: $\\vec F$ para baixo", NEG_D)):
        f.rect(192, y0, 136, 112, WHITE, RULE, 1.2, rx=6, tag="bg")
        for yy in (y0 + 14, y0 + 84):
            for xx in (214, 260, 306):
                Bmark(f, xx, yy, "in", 4.4, MAG, 1.1)
        cx, cy = 222, y0 + 49
        f.charge(cx, cy, q, 9)
        f.arrow(cx + 12, cy, cx + 66, cy, c_v, 2.8, 10)
        f.text(cx + 40, cy - 7, "$\\vec v$", 11.5, c_v, weight=700, halo=True)
        if q > 0:
            f.arrow(cx, cy - 12, cx, cy - 34, INK, 3.0, 10)
            f.text(cx + 8, cy - 22, "$\\vec F$", 12, INK, anchor="start", weight=700, halo=True)
        else:
            f.arrow(cx, cy + 12, cx, cy + 34, INK, 3.0, 10)
            f.text(cx + 8, cy + 28, "$\\vec F$", 12, INK, anchor="start", weight=700, halo=True)
        f.text(260, y0 + 104, tit, 10.5, INK, weight=700)
    return f


@fig("trajetorias")
def trajetorias():
    f = Fig(680, 176, title="Trajetórias de uma partícula carregada em campo magnético uniforme")
    pw = 226
    # painel (a): v ∥ B
    x0 = 0
    f.rect(x0 + 3, 4, pw - 6, 130, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (28, 112):
        f.arrow(x0 + 16, yy, x0 + pw - 16, yy, MAG, 2.0, 9)
    f.text(x0 + pw - 24, 20, "$\\vec B$", 12, MAG_D, anchor="end", weight=700, halo=True)
    f.charge(x0 + 40, 70, +1, 9)
    f.arrow(x0 + 52, 70, x0 + 112, 70, POS_D, 2.8, 10)
    f.text(x0 + 84, 60, "$\\vec v$", 12, POS_D, weight=700, halo=True)
    f.line(x0 + 112, 70, x0 + pw - 24, 70, CUR, 2.2, dash="6 4", tag="bg")
    f.head(x0 + pw - 14, 70, 0, CUR, 9, 0.4, "bg")
    f.text(x0 + pw / 2, 156, "(a) $\\vec v\\parallel\\vec B$: $F=0$", 11.5, INK, weight=700)
    f.text(x0 + pw / 2, 171, "reta, velocidade constante", 10.5, MUTED)
    # painel (b): v ⊥ B
    x0 = 227
    f.rect(x0 + 3, 4, pw - 6, 130, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (18, 50, 82, 114):
        for xx in (x0 + 24, x0 + 62, x0 + 100, x0 + 138, x0 + 176, x0 + 204):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    cx, cy, r = x0 + pw / 2, 68, 40
    f.circ(cx, cy, r, "none", CUR, 2.2, dash="6 4", tag="bg")
    f.dot(cx, cy, 2.4, INK)
    for ang in (200, 20):
        pts = [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(ang - 14, ang + 15, 4)]
        f.mid_head(pts, 0.5, CUR, 8.5, tag="bg")
    px, py = cx, cy + r
    f.arrow(px + 6, py, px + 52, py, POS_D, 2.8, 10)
    f.text(px + 52, py + 15, "$\\vec v$", 12, POS_D, anchor="end", weight=700, halo=True)
    f.arrow(px, py - 8, px, py - 34, INK, 2.8, 10)
    f.text(px + 7, py - 20, "$\\vec F$", 12, INK, anchor="start", weight=700, halo=True)
    f.charge(px, py, +1, 8)
    f.line(cx, cy, cx + r * 0.7, cy - r * 0.7, GRY, 1.3, tag="bg")
    f.text(cx + r * 0.42 + 3, cy - r * 0.28 - 7, "$r$", 12, INK, weight=700, halo=True)
    f.text(x0 + pw / 2, 156, "(b) $\\vec v\\perp\\vec B$: $F=|q|vB$ (máxima)", 11.5, INK, weight=700)
    f.text(x0 + pw / 2, 171, "círculo (MCU), $\\vec B$ entrando (⊗)", 10.5, MUTED)
    # painel (c): oblíquo → hélice
    x0 = 454
    f.rect(x0 + 3, 4, pw - 6, 130, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (22, 116):
        f.arrow(x0 + 14, yy, x0 + pw - 14, yy, MAG, 2.0, 9)
    f.text(x0 + pw - 22, 14, "$\\vec B$", 12, MAG_D, anchor="end", weight=700, halo=True)
    R, p_ = 24, 56
    pts = []
    for k in range(0, 241):
        u = k / 240 * 3.25
        sx = x0 + 22 + p_ * u - 0.5 * R * math.sin(2 * math.pi * u)
        sy = 69 - R * math.cos(2 * math.pi * u) * 0.85
        pts.append((sx, sy))
    f.pl(pts, CUR, 2.2, tag="bg")
    ex, ey = pts[-1]
    f.head(ex + 3, ey, math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]), CUR, 9, 0.4, "bg")
    f.charge(pts[0][0], pts[0][1], +1, 7.5)
    f.text(x0 + pw / 2, 156, "(c) oblíquo: $\\vec v$ e $\\vec B$ formam $\\theta$", 11.5, INK, weight=700)
    f.text(x0 + pw / 2, 171, "hélice: $v_\\parallel$ constante + círculo", 10.5, MUTED)
    return f


@fig("ex_eletron_B")
def ex_eletron_B():
    f = Fig(332, 206, title="Elétron em campo magnético uniforme entrando no papel: trajetória circular horária")
    f.rect(3, 3, 326, 200, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (22, 52, 82, 112, 142, 172):
        for xx in range(20, 320, 40):
            if yy < 200:
                Bmark(f, xx + (20 if (yy // 30) % 2 else 0), yy, "in", 4.2, MAG, 1.0)
    cx, cy, r = 166, 112, 62
    f.circ(cx, cy, r, "none", CUR, 2.2, dash="6 4", tag="bg")
    f.dot(cx, cy, 2.6, INK)
    f.line(cx, cy, cx - r * 0.87, cy + r * 0.5, GRY, 1.4, tag="bg")
    f.text(cx - r * 0.45 - 3, cy + r * 0.26 - 5, "$r$", 12.5, INK, anchor="end", weight=700, halo=True)
    # sentido horário: setas em alguns pontos
    for ang in (-20, 160, 250):
        pts = [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(ang + 14, ang - 15, -4)]
        f.mid_head(pts, 0.5, CUR, 9, tag="bg")
    px, py = cx, cy - r
    f.arrow(px + 11, py, px + 62, py, NEG_D, 3.0, 11)
    f.text(px + 60, py - 9, "$\\vec v$", 12.5, NEG_D, anchor="end", weight=700, halo=True)
    f.arrow(px, py + 11, px, py + 40, INK, 3.0, 11)
    f.text(px + 8, py + 31, "$\\vec F$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.charge(px, py, -1, 9)
    f.text(px - 14, py - 8, "elétron", 10.5, NEG_D, anchor="end", weight=600, halo=True)
    f.text(18, 20, "$\\vec B$ entrando (⊗)", 11, MAG_D, anchor="start", weight=700, halo=True)
    f.text(314, 196, "sentido horário (carga $-$)", 10.5, INK, anchor="end", weight=600, halo=True)
    return f


@fig("seletor_espectro")
def seletor_espectro():
    f = Fig(332, 206, title="Seletor de velocidades seguido de espectrômetro de massa")
    by = 104                                   # linha do feixe
    xs0, xs1 = 14, 134                         # seletor
    f.rect(xs1, 4, 194, 150, MAG_L, None, fop=0.35, tag="bg")
    for yy in range(18, 154, 34):
        for xx in range(xs1 + 26, 326, 36):
            Bmark(f, xx, yy, "in", 3.8, MAG, 1.0)
    f.rect(xs1 - 3, 4, 6, 64, GRY_M, GRY, 1.2, tag="bg")
    f.text(xs1 + 8, 20, "placa", 10, GRY, anchor="start", weight=600, halo=True)
    # placas do seletor
    f.rect(xs0 + 12, 64, xs1 - xs0 - 12, 7, POS_L, POS, 1.6, tag="bg")
    f.rect(xs0 + 12, 135, xs1 - xs0 - 12, 7, NEG_L, NEG, 1.6, tag="bg")
    f.text(xs0 + 6, 75, "+", 14, POS_D, anchor="middle", weight=700, lint=False)
    f.text(xs0 + 6, 144, "−", 14, NEG_D, anchor="middle", weight=700, lint=False)
    for xx in (60, 84, 108):
        f.arrow(xx, 76, xx, 92, EFD, 2.0, 7)
        Bmark(f, xx, 122, "in", 4.4, MAG, 1.2)
    f.text(118, 90, "$\\vec E$", 11, EFD_D, anchor="start", weight=700, halo=True)
    f.text(118, 126, "$\\vec B$", 11, MAG_D, anchor="start", weight=700, halo=True)
    # fendas
    f.line(xs0, by - 14, xs0, by - 4, GRY, 3, tag="bg")
    f.line(xs0, by + 4, xs0, by + 14, GRY, 3, tag="bg")
    f.line(xs1, by + 4, xs1, 135, GRY, 3, tag="bg")
    f.line(xs0 - 10, by, xs1, by, CUR, 2.2, dash="6 4", tag="bg")
    f.arrow(xs0 - 12, by, xs0 + 4, by, CUR, 2.2, 8)
    f.charge(32, by, +1, 7.5)
    f.arrow(32, by - 9, 32, by - 22, INK, 2.2, 8)
    f.arrow(32, by + 9, 32, by + 22, INK, 2.2, 8)
    f.text(41, by - 14, "$F_B$", 10, INK, anchor="start", weight=600, halo=True)
    f.text(41, by + 22, "$F_E$", 10, INK, anchor="start", weight=600, halo=True)
    # semicírculos em B'
    for r, c in ((27, CUR), (44, CUR_D)):
        ccy = by - r
        pts = [(xs1 + r * math.cos(math.radians(t)), ccy - r * math.sin(math.radians(t))) for t in range(-90, 91, 4)]
        f.pl(pts, c, 2.4, tag="bg")
        f.mid_head(pts, 0.5, c, 9, tag="bg")
        f.dot(xs1, by - 2 * r, 3.2, c)
    f.line(xs1, by, xs1 + 40, by, CUR, 2.2, tag="bg")
    f.text(xs1 + 8, by - 24, "$m_1$", 11.5, CUR_D, anchor="start", weight=700, halo=True)
    f.text(xs1 + 52, by - 56, "$m_2>m_1$", 11.5, CUR_D, anchor="start", weight=700, halo=True)
    f.text(318, 146, "$\\vec B'$ (⊗)", 10.5, MAG_D, anchor="end", weight=700, halo=True)
    f.text(166, 180, "seletor: $qE=qvB$ → $v=E/B$ (só passa essa velocidade)", 10.5, INK, weight=600)
    f.text(166, 196, "desvio em $B'$: $r=mv/(qB')$ — maior massa, maior raio", 10.5, INK, weight=600)
    return f


@fig("fio_em_B")
def fio_em_B():
    f = Fig(332, 150, title="Fio com corrente em campo magnético uniforme: força perpendicular a I e a B")
    f.rect(3, 3, 326, 144, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (20, 52, 84, 116):
        for xx in range(24, 320, 40):
            Bmark(f, xx + (20 if (yy // 32) % 2 else 0), yy, "in", 4.2, MAG, 1.0)
    f.rect(54, 63, 224, 11, GRY_L, GRY, 1.5, rx=3, tag="bg")
    f.arrow(100, 68.5, 240, 68.5, CUR, 3.2, 12)
    f.text(244, 62, "$I$", 12.5, CUR_D, anchor="start", weight=700, halo=True)
    f.arrow(166, 58, 166, 14, INK, 3.2, 12)
    f.text(176, 28, "$\\vec F$", 13, INK, anchor="start", weight=700, halo=True)
    f.arrow(54, 98, 278, 98, GRY, 1.2, 6, 0.4, both=True)
    f.text(166, 112, "$L$", 12.5, INK, weight=700, halo=True)
    f.text(160, 140, "$F=B\\,I\\,L\\,\\mathrm{sen}\\,\\theta$ — aqui $\\theta=90°$", 11, INK, weight=600, halo=True)
    f.text(20, 14, "$\\vec B$ entrando (⊗)", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    return f


@fig("motor_cc")
def motor_cc():
    f = Fig(332, 214, title="Motor de corrente contínua: forças em lados opostos da espira formam um binário")
    # ímãs e campo
    f.rect(8, 40, 34, 110, MAG_D, MAG_D, 1.6, rx=3, tag="bg")
    f.text(25, 100, "N", 15, WHITE, weight=700, lint=False)
    f.rect(178, 40, 34, 110, MAG_L, MAG_D, 1.6, rx=3, tag="bg")
    f.text(195, 100, "S", 15, MAG_D, weight=700, lint=False)
    for yy in (62, 95, 128):
        f.arrow(46, yy, 174, yy, MAG, 1.8, 8)
    f.text(110, 56, "$\\vec B$", 12, MAG_D, weight=700, halo=True)
    cx, cy, a = 110, 95, 38
    # espira vista de ponta (plano paralelo a B)
    f.line(cx - a, cy, cx + a, cy, GRY, 3.0, tag="bg")
    f.circ(cx, cy, 2.6, INK)
    f.circ(cx - a, cy, 9, WHITE, CUR_D, 2.2, tag="bg"); f.dot(cx - a, cy, 3, CUR_D)
    f.circ(cx + a, cy, 9, WHITE, CUR_D, 2.2, tag="bg")
    f.line(cx + a - 4.8, cy - 4.8, cx + a + 4.8, cy + 4.8, CUR_D, 2, tag="bg")
    f.line(cx + a - 4.8, cy + 4.8, cx + a + 4.8, cy - 4.8, CUR_D, 2, tag="bg")
    f.arrow(cx - a, cy - 12, cx - a, cy - 46, INK, 3.0, 11)
    f.arrow(cx + a, cy + 12, cx + a, cy + 46, INK, 3.0, 11)
    f.text(cx - a - 8, cy - 28, "$\\vec F$", 12, INK, anchor="end", weight=700, halo=True)
    f.text(cx + a - 8, cy + 38, "$-\\vec F$", 12, INK, anchor="end", weight=700, halo=True)
    # rotação (horária): arco por cima (esquerda → direita) e por baixo (direita → esquerda)
    pts = [(cx + 64 * math.cos(math.radians(t)), cy - 64 * math.sin(math.radians(t))) for t in range(150, 29, -4)]
    f.arrow_poly(pts, CUR, 2.2, 9)
    pts = [(cx + 64 * math.cos(math.radians(t)), cy - 64 * math.sin(math.radians(t))) for t in range(-30, -151, -4)]
    f.arrow_poly(pts, CUR, 2.2, 9)
    f.text(cx, cy - 74, "giro", 10.5, CUR_D, weight=700, halo=True)
    f.text(cx, 187, "binário: gira (sentido horário aqui)", 10.5, INK, weight=600)
    f.text(cx, 202, "$\\tau=N\\,B\\,I\\,A\\,\\mathrm{sen}\\,\\varphi$ ($\\varphi$: entre $\\vec B$ e a normal)", 10, MUTED)
    # comutador
    ox, oy, r = 282, 96, 21
    f.text(ox, 40, "comutador", 11, INK, weight=700)
    for (t0, t1, c) in ((20, 160, CUR), (200, 340, CUR_D)):
        pts = [(ox + r * math.cos(math.radians(t)), oy - r * math.sin(math.radians(t))) for t in range(t0, t1 + 1, 5)]
        f.pl(pts, c, 6.5, tag="bg")
    f.rect(ox - r - 15, oy - 5, 13, 10, GRY, GRY, 1, rx=2, tag="bg")
    f.rect(ox + r + 2, oy - 5, 13, 10, GRY, GRY, 1, rx=2, tag="bg")
    f.text(ox - r - 22, oy + 4, "+", 13, POS_D, anchor="end", weight=700, lint=False)
    f.text(ox + r + 22, oy + 4, "−", 13, NEG_D, anchor="start", weight=700, lint=False)
    f.text(ox, oy + 5, "gira", 10, MUTED, weight=600, lint=False)
    f.text(ox, 150, "inverte o sentido de $I$", 10, INK, weight=600)
    f.text(ox, 163, "a cada meia volta,", 10, INK, weight=600)
    f.text(ox, 176, "mantendo o giro", 10, INK, weight=600)
    return f


@fig("ex_fio_eq")
def ex_fio_eq():
    f = Fig(236, 214, title="Fio horizontal em equilíbrio: força magnética para cima equilibra o peso")
    f.rect(3, 3, 230, 208, WHITE, RULE, 1.2, rx=6, tag="bg")
    for yy in (68, 150, 188):
        for xx in (28, 68, 108, 148, 188):
            Bmark(f, xx + (20 if yy == 188 else 0), yy, "in", 4.2, MAG, 1.0)
    f.rect(26, 100, 184, 11, GRY_L, GRY, 1.5, rx=3, tag="bg")
    f.arrow(60, 105.5, 172, 105.5, CUR, 3.2, 12)
    f.text(178, 99, "$I$", 12.5, CUR_D, anchor="start", weight=700, halo=True)
    f.arrow(118, 96, 118, 52, INK, 3.2, 12)
    f.text(128, 76, "$\\vec F_m$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.arrow(118, 116, 118, 160, INK, 3.2, 12)
    f.text(128, 142, "$m\\vec g$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.arrow(26, 30, 210, 30, GRY, 1.2, 6, 0.4, both=True)
    f.text(118, 24, "$L=20$ cm", 11, INK, weight=700, halo=True)
    f.text(14, 46, "$\\vec B=0{,}50$ T (⊗)", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    f.text(118, 205, "$m=10$ g", 10.5, INK, weight=600, halo=True)
    return f
