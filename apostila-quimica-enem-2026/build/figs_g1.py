"""Bloco G · página 36 — modelos atômicos e tabela periódica compacta."""
import math

from rdkit import Chem

from registry import fig
from svglib import SVG, C, tw

INK = C["ink"]
SL = C["slate"]
PT = Chem.GetPeriodicTable()


# ------------------------------------------------------------------- modelos atômicos
@fig("j_modelos")
def _modelos():
    W, H = 695, 138
    s = SVG(W, H, title="Evolução dos modelos atômicos")
    cw = (W - 8) / 5
    cards = [
        ("Dalton", "1808", "esfera maciça", "átomos de um elemento são todos iguais"),
        ("Thomson", "1897", "esfera (+) com elétrons", "descobre o elétron (tubo de raios catódicos)"),
        ("Rutherford", "1911", "núcleo (+) e eletrosfera", "poucas α voltam: núcleo pequeno e denso"),
        ("Bohr", "1913", "níveis de energia", "salto de nível emite luz (teste de chama)"),
        ("Modelo atual", "1926+", "orbitais (probabilidade)", "Schrödinger e Heisenberg; nêutron: Chadwick, 1932"),
    ]
    for i, (nm, yr, l1, l2) in enumerate(cards):
        x = 4 + i * cw
        cx = x + cw / 2
        s.rect(x + 2, 3, cw - 4, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(cx, 18, nm, 11.6, "middle", 800, INK)
        s.text(cx, 30, yr, 9.6, "middle", 700, C["muted"])
        cy = 66
        if i == 0:
            s.circle(cx, cy, 24, fill="#C7CDD6", stroke=SL, sw=1.6)
        elif i == 1:
            s.circle(cx, cy, 24, fill="#FADBD8", stroke=C["red"], sw=1.6)
            for dx, dy in ((-11, -8), (8, -12), (13, 6), (-5, 11), (-15, 8), (2, 0)):
                s.circle(cx + dx, cy + dy, 3.4, fill=C["blue"])
        elif i == 2:
            s.circle(cx, cy, 24, fill="none", stroke=C["slate_m"], sw=1.2, dash="3 3")
            s.circle(cx, cy, 3.4, fill=C["red"])
            for ang in (35, 160, 275):
                s.circle(cx + 24 * math.cos(math.radians(ang)), cy - 24 * math.sin(math.radians(ang)), 3, fill=C["blue"])
        elif i == 3:
            for r in (9, 17, 25):
                s.circle(cx, cy, r, fill="none", stroke=C["slate_m"], sw=1.1)
            s.circle(cx, cy, 3.4, fill=C["red"])
            s.circle(cx + 17 * math.cos(math.radians(40)), cy - 17 * math.sin(math.radians(40)), 3, fill=C["blue"])
            s.circle(cx - 25 * math.cos(math.radians(15)), cy + 25 * math.sin(math.radians(15)), 3, fill=C["blue"])
            s.arrow(cx + 14, cy + 21, cx + 30, cy + 8, C["orange"], 1.8, 6)
        else:
            g = s.radgrad([(0, "#9DB8F5"), (0.6, "#D6E3FB"), (1, "#FFFFFF")], 0.5, 0.5, 0.5)
            s.circle(cx, cy, 25, fill=g, stroke=C["blue"], sw=1.1, dash="2 3")
            s.circle(cx, cy, 3.4, fill=C["red"])
        # legendas
        s.text(cx, 107, l1, 9.4, "middle", 800, SL)
        if len(l2) > 28:
            k = l2.rfind(" ", 0, 28)
            s.text(cx, 118, l2[:k], 8.8, "middle", 600, C["muted"])
            s.text(cx, 128, l2[k + 1:], 8.8, "middle", 600, C["muted"])
        else:
            s.text(cx, 119, l2, 8.8, "middle", 600, C["muted"])
    return s


# ------------------------------------------------------------------- tabela periódica
_ALC = {3, 11, 19, 37, 55, 87}
_ALT = {4, 12, 20, 38, 56, 88}
_SEMI = {5, 14, 32, 33, 51, 52}
_AMET = {1, 6, 7, 8, 15, 16, 34}
_HAL = {9, 17, 35, 53, 85, 117}
_NOB = {2, 10, 18, 36, 54, 86, 118}
_OMET = {13, 31, 49, 81, 113, 50, 82, 114, 83, 115, 84, 116}
_LAN = set(range(57, 72))
_ACT = set(range(89, 104))

CATS = [
    ("alcalinos", "#FFD9C7", _ALC), ("alcalinoterrosos", "#FDEBB5", _ALT),
    ("transição", "#D6E4F7", None), ("outros metais", "#DDE3EA", _OMET),
    ("semimetais", "#CFEACB", _SEMI), ("ametais", "#E6D9F4", _AMET),
    ("halogênios", "#F8D0E1", _HAL), ("gases nobres", "#C9ECEC", _NOB),
    ("lantanídeos", "#F2E3BE", _LAN), ("actinídeos", "#EBD3DC", _ACT),
]


def _cat(z):
    for nm, col, st in CATS:
        if st is not None and z in st:
            return nm, col
    return "transição", "#D6E4F7"


def _pos(z):
    """Retorna (linha, coluna) 1-based; linhas 8 e 9 = lantanídeos e actinídeos."""
    if z == 1:
        return 1, 1
    if z == 2:
        return 1, 18
    if 3 <= z <= 4:
        return 2, z - 2
    if 5 <= z <= 10:
        return 2, z + 8
    if 11 <= z <= 12:
        return 3, z - 10
    if 13 <= z <= 18:
        return 3, z
    if 19 <= z <= 36:
        return 4, z - 18
    if 37 <= z <= 54:
        return 5, z - 36
    if 55 <= z <= 56:
        return 6, z - 54
    if 57 <= z <= 71:
        return 8, z - 54
    if 72 <= z <= 86:
        return 6, z - 68
    if 87 <= z <= 88:
        return 7, z - 86
    if 89 <= z <= 103:
        return 9, z - 86
    if 104 <= z <= 118:
        return 7, z - 100
    raise ValueError(z)


@fig("j_tabela")
def _tabela():
    cw, ch = 37.6, 21.6
    x0, y0 = 14, 24
    W = x0 + 18 * cw + 4
    H = 288
    s = SVG(W, H, title="Tabela periódica: famílias e tendências")
    # cabeçalhos de grupo
    a_lab = {1: "1A", 2: "2A", 13: "3A", 14: "4A", 15: "5A", 16: "6A", 17: "7A", 18: "8A"}
    for g in range(1, 19):
        cx = x0 + (g - 0.5) * cw
        s.text(cx, 10, str(g), 9.2, "middle", 800, SL)
        if g in a_lab:
            s.text(cx, 19.5, a_lab[g], 7.4, "middle", 700, C["muted"])
    for p in range(1, 8):
        s.text(x0 - 4, y0 + (p - 0.5) * (ch + 1.4) + 3.4, str(p), 9, "end", 800, SL)
    for z in range(1, 119):
        r, c = _pos(z)
        nm, col = _cat(z)
        x = x0 + (c - 1) * cw
        yy = y0 + (r - 1) * (ch + 1.4) + (8 if r >= 8 else 0)
        s.rect(x + 0.8, yy, cw - 1.6, ch, fill=col, stroke="#FFFFFF", sw=0.6, rx=3)
        s.text(x + cw / 2 + 2.4, yy + 15, PT.GetElementSymbol(z), 10.6, "middle", 800, INK)
        s.text(x + 3.6, yy + 7.6, str(z), 5.9, "start", 600, "#4B5563")
    # marcadores de grupo 3 (lantanídeos/actinídeos)
    for r, lab in ((6, "57–71"), (7, "89–103")):
        x = x0 + 2 * cw
        yy = y0 + (r - 1) * (ch + 1.4)
        s.rect(x + 0.8, yy, cw - 1.6, ch, fill="#FBF3DE" if r == 6 else "#F6E7EC", stroke="#FFFFFF", sw=0.6, rx=3)
        s.text(x + cw / 2, yy + 14.4, lab, 7.8, "middle", 800, "#4B5563")
    # setas de tendências no espaço vazio (períodos 1–3, grupos 3–12)
    ax0 = x0 + 2.4 * cw
    s.arrow(ax0 + 2, y0 + 32, ax0 + 44, y0 + 3, C["orange"], 3, 10)
    s.text(ax0 + 58, y0 + 9, "energia de ionização, afinidade eletrônica e eletronegatividade", 9.4, "start", 800, C["orange_d"])
    s.text(ax0 + 58, y0 + 21, "crescem para a direita e para cima", 9.4, "start", 800, C["orange_d"])
    s.text(ax0 + 58, y0 + 32, "(gases nobres: sem valor usual de eletronegatividade)", 8.8, "start", 600, C["muted"])
    s.arrow(ax0 + 44, y0 + 38, ax0 + 2, y0 + 65, C["blue"], 3, 10)
    s.text(ax0 + 58, y0 + 51, "raio atômico cresce para a esquerda e para baixo", 9.4, "start", 800, C["blue_d"])
    s.text(ax0 + 58, y0 + 63, "(mais camadas ⇒ maior; mesma camada, mais prótons ⇒ menor)", 8.8, "start", 600, C["muted"])
    # legenda
    ly = y0 + 9 * (ch + 1.4) + 16
    lx = x0
    for nm, col, _ in CATS:
        wtxt = tw(nm, 8.8, 700)
        s.rect(lx, ly, 9, 9, fill=col, stroke=C["slate_m"], sw=0.6, rx=2)
        s.text(lx + 12, ly + 8, nm, 8.8, "start", 700, SL)
        lx += 12 + wtxt + 9
    return s
