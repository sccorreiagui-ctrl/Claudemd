"""Figuras do Módulo III — Eletrodinâmica (parte A: corrente, Ohm, potência, chuveiro)."""
import math, random
from . import fig
from lib.circuit import *


def coil_pts(x0, x1, y, n=10, a=7.5, h=7.0):
    """Pontos de uma bobina helicoidal vista de lado (cicloide prolata) entre x0 e x1, centrada em y."""
    L = (x1 - x0) - 2 * a
    N = n * 28
    pts = []
    for k in range(N + 1):
        t = k / N
        th = 2 * math.pi * n * t
        pts.append((x0 + a + L * t - a * math.sin(th), y - h * math.cos(th)))
    return pts


@fig("hidraulica")
def hidraulica():
    f = Circ(680, 176, title="Analogia hidráulica: bomba, tubulação, estreitamento e vazão ↔ fonte, fios, resistor e corrente")
    # ----- circuito hidráulico
    f.text(165, 14, "Analogia hidráulica", 12.5, INK, weight=700)
    x0, x1, y0, y1 = 36, 296, 48, 128
    loop = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    f.pl(loop, GRY_L, 16, tag="bg")
    f.pl(loop, "#fff", 10, tag="bg")
    f.line(150, y0, 190, y0, GRY_L, 16, cap="butt", tag="bg")
    f.line(150, y0, 190, y0, "#fff", 3.4, cap="butt", tag="bg")
    f.circ(x0, 88, 19, "#fff", GRY, 2.2, tag="bg")
    f.text(x0, 92, "↑", 15, GRY, weight=700, lint=False)
    for (ax, ay, bx, by) in ((84, y0, 118, y0), (222, y0, 262, y0), (x1, 68, x1, 100), (250, y1, 210, y1), (130, y1, 90, y1)):
        f.arrow(ax, ay, bx, by, CUR, 3.0, 10)
    f.text(x0 + 24, 148, "bomba", 11.5, INK, weight=600, anchor="start")
    f.text(170, 30, "estreitamento", 11.5, INK, weight=600)
    f.text(x1 - 8, 150, "vazão", 11.5, CUR_D, weight=600, anchor="end")
    f.arrow(x0 - 30, y1 + 4, x0 - 30, y0 - 4, GRY, 1.1, 6, 0.4, both=True)
    f.text(18, 92, "Δ", 13, GRY, lint=False)
    f.text(170, 168, "pressão ↔ tensão", 10.5, MUTED, lint=False)
    # ----- circuito elétrico
    xo = 350
    f.text(xo + 165, 14, "Circuito elétrico", 12.5, INK, weight=700)
    f.bat((xo + 40, y1), (xo + 40, y0), pos="q", lab="w", name="fonte", signs=True, size=11.5)
    f.wire([(xo + 40, y0), (xo + 130, y0)])
    f.res((xo + 130, y0), (xo + 210, y0), "$R$", lab="n", length=48)
    f.wire([(xo + 210, y0), (xo + 290, y0), (xo + 290, y1), (xo + 40, y1)])
    f.iarr((xo + 40, y0), (xo + 130, y0), 0.35, "$I$", length=24)
    f.iarr((xo + 290, y0), (xo + 290, y1), 0.5, "$I$", length=24, side="w")
    f.iarr((xo + 290, y1), (xo + 40, y1), 0.5, "$I$", length=24, side="s")
    return f


@fig("fio_micro")
def fio_micro():
    f = Fig(332, 206, title="Fio condutor: elétrons livres colidindo com a rede; deriva lenta; corrente convencional")
    f.rect(14, 56, 304, 94, "#fff", GRY, 2.2, rx=14, tag="bg")
    for i in range(7):
        for j in range(3):
            cx, cy = 40 + i * 42, 78 + j * 31
            f.circ(cx, cy, 8, GRY_XL, GRY, 1.3, tag="bg")
            f.line(cx - 3, cy, cx + 3, cy, GRY, 1.1, tag="bg")
            f.line(cx, cy - 3, cx, cy + 3, GRY, 1.1, tag="bg")
    rnd = random.Random(11)
    paths = [(70, 90), (120, 112), (190, 84), (250, 120), (100, 134), (210, 100), (290, 92), (160, 130)]
    for (px, py) in paths:
        pts = [(px, py)]
        x, y = px, py
        for _ in range(4):
            x += rnd.uniform(-14, -4)
            y += rnd.uniform(-9, 9)
            y = min(max(y, 66), 140)
            pts.append((x, y))
        f.pl(pts, NEG, 1.1, tag="bg", op=0.8)
        f.circ(pts[0][0], pts[0][1], 3.4, NEG, NEG, 1, tag="bg")
    f.arrow(300, 170, 80, 170, NEG_D, 2.4, 10)
    f.text(190, 186, "elétrons: deriva lenta (≈ 10⁻⁴ m/s), sentido oposto a $\\vec E$", 11, NEG_D)
    f.arrow(40, 32, 300, 32, EFD, 2.6, 10)
    f.text(170, 20, "$\\vec E$ no fio (estabelece-se pela fonte)", 11.5, EFD_D)
    f.arrow(40, 48, 300, 48, CUR, 3.0, 11)
    f.text(318, 42, "$I$", 12.5, CUR_D, anchor="end", weight=600)
    f.text(166, 202, "convenção: $I$ tem o sentido de $\\vec E$ (como se cargas + andassem)", 10.5, MUTED, lint=False)
    return f


@fig("cc_ca")
def cc_ca():
    f = Fig(680, 200, title="Corrente contínua e corrente alternada")
    f.text(150, 14, "Corrente contínua (pilha, bateria)", 12, INK, weight=700)
    P = Plot(f, 50, 156, 232, 110, (0, 3.2), (0, 4), xticks=[(1, "1"), (2, "2"), (3, "3")], yticks=[(2, "2")], grid=True)
    P.axis_labels("$t$ (s)", "$I$ (A)", ydx=6)
    P.line([(0, 2), (3.1, 2)], CUR, 3.0)
    f.text(P.X(1.6), P.Y(2) - 10, "$I$ constante, sempre no mesmo sentido", 11, CUR_D, halo=True)
    # CA: tensão da tomada
    f.text(490, 14, "Tensão alternada (tomada, 60 Hz)", 12, INK, weight=700)
    x0, x1, ym, A = 384, 592, 108, 62
    X = lambda t: x0 + t * (x1 - x0) / 33.4
    Y = lambda u: ym - u * A / 180
    for lvl, col in ((180, GRY_M), (127, ENE)):
        for sgn in (1, -1):
            f.line(x0, Y(sgn * lvl), x1 + 4, Y(sgn * lvl), col, 1.3, "5 4", tag="bg")
    f.arrow(x0, ym + 82, x0, ym - 86, INK, 1.6, 8, 0.34)
    f.arrow(x0 - 6, ym, x1 + 14, ym, INK, 1.6, 8, 0.34)
    data = [(X(t), Y(180 * math.sin(2 * math.pi * t / 16.667))) for t in [k * 0.2 for k in range(0, 168)]]
    f.pl(data, CUR, 2.8)
    for (lv, lb, col) in ((180, "180", MUTED), (127, "127", ENE_D), (-127, "−127", ENE_D), (-180, "−180", MUTED)):
        f.text(x0 - 6, Y(lv) + 4, lb, 10.5, col, anchor="end", lint=False)
    f.text(x0 - 8, ym - 70, "$U$ (V)", 12, INK, anchor="end")
    f.text(x1 + 18, ym - 8, "$t$ (ms)", 12, INK, anchor="start")
    f.arrow(X(0), ym - 74, X(16.667), ym - 74, GRY, 1.1, 6, 0.4, both=True)
    f.text(X(8.33), ym - 80, "$T=16{,}7$ ms", 11, INK)
    f.text(x1 + 10, Y(180) + 4, "$U_{max}=180$ V", 11, MUTED, anchor="start")
    f.text(x1 + 10, Y(127) + 4, "$U_{ef}=127$ V", 11, ENE_D, anchor="start", weight=700)
    f.text(490, 194, "$U_{ef}=U_{max}/\\sqrt2$  ·  $f=1/T=60$ Hz", 11, INK)
    return f


@fig("ohm_graf")
def ohm_graf():
    f = Fig(680, 206, title="Gráficos U×I e I×U de resistores ôhmicos e de uma lâmpada (não ôhmico)")
    # (a) U x I
    f.text(104, 14, "Resistores ôhmicos: $U\\times I$", 12, INK, weight=700)
    P = Plot(f, 46, 170, 180, 120, (0, 4.4), (0, 14), xticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], yticks=[(4, "4"), (8, "8"), (12, "12")], grid=True)
    P.axis_labels("$I$ (A)", "$U$ (V)", ydx=4)
    P.line([(0, 0), (2.3, 13.8)], INK, 2.6)
    P.line([(0, 0), (4.3, 8.6)], GRY, 2.6)
    f.text(P.X(2.35) + 3, P.Y(13.2), "$R=6\\ \\Omega$", 11.5, INK, anchor="start", weight=600)
    f.text(P.X(4.3) - 2, P.Y(8.6) - 7, "$R=2\\ \\Omega$", 11.5, GRY, anchor="end", weight=600)
    f.text(104, 198, "inclinação $=U/I=R$", 11, INK)
    # (b) I x U
    f.text(350, 14, "Os mesmos: $I\\times U$", 12, INK, weight=700)
    P2 = Plot(f, 292, 170, 180, 120, (0, 14), (0, 4.6), xticks=[(4, "4"), (8, "8"), (12, "12")], yticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], grid=True)
    P2.axis_labels("$U$ (V)", "$I$ (A)", ydx=4)
    P2.line([(0, 0), (13.8, 2.3)], INK, 2.6)
    P2.line([(0, 0), (9.2, 4.6)], GRY, 2.6)
    f.text(P2.X(13.8) - 2, P2.Y(2.3) - 16, "$R=6\\ \\Omega$", 11.5, INK, anchor="end", weight=600)
    f.text(P2.X(9.2) + 4, P2.Y(4.6) + 10, "$R=2\\ \\Omega$", 11.5, GRY, anchor="start", weight=600)
    f.text(350, 198, "inclinação $=I/U=1/R$ (condutância)", 11, INK)
    # (c) lâmpada
    f.text(570, 14, "Lâmpada de filamento (não ôhmica)", 12, INK, weight=700)
    P3 = Plot(f, 520, 170, 118, 120, (0, 13), (0, 3.4), xticks=[(4, "4"), (8, "8"), (12, "12")], yticks=[(1, "1"), (2, "2"), (3, "3")], grid=True)
    P3.axis_labels("$U$ (V)", "$I$ (A)", ydx=4)
    P3.curve(lambda u: 0.97 * u ** 0.62 / 3.8 * 3.4 / 3.4 * 1.0, 0, 12.5, 60, c=CUR, w=2.8)
    f.text(570, 198, "$R=U/I$ cresce: filamento esquenta", 11, INK)
    return f


@fig("fios_RL")
def fios_RL():
    f = Fig(332, 190, title="Dois fios do mesmo material: longo e fino × curto e grosso")
    def cyl(x0, x1, yc, r, col, face):
        f.path(f"M{x0},{yc - r} L{x1},{yc - r} A{r * 0.45},{r} 0 0 1 {x1},{yc + r} L{x0},{yc + r} A{r * 0.45},{r} 0 0 1 {x0},{yc - r} Z", GRY, 1.8, col, tag="bg")
        f.ell(x1, yc, r * 0.45, r, face, GRY, 1.8, tag="bg")
    cyl(40, 250, 46, 7, "#D9DEE7", "#B9C1CF")
    f.text(8, 50, "1", 12, INK, weight=700, anchor="start")
    f.arrow(40, 70, 250, 70, GRY, 1.1, 6, 0.4, both=True)
    f.text(145, 86, "comprimento $L$", 11, INK)
    f.text(264, 40, "área $A$", 11, INK, anchor="start")
    f.text(264, 54, "$R_1=\\rho\\,L/A$", 11.5, INK, anchor="start", weight=600)
    cyl(40, 145, 136, 17, "#D9DEE7", "#B9C1CF")
    f.text(8, 140, "2", 12, INK, weight=700, anchor="start")
    f.arrow(40, 164, 145, 164, GRY, 1.1, 6, 0.4, both=True)
    f.text(92, 180, "comprimento $L/2$", 11, INK)
    f.text(176, 130, "área $2A$", 11, INK, anchor="start")
    f.text(176, 144, "$R_2=\\rho\\,(L/2)/(2A)=R_1/4$", 11.5, INK, anchor="start", weight=600)
    return f


@fig("rho_T")
def rho_T():
    f = Fig(332, 166, title="Efeito da temperatura na resistividade: metais e termistor NTC")
    P = Plot(f, 46, 136, 238, 100, (0, 4), (0, 4), xticks=[], yticks=[], grid=False)
    P.axis_labels("$T$", "$\\rho$", xdx=-2, ydx=4)
    P.line([(0.2, 1.2), (3.8, 3.2)], CUR, 2.8)
    P.curve(lambda t: 3.6 * math.exp(-0.75 * t) + 0.35, 0.2, 3.8, 60, c=EFD, w=2.8)
    f.text(P.X(3.82) + 4, P.Y(3.2) + 3, "metais:", 11.5, CUR_D, anchor="start", weight=700, lint=False)
    f.text(P.X(3.82) + 4, P.Y(3.2) + 16, "$\\rho$ aumenta", 11.5, CUR_D, anchor="start", lint=False)
    f.text(P.X(1.6), P.Y(1.62), "NTC: $\\rho$ diminui", 11.5, EFD_D, anchor="start", weight=700, lint=False)
    return f


@fig("chuveiro")
def chuveiro():
    f = Circ(680, 214, title="Chuveiro elétrico: resistor helicoidal e comprimento útil nas posições desligada, morna e quente")
    titles = ["Desligada", "Morna (verão)", "Quente (inverno)"]
    for k in range(3):
        x0 = k * 233
        f.text(x0 + 106, 14, titles[k], 12.5, INK, weight=700)
        f.line(x0, 22, x0 + 213, 22, RULE, 1, tag="bg")
        ya, xa, xc, xb = 62, x0 + 30, x0 + 108, x0 + 186
        # bobina inteira em cinza
        n, a, h = 10, 7.5, 7.0
        cp = coil_pts(xa + 6, xb - 6, ya, n, a, h)
        f.pl([(xa, ya)] + cp + [(xb, ya)], GRY_M, 2.4)
        # parte ativa
        act = {0: None, 1: xb, 2: xc}[k]
        if act:
            seg = []
            for (px, py) in cp:
                if px > act + a:
                    break
                seg.append((px, py))
            f.pl([(xa, ya)] + seg + [(act, ya)], CUR, 3.6)
        # terminais
        for (tx, nm) in ((xa, "A"), (xc, "C"), (xb, "B")):
            f.circ(tx, ya, 3.6, "#fff", INK, 1.8, tag="bg")
            f.text(tx, ya - 22, nm, 12.5, INK, weight=700)
        # fios dos postes
        pc, pb = (xc, 108), (xb, 108)
        f.wire([(xc, ya + 4), pc])
        f.wire([(xb, ya + 4), pb])
        f.circ(pc[0], pc[1], 3.2, "#fff", INK, 1.7, tag="bg")
        f.circ(pb[0], pb[1], 3.2, "#fff", INK, 1.7, tag="bg")
        # alimentação
        sx, sy = x0 + 108, 150
        f.wire([(xa, ya + 4), (xa, sy), (sx - 16, sy)])
        f.circ(sx, sy, 14, "#fff", INK, 1.9, tag="bg")
        f.text(sx, sy + 4.5, "~", 16, INK, weight=700, lint=False)
        piv = (x0 + 160, sy)
        f.wire([(sx + 14, sy), piv])
        f.circ(piv[0], piv[1], 3.4, INK, INK, 1, tag="bg")
        if k == 0:
            f.line(piv[0], piv[1], piv[0] + 20, piv[1] - 24, INK, 2.4)
        elif k == 1:
            f.line(piv[0], piv[1], pb[0], pb[1], INK, 2.4)
        else:
            f.line(piv[0], piv[1], pc[0], pc[1], INK, 2.4)
        f.text(sx, sy + 27, "220 V", 11.5, INK, weight=600)
        notes = [("sem corrente", ""), ("$R=17{,}6\\ \\Omega$   $P=2750$ W", "fio todo (A→B): $R$ maior"),
                 ("$R=8{,}8\\ \\Omega$   $P=5500$ W", "só A→C: $R$ menor")][k]
        f.text(x0 + 106, 196, notes[0], 11.5, INK, weight=600)
        if notes[1]:
            f.text(x0 + 106, 210, notes[1], 10.5, MUTED)
    return f


@fig("ex_corrente")
def ex_corrente():
    f = Fig(332, 196, title="Exemplo 11: gráfico da corrente em função do tempo")
    P = Plot(f, 50, 160, 240, 112, (0, 5), (0, 7.5), xticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")],
             yticks=[(2, "2"), (4, "4"), (6, "6")], grid=True)
    P.axis_labels("$t$ (s)", "$I$ (A)", ydx=6)
    P.area([(0, 6), (2, 6)], 0, CUR, 0.16, None)
    P.area([(2, 6), (4, 0)], 0, CUR, 0.30, None)
    P.line([(0, 6), (2, 6), (4, 0)], CUR, 3.0)
    P.guide(x=2, y=6, c=GRY_M)
    f.text(P.X(1), P.Y(3), "$A_1=12$ C", 12, INK, halo=True)
    f.text(P.X(2.62), P.Y(1.6), "$A_2=6$ C", 12, INK, halo=True)
    f.text(166, 192, "área total = carga que atravessa a seção: $Q=A_1+A_2$", 11, MUTED)
    return f


@fig("consumo_barras")
def consumo_barras():
    f = Fig(332, 186, title="Consumo mensal de energia de alguns aparelhos (kWh)")
    rows = [("Chuveiro 5 500 W · 20 h/mês", 110), ("TV 120 W · 150 h/mês", 18), ("Ferro de passar 1 000 W · 10 h/mês", 10),
            ("Lâmpada LED 10 W · 150 h/mês", 1.5)]
    f.text(8, 14, "Energia consumida em um mês", 12, INK, anchor="start", weight=700)
    for k, (nm, v) in enumerate(rows):
        y = 40 + k * 36
        f.text(8, y, nm, 11, INK, anchor="start")
        L = max(3, v / 110 * 230)
        f.rect(8, y + 6, L, 14, ENE_L, ENE, 1.8, rx=3, tag="bg")
        f.rect(8, y + 6, L, 14, ENE, None, 0, rx=3, fop=0.35)
        f.text(8 + L + 6, y + 18, (f"{v:.0f}" if v >= 10 else f"{v:.1f}".replace(".", ",")) + " kWh", 11.5, ENE_D, anchor="start", weight=700)
    return f


@fig("ex_fio")
def ex_fio():
    f = Fig(332, 132, title="Exemplo 12: fio de cobre de 50 m com 1,6 mm de diâmetro")
    yc, r = 52, 14
    f.path(f"M30,{yc - r} L300,{yc - r} A{r * 0.45},{r} 0 0 1 300,{yc + r} L30,{yc + r} A{r * 0.45},{r} 0 0 1 30,{yc - r} Z", GRY, 1.8, "#E0C9B5", tag="bg")
    f.ell(300, yc, r * 0.45, r, "#C9A98C", GRY, 1.8, tag="bg")
    f.arrow(6, yc, 30, yc, CUR, 3.0, 10)
    f.arrow(300 + 8, yc, 326, yc, CUR, 3.0, 10)
    f.text(18, yc - 12, "$I$", 12.5, CUR_D, weight=600)
    f.arrow(30, 92, 300, 92, GRY, 1.1, 6, 0.4, both=True)
    f.text(165, 110, "comprimento $L=50$ m", 11.5, INK)
    f.text(165, 20, "$\\rho=1{,}7\\times10^{-8}\\ \\Omega\\cdot$m  ·  $d=1{,}6$ mm  ·  $I=5{,}0$ A", 11.5, INK)
    f.text(165, 126, "$A=\\pi r^2$,  $r=d/2$", 11, MUTED)
    return f


@fig("ex_tensao")
def ex_tensao():
    f = Fig(332, 128, title="Exemplo 15: o mesmo resistor em 127 V e em 220 V")
    rows = [("127 V (nominal)", 4400, "4 400 W"), ("220 V (por engano)", 13200, "13 200 W  (×3,0)")]
    f.text(8, 14, "Potência dissipada, com $R=3{,}67\\ \\Omega$", 12, INK, anchor="start", weight=700)
    for k, (nm, v, lb) in enumerate(rows):
        y = 40 + k * 40
        f.text(8, y, nm, 11, INK, anchor="start")
        L = v / 13200 * 190
        f.rect(8, y + 6, L, 15, ENE_L, ENE, 1.8, rx=3, tag="bg")
        f.rect(8, y + 6, L, 15, ENE, None, 0, rx=3, fop=0.35)
        f.text(8 + L + 6, y + 18, lb, 11.5, ENE_D if k == 0 else POS_D, anchor="start", weight=700)
    f.text(166, 122, "$P\\propto U^{2}$: tensão ×1,73 ⇒ potência ×3,0", 11, MUTED)
    return f
