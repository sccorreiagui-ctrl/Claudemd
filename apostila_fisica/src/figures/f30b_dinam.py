"""Figuras do Módulo III — Eletrodinâmica (parte B: associações, método dos nós, ponte, curto)."""
import math
from . import fig
from lib.circuit import *

WW = 3.4   # espessura dos fios coloridos por potencial


def pc(v, vmax):
    return pot_color(v, 0, vmax)


@fig("circ_serie")
def circ_serie():
    f = Circ(332, 214, title="Circuito em série com potenciais: A 12 V, B 8 V, C 0 V")
    cA, cB, cC = pc(12, 12), pc(8, 12), pc(0, 12)
    f.bat((40, 164), (40, 50), pos="q", lab="w", name="$\\varepsilon$", val="12 V", wc=(cC, cA), ww=WW, size=12)
    f.wire([(40, 50), (84, 50)], cA, WW)
    f.res((84, 50), (196, 50), "$R_1$", "4 Ω", lab="n", wc=(cA, cB), ww=WW)
    f.wire([(196, 50), (280, 50), (280, 88)], cB, WW)
    f.res((280, 88), (280, 150), "$R_2$", "8 Ω", lab="w", wc=(cB, cC), ww=WW)
    f.wire([(280, 150), (280, 164), (40, 164)], cC, WW)
    f.badge(62, 50, "A", cA)
    f.badge(238, 50, "B", cB)
    f.badge(160, 164, "C", cC)
    f.text(62, 30, "12 V", 11.5, INK, weight=700)
    f.text(238, 30, "8 V", 11.5, INK, weight=700)
    f.text(160, 190, "0 V", 11.5, INK, weight=700)
    f.iarr((280, 50), (280, 88), 0.5, "$I$ = 1 A", length=22, side="w", off=8)
    f.iarr((120, 164), (60, 164), 0.5, "$I$ = 1 A", length=22, side="s")
    f.text(166, 208, "$U_1=4$ V  ·  $U_2=8$ V  ·  $U_1+U_2=\\varepsilon$", 11.5, INK, lint=False)
    return f


@fig("circ_par")
def circ_par():
    f = Circ(332, 214, title="Circuito em paralelo com potenciais: nó superior 12 V, nó inferior 0 V")
    cA, cB = pc(12, 12), pc(0, 12)
    f.bat((40, 164), (40, 50), pos="q", lab="w", name="$\\varepsilon$", val="12 V", wc=(cB, cA), ww=WW, size=12)
    f.wire([(40, 50), (290, 50)], cA, WW)
    f.wire([(40, 164), (290, 164)], cB, WW)
    f.res((136, 50), (136, 164), "$R_1$", "4 Ω", lab="w", wc=(cA, cB), ww=WW)
    f.res((236, 50), (236, 164), "$R_2$", "6 Ω", lab="e", wc=(cA, cB), ww=WW)
    for x in (136, 236):
        f.node(x, 50, cA, 4.2)
        f.node(x, 164, cB, 4.2)
    f.badge(70, 50, "A", cA)
    f.badge(70, 164, "B", cB)
    f.text(70, 30, "12 V", 11.5, INK, weight=700)
    f.text(70, 190, "0 V", 11.5, INK, weight=700)
    f.iarr((136, 56), (136, 90), 0.5, "$I_1$ = 3 A", length=22, side="w", off=8)
    f.iarr((236, 56), (236, 90), 0.5, "$I_2$ = 2 A", length=22, side="e", off=8)
    f.iarr((96, 50), (130, 50), 0.5, "$I$ = 5 A", length=22, off=7)
    f.text(166, 208, "mesma $U=12$ V  ·  $I=I_1+I_2$", 11.5, INK, lint=False)
    return f


@fig("lamp_sp")
def lamp_sp():
    f = Circ(680, 214, title="Duas lâmpadas idênticas: em série e em paralelo")
    f.text(165, 14, "Em série", 13, INK, weight=700)
    f.text(515, 14, "Em paralelo", 13, INK, weight=700)
    y1, y2 = 56, 150
    f.bat((40, y2), (40, y1), pos="q", lab="w", name="12 V", signs=True, size=11)
    f.wire([(40, y1), (70, y1)])
    f.lamp((70, y1), (160, y1), "$L_1$", lab="s", lum=1, r=13)
    f.lamp((160, y1), (250, y1), "$L_2$", lab="s", lum=1, r=13)
    f.wire([(250, y1), (300, y1), (300, y2), (40, y2)])
    f.node(160, y1)
    f.text(166, 184, "mesma corrente; cada lâmpada recebe 6 V", 11.5, INK)
    f.text(166, 200, "brilho fraco (potência ¼ da nominal); se uma queima, a outra apaga", 10.5, MUTED)
    xo = 360
    f.bat((xo + 40, y2), (xo + 40, y1), pos="q", lab="w", name="12 V", signs=True, size=11)
    f.wire([(xo + 40, y1), (xo + 290, y1)])
    f.wire([(xo + 40, y2), (xo + 290, y2)])
    f.lamp((xo + 150, y1), (xo + 150, y2), "$L_1$", lab="w", lum=3, r=13)
    f.lamp((xo + 250, y1), (xo + 250, y2), "$L_2$", lab="e", lum=3, r=13)
    for x in (xo + 150, xo + 250):
        f.node(x, y1)
        f.node(x, y2)
    f.text(xo + 165, 184, "cada lâmpada recebe 12 V (brilho nominal)", 11.5, INK)
    f.text(xo + 165, 200, "se uma queima, a outra continua acesa", 10.5, MUTED)
    return f


@fig("ex_lamp")
def ex_lamp():
    f = Circ(680, 236, title="Exemplo 16: três lâmpadas idênticas e uma chave")
    for k, (closed, title, lums, note1, note2) in enumerate((
            (False, "Chave S aberta", (2, 2, 0), "$I=1{,}5$ A", "$P_1=P_2=9$ W · $L_3$ apagada"),
            (True, "Chave S fechada", (3, 1, 1), "$I=2{,}0$ A", "$P_1=16$ W · $P_2=P_3=4$ W"))):
        xo = k * 350
        f.text(xo + 165, 14, title, 12.5, INK, weight=700)
        f.line(xo, 22, xo + 330, 22, RULE, 1, tag="bg")
        f.bat((xo + 36, 166), (xo + 36, 62), pos="q", lab="w", name="12 V", signs=True, size=11)
        f.wire([(xo + 36, 62), (xo + 56, 62)])
        f.lamp((xo + 56, 62), (xo + 150, 62), "$L_1$", lab="n", lum=lums[0], r=13)
        f.wire([(xo + 150, 62), (xo + 290, 62)])
        f.wire([(xo + 36, 166), (xo + 290, 166)])
        f.lamp((xo + 190, 62), (xo + 190, 166), "$L_2$", lab="w", lum=lums[1], r=13)
        f.sw((xo + 270, 62), (xo + 270, 104), closed=closed, name="S", lab="w", length=30, up="e", ang=32)
        f.lamp((xo + 270, 104), (xo + 270, 166), "$L_3$", lab="e", lum=lums[2], r=13)
        f.node(xo + 190, 62)
        f.node(xo + 190, 166)
        f.node(xo + 270, 62)
        f.node(xo + 270, 166)
        f.text(xo + 165, 204, note1, 12, INK, weight=600)
        f.text(xo + 165, 222, note2, 11.5, INK)
    return f


@fig("metodo_misto")
def metodo_misto():
    f = Circ(680, 352, title="Método para circuitos mistos em quatro desenhos")
    VM = 24
    cols = {"A": pc(24, VM), "B": pc(18, VM), "C": pc(6, VM), "D": pc(0, VM)}
    yt, yb = 52, 138

    def base(ox, oy, colored=False, par_eq=False, tot_eq=False):
        cA, cB, cC, cD = (cols["A"], cols["B"], cols["C"], cols["D"]) if colored else (INK,) * 4
        ww = WW if colored else 2.0
        f.bat((ox + 40, oy + yb), (ox + 40, oy + yt), pos="q", lab="w", name="24 V", wc=(cD, cA), ww=ww, size=11)
        f.wire([(ox + 40, oy + yt), (ox + 62, oy + yt)], cA, ww)
        if tot_eq:
            f.res((ox + 62, oy + yt), (ox + 250, oy + yt), "$R_{eq}$", "8 Ω", lab="n", wc=(cA, cA), ww=ww, length=56)
            f.wire([(ox + 250, oy + yt), (ox + 290, oy + yt), (ox + 290, oy + yb), (ox + 40, oy + yb)], cD, ww)
            return
        f.res((ox + 62, oy + yt), (ox + 142, oy + yt), "$R_1$", "2 Ω", lab="n", wc=(cA, cB), ww=ww)
        f.wire([(ox + 142, oy + yt), (ox + 168, oy + yt)], cB, ww)
        if par_eq:
            f.res((ox + 168, oy + yt), (ox + 168, oy + yb), "$R_p$", "4 Ω", lab="e", wc=(cB, cC), ww=ww, length=48)
        else:
            f.wire([(ox + 168, oy + yt), (ox + 250, oy + yt)], cB, ww)
            f.res((ox + 168, oy + yt), (ox + 168, oy + yb), "$R_2$", "6 Ω", lab="w", wc=(cB, cC), ww=ww, length=44)
            f.res((ox + 250, oy + yt), (ox + 250, oy + yb), "$R_3$", "12 Ω", lab="e", wc=(cB, cC), ww=ww, length=44)
            f.wire([(ox + 250, oy + yb), (ox + 168, oy + yb)], cC, ww)
        f.node(ox + 168, oy + yt, cB, 4)
        f.node(ox + 168, oy + yb, cC, 4)
        f.res((ox + 168, oy + yb), (ox + 62, oy + yb), "$R_4$", "2 Ω", lab="n", wc=(cC, cD), ww=ww)
        f.wire([(ox + 62, oy + yb), (ox + 40, oy + yb)], cD, ww)

    heads = ["1  Circuito original", "2  Nomear os nós (cor = potencial)", "3  Substituir o paralelo por $R_p$", "4  Resistência equivalente"]
    offs = [(0, 0), (350, 0), (0, 176), (350, 176)]
    for k, (ox, oy) in enumerate(offs):
        f.text(ox + 165, oy + 14, heads[k], 12, INK, weight=700)
        f.line(ox, oy + 22, ox + 330, oy + 22, RULE, 1, tag="bg")
        base(ox, oy, colored=(k == 1), par_eq=(k == 2), tot_eq=(k == 3))
    ox, oy = 350, 0
    f.badge(ox + 51, oy + yt - 18, "A", cols["A"], r=8.5, size=11)
    f.badge(ox + 155, oy + yt - 20, "B", cols["B"], r=8.5, size=11)
    f.badge(ox + 155, oy + yb + 20, "C", cols["C"], r=8.5, size=11)
    f.badge(ox + 51, oy + yb + 18, "D", cols["D"], r=8.5, size=11)
    f.text(ox + 165, oy + 170, "A 24 V · B 18 V · C 6 V · D 0 V", 11, INK, weight=700)
    f.text(165, 170, "$R_2$ e $R_3$ ligam os mesmos nós $B$ e $C$ ⇒ paralelo", 11, MUTED)
    f.text(165, 176 + 170, "$R_p=(R_2R_3)/(R_2+R_3)=4\\ \\Omega$", 11.5, INK)
    f.text(515, 176 + 170, "$R_{eq}=R_1+R_p+R_4=8\\ \\Omega$", 11.5, INK)
    return f


@fig("ex_misto1")
def ex_misto1():
    f = Circ(332, 246, title="Exemplo 17: potenciais e correntes do circuito misto")
    cA, cB, cC, cD = pc(24, 24), pc(18, 24), pc(6, 24), pc(0, 24)
    f.bat((36, 156), (36, 56), pos="q", lab="w", name="24 V", wc=(cD, cA), ww=WW, size=11)
    f.wire([(36, 56), (60, 56)], cA, WW)
    f.res((60, 56), (146, 56), "$R_1$", "2 Ω", lab="n", wc=(cA, cB), ww=WW)
    f.wire([(146, 56), (172, 56), (252, 56)], cB, WW)
    f.res((172, 56), (172, 156), "$R_2$", "6 Ω", lab="w", wc=(cB, cC), ww=WW, length=44)
    f.res((252, 56), (252, 156), "$R_3$", "12 Ω", lab="e", wc=(cB, cC), ww=WW, length=44)
    f.wire([(252, 156), (172, 156)], cC, WW)
    f.res((172, 156), (60, 156), "$R_4$", "2 Ω", lab="n", wc=(cC, cD), ww=WW)
    f.wire([(60, 156), (36, 156)], cD, WW)
    f.node(172, 56, cB, 4.2)
    f.node(172, 156, cC, 4.2)
    f.badge(48, 36, "A", cA, r=8.5, size=11)
    f.badge(159, 36, "B", cB, r=8.5, size=11)
    f.badge(159, 178, "C", cC, r=8.5, size=11)
    f.badge(48, 178, "D", cD, r=8.5, size=11)
    f.iarr((172, 56), (172, 156), 0.2, "$I_2$", length=20, side="e", off=8)
    f.iarr((252, 56), (252, 156), 0.2, "$I_3$", length=20, side="w", off=8)
    f.iarr((36, 70), (36, 56), 0.5, None, length=0.1)
    f.iarr((60, 56), (100, 56), 0.5, None, length=0.1)
    f.iarr((210, 156), (190, 156), 0.5, None, length=0.1)
    f.text(166, 206, "A 24 V · B 18 V · C 6 V · D 0 V", 11.5, INK, weight=700)
    f.text(166, 222, "$I=3$ A  ·  $I_2=2$ A  ·  $I_3=1$ A", 12, INK, weight=600)
    f.text(166, 238, "$U_1=6$ V  ·  $U_p=12$ V  ·  $U_4=6$ V", 11.5, INK)
    return f


@fig("nos_regras")
def nos_regras():
    f = Circ(680, 214, title="Regras para ler nós e potenciais em um desenho de circuito")
    cH, cM, cL = pc(12, 12), pc(8, 12), pc(0, 12)
    heads = ["Fio ideal", "Resistor com corrente", "Paralelo", "Série"]
    for k in range(4):
        ox = k * 175
        f.text(ox + 80, 14, heads[k], 12, INK, weight=700)
        f.line(ox, 22, ox + 160, 22, RULE, 1, tag="bg")
    # (i) fio ideal
    ox = 0
    f.wire([(ox + 8, 70), (ox + 110, 70), (ox + 110, 120), (ox + 152, 120)], cH, WW)
    for (x, y) in ((ox + 8, 70), (ox + 110, 70), (ox + 152, 120)):
        f.node(x, y, cH, 4.5)
    f.text(ox + 30, 56, "12 V", 11.5, INK, weight=700)
    f.text(ox + 134, 92, "12 V", 11.5, INK, weight=700)
    f.text(ox + 130, 140, "12 V", 11.5, INK, weight=700)
    f.text(ox + 80, 166, "mesmo potencial", 11.5, INK)
    f.text(ox + 80, 181, "em todo o fio", 11.5, INK)
    f.text(ox + 80, 200, "(mesma cor)", 10.5, MUTED)
    # (ii) resistor
    ox = 175
    f.wire([(ox + 8, 96), (ox + 38, 96)], cH, WW)
    f.res((ox + 38, 96), (ox + 122, 96), "$R$", lab="n", wc=(cH, cM), ww=WW, length=44)
    f.wire([(ox + 122, 96), (ox + 152, 96)], cM, WW)
    f.text(ox + 24, 130, "12 V", 11.5, INK, weight=700)
    f.text(ox + 136, 130, "8 V", 11.5, INK, weight=700)
    f.iarr((ox + 38, 96), (ox + 122, 96), 0.5, None, length=0.1)
    f.arrow(ox + 56, 152, ox + 104, 152, CUR, 2.6, 9)
    f.text(ox + 116, 156, "$I$", 12, CUR_D, anchor="start", weight=600)
    f.text(ox + 80, 166, "o potencial cai", 11.5, INK)
    f.text(ox + 80, 181, "ao atravessar $R$", 11.5, INK)
    f.text(ox + 80, 200, "($\\Delta V=-RI$)", 10.5, MUTED)
    # (iii) paralelo
    ox = 350
    f.wire([(ox + 8, 52), (ox + 152, 52)], cH, WW)
    f.wire([(ox + 8, 132), (ox + 152, 132)], cL, WW)
    f.res((ox + 50, 52), (ox + 50, 132), "$R_1$", lab="w", wc=(cH, cL), ww=WW, length=40, size=11.5)
    f.res((ox + 112, 52), (ox + 112, 132), "$R_2$", lab="e", wc=(cH, cL), ww=WW, length=40, size=11.5)
    for x in (ox + 50, ox + 112):
        f.node(x, 52, cH, 4)
        f.node(x, 132, cL, 4)
    f.text(ox + 80, 44, "12 V", 11.5, INK, weight=700)
    f.text(ox + 80, 152, "0 V", 11.5, INK, weight=700)
    f.text(ox + 80, 166, "mesmos dois nós", 11.5, INK)
    f.text(ox + 80, 181, "(mesmas cores nas pontas)", 10.5, MUTED)
    f.text(ox + 80, 200, "⇒ mesma tensão", 11.5, INK, weight=600)
    # (iv) série
    ox = 525
    f.wire([(ox + 6, 90), (ox + 24, 90)], cH, WW)
    f.res((ox + 24, 90), (ox + 80, 90), "$R_1$", lab="n", wc=(cH, cM), ww=WW, length=32, amp=6, size=11.5)
    f.res((ox + 80, 90), (ox + 136, 90), "$R_2$", lab="n", wc=(cM, cL), ww=WW, length=32, amp=6, size=11.5)
    f.wire([(ox + 136, 90), (ox + 154, 90)], cL, WW)
    f.node(ox + 80, 90, cM, 4.2)
    f.line(ox + 80, 94, ox + 80, 138, GRY, 1.6, "4 3", tag="bg")
    f.text(ox + 80, 154, "3º ramo?", 10.5, GRY)
    f.text(ox + 80, 166, "nó com só 2 ligações", 11.5, INK)
    f.text(ox + 80, 181, "⇒ série (mesma corrente)", 11.5, INK, weight=600)
    f.text(ox + 80, 200, "com 3º ramo: não é série", 10.5, MUTED)
    return f


@fig("ex_ponte")
def ex_ponte():
    f = Circ(680, 232, title="Exemplo 18: ponte com fio entre B e C e circuito redesenhado")
    cA, cM, cD = pc(24, 24), pc(12, 24), pc(0, 24)
    f.text(165, 14, "Original: fio entre $B$ e $C$ (cores = potenciais)", 12, INK, weight=700)
    f.line(0, 22, 330, 22, RULE, 1, tag="bg")
    f.bat((36, 176), (36, 52), pos="q", lab="w", name="24 V", wc=(cD, cA), ww=WW, size=11)
    f.wire([(36, 52), (252, 52)], cA, WW)
    f.wire([(36, 176), (252, 176)], cD, WW)
    f.res((110, 52), (110, 114), "$R_1$", "6 Ω", lab="w", wc=(cA, cM), ww=WW, length=40, size=11.5)
    f.res((110, 114), (110, 176), "$R_3$", "3 Ω", lab="w", wc=(cM, cD), ww=WW, length=40, size=11.5)
    f.res((252, 52), (252, 114), "$R_2$", "3 Ω", lab="e", wc=(cA, cM), ww=WW, length=40, size=11.5)
    f.res((252, 114), (252, 176), "$R_4$", "6 Ω", lab="e", wc=(cM, cD), ww=WW, length=40, size=11.5)
    f.wire([(110, 114), (252, 114)], cM, WW)
    for (x, y, c) in ((110, 52, cA), (252, 52, cA), (110, 176, cD), (252, 176, cD), (110, 114, cM), (252, 114, cM)):
        f.node(x, y, c, 4.2)
    f.badge(70, 52, "A", cA, r=8.5, size=11)
    f.badge(70, 176, "D", cD, r=8.5, size=11)
    f.badge(140, 114, "B", cM, r=8.5, size=11)
    f.badge(222, 114, "C", cM, r=8.5, size=11)
    f.iarr((110, 56), (110, 80), 0.5, "$I_1$", length=18, side="e", off=8)
    f.iarr((252, 56), (252, 80), 0.5, "$I_2$", length=18, side="w", off=8)
    f.iarr((110, 118), (110, 142), 0.5, "$I_3$", length=18, side="e", off=8)
    f.iarr((252, 118), (252, 142), 0.5, "$I_4$", length=18, side="w", off=8)
    f.iarr((215, 114), (150, 114), 0.5, "$I_{fio}$", length=22, side="n", off=7)
    f.text(165, 205, "$V_A=24$ V · $V_B=V_C=12$ V · $V_D=0$", 11.5, INK, weight=600)
    f.text(165, 221, "$I_1=2$ A · $I_2=4$ A · $I_3=4$ A · $I_4=2$ A · $I_{fio}=2$ A", 11.5, INK)
    # equivalente
    ox = 350
    f.text(ox + 165, 14, "Equivalente: $(R_1\\parallel R_2)$ em série com $(R_3\\parallel R_4)$", 12, INK, weight=700)
    f.line(ox, 22, ox + 330, 22, RULE, 1, tag="bg")
    f.bat((ox + 40, 150), (ox + 40, 62), pos="q", lab="w", name="24 V", signs=True, size=11)
    f.wire([(ox + 40, 62), (ox + 66, 62)])
    f.res((ox + 66, 62), (ox + 168, 62), "$R_{AM}$", "2 Ω", lab="n", length=48)
    f.res((ox + 168, 62), (ox + 270, 62), "$R_{MD}$", "2 Ω", lab="n", length=48)
    f.wire([(ox + 270, 62), (ox + 300, 62), (ox + 300, 150), (ox + 40, 150)])
    f.node(ox + 168, 62)
    f.badge(ox + 168, 88, "M", cM, r=8.5, size=11)
    f.text(ox + 165, 180, "$R_{AM}=6\\parallel3=2\\ \\Omega$  ·  $R_{MD}=3\\parallel6=2\\ \\Omega$", 11.5, INK, weight=600)
    f.text(ox + 165, 196, "$R_{eq}=4\\ \\Omega$  ·  $I=24/4=6$ A", 11.5, INK)
    f.text(ox + 165, 212, "$I_{fio}=I_2-I_4=I_3-I_1=2$ A", 11.5, INK)
    return f


@fig("curto")
def curto():
    f = Circ(680, 240, title="Curto-circuito: antes e depois de um fio ideal contornar R2")
    for k in range(2):
        xo = k * 350
        short = k == 1
        f.text(xo + 165, 14, "Antes: $R_1$ e $R_2$ em série" if not short else "Depois: fio ideal em paralelo com $R_2$", 12, INK, weight=700)
        f.line(xo, 22, xo + 330, 22, RULE, 1, tag="bg")
        cA = pc(12, 12)
        cB = pc(8 if not short else 0, 12)
        cC = pc(0, 12)
        f.bat((xo + 40, 170), (xo + 40, 56), pos="q", lab="w", name="12 V", wc=(cC, cA), ww=WW, size=11)
        f.wire([(xo + 40, 56), (xo + 78, 56)], cA, WW)
        f.res((xo + 78, 56), (xo + 190, 56), "$R_1$", "4 Ω", lab="n", wc=(cA, cB), ww=WW)
        f.wire([(xo + 190, 56), (xo + 240, 56)], cB, WW)
        f.wire([(xo + 240, 56), (xo + 240, 70)], cB, WW)
        f.res((xo + 240, 70), (xo + 240, 156), "$R_2$", "8 Ω", lab="w", wc=(cB, cC), ww=WW, length=44)
        f.wire([(xo + 240, 156), (xo + 240, 170), (xo + 40, 170)], cC, WW)
        if short:
            f.wire([(xo + 240, 56), (xo + 300, 56), (xo + 300, 170), (xo + 240, 170)], cC, WW)
            f.node(xo + 240, 56, cC, 4.2)
            f.node(xo + 240, 170, cC, 4.2)
            f.text(xo + 292, 112, "fio", 11.5, INK, anchor="end", weight=600)
            f.text(xo + 292, 126, "ideal", 11.5, INK, anchor="end", weight=600)
        f.badge(xo + 60, 56, "A", cA, r=8.5, size=11)
        f.badge(xo + 214, 56, "B", cB, r=8.5, size=11)
        f.badge(xo + 150, 170, "C", cC, r=8.5, size=11)
        if not short:
            f.text(xo + 165, 204, "$I=12/(4+8)=1$ A  ·  $U_2=8$ V", 12, INK, weight=600)
            f.text(xo + 165, 222, "$P_1=I^2R_1=4$ W  ·  $P_2=8$ W", 11.5, INK)
        else:
            f.text(xo + 165, 204, "$I=12/4=3$ A  ·  $U_2=0$, $I_2=0$", 12, INK, weight=600)
            f.text(xo + 165, 222, "$P_1=I^2R_1=36$ W  (9 vezes maior!)", 11.5, ENE_D, weight=600)
        f.iarr((xo + 40, 170), (xo + 100, 170), 0.5, None, length=0.1)
        f.iarr((xo + 120, 170), (xo + 80, 170), 0.5, "$I$", length=22, side="s", off=8)
    return f
