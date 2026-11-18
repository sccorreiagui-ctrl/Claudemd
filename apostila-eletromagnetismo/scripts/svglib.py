"""svglib — mini-biblioteca para diagramas científicos em SVG (padrão CTG).

Convenções de cor (semântica fixa em todo o livro):
  blue   campo magnético externo / referência      purple  campo induzido / indução
  orange corrente elétrica convencional            green   força magnética / verificado
  cyan   velocidade / movimento de partículas      red     erros, polaridades, advertências
  gray   estruturas, eixos, auxiliares
Todas as setas são desenhadas explicitamente (polígono), sem <marker>, para renderização idêntica em PDF.
Unidades do viewBox = px CSS (96 dpi): 1 px = 0,2646 mm.
"""
import math
import os
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(HERE, '_fonts')
OUTDIR = os.path.join(os.path.dirname(HERE), 'build', 'figures')

STROKE = dict(blue='#2563C9', purple='#7E3FC4', orange='#E8710A', green='#1B8F4B', cyan='#0E9FBC', red='#C8302F',
              gray='#5C6573', navy='#0E2A47', ink='#1A2230', light='#C9D1DB', pale='#EEF1F5', white='#FFFFFF',
              mid='#98A2B0', faint='#DDE3EA')
TEXT = dict(blue='#1B4DA6', purple='#672DAE', orange='#A94E00', green='#14703A', cyan='#0A748A', red='#A82221',
            gray='#5C6573', navy='#0E2A47', ink='#1A2230', white='#FFFFFF')
FILL = dict(blue='#E8F0FD', purple='#F1EAFB', orange='#FFF0DF', green='#E5F5EB', cyan='#E0F5F9', red='#FCEBEA',
            gray='#EFF1F4', navy='#E9EFF7', white='#FFFFFF', paper='#FBFCFD')

SANS = "'Source Sans 3','KaTeX_Main',Arial,sans-serif"
SERIF = "'Source Serif 4','KaTeX_Main',Georgia,serif"


def col(c, table=STROKE):
    return table.get(c, c) if isinstance(c, str) else c


def f2(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.') if abs(v) >= 0.005 else '0'


def num(v, nd=1):
    """formata número com vírgula decimal (pt-BR)."""
    s = f'{v:.{nd}f}'
    return s.replace('.', ',').replace('-', '−')


# ----------------------------------------------------------------------------------- medidas de texto
_fcache = {}


def _font(fam, sub, weight, italic, size):
    st = 'italic' if italic else 'normal'
    name = f"{'source-serif-4' if fam == 'serif' else 'source-sans-3'}-{sub}-{weight}-{st}.ttf"
    key = (name, round(size * 10))
    if key not in _fcache:
        path = os.path.join(FONTDIR, name)
        if not os.path.exists(path):  # peso inexistente -> mais próximo
            alt = {'serif': {400: 400, 600: 700, 700: 700, 800: 700}, 'sans': {400: 400, 600: 600, 700: 700, 800: 800}}[fam]
            name = f"{'source-serif-4' if fam == 'serif' else 'source-sans-3'}-{sub}-{alt[weight]}-{st if fam == 'serif' else 'normal'}.ttf"
            path = os.path.join(FONTDIR, name)
        _fcache[key] = ImageFont.truetype(path, size=size * 10)
    return _fcache[key]


def text_width(s, size, fam='sans', weight=400, italic=False):
    tot = 0.0
    run, sub = '', 'latin'
    for ch in s + '\0':
        cs = 'greek' if 0x370 <= ord(ch) <= 0x3FF else 'latin'
        if ch == '\0' or cs != sub:
            if run:
                try:
                    tot += _font(fam, sub, weight, italic, size).getlength(run) / 10
                except Exception:
                    tot += len(run) * size * 0.55
            run, sub = '', cs
        if ch != '\0':
            run += ch
    return tot


def parse_rich(s):
    """*...* itálico serifado (variável); _{...} subscrito; ^{...} sobrescrito."""
    out, buf, i, ital = [], '', 0, False
    def flush():
        nonlocal buf
        if buf:
            out.append(('i' if ital else 'n', buf)); buf = ''
    while i < len(s):
        c = s[i]
        if c == '*':
            flush(); ital = not ital; i += 1
        elif c in '_^' and i + 1 < len(s) and s[i + 1] == '{':
            j = s.index('}', i + 2); flush()
            out.append((('sub' if c == '_' else 'sup') + ('i' if ital else ''), s[i + 2:j])); i = j + 1
        else:
            buf += c; i += 1
    flush()
    return out


def rich_width(s, size, weight=400):
    w = 0
    for kind, t in parse_rich(s):
        if kind == 'n': w += text_width(t, size, 'sans', weight)
        elif kind == 'i': w += text_width(t, size, 'serif', 400, True)
        elif kind.startswith('sub') or kind.startswith('sup'):
            w += text_width(t, size * 0.72, 'serif' if kind.endswith('i') else 'sans', 400 if kind.endswith('i') else weight, kind.endswith('i'))
    return w


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ----------------------------------------------------------------------------------- câmera 3D
class Cam:
    """Projeção ortográfica. Mundo: x direita, y cima, z para o observador (destro)."""
    def __init__(self, az=28, el=18, scale=1.0, ox=0, oy=0):
        self.az, self.el = math.radians(az), math.radians(el)
        self.s, self.ox, self.oy = scale, ox, oy

    def rot(self, p):
        x, y, z = p
        x1 = x * math.cos(self.az) + z * math.sin(self.az)
        z1 = -x * math.sin(self.az) + z * math.cos(self.az)
        y2 = y * math.cos(self.el) - z1 * math.sin(self.el)
        z2 = y * math.sin(self.el) + z1 * math.cos(self.el)
        return x1, y2, z2

    def P(self, p):
        x1, y2, _ = self.rot(p)
        return (self.ox + self.s * x1, self.oy - self.s * y2)

    def depth(self, p):
        return self.rot(p)[2]


class Obl:
    """Projeção oblíqua (cavalier/cabinet): x horizontal exato, y vertical exato, z (para o leitor) desenhado para baixo e à esquerda."""
    def __init__(self, k=0.7, phi=24, scale=1.0, ox=0, oy=0):
        self.k, self.phi, self.s, self.ox, self.oy = k, math.radians(phi), scale, ox, oy

    def P(self, p):
        x, y, z = p
        return (self.ox + self.s * (x - self.k * z * math.cos(self.phi)), self.oy - self.s * (y - self.k * z * math.sin(self.phi)))

    def depth(self, p):
        return p[2]


# ----------------------------------------------------------------------------------- SVG
class Svg:
    def __init__(self, w, h, name=None):
        self.w, self.h, self.name = w, h, name
        self.parts, self.boxes = [], []

    # --- básicos
    def add(self, s):
        self.parts.append(s)

    def _stroke(self, color, w, dash=None, cap='round', join='round', opacity=None):
        s = f'stroke="{col(color)}" stroke-width="{f2(w)}" stroke-linecap="{cap}" stroke-linejoin="{join}"'
        if dash: s += f' stroke-dasharray="{dash}"'
        if opacity is not None: s += f' stroke-opacity="{opacity}"'
        return s

    def line(self, p, q, color='gray', w=1.2, dash=None, cap='round', opacity=None):
        self.add(f'<line x1="{f2(p[0])}" y1="{f2(p[1])}" x2="{f2(q[0])}" y2="{f2(q[1])}" fill="none" {self._stroke(color, w, dash, cap, opacity=opacity)}/>')

    def polyline(self, pts, color='gray', w=1.2, dash=None, fill='none', close=False, opacity=None, join='round'):
        d = 'M' + ' L'.join(f'{f2(x)} {f2(y)}' for x, y in pts) + (' Z' if close else '')
        f = f'fill="{col(fill, FILL)}"' if fill != 'none' else 'fill="none"'
        self.add(f'<path d="{d}" {f} {self._stroke(color, w, dash, join=join, opacity=opacity)}/>')

    def polygon(self, pts, fill='gray', stroke=None, w=1.0, opacity=None, dash=None):
        # fill: nome em FILL (tom claro), nome em STROKE (cor cheia) ou hex
        d = 'M' + ' L'.join(f'{f2(x)} {f2(y)}' for x, y in pts) + ' Z'
        st = self._stroke(stroke, w, dash) if stroke else 'stroke="none"'
        op = f' fill-opacity="{opacity}"' if opacity is not None else ''
        self.add(f'<path d="{d}" fill="{col(fill, FILL) if fill in FILL else col(fill)}"{op} {st}/>')

    def path(self, d, fill='none', stroke='gray', w=1.2, dash=None, opacity=None, fill_opacity=None):
        fo = f' fill-opacity="{fill_opacity}"' if fill_opacity is not None else ''
        fc = 'none' if fill == 'none' else (col(fill, FILL) if fill in FILL else col(fill))
        st = self._stroke(stroke, w, dash, opacity=opacity) if stroke else 'stroke="none"'
        self.add(f'<path d="{d}" fill="{fc}"{fo} {st}/>')

    def circle(self, c, r, fill='none', stroke='gray', w=1.2, dash=None, opacity=None):
        fc = 'none' if fill == 'none' else (col(fill, FILL) if fill in FILL else col(fill))
        st = self._stroke(stroke, w, dash, opacity=opacity) if stroke else 'stroke="none"'
        self.add(f'<circle cx="{f2(c[0])}" cy="{f2(c[1])}" r="{f2(r)}" fill="{fc}" {st}/>')

    def ellipse(self, c, rx, ry, rot=0, fill='none', stroke='gray', w=1.2, dash=None, opacity=None):
        fc = 'none' if fill == 'none' else (col(fill, FILL) if fill in FILL else col(fill))
        st = self._stroke(stroke, w, dash, opacity=opacity) if stroke else 'stroke="none"'
        tr = f' transform="rotate({f2(rot)} {f2(c[0])} {f2(c[1])})"' if rot else ''
        self.add(f'<ellipse cx="{f2(c[0])}" cy="{f2(c[1])}" rx="{f2(rx)}" ry="{f2(ry)}"{tr} fill="{fc}" {st}/>')

    def rect(self, x, y, w, h, rx=0, fill='none', stroke='gray', sw=1.2, dash=None, opacity=None):
        fc = 'none' if fill == 'none' else (col(fill, FILL) if fill in FILL else col(fill))
        st = self._stroke(stroke, sw, dash, opacity=opacity) if stroke else 'stroke="none"'
        self.add(f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" rx="{f2(rx)}" fill="{fc}" {st}/>')

    # --- texto
    def text(self, x, y, s, size=10, color='ink', anchor='middle', weight=400, rot=0, plate=False, family='sans', name=None, op=None):
        """s aceita marcação: *var* (itálico serifado), _{sub}, ^{sup}. y = linha de base."""
        tc = col(color, TEXT)
        w = rich_width(s, size, weight) if family == 'sans' else text_width(s, size, 'serif', weight, False)
        x0 = x - w / 2 if anchor == 'middle' else (x - w if anchor == 'end' else x)
        if plate:
            self.add(f'<rect x="{f2(x0 - 1.8)}" y="{f2(y - size * 0.82)}" width="{f2(w + 3.6)}" height="{f2(size * 1.1)}" rx="1.6" fill="#fff" fill-opacity="0.88"/>')
        spans = ''
        if family == 'serif':
            spans = esc(s)
            body = f'<text x="{f2(x)}" y="{f2(y)}" font-family="{SERIF}" font-size="{f2(size)}" font-weight="{weight}" fill="{tc}" text-anchor="{anchor}">{spans}</text>'
        else:
            sub_dy = size * 0.26
            sup_dy = -size * 0.36
            cur = 0.0
            for kind, t in parse_rich(s):
                if kind == 'n':
                    spans += f'<tspan dy="{f2(-cur)}">{esc(t)}</tspan>' if cur else esc(t)
                    cur = 0
                elif kind == 'i':
                    spans += f'<tspan dy="{f2(-cur)}" font-family="{SERIF}" font-style="italic" font-weight="400">{esc(t)}</tspan>'
                    cur = 0
                else:
                    ital = kind.endswith('i')
                    dy = sub_dy if kind.startswith('sub') else sup_dy
                    fam = f'font-family="{SERIF}" font-style="italic"' if ital else ''
                    spans += f'<tspan dy="{f2(dy - cur)}" font-size="{f2(size * 0.72)}" {fam}>{esc(t)}</tspan>'
                    cur = dy
            if cur:
                spans += f'<tspan dy="{f2(-cur)}"> </tspan>'
            op_attr = f' fill-opacity="{op}"' if op is not None else ''
            tr = f' transform="rotate({f2(rot)} {f2(x)} {f2(y)})"' if rot else ''
            body = f'<text x="{f2(x)}" y="{f2(y)}" font-family="{SANS}" font-size="{f2(size)}" font-weight="{weight}" fill="{tc}"{op_attr} text-anchor="{anchor}"{tr}>{spans}</text>'
        self.add(body)
        bb = (x0, y - size * 0.8, x0 + w, y + size * 0.24)
        if not rot:
            self.boxes.append((name or s, bb))
        return bb

    def vtext(self, x, y, letter, sub=None, size=12, color='ink', anchor='middle', plate=False, arrow=True, weight=400):
        """rótulo de vetor: letra em itálico serifado com seta curta acima (como \\vec{B})."""
        wl = text_width(letter, size, 'serif', 400, True)
        ws = text_width(sub, size * 0.72, 'sans') if sub else 0
        w = wl + ws
        x0 = x - w / 2 if anchor == 'middle' else (x - w if anchor == 'end' else x)
        tc = col(color, TEXT)
        if plate:
            self.add(f'<rect x="{f2(x0 - 1.8)}" y="{f2(y - size * 1.1)}" width="{f2(w + 3.6)}" height="{f2(size * 1.38)}" rx="1.6" fill="#fff" fill-opacity="0.88"/>')
        s = f'<text x="{f2(x0)}" y="{f2(y)}" font-family="{SERIF}" font-size="{f2(size)}" font-style="italic" fill="{tc}" text-anchor="start">{esc(letter)}'
        if sub:
            s += f'<tspan dy="{f2(size * 0.26)}" font-size="{f2(size * 0.72)}" font-family="{SANS}" font-style="normal">{esc(sub)}</tspan>'
        s += '</text>'
        self.add(s)
        if arrow:
            ay = y - size * 0.93
            a0, a1 = x0 + wl * 0.12, x0 + wl * 0.95
            self.add(f'<path d="M{f2(a0)} {f2(ay)} L{f2(a1)} {f2(ay)} M{f2(a1 - size * 0.2)} {f2(ay - size * 0.12)} L{f2(a1)} {f2(ay)} L{f2(a1 - size * 0.2)} {f2(ay + size * 0.12)}" fill="none" stroke="{tc}" stroke-width="{f2(max(0.7, size * 0.07))}" stroke-linecap="round" stroke-linejoin="round"/>')
        bb = (x0, y - size * 1.1, x0 + w, y + size * 0.3)
        self.boxes.append((f'vec {letter}{sub or ""}', bb))
        return bb

    # --- setas
    def arrow(self, p, q, color='blue', w=1.6, head=None, hw=None, dash=None, opacity=None, start=None):
        x1, y1 = p; x2, y2 = q
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L < 1e-6: return
        ux, uy = dx / L, dy / L
        hl = head if head is not None else max(5.5, min(9.0, 4.0 + w * 2.0))
        hl = min(hl, L * 0.7)
        hh = hw if hw is not None else hl * 0.42
        c = col(color)
        bx, by = x2 - ux * hl * 0.78, y2 - uy * hl * 0.78
        self.add(f'<line x1="{f2(x1)}" y1="{f2(y1)}" x2="{f2(bx)}" y2="{f2(by)}" fill="none" {self._stroke(color, w, dash, "butt", opacity=opacity)}/>')
        nx, ny = -uy, ux
        pts = [(x2, y2), (x2 - ux * hl + nx * hh, y2 - uy * hl + ny * hh), (bx, by), (x2 - ux * hl - nx * hh, y2 - uy * hl - ny * hh)]
        d = 'M' + ' L'.join(f'{f2(x)} {f2(y)}' for x, y in pts) + ' Z'
        op = f' fill-opacity="{opacity}"' if opacity is not None else ''
        self.add(f'<path d="{d}" fill="{c}"{op} stroke="{c}" stroke-width="0.4" stroke-linejoin="round"/>')
        if start == 'both':
            self.arrow(q, p, color, w, head, hw, dash, opacity)

    def arc_arrow(self, c, r, a0, a1, color='blue', w=1.5, head=None, n=24):
        """arco de círculo (ângulos em graus, convenção matemática, y para cima) com seta no fim (a1)."""
        pts = []
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((c[0] + r * math.cos(a), c[1] - r * math.sin(a)))
        self.carrow(pts, color, w, head)

    def carrow(self, pts, color='blue', w=1.5, head=None, hw=None, dash=None, opacity=None):
        """polilinha com ponta de seta no último ponto (a linha termina na base da ponta)."""
        if len(pts) < 2:
            return
        hl = head if head is not None else max(5.5, min(9.0, 4.0 + w * 2.0))
        acc, k = 0.0, 0
        base = pts[-1]
        for i in range(len(pts) - 1, 0, -1):
            seg = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            if acc + seg >= hl * 0.78:
                t = (hl * 0.78 - acc) / (seg or 1)
                base = (pts[i][0] + t * (pts[i - 1][0] - pts[i][0]), pts[i][1] + t * (pts[i - 1][1] - pts[i][1]))
                k = i
                break
            acc += seg
        body = list(pts[:k]) + [base] if k else list(pts)
        if len(body) >= 2:
            self.polyline(body, color, w, dash, opacity=opacity)
        p0 = pts[max(0, len(pts) - 3)]
        self._head(p0, pts[-1], color, hl, hw, w, opacity)

    def _head(self, p0, a, color, hl, hw, w, opacity=None):
        dx, dy = a[0] - p0[0], a[1] - p0[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        hh = hw if hw is not None else hl * 0.42
        c = col(color)
        bx, by = a[0] - ux * hl * 0.78, a[1] - uy * hl * 0.78
        nx, ny = -uy, ux
        pts = [(a[0], a[1]), (a[0] - ux * hl + nx * hh, a[1] - uy * hl + ny * hh), (bx, by), (a[0] - ux * hl - nx * hh, a[1] - uy * hl - ny * hh)]
        d = 'M' + ' L'.join(f'{f2(x)} {f2(y)}' for x, y in pts) + ' Z'
        op = f' fill-opacity="{opacity}"' if opacity is not None else ''
        self.add(f'<path d="{d}" fill="{c}"{op} stroke="{c}" stroke-width="0.4" stroke-linejoin="round"/>')

    def arrow_at(self, pts, frac, color='blue', w=1.3, head=6.5, opacity=None):
        """ponta de seta posicionada na fração do comprimento da polilinha (para linhas de campo)."""
        seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
        tot = sum(seg)
        if tot < 1e-6: return
        target, acc = tot * frac, 0.0
        for i, s in enumerate(seg):
            if acc + s >= target:
                t = (target - acc) / (s or 1)
                p = (pts[i][0] + t * (pts[i + 1][0] - pts[i][0]), pts[i][1] + t * (pts[i + 1][1] - pts[i][1]))
                d = (pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                L = math.hypot(*d) or 1
                q0 = (p[0] - d[0] / L * 1.0, p[1] - d[1] / L * 1.0)
                tip = (p[0] + d[0] / L * head * 0.5, p[1] + d[1] / L * head * 0.5)
                self._head(q0, tip, color, head, None, w, opacity)
                return
            acc += s

    # --- símbolos físicos
    def sym_out(self, c, r=5.0, color='blue', w=1.3, fill='white'):
        """⊙ : vetor saindo do plano (em direção ao leitor)."""
        self.circle(c, r, fill=fill, stroke=color, w=w)
        self.circle(c, r * 0.28, fill=col(color), stroke=None)

    def sym_in(self, c, r=5.0, color='blue', w=1.3, fill='white'):
        """⊗ : vetor entrando no plano."""
        self.circle(c, r, fill=fill, stroke=color, w=w)
        k = r * 0.68
        self.line((c[0] - k * 0.7071, c[1] - k * 0.7071), (c[0] + k * 0.7071, c[1] + k * 0.7071), color, w)
        self.line((c[0] - k * 0.7071, c[1] + k * 0.7071), (c[0] + k * 0.7071, c[1] - k * 0.7071), color, w)

    def symgrid(self, x0, y0, x1, y1, dx, dy, kind='in', color='blue', r=3.6, w=1.0, opacity=0.55, skip=None):
        y = y0
        row = 0
        while y <= y1 + 1e-6:
            x = x0 + (dx / 2 if row % 2 else 0)
            while x <= x1 + 1e-6:
                if not (skip and skip(x, y)):
                    g = f'<g opacity="{opacity}">'
                    self.add(g)
                    (self.sym_in if kind == 'in' else self.sym_out)((x, y), r, color, w, fill='none')
                    self.add('</g>')
                x += dx
            y += dy; row += 1

    def charge(self, c, sign='+', r=7.5, color='red'):
        self.circle(c, r, fill='white', stroke=color, w=1.5)
        k = r * 0.5
        self.line((c[0] - k, c[1]), (c[0] + k, c[1]), color, 1.6)
        if sign == '+':
            self.line((c[0], c[1] - k), (c[0], c[1] + k), color, 1.6)

    def magnet(self, x, y, w, h, n_left=True, size=None, rot=0):
        """ímã em barra: N = vermelho cheio (letra branca); S = contorno vermelho (letra vermelha)."""
        size = size or h * 0.5
        hw = w / 2
        nx, sx = (x, x + hw) if n_left else (x + hw, x)
        tr = f'<g transform="rotate({f2(rot)} {f2(x + hw)} {f2(y + h / 2)})">' if rot else '<g>'
        self.add(tr)
        self.rect(nx, y, hw, h, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.4)
        self.rect(sx, y, hw, h, 0, fill='#FFFFFF', stroke=STROKE['red'], sw=1.4)
        self.text(nx + hw / 2, y + h / 2 + size * 0.34, 'N', size, 'white', weight=700)
        self.text(sx + hw / 2, y + h / 2 + size * 0.34, 'S', size, 'red', weight=700)
        self.add('</g>')

    def compass(self, c, ang, r=8.5, needle=None):
        """bússola: ang = direção do polo N da agulha (graus, anti-horário a partir de +x, como em matemática)."""
        self.circle(c, r, fill='white', stroke='gray', w=1.0)
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        L = r * 0.82
        nx, ny = -uy, ux
        w_ = r * 0.26
        tipN = (c[0] + ux * L, c[1] + uy * L)
        tipS = (c[0] - ux * L, c[1] - uy * L)
        self.polygon([tipN, (c[0] + nx * w_, c[1] + ny * w_), (c[0] - nx * w_, c[1] - ny * w_)], fill=STROKE['red'], stroke=STROKE['red'], w=0.6)
        self.polygon([tipS, (c[0] + nx * w_, c[1] + ny * w_), (c[0] - nx * w_, c[1] - ny * w_)], fill='#FFFFFF', stroke=STROKE['red'], w=0.8)
        self.circle(c, 1.1, fill='gray', stroke=None)

    def battery(self, c, horizontal=True, size=14):
        x, y = c
        if horizontal:
            self.line((x - size * 0.4, y - size * 0.9), (x - size * 0.4, y + size * 0.9), 'ink', 1.8)
            self.line((x + size * 0.4, y - size * 0.55), (x + size * 0.4, y + size * 0.55), 'ink', 3.2)
        else:
            self.line((x - size * 0.9, y - size * 0.4), (x + size * 0.9, y - size * 0.4), 'ink', 1.8)
            self.line((x - size * 0.55, y + size * 0.4), (x + size * 0.55, y + size * 0.4), 'ink', 3.2)

    def resistor(self, p, q, n=6, amp=5.0, color='ink', w=1.6, lead=0.18):
        x1, y1 = p; x2, y2 = q
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy, ux
        a = L * lead; b = L * (1 - lead)
        pts = [(x1, y1), (x1 + ux * a, y1 + uy * a)]
        seg = (b - a) / n
        for i in range(n):
            t = a + seg * (i + 0.5)
            s = amp if i % 2 == 0 else -amp
            pts.append((x1 + ux * t + nx * s, y1 + uy * t + ny * s))
        pts += [(x1 + ux * b, y1 + uy * b), (x2, y2)]
        self.polyline(pts, color, w)

    # --- saída
    def tostring(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(self.w)} {f2(self.h)}" '
                f'font-family="{SANS}">' + '\n'.join(self.parts) + '</svg>')

    def save(self, name=None):
        name = name or self.name
        os.makedirs(OUTDIR, exist_ok=True)
        with open(os.path.join(OUTDIR, name + '.svg'), 'w', encoding='utf8') as f:
            f.write(self.tostring())
        self.check_boxes(name)
        return name

    def check_boxes(self, name):
        """avisa sobre rótulos que se sobrepõem ou saem do quadro."""
        bs = self.boxes
        for i in range(len(bs)):
            n1, b1 = bs[i]
            if b1[0] < -1 or b1[2] > self.w + 1 or b1[1] < -1 or b1[3] > self.h + 1:
                print(f'  [{name}] rótulo fora do quadro: «{n1}» {tuple(round(v) for v in b1)}')
            for j in range(i + 1, len(bs)):
                n2, b2 = bs[j]
                ox = min(b1[2], b2[2]) - max(b1[0], b2[0])
                oy = min(b1[3], b2[3]) - max(b1[1], b2[1])
                if ox > 1.0 and oy > 2.0:
                    print(f'  [{name}] sobreposição de rótulos: «{n1}» × «{n2}» ({ox:.0f}×{oy:.0f}px)')


# ----------------------------------------------------------------------------------- gráficos
class Plot:
    """Eixos cartesianos com grade, ticks (vírgula decimal) e conversão mundo->pixel."""
    def __init__(self, svg, x, y, w, h, xlim, ylim, xticks=None, yticks=None, xlabel='', ylabel='', xfmt=None, yfmt=None,
                 grid=True, size=9.0, xlab_dy=26, ylab_dx=-34, frame=True, ytick_labels=True):
        self.s, self.x, self.y, self.w, self.h = svg, x, y, w, h
        self.xlim, self.ylim = xlim, ylim
        self.size = size
        s = svg
        if frame:
            s.rect(x, y, w, h, 0, fill='white', stroke='light', sw=1.0)
        if grid:
            for t in (xticks or []):
                s.line((self.X(t), y), (self.X(t), y + h), 'faint', 0.8)
            for t in (yticks or []):
                s.line((x, self.Y(t)), (x + w, self.Y(t)), 'faint', 0.8)
        # eixos principais em zero
        if ylim[0] < 0 < ylim[1]:
            s.line((x, self.Y(0)), (x + w, self.Y(0)), 'gray', 1.1)
        if xlim[0] < 0 < xlim[1]:
            s.line((self.X(0), y), (self.X(0), y + h), 'gray', 1.1)
        xfmt = xfmt or (lambda v: num(v, 0) if abs(v - round(v)) < 1e-9 else num(v, 1))
        yfmt = yfmt or (lambda v: num(v, 0) if abs(v - round(v)) < 1e-9 else num(v, 1))
        for t in (xticks or []):
            s.line((self.X(t), y + h), (self.X(t), y + h + 3), 'gray', 1.0)
            s.text(self.X(t), y + h + 12.5, xfmt(t), size, 'gray')
        if ytick_labels:
            for t in (yticks or []):
                s.line((x - 3, self.Y(t)), (x, self.Y(t)), 'gray', 1.0)
                s.text(x - 6, self.Y(t) + size * 0.34, yfmt(t), size, 'gray', anchor='end')
        if xlabel:
            s.text(x + w / 2, y + h + xlab_dy, xlabel, size + 1, 'ink')
        if ylabel:
            s.text(x + ylab_dx, y + h / 2, ylabel, size + 1, 'ink', rot=-90)

    def X(self, v):
        return self.x + (v - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * self.w

    def Y(self, v):
        return self.y + self.h - (v - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * self.h

    def curve(self, xs, ys, color='blue', w=2.0, dash=None, clip=True):
        pts, segs = [], []
        y0, y1 = self.y, self.y + self.h
        for a, b in zip(xs, ys):
            p = (self.X(a), self.Y(b))
            if clip and (p[1] < y0 - 0.5 or p[1] > y1 + 0.5):
                if len(pts) > 1: segs.append(pts)
                pts = []
                continue
            pts.append(p)
        if len(pts) > 1: segs.append(pts)
        for sgm in segs:
            self.s.polyline(sgm, color, w, dash)

    def dot(self, xv, yv, color='red', r=3.4):
        self.s.circle((self.X(xv), self.Y(yv)), r, fill=col(color), stroke='white', w=1.0)


def gallery_html(names, cols=2):
    cells = ''.join(f'<div class="cell"><div class="nm">{n}</div>{open(os.path.join(OUTDIR, n + ".svg"), encoding="utf8").read()}</div>' for n in names)
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/fonts/fonts.css"><link rel="stylesheet" href="../assets/katex/katex.min.css">
<style>body{{margin:10px;background:#fff;font-family:'Source Sans 3'}} .g{{display:grid;grid-template-columns:repeat({cols},1fr);gap:14px}}
.cell{{border:1px solid #ccd;padding:4px}} .nm{{font:700 11px sans-serif;color:#666}} svg{{width:100%;height:auto;display:block}}</style></head>
<body><div class="g">{cells}</div></body></html>'''
