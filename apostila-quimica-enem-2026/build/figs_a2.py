"""Bloco A · página 4 — geometria molecular e polaridade (seis moléculas + ícones de geometria)."""
import math

from registry import fig
from svglib import SVG, C, tw
from figlib import pol, wedge, dashwedge, lone_pair, sphere_h, chip_svg

INK = C["ink"]
BOND = "#6B7280"
DIP = C["blue"]
DIPD = C["blue_d"]


def _sph(s, cx, cy, el, r=None, label=None):
    base = {"H": 8.5, "C": 11.5, "O": 13.5, "N": 12.5, "Cl": 14, "S": 13.5, "F": 11, "B": 11, "Xe": 15}
    r = r or base[el]
    fill, stroke = {
        "H": ("#FFFFFF", "#6B7280"), "C": ("#4B5563", "#1F2937"), "O": ("#E5484D", "#9B1C22"),
        "N": ("#4C6FD6", "#2B3F8F"), "Cl": ("#3DB36B", "#1F7A45"), "S": ("#E8C33C", "#9A7B10"),
        "F": ("#8FD9A8", "#3E9A5E"), "B": ("#E3A27B", "#9A5A33"), "Xe": ("#9AA8C5", "#53628A"),
    }[el]
    lab = label if label is not None else el
    tcol = "#1F2937" if el in ("H", "S", "F") else "#FFFFFF"
    s.circle(cx, cy, r, fill=fill, stroke=stroke, sw=1.3)
    s.ellipse(cx - r * 0.3, cy - r * 0.36, r * 0.36, r * 0.24, fill="#FFFFFF", opacity=0.36, rot=-30)
    s.text(cx, cy + r * 0.36, lab, r * 1.02, "middle", 700, tcol)


def _bond(s, p, q, kind="plain", double=False, w=3.0):
    (x1, y1), (x2, y2) = p, q
    if kind == "wedge":
        wedge(s, x1, y1, x2, y2, BOND, 9)
    elif kind == "dash":
        dashwedge(s, x1, y1, x2, y2, BOND, 9, 6)
    elif double:
        ang = math.atan2(y2 - y1, x2 - x1)
        px, py = -math.sin(ang) * 2.8, math.cos(ang) * 2.8
        s.line(x1 + px, y1 + py, x2 + px, y2 + py, BOND, 2.6)
        s.line(x1 - px, y1 - py, x2 - px, y2 - py, BOND, 2.6)
    else:
        s.line(x1, y1, x2, y2, BOND, w)


def _dip(s, a, b, off=(0, 0), f0=0.28, f1=0.72, color=DIP, sw=1.6, head=6.5):
    """Dipolo de ligação: de a (δ+, com cruz) até b (δ−, ponta), deslocado por off."""
    ax, ay = a
    bx, by = b
    x1, y1 = ax + (bx - ax) * f0 + off[0], ay + (by - ay) * f0 + off[1]
    x2, y2 = ax + (bx - ax) * f1 + off[0], ay + (by - ay) * f1 + off[1]
    s.dipole(x1, y1, x2, y2, color, sw, head, tick=3.4)


def _res(s, x, y1, y2, label="μ_R ≠ 0", lx=None, ly=None, color=DIPD):
    """Vetor resultante (vertical, de y1 para y2) com rótulo."""
    s.dipole(x, y1, x, y2, color, 2.8, 9, tick=4.5)


W, H = 227, 138


@fig("a_mol_h2o")
def _h2o():
    s = SVG(W, H, title="Água: angular, polar")
    O, H1, H2 = (113, 52), (72, 88), (154, 88)
    _bond(s, O, H1)
    _bond(s, O, H2)
    for a in (-122, -58):
        lone_pair(s, O[0], O[1], a, 24, INK)
    _sph(s, *H1, "H")
    _sph(s, *H2, "H")
    _sph(s, *O, "O")
    _dip(s, H1, O, off=(-7, -8), f0=0.3, f1=0.7)
    _dip(s, H2, O, off=(7, -8), f0=0.3, f1=0.7)
    s.text(148, 36, "δ−", 12, "middle", 700, DIPD, halo="#fff")
    s.text(60, 110, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    s.text(166, 110, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    _res(s, 206, 100, 44)
    s.text(198, 78, "μ_R", 12, "end", 700, DIPD)
    s.text(198, 91, "≠ 0", 11, "end", 700, DIPD)
    s.text(113, 132, "2 pares livres no O", 10, "middle", 600, C["muted"])
    return s


@fig("a_mol_co2")
def _co2():
    s = SVG(W, H, title="Dióxido de carbono: linear, apolar")
    O1, Cc, O2 = (36, 80), (113, 80), (190, 80)
    _bond(s, O1, Cc, double=True)
    _bond(s, Cc, O2, double=True)
    _sph(s, *O1, "O")
    _sph(s, *O2, "O")
    _sph(s, *Cc, "C")
    s.dipole(106, 46, 58, 46, DIP, 2.2, 8, tick=3.8)
    s.dipole(120, 46, 168, 46, DIP, 2.2, 8, tick=3.8)
    s.text(36, 30, "δ−", 12, "middle", 700, DIPD, halo="#fff")
    s.text(190, 30, "δ−", 12, "middle", 700, DIPD, halo="#fff")
    s.text(113, 30, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    chip_svg(s, 113, 120, "vetores se anulam: μ_R = 0", "amber", 10.5)
    return s


@fig("a_mol_nh3")
def _nh3():
    s = SVG(W, H, title="Amônia: piramidal, polar")
    N, H1, H2, H3 = (113, 50), (66, 96), (160, 96), (113, 118)
    _bond(s, N, H1)
    _bond(s, N, H2)
    _bond(s, N, H3, "wedge")
    lone_pair(s, N[0], N[1], -90, 25, INK)
    _sph(s, *H1, "H")
    _sph(s, *H2, "H")
    _sph(s, *H3, "H")
    _sph(s, *N, "N")
    _dip(s, H1, N, off=(-7, -7), f0=0.32, f1=0.7)
    _dip(s, H2, N, off=(7, -7), f0=0.32, f1=0.7)
    s.text(146, 32, "δ−", 12, "middle", 700, DIPD, halo="#fff")
    s.text(52, 114, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    s.text(174, 114, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    s.text(138, 132, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    _res(s, 206, 100, 44)
    s.text(198, 78, "μ_R", 12, "end", 700, DIPD)
    s.text(198, 91, "≠ 0", 11, "end", 700, DIPD)
    return s


def _tetra(s, Cpos, ligs, ctr_el="C"):
    """ligs: dict com posições a(cima, plano), b(baixo-esq., plano), c(baixo-dir., cunha), d(cima-dir., tracejado)."""
    _bond(s, Cpos, ligs["a"])
    _bond(s, Cpos, ligs["b"])
    _bond(s, Cpos, ligs["c"], "wedge")
    _bond(s, Cpos, ligs["d"], "dash")


TPOS = {"a": (113, 22), "b": (62, 106), "c": (168, 108), "d": (164, 42)}
TC = (113, 70)


@fig("a_mol_ch4")
def _ch4():
    s = SVG(W, H, title="Metano: tetraédrico, apolar")
    _tetra(s, TC, TPOS)
    for k in ("d", "a", "b", "c"):
        _sph(s, *TPOS[k], "H")
    _sph(s, *TC, "C")
    s.text(198, 66, "C–H", 10.5, "middle", 700, C["muted"])
    s.text(198, 78, "ΔEN 0,35", 10, "middle", 600, C["muted"])
    s.text(198, 90, "(baixa)", 10, "middle", 600, C["muted"])
    chip_svg(s, 113, 128, "simétrica: μ_R = 0", "amber", 10.5)
    return s


@fig("a_mol_ccl4")
def _ccl4():
    s = SVG(W, H, title="Tetracloreto de carbono: tetraédrico, apolar")
    P = {"a": (113, 20), "b": (60, 106), "c": (168, 108), "d": (166, 40)}
    _tetra(s, TC, P)
    for k in ("d", "a", "b", "c"):
        _sph(s, *P[k], "Cl")
    _sph(s, *TC, "C", 10.5)
    offs = {"a": (10, 0), "b": (-6, -8), "c": (7, -8), "d": (5, 9)}
    for k in ("a", "b", "c", "d"):
        _dip(s, TC, P[k], off=offs[k], f0=0.30, f1=0.62, sw=1.5, head=5.5)
    chip_svg(s, 113, 128, "4 vetores se anulam: μ_R = 0", "amber", 10.5)
    return s


@fig("a_mol_ch3cl")
def _ch3cl():
    s = SVG(W, H, title="Clorometano: tetraédrico, polar")
    P = {"a": (113, 20), "b": (62, 106), "c": (168, 108), "d": (164, 42)}
    _tetra(s, TC, P)
    _sph(s, *P["d"], "H")
    _sph(s, *P["b"], "H")
    _sph(s, *P["c"], "H")
    _sph(s, *P["a"], "Cl")
    _sph(s, *TC, "C")
    _dip(s, TC, P["a"], off=(12, 0), f0=0.18, f1=0.74, sw=2.2, head=7)
    s.text(78, 22, "δ−", 12, "middle", 700, DIPD, halo="#fff")
    s.text(92, 70, "δ+", 12, "middle", 700, DIPD, halo="#fff")
    _res(s, 206, 108, 36)
    s.text(198, 78, "μ_R", 12, "end", 700, DIPD)
    s.text(198, 91, "≠ 0", 11, "end", 700, DIPD)
    return s


# ----------------------------------------------------------------------------- ícones de geometrias
@fig("a_geometrias")
def _geoms():
    Wd, Ht = 695, 120
    s = SVG(Wd, Ht, title="Geometrias moleculares básicas")
    cw = Wd / 5
    items = [
        ("Linear", "180°", "CO_2, HCN, BeCl_2"),
        ("Trigonal plana", "120°", "BF_3, SO_3"),
        ("Angular", "≈104,5° (2 pares livres)", "H_2O, H_2S"),
        ("Piramidal", "≈107° (1 par livre)", "NH_3, PH_3"),
        ("Tetraédrica", "109,5°", "CH_4, CCl_4, CH_3Cl"),
    ]
    cy = 43
    for i, (nm, ang, ex) in enumerate(items):
        cx = cw * i + cw / 2
        if i == 0:
            a, b, c = (cx - 34, cy), (cx, cy), (cx + 34, cy)
            s.line(*a, *b, BOND, 3)
            s.line(*b, *c, BOND, 3)
            _sph(s, *a, "H", 9, "X")
            _sph(s, *c, "H", 9, "X")
            _sph(s, *b, "C", 11, "A")
        elif i == 1:
            b = (cx, cy)
            pts = [pol(cx, cy, 31, a) for a in (-90, 30, 150)]
            for p in pts:
                s.line(*b, *p, BOND, 3)
            for p in pts:
                _sph(s, *p, "H", 9, "X")
            _sph(s, *b, "C", 11, "A")
        elif i == 2:
            b = (cx, cy - 8)
            pts = [pol(b[0], b[1], 34, a) for a in (50, 130)]
            for p in pts:
                s.line(*b, *p, BOND, 3)
            lone_pair(s, b[0], b[1], -125, 17, INK, 1.7, 3)
            lone_pair(s, b[0], b[1], -55, 17, INK, 1.7, 3)
            for p in pts:
                _sph(s, *p, "H", 9, "X")
            _sph(s, *b, "C", 11, "A")
        elif i == 3:
            b = (cx, cy - 10)
            p1, p2, p3 = (cx - 34, cy + 18), (cx + 34, cy + 18), (cx, cy + 26)
            s.line(*b, *p1, BOND, 3)
            s.line(*b, *p2, BOND, 3)
            wedge(s, b[0], b[1], p3[0], p3[1], BOND, 8)
            lone_pair(s, b[0], b[1], -90, 18, INK, 1.7, 3)
            for p in (p1, p2, p3):
                _sph(s, *p, "H", 9, "X")
            _sph(s, *b, "C", 11, "A")
        else:
            b = (cx, cy + 2)
            pa, pb, pc, pd = (cx, cy - 27), (cx - 31, cy + 23), (cx + 33, cy + 25), (cx + 31, cy - 18)
            s.line(*b, *pa, BOND, 3)
            s.line(*b, *pb, BOND, 3)
            wedge(s, b[0], b[1], pc[0], pc[1], BOND, 8)
            dashwedge(s, b[0], b[1], pd[0], pd[1], BOND, 8, 5)
            for p in (pd, pa, pb, pc):
                _sph(s, *p, "H", 9, "X")
            _sph(s, *b, "C", 11, "A")
        s.text(cx, 90, nm, 11.5, "middle", 700, C["ink"])
        s.text(cx, 103, ang, 10, "middle", 600, C["blue_d"])
        s.text(cx, 115, ex, 10, "middle", 400, C["muted"])
    return s
