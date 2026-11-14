"""Bloco D · página 23 — reagente limitante (diagrama de partículas)."""
from registry import fig
from svglib import SVG, C

INK = C["ink"]


def _h2(s, x, y, rot=0):
    s.circle(x - 5.2, y, 5.6, fill="#FFFFFF", stroke="#6B7280", sw=1.3)
    s.circle(x + 5.2, y, 5.6, fill="#FFFFFF", stroke="#6B7280", sw=1.3)


def _o2(s, x, y):
    s.circle(x - 6.5, y, 7.6, fill="#E5484D", stroke="#9B1C22", sw=1.3)
    s.circle(x + 6.5, y, 7.6, fill="#E5484D", stroke="#9B1C22", sw=1.3)


def _h2o(s, x, y):
    s.circle(x - 9, y + 8, 4.8, fill="#FFFFFF", stroke="#6B7280", sw=1.2)
    s.circle(x + 9, y + 8, 4.8, fill="#FFFFFF", stroke="#6B7280", sw=1.2)
    s.circle(x, y, 7.8, fill="#E5484D", stroke="#9B1C22", sw=1.3)


@fig("d_limitante")
def _lim():
    W, H = 695, 150
    s = SVG(W, H, title="Reagente limitante: diagrama de partículas")
    # ANTES
    s.rect(6, 4, 300, 142, fill=C["slate_l"], stroke=C["slate_m"], sw=1.3, rx=10)
    s.text(156, 21, "ANTES: 6 H_2 + 2 O_2", 11.6, "middle", 800, C["slate"])
    for i in range(6):
        _h2(s, 38 + (i % 3) * 52, 50 + (i // 3) * 32)
    for i in range(2):
        _o2(s, 218, 56 + i * 36)
    s.text(90, 130, "6 H_2", 10.4, "middle", 700, C["slate"])
    s.text(218, 130, "2 O_2 (poucas moléculas)", 10, "middle", 700, C["red_d"])
    # seta
    s.arrow(314, 76, 380, 76, C["orange"], 3, 11)
    s.text(347, 64, "2 H_2 + O_2", 10, "middle", 800, C["orange_d"])
    s.text(347, 96, "→ 2 H_2O", 10, "middle", 800, C["orange_d"])
    # DEPOIS
    s.rect(388, 4, 301, 142, fill=C["blue_l"], stroke=C["blue_m"], sw=1.3, rx=10)
    s.text(538, 21, "DEPOIS: 4 H_2O + 2 H_2 (sobram)", 11.6, "middle", 800, C["blue_d"])
    for i in range(4):
        _h2o(s, 420 + (i % 2) * 54, 46 + (i // 2) * 38)
    for i in range(2):
        _h2(s, 566, 52 + i * 32)
    s.text(448, 130, "4 H_2O formadas", 10.4, "middle", 700, C["blue_d"])
    s.text(584, 130, "excesso: sobram 2 H_2", 10, "middle", 700, C["red_d"])
    s.rect(622, 32, 62, 84, fill="#FFFFFF", stroke=C["red_m"], sw=1.2, rx=8)
    s.text(653, 50, "O_2 acabou:", 9.4, "middle", 800, C["red_d"])
    s.text(653, 63, "é o reagente", 9.4, "middle", 700, C["red_d"])
    s.text(653, 76, "LIMITANTE", 10, "middle", 800, C["red_d"])
    s.text(653, 94, "H_2: em", 9.4, "middle", 700, C["slate"])
    s.text(653, 106, "EXCESSO", 10, "middle", 800, C["slate"])
    return s
