"""Bloco C · página 19 — isomeria plana e espacial."""
from registry import fig
from svglib import SVG, C, tw
from mol import mol
from figlib import chip_svg

INK = C["ink"]
PD = C["purple_d"]


def iso_fig(name, items, w=343, h=98, conn="×", mh=42, bond=22):
    @fig(name)
    def _f(items=items, w=w, h=h, conn=conn, mh=mh, bond=bond):
        s = SVG(w, h)
        n = len(items)
        cw = w / n
        for i, (smi, hl, nm, sub, fm) in enumerate(items):
            m = mol(smi, hl=hl, formula=fm, bond=bond, font=0.66, lw=1.6, margin=5)
            sc = min(1.15, (cw - 16) / m.w, mh / m.h)
            cx = cw * (i + 0.5)
            s.raw(m.at(cx, 29, sc))
            s.text(cx, 67, nm, 10.6, "middle", 800, INK)
            s.text(cx, 79, sub, 9.6, "middle", 400, C["muted"])
            if fm:
                import re
                s.text(cx, 91, re.sub(r"(?<=[A-Za-z])(\d+)", r"_{\1}", fm), 9.6, "middle", 700, PD)
            if i < n - 1:
                s.text(cw * (i + 1), 34, conn, 15, "middle", 700, C["muted"])
        return s
    return _f


iso_fig("c_iso_cadeia", [
    ("CCCCC", None, "pentano", "normal · P.E. 36 °C", "C5H12"),
    ("CC(C)CC", None, "2-metilbutano", "ramificada · 28 °C", "C5H12"),
    ("CC(C)(C)C", None, "2,2-dimetilpropano", "ramificada · 9,5 °C", "C5H12")])
iso_fig("c_iso_posicao", [
    ("CCCO", ["[OX2H]"], "propan-1-ol", "OH no C1", "C3H8O"),
    ("CC(C)O", ["[OX2H]"], "propan-2-ol", "OH no C2", "C3H8O")])
iso_fig("c_iso_funcao", [
    ("CCO", ["[OX2H]"], "etanol", "álcool", "C2H6O"),
    ("COC", ["[OD2]"], "éter dimetílico", "éter", "C2H6O")])
iso_fig("c_iso_compens", [
    ("CCOCC", ["[OD2]"], "etoxietano", "éter · O entre etil e etil", "C4H10O"),
    ("COCCC", ["[OD2]"], "metoxipropano", "éter · O entre metil e propil", "C4H10O")])
iso_fig("c_iso_tauto", [
    ("C=CO", ["[OX2H]C=C"], "etenol (enol)", "instável", "C2H4O"),
    ("CC=O", ["[CX3H1]=O"], "etanal (aldeído)", "forma estável", "C2H4O")], conn="⇌")
iso_fig("c_iso_geom", [
    ("Cl/C=C\\Cl", ["[Cl]"], "cis-1,2-dicloroeteno", "polar · P.E. 60 °C", "C2H2Cl2"),
    ("Cl/C=C/Cl", ["[Cl]"], "trans-1,2-dicloroeteno", "apolar · P.E. 48 °C", "C2H2Cl2")])


@fig("c_iso_optica")
def _optica():
    W, H = 695, 148
    s = SVG(W, H, title="Enantiômeros do ácido lático e imagem especular")
    L = mol("C[C@H](O)C(=O)O", formula="C3H6O3", bond=28, font=0.7, lw=1.8, margin=8,
            hl=["[CX4H1]([CH3])([OX2H])[CX3]"])
    D = mol("C[C@@H](O)C(=O)O", formula="C3H6O3", bond=28, font=0.7, lw=1.8, margin=8,
            hl=["[CX4H1]([CH3])([OX2H])[CX3]"])
    s.raw(L.at(150, 54, 1.15))
    s.raw(D.at(420, 54, 1.15))
    # espelho
    s.line(285, 10, 285, 100, C["slate_m"], 2, dash="5 4")
    s.text(285, 114, "espelho", 10.4, "middle", 700, C["muted"])
    s.text(150, 124, "ácido (S)-lático · enantiômero 1", 11, "middle", 800, INK)
    s.text(420, 124, "ácido (R)-lático · enantiômero 2", 11, "middle", 800, INK)
    # legenda do C*
    s.rect(542, 12, 144, 118, fill=C["purple_l"], stroke=C["purple_m"], sw=1.2, rx=9)
    s.text(552, 30, "Carbono quiral (C*)", 11, "start", 800, PD)
    s.text(552, 44, "4 ligantes diferentes:", 10, "start", 600, C["slate"])
    for k, t in enumerate(["–H", "–OH", "–CH_3", "–COOH"]):
        s.text(560, 60 + k * 14, t, 11, "start", 700, INK)
    s.text(552, 124, "sp³ · em roxo no desenho", 9.4, "start", 400, C["muted"])
    return s
