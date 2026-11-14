"""Bloco E · página 27 — ETA (fluxograma) e chuva ácida."""
import math
import random

from registry import fig
from svglib import SVG, C, tw
from figlib import chip_svg

INK = C["ink"]
GD = C["green_d"]


def _box(s, x, y, w, h, n, title, desc, kind):
    fill, stroke, col = ((C["orange_l"], C["orange"], C["orange_d"]) if kind == "q" else (C["blue_l"], C["blue"], C["blue_d"]))
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=9)
    s.circle(x + 13, y + 13, 9, fill=stroke)
    s.text(x + 13, y + 16.6, str(n), 10.6, "middle", 800, "#FFFFFF")
    s.text(x + 27, y + 17, title, 11, "start", 800, col)
    for i, ln in enumerate(desc):
        s.text(x + 8, y + 33 + i * 11.4, ln, 9.4, "start", 400, INK)


@fig("e_eta")
def _eta():
    W, H = 695, 224
    s = SVG(W, H, title="Fluxograma de uma estação de tratamento de água (ETA)")
    bw, bh, gap = 124, 76, 15
    r1 = [("Captação", ["gradeamento retém", "detritos grosseiros"], "f"),
          ("Coagulação", ["Al₂(SO₄)₃ + cal → Al(OH)₃", "gelatinoso retém partículas"], "q"),
          ("Floculação", ["agitação lenta junta as", "partículas em flocos"], "f"),
          ("Decantação", ["flocos densos sedimentam", "formando o lodo"], "f"),
          ("Filtração", ["areia e antracito retêm", "os flocos restantes"], "f")]
    r2 = [("Desinfecção", ["cloro: HClO oxida e", "elimina micro-organismos"], "q"),
          ("Correção de pH", ["cal ou soda ajustam o pH", "(evita corrosão)"], "q"),
          ("Fluoretação", ["adição de fluoreto", "(≈ 0,7 mg/L): cáries"], "q"),
          ("Reservatório", ["cloro residual protege", "a rede de distribuição"], "f")]
    y1, y2 = 8, 116
    for i, (t, d, k) in enumerate(r1):
        x = 4 + i * (bw + gap)
        d = [x_.replace("₂", "_2").replace("₄", "_4").replace("₃", "_3") for x_ in d]
        _box(s, x, y1, bw, bh, i + 1, t, [ln for ln in d], k)
        if i < 4:
            s.arrow(x + bw + 1, y1 + bh / 2, x + bw + gap - 1, y1 + bh / 2, C["slate"], 2, 7)
    for i, (t, d, k) in enumerate(r2):
        x = 4 + i * (bw + gap)
        _box(s, x, y2, bw, bh, i + 6, t, d, k)
        if i < 3:
            s.arrow(x + bw + 1, y2 + bh / 2, x + bw + gap - 1, y2 + bh / 2, C["slate"], 2, 7)
    # ligação linha 1 -> linha 2
    s.path(f"M{4 + 4 * (bw + gap) + bw / 2} {y1 + bh} L{4 + 4 * (bw + gap) + bw / 2} {y1 + bh + 16} L{4 + bw / 2} {y1 + bh + 16} L{4 + bw / 2} {y2 - 1}",
           stroke=C["slate"], sw=2)
    s.head(4 + bw / 2, y2 - 1, math.pi / 2, C["slate"], 7)
    # torneira
    tx = 4 + 4 * (bw + gap)
    s.text(tx + bw / 2, y2 + 24, "Torneira:", 11, "middle", 800, GD)
    s.text(tx + bw / 2, y2 + 38, "água potável", 11, "middle", 800, GD)
    s.arrow(4 + 3 * (bw + gap) + bw + 1, y2 + bh / 2, tx + 2, y2 + bh / 2, C["slate"], 2, 7)
    chip_svg(s, 110, H - 10, "etapa química (reação)", "orange", 9.4, padx=7, h=15)
    chip_svg(s, 270, H - 10, "etapa física (separação)", "blue", 9.4, padx=7, h=15)
    return s


@fig("e_chuva_acida")
def _chuva():
    W, H = 695, 186
    s = SVG(W, H, title="Formação e efeitos da chuva ácida")
    # fábrica
    s.rect(24, 98, 96, 58, fill=C["slate_m"], stroke=C["slate"], sw=1.5, rx=3)
    s.rect(40, 60, 18, 40, fill=C["slate"], rx=2)
    s.rect(78, 72, 14, 28, fill=C["slate"], rx=2)
    rnd = random.Random(3)
    for i in range(5):
        s.circle(52 + i * 15 + rnd.uniform(-2, 2), 52 - i * 6 + rnd.uniform(-2, 2), 8 + i * 1.5, fill="#CBD5E1", opacity=0.8)
    s.text(72, 174, "queima de combustíveis fósseis", 10, "middle", 800, INK)
    s.text(76, 13, "SO_2 · NO · NO_2", 10.4, "start", 800, C["orange_d"])
    s.arrow(142, 46, 222, 38, C["orange"], 2.4, 8)
    # nuvem
    for (cx, cy, r) in ((254, 48, 22), (286, 38, 26), (320, 46, 24), (348, 54, 18), (270, 62, 20), (308, 66, 20)):
        s.circle(cx, cy, r, fill="#E2E8F0", stroke="#CBD5E1", sw=1.2)
    s.text(300, 45, "H_2SO_4  HNO_3", 10.6, "middle", 800, C["red_d"])
    s.text(300, 59, "na água da nuvem", 9.2, "middle", 600, C["slate"])
    for k, x in enumerate((270, 294, 318, 342, 282, 330)):
        y = 98 + (k % 3) * 14
        s.path(f"M{x} {y} q-4 7 0 10 q4 -3 0 -10 Z", fill=C["blue"], opacity=0.9)
    s.text(306, 154, "chuva com pH < 5,6", 11, "middle", 800, C["red_d"])
    s.text(306, 167, "(chuva normal: pH ≈ 5,6, pelo CO_2)", 9.2, "middle", 600, C["muted"])
    s.arrow(366, 92, 404, 110, C["red"], 2.4, 8)
    # efeitos: três colunas
    s.path("M400 124 Q440 136 480 124 L480 150 L400 150 Z", fill="#9CC3F5")
    s.text(440, 164, "lagos acidificam", 9.8, "middle", 800, INK)
    s.text(440, 176, "(morte de peixes)", 9.4, "middle", 400, C["muted"])
    s.rect(519, 114, 22, 36, fill="#E2E8F0", stroke="#94A3B8", sw=1.4, rx=3)
    s.circle(530, 106, 8, fill="#E2E8F0", stroke="#94A3B8", sw=1.4)
    s.rect(511, 150, 38, 6, fill="#94A3B8", rx=2)
    s.text(530, 168, "mármore e calcário", 9.8, "middle", 800, INK)
    s.text(530, 180, "são corroídos", 9.4, "middle", 400, C["muted"])
    s.rect(630, 122, 6, 28, fill="#8A6A3C")
    s.circle(633, 110, 17, fill=C["green_m"], stroke=C["green"], sw=1.2)
    s.text(634, 168, "solo perde Ca^2+, Mg^2+", 9.8, "middle", 800, INK)
    s.text(634, 180, "e libera Al^3+ tóxico", 9.4, "middle", 400, C["muted"])
    return s
