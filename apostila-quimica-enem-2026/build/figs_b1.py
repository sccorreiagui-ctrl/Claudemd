"""Bloco B · página 9 — carbono, notações de fórmula, classes de carbono e cadeias."""
from registry import fig
from svglib import SVG, C, tw
from mol import mol, scheme
from figlib import chip_svg

INK = C["ink"]
PD = C["purple_d"]
KW = dict(bond=26, font=0.62, lw=1.7)


def _std(smi, formula=None, **kw):
    k = dict(KW)
    k.update(kw)
    return mol(smi, formula=formula, **k)


# ------------------------------------------------------------------- hibridização (explícito)
@fig("b_hib_sp3")
def _h3():
    return _std("CC", "C2H6", add_h=True, bond=20, font=0.7).svg(0.62)


@fig("b_hib_sp2")
def _h2():
    return _std("C=C", "C2H4", add_h=True, bond=20, font=0.7).svg(0.62)


@fig("b_hib_sp")
def _h1():
    return _std("C#C", "C2H2", add_h=True, bond=20, font=0.7).svg(0.62)


# ------------------------------------------------------------------- três notações
@fig("b_notacoes")
def _notacoes():
    W, H = 695, 138
    s = SVG(W, H, title="Fórmula condensada, estrutural plana e de linha")
    cw = (W - 12) / 3
    titles = [("1 · Condensada", "agrupa os átomos de cada carbono"),
              ("2 · Estrutural plana", "mostra todos os átomos e ligações"),
              ("3 · De linha (zigue-zague)", "só o esqueleto; o resto é subentendido")]
    for i, (t, sub) in enumerate(titles):
        x = 6 + i * cw
        s.rect(x + 2, 4, cw - 4, H - 8, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + cw / 2, 22, t, 12, "middle", 800, PD)
        s.text(x + cw / 2, 35, sub, 10, "middle", 400, C["muted"])
    # 1
    s.text(6 + cw / 2, 76, "CH_3–CH(OH)–CH_3", 17, "middle", 700, INK)
    s.text(6 + cw / 2, 98, "ou  CH_3CH(OH)CH_3", 12, "middle", 600, C["muted"])
    s.text(6 + cw / 2, 124, "propan-2-ol (álcool isopropílico)", 10.4, "middle", 600, C["muted"])
    # 2
    m2 = _std("CC(C)O", "C3H8O", add_h=True, bond=24, hl=["[OX2H]"])
    s.raw(m2.at(6 + cw * 1.5, 77, 0.78))
    s.text(6 + cw * 1.5, 124, "todos os H aparecem (C_3H_8O)", 10.4, "middle", 600, C["muted"])
    # 3
    m3 = _std("CC(C)O", "C3H8O", bond=32, hl=["[OX2H]"],
              atom_marks={0: ("CH_3", "ghost"), 1: ("CH", "ghost", (22, 12)), 2: ("CH_3", "ghost")})
    s.raw(m3.at(6 + cw * 2.5, 80, 0.92))
    s.text(6 + cw * 2.5, 124, "cada ponta/vértice = 1 C · H subentendidos", 10.4, "middle", 600, C["muted"])
    return s


# ------------------------------------------------------------------- classes de carbono
@fig("b_classes_carbono")
def _classes():
    W, H = 695, 112
    s = SVG(W, H, title="Carbonos primário, secundário, terciário e quaternário")
    # 2,2,4-trimetilpentano (isoctano): atom_marks por índice
    marks = {0: "1", 1: "3", 2: "1", 3: "2", 4: "4", 5: "1", 6: "1", 7: "1"}
    m = _std("CC(C)CC(C)(C)C", "C8H18", bond=30, atom_marks=marks)
    s.raw(m.at(150, 51, 0.86))
    s.text(150, 106, "isoctano (2,2,4-trimetilpentano), C_8H_18", 10.4, "middle", 600, C["muted"])
    rows = [
        ("1", "primário", "ligado a 0 ou 1 outro carbono", "5 carbonos (os CH_3)"),
        ("2", "secundário", "ligado a 2 outros carbonos", "1 carbono (o CH_2)"),
        ("3", "terciário", "ligado a 3 outros carbonos", "1 carbono (o CH)"),
        ("4", "quaternário", "ligado a 4 outros carbonos", "1 carbono (sem H)"),
    ]
    x0 = 330
    for i, (b, nm, rule, here) in enumerate(rows):
        y = 15 + i * 23.5
        s.circle(x0, y, 9, fill=PD)
        s.text(x0, y + 4, b, 11.5, "middle", 800, "#FFFFFF")
        s.text(x0 + 18, y - 1, nm, 12, "start", 800, INK)
        s.text(x0 + 18 + tw(nm, 12, 800) + 8, y - 1, "— " + rule, 11, "start", 400, C["slate"])
        s.text(x0 + 18, y + 11, "aqui: " + here, 9.8, "start", 600, PD)
    s.text(x0 - 9, 109, "Conte só ligações com OUTROS carbonos: H e heteroátomos (O, N, Cl) não contam.", 10.2, "start", 700, C["red_d"])
    return s


# ------------------------------------------------------------------- classificação de cadeias
@fig("b_cadeias")
def _cadeias():
    W, H = 695, 196
    s = SVG(W, H, title="Classificação de cadeias carbônicas")
    cw = (W - 12) / 3
    items = [
        ("pentano", "CCCCC", "C5H12", "aberta · normal", "saturada · homogênea"),
        ("2-metilbut-1-eno", "C=C(C)CC", "C5H10", "aberta · ramificada", "insaturada · homogênea"),
        ("ciclo-hexano", "C1CCCCC1", "C6H12", "fechada (alicíclica)", "saturada · homogênea"),
        ("benzeno", "c1ccccc1", "C6H6", "fechada · aromática", "insaturada* · homogênea"),
        ("éter dietílico", "CCOCC", "C4H10O", "aberta · normal", "saturada · HETEROGÊNEA (O)"),
        ("piridina", "c1ccncc1", "C5H5N", "fechada · aromática", "heterocíclica (N no anel)"),
    ]
    for i, (nm, smi, fm, l1, l2) in enumerate(items):
        r, c = divmod(i, 3)
        x = 6 + c * cw
        y = 3 + r * 96
        s.rect(x + 2, y, cw - 4, 91, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        m = _std(smi, fm, bond=24, hl=(["[#8]"] if i == 4 else (["[#7]"] if i == 5 else None)))
        s.raw(m.at(x + cw / 2, y + 28, 0.74))
        s.text(x + cw / 2, y + 60, nm, 11.4, "middle", 800, INK)
        s.text(x + cw / 2, y + 73, l1, 10.2, "middle", 600, PD)
        s.text(x + cw / 2, y + 84, l2, 10.2, "middle", 600, PD)
    return s
