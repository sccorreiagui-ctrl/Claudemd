"""Bloco A · página 7 — solubilidade e miscibilidade."""
import math
import random

import numpy as np

from registry import fig
from svglib import SVG, C, Axes, tw
from figlib import pol, water, sphere_h, chip_svg

INK = C["ink"]
BLUED, AMBD = C["blue_d"], C["amber_d"]


def _beaker_path(cx, top, w, h, r=11):
    x1, x2 = cx - w / 2, cx + w / 2
    yb = top + h
    return (f"M{x1} {top} L{x1} {yb - r} Q{x1} {yb} {x1 + r} {yb} L{x2 - r} {yb} Q{x2} {yb} {x2} {yb - r} L{x2} {top}")


def _liquid(s, cx, top, w, h, y_from, color, r=11, opacity=1.0):
    x1, x2 = cx - w / 2, cx + w / 2
    yb = top + h
    d = (f"M{x1} {y_from} L{x1} {yb - r} Q{x1} {yb} {x1 + r} {yb} L{x2 - r} {yb} Q{x2} {yb} {x2} {yb - r} "
         f"L{x2} {y_from} Z")
    s.path(d, fill=color, opacity=opacity)


@fig("a_beakers")
def _beakers():
    W, H = 695, 154
    s = SVG(W, H, title="Miscibilidade: sal em água, óleo em água, óleo em gasolina")
    w, top, h = 132, 8, 82
    cxs = [100, 347, 594]
    rnd = random.Random(5)
    # 1. NaCl + água
    cx = cxs[0]
    _liquid(s, cx, top, w, h, top + 22, "#D3E4FA")
    for i in range(26):
        x = cx - w / 2 + 10 + rnd.random() * (w - 20)
        y = top + 30 + rnd.random() * (h - 40)
        if i % 2 == 0:
            s.circle(x, y, 3.2, fill="#B79DFB", stroke="#6D4BD0", sw=0.8)
        else:
            s.circle(x, y, 4.4, fill="#4FC083", stroke="#1F7A45", sw=0.8)
    # 2. óleo + água
    cx = cxs[1]
    _liquid(s, cx, top, w, h, top + 22, "#F8DE95")
    _liquid(s, cx, top, w, h, top + 52, "#D3E4FA")
    s.line(cx - w / 2, top + 52, cx + w / 2, top + 52, C["slate_m"], 1.2)
    s.text(cx, top + 41, "óleo", 11, "middle", 700, AMBD)
    s.text(cx, top + 72, "água", 11, "middle", 700, BLUED)
    # 3. óleo + gasolina
    cx = cxs[2]
    _liquid(s, cx, top, w, h, top + 22, "#FBEAB6")
    for i in range(22):
        x = cx - w / 2 + 10 + rnd.random() * (w - 20)
        y = top + 30 + rnd.random() * (h - 40)
        s.circle(x, y, 2.6, fill=C["amber"], opacity=0.55)
    for cx in cxs:
        s.path(_beaker_path(cx, top, w, h), stroke=C["slate"], sw=2.4)
        s.line(cx - w / 2 - 6, top, cx - w / 2 + 6, top, C["slate"], 2.4)
        s.line(cx + w / 2 - 6, top, cx + w / 2 + 6, top, C["slate"], 2.4)
    caps = [
        ("NaCl + água", "1 fase · íon–dipolo", BLUED),
        ("óleo + água", "2 fases · polar × apolar", C["slate"]),
        ("óleo + gasolina", "1 fase · apolar + apolar (London)", AMBD),
    ]
    for cx, (t1, t2, col) in zip(cxs, caps):
        s.text(cx, 108, t1, 12.2, "middle", 800, col)
        s.text(cx, 121, t2, 10.4, "middle", 600, C["muted"])
    s.text(cxs[0], 136, "miscível / solúvel", 10.4, "middle", 700, C["green_d"])
    s.text(cxs[1], 136, "imiscível: óleo (menos denso) flutua", 10.4, "middle", 700, C["red_d"])
    s.text(cxs[2], 136, "miscíveis", 10.4, "middle", 700, C["green_d"])
    return s


@fig("a_nacl_dissol")
def _nacl():
    W, H = 344, 182
    s = SVG(W, H, title="Dissolução do NaCl em água: íon–dipolo")
    # cristal
    gx, gy, d = 26, 60, 26
    for r in range(3):
        for c in range(3):
            x, y = gx + c * d, gy + r * d
            if (r + c) % 2 == 0:
                sphere_h(s, x, y, 8.2, "#B79DFB", "#6D4BD0", "+", "#fff", 11)
            else:
                sphere_h(s, x, y, 11, "#4FC083", "#1F7A45", "−", "#fff", 13)
    s.text(52, 138, "cristal de NaCl", 10.4, "middle", 700, INK)
    s.text(52, 150, "(retículo iônico)", 10, "middle", 400, C["muted"])
    s.arrow(96, 62, 122, 62, C["orange"], 2.2, 8)
    s.text(110, 48, "H_2O", 10.4, "middle", 700, BLUED)
    # íons hidratados
    def hydrated(cx, cy, cation):
        for phi in (-90, 0, 90, 180):
            ox, oy = pol(cx, cy, 34, phi)
            if cation:
                water(s, ox, oy, phi + 52.25, phi - 52.25, 0.68, False)
            else:
                # H voltado para o ânion
                water(s, ox, oy, phi + 180 + 52.25, phi + 180 - 52.25, 0.68, False)
        if cation:
            sphere_h(s, cx, cy, 8.8, "#B79DFB", "#6D4BD0", "+", "#fff", 12)
        else:
            sphere_h(s, cx, cy, 11.5, "#4FC083", "#1F7A45", "−", "#fff", 14)
    hydrated(192, 62, True)
    hydrated(284, 62, False)
    s.text(192, 116, "Na^+ hidratado", 10.6, "middle", 700, "#5B3FC0")
    s.text(192, 128, "O (δ−) voltado", 9.8, "middle", 400, C["muted"])
    s.text(192, 139, "para o cátion", 9.8, "middle", 400, C["muted"])
    s.text(284, 116, "Cl^- hidratado", 10.6, "middle", 700, C["green_d"])
    s.text(284, 128, "H (δ+) voltado", 9.8, "middle", 400, C["muted"])
    s.text(284, 139, "para o ânion", 9.8, "middle", 400, C["muted"])
    chip_svg(s, 196, 168, "interação íon–dipolo (camada de solvatação)", "blue", 10.4, padx=8, h=18)
    return s


@fig("a_o2_temp")
def _o2():
    W, H = 316, 206
    s = SVG(W, H, title="Solubilidade do O2 na água em função da temperatura")
    ax = Axes(s, 46, 14, 246, 150, 0, 45, 0, 18)
    ax.frame(xticks=[0, 10, 20, 30, 40], yticks=[0, 4, 8, 12, 16], xlabel="temperatura da água (°C)", ylabel=None,
             yfmt=str, size=10)
    s.text(14, 90, "O_2 dissolvido (mg/L)", 10.6, "middle", 600, INK, rot=-90)
    T = [0, 10, 20, 30, 40]
    S = [14.6, 11.3, 9.1, 7.6, 6.4]
    z = np.polyfit(T, S, 3)
    pts = [(t, float(np.polyval(z, t))) for t in np.linspace(0, 42, 60)]
    ax.polyline(pts, C["blue"], 3.0)
    for t, v in zip(T, S):
        s.circle(ax.X(t), ax.Y(v), 4.2, fill="#fff", stroke=C["blue"], sw=2)
        s.text(ax.X(t) + (12 if t == 0 else 0), ax.Y(v) - 8, str(v).replace(".", ","), 10, "middle", 700, BLUED, halo="#fff")
    s.line(ax.x0, ax.Y(5), ax.x0 + ax.w, ax.Y(5), C["red"], 1.5, dash="5 3")
    s.text(ax.x0 + ax.w - 2, ax.Y(5) + 12, "mínimo p/ vida aquática ≈ 5 mg/L", 9.8, "end", 700, C["red_d"])
    return s
