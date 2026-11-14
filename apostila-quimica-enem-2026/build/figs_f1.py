"""Bloco F · página 29 — cinética química."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
OD = C["orange_d"]


@fig("f_conc_tempo")
def _conc():
    W, H = 340, 224
    s = SVG(W, H, title="Concentração × tempo")
    ax = Axes(s, 48, 14, 272, 154, 0, 10, 0, 1.1)
    ax.frame(xticks=[], yticks=[], xlabel="tempo", ylabel=None, grid=False, size=10)
    s.text(14, 96, "concentração", 10.4, "middle", 800, INK, rot=-90)
    k = 0.42
    A = lambda t: math.exp(-k * t)
    B = lambda t: 1 - math.exp(-k * t)
    ax.polyline(ax.curve_fn(A, 0, 10), C["orange"], 3.2)
    ax.polyline(ax.curve_fn(B, 0, 10), C["blue"], 3.2)
    s.text(ax.X(9.3), ax.Y(A(9.3)) - 10, "[A] reagente", 10.4, "end", 800, OD, halo="#fff")
    s.text(ax.X(9.3), ax.Y(B(9.3)) - 9, "[B] produto", 10.4, "end", 800, C["blue_d"], halo="#fff")
    # tangentes em t=0.6 e t=4.5
    for t0, col in ((0.6, C["red"]), (4.5, C["red"])):
        y0 = A(t0)
        slope = -k * y0
        xa, xb = max(t0 - 1.2, 0), t0 + 1.8
        s.line(ax.X(xa), ax.Y(y0 + slope * (xa - t0)), ax.X(xb), ax.Y(y0 + slope * (xb - t0)), col, 1.8, dash="4 3")
        s.circle(ax.X(t0), ax.Y(y0), 3.8, fill="#fff", stroke=col, sw=1.8)
    s.text(ax.X(1.9), ax.Y(0.74), "tangente íngreme:", 9.4, "start", 800, C["red_d"])
    s.text(ax.X(1.9), ax.Y(0.74) + 11, "v grande no início", 9.4, "start", 800, C["red_d"])
    s.text(ax.X(5.4), ax.Y(0.36), "tangente suave:", 9.4, "start", 800, C["red_d"])
    s.text(ax.X(5.4), ax.Y(0.36) + 11, "v menor depois", 9.4, "start", 800, C["red_d"])
    s.text(W / 2 + 10, 216, "v = |Δ[X]| / Δt = inclinação (módulo) da curva", 10.2, "middle", 800, C["slate"])
    return s


@fig("f_energia_ativ")
def _energia():
    W, H = 380, 232
    s = SVG(W, H, title="Energia de ativação com e sem catalisador")
    ax = Axes(s, 40, 14, 328, 170, 0, 10, 0, 130)
    ax.frame(xticks=[], yticks=[], xlabel="caminho da reação", ylabel=None, grid=False, size=10)
    s.text(12, 104, "entalpia (energia)", 10.4, "middle", 800, INK, rot=-90)
    R, P = 52.0, 26.0

    def curve(peak, w=0.95, x0=4.6):
        def f(x):
            base = R + (P - R) / (1 + math.exp(-(x - x0) * 1.4))
            bump = (peak - max(R, base)) * math.exp(-((x - x0) / w) ** 2) if peak > R else 0
            return base + (peak - R) * math.exp(-((x - x0) / w) ** 2)
        return f
    f1, f2 = curve(118), curve(84)
    xs = [0.2 + i * 0.06 for i in range(160)]
    m1, m2 = max(f1(x) for x in xs), max(f2(x) for x in xs)
    ax.polyline(ax.curve_fn(f1, 0.2, 9.8, 160), C["orange"], 3.4)
    ax.polyline(ax.curve_fn(f2, 0.2, 9.8, 160), C["green"], 3.4, dash=None)
    # níveis
    s.line(ax.X(0.2), ax.Y(R), ax.X(2.6), ax.Y(R), C["slate_m"], 1.2, dash="3 3")
    s.line(ax.X(7.0), ax.Y(P), ax.X(9.8), ax.Y(P), C["slate_m"], 1.2, dash="3 3")
    s.text(ax.X(0.4), ax.Y(R) + 15, "reagentes", 10.6, "start", 800, C["slate"])
    s.text(ax.X(9.7), ax.Y(P) + 15, "produtos", 10.6, "end", 800, C["slate"])
    # ΔH
    s.arrow(ax.X(9.3), ax.Y(R), ax.X(9.3), ax.Y(P) - 2, C["red"], 2, 7)
    s.line(ax.X(8.9), ax.Y(R), ax.X(9.7), ax.Y(R), C["slate_m"], 1.2, dash="3 3")
    s.text(ax.X(9.15), ax.Y(40), "ΔH < 0", 10.2, "end", 800, C["red_d"])
    s.text(ax.X(9.15), ax.Y(40) + 11, "(exotérmica)", 9.2, "end", 700, C["red_d"])
    # Ea
    s.arrow(ax.X(2.2), ax.Y(R), ax.X(2.2), ax.Y(m1) + 2, OD, 2, 7)
    s.text(ax.X(2.05), ax.Y((R + m1) / 2) - 2, "E_a", 11, "end", 800, OD)
    s.text(ax.X(2.05), ax.Y((R + m1) / 2) + 10, "sem catalisador", 9, "end", 700, OD)
    s.arrow(ax.X(3.35), ax.Y(R), ax.X(3.35), ax.Y(m2) + 2, C["green"], 2, 7)
    s.text(ax.X(3.35) - 5, ax.Y((R + m2) / 2) + 4, "E_a'", 11, "end", 800, C["green_d"], halo="#fff")
    s.text(ax.X(4.7), ax.Y(m1) - 7, "complexo ativado", 10, "middle", 800, OD, halo="#fff")
    # legenda
    s.line(48, 225, 70, 225, C["orange"], 3.4)
    s.text(74, 228.5, "sem catalisador", 10, "start", 700, OD)
    s.line(170, 225, 192, 225, C["green"], 3.4)
    s.text(196, 228.5, "com catalisador (E_a menor, mesmo ΔH)", 10, "start", 700, C["green_d"])
    return s


@fig("f_enzima")
def _enzima():
    W, H = 330, 186
    s = SVG(W, H, title="Atividade de uma enzima em função da temperatura")
    ax = Axes(s, 44, 12, 262, 120, 0, 70, 0, 1.15)
    ax.frame(xticks=[0, 10, 20, 30, 40, 50, 60, 70], yticks=[], xlabel="temperatura (°C)", ylabel=None, grid=False, size=9.6)
    s.text(14, 74, "velocidade", 10, "middle", 800, INK, rot=-90)

    def enz(T):
        up = 1 / (1 + math.exp(-(T - 18) / 6))
        down = 1 / (1 + math.exp((T - 47) / 2.4))
        return up * down * 1.02
    ax.polyline(ax.curve_fn(enz, 0, 70, 160), C["green"], 3.2)
    ax.polyline(ax.curve_fn(lambda T: 0.012 * T + 0.05, 0, 70), C["slate_m"], 2.2, dash="5 3")
    s.text(ax.X(38), ax.Y(1.08), "ótimo ≈ 37 °C", 10, "middle", 800, C["green_d"], halo="#fff")
    s.text(ax.X(60), ax.Y(0.2) - 4, "desnaturação", 10, "middle", 800, C["red_d"])
    s.text(ax.X(53), ax.Y(1.04), "catalisador", 9.4, "start", 700, C["slate"])
    s.text(ax.X(53), ax.Y(1.04) + 10, "inorgânico", 9.4, "start", 700, C["slate"])
    s.text(W / 2, 176, "enzima: curva em sino (T e pH ótimos); catalisador comum: só aumenta com T", 9.4, "middle", 700, C["muted"])
    return s
