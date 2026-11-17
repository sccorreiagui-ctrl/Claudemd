#!/usr/bin/env python3
"""Gera as ilustrações científicas (SVG vetorial) da apostila.

Todas as curvas são calculadas a partir das equações físicas correspondentes
(Planck, Einstein, Bohr, Hubble, decaimento exponencial...), não desenhadas "a olho".
Saída: ../figures/*.svg  (também importados em linha pelo build.py).
"""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)

# ---- Paleta semântica ------------------------------------------------------
INK = "#1B2430"
MUTE = "#4A5568"
GRID = "#C9D0DA"
PURPLE, PURPLE_L = "#6B3FA0", "#EFE8F8"
BLUE, BLUE_L = "#1769C9", "#E6F0FB"
ORANGE, ORANGE_D, ORANGE_L = "#E07000", "#B35400", "#FDEFDC"
CYAN, CYAN_D, CYAN_L = "#0B8CA3", "#086A7C", "#E0F4F7"
GREEN, GREEN_D, GREEN_L = "#2A8A4A", "#1E6B38", "#E3F4E8"
RED, RED_L = "#C62828", "#FCE8E8"
GRAY, GRAY_L = "#5B6573", "#EEF0F3"

# Constantes (SI)
H = 6.62607e-34
C = 2.99792e8
KB = 1.380649e-23


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, name, w, h, title):
        self.name, self.w, self.h, self.title = name, w, h, title
        self.defs, self.body, self._m, self._n = [], [], {}, 0

    # -- primitivas -----------------------------------------------------
    def uid(self, p="i"):
        self._n += 1
        return f"{self.name}-{p}{self._n}"

    def marker(self, color, size=6):
        key = (color, size)
        if key not in self._m:
            mid = self.uid("m")
            self._m[key] = mid
            self.defs.append(
                f'<marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="{size}" '
                f'markerHeight="{size}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
            )
        return self._m[key]

    def raw(self, s):
        self.body.append(s)

    def line(self, x1, y1, x2, y2, color=INK, w=1.2, dash=None, arrow=False, start=False, op=None, cap="butt"):
        a = ""
        if arrow:
            a += f' marker-end="url(#{self.marker(color)})"'
        if start:
            a += f' marker-start="url(#{self.marker(color)})"'
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op else ""
        self.raw(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{w}"{d}{a}{o} stroke-linecap="{cap}"/>'
        )

    def path(self, pts, color=INK, w=1.5, dash=None, fill="none", arrow=False, close=False, clip=None, op=None, join="round"):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
        a = f' marker-end="url(#{self.marker(color)})"' if arrow else ""
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        c = f' clip-path="url(#{clip})"' if clip else ""
        o = f' opacity="{op}"' if op else ""
        self.raw(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}"{ds}{a}{c}{o} stroke-linejoin="{join}" stroke-linecap="round"/>')

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, rx=0, op=None, dash=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' opacity="{op}"' if op else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{s}{o}{d}/>')

    def circle(self, x, y, r, fill="none", stroke=None, sw=1, op=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' opacity="{op}"' if op else ""
        self.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}{o}/>')

    def text(self, x, y, t, size=10, color=INK, anchor="start", weight=400, rot=None, halo=False, italic=False):
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
        h = ' stroke="#fff" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        it = ' font-style="italic"' if italic else ""
        self.raw(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{it}{tr}{h}>{esc(t)}</text>'
        )

    def lines(self, x, y, ts, size=10, lh=12.5, **kw):
        for i, t in enumerate(ts):
            self.text(x, y + i * lh, t, size=size, **kw)

    def clip(self, x, y, w, h):
        cid = self.uid("c")
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
        return cid

    def wavy(self, x1, y1, x2, y2, amp=3, wl=12, color=BLUE, w=1.6, arrow=True):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy, ux
        pts, t = [], 0.0
        while t < L:
            off = amp * math.sin(2 * math.pi * t / wl)
            pts.append((x1 + ux * t + nx * off, y1 + uy * t + ny * off))
            t += 1.5
        pts.append((x2, y2))
        self.path(pts, color=color, w=w, arrow=arrow)

    def axes(self, x0, y0, x1, y1, xlab="", ylab="", color=INK, ylab_x=None, xlab_dy=26):
        """x0,y0 = origem; x1 = fim eixo x; y1 = topo do eixo y (y1<y0)."""
        self.line(x0, y0, x1, y0, color=color, w=1.3, arrow=True)
        self.line(x0, y0, x0, y1, color=color, w=1.3, arrow=True)
        if xlab:
            self.text((x0 + x1) / 2, y0 + xlab_dy, xlab, size=10, color=color, anchor="middle")
        if ylab:
            lx = ylab_x if ylab_x is not None else x0 - 30
            self.text(lx, (y0 + y1) / 2, ylab, size=10, color=color, anchor="middle", rot=-90)

    def render(self):
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" class="fig" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-label="{esc(self.title)}">'
            f"<title>{esc(self.title)}</title>{defs}{''.join(self.body)}</svg>"
        )

    def save(self):
        with open(os.path.join(OUT, self.name + ".svg"), "w", encoding="utf-8") as f:
            f.write(self.render())


def wl_to_rgb(wl):
    """Aproximação usual de cor visível para comprimento de onda em nm."""
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / 60, 0, 1
    elif 440 <= wl < 490:
        r, g, b = 0, (wl - 440) / 50, 1
    elif 490 <= wl < 510:
        r, g, b = 0, 1, -(wl - 510) / 20
    elif 510 <= wl < 580:
        r, g, b = (wl - 510) / 70, 1, 0
    elif 580 <= wl < 645:
        r, g, b = 1, -(wl - 645) / 65, 0
    elif 645 <= wl <= 700:
        r, g, b = 1, 0, 0
    else:
        r = g = b = 0
    f = 1.0
    if 380 <= wl < 420:
        f = 0.35 + 0.65 * (wl - 380) / 40
    elif 645 < wl <= 700:
        f = 0.55 + 0.45 * (700 - wl) / 55
    return "#%02x%02x%02x" % tuple(int(255 * (c * f) ** 0.8) for c in (r, g, b))


# =============================================================================
# 0. Linha do tempo
# =============================================================================
def fig_timeline():
    s = Svg("timeline", 703, 124, "Linha do tempo da Física Moderna, de 1887 a 2015")
    ev = [
        ("1887", "Michelson–Morley", "sem éter detectado", CYAN, None),
        ("1896", "Becquerel", "radioatividade", ORANGE, None),
        ("1900", "Planck", "quanta de energia", PURPLE, None),
        ("1905", "Einstein", "fóton; relatividade", PURPLE, CYAN),
        ("1913", "Bohr", "níveis de energia", PURPLE, None),
        ("1915–19", "Relat. Geral", "eclipse de 1919", CYAN, None),
        ("1924", "de Broglie", "ondas de matéria", PURPLE, None),
        ("1927", "Heisenberg", "incerteza; Lemaître", PURPLE, GREEN),
        ("1929", "Hubble", "expansão observada", GREEN, None),
        ("1965", "Penzias e Wilson", "CMB detectada", GREEN, None),
        ("2015", "LIGO", "ondas gravitacionais", CYAN, None),
    ]
    y = 62
    s.line(14, y, 689, y, color=GRAY, w=2.5, arrow=True)
    for i, (yr, a, b, c1, c2) in enumerate(ev):
        x = 58 + i * 58.7
        up = i % 2 == 0
        if c2:
            s.circle(x, y, 7, fill=c1, stroke=c2, sw=3.2)
        else:
            s.circle(x, y, 6, fill=c1, stroke="#fff", sw=1.5)
        if up:
            s.line(x, y - 7, x, y - 17, color=GRID, w=1)
            ty = 14
        else:
            s.line(x, y + 7, x, y + 17, color=GRID, w=1)
            ty = 86
        s.text(x, ty, yr, size=11, color=INK, anchor="middle", weight=700)
        s.text(x, ty + 12, a, size=9.5, color=INK, anchor="middle", weight=600)
        s.text(x, ty + 23, b, size=9, color=MUTE, anchor="middle")
    s.save()
    return s


# =============================================================================
# 1. Corpo negro (Planck × Rayleigh–Jeans)
# =============================================================================
def planck(l_nm, T):
    lam = l_nm * 1e-9
    x = H * C / (lam * KB * T)
    if x > 600:
        return 0.0
    return 2 * H * C**2 / lam**5 / (math.exp(x) - 1)


def rayleigh_jeans(l_nm, T):
    lam = l_nm * 1e-9
    return 2 * C * KB * T / lam**4


def fig_blackbody():
    W, Hh = 345, 262
    s = Svg("corponegro", W, Hh, "Curvas de corpo negro para três temperaturas e previsão clássica de Rayleigh–Jeans")
    x0, x1, y0, y1 = 46, 330, 206, 14  # origem x, fim x, base y, topo y
    lmax = 3000.0
    ymax = 1.22 * planck(2.898e6 / 5000, 5000)
    X = lambda l: x0 + (l / lmax) * (x1 - 8 - x0)
    Y = lambda b: y0 - (b / ymax) * (y0 - y1 - 8)
    clip = s.clip(x0, y1 - 4, x1 - x0, y0 - y1 + 4)

    # faixa UV / visível / IV
    s.rect(X(0), y0, X(400) - X(0), 8, fill=PURPLE_L)
    gid = s.uid("g")
    stops = "".join(
        f'<stop offset="{(w - 400) / 300:.3f}" stop-color="{wl_to_rgb(w)}"/>' for w in range(400, 701, 25)
    )
    s.defs.append(f'<linearGradient id="{gid}" x1="0" x2="1" y1="0" y2="0">{stops}</linearGradient>')
    s.rect(X(400), y0, X(700) - X(400), 8, fill=f"url(#{gid})")
    s.text(X(200), y0 + 19, "UV", size=9.5, color=PURPLE, anchor="middle", weight=600)
    s.text(X(550), y0 + 19, "visível", size=9.5, color=MUTE, anchor="middle", weight=600)
    s.text(X(1700), y0 + 19, "infravermelho", size=9.5, color=MUTE, anchor="middle", weight=600)

    # eixos e ticks
    s.axes(x0, y0, x1, y1, ylab="intensidade espectral (u.a.)", ylab_x=14)
    for l in (0, 500, 1000, 1500, 2000, 2500, 3000):
        if l == 0:
            continue
        s.line(X(l), y0, X(l), y0 - 4, color=INK, w=1)
    for l in (1000, 2000, 3000):
        s.text(X(l), y0 + 31, f"{l}", size=9.5, color=INK, anchor="middle")
    s.text(x1 - 4, y0 + 43, "comprimento de onda λ (nm)", size=10, color=INK, anchor="end")

    # previsão clássica (5000 K) — diverge para λ → 0
    pts = []
    l = 70.0
    while l <= 3000:
        v = rayleigh_jeans(l, 5000)
        pts.append((X(l), max(Y(v), y1 - 40)))
        l += 10
    s.path(pts, color=RED, w=1.8, dash="5 3", clip=clip)
    lexit = next(l for l in range(3000, 60, -10) if Y(rayleigh_jeans(l, 5000)) < y1 - 2)
    s.text(X(lexit) + 7, y1 + 10, "↑ → ∞ quando λ → 0", size=9.5, color=RED, weight=700, halo=True)
    s.text(X(1650), Y(rayleigh_jeans(1650, 5000)) - 8, "previsão clássica (5000 K)", size=9.5, color=RED, weight=600, halo=True)

    # curvas de Planck
    shades = {3000: "#B79BDB", 4000: "#8C62C3", 5000: PURPLE}
    for T in (3000, 4000, 5000):
        pts = [(X(l), Y(planck(l, T))) for l in range(60, 3001, 15)]
        s.path(pts, color=shades[T], w=2.4)
        lp = 2.898e6 / T
        yp = Y(planck(lp, T))
        s.line(X(lp), yp, X(lp), y0, color=shades[T], w=1, dash="2 3")
        s.circle(X(lp), yp, 3, fill=shades[T])
    s.text(X(620), Y(planck(580, 5000)) - 7, "5000 K", size=10, color=PURPLE, weight=700, halo=True)
    s.text(X(790), Y(planck(724, 4000)) - 7, "4000 K", size=10, color="#7B4FB3", weight=700, halo=True)
    s.text(X(1060), Y(planck(966, 3000)) - 7, "3000 K", size=10, color="#8F70BC", weight=700, halo=True)
    # seta de deslocamento do pico
    s.save()
    return s


# =============================================================================
# 2. Efeito fotoelétrico — diagrama em três situações
# =============================================================================
def fig_photoelectric():
    W, Hh = 703, 236
    s = Svg("fotoeletrico", W, Hh, "Efeito fotoelétrico: luz abaixo do limiar, acima do limiar e acima do limiar com maior intensidade")
    pw = 226
    panels = [
        (10, "(a) f < f₀", "mesmo com luz muito intensa:", "nenhum elétron é emitido", False, 4, 26),
        (238, "(b) f > f₀", "elétrons emitidos com", "K_máx = hf − Φ", True, 2, 9),
        (466, "(c) f > f₀ e intensidade maior", "mais fótons por segundo → mais elétrons;", "K_máx não muda", True, 4, 9),
    ]
    for (px, title, l1, l2, emit, n, wl) in panels:
        s.rect(px, 6, pw, 224, fill="#FFFFFF", stroke=GRID, sw=1, rx=6)
        s.text(px + 12, 24, title, size=11.5, color=BLUE, weight=700)
        s.rect(px + 12, 152, pw - 24, 40, fill=GRAY_L, stroke=GRAY, sw=1.2)
        s.text(px + 20, 166, "metal (função trabalho Φ)", size=9.5, color=MUTE, weight=600)
        for k in range(7):
            s.circle(px + 28 + k * 28, 180, 3, fill=PURPLE, op=0.6)
        s.text(px + pw - 16, 166, "e⁻ no metal", size=8.5, color=PURPLE, anchor="end")
        sp = 28
        for i in range(n):
            top_x = px + 26 + i * sp
            bot_x = top_x + 28
            s.wavy(top_x, 44, bot_x, 150, amp=3.0, wl=wl, color=BLUE, w=1.7)
            if i == 0:
                s.text(top_x - 4, 40, "hf", size=10.5, color=BLUE, weight=700, anchor="end", halo=True)
            if emit:
                s.line(bot_x, 150, bot_x + 34, 96, color=ORANGE, w=2.2, arrow=True)
                s.circle(bot_x + 36, 93, 4.2, fill=PURPLE)
                if i == n - 1:
                    s.text(bot_x + 44, 94, "e⁻", size=10, color=PURPLE, weight=700, halo=True)
                    s.text(bot_x + 40, 112, "K", size=10.5, color=ORANGE_D, weight=700, halo=True)
        if not emit:
            s.lines(px + pw - 12, 62, ["hf < Φ", "(fótons sem", "energia para", "arrancar elétron)"], size=9.5, lh=12, color=RED, anchor="end", weight=700)
        else:
            s.text(px + pw - 12, 62, "hf > Φ", size=10.5, color=GREEN_D, weight=700, anchor="end")
        s.text(px + pw / 2, 208, l1, size=9.5, color=INK, anchor="middle")
        s.text(px + pw / 2, 221, l2, size=9.5, color=ORANGE_D if emit else RED, anchor="middle", weight=700)
    s.save()
    return s


# =============================================================================
# 3. Gráficos fotoelétricos
# =============================================================================
def fig_photographs():
    W, Hh = 703, 252
    s = Svg("fotografs", W, Hh, "Gráficos do efeito fotoelétrico: K máximo versus frequência, corrente versus intensidade e corrente versus tensão")

    # (a) K_max x f
    ox, oy = 50, 128
    fx = lambda f: ox + f * 14.0
    ky = lambda k: oy - k * 22.0
    s.text(8, 16, "(a) K_máx × f", size=11.5, color=PURPLE, weight=700)
    s.axes(ox, oy, 262, 26, ylab="K_máx (eV)", ylab_x=14)
    s.line(ox, oy, ox, ky(-4.7), color=INK, w=1.3)
    s.text(262, oy + 26, "f (10¹⁴ Hz)", size=10, anchor="end")
    for f in (4, 8, 12):
        s.line(fx(f), oy - 3, fx(f), oy + 3, color=INK, w=1)
        s.text(fx(f), oy + 14, f"{f}", size=9, color=MUTE, anchor="middle")
    for k in (-4, -2, 2, 4):
        s.line(ox - 3, ky(k), ox + 3, ky(k), color=INK, w=1)
        s.text(ox - 6, ky(k) + 3, "−" * (k < 0) + f"{abs(k)}", size=9, color=MUTE, anchor="end")
    h = 0.4136
    for phi, col in ((2.0, PURPLE), (4.1, ORANGE_D)):
        f0 = phi / h
        fmax = 13.8
        s.line(fx(f0), ky(0), fx(fmax), ky(h * (fmax - f0)), color=col, w=2.3)
        s.line(fx(0), ky(-phi), fx(f0), ky(0), color=col, w=1.4, dash="3 3")
        s.circle(fx(f0), ky(0), 3.2, fill=col)
        s.circle(ox, ky(-phi), 3.2, fill=col, stroke="#fff", sw=1)
        s.text(ox + 7, ky(-phi) + 4, f"−Φ = −{phi:.1f} eV", size=9, color=col, weight=600, halo=True)
    s.text(fx(4.84) - 4, ky(0) - 8, "f₀(A)", size=9, color=PURPLE, weight=700, anchor="middle")
    s.text(fx(9.9) + 4, ky(0) - 8, "f₀(B)", size=9, color=ORANGE_D, weight=700, anchor="middle")
    s.text(fx(0.6), ky(3.9), "A: Φ = 2,0 eV (λ₀ ≈ 620 nm)", size=9, color=PURPLE, weight=600)
    s.text(fx(0.6), ky(3.9) + 11, "B: Φ = 4,1 eV (λ₀ ≈ 300 nm)", size=9, color=ORANGE_D, weight=600)
    s.text(fx(8.6), ky(-2.2), "retas paralelas:", size=9.5, color=INK, halo=True)
    s.text(fx(8.6), ky(-2.2) + 11, "inclinação = h (igual", size=9.5, color=INK, weight=700, halo=True)
    s.text(fx(8.6), ky(-2.2) + 22, "para todos os metais)", size=9.5, color=INK, weight=700, halo=True)

    # (b) corrente x intensidade
    ox2, oy2 = 320, 128
    s.text(296, 16, "(b) corrente × intensidade", size=11.5, color=BLUE, weight=700)
    s.axes(ox2, oy2, 462, 26, xlab="intensidade da luz", ylab="corrente fotoelétrica", ylab_x=ox2 - 14)
    s.line(ox2, oy2, ox2 + 126, oy2 - 92, color=BLUE, w=2.4)
    s.text(ox2 + 8, oy2 - 100, "f > f₀:", size=9.5, color=BLUE, weight=700)
    s.text(ox2 + 8, oy2 - 88, "corrente ∝ intensidade", size=9.5, color=BLUE)
    s.line(ox2, oy2 - 1, ox2 + 136, oy2 - 1, color=RED, w=2.6)
    s.text(ox2 + 138, oy2 - 24, "f < f₀: corrente nula", size=9.5, color=RED, weight=700, anchor="end", halo=True)
    s.text(ox2 + 138, oy2 - 12, "para qualquer intensidade", size=9.5, color=RED, anchor="end", halo=True)
    s.text(ox2 + 4, oy2 + 46, "f fixa; tensão suficiente para coletar", size=9, color=MUTE)
    s.text(ox2 + 4, oy2 + 57, "todos os fotoelétrons emitidos", size=9, color=MUTE)

    # (c) I x V
    ox3, oy3 = 580, 150
    s.text(512, 16, "(c) corrente × tensão (f fixa)", size=11.5, color=ORANGE_D, weight=700)
    s.axes(ox3, oy3, 696, 26, ylab="corrente", ylab_x=ox3 - 16)
    s.line(532, oy3, ox3, oy3, color=INK, w=1.3)
    s.text(696, oy3 + 26, "tensão V", size=10, anchor="end")
    vc = 44.0

    def curve(isat, rise):
        pts = []
        for i in range(0, 121):
            v = -vc + i * 1.9
            t = min(max((v + vc) / rise, 0), 1)
            pts.append((ox3 + v, oy3 - isat * t * t * (3 - 2 * t)))
        return pts

    s.path(curve(62, 80), color=ORANGE, w=2.2)
    s.path(curve(104, 80), color=ORANGE_D, w=2.2)
    s.line(ox3 - vc, oy3 - 112, ox3 - vc, oy3 + 8, color=GRAY, w=1, dash="3 3")
    s.text(ox3 - vc, oy3 + 20, "−V_c", size=10, color=INK, anchor="middle", weight=700)
    s.text(ox3 + 112, oy3 - 112, "intensidade maior", size=9.5, color=ORANGE_D, anchor="end", weight=600)
    s.text(ox3 + 112, oy3 - 70, "intensidade menor", size=9.5, color=ORANGE, anchor="end", weight=600)
    s.text(ox3 - vc - 8, oy3 + 42, "mesmo V_c nas duas curvas:", size=9.5, color=INK, weight=700)
    s.text(ox3 - vc - 8, oy3 + 54, "K_máx = e·V_c não depende", size=9.5, color=INK)
    s.text(ox3 - vc - 8, oy3 + 66, "da intensidade", size=9.5, color=INK)
    s.save()
    return s


# =============================================================================
# 4. Modelo de Bohr — níveis do hidrogênio (escala de energia proporcional)
# =============================================================================
def fig_bohr():
    W, Hh = 440, 386
    s = Svg("bohr", W, Hh, "Níveis de energia do hidrogênio com excitação, emissão, absorção e ionização")
    e0y = 58
    sc = 300 / 13.6
    Y = lambda e: e0y - e * sc  # e em eV negativo -> mais abaixo
    xL, xR = 54, 292
    # contínuo
    s.rect(xL - 10, 8, xR - xL + 20, e0y - 8, fill=PURPLE_L)
    s.text(xL, 24, "contínuo: elétron livre (E ≥ 0)", size=9.5, color=PURPLE, weight=700)
    # eixo
    s.line(30, Y(-13.6) + 14, 30, 10, color=INK, w=1.3, arrow=True)
    s.text(18, 190, "energia (eV)", size=10, anchor="middle", rot=-90)
    levels = [(1, -13.6), (2, -3.40), (3, -1.51), (4, -0.85), (5, -0.54)]
    for n, e in levels:
        y = Y(e)
        s.line(xL, y, xR, y, color=INK, w=2.2)
        s.line(27, y, 33, y, color=INK, w=1)
    s.line(xL, e0y, xR, e0y, color=PURPLE, w=2, dash="4 3")
    # rótulos dos níveis, com espaçamento para evitar sobreposição
    lab = {1: Y(-13.6), 2: Y(-3.40), 3: 88, 4: 75, 5: 62}
    for n, e in levels:
        ytrue = Y(e)
        ylab = lab[n] + 4
        if n >= 3:
            s.line(xR + 2, ytrue, xR + 12, lab[n], color=GRID, w=0.8)
        s.text(xR + 15, ylab, f"n = {n}", size=10, weight=700)
        s.text(xR + 52, ylab, "−" + f"{abs(e):.2f}".replace(".", ",") + " eV", size=10, color=MUTE)
    s.text(xR + 15, e0y - 12, "n → ∞", size=10, weight=700, color=PURPLE)
    s.text(xR + 52, e0y - 12, "0 eV", size=10, color=PURPLE)
    s.text(xR - 8, Y(-13.6) + 15, "estado fundamental", size=9.5, color=MUTE, anchor="end", weight=600)

    # absorção 1→2 (azul)
    s.line(84, Y(-13.6), 84, Y(-3.4) + 2, color=BLUE, w=2.4, arrow=True)
    s.text(76, 235, "absorção 1→2: 10,2 eV", size=9.5, color=BLUE, weight=700, rot=-90, anchor="middle")
    # emissão 2→1 (laranja)
    s.line(118, Y(-3.4), 118, Y(-13.6) - 2, color=ORANGE, w=2.4, arrow=True)
    s.text(133, 238, "emissão 2→1: 10,2 eV (UV, 122 nm)", size=9.5, color=ORANGE_D, weight=700, rot=-90, anchor="middle")
    # emissões 3→2 e 4→2
    s.line(172, Y(-1.51), 172, Y(-3.4) - 2, color=ORANGE, w=2.4, arrow=True)
    s.line(212, Y(-0.85), 212, Y(-3.4) - 2, color=ORANGE, w=2.4, arrow=True)
    s.text(146, Y(-3.4) + 22, "↓ 3→2: 1,89 eV · 656 nm", size=9.5, color=ORANGE_D, weight=700)
    s.text(146, Y(-3.4) + 36, "↓ 4→2: 2,55 eV · 486 nm", size=9.5, color=ORANGE_D, weight=700)
    # ionização (roxo tracejado)
    s.line(276, Y(-13.6), 276, 30, color=PURPLE, w=2.4, dash="6 3", arrow=True)
    s.circle(276, 24, 4.5, fill=PURPLE)
    s.text(266, 300, "ionização: E ≥ 13,6 eV", size=9.5, color=PURPLE, weight=700, rot=-90, anchor="middle")
    s.text(258, 27, "e⁻", size=10, color=PURPLE, weight=700)
    s.save()
    return s


# =============================================================================
# 5. Espectros: contínuo, emissão e absorção (hidrogênio, série de Balmer)
# =============================================================================
def fig_spectra():
    W, Hh = 703, 176
    s = Svg("espectros", W, Hh, "Espectro contínuo, de emissão e de absorção do hidrogênio no visível")
    x0, x1 = 92, 690
    X = lambda l: x0 + (l - 400) / 300 * (x1 - x0)
    gid = s.uid("g")
    stops = "".join(f'<stop offset="{(w - 400) / 300:.3f}" stop-color="{wl_to_rgb(w)}"/>' for w in range(400, 701, 10))
    s.defs.append(f'<linearGradient id="{gid}" x1="0" x2="1">{stops}</linearGradient>')
    lines = [(410.2, "6→2"), (434.0, "5→2"), (486.1, "4→2"), (656.3, "3→2")]
    rows = [("contínuo", 20), ("emissão", 62), ("absorção", 104)]
    for nm, y in rows:
        s.text(x0 - 10, y + 19, nm, size=11, anchor="end", weight=700, color=ORANGE_D if nm == "emissão" else (BLUE if nm == "absorção" else INK))
    # contínuo
    s.rect(x0, 20, x1 - x0, 28, fill=f"url(#{gid})")
    # emissão
    s.rect(x0, 62, x1 - x0, 28, fill="#0B0F16")
    for l, lb in lines:
        s.rect(X(l) - 1.6, 62, 3.2, 28, fill=wl_to_rgb(l) if l != 410.2 else "#8A5BFF")
    # absorção
    s.rect(x0, 104, x1 - x0, 28, fill=f"url(#{gid})")
    for l, lb in lines:
        s.rect(X(l) - 1.6, 104, 3.2, 28, fill="#0B0F16")
        s.text(X(l), 100, lb, size=9, color=MUTE, anchor="middle", weight=600)
    # eixo
    s.line(x0, 138, x1, 138, color=INK, w=1.2)
    for l in range(400, 701, 50):
        s.line(X(l), 138, X(l), 143, color=INK, w=1)
        s.text(X(l), 154, str(l), size=9.5, color=MUTE, anchor="middle")
    s.text(x1, 170, "comprimento de onda λ (nm)", size=10, anchor="end")
    s.text(x0, 170, "linhas = transições n → 2 (série de Balmer)", size=9.5, color=MUTE)
    s.save()
    return s


# =============================================================================
# 6. Dualidade: elétrons um a um formando interferência
# =============================================================================
def fig_doubleslit():
    W, Hh = 703, 192
    s = Svg("duplafenda", W, Hh, "Elétrons detectados um a um formam gradualmente um padrão de interferência")
    # esquema à esquerda
    s.text(8, 16, "experimento (esquema)", size=11, color=PURPLE, weight=700)
    s.rect(14, 84, 28, 26, fill=GRAY_L, stroke=GRAY, sw=1.2, rx=3)
    s.text(28, 125, "canhão de", size=9, color=MUTE, anchor="middle")
    s.text(28, 136, "elétrons", size=9, color=MUTE, anchor="middle")
    s.line(42, 97, 112, 97, color=PURPLE, w=1.5, arrow=True)
    # barreira com duas fendas
    bx = 118
    for (ya, yb) in ((34, 86), (92, 102), (108, 160)):
        s.rect(bx, ya, 7, yb - ya, fill=GRAY)
    s.text(bx + 3, 176, "duas fendas", size=9, color=MUTE, anchor="middle")
    # anteparo
    s.rect(236, 34, 6, 126, fill=GRAY)
    s.text(239, 176, "detector", size=9, color=MUTE, anchor="middle")
    for r in (30, 52, 74):
        s.path([(bx + 7 + r * math.cos(t), 91 + r * math.sin(t)) for t in [i * math.pi / 40 - math.pi / 2 for i in range(41)]], color=PURPLE, w=0.9, op=0.35)
    # painéis de detecção
    def sample(n, seed, w=140, d=17.0, sg=40.0):
        rnd = random.Random(seed)
        pts = []
        while len(pts) < n:
            x = rnd.uniform(-w / 2, w / 2)
            if rnd.random() < math.cos(math.pi * x / d) ** 2 * math.exp(-((x / sg) ** 2)):
                pts.append(x)
        return pts, rnd

    px = [270, 417, 564]
    for (n, seed, pxi) in ((30, 3, px[0]), (500, 5, px[1]), (6000, 9, px[2])):
        s.rect(pxi, 22, 130, 138, fill="#10131A", rx=3)
        pts, rnd = sample(n, seed, w=126)
        for x in pts:
            y = 22 + 4 + rnd.random() * 130
            s.raw(f'<rect x="{pxi + 65 + x:.1f}" y="{y:.1f}" width="1.5" height="1.5" fill="#E9DEFF"/>')
        s.text(pxi + 65, 176, f"{n:,} elétrons".replace(",", " ") if n >= 1000 else f"{n} elétrons", size=10, anchor="middle", weight=700, color=PURPLE)
    s.text(270, 16, "detecções acumuladas na tela", size=11, color=PURPLE, weight=700)
    s.text(693, 16, "cada ponto = 1 elétron detectado", size=9.5, color=MUTE, anchor="end")
    s.save()
    return s


# =============================================================================
# 7. Probabilidade: clássico × nuvem de probabilidade; incerteza
# =============================================================================
def fig_probability():
    W, Hh = 703, 200
    s = Svg("probabilidade", W, Hh, "Descrição clássica (trajetória) comparada com nuvem de probabilidade do hidrogênio")
    # (A) clássico
    s.rect(6, 6, 200, 188, fill="#fff", stroke=GRID, rx=6)
    s.text(16, 24, "Clássico: bola", size=11.5, color=GRAY, weight=700)
    s.text(16, 37, "posição e velocidade definidas", size=9.5, color=MUTE)
    pts = []
    for i in range(0, 61):
        t = i / 60
        pts.append((26 + t * 160, 168 - 4 * 100 * t * (1 - t) * 0.9))
    s.path(pts, color=GRAY, w=1.2, dash="3 3")
    for i in (0, 10, 20, 30, 40, 50, 60):
        x, y = pts[i]
        s.circle(x, y, 4.2, fill=GRAY)
    x, y = pts[30]
    s.line(x, y, x + 26, y, color=ORANGE, w=2, arrow=True)
    s.text(x + 4, y - 9, "v", size=11, color=ORANGE_D, weight=700, italic=True)
    s.text(106, 188, "trajetória bem determinada", size=9.5, color=MUTE, anchor="middle")

    # (B) nuvem
    s.rect(214, 6, 250, 188, fill="#fff", stroke=GRID, rx=6)
    s.text(224, 24, "Quântico: H, estado fundamental", size=11.5, color=PURPLE, weight=700)
    s.text(224, 37, "cada ponto = uma detecção do elétron", size=9.5, color=MUTE)
    cx, cy, sc = 339, 118, 34.0
    clip = s.clip(220, 44, 238, 142)
    rnd = random.Random(11)
    for _ in range(1500):
        r = sum(rnd.expovariate(1 / 0.5) for _ in range(3))  # Gamma(3, a0/2)
        ct = rnd.uniform(-1, 1)
        ph = rnd.uniform(0, 2 * math.pi)
        st = math.sqrt(1 - ct * ct)
        x, y = r * st * math.cos(ph), r * st * math.sin(ph)
        px_, py_ = cx + x * sc, cy + y * sc
        if 222 < px_ < 456 and 46 < py_ < 184:
            s.raw(f'<rect x="{px_:.1f}" y="{py_:.1f}" width="1.6" height="1.6" fill="{PURPLE}" opacity="0.55"/>')
    s.circle(cx, cy, 3.2, fill=RED)
    s.text(cx + 6, cy + 14, "próton", size=9, color=RED, weight=600, halo=True)
    s.text(339, 188, "sem órbita: só probabilidades", size=9.5, color=MUTE, anchor="middle", halo=True)

    # (C) densidade radial
    s.rect(472, 6, 225, 188, fill="#fff", stroke=GRID, rx=6)
    s.text(482, 24, "Probabilidade radial P(r)", size=11.5, color=PURPLE, weight=700)
    ox, oy = 502, 160
    s.axes(ox, oy, 684, 44, xlab="distância ao núcleo r (em a₀)", ylab="P(r)", ylab_x=ox - 12, xlab_dy=26)
    pts = []
    for i in range(0, 161):
        r = i * 5.0 / 160
        pts.append((ox + r * 33, oy - 4 * r * r * math.exp(-2 * r) / 0.5413 * 82))
    s.path(pts, color=PURPLE, w=2.4)
    for r in (1, 2, 3, 4):
        s.line(ox + r * 33, oy, ox + r * 33, oy + 4, color=INK)
        s.text(ox + r * 33, oy + 14, str(r), size=9, anchor="middle", color=MUTE)
    s.line(ox + 33, oy, ox + 33, oy - 82, color=PURPLE, w=1, dash="3 3")
    s.text(ox + 40, oy - 88, "máximo em r = a₀ ≈ 0,053 nm", size=9.5, color=PURPLE, weight=700)
    s.text(ox + 40, oy - 76, "(mais provável, não é “a órbita”)", size=9, color=MUTE)
    s.save()
    return s


def fig_uncertainty():
    W, Hh = 340, 214
    s = Svg("incerteza", W, Hh, "Duas distribuições posição-momento ilustrando Δx Δp ≥ ħ/2")
    rows = [(4, 0.5, "estado concentrado: Δx pequeno ⇒ Δp grande"), (108, 1.5, "estado espalhado: Δx grande ⇒ Δp pequeno")]
    for (y0, sx, title) in rows:
        sp = 0.5 / sx
        s.text(8, y0 + 12, title, size=10, weight=700, color=PURPLE)
        for k, (ox, sg, lab) in enumerate(((22, sx, "posição x"), (186, sp, "momento p"))):
            base = y0 + 78
            s.line(ox, base, ox + 140, base, color=INK, w=1.2)
            s.text(ox + 70, base + 12, lab, size=9.5, color=MUTE, anchor="middle")
            pts = []
            for i in range(0, 141):
                x = (i - 70) / 70 * 4
                y = math.exp(-x * x / (2 * sg * sg)) / (sg * math.sqrt(2 * math.pi))
                pts.append((ox + i, base - y * 44))
            s.path(pts, color=PURPLE if k == 0 else ORANGE, w=2.1)
            s.path(pts + [(ox + 140, base), (ox, base)], color="none", fill=(PURPLE_L if k == 0 else ORANGE_L), w=0, op=0.7)
            # largura
            w2 = sg / 4 * 70
            s.line(ox + 70 - w2, base - 8, ox + 70 + w2, base - 8, color=INK, w=1.1, start=True, arrow=True)
            s.text(ox + 70, base - 12, "Δx" if k == 0 else "Δp", size=9.5, anchor="middle", weight=700, halo=True)
    s.save()
    return s


# =============================================================================
# 8. Simultaneidade — trem e plataforma
# =============================================================================
def wagon(s, xc, y, w=120, h=34, label_ab=True, col=CYAN, fill=CYAN_L):
    s.rect(xc - w / 2, y, w, h, fill=fill, stroke=col, sw=1.6, rx=3)
    s.circle(xc - w / 4, y + h + 4, 4, fill=GRAY)
    s.circle(xc + w / 4, y + h + 4, 4, fill=GRAY)
    s.circle(xc, y + h / 2 + 3, 3.6, fill=BLUE)  # lâmpada no centro
    if label_ab:
        s.text(xc - w / 2 + 6, y + 11, "A", size=10.5, color=CYAN_D, weight=700)
        s.text(xc + w / 2 - 6, y + 11, "B", size=10.5, color=CYAN_D, weight=700, anchor="end")


def fig_simultaneity():
    W, Hh = 703, 262
    s = Svg("simultaneidade", W, Hh, "Simultaneidade relativa: lâmpada no centro de um vagão vista do trem e da plataforma")
    # Painel esquerdo: referencial do trem
    s.rect(4, 4, 326, 254, fill="#fff", stroke=GRID, rx=6)
    s.text(14, 22, "Referencial do TREM (vagão em repouso)", size=11.5, color=CYAN_D, weight=700)
    xc = 167
    ys = [48, 140]
    s.text(14, 40, "① emissão: lâmpada no centro", size=9.5, color=MUTE)
    wagon(s, xc, 50)
    s.circle(xc, 52 + 20, 7, fill="none", stroke=BLUE, sw=1)
    s.text(14, 134, "② chegada: os dois pulsos atingem A e B no mesmo instante", size=9.5, color=MUTE)
    wagon(s, xc, 146)
    s.line(xc - 3, 146 + 20, xc - 55, 146 + 20, color=BLUE, w=2, arrow=True)
    s.line(xc + 3, 146 + 20, xc + 55, 146 + 20, color=BLUE, w=2, arrow=True)
    s.text(xc, 214, "t_A = t_B", size=13, color=CYAN_D, anchor="middle", weight=700)
    s.text(xc, 228, "(distâncias iguais, c igual nos dois sentidos)", size=9.5, color=MUTE, anchor="middle")
    s.text(167, 248, "eventos A e B simultâneos neste referencial", size=10, color=INK, anchor="middle", weight=600)

    # Painel direito: referencial da plataforma
    s.rect(338, 4, 361, 254, fill="#fff", stroke=GRID, rx=6)
    s.text(348, 22, "Referencial da PLATAFORMA (vagão a 0,5c →)", size=11.5, color=CYAN_D, weight=700)
    ox = 505  # ponto da plataforma onde a luz foi emitida
    L = 120
    rows = [
        (36, 0.0, "t = 0: emissão (ponto fixo na plataforma)", None),
        (96, 0.3333, "t₁: pulso da esquerda atinge A (traseira)", "A"),
        (156, 1.0, "t₂ > t₁: pulso da direita atinge B (frente)", "B"),
    ]
    for (y, t, lab, hit) in rows:
        s.text(348, y, lab, size=9.5, color=MUTE)
        xc2 = ox + 0.5 * t * L
        wagon(s, xc2, y + 6)
        yl = y + 26
        # pulsos (c = 1 -> posição = ± t*L)
        if t == 0:
            s.circle(ox, yl, 6.5, fill="none", stroke=BLUE, sw=1)
        else:
            xl, xr = ox - t * L, ox + t * L
            s.line(ox - 2, yl, xl + 2, yl, color=BLUE, w=1.8, arrow=True) if xl > 352 else None
            s.line(ox + 2, yl, xr - 2, yl, color=BLUE, w=1.8, arrow=True)
            if hit == "A":
                s.circle(xl, yl, 6.5, fill="none", stroke=RED, sw=1.6)
            if hit == "B":
                s.circle(xr, yl, 6.5, fill="none", stroke=RED, sw=1.6)
        s.line(ox, y + 2, ox, y + 50, color=GRAY, w=1, dash="2 3")
    s.text(350, 253, "linha tracejada: ponto da plataforma onde a luz foi emitida", size=9, color=MUTE)
    s.text(560, 222, "t_A < t_B", size=13, color=CYAN_D, weight=700, anchor="middle")
    s.text(560, 236, "A vem ao encontro da luz; B foge dela", size=9.5, color=MUTE, anchor="middle")
    s.save()
    return s


# =============================================================================
# 9. Dilatação do tempo e contração do comprimento
# =============================================================================
def fig_ship():
    W, Hh = 703, 232
    s = Svg("nave", W, Hh, "Nave a 0,8c vista no referencial da nave e no referencial Terra–estrela")
    k = 50.0  # px por ano-luz (distância no referencial Terra-estrela: 8 al -> 400 px)

    def ship(x, y, w, color=CYAN, fill=CYAN_L):
        s.path([(x, y), (x + w - 12, y), (x + w, y + 11), (x + w - 12, y + 22), (x, y + 22)], color=color, w=1.8, fill=fill, close=True)

    def body(x, y, name):
        s.circle(x, y, 9, fill=BLUE, stroke="#fff", sw=1)
        s.text(x, y + 22, name, size=9.5, anchor="middle", weight=700, color=MUTE)

    # referencial Terra–estrela
    s.rect(4, 120, 695, 108, fill="#fff", stroke=GRID, rx=6)
    s.text(14, 138, "Referencial TERRA–ESTRELA (S): Terra e estrela em repouso, nave a 0,8c", size=11.5, color=CYAN_D, weight=700)
    xT, xE = 62, 62 + 8 * k
    body(xT, 174, "Terra")
    body(xE, 174, "estrela")
    s.line(xT + 12, 174, xE - 12, 174, color=GRAY, w=1.2, dash="3 3", start=True, arrow=True)
    s.text((xT + xE) / 2, 166, "distância medida em S: 8 anos-luz", size=10, anchor="middle", weight=600, halo=True)
    ship(xT + 22, 182, 60)
    s.line(xT + 86, 193, xT + 120, 193, color=CYAN, w=2, arrow=True)
    s.text(xT + 123, 197, "v = 0,8c", size=9.5, color=CYAN_D, weight=700)
    s.text(xT + 22, 218, "L = 60 m", size=10, color=CYAN_D, weight=700)
    s.text(xE + 24, 170, "Δt = 10 anos", size=12, color=CYAN_D, weight=700)
    s.text(xE + 24, 184, "(relógios da Terra e", size=9.5, color=MUTE)
    s.text(xE + 24, 196, "da estrela, sincronizados)", size=9.5, color=MUTE)
    s.text(xE + 24, 213, "nave contraída: L = L₀/γ", size=9.5, color=INK)

    # referencial da nave
    s.rect(4, 4, 695, 108, fill="#fff", stroke=GRID, rx=6)
    s.text(14, 22, "Referencial da NAVE (S′): nave em repouso; Terra e estrela passam a 0,8c", size=11.5, color=CYAN_D, weight=700)
    ship(262, 50, 100)
    s.text(312, 92, "L₀ = 100 m", size=10, color=CYAN_D, weight=700, anchor="middle")
    s.text(312, 106, "(comprimento próprio)", size=9.5, color=MUTE, anchor="middle")
    yT = 61
    xT2, xE2 = 430, 430 + 4.8 * k
    s.circle(xT2, yT, 9, fill=BLUE, stroke="#fff", sw=1)
    s.text(xT2, yT + 24, "Terra", size=9.5, anchor="middle", weight=700, color=MUTE)
    s.circle(xE2, yT, 9, fill=BLUE, stroke="#fff", sw=1)
    s.text(xE2, yT + 24, "estrela", size=9.5, anchor="middle", weight=700, color=MUTE)
    s.line(xT2 + 12, yT, xE2 - 12, yT, color=GRAY, w=1.2, dash="3 3", start=True, arrow=True)
    s.text((xT2 + xE2) / 2, yT - 9, "distância medida em S′: 4,8 anos-luz", size=10, anchor="middle", weight=600, halo=True)
    s.line(xT2 - 14, 40, xT2 - 48, 40, color=GRAY, w=1.6, arrow=True)
    s.text(xT2 - 50, 36, "Terra e estrela se movem", size=9, color=MUTE, anchor="end")
    s.text(14, 50, "Δτ = 6 anos", size=12, color=CYAN_D, weight=700)
    s.text(14, 64, "(tempo próprio: o relógio", size=9.5, color=MUTE)
    s.text(14, 76, "da nave está presente na", size=9.5, color=MUTE)
    s.text(14, 88, "partida e na chegada)", size=9.5, color=MUTE)
    s.text(690, 100, "escalas de comprimento: nave e distâncias independentes", size=8.5, color=MUTE, anchor="end")
    s.save()
    return s


# =============================================================================
# 10. Lente gravitacional e curvatura (grade)
# =============================================================================
def fig_lens():
    W, Hh = 703, 232
    s = Svg("lente", W, Hh, "Lente gravitacional: luz de fonte distante desviada por objeto massivo; grade espacial deformada")
    s.rect(4, 4, 470, 224, fill="#fff", stroke=GRID, rx=6)
    s.text(14, 22, "Lente gravitacional (esquema conceitual)", size=11.5, color=CYAN_D, weight=700)
    ox, oy = 52, 124
    lx = 256
    sx, sy = 424, 124
    # observador
    s.circle(ox, oy, 7, fill=GRAY)
    s.text(ox, oy + 24, "observador", size=9.5, anchor="middle", weight=600, color=MUTE)
    # lente (massa)
    gid = s.uid("g")
    s.defs.append(f'<radialGradient id="{gid}"><stop offset="0" stop-color="#7C4DC4"/><stop offset="1" stop-color="#C8B3E8"/></radialGradient>')
    s.circle(lx, oy, 17, fill=f"url(#{gid})", stroke=PURPLE, sw=1.2)
    s.text(lx, oy + 68, "objeto massivo (lente)", size=9.5, anchor="middle", weight=600, color=PURPLE)
    # fonte
    s.circle(sx, sy, 7, fill=ORANGE)
    s.text(sx, sy + 22, "fonte real", size=9.5, anchor="middle", weight=600, color=ORANGE_D)
    for sgn in (-1, 1):
        by = oy + sgn * 40
        s.path([(sx - 6, sy + sgn * 3), (lx, by)], color=BLUE, w=1.8)
        s.path([(lx, by), (ox + 6, oy + sgn * 1)], color=BLUE, w=1.8, arrow=True)
        # prolongamento aparente
        dx, dy = (lx - ox - 6), (by - oy)
        k = (sx - ox) / dx
        ix, iy = ox + k * dx, oy + k * dy
        s.line(lx, by, ix, iy, color=GRAY, w=1.1, dash="3 3")
        s.circle(ix, iy, 6, fill="none", stroke=ORANGE, sw=1.6)
    s.text(sx, oy - 91, "imagem aparente", size=9.5, color=ORANGE_D, weight=700, anchor="middle")
    s.text(sx, oy + 100, "imagem aparente", size=9.5, color=ORANGE_D, weight=700, anchor="middle")

    # grade deformada
    gx0, gy0, gw, gh = 486, 4, 213, 210
    s.rect(gx0, gy0, gw, gh + 14, fill="#fff", stroke=GRID, rx=6)
    s.text(gx0 + 10, 22, "Massa deforma a geometria", size=11, color=CYAN_D, weight=700)
    cx, cy = gx0 + gw / 2, gy0 + 122
    clip = s.clip(gx0 + 6, gy0 + 30, gw - 12, gh - 40)

    def warp(x, y):
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy
        f = 1 - 0.45 * math.exp(-r2 / (2 * 38**2))
        return cx + dx * f, cy + dy * f

    n = 11
    xs = [gx0 + 14 + i * (gw - 28) / (n - 1) for i in range(n)]
    ys = [gy0 + 36 + j * (gh - 56) / (n - 1) for j in range(n)]
    for xv in xs:
        s.path([warp(xv, y) for y in [ys[0] + t * (ys[-1] - ys[0]) / 40 for t in range(41)]], color=CYAN, w=1.1, clip=clip, op=0.8)
    for yv in ys:
        s.path([warp(x, yv) for x in [xs[0] + t * (xs[-1] - xs[0]) / 40 for t in range(41)]], color=CYAN, w=1.1, clip=clip, op=0.8)
    s.circle(cx, cy, 8, fill=f"url(#{gid})", stroke=PURPLE, sw=1)
    s.text(gx0 + gw / 2, gy0 + gh + 4, "(2D: só representa a curvatura espacial)", size=8.5, color=MUTE, anchor="middle")
    s.save()
    return s


# =============================================================================
# 11. Expansão do Universo
# =============================================================================
def fig_expansion():
    W, Hh = 703, 252
    s = Svg("expansao", W, Hh, "Galáxias em malha que se expande, alongamento do comprimento de onda e gráfico v versus d")
    frames = [(10, 1.0, "instante 1"), (152, 1.45, "instante 2 (depois)"), (294, 1.95, "instante 3 (depois)")]
    fw = 134
    sp0 = 14.0
    for (fx, a, name) in frames:
        s.rect(fx, 6, fw, 164, fill="#fff", stroke=GRID, rx=6)
        s.text(fx + fw / 2, 22, name, size=10.5, anchor="middle", weight=700, color=GREEN_D)
        cx, cy = fx + fw / 2, 96
        clip = s.clip(fx + 2, 30, fw - 4, 138)
        for i in range(-2, 3):
            for j in range(-2, 3):
                x, y = cx + i * sp0 * a, cy + j * sp0 * a
                hl = (i, j) in ((0, 0), (2, 0))
                s.circle(x, y, 3.6 if not hl else 4.4, fill=GREEN if not hl else ORANGE, op=0.9 if not hl else 1)
        d = 2 * sp0 * a
        s.line(cx + 4, cy - 10, cx + d - 4, cy - 10, color=ORANGE_D, w=1.3, start=True, arrow=True)
        s.text(cx + d / 2, cy - 14, "d", size=10, color=ORANGE_D, anchor="middle", weight=700, italic=True, halo=True)
        # onda esticada
        wl = 14 * a
        pts = [(fx + 8 + t, 188 + 9 * math.sin(2 * math.pi * t / wl)) for t in range(0, fw - 16 + 1, 1)]
        s.path(pts, color=BLUE, w=1.8)
        s.text(fx + fw / 2, 214, f"λ cresce ({'×1' if a == 1 else '×' + str(round(a, 2)).replace('.', ',')})", size=9.5, anchor="middle", color=BLUE, weight=700)
    s.text(10, 238, "mesma malha em instantes diferentes: as separações crescem; qualquer galáxia veria as outras se afastarem (sem centro).", size=9.5, color=MUTE)

    # gráfico v × d
    ox, oy = 470, 190
    s.text(446, 20, "Lei de Hubble–Lemaître (z pequeno)", size=11.5, color=GREEN_D, weight=700)
    s.axes(ox, oy, 692, 36, xlab="distância d (Mpc)", ylab="velocidade de recessão v (10³ km/s)", ylab_x=ox - 28, xlab_dy=28)
    rnd = random.Random(4)
    for d in (30, 60, 90, 130, 170, 210, 250, 290):
        v = 70 * d * (1 + rnd.uniform(-0.07, 0.07))
        s.circle(ox + d * 0.64, oy - v / 1000 * 6.4, 3.6, fill=GREEN)
    s.line(ox, oy, ox + 192, oy - 70 * 300 / 1000 * 6.4, color=GREEN_D, w=2)
    for d in (100, 200, 300):
        s.line(ox + d * 0.64, oy, ox + d * 0.64, oy + 4, color=INK)
        s.text(ox + d * 0.64, oy + 15, str(d), size=9, color=MUTE, anchor="middle")
    for v in (10, 20):
        s.line(ox, oy - v * 6.4, ox - 4, oy - v * 6.4, color=INK)
        s.text(ox - 7, oy - v * 6.4 + 3, str(v), size=9, color=MUTE, anchor="end")
    s.text(ox + 6, oy - 128, "inclinação = H₀ ≈ 70 km/s/Mpc", size=9.5, color=GREEN_D, weight=700)
    s.text(ox + 6, oy - 116, "(dados ilustrativos)", size=9, color=MUTE)
    s.save()
    return s


# =============================================================================
# 12. Evolução cósmica + espectro da CMB
# =============================================================================
def fig_cosmic_timeline():
    W, Hh = 703, 188
    s = Svg("evolucao", W, Hh, "Linha do tempo da evolução cósmica, do Universo primordial ao presente")
    cy = 92
    x0, x1 = 20, 683
    top, bot = [], []
    for i in range(0, 101):
        t = i / 100
        h = 4 + 44 * (t**0.75)
        top.append((x0 + t * (x1 - x0), cy - h))
        bot.append((x0 + t * (x1 - x0), cy + h))
    s.path(top + bot[::-1], color=GREEN, w=1.5, fill=GREEN_L, close=True)
    marks = [
        (0.015, "Universo primordial", ["muito quente e denso"], "start"),
        (0.20, "primeiros minutos", ["primeiros núcleos", "(H e He)"], "middle"),
        (0.40, "≈ 380 mil anos", ["átomos neutros: o Universo", "fica transparente → CMB"], "middle"),
        (0.66, "centenas de milhões de anos", ["primeiras estrelas e galáxias"], "middle"),
        (0.985, "hoje: ≈ 13,8 bilhões de anos", ["estruturas atuais"], "end"),
    ]
    for i, (t, a, bl, anc) in enumerate(marks):
        x = x0 + t * (x1 - x0)
        up = i % 2 == 0
        h = 4 + 44 * (t**0.75)
        s.circle(x, cy, 5, fill=GREEN_D, stroke="#fff", sw=1.5)
        tx = x - 4 if anc == "start" else x
        if up:
            s.line(x, cy - h - 2, x, 44, color=GRID, w=1)
            ty = 14
        else:
            s.line(x, cy + h + 2, x, 142, color=GRID, w=1)
            ty = 154
        s.text(tx, ty, a, size=10, color=GREEN_D, anchor=anc, weight=700)
        for j, b in enumerate(bl):
            s.text(tx, ty + 11.5 * (j + 1), b, size=9.5, color=MUTE, anchor=anc)
    xc = x0 + 0.40 * (x1 - x0)
    for k in range(3):
        s.wavy(xc + 16, cy - 12 + k * 12, xc + 92, cy - 12 + k * 12, amp=2.2, wl=9, color=BLUE, w=1.3)
    s.text(xc + 98, cy + 4, "luz livre (CMB)", size=9, color=BLUE, weight=700)
    s.text(683, 184, "sem escala; é o próprio espaço que se expande (não é uma explosão em um ponto)", size=9, color=MUTE, anchor="end")
    s.save()
    return s


def fig_cmb():
    W, Hh = 300, 176
    s = Svg("cmb", W, Hh, "Espectro de corpo negro de 2,725 K da radiação cósmica de fundo")
    ox, oy = 44, 132
    lm = 5.0
    X = lambda l: ox + l / lm * 236
    T = 2.725

    def B(l_mm):
        lam = l_mm * 1e-3
        x = H * C / (lam * KB * T)
        return 2 * H * C**2 / lam**5 / (math.exp(x) - 1) if x < 600 else 0

    bmax = B(2.898 / T)
    s.axes(ox, oy, 284, 22, xlab="comprimento de onda λ (mm)", ylab="intensidade (u.a.)", ylab_x=14, xlab_dy=28)
    pts = [(X(l / 100), oy - B(l / 100) / bmax * 92) for l in range(8, 501, 4)]
    s.path(pts, color=GREEN_D, w=2.5)
    pk = 2.898 / T
    s.line(X(pk), oy - 92, X(pk), oy, color=GRID, w=1, dash="3 3")
    s.circle(X(pk), oy - 92, 3.5, fill=GREEN_D)
    s.text(X(pk) + 14, oy - 86, "pico ≈ 1 mm", size=9.5, color=GREEN_D, weight=700)
    s.text(X(pk) + 14, oy - 74, "(micro-ondas)", size=9, color=MUTE)
    s.text(X(1.5) + 60, oy - 52, "T = 2,725 K", size=10.5, color=INK, weight=700)
    for l in (1, 2, 3, 4, 5):
        s.line(X(l), oy, X(l), oy + 3, color=INK)
        s.text(X(l), oy + 13, str(l), size=9, color=MUTE, anchor="middle")
    s.save()
    return s


# =============================================================================
# 13. Radioatividade: emissões e penetração
# =============================================================================
def fig_radiation():
    W, Hh = 703, 178
    s = Svg("radiacao", W, Hh, "Poder de penetração das radiações alfa, beta e gama")
    # fonte
    s.circle(46, 84, 17, fill=ORANGE_L, stroke=ORANGE, sw=1.5)
    s.text(46, 88, "☢", size=16, color=ORANGE_D, anchor="middle", weight=700)
    s.text(46, 118, "fonte", size=9.5, anchor="middle", color=MUTE, weight=600)
    s.text(46, 129, "radioativa", size=9.5, anchor="middle", color=MUTE, weight=600)
    # barreiras
    bx = {"papel": 270, "Al": 380, "Pb": 500}
    s.rect(bx["papel"], 20, 2.5, 128, fill=GRAY)
    s.rect(bx["Al"], 20, 9, 128, fill="#9AA4B2")
    s.rect(bx["Pb"], 20, 34, 128, fill="#5B6573")
    s.text(bx["papel"] + 1, 14, "papel", size=9.5, anchor="middle", color=INK, weight=700)
    s.text(bx["Al"] + 4, 14, "alumínio (mm)", size=9.5, anchor="middle", color=INK, weight=700)
    s.text(bx["Pb"] + 17, 14, "chumbo / concreto", size=9.5, anchor="middle", color=INK, weight=700)
    rows = [(46, "α", ORANGE_D, bx["papel"] - 2), (86, "β", ORANGE, bx["Al"] - 2), (126, "γ", BLUE, None)]
    for (y, nm, col, stop) in rows:
        s.text(88, y + 5, nm, size=16, color=col, weight=700, anchor="middle")
        if nm == "γ":
            s.wavy(104, y, bx["Pb"], y, amp=3, wl=10, color=col, w=1.7, arrow=False)
            s.wavy(bx["Pb"] + 34, y, 660, y, amp=1.3, wl=10, color=col, w=1.2, arrow=True)
            s.text(600, y - 12, "atenuada (menos intensa),", size=9.5, color=BLUE, weight=600, anchor="middle")
            s.text(600, y + 22, "não totalmente barrada", size=9.5, color=BLUE, weight=600, anchor="middle")
        else:
            s.line(104, y, stop, y, color=col, w=2.6)
            s.text(stop + 5, y + 5, "✕", size=13, color=RED, weight=700)
            msg = "α: barrada por papel" if nm == "α" else "β: barrada por poucos mm de alumínio"
            s.text(112, y - 8, msg, size=9.5, color=ORANGE_D, weight=600)
    s.text(693, 172, "poder de penetração: α < β < γ", size=10, color=INK, anchor="end", weight=700)
    s.save()
    return s


# =============================================================================
# 14. Meia-vida
# =============================================================================
def fig_halflife():
    W, Hh = 352, 232
    s = Svg("meiavida", W, Hh, "Decaimento exponencial: 100%, 50%, 25% e 12,5% após 0, 1, 2 e 3 meias-vidas")
    ox, oy = 66, 160
    X = lambda t: ox + t * 64
    Y = lambda p: oy - p / 100 * 124
    s.axes(ox, oy, 340, 22, ylab="N / N₀ (núcleos restantes)", ylab_x=12)
    pts = [(X(t / 40), Y(100 * 0.5 ** (t / 40))) for t in range(0, 161)]
    s.path(pts, color=ORANGE, w=2.6)
    for k in range(4):
        p = 100 * 0.5**k
        s.line(ox, Y(p), X(k), Y(p), color=GRID, w=1, dash="3 3")
        s.line(X(k), Y(p), X(k), oy, color=GRID, w=1, dash="3 3")
        s.circle(X(k), Y(p), 4.6, fill=ORANGE_D, stroke="#fff", sw=1.2)
        s.text(ox - 6, Y(p) + 3.5, f"{p:g}".replace(".", ",") + "%", size=9.5, anchor="end", weight=700, color=ORANGE_D)
        s.text(X(k), oy + 14, "0" if k == 0 else (f"{k} T½" if k > 1 else "T½"), size=9.5, anchor="middle", color=INK, weight=600)
    s.text(X(0.1) + 40, 32, "a cada T½, o que sobrou", size=9.5, color=MUTE)
    s.text(X(0.1) + 40, 44, "cai à metade", size=9.5, color=MUTE)
    s.text(200, oy + 34, "tempo t (em unidades de meia-vida T½)", size=10, anchor="middle")
    s.text(200, oy + 48, "ex.: ¹⁴C (T½ = 5730 anos): 0 · 5730 · 11 460 · 17 190 anos", size=9, anchor="middle", color=MUTE)
    s.text(200, oy + 61, "ex.: ¹³¹I (T½ ≈ 8 dias): 0 · 8 · 16 · 24 dias", size=9, anchor="middle", color=MUTE)
    s.save()
    return s


# =============================================================================
# 15. Energia de ligação por nucleon
# =============================================================================
def fig_binding():
    W, Hh = 345, 226
    s = Svg("ligacao", W, Hh, "Energia de ligação por núcleon em função do número de massa; fusão e fissão")
    ox, oy = 46, 176
    X = lambda a: ox + a / 240 * 280
    Y = lambda e: oy - e / 10 * 140
    s.axes(ox, oy, 332, 22, xlab="número de massa A", ylab="E de ligação por núcleon (MeV)", ylab_x=14, xlab_dy=26)
    data = [(1, 0), (2, 1.11), (4, 7.07), (12, 7.68), (16, 7.98), (28, 8.45), (56, 8.79), (84, 8.72), (120, 8.51), (160, 8.20), (208, 7.87), (238, 7.57)]
    s.path([(X(a), Y(e)) for a, e in data], color=ORANGE_D, w=2.4)
    for a, e, nm in ((2, 1.11, "²H"), (12, 7.68, "¹²C"), (56, 8.79, "⁵⁶Fe"), (238, 7.57, "²³⁸U")):
        s.circle(X(a), Y(e), 3.6, fill=ORANGE_D, stroke="#fff", sw=1)
    s.circle(X(4), Y(7.07), 3.6, fill=ORANGE_D, stroke="#fff", sw=1)
    s.line(X(4), Y(7.07) + 3, X(26), Y(5.5) - 6, color=GRAY, w=1)
    s.text(X(27), Y(5.5), "⁴He (pico local)", size=9.5, weight=700, halo=True)
    s.text(X(2) + 8, Y(1.11) + 4, "²H", size=9.5, weight=700)
    s.text(X(70), Y(8.79) - 9, "⁵⁶Fe: máximo (≈ 8,8 MeV)", size=9.5, weight=700, anchor="middle", halo=True)
    s.text(X(238), Y(7.57) + 15, "²³⁸U", size=9.5, weight=700, anchor="end", halo=True)
    for e in (2, 4, 6, 8):
        s.line(ox, Y(e), ox - 4, Y(e), color=INK)
        s.text(ox - 7, Y(e) + 3, str(e), size=9, color=MUTE, anchor="end")
    for a in (50, 100, 150, 200):
        s.line(X(a), oy, X(a), oy + 4, color=INK)
        s.text(X(a), oy + 14, str(a), size=9, color=MUTE, anchor="middle")
    # setas
    s.line(X(22), Y(3.2), X(54), Y(3.2), color=GREEN_D, w=2.2, arrow=True)
    s.text(X(22), Y(3.2) + 14, "fusão", size=10.5, color=GREEN_D, weight=700)
    s.text(X(22), Y(3.2) + 26, "(núcleos leves se unem)", size=9, color=MUTE)
    s.line(X(236), Y(5.0), X(130), Y(5.0), color=RED, w=2.2, arrow=True)
    s.text(X(236), Y(5.0) + 14, "fissão", size=10.5, color=RED, weight=700, anchor="end")
    s.text(X(236), Y(5.0) + 26, "(núcleo pesado se divide)", size=9, color=MUTE, anchor="end")
    s.text(332, 18, "valores aproximados", size=8.5, color=MUTE, anchor="end")
    s.save()
    return s


FIGS = [
    fig_timeline, fig_blackbody, fig_photoelectric, fig_photographs, fig_bohr, fig_spectra,
    fig_doubleslit, fig_probability, fig_uncertainty, fig_simultaneity, fig_ship, fig_lens,
    fig_expansion, fig_cosmic_timeline, fig_cmb, fig_radiation, fig_halflife, fig_binding,
]

if __name__ == "__main__":
    for f in FIGS:
        f()
    print("figuras geradas:", len(FIGS))
