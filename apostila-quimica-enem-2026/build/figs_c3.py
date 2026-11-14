"""Bloco C · página 17 — tensoativos: limpeza, tensão superficial, estrutura."""
import math
import random

from registry import fig
from svglib import SVG, C, tw
from figlib import pol, chip_svg
from mol import mol

INK = C["ink"]
HEAD_F, HEAD_S = "#8DBBF2", C["blue"]
TAIL = C["amber"]


def surf(s, x, y, ang, tail=13, r=3.9, sign=None, sw=1.8):
    """Molécula tensoativa em (x,y)=posição da cabeça; ang = direção cabeça→cauda (graus, tela)."""
    ex, ey = pol(x, y, tail + r, ang)
    s.line(*pol(x, y, r * 0.8, ang), ex, ey, TAIL, sw)
    s.circle(x, y, r, fill=HEAD_F, stroke=HEAD_S, sw=1.2)


def _tail_zz(s, x, y, n=6, step=9, amp=5.5):
    pts = [(x, y)]
    for i in range(n):
        pts.append((pts[-1][0] + step, y + (-amp if i % 2 == 0 else 0)))
    s.poly(pts, stroke=TAIL, sw=2.6, close=False)


@fig("c_ico_anionico")
def _ia():
    s = SVG(110, 34)
    s.circle(16, 17, 9.5, fill=HEAD_F, stroke=HEAD_S, sw=1.4)
    s.text(16, 21, "−", 14, "middle", 800, C["blue_d"])
    _tail_zz(s, 26, 21)
    return s


@fig("c_ico_cationico")
def _ic():
    s = SVG(110, 34)
    s.circle(16, 17, 9.5, fill=HEAD_F, stroke=HEAD_S, sw=1.4)
    s.text(16, 21, "+", 13, "middle", 800, C["blue_d"])
    _tail_zz(s, 26, 21)
    return s


@fig("c_ico_naoionico")
def _in():
    s = SVG(110, 34)
    for i in range(4):
        s.circle(8 + i * 10, 17, 4.6, fill=HEAD_F, stroke=HEAD_S, sw=1.2)
    s.line(8, 17, 38, 17, HEAD_S, 1.4)
    _tail_zz(s, 50, 21, 5)
    return s


@fig("c_ico_anfotero")
def _iz():
    s = SVG(110, 34)
    s.circle(11, 9, 6.6, fill=HEAD_F, stroke=HEAD_S, sw=1.3)
    s.text(11, 12.4, "+", 10, "middle", 800, C["blue_d"])
    s.circle(11, 25, 6.6, fill=HEAD_F, stroke=HEAD_S, sw=1.3)
    s.text(11, 28.4, "−", 10, "middle", 800, C["blue_d"])
    _tail_zz(s, 20, 21)
    return s


@fig("c_limpeza")
def _limpeza():
    W, H = 695, 160
    s = SVG(W, H, title="Como o sabão e o detergente removem a gordura")
    cw = W / 3
    rnd = random.Random(12)
    titles = ["1 · Gordura aderida ao tecido", "2 · Tensoativos se orientam", "3 · Gotícula destacada (micela)"]
    for i, t in enumerate(titles):
        x = i * cw
        s.rect(x + 4, 4, cw - 8, H - 8, fill=C["blue_l"], stroke=C["blue_m"], sw=1.2, rx=10)
        s.text(x + cw / 2, 21, t, 11.6, "middle", 800, C["blue_d"])
        s.text(x + cw / 2, H - 8, ["água + tensoativos soltos", "caudas entram na gordura", "gordura no núcleo apolar"][i],
               10, "middle", 600, C["muted"])
    # tecido (painéis 1 e 2)
    for i in (0, 1):
        x = i * cw
        pts = [(x + 14 + k * 8, 132 + (3 if k % 2 else 0)) for k in range(int((cw - 28) / 8) + 1)]
        s.poly(pts, stroke=C["slate_m"], sw=3.2, close=False)
    # painel 1
    cx = cw / 2
    s.ellipse(cx, 120, 48, 14, fill=C["amber_m"], stroke=C["amber"], sw=1.4)
    s.text(cx, 124, "gordura", 10.4, "middle", 800, C["amber_d"])
    for _ in range(9):
        sx, sy = rnd.uniform(24, cw - 24), rnd.uniform(40, 88)
        surf(s, sx, sy, rnd.uniform(0, 360))
    # painel 2
    x2 = cw
    cx = x2 + cw / 2
    s.ellipse(cx, 120, 48, 14, fill=C["amber_m"], stroke=C["amber"], sw=1.4)
    s.text(cx, 124, "gordura", 10.4, "middle", 800, C["amber_d"])
    for k in range(9):
        a = 190 + k * 20
        px, py = cx + 56 * math.cos(math.radians(a)), 120 + 22 * math.sin(math.radians(a))
        # cabeça fora, cauda apontando para a gordura
        tx, ty = cx + 48 * math.cos(math.radians(a)), 120 + 14 * math.sin(math.radians(a))
        ang = math.degrees(math.atan2(ty - py, tx - px))
        surf(s, px, py, ang, tail=11)
    for _ in range(4):
        surf(s, x2 + rnd.uniform(24, cw - 24), rnd.uniform(40, 80), rnd.uniform(0, 360))
    # painel 3: micela com gordura
    x3 = 2 * cw
    cx = x3 + cw / 2
    cy = 74
    s.circle(cx, cy, 16, fill=C["amber_m"], stroke=C["amber"], sw=1.2)
    s.text(cx, cy + 3.4, "gordura", 8.8, "middle", 800, C["amber_d"])
    n = 16
    for k in range(n):
        a = k * 360 / n
        px, py = pol(cx, cy, 38, a)
        surf(s, px, py, a + 180, tail=17, r=4.2)
    s.arrow(x3 + 24, 136, x3 + cw - 24, 136, C["slate"], 1.6, 6)
    s.text(cx, 131, "arrastada pela água", 9.8, "middle", 700, C["slate"], halo="#E6F0FD")
    # setas entre painéis
    for i in (1, 2):
        xx = i * cw
        s.arrow(xx - 5, 80, xx + 5, 80, C["orange"], 2, 6)
    return s


@fig("c_tensao")
def _tensao():
    W, H = 340, 150
    s = SVG(W, H, title="Tensão superficial da água pura e com tensoativo")
    hw = W / 2
    rnd = random.Random(4)
    for i, (t, sub) in enumerate([("Água pura", "tensão superficial alta"), ("Água + tensoativo", "tensão superficial menor")]):
        x = i * hw
        s.rect(x + 3, 3, hw - 6, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + hw / 2, 18, t, 11.4, "middle", 800, C["blue_d"])
        s.rect(x + 14, 58, hw - 28, 72, fill=C["blue_l"], stroke=C["blue_m"], sw=1.2, rx=4)
        s.text(x + hw / 2, 143, sub, 10, "middle", 700, C["muted"])
        s.text(x + hw / 2, 40, "ar", 10, "middle", 600, C["muted"])
    # água pura: moléculas com setas
    for r in range(3):
        for c in range(6):
            cx, cy = 28 + c * 25, 70 + r * 19
            s.circle(cx, cy, 6.6, fill="#8DBBF2", stroke=C["blue"], sw=1.1)
    for c in (1, 2, 3, 4):
        cx, cy = 28 + c * 25, 70
        s.arrow(cx, cy + 8, cx, cy + 20, C["blue_d"], 1.6, 5)
    s.text(84, 56, "forças coesivas puxam a superfície para dentro", 8.8, "middle", 700, C["blue_d"]) if False else None
    # com tensoativo
    for r in range(3):
        for c in range(6):
            cx, cy = hw + 28 + c * 25, 80 + r * 19
            s.circle(cx, cy, 6.2, fill="#8DBBF2", stroke=C["blue"], sw=1.1)
    for c in range(7):
        px = hw + 22 + c * 22.5
        surf(s, px, 66, -90, tail=14, r=4.4)
    return s


@fig("c_abs_las")
def _abs_las():
    W, H = 340, 150
    s = SVG(W, H, title="Detergente de cadeia linear × ramificada")
    las = mol("CCCCCCCCCCCCc1ccc(cc1)S(=O)(=O)[O-]", bond=22, font=0.66, lw=1.6, margin=4, horizontal=True,
              hl=["S(=O)(=O)[O-]"])
    br = mol("CC(C)CC(C)CC(C)CC(C)c1ccc(cc1)S(=O)(=O)[O-]", bond=22, font=0.66, lw=1.6, margin=4, horizontal=True,
             hl=["S(=O)(=O)[O-]"])
    s.raw(las.at(W / 2, 34, min(1.0, 320 / las.w, 46 / las.h)))
    s.text(W / 2, 66, "linear (LAS): degradação microbiana em geral mais fácil", 10.6, "middle", 700, C["green_d"])
    s.raw(br.at(W / 2, 108, min(1.0, 320 / br.w, 46 / br.h)))
    s.text(W / 2, 140, "muito ramificado (tipo ABS): foi persistente em rios", 10.6, "middle", 700, C["red_d"])
    return s
