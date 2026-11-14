"""Bloco D · página 21 — diluição, mistura e titulação."""
import math
import random

from registry import fig
from svglib import SVG, C, Axes, tw
from figs_a5 import _beaker_path, _liquid

INK = C["ink"]
BD = C["blue_d"]


def _beaker(s, cx, top, w, h, level, fill, ndots, rnd, dot_col="#6D4BD0", mark=None):
    y_from = top + h - level
    _liquid(s, cx, top, w, h, y_from, fill)
    for _ in range(ndots):
        x = cx - w / 2 + 8 + rnd.random() * (w - 16)
        y = y_from + 7 + rnd.random() * max(level - 14, 4)
        s.circle(x, y, 3.0, fill="#B79DFB", stroke=dot_col, sw=0.9)
    s.path(_beaker_path(cx, top, w, h), stroke=C["slate"], sw=2.2)
    s.line(cx - w / 2 - 5, top, cx - w / 2 + 5, top, C["slate"], 2.2)
    s.line(cx + w / 2 - 5, top, cx + w / 2 + 5, top, C["slate"], 2.2)


@fig("d_diluicao")
def _dil():
    W, H = 343, 160
    s = SVG(W, H, title="Diluição: o número de mols de soluto não muda")
    rnd = random.Random(8)
    top, h = 10, 84
    _beaker(s, 62, top, 84, h, 40, "#9CC3F5", 9, rnd)
    rnd = random.Random(8)
    _beaker(s, 262, top, 108, h, 70, "#D3E4FA", 9, rnd)
    s.arrow(118, 50, 196, 50, C["blue"], 2.4, 9)
    s.text(157, 40, "+ água", 11, "middle", 800, BD)
    s.text(157, 66, "(solvente)", 9.6, "middle", 600, C["muted"])
    s.text(62, 112, "C_1 , V_1", 12, "middle", 800, INK)
    s.text(62, 126, "n_1 = C_1·V_1", 10.4, "middle", 600, C["slate"])
    s.text(262, 112, "C_2 , V_2", 12, "middle", 800, INK)
    s.text(262, 126, "n_2 = C_2·V_2", 10.4, "middle", 600, C["slate"])
    s.text(W / 2, 151, "mesmos 9 solutos → n_1 = n_2  ⇒  C_1·V_1 = C_2·V_2", 11, "middle", 800, C["blue_d"])
    return s


@fig("d_mistura")
def _mist():
    W, H = 343, 160
    s = SVG(W, H, title="Mistura de soluções do mesmo soluto")
    top, h = 10, 84
    _beaker(s, 44, top, 66, h, 38, "#9CC3F5", 6, random.Random(1))
    _beaker(s, 140, top, 66, h, 50, "#D3E4FA", 4, random.Random(2))
    _beaker(s, 262, top, 100, h, 72, "#BBD6F8", 10, random.Random(3))
    s.text(92, 58, "+", 18, "middle", 700, C["muted"])
    s.arrow(188, 52, 206, 52, C["blue"], 2.2, 8)
    s.text(44, 112, "C_1 , V_1", 11, "middle", 800, INK)
    s.text(140, 112, "C_2 , V_2", 11, "middle", 800, INK)
    s.text(262, 112, "C_f , V_f = V_1 + V_2", 11, "middle", 800, INK)
    s.text(W / 2, 135, "n_f = n_1 + n_2 (sem reação)", 10.6, "middle", 700, C["slate"])
    s.text(W / 2, 151, "C_f = (C_1·V_1 + C_2·V_2) / (V_1 + V_2)", 11, "middle", 800, C["blue_d"])
    return s


@fig("d_bureta")
def _bureta():
    W, H = 150, 222
    s = SVG(W, H, title="Aparelhagem de titulação")
    cx = 76
    # suporte
    s.line(26, 10, 26, 204, C["slate_m"], 5)
    s.line(10, 204, 52, 204, C["slate_m"], 5)
    s.line(26, 34, cx - 8, 34, C["slate_m"], 4)
    # bureta
    s.rect(cx - 7, 12, 14, 112, fill="#FFFFFF", stroke=C["slate"], sw=1.8, rx=3)
    s.rect(cx - 5.2, 56, 10.4, 66, fill="#9CC3F5")
    for yy in range(20, 120, 8):
        s.line(cx - 7, yy, cx - 3, yy, C["slate"], 1)
    s.rect(cx - 9, 124, 18, 6, fill=C["slate"], rx=2)  # torneira
    s.line(cx, 130, cx, 142, C["slate"], 2)
    s.circle(cx, 150, 2.4, fill=C["blue"])
    s.text(cx + 12, 72, "bureta:", 10, "start", 800, INK)
    s.text(cx + 12, 84, "NaOH", 9.6, "start", 600, C["muted"])
    s.text(cx + 12, 95, "0,10 mol/L", 9.6, "start", 600, C["muted"])
    # erlenmeyer
    s.path(f"M{cx - 9} 158 L{cx - 9} 172 L{cx - 34} 200 L{cx + 34} 200 L{cx + 9} 172 L{cx + 9} 158", stroke=C["slate"], sw=2.2)
    s.path(f"M{cx - 25} 184 L{cx + 25} 184 L{cx + 34} 200 L{cx - 34} 200 Z", fill="#F7B6D2", opacity=0.9)
    s.text(cx, 214, "erlenmeyer: HCl + indicador", 9.8, "middle", 800, INK)
    return s


def _ph(vb, va=25.0, ma=0.1, mb=0.1):
    na = ma * va / 1000
    nb = mb * vb / 1000
    vt = (va + vb) / 1000
    if abs(na - nb) < 1e-12:
        return 7.0
    if na > nb:
        return -math.log10((na - nb) / vt)
    return 14 + math.log10((nb - na) / vt)


@fig("d_curva_titulacao")
def _curva_tit():
    W, H = 262, 214
    s = SVG(W, H, title="Curva de titulação ácido forte × base forte")
    ax = Axes(s, 40, 10, 208, 160, 0, 50, 0, 14)
    ax.frame(xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 2, 4, 6, 8, 10, 12, 14], xlabel="volume de NaOH (mL)", ylabel=None,
             size=9.6)
    s.text(12, 92, "pH", 10.4, "middle", 800, INK, rot=-90)
    # faixa do indicador
    s.rect(ax.x0, ax.Y(10), ax.w, ax.Y(8.2) - ax.Y(10), fill="#F7B6D2", opacity=0.55)
    s.text(ax.x0 + 4, ax.Y(10) + 9, "fenolftaleína (rosa, pH 8,2–10)", 8.8, "start", 700, "#9D2F63")
    pts = []
    v = 0.0
    while v <= 50:
        pts.append((v, _ph(v)))
        v += 0.25 if 22 < v < 28 else 1.0
    ax.polyline(pts, C["blue"], 3.0)
    s.circle(ax.X(25), ax.Y(7), 4.8, fill=C["orange"], stroke="#fff", sw=1.4)
    s.line(ax.X(25), ax.Y(7), ax.X(25), ax.Y(0), C["orange"], 1.4, dash="3 3")
    s.line(ax.X(0), ax.Y(7), ax.X(25), ax.Y(7), C["orange"], 1.4, dash="3 3")
    s.text(ax.X(25) + 8, ax.Y(6) + 6, "ponto de equivalência", 9.4, "start", 800, C["orange_d"], halo="#fff")
    s.text(ax.X(25) + 8, ax.Y(6) + 17, "pH = 7 (25 mL)", 9.4, "start", 800, C["orange_d"], halo="#fff")
    s.text(ax.X(3), ax.Y(2.4) , "excesso de ácido", 9.2, "start", 600, C["muted"])
    s.text(ax.X(33), ax.Y(12.2) + 4, "excesso de base", 9.2, "start", 600, C["muted"])
    return s
