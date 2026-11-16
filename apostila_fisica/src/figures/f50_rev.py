"""Figuras da Revisão final (questões integradoras)."""
import math
from . import fig
from lib.circuit import *


@fig("fi_circ")
def fi_circ():
    f = Circ(332, 168, title="Gerador real alimentando uma lâmpada e um motor em paralelo")
    yt, yb = 40, 126
    f.bat((36, yb), (36, 86), pos="q", lab="w", name="12 V", signs=True, size=11)
    f.res((36, 86), (36, yt), "$r$", "1,0 Ω", lab="w", length=34, size=11, stack=True)
    f.wire([(36, yt), (236, yt)])
    f.wire([(36, yb), (236, yb)])
    f.lamp((134, yt), (134, yb), name="$R$", val="6,0 Ω", lab="e", size=11)
    f.box((236, yt), (236, yb), "M", name="$\\varepsilon'=6{,}0$ V", val="$r'=2{,}0$ Ω", lab="e", circle=True, height=24, size=11,
          stack=True)
    for x in (134, 236):
        f.node(x, yt)
        f.node(x, yb)
    f.text(166, 160, "gerador (esq.) · lâmpada e motor em paralelo", 10.5, MUTED, lint=False)
    return f


@fig("fi_graf")
def fi_graf():
    f = Fig(236, 150, title="Gráfico da corrente em um resistor de 4 ohms em função do tempo")
    pl = Plot(f, 44, 118, 148, 84, (0, 9.6), (0, 2.6), xticks=[(3, "3"), (5, "5"), (9, "9")], yticks=[(1, "1"), (2, "2")], grid=True)
    pl.line([(0, 2), (3, 2), (3, 0), (5, 0), (5, 1), (9, 1)], CUR, 2.6)
    pl.axis_labels("$t$ (s)", "$I$ (A)", ydx=2)
    return f
