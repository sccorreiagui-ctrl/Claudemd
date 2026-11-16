"""Figuras do Módulo III — diagramas dos exercícios."""
import math
from . import fig
from lib.circuit import *


@fig("fx_instal")
def fx_instal():
    f = Circ(332, 156, title="Exercício: três aparelhos em paralelo em uma tomada de 127 V")
    yt, yb = 44, 112
    f.box((52, yb), (52, yt), "~", circle=True, height=24, tsize=15, name="127 V", lab="w", size=11)
    f.wire([(52, yt), (300, yt)])
    f.wire([(52, yb), (300, yb)])
    f.lamp((120, yt), (120, yb), "lâmpada", "60 W", lab="w", r=11, size=10.5, stack=True)
    f.box((200, yt), (200, yb), "TV", "120 W", lab="e", length=34, height=26, size=10.5, stack=True, tsize=11.5)
    f.res((272, yt), (272, yb), "ferro", "1000 W", lab="e", length=40, size=10.5, stack=True)
    for x in (120, 200, 272):
        f.node(x, yt)
        f.node(x, yb)
    f.text(166, 148, "mesma tensão (127 V) em todos os aparelhos", 10.5, MUTED)
    return f


@fig("fx_misto")
def fx_misto():
    f = Circ(332, 160, title="Exercício: circuito misto com fonte de 36 V")
    yt, yb = 40, 116
    f.bat((40, yb), (40, yt), pos="q", lab="w", name="36 V", signs=True, size=11)
    f.wire([(40, yt), (56, yt)])
    f.res((56, yt), (136, yt), "$R_1$", "6 Ω", lab="n", size=11.5)
    f.wire([(136, yt), (160, yt), (252, yt)])
    f.res((160, yt), (160, yb), "$R_2$", "4 Ω", lab="w", length=40, size=11.5)
    f.res((252, yt), (252, yb), "$R_3$", "4 Ω", lab="e", length=40, size=11.5)
    f.wire([(252, yb), (160, yb)])
    f.res((160, yb), (56, yb), "$R_4$", "4 Ω", lab="s", size=11.5)
    f.wire([(56, yb), (40, yb)])
    f.node(160, yt)
    f.node(160, yb)
    f.text(166, 154, "$R_2\\parallel R_3$ em série com $R_1$ e $R_4$", 10.5, MUTED, lint=False)
    return f


@fig("fx_motor")
def fx_motor():
    f = Circ(332, 176, title="Exercício: bateria real alimentando um motor (receptor)")
    yt, yb = 44, 128
    f.bat((40, yb), (40, 84), pos="q", lab="w", name="12 V", signs=True, size=11)
    f.res((40, 84), (40, yt), "$r$", "0,5 Ω", lab="w", length=34, size=11, stack=True)
    f.wire([(40, yt), (160, yt)])
    f.box((160, yt), (290, yt), "M", name="$\\varepsilon'$ = 6 V", val="$r'$ = 1 Ω", lab="n", circle=True, height=24, size=11, stack=True)
    f.wire([(290, yt), (290, yb), (40, yb)])
    f.iarr((60, yt), (120, yt), 0.5, "$I$", length=22, off=7)
    f.text(166, 168, "gerador: corrente sai pelo $+$ · motor: entra pelo $+$", 10.5, MUTED, lint=False)
    return f


@fig("fx_volt")
def fx_volt():
    f = Circ(332, 168, title="Exercício: voltímetro real em paralelo com um resistor de 10 kΩ")
    yt, yb = 42, 108
    f.bat((40, yb), (40, yt), pos="q", lab="w", name="12 V", signs=True, size=11)
    f.wire([(40, yt), (58, yt)])
    f.res((58, yt), (158, yt), "$R_a$", "10 kΩ", lab="n", size=11.5)
    f.res((158, yt), (258, yt), "$R_b$", "10 kΩ", lab="n", size=11.5)
    f.wire([(258, yt), (290, yt), (290, yb), (40, yb)])
    f.node(158, yt)
    f.node(258, yt)
    f.wire([(158, yt), (158, yt + 18)])
    f.wire([(258, yt), (258, yt + 18)])
    f.meter((158, yt + 18), (258, yt + 18), "V", lab="s", r=11, name="10 kΩ", size=10.5)
    f.text(166, 162, "voltímetro real em paralelo com $R_b$", 10.5, MUTED, lint=False)
    return f


@fig("fx_gerador_misto")
def fx_gerador_misto():
    f = Circ(332, 170, title="Exercício: gerador real e circuito misto")
    yt, yb = 44, 122
    f.bat((40, yb), (40, 88), pos="q", lab="w", name="24 V", signs=True, size=11)
    f.res((40, 88), (40, yt), "$r$", "1 Ω", lab="w", length=32, size=11, stack=True)
    f.wire([(40, yt), (60, yt)])
    f.res((60, yt), (140, yt), "$R_1$", "5 Ω", lab="n", size=11.5)
    f.wire([(140, yt), (170, yt), (250, yt)])
    f.res((170, yt), (170, yb), "12 Ω", lab="w", length=40, size=11)
    f.res((250, yt), (250, yb), "6 Ω", lab="e", length=40, size=11)
    f.wire([(250, yb), (40, yb)])
    f.node(170, yt)
    f.node(170, yb)
    f.text(166, 160, "gerador $(\\varepsilon,r)$ + $R_1$ em série com $(12\\ \\Omega\\parallel6\\ \\Omega)$", 10.5, MUTED, lint=False)
    return f


@fig("fx_kirch")
def fx_kirch():
    f = Circ(332, 232, title="Exercício: Kirchhoff com duas malhas e um resistor compartilhado")
    xL, xM, xR, yt, yb = 56, 176, 296, 40, 188
    f.bat((xL, yb), (xL, 126), pos="q", lab="w", name="$\\varepsilon$", val="24 V", signs=True, size=11)
    f.res((xL, 126), (xL, yt), "$R_1$", "2 Ω", lab="w", length=42, stack=True, size=11)
    f.wire([(xL, yt), (xR, yt)])
    f.wire([(xL, yb), (xR, yb)])
    f.res((xM, yt), (xM, yb), "$R_2$", "3 Ω", lab="e", length=46, stack=True, size=11)
    f.res((xR, yt), (xR, yb), "$R_3$", "6 Ω", lab="e", length=46, stack=True, size=11)
    f.node(xM, yt)
    f.node(xM, yb)
    f.iarr((xL, yt), (xM - 36, yt), 0.5, "$I_1$", length=22, off=7)
    f.iarr((xM, 58), (xM, 90), 0.5, "$I_2$", length=20, side="w", off=8)
    f.iarr((xR, 58), (xR, 90), 0.5, "$I_3$", length=20, side="w", off=8)
    f.text(166, 218, "escreva: 1 equação de nó e 2 de malha", 10.5, MUTED)
    return f


@fig("fx_escada")
def fx_escada():
    f = Circ(332, 150, title="Desafio: rede infinita de resistores iguais a R")
    yt, yb = 46, 110
    f.circ(34, yt, 3.8, "#fff", INK, 1.9, tag="bg")
    f.circ(34, yb, 3.8, "#fff", INK, 1.9, tag="bg")
    f.text(22, yt + 4, "A", 12, INK, anchor="end", weight=700)
    f.text(22, yb + 4, "B", 12, INK, anchor="end", weight=700)
    xs = [38, 128, 218]
    for k, x in enumerate(xs):
        f.res((x, yt), (x + 54, yt), "$R$", lab="n", length=34, amp=6, size=11)
        f.wire([(x + 54, yt), (x + 64, yt)])
        f.res((x + 64, yt), (x + 64, yb), "$R$", lab="e", length=34, amp=6, size=11)
        f.wire([(x + 64, yb), (x, yb)])
        f.node(x + 64, yt)
        f.node(x + 64, yb)
        if k < 2:
            f.wire([(x + 64, yt), (x + 90, yt)])
    f.wire([(282 + 0, yt), (300, yt)])
    f.wire([(282, yb), (300, yb)])
    f.text(316, yt + 28, "···", 18, GRY, weight=700, lint=False)
    f.text(166, 144, "$R_{AB}=?$ (o módulo se repete indefinidamente)", 11, INK)
    return f


def _bx(f, x, y, w, h, lines, col, fill, size=11, bold_first=True):
    f.rect(x, y, w, h, fill, col, 2.0, rx=9, tag="bg")
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * (size + 3) / 2 + size * 0.34
    for k, s in enumerate(lines):
        f.text(x + w / 2, y0 + k * (size + 3), s, size, INK, weight=700 if (k == 0 and bold_first) else 400)


@fig("decisor_circ")
def decisor_circ():
    f = Fig(680, 226, title="Fluxograma: que método usar para resolver um circuito")
    # linha 1
    _bx(f, 0, 14, 118, 50, ["Circuito dado", "(desenho + dados)"], GRY, SOFT, 11)
    f.arrow(120, 39, 168, 39, INK, 2.2, 10, 0.4)
    _bx(f, 170, 4, 232, 70, ["Uma só fonte e resistores", "que se reduzem a", "série e paralelo?"], INK, WHITE, 11, False)
    f.arrow(404, 39, 452, 39, ENE_D, 2.4, 10, 0.4)
    f.text(428, 30, "sim", 11, ENE_D, weight=700, halo=True)
    _bx(f, 454, 4, 226, 70, ["Reduza a $R_{eq}$ (seção 3.4)", "de dentro para fora e volte", "aos ramos com $U=RI$"], ENE, ENE_L, 11)
    # linha 2
    f.arrow(286, 76, 286, 104, INK, 2.2, 10, 0.4)
    f.text(298, 94, "não", 11, INK, anchor="start", weight=700, halo=True)
    _bx(f, 170, 106, 232, 56, ["Uma só fonte, mas há ponte ou", "fio ligando nós?"], INK, WHITE, 11, False)
    f.arrow(404, 134, 452, 134, CUR_D, 2.4, 10, 0.4)
    f.text(428, 125, "sim", 11, CUR_D, weight=700, halo=True)
    _bx(f, 454, 106, 226, 56, ["Nós e potenciais (3.5)", "fio ideal que contorna (3.6)"], CUR, CUR_L, 11)
    # linha 3
    f.arrow(286, 164, 286, 184, INK, 2.2, 10, 0.4)
    f.text(298, 178, "não", 11, INK, anchor="start", weight=700, halo=True)
    _bx(f, 170, 186, 232, 38, ["Várias fontes: Kirchhoff (3.7)"], INK, SOFT, 11)
    _bx(f, 454, 176, 226, 48, ["Fonte real? $U=\\varepsilon-rI$ (3.8)", "Medidores? (3.9) · confira $\\sum P$"], GRY, SOFT, 10.5, False)
    f.text(60, 150, "Em qualquer caso:", 10.5, MUTED, weight=600)
    f.text(60, 165, "unidades SI e", 10.5, MUTED)
    f.text(60, 180, "verificação física", 10.5, MUTED)
    return f
