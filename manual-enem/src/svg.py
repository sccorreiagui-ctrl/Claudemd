"""Biblioteca mínima de figuras vetoriais (SVG) do manual.

Todas as figuras usam a mesma paleta semântica:
  navy   -> títulos / estrutura          blue  -> explicação, esquemas
  green  -> fórmula, resultado            orange-> atenção, erro
  purple -> memorização, relação chave
Unidades: 1 unidade do viewBox ~ 1 px CSS (96 dpi), então fonte 10 ≈ 7,5 pt.
"""
import math
import itertools
from html import escape

_uid = itertools.count(1)

COL = dict(
    navy='#14284B', blue='#2B6CB0', lblue='#E3EEFA', mblue='#9CC3EA',
    green='#0F7B4F', lgreen='#D8F0E3', mgreen='#7CC4A0',
    orange='#D2600A', lorange='#FFE8D0', morange='#F0A868',
    purple='#6A3FB5', lpurple='#EADFFA', mpurple='#B79AE6',
    ink='#1B2430', grey='#6B7280', lgrey='#E8EAEE', mgrey='#B8BEC9',
    white='#FFFFFF', paper='#FCFBF7', red='#B42318',
)


def c(name):
    return COL.get(name, name)


def mk(s):
    """Mini-markup -> tspans.  *x* = variável em itálico, _x / _{xy} = subscrito,
    ^x / ^{xy} = sobrescrito.  Use \\* para um asterisco literal."""
    out = []
    i = 0
    ital = False
    buf = ''

    def flush():
        nonlocal buf
        if buf:
            t = escape(buf)
            out.append(f'<tspan class="mi">{t}</tspan>' if ital else t)
            buf = ''

    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s):
            buf += s[i + 1]
            i += 2
            continue
        if ch == '*':
            flush()
            ital = not ital
            i += 1
            continue
        if ch in '_^':
            flush()
            kind = 'sub' if ch == '_' else 'super'
            i += 1
            if i < len(s) and s[i] == '{':
                j = s.index('}', i)
                inner = s[i + 1:j]
                i = j + 1
            else:
                inner = s[i] if i < len(s) else ''
                i += 1
            t = escape(inner)
            cls = 'mi' if (inner.isalpha() and len(inner) == 1 and kind == 'sub' and False) else ''
            out.append(f'<tspan baseline-shift="{kind}" font-size="70%" class="{cls}">{t}</tspan>')
            continue
        buf += ch
        i += 1
    flush()
    return ''.join(out)


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.el = []
        self.uid = next(_uid)
        self.markers = {}
        self.extra_defs = []

    # ---------- infra
    def group(self, child, x, y):
        """Embute outra figura (ex.: dois gráficos lado a lado) numa translação (x, y)."""
        self.extra_defs.append(child._defs_inner())
        self.el.append(f'<g transform="translate({x},{y})">{"".join(child.el)}</g>')
        return self

    def raw(self, s):
        self.el.append(s)
        return self

    def _marker(self, color, kind='arrow'):
        key = (color, kind)
        if key not in self.markers:
            self.markers[key] = f'm{self.uid}_{len(self.markers)}'
        return self.markers[key]

    def _defs_inner(self):
        d = []
        for (color, kind), mid in self.markers.items():
            if kind == 'arrow':
                d.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                         f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="{color}"/></marker>')
        return ''.join(d)

    def _defs(self):
        inner = self._defs_inner() + ''.join(self.extra_defs)
        return f'<defs>{inner}</defs>' if inner else ''

    def svg(self, width=None, cls=''):
        wattr = f' style="width:{width}"' if width else f' width="{self.w}"'
        return (f'<svg class="fig {cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}"{wattr}>'
                f'{self._defs()}{"".join(self.el)}</svg>')

    # ---------- primitivas
    def line(self, x1, y1, x2, y2, col='ink', w=1.2, dash=None, arrow=False, arrow0=False, op=None):
        col = c(col)
        a = ''
        if arrow:
            a += f' marker-end="url(#{self._marker(col)})"'
        if arrow0:
            a += f' marker-start="url(#{self._marker(col)})"'
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.el.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" '
                       f'stroke-width="{w}" stroke-linecap="round"{d}{a}{o}/>')
        return self

    def rect(self, x, y, w, h, fill='none', stroke=None, sw=1.2, rx=0, dash=None, op=None):
        s = f' stroke="{c(stroke)}" stroke-width="{sw}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.el.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{c(fill)}"{s}{d}{o}/>')
        return self

    def circ(self, cx, cy, r, fill='none', stroke=None, sw=1.2, dash=None, op=None):
        s = f' stroke="{c(stroke)}" stroke-width="{sw}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.el.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{c(fill)}"{s}{d}{o}/>')
        return self

    def ell(self, cx, cy, rx, ry, fill='none', stroke=None, sw=1.2, dash=None, op=None):
        s = f' stroke="{c(stroke)}" stroke-width="{sw}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.el.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{c(fill)}"{s}{d}{o}/>')
        return self

    def poly(self, pts, fill='none', stroke=None, sw=1.2, close=True, dash=None, op=None, join='round'):
        p = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        s = f' stroke="{c(stroke)}" stroke-width="{sw}" stroke-linejoin="{join}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.el.append(f'<{tag} points="{p}" fill="{c(fill)}"{s}{d}{o}/>')
        return self

    def path(self, d, fill='none', stroke=None, sw=1.2, dash=None, op=None, arrow=False):
        s = f' stroke="{c(stroke)}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ''
        dd = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        a = f' marker-end="url(#{self._marker(c(stroke))})"' if arrow and stroke else ''
        self.el.append(f'<path d="{d}" fill="{c(fill)}"{s}{dd}{o}{a}/>')
        return self

    def text(self, x, y, s, size=10.5, col='ink', anchor='middle', bold=False, rot=0, halo=False, base='alphabetic',
             style=''):
        fw = ' font-weight="700"' if bold else ''
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ''
        h = ' class="halo"' if halo else ''
        bl = '' if base == 'alphabetic' else f' dominant-baseline="{base}"'
        st = f' style="{style}"' if style else ''
        self.el.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{c(col)}" text-anchor="{anchor}"{fw}{tr}{h}{bl}{st}>{mk(s)}</text>')
        return self

    def dot(self, x, y, r=3.2, col='ink'):
        return self.circ(x, y, r, fill=col)

    def arc(self, cx, cy, r, a0, a1, col='orange', sw=1.6, fill='none', op=None, arrow=False):
        """Arco de a0 a a1 (graus, sentido anti-horário visto na tela, 0° = direita; y da tela invertido)."""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        large = 1 if (a1 - a0) % 360 > 180 else 0
        d = f'M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 0 {x1:.2f},{y1:.2f}'
        return self.path(d, fill=fill, stroke=col, sw=sw, op=op, arrow=arrow)

    def sector(self, cx, cy, r, a0, a1, fill='lblue', stroke=None, sw=1.2, op=None):
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        large = 1 if (a1 - a0) % 360 > 180 else 0
        d = f'M{cx:.2f},{cy:.2f} L{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 0 {x1:.2f},{y1:.2f} Z'
        return self.path(d, fill=fill, stroke=stroke, sw=sw, op=op)

    def rightangle(self, x, y, d1, d2, s=8, col='ink'):
        """Marca de ângulo reto no vértice (x,y); d1 e d2 são vetores unitários (dx,dy) na tela."""
        p1 = (x + d1[0] * s, y + d1[1] * s)
        p2 = (x + d1[0] * s + d2[0] * s, y + d1[1] * s + d2[1] * s)
        p3 = (x + d2[0] * s, y + d2[1] * s)
        return self.poly([p1, p2, p3], stroke=col, sw=1, close=False)

    def label(self, x, y, s, **kw):
        kw.setdefault('halo', True)
        return self.text(x, y, s, **kw)

    def pill(self, x, y, s, fill='lblue', col='navy', size=10, padx=6, h=15, stroke=None, bold=True):
        w = max(14, len(s.replace('*', '').replace('_', '').replace('^', '').replace('{', '').replace('}', '')) * size * 0.58 + 2 * padx)
        self.rect(x - w / 2, y - h / 2, w, h, fill=fill, stroke=stroke, rx=h / 2)
        self.text(x, y + size * 0.35, s, size=size, col=col, bold=bold)
        return self

    def brace_h(self, x1, x2, y, up=True, col='grey', depth=6):
        """Chave horizontal simples (colchete) para indicar medidas."""
        d = depth if not up else -depth
        self.path(f'M{x1},{y} L{x1},{y + d} L{x2},{y + d} L{x2},{y}', stroke=col, sw=1.1)
        return self

    def dim(self, x1, y1, x2, y2, s, col='grey', off=0, size=10, text_dy=-4, anchor='middle'):
        """Cota com setas nas duas pontas e rótulo central."""
        self.line(x1, y1, x2, y2, col=col, w=1.1, arrow=True, arrow0=True)
        self.label((x1 + x2) / 2, (y1 + y2) / 2 + text_dy, s, size=size, col=col, anchor=anchor)
        return self


class Plot(Fig):
    """Plano cartesiano com mapeamento matemático -> tela."""

    def __init__(self, w, h, xmin, xmax, ymin, ymax, l=22, r=10, t=10, b=18):
        super().__init__(w, h)
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.l, self.r, self.t, self.b = l, r, t, b

    def X(self, x):
        return self.l + (x - self.xmin) / (self.xmax - self.xmin) * (self.w - self.l - self.r)

    def Y(self, y):
        return self.h - self.b - (y - self.ymin) / (self.ymax - self.ymin) * (self.h - self.t - self.b)

    def grid(self, dx=1, dy=1, col='lgrey'):
        x = math.ceil(self.xmin / dx) * dx
        while x <= self.xmax + 1e-9:
            self.line(self.X(x), self.Y(self.ymin), self.X(x), self.Y(self.ymax), col=col, w=0.7)
            x += dx
        y = math.ceil(self.ymin / dy) * dy
        while y <= self.ymax + 1e-9:
            self.line(self.X(self.xmin), self.Y(y), self.X(self.xmax), self.Y(y), col=col, w=0.7)
            y += dy
        return self

    def axes(self, xlab='x', ylab='y', xticks=(), yticks=(), tick=True, origin=True, size=9.5, xfmt=None, yfmt=None):
        x0 = self.X(0) if self.xmin <= 0 <= self.xmax else self.X(self.xmin)
        y0 = self.Y(0) if self.ymin <= 0 <= self.ymax else self.Y(self.ymin)
        self.line(self.X(self.xmin), y0, self.X(self.xmax) + 4, y0, col='ink', w=1.3, arrow=True)
        self.line(x0, self.Y(self.ymin), x0, self.Y(self.ymax) - 4, col='ink', w=1.3, arrow=True)
        self.text(self.X(self.xmax) + 2, y0 + 12, xlab, size=size + 1, anchor='end', col='ink')
        self.text(x0 + 6, self.Y(self.ymax) + 2, ylab, size=size + 1, anchor='start', col='ink')
        for tx in xticks:
            if tx == 0 and origin is False:
                continue
            xs = self.X(tx)
            self.line(xs, y0 - 3, xs, y0 + 3, col='ink', w=1)
            lab = xfmt(tx) if xfmt else fmt(tx)
            self.text(xs, y0 + 13, lab, size=size, col='grey')
        for ty in yticks:
            if ty == 0:
                continue
            ys = self.Y(ty)
            self.line(x0 - 3, ys, x0 + 3, ys, col='ink', w=1)
            lab = yfmt(ty) if yfmt else fmt(ty)
            self.text(x0 - 6, ys + 3.5, lab, size=size, col='grey', anchor='end')
        return self

    def curve(self, f, x0, x1, n=160, col='blue', w=2.2, ylim=None, dash=None):
        pts = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
            if ylim and not (ylim[0] <= y <= ylim[1]):
                if pts:
                    self.poly(pts, stroke=col, sw=w, close=False, dash=dash)
                    pts = []
                continue
            pts.append((self.X(x), self.Y(y)))
        if pts:
            self.poly(pts, stroke=col, sw=w, close=False, dash=dash)
        return self

    def pt(self, x, y, col='ink', r=3.4):
        return self.dot(self.X(x), self.Y(y), r, col)

    def ptlabel(self, x, y, s, dx=6, dy=-6, anchor='start', **kw):
        return self.label(self.X(x) + dx, self.Y(y) + dy, s, anchor=anchor, **kw)

    def seg(self, x1, y1, x2, y2, **kw):
        return self.line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), **kw)

    def fill_between(self, f, g, x0, x1, n=80, fill='lgreen', op=0.7):
        top = [(self.X(x0 + (x1 - x0) * i / n), self.Y(f(x0 + (x1 - x0) * i / n))) for i in range(n + 1)]
        bot = [(self.X(x0 + (x1 - x0) * i / n), self.Y(g(x0 + (x1 - x0) * i / n))) for i in range(n, -1, -1)]
        return self.poly(top + bot, fill=fill, op=op)


def fmt(v):
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = ('%g' % v).replace('.', ',')
    return s.replace('-', '−')


def polygon_pts(n, cx, cy, r, rot=90):
    """Vértices de um polígono regular (rot = ângulo do primeiro vértice, graus; y para cima)."""
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)),
             cy - r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]


# ---------- sólidos 3D (projeção oblíqua simples) ----------
def cylinder(f, cx, ytop, rx, ry, h, fill='lblue', stroke='navy', sw=1.4):
    """Cilindro reto: elipse superior em (cx,ytop), altura h (pixels)."""
    f.path(f'M{cx - rx},{ytop} L{cx - rx},{ytop + h} A{rx},{ry} 0 0 0 {cx + rx},{ytop + h} L{cx + rx},{ytop} Z',
           fill=fill, stroke=stroke, sw=sw)
    f.ell(cx, ytop, rx, ry, fill='white', stroke=stroke, sw=sw)
    f.path(f'M{cx - rx},{ytop + h} A{rx},{ry} 0 0 1 {cx + rx},{ytop + h}', stroke=stroke, sw=sw, dash='3 3', op=0.8)


def cone(f, cx, ytop, rx, ry, h, fill='lblue', stroke='navy', sw=1.4):
    """Cone reto: vértice em (cx,ytop); base com centro em (cx,ytop+h)."""
    yb = ytop + h
    f.path(f'M{cx},{ytop} L{cx - rx},{yb} A{rx},{ry} 0 0 0 {cx + rx},{yb} Z', fill=fill, stroke=stroke, sw=sw)
    f.path(f'M{cx - rx},{yb} A{rx},{ry} 0 0 1 {cx + rx},{yb}', stroke=stroke, sw=sw, dash='3 3', op=0.8)


def box3d(f, x, y, w, h, dx, dy, fill='lblue', stroke='navy', sw=1.4, hidden=True):
    """Paralelepípedo em projeção oblíqua: face frontal (x,y,w,h), profundidade (dx,-dy)."""
    front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    top = [(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w, y)]
    side = [(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)]
    f.poly(top, fill=fill, stroke=stroke, sw=sw, op=1)
    f.poly(side, fill=fill, stroke=stroke, sw=sw)
    f.poly(front, fill=fill, stroke=stroke, sw=sw)
    f.poly(top, fill='white', op=0.55)
    f.poly(side, fill=stroke, op=0.12)
    if hidden:
        f.line(x, y + h, x + dx, y + h - dy, col=stroke, w=1, dash='3 3', op=0.7)
        f.line(x + dx, y - dy, x + dx, y + h - dy, col=stroke, w=1, dash='3 3', op=0.7)
        f.line(x + dx, y + h - dy, x + w + dx, y + h - dy, col=stroke, w=1, dash='3 3', op=0.7)
    return f
