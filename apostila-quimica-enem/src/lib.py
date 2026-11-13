# -*- coding: utf-8 -*-
"""Biblioteca base da apostila: paleta semântica, CSS, primitivas SVG e componentes HTML."""
import re, math, html

# ---------- Paleta semântica ----------
INK = '#1B2236'; GRAY = '#5B6575'; LGRAY = '#D6DBE4'; BG = '#F5F7FA'
BLUE = '#1F6FD0'; BLUE_D = '#12528F'; BLUE_L = '#DCEBFB'
AMBER = '#E9A100'; AMBER_D = '#8A5600'; AMBER_L = '#FFF0C7'
PURPLE = '#7B3FBF'; PURPLE_D = '#5A2A96'; PURPLE_L = '#EDE0F8'
GREEN = '#2E9E5B'; GREEN_D = '#17713E'; GREEN_L = '#DDF3E4'
ORANGE = '#F26B1D'; ORANGE_D = '#B94A07'; ORANGE_L = '#FFE4D2'
RED = '#D62F3A'; RED_D = '#A81F2A'; RED_L = '#FDE2E4'
COL = dict(blue=(BLUE, BLUE_D, BLUE_L), amber=(AMBER, AMBER_D, AMBER_L), purple=(PURPLE, PURPLE_D, PURPLE_L),
           green=(GREEN, GREEN_D, GREEN_L), orange=(ORANGE, ORANGE_D, ORANGE_L), red=(RED, RED_D, RED_L),
           ink=(INK, INK, BG), gray=(GRAY, GRAY, BG))

# ---------- Fórmulas ----------
def fm(s):
    """Markup HTML: H_2O, Ca^2+, SO_4^2-, x_{12}, 10^{-14}."""
    s = html.escape(s, quote=False)
    s = re.sub(r'_\{([^}]*)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'\^\{([^}]*)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'_(\d+)', r'<sub>\1</sub>', s)
    s = re.sub(r'\^(\d*[+\-−])', r'<sup>\1</sup>', s)
    s = re.sub(r'\^(\d+)', r'<sup>\1</sup>', s)
    return s

def svg_tspans(s, size):
    """Converte markup em tspans (sub/sup) para texto SVG."""
    out = []; i = 0
    s = html.escape(s, quote=False)
    pat = re.compile(r'_\{([^}]*)\}|\^\{([^}]*)\}|_(\d+)|\^(\d*[+\-−])|\^(\d+)')
    pos = 0; shift = 0
    for mt in pat.finditer(s):
        if mt.start() > pos:
            out.append(s[pos:mt.start()])
        sub = mt.group(1) or mt.group(3)
        sup = mt.group(2) or mt.group(4) or mt.group(5)
        if sub is not None:
            out.append(f'<tspan font-size="{size*0.72:.1f}" dy="{size*0.22:.1f}">{sub}</tspan><tspan dy="{-size*0.22:.1f}"></tspan>')
        else:
            out.append(f'<tspan font-size="{size*0.72:.1f}" dy="{-size*0.38:.1f}">{sup}</tspan><tspan dy="{size*0.38:.1f}"></tspan>')
        pos = mt.end()
    out.append(s[pos:])
    return ''.join(out)

# ---------- SVG ----------
_CLIP = [0]
TEX = {'hatch-amber': (AMBER_L, AMBER, 'hatch'), 'dots-blue': (BLUE_L, BLUE, 'dots'), 'hatch-purple': (PURPLE_L, PURPLE, 'hatch-'),
       'hatch-red': (RED_L, RED, 'hatch'), 'hatch-green': (GREEN_L, GREEN, 'hatch-'), 'hatch-orange': (ORANGE_L, ORANGE, 'hatch'), 'waterbg': ('#EAF3FD', BLUE, 'water')}
def solid(fill):
    return TEX[fill[5:-1]][0] if isinstance(fill, str) and fill.startswith('url(#') else fill

class Svg:
    def _tex(self, x, y, w, h, name, rx):
        base, col, kind = TEX[name]
        _CLIP[0] += 1; cid = f'tc{_CLIP[0]}'
        out = [f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}"/></clipPath><g clip-path="url(#{cid})">']
        if kind.startswith('hatch'):
            sp = 6; k = -h
            sgn = 1 if kind == 'hatch' else -1
            while k < w + h:
                if sgn == 1: out.append(f'<line x1="{x+k:.1f}" y1="{y+h:.1f}" x2="{x+k+h:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="1.5"/>')
                else: out.append(f'<line x1="{x+k:.1f}" y1="{y:.1f}" x2="{x+k+h:.1f}" y2="{y+h:.1f}" stroke="{col}" stroke-width="1.5"/>')
                k += sp
        elif kind == 'dots':
            yy = y + 3
            while yy < y + h:
                xx = x + 3 + (3 if int((yy - y)/6) % 2 else 0)
                while xx < x + w:
                    out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="1.2" fill="{col}"/>'); xx += 6
                yy += 6
        elif kind == 'water':
            import math as _m
            row = 0; yy = y + 10
            while yy < y + h + 10:
                xx = x + 12 + (12 if row % 2 else 0)
                while xx < x + w + 10:
                    rot = (int(xx*7 + yy*13) % 6) * 60 + 20
                    out.append(f'<use href="#wm" transform="translate({xx:.1f},{yy:.1f}) rotate({rot}) scale(0.95)"/>'); xx += 24
                yy += 20; row += 1
        out.append('</g>')
        return ''.join(out)
    def __init__(self, w, h, style=''):
        self.w, self.h, self.p, self.style = w, h, [], style
    def add(self, s): self.p.append(s); return self
    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None, cap='round', op=None):
        a = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#arr-{marker})"' if marker else ''
        o = f' opacity="{op}"' if op else ''
        return self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{a}{m}{o}/>')
    def arrow(self, x1, y1, x2, y2, color='ink', sw=2): 
        return self.line(x1, y1, x2, y2, stroke=COL[color][0] if color in COL else color, sw=sw, marker=color)
    def rect(self, x, y, w, h, fill='none', stroke=None, rx=0, sw=1, dash=None, op=None):
        if isinstance(fill, str) and fill.startswith('url(#'):
            name = fill[5:-1]
            self.rect(x, y, w, h, TEX[name][0], None, rx, 1, None, op)
            self.add(self._tex(x, y, w, h, name, rx))
            if stroke: self.rect(x, y, w, h, 'none', stroke, rx, sw, dash, op)
            return self
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        return self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{s}{d}{o}/>')
    def circ(self, cx, cy, r, fill='none', stroke=None, sw=1.2, op=None):
        fill = solid(fill)
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        o = f' opacity="{op}"' if op else ''
        return self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"{s}{o}/>')
    def ell(self, cx, cy, rx, ry, fill='none', stroke=None, sw=1.2, rot=0, dash=None):
        fill = solid(fill)
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        t = f' transform="rotate({rot} {cx:.1f} {cy:.1f})"' if rot else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}"{s}{t}{d}/>')
    def path(self, d, fill='none', stroke=INK, sw=1.5, dash=None, marker=None, cap='round', op=None):
        fill = solid(fill)
        a = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#arr-{marker})"' if marker else ''
        o = f' opacity="{op}"' if op else ''
        return self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"{a}{m}{o}/>')
    def poly(self, pts, fill='none', stroke=INK, sw=1.5, dash=None, close=False):
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + (' Z' if close else '')
        return self.path(d, fill=fill, stroke=stroke, sw=sw, dash=dash)
    def text(self, x, y, s, size=11, fill=INK, anchor='start', weight=400, italic=False, rot=None, lh=1.25, op=None):
        lines = s.split('\n'); out = []
        for i, ln in enumerate(lines):
            yy = y + i*size*lh
            tr = f' transform="rotate({rot} {x:.1f} {yy:.1f})"' if rot else ''
            st = ' font-style="italic"' if italic else ''
            o = f' opacity="{op}"' if op else ''
            out.append(f'<text x="{x:.1f}" y="{yy:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{st}{tr}{o}>{svg_tspans(ln, size)}</text>')
        return self.add(''.join(out))
    def label(self, x, y, s, size=10.5, color=INK, bg='#fff', weight=600, anchor='middle', pad=3):
        """Texto com fundo para legibilidade."""
        w = len(re.sub(r'[_^{}]', '', s)) * size * 0.56 + pad*2
        x0 = x - w/2 if anchor == 'middle' else (x - pad if anchor == 'start' else x - w + pad)
        self.rect(x0, y - size - 1, w, size + 5, fill=bg, rx=3, op=0.92)
        return self.text(x, y, s, size, color, anchor, weight)
    def g(self, inner, tx=0, ty=0, extra=''):
        return self.add(f'<g transform="translate({tx:.1f},{ty:.1f})" {extra}>{inner}</g>')
    def embed(self, svg_str, x, y):
        """Embute outro SVG (ex.: RDKit) em x,y."""
        svg_str = re.sub(r'<svg ', f'<svg x="{x}" y="{y}" ', svg_str, count=1)
        return self.add(svg_str)
    def render(self, cls=''):
        return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="InterT, Inter, \'DejaVu Sans\', sans-serif" style="{self.style}">' + ''.join(self.p) + '</svg>')

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="wm"><line x1="0" y1="0" x2="-6.5" y2="6" stroke="%s" stroke-width="1.3"/><line x1="0" y1="0" x2="6.5" y2="6" stroke="%s" stroke-width="1.3"/><circle cx="0" cy="0" r="3.6" fill="%s" stroke="%s"/><circle cx="-6.5" cy="6" r="2.1" fill="#fff" stroke="%s"/><circle cx="6.5" cy="6" r="2.1" fill="#fff" stroke="%s"/></g>''' % (BLUE_D, BLUE_D, BLUE, BLUE_D, BLUE_D, BLUE_D) + ''.join(
    f'<marker id="arr-{n}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0.5 L9.5,5 L0,9.5 L2.6,5 Z" fill="{c[0]}"/></marker>'
    for n, c in COL.items()) + f'''
</defs></svg>'''

# ---------- Eixos / gráficos ----------
class Axes:
    def __init__(self, svg, x0, y0, w, h, xr, yr):
        self.s, self.x0, self.y0, self.w, self.h, self.xr, self.yr = svg, x0, y0, w, h, xr, yr
    def X(self, v): return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w
    def Y(self, v): return self.y0 + self.h - (v - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h
    def frame(self, xticks=None, yticks=None, xlabel='', ylabel='', grid=True, xfmt=str, yfmt=str, size=10, xlabel_dy=34, ylabel_dx=40):
        s = self.s
        if yticks is not None:
            for v in yticks:
                y = self.Y(v)
                if grid: s.line(self.x0, y, self.x0+self.w, y, LGRAY, 0.8)
                s.text(self.x0-6, y+3.5, yfmt(v), size, GRAY, 'end')
        if xticks is not None:
            for v in xticks:
                x = self.X(v)
                if grid and v != self.xr[0]: s.line(x, self.y0, x, self.y0+self.h, '#E9EDF3', 0.8)
                s.line(x, self.y0+self.h, x, self.y0+self.h+4, GRAY, 1)
                s.text(x, self.y0+self.h+15, xfmt(v), size, GRAY, 'middle')
        s.line(self.x0, self.y0, self.x0, self.y0+self.h, INK, 1.4)
        s.line(self.x0, self.y0+self.h, self.x0+self.w, self.y0+self.h, INK, 1.4)
        if xlabel: s.text(self.x0+self.w/2, self.y0+self.h+xlabel_dy, xlabel, size+0.5, INK, 'middle', 600)
        if ylabel: s.text(self.x0-ylabel_dx, self.y0+self.h/2, ylabel, size+0.5, INK, 'middle', 600, rot=-90)
    def pts(self, data): return [(self.X(x), self.Y(y)) for x, y in data]
    def line(self, data, color=INK, sw=2.2, dash=None):
        self.s.poly(self.pts(data), stroke=color, sw=sw, dash=dash)
    def marker(self, x, y, shape='o', color=INK, r=4.2, fill='#fff'):
        X, Y = self.X(x), self.Y(y); s = self.s
        if shape == 'o': s.circ(X, Y, r, fill, color, 1.8)
        elif shape == 's': s.rect(X-r, Y-r, 2*r, 2*r, fill, color, sw=1.8)
        elif shape == 'd': s.poly([(X, Y-r*1.3), (X+r*1.3, Y), (X, Y+r*1.3), (X-r*1.3, Y)], fill, color, 1.8, close=True)
        elif shape == '^': s.poly([(X, Y-r*1.3), (X+r*1.2, Y+r), (X-r*1.2, Y+r)], fill, color, 1.8, close=True)
        elif shape == 'f': s.circ(X, Y, r, color, '#fff', 1.2)

# ---------- HTML ----------
def box(kind, title, body, cls='', icon=None):
    """kind: blue amber purple green orange red ink gray"""
    c = COL[kind]
    ic = {'red': '⚠', 'orange': '⚗', 'green': '❀', 'ink': '◆', 'gray': '↔', 'purple': '⬡', 'blue': '≈', 'amber': '≈'}.get(kind, '') if icon is None else icon
    return (f'<div class="box {kind} {cls}" style="--c:{c[0]};--cd:{c[1]};--cl:{c[2]}">'
            f'<div class="bt">{ic} {title}</div><div class="bb">{body}</div></div>')

def tag(kind, text):
    c = COL[kind]
    return f'<span class="chip" style="--c:{c[0]};--cd:{c[1]};--cl:{c[2]}">{text}</span>'

def quiz(items, title='TESTE-SE (recuperação ativa)'):
    lis = ''.join(f'<li>{q}<span class="ans">→ {a}</span></li>' for q, a in items)
    return f'<div class="box quiz"><div class="bt">✎ {title}</div><ol>{lis}</ol></div>'

CHAPTERS = {
    'I': ('Introdução', ''), 'A': ('Módulo A', 'Ligações, polaridade e forças intermoleculares'),
    'B': ('Módulo B', 'Solubilidade, hidrofobicidade e lipofilicidade'), 'C': ('Módulo C', 'Funções orgânicas'),
    'D': ('Módulo D', 'Reações orgânicas, biomoléculas e polímeros'), 'E': ('Módulo E', 'Soluções e cálculos'),
    'F': ('Módulo F', 'Separação de misturas e Química ambiental'), 'G': ('Módulo G', 'Estequiometria'),
    'H': ('Módulo H', 'Cinética química'), 'I2': ('Módulo I', 'Equilíbrio, ácidos, bases e pH'),
    'J': ('Módulo J', 'Eletroquímica'), 'K': ('Módulo K', 'Termoquímica'), 'R': ('Revisão', 'Questões, fórmulas e fontes'),
}
PAGES = []
QC = []  # registro de verificações automáticas (estruturas, fórmulas, cálculos)
def page(mod, kicker, title, body, sub=None, cls='', key=None):
    PAGES.append(dict(mod=mod, kicker=kicker, title=title, body=body, sub=sub, cls=cls, key=key))

CSS = '''
@font-face { font-family: InterT; font-weight: 400; font-style: normal; src: url('fonts/InterT-400.ttf'); }
@font-face { font-family: InterT; font-weight: 500; font-style: normal; src: url('fonts/InterT-500.ttf'); }
@font-face { font-family: InterT; font-weight: 600; font-style: normal; src: url('fonts/InterT-600.ttf'); }
@font-face { font-family: InterT; font-weight: 700; font-style: normal; src: url('fonts/InterT-700.ttf'); }
@font-face { font-family: InterT; font-weight: 800; font-style: normal; src: url('fonts/InterT-800.ttf'); }
@font-face { font-family: InterT; font-weight: 900; font-style: normal; src: url('fonts/InterT-900.ttf'); }
@font-face { font-family: InterT; font-weight: 400; font-style: italic; src: url('fonts/InterT-400i.ttf'); }
@page { size: 210mm 297mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: InterT, Inter, 'DejaVu Sans', sans-serif; color: %(INK)s; font-size: 8.7pt; line-height: 1.36; background: #fff; }
sub, sup { font-size: 70%%; line-height: 0; } sub { vertical-align: -0.28em; } sup { vertical-align: 0.5em; }
.page { width: 210mm; height: 297mm; padding: 11mm 13mm 10mm 13mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; display: flex; flex-direction: column; background: #fff; }
.ph { display: flex; justify-content: space-between; align-items: center; font-size: 6.9pt; letter-spacing: .06em; color: %(GRAY)s; text-transform: uppercase; border-bottom: .4mm solid %(LGRAY)s; padding-bottom: 1.6mm; font-weight: 600; }
.ph .mod { display: flex; align-items: center; gap: 2mm; } .ph .letter { background: %(INK)s; color: #fff; border-radius: 1mm; padding: .2mm 1.6mm; font-weight: 800; letter-spacing: 0; }
.pt { margin: 3.2mm 0 3mm; } .kick { font-size: 7pt; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; color: %(GRAY)s; }
h1 { font-size: 17.5pt; line-height: 1.12; font-weight: 800; letter-spacing: -.01em; margin-top: .6mm; }
h1 .sub { display:block; font-size: 9pt; font-weight: 500; color: %(GRAY)s; letter-spacing: 0; margin-top: 1mm; }
.pbody { flex: 1; min-height: 0; overflow: hidden; display: flex; flex-direction: column; gap: 3mm; }
.pf { display: flex; justify-content: space-between; font-size: 6.8pt; color: %(GRAY)s; padding-top: 1.5mm; border-top: .3mm solid %(LGRAY)s; margin-top: 2mm; }
.pf b { color: %(INK)s; }
h2 { font-size: 10.2pt; font-weight: 800; margin-bottom: 1.2mm; line-height: 1.2; } h3 { font-size: 8.8pt; font-weight: 700; margin-bottom: .8mm; }
p { margin-bottom: 1.4mm; } p:last-child { margin-bottom: 0; } ul, ol { padding-left: 4mm; } li { margin-bottom: .7mm; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; } .cols3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.5mm; }
.cols21 { display: grid; grid-template-columns: 2fr 1fr; gap: 4mm; } .cols12 { display: grid; grid-template-columns: 1fr 2fr; gap: 4mm; }
.row { display: flex; gap: 4mm; align-items: flex-start; } .grow { flex: 1; min-width: 0; } .center { text-align: center; } svg { display: block; max-width: 100%%; }
.box { border-left: 1.1mm solid var(--c); background: var(--cl); border-radius: 0 1.6mm 1.6mm 0; padding: 1.8mm 2.6mm 2mm; font-size: 8.2pt; }
.box .bt { font-size: 7.1pt; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; color: var(--cd); margin-bottom: .8mm; }
.box.quiz { border-left-color: %(INK)s; background: %(BG)s; --cd: %(INK)s; } .box.quiz ol { padding-left: 4.2mm; } .box.quiz li { margin-bottom: 1mm; }
.ans { display: block; font-size: 7.4pt; color: %(GRAY)s; font-style: italic; }
.chip { display: inline-block; background: var(--cl); color: var(--cd); border: .3mm solid var(--c); border-radius: 5mm; padding: 0 2mm; font-size: 7.3pt; font-weight: 700; line-height: 1.5; white-space: nowrap; }
.card { border: .35mm solid %(LGRAY)s; border-radius: 2mm; padding: 2mm 2.6mm; background: #fff; }
.card h3 { display:flex; align-items:center; gap:1.5mm; }
table { border-collapse: collapse; width: 100%%; font-size: 8pt; } th { background: %(INK)s; color: #fff; font-weight: 700; padding: 1mm 1.6mm; text-align: left; font-size: 7.5pt; }
td { padding: 1mm 1.6mm; border-bottom: .25mm solid %(LGRAY)s; vertical-align: middle; } tr:nth-child(even) td { background: %(BG)s; }
.eq { font-size: 11pt; font-weight: 700; background: #fff; border: .35mm solid %(LGRAY)s; border-radius: 1.6mm; padding: 1mm 2.4mm; display: inline-block; letter-spacing: .01em; }
.small { font-size: 7.3pt; color: %(GRAY)s; } .cap { font-size: 7.2pt; color: %(GRAY)s; margin-top: 1mm; line-height: 1.3; } .b { font-weight: 700; }
.t-blue { color: %(BLUE_D)s; } .t-amber { color: %(AMBER_D)s; } .t-purple { color: %(PURPLE_D)s; } .t-green { color: %(GREEN_D)s; } .t-orange { color: %(ORANGE_D)s; } .t-red { color: %(RED_D)s; }
.kbd { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.6pt; background: %(BG)s; border: .25mm solid %(LGRAY)s; border-radius: .8mm; padding: 0 1mm; }
.step { display:inline-flex; align-items:center; justify-content:center; width: 4.6mm; height: 4.6mm; border-radius: 50%%; background: %(INK)s; color:#fff; font-weight: 800; font-size: 7.4pt; flex: none; }
.rx { display: flex; align-items: center; gap: 1.5mm; flex-wrap: nowrap; justify-content: center; }
.mol { text-align: center; font-size: 7pt; color: %(GRAY)s; line-height: 1.2; } .mol svg { margin: 0 auto; }
''' % dict(INK=INK, GRAY=GRAY, LGRAY=LGRAY, BG=BG, BLUE_D=BLUE_D, AMBER_D=AMBER_D, PURPLE_D=PURPLE_D, GREEN_D=GREEN_D, ORANGE_D=ORANGE_D, RED_D=RED_D)

def render_pages():
    out = []
    total = len(PAGES)
    for i, p in enumerate(PAGES, 1):
        ch = CHAPTERS[p['mod']]
        letter = {'I': '★', 'I2': 'I', 'R': '✔'}.get(p['mod'], p['mod'])
        sub = f'<span class="sub">{p["sub"]}</span>' if p['sub'] else ''
        if p['cls'] == 'cover':
            out.append(f'<section class="page cover">{p["body"]}</section>'); continue
        out.append(f'''<section class="page {p['cls']}">
<div class="ph"><span class="mod"><span class="letter">{letter}</span><span>{ch[0]}{' · ' + ch[1] if ch[1] else ''}</span></span><span>Apostila visual de Química · ENEM</span></div>
<div class="pt"><div class="kick">{p['kicker']}</div><h1>{p['title']}{sub}</h1></div>
<div class="pbody">{p['body']}</div>
<div class="pf"><span><b>Química ENEM</b> · conteúdo priorizado por incidência histórica, pré-requisitos e rendimento</span><span><b>{i}</b> / {total}</span></div>
</section>''')
    doc = ''.join(out)
    keys = {p['key']: i for i, p in enumerate(PAGES, 1) if p['key']}
    doc = re.sub(r'@@P:(\w+)@@', lambda m: str(keys.get(m.group(1), '?')), doc)
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Apostila visual de Química para o ENEM</title><style>' + CSS + '</style></head><body>' + DEFS + doc + '</body></html>'
