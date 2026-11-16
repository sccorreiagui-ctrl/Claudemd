"""Figura da capa: tríptico eletrostática · eletrodinâmica · magnetismo."""
import math
from . import fig
from lib.circuit import *


def _panel(f, x, w, h, title, col):
    f.rect(x, 0, w, h, "#fff", RULE, 1.2, rx=10, tag="bg")
    f.text(x + w / 2, h + 26, title, 13.5, col, weight=700)


@fig("capa")
def capa():
    W, H, PW = 680, 330, 214
    f = Circ(W, H + 36, title="Capa: campo elétrico de um dipolo, circuito com potenciais e campo de um ímã")
    # 1 — dipolo elétrico
    _panel(f, 0, PW, H, "ELETROSTÁTICA", EFD_D)
    ch = [(62, 165, +1), (152, 165, -1)]
    field_lines(f, ch, (3, 3, PW - 3, H - 3), n_per_unit=11, c=EFD, w=1.6, r0=14, stop_r=11)
    f.charge(62, 165, +1, 12)
    f.charge(152, 165, -1, 12)
    # 2 — circuito colorido por potencial
    x0 = 233
    _panel(f, x0, PW, H, "ELETRODINÂMICA", CUR_D)
    L, R, T, B = x0 + 42, x0 + PW - 44, 92, 246
    c12, c7, c0 = pot_color(12, 0, 12), pot_color(7, 0, 12), pot_color(0, 0, 12)
    f.bat((L, B), (L, T + 36), pos="q", wc=(c0, c12), ww=3.4, lab="w", name=None, signs=True)
    f.wire([(L, T + 36), (L, T), (x0 + 70, T)], c12, 3.4)
    f.res((x0 + 70, T), (x0 + 128, T), wc=(c12, c7), ww=3.4)
    f.wire([(x0 + 128, T), (R, T), (R, T + 40)], c7, 3.4)
    f.lamp((R, T + 40), (R, B - 40), lum=3, wc=(c7, c0), ww=3.4, r=15)
    f.wire([(R, B - 40), (R, B), (x0 + 128, B)], c0, 3.4)
    f.sw((x0 + 128, B), (x0 + 70, B), closed=True, wc=c0, ww=3.4, length=40)
    f.wire([(x0 + 70, B), (L, B)], c0, 3.4)
    f.iarr((x0 + 128, T), (R, T), 0.5, None, length=26, w=3)
    f.iarr((R, T), (R, T + 40), 0.5, None, length=22, w=3)
    f.iarr((R, B - 40), (R, B), 0.5, None, length=22, w=3)
    f.iarr((R, B), (x0 + 128, B), 0.5, None, length=26, w=3)
    f.iarr((L, T + 36), (L, T), 0.5, None, length=22, w=3)
    # escala de potencial
    for k in range(5):
        f.rect(x0 + 52 + k * 22, 292, 22, 7, pot_color(k, 0, 4), None, 0)
    f.text(x0 + 48, 297, "0 V", 10, MUTED, anchor="end", lint=False)
    f.text(x0 + 52 + 110 + 4, 297, "12 V", 10, MUTED, anchor="start", lint=False)
    # 3 — ímã
    x0 = 466
    _panel(f, x0, PW, H, "MAGNETISMO", MAG_D)
    cx, cy = x0 + PW / 2, 165
    ch = [(cx + 36, cy, +1), (cx - 36, cy, -1)]
    field_lines(f, ch, (x0 + 3, 3, x0 + PW - 3, H - 3), n_per_unit=11, c=MAG, w=1.6, r0=10, stop_r=9, sources=[ch[0]])
    for dy in (-7, 0, 7):
        f.line(cx - 34, cy + dy, cx + 34, cy + dy, MAG, 1.6)
        f.head(cx + 8, cy + dy, 0, MAG, 8)
    f.rect(cx - 42, cy - 14, 42, 28, MAG_L, MAG_D, 2.2, rx=3)
    f.rect(cx, cy - 14, 42, 28, MAG_D, MAG_D, 2.2, rx=3)
    f.text(cx - 21, cy + 6, "S", 16, MAG_D, weight=700, lint=False)
    f.text(cx + 21, cy + 6, "N", 16, "#fff", weight=700, lint=False)
    return f
