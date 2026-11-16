"""Figuras do Módulo IV — Magnetismo (parte A): ímãs, campo terrestre, campo criado por correntes."""
import math
import random
from . import fig
from lib.circuit import *


# ───────────────────────── primitivas compartilhadas ─────────────────────────
def needle(f, x, y, ang, L=26, w=7.0):
    """Agulha de bússola em (x, y); a metade N (escura) aponta para ``ang`` (rad, coordenadas de tela)."""
    ca, sa = math.cos(ang), math.sin(ang)
    px, py = -sa * w / 2, ca * w / 2
    tip = (x + ca * L / 2, y + sa * L / 2)
    tail = (x - ca * L / 2, y - sa * L / 2)
    f.pl([tail, (x + px, y + py), (x - px, y - py)], MAG_D, 1.0, fill=MAG_L, close=True, tag="bg")
    f.pl([tip, (x + px, y + py), (x - px, y - py)], MAG_D, 1.0, fill=MAG_D, close=True, tag="bg")
    f.dot(x, y, 1.5, WHITE)


def bar(f, x, y, w, h, n="right", fs=14, lab=True):
    """Ímã de barra horizontal (canto superior esquerdo em x, y). Metade N roxo escuro; metade S roxo claro."""
    half = w / 2
    sx = x if n == "right" else x + half
    nx = x + half if n == "right" else x
    f.rect(sx, y, half, h, MAG_L, MAG_D, 1.8, tag="bg")
    f.rect(nx, y, half, h, MAG_D, MAG_D, 1.8, tag="bg")
    if lab:
        f.tb(sx + half / 2, y + h / 2, "S", size=fs, c=MAG_D, weight=700, lint=False)
        f.tb(nx + half / 2, y + h / 2, "N", size=fs, c=WHITE, weight=700, lint=False)


def dip_B(px, py, poles):
    """Direção do campo de um conjunto de ‘polos’ [(x, y, q)] (modelo de dois polos; q>0 = N)."""
    ex = ey = 0.0
    for cx, cy, q in poles:
        dx, dy = px - cx, py - cy
        r2 = dx * dx + dy * dy + 1e-9
        r3 = r2 * math.sqrt(r2)
        ex += q * dx / r3
        ey += q * dy / r3
    return ex, ey


def Bmark(f, x, y, kind, r=4.6, c=MAG, w=1.2):
    """Marca ⊗ (entrando) ou ⊙ (saindo) para o campo B, sem preenchimento."""
    f.cross_dot(x, y, kind, r=r, c=c, w=w, fill="none")


def Bgrid(f, x0, y0, x1, y1, kind="in", dx=24, dy=24, r=4.6, c=MAG, op=None):
    y = y0
    while y <= y1 + 0.1:
        x = x0
        while x <= x1 + 0.1:
            Bmark(f, x, y, kind, r, c)
            x += dx
        y += dy


def lines_from_pole(f, poles, start_pole, angs, bounds, r0=6, c=MAG, w=1.5, arrows=(0.5,), stop_r=10, size=8.5):
    px, py, _ = start_pole
    out = []
    for a in angs:
        st = (px + r0 * math.cos(math.radians(a)), py + r0 * math.sin(math.radians(a)))
        pts = trace_field(poles, st, +1, 3.0, 1400, bounds, stop_r)
        f.pl(pts, c, w, tag="bg", op=0.95)
        for t in arrows:
            f.mid_head(pts, t, c, size, tag="bg")
        out.append(pts)
    return out


def closed_lines(f, poles, cx, cy, svals, bounds, c=MAG, w=1.5, t=0.5, size=8.5, stop_r=9):
    """Linhas de campo que cruzam a mediatriz dos polos a distância s (acima e abaixo): sempre fecham em N e S."""
    for s_ in svals:
        for sg in (-1, +1):
            st = (cx, cy + sg * s_)
            fw = trace_field(poles, st, +1, 2.5, 3000, bounds, stop_r)
            bw = trace_field(poles, st, -1, 2.5, 3000, bounds, stop_r)
            pts = bw[::-1] + fw[1:]
            f.pl(pts, c, w, tag="bg", op=0.95)
            f.mid_head(pts, t, c, size, tag="bg")


def bez(f, p0, p1, p2, p3, c=MAG, w=1.3, t=0.5, size=7.5, n=36, arrow=True):
    pts = []
    for k in range(n + 1):
        u = k / n
        a, b, cc, d = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u ** 2, u ** 3
        pts.append((a * p0[0] + b * p1[0] + cc * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + cc * p2[1] + d * p3[1]))
    f.pl(pts, c, w, tag="bg", op=0.95)
    if arrow:
        f.mid_head(pts, t, c, size, tag="bg")
    return pts


# ───────────────────────── 4.1 ímãs e campo ─────────────────────────
@fig("ima_barra")
def ima_barra():
    f = Fig(332, 208, title="Ímã de barra: linhas de campo e agulhas de bússola")
    cx, cy, w, h = 166, 102, 124, 32
    xS, xN = cx - w / 2, cx + w / 2
    poles = [(xN - 14, cy, +1), (xS + 14, cy, -1)]
    bounds = (3, 3, 329, 205)
    closed_lines(f, poles, cx, cy, (19, 33, 51, 68), bounds, c=MAG, w=1.5, t=0.5)
    f.arrow(xN + 8, cy, xN + 34, cy, MAG, 1.5, 8)
    f.arrow(xS - 38, cy, xS - 8, cy, MAG, 1.5, 8)
    bar(f, xS, cy - h / 2, w, h, n="right", fs=16)
    for dy in (-10.5, 10.5):
        f.line(xS + 9, cy + dy, cx, cy + dy, MAG_D, 1.5, tag="bg")
        f.mid_head([(xS + 9, cy + dy), (cx, cy + dy)], 0.55, MAG_D, 7.5, tag="bg")
        f.line(cx, cy + dy, xN - 9, cy + dy, WHITE, 1.5, tag="bg")
        f.mid_head([(cx, cy + dy), (xN - 9, cy + dy)], 0.45, WHITE, 7.5, tag="bg")
    for (px_, py_) in ((cx, cy - 51), (cx, cy + 51), (xN + 54, cy), (xS - 54, cy)):
        ex, ey = dip_B(px_, py_, poles)
        needle(f, px_, py_, math.atan2(ey, ex))
    f.text(166, 14, "fora do ímã: as linhas de $\\vec B$ vão de N para S", 11, INK, weight=600)
    f.text(166, 187, "dentro do ímã: de S para N — as linhas são fechadas", 11, INK, weight=600)
    f.text(166, 201, "agulha de bússola: a ponta escura (N) aponta no sentido de $\\vec B$", 9.5, MUTED)
    return f


@fig("dois_imas")
def dois_imas():
    f = Fig(332, 206, title="Dois ímãs: polos diferentes se atraem; polos iguais se repelem")
    W, Hh, gap = 76, 20, 36
    xa = 14
    xb = xa + W + gap
    for row, (n2, titulo, sub, sgn) in enumerate((("right", "atração", "N diante de S", +1),
                                                 ("left", "repulsão", "N diante de N", -1))):
        cy = 70 + row * 90
        if sgn > 0:
            for d in (-6, 0, 6):
                f.arrow(xa + W, cy + d, xb, cy + d, MAG, 1.3, 7)
            for sg in (-1, +1):
                bez(f, (xa + W, cy + sg * 9), (xa + W + 20, cy + sg * 26), (xb - 20, cy + sg * 26), (xb, cy + sg * 9))
                bez(f, (xb + W, cy + sg * 7), (xb + W + 44, cy + sg * 46), (xa - 44, cy + sg * 46), (xa, cy + sg * 7))
        else:
            for sg in (-1, +1):
                bez(f, (xa + W, cy + sg * 7), (xa + W + 22, cy + sg * 46), (xa - 22, cy + sg * 46), (xa, cy + sg * 7))
                bez(f, (xb, cy + sg * 7), (xb - 22, cy + sg * 46), (xb + W + 22, cy + sg * 46), (xb + W, cy + sg * 7))
        bar(f, xa, cy - Hh / 2, W, Hh, n="right", fs=12)
        bar(f, xb, cy - Hh / 2, W, Hh, n=n2, fs=12)
        ya = cy - (42 if sgn > 0 else 40)
        if sgn > 0:
            f.arrow(xa + W - 30, ya, xa + W + 8, ya, INK, 2.8, 10)
            f.arrow(xb + 30, ya, xb - 8, ya, INK, 2.8, 10)
        else:
            f.arrow(xa + W - 6, ya, xa + W - 44, ya, INK, 2.8, 10)
            f.arrow(xb + 6, ya, xb + 44, ya, INK, 2.8, 10)
        f.text(xa + W - 19 if sgn > 0 else xa + W - 25, ya - 7, "$\\vec F$", 11.5, INK, halo=True)
        f.text(xb + 19 if sgn > 0 else xb + 25, ya - 7, "$\\vec F$", 11.5, INK, halo=True)
        f.text(274, cy - 4, titulo, 13, INK, weight=700)
        f.text(274, cy + 12, sub, 10.5, MUTED)
    return f


@fig("ima_cortado")
def ima_cortado():
    f = Fig(332, 168, title="Partir um ímã: cada pedaço é um ímã completo, com N e S")
    X0, W = 96, 200
    rows = [(1, 22, "1 ímã"), (2, 66, "2 ímãs"), (4, 110, "4 ímãs")]
    for n, y, lab in rows:
        pw = (W - (n - 1) * 3) / n
        for k in range(n):
            bar(f, X0 + k * (pw + 3), y, pw, 24, n="right", fs=11 if n < 4 else 10)
        f.text(X0 - 12, y + 16.5, lab, 11, INK, anchor="end", weight=600)
    for y in (50, 94):
        f.line(X0 - 2, y, X0 + W + 2, y, GRY, 1.4, dash="5 4", tag="bg")
        f.text(X0 + W + 8, y + 4, "corte", 10, MUTED, anchor="start")
    f.text(166, 152, "nunca se obtém um polo N (ou S) isolado", 11, INK, weight=600)
    f.text(166, 12, "partir um ímã não separa os polos:", 10.5, MUTED)
    return f


@fig("dominios")
def dominios():
    f = Fig(332, 168, title="Domínios magnéticos: ferro não imantado e ímã")
    rnd = random.Random(7)
    def block(x0, y0, w, h, aligned, title):
        cols, rows = 4, 3
        cw, ch = w / cols, h / rows
        f.rect(x0, y0, w, h, SOFT, GRY, 1.6, rx=4, tag="bg")
        for r in range(rows):
            for c in range(cols):
                cx, cy = x0 + cw * (c + 0.5), y0 + ch * (r + 0.5)
                f.rect(x0 + c * cw + 1.5, y0 + r * ch + 1.5, cw - 3, ch - 3, WHITE, GRY_L, 0.8, rx=2, tag="bg")
                ang = 0.0 if aligned else rnd.uniform(0, 2 * math.pi)
                L = 17
                f.arrow(cx - L * math.cos(ang) / 2, cy + L * math.sin(ang) / 2, cx + L * math.cos(ang) / 2,
                        cy - L * math.sin(ang) / 2, MAG, 2.0, 7.5, 0.4)
        f.text(x0 + w / 2, y0 + h + 17, title, 11, INK, weight=600)
    block(14, 30, 124, 84, False, "ferro comum")
    block(196, 30, 124, 84, True, "ferro imantado")
    f.arrow(146, 72, 188, 72, INK, 2.2, 9)
    f.text(167, 62, "imantar", 10.5, INK, weight=600, halo=True)
    f.text(76, 15, "domínios em desordem", 10.5, MUTED)
    f.text(258, 15, "domínios alinhados", 10.5, MUTED)
    f.text(76, 150, "efeitos se cancelam", 10.5, MUTED)
    f.text(258, 150, "campo resultante forte", 10.5, MUTED)
    return f


@fig("terra_B")
def terra_B():
    f = Fig(332, 206, title="Campo magnético da Terra: um dipolo levemente inclinado em relação ao eixo de rotação")
    cx, cy, R = 166, 90, 40
    tau = math.radians(11)
    n = (math.sin(tau), -math.cos(tau))        # sentido ‘norte’ do eixo magnético (tela)
    p = (math.cos(tau), math.sin(tau))

    def pt(r, th, side=1):
        return (cx + r * (math.cos(th) * n[0] + side * math.sin(th) * p[0]),
                cy + r * (math.cos(th) * n[1] + side * math.sin(th) * p[1]))
    for Lsh in (1.9, 2.5, 3.1, 3.8):
        th0 = math.asin(1 / math.sqrt(Lsh))
        for side in (+1, -1):
            pts = [pt(Lsh * R * math.sin(th) ** 2, th, side)
                   for th in [math.pi - th0 + (2 * th0 - math.pi) * k / 90 for k in range(91)]]
            f.pl(pts, MAG, 1.5, tag="bg", op=0.95)
            f.mid_head(pts, 0.5, MAG, 8.5, tag="bg")
    # globo
    f.circ(cx, cy, R, GRY_XL, GRY, 1.8, tag="bg")
    f.ell(cx, cy, R, R * 0.26, "none", GRY_M, 0.9, tag="bg")
    f.ell(cx, cy, R * 0.34, R, "none", GRY_M, 0.9, tag="bg")
    # eixos
    f.line(cx, cy - R - 20, cx, cy + R + 20, GRY, 1.3, dash="5 4", tag="bg")
    a1, a2 = pt(R + 20, 0), pt(R + 20, math.pi)
    f.line(a1[0], a1[1], a2[0], a2[1], MAG_D, 1.3, dash="5 4", tag="bg")
    # ímã interno (S em cima, N embaixo)
    s0, s1, n1 = pt(26, 0), pt(0, 0), pt(26, math.pi)
    def quad(a, b, hw, fill, c):
        dxp, dyp = p[0] * hw, p[1] * hw
        f.pl([(a[0] + dxp, a[1] + dyp), (b[0] + dxp, b[1] + dyp), (b[0] - dxp, b[1] - dyp), (a[0] - dxp, a[1] - dyp)],
             c, 1.3, fill=fill, close=True, tag="bg")
    quad(s0, s1, 6.5, MAG_L, MAG_D)
    quad(s1, n1, 6.5, MAG_D, MAG_D)
    ts = pt(15, 0)
    tn = pt(15, math.pi)
    f.tb(ts[0], ts[1], "S", size=10, c=MAG_D, weight=700, lint=False)
    f.tb(tn[0], tn[1], "N", size=10, c=WHITE, weight=700, lint=False)
    # agulhas de bússola na superfície
    for th in (math.radians(90), math.radians(52), math.radians(22)):
        x, y = pt(R + 12, th, +1)
        rx, ry = x - cx, y - cy
        rr = math.hypot(rx, ry)
        ux, uy = rx / rr, ry / rr
        mx, my = -n[0], -n[1]                       # momento de dipolo: do N geográfico para o S
        d = ux * mx + uy * my
        bx, by = 3 * d * ux - mx, 3 * d * uy - my
        needle(f, x, y, math.atan2(by, bx), L=20, w=6)
    # rótulos
    f.text(cx - 5, cy - R - 24, "N geog.", 10.5, GRY, anchor="end", weight=600)
    f.text(cx + 8, cy + R + 30, "S geog.", 10.5, GRY, anchor="start", weight=600)
    t0, t1 = pt(R + 20, 0), pt(R + 20, math.pi)
    f.text(t0[0] + 7, t0[1] - 5, "polo SUL magnético", 10.5, MAG_D, anchor="start", weight=600)
    f.text(t1[0] - 7, t1[1] + 14, "polo NORTE magnético", 10.5, MAG_D, anchor="end", weight=600)
    f.text(166, 200, "eixo magnético ≈ 11° do eixo de rotação (valor aproximado, varia com o tempo)", 9.5, MUTED)
    return f


# ───────────────────────── 4.2 campo de correntes ─────────────────────────
@fig("fio_B")
def fio_B():
    f = Fig(332, 212, title="Campo magnético de um fio retilíneo longo: linhas circulares e regra da mão direita")
    wx = 74
    ry = 10.5
    for yy, rx in ((62, 28), (108, 28), (154, 28)):
        back = [(wx + rx * math.cos(math.radians(a)), yy - ry * math.sin(math.radians(a))) for a in range(180, -1, -6)]
        f.pl(back, MAG, 1.3, tag="bg", op=0.45)
        f.mid_head(back, 0.5, MAG, 7.5, tag="bg")      # arco de trás: da direita para a esquerda
    f.rect(wx - 6, 28, 12, 164, GRY_L, GRY, 1.4, tag="bg")
    f.arrow(wx, 184, wx, 40, CUR, 3.0, 12, 0.42)
    for yy, rx in ((62, 28), (108, 28), (154, 28)):
        # arco da frente (parte de baixo da elipse): da esquerda para a direita
        front = [(wx - rx * math.cos(math.radians(t)), yy + ry * math.sin(math.radians(t))) for t in range(0, 181, 6)]
        f.pl(front, MAG, 2.0, tag="bg")
        f.mid_head(front, 0.5, MAG, 9.5, tag="bg")
    f.text(wx + 10, 30, "$I$", 13, CUR_D, anchor="start", weight=600, halo=True)
    f.text(wx + 42, 124, "$\\vec B$", 13, MAG_D, anchor="start", weight=700, halo=True)
    # vistas de cima
    def topo(cx, cy, kind, titulo, sub):
        ccw = kind == "out"
        for r in (14, 26, 38):
            f.circ(cx, cy, r, "none", MAG, 1.4, tag="bg")
            a0 = 40 if ccw else 140
            pts = [(cx + r * math.cos(math.radians(a0 + (30 if ccw else -30) * k / 8)),
                    cy - r * math.sin(math.radians(a0 + (30 if ccw else -30) * k / 8))) for k in range(9)]
            f.mid_head(pts, 0.5, MAG, 8.5, tag="bg")
        for phi in (70, 250):
            x, y = cx + 26 * math.cos(math.radians(phi)), cy - 26 * math.sin(math.radians(phi))
            tx, ty = (-math.sin(math.radians(phi)), -math.cos(math.radians(phi)))
            if not ccw:
                tx, ty = -tx, -ty
            needle(f, x, y, math.atan2(ty, tx), L=15, w=5.0)
        f.cross_dot(cx, cy, kind, r=7.5, c=CUR_D, w=1.9, fill=WHITE)
        f.text(cx, cy - 47, titulo, 11, CUR_D, weight=700)
        f.text(cx, cy + 56, sub, 10.5, MAG_D, weight=600)
    topo(214, 104, "out", "$I$ saindo ⊙", "$\\vec B$ anti-horário")
    topo(292, 104, "in", "$I$ entrando ⊗", "$\\vec B$ horário")
    f.text(214, 22, "vistas de cima", 10.5, MUTED, anchor="start")
    f.text(176, 205, "polegar no sentido de $I$; os dedos “abraçam” o fio no sentido de $\\vec B$", 10.5, INK, weight=600,
           anchor="middle")
    return f


@fig("espira_B")
def espira_B():
    f = Fig(332, 196, title="Campo magnético de uma espira: vista em perspectiva e corte lateral")
    # (a) perspectiva: anel vertical, eixo horizontal
    cx, cy, rx, ry = 80, 90, 17, 44
    back = [(cx - rx * math.sin(math.radians(t)), cy - ry * math.cos(math.radians(t))) for t in range(0, 181, 6)]
    front = [(cx + rx * math.sin(math.radians(t)), cy - ry * math.cos(math.radians(t))) for t in range(0, 181, 6)]
    f.pl(back, CUR_D, 1.8, dash="4 3", op=0.7, tag="bg")
    f.pl(front, CUR, 3.0, tag="bg")
    f.mid_head(front, 0.5, CUR, 11, hw=0.42, tag="bg")          # arco da frente: corrente para baixo
    # linhas de B que atravessam o anel (acima e abaixo do eixo) e voltam por fora
    for sgn in (-1, +1):
        ccy = cy + sgn * ry
        pts = [(cx + 46 * math.cos(math.radians(t)), ccy + sgn * 0 + 24 * math.sin(math.radians(t))) for t in range(0, 361, 6)]
        seq = pts[::-1] if sgn < 0 else pts          # em torno de ⊙ (cima): anti-horário; em torno de ⊗ (baixo): horário
        f.pl(pts, MAG, 1.4, tag="bg", op=0.9)
        f.mid_head(seq, 0.25, MAG, 8, tag="bg")
        f.mid_head(seq, 0.75, MAG, 8, tag="bg")
    f.arrow(26, cy, 138, cy, MAG, 2.4, 10)
    f.text(126, cy - 8, "$\\vec B$", 12.5, MAG_D, anchor="middle", weight=700, halo=True)
    f.text(cx + 27, cy - 14, "N", 12.5, MAG_D, weight=700, halo=True)
    f.text(cx - 27, cy - 14, "S", 12.5, MAG_D, weight=700, halo=True)
    f.text(cx + rx + 12, cy + 38, "$I$", 12.5, CUR_D, weight=700, halo=True)
    f.text(cx, 188, "perspectiva: face N à direita", 10, MUTED)
    # (b) corte lateral: duas seções do fio, ⊙ (em cima) e ⊗ (embaixo)
    ox, oy, a = 252, 92, 30
    f.line(178, 14, 178, 178, RULE, 1.0, dash="3 4", tag="bg")
    for lam in (0.30, 0.46):
        fac = (1 + lam * lam) / (1 - lam * lam)
        Rr = 2 * a * lam / (1 - lam * lam)
        cyt, cyb = oy - a * fac, oy + a * fac
        f.circ(ox, cyt, Rr, "none", MAG, 1.4, tag="bg")
        f.circ(ox, cyb, Rr, "none", MAG, 1.4, tag="bg")
        f.head(ox + 3, cyt + Rr, 0, MAG, 8.5, 0.42, "bg")            # em torno de ⊙: anti-horário
        f.head(ox - 3, cyt - Rr, math.pi, MAG, 8.5, 0.42, "bg")
        f.head(ox + 3, cyb - Rr, 0, MAG, 8.5, 0.42, "bg")            # em torno de ⊗: horário
        f.head(ox - 3, cyb + Rr, math.pi, MAG, 8.5, 0.42, "bg")
    f.arrow(ox - 54, oy, ox + 54, oy, MAG, 2.4, 10)
    f.cross_dot(ox, oy - a, "out", r=8, c=CUR_D, w=1.9, fill=WHITE)
    f.cross_dot(ox, oy + a, "in", r=8, c=CUR_D, w=1.9, fill=WHITE)
    f.text(ox + 56, oy - 8, "$\\vec B$", 12.5, MAG_D, anchor="end", weight=700, halo=True)
    f.text(ox - 8, 188, "corte lateral da espira", 10, MUTED)
    return f


@fig("solenoide_B")
def solenoide_B():
    f = Fig(332, 172, title="Campo magnético de um solenoide: interior uniforme e polos N e S nas extremidades")
    x0, x1, yt, yb = 96, 240, 62, 112
    n = 6
    pitch = (x1 - x0) / n
    yc = (yt + yb) / 2
    # linhas de retorno (por fora): saem do N (direita) e entram no S (esquerda)
    for hh, dx in ((46, 30), (27, 15)):
        for sg in (-1, +1):
            pts = [((x0 + x1) / 2 + ((x1 - x0) / 2 + dx) * math.cos(math.radians(t)),
                    yc + sg * (hh + 4) * math.sin(math.radians(t))) for t in range(0, 181, 5)]
            f.pl(pts, MAG, 1.4, tag="bg", op=0.9)
            f.mid_head(pts, 0.5, MAG, 8, tag="bg")
    # bobina: cilindro suave, espiras traseiras (fracas) e dianteiras
    f.rect(x0, yt, x1 - x0, yb - yt, SOFT, None, tag="bg")
    for k in range(n):
        xa = x0 + k * pitch
        f.line(xa + pitch * 0.5, yb, xa + pitch, yt, GRY_M, 1.3, dash="3 3", op=0.7, tag="bg")
    for k in range(n):
        xa = x0 + k * pitch
        f.line(xa, yt, xa + pitch * 0.5, yb, CUR, 2.8, tag="bg")
    for k in (1, 3, 5):
        xa = x0 + k * pitch
        f.mid_head([(xa, yt), (xa + pitch * 0.5, yb)], 0.55, CUR_D, 9.5, hw=0.45, tag="bg")
    # terminais
    f.line(64, yt, x0, yt, CUR, 2.8, tag="bg")
    f.arrow(64, yt, 84, yt, CUR_D, 2.8, 9)
    f.line(x1, yt, 276, yt, CUR, 2.8, tag="bg")
    f.arrow(x1 + 8, yt, x1 + 30, yt, CUR_D, 2.8, 9)
    f.text(70, yt - 8, "$I$", 12, CUR_D, anchor="middle", weight=700, halo=True)
    f.text(272, yt - 8, "$I$", 12, CUR_D, anchor="middle", weight=700, halo=True)
    # B interno uniforme
    for dy in (-9, 9):
        f.line(x0 + 6, yc + dy, x1 - 6, yc + dy, MAG_D, 1.8, tag="bg")
        f.mid_head([(x0 + 6, yc + dy), (x1 - 6, yc + dy)], 0.5, MAG_D, 9, tag="bg")
    f.rect(x1 + 12, yc - 11, 20, 22, MAG_D, MAG_D, 1, rx=3, tag="bg")
    f.text(x1 + 22, yc + 5, "N", 13, WHITE, weight=700, lint=False)
    f.rect(x0 - 32, yc - 11, 20, 22, MAG_L, MAG_D, 1.2, rx=3, tag="bg")
    f.text(x0 - 22, yc + 5, "S", 13, MAG_D, weight=700, lint=False)
    f.text(166, 13, "dentro: $\\vec B$ uniforme, $B=\\mu_0\\,n\\,I$ (solenoide longo)", 11, INK, weight=600)
    f.text(166, 166, "fora: campo fraco e disperso, como o de um ímã de barra", 10.5, MUTED)
    return f


@fig("fios_paralelos")
def fios_paralelos():
    f = Fig(332, 190, title="Força entre dois fios paralelos: mesmo sentido atrai, sentidos opostos repelem")

    def painel(cx, tipo, titulo, forca):
        d = 80
        x1, x2 = cx - d / 2, cx + d / 2
        y = 86
        k2 = "out" if tipo == "mesmo" else "in"
        for xc in (x1, x2):
            for r in (18, 31):
                f.circ(xc, y, r, "none", MAG, 1.1, tag="bg", op=0.6)
        # campo do fio 1 sobre o fio 2
        f.arrow(x2, y - 9, x2, y - 46, MAG_D, 2.6, 9)
        f.text(x2 + 7, y - 33, "$\\vec B_1$", 11.5, MAG_D, anchor="start", weight=600, halo=True)
        f.cross_dot(x1, y, "out", r=8, c=CUR_D, w=1.9, fill=WHITE)
        f.cross_dot(x2, y, k2, r=8, c=CUR_D, w=1.9, fill=WHITE)
        f.text(x1, y + 31, "$I_1$", 11.5, CUR_D, weight=700, halo=True)
        f.text(x2, y + 31, "$I_2$", 11.5, CUR_D, weight=700, halo=True)
        # forças sobre cada fio (no nível dos fios)
        if tipo == "mesmo":
            f.arrow(x1 + 11, y, x1 + 35, y, INK, 3.0, 10)
            f.arrow(x2 - 11, y, x2 - 35, y, INK, 3.0, 10)
            f.text(x1 + 23, y - 10, "$\\vec F_1$", 11, INK, weight=600, halo=True)
            f.text(x2 - 23, y - 10, "$\\vec F_2$", 11, INK, weight=600, halo=True)
        else:
            f.arrow(x1 - 11, y, x1 - 35, y, INK, 3.0, 10)
            f.arrow(x2 + 11, y, x2 + 35, y, INK, 3.0, 10)
            f.text(x1 - 23, y - 10, "$\\vec F_1$", 11, INK, weight=600, halo=True)
            f.text(x2 + 23, y - 10, "$\\vec F_2$", 11, INK, weight=600, halo=True)
        f.text(cx, y + 62, forca, 12, INK, weight=700)
        f.text(cx, 15, titulo, 11.5, INK, weight=700)
    painel(86, "mesmo", "mesmo sentido", "atração")
    painel(246, "oposto", "sentidos opostos", "repulsão")
    f.line(166, 4, 166, 156, RULE, 1.0, dash="3 4", tag="bg")
    f.text(166, 176, "$F/L=\\mu_0 I_1 I_2/(2\\pi d)$ — pares ação–reação: $F_1=F_2$", 11, INK, weight=600)
    return f


@fig("ex_fios_B")
def ex_fios_B():
    f = Fig(236, 214, title="Campo no ponto médio entre dois fios paralelos: correntes opostas somam, iguais se cancelam")

    def painel(y0, k2, titulo, b2_up, res):
        cx, d, y = 118, 128, y0 + 52
        x1, x2 = cx - d / 2, cx + d / 2
        for xc in (x1, x2):
            f.circ(xc, y, 32, "none", MAG, 1.0, tag="bg", op=0.5)
        f.cross_dot(x1, y, "out", r=8.5, c=CUR_D, w=2.0, fill=WHITE)
        f.cross_dot(x2, y, k2, r=8.5, c=CUR_D, w=2.0, fill=WHITE)
        f.dot(cx, y, 3.4, INK)
        f.text(cx, y + 19, "P", 12, INK, weight=700, halo=True)
        f.arrow(cx - 6, y - 4, cx - 6, y - 36, MAG_D, 2.8, 10)
        f.text(cx - 12, y - 24, "$\\vec B_1$", 11.5, MAG_D, anchor="end", weight=700, halo=True)
        if b2_up:
            f.arrow(cx + 6, y - 4, cx + 6, y - 36, MAG, 2.8, 10)
        else:
            f.arrow(cx + 6, y + 4, cx + 6, y + 36, MAG, 2.8, 10)
        f.text(cx + 12, y - 24 if b2_up else y + 30, "$\\vec B_2$", 11.5, MAG_D, anchor="start", weight=700, halo=True)
        f.text(x1, y - 16, "$I_1$ sai", 10.5, CUR_D, weight=600)
        f.text(x2, y - 16, "$I_2$ sai" if k2 == "out" else "$I_2$ entra", 10.5, CUR_D, weight=600)
        f.text(cx, y0 + 12, titulo, 11.5, INK, weight=700)
        f.text(cx, y0 + 98, res, 11.5, INK, weight=700)
    painel(0, "in", "correntes opostas", True, "$B=B_1+B_2=80$ µT")
    painel(110, "out", "mesmo sentido", False, "$B=B_1-B_2=0$")
    f.line(6, 108, 230, 108, RULE, 1.0, dash="3 4", tag="bg")
    return f
