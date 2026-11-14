"""Módulo A — diagramas: solos, intemperismo/erosão, estrutura geológica, tipos de chuva."""
import math, random
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, wrap, text_width
from common import save_svg

SEA = "#A9D3F0"
SKY = "#EAF4FC"
MANTLE = "#F6D3AE"


def rock_frags(f, x, y, w, h, n=12, seed=1, colors=("#8E969D", "#A7AEB4", "#757E86"), smin=3, smax=7):
    rnd = random.Random(seed)
    for _ in range(n):
        cx, cy = x + rnd.random() * w, y + rnd.random() * h
        s = rnd.uniform(smin, smax)
        pts = [(cx + math.cos(a) * s * rnd.uniform(0.7, 1.2), cy + math.sin(a) * s * rnd.uniform(0.6, 1.0)) for a in [i * 2 * math.pi / 6 + rnd.random() * 0.5 for i in range(6)]]
        f.poly(pts, fill=rnd.choice(colors), stroke="#5F676E", sw=0.5)


def soil_column(f, x, y, w, hs, colors, seed=3, leaves=True, roots=True):
    """Desenha colunas de horizontes. hs: lista [(sigla, altura)], colors: dict sigla->cor."""
    yy = y
    pos = {}
    for sig, h in hs:
        f.rect(x, yy, w, h, fill=colors[sig])
        pos[sig] = (yy, yy + h)
        yy += h
    rnd = random.Random(seed)
    if "O" in pos:
        y0, y1 = pos["O"]
        for _ in range(int(w / 5)):
            f.ellipse(x + rnd.random() * w, y0 + rnd.random() * (y1 - y0), 2.6, 1.2, fill=rnd.choice(["#7A5230", "#9A6A3A", "#5B3A20"]), rot=rnd.randint(0, 150))
    if "A" in pos:
        y0, y1 = pos["A"]
        for _ in range(int(w / 3)):
            f.circle(x + rnd.random() * w, y0 + rnd.random() * (y1 - y0), 0.9, fill="#2E1B0F", opacity=0.55)
    if "B" in pos:
        y0, y1 = pos["B"]
        for _ in range(int(w / 3.2)):
            f.circle(x + rnd.random() * w, y0 + rnd.random() * (y1 - y0), 1.1, fill="#8A3F1E", opacity=0.5)
    if "C" in pos:
        y0, y1 = pos["C"]
        rock_frags(f, x + 3, y0 + 3, w - 6, (y1 - y0) - 6, n=int(w / 9), seed=seed, smin=3, smax=6)
    if "R" in pos:
        y0, y1 = pos["R"]
        f.path(f"M{x},{y0+8} L{x+w*0.25},{y0+14} L{x+w*0.5},{y0+7} L{x+w*0.8},{y0+15} L{x+w},{y0+9}", stroke="#5F676E", sw=0.8)
        f.path(f"M{x+w*0.3},{y0+14} L{x+w*0.28},{y1-6}", stroke="#5F676E", sw=0.7)
        f.path(f"M{x+w*0.7},{y0+15} L{x+w*0.74},{y1-6}", stroke="#5F676E", sw=0.7)
    return pos


# ------------------------------------------------------------------------------
def perfil_solo():
    f = Fig(HALF, 300, "perfil_solo", "Perfil de solo com horizontes")
    W = HALF
    colors = {"O": "#3B2716", "A": "#6A4A2E", "B": "#B46A3C", "C": "#D8BC92", "R": "#8D9399"}
    x, w, y0 = 14, 128, 36
    hs = [("O", 14), ("A", 40), ("B", 70), ("C", 54), ("R", 62)]
    f.rect(x - 6, 8, w + 12, y0 - 8, fill=SKY)
    for xx in range(x + 4, x + w, 11):
        f.path(f"M{xx},{y0} q-2,-8 -4,-12 M{xx},{y0} q1,-9 3,-13", stroke="#43A047", sw=1.3)
    f.tree(x + 98, y0 + 1, 1.1)
    pos = soil_column(f, x, y0, w, hs, colors)
    for dx, dd in [(92, 46), (100, 62), (106, 42)]:
        f.path(f"M{x+dx},{y0+10} C {x+dx-4},{y0+dd/2} {x+dx+6},{y0+dd*0.8} {x+dx-2},{y0+dd+14}", stroke="#2E1B0F", sw=1.0, opacity=0.8)
    f.arrow(x + 22, y0 + 6, x + 22, y0 + 120, "#1E88E5", 2.2, 8)
    f.text(x + 30, y0 + 72, "lixiviação:\nágua leva\nnutrientes\npara baixo", 5.9, 800, "#FFFFFF", lh=1.12)
    lx = x + w + 16
    items = [("O", "O · Orgânico", "serapilheira e húmus: folhas e restos em decomposição (decompositores reciclam nutrientes).", "#3B2716"),
             ("A", "A · Horizonte superficial", "matéria orgânica + minerais; mais escuro, mais fértil e o mais exposto à erosão.", "#6A4A2E"),
             ("B", "B · Horizonte de acumulação", "argilas e óxidos de ferro e alumínio (cores vermelha e amarela dos solos tropicais).", "#9A5530"),
             ("C", "C · Rocha alterada", "saprolito: fragmentos da rocha-mãe em intemperismo.", "#8C6F45"),
             ("R", "R · Rocha-mãe", "material de origem, ainda inalterado.", "#5F676E")]
    ys = {"O": 16, "A": 64, "B": 118, "C": 192, "R": 246}
    for sig, t, d, c in items:
        a, b = pos[sig]
        yy = ys[sig]
        f.line(x + w + 3, (a + b) / 2, lx - 4, yy + 7, "#37474F", 0.7)
        f.text(lx, yy, t, 7.2, 800, c)
        f.para(lx, yy + 11.5, W - lx - 4, d, 6.3, 400, INK, lh=1.2)
    f.text(x + w / 2, 8, "superfície", 6.0, 600, MUTED, "middle", italic=True)
    f.text(W / 2, 284, "Pedogênese = clima + organismos + relevo + rocha-mãe + tempo", 6.3, 800, "#5D3A1A", "middle")
    save_svg("perfil_solo", f.render())


# ------------------------------------------------------------------------------
def solos_comparados():
    f = Fig(FULL, 236, "solos_comparados", "Perfis comparados de solos brasileiros")
    W = FULL
    cw = (W - 3 * 10) / 4
    cols = [
        dict(t="Terra roxa / Latossolo vermelho", sub="derivado de basalto (Sul, MS, SP, GO)",
             hs=[("O", 8), ("A", 30), ("B", 92), ("C", 28), ("R", 20)], colors={"O": "#3B2716", "A": "#5A3A25", "B": "#9C3F26", "C": "#C79A72", "R": "#6E767D"},
             txt="Profundo, argiloso e **fértil**; boa retenção de água. Café (séc. XIX) e soja.", prof=5, fert=4),
        dict(t="Massapê", sub="argiloso escuro (Zona da Mata e Recôncavo)",
             hs=[("O", 6), ("A", 44), ("B", 70), ("C", 34), ("R", 24)], colors={"O": "#3B2716", "A": "#2F2018", "B": "#493021", "C": "#B79A72", "R": "#6E767D"},
             txt="Argila escura, profunda e fértil; pesado e pegajoso quando molhado. **Cana-de-açúcar** colonial.", prof=4, fert=4),
        dict(t="Solos da Amazônia", sub="Latossolos e Argissolos (terra firme)",
             hs=[("O", 12), ("A", 14), ("B", 110), ("C", 28), ("R", 14)], colors={"O": "#3B2716", "A": "#7A5A3A", "B": "#C98A4B", "C": "#E3C79B", "R": "#6E767D"},
             txt="Profundos, **ácidos e pobres** (lixiviação intensa); a floresta se sustenta pela **serapilheira** (ciclagem rápida).", prof=5, fert=1),
        dict(t="Solos do semiárido", sub="Neossolos e Luvissolos (Caatinga)",
             hs=[("O", 3), ("A", 14), ("B", 26), ("C", 30), ("R", 90)], colors={"O": "#3B2716", "A": "#8A6A4A", "B": "#B58B5E", "C": "#CDB38E", "R": "#7E858B"},
             txt="**Rasos e pedregosos**, pouco intemperizados (falta de água); riscos de erosão e **salinização** com irrigação mal manejada.", prof=1, fert=3),
    ]
    for i, c in enumerate(cols):
        x0 = i * (cw + 10)
        f.rect(x0, 0, cw, 232, fill="#FFFFFF", stroke="#D5DBE4", sw=0.8, rx=5)
        f.text(x0 + cw / 2, 5, c["t"], 7.2, 800, "#5D3A1A", "middle")
        f.text(x0 + cw / 2, 17, c["sub"], 5.8, 500, MUTED, "middle")
        f.rect(x0 + 10, 28, cw - 20, 8, fill=SKY)
        for xx in range(int(x0 + 14), int(x0 + cw - 12), 11):
            f.path(f"M{xx},36 q-1,-5 -3,-7 M{xx},36 q1,-6 2,-8", stroke="#43A047" if i != 3 else "#A59A4B", sw=1.1)
        tot = sum(h for _, h in c["hs"])
        c["hs"] = [(sg, h * 100.0 / tot) for sg, h in c["hs"]]
        soil_column(f, x0 + 10, 36, cw - 20, c["hs"], c["colors"], seed=i + 2)
        yy = 36
        for sig, h in c["hs"]:
            if h >= 12:
                f.text(x0 + 15, yy + h / 2, sig, 6.2, 800, "#FFFFFF" if sig in "OAB" else "#2B2B2B", valign="mid")
            yy += h
        f.para(x0 + 8, 36 + 100 + 6, cw - 16, c["txt"], 6.2, 400, INK, lh=1.18)
        # indicadores qualitativos
        yb = 204
        f.text(x0 + 8, yb, "Profundidade", 5.8, 700, MUTED)
        f.text(x0 + cw / 2 + 4, yb, "Fertilidade nat.", 5.8, 700, MUTED)
        for k in range(5):
            f.circle(x0 + 12 + k * 10, yb + 15, 3, fill="#8D5B2E" if k < c["prof"] else "#E4DACB")
            f.circle(x0 + cw / 2 + 8 + k * 10, yb + 15, 3, fill="#2E7D32" if k < c["fert"] else "#DCE8DC")
    save_svg("solos_comparados", f.render())


# ------------------------------------------------------------------------------
def intemperismo_erosao():
    H = 206
    f = Fig(FULL, H, "intemperismo_erosao", "Intemperismo, erosão e sedimentação")
    W = FULL
    f.rect(0, 0, W, H, fill="#FFFFFF")
    f.rect(0, 26, W, 150, fill=SKY)
    terrain = [(0, 100), (40, 96), (120, 98), (190, 108), (250, 130), (330, 152), (420, 166), (520, 172), (W, 176)]
    f.poly(terrain + [(W, H), (0, H)], fill="#C9A77C", stroke="#8C6039", sw=1.0)
    f.poly([(470, 172), (W, 176), (W, H), (470, H)], fill="#E7D0A6")
    for yy, cc in [(186, "#D4B07A"), (196, "#C49A62")]:
        f.path(f"M470,{yy} C 540,{yy+3} 620,{yy-2} {W},{yy+2}", stroke=cc, sw=6, opacity=0.9, cap="butt")
    f.text(590, 150, "camadas (estratos) com fósseis", 5.8, 800, "#5D3A1A", "middle", italic=True, halo="#FFFFFF")
    # rocha com fraturas
    f.poly([(22, 98), (32, 72), (70, 64), (116, 68), (138, 94)], fill="#8E969D", stroke="#5F676E", sw=1.0)
    for a, b, c_, d in [(48, 68, 56, 84), (84, 66, 78, 82), (102, 70, 110, 88), (60, 84, 76, 96)]:
        f.line(a, b, c_, d, "#3E464C", 1.0)
    rock_frags(f, 122, 88, 40, 12, n=5, seed=5, smin=2.5, smax=4.5)
    # tipos de intemperismo (coluna de rótulos)
    f.sun(24, 38, 5)
    f.text(38, 32, "dilatação e contração térmica = FÍSICO", 6.1, 800, "#C62828")
    f.raindrops(18, 49, 3, "#1565C0", 5, 6)
    f.text(38, 45, "água, CO₂ e oxigênio (dissolução, oxidação) = QUÍMICO", 6.1, 800, "#0D47A1")
    f.path("M146,74 q-8,-6 -10,-14 M146,74 q2,-9 8,-14", stroke="#2E7D32", sw=1.4)
    f.text(158, 62, "raízes e liquens\n= BIOLÓGICO", 5.9, 800, "#2E7D32", lh=1.1)
    # erosão
    pts = [(196, 112), (228, 124), (262, 138), (300, 150), (340, 158), (388, 164)]
    for i in range(len(pts) - 1):
        f.arrow(pts[i][0], pts[i][1] - 8, pts[i + 1][0], pts[i + 1][1] - 8, "#1E88E5", 2.2, 7)
    for (xx, yy) in [(212, 112), (248, 128), (286, 144), (330, 152), (372, 158)]:
        f.circle(xx, yy - 3, 2.0, fill="#7A5A3A")
    f.arrow(54, 118, 140, 118, "#78909C", 1.6, 7, dash="4 3")
    f.text(96, 123, "vento", 5.8, 700, "#546E7A", "middle", italic=True)
    f.text(310, 104, "água de chuva e dos rios\n(também vento e gelo)", 5.9, 800, "#0D47A1", "middle", lh=1.1, halo="#EAF4FC")
    f.path("M392,166 C 430,168 450,171 470,172", stroke="#1E88E5", sw=3.5)
    f.arrow(428, 146, 470, 154, "#1E88E5", 2.2, 7)
    f.text(424, 118, "o rio transporta\nsedimentos", 5.9, 800, "#0D47A1", "middle", lh=1.1, halo="#EAF4FC")
    for (xx, yy) in [(500, 180), (540, 183), (580, 181), (620, 184), (660, 183)]:
        f.circle(xx, yy - 3, 2.2, fill="#8D5B2E")
    f.arrow(540, 152, 540, 172, "#8D5B2E", 2.0, 6)
    # faixas
    f.rect(0, 0, 232, 20, fill="#B23C00")
    f.text(116, 10, "INTEMPERISMO · altera a rocha NO LUGAR", 6.5, 800, "#FFFFFF", "middle", valign="mid")
    f.rect(236, 0, 230, 20, fill="#1565C0")
    f.text(351, 10, "EROSÃO · REMOVE e TRANSPORTA", 6.5, 800, "#FFFFFF", "middle", valign="mid")
    f.rect(470, 0, 240, 20, fill="#6D4C41")
    f.text(590, 10, "SEDIMENTAÇÃO · DEPOSITA", 6.5, 800, "#FFFFFF", "middle", valign="mid")
    f.text(8, 188, "Energia do relevo exógeno: Sol + gravidade + água, vento e gelo.", 6.2, 700, "#5D3A1A")
    save_svg("intemperismo_erosao", f.render())


# ------------------------------------------------------------------------------
def estrutura_geologica():
    f = Fig(FULL, 214, "estrutura_geologica", "Escudo cristalino, bacia sedimentar e dobramentos modernos")
    W = FULL
    f.rect(0, 0, W, 214, fill="#FFFFFF")
    f.rect(0, 28, W, 150, fill=SKY)
    f.poly([(0, 92), (60, 70), (150, 66), (210, 92), (232, 150), (0, 150)], fill="#B07A8A", stroke="#7C4A5A", sw=1.0)
    for (a, b) in [(20, 100), (60, 118), (110, 96), (150, 124), (190, 108), (90, 138), (30, 134)]:
        f.path(f"M{a},{b} q10,-6 20,0 q6,6 -4,10", stroke="#6A3B4B", sw=0.9, opacity=0.8)
    f.text(112, 32, "ESCUDO CRISTALINO (Pré-Cambriano)", 7.6, 800, "#6A3B4B", "middle")
    f.text(112, 44, "rochas magmáticas e metamórficas\nrelevo desgastado e antigo", 6.0, 600, "#6A3B4B", "middle", lh=1.15)
    f.text(112, 100, "granito · gnaisse", 6.2, 800, "#FFFFFF", "middle")
    f.text(112, 112, "minerais metálicos: ferro,\nmanganês, ouro, bauxita", 5.9, 700, "#FFFFFF", "middle", lh=1.1)
    f.arrow(196, 72, 244, 98, "#1E88E5", 2.2, 8)
    f.text(204, 46, "erosão e\ntransporte", 5.9, 800, "#0D47A1", "middle", italic=True, lh=1.1)
    f.poly([(236, 108), (310, 126), (410, 134), (500, 126), (560, 108), (560, 178), (236, 178)], fill="#E9D7B0", stroke="#A68A55", sw=1.0)
    for cc, yy in [("#D8C08A", 130), ("#C9AB6F", 146), ("#B8955A", 160)]:
        f.path(f"M242,{yy-14} C 310,{yy-4} 410,{yy+2} 500,{yy-4} S 552,{yy-14} 556,{yy-18}", stroke=cc, sw=10, cap="butt", opacity=0.95)
    f.text(398, 32, "BACIA SEDIMENTAR (Paleozoico–Cenozoico)", 7.6, 800, "#6D4C41", "middle")
    f.text(398, 44, "sedimentos compactados em camadas · relevo mais baixo", 6.0, 600, "#6D4C41", "middle")
    f.path("M342,148 q8,-14 8,-6 q0,8 -8,6 z", fill="#2B2B2B")
    f.path("M368,150 q8,-14 8,-6 q0,8 -8,6 z", fill="#2B2B2B")
    f.text(386, 146, "petróleo e gás", 6.0, 800, "#2B2B2B")
    f.rect(290, 162, 160, 12, fill="#90CAF9", opacity=0.9)
    f.text(370, 168, "aquífero (rocha porosa com água)", 5.8, 800, "#0D47A1", "middle", valign="mid")
    f.circle(470, 112, 2.8, fill="#2B2B2B")
    f.text(478, 106, "carvão", 6.0, 800, "#2B2B2B", "start")
    f.path("M492,140 q6,-6 12,0 q-6,6 -12,0 z", fill="#FFFFFF", stroke="#6D4C41", sw=0.8)
    f.text(508, 136, "fósseis", 6.0, 700, "#6D4C41", "start", italic=True)
    f.poly([(584, 150), (616, 96), (636, 118), (652, 100), (704, 150)], fill="#C9C9C9", stroke="#8A8A8A", sw=0.9, dash="3 2")
    f.text(645, 32, "DOBRAMENTOS MODERNOS", 6.8, 800, "#7A7A7A", "middle")
    f.text(645, 44, "Cenozoico: Andes, Himalaia", 5.7, 600, "#7A7A7A", "middle")
    f.text(645, 54, "ausentes no território brasileiro", 5.7, 800, "#C62828", "middle")
    f.line(596, 70, 700, 146, "#C62828", 1.6)
    f.line(700, 70, 596, 146, "#C62828", 1.6)
    f.rect(0, 178, W, 36, fill="#F4EBE0")
    f.text(8, 183, "Brasil: no centro da Placa Sul-Americana (tectonicamente estável) → escudos e bacias; sem dobramentos modernos nem vulcanismo ativo.", 6.3, 800, "#5D3A1A")
    f.text(8, 196, "Recursos associados: escudos → minerais metálicos · bacias → combustíveis fósseis (petróleo, gás, carvão) e grandes aquíferos.", 6.3, 600, "#5D3A1A")
    save_svg("estrutura_geologica", f.render())


# ------------------------------------------------------------------------------
def chuva_convectiva():
    f = Fig(THIRD, 196, "chuva_convectiva", "Chuva convectiva")
    W = THIRD
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.rect(0, 20, W, 140, fill=SKY)
    f.rect(0, 150, W, 46, fill="#C9A77C")
    f.sun(30, 44, 9)
    f.text(W / 2, 3, "CONVECTIVA (verão)", 7.2, 800, "#E65100", "middle")
    # nuvem cumulonimbus
    f.path("M80,60 a22,18 0 0 1 36,-12 a24,20 0 0 1 46,6 a16,14 0 0 1 14,22 l-96,0 a12,10 0 0 1 0,-16 z", fill="#B0BEC5", stroke="#78909C", sw=1)
    f.poly([(92, 76), (170, 76), (156, 66), (104, 66)], fill="#90A4AE")
    f.raindrops(98, 86, 8, "#1565C0", 9, 11)
    f.raindrops(104, 102, 7, "#1565C0", 9, 11)
    # ar quente ascendente
    for x in (60, 100, 140, 180):
        f.arrow(x, 146, x, 108 if x in (100, 140) else 120, "#E53935", 2.2, 7)
    f.text(18, 124, "ar quente\ne úmido sobe", 6.0, 800, "#C62828", lh=1.1)
    f.text(W - 8, 140, "solo muito\naquecido", 6.0, 800, "#8C6039", "end", lh=1.1)
    f.text(W / 2, 166, "Aquecimento do solo → ar sobe → resfria e\ncondensa → pancadas fortes e rápidas\n(fim de tarde, verão). Típica do Brasil tropical.", 6.2, 600, INK, "middle", lh=1.2)
    save_svg("chuva_convectiva", f.render())


def chuva_frontal():
    f = Fig(THIRD, 196, "chuva_frontal", "Chuva frontal")
    W = THIRD
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.rect(0, 20, W, 140, fill=SKY)
    f.rect(0, 150, W, 46, fill="#C9A77C")
    f.text(W / 2, 3, "FRONTAL (encontro de massas)", 7.2, 800, "#5E35B1", "middle")
    # cunha de ar frio
    f.poly([(0, 150), (0, 60), (60, 82), (150, 150)], fill="#C5CAE9", stroke="#5E35B1", sw=1.2)
    f.text(12, 112, "mPa\nfria e densa", 6.2, 800, "#3F2B8F", lh=1.1)
    f.arrow(26, 52, 70, 70, "#3F2B8F", 2.2, 7)
    # ar quente e úmido sobe sobre a cunha
    f.path("M210,134 C 190,126 170,110 150,90 C 135,76 118,62 104,50", stroke="#E53935", sw=2.6, opacity=0.9)
    f.arrow(112, 56, 100, 46, "#E53935", 2.6, 8)
    f.text(W - 8, 126, "mTa/mEc\nquente e úmida", 6.2, 800, "#C62828", "end", lh=1.1)
    f.path("M70,44 a14,12 0 0 1 24,-8 a16,13 0 0 1 30,4 a10,9 0 0 1 8,14 l-62,0 a8,7 0 0 1 0,-10 z", fill="#B0BEC5", stroke="#78909C", sw=1)
    f.path("M118,48 a12,10 0 0 1 20,-6 a14,12 0 0 1 26,4 a9,8 0 0 1 6,12 l-52,0 z", fill="#B0BEC5", stroke="#78909C", sw=1)
    f.raindrops(84, 66, 6, "#1565C0", 9, 11)
    f.raindrops(130, 66, 6, "#1565C0", 9, 11)
    # frente (símbolo)
    f.line(60, 82, 150, 150, "#5E35B1", 2.4)
    for t in (0.22, 0.5, 0.78):
        x, y = 60 + 90 * t, 82 + 68 * t
        f.poly([(x - 5.5, y - 4.2), (x + 5.5, y + 4.2), (x + 7.4, y - 9.8)], fill="#5E35B1")
    f.text(W / 2, 166, "Massa de ar fria empurra a quente → o ar\nquente sobe, condensa → chuva prolongada,\nampla e mais fria (frente fria: S/SE no inverno).", 6.2, 600, INK, "middle", lh=1.2)
    save_svg("chuva_frontal", f.render())


def chuva_orografica():
    f = Fig(TWO_THIRD, 236, "chuva_orografica", "Chuva orográfica: barlavento e sotavento")
    W = TWO_THIRD
    f.rect(0, 0, W, 236, fill="#FFFFFF")
    f.rect(0, 24, W, 162, fill=SKY)
    land = [(117, 150), (165, 134), (215, 96), (250, 66), (270, 56), (292, 66), (325, 108), (362, 148), (W, 152)]
    f.poly(land + [(W, 186), (117, 186)], fill="#C9A77C", stroke="#8C6039", sw=1.0)
    f.rect(0, 150, 117, 36, fill=SEA)
    f.rect(0, 186, W, 50, fill="#F4EBE0")
    for (xx, yy) in [(178, 124), (200, 107), (222, 90)]:
        f.tree(xx, yy, 0.8)
    for (xx, yy) in [(332, 115), (347, 131), (364, 147), (395, 151), (430, 152)]:
        f.path(f"M{xx},{yy} l0,-8 m-4,3 l4,-3 l4,-5", stroke="#A59A4B", sw=1.2)
    f.curve_arrow(14, 108, 96, 104, 176, 90, "#1E88E5", 2.6, 9)
    f.curve_arrow(14, 82, 110, 70, 226, 42, "#1E88E5", 2.6, 9)
    f.path("M218,52 a16,13 0 0 1 28,-8 a18,15 0 0 1 34,4 a11,10 0 0 1 8,16 l-72,0 a9,8 0 0 1 2,-12 z", fill="#B0BEC5", stroke="#78909C", sw=1)
    f.raindrops(230, 72, 7, "#1565C0", 8, 10)
    f.curve_arrow(296, 40, 346, 46, 380, 92, "#E53935", 2.4, 9)
    f.curve_arrow(310, 28, 380, 30, 426, 90, "#E53935", 2.0, 8)
    f.text(W - 8, 100, "ar seco e quente\ndesce e se aquece", 6.2, 800, "#C62828", "end", lh=1.1)
    f.sun(446, 70, 7)
    f.text(8, 30, "BARLAVENTO", 8.2, 800, "#0D47A1")
    f.text(8, 42, "lado de onde vem o vento", 5.9, 600, "#0D47A1")
    f.text(W - 8, 30, "SOTAVENTO", 8.2, 800, "#C62828", "end")
    f.text(W - 8, 42, "lado “protegido” do vento", 5.9, 600, "#C62828", "end")
    f.text(58, 170, "Oceano\n(umidade)", 6.2, 800, "#0D47A1", "middle", lh=1.1)
    f.text(8, 120, "ar úmido sobe → esfria\n≈ 0,6 °C a cada 100 m\n→ vapor condensa → chove", 5.9, 800, "#0D47A1", lh=1.12)
    f.text(398, 170, "SOMBRA DE CHUVA\nclima mais seco", 6.3, 800, "#FFFFFF", "middle", lh=1.12)
    f.text(206, 166, "chuvas abundantes\nvegetação úmida", 6.2, 800, "#FFFFFF", "middle", lh=1.12)
    f.para(12, 193, W - 24, "O relevo obriga o ar úmido a subir: esfria, o vapor condensa e chove na encosta exposta ao vento (barlavento). O ar chega seco ao outro lado (sotavento), desce e aquece: chuva escassa. Ex.: o Sertão, a oeste do Planalto da Borborema.", 6.3, 600, INK, lh=1.25)
    save_svg("chuva_orografica", f.render())


def build():
    perfil_solo()
    solos_comparados()
    intemperismo_erosao()
    estrutura_geologica()
    chuva_convectiva()
    chuva_frontal()
    chuva_orografica()
