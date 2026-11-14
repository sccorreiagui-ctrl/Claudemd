"""Módulo D — Urbanização e demografia: gráficos (dados IBGE) e diagramas."""
import json, math, random
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, wrap
from common import save_svg, PROC

ROXO = "#7B3FA0"
MAN, WOM = "#5C6BC0", "#AB47BC"


def urbanizacao():
    d = json.load(open(PROC / "urbanizacao_ibge.json"))["series"]
    anos = ["1970", "1980", "1991", "2000", "2010", "2022"]
    f = Fig(FULL, 196, "urbanizacao_grafico", "População urbana e rural do Brasil, 1970–2022")
    W = FULL
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.text(0, 0, "População urbana e rural e taxa de urbanização (milhões de pessoas; IBGE, Censos 1970–2022)", 8.0, 800, "#4A148C")
    x0, y0, x1, y1 = 40, 28, 560, 160
    vmax = 210
    for v in (0, 50, 100, 150, 200):
        y = y1 - (y1 - y0) * v / vmax
        f.line(x0, y, x1, y, "#DDE3EA" if v else "#37474F", 0.6 if v else 0.9)
        f.text(x0 - 4, y, str(v), 5.8, 600, MUTED, "end", valign="mid")
    slot = (x1 - x0) / len(anos)
    for i, a in enumerate(anos):
        s = d[a]
        urb = s["urbana"] / 1e6; rur = s["rural"] / 1e6
        bx = x0 + i * slot + (slot - 44) / 2
        hu = (y1 - y0) * urb / vmax; hr = (y1 - y0) * rur / vmax
        f.rect(bx, y1 - hu, 44, hu, fill="#7B3FA0")
        f.rect(bx, y1 - hu - hr, 44, hr, fill="#C9A77C")
        f.text(bx + 22, y1 - hu / 2, f"{urb:.0f}".replace(".", ","), 7.0, 800, "#FFFFFF", "middle", valign="mid")
        f.text(bx + 22, y1 - hu - hr / 2, f"{rur:.0f}", 6.4, 800, "#5D3A1A", "middle", valign="mid")
        f.text(bx + 22, y1 + 4, a, 6.8, 800, INK, "middle")
        f.text(bx + 22, y1 - hu - hr - 12, f"{s['pct_urbana']:.1f}%".replace(".", ","), 7.2, 800, "#4A148C", "middle")
    f.rect(x1 + 24, 36, 10, 8, fill="#7B3FA0"); f.text(x1 + 38, 33, "urbana", 6.4, 700, INK)
    f.rect(x1 + 24, 52, 10, 8, fill="#C9A77C"); f.text(x1 + 38, 49, "rural", 6.4, 700, INK)
    f.text(x1 + 24, 76, "% = taxa de\nurbanização", 6.2, 700, "#4A148C", lh=1.15)
    f.para(x1 + 24, 104, 126, "Em ≈ 50 anos o Brasil passou de país <b>rural</b> para <b>urbano</b>: +125 milhões de pessoas nas cidades.".replace("<b>", "**").replace("</b>", "**"), 6.4, 500, INK, lh=1.22)
    f.text(0, 184, "Nota: 2022 usa a classificação IBGE (87,4%; ≈ 177,5 mi urbanos e ≈ 25,6 mi rurais). O ritmo mais rápido ocorreu entre as décadas de 1950 e 1980.", 5.9, 500, MUTED, italic=True)
    save_svg("urbanizacao_grafico", f.render())


def piramide(name, ano):
    j = json.load(open(PROC / "piramide_etaria_ibge.json"))
    d = j[ano]
    H, M = list(d["homens"]), list(d["mulheres"])
    if ano == "2022":
        H = H[:16] + [sum(H[16:])]; M = M[:16] + [sum(M[16:])]
    tot = sum(H) + sum(M) + (sum(d["idade_ignorada"].values()) if "idade_ignorada" in d else 0)
    labels = [f"{a}–{a+4}" for a in range(0, 80, 5)] + ["80+"]
    f = Fig(HALF, 268, name, f"Pirâmide etária do Brasil, {ano}")
    W = HALF
    f.rect(0, 0, W, 268, fill="#FFFFFF")
    f.text(W / 2, 0, f"BRASIL {ano}", 9.0, 800, "#4A148C", "middle")
    f.text(W / 2, 14, "% da população total, por sexo e faixa de idade", 6.0, 500, MUTED, "middle")
    cx, gap, sc = W / 2, 15, 16.0
    y0, bh = 36, 11.2
    for v in (2, 4, 6):
        for sgn in (-1, 1):
            xx = cx + sgn * (gap + v * sc)
            f.line(xx, y0 - 2, xx, y0 + 17 * bh + 2, "#E3E8EE", 0.6)
            f.text(xx, y0 + 17 * bh + 4, f"{v}%", 5.6, 600, MUTED, "middle")
    for i in range(17):
        yy = y0 + (16 - i) * bh
        h = 100 * H[i] / tot; m = 100 * M[i] / tot
        f.rect(cx - gap - h * sc, yy, h * sc, bh - 1.2, fill=MAN)
        f.rect(cx + gap, yy, m * sc, bh - 1.2, fill=WOM)
        f.text(cx, yy + (bh - 1.2) / 2, labels[i], 5.6, 700, "#37474F", "middle", valign="mid")
    f.text(cx - gap - 6, y0 - 8, "Homens", 6.4, 800, MAN, "end")
    f.text(cx + gap + 6, y0 - 8, "Mulheres", 6.4, 800, WOM, "start")
    t = sum(H) + sum(M)
    jov = sum(H[:3]) + sum(M[:3]); ido = sum(H[13:]) + sum(M[13:]); at = t - jov - ido
    f.text(8, 238, f"0–14 anos: **{100*jov/tot:.1f}%**   ·   15–64: **{100*at/tot:.1f}%**   ·   65+: **{100*ido/tot:.1f}%**".replace(".", ","), 6.3, 500, INK)
    rd = 100 * (jov + ido) / at
    f.text(8, 250, f"Razão de dependência: **{rd:.0f}** pessoas de 0–14 e 65+ para cada 100 de 15–64 anos".replace(".", ","), 6.3, 500, INK)
    save_svg(name, f.render())


def transicao():
    f = Fig(HALF, 250, "transicao_demografica", "Modelo da transição demográfica")
    W = HALF
    f.rect(0, 0, W, 250, fill="#FFFFFF")
    f.text(W / 2, 0, "Transição demográfica (modelo esquemático)", 7.6, 800, "#4A148C", "middle")
    x0, x1, y0, y1 = 24, W - 8, 30, 138
    ph = [(x0, x0 + 60, "1", "#ECEFF1"), (x0 + 60, x0 + 130, "2", "#E3F2FD"), (x0 + 130, x0 + 214, "3", "#F3E8F9"), (x0 + 214, x1, "4", "#E8F5E9")]
    for a, b, n, c in ph:
        f.rect(a, y0 - 4, b - a, y1 - y0 + 4, fill=c)
        f.text((a + b) / 2, y0 - 2, f"FASE {n}", 5.8, 800, "#37474F", "middle")
    f.line(x0, y1, x1, y1, "#37474F", 1.0); f.line(x0, y0 - 4, x0, y1, "#37474F", 1.0)
    f.text(x0 + 2, y1 + 3, "tempo / desenvolvimento →", 5.6, 700, MUTED)
    def curve(pts, col, sw=2.2):
        f.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), stroke=col, sw=sw)
    nat = [(x0, y0 + 10), (x0 + 60, y0 + 10), (x0 + 96, y0 + 14), (x0 + 130, y0 + 28), (x0 + 175, y0 + 62), (x0 + 214, y0 + 80), (x1, y0 + 84)]
    mor = [(x0, y0 + 12), (x0 + 36, y0 + 14), (x0 + 60, y0 + 28), (x0 + 96, y0 + 66), (x0 + 130, y0 + 80), (x0 + 214, y0 + 80), (x1, y0 + 80)]
    f.poly(nat + mor[::-1], fill="#AB47BC", opacity=0.20)
    curve(nat, "#C62828"); curve(mor, "#1565C0")
    f.text(x0 + 4, y0 + 22, "natalidade", 5.8, 800, "#C62828"); f.text(x0 + 76, y0 + 74, "mortalidade", 5.8, 800, "#1565C0")
    bx = x0 + 208
    f.circle(bx, y0 + 80, 3.6, fill="#2E7D32", stroke="#FFFFFF", sw=1.0)
    f.text(bx - 6, y0 + 36, "Brasil hoje\n(fase 3→4)", 5.8, 800, "#1B5E20", "end", lh=1.1)
    f.line(bx - 4, y0 + 50, bx, y0 + 76, "#1B5E20", 0.8)
    ft = ["alta natalidade e alta mortalidade", "mortalidade cai primeiro: “explosão”", "natalidade cai: crescimento desacelera", "taxas baixas; envelhecimento"]
    for (a, b, n, c), t in zip(ph, ft):
        f.rect(a, y1 + 14, b - a - 2, 48, fill=c, rx=3)
        f.para(a + 3, y1 + 17, b - a - 8, t, 5.6, 700, "#263238", "start", lh=1.12)
    f.rect(8, 210, 10, 7, fill="#AB47BC", opacity=0.35); f.text(22, 208, "crescimento natural = natalidade − mortalidade", 5.8, 600, INK)
    f.para(8, 222, W - 16, "No Brasil: urbanização, mulher no mercado de trabalho, contraceptivos, custo de vida e queda da mortalidade infantil. TFT ≈ 6 filhos por mulher (1960) → 1,55 (2022).", 6.0, 600, INK, lh=1.2)
    save_svg("transicao_demografica", f.render())


def populoso_povoado():
    f = Fig(HALF, 150, "populoso_povoado", "Populoso e povoado")
    W = HALF
    f.rect(0, 0, W, 150, fill="#FFFFFF")
    f.text(W / 2, 0, "POPULOSO × POVOADO", 8.0, 800, "#4A148C", "middle")
    rnd = random.Random(8)
    def box(x, y, w, h, n, label, sub, col_):
        f.rect(x, y, w, h, fill="#FAF6FC", stroke=col_, sw=1.4, rx=4)
        for _ in range(n):
            f.circle(x + 6 + rnd.random() * (w - 12), y + 6 + rnd.random() * (h - 12), 2.0, fill=col_)
        f.text(x + w / 2, y + h + 5, label, 7.0, 800, col_, "middle")
        f.text(x + w / 2, y + h + 16, sub, 6.0, 500, INK, "middle", lh=1.15)
    box(8, 22, 150, 70, 26, "POPULOSO", "muita gente (população absoluta)\nex.: Brasil: ≈ 203 milhões", "#4A148C")
    box(190, 22, 150, 70, 26, "POPULOSO", "e também…", "#4A148C") if False else None
    box(190, 26, 66, 40, 26, "POVOADO", "muita gente por km²\n(densidade alta)", "#C2185B")
    f.para(8, 124, W - 16, "Densidade demográfica = população ÷ área (hab/km²). Brasil: ≈ 23,9 hab/km² (Censo 2022): **populoso**, mas **pouco povoado**.", 6.2, 600, INK, "middle", lh=1.2)
    save_svg("populoso_povoado", f.render())


def metropolizacao():
    f = Fig(FULL, 220, "metropolizacao", "Conurbação, metropolização, macrocefalia e migração pendular")
    W = FULL
    pw = (W - 24) / 3
    heads = [("CONURBAÇÃO", "cidades vizinhas se fundem fisicamente"), ("METRÓPOLE E MIGRAÇÃO PENDULAR", "polo + cidades-dormitório; vai e vem diário"), ("MACROCEFALIA URBANA", "uma cidade muito maior que as demais")]
    for i, (t, s) in enumerate(heads):
        x0 = i * (pw + 12)
        f.rect(x0, 0, pw, 20, fill=ROXO, rx=4)
        f.text(x0 + pw / 2, 10, t, 6.4, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 22, pw, 124, fill="#F7F0FB", stroke="#D8BFE8", sw=0.8)
        f.text(x0 + pw / 2, 28, s, 5.9, 600, "#4A148C", "middle")
    # 1 conurbação
    for (cx, cy, r) in [(60, 90, 28), (116, 96, 24), (170, 88, 30)]:
        f.circle(cx, cy, r, fill="#B39DDB", opacity=0.55, stroke="#7B3FA0", sw=0.8)
    for (cx, cy, r) in [(60, 90, 12), (116, 96, 10), (170, 88, 13)]:
        f.circle(cx, cy, r, fill="#7B3FA0")
    f.para(6, 120, pw - 12, "áreas urbanas contíguas (ex.: Santos–São Vicente–Guarujá, SP; Belo Horizonte–Contagem, MG)", 5.8, 600, INK, "middle", lh=1.12)
    # 2 metrópole + pendular
    x0 = pw + 12
    cx, cy = x0 + pw / 2, 86
    f.circle(cx, cy, 20, fill="#7B3FA0")
    f.text(cx, cy, "polo", 6.4, 800, "#FFFFFF", "middle", valign="mid")
    for ang in (20, 80, 150, 210, 270, 330):
        a = math.radians(ang); px, py = cx + 62 * math.cos(a), cy + 34 * math.sin(a)
        f.circle(px, py, 8, fill="#B39DDB", stroke="#7B3FA0", sw=0.8)
        f.arrow(px - 3 * math.cos(a), py - 3 * math.sin(a), cx + 22 * math.cos(a), cy + 22 * math.sin(a), "#E65100", 1.2, 5)
    f.para(x0 + 6, 120, pw - 12, "cidades-dormitório → trabalho e estudo no polo; a residência não muda (região metropolitana)", 5.8, 600, INK, "middle", lh=1.12)
    # 3 macrocefalia (barras)
    x0 = 2 * (pw + 12)
    vals = [("A", 100), ("B", 22), ("C", 14), ("D", 9), ("E", 6)]
    for k, (lab, v) in enumerate(vals):
        bx = x0 + 18 + k * 36
        f.rect(bx, 134 - v * 0.9, 22, v * 0.9, fill="#7B3FA0" if k == 0 else "#B39DDB")
        f.text(bx + 11, 138, lab, 5.8, 700, INK, "middle")
    f.text(x0 + pw / 2, 148, "", 5, 400)
    f.text(x0 + 70, 62, "metrópole\n(exemplo didático)", 5.8, 800, "#4A148C", "start", lh=1.1)
    # explicações
    exp = ["**Conurbação:** união física de malhas urbanas de municípios vizinhos; pode ou não formar metrópole.",
           "**Metropolização:** concentração de pessoas, serviços e gestão em um polo e sua região; gera fluxos **pendulares** diários.",
           "**Macrocefalia urbana:** desequilíbrio da rede urbana (uma cidade concentra população e funções), típica de urbanização rápida e desigual."]
    for i, t in enumerate(exp):
        f.para(i * (pw + 12) + 2, 154, pw - 4, t, 6.3, 500, INK, lh=1.2)
    save_svg("metropolizacao", f.render())


def impermeabilizacao():
    f = Fig(FULL, 212, "impermeabilizacao", "Impermeabilização do solo e enchentes")
    W = FULL
    f.rect(0, 0, W, 212, fill="#FFFFFF")
    # painéis esquema
    hw = (W - 12) / 2
    for i, (t, c) in enumerate([("ÁREA COM VEGETAÇÃO", "#2E7D32"), ("ÁREA IMPERMEABILIZADA", "#455A64")]):
        x0 = i * (hw + 12)
        f.rect(x0, 0, hw, 18, fill=c, rx=4)
        f.text(x0 + hw / 2, 9, t, 6.8, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 20, hw, 74, fill="#EAF4FC")
    # verde: árvores, solo permeável; setas de infiltração
    f.rect(0, 70, hw, 24, fill="#8D6E63")
    for x in (30, 90, 150, 220, 290):
        f.tree(x, 70, 0.9)
    f.raindrops(24, 26, 9, "#1E88E5", 34, 8)
    for x in (60, 140, 220, 300):
        f.arrow(x, 74, x, 92, "#1565C0", 1.6, 5)
    # asfalto
    x1 = hw + 12
    f.rect(x1, 70, hw, 24, fill="#8D6E63")
    f.rect(x1, 66, hw, 6, fill="#37474F")
    for x in (24, 92, 160, 236):
        f.rect(x1 + x, 38, 40, 28, fill="#B0BEC5", stroke="#78909C", sw=0.8)
        for k in range(3):
            f.rect(x1 + x + 6 + k * 11, 44, 6, 6, fill="#ECEFF1")
    f.raindrops(x1 + 24, 26, 9, "#1E88E5", 34, 8)
    f.arrow(x1 + 250, 82, x1 + 330, 82, "#1565C0", 2.2, 7)
    f.text(x1 + 290, 74, "escoamento", 5.8, 800, "#0D47A1", "middle")
    # barras comparativas
    f.text(0, 104, "Destino da água da chuva (valores de referência didática; FISRWG, 1998; % do total)", 6.6, 800, "#37474F")
    rows = [("Cobertura natural", [("escoamento", 10, "#1565C0"), ("infiltração", 50, "#2E7D32"), ("evapotranspiração", 40, "#81C784")]),
            ("75–100% impermeabilizado", [("escoamento", 55, "#1565C0"), ("infiltração", 15, "#2E7D32"), ("evapotranspiração", 30, "#81C784")])]
    for k, (nm, c) in enumerate([("escoamento superficial", "#1565C0"), ("infiltração", "#2E7D32"), ("evapotranspiração", "#81C784")]):
        f.rect(150 + k * 150, 120, 10, 8, fill=c); f.text(164 + k * 150, 118, nm, 6.0, 700, INK)
    y = 136
    for lab, parts in rows:
        f.text(0, y + 3, lab, 6.6, 800, INK)
        xx = 150
        for nm, v, c in parts:
            w = 520 * v / 100
            f.rect(xx, y, w, 20, fill=c)
            f.text(xx + w / 2, y + 10, f"{v}%", 7.0, 800, "#FFFFFF", "middle", valign="mid")
            xx += w
        y += 28
    f.text(0, 190, "Consequência: muita água escoa de uma vez por ruas e bueiros → galerias sobrecarregadas, rios retificados e assoreados → enchentes, alagamentos e inundações.", 6.2, 700, "#5D3A1A")
    f.text(0, 200, "Soluções: pavimento permeável, parques lineares, jardins de chuva, telhados verdes, reservatórios (“piscinões”) e preservação de várzeas.", 6.2, 600, INK)
    save_svg("impermeabilizacao", f.render())


def inversao_termica():
    f = Fig(FULL, 184, "inversao_termica", "Inversão térmica")
    W = FULL
    hw = (W - 12) / 2
    for i, (t, c) in enumerate([("CONDIÇÃO NORMAL: o ar quente sobe e dispersa a poluição", "#1565C0"), ("INVERSÃO TÉRMICA: camada de ar quente “tampa” o ar frio", "#C62828")]):
        x0 = i * (hw + 12)
        f.rect(x0, 0, hw, 20, fill=c, rx=4)
        f.text(x0 + hw / 2, 10, t, 6.2, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 22, hw, 108, fill="#EAF4FC" if i == 0 else "#FDEDEC")
        # cidade
        for k, (bx, bh) in enumerate([(30, 30), (52, 44), (76, 24), (96, 36), (122, 48), (150, 28), (174, 38), (200, 26)]):
            f.rect(x0 + bx, 126 - bh, 16, bh, fill="#78909C", stroke="#546E7A", sw=0.6)
        f.rect(x0, 126, hw, 6, fill="#546E7A")
    # normal: setas subindo, poluentes dispersos
    for x in (50, 92, 140, 190):
        f.arrow(x, 100, x, 38, "#E53935", 1.8, 6)
    for (x, y) in [(60, 50), (110, 40), (150, 48), (190, 36), (230, 56)]:
        f.circle(x, y, 2.4, fill="#6D4C41", opacity=0.55)
    f.text(10, 28, "ar frio ↑ altitude", 5.8, 700, "#0D47A1", italic=True)
    # inversão: camada quente, poluentes presos
    x1 = hw + 12
    f.rect(x1, 46, hw, 14, fill="#EF9A9A", opacity=0.85)
    f.text(x1 + hw / 2, 53, "camada de ar QUENTE (menos denso)", 6.0, 800, "#B71C1C", "middle", valign="mid")
    f.rect(x1, 60, hw, 70, fill="#E1F5FE", opacity=0.55)
    for (x, y) in [(40, 78), (60, 90), (88, 72), (110, 96), (140, 84), (170, 76), (196, 94), (228, 88), (250, 100), (120, 106), (70, 108)]:
        f.circle(x1 + x, y, 2.6, fill="#3E2723", opacity=0.75)
    f.text(x1 + hw / 2, 66, "ar FRIO e denso preso junto ao solo: poluentes acumulam", 6.0, 800, "#3E2723", "middle")
    f.path(f"M{x1+10},100 q10,-8 20,0", stroke="#546E7A", sw=1.0)
    # perfis de temperatura
    f.text(0, 136, "Temperatura × altitude", 6.3, 800, "#37474F")
    def perfil(x0, normal):
        f.line(x0 + 4, 146, x0 + 4, 172, "#37474F", 0.8); f.line(x0 + 4, 172, x0 + 100, 172, "#37474F", 0.8)
        if normal:
            f.path(f"M{x0+90},170 L{x0+30},148", stroke="#C62828", sw=1.8)
        else:
            f.path(f"M{x0+30},170 L{x0+60},158 L{x0+88},150", stroke="#C62828", sw=1.8)
    perfil(0, True); perfil(hw + 12, False)
    f.text(112, 156, "normal: esfria com a altitude", 6.0, 700, INK)
    f.text(hw + 12 + 112, 156, "inversão: o ar fica mais quente em cima", 6.0, 700, INK)
    f.para(hw + 12 + 112, 166, hw - 118, "mais frequente no inverno, em noites frias e secas; agrava doenças respiratórias", 5.6, 600, MUTED, lh=1.15)
    save_svg("inversao_termica", f.render())


def ilha_calor():
    f = Fig(FULL, 190, "ilha_calor", "Perfil da ilha de calor urbana")
    W = FULL
    f.rect(0, 0, W, 190, fill="#FFFFFF")
    f.text(0, 0, "Ilha de calor: temperatura do ar ao longo de uma linha rural → centro urbano → rural (perfil ilustrativo)", 7.4, 800, "#B71C1C")
    x0, x1, y0, y1 = 36, W - 8, 40, 108
    f.line(x0, y1, x1, y1, "#37474F", 0.9)
    # curva
    import math as m
    pts = []
    for i in range(0, 61):
        x = x0 + (x1 - x0) * i / 60
        t = i / 60
        base = 0.15 + 0.85 * (0.5 * (1 + m.tanh((t - 0.18) * 9)) * 0.5 * (1 + m.tanh((0.82 - t) * 9)))
        dip = -0.28 * m.exp(-((t - 0.60) / 0.045) ** 2)       # parque
        peak = 0.12 * m.exp(-((t - 0.38) / 0.1) ** 2)
        v = base + dip + peak
        pts.append((x, y1 - 8 - (y1 - y0 - 12) * v))
    f.poly(pts + [(x1, y1), (x0, y1)], fill="#FFCDD2", opacity=0.6)
    f.poly(pts, stroke="#C62828", sw=2.2, close=False)
    # cenário
    sky = 100
    labs = [(0.07, "rural"), (0.24, "subúrbio"), (0.40, "centro\nverticalizado"), (0.60, "parque"), (0.76, "subúrbio"), (0.92, "rural")]
    f.rect(x0, y1, x1 - x0, 46, fill="#ECEFF1")
    for t, lab in labs:
        x = x0 + (x1 - x0) * t
        f.text(x, y1 + 52, lab, 5.9, 700, INK, "middle", lh=1.05)
    for (t, bh, w_, c_) in [(0.30, 28, 12, "#78909C"), (0.34, 40, 14, "#607D8B"), (0.38, 48, 14, "#546E7A"), (0.42, 36, 14, "#78909C"), (0.46, 24, 12, "#90A4AE"), (0.22, 12, 10, "#90A4AE"), (0.26, 16, 10, "#90A4AE"), (0.74, 10, 10, "#90A4AE"), (0.78, 14, 10, "#90A4AE")]:
        x = x0 + (x1 - x0) * t
        f.rect(x, y1 + 46 - bh, w_, bh, fill=c_) if False else f.rect(x, y1 + 48 - bh - 2, w_, bh, fill=c_)
    x = x0 + (x1 - x0) * 0.60
    f.circle(x, y1 + 30, 12, fill="#66BB6A"); f.circle(x + 12, y1 + 34, 9, fill="#43A047"); f.circle(x - 12, y1 + 34, 9, fill="#43A047")
    for t in (0.04, 0.08, 0.12, 0.90, 0.94):
        xx = x0 + (x1 - x0) * t
        f.tree(xx, y1 + 46, 0.7)
    f.text(x0 + (x1 - x0) * 0.38, y0 - 8, "pico: maior temperatura no centro verticalizado", 6.0, 800, "#B71C1C", "middle")
    f.text(x0 + (x1 - x0) * 0.60 + 8, y1 - 40, "parque: ilha de frescor", 5.8, 800, "#2E7D32", "start")
    f.text(0, 176, "Causas: asfalto e concreto absorvem calor (baixo albedo), pouca vegetação, calor liberado por veículos/ar-condicionado e paredões de edifícios que dificultam a ventilação.", 6.0, 600, INK)
    save_svg("ilha_calor", f.render())


def segregacao():
    f = Fig(FULL, 178, "segregacao", "Segregação socioespacial e áreas de risco")
    W = FULL
    f.rect(0, 0, W, 178, fill="#FFFFFF")
    f.rect(0, 0, W, 104, fill="#EAF4FC")
    # relevo: várzea à esquerda (rio), centro plano, encosta à direita
    f.poly([(0, 104), (0, 78), (150, 78), (250, 76), (360, 70), (460, 52), (560, 30), (W, 22), (W, 104)], fill="#C9A77C", stroke="#8C6039", sw=0.9)
    f.rect(0, 78, 120, 26, fill="#7CB342")
    f.path("M0,92 q40,-6 120,2", stroke="#1E88E5", sw=4)
    # bairros
    for k in range(6):
        x = 154 + k * 20
        f.rect(x, 78 - 20 - (k % 3) * 12, 14, 20 + (k % 3) * 12, fill="#78909C", stroke="#546E7A", sw=0.6)
    for k in range(5):
        f.rect(8 + k * 22, 78 - 10, 18, 10, fill="#D7A86E", stroke="#8C5E2B", sw=0.7)       # palafitas/várzea
    for k in range(10):
        x = 400 + k * 22
        f.rect(x, 70 - k * 4.4 - 10, 15, 12, fill="#D7A86E", stroke="#8C5E2B", sw=0.7)         # favela na encosta
    for k in range(4):
        x = 300 + k * 18
        f.rect(x, 70 - 12, 14, 12, fill="#F5E6C8", stroke="#8C6039", sw=0.7)
        f.poly([(x - 1, 58), (x + 7, 52), (x + 15, 58)], fill="#B2493A")
    f.rect(280, 56, 80, 3, fill="#388E3C")
    # setas e rótulos
    f.text(60, 24, "VÁRZEA\n(inunda)", 6.4, 800, "#B71C1C", "middle", lh=1.1)
    f.text(206, 24, "CENTRO\nvalorizado", 6.4, 800, "#4A148C", "middle", lh=1.1)
    f.text(330, 24, "condomínios\nfechados", 6.2, 800, "#4A148C", "middle", lh=1.1)
    f.text(500, 14, "ENCOSTA\n(deslizamentos)", 6.4, 800, "#B71C1C", "middle", lh=1.1)
    f.rect(0, 112, W, 66, fill="#F7F0FB", rx=4)
    t = [("**Mecanismo:** o preço do solo urbano seleciona quem vive onde; sem moradia acessível, a população pobre ocupa várzeas e encostas (autoconstrução, favelas).",),
         ("**Consequências:** deslizamentos e enchentes, falta de saneamento e transporte, **segregação** (condomínios × favelas) e violência urbana.",),
         ("**Resposta:** habitação de interesse social, regularização fundiária, plano diretor, parques e contenção de encostas (ver Estatuto da Cidade, 2001).",)]
    for i, (s_,) in enumerate(t):
        f.para(8 + i * 236, 118, 226, s_, 6.2, 500, INK, lh=1.22)
    save_svg("segregacao", f.render())


def rede_urbana():
    f = Fig(HALF, 276, "rede_urbana", "Hierarquia e rede urbana (REGIC 2018)")
    W = HALF
    f.rect(0, 0, W, 276, fill="#FFFFFF")
    f.text(W / 2, 0, "Rede urbana brasileira (IBGE, REGIC 2018)", 7.4, 800, "#4A148C", "middle")
    levels = [("Metrópoles (15)", "SP · RJ e Brasília · BH, Curitiba, Porto Alegre…", "#4A148C", 11, [174]),
              ("Capitais regionais", "ex.: Campinas, Ribeirão Preto, Londrina", "#7B3FA0", 8.5, [96, 174, 252]),
              ("Centros sub-regionais", "cidades médias", "#9C5CC4", 7, [44, 96, 148, 200, 252, 304]),
              ("Centros de zona", "cidades pequenas que polarizam vizinhas", "#B987D6", 5.6, [26, 62, 98, 134, 170, 206, 242, 278, 314]),
              ("Centros locais", "municípios sem polarização relevante", "#D3B3E6", 4.4, [14, 38, 62, 86, 110, 134, 158, 182, 206, 230, 254, 278, 302, 326])]
    y = 20
    ycs = []
    for t, sub, c, r, xs in levels:
        f.text(8, y, t, 6.8, 800, c); f.text(8 + 4 + 100 if False else 150, y + 1, sub, 5.6, 500, MUTED) if False else f.text(8, y + 10, sub, 5.6, 500, MUTED)
        ycs.append(y + 30)
        y += 46
    for i in range(4):
        for a in levels[i][4]:
            for b in levels[i + 1][4]:
                if abs(a - b) < 70 + i * 6:
                    f.line(a, ycs[i] + levels[i][3], b, ycs[i + 1] - levels[i + 1][3], "#B39DDB", 0.7, opacity=0.75)
    for (t, sub, c, r, xs), yc in zip(levels, ycs):
        for x in xs:
            f.circle(x, yc, r, fill=c, stroke="#FFFFFF", sw=0.8)
    f.para(8, 258 - 6, W - 16, "", 5.9, 600, INK)
    f.para(8, y - 4, W - 16, "Gestão, saúde, ensino, comércio e serviços ligam o local ao regional e ao nacional: quanto mais alto o nível, maior a área de influência.", 5.9, 600, INK, lh=1.2)
    save_svg("rede_urbana", f.render())


def build():
    urbanizacao()
    piramide("piramide_1980", "1980")
    piramide("piramide_2022", "2022")
    transicao(); populoso_povoado(); metropolizacao(); impermeabilizacao(); inversao_termica(); ilha_calor(); segregacao(); rede_urbana()
