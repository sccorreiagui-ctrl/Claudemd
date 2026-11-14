"""Bloco C · página 15 — reações orgânicas (esquemas)."""
from registry import fig
from svglib import SVG, C
from mol import mol, scheme

KW = dict(bond=24, font=0.66, lw=1.6, margin=5)


def M(smi, formula=None, hl=None, **kw):
    k = dict(KW)
    k.update(kw)
    return mol(smi, formula=formula, hl=hl, **k)


def rx(name, items, gap=9, arrow_len=64, maxw=520):
    @fig(name)
    def _f(items=items, gap=gap, arrow_len=arrow_len, maxw=maxw):
        svg, W, H = scheme(items, gap=gap, arrow_len=arrow_len)
        if W > maxw:
            import re as _re
            k = maxw / W
            svg = _re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{maxw}" height="{H * k:.1f}"', svg, count=1)
        return svg
    return _f


HAL = ["[Br]", "[Cl]"]
# substituição
rx("c_rx_sub1", [("text", "CH_3–CH_3", 16), ("op", "+"), ("text", "Br–Br", 16),
                 ("arrow", "luz", "", "r"), ("text", "CH_3–CH_2–Br", 16), ("op", "+"), ("text", "HBr", 16)])
rx("c_rx_sub2", [("mol", M("c1ccccc1", "C6H6"), 1.1), ("op", "+"), ("text", "HNO_3", 17),
                 ("arrow", "H_2SO_4", "", "r"), ("mol", M("[O-][N+](=O)c1ccccc1", "C6H5NO2", hl=["[N+](=O)[O-]"]), 1.1),
                 ("op", "+"), ("mol", M("O", "H2O"), 1.1)])
# adição
rx("c_rx_add1", [("text", "H_2C=CH_2", 16), ("op", "+"), ("text", "H_2", 16),
                 ("arrow", "Ni, calor", "", "r"), ("text", "H_3C–CH_3", 16)])
rx("c_rx_add2", [("text", "H_2C=CH_2", 16), ("op", "+"), ("text", "Br–Br", 16),
                 ("arrow", "CCl_4", "", "r"), ("text", "BrH_2C–CH_2Br", 16)])
rx("c_rx_add3", [("mol", M("CC=C", "C3H6", hl=["[CX3]=[CX3]"]), 1.1), ("op", "+"), ("text", "H_2O", 16),
                 ("arrow", "H^+", "", "r"), ("mol", M("CC(C)O", "C3H8O", hl=["[OX2H]"]), 1.1)])
# eliminação
rx("c_rx_elim1", [("mol", M("CCO", "C2H6O", hl=["[OX2H]"]), 1.1), ("arrow", "H_2SO_4 conc.", "170 °C", "r"),
                  ("text", "H_2C=CH_2", 16), ("op", "+"), ("text", "H_2O", 16)])
rx("c_rx_elim2", [("mol", M("CC(Br)C", "C3H7Br", hl=["[Br]"]), 1.1), ("arrow", "KOH (etanol)", "", "r"),
                  ("mol", M("CC=C", "C3H6", hl=["[CX3]=[CX3]"]), 1.1), ("op", "+"), ("text", "HBr", 16)])
