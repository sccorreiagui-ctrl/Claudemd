"""Bloco D · página 20 — curva de solubilidade."""
from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]

T = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
KNO3 = [13.3, 20.9, 31.6, 45.8, 63.9, 85.5, 110, 138, 169, 202, 246]
KCL = [28.0, 31.2, 34.2, 37.2, 40.1, 42.6, 45.8, 48.3, 51.3, 54.0, 56.3]
NACL = [35.7, 35.8, 36.0, 36.3, 36.6, 37.0, 37.3, 37.8, 38.4, 39.0, 39.8]


@fig("d_curva_solub")
def _curva():
    W, H = 490, 262
    s = SVG(W, H, title="Curvas de solubilidade em água")
    ax = Axes(s, 52, 12, 372, 206, 0, 100, 0, 250)
    ax.frame(xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 50, 100, 150, 200, 250], xlabel="temperatura (°C)", ylabel=None,
             size=10.4)
    s.text(14, 118, "g de soluto / 100 g de água", 10.6, "middle", 600, INK, rot=-90)
    # regiões
    ax.polyline(list(zip(T, KNO3)), C["blue"], 3.2)
    ax.polyline(list(zip(T, KCL)), C["blue_m"], 2.6)
    ax.polyline(list(zip(T, NACL)), C["slate"], 2.6)
    # exceção (esquemática): dissolução exotérmica
    exo = [(t, 30 - 0.26 * t) for t in T]
    ax.polyline(exo, C["red"], 2.2, dash="5 3")
    for t, v in zip(T, KNO3):
        s.circle(ax.X(t), ax.Y(v), 2.6, fill="#fff", stroke=C["blue"], sw=1.4)
    # rótulos
    s.text(ax.X(100) + 6, ax.Y(246) + 4, "KNO_3", 11, "start", 800, C["blue_d"])
    s.text(ax.X(100) + 6, ax.Y(56.3) - 4, "KCl", 11, "start", 800, C["blue_d"])
    s.text(ax.X(100) + 6, ax.Y(39.8) + 8, "NaCl", 11, "start", 800, C["slate"])
    s.text(ax.X(100) + 6, ax.Y(4), "exceção", 10, "start", 800, C["red_d"])
    s.text(ax.X(100) + 6, ax.Y(4) + 11, "(esquema)", 9.2, "start", 600, C["red_d"])
    # regiões nomeadas
    s.text(ax.X(8), ax.Y(236), "acima da curva:", 10.4, "start", 800, C["red_d"])
    s.text(ax.X(8), ax.Y(236) + 12, "excesso de soluto", 10.4, "start", 600, C["red_d"])
    s.text(ax.X(8), ax.Y(236) + 24, "(corpo de fundo ou supersaturada)", 9.4, "start", 400, C["red_d"])
    s.text(ax.X(54), ax.Y(22), "abaixo da curva: INSATURADA", 10.4, "middle", 800, C["green_d"], halo="#fff")
    s.text(ax.X(26), ax.Y(172), "na curva:", 10, "start", 800, C["blue_d"])
    s.text(ax.X(26), ax.Y(172) + 11, "SATURADA", 10, "start", 800, C["blue_d"])
    s.line(ax.X(40), ax.Y(150), ax.X(47), ax.Y(76), C["blue"], 1.0)
    # exemplo de leitura: 60 -> 20 °C
    s.line(ax.X(60), ax.Y(0), ax.X(60), ax.Y(110), C["orange"], 1.4, dash="3 3")
    s.line(ax.X(20), ax.Y(0), ax.X(20), ax.Y(31.6), C["orange"], 1.4, dash="3 3")
    s.line(ax.X(20), ax.Y(110), ax.X(60), ax.Y(110), C["orange"], 1.4, dash="3 3")
    s.line(ax.X(20), ax.Y(31.6), ax.X(20) - 0, ax.Y(110), C["orange"], 2.2)
    s.text(ax.X(20) - 6, ax.Y(70), "≈ 78 g", 10.4, "end", 800, C["orange_d"], halo="#fff")
    s.text(ax.X(20) - 6, ax.Y(70) + 11, "precipitam", 9.6, "end", 700, C["orange_d"], halo="#fff")
    s.circle(ax.X(60), ax.Y(110), 4.4, fill=C["orange"])
    s.circle(ax.X(20), ax.Y(31.6), 4.4, fill=C["orange"])
    return s
