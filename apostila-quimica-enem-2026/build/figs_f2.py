"""Bloco F · página 30 — equilíbrio químico."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
OD = C["orange_d"]


@fig("f_equil_graf")
def _eq():
    W, H = 695, 216
    s = SVG(W, H, title="Equilíbrio químico: concentração e velocidades em função do tempo")
    # painel 1: concentrações
    s.rect(3, 3, 340, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
    s.text(173, 19, "Concentração × tempo:  A ⇌ B", 11.4, "middle", 800, OD)
    ax = Axes(s, 48, 30, 270, 136, 0, 10, 0, 1.05)
    ax.frame(xticks=[], yticks=[], xlabel="tempo", ylabel=None, grid=False, size=10)
    s.text(18, 98, "concentração", 10, "middle", 800, INK, rot=-90)
    A = lambda t: 0.4 + 0.6 * math.exp(-0.85 * t)
    B = lambda t: 0.6 * (1 - math.exp(-0.85 * t))
    s.rect(ax.X(5.2), ax.Y(1.02), ax.X(10) - ax.X(5.2), ax.Y(0) - ax.Y(1.02), fill=C["blue_l"], opacity=0.7)
    ax.polyline(ax.curve_fn(A, 0, 10), C["orange"], 3.2)
    ax.polyline(ax.curve_fn(B, 0, 10), C["blue"], 3.2)
    s.line(ax.X(5.2), ax.Y(0), ax.X(5.2), ax.Y(1.02), C["slate"], 1.4, dash="4 3")
    s.text(ax.X(5.3), ax.Y(0.98), "equilíbrio atingido", 9.8, "start", 800, C["blue_d"])
    s.text(ax.X(5.3), ax.Y(0.98) + 11, "(concentrações constantes)", 9, "start", 700, C["blue_d"])
    s.text(ax.X(1.6), ax.Y(0.8), "[A]", 11, "start", 800, OD)
    s.text(ax.X(1.9), ax.Y(0.2), "[B]", 11, "start", 800, C["blue_d"])
    s.text(ax.X(9.8), ax.Y(0.6) - 7, "[B] = 0,6", 9.4, "end", 800, C["blue_d"])
    s.text(ax.X(9.8), ax.Y(0.4) + 14, "[A] = 0,4", 9.4, "end", 800, OD)
    s.text(173, 207, "constantes ≠ iguais: A e B não precisam ter o mesmo valor", 9.6, "middle", 700, C["muted"])
    # painel 2: velocidades
    s.rect(352, 3, 340, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
    s.text(522, 19, "Velocidades × tempo", 11.4, "middle", 800, OD)
    ax2 = Axes(s, 396, 30, 270, 136, 0, 10, 0, 1.05)
    ax2.frame(xticks=[], yticks=[], xlabel="tempo", ylabel=None, grid=False, size=10)
    s.text(366, 98, "velocidade", 10, "middle", 800, INK, rot=-90)
    vd = lambda t: A(t)
    vi = lambda t: 0.4 / 0.6 * B(t)
    s.rect(ax2.X(5.2), ax2.Y(1.02), ax2.X(10) - ax2.X(5.2), ax2.Y(0) - ax2.Y(1.02), fill=C["blue_l"], opacity=0.7)
    ax2.polyline(ax2.curve_fn(vd, 0, 10), C["orange"], 3.2)
    ax2.polyline(ax2.curve_fn(vi, 0, 10), C["blue"], 3.2, dash="6 3")
    s.line(ax2.X(5.2), ax2.Y(0), ax2.X(5.2), ax2.Y(1.02), C["slate"], 1.4, dash="4 3")
    s.text(ax2.X(1.6), ax2.Y(0.88), "v direta (A → B)", 9.8, "start", 800, OD)
    s.text(ax2.X(2.4), ax2.Y(0.1), "v inversa (B → A)", 9.8, "start", 800, C["blue_d"])
    s.text(ax2.X(7.6), ax2.Y(0.4) - 8, "v direta = v inversa", 9.8, "middle", 800, C["blue_d"])
    s.text(522, 207, "equilíbrio dinâmico: as duas reações continuam ocorrendo", 9.6, "middle", 700, C["muted"])
    return s


def _tube(s, cx, color, label, sub):
    s.rect(cx - 14, 24, 28, 82, fill=color, stroke=C["slate"], sw=2, rx=6)
    s.rect(cx - 14, 24, 28, 12, fill="#FFFFFF", opacity=0.55, rx=6)
    s.text(cx, 122, label, 10.4, "middle", 800, INK)
    s.text(cx, 134, sub, 9.2, "middle", 600, C["muted"])


@fig("f_tubos_no2")
def _tubos():
    W, H = 330, 150
    s = SVG(W, H, title="Equilíbrio NO2 / N2O4 e temperatura")
    s.text(W / 2, 14, "N_2O_4 (incolor) ⇌ 2 NO_2 (castanho)   ΔH > 0", 10.6, "middle", 800, OD)
    _tube(s, 60, "#F7EFE4", "gelo", "0 °C: pálido")
    _tube(s, 165, "#D9A86C", "ambiente", "25 °C: intermediário")
    _tube(s, 270, "#7A3E10", "água quente", "100 °C: escuro")
    s.arrow(92, 66, 134, 66, C["red"], 2.2, 7)
    s.arrow(196, 66, 238, 66, C["red"], 2.2, 7)
    s.text(113, 58, "↑T", 10, "middle", 800, C["red_d"])
    s.text(217, 58, "↑T", 10, "middle", 800, C["red_d"])
    return s


@fig("f_perturb")
def _perturb():
    W, H = 695, 150
    s = SVG(W, H, title="Perturbações do equilíbrio: leitura de gráficos")
    cw = W / 3
    titles = ["Adição de A no instante t₁", "↑ temperatura (direta endotérmica)", "Catalisador"]
    for i, t in enumerate(titles):
        x = i * cw
        s.rect(x + 3, 3, cw - 6, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + cw / 2, 18, t, 10.6, "middle", 800, OD)
    def mk(i):
        return Axes(s, i * cw + 30, 26, cw - 54, 80, 0, 10, 0, 1.0)
    # 1
    a = mk(0)
    a.frame(xticks=[], yticks=[], xlabel=None, ylabel=None, grid=False, size=9, arrows=True)
    t1 = 4.0
    A1 = lambda t: 0.4 if t < t1 else 0.55 + 0.45 * math.exp(-1.1 * (t - t1))
    B1 = lambda t: 0.6 if t < t1 else 0.85 - 0.25 * math.exp(-1.1 * (t - t1))
    ptsA = [(t / 20, A1(t / 20)) for t in range(0, 201)]
    ptsA = [(0, 0.4), (t1, 0.4), (t1, 0.95)] + [(t1 + k * 0.1, A1(t1 + k * 0.1)) for k in range(1, 60)]
    ptsB = [(0, 0.6), (t1, 0.6)] + [(t1 + k * 0.1, B1(t1 + k * 0.1)) for k in range(1, 60)]
    a.polyline(ptsA, C["orange"], 2.8)
    a.polyline(ptsB, C["blue"], 2.8)
    s.line(a.X(t1), a.Y(0), a.X(t1), a.Y(1.0), C["slate"], 1.2, dash="3 3")
    s.text(a.X(t1), a.Y(0) + 12, "t₁", 9.4, "middle", 800, C["slate"])
    s.text(a.x0 + a.w + 6, a.Y(0) + 12, "tempo", 9, "end", 600, C["muted"])
    s.text(a.X(9.9), a.Y(0.62), "[A]", 9.6, "end", 800, OD)
    s.text(a.X(9.9), a.Y(0.86) - 3, "[B]", 9.6, "end", 800, C["blue_d"])
    s.text(cw / 2, 132, "A sobe e é consumido;", 9.6, "middle", 700, C["slate"])
    s.text(cw / 2, 144, "[B] aumenta: desloca p/ direita", 9.6, "middle", 800, C["orange_d"])
    # 2
    b = mk(1)
    b.frame(xticks=[], yticks=[], xlabel=None, ylabel=None, grid=False, size=9, arrows=True)
    ta = 4.0
    A2 = lambda t: 0.4 if t < ta else 0.25 + 0.15 * math.exp(-0.9 * (t - ta))
    B2 = lambda t: 0.6 if t < ta else 0.75 - 0.15 * math.exp(-0.9 * (t - ta))
    b.polyline([(t / 10, A2(t / 10)) for t in range(0, 101)], C["orange"], 2.8)
    b.polyline([(t / 10, B2(t / 10)) for t in range(0, 101)], C["blue"], 2.8)
    s.line(b.X(ta), b.Y(0), b.X(ta), b.Y(1.0), C["slate"], 1.2, dash="3 3")
    s.text(b.X(ta), b.Y(0) + 12, "t₁", 9.4, "middle", 800, C["slate"])
    s.text(b.x0 + b.w + 6, b.Y(0) + 12, "tempo", 9, "end", 600, C["muted"])
    s.text(b.X(9.9), b.Y(0.25) + 12, "[A]", 9.6, "end", 800, OD)
    s.text(b.X(9.9), b.Y(0.75) - 4, "[B]", 9.6, "end", 800, C["blue_d"])
    s.text(cw + cw / 2, 132, "sem salto: muda K", 9.6, "middle", 700, C["slate"])
    s.text(cw + cw / 2, 144, "[B] aumenta; [A] diminui", 9.6, "middle", 800, C["orange_d"])
    # 3
    c = mk(2)
    c.frame(xticks=[], yticks=[], xlabel=None, ylabel=None, grid=False, size=9, arrows=True)
    c.polyline(c.curve_fn(lambda t: 0.6 * (1 - math.exp(-0.28 * t)), 0, 10), C["slate_m"], 2.6, dash="5 3")
    c.polyline(c.curve_fn(lambda t: 0.6 * (1 - math.exp(-0.95 * t)), 0, 10), C["green"], 2.8)
    s.text(c.X(5.2), c.Y(0.6) - 7, "mesmo patamar", 9.4, "middle", 800, C["green_d"])
    s.text(c.X(5.5), c.Y(0.22), "sem catalisador", 9.2, "start", 700, C["slate"])
    s.line(c.X(0.3), c.Y(0.94), c.X(1.3), c.Y(0.94), C["green"], 2.8)
    s.text(c.X(1.5), c.Y(0.94) + 3.2, "com catalisador", 9.2, "start", 700, C["green_d"])
    s.text(c.x0 + c.w + 6, c.Y(0) + 12, "tempo", 9, "end", 600, C["muted"])
    s.text(2 * cw + cw / 2, 132, "atinge o equilíbrio mais rápido;", 9.6, "middle", 700, C["slate"])
    s.text(2 * cw + cw / 2, 144, "não desloca nem muda K", 9.6, "middle", 800, C["orange_d"])
    return s
