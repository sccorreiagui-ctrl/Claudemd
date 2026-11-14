"""Bloco E · página 26 — destilação simples × fracionada e torre de petróleo."""
import math

from registry import fig
from svglib import SVG, C, tw

INK = C["ink"]
GD = C["green_d"]
GLASS = "#5B6575"
LIQ = "#9CC3F5"


def _flask(s, cx, cy, r, level_dy=-4, liquid=LIQ):
    d = level_dy
    w = math.sqrt(max(r * r - d * d, 1))
    s.path(f"M{cx - w:.1f} {cy + d} A{r} {r} 0 1 0 {cx + w:.1f} {cy + d} Z", fill=liquid, opacity=0.95)
    # contorno (círculo + gargalo)
    s.circle(cx, cy, r, stroke=GLASS, sw=2.2)


def _flame(s, x, y, k=1.0):
    s.path(f"M{x} {y} C{x - 9 * k} {y - 8 * k} {x - 5 * k} {y - 18 * k} {x} {y - 26 * k} C{x + 5 * k} {y - 18 * k} {x + 9 * k} {y - 8 * k} {x} {y} Z",
           fill=C["orange"], opacity=0.95)
    s.path(f"M{x} {y} C{x - 4 * k} {y - 4 * k} {x - 2 * k} {y - 10 * k} {x} {y - 14 * k} C{x + 2 * k} {y - 10 * k} {x + 4 * k} {y - 4 * k} {x} {y} Z",
           fill="#FDE68A")


def _leader(s, x1, y1, x2, y2, text, anchor="start", col=INK, size=10, dy=3.5):
    s.line(x1, y1, x2, y2, C["slate_m"], 1.0)
    s.text(x2 + (4 if anchor == "start" else -4), y2 + dy, text, size, anchor, 700, col)


def _condenser(s, x1, y1, x2, y2, tube=10):
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = math.hypot(x2 - x1, y2 - y1)
    s.raw(f'<g transform="translate({x1} {y1}) rotate({ang:.2f})">'
          f'<rect x="0" y="-{tube}" width="{L:.1f}" height="{2 * tube}" rx="3" fill="#D3E4FA" stroke="{GLASS}" stroke-width="2"/>'
          f'<rect x="-4" y="-2.6" width="{L + 8:.1f}" height="5.2" rx="2" fill="#FFFFFF" stroke="{GLASS}" stroke-width="1.6"/></g>')


def _apparatus(s, x0, fractional):
    fx, fy, r = x0 + 58, 160, 30
    _flame(s, fx, fy + r + 26, 0.95)
    s.rect(fx - 22, fy + r + 26, 44, 5, fill=C["slate_m"], rx=2)
    _flask(s, fx, fy, r)
    neck_top = 52 if fractional else 92
    s.rect(fx - 7, neck_top, 14, fy - r + 4 - neck_top, fill="#FFFFFF", stroke=GLASS, sw=2)
    if fractional:
        for k in range(5):
            yy = neck_top + 4 + k * 14.5
            s.line(fx - 7, yy, fx + 7, yy + 7, GLASS, 1.2)
            s.line(fx + 7, yy + 7, fx - 7, yy + 14.5, GLASS, 1.2)
        side_y = neck_top + 10
        s.text(fx - 14, neck_top + 14, "↓T", 10, "end", 800, C["blue_d"])
        s.text(fx - 14, fy - r - 6, "↑T", 10, "end", 800, C["red_d"])
    else:
        side_y = neck_top + 14
    # rolha + termômetro
    s.rect(fx - 8, neck_top - 6, 16, 8, fill="#8A6A3C", rx=2)
    s.line(fx, neck_top - 20, fx, side_y + 4, C["red"], 2.4)
    s.circle(fx, side_y + 6, 3.2, fill=C["red"])
    s.text(fx + 12, neck_top - 12, "termômetro", 9.6, "start", 700, INK)
    # braço lateral + condensador
    cx1, cy1 = fx + 34, side_y + 12
    s.line(fx + 7, side_y, cx1, cy1, GLASS, 3.2)
    cx2, cy2 = x0 + 204, 172
    _condenser(s, cx1, cy1, cx2, cy2)
    # água do condensador: entra por baixo, sai por cima
    ang = math.atan2(cy2 - cy1, cx2 - cx1)
    ux, uy = cx1 + (cx2 - cx1) * 0.12, cy1 + (cy2 - cy1) * 0.12
    s.arrow(ux, uy - 12, ux, uy - 32, C["blue"], 2, 6)
    s.text(ux + 6, uy - 28, "H_2O sai", 9.4, "start", 700, C["blue_d"])
    lx, ly = cx1 + (cx2 - cx1) * 0.88, cy1 + (cy2 - cy1) * 0.88
    s.arrow(lx, ly + 34, lx, ly + 14, C["blue"], 2, 6)
    s.text(lx - 8, ly + 42, "H_2O entra", 9.4, "end", 700, C["blue_d"])
    # coletor (erlenmeyer)
    ex, ey = cx2 + 16, cy2 + 6
    s.path(f"M{ex - 5} {ey} L{ex - 5} {ey + 12} L{ex - 20} {ey + 40} L{ex + 20} {ey + 40} L{ex + 5} {ey + 12} L{ex + 5} {ey}", stroke=GLASS, sw=2)
    s.path(f"M{ex - 13} {ey + 28} L{ex + 13} {ey + 28} L{ex + 20} {ey + 40} L{ex - 20} {ey + 40} Z", fill="#D3E4FA", opacity=0.95)
    s.text(ex, ey + 54, "destilado", 9.8, "middle", 800, GD)
    s.text(fx, fy + r + 44, "mistura aquecida", 9.6, "middle", 700, C["slate"])


@fig("e_destil3")
def _destil():
    W, H = 695, 262
    s = SVG(W, H, title="Destilação simples, fracionada e torre de petróleo")
    # painéis
    s.rect(3, 3, 258, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=10)
    s.rect(265, 3, 258, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=10)
    s.rect(527, 3, 165, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=10)
    s.text(132, 19, "Destilação SIMPLES", 11.6, "middle", 800, GD)
    s.text(394, 19, "Destilação FRACIONADA", 11.6, "middle", 800, GD)
    _apparatus(s, 4, False)
    _apparatus(s, 266, True)
    # legenda breve
    s.text(132, 245, "P.E. muito diferentes ou soluto não volátil", 9.4, "middle", 700, C["slate"])
    s.text(132, 257, "(água do mar, salmoura)", 9.2, "middle", 400, C["muted"])
    s.text(394, 245, "líquidos miscíveis, P.E. próximos", 9.4, "middle", 700, C["slate"])
    s.text(394, 257, "(etanol + água, petróleo, ar líquido)", 9.2, "middle", 400, C["muted"])
    # torre de petróleo
    tx, tw_ = 548, 36
    g = s.lingrad([(0, "#FDE8D6"), (1, "#F2A15C")], 0, 0, 0, 1)
    s.rect(tx, 34, tw_, 150, fill=g, stroke=GLASS, sw=2, rx=6)
    s.text(609, 19, "Torre de petróleo", 11.6, "middle", 800, GD)
    fr = [("gases (GLP): < 40 °C", 46), ("gasolina: 40–200 °C", 70), ("querosene: 175–275 °C", 98),
          ("diesel: 250–375 °C", 126), ("óleos pesados e resíduo", 160)]
    for (t, y) in fr:
        s.line(tx, y, tx + tw_, y, GLASS, 1.2)
        s.line(tx + tw_, y - 8 if y > 50 else y, tx + tw_ + 10, y - 8 if y > 50 else y, GLASS, 1.4)
        s.text(tx + tw_ + 14, (y - 8 if y > 50 else y) + 3.4, t, 9.2, "start", 700, INK)
    s.text(tx + tw_ / 2, 44, "frio", 8.6, "middle", 700, C["blue_d"])
    s.text(tx + tw_ / 2, 178, "quente", 8.6, "middle", 700, C["red_d"])
    _flame(s, tx + tw_ / 2 - 8, 214, 1.0)
    _flame(s, tx + tw_ / 2 + 10, 214, 0.9)
    s.text(609, 232, "petróleo aquecido na base", 9.2, "middle", 700, C["slate"])
    s.text(609, 245, "separa por faixas de P.E.", 9.4, "middle", 700, C["slate"])
    s.text(609, 257, "(valores aproximados)", 9.2, "middle", 400, C["muted"])
    return s


@fig("e_cromato")
def _cromato():
    W, H = 300, 166
    s = SVG(W, H, title="Cromatografia em papel")
    cx = 110
    # béquer com solvente
    s.path(f"M{cx - 60} 60 L{cx - 60} 150 Q{cx - 60} 160 {cx - 50} 160 L{cx + 50} 160 Q{cx + 60} 160 {cx + 60} 150 L{cx + 60} 60", stroke=C["slate"], sw=2.2)
    s.path(f"M{cx - 59} 138 L{cx - 59} 150 Q{cx - 59} 159 {cx - 50} 159 L{cx + 50} 159 Q{cx + 59} 159 {cx + 59} 150 L{cx + 59} 138 Z", fill="#D3E4FA")
    # papel
    s.rect(cx - 36, 8, 72, 138, fill="#FFFFFF", stroke=C["slate_m"], sw=1.6, rx=2)
    s.line(cx - 36, 30, cx + 36, 30, C["slate"], 1.2, dash="3 2")
    s.line(cx - 36, 118, cx + 36, 118, C["slate"], 1.2, dash="3 2")
    s.text(cx + 42, 33, "frente do solvente", 9.4, "start", 700, C["blue_d"])
    s.text(cx + 42, 121, "linha de aplicação", 9.4, "start", 700, C["slate"])
    lanes = [cx - 24, cx, cx + 24]
    # amostra A (corante puro, magenta), mistura, corante B (azul)
    def spot(x, y, col, rx=7, ry=5):
        s.ellipse(x, y, rx, ry, fill=col, opacity=0.9)
    spot(lanes[0], 62, "#D6338B")
    spot(lanes[1], 96, "#F2C230"); spot(lanes[1], 62, "#D6338B"); spot(lanes[1], 44, "#2F6FD6")
    spot(lanes[2], 44, "#2F6FD6")
    for x, t in zip(lanes, ("A", "mistura", "B")):
        s.text(x, 134, t, 8.6 if t != "mistura" else 7.8, "middle", 700, INK)
    # cotas
    s.line(cx + 40, 118, cx + 40, 62, C["orange"], 1.4)
    s.line(cx + 36, 62, cx + 44, 62, C["orange"], 1.4)
    s.text(cx + 48, 94, "d", 11, "start", 800, C["orange_d"])
    s.line(cx + 74, 118, cx + 74, 30, C["red"], 1.4)
    s.line(cx + 70, 30, cx + 78, 30, C["red"], 1.4)
    s.text(cx + 82, 78, "D", 11, "start", 800, C["red_d"])
    s.arrow(cx - 66, 120, cx - 66, 46, C["slate"], 1.6, 6)
    s.text(cx - 70, 80, "solvente sobe", 9, "end", 700, C["slate"], rot=0) if False else None
    return s
