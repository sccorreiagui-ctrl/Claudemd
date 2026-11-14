"""Módulo C — Geografia Agrária: gráficos (Censo Agro 2017) e diagramas."""
import math, random
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, wrap, text_width
from common import save_svg

SKY = "#EAF4FC"
SOIL = "#8D5B2E"
GREEN = "#43A047"
FAM = "#2E7D32"        # familiar
NFAM = "#E65100"       # não familiar (empresarial)


def barras_censo():
    f = Fig(FULL, 204, "agro_censo", "Agricultura familiar no Censo Agropecuário 2017")
    W = FULL
    f.rect(0, 0, W, 204, fill="#FFFFFF")
    f.text(0, 0, "Agricultura familiar × não familiar no Brasil (Censo Agropecuário 2017, IBGE)", 8.4, 800, "#5D3A1A")
    x0, bw = 150, 430
    rows = [("Estabelecimentos", 77, "≈ 3,9 milhões de ≈ 5,07 milhões"), ("Área ocupada", 23, "80,9 milhões de hectares"),
            ("Valor da produção", 23, "R$ 107 bi de R$ 465 bi"), ("Pessoal ocupado", 67, "2/3 do pessoal do campo")]
    y = 26
    for lab, v, sub in rows:
        f.text(0, y + 2, lab, 7.4, 800, INK)
        f.text(0, y + 14, sub, 6.0, 500, MUTED)
        f.rect(x0, y, bw * v / 100, 24, fill=FAM)
        f.rect(x0 + bw * v / 100, y, bw * (100 - v) / 100, 24, fill=NFAM)
        f.text(x0 + 6, y + 12, f"{v}%", 8.6, 800, "#FFFFFF", valign="mid") if v >= 15 else None
        f.text(x0 + bw - 6, y + 12, f"{100 - v}%", 8.6, 800, "#FFFFFF", "end", valign="mid")
        y += 34
    f.rect(x0, 166, 10, 8, fill=FAM); f.text(x0 + 14, 164, "Agricultura familiar (Lei 11.326/2006)", 6.6, 700, INK)
    f.rect(x0 + 220, 166, 10, 8, fill=NFAM); f.text(x0 + 234, 164, "Não familiar", 6.6, 700, INK)
    f.text(0, 182, "Ideia central: muitos estabelecimentos e muita gente ocupada em pouca área; pouca área concentra grande parte do valor.", 6.3, 700, "#5D3A1A")
    f.text(0, 191, "Os números NÃO significam que a agricultura familiar produza “70% dos alimentos” do país; o recorte é por estabelecimentos.", 5.9, 600, "#B71C1C")
    save_svg("agro_censo", f.render())


def concentracao():
    f = Fig(HALF, 150, "agro_concentracao", "Concentração fundiária: estabelecimentos de 1.000 ha ou mais")
    W = HALF
    f.rect(0, 0, W, 150, fill="#FFFFFF")
    f.text(0, 0, "Concentração fundiária (Censo Agro 2017)", 8.0, 800, "#5D3A1A")
    x0, bw = 8, W - 16
    f.text(x0, 24, "Estabelecimentos com 1.000 ha ou mais", 6.8, 800, INK)
    f.text(x0, 34, "51.203 estabelecimentos", 6.0, 500, MUTED)
    y = 46
    f.text(x0, y, "% dos estabelecimentos", 6.3, 700, MUTED)
    f.rect(x0, y + 11, bw, 20, fill="#EFEBE9")
    f.rect(x0, y + 11, max(bw * 0.01, 3), 20, fill="#B71C1C")
    f.text(x0 + 10, y + 21, "1,0%", 8.4, 800, "#B71C1C", valign="mid")
    y = 92
    f.text(x0, y, "% da área total dos estabelecimentos", 6.3, 700, MUTED)
    f.rect(x0, y + 11, bw, 20, fill="#EFEBE9")
    f.rect(x0, y + 11, bw * 0.476, 20, fill="#B71C1C")
    f.text(x0 + bw * 0.476 + 6, y + 21, "47,6%", 8.4, 800, "#B71C1C", valign="mid")
    f.text(x0, 134, "Poucos estabelecimentos controlam quase metade da área.", 6.2, 700, "#5D3A1A")
    save_svg("agro_concentracao", f.render())


# ----------------------------------------------------------------------------- cenas
def field(f, x, y, w, h, color, rows=6, horizontal=True, bg="#C9A77C"):
    f.rect(x, y, w, h, fill=bg)
    if horizontal:
        for i in range(rows):
            yy = y + (i + 0.5) * h / rows
            f.line(x + 2, yy, x + w - 2, yy, color, max(1.6, h / rows * 0.55), cap="butt")
    else:
        for i in range(rows):
            xx = x + (i + 0.5) * w / rows
            f.line(xx, y + 2, xx, y + h - 2, color, max(1.6, w / rows * 0.55), cap="butt")


def person(f, x, y, s=1.0, c="#37474F"):
    f.circle(x, y - 14 * s, 3.4 * s, fill=c)
    f.line(x, y - 10 * s, x, y, c, 2.0 * s)
    f.line(x, y - 7 * s, x - 4 * s, y - 2 * s, c, 1.6 * s)
    f.line(x, y - 7 * s, x + 4 * s, y - 2 * s, c, 1.6 * s)
    f.line(x, y, x - 3 * s, y + 8 * s, c, 1.6 * s)
    f.line(x, y, x + 3 * s, y + 8 * s, c, 1.6 * s)


def house(f, x, y, s=1.0):
    f.rect(x, y - 14 * s, 22 * s, 14 * s, fill="#F5E6C8", stroke="#8C6039", sw=0.8)
    f.poly([(x - 3 * s, y - 14 * s), (x + 11 * s, y - 26 * s), (x + 25 * s, y - 14 * s)], fill="#B2493A", stroke="#7C2F25", sw=0.8)
    f.rect(x + 8 * s, y - 8 * s, 6 * s, 8 * s, fill="#8C6039")


def tractor(f, x, y, s=1.0, big=False, color="#E65100"):
    f.rect(x, y - 12 * s, 20 * s, 8 * s, fill=color)
    f.rect(x + 12 * s, y - 20 * s, 8 * s, 8 * s, fill=color)
    f.circle(x + 5 * s, y - 2 * s, 5 * s, fill="#263238")
    f.circle(x + 18 * s, y - 2 * s, 3.4 * s, fill="#263238")


def cow(f, x, y, s=1.0):
    f.rect(x - 7 * s, y - 7 * s, 14 * s, 7 * s, fill="#FFFFFF", stroke="#455A64", sw=0.8, rx=2)
    f.rect(x - 7 * s, y - 7 * s, 5 * s, 5 * s, fill="#37474F", rx=1)
    f.rect(x + 7 * s, y - 9 * s, 4 * s, 4 * s, fill="#FFFFFF", stroke="#455A64", sw=0.7)
    for dx in (-5, -1, 3, 6):
        f.line(x + dx * s, y, x + dx * s, y + 4 * s, "#455A64", 1.0)


def cena_fam_emp():
    f = Fig(FULL, 214, "agro_familiar_empresarial", "Agricultura familiar e agricultura empresarial")
    W = FULL
    hw = (W - 12) / 2
    f.g("translate(0,-32)")
    for i in (0, 1):
        f.rect(i * (hw + 12), 56, hw, 90, fill=SKY)
    for k, (xx, yy, w_, h_, c_) in enumerate([(8, 96, 70, 46, "#F9A825"), (82, 96, 60, 46, "#43A047"), (146, 96, 70, 46, "#8D6E63"), (220, 96, 60, 46, "#66BB6A"), (284, 96, 52, 46, "#EF5350")]):
        field(f, xx, yy, w_, h_, c_, rows=5, horizontal=(k % 2 == 0))
    house(f, 20, 96, 1.0); person(f, 62, 96, 0.9); person(f, 74, 96, 0.8, "#6D4C41")
    f.tree(300, 92, 0.9); f.sun(330, 78, 7)
    f.text(8, 60, "poucos hectares, vários cultivos (policultura)", 6.2, 800, "#1B5E20")
    x1 = hw + 12
    field(f, x1 + 8, 96, hw - 16, 46, "#7CB342", rows=8, horizontal=True)
    tractor(f, x1 + 40, 100, 1.4); tractor(f, x1 + 120, 106, 1.2, color="#FDD835")
    f.poly([(x1 + 250, 96), (x1 + 262, 70), (x1 + 274, 70), (x1 + 286, 96)], fill="#CFD8DC", stroke="#78909C", sw=0.8)
    f.rect(x1 + 262, 56, 12, 14, fill="#B0BEC5", stroke="#78909C", sw=0.8)
    f.text(x1 + 8, 60, "centenas ou milhares de ha, uma cultura (monocultura)", 6.2, 800, "#B23C00")
    f.sun(x1 + 320, 78, 7)
    f.circle(x1 + 180, 80, 3, fill="#455A64"); f.line(x1 + 170, 76, x1 + 190, 76, "#455A64", 1.2); f.line(x1 + 170, 84, x1 + 190, 84, "#455A64", 1.2)
    f.text(x1 + 180, 87, "drone / GPS", 5.8, 800, "#455A64", "middle")
    f.gend()
    for i, (title, col_) in enumerate([("AGRICULTURA FAMILIAR", FAM), ("AGRICULTURA EMPRESARIAL (NÃO FAMILIAR)", NFAM)]):
        x0 = i * (hw + 12)
        f.rect(x0, 0, hw, 22, fill=col_, rx=4)
        f.text(x0 + hw / 2, 11, title, 7.2, 800, "#FFFFFF", "middle", valign="mid")
    attrs = [("Área", "pequena (limite legal: até 4 módulos fiscais)", "grande, em geral acima do limite familiar"),
             ("Trabalho", "predominantemente da família", "assalariado; poucos operadores qualificados"),
             ("Capital e tecnologia", "variáveis; em geral menor", "alto capital, máquinas, insumos, crédito"),
             ("Produção e destino", "diversificada: consumo da família e mercado local", "monocultura de commodities (soja, milho, cana); exportação")]
    y = 118
    for lab, a, b in attrs:
        f.rect(0, y, hw, 22, fill="#E8F5E9", rx=3)
        f.rect(hw + 12, y, hw, 22, fill="#FFF0E0", rx=3)
        f.text(6, y + 11, f"**{lab}:** {a}", 6.1, 500, "#1B5E20", valign="mid")
        f.text(hw + 18, y + 11, f"**{lab}:** {b}", 6.1, 500, "#B23C00", valign="mid")
        y += 24
    save_svg("agro_familiar_empresarial", f.render())


def cena_int_ext():
    f = Fig(FULL, 168, "agro_intensiva_extensiva", "Agricultura/pecuária intensiva e extensiva")
    W = FULL
    hw = (W - 12) / 2
    f.g("translate(0,-44)")
    for i in (0, 1):
        f.rect(i * (hw + 12), 68, hw, 76, fill=SKY)
    f.rect(8, 100, 120, 36, fill="#7CB342")
    for i in range(7):
        f.line(14 + i * 16, 100, 14 + i * 16, 136, "#558B2F", 3.0)
    f.path("M8,92 q60,-14 120,0", stroke="#1E88E5", sw=1.6, dash="3 2")
    f.raindrops(30, 96, 3, "#1E88E5", 22, 6)
    f.poly([(140, 136), (140, 108), (176, 92), (212, 108), (212, 136)], fill="#E3F2FD", stroke="#78909C", sw=1.0)
    f.text(176, 122, "estufa", 5.8, 800, "#37474F", "middle")
    f.rect(226, 112, 100, 24, fill="#BCAAA4", stroke="#6D4C41", sw=0.8)
    for xx in (236, 258, 280, 302):
        cow(f, xx, 130, 0.9)
    f.text(276, 100, "confinamento", 5.8, 800, "#4E342E", "middle", halo="#EAF4FC")
    f.text(8, 72, "área pequena · alto capital, tecnologia, ração e vacinas", 6.2, 800, "#0D47A1")
    x1 = hw + 12
    f.rect(x1, 100, hw, 36, fill="#9CCC65")
    f.path(f"M{x1},100 C {x1+80},84 {x1+180},96 {x1+hw},88 L{x1+hw},100 Z", fill="#AED581")
    for (xx, yy) in [(60, 124), (150, 114), (240, 126)]:
        cow(f, x1 + xx, yy, 0.9)
    person(f, x1 + 296, 130, 0.9, "#6D4C41")
    f.line(x1, 98, x1 + hw, 98, "#8D6E63", 1.2, dash="1 5")
    f.tree(x1 + 120, 100, 0.8); f.tree(x1 + 220, 98, 0.8)
    f.text(x1 + 8, 72, "grande área · pouco capital e poucos trabalhadores", 6.2, 800, "#5D3A1A")
    f.gend()
    for i, (title, col_) in enumerate([("INTENSIVA: muito capital por hectare", "#1565C0"), ("EXTENSIVA: muita área, pouco capital por hectare", "#8D5B2E")]):
        x0 = i * (hw + 12)
        f.rect(x0, 0, hw, 22, fill=col_, rx=4)
        f.text(x0 + hw / 2, 11, title, 7.0, 800, "#FFFFFF", "middle", valign="mid")
    attrs = [("Investimento por hectare", "alto", "baixo"), ("Produtividade por hectare", "alta", "baixa"),
             ("Mão de obra", "mais especializada", "pouca (poucos vaqueiros)"), ("Ex. no Brasil", "granjas, cana irrigada, hortifruti, confinamento", "pecuária de corte em grandes pastos (CO, Norte)")]
    y = 104
    for lab, a, b in attrs:
        f.rect(0, y, hw, 16, fill="#E3F2FD", rx=3)
        f.rect(hw + 12, y, hw, 16, fill="#F4EBE0", rx=3)
        f.text(6, y + 8, f"**{lab}:** {a}", 6.1, 500, "#0D47A1", valign="mid")
        f.text(hw + 18, y + 8, f"**{lab}:** {b}", 6.1, 500, "#5D3A1A", valign="mid")
        y += 17
    save_svg("agro_intensiva_extensiva", f.render())


def revolucao_verde():
    f = Fig(FULL, 236, "revolucao_verde", "Revolução Verde: pacote tecnológico e consequências")
    W = FULL
    f.rect(0, 0, W, 236, fill="#FFFFFF")
    f.rect(0, 0, 470, 20, fill="#E65100", rx=4)
    f.text(235, 10, "PACOTE TECNOLÓGICO (difundido a partir dos anos 1940–60)", 6.8, 800, "#FFFFFF", "middle", valign="mid")
    pk = [("Máquinas e mecanização", "terra"), ("Sementes melhoradas (híbridos de alto rendimento)", "verde"), ("Fertilizantes (NPK) e calagem", "azul"),
          ("Agrotóxicos (defensivos)", "vermelho"), ("Irrigação", "azul"), ("Crédito e assistência técnica", "laranja")]
    for i, (t, c) in enumerate(pk):
        r, k = divmod(i, 3)
        f.box(k * 160, 28 + r * 38, 150, 32, t, fill=c, pt=6.6, weight=700)
    f.arrow(476, 62, 508, 62, "#37474F", 3.0, 11)
    f.box(514, 28, 196, 70, "↑ produtividade e produção de alimentos e commodities", fill="verde", pt=7.4, weight=800)
    f.text(612, 104, "efeito positivo: oferta e escala", 5.9, 600, MUTED, "middle")
    f.text(0, 112, "CONSEQUÊNCIAS", 6.6, 800, "#5D3A1A")
    cols = [("TÉCNICAS", "#8D5B2E", ["Mecanização", "Monocultura em grande escala", "Dependência de insumos industriais"]),
            ("ECONÔMICAS E SOCIAIS", "#E65100", ["Custo alto: pequenos produtores endividados", "Concentração fundiária e de renda", "Menos empregos por hectare → êxodo rural"]),
            ("AMBIENTAIS", "#C62828", ["Erosão e compactação do solo", "Contaminação por agrotóxicos e NPK", "Eutrofização e perda de biodiversidade", "Pragas resistentes (seleção)"])]
    cw = (W - 24) / 3
    for i, (title, c, items) in enumerate(cols):
        x0 = i * (cw + 12)
        f.rect(x0, 124, cw, 18, fill=c, rx=4)
        f.text(x0 + cw / 2, 133, title, 6.6, 800, "#FFFFFF", "middle", valign="mid")
        yy = 146
        for it in items:
            f.rect(x0, yy, cw, 17, fill="#FFFFFF", stroke=c, sw=1.0, rx=3)
            f.text(x0 + 6, yy + 8.5, it, 6.1, 600, INK, valign="mid")
            yy += 19
    f.text(0, 226, "Cadeia: mecanização → menor demanda de trabalho rural → êxodo rural → expansão urbana (tendência histórica; varia por região e cultura).", 6.4, 800, "#5D3A1A")
    save_svg("revolucao_verde", f.render())


def eutrofizacao():
    f = Fig(FULL, 216, "eutrofizacao", "Eutrofização")
    W = FULL
    f.rect(0, 0, W, 216, fill="#FFFFFF")
    steps = [("Adubação com N e P (fertilizantes)", "marrom"), ("Chuva carrega o excesso (lixiviação e escoamento) até rios e lagos", "azul"), ("Água rica em nutrientes", "azul"),
             ("Proliferação de algas e cianobactérias (“floração”)", "verde"), ("A camada de algas bloqueia a luz", "verde"), ("Plantas submersas morrem: menos fotossíntese", "verde"),
             ("Bactérias decompõem a matéria orgânica e consomem O₂", "laranja"), ("Queda do oxigênio dissolvido: mortandade de peixes", "vermelho")]
    cmap = {"marrom": "terra"}
    bw, bh, gap = 158, 46, 26
    pos = []
    for i, (t, c) in enumerate(steps):
        row, colx = divmod(i, 4)
        x = colx * (bw + gap)
        y = 6 + row * 78
        f.box(x, y, bw, bh, t, fill=cmap.get(c, c), pt=6.6, weight=700, rx=6)
        f.badge(x + 10, y - 2, i + 1, "navy", 7.5, 6.4)
        pos.append((x, y))
    for i in range(7):
        (x, y), (x2, y2) = pos[i], pos[i + 1]
        if i % 4 != 3:
            f.arrow(x + bw + 1, y + bh / 2, x2 - 1, y2 + bh / 2, "#37474F", 1.6, 6)
    # volta de linha
    f.curve_arrow(pos[3][0] + bw / 2, pos[3][1] + bh + 1, pos[3][0] + bw / 2, 100, pos[4][0] + bw / 2 + 60, pos[4][1] - 3, "#37474F", 1.6, 6) if False else f.arrow(pos[3][0] + bw / 2, pos[3][1] + bh + 1, pos[4][0] + bw / 2 + 1, pos[4][1] - 2, "#37474F", 1.6, 6) if False else None
    f.path(f"M{pos[3][0]+bw/2},{pos[3][1]+bh+1} V{pos[3][1]+bh+14} H{pos[4][0]+bw/2} V{pos[4][1]-3}", stroke="#37474F", sw=1.6)
    f.poly([(pos[4][0] + bw / 2, pos[4][1] - 1), (pos[4][0] + bw / 2 - 3.5, pos[4][1] - 8), (pos[4][0] + bw / 2 + 3.5, pos[4][1] - 8)], fill="#37474F")
    # lago saudável × eutrofizado
    y0 = 166
    f.rect(0, y0, 340, 40, fill="#B3E5FC", stroke="#64B5F6", sw=0.8, rx=4)
    f.text(8, y0 + 4, "LAGO SAUDÁVEL", 6.2, 800, "#0D47A1")
    for xx in (90, 160, 230):
        f.path(f"M{xx},{y0+34} q4,-8 8,0 M{xx+14},{y0+34} q4,-10 8,0", stroke="#2E7D32", sw=1.2)
    f.path("M120,%d q10,-4 20,0 l-6,-3 m6,3 l-6,3" % (y0 + 20), stroke="#546E7A", sw=1.2)
    f.rect(370, y0, 340, 40, fill="#7CB342", stroke="#558B2F", sw=0.8, rx=4)
    f.text(378, y0 + 4, "LAGO EUTROFIZADO", 6.2, 800, "#FFFFFF")
    f.text(540, y0 + 22, "algas cobrem a superfície · peixes mortos", 6.2, 800, "#1B5E20", "middle", halo="#C5E1A5")
    f.path("M470,%d q10,4 20,0 l-8,4 m8,-4 l-8,-4" % (y0 + 32), stroke="#37474F", sw=1.0)
    f.text(0, 208, "Química/Biologia: N e P (fósforo) em excesso; consumo de O₂ na decomposição aeróbia (DBO). Esgoto doméstico também causa eutrofização.", 6.1, 700, "#5D3A1A")
    save_svg("eutrofizacao", f.render())


def manejo_solo():
    f = Fig(FULL, 212, "manejo_solo", "Erosão em encosta e práticas conservacionistas")
    W = FULL
    pw = (W - 24) / 3
    titles = [("SEM MANEJO: plantio morro abaixo", "#C62828"), ("CURVAS DE NÍVEL: plantio em contorno", "#1B5E20"), ("TERRACEAMENTO: degraus na encosta", "#1565C0")]
    for i, (t, c) in enumerate(titles):
        x0 = i * (pw + 12)
        f.rect(x0, 0, pw, 20, fill=c, rx=4)
        f.text(x0 + pw / 2, 10, t, 6.2, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 22, pw, 112, fill=SKY)
    # perfil de encosta
    def slope(x0):
        return [(x0, 60), (x0 + pw * 0.15, 66), (x0 + pw * 0.9, 124), (x0 + pw, 128)]
    # 1: sem manejo
    s1 = slope(0)
    f.poly(s1 + [(pw, 134), (0, 134)], fill="#C9A77C", stroke="#8C6039", sw=1.0)
    for k in range(5):
        xx = pw * (0.2 + k * 0.15)
        f.line(xx, 70 + k * 12, xx + 18, 86 + k * 12, "#7CB342", 3.0)
    for (a, b) in [(40, 78), (74, 98), (104, 114)]:
        f.arrow(a, b, a + 20, b + 12, "#1E88E5", 2.0, 6)
    f.path(f"M{pw*0.5},96 q4,10 10,14 q-2,6 6,10", stroke="#6D4C41", sw=2.2)
    f.text(pw / 2, 26, "chuva escorre depressa", 5.8, 800, "#C62828", "middle")
    f.text(pw / 2 + 10, 122, "voçoroca (sulco) · assoreamento", 5.6, 800, "#FFFFFF", "middle")
    # 2: curvas de nível (linhas em contorno)
    x2 = pw + 12
    f.poly(slope(x2) + [(x2 + pw, 134), (x2, 134)], fill="#C9A77C", stroke="#8C6039", sw=1.0)
    for k in range(5):
        px = x2 + pw * (0.12 + k * 0.17)
        py = 66 + k * 12
        f.line(px - 12, py + 5, px + 14, py - 1, "#2E7D32", 4.0, cap="butt")
    for (a, b) in [(x2 + 40, 78), (x2 + 74, 98)]:
        f.arrow(a, b, a + 12, b + 4, "#1E88E5", 1.6, 5)
    f.text(x2 + pw / 2, 26, "fileiras acompanham as cotas", 5.8, 800, "#1B5E20", "middle")
    f.text(x2 + pw / 2, 122, "a água perde velocidade e infiltra", 5.6, 800, "#FFFFFF", "middle")
    # 3: terraços
    x3 = 2 * (pw + 12)
    steps_ = [(x3 + 8, 68), (x3 + 40, 68), (x3 + 40, 82), (x3 + 72, 82), (x3 + 72, 96), (x3 + 104, 96), (x3 + 104, 110), (x3 + 136, 110), (x3 + 136, 122), (x3 + pw, 122)]
    f.poly([(x3, 68)] + steps_ + [(x3 + pw, 134), (x3, 134)], fill="#C9A77C", stroke="#8C6039", sw=1.0)
    for (a, b) in [(x3 + 8, 68), (x3 + 40, 82), (x3 + 72, 96), (x3 + 104, 110)]:
        f.line(a + 2, b - 3, a + 28, b - 3, "#7CB342", 4.0, cap="butt")
    f.arrow(x3 + 14, 56, x3 + 28, 62, "#1E88E5", 1.6, 5)
    f.text(x3 + pw / 2, 26, "patamares retêm a água", 5.8, 800, "#0D47A1", "middle")
    f.text(x3 + pw / 2, 126, "técnica milenar (Incas, Andes)", 5.6, 800, "#FFFFFF", "middle")
    # texto abaixo
    cols = ["Sem proteção o solo perde a camada fértil (A); sedimentos assoreiam rios e açudes.", "As linhas de plantio seguem a mesma altitude (curvas de nível): menor escoamento e mais infiltração.", "Degraus horizontais quebram a velocidade da água; usado em encostas íngremes."]
    for i, t in enumerate(cols):
        f.para(i * (pw + 12) + 2, 142, pw - 4, t, 6.3, 600, INK, lh=1.2)
    f.rect(0, 186, W, 22, fill="#F4EBE0", rx=4)
    f.text(W / 2, 197, "Também: plantio direto (palhada), cobertura vegetal, rotação de culturas, pousio, cordões de vegetação e matas ciliares.", 6.5, 800, "#5D3A1A", "middle", valign="mid")
    save_svg("manejo_solo", f.render())


def rotacao():
    f = Fig(FULL, 112, "rotacao_culturas", "Rotação de culturas, leguminosas e fixação de nitrogênio")
    W = FULL
    f.rect(0, 0, W, 112, fill="#FFFFFF")
    items = [("ANO 1: SOJA (leguminosa)", "#2E7D32", "bactérias Rhizobium nas raízes fixam N₂ do ar → nitrogênio no solo"), ("ANO 2: MILHO (gramínea)", "#F9A825", "aproveita o nitrogênio deixado; quebra o ciclo de pragas"),
             ("ANO 3: POUSIO ou adubo verde", "#8D6E63", "solo “descansa”: regenera microbiota, matéria orgânica e nutrientes")]
    bw = 214
    for i, (t, c, d) in enumerate(items):
        x = i * (bw + 34)
        field(f, x, 8, bw, 40, c, rows=6, bg="#C9A77C")
        f.rect(x, 52, bw, 14, fill=c, rx=3)
        f.text(x + bw / 2, 59, t, 6.4, 800, "#FFFFFF", "middle", valign="mid")
        f.para(x, 70, bw, d, 6.3, 600, INK, lh=1.2)
        if i < 2:
            f.arrow(x + bw + 6, 28, x + bw + 28, 28, "#37474F", 2.0, 8)
    f.curve_arrow(W - 40, 106, W / 2, 124, 40, 106, "#37474F", 1.4, 6) if False else None
    f.text(W / 2, 100, "↻ ciclo se repete: evita o esgotamento de nutrientes específicos e reduz o uso de adubo nitrogenado", 6.3, 800, "#5D3A1A", "middle")
    save_svg("rotacao_culturas", f.render())


def especulacao():
    f = Fig(FULL, 180, "especulacao_fundiaria", "Esquema de concentração e especulação fundiária")
    W = FULL
    fw = (W - 3 * 12) / 4
    frames = [("1. COMPRA BARATA", "Terra isolada e barata é comprada e mantida ociosa (reserva de valor)."),
              ("2. O ESTADO INVESTE", "Estrada, energia, escola e saneamento pagos com dinheiro público chegam à região."),
              ("3. A TERRA VALORIZA", "Sem investir, o dono vê o preço da terra subir por causa da infraestrutura alheia."),
              ("4. VENDA OU LOTEAMENTO", "Venda por preço muito maior; pequenos agricultores ficam sem acesso à terra.")]
    for i, (t, d) in enumerate(frames):
        x0 = i * (fw + 12)
        f.rect(x0, 0, fw, 16, fill="#5D3A1A", rx=3)
        f.text(x0 + fw / 2, 8, t, 6.2, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 18, fw, 84, fill=SKY)
        f.rect(x0, 78, fw, 24, fill="#C9A77C")
        if i == 0:
            f.rect(x0 + 14, 62, fw - 28, 16, fill="#BCAAA4", stroke="#6D4C41", sw=0.8)
            f.text(x0 + fw / 2, 70, "terra ociosa (cerca)", 5.8, 800, "#4E342E", "middle", valign="mid")
            f.text(x0 + fw / 2, 32, "R$", 8, 800, "#2E7D32", "middle")
            f.text(x0 + fw / 2, 46, "preço baixo", 6.0, 800, "#2E7D32", "middle")
        elif i == 1:
            f.line(x0 + 4, 90, x0 + fw - 4, 88, "#37474F", 5.0)
            f.line(x0 + 4, 90, x0 + fw - 4, 88, "#FFFFFF", 1.0, dash="4 3")
            f.rect(x0 + 18, 62, fw - 36, 12, fill="#BCAAA4", stroke="#6D4C41", sw=0.8)
            f.path(f"M{x0+10},40 L{x0+fw-10},40", stroke="#78909C", sw=1.4)
            for xx in (x0 + 28, x0 + 56, x0 + 84):
                f.line(xx, 40, xx, 56, "#78909C", 1.4)
            f.text(x0 + fw / 2, 26, "Estado: estrada, luz, escola", 5.8, 800, "#0D47A1", "middle")
        elif i == 2:
            f.rect(x0 + 18, 62, fw - 36, 12, fill="#BCAAA4", stroke="#6D4C41", sw=0.8)
            f.line(x0 + 4, 90, x0 + fw - 4, 88, "#37474F", 4.0)
            f.arrow(x0 + fw / 2, 56, x0 + fw / 2, 26, "#E65100", 3.0, 9)
            f.text(x0 + fw / 2 + 24, 38, "preço ↑↑", 6.4, 800, "#E65100", "start")
        else:
            for k in range(6):
                f.rect(x0 + 6 + k * (fw - 12) / 6, 56, (fw - 12) / 6 - 3, 22, fill="#F5E6C8", stroke="#8C6039", sw=0.7)
            f.line(x0 + 4, 90, x0 + fw - 4, 88, "#37474F", 4.0)
            f.text(x0 + fw / 2, 32, "R$$$ para o proprietário", 6.2, 800, "#B71C1C", "middle")
        f.para(x0 + 2, 108, fw - 4, d, 6.3, 600, INK, lh=1.2)
        if i < 3:
            f.arrow(x0 + fw + 1, 56, x0 + fw + 11, 56, "#37474F", 1.8, 6)
    f.text(0, 168, "Grilagem: apropriação de terras públicas com documentos falsificados. Função social da propriedade (CF/1988, art. 186): uso adequado, respeito ao ambiente e às leis trabalhistas.", 6.0, 700, "#5D3A1A")
    save_svg("especulacao_fundiaria", f.render())


def agro_precisao():
    f = Fig(FULL, 184, "agro_precisao", "Agricultura de precisão e sensoriamento remoto")
    W = FULL
    f.rect(0, 0, W, 184, fill="#FFFFFF")
    # satélite e drone
    f.rect(0, 0, W, 76, fill="#0E1730", rx=6)
    f.circle(60, 30, 2, fill="#FFFFFF"); f.circle(180, 20, 1.5, fill="#FFFFFF"); f.circle(300, 38, 1.8, fill="#FFFFFF")
    f.rect(70, 22, 20, 12, fill="#90A4AE", stroke="#CFD8DC", sw=1.0)
    f.rect(52, 24, 14, 8, fill="#1565C0"); f.rect(94, 24, 14, 8, fill="#1565C0")
    f.text(80, 40, "satélite", 6.0, 800, "#FFFFFF", "middle")
    for dx in (-14, 0, 14):
        f.line(80, 34, 80 + dx * 3, 70, "#FFEB3B", 0.8, dash="2 3", opacity=0.8)
    f.rect(260, 40, 20, 6, fill="#CFD8DC"); f.line(250, 38, 290, 38, "#CFD8DC", 1.2); f.circle(250, 38, 4, fill="none", stroke="#CFD8DC", sw=1.0); f.circle(290, 38, 4, fill="none", stroke="#CFD8DC", sw=1.0)
    f.text(270, 56, "drone", 6.0, 800, "#FFFFFF", "middle")
    f.text(W - 8, 8, "GPS · satélites · sensores · drones · máquinas com taxa variável", 6.6, 800, "#FFFFFF", "end")
    # mapa de produtividade
    gx, gy, cs = 380, 90, 30
    cols = ["#C62828", "#EF6C00", "#FDD835", "#9CCC65", "#2E7D32"]
    rnd = random.Random(11)
    for i in range(7):
        for j in range(3):
            v = min(4, max(0, int(2 + 1.8 * math.sin(i * 0.9) + 0.9 * math.cos(j * 2.0) + rnd.uniform(-0.6, 0.6))))
            f.rect(gx + i * cs, gy + j * cs, cs - 1.5, cs - 1.5, fill=cols[v])
    f.text(gx, gy - 12, "Mapa de produtividade (exemplo ilustrativo)", 6.4, 800, INK)
    for k, c in enumerate(cols):
        f.rect(gx + 7 * cs + 10, gy + k * 18, 12, 10, fill=c)
        f.text(gx + 7 * cs + 26, gy + k * 18 + 1, ["muito baixa", "baixa", "média", "alta", "muito alta"][k], 5.8, 600, MUTED)
    # lista
    items = ["**Sensoriamento remoto:** imagens de satélite e drone (índices de vegetação, ex.: NDVI) mostram falhas e estresse hídrico.",
             "**GPS e piloto automático:** máquinas seguem trajetos exatos, sem sobreposição.",
             "**Taxa variável:** aplica adubo, calcário e defensivos **só onde é preciso** → menos insumo, menos contaminação.",
             "**Limites:** custo elevado e dependência de conectividade; tende a **concentrar** tecnologia em grandes propriedades."]
    y = 84
    for t in items:
        h = f.para(0, y, 360, t, 6.5, 500, INK, lh=1.22)
        y += h + 4
    save_svg("agro_precisao", f.render())



def mapa_mental():
    f = Fig(FULL, 168, "agro_mapa_mental", "Mapa mental da Geografia Agrária")
    W = FULL
    f.rect(0, 0, W, 168, fill="#FFFFFF")
    f.circle(355, 84, 46, fill="#8D5B2E")
    f.text(355, 84, "GEOGRAFIA\nAGRÁRIA", 8.6, 800, "#FFFFFF", "middle", valign="mid", lh=1.1)
    L = [("Sistemas agrícolas", "familiar × empresarial · intensiva × extensiva · plantation", "terra"),
         ("Revolução Verde", "pacote técnico → produtividade ↑ · concentração ↑ · êxodo rural", "laranja"),
         ("Insumos e química", "NPK, agrotóxicos → eutrofização, resistência, contaminação", "azul")]
    R = [("Solo e manejo", "calagem · rotação · pousio · curvas de nível · terraços", "verde"),
         ("Fronteira agrícola", "Cerrado → MATOPIBA → Amazônia · pecuária e grilagem", "vermelho"),
         ("Terra e poder", "sesmarias → Lei de Terras → especulação → reforma agrária", "roxo")]
    for i, (t, d, c) in enumerate(L):
        y = 6 + i * 54
        f.box(0, y, 270, 46, "", fill=c)
        f.text(8, y + 6, t, 7.2, 800, C[c][2]); f.para(8, y + 19, 254, d, 6.3, 500, INK, lh=1.2)
        f.line(270, y + 23, 322, 84, C[c][0], 1.6)
    for i, (t, d, c) in enumerate(R):
        y = 6 + i * 54
        f.box(440, y, 270, 46, "", fill=c)
        f.text(448, y + 6, t, 7.2, 800, C[c][2]); f.para(448, y + 19, 254, d, 6.3, 500, INK, lh=1.2)
        f.line(440, y + 23, 388, 84, C[c][0], 1.6)
    save_svg("agro_mapa_mental", f.render())


def build():
    barras_censo(); concentracao(); cena_fam_emp(); cena_int_ext(); revolucao_verde(); eutrofizacao(); manejo_solo(); rotacao(); especulacao(); agro_precisao(); mapa_mental()
