"""Bloco B · página 13 — moléculas multifuncionais e identificação de grupos."""
from registry import fig
from svglib import SVG, C, tw
from mol import mol

INK = C["ink"]
PD = C["purple_d"]


def multi(name, smi, formula, title, groups, legend, W=227, H=176, bond=28, horizontal=False, extra=None, mw=None, mh=None):
    """groups: lista (SMARTS, rótulo) — destaca e numera; legend: lista (rótulo, texto)."""
    @fig(name)
    def _f(smi=smi, formula=formula, title=title, groups=groups, legend=legend, W=W, H=H, bond=bond):
        s = SVG(W, H, title=title)
        s.rect(1, 1, W - 2, H - 2, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        m = mol(smi, formula=formula, bond=bond, font=0.64, lw=1.7, margin=8, hl=[g[0] for g in groups],
                mark=groups, horizontal=horizontal)
        maxw = (mw or (W - 18))
        maxh = (mh or (H - 84))
        sc = min(1.45, maxw / m.w, maxh / m.h)
        s.raw(m.at(W / 2, 22 + 8 + maxh / 2, sc))
        s.text(10, 17, title, 12, "start", 800, INK)
        import re as _re
        s.text(W - 10, 17, _re.sub(r"(?<=[A-Za-z])(\d+)", r"_{\1}", formula), 10.4, "end", 600, C["muted"])
        # legenda
        ncol = 2 if W < 400 else 3
        for k, (lab, txt) in enumerate(legend):
            col, row = k % ncol, k // ncol
            x = 12 + col * (W - 24) / ncol
            y = H - 12 - (((len(legend) - 1) // ncol) - row) * 17
            s.circle(x + 6.5, y - 3.5, 7.2, fill=PD)
            s.text(x + 6.5, y, lab, 9.8, "middle", 800, "#FFFFFF")
            s.text(x + 17, y, txt, 10.4, "start", 600, INK)
        return s
    return _f


ACID = "[CX3](=O)[OX2H1]"
multi("b_m_aspirina", "CC(=O)Oc1ccccc1C(=O)O", "C9H8O4", "Aspirina (AAS)",
      [(ACID, "1"), ("[CH3][CX3](=O)[OX2]c", "2")],
      [("1", "ácido carboxílico"), ("2", "éster")], H=186)
multi("b_m_paracetamol", "CC(=O)Nc1ccc(O)cc1", "C8H9NO2", "Paracetamol",
      [("[CX3](=O)[NX3H1]c", "1"), ("[OX2H]c", "2")],
      [("1", "amida"), ("2", "fenol")], H=186)
multi("b_m_vanilina", "COc1cc(C=O)ccc1O", "C8H8O3", "Vanilina (baunilha)",
      [("[CX3H1]=O", "1"), ("[OX2H]c", "2"), ("[OD2]([CH3])c", "3")],
      [("1", "aldeído"), ("2", "fenol"), ("3", "éter")], H=186)
multi("b_m_adrenalina", "CNCC(O)c1ccc(O)c(O)c1", "C9H13NO3", "Adrenalina",
      [("[NX3H1]([CH3])[CH2]", "1"), ("[CX4][OX2H]", "2"), ("[OX2H]c", "3")],
      [("1", "amina secundária"), ("2", "álcool"), ("3", "fenol (× 2)")], W=343, H=176)
multi("b_m_ibuprofeno", "CC(C)Cc1ccc(C(C)C(=O)O)cc1", "C13H18O2", "Ibuprofeno",
      [(ACID, "1")],
      [("1", "ácido carboxílico"), ("–", "anel aromático e cadeia apolar")], W=343, H=176)
multi("b_m_capsaicina", "COc1cc(CNC(=O)CCCCC=CC(C)C)ccc1O", "C18H27NO3", "Capsaicina (pimenta)",
      [("[CX3](=O)[NX3H1]", "1"), ("[OD2]([CH3])c", "2"), ("[OX2H]c", "3"), ("[CX3;!a]=[CX3;!a]", "4")],
      [("1", "amida"), ("2", "éter"), ("3", "fenol"), ("4", "alceno (C=C)")], W=695, H=150, horizontal=True,
      bond=26, mw=560, mh=84)


@fig("b_q_eugenol")
def _eug():
    m = mol("C=CCc1ccc(O)c(OC)c1", formula="C10H12O2", bond=26, font=0.64, lw=1.7, margin=6, horizontal=True)
    return m.svg(min(1.0, 200 / m.w, 80 / m.h))


@fig("b_q_acucares")
def _acucares():
    s = SVG(470, 120, title="Glicose e frutose (formas abertas)")
    g = mol("OCC(O)C(O)C(O)C(O)C=O", formula="C6H12O6", bond=24, font=0.64, lw=1.6, margin=6, horizontal=True)
    f = mol("OCC(O)C(O)C(O)C(=O)CO", formula="C6H12O6", bond=24, font=0.64, lw=1.6, margin=6, horizontal=True)
    s.raw(g.at(120, 48, min(1.0, 220 / g.w, 70 / g.h)))
    s.raw(f.at(350, 48, min(1.0, 220 / f.w, 70 / f.h)))
    s.text(120, 108, "Glicose (forma aberta)", 11, "middle", 800, INK)
    s.text(350, 108, "Frutose (forma aberta)", 11, "middle", 800, INK)
    return s
