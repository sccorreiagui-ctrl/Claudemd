"""Bloco E · página 28 — efeito estufa, eutrofização e biomagnificação."""
import math
import random

from registry import fig
from svglib import SVG, C, tw
from figlib import chip_svg

INK = C["ink"]
GD = C["green_d"]


@fig("e_estufa")
def _estufa():
    W, H = 440, 176
    s = SVG(W, H, title="Efeito estufa")
    # atmosfera
    s.rect(4, 50, W - 8, 52, fill="#E6F0FD", stroke=C["blue_m"], sw=1.2, rx=6)
    s.text(12, 63, "atmosfera: CO_2, CH_4, N_2O, H_2O", 9.6, "start", 800, C["blue_d"])
    # superfície
    s.rect(4, 144, W - 8, 26, fill=C["green_m"], stroke=C["green"], sw=1.2, rx=6)
    s.text(W / 2, 161, "superfície da Terra (absorve luz e emite infravermelho)", 10, "middle", 800, GD)
    # sol
    s.circle(44, 22, 15, fill="#F6C945", stroke=C["amber"], sw=1.5)
    for k in range(10):
        a = k * 36
        s.line(44 + 19 * math.cos(math.radians(a)), 22 + 19 * math.sin(math.radians(a)),
               44 + 25 * math.cos(math.radians(a)), 22 + 25 * math.sin(math.radians(a)), C["amber"], 1.6)
    s.text(78, 14, "luz visível e UV", 9.8, "start", 800, C["amber_d"])
    s.text(78, 26, "atravessam", 9.8, "start", 800, C["amber_d"])
    for x0, x1 in ((70, 108), (94, 132), (118, 156)):
        s.arrow(x0 + 38, 40, x1 + 30, 142, "#F2A81A", 2.6, 8)
    # IV emitido
    for x in (210, 262, 314):
        s.path(f"M{x} 142 q6 -10 0 -20 t0 -20", stroke=C["red"], sw=2.2)
        s.head(x, 102, -math.pi / 2, C["red"], 7)
    s.text(238, 136, "radiação infravermelha (calor)", 9.6, "middle", 800, C["red_d"], halo="#FFFFFF")
    # IV retido: setas de volta
    for (x, y0, y1, xo) in ((200, 80, 134, 176), (286, 80, 134, 306), (356, 78, 134, 380)):
        s.arrow(x, y0, xo, y1, C["orange"], 2.2, 7)
    s.text(360, 112, "reemitido p/ baixo", 9.4, "middle", 800, C["orange_d"], halo="#fff")
    # escape
    s.arrow(424, 120, 424, 8, C["red"], 2, 7, dash="4 3")
    s.text(418, 32, "escapa", 9.4, "end", 800, C["red_d"])
    s.text(418, 44, "p/ o espaço", 9.4, "end", 800, C["red_d"])
    # moléculas no band
    for (x, y) in ((190, 82), (232, 90), (300, 80), (338, 90)):
        s.circle(x, y, 5, fill="#4B5563", stroke="#1F2937", sw=1)
        s.circle(x - 8, y + 1, 3.8, fill="#E5484D", stroke="#9B1C22", sw=1)
        s.circle(x + 8, y + 1, 3.8, fill="#E5484D", stroke="#9B1C22", sw=1)
    return s


@fig("e_eutrof")
def _eutrof():
    W, H = 695, 150
    s = SVG(W, H, title="Eutrofização: etapas")
    cw = W / 4
    titles = ["1 · Lago equilibrado", "2 · Excesso de N e P", "3 · Algas morrem e se decompõem", "4 · Hipóxia: peixes morrem"]
    rnd = random.Random(4)
    for i, t in enumerate(titles):
        x = i * cw
        s.rect(x + 3, 3, cw - 6, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + cw / 2, 18, t, 10, "middle", 800, GD)
        top, bot = 34, 106
        # água
        wcol = ["#C7DEFA", "#A7D6B5", "#C9D6B0", "#B6A98E"][i]
        s.rect(x + 12, top, cw - 24, bot - top, fill=wcol, stroke=C["blue_m"], sw=1.1, rx=6)
        # algas na superfície
        if i >= 1:
            for k in range(14 if i == 1 else 8):
                s.circle(x + 18 + k * (cw - 36) / (14 if i == 1 else 8), top + 4 + rnd.uniform(-1, 3), 3.6,
                         fill="#3DAA5C" if i < 3 else "#7A8B3C", opacity=0.95)
        # bolhas de O2 (menos a cada etapa)
        nb = [8, 6, 3, 0][i]
        for k in range(nb):
            s.circle(x + 24 + rnd.uniform(0, cw - 56), top + 14 + rnd.uniform(0, 44), 2.2, fill="#FFFFFF", stroke=C["blue"], sw=0.9)
        # peixes
        def fish(fx, fy, dead=False):
            col = "#F28C28" if not dead else "#9AA3AF"
            s.ellipse(fx, fy, 9, 4.6, fill=col, rot=0 if not dead else 180)
            s.poly([(fx + 8, fy), (fx + 14, fy - 4), (fx + 14, fy + 4)], fill=col)
        if i <= 1:
            fish(x + 40, top + 40); fish(x + 90, top + 52)
        if i == 2:
            fish(x + 44, top + 48)
        if i == 3:
            fish(x + 40, top + 14, True); fish(x + 90, top + 20, True)
        s.text(x + cw / 2, 124, ["O_2 alto · DBO baixa", "algas proliferam", "DBO alta · O_2 cai", "O_2 ≈ 0 (anoxia)"][i], 10, "middle", 800,
               [C["green_d"], C["orange_d"], C["red_d"], C["red_d"]][i])
        s.text(x + cw / 2, 137, ["luz chega ao fundo", "bloqueiam a luz", "decomposição aeróbia", "H_2S e CH_4 (odor)"][i], 9.2, "middle", 400, C["muted"])
    return s


@fig("e_biomag")
def _biomag():
    W, H = 440, 168
    s = SVG(W, H, title="Biomagnificação ao longo da cadeia alimentar")
    levels = [("água", "1", 0.1), ("fitoplâncton", "10^4", 0.34), ("peixe pequeno", "10^5", 0.5),
              ("peixe grande", "10^6", 0.72), ("ave piscívora / humano", "10^7", 0.95)]
    y = 10
    for k, (nm, val, f) in enumerate(levels):
        w = 30 + f * 190
        s.rect(130, y, w, 22, fill=C["green"], opacity=0.25 + 0.15 * k, rx=4)
        s.rect(130, y, w, 22, stroke=C["green"], sw=1.2, rx=4)
        s.text(122, y + 15, nm, 10.2, "end", 700, INK)
        s.text(130 + w + 6, y + 15, val + "×", 11, "start", 800, GD)
        y += 28
    s.arrow(424, 142, 424, 10, C["red"], 2.4, 8)
    s.text(418, 80, "níveis tróficos", 9.2, "middle", 700, C["red_d"], rot=-90)
    s.text(132, 160, "concentração relativa do poluente (valores ilustrativos, ordem de grandeza)", 9.2, "start", 600, C["muted"])
    return s
