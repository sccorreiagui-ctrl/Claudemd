"""Figuras do Módulo II — Eletrostática (parte A: carga, eletrização, Coulomb)."""
import math
from . import fig
from lib.circuit import *


def _body(f, x, y, w, h, plus, minus, label=None, col=GRY_L):
    """Corpo retangular com `plus` sinais + e `minus` sinais − dispostos em grade."""
    f.rect(x, y, w, h, "#fff", GRY, 1.6, rx=8, tag="bg")
    n = plus + minus
    cols = max(plus, minus, 1)
    sy = [y + h * 0.30, y + h * 0.70]
    for i in range(plus):
        px = x + w * (i + 0.5) / max(plus, 1)
        f.line(px - 3.6, sy[0], px + 3.6, sy[0], POS, 1.6, tag="bg")
        f.line(px, sy[0] - 3.6, px, sy[0] + 3.6, POS, 1.6, tag="bg")
    for i in range(minus):
        px = x + w * (i + 0.5) / max(minus, 1)
        f.line(px - 3.6, sy[1], px + 3.6, sy[1], NEG, 1.6, tag="bg")


@fig("cargas_inter")
def cargas_inter():
    f = Fig(332, 178, title="Interação entre cargas: mesmos sinais repelem, sinais opostos atraem")
    rows = [(34, +1, +1, "repulsão"), (92, -1, -1, "repulsão"), (150, +1, -1, "atração")]
    for y, qa, qb, txt in rows:
        xa, xb = 112, 220
        f.charge(xa, y, qa, 12)
        f.charge(xb, y, qb, 12)
        if txt == "repulsão":
            f.arrow(xa - 15, y, xa - 58, y, INK, 2.4, 9)
            f.arrow(xb + 15, y, xb + 58, y, INK, 2.4, 9)
            f.text(xa - 36, y - 9, "$\\vec F_{12}$", 12.5, INK)
            f.text(xb + 36, y - 9, "$\\vec F_{21}$", 12.5, INK)
        else:
            f.arrow(xa + 15, y, xa + 50, y, INK, 2.4, 9)
            f.arrow(xb - 15, y, xb - 50, y, INK, 2.4, 9)
            f.text(xa + 33, y - 9, "$\\vec F_{12}$", 12.5, INK)
            f.text(xb - 33, y - 9, "$\\vec F_{21}$", 12.5, INK)
        f.text(8, y + 4, txt, 11.5, INK, anchor="start", weight=600)
    f.text(324, 172, "|F₁₂| = |F₂₁|  (3ª lei de Newton)", 10.5, MUTED, anchor="end")
    return f


@fig("cond_iso")
def cond_iso():
    f = Fig(332, 164, title="Condutor: elétrons livres. Isolante: elétrons presos aos átomos")
    import random
    rnd = random.Random(4)
    for k, (x0, title) in enumerate(((0, "Condutor (metal)"), (172, "Isolante"))):
        f.text(x0 + 80, 13, title, 12, INK, weight=700)
        f.rect(x0, 22, 160, 112, "#fff", GRY_M, 1.3, rx=6, tag="bg")
        for i in range(4):
            for j in range(3):
                cx, cy = x0 + 22 + i * 39, 44 + j * 36
                f.circ(cx, cy, 8.5, GRY_XL, GRY, 1.4, tag="bg")
                f.line(cx - 3.4, cy, cx + 3.4, cy, GRY, 1.2, tag="bg")
                f.line(cx, cy - 3.4, cx, cy + 3.4, GRY, 1.2, tag="bg")
                if k == 1:   # elétrons presos: órbita curta
                    ex, ey = cx + 13 * math.cos(1.0 + i + j), cy + 13 * math.sin(1.0 + i + j)
                    f.circ(cx, cy, 13, "none", GRY_L, 1, dash="2 2", tag="bg")
                    f.circ(ex, ey, 3.2, NEG, NEG, 1, tag="bg")
        if k == 0:
            pts = [(34, 61), (62, 80), (95, 52), (125, 78), (150, 56), (48, 100), (86, 112), (118, 108), (140, 120), (20, 124), (70, 40), (110, 36)]
            for (px, py) in pts:
                f.circ(x0 + px, py, 3.4, NEG, NEG, 1, tag="bg")
                a = rnd.uniform(0, 6.28)
                f.arrow(x0 + px + 4 * math.cos(a), py + 4 * math.sin(a), x0 + px + 13 * math.cos(a), py + 13 * math.sin(a), NEG, 1.1, 5, 0.5, tag="bg")
        txt = ("elétrons livres percorrem o material:", "a carga se espalha e circula") if k == 0 else (
            "elétrons presos aos átomos:", "a carga fica onde foi colocada")
        f.text(x0 + 80, 148, txt[0], 10.5, MUTED)
        f.text(x0 + 80, 160, txt[1], 10.5, MUTED)
    return f


@fig("polariza")
def polariza():
    f = Fig(332, 150, title="Polarização de um isolante neutro por um bastão negativo")
    f.rect(8, 52, 78, 22, GRY_XL, GRY, 1.6, rx=11, tag="bg")
    for k in range(3):
        px = 42 + k * 15
        f.line(px - 3.4, 63, px + 3.4, 63, NEG, 1.7, tag="bg")
    f.text(47, 94, "bastão (−)", 11.5, NEG_D, weight=600)
    f.rect(138, 20, 150, 104, "#fff", GRY, 1.5, rx=6, tag="bg")
    f.text(213, 14, "isolante neutro", 11.5, INK, weight=600)
    for i in range(3):
        for j in range(3):
            cx, cy = 168 + i * 48, 42 + j * 34
            f.ell(cx, cy, 15, 9, "#fff", GRY_M, 1.2, tag="bg")
            f.line(cx - 10, cy, cx - 4, cy, POS, 1.5, tag="bg")
            f.line(cx - 7, cy - 3, cx - 7, cy + 3, POS, 1.5, tag="bg")
            f.line(cx + 4, cy, cx + 10, cy, NEG, 1.5, tag="bg")
    f.arrow(130, 74, 96, 74, INK, 2.4, 9)
    f.text(113, 66, "$\\vec F$", 12.5, INK)
    f.text(213, 142, "polos + (coral) ficam mais perto do bastão", 10.5, MUTED)
    return f


@fig("atrito")
def atrito():
    f = Fig(332, 188, title="Eletrização por atrito")
    f.text(8, 14, "antes (neutros)", 11.5, INK, anchor="start", weight=700)
    _body(f, 8, 22, 98, 50, 4, 4)
    _body(f, 112, 22, 98, 50, 4, 4)
    f.text(57, 86, "A", 12, INK)
    f.text(161, 86, "B", 12, INK)
    f.text(226, 50, "atritando A com B", 11, MUTED, anchor="start")
    f.line(8, 100, 324, 100, RULE, 1, tag="bg")
    f.text(8, 118, "depois (2 elétrons passam de A para B)", 11.5, INK, anchor="start", weight=700)
    _body(f, 8, 128, 98, 40, 4, 2)
    _body(f, 130, 128, 98, 40, 4, 6)
    f.arrow(110, 152, 126, 152, NEG, 2.2, 8)
    f.text(118, 144, "e⁻", 10.5, NEG_D)
    f.text(57, 182, "A:  $Q=+2e$", 11.5, POS_D, weight=600)
    f.text(179, 182, "B:  $Q=-2e$", 11.5, NEG_D, weight=600)
    f.text(240, 152, "soma: 0", 11.5, INK, anchor="start", weight=600)
    f.text(240, 166, "(carga conservada)", 10.5, MUTED, anchor="start")
    return f


@fig("contato")
def contato():
    f = Fig(332, 152, title="Eletrização por contato entre esferas idênticas")
    rows = [(30, "antes", ("+6 µC", "−2 µC"), (POS, NEG), 56), (76, "contato", ("", ""), (GRY, GRY), 0), (122, "depois", ("+2 µC", "+2 µC"), (POS, POS), 56)]
    for y, lab, vals, cols, gap in rows:
        f.text(8, y + 4, lab, 11.5, INK, anchor="start", weight=700)
        xa = 140
        xb = xa + (46 if gap == 0 else 78)
        f.circ(xa, y, 21, GRY_XL, GRY, 1.8, tag="bg")
        f.circ(xb, y, 21, GRY_XL, GRY, 1.8, tag="bg")
        if vals[0]:
            f.text(xa, y + 4, vals[0], 11.5, POS_D if "+" in vals[0] else NEG_D, weight=700, lint=False)
            f.text(xb, y + 4, vals[1], 11.5, POS_D if "+" in vals[1] else NEG_D, weight=700, lint=False)
        if lab == "contato":
            f.text(xb + 34, y - 2, "elétrons passam", 10.5, MUTED, anchor="start")
            f.text(xb + 34, y + 11, "de B para A", 10.5, MUTED, anchor="start")
    return f


@fig("inducao")
def inducao():
    f = Fig(680, 176, title="Eletrização por indução em três etapas")
    W = 213
    titles = ["1  Aproxima-se o indutor", "2  Liga-se à Terra", "3  Desliga-se a Terra, afasta-se o indutor"]
    notes = [("elétrons livres são repelidos:", "as cargas se separam"), ("elétrons escoam para a Terra", "(o lado + permanece)"),
             ("o excesso de carga + se espalha:", "esfera final positiva")]
    for k in range(3):
        x0 = k * (W + 20)
        f.text(x0 + W / 2, 14, titles[k], 12, INK, weight=700)
        f.line(x0, 22, x0 + W, 22, RULE, 1, tag="bg")
        cx, cy, R = x0 + 140, 66, 34
        f.rect(cx - 10, cy + R, 20, 26, "#fff", GRY, 1.4, tag="bg")
        for h in range(3):
            f.line(cx - 10, cy + R + 7 + h * 7, cx + 10, cy + R + 2 + h * 7, GRY_L, 1, tag="bg")
        f.rect(cx - 24, cy + R + 26, 48, 6, GRY_XL, GRY, 1.2, tag="bg")
        f.circ(cx, cy, R, GRY_XL, GRY, 2.4, tag="bg")

        def sg(a, ch, col, rad=R - 12, size=17):
            f.text(cx + rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a)) + 5.6, ch, size, col, weight=700, lint=False)
        if k == 0:
            for a_ in (150, 180, 210):
                sg(a_, "+", POS_D)
            for a_ in (-30, 0, 30):
                sg(a_, "−", NEG_D)
        if k == 1:
            for a_ in (150, 180, 210):
                sg(a_, "+", POS_D)
            f.pl([(cx + R, cy), (cx + R + 24, cy), (cx + R + 24, 128)], INK, 2.0)
            f.ground(cx + R + 24, 128)
            f.arrow(cx + R + 24, cy + 4, cx + R + 24, cy + 38, NEG, 2.4, 9)
            f.text(cx + R + 32, cy + 26, "e⁻", 11.5, NEG_D, anchor="start", weight=600)
        if k < 2:
            f.rect(x0 + 6, cy - 9, 70, 18, GRY_XL, GRY, 1.6, rx=9, tag="bg")
            for m in range(3):
                f.line(x0 + 17 + m * 11, cy, x0 + 24 + m * 11, cy, NEG, 1.7, tag="bg")
            f.text(x0 + 41, cy + 28, "bastão (−)", 10.5, NEG_D, weight=600)
        else:
            for a_ in range(0, 360, 60):
                sg(a_, "+", POS_D)
        f.text(x0 + W / 2, 148, notes[k][0], 11, MUTED)
        f.text(x0 + W / 2, 162, notes[k][1], 11, MUTED)
    return f


@fig("eletroscopio")
def eletroscopio():
    f = Fig(680, 178, title="Eletroscópio de folhas: neutro, carregado e sob indução")
    W = 213
    panels = [("Neutro", 0, None, "folhas juntas"), ("Carregado (+)", 26, "c", "folhas se repelem (mesmo sinal)"),
              ("Bastão (−) próximo, sem tocar", 20, "i", "as folhas se repelem mesmo sem contato")]
    for k, (title, ang, mode, note) in enumerate(panels):
        x0 = k * (W + 20)
        cx = x0 + 132
        f.text(x0 + W / 2, 14, title, 12, INK, weight=700)
        f.line(x0, 22, x0 + W, 22, RULE, 1, tag="bg")
        f.path(f"M{cx-36},50 L{cx-36},128 Q{cx-36},144 {cx-20},144 L{cx+20},144 Q{cx+36},144 {cx+36},128 L{cx+36},50", GRY_L, 2.0)
        f.line(cx, 46, cx, 88, GRY, 3.4)
        f.circ(cx, 38, 12, GRY_XL, GRY, 2.2, tag="bg")
        for s_ in (-1, 1):
            ex, ey = cx + s_ * 40 * math.sin(math.radians(ang)), 88 + 40 * math.cos(math.radians(ang))
            f.line(cx, 88, ex, ey, GRY, 4.2)
        def sg(x, y, ch, col):
            f.text(x, y + 4.5, ch, 14, col, weight=700, lint=False)
        if mode == "c":
            sg(cx, 38, "+", POS_D)
            for s_ in (-1, 1):
                sg(cx + s_ * 40 * math.sin(math.radians(ang)) * 0.8 + s_ * 8, 88 + 40 * math.cos(math.radians(ang)) * 0.8, "+", POS_D)
        if mode == "i":
            f.rect(x0 + 2, 29, 62, 18, GRY_XL, GRY, 1.6, rx=9, tag="bg")
            for m in range(3):
                f.line(x0 + 12 + m * 10, 38, x0 + 18 + m * 10, 38, NEG, 1.7, tag="bg")
            sg(cx - 3, 38, "+", POS_D)
            for s_ in (-1, 1):
                sg(cx + s_ * 40 * math.sin(math.radians(ang)) * 0.8 + s_ * 8, 88 + 40 * math.cos(math.radians(ang)) * 0.8, "−", NEG_D)
        f.text(x0 + W / 2, 168, note, 11, MUTED)
    return f


@fig("coulomb_r")
def coulomb_r():
    f = Fig(332, 202, title="Força de Coulomb para as distâncias r, 2r e 3r")
    rows = [(30, 60, 54, "$F$"), (94, 120, 13.5, "$F/4$"), (158, 180, 6, "$F/9$")]
    for y, d, L, lab in rows:
        xa, xb = 34, 34 + d
        f.charge(xa, y, +1, 10)
        f.charge(xb, y, +1, 10)
        f.line(xa, y + 24, xb, y + 24, GRY, 1.1, tag="bg")
        f.arrow(xa, y + 24, xb, y + 24, GRY, 1.1, 6, 0.4, both=True)
        f.text((xa + xb) / 2, y + 38, {60: "$r$", 120: "$2r$", 180: "$3r$"}[d], 12, INK)
        f.arrow(xb + 12, y, xb + 12 + L, y, INK, 2.6, 9 if L > 10 else 6)
        f.text(xb + 12 + L + 6, y + 4, lab, 12.5, INK, anchor="start")
    return f


@fig("coulomb_graf")
def coulomb_graf():
    f = Fig(332, 166, title="Gráfico F × r da lei de Coulomb")
    P = Plot(f, 52, 138, 252, 108, (0, 3.5), (0, 1.25), xticks=[(1, "$r_0$"), (2, "$2r_0$"), (3, "$3r_0$")],
             yticks=[(1, "$F_0$"), (0.25, "$F_0/4$"), (0.111, "$F_0/9$")], grid=False, tick_size=11)
    P.axis_labels("$r$", "$F$")
    P.curve(lambda r: 1 / r ** 2, 0.93, 3.4, 90, c=EFD, w=2.6)
    for r, F in ((1, 1), (2, 0.25), (3, 1 / 9)):
        P.guide(x=r, y=F, c=GRY_M)
        P.point(r, F, INK, 3.8)
    f.text(P.X(1.55), P.Y(0.9), "$F\\propto 1/r^{2}$", 13, EFD_D, anchor="start", weight=600)
    f.text(P.X(1.55), P.Y(0.72), "dobrar $r$ ⇒ $F$ cai a ¼", 11.5, INK, anchor="start")
    return f


@fig("inv_sq")
def inv_sq():
    f = Fig(332, 166, title="A mesma 'quantidade de linhas' cobre área 4 vezes maior ao dobrar a distância")
    S = (26, 88)
    c0, u, v = (116, 106), (0, -38), (14, -9)

    def corners(k):
        pts = [c0, (c0[0] + u[0], c0[1] + u[1]), (c0[0] + u[0] + v[0], c0[1] + u[1] + v[1]), (c0[0] + v[0], c0[1] + v[1])]
        return [(S[0] + k * (p[0] - S[0]), S[1] + k * (p[1] - S[1])) for p in pts]
    c1, c2 = corners(1), corners(2)
    f.pl(c2, EFD, 1.6, fill=EFD_L, close=True, fop=0.55, tag="bg")
    a = [((c2[0][0] + c2[1][0]) / 2, (c2[0][1] + c2[1][1]) / 2), ((c2[3][0] + c2[2][0]) / 2, (c2[3][1] + c2[2][1]) / 2)]
    b = [((c2[0][0] + c2[3][0]) / 2, (c2[0][1] + c2[3][1]) / 2), ((c2[1][0] + c2[2][0]) / 2, (c2[1][1] + c2[2][1]) / 2)]
    f.line(*a[0], *a[1], EFD, 1.1, tag="bg")
    f.line(*b[0], *b[1], EFD, 1.1, tag="bg")
    f.pl(c1, EFD_D, 1.8, fill=EFD, close=True, fop=0.55, tag="bg")
    for p in c2:
        f.line(S[0], S[1], p[0], p[1], GRY, 1.1, "4 3", tag="bg")
    f.charge(S[0], S[1], +1, 10)
    f.text(c1[0][0] + 8, 150, "área $A$", 12, INK)
    f.text(c2[0][0] + 22, 150, "área $4A$", 12, INK)
    f.arrow(S[0], 128, c1[0][0] - 2, 128, GRY, 1.1, 6, 0.4, both=True)
    f.text(64, 142, "$r$", 12, INK)
    f.text(40, 14, "mesmas 4 linhas (tracejadas)", 11, MUTED, anchor="start")
    f.text(40, 27, "→ densidade ÷ 4", 11, INK, anchor="start", weight=600)
    return f


@fig("tri_coulomb")
def tri_coulomb():
    f = Fig(332, 236, title="Exemplo 4: forças sobre a carga A (triângulo retângulo)")
    A, B, C = (112, 190), (262, 190), (112, 40)
    f.line(A[0], A[1], B[0], B[1], GRY_M, 1.2, "5 4", tag="bg")
    f.line(A[0], A[1], C[0], C[1], GRY_M, 1.2, "5 4", tag="bg")
    f.arrow(A[0] + 44, 218, B[0] - 20, 218, GRY, 1.1, 6, 0.4, both=True)
    f.text(188, 232, "0,30 m", 11.5, INK)
    f.arrow(166, C[1] + 24, 166, A[1] - 24, GRY, 1.1, 6, 0.4, both=True)
    f.text(174, 120, "0,30 m", 11.5, INK, anchor="start")
    s = 120   # px por newton
    # forças em A
    f.line(A[0] - 0.6 * s, A[1], A[0] - 0.6 * s, A[1] - 0.6 * s, GRY, 1.1, "4 3", tag="bg")
    f.line(A[0], A[1] - 0.6 * s, A[0] - 0.6 * s, A[1] - 0.6 * s, GRY, 1.1, "4 3", tag="bg")
    f.arrow(A[0], A[1], A[0] - 0.6 * s, A[1], INK, 2.6, 10)
    f.arrow(A[0], A[1], A[0], A[1] - 0.6 * s, INK, 2.6, 10)
    f.arrow(A[0], A[1], A[0] - 0.6 * s, A[1] - 0.6 * s, INK, 3.6, 12)
    f.text(A[0] - 36, A[1] + 15, "$\\vec F_{B}$", 12.5, INK)
    f.text(A[0] + 20, A[1] - 24, "$\\vec F_{C}$", 12.5, INK, anchor="start")
    f.text(A[0] - 56, A[1] - 0.6 * s - 8, "$\\vec F_R$", 13, INK, anchor="end")
    f.charge(*A, +1, 12)
    f.charge(*B, +1, 12)
    f.charge(*C, -1, 12)
    f.text(A[0] + 20, A[1] + 22, "A  (+2,0 µC)", 11.5, POS_D, anchor="start", weight=600)
    f.text(B[0], B[1] - 20, "B (+3,0 µC)", 11.5, POS_D, weight=600)
    f.text(C[0] + 18, C[1] + 5, "C (−3,0 µC)", 11.5, NEG_D, anchor="start", weight=600)
    return f


@fig("ex_coulomb2")
def ex_coulomb2():
    f = Fig(332, 132, title="Exemplo 2: duas cargas positivas a 30 cm")
    xa, xb, y = 112, 202, 44
    f.charge(xa, y, +1, 12)
    f.charge(xb, y, +1, 12)
    f.arrow(xa - 14, y, xa - 14 - 12, y, INK, 2.6, 8)
    f.arrow(xb + 14, y, xb + 14 + 12, y, INK, 2.6, 8)
    f.text(xa - 14, y - 13, "0,60 N", 11.5, INK, anchor="end")
    f.text(xb + 14, y - 13, "0,60 N", 11.5, INK, anchor="start")
    f.arrow(xa, y + 30, xb, y + 30, GRY, 1.1, 6, 0.4, both=True)
    f.text((xa + xb) / 2, y + 46, "$r$ = 30 cm", 11.5, INK)
    f.text(xa, y + 66, "+2,0 µC", 11.5, POS_D, weight=600)
    f.text(xb, y + 66, "+3,0 µC", 11.5, POS_D, weight=600)
    f.text(166, 127, "setas na escala de 20 px por newton", 10, MUTED)
    return f


@fig("ex_coulomb3")
def ex_coulomb3():
    f = Fig(332, 132, title="Exemplo 3: as mesmas cargas a 10 cm")
    xa, xb, y = 138, 168, 44
    f.charge(xa, y, +1, 12)
    f.charge(xb, y, +1, 12)
    f.arrow(xa - 14, y, xa - 14 - 108, y, INK, 2.8, 10)
    f.arrow(xb + 14, y, xb + 14 + 108, y, INK, 2.8, 10)
    f.text(xa - 14 - 54, y - 13, "5,4 N", 11.5, INK)
    f.text(xb + 14 + 54, y - 13, "5,4 N", 11.5, INK)
    f.arrow(xa, y + 30, xb, y + 30, GRY, 1.1, 6, 0.4, both=True)
    f.text((xa + xb) / 2, y + 46, "$r$ = 10 cm", 11.5, INK)
    f.text(xa - 14, y + 66, "+2,0 µC", 11.5, POS_D, weight=600, anchor="end")
    f.text(xb + 14, y + 66, "+3,0 µC", 11.5, POS_D, weight=600, anchor="start")
    f.text(166, 127, "mesma escala: 20 px por newton", 10, MUTED)
    return f
