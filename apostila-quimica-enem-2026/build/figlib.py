"""Elementos de desenho reutilizáveis nas figuras (moléculas 3D esquemáticas, pílulas, cunhas...)."""
import math

from svglib import C, ATOM, tw, tspans, n


def rad(a):
    return a * math.pi / 180.0


def pol(cx, cy, r, ang):
    """ponto em coordenadas de tela (y para baixo): ang em graus a partir de +x, sentido horário."""
    return cx + r * math.cos(rad(ang)), cy + r * math.sin(rad(ang))


def pill2(s, cx, cy, sym, val, fill, stroke, color, size=10.5, h=17):
    """Pílula com símbolo em negrito e valor normal."""
    w1 = tw(sym, size + 0.5, 700)
    w2 = tw(val, size - 0.5, 400)
    w = w1 + w2 + 4 + 12
    s.rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=stroke, sw=1.1, rx=h / 2)
    s.text(cx - w / 2 + 6, cy + size * 0.34, sym, size + 0.5, "start", 700, color)
    s.text(cx - w / 2 + 6 + w1 + 4, cy + size * 0.34, val, size - 0.5, "start", 400, color)
    return w


def atom_ball(s, cx, cy, el, r=None, label=None, size=None):
    base = ATOM.get(el, ("#CBD5E1", "#64748B", 1.0))[2]
    r = r or 10 * base
    s.ball(cx, cy, r, el, size=size or r * 1.0, label=label)
    return r


def water(s, cx, cy, a1=37.75, a2=142.25, scale=1.0, label=True, hlabel=False, lp=False):
    """Molécula de água 2D: O em (cx,cy); H nos ângulos absolutos a1,a2 (graus, tela)."""
    L = 21 * scale
    rO, rH = 10.5 * scale, 6.2 * scale
    for a in (a1, a2):
        x, y = pol(cx, cy, L, a)
        s.line(cx, cy, x, y, "#6B7280", 2.2 * scale)
    for a in (a1, a2):
        x, y = pol(cx, cy, L, a)
        s.ball(x, y, rH, "H", label="H" if hlabel else "")
    s.ball(cx, cy, rO, "O", size=11 * scale if label else 1, label="O" if label else "")
    return [pol(cx, cy, L, a) for a in (a1, a2)]


def wedge(s, x1, y1, x2, y2, color="#1F2937", w=6.5):
    """Ligação em cunha (para a frente): estreita em (x1,y1), larga em (x2,y2)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    px, py = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    s.poly([(x1, y1), (x2 + px, y2 + py), (x2 - px, y2 - py)], fill=color)


def dashwedge(s, x1, y1, x2, y2, color="#1F2937", w=6.5, n_dash=6):
    """Ligação tracejada (para trás)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    px, py = -math.sin(ang), math.cos(ang)
    for i in range(1, n_dash + 1):
        t = i / n_dash
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        half = w / 2 * t
        s.line(x - px * half, y - py * half, x + px * half, y + py * half, color, 1.6, cap="butt")


def lone_pair(s, cx, cy, ang, dist=15, color="#1F2937", r=1.9, sep=3.4):
    """Par de elétrons livres (dois pontos) na direção ang em torno de (cx,cy)."""
    x, y = pol(cx, cy, dist, ang)
    px, py = -math.sin(rad(ang)), math.cos(rad(ang))
    s.circle(x + px * sep, y + py * sep, r, fill=color)
    s.circle(x - px * sep, y - py * sep, r, fill=color)


def delta(s, x, y, sign, size=11, color=None, anchor="middle"):
    t = "δ+" if sign > 0 else "δ−"
    col = color or (C["blue_d"] if sign > 0 else C["blue_d"])
    s.text(x, y, t, size, anchor, 700, col, halo="#FFFFFF")


def chip_svg(s, x, y, text, kind="blue", size=10.5, anchor="middle", weight=700, padx=7, h=None):
    """Pílula semântica (blue/amber/purple/green/orange/red)."""
    fills = {
        "blue": (C["blue_l"], C["blue_m"], C["blue_d"]),
        "amber": (C["amber_l"], C["amber_m"], C["amber_d"]),
        "purple": (C["purple_l"], C["purple_m"], C["purple_d"]),
        "green": (C["green_l"], C["green_m"], C["green_d"]),
        "orange": (C["orange_l"], C["orange_m"], C["orange_d"]),
        "red": (C["red_l"], C["red_m"], C["red_d"]),
        "slate": (C["slate_l"], C["slate_m"], C["slate"]),
        "white": ("#FFFFFF", C["line"], C["ink"]),
    }
    f, st, col = fills[kind]
    return s.tag(x, y, text, size, fill=f, stroke=st, color=col, weight=weight, padx=padx, anchor=anchor, h=h)


def zigzag(s, x, y, nseg, dx=12, dy=7, color="#1F2937", sw=2.2, start_up=False):
    """Cadeia em zigue-zague; retorna lista de pontos."""
    pts = [(x, y)]
    up = start_up
    for i in range(nseg):
        x += dx
        y += -dy if up else dy
        up = not up
        pts.append((x, y))
    s.poly(pts, stroke=color, sw=sw, close=False)
    return pts


def sphere_h(s, cx, cy, r, fill, stroke, label=None, lab_color="#fff", size=None):
    s.circle(cx, cy, r, fill=fill, stroke=stroke, sw=1.3)
    s.ellipse(cx - r * 0.3, cy - r * 0.35, r * 0.36, r * 0.24, fill="#FFFFFF", opacity=0.35, rot=-30)
    if label:
        s.text(cx, cy + (size or r) * 0.36, label, size or r, "middle", 700, lab_color)
