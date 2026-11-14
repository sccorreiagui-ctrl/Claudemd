"""Bloco F · página 31 — pH, tampão."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
OD = C["orange_d"]


@fig("f_ph_escala")
def _ph():
    W, H = 695, 128
    s = SVG(W, H, title="Escala de pH")
    x0, x1 = 20, 675
    X = lambda v: x0 + v / 14 * (x1 - x0)
    by = 52
    g = s.lingrad([(0, "#F2A15C"), (0.33, "#F6D9B5"), (0.5, "#E5E7EB"), (0.66, "#BBD6F8"), (1, "#3B6FE0")])
    s.rect(x0, by, x1 - x0, 14, fill=g, stroke=C["line"], sw=1, rx=7)
    for v in range(0, 15):
        s.line(X(v), by + 14, X(v), by + 19, INK, 1.0)
        s.text(X(v), by + 30, str(v), 9.6, "middle", 700 if v == 7 else 400, C["muted"])
    s.text(X(3.5), by + 44, "ÁCIDO  [H⁺] > [OH⁻]", 10.4, "middle", 800, OD)
    s.text(X(7), by + 44, "NEUTRO", 10.4, "middle", 800, C["slate"])
    s.text(X(10.5), by + 44, "BÁSICO  [OH⁻] > [H⁺]", 10.4, "middle", 800, C["blue_d"])
    pins = [(1.5, "suco gástrico", 0), (2.2, "limão", 1), (3.0, "refrigerante", 0), (5.0, "café", 1), (5.6, "chuva normal", 0),
            (7.0, "água pura", 1), (7.4, "sangue", 0), (8.1, "água do mar", 1), (10.5, "leite de magnésia", 0),
            (11.5, "amônia doméstica", 1), (13, "NaOH 0,1 mol/L", 0)]
    for v, nm, lv in pins:
        x = X(v)
        cy = by - 12 - lv * 22 if True else 0
        s.line(x, by, x, cy + 8, C["slate_m"], 1.0)
        s.circle(x, by + 7, 3.2, fill="#fff", stroke=INK, sw=1.2)
        w = tw(nm, 9.6, 700) + 10
        s.rect(x - w / 2, cy - 8, w, 16, fill="#FFFFFF", stroke=C["slate_m"], sw=1.1, rx=8)
        s.text(x, cy + 3.4, nm, 9.6, "middle", 700, INK)
    s.text(W - 8, H - 2, "valores aproximados · cada unidade de pH = fator 10 em [H⁺]", 9.2, "end", 700, C["muted"])
    return s


@fig("f_tampao")
def _tampao():
    W, H = 330, 200
    s = SVG(W, H, title="Tampão resiste à variação de pH")
    ax = Axes(s, 44, 14, 266, 136, 0, 100, 0, 8)
    ax.frame(xticks=[0, 25, 50, 75, 100], yticks=[0, 2, 4, 6, 8], xlabel="HCl 0,1 mol/L adicionado (mL)", ylabel=None, grid=True, size=9.6)
    s.text(14, 84, "pH", 10.4, "middle", 800, INK, rot=-90)
    water = []
    for k in range(0, 101):
        x = k
        if x == 0:
            water.append((0, 7.0))
        else:
            water.append((x, -math.log10(0.1 * x / (100 + x))))
    # primeira queda: ponto intermediário para mostrar a descida brusca
    water = [(0, 7.0), (0.15, 4.0)] + water[1:]
    ax.polyline(water, C["blue"], 3.0)
    buf = []
    for k in range(0, 100):
        nA = 0.01 - 0.0001 * k
        nHA = 0.01 + 0.0001 * k
        buf.append((k, 4.76 + math.log10(nA / nHA)))
    buf += [(99.0, 4.76 + math.log10(0.00001 / 0.01999)), (99.9, 2.4), (100, 1.9)]
    ax.polyline(buf, C["green"], 3.0)
    s.text(ax.X(40), ax.Y(2.4) , "água pura: pH despenca", 9.8, "start", 800, C["blue_d"], halo="#fff")
    s.text(ax.X(8), ax.Y(5.6), "tampão ácido acético / acetato:", 9.8, "start", 800, C["green_d"], halo="#fff")
    s.text(ax.X(8), ax.Y(5.6) + 11, "pH quase constante", 9.8, "start", 800, C["green_d"], halo="#fff")
    s.text(ax.X(88), ax.Y(3.7), "capacidade", 9, "middle", 700, C["muted"], halo="#fff")
    s.text(ax.X(88), ax.Y(3.7) + 10, "esgotada", 9, "middle", 700, C["muted"], halo="#fff")
    return s


@fig("f_indicadores")
def _indic():
    W, H = 695, 128
    s = SVG(W, H, title="Indicadores ácido-base")
    x0, x1 = 150, 675
    X = lambda v: x0 + v / 14 * (x1 - x0)
    rows = [
        ("Fenolftaleína", [(0, 8.2, "#F4F4F5"), (8.2, 10.0, "#F5B5D2"), (10.0, 14, "#D6338B")], "incolor → rosa (8,2–10)"),
        ("Azul de bromotimol", [(0, 6.0, "#F2D544"), (6.0, 7.6, "#7FBF6A"), (7.6, 14, "#3B6FE0")], "amarelo → azul (6,0–7,6)"),
        ("Alaranjado de metila", [(0, 3.1, "#E5484D"), (3.1, 4.4, "#F28C28"), (4.4, 14, "#F2D544")], "vermelho → amarelo (3,1–4,4)"),
        ("Tornassol", [(0, 5.0, "#E5484D"), (5.0, 8.0, "#9B6FD6"), (8.0, 14, "#3B6FE0")], "vermelho → azul (5–8)"),
        ("Repolho roxo (antocianinas)", [(0, 3, "#E5484D"), (3, 6, "#E58BB8"), (6, 8, "#9B6FD6"), (8, 10, "#3B6FE0"), (10, 12, "#3DAA5C"), (12, 14, "#F2D544")], "vermelho · rosa · roxo · azul · verde · amarelo"),
    ]
    for i, (nm, segs, note) in enumerate(rows):
        y = 4 + i * 21
        s.text(x0 - 8, y + 13, nm, 10.2, "end", 800, INK)
        for a, b, col in segs:
            s.rect(X(a), y, X(b) - X(a), 17, fill=col, stroke="#FFFFFF", sw=0.6)
        s.rect(x0, y, x1 - x0, 17, stroke=C["line"], sw=1, rx=3)
        s.text(x1 + 0, y + 13, "", 9)
    for v in range(0, 15, 2):
        s.line(X(v), 110, X(v), 114, INK, 1.0)
        s.text(X(v), 125, str(v), 9.6, "middle", 400, C["muted"])
    s.text(x0 - 8, 125, "pH →", 9.6, "end", 800, C["muted"])
    return s
