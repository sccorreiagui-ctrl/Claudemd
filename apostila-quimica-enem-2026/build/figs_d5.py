"""Bloco D · página 24 — gases (transformações) e propriedades coligativas."""
import math
import random

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
BD = C["blue_d"]


@fig("d_gases_graf")
def _gases():
    W, H = 695, 188
    s = SVG(W, H, title="Transformações gasosas")
    cw = W / 3
    titles = [("Isotérmica (T constante)", "lei de Boyle: P · V = constante"),
              ("Isobárica (P constante)", "lei de Charles: V / T = constante"),
              ("Isocórica ou isovolumétrica (V constante)", "lei de Gay-Lussac: P / T = constante")]
    for i, (t, sub) in enumerate(titles):
        x = i * cw
        s.rect(x + 3, 3, cw - 6, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + cw / 2, 19, t, 10.6, "middle", 800, INK)
        s.text(x + cw / 2, H - 10, sub, 10, "middle", 700, C["orange_d"])
    # 1 hipérbole
    ax = Axes(s, 34, 30, 164, 100, 0, 10, 0, 10)
    ax.frame(xticks=[], yticks=[], xlabel="V", ylabel=None, grid=False, size=10)
    s.text(22, 82, "P", 11, "middle", 800, INK)
    pts = [(v, 10 / v) for v in [0.9 + k * 0.1 for k in range(0, 92)]]
    pts = [(v, p) for v, p in pts if p <= 10 and v <= 10]
    ax.polyline(pts, C["blue"], 3.0)
    ax.polyline([(v, 5 / v * 1.0) for v in [0.5 + k * 0.1 for k in range(0, 96)] if 5 / v <= 10][::1], C["blue_m"], 2.2, dash="4 3")
    s.text(ax.X(8.5), ax.Y(2.7), "T_1 > T_2", 9.4, "middle", 700, C["blue_d"])
    # 2 reta V x T
    ax2 = Axes(s, cw + 34, 30, 164, 100, 0, 10, 0, 10)
    ax2.frame(xticks=[], yticks=[], xlabel="T (K)", ylabel=None, grid=False, size=10)
    s.text(cw + 22, 82, "V", 11, "middle", 800, INK)
    ax2.polyline([(0, 0), (9.4, 9.0)], C["blue"], 3.0)
    s.circle(ax2.X(0), ax2.Y(0), 3.4, fill="#fff", stroke=C["red"], sw=1.8)
    s.text(ax2.X(0) + 6, ax2.Y(0) - 6, "0 K", 9.4, "start", 700, C["red_d"])
    # 3 reta P x T
    ax3 = Axes(s, 2 * cw + 34, 30, 164, 100, 0, 10, 0, 10)
    ax3.frame(xticks=[], yticks=[], xlabel="T (K)", ylabel=None, grid=False, size=10)
    s.text(2 * cw + 22, 82, "P", 11, "middle", 800, INK)
    ax3.polyline([(0, 0), (9.4, 9.0)], C["blue"], 3.0)
    s.circle(ax3.X(0), ax3.Y(0), 3.4, fill="#fff", stroke=C["red"], sw=1.8)
    s.text(ax3.X(0) + 6, ax3.Y(0) - 6, "0 K", 9.4, "start", 700, C["red_d"])
    return s


@fig("d_coligativas")
def _colig():
    W, H = 340, 236
    s = SVG(W, H, title="Efeito coligativo no diagrama de fases da água (exagerado)")
    ax = Axes(s, 40, 28, 284, 150, -26, 112, 0, 1.4)
    ax.frame(xticks=[0, 100], yticks=[1.0], xlabel="temperatura (°C)", ylabel=None, grid=False, size=10,
             xfmt=lambda v: str(v), yfmt=lambda v: "1 atm")
    s.text(14, 104, "pressão", 10.4, "middle", 800, INK, rot=-90)
    s.line(ax.X(-26), ax.Y(1.0), ax.X(112), ax.Y(1.0), C["slate_m"], 1.2, dash="4 3")

    def pv(T, Tb):
        return math.exp(0.034 * (T - Tb))
    pure = [(T, pv(T, 100)) for T in range(10, 113, 2) if pv(T, 100) <= 1.38]
    sol = [(T, pv(T, 108)) for T in range(18, 113, 2) if pv(T, 108) <= 1.38]
    ax.polyline(pure, C["blue"], 3.0)
    ax.polyline(sol, C["orange"], 3.0)
    ax.polyline([(0.0, 0.0), (0.0, 1.38)], C["blue"], 3.0)
    ax.polyline([(-10.0, 0.0), (-10.0, 1.38)], C["orange"], 3.0)
    for (t, col) in ((0, C["blue"]), (100, C["blue"]), (-10, C["orange"]), (108, C["orange"])):
        s.circle(ax.X(t), ax.Y(1.0), 4.4, fill=col, stroke="#fff", sw=1.4)
    s.arrow(ax.X(100) + 5, ax.Y(1.17), ax.X(108) - 2, ax.Y(1.17), C["red"], 2, 6)
    s.text(ax.X(104), ax.Y(1.17) - 11, "↑ P.E.", 10, "middle", 800, C["red_d"], halo="#fff")
    s.arrow(ax.X(0) - 5, ax.Y(1.17), ax.X(-10) + 2, ax.Y(1.17), C["red"], 2, 6)
    s.text(ax.X(-5), ax.Y(1.17) - 11, "↓ P.F.", 10, "middle", 800, C["red_d"], halo="#fff")
    s.text(ax.X(-18), ax.Y(0.55), "sólido", 10.4, "middle", 800, C["slate"])
    s.text(ax.X(30), ax.Y(0.2), "líquido", 11, "middle", 800, C["blue_d"])
    s.text(ax.X(88), ax.Y(0.2), "gás", 11, "middle", 800, C["slate"])
    ly = H - 24
    s.line(46, ly, 68, ly, C["blue"], 3)
    s.text(72, ly + 3.6, "solvente puro", 10, "start", 700, C["blue_d"])
    s.line(172, ly, 194, ly, C["orange"], 3)
    s.text(198, ly + 3.6, "solução (soluto não volátil)", 10, "start", 700, C["orange_d"])
    s.text(W / 2, H - 6, "esquema: deslocamentos exagerados", 9, "middle", 400, C["muted"])
    return s


def _utube(s, x0, title, mode):
    """U com membrana: mode 'osmose' ou 'reversa'. x0 = canto esquerdo (largura 160)."""
    w, h = 160, 104
    top = 38
    s.text(x0 + w / 2, 14, title, 11, "middle", 800, INK)
    mid = x0 + w / 2
    lvl_l, lvl_r = (top + 40, top + 22) if mode == "osmose" else (top + 22, top + 44)
    # compartimentos
    s.path(f"M{x0} {top} L{x0} {top + h} L{x0 + w} {top + h} L{x0 + w} {top}", stroke=C["slate"], sw=2.4)
    s.rect(x0 + 1.2, lvl_l, w / 2 - 2.2, top + h - lvl_l - 1.2, fill="#D3E4FA")
    s.rect(mid + 1, lvl_r, w / 2 - 2.2, top + h - lvl_r - 1.2, fill="#9CC3F5")
    rnd = random.Random(5)
    for _ in range(9):
        s.circle(rnd.uniform(mid + 10, x0 + w - 10), rnd.uniform(lvl_r + 8, top + h - 8), 2.8, fill="#B79DFB", stroke="#6D4BD0", sw=0.8)
    # membrana semipermeável
    s.line(mid, top + 20, mid, top + h, C["slate"], 2.2, dash="3 3")
    s.text(mid, top + h + 13, "membrana semipermeável", 9, "middle", 600, C["muted"])
    s.text(x0 + w * 0.25, top + 14, "solvente puro", 9.2, "middle", 700, C["blue_d"])
    s.text(x0 + w * 0.75, top + 14, "solução", 9.2, "middle", 700, C["blue_d"])
    if mode == "osmose":
        s.arrow(mid - 22, top + 70, mid + 22, top + 70, C["orange"], 2.6, 8)
        s.text(mid, top + 58, "H_2O", 10, "middle", 800, C["orange_d"], halo="#D3E4FA")
        s.line(x0 + w - 4, lvl_l, x0 + w + 6, lvl_l, C["red"], 1.4, dash="2 2")
        s.line(x0 + w, lvl_r, x0 + w + 12, lvl_r, C["red"], 1.4)
        s.text(x0 + w + 8, (lvl_l + lvl_r) / 2 + 3, "π", 11, "start", 800, C["red_d"])
    else:
        s.arrow(mid + 22, top + 70, mid - 22, top + 70, C["green"], 2.6, 8)
        s.text(mid, top + 58, "H_2O", 10, "middle", 800, C["green_d"], halo="#D3E4FA")
        s.arrow(x0 + w * 0.75, top - 18, x0 + w * 0.75, lvl_r - 6, C["red"], 3, 9)
        s.text(x0 + w * 0.75 - 8, top - 8, "P > π", 10, "end", 800, C["red_d"])


@fig("d_osmose")
def _osmose():
    W, H = 360, 168
    s = SVG(W, H, title="Osmose e osmose reversa")
    _utube(s, 8, "Osmose (espontânea)", "osmose")
    _utube(s, 188, "Osmose reversa (pressão externa)", "reversa")
    return s
