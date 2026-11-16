"""Mapas mentais (fluxos de ideias) dos módulos."""
import math
from . import fig
from lib.circuit import *


def _node(f, x, y, w, h, title, sub, col, fill):
    f.rect(x, y, w, h, fill, col, 2.2, rx=9, tag="bg")
    f.text(x + w / 2, y + h / 2 - 3, title, 13, INK, weight=700)
    f.text(x + w / 2, y + h / 2 + 13, sub, 10.5, MUTED)


def _link(f, x1, y1, x2, y2, top, bot, col=INK, dy=0):
    f.arrow(x1, y1, x2, y2, col, 2.2, 10, 0.4)
    mx = (x1 + x2) / 2
    f.text(mx, y1 - 9 + dy, top, 11, INK, weight=600, halo=True)
    f.text(mx, y1 + 18 + dy, bot, 10.5, MUTED, halo=True)


@fig("mapa_estat")
def mapa_estat():
    f = Fig(680, 168, title="Mapa mental da Eletrostática")
    W, H = 168, 50
    y1, y2 = 4, 112
    xs = [0, 256, 512]
    _node(f, xs[0], y1, W, H, "Carga  q", "Q = ± n e", GRY, SOFT)
    _node(f, xs[1], y1, W, H, "Força  F", "par ação–reação", INK, SOFT)
    _node(f, xs[2], y1, W, H, "Campo  E", "linhas de campo", EFD, EFD_L)
    _node(f, xs[2], y2, W, H, "Potencial V, DDP U", "equipotenciais", EFD, EFD_L)
    _node(f, xs[1], y2, W, H, "Trabalho e energia", "ΔE_c = q·U", ENE, ENE_L)
    _node(f, xs[0], y2, W, H, "Capacitor", "C = Q/U", ENE, ENE_L)
    mid1, mid2 = y1 + H / 2, y2 + H / 2
    _link(f, xs[0] + W + 4, mid1, xs[1] - 4, mid1, "Coulomb", "F = k|q₁q₂|/r²")
    _link(f, xs[1] + W + 4, mid1, xs[2] - 4, mid1, "F = qE", "E = kQ/r²")
    f.arrow(xs[2] + W / 2, y1 + H + 3, xs[2] + W / 2, y2 - 3, INK, 2.2, 10, 0.4)
    f.text(xs[2] + W / 2 - 10, y1 + H + 24, "U = E·d  (E uniforme)", 11, INK, anchor="end", weight=600, halo=True)
    f.text(xs[2] + W / 2 - 10, y1 + H + 38, "V = kQ/r  (carga puntiforme)", 10.5, MUTED, anchor="end", halo=True)
    _link(f, xs[2] - 4, mid2, xs[1] + W + 4, mid2, "W = q·U", "E_p = q·V")
    _link(f, xs[1] - 4, mid2, xs[0] + W + 4, mid2, "energia armazenada", "E = C·U²/2")
    return f
