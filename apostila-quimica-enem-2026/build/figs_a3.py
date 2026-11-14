"""Bloco A · página 5 — fluxograma polar/apolar e solubilidade de álcoois (cadeia apolar)."""
import math

from registry import fig
from svglib import SVG, C, tw
from figlib import chip_svg, zigzag


def _node(s, x, y, w, h, fill, stroke, rx=12):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=rx)


def _badge(s, x, y, t):
    s.circle(x, y, 9, fill=C["slate"])
    s.text(x, y + 3.6, t, 11, "middle", 700, "#FFFFFF")


@fig("a_fluxo_polar")
def _fluxo():
    W, H = 695, 228
    s = SVG(W, H, title="Fluxograma: molécula polar ou apolar?")
    sl, slm = C["slate_l"], C["slate_m"]
    ink = C["ink"]
    # decisões
    y0, h0 = 12, 76
    nodes = [(6, 160, "Existe alguma ligação", "polar na molécula?", "(átomos com EN diferentes)", "1"),
             (204, 150, "A molécula tem", "só 2 átomos?", "(diatômica)", "2"),
             (392, 297, "O átomo central tem par livre", "ou os ligantes são diferentes?", "(assimetria dos vetores μ)", "3")]
    for x, w, l1, l2, l3, b in nodes:
        _node(s, x, y0, w, h0, sl, slm)
        _badge(s, x + 14, y0 + 14, b)
        s.text(x + w / 2 + 8, y0 + 30, l1, 11.8, "middle", 700, ink)
        s.text(x + w / 2 + 8, y0 + 45, l2, 11.8, "middle", 700, ink)
        s.text(x + w / 2 + 8, y0 + 62, l3, 10, "middle", 400, C["muted"])
    # setas horizontais
    s.arrow(166, y0 + h0 / 2, 204, y0 + h0 / 2, C["slate"], 1.8, 7)
    s.text(185, y0 + h0 / 2 - 6, "sim", 10.5, "middle", 700, C["slate"], halo="#fff")
    s.arrow(354, y0 + h0 / 2, 392, y0 + h0 / 2, C["slate"], 1.8, 7)
    s.text(373, y0 + h0 / 2 - 6, "não", 10.5, "middle", 700, C["slate"], halo="#fff")
    # nós finais
    ye, he = 140, 84
    ends = [
        (6, 160, "amber", "APOLAR", "sem ligação polar", "O_2, N_2, Cl_2, hidrocarbonetos"),
        (204, 150, "blue", "POLAR", "ligação polar única", "HCl, HF, CO, NO"),
        (392, 142, "blue", "POLAR · μ_R ≠ 0", "vetores não se anulam", "H_2O, NH_3, SO_2, CH_3Cl"),
        (547, 142, "amber", "APOLAR · μ_R = 0", "vetores se anulam", "CO_2, CH_4, CCl_4, BF_3"),
    ]
    for x, w, kind, t1, t2, t3 in ends:
        fill, stroke, dark = ((C["blue_l"], C["blue"], C["blue_d"]) if kind == "blue"
                              else (C["amber_l"], C["amber"], C["amber_d"]))
        _node(s, x, ye, w, he, fill, stroke)
        s.text(x + w / 2, ye + 20, t1, 12.6, "middle", 800, dark)
        s.text(x + w / 2, ye + 36, t2, 10, "middle", 400, C["muted"])
        s.text(x + w / 2, ye + 56, t3, 10.4, "middle", 700, dark)
    # setas verticais
    for xc, lab in ((86, "não"), (279, "sim"), (463, "sim"), (618, "não")):
        s.arrow(xc, y0 + h0, xc, ye, C["slate"], 1.8, 7)
        s.text(xc + 14, (y0 + h0 + ye) / 2 + 4, lab, 10.5, "start", 700, C["slate"], halo="#fff")
    return s


# ----------------------------------------------------------------------------- solubilidade dos álcoois
@fig("a_alcoois")
def _alcoois():
    W, H = 695, 232
    s = SVG(W, H, title="Solubilidade em água de álcoois lineares")
    x0, x1 = 64, 676
    y0, y1 = 24, 150  # topo e base do gráfico
    import math as m
    ymin, ymax = -2.0, 2.0  # log10 g/100 mL (0,01 a 100)

    def Y(v):
        return y1 - (m.log10(v) - ymin) / (ymax - ymin) * (y1 - y0)

    # grade
    for lv, lab in ((-2, "0,01"), (-1, "0,1"), (0, "1"), (1, "10"), (2, "100")):
        yy = y1 - (lv - ymin) / (ymax - ymin) * (y1 - y0)
        s.line(x0, yy, x1, yy, C["grid"], 0.9)
        s.line(x0 - 3.5, yy, x0, yy, C["ink"], 1.1)
        s.text(x0 - 7, yy + 3.6, lab, 10, "end", 400, C["muted"])
    s.arrow(x0, y1, x1 + 6, y1, C["ink"], 1.4, 6)
    s.arrow(x0, y1, x0, y0 - 8, C["ink"], 1.4, 6)
    s.text(20, (y0 + y1) / 2, "g / 100 mL de água (log)", 10.5, "middle", 600, C["ink"], rot=-90)

    data = [
        (1, "metanol", None), (2, "etanol", None), (3, "1-propanol", None),
        (4, "1-butanol", 7.5), (5, "1-pentanol", 2.2), (6, "1-hexanol", 0.6), (7, "1-heptanol", 0.17),
        (8, "1-octanol", 0.054),
    ]
    step = (x1 - x0) / len(data)
    bw = 44
    hatch = s.pat_hatch(C["blue"], "#D9E8FB", 5, 1.3)
    shades = ["#F4D27A", "#EDBE4F", "#E5AB2C", "#DD9A12", "#D99100"]

    for i, (n_c, name, val) in enumerate(data):
        cx = x0 + step * (i + 0.5)
        col = shades[max(0, i - 3)] if i >= 3 else C['blue']
        if val is None:
            s.rect(cx - bw / 2, y0, bw, y1 - y0, fill=hatch, stroke=C["blue"], sw=1.3, rx=3)
            s.text(cx, y0 + 40, "miscível", 10.4, "middle", 700, C["blue_d"], halo="#D9E8FB")
            s.text(cx, y0 + 53, "em qualquer", 10, "middle", 600, C["blue_d"], halo="#D9E8FB")
            s.text(cx, y0 + 65, "proporção", 10, "middle", 600, C["blue_d"], halo="#D9E8FB")
        else:
            top = Y(val)
            s.rect(cx - bw / 2, top, bw, y1 - top, fill=col, stroke="#FFFFFF", sw=1, rx=3)
            vtxt = ("%g" % val).replace(".", ",")
            s.text(cx, top - 5, "≈ " + vtxt, 10.5, "middle", 700, C["ink"])
        # esqueleto: cauda apolar (âmbar) + OH (azul)
        w_tot = n_c * 6.4
        sx = cx - w_tot / 2
        sy = y1 + 33
        pts = [(sx, sy)]
        up = False
        for k in range(n_c):
            sx2 = pts[-1][0] + 6.4
            sy2 = pts[-1][1] + (-5.2 if up else 5.2)
            pts.append((sx2, sy2))
            up = not up
        chain = pts[:-1]
        s.poly(chain + [pts[-1]], stroke=C["amber"], sw=2.2, close=False)
        s.circle(pts[-1][0], pts[-1][1], 3.2, fill=C["blue"])
        s.text(pts[-1][0] + 5, pts[-1][1] + 3.2, "OH", 9.4, "start", 800, C["blue_d"])
        s.text(cx, y1 + 16, f"C{n_c}", 10.5, "middle", 700, C["muted"])
        s.text(cx, y1 + 58, name, 10.3, "middle", 600, C["ink"])
    # legenda
    s.line(x0 + 4, H - 12, x0 + 26, H - 12, C["amber"], 2.4)
    s.text(x0 + 32, H - 8.5, "cauda hidrocarbônica (apolar)", 10, "start", 600, C["amber_d"])
    s.circle(x0 + 218, H - 12, 3.4, fill=C["blue"])
    s.text(x0 + 226, H - 8.5, "grupo –OH (polar)", 10, "start", 600, C["blue_d"])
    s.text(x1, H - 8.5, "valores aproximados a 20–25 °C (ordem de grandeza)", 9.6, "end", 400, C["muted"])
    return s
