"""Biblioteca mínima para gerar SVG vetorial legível (diagramas e gráficos científicos).

Convenções de cor semântica (usadas em toda a apostila):
  azul   -> água, polaridade, hidrofilicidade
  âmbar  -> apolar, gorduras, lipofilicidade, hidrofobicidade
  roxo   -> funções orgânicas e grupos funcionais
  verde  -> Biologia e meio ambiente
  laranja-> reações e transformações
  vermelho-> erros frequentes, exceções, alertas
"""
import math
import os
import re
from itertools import count

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "assets", "fonts")

C = {
    "ink": "#1F2937", "muted": "#5B6575", "line": "#CBD5E1", "grid": "#E5EAF1", "soft": "#F4F6FA",
    "paper": "#FFFFFF", "slate": "#334155", "slate_l": "#EEF2F7", "slate_m": "#94A3B8",
    "blue": "#1D6FD8", "blue_d": "#0B3F94", "blue_l": "#E6F0FD", "blue_m": "#9CC3F5",
    "amber": "#D99100", "amber_d": "#7A5200", "amber_l": "#FFF2CC", "amber_m": "#F3CD6B",
    "purple": "#7C3AED", "purple_d": "#4C1D95", "purple_l": "#F0E9FE", "purple_m": "#BFA2F7",
    "green": "#1E9E5A", "green_d": "#0E5C33", "green_l": "#E4F5EB", "green_m": "#8ED3AB",
    "orange": "#EE6A1B", "orange_d": "#8F3A06", "orange_l": "#FFEBDC", "orange_m": "#F7B68A",
    "red": "#D6333B", "red_d": "#8A171D", "red_l": "#FDE8E9", "red_m": "#F2A0A5",
}

# cores CPK suavizadas (apenas esferas de átomos; não têm significado semântico)
ATOM = {
    "H": ("#FFFFFF", "#6B7280", 0.62), "C": ("#4B5563", "#1F2937", 1.0), "O": ("#E5484D", "#9B1C22", 0.92),
    "N": ("#4C6FD6", "#2B3F8F", 0.95), "Cl": ("#3DB36B", "#1F7A45", 1.18), "S": ("#E8C33C", "#9A7B10", 1.15),
    "Na": ("#A78BFA", "#6D4BD0", 1.2), "Br": ("#B5503C", "#7A2F20", 1.3), "F": ("#8FD9A8", "#3E9A5E", 0.85),
    "Ca": ("#94A3B8", "#475569", 1.3), "Mg": ("#94A3B8", "#475569", 1.15),
}

FONT_STACK = "'Source Sans 3','Inter','DejaVu Sans',Arial,sans-serif"

_uid = count(1)


# --------------------------------------------------------------------------- métricas de fonte
class _Metrics:
    def __init__(self):
        self.fonts = {}

    def _load(self, weight, italic=False):
        key = (weight, italic)
        if key in self.fonts:
            return self.fonts[key]
        w = {400: 400, 500: 600, 600: 600, 700: 700, 800: 800, 900: 800}.get(weight, 400)
        style = "italic" if italic and w in (400, 600, 700) else "normal"
        path = os.path.join(FONT_DIR, f"source-sans-3-latin-{w}-{style}.woff2")
        f = TTFont(path)
        gpath = os.path.join(FONT_DIR, f"source-sans-3-greek-{w if w in (400,600,700) else 700}-normal.woff2")
        g = TTFont(gpath) if os.path.exists(gpath) else None
        entry = (f, f.getBestCmap(), f["hmtx"], g, g.getBestCmap() if g else {}, g["hmtx"] if g else None,
                 f["head"].unitsPerEm)
        self.fonts[key] = entry
        return entry

    def width(self, s, size, weight=400, italic=False):
        f, cm, hm, g, gcm, ghm, upm = self._load(weight, italic)
        total = 0.0
        for ch in s:
            o = ord(ch)
            if o in cm:
                total += hm[cm[o]][0]
            elif g is not None and o in gcm:
                total += ghm[gcm[o]][0]
            else:
                total += upm * 0.62
        return total * size / upm


METRICS = _Metrics()


def tw(s, size=11, weight=400, italic=False):
    """Largura estimada do texto (aceita marcação _x ^x para sub/sobrescrito)."""
    total = 0.0
    for txt, mode in _segments(s):
        sz = size * (0.72 if mode else 1.0)
        total += METRICS.width(txt, sz, weight, italic)
    return total


def _segments(s):
    """Divide 'H_2SO_4^{2-}' em [(texto, modo)] com modo 0 normal, 1 sub, 2 sup."""
    out = []
    i = 0
    buf = ""
    n = len(s)
    while i < n:
        c = s[i]
        if c in "_^" and i + 1 < n:
            if buf:
                out.append((buf, 0))
                buf = ""
            mode = 1 if c == "_" else 2
            j = i + 1
            if s[j] == "{":
                k = s.index("}", j)
                content = s[j + 1:k]
                i = k + 1
            else:
                m = re.match(r"\d+[+\-−]?|[+\-−]|[A-Za-z]", s[j:])
                content = m.group(0)
                i = j + len(content)
            out.append((content.replace("-", "−"), mode))
            continue
        buf += c
        i += 1
    if buf:
        out.append((buf, 0))
    return out


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v):
    """formata número para SVG."""
    if isinstance(v, (int,)):
        return str(v)
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def tspans(s, size):
    """Converte marcação química/matemática simples em <tspan>."""
    segs = _segments(s)
    if len(segs) == 1 and segs[0][1] == 0:
        return esc(segs[0][0])
    out = []
    cur = 0.0
    for txt, mode in segs:
        target = {0: 0.0, 1: size * 0.24, 2: -size * 0.40}[mode]
        attrs = ""
        if target != cur:
            attrs += f' dy="{n(target - cur)}"'
            cur = target
        if mode:
            attrs += f' font-size="{n(size * 0.72)}"'
        elif out:
            attrs += f' font-size="{n(size)}"'
        out.append(f"<tspan{attrs}>{esc(txt)}</tspan>")
    return "".join(out)


# --------------------------------------------------------------------------- classe SVG
class SVG:
    def __init__(self, w, h, title=None):
        self.w = w
        self.h = h
        self.parts = []
        self.uid = next(_uid)
        self.title = title
        self.defs = []

    # ---- primitivos
    def raw(self, s):
        self.parts.append(s)
        return self

    def _style(self, fill=None, stroke=None, sw=None, dash=None, opacity=None, cap=None, join=None, extra=""):
        a = []
        a.append(f'fill="{fill}"' if fill else 'fill="none"')
        if stroke:
            a.append(f'stroke="{stroke}"')
            a.append(f'stroke-width="{n(sw if sw is not None else 1)}"')
            if dash:
                a.append(f'stroke-dasharray="{dash}"')
            a.append(f'stroke-linecap="{cap or "round"}"')
            a.append(f'stroke-linejoin="{join or "round"}"')
        if opacity is not None:
            a.append(f'opacity="{n(opacity)}"')
        if extra:
            a.append(extra)
        return " ".join(a)

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1, rx=0, dash=None, opacity=None, extra=""):
        st = self._style(fill, stroke, sw, dash, opacity, extra=extra)
        return self.raw(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" {st}/>')

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1, dash=None, opacity=None, extra=""):
        st = self._style(fill, stroke, sw, dash, opacity, extra=extra)
        return self.raw(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" {st}/>')

    def ellipse(self, cx, cy, rx, ry, fill=None, stroke=None, sw=1, dash=None, opacity=None, rot=0, extra=""):
        st = self._style(fill, stroke, sw, dash, opacity, extra=extra)
        tr = f' transform="rotate({n(rot)} {n(cx)} {n(cy)})"' if rot else ""
        return self.raw(f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" {st}{tr}/>')

    def line(self, x1, y1, x2, y2, stroke="#1F2937", sw=1.2, dash=None, cap="round", opacity=None):
        st = self._style(None, stroke, sw, dash, opacity, cap=cap)
        return self.raw(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" {st}/>')

    def poly(self, pts, fill=None, stroke=None, sw=1, close=True, dash=None, opacity=None):
        d = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        st = self._style(fill, stroke, sw, dash, opacity)
        tag = "polygon" if close else "polyline"
        return self.raw(f'<{tag} points="{d}" {st}/>')

    def path(self, d, fill=None, stroke=None, sw=1, dash=None, opacity=None, cap=None, join=None, extra=""):
        st = self._style(fill, stroke, sw, dash, opacity, cap=cap, join=join, extra=extra)
        return self.raw(f'<path d="{d}" {st}/>')

    # ---- texto
    def text(self, x, y, s, size=11, anchor="start", weight=400, fill="#1F2937", italic=False, rot=None,
             halo=None, opacity=None, spacing=None, extra=""):
        inner = tspans(s, size)
        a = f'x="{n(x)}" y="{n(y)}" font-size="{n(size)}" text-anchor="{anchor}"'
        if weight != 400:
            a += f' font-weight="{weight}"'
        if italic:
            a += ' font-style="italic"'
        if spacing:
            a += f' letter-spacing="{spacing}"'
        if opacity is not None:
            a += f' opacity="{n(opacity)}"'
        if rot:
            a += f' transform="rotate({n(rot)} {n(x)} {n(y)})"'
        if extra:
            a += " " + extra
        if halo:
            self.raw(f'<text {a} fill="none" stroke="{halo}" stroke-width="3.2" stroke-linejoin="round">{inner}</text>')
        return self.raw(f'<text {a} fill="{fill}">{inner}</text>')

    def mtext(self, x, y, lines, size=11, lh=1.22, anchor="start", weight=400, fill="#1F2937", italic=False,
              halo=None):
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, size, anchor, weight, fill, italic, halo=halo)
        return self

    def tag(self, x, y, s, size=10.5, fill="#E6F0FD", stroke=None, color="#0B3F94", weight=700, padx=6, h=None,
            rx=None, anchor="middle", sw=1):
        """Rótulo em pílula; (x,y) = centro (anchor middle) ou início (start); y = centro vertical."""
        w = tw(s, size, weight) + 2 * padx
        h = h or size + 7
        rx = h / 2 if rx is None else rx
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        self.rect(x0, y - h / 2, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)
        self.text(x0 + w / 2, y + size * 0.34, s, size, "middle", weight, color)
        return w

    # ---- setas
    def head(self, x2, y2, ang, color, size=7, wide=0.42):
        """Triângulo de seta com ponta em (x2,y2) apontando na direção ang (rad)."""
        bx = x2 - size * math.cos(ang)
        by = y2 - size * math.sin(ang)
        px, py = -math.sin(ang) * size * wide, math.cos(ang) * size * wide
        return self.poly([(x2, y2), (bx + px, by + py), (bx - px, by - py)], fill=color)

    def arrow(self, x1, y1, x2, y2, color="#1F2937", sw=1.6, head=7, dash=None, both=False, wide=0.42):
        ang = math.atan2(y2 - y1, x2 - x1)
        sx, sy = x1, y1
        ex, ey = x2, y2
        if both:
            sx = x1 + head * 0.8 * math.cos(ang)
            sy = y1 + head * 0.8 * math.sin(ang)
        ex = x2 - head * 0.8 * math.cos(ang)
        ey = y2 - head * 0.8 * math.sin(ang)
        self.line(sx, sy, ex, ey, color, sw, dash)
        self.head(x2, y2, ang, color, head, wide)
        if both:
            self.head(x1, y1, ang + math.pi, color, head, wide)
        return self

    def carrow(self, x1, y1, cx, cy, x2, y2, color="#1F2937", sw=1.6, head=7, dash=None):
        """Seta curva (Bézier quadrática) com ponta em (x2,y2)."""
        ang = math.atan2(y2 - cy, x2 - cx)
        ex = x2 - head * 0.8 * math.cos(ang)
        ey = y2 - head * 0.8 * math.sin(ang)
        self.path(f"M{n(x1)} {n(y1)} Q{n(cx)} {n(cy)} {n(ex)} {n(ey)}", stroke=color, sw=sw, dash=dash)
        self.head(x2, y2, ang, color, head)
        return self

    def dipole(self, x1, y1, x2, y2, color="#0B3F94", sw=1.8, head=7, tick=3.6):
        """Vetor momento dipolar: cruz no polo positivo (x1,y1) e ponta no polo negativo (x2,y2)."""
        ang = math.atan2(y2 - y1, x2 - x1)
        self.arrow(x1, y1, x2, y2, color, sw, head)
        px, py = -math.sin(ang), math.cos(ang)
        self.line(x1 - px * tick, y1 - py * tick, x1 + px * tick, y1 + py * tick, color, sw)
        return self

    # ---- átomos / esferas
    def ball(self, cx, cy, r, el, size=None, label=None, lab_fill=None):
        fill, stroke, _ = ATOM.get(el, ("#CBD5E1", "#64748B", 1))
        self.circle(cx, cy, r, fill=fill, stroke=stroke, sw=1.3)
        self.ellipse(cx - r * 0.3, cy - r * 0.35, r * 0.36, r * 0.24, fill="#FFFFFF", opacity=0.38, rot=-30)
        size = size or r * 1.05
        lab = label if label is not None else el
        if lab:
            col = lab_fill or ("#1F2937" if el in ("H", "S", "F") else "#FFFFFF")
            self.text(cx, cy + size * 0.35, lab, size, "middle", 700, col)
        return self

    def lingrad(self, stops, x1=0, y1=0, x2=1, y2=0, units="objectBoundingBox"):
        gid = f"g{self.uid}_{len(self.defs)}"
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                         f'gradientUnits="{units}">{st}</linearGradient>')
        return f"url(#{gid})"

    def radgrad(self, stops, cx=0.35, cy=0.3, r=0.75):
        gid = f"r{self.uid}_{len(self.defs)}"
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        self.defs.append(f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{st}</radialGradient>')
        return f"url(#{gid})"

    def pat_hatch(self, color, bg=None, gap=5, sw=1.2):
        pid = f"h{self.uid}_{len(self.defs)}"
        b = f'<rect width="{gap}" height="{gap}" fill="{bg}"/>' if bg else ""
        self.defs.append(f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" '
                         f'patternTransform="rotate(45)">{b}<line x1="0" y1="0" x2="0" y2="{gap}" stroke="{color}" '
                         f'stroke-width="{sw}"/></pattern>')
        return f"url(#{pid})"

    # ---- saída
    def render(self, fit="natural", maxw=None, cls="", title=None):
        style = "display:block;"
        if fit == "width":
            style += "width:100%;height:auto;"
        else:
            style += "max-width:100%;height:auto;"
            if maxw:
                style += f"width:{maxw}px;"
        t = title or self.title
        ttl = f"<title>{esc(t)}</title>" if t else ""
        c = f' class="{cls}"' if cls else ""
        return (f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(self.w)} {n(self.h)}" '
                f'width="{n(self.w)}" height="{n(self.h)}" font-family="{FONT_STACK}" style="{style}" '
                f'role="img">{ttl}{"<defs>" + "".join(self.defs) + "</defs>" if self.defs else ""}{"".join(self.parts)}</svg>')

    def standalone(self):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n' +
                self.render().replace('style="display:block;max-width:100%;height:auto;"', ""))


# --------------------------------------------------------------------------- eixos de gráfico
class Axes:
    """Área de plotagem cartesiana dentro de um SVG."""

    def __init__(self, svg, x0, y0, w, h, xmin, xmax, ymin, ymax):
        self.s = svg
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def X(self, v):
        return self.x0 + (v - self.xmin) / (self.xmax - self.xmin) * self.w

    def Y(self, v):
        return self.y0 + self.h - (v - self.ymin) / (self.ymax - self.ymin) * self.h

    def frame(self, xticks=None, yticks=None, xfmt=str, yfmt=str, xlabel=None, ylabel=None, grid=True,
              size=10, arrows=True, xlab_dy=0, ylab_dx=0, tick_len=3.5):
        s = self.s
        if grid:
            for v in (yticks or []):
                s.line(self.x0, self.Y(v), self.x0 + self.w, self.Y(v), C["grid"], 0.9)
            for v in (xticks or []):
                s.line(self.X(v), self.y0, self.X(v), self.y0 + self.h, C["grid"], 0.9)
        # eixos
        if arrows:
            s.arrow(self.x0, self.y0 + self.h, self.x0 + self.w + 8, self.y0 + self.h, C["ink"], 1.4, 6)
            s.arrow(self.x0, self.y0 + self.h, self.x0, self.y0 - 8, C["ink"], 1.4, 6)
        else:
            s.line(self.x0, self.y0 + self.h, self.x0 + self.w, self.y0 + self.h, C["ink"], 1.4)
            s.line(self.x0, self.y0 + self.h, self.x0, self.y0, C["ink"], 1.4)
        for v in (xticks or []):
            s.line(self.X(v), self.y0 + self.h, self.X(v), self.y0 + self.h + tick_len, C["ink"], 1.1)
            s.text(self.X(v), self.y0 + self.h + tick_len + size + 1.5, xfmt(v), size, "middle", fill=C["muted"])
        for v in (yticks or []):
            s.line(self.x0 - tick_len, self.Y(v), self.x0, self.Y(v), C["ink"], 1.1)
            s.text(self.x0 - tick_len - 3, self.Y(v) + size * 0.34, yfmt(v), size, "end", fill=C["muted"])
        if xlabel:
            s.text(self.x0 + self.w / 2, self.y0 + self.h + tick_len + size * 2 + 6 + xlab_dy, xlabel, size + 0.5,
                   "middle", 600, C["ink"])
        if ylabel:
            lx = self.x0 - 30 + ylab_dx
            s.text(lx, self.y0 + self.h / 2, ylabel, size + 0.5, "middle", 600, C["ink"], rot=-90)
        return self

    def polyline(self, pts, color, sw=2.4, dash=None, fill=None, opacity=None):
        P = [(self.X(x), self.Y(y)) for x, y in pts]
        return self.s.poly(P, fill=fill, stroke=color, sw=sw, close=False, dash=dash, opacity=opacity)

    def curve_fn(self, fn, xa, xb, steps=120):
        return [(xa + (xb - xa) * i / steps, fn(xa + (xb - xa) * i / steps)) for i in range(steps + 1)]


def save_svg(svg_obj, name, outdir):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg_obj.standalone())
