"""Bloco C · página 18 — polímeros de adição e de condensação."""
from registry import fig
from svglib import SVG, C
from mol import mol, scheme
from figs_c2 import stack

KW = dict(bond=24, font=0.66, lw=1.6, margin=5)


def M(smi, formula=None, hl=None, **kw):
    k = dict(KW)
    k.update(kw)
    return mol(smi, formula=formula, hl=hl, **k)


POLY = "[ "  # início do colchete tipográfico


@fig("c_poli_adicao")
def _adic():
    arrow = ("arrow", "n · catalisador", "", "r")
    rows = [
        scheme([("text", "n  H_2C=CH_2", 15), arrow, ("text", "[ –CH_2–CH_2– ]_n", 15)], gap=10, arrow_len=92),
        scheme([("text", "n", 15), ("mol", M("CC=C", "C3H6", hl=["[CX3]=[CX3]"]), 1.0), arrow,
                ("text", "[ –CH_2–CH(CH_3)– ]_n", 15)], gap=8, arrow_len=92),
        scheme([("text", "n", 15), ("mol", M("C=CCl", "C2H3Cl", hl=["[CX3]=[CX3]"]), 1.0), arrow,
                ("text", "[ –CH_2–CHCl– ]_n", 15)], gap=8, arrow_len=92),
        scheme([("text", "n  F_2C=CF_2", 15), arrow, ("text", "[ –CF_2–CF_2– ]_n", 15)], gap=10, arrow_len=92),
    ]
    labels = [("polietileno", "PE (sacolas, frascos)", ""), ("polipropileno", "PP (tampas, seringas)", ""),
              ("poli(cloreto de vinila)", "PVC (tubos)", ""), ("politetrafluoroetileno", "PTFE (Teflon)", "")]
    return stack(rows, 695, 150, 2, labels)


@fig("c_poli_cond")
def _cond():
    eq = ("arrow", "calor", "", "r")
    pet_a = M("OC(=O)c1ccc(cc1)C(=O)O", "C8H6O4", hl=["[CX3](=O)[OX2H1]"])
    glicol = M("OCCO", "C2H6O2", hl=["[OX2H]"])
    adip = M("OC(=O)CCCCC(=O)O", "C6H10O4", hl=["[CX3](=O)[OX2H1]"])
    hmd = M("NCCCCCCN", "C6H16N2", hl=["[NX3H2]"])
    rows = [
        scheme([("text", "n", 15), ("mol", pet_a, 0.74), ("op", "+"), ("text", "n", 15), ("mol", glicol, 0.74), eq,
                ("text", "[ –CO–C_6H_4–CO–O–CH_2CH_2–O– ]_n", 13), ("op", "+"), ("text", "2n H_2O", 13)],
               gap=5, arrow_len=46),
        scheme([("text", "n", 15), ("mol", adip, 0.74), ("op", "+"), ("text", "n", 15), ("mol", hmd, 0.7), eq,
                ("text", "[ –CO–(CH_2)_4–CO–NH–(CH_2)_6–NH– ]_n", 13), ("op", "+"), ("text", "2n H_2O", 13)],
               gap=5, arrow_len=46),
    ]
    labels = [("PET", "poliéster · ligação éster", ""), ("Náilon 6,6", "poliamida · ligação amida", "")]
    return stack(rows, 695, 118, 2, labels)
