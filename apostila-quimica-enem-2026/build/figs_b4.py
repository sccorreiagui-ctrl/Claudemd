"""Bloco B · página 14 — propriedades físicas e caráter ácido-base dos compostos orgânicos."""
from registry import fig
from svglib import SVG, C, tw
from mol import mol

INK = C["ink"]
PD = C["purple_d"]


@fig("b_pe_funcoes")
def _pe_funcoes():
    W, H = 695, 252
    s = SVG(W, H, title="Pontos de ebulição de compostos de massa molar ≈ 58–60 g/mol")
    rows = [
        ("butano", "alcano", 58, -0.5, "CCCC", None, "C4H10", "L"),
        ("metoxietano", "éter", 60, 7.4, "CCOC", "[OD2]", "C3H8O", "D"),
        ("propanal", "aldeído", 58, 48.0, "CCC=O", "[CX3H1]=O", "C3H6O", "D"),
        ("propilamina", "amina", 59, 48.0, "CCCN", "[NX3]", "C3H9N", "H"),
        ("propanona", "cetona", 58, 56.0, "CC(=O)C", "[CX3]=O", "C3H6O", "D"),
        ("propan-1-ol", "álcool", 60, 97.2, "CCCO", "[OX2H]", "C3H8O", "H"),
        ("ác. etanoico", "ác. carboxílico", 60, 118.0, "CC(=O)O", "[CX3](=O)[OX2H1]", "C2H4O2", "H"),
        ("etanamida", "amida", 59, 221.0, "CC(N)=O", "[CX3](=O)[NX3]", "C2H5NO", "H"),
    ]
    col = {"L": C["amber"], "D": "#7DB2F0", "H": C["blue"]}
    x0 = 286
    xz = x0 + 14
    sc = 340 / 225.0
    y0 = 24
    rh = 24.5
    s.text(8, 14, "composto", 9.6, "start", 800, C["muted"], spacing="0.06em")
    s.text(xz, 14, "ponto de ebulição (°C)", 9.6, "start", 800, C["muted"], spacing="0.06em")
    for t in (0, 50, 100, 150, 200):
        x = xz + t * sc
        s.line(x, y0 - 4, x, y0 + rh * len(rows) + 2, C["grid"], 0.9)
        s.text(x, y0 + rh * len(rows) + 14, str(t), 9.6, "middle", 400, C["muted"])
    for i, (nm, fn, M, bp, smi, hl, fm, kind) in enumerate(rows):
        y = y0 + i * rh
        m = mol(smi, formula=fm, bond=17, font=0.7, lw=1.4, margin=3, hl=[hl] if hl else None)
        k = min(1.0, 74 / m.w, 24 / m.h)
        s.raw(m.at(46, y + rh / 2 - 1, k))
        s.text(96, y + 11, nm, 10.8, "start", 800, INK)
        s.text(96, y + 21.5, f"{fn} · M = {M}", 9.4, "start", 400, C["muted"])
        L = bp * sc
        if L >= 0:
            s.rect(xz, y + 3.5, max(L, 2), 16, fill=col[kind], rx=3)
            tx = xz + max(L, 2) + 5
        else:
            s.rect(xz + L, y + 3.5, -L, 16, fill=col[kind], rx=3)
            tx = xz + 5
        s.text(tx, y + 16, ("%g" % bp).replace(".", ",").replace("-", "−"), 10.8, "start", 800, INK)
    s.line(xz, y0 - 4, xz, y0 + rh * len(rows) + 2, C["slate"], 1.2)
    # legenda
    ly = H - 3
    s.rect(8, ly - 9, 12, 9, fill=C["amber"], rx=2)
    s.text(24, ly - 1, "só London", 9.8, "start", 700, C["amber_d"])
    s.rect(98, ly - 9, 12, 9, fill="#7DB2F0", rx=2)
    s.text(114, ly - 1, "dipolo–dipolo", 9.8, "start", 700, C["blue_d"])
    s.rect(206, ly - 9, 12, 9, fill=C["blue"], rx=2)
    s.text(222, ly - 1, "com ligação de hidrogênio (amina: mais fraca que álcool; ácido forma dímeros; amida: a mais forte)", 9.8, "start", 700, C["blue_d"])
    return s


def _pin_axis(title, lo, hi, step, pins, W=695, H=108, unit="pK_a", note_left="mais ácido", note_right="menos ácido", levels=3):
    s = SVG(W, H, title=title)
    x0, x1 = 30, 665

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    by = 58
    g = s.lingrad([(0, C["purple"]), (0.5, "#CDB9F8"), (1, "#F6F1FE")])
    s.rect(x0, by, x1 - x0, 12, fill=g, stroke=C["purple_m"], sw=1, rx=6)
    v = lo
    while v <= hi + 1e-9:
        s.line(X(v), by + 12, X(v), by + 17, INK, 1.0)
        s.text(X(v), by + 28, ("%g" % v).replace(".", ","), 9.6, "middle", 400, C["muted"])
        v += step
    s.text(x0, 12, note_left, 9.8, "start", 800, C["purple_d"])
    s.text(x1, 12, note_right, 9.8, "end", 800, C["muted"])
    s.text((x0 + x1) / 2, 12, unit + " →", 10, "middle", 800, INK)
    for k, pin in enumerate(pins):
        v, lab, col = pin[:3]
        lvl = pin[3] if len(pin) > 3 else k % levels
        top = lvl % 2 == 0
        cy = by - 18 - (lvl // 2) * 20 if top else by + 12 + 36 + (lvl // 2) * 20 - 14
        cy = (by - 19 - 17 * (lvl // 2)) if top else (by + 40 + 17 * (lvl // 2))
        x = X(v)
        s.line(x, (cy + 8) if top else by + 12, x, by if top else (cy - 8), C["slate_m"], 1.0)
        s.circle(x, by + 6, 3.2, fill="#FFFFFF", stroke=C["purple_d"], sw=1.3)
        w = tw(lab, 9.8, 700) + 10
        s.rect(x - w / 2, cy - 8, w, 16, fill="#FFFFFF", stroke=col, sw=1.2, rx=8)
        s.text(x, cy + 3.4, lab, 9.8, "middle", 700, INK)
    return s


@fig("b_acidez_escala")
def _acidez():
    pins = [(0.65, "Cl₃C–COOH 0,65", C["purple"], 0), (1.29, "Cl₂CH–COOH 1,29", C["purple"], 1), (2.86, "ClCH₂–COOH 2,86", C["purple"], 2),
            (3.75, "HCOOH 3,75", C["purple"], 0), (4.76, "CH₃COOH 4,76", C["purple"], 1), (9.95, "fenol 10", C["red"], 0),
            (15.5, "metanol 15,5", C["slate_m"], 0), (15.9, "etanol 15,9", C["slate_m"], 1)]
    pins = [(v, l.replace("₃", "_3").replace("₂", "_2"), c, k) for v, l, c, k in pins]
    return _pin_axis("Escala de acidez (pKa)", 0, 18, 2, pins, H=112, levels=3)


@fig("b_basicidade_escala")
def _basicidade():
    pins = [(3.27, "dimetilamina 3,3", C["purple"], 0), (3.36, "metilamina 3,4", C["purple"], 1), (4.19, "trimetilamina 4,2", C["purple"], 2),
            (4.75, "NH_3 4,75", C["slate_m"], 0), (9.37, "anilina 9,4", C["red"], 0)]
    return _pin_axis("Escala de basicidade (pKb)", 2, 11, 1, pins, H=112, unit="pK_b", note_left="mais básico",
                     note_right="menos básico", levels=3)
