"""Bloco A · página 3 — eletronegatividade e tipos de ligação."""
import math

from registry import fig
from svglib import SVG, C, tw
from figlib import pill2, pol, sphere_h


@fig("a_en_escala")
def _en_escala():
    W, H = 695, 150
    s = SVG(W, H, title="Escala de eletronegatividade de Pauling")
    x0, x1 = 26, 669

    def X(v):
        return x0 + (v - 0.7) / (4.1 - 0.7) * (x1 - x0)

    by, bh = 72, 14
    g = s.lingrad([(0, "#F5F9FF"), (0.5, "#8DBBF2"), (1, C["blue_d"])])
    s.text(x0, 12, "Eletronegatividade (Pauling): tendência de atrair o par de elétrons da ligação", 11, "start", 700, C["blue_d"])
    s.text(x1, 12, "← metais · ametais →", 10.2, "end", 700, C["muted"])
    s.rect(x0, by, x1 - x0, bh, fill=g, stroke=C["blue_m"], sw=1, rx=7)
    els = [("K", 0.82, 1), ("Na", 0.93, 1), ("Ca", 1.00, 1), ("Mg", 1.31, 1), ("Al", 1.61, 1), ("Si", 1.90, 1),
           ("P", 2.19, 0), ("H", 2.20, 0), ("C", 2.55, 0), ("S", 2.58, 0), ("I", 2.66, 0), ("Br", 2.96, 0),
           ("N", 3.04, 0), ("Cl", 3.16, 0), ("O", 3.44, 0), ("F", 3.98, 0)]
    ys = {0: by - 22, 1: by + bh + 24, 2: by - 46, 3: by + bh + 46}
    for i, (sym, v, metal) in enumerate(els):
        lvl = i % 4
        cy = ys[lvl]
        x = X(v)
        top = lvl in (0, 2)
        if top:
            s.line(x, cy + 8.5, x, by, C["slate_m"] if metal else C["blue_m"], 1.0)
        else:
            s.line(x, by + bh, x, cy - 8.5, C["slate_m"] if metal else C["blue_m"], 1.0)
        s.circle(x, by + bh / 2, 3.4, fill="#FFFFFF", stroke=C["blue_d"], sw=1.3)
        val = f"{v:.2f}".replace(".", ",")
        if metal:
            pill2(s, x, cy, sym, val, "#FFFFFF", C["slate_m"], C["slate"])
        else:
            pill2(s, x, cy, sym, val, C["blue_l"], C["blue"], C["blue_d"])
    return s


@fig("a_continuo")
def _continuo():
    W, H = 695, 110
    s = SVG(W, H, title="Contínuo de tipos de ligação segundo ΔEN")
    x0, x1 = 30, 665

    def X(d):
        return x0 + d / 3.4 * (x1 - x0)

    by, bh = 34, 14
    g = s.lingrad([(0, C["amber_m"]), (0.22, "#F6E3B0"), (0.34, "#CFE1F8"), (1, C["blue"])])
    s.rect(x0, by, x1 - x0, bh, fill=g, stroke=C["line"], sw=1, rx=7)
    for d in (0.4, 1.7):
        s.line(X(d), by - 6, X(d), by + bh + 4, C["muted"], 1.1, dash="3 3")
    s.text(X(0.2) + 8, by - 10, "covalente apolar", 10.6, "middle", 700, C["amber_d"])
    s.text((X(0.4) + X(1.7)) / 2, by - 10, "covalente polar", 10.6, "middle", 700, C["blue_d"])
    s.text((X(1.7) + x1) / 2, by - 10, "iônica (predominante)", 10.6, "middle", 700, C["blue_d"])
    s.text(X(0.4), by - 22, "≈ 0,4", 9.2, "middle", 600, C["muted"])
    s.text(X(1.7), by - 22, "≈ 1,7", 9.2, "middle", 600, C["muted"])
    s.text(x1, by - 22, "ΔEN →", 10, "end", 700, C["ink"])
    ex = [("Cl–Cl", 0.0, 0), ("C–H", 0.35, 1), ("H–Cl", 0.96, 0), ("O–H", 1.24, 1), ("H–F", 1.78, 0), ("Na–Cl", 2.23, 1),
          ("K–F", 3.16, 0)]
    for lab, d, lv in ex:
        x = X(d)
        cy = by + bh + 19 + lv * 23
        s.line(x, by + bh, x, cy - 8.5, C["slate_m"], 1.0)
        s.circle(x, by + bh / 2, 3.4, fill="#FFFFFF", stroke=C["ink"], sw=1.3)
        val = f"{d:.2f}".replace(".", ",")
        pill2(s, x, cy, lab, val, "#FFFFFF", C["line"], C["ink"])
    return s


# ----------------------------------------------------------------------------- três tipos de ligação
@fig("a_lig_ionica")
def _ionica():
    W, H = 236, 148
    s = SVG(W, H, title="Ligação iônica")
    ink = C["ink"]

    def lewis(cx, cy, sym, pairs, singles, size=13):
        s.text(cx, cy + 4.6, sym, size, "middle", 700, ink)
        off = {0: (0, -11), 1: (13, 0), 2: (0, 11), 3: (-13, 0)}
        for k in pairs:
            ox, oy = off[k]
            if k in (0, 2):
                s.circle(cx + ox - 2.4, cy + oy, 1.7, fill=ink)
                s.circle(cx + ox + 2.4, cy + oy, 1.7, fill=ink)
            else:
                s.circle(cx + ox, cy + oy - 2.4, 1.7, fill=ink)
                s.circle(cx + ox, cy + oy + 2.4, 1.7, fill=ink)
        for k in singles:
            ox, oy = off[k]
            s.circle(cx + ox, cy + oy, 1.7, fill=ink)

    cy0 = 26
    lewis(20, cy0, "Na", [], [1])
    s.text(44, cy0 + 5, "+", 15, "middle", 600, C["muted"])
    lewis(72, cy0, "Cl", [0, 2, 3], [1])
    s.carrow(33, cy0 - 12, 52, cy0 - 26, 68, cy0 - 12, C["orange"], 1.5, 6)
    s.arrow(100, cy0, 122, cy0, C["orange"], 2, 7)
    s.text(138, cy0 + 5, "Na", 13, "start", 700, ink)
    s.text(158, cy0 - 3, "+", 10.5, "start", 700, ink)
    s.text(168, cy0 + 7, "[", 20, "middle", 400, ink)
    lewis(188, cy0, "Cl", [0, 1, 2, 3], [])
    s.text(207, cy0 + 7, "]", 20, "middle", 400, ink)
    s.text(213, cy0 - 5, "−", 11, "start", 700, ink)
    s.text(118, 56, "1 elétron passa do Na para o Cl", 10, "middle", 600, C["muted"])
    gx, gy = 36, 78
    dx, dy = 32, 25
    for r in range(3):
        for c in range(4):
            x, y = gx + c * dx, gy + r * dy
            if c < 3:
                s.line(x, y, x + dx, y, C["slate_m"], 1.0, dash="2 3")
            if r < 2:
                s.line(x, y, x, y + dy, C["slate_m"], 1.0, dash="2 3")
    for r in range(3):
        for c in range(4):
            x, y = gx + c * dx, gy + r * dy
            if (r + c) % 2 == 0:
                sphere_h(s, x, y, 8, "#B79DFB", "#6D4BD0", "+", "#fff", 11)
            else:
                sphere_h(s, x, y, 11, "#4FC083", "#1F7A45", "−", "#fff", 13)
    s.text(176, 88, "retículo", 11, "start", 700, ink)
    s.text(176, 101, "cristalino", 11, "start", 700, ink)
    s.text(176, 117, "atração em", 10, "start", 400, C["muted"])
    s.text(176, 129, "todas as", 10, "start", 400, C["muted"])
    s.text(176, 141, "direções", 10, "start", 400, C["muted"])
    return s


@fig("a_lig_cov")
def _cov():
    W, H = 236, 148
    s = SVG(W, H, title="Ligação covalente apolar e polar")
    ink = C["ink"]
    cy = 30
    s.circle(56, cy, 21, fill=C["amber_l"], stroke=C["amber_m"], sw=1.3)
    s.circle(92, cy, 21, fill=C["amber_l"], stroke=C["amber_m"], sw=1.3, opacity=0.9)
    s.text(45, cy + 4.5, "Cl", 12.5, "middle", 700, ink)
    s.text(103, cy + 4.5, "Cl", 12.5, "middle", 700, ink)
    s.circle(74 - 2.6, cy, 2, fill=ink)
    s.circle(74 + 2.6, cy, 2, fill=ink)
    s.text(126, cy - 7, "Cl_2 · apolar", 11, "start", 700, C["amber_d"])
    s.text(126, cy + 6, "ΔEN = 0", 10, "start", 600, C["muted"])
    s.text(126, cy + 18, "nuvem simétrica", 10, "start", 400, C["muted"])
    cy = 98
    s.circle(42, cy, 15, fill=C["blue_l"], stroke=C["blue_m"], sw=1.3)
    s.circle(80, cy, 23, fill=C["blue_l"], stroke=C["blue_m"], sw=1.3, opacity=0.95)
    s.text(36, cy + 4.5, "H", 12.5, "middle", 700, ink)
    s.text(91, cy + 4.5, "Cl", 12.5, "middle", 700, ink)
    s.circle(60 + 4.6 - 2.6, cy, 2, fill=ink)
    s.circle(60 + 4.6 + 2.6, cy, 2, fill=ink)
    s.text(30, cy - 22, "δ+", 11.5, "middle", 700, C["blue_d"], halo="#fff")
    s.text(94, cy - 27, "δ−", 11.5, "middle", 700, C["blue_d"], halo="#fff")
    s.dipole(30, cy + 31, 98, cy + 31, C["blue_d"], 1.8, 7)
    s.text(126, cy - 7, "HCl · polar", 11, "start", 700, C["blue_d"])
    s.text(126, cy + 6, "ΔEN ≈ 0,96", 10, "start", 600, C["muted"])
    s.text(126, cy + 18, "par deslocado p/ Cl", 10, "start", 400, C["muted"])
    return s


@fig("a_lig_met")
def _met():
    W, H = 236, 148
    s = SVG(W, H, title="Ligação metálica: cátions e mar de elétrons")
    import random
    s.rect(6, 6, 152, 108, fill=C["slate_l"], stroke=C["slate_m"], sw=1, rx=12, dash="4 3")
    rnd = random.Random(11)
    for _ in range(30):
        s.circle(rnd.uniform(14, 150), rnd.uniform(14, 106), 2.0, fill=C["ink"], opacity=0.85)
    for r in range(3):
        for c in range(4):
            sphere_h(s, 28 + c * 34, 24 + r * 33, 10, "#94A3B8", "#475569", "+", "#fff", 13)
    s.arrow(16, 128, 148, 128, C["slate"], 1.5, 6)
    s.text(82, 144, "elétrons livres conduzem corrente", 10, "middle", 600, C["slate"])
    s.text(166, 40, "cátions", 11, "start", 700, C["slate"])
    s.text(166, 53, "metálicos", 11, "start", 700, C["slate"])
    s.text(166, 66, "fixos", 10, "start", 400, C["muted"])
    s.circle(168, 86, 2.2, fill=C["ink"])
    s.text(175, 90, "elétrons", 11, "start", 700, C["ink"])
    s.text(166, 103, "deslocalizados", 10, "start", 400, C["muted"])
    return s
