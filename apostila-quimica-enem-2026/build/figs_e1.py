"""Bloco E · página 25 — matéria, estados físicos e curvas de aquecimento."""
import math
import random

from registry import fig
from svglib import SVG, C, Axes, tw
from figlib import chip_svg

INK = C["ink"]
GD = C["green_d"]


def _atom(s, x, y, r=6.0, kind="a"):
    fills = {"a": ("#4B5563", "#1F2937"), "b": ("#E5484D", "#9B1C22"), "c": ("#FFFFFF", "#6B7280"),
             "d": ("#4C6FD6", "#2B3F8F")}
    f, st = fills[kind]
    s.circle(x, y, r, fill=f, stroke=st, sw=1.2)


@fig("e_particulas")
def _part():
    W, H = 695, 122
    s = SVG(W, H, title="Substâncias puras e misturas em nível de partículas")
    cw = (W - 12) / 4
    cells = [("Substância simples", "só átomos de um elemento", "O₂ · Fe · C (grafite)", "puro"),
             ("Substância composta", "moléculas iguais, ≥ 2 elementos", "H₂O · CO₂ · NaCl", "puro"),
             ("Mistura de simples", "substâncias diferentes juntas", "ar (N₂ + O₂) · ligas", "mist"),
             ("Mistura de compostos", "moléculas diferentes juntas", "água do mar · petróleo", "mist")]
    rnd = random.Random(2)
    for i, (t, sub, ex, kind) in enumerate(cells):
        x = 6 + i * cw
        col = C["green"] if kind == "puro" else C["slate"]
        s.rect(x + 2, 3, cw - 4, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        chip_svg(s, x + cw / 2, 15, "SUBSTÂNCIA PURA" if kind == "puro" else "MISTURA", "green" if kind == "puro" else "slate",
                 8.6, padx=6, h=14)
        cx0, cy0 = x + cw / 2, 52
        pos = [(cx0 - 52, cy0 - 12), (cx0 - 18, cy0 - 4), (cx0 + 20, cy0 - 14), (cx0 + 52, cy0 - 2),
               (cx0 - 40, cy0 + 20), (cx0 - 2, cy0 + 22), (cx0 + 36, cy0 + 20)]
        for j, (px, py) in enumerate(pos):
            if i == 0:
                # moléculas diatômicas de um só elemento
                _atom(s, px - 5.5, py, 5.4, "a"); _atom(s, px + 5.5, py, 5.4, "a")
            elif i == 1:
                _atom(s, px, py, 6.6, "b"); _atom(s, px - 8, py + 5, 4.2, "c"); _atom(s, px + 8, py + 5, 4.2, "c")
            elif i == 2:
                if j % 2 == 0:
                    _atom(s, px - 5.5, py, 5.4, "a"); _atom(s, px + 5.5, py, 5.4, "a")
                else:
                    _atom(s, px - 5.5, py, 5.4, "d"); _atom(s, px + 5.5, py, 5.4, "d")
            else:
                if j % 2 == 0:
                    _atom(s, px, py, 6.6, "b"); _atom(s, px - 8, py + 5, 4.2, "c"); _atom(s, px + 8, py + 5, 4.2, "c")
                else:
                    _atom(s, px - 8, py, 5.0, "b"); _atom(s, px, py, 6.0, "a"); _atom(s, px + 8, py, 5.0, "b")
        s.text(x + cw / 2, 93, t, 11.2, "middle", 800, INK)
        s.text(x + cw / 2, 104, sub, 9.4, "middle", 400, C["muted"])
        s.text(x + cw / 2, 115, ex, 9.4, "middle", 700, col)
    return s


@fig("e_estados")
def _estados():
    W, H = 695, 164
    s = SVG(W, H, title="Estados físicos e mudanças de estado")
    rnd = random.Random(9)
    bx = [(10, "SÓLIDO", "forma e volume fixos", "partículas ordenadas e em contato"),
          (255, "LÍQUIDO", "volume fixo, forma do recipiente", "próximas, sem ordem fixa"),
          (500, "GASOSO", "sem forma nem volume fixos", "muito afastadas, desordenadas")]
    bw, bh = 185, 82
    for k, (x, nm, l1, l2) in enumerate(bx):
        s.rect(x, 8, bw, bh, fill=C["green_l"], stroke=C["green_m"], sw=1.4, rx=10)
        s.text(x + bw / 2, 24, nm, 12, "middle", 800, GD)
        if k == 0:
            for r in range(3):
                for c in range(5):
                    s.circle(x + 30 + c * 31, 40 + r * 16, 6.6, fill="#8DBBF2", stroke=C["blue"], sw=1.1)
        elif k == 1:
            pts = [(40, 40), (68, 44), (98, 38), (130, 46), (156, 40), (50, 58), (82, 62), (114, 56), (146, 62), (36, 74),
                   (66, 78), (98, 72), (130, 78), (158, 74)]
            for (px, py) in pts:
                s.circle(x + px + rnd.uniform(-3, 3), 8 + py - 12 + rnd.uniform(-2, 2), 6.6, fill="#8DBBF2", stroke=C["blue"], sw=1.1)
        else:
            for _ in range(8):
                s.circle(x + rnd.uniform(18, bw - 18), 8 + rnd.uniform(34, bh - 10), 6, fill="#8DBBF2", stroke=C["blue"], sw=1.1)
        s.text(x + bw / 2, 8 + bh + 13, l1, 9.8, "middle", 700, INK)
        s.text(x + bw / 2, 8 + bh + 25, l2, 9.4, "middle", 400, C["muted"])
    # setas: fusão/solidificação, vaporização/condensação
    def pair(x1, x2, up, dn, y):
        s.arrow(x1, y, x2, y, C["red"], 2.2, 8)
        s.arrow(x2, y + 16, x1, y + 16, C["blue"], 2.2, 8)
        s.text((x1 + x2) / 2, y - 5, up, 10.4, "middle", 800, C["red_d"])
        s.text((x1 + x2) / 2, y + 30, dn, 10.4, "middle", 800, C["blue_d"])
    pair(198, 252, "fusão", "solidificação", 36)
    pair(443, 497, "vaporização", "condensação", 36)
    # sublimação: setas longas abaixo dos rótulos
    s.arrow(100, 128, 595, 128, C["red"], 2, 8, dash="6 3")
    s.arrow(595, 142, 100, 142, C["blue"], 2, 8, dash="6 3")
    s.text(347, 124, "sublimação", 10.4, "middle", 800, C["red_d"], halo="#fff")
    s.text(347, 156, "ressublimação (deposição)", 10.4, "middle", 800, C["blue_d"], halo="#fff")
    s.text(W - 4, 12, "vermelho: absorve calor · azul: libera calor", 9.4, "end", 700, C["muted"])
    return s


def _curve(pts, ax, color, sw=3.0, dash=None):
    ax.polyline(pts, color, sw, dash)


@fig("e_aquec")
def _aquec():
    W, H = 695, 196
    s = SVG(W, H, title="Curvas de aquecimento: substância pura e misturas")
    # grande: água pura
    ax = Axes(s, 46, 22, 288, 132, 0, 10, -30, 130)
    ax.frame(xticks=[], yticks=[0, 100], xlabel="calor fornecido (ou tempo)", ylabel=None, grid=False, size=10,
             yfmt=lambda v: f"{v} °C")
    s.text(14, 90, "temperatura", 10.4, "middle", 800, INK, rot=-90)
    pts = [(0.3, -25), (2.0, 0), (4.2, 0), (6.0, 100), (8.4, 100), (9.7, 125)]
    ax.polyline(pts, C["blue"], 3.4)
    s.line(ax.X(0), ax.Y(0), ax.X(10), ax.Y(0), C["slate_m"], 1, dash="3 3")
    s.line(ax.X(0), ax.Y(100), ax.X(10), ax.Y(100), C["slate_m"], 1, dash="3 3")
    for (x, y, t, col) in ((1.0, -14, "sólido", C["slate"]), (3.1, 9, "sólido + líquido", C["blue_d"]),
                           (5.1, 56, "líquido", C["slate"]), (7.2, 109, "líquido + gás", C["blue_d"]), (9.2, 112, "gás", C["slate"])):
        pass
    s.text(ax.X(1.0), ax.Y(-14) , "sólido", 10.4, "middle", 800, C["slate"], halo="#fff")
    s.text(ax.X(3.1), ax.Y(0) - 7, "fusão", 10.4, "middle", 800, C["blue_d"], halo="#fff")
    s.text(ax.X(3.1), ax.Y(0) + 15, "sólido + líquido", 9.4, "middle", 700, C["blue_d"], halo="#fff")
    s.text(ax.X(4.6), ax.Y(52), "líquido", 10.4, "middle", 800, C["slate"], halo="#fff")
    s.text(ax.X(7.2), ax.Y(100) - 7, "ebulição", 10.4, "middle", 800, C["blue_d"], halo="#fff")
    s.text(ax.X(7.2), ax.Y(100) + 15, "líquido + gás", 9.4, "middle", 700, C["blue_d"], halo="#fff")
    s.text(ax.X(9.0), ax.Y(118), "gás", 10.4, "middle", 800, C["slate"], halo="#fff")
    s.text(46 + 144, 13, "Substância PURA (água, 1 atm)", 11.4, "middle", 800, GD)
    s.text(ax.X(1.2) , ax.Y(0) - 6 , "", 9)
    chip_svg(s, ax.X(8.6), ax.Y(-14), "2 patamares: P.F. e P.E. constantes", "green", 9.2, padx=6, h=15)
    # três painéis menores
    def small(x0, title, pts, plats, note, col):
        a = Axes(s, x0, 40, 92, 64, 0, 10, 0, 10)
        a.frame(xticks=[], yticks=[], xlabel=None, ylabel=None, grid=False, size=9, arrows=True)
        a.polyline(pts, col, 3.0)
        for (x1, x2, y) in plats:
            s.line(a.X(x1), a.Y(y), a.X(x2), a.Y(y), C["red"], 4.0, cap="butt", opacity=0.0)
        s.text(x0 + 46, 14, title, 10.4, "middle", 800, GD)
        s.text(x0 + 46, 27, note[0], 9.2, "middle", 600, C["slate"])
        s.text(x0 + 46, 122, note[1], 9.4, "middle", 700, col)
        s.text(x0 + 46, 134, note[2], 9, "middle", 400, C["muted"])
        return a
    # mistura comum: sem patamares
    a1 = small(372, "Mistura comum", [(0.5, 0.8), (3.0, 4.2), (4.0, 5.0), (6.0, 7.2), (9.5, 9.5)], [], ("sem patamar", "P.F. e P.E. variam", "(T sobe durante a mudança)"), C["slate"])
    # eutética: patamar na fusão apenas
    a2 = small(472, "Eutética", [(0.5, 0.8), (3.0, 3.0), (4.0, 3.0), (6.0, 6.2), (7.0, 7.2), (9.5, 9.5)], [], ("patamar só na fusão", "P.F. constante", "ex.: solda Sn–Pb (63/37)"), C["blue"])
    # azeotrópica: patamar só na ebulição
    a3 = small(572, "Azeotrópica", [(0.5, 0.8), (3.0, 2.6), (4.2, 3.9), (6.0, 6.4), (7.0, 7.4), (8.0, 7.4), (9.5, 9.6)], [], ("patamar só na ebulição", "P.E. constante", "ex.: etanol 96% + água"), C["orange"])
    return s
