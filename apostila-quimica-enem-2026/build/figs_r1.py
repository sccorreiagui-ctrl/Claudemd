"""Revisão final · página 39 — mapa conceitual dos blocos."""
import math

from registry import fig
from svglib import SVG, C, tw

INK = C["ink"]

TH = {  # fill, stroke, texto forte
    "A": ("#E6F0FD", C["blue"], C["blue_d"]),
    "B": ("#F0E9FE", C["purple"], C["purple_d"]),
    "C": ("#FFEBDC", C["orange"], C["orange_d"]),
    "D": ("#EEF2F7", C["slate_m"], C["slate"]),
    "E": ("#E4F5EB", C["green"], C["green_d"]),
    "F": ("#FFEBDC", C["orange"], C["orange_d"]),
}

NW, NH = 150, 40


def _node(s, cx, cy, kind, title, sub, hub=False, dual=False):
    fill, stroke, strong = TH[kind]
    x, y = cx - NW / 2, cy - NH / 2
    s.rect(x, y, NW, NH, fill=fill, stroke=stroke, sw=2.6 if hub else 1.6, rx=9)
    if dual:   # tensoativos: metade azul (polar) / metade âmbar (apolar)
        s.rect(x + 1, y + 1, NW / 2 - 1, 5, fill=C["blue"], rx=2)
        s.rect(x + NW / 2, y + 1, NW / 2 - 1, 5, fill=C["amber"], rx=2)
    s.text(cx, cy - 3, title, 10.4, "middle", 800, strong)
    s.text(cx, cy + 10, sub, 8.8, "middle", 600, C["slate"])


def _edge(s, p, q, label=None, col=None, lab_dx=0, lab_dy=0, anchor="middle", dash=None):
    """Seta de p a q (centros de nós); recorta nas bordas do retângulo."""
    col = col or C["slate_m"]
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1

    def clip(cx, cy, ux, uy):
        tx = (NW / 2 + 3) / abs(ux) if abs(ux) > 1e-9 else 1e9
        ty = (NH / 2 + 3) / abs(uy) if abs(uy) > 1e-9 else 1e9
        t = min(tx, ty)
        return cx + ux * t, cy + uy * t
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    a = clip(x1, y1, ux, uy)
    b = clip(x2, y2, -ux, -uy)
    s.arrow(a[0], a[1], b[0], b[1], col, 1.9, 7, dash=dash)
    if label:
        mx, my = (a[0] + b[0]) / 2 + lab_dx, (a[1] + b[1]) / 2 + lab_dy
        lines = label.split("|")
        for i, t in enumerate(lines):
            s.text(mx, my + i * 10.4 - (len(lines) - 1) * 5.2 + 3, t, 8.8, anchor, 700, C["slate"], halo="#FFFFFF")


@fig("r_mapa")
def _mapa():
    W, H = 695, 360
    s = SVG(W, H, title="Mapa conceitual: estrutura, propriedades, reações e aplicações")
    cx = [86, 347, 608]
    ry = [30, 118, 206, 294]
    P = lambda r, c: (cx[c], ry[r])
    _node(s, *P(0, 0), "A", "Átomo, tabela e ligações", "eletronegatividade (Δχ)")
    _node(s, *P(0, 1), "A", "Geometria e polaridade", "forma 3D · soma dos dipolos")
    _node(s, *P(0, 2), "E", "Ambiente e saúde", "DBO · biomagnificação · chuva ácida")
    _node(s, *P(1, 0), "B", "Funções orgânicas", "–OH · C=O · –COOH · –NH_2")
    _node(s, *P(1, 1), "A", "Forças intermoleculares", "London · dipolo · lig. de H", hub=True)
    _node(s, *P(1, 2), "A", "Solubilidade, P.E. e estados", "miscibilidade · curvas")
    _node(s, *P(2, 0), "C", "Reações orgânicas, polímeros", "adição · substituição · condensação")
    _node(s, *P(2, 1), "A", "Tensoativos e membrana", "sabão · detergente · fosfolipídio", dual=True)
    _node(s, *P(2, 2), "D", "Soluções e estequiometria", "concentração · diluição · limitante")
    _node(s, *P(3, 0), "F", "Cinética e termoquímica", "E_a · catalisador · ΔH · Hess")
    _node(s, *P(3, 1), "F", "Equilíbrio, ácido-base, K_{ps}", "K · Le Chatelier · pH · tampão")
    _node(s, *P(3, 2), "F", "Eletroquímica e radioatividade", "pilhas · eletrólise · meia-vida")
    B, PU, OR, GR = C["blue"], C["purple"], C["orange"], C["green"]
    _edge(s, P(0, 0), P(0, 1), "ligação|+ forma", B, 0, -9)
    _edge(s, P(0, 1), P(1, 1), "polar ou apolar", B, 44, 0)
    _edge(s, P(1, 0), P(1, 1), "grupo funcional|define as forças", PU, 0, -11)
    _edge(s, P(1, 1), P(1, 2), "semelhante|dissolve semelhante", B, 0, -13)
    _edge(s, P(1, 1), P(2, 1), "parte polar +|parte apolar", B, 48, 0)
    _edge(s, P(1, 0), P(2, 0), "reatividade|do grupo", OR, 38, 0)
    _edge(s, P(2, 0), P(2, 1), "saponificação|(éster + base)", OR, 0, -13)
    _edge(s, P(1, 2), P(0, 2), "O_2 dissolvido,|bioacumulação", GR, 50, 0)
    _edge(s, P(1, 2), P(2, 2), "nº de partículas,|concentração", C["slate_m"], 52, 0)
    _edge(s, P(2, 0), P(3, 0), "velocidade|e energia", OR, 38, 0)
    _edge(s, P(3, 0), P(3, 1), "reversibilidade", OR, 0, -9)
    _edge(s, P(2, 2), P(3, 1), "ácido-base, K_{ps}|(íons em solução)", C["slate_m"], -50, -4)
    _edge(s, P(3, 2), P(3, 1), "íons, e^−,|oxirredução", OR, 0, -13)
    # legenda de cores
    leg = [("A", "estrutura e polaridade"), ("B", "funções orgânicas"), ("C", "reações"), ("D", "quantidades"), ("E", "ambiente")]
    x = 6
    y = H - 12
    for k, t in leg:
        fill, stroke, strong = TH[k]
        s.rect(x, y - 8, 12, 10, fill=fill, stroke=stroke, sw=1.4, rx=3)
        s.text(x + 17, y, t, 9.2, "start", 700, C["slate"])
        x += 17 + tw(t, 9.2, 700) + 16
    s.text(W - 4, y, "setas: “leva a / explica”", 9.2, "end", 600, C["muted"])
    return s
