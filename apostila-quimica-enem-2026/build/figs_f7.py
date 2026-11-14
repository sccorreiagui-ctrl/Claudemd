"""Bloco F · página 35 — radioatividade: radiações, meia-vida, fissão e fusão."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw

INK = C["ink"]
OD = C["orange_d"]
PD = C["purple_d"]


@fig("i_radiacoes")
def _radiacoes():
    W, H = 460, 214
    s = SVG(W, H, title="Poder de penetração das radiações alfa, beta e gama")
    rows = [
        (46, "α", "alfa", C["red"], C["red_d"], "^4He, carga +2", "ΔA −4 · ΔZ −2"),
        (108, "β", "beta", C["orange"], OD, "elétron, carga −1", "ΔA 0 · ΔZ +1"),
        (170, "γ", "gama", C["purple"], PD, "onda EM, neutra", "ΔA 0 · ΔZ 0"),
    ]
    x_src, x_pap, x_al, x_pb = 128, 214, 292, 366
    # barreiras
    s.rect(x_pap - 2, 14, 4, 186, fill="#E8D9B0", stroke="#B79B5C", sw=1)
    s.rect(x_al - 5, 14, 10, 186, fill="#C7CDD6", stroke=C["slate_m"], sw=1.2)
    s.rect(x_pb - 9, 14, 18, 186, fill="#4B5563", stroke="#111827", sw=1.2)
    s.text(x_pap, 10, "papel", 9.6, "middle", 800, C["slate"])
    s.text(x_al, 10, "Al (mm)", 9.6, "middle", 800, C["slate"])
    s.text(x_pb, 10, "Pb (cm)", 9.6, "middle", 800, C["slate"])
    s.rect(x_src - 8, 24, 8, 168, fill="#FDE8A8", stroke="#D49B1D", sw=1.4, rx=2)
    s.text(x_src - 4, 208, "fonte", 9.6, "middle", 800, C["slate"])
    for i, (y, g, nm, col, cold, nat, dz) in enumerate(rows):
        s.circle(18, y - 2, 13, fill=col)
        s.text(18, y + 3, g, 16, "middle", 800, "#FFFFFF")
        s.text(38, y - 9, nm, 12, "start", 800, cold)
        s.text(38, y + 3, nat, 9.2, "start", 600, C["muted"])
        s.text(38, y + 15, dz, 9.2, "start", 800, C["slate"])
        # raio
        if i == 0:
            xe = x_pap - 4
            s.arrow(x_src, y, xe, y, col, 3, 9)
            s.text(xe - 4, y - 8, "para aqui (até na pele)", 9.4, "end", 800, cold, halo="#fff")
        elif i == 1:
            xe = x_al - 8
            s.arrow(x_src, y, xe, y, col, 3, 9)
            s.text(xe - 4, y - 8, "para na folha de Al", 9.4, "end", 800, cold, halo="#fff")
        else:
            s.line(x_src, y, x_pb - 11, y, col, 3)
            s.line(x_pb + 11, y, 446, y, col, 1.6, dash="3 3", opacity=0.6)
            s.arrow(436, y, 448, y, col, 1.6, 6)
            s.text(x_pb - 14, y - 8, "atravessa; só é atenuada", 9.4, "end", 800, cold, halo="#fff")
    return s


@fig("i_meia_vida")
def _meia():
    W, H = 340, 226
    s = SVG(W, H, title="Decaimento radioativo: massa restante × número de meias-vidas")
    ax = Axes(s, 46, 18, 266, 158, 0, 5.2, 0, 108)
    ax.frame(xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 25, 50, 75, 100], xfmt=lambda v: str(int(v)),
             yfmt=lambda v: f"{int(v)}%", xlabel="nº de meias-vidas  x = t / t_{1/2}", ylabel=None, size=10)
    s.text(12, 98, "massa restante (% da inicial)", 10.2, "middle", 800, INK, rot=-90)
    f = lambda x: 100 * 2 ** (-x)
    ax.polyline(ax.curve_fn(f, 0, 5.1, 120), C["orange"], 3.2)
    labs = {0: "100%", 1: "50%", 2: "25%", 3: "12,5%", 4: "6,25%", 5: "3,1%"}
    for x, t in labs.items():
        px, py = ax.X(x), ax.Y(f(x))
        s.line(px, py, px, ax.Y(0), C["slate_m"], 1, dash="3 3")
        s.line(ax.X(0), py, px, py, C["slate_m"], 1, dash="3 3")
        s.circle(px, py, 4.2, fill="#FFFFFF", stroke=OD, sw=2)
        s.text(px + 9, py - 6, t, 10, "start", 800, OD, halo="#fff")
    s.text(ax.X(3.0), ax.Y(88), "m = m_0 / 2^x", 12.4, "middle", 800, INK)
    s.text(ax.X(3.0), ax.Y(88) + 13, "cada t_{1/2}: metade do que restava", 9.6, "middle", 600, C["muted"])
    return s


def _nuc(s, x, y, r, fill, stroke, label, size=10.4, lab_col=None):
    s.circle(x, y, r, fill=fill, stroke=stroke, sw=1.6)
    s.text(x, y + size * 0.36, label, size, "middle", 800, lab_col or INK)


@fig("i_fissao_fusao")
def _fis_fus():
    W, H = 695, 138
    s = SVG(W, H, title="Fissão e fusão nuclear")
    half = W / 2
    for i, (t, col) in enumerate((("FISSÃO · núcleo pesado se parte", OD), ("FUSÃO · núcleos leves se unem", PD))):
        s.rect(4 + i * half, 2, half - 8, H - 4, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(4 + i * half + (half - 8) / 2, 18, t, 11, "middle", 800, col)
    # fissão
    y = 68
    _nuc(s, 36, y, 6, "#FFFFFF", INK, "n", 8)
    s.arrow(44, y, 78, y, INK, 1.8, 7)
    _nuc(s, 112, y, 27, "#FDE8C8", C["orange"], "^235U", 12, OD)
    s.arrow(142, y - 8, 190, y - 22, OD, 2.2, 8)
    s.arrow(142, y + 8, 192, y + 22, OD, 2.2, 8)
    _nuc(s, 212, y - 27, 18, "#FFE0C2", C["orange"], "^141Ba", 10, OD)
    _nuc(s, 212, y + 28, 15, "#FFE0C2", C["orange"], "^92Kr", 9.6, OD)
    for dy in (-30, 0, 30):
        s.arrow(252, y + dy * 0.5, 292, y + dy, C["slate"], 1.4, 6)
        _nuc(s, 300, y + dy, 6, "#FFFFFF", INK, "n", 8)
    s.text(172, 128, "3 nêutrons livres → reação em cadeia + energia", 9.8, "middle", 700, C["slate"])
    # fusão
    x0 = half + 4
    y = 66
    _nuc(s, x0 + 36, y - 22, 13, "#EDE4FA", C["purple"], "^2H", 10.2, PD)
    _nuc(s, x0 + 36, y + 26, 16, "#EDE4FA", C["purple"], "^3H", 10.2, PD)
    s.arrow(x0 + 56, y - 14, x0 + 100, y - 2, PD, 2.2, 8)
    s.arrow(x0 + 58, y + 22, x0 + 100, y + 6, PD, 2.2, 8)
    _nuc(s, x0 + 130, y, 22, "#EDE4FA", C["purple"], "^4He", 11, PD)
    s.arrow(x0 + 156, y - 6, x0 + 214, y - 22, C["slate"], 1.4, 6)
    _nuc(s, x0 + 226, y - 26, 6, "#FFFFFF", INK, "n", 8)
    s.arrow(x0 + 156, y + 8, x0 + 214, y + 20, C["red"], 2, 7)
    s.text(x0 + 220, y + 30, "+ energia", 10.4, "start", 800, C["red_d"])
    s.text(half + 4 + (half - 8) / 2, 128, "Sol e estrelas · exige temperatura da ordem de 10^7 K", 9.6, "middle", 700, C["slate"])
    return s
