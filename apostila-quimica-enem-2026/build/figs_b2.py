"""Bloco B · linhas de função orgânica (estrutura genérica + exemplo) e comparações visuais."""
from registry import fig
from svglib import SVG, C, tw
from mol import mol

INK = C["ink"]
PD = C["purple_d"]


def reg(name, smi, hl=None, labels=None, formula=None, w=88, h=50, bond=24, font=0.66, lw=1.7, **kw):
    """Registra uma figura de molécula dimensionada para caber em w×h px."""
    @fig(name)
    def _f(smi=smi, hl=hl, labels=labels, formula=formula, w=w, h=h, bond=bond, font=font, lw=lw, kw=kw):
        m = mol(smi, hl=hl, labels=labels, formula=formula, bond=bond, font=font, lw=lw, margin=6, **kw)
        sc = min(1.0, w / m.w, h / m.h)
        return m.svg(sc)
    return _f


# generic (R–grupo) --------------------------------------------------------------
reg("b_g_alceno", "*C=C*", hl=["[CX3]=[CX3]"], labels={0: "R", 3: "R'"})
reg("b_g_alcino", "*C#C*", hl=["[CX2]#[CX2]"], labels={0: "R", 3: "R'"})
reg("b_g_arom", "c1ccccc1", hl=["c1ccccc1"], formula="C6H6", h=54)
reg("b_g_haleto", "*Cl", hl=["[Cl]"], labels={1: "X"})
reg("b_g_alcool", "*O", hl=["[OX2H]"], formula=None)
reg("b_g_fenol", "Oc1ccccc1", hl=["[OX2H]"], formula="C6H6O", h=54)
reg("b_g_enol", "*C(O)=C*", hl=["[OX2H]C=C"], labels={0: "R", 4: "R'"})

# exemplos ------------------------------------------------------------------------
reg("b_e_alcano", "CCC", formula="C3H8", w=110)
reg("b_e_alceno", "CC=C", hl=["[CX3]=[CX3]"], formula="C3H6", w=110)
reg("b_e_alcino", "C#C", hl=["[CX2]#[CX2]"], formula="C2H2", w=110, add_h=True)
reg("b_e_arom", "Cc1ccccc1", formula="C7H8", w=110, h=54)
reg("b_e_haleto", "FC(F)(Cl)Cl", hl=["[Cl]", "[F]"], formula="CCl2F2", w=110, h=54)
reg("b_e_alcool", "CCO", hl=["[OX2H]"], formula="C2H6O", w=110)
reg("b_e_fenol", "Cc1ccc(C(C)C)c(O)c1", hl=["[OX2H]c"], formula="C10H14O", w=118, h=56)
reg("b_e_enol", "C=CO", hl=["[OX2H]C=C"], formula="C2H4O", w=110)


# comparações lado a lado -----------------------------------------------------------
def cmp_fig(name, A, B, w=343, h=122, maxh=62):
    @fig(name)
    def _f(A=A, B=B, w=w, h=h, maxh=maxh):
        s = SVG(w, h)
        for k, side in enumerate((A, B)):
            m = mol(side["smi"], hl=side.get("hl"), formula=side.get("formula"), bond=side.get("bond", 26), font=0.66,
                    lw=1.7, margin=6, labels=side.get("labels"))
            sc = min(1.0, (w / 2 - 26) / m.w, maxh / m.h)
            cx = w * (0.25 if k == 0 else 0.75)
            s.raw(m.at(cx, 40, sc))
            nm = side["name"]
            if " (" in nm:
                n1, n2 = nm.split(" (", 1)
                n2 = "(" + n2
                s.text(cx, 88, n1, 11.6, "middle", 800, INK)
                s.text(cx, 100, n2, 10.4, "middle", 700, INK)
                s.text(cx, 113, side["sub"], 9.8, "middle", 400, C["muted"])
            else:
                s.text(cx, 90, nm, 11.6, "middle", 800, INK)
                s.text(cx, 103, side["sub"], 10, "middle", 400, C["muted"])
        s.text(w / 2, 46, "×", 20, "middle", 700, C["muted"])
        return s
    return _f


cmp_fig("b_cmp_alcool_fenol",
        dict(smi="CCO", hl=["[OX2H]"], formula="C2H6O", name="Álcool (etanol)", sub="OH em carbono saturado"),
        dict(smi="Oc1ccccc1", hl=["[OX2H]"], formula="C6H6O", name="Fenol", sub="OH direto no anel aromático"))


@fig("b_alcoois_classes")
def _alc_classes():
    from mol import scheme
    W, H = 695, 112
    s = SVG(W, H, title="Álcoois primário, secundário e terciário")
    items = [("CCO", "primário", ["OH em C ligado a", "0 ou 1 outro C"], "etanol", "C2H6O"),
             ("CC(C)O", "secundário", ["OH em C ligado a", "2 outros C"], "propan-2-ol", "C3H8O"),
             ("CC(C)(C)O", "terciário", ["OH em C ligado a", "3 outros C"], "2-metilpropan-2-ol", "C4H10O")]
    cw = (W - 12) / 3
    for i, (smi, cl, rule, nm, fm) in enumerate(items):
        x = 6 + i * cw
        s.rect(x + 2, 3, cw - 4, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        m = mol(smi, formula=fm, bond=26, font=0.66, lw=1.7, margin=6, hl=["[CX4][OX2H]"])
        sc = min(1.0, 84 / m.w, 56 / m.h)
        s.raw(m.at(x + cw * 0.22, 40, sc))
        s.text(x + cw * 0.44, 26, "álcool " + cl, 12.4, "start", 800, C["purple_d"])
        s.text(x + cw * 0.44, 40, rule[0], 9.8, "start", 400, C["slate"])
        s.text(x + cw * 0.44, 51, rule[1], 9.8, "start", 400, C["slate"])
        s.text(x + cw * 0.44, 65, nm, 10.2, "start", 700, INK)
        s.text(x + cw / 2, 97, {0: "→ oxida a aldeído e depois a ácido carboxílico",
                                1: "→ oxida a cetona",
                                2: "→ não oxida em condições brandas"}[i], 10.2, "middle", 700, C["orange_d"])
    return s


# ---- p11: oxigenadas II ----------------------------------------------------------
reg("b_g_eter", "*O*", hl=["[OD2]"], labels={0: "R", 2: "R'"})
reg("b_g_aldeido", "*C=O", hl=["[CX3H1]=O"])
reg("b_g_cetona", "*C(=O)*", hl=["[CX3](=O)"], labels={0: "R", 3: "R'"})
reg("b_g_acido", "*C(=O)O", hl=["[CX3](=O)[OX2H1]"])
reg("b_g_ester", "*C(=O)O*", hl=["[CX3](=O)[OX2]"], labels={0: "R", 4: "R'"})
reg("b_e_eter", "CCOCC", hl=["[OD2]"], formula="C4H10O", w=116)
reg("b_e_aldeido", "CC=O", hl=["[CX3H1]=O"], formula="C2H4O", w=110)
reg("b_e_cetona", "CC(=O)C", hl=["[CX3](=O)"], formula="C3H6O", w=110)
reg("b_e_acido", "CC(=O)O", hl=["[CX3](=O)[OX2H1]"], formula="C2H4O2", w=110)
reg("b_e_ester", "CCCC(=O)OCC", hl=["[CX3](=O)[OX2]"], formula="C6H12O2", w=124)

cmp_fig("b_cmp_ald_cet",
        dict(smi="CC=O", hl=["[CX3H1]=O"], formula="C2H4O", name="Aldeído (etanal)", sub="C=O na ponta (com H)"),
        dict(smi="CC(=O)C", hl=["[CX3](=O)"], formula="C3H6O", name="Cetona (propanona)", sub="C=O entre 2 carbonos"),
        w=222, h=120)
cmp_fig("b_cmp_eter_ester",
        dict(smi="CCOCC", hl=["[OD2]"], formula="C4H10O", name="Éter (etoxietano)", sub="O entre 2 carbonos"),
        dict(smi="CC(=O)OCC", hl=["[CX3](=O)[OX2]"], formula="C4H8O2", name="Éster (etanoato de etila)", sub="O ligado a C=O e a C"),
        w=222, h=120)
cmp_fig("b_cmp_acido_ester",
        dict(smi="CC(=O)O", hl=["[CX3](=O)[OX2H1]"], formula="C2H4O2", name="Ácido (etanoico)", sub="–COOH: tem O–H"),
        dict(smi="CC(=O)OCC", hl=["[CX3](=O)[OX2]"], formula="C4H8O2", name="Éster (etanoato de etila)", sub="–COO–R: sem O–H"),
        w=222, h=120)


@fig("b_esteres_aromas")
def _aromas():
    W, H = 695, 120
    s = SVG(W, H, title="Ésteres e aromas de frutas")
    items = [("CC(=O)OCCC(C)C", "C7H14O2", "etanoato de isopentila", "banana"),
             ("CCCC(=O)OCC", "C6H12O2", "butanoato de etila", "abacaxi"),
             ("CCCC(=O)OC", "C5H10O2", "butanoato de metila", "maçã"),
             ("CC(=O)OCCCCCCCC", "C10H20O2", "etanoato de octila", "laranja"),
             ("COC(=O)c1ccccc1O", "C8H8O3", "salicilato de metila", "pomada (gaultéria)")]
    cw = (W - 12) / 5
    for i, (smi, fm, nm, aroma) in enumerate(items):
        x = 6 + i * cw
        s.rect(x + 2, 3, cw - 4, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        m = mol(smi, formula=fm, bond=22, font=0.66, lw=1.6, margin=5, hl=["[CX3](=O)[OX2]"])
        sc = min(1.0, (cw - 20) / m.w, 52 / m.h)
        s.raw(m.at(x + cw / 2, 36, sc))
        s.text(x + cw / 2, 82, nm, 10.2, "middle", 700, INK)
        s.text(x + cw / 2, 96, "aroma de", 9.6, "middle", 400, C["muted"])
        s.text(x + cw / 2, 109, aroma, 10.8, "middle", 800, C["purple_d"])
    return s


# ---- p12: nitrogenadas e outras --------------------------------------------------
reg("b_g_amina", "*N", hl=["[NX3]"])
reg("b_g_amida", "*C(=O)N", hl=["[CX3](=O)[NX3]"])
reg("b_g_nitrila", "*C#N", hl=["[CX2]#[NX1]"])
reg("b_g_nitro", "*[N+](=O)[O-]", hl=["[N+](=O)[O-]"])
reg("b_g_sulfonico", "*S(=O)(=O)O", hl=["S(=O)(=O)[OX2H1]"])
reg("b_g_tiol", "*S", hl=["[SX2H1]"])
reg("b_e_amina", "CN(C)C", hl=["[NX3]"], formula="C3H9N", w=110)
reg("b_e_amida", "NC(N)=O", hl=["[CX3](=O)[NX3]"], formula="CH4N2O", w=110)
reg("b_e_nitrila", "C=CC#N", hl=["[CX2]#[NX1]"], formula="C3H3N", w=110)
reg("b_e_nitro", "Cc1c([N+](=O)[O-])cc([N+](=O)[O-])cc1[N+](=O)[O-]", hl=["[N+](=O)[O-]"], formula="C7H5N3O6", w=124, h=60, bond=22)
reg("b_e_sulfonico", "OS(=O)(=O)c1ccccc1", hl=["S(=O)(=O)[OX2H1]"], formula="C6H6O3S", w=124, h=54)
reg("b_e_tiol", "CCS", hl=["[SX2H1]"], formula="C2H6S", w=110)

cmp_fig("b_cmp_amina_amida",
        dict(smi="CN", hl=["[NX3]"], formula="CH5N", name="Amina (metilamina)", sub="N ligado só a C saturado"),
        dict(smi="CC(N)=O", hl=["[CX3](=O)[NX3]"], formula="C2H5NO", name="Amida (etanamida)", sub="N ligado a C=O"),
        w=343, h=122)


@fig("b_aminas_classes")
def _am_classes():
    W, H = 695, 98
    s = SVG(W, H, title="Aminas primária, secundária e terciária")
    items = [("CN", "primária", "1 grupo R ligado ao N", "C H5N".replace(" ", ""), "metilamina"),
             ("CNC", "secundária", "2 grupos R ligados ao N", "C2H7N", "dimetilamina"),
             ("CN(C)C", "terciária", "3 grupos R ligados ao N", "C3H9N", "trimetilamina (cheiro de peixe)")]
    cw = (W - 12) / 3
    for i, (smi, cl, rule, fm, nm) in enumerate(items):
        x = 6 + i * cw
        s.rect(x + 2, 3, cw - 4, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        m = mol(smi, formula=fm, bond=26, font=0.66, lw=1.7, margin=6, hl=["[NX3]"])
        sc = min(1.0, 80 / m.w, 56 / m.h)
        s.raw(m.at(x + cw * 0.2, 40, sc))
        s.text(x + cw * 0.42, 28, "amina " + cl, 12.4, "start", 800, C["purple_d"])
        s.text(x + cw * 0.42, 42, rule, 9.8, "start", 400, C["slate"])
        s.text(x + cw * 0.42, 56, nm, 10, "start", 700, INK)
        s.text(x + cw / 2, 88, "base fraca: R–NH_2 + H^+ → R–NH_3^+" if i == 0 else
               ("o N tem par livre → aceita H^+" if i == 1 else "sal da amina = não volátil, sem cheiro"),
               10, "middle", 700, C["orange_d"])
    return s


@fig("b_peptidica")
def _pept():
    from mol import scheme
    g1 = mol("NCC(=O)O", formula="C2H5NO2", bond=26, font=0.66, lw=1.7, margin=6, hl=["[NX3H2]", "[CX3](=O)[OX2H1]"])
    g2 = mol("NCC(=O)O", formula="C2H5NO2", bond=26, font=0.66, lw=1.7, margin=6, hl=["[NX3H2]", "[CX3](=O)[OX2H1]"])
    dp = mol("NCC(=O)NCC(=O)O", formula="C4H8N2O3", bond=26, font=0.66, lw=1.7, margin=6,
             hl=["[CX3](=O)[NX3H1]"])
    w = mol("O", formula="H2O", bond=26, font=0.7, margin=4)
    svg, W, H = scheme([("mol", g1, 0.9), ("op", "+"), ("mol", g2, 0.9), ("arrow", "−H_2O", "", "r"),
                        ("mol", dp, 0.9), ("op", "+"), ("mol", w, 0.9)], gap=12, arrow_len=70)
    return svg
