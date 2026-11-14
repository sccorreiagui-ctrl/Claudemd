"""Bloco F · página 33 — pilhas e corrosão."""
import math

from registry import fig
from svglib import SVG, C, Axes, tw
from figlib import pill2, chip_svg

INK = C["ink"]
OD = C["orange_d"]
GL = C["slate"]


def _beaker(s, x, y, w, h, liq):
    s.path(f"M{x} {y} L{x} {y + h - 8} Q{x} {y + h} {x + 8} {y + h} L{x + w - 8} {y + h} Q{x + w} {y + h} {x + w} {y + h - 8} L{x + w} {y}",
           stroke=GL, sw=2.4)
    s.path(f"M{x + 1} {y + 24} L{x + 1} {y + h - 8} Q{x + 1} {y + h - 1} {x + 8} {y + h - 1} L{x + w - 8} {y + h - 1} Q{x + w - 1} {y + h - 1} {x + w - 1} {y + h - 8} L{x + w - 1} {y + 24} Z",
           fill=liq, opacity=0.9)


@fig("g_daniell")
def _daniell():
    W, H = 460, 296
    s = SVG(W, H, title="Pilha de Daniell")
    bx1, bx2, by, bw, bh = 34, 262, 126, 164, 100
    _beaker(s, bx1, by, bw, bh, "#DDEBFB")
    _beaker(s, bx2, by, bw, bh, "#7FB2F0")
    # eletrodos
    ez, ec = bx1 + 82, bx2 + 82
    s.rect(ez - 9, 60, 18, 128, fill="#9AA3AF", stroke=GL, sw=1.6, rx=2)
    s.rect(ec - 9, 60, 18, 128, fill="#C9773B", stroke="#7C3F12", sw=1.6, rx=2)
    s.text(ez, 176, "Zn", 11.4, "middle", 800, "#FFFFFF")
    s.text(ec, 176, "Cu", 11.4, "middle", 800, "#FFFFFF")
    # soluções
    s.text(bx1 + bw / 2, by + bh + 14, "ZnSO_4 (aq)", 10.4, "middle", 800, C["blue_d"])
    s.text(bx2 + bw / 2, by + bh + 14, "CuSO_4 (aq)", 10.4, "middle", 800, C["blue_d"])
    # fio externo e voltímetro
    s.path(f"M{ez} 60 L{ez} 34 L{ec} 34 L{ec} 60", stroke=INK, sw=2.2)
    s.circle((ez + ec) / 2, 34, 17, fill="#FFFFFF", stroke=INK, sw=2)
    s.text((ez + ec) / 2, 31, "V", 12, "middle", 800, INK)
    s.text((ez + ec) / 2, 43, "1,10 V", 9.6, "middle", 800, C["red_d"])
    s.arrow(ez + 6, 34, (ez + ec) / 2 - 20, 34, C["orange"], 2.4, 8)
    s.arrow((ez + ec) / 2 + 20, 34, ec - 6, 34, C["orange"], 2.4, 8)
    s.text((ez + ec) / 2, 11, "fluxo de elétrons (e⁻): do Zn para o Cu", 10, "middle", 800, OD)
    # ponte salina (arco)
    s.path(f"M{bx1 + bw - 28} {by + 34} L{bx1 + bw - 28} 80 Q{bx1 + bw - 28} 56 {bx1 + bw - 4} 56 L{bx2 + 4} 56 Q{bx2 + 28} 56 {bx2 + 28} 80 L{bx2 + 28} {by + 34}",
           stroke=GL, sw=9)
    s.path(f"M{bx1 + bw - 28} {by + 34} L{bx1 + bw - 28} 80 Q{bx1 + bw - 28} 56 {bx1 + bw - 4} 56 L{bx2 + 4} 56 Q{bx2 + 28} 56 {bx2 + 28} 80 L{bx2 + 28} {by + 34}",
           stroke="#FDE8A8", sw=6)
    s.text((bx1 + bw + bx2) / 2, 78, "ponte salina", 10, "middle", 800, GL)
    s.text((bx1 + bw + bx2) / 2, 91, "(KNO_3 ou KCl)", 9.2, "middle", 600, C["muted"])
    # íons na ponte
    s.arrow(bx2 - 14, 64, bx1 + bw - 8, 64, C["red_d"], 1.6, 6) if False else None
    s.text(bx1 + bw + 8, 92, "ânions (−) →", 9, "start", 800, C["blue_d"]) if False else None
    s.text(bx1 + bw - 36, 100, "ânions", 9.2, "end", 800, C["blue_d"])
    s.arrow(bx1 + bw - 36, 108, bx1 + bw - 62, 108, C["blue"], 1.8, 6)
    s.text(bx2 + 36, 100, "cátions", 9.2, "start", 800, C["blue_d"])
    s.arrow(bx2 + 36, 108, bx2 + 62, 108, C["blue"], 1.8, 6)
    # polos e semirreações
    chip_svg(s, ez, 112, "ÂNODO (−)", "orange", 9.6, padx=6, h=15)
    chip_svg(s, ec, 112, "CÁTODO (+)", "orange", 9.6, padx=6, h=15)
    s.text(bx1 + bw / 2, 258, "Zn → Zn^2+ + 2 e⁻   (oxidação)", 10.6, "middle", 800, OD)
    s.text(bx1 + bw / 2, 271, "Zn desgasta · [Zn^2+] aumenta", 9.6, "middle", 600, C["slate"])
    s.text(bx2 + bw / 2, 258, "Cu^2+ + 2 e⁻ → Cu   (redução)", 10.6, "middle", 800, OD)
    s.text(bx2 + bw / 2, 271, "Cu deposita · [Cu^2+] diminui", 9.6, "middle", 600, C["slate"])
    s.text(W / 2, 290, "Zn(s) | Zn^2+(aq) || Cu^2+(aq) | Cu(s)     ΔE° = 0,34 − (−0,76) = +1,10 V", 10.4, "middle", 800, INK)
    return s


@fig("g_potenciais")
def _pot():
    W, H = 695, 128
    s = SVG(W, H, title="Potenciais padrão de redução")
    x0, x1 = 28, 667
    X = lambda v: x0 + (v + 3.2) / (3.2 + 1.7) * (x1 - x0)
    by = 56
    g = s.lingrad([(0, "#F2A15C"), (0.5, "#E5E7EB"), (1, "#3B6FE0")])
    s.rect(x0, by, x1 - x0, 14, fill=g, stroke=C["line"], sw=1, rx=7)
    els = [("Li", -3.04), ("Na", -2.71), ("Mg", -2.37), ("Al", -1.66), ("Zn", -0.76), ("Fe", -0.44), ("Pb", -0.13), ("H₂", 0.0),
           ("Cu", 0.34), ("Ag", 0.80), ("Au", 1.50)]
    ys = {0: by - 22, 1: by + 14 + 24}
    for i, (sym, v) in enumerate(els):
        top = i % 2 == 0
        cy = ys[0] if top else ys[1]
        x = X(v)
        s.line(x, cy + 8.5 if top else by + 14, x, by if top else cy - 8.5, C["slate_m"], 1.0)
        s.circle(x, by + 7, 3.2, fill="#fff", stroke=INK, sw=1.2)
        pill2(s, x, cy, sym.replace("₂", "_2") if False else sym, ("%+.2f" % v).replace(".", ",").replace("-", "−") if v else "0,00",
              "#FFFFFF", C["slate_m"], INK)
    s.text(x0, 12, "← oxida com mais facilidade", 10, "start", 800, OD)
    s.text(x0, 24, "bom ânodo, bom agente redutor", 9.4, "start", 600, C["muted"])
    s.text(x1, 12, "reduz com mais facilidade →", 10, "end", 800, C["blue_d"])
    s.text(x1, 24, "bom cátodo, bom agente oxidante", 9.4, "end", 600, C["muted"])
    s.text(W / 2, H - 4, "E° de redução (V, 25 °C, 1 mol/L, 1 atm); metal de MENOR E° oxida e vira ânodo", 9.6, "middle", 700, C["muted"])
    return s


def _bar(s, x, y, w, coat, coat_col, scratch=True):
    s.rect(x, y, w, 22, fill="#9AA3AF", stroke=GL, sw=1.4, rx=2)
    if coat:
        s.rect(x, y - 5, w, 6, fill=coat_col, stroke=GL, sw=0.8)
        if scratch:
            s.rect(x + w / 2 - 12, y - 6, 24, 8, fill="#FFFFFF")
    return


@fig("g_corrosao")
def _corr():
    W, H = 695, 172
    s = SVG(W, H, title="Corrosão e proteção do ferro")
    cw = W / 3
    titles = ["Ferro exposto", "Galvanizado (Zn) riscado", "Folha-de-flandres (Sn) riscada"]
    for i, t in enumerate(titles):
        x = i * cw
        s.rect(x + 3, 3, cw - 6, H - 6, fill="#FFFFFF", stroke=C["grid"], sw=1.2, rx=9)
        s.text(x + cw / 2, 18, t, 11, "middle", 800, OD)
        bx, by_, bw = x + 22, 70, cw - 44
        s.rect(bx, by_, bw, 24, fill="#9AA3AF", stroke=GL, sw=1.4, rx=2)
        if i > 0:
            col = "#D3E4FA" if i == 1 else "#E8E4D2"
            s.rect(bx, by_ - 6, bw / 2 - 14, 6, fill=col, stroke=GL, sw=0.8)
            s.rect(bx + bw / 2 + 14, by_ - 6, bw / 2 - 14, 6, fill=col, stroke=GL, sw=0.8)
        s.ellipse(bx + bw / 2, by_ - 12, 22, 9, fill="#BBD6F8", stroke=C["blue"], sw=1.2)
        s.text(bx + bw / 2, by_ - 9, "H_2O + O_2", 8.4, "middle", 800, C["blue_d"])
        if i == 0:
            s.circle(bx + bw / 2, by_ + 12, 6, fill="#B5651D", opacity=0.9)
            s.text(x + cw / 2, 118, "Fe → Fe^2+ + 2 e⁻ (ânodo)", 10, "middle", 800, OD)
            s.text(x + cw / 2, 131, "O_2 + 2H_2O + 4e⁻ → 4OH⁻ (cátodo)", 9.6, "middle", 700, C["slate"])
            s.text(x + cw / 2, 148, "ferrugem: Fe_2O_3·nH_2O", 10, "middle", 800, C["red_d"])
            s.text(x + cw / 2, 161, "(porosa: não protege)", 9.2, "middle", 400, C["muted"])
        elif i == 1:
            s.text(bx + 24, by_ - 14, "Zn", 9.6, "middle", 800, C["blue_d"])
            s.text(bx + bw - 24, by_ - 14, "Zn", 9.6, "middle", 800, C["blue_d"])
            s.text(x + cw / 2, 118, "Zn é o ânodo de sacrifício:", 10, "middle", 800, C["green_d"])
            s.text(x + cw / 2, 131, "Zn → Zn^2+ + 2e⁻ (E° Zn < E° Fe)", 9.6, "middle", 700, C["slate"])
            s.text(x + cw / 2, 148, "o Fe fica protegido,", 10, "middle", 800, C["green_d"])
            s.text(x + cw / 2, 161, "mesmo com a camada riscada", 9.2, "middle", 400, C["muted"])
        else:
            s.text(bx + 24, by_ - 14, "Sn", 9.6, "middle", 800, C["slate"])
            s.text(bx + bw - 24, by_ - 14, "Sn", 9.6, "middle", 800, C["slate"])
            s.text(x + cw / 2, 118, "Sn é menos reativo que Fe", 10, "middle", 800, C["red_d"])
            s.text(x + cw / 2, 131, "(E° Sn > E° Fe): o Fe vira ânodo", 9.6, "middle", 700, C["slate"])
            s.text(x + cw / 2, 148, "e oxida mais rápido que sozinho", 10, "middle", 800, C["red_d"])
            s.text(x + cw / 2, 161, "quando a camada é riscada", 9.2, "middle", 400, C["muted"])
        # setas de elétrons
        if i == 1:
            s.arrow(bx + bw / 2 - 40, by_ - 2, bx + bw / 2 - 8, by_ + 12, C["orange"], 2, 6)
            s.text(bx + bw / 2 - 30, by_ + 22, "e⁻", 9, "middle", 800, OD)
        if i == 2:
            s.arrow(bx + bw / 2 + 6, by_ + 12, bx + bw / 2 + 40, by_ - 2, C["orange"], 2, 6)
            s.text(bx + bw / 2 + 34, by_ + 22, "e⁻", 9, "middle", 800, OD)
    return s
