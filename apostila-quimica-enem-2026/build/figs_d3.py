"""Bloco D · página 22 — ponte do mol."""
from registry import fig
from svglib import SVG, C, tw

INK = C["ink"]
SL = C["slate"]


def _node(s, x, y, w, h, t1, t2, fill, stroke, col):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=9)
    s.text(x + w / 2, y + h / 2 - 2, t1, 11.4, "middle", 800, col)
    s.text(x + w / 2, y + h / 2 + 11, t2, 9.8, "middle", 600, C["muted"])


@fig("d_ponte_mol")
def _ponte():
    W, H = 695, 218
    s = SVG(W, H, title="Ponte do mol")
    ys = [8, 60, 112, 164]
    left = [("massa de A", "m_A (g)", "÷ M_A"), ("gás A", "V_A (L)", "÷ V_m"),
            ("solução de A", "𝓜_A · V (L)", "𝓜 · V"), ("partículas de A", "N_A", "÷ 6,02·10^{23}")]
    right = [("massa de B", "m_B (g)", "× M_B"), ("gás B", "V_B (L)", "× V_m"),
             ("solução de B", "V = n_B / 𝓜_B", "÷ 𝓜_B"), ("partículas de B", "N_B", "× 6,02·10^{23}")]
    cA, cB = (252, 109), (443, 109)
    for (t1, t2, conv), y in zip(left, ys):
        _node(s, 6, y, 148, 44, t1, t2, C["slate_l"], C["slate_m"], INK)
        s.line(154, y + 22, cA[0] - 34, cA[1] + (y + 22 - cA[1]) * 0.28, C["slate"], 1.8)
        s.text(184, y + 14 + (0 if y < 109 else 10) - 0, conv, 9.8, "middle", 800, C["orange_d"], halo="#fff")
    for (t1, t2, conv), y in zip(right, ys):
        _node(s, 541, y, 148, 44, t1, t2, C["slate_l"], C["slate_m"], INK)
        s.arrow(cB[0] + 34, cB[1] + (y + 22 - cB[1]) * 0.28, 541, y + 22, C["slate"], 1.8, 7)
        s.text(512, y + 14 + (0 if y < 109 else 10), conv, 9.8, "middle", 800, C["orange_d"], halo="#fff")
    for (cx, cy), lab, sub in ((cA, "n_A", "mol de A"), (cB, "n_B", "mol de B")):
        s.circle(cx, cy, 33, fill=C["blue_l"], stroke=C["blue"], sw=2)
        s.text(cx, cy + 2, lab, 17, "middle", 800, C["blue_d"])
        s.text(cx, cy + 16, sub, 9.6, "middle", 600, C["blue_d"])
    s.arrow(cA[0] + 33, cA[1], cB[0] - 34, cB[1], C["orange"], 3, 11)
    s.text((cA[0] + cB[0]) / 2, cA[1] - 16, "× (b / a)", 14, "middle", 800, C["orange_d"])
    s.text((cA[0] + cB[0]) / 2, cA[1] + 18, "coeficientes da", 9.8, "middle", 700, C["orange_d"])
    s.text((cA[0] + cB[0]) / 2, cA[1] + 30, "equação balanceada", 9.8, "middle", 700, C["orange_d"])
    s.text(W / 2, 14, "a A + … → b B + …", 11, "middle", 700, C["muted"])
    return s
