"""Figuras do Módulo IV — Indução eletromagnética (Lenz, haste, gerador), transformador, transmissão, mapa."""
import math
from . import fig
from lib.circuit import *
from .f40a_magn import Bmark, bar
from .f90_maps import _node, _link


# ───────────────────────── Lenz em quatro quadros ─────────────────────────
def _ring(f, cx, cy, rx, ry, cur, sentido):
    """Anel visto em perspectiva: metade traseira (esquerda, tracejada) e dianteira (direita, cheia).
    cur=True: corrente; sentido='baixo'|'cima' é o sentido da corrente no arco dianteiro."""
    back = [(cx - rx * math.sin(math.radians(t)), cy - ry * math.cos(math.radians(t))) for t in range(0, 181, 6)]
    front = [(cx + rx * math.sin(math.radians(t)), cy - ry * math.cos(math.radians(t))) for t in range(0, 181, 6)]
    c = CUR if cur else GRY_M
    f.pl(back, CUR_D if cur else GRY_M, 1.8, dash="4 3", op=0.75, tag="bg")
    f.pl(front, c, 3.0, tag="bg")
    if cur:
        seq = front if sentido == "baixo" else front[::-1]
        f.mid_head(seq, 0.5, CUR, 11, hw=0.42, tag="bg")


@fig("lenz_paineis")
def lenz_paineis():
    f = Fig(680, 212, title="Lei de Lenz: ímã se aproximando, se afastando e parado diante de uma espira")
    panels = [
        ("(a) polo N se aproxima", "n", +1, "cima", "$\\Phi$ aumenta", "$\\vec B_{ind}$ oposto a $\\vec B_{ext}$",
         "anti-horário (visto do ímã)", "face N diante do N: repulsão", True, -1),
        ("(b) polo N se afasta", "n", -1, "baixo", "$\\Phi$ diminui", "$\\vec B_{ind}$ no mesmo sentido de $\\vec B_{ext}$",
         "horário (visto do ímã)", "face S diante do N: atração", True, +1),
        ("(c) polo S se aproxima", "s", +1, "baixo", "$|\\Phi|$ aumenta", "$\\vec B_{ind}$ oposto a $\\vec B_{ext}$",
         "horário (visto do ímã)", "face S diante do S: repulsão", True, +1),
        ("(d) ímã parado", "n", 0, None, "$\\Phi$ constante", "não há $\\vec B_{ind}$", "$I=0$ (mesmo com $B$ intenso)",
         "nenhuma força sobre o ímã", False, 0),
    ]
    for k, (tit, pol, mov, sent, l1, l2, l3, l4, cur, bdir) in enumerate(panels):
        x0 = k * 170
        f.rect(x0 + 3, 3, 164, 206, WHITE, RULE, 1.1, rx=6, tag="bg")
        f.text(x0 + 85, 17, tit, 11.5, INK, weight=700)
        # ímã
        mx0 = x0 + 12
        bar(f, mx0, 56, 70, 20, n="right" if pol == "n" else "left", fs=12)
        # anel
        rcx, rcy = x0 + 124, 66
        _ring(f, rcx, rcy, 11, 33, cur, sent)
        # movimento do ímã
        if mov != 0:
            if mov > 0:
                f.arrow(mx0 + 14, 42, mx0 + 52, 42, INK, 2.6, 9)
            else:
                f.arrow(mx0 + 52, 42, mx0 + 14, 42, INK, 2.6, 9)
            f.text(mx0 + 33, 36, "$\\vec v$", 11.5, INK, weight=700, halo=True)
        else:
            f.text(mx0 + 35, 42, "$v=0$", 11, INK, weight=700, halo=True)
        # B externo (sempre aponta ao longo do eixo; N à direita → para a direita; S à direita → para a esquerda)
        bext = +1 if pol == "n" else -1
        ya = 118
        if bext > 0:
            f.arrow(x0 + 18, ya, x0 + 50, ya, MAG, 2.8, 10)
        else:
            f.arrow(x0 + 50, ya, x0 + 18, ya, MAG, 2.8, 10)
        f.text(x0 + 56, ya + 4, "$\\vec B_{ext}$", 11.5, MAG_D, anchor="start", weight=700)
        if cur:
            yb = 140
            if bdir > 0:
                f.arrow(x0 + 18, yb, x0 + 50, yb, MAG, 2.8, 10, dash="5 3")
            else:
                f.arrow(x0 + 50, yb, x0 + 18, yb, MAG, 2.8, 10, dash="5 3")
            f.text(x0 + 56, yb + 4, "$\\vec B_{ind}$", 11.5, MAG_D, anchor="start", weight=700)
        f.text(x0 + 85, 170, l1, 11.5, INK, weight=700)
        f.text(x0 + 85, 186, l3, 10.5, CUR_D if cur else MUTED, weight=600)
        f.text(x0 + 85, 201, l4, 10, MUTED)
    return f


# ───────────────────────── fluxo magnético ─────────────────────────
@fig("fluxo_geom")
def fluxo_geom():
    f = Fig(332, 154, title="Fluxo magnético através de uma espira em três orientações")
    for k, (th, tit, res) in enumerate(((0, "$\\theta=0^\\circ$", "$\\Phi=BA$ (máximo)"),
                                          (60, "$\\theta=60^\\circ$", "$\\Phi=BA/2$"),
                                          (90, "$\\theta=90^\\circ$", "$\\Phi=0$"))):
        x0 = k * 110
        f.rect(x0 + 3, 3, 104, 148, WHITE, RULE, 1.1, rx=6, tag="bg")
        cx, cy = x0 + 55, 66
        for yy in (20, 42, 90, 112):
            f.arrow(x0 + 10, yy, x0 + 100, yy, MAG, 1.7, 8)
        a = math.radians(th)
        ex, ey = -math.sin(a), -math.cos(a)             # direção do plano da espira (perpendicular à normal)
        L = 38
        f.line(cx - L * ex, cy - L * ey, cx + L * ex, cy + L * ey, GRY, 5.0, tag="bg")
        nx, ny = math.cos(a), -math.sin(a)
        f.arrow(cx, cy, cx + 28 * nx, cy + 28 * ny, INK, 2.4, 9)
        f.text(cx + 33 * nx + (4 if th < 90 else 8), cy + 33 * ny + (4 if th == 0 else 0), "$\\vec n$", 11.5, INK,
               anchor="start" if th < 90 else "middle", weight=700, halo=True)
        if th > 0:
            f.arc(cx, cy, 18, 0, th, GRY, 1.3)
            f.text(cx + 26, cy - 5 if th == 60 else cy - 16, "$\\theta$", 11, INK, anchor="start", weight=700, halo=True)
        f.dot(cx, cy, 2.4, INK)
        f.text(x0 + 55, 130, tit, 11.5, INK, weight=700)
        f.text(x0 + 55, 145, res, 11, INK, weight=600)
    return f


@fig("ex_bobina")
def ex_bobina():
    f = Fig(236, 142, title="Bobina em campo crescente: corrente induzida anti-horária")
    f.rect(3, 3, 230, 136, WHITE, RULE, 1.2, rx=6, tag="bg")
    cx, cy, r = 118, 72, 44
    for yy in (22, 52, 92, 122):
        for xx in (22, 62, 174, 214):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    for (xx, yy) in ((84, 30), (152, 30), (84, 116), (152, 116)):
        Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    f.circ(cx, cy, r, "none", CUR, 3.0, tag="bg")
    pts = [(cx + r * math.cos(math.radians(t)), cy - r * math.sin(math.radians(t))) for t in range(10, 80, 4)]
    f.mid_head(pts, 0.5, CUR, 11, hw=0.42, tag="bg")
    pts = [(cx + r * math.cos(math.radians(t)), cy - r * math.sin(math.radians(t))) for t in range(190, 260, 4)]
    f.mid_head(pts, 0.5, CUR, 11, hw=0.42, tag="bg")
    f.circ(cx, cy, 11, WHITE, MAG, 1.7, dash="3 2", tag="bg")
    f.dot(cx, cy, 3.2, MAG)
    f.text(cx, cy + 27, "$\\vec B_{ind}$ (⊙)", 10.5, MAG_D, weight=700, halo=True)
    f.text(cx + r + 6, cy - r + 6, "$I$", 12.5, CUR_D, anchor="start", weight=700, halo=True)
    f.text(14, 15, "$\\vec B$ cresce (⊗)", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    return f


# ───────────────────────── haste em trilhos ─────────────────────────
@fig("haste_trilhos")
def haste_trilhos():
    f = Circ(332, 206, title="Haste condutora em trilhos horizontais dentro de campo magnético")
    yT, yB, xL, xR, xr = 44, 152, 70, 292, 196
    for yy in (24, 98, 178):
        for xx in (110, 150, 232, 270):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    for yy in (62, 134):
        for xx in (232, 270):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    # trilhos e resistor
    f.wire([(xL, yT), (xR + 36, yT)], INK, 2.4)
    f.wire([(xL, yB), (xR + 36, yB)], INK, 2.4)
    f.res((xL, yT), (xL, yB), lab="w", name="$R$", length=50, ldx=-4)
    # haste
    f.line(xr, yT - 8, xr, yB + 8, GRY, 7, tag="bg")
    f.dot(xr, yT, 3.6, INK)
    f.dot(xr, yB, 3.6, INK)
    # corrente (anti-horária): sobe na haste, vai para a esquerda em cima, desce em R, volta para a direita embaixo
    f.iarr((xr, yB), (xr, yT), 0.5, "$I$", side="e", lc=CUR_D)
    f.iarr((xr, yT), (xL, yT), 0.55, None)
    f.iarr((xL, yB), (xr, yB), 0.5, None)
    f.arrow(xL, 90, xL, 108, CUR, 2.6, 10)
    # B induzido (⊙) no interior da espira
    f.circ(130, 98, 8.5, "none", MAG, 1.6, dash="3 2", tag="bg")
    f.dot(130, 98, 2.6, MAG)
    f.text(130, 128, "$\\vec B_{ind}$ ⊙", 10.5, MAG_D, weight=700, halo=True)
    # v e F
    f.arrow(xr + 8, 98, xr + 54, 98, GRY, 3.2, 12)
    f.text(xr + 40, 89, "$\\vec v$", 12.5, GRY, weight=700, halo=True)
    f.arrow(xr - 8, 98, xr - 48, 98, INK, 3.2, 12)
    f.text(xr - 29, 89, "$\\vec F_m$", 12, INK, weight=700, halo=True)
    # L
    f.arrow(xR + 22, yT, xR + 22, yB, GRY, 1.2, 6, 0.4, both=True)
    f.text(xR + 28, 100, "$L$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.text(14, 14, "$\\vec B$ entrando (⊗)", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    f.text(174, 196, "$\\varepsilon=B\\,L\\,v$,  $I=\\varepsilon/R$,  $F_m=B\\,I\\,L$ (freia a haste)", 10.5, INK, weight=600)
    return f


@fig("ex_haste_vert")
def ex_haste_vert():
    f = Circ(332, 232, title="Haste em trilhos verticais caindo em campo magnético horizontal (entrando no papel)")
    xL, xR, yT, yB, yr = 98, 234, 40, 214, 128
    for yy in (84, 170):
        for xx in (130, 202):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    for yy in (62, 118, 160, 196):
        for xx in (60, 272, 300):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    f.wire([(xL, yT), (xL, yB)], INK, 2.4)
    f.wire([(xR, yT), (xR, yB)], INK, 2.4)
    f.res((xL, yT), (xR, yT), lab="n", name="$R=0{,}50\\ \\Omega$", length=54)
    f.line(xL - 8, yr, xR + 8, yr, GRY, 7, tag="bg")
    f.dot(xL, yr, 3.6, INK)
    f.dot(xR, yr, 3.6, INK)
    # corrente (anti-horária): na haste vai para a direita, sobe à direita, esquerda em cima, desce à esquerda
    f.iarr((xL, yr), (xR, yr), 0.28, "$I$", side="s", lc=CUR_D, off=7)
    f.iarr((xR, yr), (xR, yT), 0.5, None)
    f.iarr((xR, yT), (xL, yT), 0.2, None)
    f.arrow(xL, 80, xL, 100, CUR, 2.6, 10)
    f.circ(166, 84, 8.5, "none", MAG, 1.6, dash="3 2", tag="bg")
    f.dot(166, 84, 2.6, MAG)
    f.text(166, 106, "$\\vec B_{ind}$ ⊙", 10.5, MAG_D, weight=700, halo=True)
    # forças
    f.arrow(166, yr + 6, 166, yr + 62, INK, 3.2, 12)
    f.text(176, yr + 52, "$m\\vec g$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.arrow(196, yr - 6, 196, yr - 46, INK, 3.2, 12)
    f.text(205, yr - 30, "$\\vec F_m$", 12, INK, anchor="start", weight=700, halo=True)
    f.arrow(xR + 24, yr - 14, xR + 24, yr + 22, GRY, 3.0, 11)
    f.text(xR + 31, yr + 8, "$\\vec v$", 12.5, GRY, anchor="start", weight=700, halo=True)
    f.text(14, 14, "$\\vec B$ entrando (⊗): $B=1{,}0$ T", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    f.text(14, 28, "$L=0{,}50$ m;  $m=25$ g", 10.5, INK, anchor="start", weight=600, halo=True)
    return f


# ───────────────────────── gerador de corrente alternada ─────────────────────────
@fig("gerador_ca")
def gerador_ca():
    f = Fig(332, 206, title="Espira girando em campo uniforme: fluxo e fem induzida em função do tempo")
    # esquerda: vista de topo (eixo de rotação perpendicular ao papel)
    f.rect(6, 52, 26, 100, MAG_D, MAG_D, 1.6, rx=3, tag="bg")
    f.text(19, 107, "N", 14, WHITE, weight=700, lint=False)
    f.rect(138, 52, 26, 100, MAG_L, MAG_D, 1.6, rx=3, tag="bg")
    f.text(151, 107, "S", 14, MAG_D, weight=700, lint=False)
    for yy in (68, 102, 136):
        f.arrow(36, yy, 134, yy, MAG, 1.6, 8)
    th = math.radians(50)
    cx, cy, a = 85, 102, 36
    # espira (vista de ponta): reta perpendicular à normal n
    ex, ey = -math.sin(th), math.cos(th)
    p1 = (cx - a * ex, cy + a * ey)
    p2 = (cx + a * ex, cy - a * ey)
    f.line(p1[0], p1[1], p2[0], p2[1], GRY, 4.0, tag="bg")
    f.circ(*p1, 7, WHITE, CUR_D, 1.9, tag="bg"); f.dot(*p1, 2.4, CUR_D)
    f.circ(*p2, 7, WHITE, CUR_D, 1.9, tag="bg")
    f.line(p2[0] - 3.6, p2[1] - 3.6, p2[0] + 3.6, p2[1] + 3.6, CUR_D, 1.7, tag="bg")
    f.line(p2[0] - 3.6, p2[1] + 3.6, p2[0] + 3.6, p2[1] - 3.6, CUR_D, 1.7, tag="bg")
    # normal e ângulo
    nx_, ny_ = math.cos(th), -math.sin(th)
    f.arrow(cx, cy, cx + 38 * nx_, cy + 38 * ny_, INK, 2.2, 9)
    f.text(cx + 46 * nx_ + 6, cy + 46 * ny_ - 2, "$\\vec n$", 12, INK, anchor="start", weight=700, halo=True)
    f.arc(cx, cy, 24, 0, 50, GRY, 1.4)
    f.text(cx + 32, cy - 6, "$\\theta$", 11.5, INK, anchor="start", weight=700, halo=True)
    f.dot(cx, cy, 2.6, INK)
    f.text(85, 40, "$\\Phi=B\\,A\\cos\\theta$,  $\\theta=\\omega t$", 11, INK, weight=600)
    f.text(85, 176, "vista de ponta da espira", 10, MUTED)
    f.text(85, 190, "($\\vec n$ ⟂ plano da espira)", 10, MUTED)
    # direita: gráfico
    gx0, gx1, gy0, gamp = 190, 322, 108, 54
    f.arrow(gx0, gy0, gx1 + 6, gy0, INK, 1.4, 7, 0.34)
    f.arrow(gx0, gy0 + gamp + 10, gx0, gy0 - gamp - 14, INK, 1.4, 7, 0.34)
    f.text(gx1 + 8, gy0 + 14, "$t$", 11.5, INK, anchor="end", weight=700, halo=True)
    T = gx1 - gx0 - 6
    for fr, lab in ((0.25, "T/4"), (0.5, "T/2"), (0.75, "3T/4"), (1.0, "T")):
        xx = gx0 + fr * T
        f.line(xx, gy0 - 3, xx, gy0 + 3, INK, 1.1)
        if lab in ("T/2", "T"):
            f.text(xx, gy0 + 15, lab, 9.5, MUTED, halo=True)
    pf = [(gx0 + T * u / 100, gy0 - gamp * math.cos(2 * math.pi * u / 100)) for u in range(101)]
    pe = [(gx0 + T * u / 100, gy0 - gamp * math.sin(2 * math.pi * u / 100)) for u in range(101)]
    f.pl(pf, MAG, 2.2, dash="6 4", tag="bg")
    f.pl(pe, INK, 2.4, tag="bg")
    f.text(gx0 + 4, gy0 - gamp - 14, "$\\Phi$", 12.5, MAG_D, anchor="start", weight=700, halo=True)
    f.text(gx0 + 0.25 * T + 8, gy0 - gamp - 2, "$\\varepsilon$", 12.5, INK, anchor="start", weight=700, halo=True)
    f.line(gx0 + 0.25 * T, gy0 - gamp, gx0 + 0.25 * T, gy0 + gamp + 6, GRY, 1.0, dash="3 3", tag="bg")
    f.text(gx0 + 0.25 * T, gy0 + gamp + 20, "$\\Phi=0$: $\\varepsilon$ máx", 10, INK, weight=600, halo=True)
    f.text(gx0 + 2, gy0 + gamp + 34, "$\\Phi$ máx: $\\varepsilon=0$", 10, MAG_D, anchor="start", weight=600, halo=True)
    f.text(255, 24, "$\\varepsilon=-\\Delta\\Phi/\\Delta t$", 11, INK, weight=600)
    f.text(255, 38, "$=N\\,B\\,A\\,\\omega\\,\\mathrm{sen}\\,\\omega t$", 11, INK, weight=600)
    return f


# ───────────────────────── transformador e transmissão ─────────────────────────
@fig("transformador")
def transformador():
    f = Circ(332, 186, title="Transformador ideal: dois enrolamentos em um núcleo de ferro")
    # núcleo
    f.rect(104, 28, 128, 120, "none", GRY, 2.0, tag="bg")
    f.rect(126, 50, 84, 76, "none", GRY, 2.0, tag="bg")
    f.rect(104, 28, 128, 22, GRY_XL, None, tag="bg")
    f.rect(104, 126, 128, 22, GRY_XL, None, tag="bg")
    f.rect(104, 50, 22, 76, GRY_XL, None, tag="bg")
    f.rect(210, 50, 22, 76, GRY_XL, None, tag="bg")
    f.rect(104, 28, 128, 120, "none", GRY, 2.0, tag="bg")
    f.rect(126, 50, 84, 76, "none", GRY, 2.0, tag="bg")
    # enrolamentos
    for k in range(7):
        y = 58 + k * 9
        f.line(98, y, 132, y + 5, CUR, 2.6, tag="bg")
        f.line(204, y, 238, y + 5, CUR, 2.6, tag="bg")
    f.text(88, 94, "$N_p$", 12.5, INK, anchor="end", weight=700, halo=True)
    f.text(246, 94, "$N_s$", 12.5, INK, anchor="start", weight=700, halo=True)
    # fluxo no núcleo
    f.rect(146, 70, 44, 36, "none", MAG, 2.0, tag="bg", dash="5 3")
    f.mid_head([(146, 70), (190, 70)], 0.5, MAG, 10, tag="bg")
    f.mid_head([(190, 106), (146, 106)], 0.5, MAG, 10, tag="bg")
    f.text(168, 92, "$\\Phi$", 13, MAG_D, weight=700, halo=True)
    f.text(168, 118, "(variável)", 9.5, MAG_D, weight=600)
    # fonte CA e carga
    f.circ(36, 90, 15, WHITE, INK, 2.0, tag="bg")
    f.path("M 27 90 C 31 80, 35 80, 36 90 S 41 100, 45 90", INK, 1.8)
    f.wire([(36, 75), (36, 58), (98, 58)], INK, 2.0)
    f.wire([(36, 105), (36, 122), (98, 90 + 36)], INK, 2.0)
    f.wire([(98, 58 + 9 * 6 + 5), (98, 126)], INK, 2.0)
    f.text(36, 140, "fonte CA", 10, MUTED)
    f.text(36, 153, "$V_p$,  $I_p$", 11, INK, weight=600)
    f.wire([(238, 58), (292, 58), (292, 72)], INK, 2.0)
    f.res((292, 72), (292, 124), lab="e", name="$R$", length=40)
    f.wire([(292, 124), (292, 126), (238, 126)], INK, 2.0)
    f.wire([(238, 58 + 9 * 6 + 5), (238, 126)], INK, 2.0)
    f.text(292, 153, "$V_s$,  $I_s$", 11, INK, weight=600)
    f.text(166, 14, "$V_s/V_p=N_s/N_p$  e  $V_pI_p=V_sI_s$ (ideal)", 11, INK, weight=700)
    f.text(166, 174, "só funciona com fluxo variável: corrente alternada", 10, MUTED)
    return f


def _trafo(f, cx, cy, h=54):
    """Símbolo simplificado de transformador (duas bobinas com núcleo)."""
    for sg in (-1, +1):
        for k in range(4):
            y0 = cy - h / 2 + k * h / 4
            pts = [(cx + sg * 7 + sg * 9 * math.sin(math.radians(t)), y0 + (h / 4) * t / 180) for t in range(0, 181, 15)]
            f.pl(pts, INK, 2.0, tag="bg")
    f.line(cx - 3, cy - h / 2, cx - 3, cy + h / 2, GRY, 2, tag="bg")
    f.line(cx + 3, cy - h / 2, cx + 3, cy + h / 2, GRY, 2, tag="bg")


@fig("transmissao")
def transmissao():
    f = Circ(680, 168, title="Transmissão de energia: eleva-se a tensão para reduzir a corrente e as perdas")
    yt, yb = 56, 112
    # usina
    f.rect(2, 40, 74, 88, SOFT, GRY, 1.6, rx=6, tag="bg")
    f.circ(39, 84, 17, WHITE, INK, 2.0, tag="bg")
    f.path("M 29 84 C 33 74, 37 74, 39 84 S 45 94, 49 84", INK, 1.8)
    f.text(39, 31, "usina", 11.5, INK, weight=700)
    f.text(39, 144, "$10$ MW", 10.5, MUTED)
    f.wire([(76, yt), (122, yt)], INK, 2.2)
    f.wire([(76, yb), (122, yb)], INK, 2.2)
    f.text(99, yt - 8, "10 kV", 10.5, INK, weight=600, halo=True)
    # trafo elevador
    _trafo(f, 152, 84)
    f.wire([(122, yt), (143, yt), (143, 60)], INK, 2.0)
    f.wire([(122, yb), (143, yb), (143, 108)], INK, 2.0)
    f.text(152, 31, "elevador", 11.5, INK, weight=700)
    f.text(152, 144, "$N_s/N_p=10$", 10.5, MUTED)
    # linha
    f.wire([(161, 60), (161, yt), (470, yt)], INK, 2.2)
    f.wire([(161, 108), (161, yb), (470, yb)], INK, 2.2)
    f.res((290, yt), (400, yt), lab="n", name="$R_{linha}=5\\ \\Omega$", length=56)
    f.iarr((180, yt), (250, yt), 0.5, "$I=100$ A", side="n", off=6)
    f.text(316, 144, "linha: $P_{perda}=R\\,I^2=50$ kW", 11, ENE_D, weight=700)
    f.text(316, 129, "(a $10$ kV seria $I=1000$ A e perda de $5$ MW)", 10.5, MUTED)
    f.text(250, 99, "100 kV", 10.5, INK, weight=600, halo=True)
    f.text(316, 31, "linha de transmissão", 11.5, INK, weight=700)
    # abaixador
    _trafo(f, 508, 84)
    f.wire([(470, yt), (499, yt), (499, 60)], INK, 2.0)
    f.wire([(470, yb), (499, yb), (499, 108)], INK, 2.0)
    f.text(508, 31, "abaixador", 11.5, INK, weight=700)
    f.wire([(517, 60), (517, yt), (560, yt)], INK, 2.2)
    f.wire([(517, 108), (517, yb), (560, yb)], INK, 2.2)
    # consumidores
    f.rect(560, 40, 118, 88, SOFT, GRY, 1.6, rx=6, tag="bg")
    f.text(619, 31, "consumidores", 11.5, INK, weight=700)
    f.text(619, 78, "127 V / 220 V", 12, INK, weight=700)
    f.text(619, 96, "casas, indústrias", 10.5, MUTED)
    return f


# ───────────────────────── mapa mental do Módulo IV ─────────────────────────
@fig("mapa_magn")
def mapa_magn():
    f = Fig(680, 232, title="Mapa mental do Magnetismo e do Eletromagnetismo")
    W, H = 168, 50
    xs = [0, 256, 512]
    y1, y2 = 6, 120
    _node(f, xs[0], y1, W, H, "Corrente $I$", "cargas em movimento", CUR, CUR_L)
    _node(f, xs[1], y1, W, H, "Campo magnético $\\vec B$", "linhas fechadas; T", MAG, MAG_L)
    _node(f, xs[2], y1, W, H, "Força magnética", "$\\vec F=q\\vec v\\times\\vec B$", INK, SOFT)
    _node(f, xs[0], y2, W, H, "Fluxo $\\Phi$ variável", "$\\Phi=BA\\cos\\theta$", MAG, MAG_L)
    _node(f, xs[1], y2, W, H, "Fem induzida", "$\\varepsilon=-N\\Delta\\Phi/\\Delta t$", ENE, ENE_L)
    _node(f, xs[2], y2, W, H, "Corrente induzida", "sentido: Lenz", CUR, CUR_L)
    m1, m2 = y1 + H / 2, y2 + H / 2
    _link(f, xs[0] + W + 4, m1, xs[1] - 4, m1, "Oersted, Ampère", "$B=\\mu_0I/(2\\pi r)$")
    _link(f, xs[1] + W + 4, m1, xs[2] - 4, m1, "carga ou fio", "$F=qvB\\,\\mathrm{sen}\\,\\theta$; $BIL$")
    _link(f, xs[0] + W + 4, m2, xs[1] - 4, m2, "Faraday", "$\\varepsilon\\propto\\Delta\\Phi/\\Delta t$")
    _link(f, xs[1] + W + 4, m2, xs[2] - 4, m2, "Ohm", "$I=\\varepsilon/R$")
    f.arrow(xs[2] + W / 2 - 30, y1 + H + 3, xs[2] + W / 2 - 30, y2 - 3, INK, 2.2, 10, 0.4)
    f.text(xs[2] + W / 2 - 38, y1 + H + 28, "motor: $I$ ⇒ $F$ ⇒ giro", 10.5, INK, anchor="end", weight=600, halo=True)
    f.arrow(xs[0] + W / 2, y2 - 3, xs[0] + W / 2, y1 + H + 3, INK, 2.2, 10, 0.4)
    f.text(xs[0] + W / 2 + 8, y1 + H + 28, "gerador: giro ⇒ $\\Phi$ varia", 10.5, INK, anchor="start", weight=600, halo=True)
    f.text(340, 207, "Lenz: o efeito induzido se opõe à VARIAÇÃO do fluxo — conservação da energia", 11.5, INK, weight=700)
    f.text(340, 224, "motor girando induz fcem (receptor);  transformador ideal: $V_s/V_p=N_s/N_p$ (só CA)", 10.5, MUTED)
    return f


@fig("fx_fluxo")
def fx_fluxo():
    f = Fig(236, 150, title="Gráfico do fluxo magnético em função do tempo")
    pl = Plot(f, 44, 118, 150, 84, (0, 0.65), (0, 7.2), xticks=[(0.2, "0,2"), (0.5, "0,5"), (0.6, "0,6")],
              yticks=[(6, "6")], grid=True)
    pl.line([(0, 0), (0.2, 6), (0.5, 6), (0.6, 0)], MAG, 2.6)
    pl.guide(x=0.2, y=6)
    pl.axis_labels("$t$ (s)", "$\\Phi$ (mWb)", ydx=2)
    return f


@fig("fx_espira_saindo")
def fx_espira_saindo():
    f = Fig(236, 132, title="Espira quadrada saindo de uma região de campo magnético")
    f.rect(8, 8, 96, 116, MAG_L, MAG, 1.2, rx=4, fop=0.45, tag="bg")
    for yy in (28, 64, 100):
        for xx in (26, 62, 90):
            Bmark(f, xx, yy, "in", 4.2, MAG, 1.0)
    x0, x1, y0, y1 = 56, 124, 34, 102
    f.rect(x0, y0, x1 - x0, y1 - y0, "none", INK, 2.6, tag="bg")
    f.arrow(x0, y1 - 10, x0, y0 + 10, CUR, 2.8, 10)
    f.text(x0 - 8, 70, "$I$", 12, CUR_D, anchor="end", weight=700, halo=True)
    f.arrow(x0 - 3, 42, x0 - 30, 42, INK, 3.0, 10)
    f.text(x0 - 36, 36, "$\\vec F_m$", 11.5, INK, anchor="end", weight=700, halo=True)
    f.arrow(x1 + 6, 68, x1 + 46, 68, GRY, 3.0, 11)
    f.text(x1 + 26, 60, "$\\vec v$", 12, GRY, weight=700, halo=True)
    f.text(14, 18, "$B$ (⊗)", 10.5, MAG_D, anchor="start", weight=700, halo=True)
    f.text(x0 + 34, 118, "$L=10$ cm", 10.5, INK, weight=600, halo=True)
    f.text(190, 112, "$R=0{,}20\\ \\Omega$", 10.5, INK, anchor="middle", weight=600)
    return f
