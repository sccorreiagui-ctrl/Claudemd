"""Mini-biblioteca para gerar figuras vetoriais (SVG) matematicamente precisas.

Unidade: 1 unidade = 0,25 mm  (largura física = W*0.25 mm). Fonte 10.5u ~= 7.4 pt.

Mini-marcação de texto:
  _x  _{xy}   subscrito          ^2  ^{-1}  sobrescrito
  \\bar{z}     barra de conjugado
  \\r{cos}     texto reto (não itálico)
  «blue:txt»  texto colorido (nomes da paleta)
  prefixo ~   rótulo em sans-serif (português)
"""
import math, os, re

PAL = dict(
    blue='#1f5fbf', blue_l='#dbe8fa', purple='#7a3fc2', purple_l='#eadcf8',
    green='#167a44', green_l='#d9f0e2', orange='#d4690a', orange_l='#fbe5cb',
    red='#c62828', red_l='#fadcdc', gray='#5f6b7a', gray_l='#e6e9ee', gray_m='#aab3c0',
    ink='#1a2233', white='#ffffff', cyan='#0b6fa4', cyan_l='#dcecf6', violet='#5b2a9e', violet_l='#e7dcf6',
    yellow='#e0a800', yellow_l='#fbf0c9',
)
U = 0.25  # mm por unidade


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _match(s, i, open_c, close_c):
    """índice do fecho correspondente a s[i]==open_c"""
    d = 0
    for j in range(i, len(s)):
        if s[j] == open_c: d += 1
        elif s[j] == close_c:
            d -= 1
            if d == 0: return j
    raise ValueError('grupo não fechado: ' + s)


_GREEK = set('αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ')


def _cls(ch):
    if ch.isalpha() and (ch.isascii() or ch in _GREEK) and ch not in 'ΓΔΘΛΞΠΣΦΨΩ':
        return 'i'
    return 'm'


def parse(s, st=None):
    """-> lista de runs (texto, classe, escala, shift_em, overline, color)"""
    st = st or dict(scale=1.0, shift=0.0, over=False, color=None, upright=False, bb=False)
    runs, buf, i = [], '', 0

    def flush():
        nonlocal buf
        for ch in buf:
            c = 'a' if st.get('bb') else ('m' if st['upright'] else _cls(ch))
            if runs and runs[-1][1:] == (c, st['scale'], st['shift'], st['over'], st['color']):
                runs[-1] = (runs[-1][0] + ch,) + runs[-1][1:]
            else:
                runs.append((ch, c, st['scale'], st['shift'], st['over'], st['color']))
        buf = ''

    while i < len(s):
        ch = s[i]
        if ch in '_^':
            flush()
            if s[i + 1] == '{':
                j = _match(s, i + 1, '{', '}'); inner = s[i + 2:j]; i = j + 1
            else:
                inner = s[i + 1]; i += 2
            ns = dict(st, scale=st['scale'] * 0.72, shift=st['shift'] + (0.42 if ch == '^' else -0.2))
            runs += parse(inner, ns)
        elif s.startswith('\\bar{', i):
            flush(); j = _match(s, i + 4, '{', '}')
            runs += parse(s[i + 5:j], dict(st, over=True)); i = j + 1
        elif s.startswith('\\bb{', i):
            flush(); j = _match(s, i + 3, '{', '}')
            runs += parse(s[i + 4:j], dict(st, bb=True)); i = j + 1
        elif s.startswith('\\r{', i):
            flush(); j = _match(s, i + 2, '{', '}')
            runs += parse(s[i + 3:j], dict(st, upright=True)); i = j + 1
        elif ch == '«':
            flush(); j = _match(s, i, '«', '»'); inner = s[i + 1:j]; name, txt = inner.split(':', 1)
            runs += parse(txt, dict(st, color=PAL.get(name, name))); i = j + 1
        else:
            buf += ch; i += 1
    flush()
    return runs


_FN = re.compile(r'(?<![A-Za-z\\])(cos|sen|tg|cis|Re|Im)(?![A-Za-z])')


def text_inner(s, size):
    """tspans para a string s (sem o elemento <text>)."""
    s = _FN.sub(lambda m: '\\r{' + m.group(1) + '}', s)
    out, cur = [], 0.0
    for (t, c, sc, sh, over, col) in parse(s):
        dy = (-(sh) * size - cur)  # y SVG cresce para baixo: sh>0 => subir
        cur = -(sh) * size
        a = f' dy="{dy:.2f}"' if abs(dy) > 1e-6 else ''
        a += f' font-size="{size * sc:.2f}"' if sc != 1.0 else ''
        a += f' fill="{col}"' if col else ''
        a += ' text-decoration="overline"' if over else ''
        out.append(f'<tspan class="{c}"{a}>{esc(t)}</tspan>')
    if abs(cur) > 1e-6:
        out.append(f'<tspan dy="{-cur:.2f}"> </tspan>')
    return ''.join(out)


class Fig:
    def __init__(self, w, h):
        self.w, self.h, self.els = w, h, []

    def add(self, s): self.els.append(s); return self

    # ----- primitivas -----
    def line(self, x1, y1, x2, y2, stroke='ink', w=1.2, dash=None, cap='round', op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' stroke-opacity="{op}"' if op else ''
        return self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{PAL.get(stroke, stroke)}" stroke-width="{w}"{d}{o} stroke-linecap="{cap}"/>')

    def arrow(self, x1, y1, x2, y2, stroke='ink', w=1.4, head=7, dash=None, both=False):
        ang = math.atan2(y2 - y1, x2 - x1)
        col = PAL.get(stroke, stroke)
        # encurta a linha para a ponta não ser sobreposta
        lx2, ly2 = x2 - math.cos(ang) * head * 0.7, y2 - math.sin(ang) * head * 0.7
        lx1, ly1 = x1, y1
        if both:
            lx1, ly1 = x1 + math.cos(ang) * head * 0.7, y1 + math.sin(ang) * head * 0.7
        self.line(lx1, ly1, lx2, ly2, stroke, w, dash)
        self._head(x2, y2, ang, head, col)
        if both: self._head(x1, y1, ang + math.pi, head, col)
        return self

    def _head(self, x, y, ang, head, col):
        a1, a2 = ang + math.radians(155), ang - math.radians(155)
        p = [(x, y), (x + head * math.cos(a1), y + head * math.sin(a1)), (x + head * 0.55 * math.cos(ang + math.pi), y + head * 0.55 * math.sin(ang + math.pi)), (x + head * math.cos(a2), y + head * math.sin(a2))]
        self.add(f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in p)}" fill="{col}"/>')

    def circle(self, cx, cy, r, fill='none', stroke='ink', w=1.2, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op else ''
        return self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{PAL.get(fill, fill)}" stroke="{PAL.get(stroke, stroke)}" stroke-width="{w}"{d}{o}/>')

    def dot(self, x, y, r=2.6, fill='ink', stroke='white', w=0.8):
        return self.circle(x, y, r, fill, stroke, w)

    def rect(self, x, y, w, h, fill='none', stroke='ink', sw=1.0, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op else ''
        return self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{PAL.get(fill, fill)}" stroke="{PAL.get(stroke, stroke)}" stroke-width="{sw}"{d}{o}/>')

    def poly(self, pts, fill='none', stroke='ink', w=1.2, op=None, dash=None, close=True):
        tag = 'polygon' if close else 'polyline'
        o = f' fill-opacity="{op}"' if op else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return self.add(f'<{tag} points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="{PAL.get(fill, fill)}" stroke="{PAL.get(stroke, stroke)}" stroke-width="{w}" stroke-linejoin="round"{o}{d}/>')

    def path(self, d, fill='none', stroke='ink', w=1.2, dash=None, op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op else ''
        return self.add(f'<path d="{d}" fill="{PAL.get(fill, fill)}" stroke="{PAL.get(stroke, stroke)}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{da}{o}/>')

    def arc(self, cx, cy, r, a0, a1, stroke='orange', w=1.4, arrow=False, head=5.5, dash=None):
        """arco anti-horário de a0 a a1 (graus, orientação matemática) com centro em px (cx,cy)."""
        def pt(a): return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))
        (x0, y0), (x1, y1) = pt(a0), pt(a1)
        large = 1 if ((a1 - a0) % 360) > 180 else 0
        self.path(f'M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {large} 0 {x1:.2f},{y1:.2f}', stroke=stroke, w=w, dash=dash)
        if arrow:
            ang = math.radians(a1)
            tx, ty = -math.sin(ang), -math.cos(ang)  # tangente anti-horária em coords de tela
            self._head(x1, y1, math.atan2(ty, tx), head, PAL.get(stroke, stroke))
        return self

    def text(self, x, y, s, size=10.5, fill='ink', anchor='middle', weight=None, rot=None, op=None, bg=None):
        sans = s.startswith('~')
        if sans: s = s[1:]
        col = PAL.get(fill, fill)
        wt = f' font-weight="{weight}"' if weight else ''
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ''
        o = f' fill-opacity="{op}"' if op else ''
        inner = f'<tspan>{esc(s)}</tspan>' if sans else text_inner(s, size)
        if bg:  # halo branco para legibilidade
            self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{PAL.get(bg, bg)}" stroke="{PAL.get(bg, bg)}" stroke-width="3.2" stroke-linejoin="round" text-anchor="{anchor}"{wt}{tr}>{inner}</text>')
        return self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{col}" text-anchor="{anchor}"{wt}{tr}{o}>{inner}</text>')

    def label_box(self, x, y, w, h, s, fill='white', stroke='gray', size=10, tcol='ink', rx=3, weight=None, sw=1.0):
        self.rect(x, y, w, h, fill, stroke, sw, rx)
        return self.text(x + w / 2, y + h / 2 + size * 0.34, s, size, tcol, weight=weight)

    def svg(self):
        body = '\n'.join(self.els)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w * U:.2f}mm" height="{self.h * U:.2f}mm">\n{body}\n</svg>\n')

    def save(self, name, outdir):
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(self.svg())


class Plane:
    """Plano cartesiano/complexo: x,y matemáticos -> px da figura (y invertido), escala igual nos dois eixos."""

    def __init__(self, fig, ox, oy, s):
        self.f, self.ox, self.oy, self.s = fig, ox, oy, s

    def P(self, x, y): return self.ox + x * self.s, self.oy - y * self.s

    def axes(self, xmin, xmax, ymin, ymax, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=8, origin=True, xcol='blue', ycol='purple', lab_size=9.5):
        f = self.f
        if grid:
            k = math.ceil(xmin / step) * step
            while k <= xmax + 1e-9:
                if abs(k) > 1e-9: f.line(*self.P(k, ymin), *self.P(k, ymax), stroke='#e3e7ed', w=0.7)
                k += step
            k = math.ceil(ymin / step) * step
            while k <= ymax + 1e-9:
                if abs(k) > 1e-9: f.line(*self.P(xmin, k), *self.P(xmax, k), stroke='#e3e7ed', w=0.7)
                k += step
        f.arrow(*self.P(xmin, 0), *self.P(xmax, 0), stroke=xcol, w=1.5, head=7)
        f.arrow(*self.P(0, ymin), *self.P(0, ymax), stroke=ycol, w=1.5, head=7)
        if ticks:
            k = math.ceil(xmin / step) * step
            while k <= xmax - 0.4 + 1e-9:
                if abs(k) > 1e-9:
                    x, y = self.P(k, 0)
                    f.line(x, y - 2, x, y + 2, stroke='gray', w=0.9)
                    f.text(x, y + 10, fmt(k), tick_size, 'gray')
                k += step
            k = math.ceil(ymin / step) * step
            while k <= ymax - 0.4 + 1e-9:
                if abs(k) > 1e-9:
                    x, y = self.P(0, k)
                    f.line(x - 2, y, x + 2, y, stroke='gray', w=0.9)
                    f.text(x - 5, y + 3, fmt(k) + ('' if False else ''), tick_size, 'gray', anchor='end')
                k += step
        if origin:
            x, y = self.P(0, 0)
            f.text(x - 5, y + 10, 'O', tick_size, 'gray', anchor='end')
        if xlab:
            x, y = self.P(xmax, 0); f.text(x - 1, y - 6, xlab, lab_size, xcol, anchor='end', weight=700)
        if ylab:
            x, y = self.P(0, ymax); f.text(x + 6, y + 6, ylab, lab_size, ycol, anchor='start', weight=700)

    def vec(self, x, y, stroke='ink', w=1.7, head=7, x0=0, y0=0, dash=None):
        a, b = self.P(x0, y0); c, d = self.P(x, y)
        self.f.arrow(a, b, c, d, stroke, w, head, dash)

    def pt(self, x, y, fill='ink', r=2.8):
        self.f.dot(*self.P(x, y), r, fill)

    def line(self, x1, y1, x2, y2, stroke='gray', w=1.0, dash=None):
        self.f.line(*self.P(x1, y1), *self.P(x2, y2), stroke=stroke, w=w, dash=dash)

    def arc(self, r, a0, a1, stroke='orange', w=1.5, arrow=False, cx=0, cy=0, head=6.5):
        px, py = self.P(cx, cy)
        self.f.arc(px, py, r * self.s, a0, a1, stroke, w, arrow, head)

    def circle(self, r, cx=0, cy=0, stroke='gray', w=1.2, dash=None, fill='none', op=None):
        px, py = self.P(cx, cy)
        self.f.circle(px, py, r * self.s, fill, stroke, w, dash, op)

    def text(self, x, y, s, size=10, fill='ink', anchor='middle', dx=0, dy=0, weight=None, bg=None):
        px, py = self.P(x, y)
        self.f.text(px + dx, py + dy, s, size, fill, anchor, weight, bg=bg)


def fmt(k):
    if abs(k - round(k)) < 1e-9: return str(int(round(k))).replace('-', '−')
    return f'{k:g}'.replace('-', '−')
