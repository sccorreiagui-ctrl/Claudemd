"""Capa e guia de uso: arte da capa e gráfico Raio-X SAS."""
import math
import random

from registry import fig
from svglib import SVG, C, tw

INK = C["ink"]


def _hexagon(cx, cy, r, rot=30):
    return [(cx + r * math.cos(math.radians(rot + 60 * i)), cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]


# ------------------------------------------------------------------- arte da capa (A4: 794 × 1121)
@fig("i_capa")
def _capa():
    W, H = 794, 1121
    s = SVG(W, H, title="Arte da capa")
    bg = s.lingrad([(0, "#0A1630"), (0.55, "#10285A"), (1, "#0C1D3E")], 0, 0, 0.6, 1)
    s.rect(0, 0, W, H, fill=bg)
    # rede hexagonal sutil (topo e direita)
    r = 34
    dx, dy = r * math.sqrt(3), r * 1.5
    for row in range(0, 12):
        for col in range(0, 14):
            cx = col * dx + (dx / 2 if row % 2 else 0) - 10
            cy = row * dy + 20
            fade = max(0.0, 1 - (cy / 600)) * 0.12 + max(0.0, (cx - 420) / 800) * 0.05
            if fade > 0.02:
                s.poly(_hexagon(cx, cy, r - 1.5), stroke="#9DB8F5", sw=1, opacity=min(fade, 0.14))
    # anéis de benzeno em destaque
    for (cx, cy, rr, col) in ((640, 190, 62, C["purple"]), (560, 300, 40, C["blue"]), (700, 330, 30, C["amber"])):
        pts = _hexagon(cx, cy, rr)
        s.poly(pts, stroke=col, sw=3.2, opacity=0.85)
        ins = _hexagon(cx, cy, rr * 0.72)
        for i in (0, 2, 4):
            a, b = ins[i], ins[(i + 1) % 6]
            s.line(a[0], a[1], b[0], b[1], col, 2.4, opacity=0.8)
        for (x, y) in pts:
            s.circle(x, y, 3.4, fill=col, opacity=0.95)
    # moléculas decorativas (CPK) à esquerda
    s.line(120, 652, 162, 626, "#FFFFFF", 3, opacity=0.5)
    s.line(120, 652, 162, 678, "#FFFFFF", 3, opacity=0.5)
    s.ball(120, 652, 22, "O", label="O")
    s.ball(162, 624, 13, "H", label="H")
    s.ball(162, 680, 13, "H", label="H")
    s.line(318, 652, 400, 652, "#FFFFFF", 3, opacity=0.5)
    s.ball(359, 652, 17, "C", label="C")
    s.ball(306, 652, 21, "O", label="O")
    s.ball(412, 652, 21, "O", label="O")
    # micela
    mx, my, mr = 640, 650, 62
    for i in range(26):
        a = 2 * math.pi * i / 26
        x1, y1 = mx + (mr - 16) * math.cos(a), my + (mr - 16) * math.sin(a)
        x2, y2 = mx + 6 * math.cos(a + 0.2), my + 6 * math.sin(a + 0.2)
        s.path(f"M{x1:.1f} {y1:.1f} Q{(x1 + x2) / 2 + 5 * math.sin(a):.1f} {(y1 + y2) / 2 - 5 * math.cos(a):.1f} {x2:.1f} {y2:.1f}",
               stroke=C["amber"], sw=2.4, opacity=0.9)
    for i in range(26):
        a = 2 * math.pi * i / 26
        s.circle(mx + mr * math.cos(a), my + mr * math.sin(a), 8.2, fill=C["blue"], stroke="#CFE3FF", sw=1.4)
    # bicamada fosfolipídica (faixa inferior)
    random.seed(7)
    y_top, y_bot = 800, 918
    n = 27
    for i in range(n):
        x = 14 + i * 29.5
        for (yh, d) in ((y_top, 1), (y_bot, -1)):
            yy = yh + (3 if i % 2 else 0) * d
            s.circle(x, yy, 9.6, fill=C["blue"], stroke="#CFE3FF", sw=1.3)
            for off in (-3.4, 3.4):
                ytail = yy + d * 52
                s.path(f"M{x + off:.1f} {yy + d * 9:.1f} Q{x + off + 4 * d:.1f} {yy + d * 26:.1f} {x + off:.1f} {yy + d * 38:.1f} T{x + off:.1f} {ytail:.1f}",
                       stroke=C["amber"], sw=2.2, opacity=0.95)
    s.rect(0, 1030, W, H - 1030, fill="#07102A", opacity=0.55)
    return s


# ------------------------------------------------------------------- Raio-X SAS (top 10 de Química)
@fig("i_raiox")
def _raiox():
    W, H = 340, 176
    s = SVG(W, H, title="Raio-X SAS: assuntos de Química mais frequentes")
    rows = [
        ("Funções orgânicas", 36, C["purple"]), ("Reações orgânicas", 28, C["purple"]), ("Cinética química", 25, C["orange"]),
        ("Pilhas", 19, C["orange"]), ("Separação de misturas", 19, C["green"]), ("Tecnologias ambientais", 18, C["green"]),
        ("Controle de poluição", 17, C["green"]), ("Concentração de soluções", 17, C["slate"]),
        ("Poluição da água", 16, C["green"]), ("Tipos de reações químicas", 15, C["slate"]),
    ]
    x0, bw = 124, 170
    for i, (nm, v, col) in enumerate(rows):
        y = 6 + i * 15.4
        s.text(x0 - 5, y + 9.4, nm, 9.4, "end", 600, INK)
        s.rect(x0, y + 1, bw * v / 36, 11, fill=col, rx=3)
        s.text(x0 + bw * v / 36 + 4, y + 9.8, f"{v}", 9.6, "start", 800, INK)
    s.text(W - 4, H - 3, "599 itens (2009–2025) · top 10 = 210 itens ≈ 35,1%", 9, "end", 600, C["muted"])
    return s
