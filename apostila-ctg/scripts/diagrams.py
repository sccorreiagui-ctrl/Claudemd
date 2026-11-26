#!/usr/bin/env python3
"""Gera todos os diagramas SVG da apostila CTG a partir de coordenadas EXATAS.

Cada ponto de apoio (pé de perpendicular, ponto de tangência, interseção...) é
calculado aqui e, antes de desenhar, conferido numericamente contra as
equações (função `assert_on`). Se um desenho contradisser a resolução, o script
falha. Escala é sempre 1:1 nos dois eixos (perpendiculares parecem
perpendiculares e circunferências parecem circunferências).
"""
import math
import os
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams")
os.makedirs(OUT, exist_ok=True)

# ---- paleta semântica CTG --------------------------------------------------
AZ = "#1f5fbf"   # dados / enunciado
VD = "#1e8a4c"   # resultado / interseção / verificação
RX = "#6b3fa0"   # centro, raio, circunferência
LJ = "#d9730d"   # transformações / passos
VM = "#c62828"   # perpendicularidade / alerta
OU = "#a87b0a"   # dourado discreto (fórmula-chave)
CZ = "#6b7280"   # neutro
GR = "#e3e7ee"   # grade
INK = "#1c2330"

EPS = 1e-9


def assert_on(a, b, c, P, what=""):
    v = a * P[0] + b * P[1] + c
    assert abs(v) < 1e-7, f"ponto {P} não está na reta {a}x+{b}y+{c}=0 ({what}) resíduo={v}"


def assert_circ(C, R, P, what=""):
    v = math.hypot(P[0] - C[0], P[1] - C[1]) - R
    assert abs(v) < 1e-7, f"ponto {P} não está na circunferência ({what}) resíduo={v}"


def foot(P, a, b, c):
    t = (a * P[0] + b * P[1] + c) / (a * a + b * b)
    return (P[0] - a * t, P[1] - b * t)


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Plot:
    def __init__(self, name, x0, x1, y0, y1, width=265, pad=(18, 12, 14, 14), step=1,
                 label_step=None, grid=True, axes=True, label=""):
        self.name, self.x0, self.x1, self.y0, self.y1 = name, x0, x1, y0, y1
        l, t, r, b = pad
        self.l, self.t, self.r, self.b = l, t, r, b
        self.s = (width - l - r) / (x1 - x0)
        self.W = width
        self.H = self.s * (y1 - y0) + t + b
        self.step = step
        self.label_step = label_step or step
        self.layers = {"grid": [], "shade": [], "line": [], "top": [], "txt": []}
        self.aria = label or name
        if grid:
            self._grid()
        if axes:
            self._axes()

    # coordenadas -> pixels
    def X(self, x):
        return self.l + self.s * (x - self.x0)

    def Y(self, y):
        return self.t + self.s * (self.y1 - y)

    def P(self, p):
        return self.X(p[0]), self.Y(p[1])

    def add(self, layer, s):
        self.layers[layer].append(s)

    # ---- base ---------------------------------------------------------------
    def _grid(self):
        k = math.ceil(self.x0 / self.step - EPS)
        while k * self.step <= self.x1 + EPS:
            x = k * self.step
            self.add("grid", f'<line x1="{fmt(self.X(x))}" y1="{fmt(self.Y(self.y0))}" x2="{fmt(self.X(x))}" y2="{fmt(self.Y(self.y1))}" stroke="{GR}" stroke-width="0.7"/>')
            k += 1
        k = math.ceil(self.y0 / self.step - EPS)
        while k * self.step <= self.y1 + EPS:
            y = k * self.step
            self.add("grid", f'<line x1="{fmt(self.X(self.x0))}" y1="{fmt(self.Y(y))}" x2="{fmt(self.X(self.x1))}" y2="{fmt(self.Y(y))}" stroke="{GR}" stroke-width="0.7"/>')
            k += 1

    def _axes(self):
        ax_y = 0 if self.y0 <= 0 <= self.y1 else self.y0
        ax_x = 0 if self.x0 <= 0 <= self.x1 else self.x0
        xa, ya = self.X(ax_x), self.Y(ax_y)
        c = "#4b5563"
        self.add("grid", f'<line x1="{fmt(self.X(self.x0))}" y1="{fmt(ya)}" x2="{fmt(self.X(self.x1)+6)}" y2="{fmt(ya)}" stroke="{c}" stroke-width="1.2"/>')
        self.add("grid", f'<line x1="{fmt(xa)}" y1="{fmt(self.Y(self.y0))}" x2="{fmt(xa)}" y2="{fmt(self.Y(self.y1)-6)}" stroke="{c}" stroke-width="1.2"/>')
        ex, ey = self.X(self.x1) + 6, self.Y(self.y1) - 6
        self.add("grid", f'<path d="M{fmt(ex)} {fmt(ya)} l-5 -2.6 v5.2z" fill="{c}"/>')
        self.add("grid", f'<path d="M{fmt(xa)} {fmt(ey)} l-2.6 5 h5.2z" fill="{c}"/>')
        self.add("txt", f'<text x="{fmt(ex+1)}" y="{fmt(ya-5)}" font-size="9.5" font-style="italic" fill="{c}" text-anchor="end">x</text>')
        self.add("txt", f'<text x="{fmt(xa+6)}" y="{fmt(ey+8)}" font-size="9.5" font-style="italic" fill="{c}">y</text>')
        # marcas
        k = math.ceil(self.x0 / self.label_step - EPS)
        while k * self.label_step <= self.x1 + EPS:
            x = k * self.label_step
            if abs(x) > EPS:
                self.add("grid", f'<line x1="{fmt(self.X(x))}" y1="{fmt(ya-2.5)}" x2="{fmt(self.X(x))}" y2="{fmt(ya+2.5)}" stroke="{c}" stroke-width="1"/>')
                self.add("txt", f'<text x="{fmt(self.X(x))}" y="{fmt(ya+11)}" font-size="7.6" fill="{CZ}" text-anchor="middle">{fmt(x).replace("-", "−")}</text>')
            k += 1
        k = math.ceil(self.y0 / self.label_step - EPS)
        while k * self.label_step <= self.y1 + EPS:
            y = k * self.label_step
            if abs(y) > EPS:
                self.add("grid", f'<line x1="{fmt(xa-2.5)}" y1="{fmt(self.Y(y))}" x2="{fmt(xa+2.5)}" y2="{fmt(self.Y(y))}" stroke="{c}" stroke-width="1"/>')
                self.add("txt", f'<text x="{fmt(xa-5)}" y="{fmt(self.Y(y)+2.8)}" font-size="7.6" fill="{CZ}" text-anchor="end">{fmt(y).replace("-", "−")}</text>')
            k += 1
        if self.x0 <= 0 <= self.x1 and self.y0 <= 0 <= self.y1:
            self.add("txt", f'<text x="{fmt(xa-4)}" y="{fmt(ya+10)}" font-size="7.6" fill="{CZ}" text-anchor="end">O</text>')

    # ---- elementos ----------------------------------------------------------
    def _ends(self, a, b, c):
        if abs(b) > EPS:
            return (self.x0 - 1, (-a * (self.x0 - 1) - c) / b), (self.x1 + 1, (-a * (self.x1 + 1) - c) / b)
        x = -c / a
        return (x, self.y0 - 1), (x, self.y1 + 1)

    def line(self, a, b, c, color=AZ, w=1.8, dash=None, layer="line", opacity=1):
        p, q = self._ends(a, b, c)
        self.seg(p, q, color, w, dash, layer, opacity, clip=True)

    def seg(self, p, q, color=AZ, w=1.8, dash=None, layer="line", opacity=1, clip=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity != 1 else ""
        el = (f'<line x1="{fmt(self.X(p[0]))}" y1="{fmt(self.Y(p[1]))}" x2="{fmt(self.X(q[0]))}" y2="{fmt(self.Y(q[1]))}" '
              f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}{o}/>')
        self.add(layer, f'<g clip-path="url(#clip-{self.name})">{el}</g>' if clip else el)

    def circle(self, C, R, color=RX, w=2, fill="none", dash=None, opacity=1, fill_opacity=0.08):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        f = fill if fill != "none" else "none"
        fo = f' fill-opacity="{fill_opacity}"' if fill != "none" else ""
        o = f' opacity="{opacity}"' if opacity != 1 else ""
        self.add("line", f'<circle cx="{fmt(self.X(C[0]))}" cy="{fmt(self.Y(C[1]))}" r="{fmt(R*self.s)}" fill="{f}"{fo} stroke="{color}" stroke-width="{w}"{d}{o}/>')

    def poly(self, pts, fill=VD, opacity=0.12, stroke="none", w=1.6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        pp = " ".join(f"{fmt(self.X(p[0]))},{fmt(self.Y(p[1]))}" for p in pts)
        self.add("shade", f'<polygon points="{pp}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"{d}/>')

    def pt(self, p, label=None, color=AZ, dx=6, dy=-6, anchor="start", r=3.4, hollow=False, size=9.5, weight=600, lcolor=None):
        fill = "#fff" if hollow else color
        self.add("top", f'<circle cx="{fmt(self.X(p[0]))}" cy="{fmt(self.Y(p[1]))}" r="{r}" fill="{fill}" stroke="{color if hollow else "#fff"}" stroke-width="{1.6 if hollow else 1.2}"/>')
        if label:
            self.text(p, label, dx, dy, lcolor or color, anchor, size, weight)

    def text(self, p, s, dx=0, dy=0, color=INK, anchor="start", size=9.5, weight=500, italic=False):
        it = ' font-style="italic"' if italic else ""
        self.add("txt", f'<text x="{fmt(self.X(p[0])+dx)}" y="{fmt(self.Y(p[1])+dy)}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{it} '
                        f'stroke="#fff" stroke-width="3" paint-order="stroke" stroke-linejoin="round">{s}</text>')

    def rightangle(self, V, u, w, size=7.5, color=VM):
        """quadradinho em V com pernas nas direções u e w (vetores no plano de dados)"""
        def unit(v):
            n = math.hypot(*v)
            return (v[0] / n, -v[1] / n)  # pixel (y invertido)
        ux, uy = unit(u)
        wx, wy = unit(w)
        vx, vy = self.P(V)
        p1 = (vx + size * ux, vy + size * uy)
        p2 = (vx + size * (ux + wx), vy + size * (uy + wy))
        p3 = (vx + size * wx, vy + size * wy)
        self.add("top", f'<path d="M{fmt(p1[0])} {fmt(p1[1])} L{fmt(p2[0])} {fmt(p2[1])} L{fmt(p3[0])} {fmt(p3[1])}" fill="none" stroke="{color}" stroke-width="1.5"/>')

    def tick(self, p, q, n=1, color=CZ, size=4):
        """marcas de congruência no ponto médio do segmento pq"""
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, -dy / L  # pixel
        nx, ny = -uy, ux
        cx, cy = self.P((mx, my))
        for i in range(n):
            off = (i - (n - 1) / 2) * 3.4
            ax, ay = cx + ux * off, cy + uy * off
            self.add("top", f'<line x1="{fmt(ax-nx*size)}" y1="{fmt(ay-ny*size)}" x2="{fmt(ax+nx*size)}" y2="{fmt(ay+ny*size)}" stroke="{color}" stroke-width="1.4"/>')

    def arrow(self, p, q, color=LJ, w=1.5):
        self.seg(p, q, color, w, layer="top")
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        ang = math.atan2(y2 - y1, x2 - x1)
        a = 5.5
        pts = [(x2, y2), (x2 - a * math.cos(ang - 0.4), y2 - a * math.sin(ang - 0.4)), (x2 - a * math.cos(ang + 0.4), y2 - a * math.sin(ang + 0.4))]
        self.add("top", f'<polygon points="{" ".join(f"{fmt(px)},{fmt(py)}" for px,py in pts)}" fill="{color}"/>')

    def raw(self, layer, s):
        self.add(layer, s)

    def svg(self):
        body = "".join(self.layers["grid"] + self.layers["shade"] + self.layers["line"] + self.layers["top"] + self.layers["txt"])
        clip = (f'<defs><clipPath id="clip-{self.name}"><rect x="{fmt(self.X(self.x0))}" y="{fmt(self.Y(self.y1))}" '
                f'width="{fmt(self.s*(self.x1-self.x0))}" height="{fmt(self.s*(self.y1-self.y0))}"/></clipPath></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(self.W)} {fmt(self.H)}" width="{fmt(self.W)}" height="{fmt(self.H)}" '
                f'font-family="Inter, \'DejaVu Sans\', Arial, sans-serif" role="img" aria-label="{escape(self.aria)}">{clip}{body}</svg>')

    def save(self):
        with open(os.path.join(OUT, self.name + ".svg"), "w", encoding="utf-8") as f:
            f.write(self.svg())


MINUS = "−"


def sg(v):
    return fmt(v).replace("-", MINUS)


# =============================================================================
# PÁGINA 1
# =============================================================================
def d_plano():
    p = Plot("t_plano", -1, 6.4, -1, 5.2, width=300, label="Plano cartesiano com A(1,1), B(5,4), abscissa, ordenada e triângulo retângulo")
    A, B = (1, 1), (5, 4)
    C = (5, 1)
    M = (3, 2.5)
    p.seg((5, 0), B, CZ, 1, "2 3", "line")
    p.seg((0, 4), B, CZ, 1, "2 3", "line")
    p.seg(A, C, LJ, 1.8, "5 3")
    p.seg(C, B, LJ, 1.8, "5 3")
    p.seg(A, B, AZ, 2.2)
    p.rightangle(C, (-1, 0), (0, 1), 6)
    p.pt(A, "A(1, 1)", AZ, -4, 14, "end")
    p.pt(B, "B(5, 4)", AZ, 7, -4)
    p.pt(M, "M", VD, -9, -4, "end")
    p.pt((5, 0), None, CZ, r=2.4)
    p.pt((0, 4), None, CZ, r=2.4)
    p.text((5, 0), "abscissa x<tspan baseline-shift=\"sub\" font-size=\"6.5\">B</tspan> = 5", 0, 22, CZ, "middle", 8.6)
    p.text((0, 4), "ordenada y<tspan baseline-shift=\"sub\" font-size=\"6.5\">B</tspan> = 4", 6, -6, CZ, "start", 8.6)
    p.text((3, 1), "Δx = 4", 0, 12, LJ, "middle", 9.5, 700)
    p.text((5, 2.5), "Δy = 3", 6, 3, LJ, "start", 9.5, 700)
    p.text((2.3, 3.15), "d = 5", -2, 0, AZ, "end", 10.5, 700)
    p.save()


def d_inclin():
    specs = [
        ("t_inc_a", "m > 0 · α agudo", "reta crescente", lambda p: p.line(1, -1, 0.3, AZ, 2.2), "↗"),
        ("t_inc_b", "m < 0 · α obtuso", "reta decrescente", lambda p: p.line(1, 1, -0.3, AZ, 2.2), "↘"),
        ("t_inc_c", "m = 0 · α = 0°", "horizontal  y = k", lambda p: p.line(0, 1, -1.4, AZ, 2.2), "→"),
        ("t_inc_d", "m não existe · α = 90°", "vertical  x = k", lambda p: p.line(1, 0, -1.4, AZ, 2.2), "↑"),
    ]
    for name, t1, t2, fn, ic in specs:
        p = Plot(name, -2.5, 3.5, -2.2, 3.2, width=150, pad=(10, 26, 10, 22), grid=False, label=t1 + " " + t2)
        fn(p)
        p.raw("txt", f'<text x="75" y="10" font-size="9" font-weight="700" fill="{INK}" text-anchor="middle">{t1}</text>')
        p.raw("txt", f'<text x="75" y="{fmt(p.H-6)}" font-size="8.6" fill="{CZ}" text-anchor="middle">{t2}</text>')
        p.save()


# =============================================================================
# PÁGINA 2 — triângulo em 3 painéis (altura ≠ mediana ≠ mediatriz)
# =============================================================================
TA, TB, TC = (0, 1), (8, 5), (0, 6)


def _tri_base(name, title, sub):
    p = Plot(name, -1.2, 9.2, -0.8, 8.2, width=215, pad=(6, 16, 8, 22), step=1, label_step=2, label=title)
    p.poly([TA, TB, TC], AZ, 0.07)
    for a, b in [(TA, TB), (TB, TC), (TC, TA)]:
        p.seg(a, b, AZ, 1.9)
    p.pt(TA, "A", AZ, -9, 12, size=9.5)
    p.pt(TB, "B", AZ, 6, 4)
    p.pt(TC, "C", AZ, -9, -3)
    p.raw("txt", f'<text x="107" y="11" font-size="9.4" font-weight="700" fill="{INK}" text-anchor="middle">{title}</text>')
    return p


def d_triangulos():
    H = foot(TC, 1, -2, 2)  # (2,2)
    M = (4, 3)
    assert abs(H[0] - 2) < 1e-9 and abs(H[1] - 2) < 1e-9
    # altura
    p = _tri_base("t_tri_altura", "ALTURA relativa a AB", "")
    p.seg(TC, H, VM, 2.4)
    p.rightangle(H, (-2, 1), (-1, -0.5), 6.5)
    p.pt(H, "H", VM, 5, 11)
    p.pt(M, "M", CZ, 6, -4, hollow=True, size=8.6)
    p.raw("txt", f'<text x="107" y="{fmt(p.H-4)}" font-size="8.4" fill="{VM}" text-anchor="middle" font-weight="600">⊥ a AB · H ≠ M</text>')
    p.save()
    # mediana
    p = _tri_base("t_tri_mediana", "MEDIANA relativa a AB", "")
    p.seg(TC, M, AZ, 2.4, "6 3")
    p.tick(TA, M, 1, AZ)
    p.tick(M, TB, 1, AZ)
    p.pt(M, "M", AZ, 6, 12)
    p.pt(H, "H", CZ, -4, 12, hollow=True, size=8.6, anchor="end")
    p.raw("txt", f'<text x="107" y="{fmt(p.H-4)}" font-size="8.4" fill="{AZ}" text-anchor="middle" font-weight="600">AM = MB · vai ao ponto médio</text>')
    p.save()
    # mediatriz de AB: perpendicular por M
    p = _tri_base("t_tri_mediatriz", "MEDIATRIZ de AB", "")
    p.line(2, 1, -11, VD, 2.4)  # 2x + y - 11 = 0 passa por M, ⊥ AB
    p.tick(TA, M, 1, VD)
    p.tick(M, TB, 1, VD)
    p.rightangle(M, (1, -2), (2, 1), 6.5)
    p.pt(M, "M", VD, 7, -5)
    p.raw("txt", f'<text x="107" y="{fmt(p.H-4)}" font-size="8.4" fill="{VD}" text-anchor="middle" font-weight="600">por M e ⊥ a AB (não passa por C)</text>')
    p.save()


def d_ciclico():
    """esquema do método cíclico (falso determinante) para A(−2,1), B(4,3)"""
    W, H = 150, 132
    xs = (48, 104)
    ys = (22, 48, 74, 100)
    rows = [("x", "y"), ("−2", "1"), ("4", "3"), ("x", "y")]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, \'DejaVu Sans\', Arial, sans-serif" role="img" aria-label="Esquema do método cíclico">']
    # diagonais descendo (laranja) e subindo (azul tracejado)
    for i in range(3):
        s.append(f'<line x1="{xs[0]+8}" y1="{ys[i]-3}" x2="{xs[1]-8}" y2="{ys[i+1]-3}" stroke="{LJ}" stroke-width="2.2" stroke-linecap="round"/>')
        s.append(f'<line x1="{xs[0]+8}" y1="{ys[i+1]-3}" x2="{xs[1]-8}" y2="{ys[i]-3}" stroke="{AZ}" stroke-width="2" stroke-dasharray="4 3" stroke-linecap="round"/>')
    for (a, b), y in zip(rows, ys):
        col = INK
        s.append(f'<text x="{xs[0]}" y="{y}" font-size="13" font-weight="700" text-anchor="middle" fill="{VD if a=="x" else col}" font-style="{"italic" if a=="x" else "normal"}" stroke="#fff" stroke-width="3" paint-order="stroke">{a}</text>')
        s.append(f'<text x="{xs[1]}" y="{y}" font-size="13" font-weight="700" text-anchor="middle" fill="{VD if b=="y" else col}" font-style="{"italic" if b=="y" else "normal"}" stroke="#fff" stroke-width="3" paint-order="stroke">{b}</text>')
    s.append(f'<text x="4" y="{ys[1]}" font-size="9" fill="{CZ}">A</text><text x="4" y="{ys[2]}" font-size="9" fill="{CZ}">B</text>')
    s.append(f'<text x="{W-2}" y="{ys[0]-9}" font-size="8" fill="{CZ}" text-anchor="end">repete a 1ª linha</text>')
    s.append(f'<text x="{W-2}" y="{ys[3]+13}" font-size="8" fill="{CZ}" text-anchor="end">(x, y) no fim</text>')
    s.append("</svg>")
    open(os.path.join(OUT, "t_ciclico.svg"), "w", encoding="utf-8").write("".join(s))


# =============================================================================
# EXERCÍCIOS — PONTO E RETA
# =============================================================================
def d_r1():
    p = Plot("r1", -4.6, 5.4, -2, 6.4, width=268, label="R1: pontos A(-1,3) e B(3,1) e a reta AB")
    A, B = (-1, 3), (3, 1)
    assert_on(2, -1, 5, A, "A em r")
    assert_on(1, 1, -4, B, "B em s")
    assert_on(1, 2, -5, A)
    assert_on(1, 2, -5, B)
    p.line(2, -1, 5, CZ, 1.6)
    p.line(1, 1, -4, CZ, 1.6)
    p.seg((-1, 0), A, CZ, 1, "2 3", "line")
    p.seg((0, 1), B, CZ, 1, "2 3", "line")
    p.line(1, 2, -5, AZ, 2.4)
    p.seg(A, (3, 3), LJ, 1.6, "5 3")
    p.seg((3, 3), B, LJ, 1.6, "5 3")
    p.text((1, 3), "Δx = 4", 0, -5, LJ, "middle", 9, 700)
    p.text((3, 2), "Δy = −2", 6, 3, LJ, "start", 9, 700)
    p.pt(A, "A(−1, 3)", VD, -8, -9, "end")
    p.pt(B, "B(3, 1)", VD, 8, -8)
    p.text((-3.6, -1.1), "r: y = 2x + 5", 4, 0, CZ, "start", 8.8, 600)
    p.text((5.3, -1.3), "s: y = −x + 4", 0, 12, CZ, "end", 8.8, 600)
    p.text((-3.5, 4.3), "AB", 0, -6, AZ, "start", 10, 700)
    p.text((-1, 0), "x = −1", 3, -4, CZ, "start", 8, 500)
    p.text((0, 1), "y = 1", -6, -4, CZ, "end", 8, 500)
    p.save()


def d_r2():
    p = Plot("r2", -3.4, 5.4, -2, 6.4, width=262, label="R2: reta r, ponto P e a perpendicular s")
    P = (2, 1)
    F = (1.6, 0.8)
    assert_on(6, 3, -12, F)
    assert abs(F[1] - F[0] / 2) < 1e-9
    assert abs(P[1] - P[0] / 2) < 1e-9
    p.line(6, 3, -12, AZ, 2.2)       # r
    p.line(1, -2, 0, VM, 2.2)         # s: y = x/2  -> x - 2y = 0
    p.seg((0, 4), (1, 2), LJ, 1.6, "5 3")
    p.seg((1, 4), (1, 2), LJ, 1.6, "5 3")
    p.text((0.5, 4), "Δx=1", 0, -5, LJ, "middle", 8.4, 700)
    p.text((1, 3), "Δy=−2", 5, 3, LJ, "start", 8.4, 700)
    p.rightangle(F, (-1, 2), (2, 1), 7)
    p.pt((0, 4), "n = 4", AZ, -6, -4, "end", r=3)
    p.pt(P, "P(2, 1)", AZ, 7, 3)
    p.text((-2.9, 2.4), "r: m = −2", 0, -2, AZ, "start", 9, 700)
    p.text((4.5, 2.25), "s: y = x/2", 0, -6, VM, "end", 9, 700)
    p.text(F, "90°", -8, 14, VM, "end", 8.4, 700)
    p.save()


def d_r3():
    p = Plot("r3", -3.6, 6.6, -1, 7, width=272, label="R3: reta AB e a perpendicular por P(1,4)")
    A, B, Pp = (-2, 1), (4, 3), (1, 4)
    F = (1.6, 2.2)
    assert_on(1, -3, 5, A)
    assert_on(1, -3, 5, B)
    assert_on(3, 1, -7, Pp)
    assert_on(1, -3, 5, F)
    assert_on(3, 1, -7, F)
    p.line(1, -3, 5, AZ, 2.2)
    p.line(3, 1, -7, VM, 2.2)
    p.seg(A, B, AZ, 3.2)
    p.rightangle(F, (-3, -1), (-1, 3), 7)
    p.pt(A, "A(−2, 1)", AZ, -2, 15, "middle")
    p.pt(B, "B(4, 3)", AZ, 5, 14)
    p.pt(Pp, "P(1, 4)", AZ, 8, -5)
    p.pt((1, 2), "ponto médio de AB = (1, 2) ≠ P", CZ, 8, 16, hollow=True, r=3, size=8.2, weight=500)
    p.pt(F, None, VD)
    p.text(F, "pé (1,6; 2,2)", 12, 6, VD, "start", 8.4, 700)
    p.text((5.45, 3.4), "AB", 0, -4, AZ, "start", 9.5, 700)
    p.text((0.45, 6.5), "⊥: 3x + y − 7 = 0", 0, 0, VM, "start", 9, 700)
    p.save()


def d_r4():
    p = Plot("r4", -1.6, 9.6, -1, 8.2, width=285, step=1, label_step=1, label="R4: altura CH e ponto médio M de AB")
    A, B, C = (0, 1), (8, 5), (0, 6)
    H, M = (2, 2), (4, 3)
    assert_on(1, -2, 2, A)
    assert_on(1, -2, 2, B)
    assert_on(1, -2, 2, H)
    assert abs((C[0] - H[0]) * (B[0] - A[0]) + (C[1] - H[1]) * (B[1] - A[1])) < 1e-9
    p.poly([A, B, C], AZ, 0.07)
    for a, b in [(A, B), (B, C), (C, A)]:
        p.seg(a, b, AZ, 2.2)
    p.seg(C, M, CZ, 1.4, "4 3")
    p.seg(C, H, VM, 2.6)
    p.rightangle(H, (-2, 1), (-1, -0.5), 7.5)
    p.pt(A, "A(0, 1)", AZ, -6, 14, "end")
    p.pt(B, "B(8, 5)", AZ, 7, 4)
    p.pt(C, "C(0, 6)", AZ, -6, -4, "end")
    p.pt(H, "H(2, 2)", VD, 6, 15, size=10)
    p.pt(M, "M(4, 3)  ponto médio de AB", CZ, 6, 14, hollow=True, size=8.6, weight=600)
    p.text((1, 4), "CH", -9, 0, VM, "end", 10, 700)
    p.text((9.7, 3.4), "AB: x − 2y + 2 = 0", 0, 0, AZ, "end", 8.6, 700)
    p.save()


def d_r5():
    p = Plot("r5", -5, 6, -1.6, 7, width=268, label="R5: P, origem e a reta r; dois segmentos diferentes")
    P, O = (3, 4), (0, 0)
    F = (2.4, 4.8)
    assert_on(3, -4, 12, F)
    assert abs(math.hypot(P[0] - F[0], P[1] - F[1]) - 1) < 1e-9
    p.line(3, -4, 12, AZ, 2.2)
    p.seg(P, O, LJ, 2.2)
    p.seg(P, F, VM, 3)
    p.rightangle(F, (4, 3), (3, -4), 5)
    p.pt(O, "O", CZ, -9, 14, r=3)
    p.pt(P, "P(3, 4)", AZ, 8, 4)
    p.pt(F, None, VD, r=3)
    p.text((1.5, 2), "5", 8, -2, LJ, "start", 10.5, 700)
    p.text(F, "F", -9, -4, VD, "end", 9.5, 700)
    p.text((3, 4.3), "1", 9, -9, VM, "start", 10.5, 700)
    p.text((-4.7, 0.6), "r: 3x − 4y + 12 = 0", 0, -2, AZ, "start", 9, 700)
    p.text((3.6, 1.0), "ponto–ponto", 0, 0, LJ, "start", 8.6, 700)
    p.text((3.6, 0.35), "ponto–reta", 0, 0, VM, "start", 8.6, 700)
    p.save()


def d_r6():
    p = Plot("r6", -8.6, 7.2, -6.6, 9.2, width=262, step=1, label_step=2, label="R6: reta r e as duas paralelas a distância 5")
    assert_on(3, -4, 32, (-4, 5))
    assert_on(3, -4, 7, (-1, 1))
    assert_on(3, -4, -18, (2, -3))
    assert abs(math.hypot(3, -4) - 5) < 1e-9
    p.line(3, -4, 32, VD, 2.2)
    p.line(3, -4, 7, AZ, 2.4)
    p.line(3, -4, -18, VD, 2.2)
    p.seg((-4, 5), (2, -3), LJ, 1.6, "4 3", "top")
    p.rightangle((-1, 1), (3, 4), (3, -4), 6)
    p.pt((-4, 5), None, VD, r=2.8)
    p.pt((2, -3), None, VD, r=2.8)
    p.pt((-1, 1), None, AZ, r=2.8)
    p.text((-2.5, 3), "5", -7, 0, LJ, "end", 10, 700)
    p.text((0.5, -1), "5", 7, 4, LJ, "start", 10, 700)
    p.text((-7.4, 2.2), "3x − 4y + 32 = 0", 0, -2, VD, "start", 8.6, 700)
    p.text((-7.4, -2.6), "r: 3x − 4y + 7 = 0", -2, -6, AZ, "start", 8.6, 700)
    p.text((4.4, 0.4), "3x − 4y − 18 = 0", 0, -6, VD, "end", 8.6, 700)
    p.save()


def d_r7():
    p = Plot("r7", -7.2, 5.4, -4.2, 8.6, width=275, label_step=1, label="R7: triângulo formado pelas retas r, s, t")
    A, B, C = (-4, 0), (2, -2), (0, 6)
    assert_on(3, -2, 12, A); assert_on(1, 3, 4, A)
    assert_on(1, 3, 4, B); assert_on(4, 1, -6, B)
    assert_on(4, 1, -6, C); assert_on(3, -2, 12, C)
    p.poly([A, B, C], VD, 0.14)
    p.line(3, -2, 12, AZ, 1.8)
    p.line(1, 3, 4, AZ, 1.8)
    p.line(4, 1, -6, AZ, 1.8)
    for a, b in [(A, B), (B, C), (C, A)]:
        p.seg(a, b, AZ, 2.8)
    p.pt(A, "A(−4, 0)", VD, -7, -8, "end")
    p.pt(B, "B(2, −2)", VD, 5, 21)
    p.pt(C, "C(0, 6)", VD, 7, 2)
    p.text((-6.9, -2.55), "r: 3x − 2y + 12 = 0", 0, 0, AZ, "start", 8.6, 700)
    p.text((-6.9, 1.6), "s: x + 3y + 4 = 0", 0, 0, AZ, "start", 8.6, 700)
    p.text((-0.45, 7.9), "t: 4x + y − 6 = 0", -6, 0, AZ, "end", 8.6, 700)
    p.text((-0.7, 1.2), "área = 22", 0, 0, VD, "middle", 10, 700)
    p.save()


# =============================================================================
# CIRCUNFERÊNCIA — TEORIA
# =============================================================================
def d_tcirc():
    p = Plot("t_circ", -1.6, 7, -1.4, 5.9, width=270, label="Circunferência com centro C(a,b), ponto P(x,y) e triângulo retângulo auxiliar")
    C, R = (2.6, 1.6), 2.8
    ang = math.radians(38)
    P = (C[0] + R * math.cos(ang), C[1] + R * math.sin(ang))
    Q = (P[0], C[1])
    p.circle(C, R, RX, 2.2, RX, fill_opacity=0.06)
    p.poly([C, Q, P], "#f2c94c", 0.28)
    p.seg(C, Q, LJ, 1.8)
    p.seg(Q, P, LJ, 1.8)
    p.seg(C, P, RX, 2.4)
    p.rightangle(Q, (-1, 0), (0, 1), 6)
    p.pt(C, "C(a, b)", RX, -8, 13, "end")
    p.pt(P, "P(x, y)", AZ, 7, -4)
    p.text(((C[0] + P[0]) / 2, (C[1] + P[1]) / 2), "R", -5, -5, RX, "end", 11, 700, italic=True)
    p.text(((C[0] + Q[0]) / 2, C[1]), "x − a", 0, 13, LJ, "middle", 9, 700)
    p.text((Q[0], (Q[1] + P[1]) / 2), "y − b", 6, 3, LJ, "start", 9, 700)
    p.text((6.9, 5.4), "(x−a)² + (y−b)² = R²", 0, 0, RX, "end", 9.4, 700)
    p.save()


def d_tpos():
    p = Plot("t_pos", -5, 8.8, -3.6, 7.8, width=270, label_step=2, label="Pontos P, Q, R em relação à circunferência de centro (1,2) e raio 5")
    C, R = (1, 2), 5
    for P in [(4, 6)]:
        assert_circ(C, R, P)
    p.circle(C, R, RX, 2.2, RX, fill_opacity=0.06)
    p.pt(C, "C(1, 2)", RX, -7, 4, "end", size=9)
    p.seg(C, (4, 6), RX, 1.4, "3 3")
    p.pt((4, 6), "P(4, 6)", AZ, 8, -6)
    p.pt((1, 5), "Q(1, 5)", VD, -7, -6, "end")
    p.pt((7, 2), "R(7, 2)", VM, 8, -6)
    p.text((6.3, -2.1), "R² = 25", 0, 0, RX, "end", 9, 700)
    p.save()


def d_trel():
    specs = [
        ("t_rel_a", 1.0, "SECANTE", "d < R · 2 pontos · Δ > 0", VD),
        ("t_rel_b", 2.0, "TANGENTE", "d = R · 1 ponto · Δ = 0", AZ),
        ("t_rel_c", 3.1, "EXTERNA", "d > R · 0 pontos · Δ < 0", CZ),
    ]
    R = 2.0
    for name, h, t1, t2, col in specs:
        p = Plot(name, -3, 3, -2.4, 3.5, width=170, pad=(6, 20, 6, 20), grid=False, axes=False, label=t1)
        p.circle((0, 0), R, RX, 2.2, RX, fill_opacity=0.06)
        p.seg((-3, h), (3, h), col if name != "t_rel_c" else CZ, 2.4)
        p.pt((0, 0), None, RX, r=2.8)
        p.seg((0, 0), (0, h), VM, 2)
        p.rightangle((0, h), (0, -1), (1, 0), 6)
        p.seg((0, 0), (-R * math.cos(math.radians(35)), -R * math.sin(math.radians(35))), RX, 1.5, "3 2")
        p.text((0, h / 2), "d", 6, 3, VM, "start", 9.5, 700, italic=True)
        p.text((-1.25, -0.95), "R", -3, 0, RX, "end", 9.5, 700, italic=True)
        if name == "t_rel_a":
            dx = math.sqrt(R * R - h * h)
            p.pt((dx, h), None, VD, r=3)
            p.pt((-dx, h), None, VD, r=3)
        if name == "t_rel_b":
            p.pt((0, h), None, VD, r=3.2)
        p.raw("txt", f'<text x="85" y="11" font-size="9" font-weight="800" fill="{INK}" text-anchor="middle">{t1}</text>')
        p.raw("txt", f'<text x="85" y="{fmt(p.H-6)}" font-size="8.3" fill="{CZ}" text-anchor="middle">{t2}</text>')
        p.save()


def d_ttwo():
    """seis posições relativas entre duas circunferências (R1=1,2; R2=0,7)"""
    R1, R2 = 1.2, 0.7
    cfg = [
        ("t_two_a", "externas", "d > R₁+R₂", 2.6),
        ("t_two_b", "tang. externas", "d = R₁+R₂", 1.9),
        ("t_two_c", "secantes", "|R₁−R₂| < d < R₁+R₂", 1.3),
        ("t_two_d", "tang. internas", "d = |R₁−R₂| > 0", 0.5),
        ("t_two_e", "internas", "d < |R₁−R₂|", 0.2),
        ("t_two_f", "coincidentes", "d = 0 e R₁ = R₂", 0.0),
    ]
    for name, t1, t2, d in cfg:
        w = 112
        p = Plot(name, -1.4, 3.6, -1.4, 1.4, width=w, pad=(4, 4, 4, 24), grid=False, axes=False, label=t1)
        r2 = R2 if name != "t_two_f" else R1
        p.circle((0, 0), R1, RX, 1.9, RX, fill_opacity=0.05)
        p.circle((d, 0), r2, AZ if name != "t_two_f" else VM, 1.6 if name != "t_two_f" else 1.2, "none", dash=("3 2" if name == "t_two_f" else None))
        p.pt((0, 0), None, RX, r=2.2)
        if name != "t_two_f":
            p.pt((d, 0), None, AZ, r=2.2)
        if name == "t_two_b":
            p.pt((R1, 0), None, VD, r=2.6)
        if name == "t_two_d":
            p.pt((R1, 0), None, VD, r=2.6)
        if name == "t_two_c":
            x = (d * d + R1 * R1 - R2 * R2) / (2 * d)
            yv = math.sqrt(R1 * R1 - x * x)
            p.pt((x, yv), None, VD, r=2.6)
            p.pt((x, -yv), None, VD, r=2.6)
        p.raw("txt", f'<text x="{w/2}" y="{fmt(p.H-13)}" font-size="8.2" font-weight="800" fill="{INK}" text-anchor="middle">{t1}</text>')
        p.raw("txt", f'<text x="{w/2}" y="{fmt(p.H-3)}" font-size="7.4" fill="{CZ}" text-anchor="middle">{t2}</text>')
        p.save()


# =============================================================================
# EXERCÍCIOS — CIRCUNFERÊNCIA
# =============================================================================
def d_c1():
    p = Plot("c1", -4.6, 8.6, -9, 3.2, width=268, label_step=2, label="C1: circunferência de centro (2,-3) e raio 4 e seus extremos")
    C, R = (2, -3), 4
    pts = [(6, -3), (-2, -3), (2, 1), (2, -7)]
    for q in pts:
        assert_circ(C, R, q)
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.07)
    p.seg(C, (6, -3), RX, 1.8)
    p.pt(C, "C(2, −3)", RX, -6, 14, "end")
    p.text((4, -3), "R = 4", 0, -6, RX, "middle", 9.5, 700)
    p.pt((6, -3), "(6, −3)", VD, 7, 4)
    p.pt((-2, -3), "(−2, −3)", VD, -7, 4, "end")
    p.pt((2, 1), "(2, 1)", VD, 7, -2)
    p.pt((2, -7), "(2, −7)", VD, 7, 12)
    p.save()


def d_c2():
    p = Plot("c2", -2.4, 8.4, -7.8, 3.6, width=246, label_step=2, label="C2: circunferência de centro (3,-2) e raio 4")
    C, R = (3, -2), 4
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.07)
    p.seg(C, (7, -2), RX, 1.8)
    p.pt(C, "C(3, −2)", RX, -5, 14, "end")
    p.text((5, -2), "R = 4", 0, -6, RX, "middle", 9.5, 700)
    for q in [(7, -2), (-1, -2), (3, 2), (3, -6)]:
        assert_circ(C, R, q)
        p.pt(q, None, RX, r=2.4)
    p.save()


def d_c3():
    p = Plot("c3", -7.4, 7.6, -11, 4.2, width=272, label_step=2, label="C3: três retas e a circunferência de centro (1,-2) e raio 5")
    C, R = (1, -2), 5
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.06)
    cols = {20: (VD, "s"), 30: (AZ, "t"), 40: (CZ, "u")}
    for cc, (col, nm) in cols.items():
        p.line(3, 4, cc, col, 2.1)
    feet = {cc: foot(C, 3, 4, cc) for cc in cols}
    for cc, F in feet.items():
        assert_on(3, 4, cc, F)
    assert_circ(C, R, feet[30])
    p.seg(C, feet[40], RX, 1.5, "4 3", "top")
    p.pt(C, "C(1, −2)", RX, 7, -4)
    for cc, F in feet.items():
        p.rightangle(F, (3, 4), (4, -3), 5.5)
        p.pt(F, None, cols[cc][0], r=2.7)
    # interseções da secante s com a circunferência
    d = 3.0
    h = math.sqrt(R * R - d * d)  # 4
    n = (3 / 5, 4 / 5)
    t = (-4 / 5, 3 / 5)
    F = feet[20]
    for sgn in (1, -1):
        q = (F[0] + sgn * h * t[0], F[1] + sgn * h * t[1])
        assert_circ(C, R, q)
        assert_on(3, 4, 20, q)
        p.pt(q, None, VD, r=3)
    p.text((-0.4, -3.2), "d = 3", -4, 0, VD, "end", 9, 700)
    p.text((-1.2, -5.1), "d = 5", -4, 0, AZ, "end", 9, 700)
    p.text((-2.6, -6.8), "d = 7", -4, 0, CZ, "end", 9, 700)
    p.text((3.2, -6.55), "s", 0, 0, VD, "start", 10, 800)
    p.text((6.6, -8.5), "t", -2, 0, AZ, "end", 10, 800)
    p.text((6.6, -11.0), "u", -2, -6, CZ, "end", 10, 800)
    p.save()


def d_c4():
    p = Plot("c4", -6.4, 8.4, -4.2, 8.4, width=270, label_step=2, label="C4: circunferência e a reta y=6")
    C, R = (1, 2), 5
    for q in [(4, 6), (-2, 6)]:
        assert_circ(C, R, q)
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.06)
    p.line(0, 1, -6, AZ, 2.3)
    p.seg(C, (1, 6), VM, 1.6, "4 3")
    p.seg(C, (4, 6), RX, 1.5, "4 3")
    p.rightangle((1, 6), (0, -1), (1, 0), 6)
    p.pt(C, "C(1, 2)", RX, 7, 14)
    p.pt((4, 6), "(4, 6)", VD, 7, -6)
    p.pt((-2, 6), "(−2, 6)", VD, -7, -6, "end")
    p.text((1, 4), "d = 4", 6, 3, VM, "start", 9, 700)
    p.text((2.6, 4), "R=5", 4, 0, RX, "start", 9, 700)
    p.text((8.2, 6), "y = 6", 0, -6, AZ, "end", 9.2, 700)
    p.save()


def d_c5():
    p = Plot("c5", -6.4, 9.6, -4.4, 10.6, width=268, label_step=2, label="C5: tangente à circunferência no ponto P(4,6)")
    C, R, P = (1, 2), 5, (4, 6)
    assert_circ(C, R, P)
    assert_on(3, 4, -36, P)
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.06)
    p.line(3, 4, -36, VD, 2.4)
    p.seg(C, P, RX, 2.2)
    p.rightangle(P, (-3, -4), (4, -3), 7, VM)
    p.pt(C, "C(1, 2)", RX, -6, 14, "end")
    p.pt(P, "P(4, 6)", AZ, 9, -7)
    p.text((2.5, 4), "R = 5", -4, 0, RX, "end", 9.5, 700)
    p.text((9.6, 1.5), "t: 3x + 4y − 36 = 0", 0, 0, VD, "end", 9, 700)
    p.save()


def d_c6():
    p = Plot("c6", -1.4, 11, -5.2, 7.4, width=270, label_step=2, label="C6: corda determinada pela reta x-2y+2=0 na circunferência de centro (5,0)")
    C, R = (5, 0), 4
    M = (3.6, 2.8)
    assert_on(1, -2, 2, M)
    ys = [(14 + math.sqrt(31)) / 5, (14 - math.sqrt(31)) / 5]
    A, B = [(2 * y - 2, y) for y in ys]
    for q in (A, B):
        assert_circ(C, R, q)
        assert_on(1, -2, 2, q)
    assert abs(((A[0] + B[0]) / 2 - M[0])) < 1e-9 and abs(((A[1] + B[1]) / 2 - M[1])) < 1e-9
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.05)
    p.line(1, -2, 2, AZ, 1.8)
    p.poly([C, M, A], "#f2c94c", 0.32)
    p.seg(A, B, VD, 3.4)
    p.seg(C, M, VM, 2.2)
    p.seg(C, A, RX, 2.2)
    p.rightangle(M, (-1, 2), (2, 1), 6.5)
    p.pt(C, "C(5, 0)", RX, 6, 14)
    p.pt(M, "M", VM, -7, -6, "end")
    p.pt(A, "A", VD, 4, -7)
    p.pt(B, "B", VD, -6, 10, "end")
    p.text(((C[0] + M[0]) / 2, (C[1] + M[1]) / 2), "d = 7/√5", 8, 8, VM, "start", 8.8, 700)
    p.text(((C[0] + A[0]) / 2, (C[1] + A[1]) / 2), "R = 4", 3, 2, RX, "start", 9, 700)
    p.text(((M[0] + A[0]) / 2, (M[1] + A[1]) / 2), "c/2", 0, 15, VD, "middle", 9, 700)
    p.text((10.9, 6.6), "x − 2y + 2 = 0", 0, 0, AZ, "end", 8.6, 700)
    p.save()


def d_c7():
    p = Plot("c7", -2.6, 10.6, -4.4, 7.8, width=278, label_step=2, label="C7: as duas tangentes por P(0,4) à circunferência de centro (6,1)")
    C, R, P = (6, 1), 3, (0, 4)
    T1, T2 = (6, 4), (3.6, -0.8)
    assert_circ(C, R, T1)
    assert_circ(C, R, T2)
    assert_on(0, 1, -4, T1)
    assert_on(4, 3, -12, T2)
    assert_on(0, 1, -4, P)
    assert_on(4, 3, -12, P)
    p.circle(C, R, RX, 2.4, RX, fill_opacity=0.06)
    p.line(1, 0, 0, CZ, 1.4, "5 4")                # x = 0 (não tangente)
    p.line(0, 1, -4, VD, 2.4)
    p.line(4, 3, -12, VD, 2.4)
    p.seg(C, T1, RX, 1.8)
    p.seg(C, T2, RX, 1.8)
    p.rightangle(T1, (-1, 0), (0, -1), 6)
    p.rightangle(T2, (2.4, 1.8), (1.8, -2.4), 6)
    p.pt(C, "C(6, 1)", RX, 6, 14)
    p.pt(P, "P(0, 4)", AZ, 8, -6)
    p.pt(T1, "T₁(6, 4)", VD, -2, -8, "middle")
    p.pt(T2, "T₂(3,6; −0,8)", VD, -9, 14, "end")
    p.text((0.2, 7.15), "x = 0 (eixo y): d = 6 > R, não é tangente", 0, 0, CZ, "start", 8.2, 600)
    p.text((10.4, 4), "y = 4", 0, -6, VD, "end", 9, 700)
    p.text((6.4, -3.2), "4x + 3y − 12 = 0", 6, 0, VD, "start", 8.8, 700)
    p.save()


def d_c8():
    p = Plot("c8", 0.3, 7.0, -3.9, 1.9, width=262, label_step=1, label="C8: circunferência tangente à reta 3x+4y-10=0 quando p=9")
    C = (3, -1)
    T = (3.6, -0.2)
    assert_circ(C, 1, T)
    assert_on(3, 4, -10, T)
    p.line(3, 4, -10, AZ, 2.2)
    p.circle(C, math.sqrt(3), RX, 1.5, "none", dash="4 3", opacity=0.85)    # p = 7  (secante)
    p.circle(C, math.sqrt(0.5), RX, 1.5, "none", dash="2 2", opacity=0.85)  # p = 9,5 (externa)
    p.circle(C, 1, RX, 2.6, RX, fill_opacity=0.08)
    p.seg(C, T, VM, 2)
    p.rightangle(T, (-3, -4), (4, -3), 5)
    p.pt(C, "C(3, −1)", RX, -8, 4, "end")
    p.pt(T, None, VD, r=3.2)
    p.text(T, "T(3,6; −0,2)", 10, -9, VD, "start", 8.8, 700)
    p.text((0.45, -2.95), "—  p = 9: R = d = 1 (tangente)", 0, 0, RX, "start", 8.4, 700)
    p.text((0.45, -3.3), "- -  p = 7: R² = 3 (secante)", 0, 0, RX, "start", 8.2, 600)
    p.text((0.45, -3.65), "· ·  p = 9,5: R² = 0,5 (externa)", 0, 0, RX, "start", 8.2, 600)
    p.text((6.9, 1.1), "3x + 4y − 10 = 0", 0, -2, AZ, "end", 8.8, 700)
    p.save()


def main():
    for fn in (d_plano, d_inclin, d_triangulos, d_ciclico, d_r1, d_r2, d_r3, d_r4, d_r5, d_r6, d_r7,
               d_tcirc, d_tpos, d_trel, d_ttwo, d_c1, d_c2, d_c3, d_c4, d_c5, d_c6, d_c7, d_c8):
        fn()
    n = len([f for f in os.listdir(OUT) if f.endswith(".svg")])
    print(f"{n} diagramas SVG gerados em {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
