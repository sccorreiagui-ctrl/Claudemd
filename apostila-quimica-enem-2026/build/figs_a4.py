"""Bloco A · página 6 — forças intermoleculares."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw
from figlib import pol, water, sphere_h, chip_svg

INK = C["ink"]
BLUE, BLUED = C["blue"], C["blue_d"]
AMB, AMBD = C["amber"], C["amber_d"]


def _ang_from_to(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


@fig("a_if_london")
def _london():
    W, H = 176, 122
    s = SVG(W, H, title="Dispersão de London")
    for cx in (48, 128):
        s.circle(cx, 40, 30, fill=C["amber_l"], stroke=C["amber_m"], sw=1.4)
        s.circle(cx - 8, 40, 19, fill=C["amber_m"], opacity=0.55)
        s.circle(cx + 4, 40, 3.2, fill=INK)
    s.text(21, 44, "δ−", 10.5, "middle", 700, AMBD)
    s.text(70, 44, "δ+", 10.5, "middle", 700, AMBD)
    s.text(101, 44, "δ−", 10.5, "middle", 700, AMBD)
    s.text(150, 44, "δ+", 10.5, "middle", 700, AMBD)
    s.line(77, 40, 98, 40, AMBD, 1.8, dash="2 2.5")
    s.text(48, 88, "dipolo", 9.8, "middle", 700, AMBD)
    s.text(48, 99, "instantâneo", 9.8, "middle", 700, AMBD)
    s.text(128, 88, "dipolo", 9.8, "middle", 700, AMBD)
    s.text(128, 99, "induzido", 9.8, "middle", 700, AMBD)
    s.text(88, 117, "atração fraca e momentânea", 9.6, "middle", 600, C["muted"])
    return s


@fig("a_if_dd")
def _dd():
    W, H = 176, 122
    s = SVG(W, H, title="Dipolo permanente–dipolo permanente")

    def hcl(x, y, flip=False):
        h, c = (x, x + 34) if not flip else (x + 34, x)
        s.line(h, y, c, y, "#6B7280", 3)
        sphere_h(s, h, y, 6.5, "#FFFFFF", "#6B7280", "H", INK, 8.5)
        sphere_h(s, c, y, 11, "#3DB36B", "#1F7A45", "Cl", "#fff", 10.5)
        return h, c
    h1, c1 = hcl(16, 28)
    h2, c2 = hcl(104, 28)
    s.text(h1, 12, "δ+", 9.8, "middle", 700, BLUED)
    s.text(c1, 10, "δ−", 9.8, "middle", 700, BLUED)
    s.text(h2, 12, "δ+", 9.8, "middle", 700, BLUED)
    s.text(c2, 10, "δ−", 9.8, "middle", 700, BLUED)
    s.line(c1 + 12, 28, h2 - 8, 28, BLUED, 1.8, dash="2.5 2.5")
    s.text(88, 52, "cabeça com cauda", 9.6, "middle", 600, C["muted"])
    # antiparalelas
    ha, ca = hcl(22, 76)
    hb, cb = hcl(22, 104, flip=True)
    for xx in (ha, ca):
        s.line(xx, 84, xx, 96, BLUED, 1.6, dash="2.5 2.5")
    s.text(104, 84, "polos opostos", 10, "start", 700, BLUED)
    s.text(104, 96, "se alinham e", 10, "start", 600, C["muted"])
    s.text(104, 108, "se atraem", 10, "start", 600, C["muted"])
    return s


@fig("a_if_hb")
def _hb():
    W, H = 176, 122
    s = SVG(W, H, title="Ligação de hidrogênio na água")
    OA, OB, OC = (28, 40), (86, 74), (146, 38)
    a_ab = _ang_from_to(OA, OB)
    a_bc = _ang_from_to(OB, OC)
    sc = 0.86
    L = 21 * sc
    hA = pol(OA[0], OA[1], L, a_ab)
    hB = pol(OB[0], OB[1], L, a_bc)
    s.line(hA[0], hA[1], OB[0], OB[1], BLUED, 2.2, dash="3 2.6")
    s.line(hB[0], hB[1], OC[0], OC[1], BLUED, 2.2, dash="3 2.6")
    water(s, OA[0], OA[1], a_ab, a_ab + 104.5, sc, True)
    water(s, OB[0], OB[1], a_bc, a_bc + 104.5, sc, True)
    water(s, OC[0], OC[1], 25, 25 + 104.5, sc, True)
    s.text(88, 108, "O–H···O  (tracejado = lig. de H)", 9.6, "middle", 700, BLUED)
    s.text(88, 119, "", 8)
    return s


@fig("a_if_id")
def _ion_dipole():
    W, H = 176, 122
    s = SVG(W, H, title="Íon–dipolo")
    cx, cy = 88, 52
    for phi in (-90, 0, 90, 180):
        ox, oy = pol(cx, cy, 36, phi)
        s.line(cx, cy, ox, oy, BLUED, 1.6, dash="2.5 2.5")
    for phi in (-90, 0, 90, 180):
        ox, oy = pol(cx, cy, 36, phi)
        water(s, ox, oy, phi + 52.25, phi - 52.25, 0.66, False)
    sphere_h(s, cx, cy, 11.5, "#B79DFB", "#6D4BD0", "+", "#fff", 15)
    s.text(88, 112, "O (δ−) voltado para o cátion", 9.6, "middle", 600, C["muted"])
    return s


# ----------------------------------------------------------------------------- gráfico de PE dos hidretos
@fig("a_pe_hidretos")
def _hidretos():
    W, H = 458, 262
    s = SVG(W, H, title="Pontos de ebulição dos hidretos dos grupos 14 a 17")
    ax = Axes(s, 58, 14, 288, 196, 0.5, 4.5, -180, 120)
    ax.frame(xticks=[], yticks=[-160, -120, -80, -40, 0, 40, 80, 120], xlabel=None, ylabel=None, grid=True,
             xfmt=str, yfmt=lambda v: f"{v:d}".replace("-", "−"), arrows=True)
    # eixo x: períodos
    for i, per in enumerate([2, 3, 4, 5], start=1):
        x = ax.X(i)
        s.line(x, 210, x, 215, INK, 1.1)
        s.text(x, 228, f"{per}º período", 10.4, "middle", 600, C["muted"])
    s.text(ax.x0 + ax.w / 2, 247, "(a massa molar aumenta para a direita)", 10, "middle", 400, C["muted"])
    s.text(18, 112, "Ponto de ebulição (°C)", 10.8, "middle", 600, INK, rot=-90)
    s.line(ax.x0, ax.Y(0), ax.x0 + ax.w, ax.Y(0), C["slate_m"], 1.0, dash="4 3")
    data = {
        "16": ([100.0, -60.3, -41.4, -2.2], ["H_2O", "H_2S", "H_2Se", "H_2Te"], BLUE, None, 3.0),
        "17": ([19.5, -85.0, -66.8, -35.4], ["HF", "HCl", "HBr", "HI"], BLUE, "6 4", 2.2),
        "15": ([-33.3, -87.7, -62.5, -17.1], ["NH_3", "PH_3", "AsH_3", "SbH_3"], BLUE, "2 3", 2.2),
        "14": ([-161.5, -111.9, -88.5, -52.0], ["CH_4", "SiH_4", "GeH_4", "SnH_4"], AMB, None, 3.0),
    }
    for g, (vals, names, col, dash, sw) in data.items():
        pts = [(i + 1, v) for i, v in enumerate(vals)]
        ax.polyline(pts, col, sw, dash)
    for g, (vals, names, col, dash, sw) in data.items():
        for i, v in enumerate(vals):
            x, y = ax.X(i + 1), ax.Y(v)
            s.circle(x, y, 4.2, fill="#FFFFFF", stroke=col, sw=2)
    # rótulos de séries (coluna à direita, com linhas-guia)
    base = ax.Y(-2.2) - 22
    labs = [("grupo 16", -2.2, BLUED), ("grupo 15", -17.1, BLUED), ("grupo 17", -35.4, BLUED),
            ("grupo 14 (só London)", -52.0, AMBD)]
    for k, (t, v, col) in enumerate(labs):
        ly = base + 17 * k + 8
        px, py = ax.X(4) + 5, ax.Y(v)
        s.line(px, py, ax.X(4) + 20, ly - 3.5, col, 1.0)
        s.text(ax.X(4) + 23, ly, t, 10.2, "start", 700, col)
    # anomalias: círculos + nomes
    for (i, v, nm, dx, dy) in ((0, 100.0, "H_2O", 24, 4), (0, 19.5, "HF", 24, 4), (0, -33.3, "NH_3", 24, 4)):
        x, y = ax.X(i + 1), ax.Y(v)
        s.circle(x, y, 9.5, stroke=BLUED, sw=1.6)
        s.text(x + dx - 4, y + dy, nm, 10.6, "start", 800, BLUED, halo="#FFFFFF")
    s.text(ax.X(1) + 54, ax.Y(78), "ligações de hidrogênio", 10.4, "start", 700, BLUED)
    s.text(ax.X(1) + 54, ax.Y(78) + 12, "elevam muito o P.E.", 10.4, "start", 700, BLUED)
    s.text(ax.X(2) + 6, ax.Y(-128), "CH_4 → SnH_4", 10, "start", 600, AMBD)
    return s


# ----------------------------------------------------------------------------- P.E. e tipo de força (mesma massa molar)
@fig("a_pe_comparacao")
def _pe_comp():
    from mol import mol
    W, H = 695, 196
    s = SVG(W, H, title="Pontos de ebulição de substâncias de massa molar semelhante")
    items = [
        ("butano", "C_4H_{10}", "M = 58", -0.5, "London", "amber", mol("CCCC", bond=20, font=0.62, lw=1.6, formula="C4H10")),
        ("propanona", "C_3H_6O", "M = 58", 56.1, "dipolo–dipolo", "blue",
         mol("CC(=O)C", bond=20, font=0.62, lw=1.6, hl=["[CX3]=O"], formula="C3H6O")),
        ("propan-1-ol", "C_3H_8O", "M = 60", 97.2, "lig. de hidrogênio", "blue",
         mol("CCCO", bond=20, font=0.62, lw=1.6, hl=["[OX2H]"], formula="C3H8O")),
        ("éter dimetílico", "C_2H_6O", "M = 46", -24.8, "dipolo–dipolo (fraca)", "blue",
         mol("COC", bond=20, font=0.62, lw=1.6, hl=["[OD2]"], formula="C2H6O")),
        ("etanol", "C_2H_6O", "M = 46", 78.4, "lig. de hidrogênio", "blue",
         mol("CCO", bond=20, font=0.62, lw=1.6, hl=["[OX2H]"], formula="C2H6O")),
    ]
    cw = (W - 12) / 5
    for i, (nm, fml, M, bp, force, kind, m) in enumerate(items):
        x = 6 + cw * i
        cx = x + cw / 2
        s.raw(m.at(cx, 44, 1.0))
        s.text(cx, 92, nm, 11.6, "middle", 700, INK)
        s.text(cx, 105, fml + "  ·  " + M, 10, "middle", 400, C["muted"])
        # barra de P.E.
        bx0 = x + 10
        scale = (cw - 66) / 160.0
        zero = bx0 + 40 * scale
        s.line(zero, 114, zero, 150, C["slate_m"], 1.0, dash="3 2")
        L = (bp + 40) * scale
        col = C["amber"] if kind == "amber" else C["blue"]
        s.rect(bx0, 120, L, 15, fill=col, rx=3)
        val = ("%g" % bp).replace(".", ",").replace("-", "−")
        s.text(bx0 + L + 4, 132, f"{val} °C", 10.8, "start", 800, INK)
        chip_svg(s, cx, 158, force, kind, 9.6, padx=6, h=16)
    s.text(6 + cw * 3 - 0, 192, "", 8)
    s.line(6 + cw * 3, 8, 6 + cw * 3, 172, C["line"], 1.2, dash="4 3")
    s.text(6 + cw * 1.5, 182 + 8, "massa molar semelhante: a força decide", 10.4, "middle", 700, C["blue_d"])
    s.text(6 + cw * 4, 190, "isômeros: o grupo –OH decide", 10.4, "middle", 700, C["blue_d"])
    s.text(6 + cw * 4, 180, "", 8)
    return s
