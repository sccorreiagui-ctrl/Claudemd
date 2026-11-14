"""Bloco C · página 16 — oxidação, esterificação, saponificação, biodiesel."""
import re

from registry import fig
from svglib import SVG, C, tw, tspans
from mol import mol, scheme

INK = C["ink"]
KW = dict(bond=24, font=0.66, lw=1.6, margin=5)


def M(smi, formula=None, hl=None, **kw):
    k = dict(KW)
    k.update(kw)
    return mol(smi, formula=formula, hl=hl, **k)


def stack(rows, W, label_w=118, gap=4, labels=None, title=None):
    """Empilha esquemas (svg strings) verticalmente num único SVG com rótulos à esquerda."""
    parts = []
    y = 0
    tot_h = 0
    for i, (svg, w, h) in enumerate(rows):
        parts.append((y, svg, w, h))
        y += h + gap
    H = y - gap
    s = SVG(W, H)
    for i, (y, svg, w, h) in enumerate(parts):
        k = min(1.0, (W - label_w) / w)
        svg2 = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" viewBox="([^"]+)" width="[\d.]+" height="[\d.]+"',
                      lambda m: f'<svg x="{label_w}" y="{y}" viewBox="{m.group(1)}" width="{w * k:.1f}" height="{h * k:.1f}"', svg, count=1)
        s.raw(svg2)
        if labels:
            lab, sub, kind = labels[i]
            s.rect(2, y + h / 2 - 22, label_w - 14, 44, fill=C["orange_l"], stroke=C["orange_m"], sw=1.2, rx=8)
            s.text(2 + (label_w - 14) / 2, y + h / 2 - 4, lab, 11.2, "middle", 800, C["orange_d"])
            s.text(2 + (label_w - 14) / 2, y + h / 2 + 10, sub, 9.6, "middle", 600, C["slate"])
        if i < len(parts) - 1:
            s.line(2, y + h + gap / 2, W - 2, y + h + gap / 2, C["grid"], 1.0)
    return s


@fig("c_oxidacao")
def _oxid():
    ox = "[O]"
    r1 = scheme([("mol", M("CCO", "C2H6O", hl=["[OX2H]"]), 1.05), ("arrow", ox, "", "r"),
                 ("mol", M("CC=O", "C2H4O", hl=["[CX3H1]=O"]), 1.05), ("arrow", ox, "", "r"),
                 ("mol", M("CC(=O)O", "C2H4O2", hl=["[CX3](=O)[OX2H1]"]), 1.05)], gap=8, arrow_len=54)
    r2 = scheme([("mol", M("CC(C)O", "C3H8O", hl=["[OX2H]"]), 1.0), ("arrow", ox, "", "r"),
                 ("mol", M("CC(=O)C", "C3H6O", hl=["[CX3](=O)"]), 1.0), ("space", 22),
                 ("mol", M("CC(C)(C)O", "C4H10O", hl=["[OX2H]"]), 1.0), ("arrow", ox, "", "r"),
                 ("text", "não reage", 12)], gap=8, arrow_len=46)
    labels = [("álcool primário", "→ aldeído → ácido", "p"), ("secundário · terciário", "cetona · não oxida", "s")]
    return stack([r1, r2], 695, 124, 2, labels)


@fig("c_esterif")
def _ester():
    svg, W, H = scheme([("mol", M("CC(=O)O", "C2H4O2", hl=["[CX3](=O)[OX2H1]"]), 1.05), ("op", "+"),
                        ("mol", M("CCO", "C2H6O", hl=["[OX2H]"]), 1.05), ("arrow", "H^+", "calor", "eq"),
                        ("mol", M("CC(=O)OCC", "C4H8O2", hl=["[CX3](=O)[OX2]"]), 1.05), ("op", "+"),
                        ("mol", M("O", "H2O"), 1.05)], gap=9, arrow_len=76)
    return svg


R_TG = "*C(=O)OCC(OC(=O)*)COC(=O)*"


@fig("c_sapon")
def _sapon():
    tg = M(R_TG, None, hl=["[CX3](=O)[OX2][CX4]"], labels={0: "R", 6: "R'", 10: "R''"}) if False else M(R_TG, None, hl=["[CX3](=O)[OX2][CX4]"])
    gl = M("OCC(O)CO", "C3H8O3", hl=["[OX2H]"])
    r1 = scheme([("mol", tg, 0.74), ("op", "+"), ("text", "3 NaOH", 14), ("arrow", "calor", "", "r"),
                 ("mol", gl, 0.95), ("op", "+"), ("text", "3 R–COO^- Na^+", 14)], gap=7, arrow_len=50)
    r2 = scheme([("mol", tg, 0.74), ("op", "+"), ("text", "3 CH_3OH", 14), ("arrow", "NaOH (cat.)", "", "r"),
                 ("mol", gl, 0.95), ("op", "+"), ("text", "3 R–COO–CH_3", 14)], gap=7, arrow_len=60)
    labels = [("Saponificação", "→ glicerol + SABÃO", "a"), ("Transesterificação", "→ glicerol + BIODIESEL", "b")]
    return stack([r1, r2], 695, 124, 2, labels)
