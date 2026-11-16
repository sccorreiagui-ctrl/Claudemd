"""Figuras do Módulo III — Eletrodinâmica (parte C: Kirchhoff, geradores, instrumentos, mapa)."""
import math
from . import fig
from lib.circuit import *

WW = 3.2


def pc(v, vmax):
    return pot_color(v, 0, vmax)


@fig("kirch_regras")
def kirch_regras():
    f = Circ(680, 232, title="Regras de Kirchhoff: lei dos nós e sinais na lei das malhas")
    # --- lei dos nós
    f.text(100, 14, "1ª lei — nós (carga)", 12.5, INK, weight=700)
    f.line(0, 22, 200, 22, RULE, 1, tag="bg")
    cx, cy = 100, 96
    f.wire([(18, cy), (cx, cy)])
    f.wire([(cx, 38), (cx, cy)])
    f.wire([(cx, cy), (182, cy)])
    f.wire([(cx, cy), (cx, 154)])
    f.node(cx, cy, INK, 5)
    f.arrow(24, cy - 12, 70, cy - 12, CUR, 2.8, 10)
    f.text(46, cy - 20, "$i_1$", 12.5, CUR_D, weight=600)
    f.arrow(cx + 14, 44, cx + 14, 76, CUR, 2.8, 10)
    f.text(cx + 24, 64, "$i_2$", 12.5, CUR_D, anchor="start", weight=600)
    f.arrow(128, cy - 12, 174, cy - 12, CUR, 2.8, 10)
    f.text(152, cy - 20, "$i_3$", 12.5, CUR_D, weight=600)
    f.arrow(cx + 14, 112, cx + 14, 148, CUR, 2.8, 10)
    f.text(cx + 24, 134, "$i_4$", 12.5, CUR_D, anchor="start", weight=600)
    f.text(100, 184, "$\\sum i_{entram}=\\sum i_{saem}$", 12, INK, weight=600)
    f.text(100, 202, "$i_1+i_2=i_3+i_4$", 12, INK)
    f.text(100, 220, "(a carga não se acumula no nó)", 10.5, MUTED)
    # --- lei das malhas: 4 casos
    f.text(450, 14, "2ª lei — malhas (energia): $\\sum\\Delta V=0$ ao percorrer a malha", 12.5, INK, weight=700)
    f.line(222, 22, 680, 22, RULE, 1, tag="bg")
    cells = [(222, 30, "res_fav"), (452, 30, "res_con"), (222, 128, "ger_up"), (452, 128, "ger_dn")]
    subs = {"res_fav": "a favor de $I$: o potencial cai", "res_con": "contra $I$: o potencial sobe",
            "ger_up": "de − para +: o potencial sobe", "ger_dn": "de + para −: o potencial cai"}
    for (ox, oy, kind) in cells:
        yc = oy + 38
        if kind.startswith("res"):
            f.res((ox + 8, yc), (ox + 124, yc), "$R$", lab="n", length=44, amp=7, gap=5)
            ci = (ox + 38, yc - 25, ox + 90, yc - 25) if kind == "res_fav" else (ox + 90, yc - 25, ox + 38, yc - 25)
            f.arrow(*ci, CUR, 2.4, 9)
            f.text(ox + 100, yc - 21, "$I$", 12, CUR_D, anchor="start", weight=600)
            txt = "$\\Delta V=-R\\,I$" if kind == "res_fav" else "$\\Delta V=+R\\,I$"
            ya = yc + 22
        else:
            f.bat((ox + 8, yc), (ox + 124, yc), pos="q", signs=False, lab="n", size=11)
            txt = "$\\Delta V=+\\varepsilon$" if kind == "ger_up" else "$\\Delta V=-\\varepsilon$"
            f.text(ox + 66 - 14, yc - 14, "−", 13, NEG_D, weight=700, lint=False)
            f.text(ox + 66 + 14, yc - 14, "+", 13, POS_D, weight=700, lint=False)
            ya = yc + 22
        if kind in ("res_fav", "res_con", "ger_up"):
            f.arrow(ox + 18, ya, ox + 114, ya, GRY, 2.0, 9, dash="6 4")
        else:
            f.arrow(ox + 114, ya, ox + 18, ya, GRY, 2.0, 9, dash="6 4")
        f.text(ox + 66, ya + 15, "percurso", 10.5, GRY)
        f.text(ox + 176, yc + 4, txt, 13, INK, weight=600)
        f.text(ox + 176, yc + 24, subs[kind], 10, MUTED, lint=False)
    return f


@fig("k1")
def k1():
    f = Circ(332, 250, title="Exemplo 20: malha única com dois geradores")
    TL, TR, BR, BL = (58, 48), (282, 48), (282, 190), (58, 190)
    f.bat(BL, TL, pos="q", lab="w", name="$\\varepsilon_1$", val="12 V", signs=True, size=11.5)
    f.wire([TL, (96, 48)])
    f.res((96, 48), (214, 48), "$R_1$", "2 Ω", lab="n")
    f.wire([(214, 48), TR, (282, 70)])
    f.bat((282, 70), (282, 118), pos="p", lab="e", name="$\\varepsilon_2$", val="4 V", signs=True, size=11.5)
    f.res((282, 118), (282, 188), "$R_3$", "2 Ω", lab="w", length=44)
    f.wire([(282, 188), BR, (214, 190)])
    f.res((214, 190), (96, 190), "$R_2$", "4 Ω", lab="s")
    f.wire([(96, 190), BL])
    f.loop_arrow(170, 120, 52, 40, 30, 330, GRY, 2.0, ccw=False)
    f.text(170, 124, "percurso", 11, GRY, lint=False)
    f.text(170, 138, "e $I$ (supostos)", 11, GRY, lint=False)
    f.iarr((214, 48), (260, 48), 0.5, "$I$", length=22, off=7)
    f.text(166, 230, "$\\varepsilon_1$ eleva 12 V; $\\varepsilon_2$ (oposto) reduz 4 V", 11, MUTED)
    return f


@fig("k2")
def k2():
    f = Circ(332, 262, title="Exemplo 21: duas malhas com resistor compartilhado")
    xL, xM, xR, yt, yb = 56, 176, 296, 46, 214
    f.bat((xL, yb), (xL, 140), pos="q", lab="w", name="$\\varepsilon$", val="18 V", signs=True, size=11)
    f.res((xL, 140), (xL, yt), "$R_1$", "1 Ω", lab="w", length=44, stack=True)
    f.wire([(xL, yt), (xR, yt)])
    f.wire([(xL, yb), (xR, yb)])
    f.res((xM, yt), (xM, yb), "$R_2$", "6 Ω", lab="e", length=50, stack=True)
    f.res((xR, yt), (xR, yb), "$R_3$", "3 Ω", lab="e", length=50, stack=True)
    for (x, y) in ((xM, yt), (xM, yb)):
        f.node(x, y, INK, 4.2)
    f.iarr((xL, yt), (xM - 40, yt), 0.5, "$I_1$", length=22, off=7)
    f.iarr((xM, 66), (xM, 100), 0.5, "$I_2$", length=20, side="w", off=8)
    f.iarr((xR, 66), (xR, 100), 0.5, "$I_3$", length=20, side="w", off=8)
    f.loop_arrow((xL + xM) / 2 + 2, 130, 28, 36, 30, 330, GRY, 1.8, ccw=False)
    f.loop_arrow((xM + xR) / 2 + 12, 130, 24, 36, 30, 330, GRY, 1.8, ccw=False)
    f.text((xL + xM) / 2 + 2, 135, "α", 13, GRY, lint=False)
    f.text((xM + xR) / 2 + 12, 135, "β", 13, GRY, lint=False)
    f.text(166, 244, "$I_1=I_2+I_3$ (nó superior)", 11.5, INK)
    f.text(166, 258, "malhas α e β percorridas no sentido horário", 10.5, MUTED)
    return f


@fig("k3")
def k3():
    f = Circ(332, 262, title="Exemplo 22: dois geradores em ramos diferentes (uma corrente é negativa)")
    xL, xM, xR, yt, yb = 56, 176, 296, 46, 214
    f.bat((xL, yb), (xL, 140), pos="q", lab="w", name="$\\varepsilon_1$", val="6 V", signs=True, size=11)
    f.res((xL, 140), (xL, yt), "$R_1$", "1 Ω", lab="e", length=44)
    f.bat((xR, yb), (xR, 140), pos="q", lab="e", name="$\\varepsilon_2$", val="2 V", signs=True, size=11)
    f.res((xR, 140), (xR, yt), "$R_2$", "2 Ω", lab="w", length=44)
    f.wire([(xL, yt), (xR, yt)])
    f.wire([(xL, yb), (xR, yb)])
    f.res((xM, yt), (xM, yb), "$R_3$", "4 Ω", lab="e", length=50)
    for (x, y) in ((xM, yt), (xM, yb)):
        f.node(x, y, INK, 4.2)
    f.iarr((xL, yt), (xM - 36, yt), 0.5, "$I_1$", length=22, off=7)
    f.iarr((xR, yt), (xM + 36, yt), 0.5, "$I_2$", length=22, off=7)
    f.iarr((xM, 66), (xM, 100), 0.5, "$I_3$", length=20, side="w", off=8)
    f.text(166, 244, "sentidos de $I_1$, $I_2$, $I_3$ escolhidos livremente", 11.5, INK)
    f.text(166, 258, "o sinal do resultado dirá se a escolha estava certa", 10.5, MUTED)
    return f


@fig("ger_circ")
def ger_circ():
    f = Circ(332, 214, title="Gerador real: fem em série com resistência interna, ligado a uma carga")
    f.rect(26, 40, 162, 114, "none", GRY, 1.6, dash="6 4", tag="bg")
    f.text(107, 34, "gerador real", 11.5, GRY, weight=600, lint=False)
    f.bat((56, 140), (56, 70), pos="q", lab="w", name="$\\varepsilon$", signs=True, size=11.5)
    f.wire([(56, 70), (74, 70)])
    f.res((74, 70), (170, 70), "$r$", lab="n", length=46)
    f.wire([(56, 140), (188, 140)])
    f.wire([(170, 70), (188, 70)])
    f.circ(188, 70, 3.8, "#fff", INK, 1.9, tag="bg")
    f.circ(188, 140, 3.8, "#fff", INK, 1.9, tag="bg")
    f.text(200, 66, "A", 12.5, INK, anchor="start", weight=700)
    f.text(200, 156, "B", 12.5, INK, anchor="start", weight=700)
    f.wire([(188, 70), (290, 70)])
    f.wire([(188, 140), (290, 140)])
    f.res((290, 70), (290, 140), "$R$", lab="w", length=44)
    f.iarr((214, 70), (262, 70), 0.5, "$I$", length=22, off=7)
    f.arrow(226, 140 - 12, 226, 70 + 12, GRY, 1.2, 7, 0.4)
    f.text(236, 108, "$U$", 12.5, INK, anchor="start")
    f.text(166, 182, "$U=\\varepsilon-r\\,I$  (tensão nos terminais)", 12, INK, weight=600)
    f.text(166, 202, "$I=\\varepsilon/(R+r)$ com carga $R$", 11.5, INK)
    return f


@fig("ger_graf")
def ger_graf():
    f = Fig(680, 226, title="Curvas características de um gerador e de um receptor")
    f.text(165, 14, "Gerador: $U=\\varepsilon-rI$", 12.5, INK, weight=700)
    P = Plot(f, 52, 176, 250, 124, (0, 26), (0, 13.5), xticks=[(6, "6"), (12, "12"), (18, "18"), (24, "24")],
             yticks=[(4, "4"), (8, "8"), (12, "12")], grid=True)
    P.axis_labels("$I$ (A)", "$U$ (V)", ydx=4)
    P.line([(0, 12), (24, 0)], INK, 2.8)
    P.guide(x=2, y=11, c=GRY_M)
    P.point(2, 11, ENE_D, 4.2, "#fff")
    f.text(P.X(2.6), P.Y(11) - 9, "operação: 2 A e 11 V", 11, ENE_D, anchor="start", weight=600, halo=True)
    f.text(P.X(11), P.Y(10.3), "$I=0$: $U=\\varepsilon=12$ V", 11, INK, anchor="start", halo=True)
    f.text(P.X(11), P.Y(8.6), "$U=0$: $I_{cc}=\\varepsilon/r=24$ A", 11, INK, anchor="start", halo=True)
    f.text(P.X(11), P.Y(6.9), "inclinação $=-r=-0{,}5\\ \\Omega$", 11, MUTED, anchor="start", halo=True)
    f.text(515, 14, "Receptor: $U=\\varepsilon'+r'I$", 12.5, INK, weight=700)
    Q = Plot(f, 402, 176, 230, 124, (0, 7), (0, 13.5), xticks=[(2, "2"), (4, "4"), (6, "6")],
             yticks=[(4, "4"), (8, "8"), (12, "12")], grid=True)
    Q.axis_labels("$I$ (A)", "$U$ (V)", ydx=4)
    Q.line([(0, 6), (6.5, 12.5)], INK, 2.8)
    Q.guide(x=2, y=8, c=GRY_M)
    Q.point(2, 8, ENE_D, 4.2, "#fff")
    f.text(Q.X(2.4), Q.Y(8) + 17, "operação: 2 A e 8 V", 11, ENE_D, anchor="start", weight=600, halo=True)
    f.text(Q.X(2.4), Q.Y(8) + 34, "$I=0$: $U=\\varepsilon'=6$ V (fcem)", 11, INK, anchor="start", halo=True)
    f.text(Q.X(2.4), Q.Y(8) + 51, "inclinação $=r'=1\\ \\Omega$", 11, MUTED, anchor="start", halo=True)
    return f


@fig("instrumentos")
def instrumentos():
    f = Circ(680, 268, title="Ligação correta e incorreta de amperímetro e voltímetro")
    cells = [(0, 0, "A_ok", "Amperímetro em série (correto)"), (350, 0, "V_ok", "Voltímetro em paralelo (correto)"),
             (0, 136, "A_bad", "Amperímetro em paralelo: curto-circuito"), (350, 136, "V_bad", "Voltímetro em série: não passa corrente")]
    for (ox, oy, kind, title) in cells:
        f.text(ox + 165, oy + 14, title, 12, INK, weight=700)
        f.line(ox, oy + 22, ox + 330, oy + 22, RULE, 1, tag="bg")
        yt, yb = oy + 46, oy + 100
        f.bat((ox + 36, yb), (ox + 36, yt), pos="q", lab="w", signs=True, size=11)
        f.wire([(ox + 36, yb), (ox + 290, yb)])
        f.wire([(ox + 36, yt), (ox + 60, yt)])
        if kind == "A_ok":
            f.meter((ox + 60, yt), (ox + 150, yt), "A", lab="n")
            f.wire([(ox + 150, yt), (ox + 170, yt)])
            f.res((ox + 170, yt), (ox + 290, yt), "$R$", lab="n", length=46)
            f.wire([(ox + 290, yt), (ox + 290, yb)])
        elif kind == "V_ok":
            f.wire([(ox + 60, yt), (ox + 100, yt)])
            f.res((ox + 100, yt), (ox + 230, yt), "$R$", lab="n", length=50)
            f.wire([(ox + 230, yt), (ox + 290, yt), (ox + 290, yb)])
            f.node(ox + 130, yt)
            f.node(ox + 200, yt)
            f.wire([(ox + 130, yt), (ox + 130, yt + 14)])
            f.wire([(ox + 200, yt), (ox + 200, yt + 14)])
            f.wire([(ox + 130, yt + 14), (ox + 130, yt + 22)])
            f.wire([(ox + 200, yt + 14), (ox + 200, yt + 22)])
            f.meter((ox + 130, yt + 22), (ox + 200, yt + 22), "V", lab="s", r=11)
        elif kind == "A_bad":
            f.wire([(ox + 60, yt), (ox + 100, yt)])
            f.res((ox + 100, yt), (ox + 230, yt), "$R$", lab="n", length=50)
            f.wire([(ox + 230, yt), (ox + 290, yt), (ox + 290, yb)])
            f.node(ox + 130, yt)
            f.node(ox + 200, yt)
            f.wire([(ox + 130, yt), (ox + 130, yt + 22)])
            f.wire([(ox + 200, yt), (ox + 200, yt + 22)])
            f.meter((ox + 130, yt + 22), (ox + 200, yt + 22), "A", lab="s", r=11)
        else:
            f.meter((ox + 60, yt), (ox + 150, yt), "V", lab="n")
            f.wire([(ox + 150, yt), (ox + 170, yt)])
            f.res((ox + 170, yt), (ox + 290, yt), "$R$", lab="n", length=46)
            f.wire([(ox + 290, yt), (ox + 290, yb)])
        note = {"A_ok": "mede a corrente que passa por $R$; ideal: $R_A=0$",
                "V_ok": "mede a DDP em $R$; ideal: $R_V\\to\\infty$",
                "A_bad": "$R_A\\approx0$ contorna $R$: corrente enorme!",
                "V_bad": "$R_V$ enorme bloqueia: $I\\approx0$ e lê $\\approx\\varepsilon$"}[kind]
        f.text(ox + 165, yb + 24, note, 11, INK if kind.endswith("ok") else POS_D, weight=600 if kind.endswith("bad") else 400)
    return f


@fig("wheatstone")
def wheatstone():
    f = Circ(332, 232, title="Ponte de Wheatstone com galvanômetro")
    cA = pc(10, 10)
    f.bat((40, 190), (40, 44), pos="q", lab="w", signs=True, size=11)
    f.wire([(40, 44), (90, 44), (250, 44)])
    f.wire([(40, 190), (90, 190), (250, 190)])
    f.res((90, 44), (90, 117), "$R_1$", lab="w", length=40, size=11.5)
    f.res((90, 117), (90, 190), "$R_2$", lab="w", length=40, size=11.5)
    f.res((250, 44), (250, 117), "$R_3$", lab="e", length=40, size=11.5)
    f.res((250, 117), (250, 190), "$R_x$", lab="e", length=40, size=11.5)
    f.wire([(90, 117), (118, 117)])
    f.wire([(222, 117), (250, 117)])
    f.meter((118, 117), (222, 117), "G", lab="s", r=13)
    f.node(90, 117)
    f.node(250, 117)
    f.text(166, 218, "equilíbrio ($I_G=0$, $V_B=V_C$):  $R_1R_x=R_2R_3$", 11.5, INK, weight=600)
    return f


@fig("led_res")
def led_res():
    f = Circ(332, 190, title="LED com resistor de proteção")
    VM = 5
    cH, cM, cL = pc(5, VM), pc(2, VM), pc(0, VM)
    f.bat((40, 140), (40, 50), pos="q", lab="w", name="5 V", wc=(cL, cH), ww=WW, size=11)
    f.wire([(40, 50), (76, 50)], cH, WW)
    f.res((76, 50), (170, 50), "$R$", "150 Ω", lab="n", wc=(cH, cM), ww=WW)
    f.wire([(170, 50), (216, 50), (216, 66)], cM, WW)
    f.led((216, 66), (216, 126), "LED", lab="e", wc=(cM, cL), ww=WW)
    f.wire([(216, 126), (216, 140), (40, 140)], cL, WW)
    f.text(124, 166, "$U_R=5-2{,}0=3{,}0$ V", 11.5, INK, anchor="middle")
    f.text(124, 182, "$R=U_R/I=3{,}0/0{,}020=150\\ \\Omega$", 11.5, INK, weight=600)
    return f


@fig("mapa_dinam")
def mapa_dinam():
    f = Fig(680, 206, title="Mapa mental da Eletrodinâmica")
    W, H, G = 100, 50, 45
    xs = [k * (W + G) for k in range(5)]

    def node(x, y, t1, t2, col, fill):
        f.rect(x, y, W, H, fill, col, 2.2, rx=9, tag="bg")
        f.text(x + W / 2, y + 21, t1, 11.5, INK, weight=700)
        f.text(x + W / 2, y + 37, t2, 9.5, MUTED)

    def link(x, y, top, bot):
        f.arrow(x + W + 3, y + H / 2, x + W + G - 3, y + H / 2, INK, 2.0, 8, 0.4)
        f.text(x + W + G / 2, y + H / 2 - 8, top, 10, INK, weight=600)
        f.text(x + W + G / 2, y + H / 2 + 19, bot, 9.5, MUTED)
    row1 = [("DDP  $U$", "energia/carga", EFD, EFD_L), ("Corrente  $I$", "carga/tempo", CUR, CUR_L),
            ("Resistência $R$", "oposição", GRY, SOFT), ("Potência  $P$", "energia/tempo", ENE, ENE_L),
            ("Energia  $E$", "J ou kWh", ENE, ENE_L)]
    labs1 = [("$U=RI$", ""), ("$\\rho L/A$", "2ª lei"), ("$P=UI$", "$RI^2$ · $U^2/R$"), ("$P\\,\\Delta t$", "")]
    for k, (t1, t2, col, fil) in enumerate(row1):
        node(xs[k], 6, t1, t2, col, fil)
    for k in range(4):
        link(xs[k], 6, labs1[k][0], labs1[k][1])
    row2 = [("Circuito", "símbolos", GRY, SOFT), ("Nós", "potenciais, cores", INK, SOFT),
            ("Associação", "série · paralelo", CUR, CUR_L), ("Kirchhoff", "nós e malhas", INK, SOFT),
            ("$I$ e $U$ em tudo", "resultado", CUR, CUR_L)]
    labs2 = [("nomear", ""), ("agrupar", "$R_{eq}$"), ("se não", "reduz"), ("sistema", "linear")]
    for k, (t1, t2, col, fil) in enumerate(row2):
        node(xs[k], 120, t1, t2, col, fil)
    for k in range(4):
        link(xs[k], 120, labs2[k][0], labs2[k][1])
    f.text(340, 98, "gerador real:  $U=\\varepsilon-rI$  ·  rendimento  $\\eta=U/\\varepsilon$", 11, MUTED)
    f.text(340, 196, "$U=RI$ só para resistor ôhmico  ·  $P=UI$ vale sempre  ·  $R_{eq}$ só para trechos em série ou em paralelo", 10.5, MUTED)
    return f
