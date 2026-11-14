"""Bloco F · página 32 — termoquímica."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
OD = C["orange_d"]


def _profile(s, x0, w, title, R, P, kind):
    top = 6
    s.rect(x0 + 2, top, w - 4, 190, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
    s.text(x0 + w / 2, top + 16, title, 11.4, "middle", 800, OD if kind == "exo" else C["blue_d"])
    ax = Axes(s, x0 + 36, top + 28, w - 64, 106, 0, 10, 0, 100)
    ax.frame(xticks=[], yticks=[], xlabel="caminho da reação", ylabel=None, grid=False, size=9.6)
    s.text(x0 + 12, top + 84, "entalpia (H)", 10, "middle", 800, INK, rot=-90)
    peak = max(R, P) + 30
    x0c = 5.0

    def f(x):
        base = R + (P - R) / (1 + math.exp(-(x - x0c) * 1.5))
        return base + (peak - (R + P) / 2) * math.exp(-((x - x0c) / 1.0) ** 2)
    col = C["orange"] if kind == "exo" else C["blue"]
    ax.polyline(ax.curve_fn(f, 0.2, 9.8, 160), col, 3.4)
    s.line(ax.X(0.2), ax.Y(R), ax.X(3.4), ax.Y(R), C["slate_m"], 1.2, dash="3 3")
    s.line(ax.X(6.6), ax.Y(P), ax.X(9.8), ax.Y(P), C["slate_m"], 1.2, dash="3 3")
    s.text(ax.X(0.5), ax.Y(R) - 6, "reagentes", 10.2, "start", 800, C["slate"])
    s.text(ax.X(9.7), ax.Y(P) - 6 if kind == "endo" else ax.Y(P) + 14, "produtos", 10.2, "end", 800, C["slate"])
    xm = 8.9
    s.arrow(ax.X(xm), ax.Y(R) if kind == "exo" else ax.Y(R), ax.X(xm), ax.Y(P), C["red"], 2.2, 8)
    s.line(ax.X(xm - 0.4), ax.Y(R), ax.X(xm + 0.4), ax.Y(R), C["slate_m"], 1.2, dash="3 3")
    sign = "<" if kind == "exo" else ">"
    s.text(ax.X(xm - 0.35), ax.Y((R + P) / 2) + 3, f"ΔH {sign} 0", 10.4, "end", 800, C["red_d"])
    s.text(x0 + w / 2, top + 182, ("libera calor: o ambiente esquenta" if kind == "exo" else "absorve calor: o ambiente esfria"), 10, "middle", 800, C["slate"])


@fig("f_endo_exo")
def _eex():
    W, H = 695, 204
    s = SVG(W, H, title="Reações exotérmica e endotérmica: gráficos de entalpia")
    _profile(s, 0, 347, "EXOTÉRMICA: H(produtos) < H(reagentes)", 74, 32, "exo")
    _profile(s, 348, 347, "ENDOTÉRMICA: H(produtos) > H(reagentes)", 32, 74, "endo")
    return s
