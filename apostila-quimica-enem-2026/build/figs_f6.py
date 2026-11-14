"""Bloco F · página 34 — eletrólise (ígnea, aquosa, fila de descarga)."""
from registry import fig
from svglib import SVG, C, tw
from figlib import chip_svg

INK = C["ink"]
OD = C["orange_d"]
GL = C["slate"]
BD = C["blue_d"]


def _vessel(s, x, y, w, h, liq, liq_top=26, stroke=GL):
    s.path(f"M{x} {y} L{x} {y + h - 8} Q{x} {y + h} {x + 8} {y + h} L{x + w - 8} {y + h} Q{x + w} {y + h} {x + w} {y + h - 8} L{x + w} {y}",
           stroke=stroke, sw=2.4)
    s.path(f"M{x + 1} {y + liq_top} L{x + 1} {y + h - 8} Q{x + 1} {y + h - 1} {x + 8} {y + h - 1} L{x + w - 8} {y + h - 1} Q{x + w - 1} {y + h - 1} {x + w - 1} {y + h - 8} L{x + w - 1} {y + liq_top} Z",
           fill=liq, opacity=0.9)


def _source(s, cx, y, xc, xa):
    """Fonte (bateria) em y; fio liga cátodo (−, esquerda) e ânodo (+, direita). Elétrons: ânodo → fonte → cátodo."""
    s.line(xc, y, cx - 7, y, INK, 2.2)
    s.line(cx + 7, y, xa, y, INK, 2.2)
    s.line(cx - 7, y - 6, cx - 7, y + 6, INK, 3.2)      # placa curta (−)
    s.line(cx + 7, y - 11, cx + 7, y + 11, INK, 2.2)    # placa longa (+)
    s.text(cx - 17, y - 8, "−", 13, "middle", 800, C["blue_d"])
    s.text(cx + 17, y - 8, "+", 13, "middle", 800, C["red_d"])
    # sentido dos elétrons
    s.arrow(xa - 10, y - 5, cx + 24, y - 5, C["orange"], 2.2, 7)
    s.arrow(cx - 24, y - 5, xc + 10, y - 5, C["orange"], 2.2, 7)
    s.text((xa + cx) / 2 + 4, y - 11, "e^−", 10, "middle", 800, OD)
    s.text((xc + cx) / 2 - 4, y - 11, "e^−", 10, "middle", 800, OD)


def _electrode(s, x, y0, y1, col="#4B5563"):
    s.rect(x - 7, y0, 14, y1 - y0, fill=col, stroke="#111827", sw=1.3, rx=2)


@fig("h_eletro_nacl")
def _nacl_aq():
    W, H = 460, 282
    s = SVG(W, H, title="Eletrólise aquosa do NaCl com eletrodos inertes")
    cx = W / 2
    bx, by, bw, bh = 52, 98, 356, 100
    _vessel(s, bx, by, bw, bh, "#DCEBFB")
    xc, xa = bx + 92, bx + bw - 92
    _electrode(s, xc, 46, by + bh - 18)
    _electrode(s, xa, 46, by + bh - 18)
    s.line(xc, 46, xc, 22, INK, 2.2)
    s.line(xa, 46, xa, 22, INK, 2.2)
    _source(s, cx, 22, xc, xa)
    # bolhas
    for dx, dy, r in ((-14, 0, 3.4), (-18, 22, 2.8), (-12, 42, 3.2)):
        s.circle(xc + dx, by + 36 + dy, r, fill="#FFFFFF", stroke=C["blue"], sw=1.1)
    for dx, dy, r in ((14, 0, 3.6), (18, 22, 3), (12, 42, 3.4)):
        s.circle(xa + dx, by + 36 + dy, r, fill="#E9F5B0", stroke="#6B8E23", sw=1.1)
    s.text(xc - 28, by + 24, "H_2(g)", 10.4, "end", 800, BD)
    s.text(xa + 28, by + 24, "Cl_2(g)", 10.4, "start", 800, C["green_d"])
    # íons
    s.text(cx, by + 30, "Na^+ e H_2O", 10, "middle", 700, C["slate"])
    s.text(cx, by + 43, "(Na^+ fica em solução)", 9, "middle", 400, C["muted"])
    s.arrow(cx + 52, by + 62, xa - 18, by + 62, C["blue"], 1.8, 6)
    s.text(cx + 8, by + 76, "Cl^− → ânodo", 9.6, "start", 800, BD)
    s.arrow(cx - 52, by + 62, xc + 18, by + 62, C["red"], 1.8, 6)
    s.text(cx - 8, by + 76, "Na^+ → cátodo", 9.6, "end", 800, C["red_d"])
    chip_svg(s, xc, by + bh + 14, "CÁTODO (−) · redução", "blue", 9.4, padx=6, h=15)
    chip_svg(s, xa, by + bh + 14, "ÂNODO (+) · oxidação", "orange", 9.4, padx=6, h=15)
    # semirreações
    s.text(xc, by + bh + 40, "2 H_2O + 2 e^− → H_2 + 2 OH^−", 10.6, "middle", 800, BD)
    s.text(xa, by + bh + 40, "2 Cl^− → Cl_2 + 2 e^−", 10.6, "middle", 800, OD)
    s.text(cx, by + bh + 62, "Global: 2 NaCl + 2 H_2O → H_2 + Cl_2 + 2 NaOH", 11, "middle", 800, INK)
    s.text(cx, by + bh + 76, "indústria cloro-soda: H_2, Cl_2 e NaOH (o OH^− fica no cátodo, com Na^+)", 9.4, "middle", 600, C["muted"])
    return s


def _small_cell(s, x0, w, liq, cat_lab, an_lab, cat_gas, an_gas, title, cat_eq, an_eq, glob, note):
    cx = x0 + w / 2
    bx, by, bw, bh = x0 + 28, 66, w - 56, 62
    s.text(cx, 12, title, 11, "middle", 800, OD)
    _vessel(s, bx, by, bw, bh, liq, liq_top=14)
    xc, xa = bx + bw * 0.27, bx + bw * 0.73
    _electrode(s, xc, 30, by + bh - 12)
    _electrode(s, xa, 30, by + bh - 12)
    s.line(xc, 30, xc, 36, INK, 2)
    # fios e fonte (mais compacta)
    yw = 30
    s.line(xc, yw, cx - 7, yw, INK, 2.2)
    s.line(cx + 7, yw, xa, yw, INK, 2.2)
    s.line(cx - 7, yw - 5, cx - 7, yw + 5, INK, 3)
    s.line(cx + 7, yw - 9, cx + 7, yw + 9, INK, 2.2)
    s.text(cx - 16, yw - 6, "−", 12, "middle", 800, BD)
    s.text(cx + 16, yw - 6, "+", 12, "middle", 800, C["red_d"])
    s.text(xc - 12, by + 20, cat_gas, 9.8, "end", 800, "#1F2937", halo=liq)
    s.text(xa + 12, by + 20, an_gas, 9.8, "start", 800, "#1F2937", halo=liq)
    chip_svg(s, xc, by + bh + 12, cat_lab, "blue", 9, padx=5, h=14)
    chip_svg(s, xa, by + bh + 12, an_lab, "orange", 9, padx=5, h=14)
    y = by + bh + 34
    s.text(xc - 4, y, cat_eq, 10, "middle", 800, BD)
    s.text(xa + 4, y, an_eq, 10, "middle", 800, OD)
    s.text(cx, y + 15, glob, 10.4, "middle", 800, INK)
    s.text(cx, y + 28, note, 9.2, "middle", 600, C["muted"])


@fig("h_ignea")
def _ignea():
    W, H = 695, 218
    s = SVG(W, H, title="Eletrólise ígnea: NaCl fundido e alumínio (Hall–Héroult)")
    half = W / 2
    for i in range(2):
        s.rect(4 + i * half, 2, half - 8, H - 4, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
    _small_cell(s, 4, half - 8, "#F6D6A8", "CÁTODO (−)", "ÂNODO (+)", "Na(l)", "Cl_2(g)",
                "Ígnea · NaCl fundido (sem água)",
                "Na^+ + e^− → Na(l)", "2 Cl^− → Cl_2 + 2 e^−", "2 NaCl(l) → 2 Na(l) + Cl_2(g)",
                "só existem íons Na^+ e Cl^−: o que descarrega é fixo")
    _small_cell(s, half + 4, half - 8, "#F6D6A8", "CÁTODO (−)", "ÂNODO (+) · grafite", "Al(l)", "CO_2",
                "Alumínio · Hall–Héroult (Al_2O_3 em criolita, ≈ 950 °C)",
                "Al^3+ + 3 e^− → Al(l)", "2 O^2− → O_2 + 4 e^−", "2 Al_2O_3 + 3 C → 4 Al + 3 CO_2",
                "o O_2 queima o ânodo de carbono (C + O_2 → CO_2): ele é consumido")
    return s


@fig("h_fila")
def _fila():
    W, H = 695, 132
    s = SVG(W, H, title="Fila de descarga em eletrólise aquosa")
    rows = [
        ("CÁTODO", "cátions (reduzem)", "blue",
         [("demais cátions", "Cu^2+, Ag^+, Zn^2+, Fe^2+, Ni^2+, Pb^2+…", "#E6F0FD"),
          ("H^+ da água", "forma H_2", "#FFFFFF"),
          ("1A, 2A e Al^3+", "Na^+, K^+, Ca^2+, Mg^2+, Al^3+ (não descarregam)", "#F3F4F6")]),
        ("ÂNODO", "ânions (oxidam)", "orange",
         [("não oxigenados", "Cl^−, Br^−, I^−, S^2−", "#FFF1E3"),
          ("OH^− da água", "forma O_2 (+ H_2O)", "#FFFFFF"),
          ("oxigenados e F^−", "SO_4^2−, NO_3^−, CO_3^2−, PO_4³^−, F^− (não descarregam)", "#F3F4F6")]),
    ]
    x0, cw, gap = 126, 176, 16
    for r, (pol, sub, kind, cells) in enumerate(rows):
        y = 6 + r * 62
        col = BD if kind == "blue" else OD
        s.text(8, y + 21, pol, 11.4, "start", 800, col)
        s.text(8, y + 34, sub, 9.2, "start", 600, C["muted"])
        for i, (t, ex, fill) in enumerate(cells):
            x = x0 + i * (cw + gap)
            s.rect(x, y, cw, 50, fill=fill, stroke=C["blue"] if kind == "blue" else C["orange"], sw=1.4, rx=8)
            s.text(x + cw / 2, y + 18, t, 11, "middle", 800, INK)
            if len(ex) > 30:
                half = ex.index("(") if "(" in ex else len(ex) // 2
                s.text(x + cw / 2, y + 32, ex[:half].strip(), 9, "middle", 600, C["slate"])
                s.text(x + cw / 2, y + 43, ex[half:].strip(), 9, "middle", 600, C["slate"])
            else:
                s.text(x + cw / 2, y + 35, ex, 9.2, "middle", 600, C["slate"])
            if i < 2:
                s.arrow(x + cw + 1, y + 25, x + cw + gap - 1, y + 25, col, 1.8, 6)
    s.text(W - 4, 6 + 2 * 62 - 2, "← descarrega primeiro  ·  descarrega por último →   (regra de ensino simplificada)", 9.2, "end", 700, C["muted"])
    return s
