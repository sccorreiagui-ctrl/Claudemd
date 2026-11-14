"""Módulo E — Geografia Econômica: revoluções industriais, modelos produtivos, cadeias globais, DIT,
integração regional, matrizes energética/elétrica e de transportes, trabalho e desindustrialização."""
import math
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, wrap
from common import save_svg

OR_D = "#B23C00"


def gear(f, cx, cy, r, color="#546E7A", n=8):
    f.circle(cx, cy, r, fill=color)
    for k in range(n):
        a = k * 2 * math.pi / n
        f.rect(cx + math.cos(a) * r - 2, cy + math.sin(a) * r - 2, 4, 4, fill=color)
    f.circle(cx, cy, r * 0.4, fill="#FFFFFF")


# ------------------------------------------------------------------ E1
def timeline():
    H = 222
    f = Fig(FULL, H, "rev_industriais", "Linha do tempo das Revoluções Industriais")
    W = FULL
    cw, gap = 168, 12.6
    data = [
        ("1ª", "c. 1760–1840", "Inglaterra", "Carvão mineral e máquina a vapor", ["Tecelagem mecanizada, ferrovias", "Fábricas, proletariado", "Urbanização e liberalismo"], "#6D4C41"),
        ("2ª", "c. 1870–1914", "EUA, Alemanha, Inglaterra, Japão", "Eletricidade, petróleo e aço", ["Motor a combustão, química", "Telefone e automóvel", "Imperialismo e capital financeiro"], "#E65100"),
        ("3ª", "pós-1950 →", "EUA, Japão, Alemanha", "Eletrônica, informática, robótica", ["Automação flexível, telecomunicações", "Toyotismo e globalização", "Desemprego estrutural"], "#1565C0"),
        ("4ª", "séc. XXI (conceito, 2016)", "EUA, China, UE", "Inteligência artificial, big data, IoT", ["Fábricas “inteligentes”, 5G", "Plataformas e algoritmos", "Disputa por chips e redes"], "#7B3FA0"),
    ]
    f.line(8, 22, W - 8, 22, "#B0BEC5", 3)
    for i, (n, ano, pais, base, items, c) in enumerate(data):
        x = i * (cw + gap)
        f.circle(x + cw / 2, 22, 11, fill=c)
        f.text(x + cw / 2, 22, n, 8.0, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x, 40, cw, H - 42, fill="#FFFFFF", stroke=c, sw=1.4, rx=6)
        f.rect(x, 40, cw, 22, fill=c, rx=6)
        f.text(x + cw / 2, 51, ano, 7.0, 800, "#FFFFFF", "middle", valign="mid")
        ix, iy = x + cw / 2, 96
        if i == 0:
            gear(f, ix - 18, iy, 16, "#6D4C41"); gear(f, ix + 14, iy + 8, 11, "#8D6E63")
            f.rect(ix - 4, iy - 34, 8, 14, fill="#546E7A"); f.path(f"M{ix},{iy-36} q6,-10 14,-8", stroke="#B0BEC5", sw=2)
        elif i == 1:
            f.circle(ix - 18, iy - 4, 12, fill="#FFD54F", stroke="#F9A825", sw=1.2); f.rect(ix - 22, iy + 8, 8, 6, fill="#78909C")
            f.rect(ix + 2, iy - 2, 34, 14, fill="#E65100", rx=3); f.circle(ix + 10, iy + 14, 5, fill="#263238"); f.circle(ix + 28, iy + 14, 5, fill="#263238")
        elif i == 2:
            f.rect(ix - 24, iy - 20, 48, 40, fill="#37474F", rx=4)
            for k in range(3):
                f.line(ix - 16, iy - 10 + k * 10, ix + 16, iy - 10 + k * 10, "#80CBC4", 1.6)
            for k in range(4):
                f.line(ix - 30, iy - 12 + k * 8, ix - 24, iy - 12 + k * 8, "#37474F", 2); f.line(ix + 24, iy - 12 + k * 8, ix + 30, iy - 12 + k * 8, "#37474F", 2)
        else:
            f.circle(ix, iy, 14, fill="#B39DDB")
            for a in range(0, 360, 60):
                x2, y2 = ix + 28 * math.cos(math.radians(a)), iy + 22 * math.sin(math.radians(a))
                f.line(ix, iy, x2, y2, "#7B3FA0", 1.4); f.circle(x2, y2, 4.5, fill="#7B3FA0")
        f.text(x + cw / 2, 128, pais, 6.0, 700, MUTED, "middle")
        h = f.para(x + 8, 141, cw - 16, base, 6.8, 800, c, "middle", lh=1.15)
        yy = 141 + h + 8
        for it in items:
            f.rect(x + 8, yy + 2, 4, 4, fill=c)
            hh = f.para(x + 16, yy - 1, cw - 24, it, 6.3, 500, INK, lh=1.2)
            yy += max(hh, 10) + 6
    save_svg("rev_industriais", f.render())


def modelos():
    RH, RG = 33, 3
    top = 100
    H = top + 4 * (RH + RG) + 20
    f = Fig(FULL, H, "taylor_ford_toyota", "Taylorismo, fordismo e toyotismo")
    W = FULL
    cw, gap = 226, 16
    cols = [
        ("TAYLORISMO", "EUA, c. 1900–1911 (F. W. Taylor)", "#5E35B1",
         [("Ideia", "Administração científica: máxima eficiência individual"), ("Como", "Cronometragem, divisão extrema de tarefas, gestos “inúteis” eliminados"),
          ("Trabalho", "Separa **pensar** (gerência) de **fazer** (operário); salário por produtividade"), ("Crítica", "Alienação; trabalho repetitivo e controlado")]),
        ("FORDISMO", "EUA, 1913 (H. Ford)", "#E65100",
         [("Ideia", "Produção **em massa** de produtos padronizados"), ("Como", "**Linha de montagem** (esteira) + taylorismo; grandes estoques; “qualquer cor, desde que preta”"),
          ("Trabalho", "Salários maiores e jornada de 8 h para formar consumidores de massa"), ("Crise", "Anos 1970: saturação, rigidez e choques do petróleo")]),
        ("TOYOTISMO", "Japão, pós-1950 (T. Ohno)", "#1565C0",
         [("Ideia", "Produção **flexível** e enxuta (acumulação flexível)"), ("Como", "**Just-in-time**, kanban, estoque mínimo, controle de qualidade total"),
          ("Trabalho", "Operário **polivalente**, equipes; terceirização e rede de fornecedores"), ("Efeitos", "Precarização, fragmentação sindical, produtos personalizados")]),
    ]
    for i, (t, sub, c, rows) in enumerate(cols):
        x = i * (cw + gap)
        f.rect(x, 0, cw, 30, fill=c, rx=6)
        f.text(x + cw / 2, 9, t, 8.6, 800, "#FFFFFF", "middle")
        f.text(x + cw / 2, 21, sub, 6.0, 600, "#FFFFFF", "middle")
        f.rect(x, 34, cw, 60, fill="#F5F7FA", stroke="#D5DBE4", sw=0.8, rx=4)
        ix = x + cw / 2
        if i == 0:
            f.circle(ix - 30, 66, 19, fill="#FFFFFF", stroke=c, sw=2.4); f.line(ix - 30, 66, ix - 30, 53, c, 2.0); f.line(ix - 30, 66, ix - 21, 70, c, 2.0); f.rect(ix - 33, 42, 6, 4, fill=c)
            f.text(ix + 4, 58, "cronômetro:\ntempo e movimentos", 6.0, 700, c, lh=1.15)
        elif i == 1:
            f.text(ix, 39, "esteira de montagem", 6.0, 700, c, "middle")
            f.rect(ix - 70, 74, 140, 8, fill="#546E7A", rx=4)
            for k in range(5):
                f.circle(ix - 60 + k * 30, 86, 3.5, fill="#263238")
            for k in range(3):
                f.rect(ix - 50 + k * 44, 58, 18, 14, fill=c, rx=1.5)
        else:
            f.text(ix, 39, "Just-in-time (puxado pela demanda)", 6.0, 700, c, "middle")
            for k, tx in enumerate(["demanda", "kanban", "produção"]):
                f.rect(ix - 78 + k * 54, 54, 48, 28, fill="#FFFFFF", stroke=c, sw=1.4, rx=3)
                f.text(ix - 54 + k * 54, 68, tx, 6.2, 800, c, "middle", valign="mid")
                if k < 2:
                    f.arrow(ix - 30 + k * 54, 68, ix - 24 + k * 54, 68, c, 1.4, 5)
        y = top
        for lab, txt in rows:
            f.rect(x, y, cw, RH, fill="#FFFFFF", stroke="#E3E8EE", sw=0.8, rx=3)
            f.rect(x, y, 46, RH, fill=c, rx=3, opacity=0.14)
            f.text(x + 23, y + RH / 2, lab, 6.5, 800, c, "middle", valign="mid")
            f.para(x + 52, y + 5, cw - 58, txt, 6.3, 500, INK, lh=1.18)
            y += RH + RG
    f.text(W / 2, H - 12, "Fordismo = taylorismo + esteira + consumo de massa  ·  Toyotismo = flexibilidade, polivalência e terceirização.", 6.6, 800, "#5D3A1A", "middle", valign="mid")
    save_svg("taylor_ford_toyota", f.render())


# ------------------------------------------------------------------ E3
def cadeia_global():
    f = Fig(FULL, 240, "cadeia_global", "Cadeia produtiva internacional e curva do sorriso")
    W = FULL
    f.text(0, 0, "Exemplo: smartphone (cadeia global de valor; países ilustrativos)", 8.0, 800, OR_D)
    nodes = [("P&D e design", "sede da empresa: EUA, Japão, UE, Coreia do Sul", "#7B3FA0"), ("Matérias-primas", "minérios e terras raras: Brasil, África, Austrália, China", "#8D5B2E"),
             ("Componentes", "chips e telas: Coreia do Sul, Taiwan, Japão", "#1565C0"), ("Montagem", "China, Vietnã, Índia (mão de obra barata, incentivos)", "#E65100"),
             ("Marca e serviços", "lojas, logística e software no mundo todo", "#7B3FA0")]
    bw, gap = 128, 17.5
    for i, (t, s, c) in enumerate(nodes):
        x = i * (bw + gap)
        f.rect(x, 22, bw, 60, fill="#FFFFFF", stroke=c, sw=1.6, rx=6)
        f.rect(x, 22, bw, 18, fill=c, rx=6)
        f.text(x + bw / 2 + 6, 31, t, 6.6, 800, "#FFFFFF", "middle", valign="mid")
        f.para(x + 5, 44, bw - 10, s, 6.0, 500, INK, "start", lh=1.18)
        f.badge(x + 11, 31, i + 1, "navy", 7.5, 6.4)
        if i < 4:
            f.arrow(x + bw + 1, 52, x + bw + gap - 1, 52, "#37474F", 1.8, 6)
    f.text(0, 94, "“Curva do sorriso” (conceito): valor agregado alto em P&D e em marca/serviços; baixo na montagem", 6.6, 800, "#37474F")
    x0, x1, y0, y1 = 24, 462, 124, 226
    f.line(x0, y1, x1, y1, "#37474F", 1.0); f.line(x0, y0 - 6, x0, y1, "#37474F", 1.0)
    f.text(x0 + 4, y0 - 12, "valor agregado ↑", 5.8, 700, MUTED)
    pts = []
    for k in range(0, 41):
        t = k / 40
        v = 0.15 + 0.8 * ((2 * t - 1) ** 2)
        pts.append((x0 + (x1 - x0) * t, y1 - 8 - (y1 - y0 - 12) * v))
    f.poly(pts + [(x1, y1), (x0, y1)], fill="#FFE0B2", opacity=0.6)
    f.poly(pts, stroke="#E65100", sw=2.4, close=False)
    for t, lab in [(0.0, "P&D e design"), (0.5, "montagem"), (1.0, "marca e serviços")]:
        f.text(x0 + (x1 - x0) * t, y1 + 4, lab, 6.0, 800, INK, "start" if t < 0.1 else ("end" if t > 0.9 else "middle"))
    f.text(x1, y0 - 12, "etapas da cadeia →", 5.8, 700, MUTED, "end")
    ex = ["**Fragmentação:** a empresa transnacional divide a produção por vários países, buscando custos baixos, incentivos fiscais, mercado e mão de obra qualificada.",
          "**Ganho desigual:** países de montagem ficam com **pouco valor**; sede e marca retêm lucros e patentes.",
          "**Brasil:** exporta commodities (minério, soja, petróleo) e importa componentes; pouca participação em etapas de alta tecnologia."]
    y = 108
    for t in ex:
        h = f.para(484, y, 226, t, 6.4, 500, INK, lh=1.22)
        y += h + 7
    save_svg("cadeia_global", f.render())


def dit():
    f = Fig(FULL, 232, "dit_esquema", "Divisão Internacional do Trabalho: tradicional e nova")
    W = FULL
    hw = (W - 14) / 2
    PH = 168
    for i, (t, c) in enumerate([("DIT TRADICIONAL (colonial e industrial, até meados do séc. XX)", "#6D4C41"), ("NOVA DIT (a partir de 1950–70: transnacionais e cadeias globais)", "#E65100")]):
        x0 = i * (hw + 14)
        f.rect(x0, 0, hw, 22, fill=c, rx=5)
        f.text(x0 + hw / 2, 11, t, 6.2, 800, "#FFFFFF", "middle", valign="mid")
        f.rect(x0, 24, hw, PH, fill="#FAFAFA", stroke="#E3E8EE", sw=0.8, rx=4)
    # esquerda: centro e periferia
    f.circle(62, 70, 29, fill="#1565C0"); f.text(62, 66, "CENTRO", 6.8, 800, "#FFFFFF", "middle", valign="mid"); f.text(62, 77, "EUA · Europa", 5.6, 600, "#FFFFFF", "middle", valign="mid")
    f.circle(288, 124, 29, fill="#8D5B2E"); f.text(288, 120, "PERIFERIA", 6.6, 800, "#FFFFFF", "middle", valign="mid"); f.text(288, 131, "Brasil · África", 5.6, 600, "#FFFFFF", "middle", valign="mid")
    f.arrow(98, 66, 252, 108, "#1565C0", 2.6, 8); f.arrow(256, 130, 100, 88, "#8D5B2E", 2.6, 8)
    f.text(190, 66, "manufaturados\n(alto valor)", 6.2, 800, "#0D47A1", "middle", lh=1.1)
    f.text(160, 124, "matérias-primas e commodities\n(baixo valor)", 6.2, 800, "#5D3A1A", "middle", lh=1.1)
    f.para(8, 150, hw - 16, "**Periferia:** agrícola e extrativista, dependente. **Centro:** industrial. Consequência: troca desigual e dependência tecnológica.", 6.3, 500, INK, lh=1.2)
    # direita: nova DIT
    x1 = hw + 14
    f.rect(x1 + 10, 40, 120, 60, fill="#7B3FA0", rx=6)
    f.text(x1 + 70, 52, "SEDE · P&D · FINANÇAS", 6.2, 800, "#FFFFFF", "middle")
    f.text(x1 + 70, 64, "países centrais", 5.8, 600, "#FFFFFF", "middle")
    f.text(x1 + 70, 76, "retém patentes e lucros", 5.8, 700, "#FFFFFF", "middle")
    for k, (lab, y) in enumerate([("montagem\nChina · Vietnã", 30), ("indústria poluente\nMéxico · Índia", 72), ("serviços (call center)\nFilipinas · Índia", 112)]):
        f.rect(x1 + 214, y, 126, 38, fill="#FFE0B2", stroke="#E65100", sw=1.2, rx=5)
        f.text(x1 + 277, y + 19, lab, 6.0, 800, OR_D, "middle", valign="mid", lh=1.12)
        f.arrow(x1 + 132, 70, x1 + 211, y + 19, "#7B3FA0", 1.8, 6)
    f.para(x1 + 10, 108, 120, "ordens, projetos e capital →\n← mercadorias e lucros", 5.8, 700, "#4A148C", "start", lh=1.15)
    f.para(x1 + 8, 150, hw - 16, "**Transnacionais** buscam mão de obra barata, incentivos fiscais e leis ambientais e trabalhistas mais brandas. Surgem países industrializados na periferia e há **desindustrialização relativa** de parte do centro.", 6.1, 500, INK, lh=1.18)
    f.rect(0, 24 + PH + 6, W, 30, fill="#FFF0E0", rx=4)
    f.para(8, 24 + PH + 11, W - 16, "**Fuga de cérebros (brain drain):** profissionais qualificados da periferia migram para centros de pesquisa.  **Compressão espaço-tempo:** transportes e comunicações encurtam o tempo, não a distância.", 6.2, 700, OR_D, "middle", lh=1.18)
    save_svg("dit_esquema", f.render())


# ------------------------------------------------------------------ E4
def terc():
    f = Fig(FULL, 214, "terc_terc", "Terceirização e terciarização")
    W = FULL
    hw = (W - 14) / 2
    f.rect(0, 0, hw, 22, fill="#E65100", rx=5); f.text(hw / 2, 11, "TERCEIRIZAÇÃO (organização do trabalho)", 6.8, 800, "#FFFFFF", "middle", valign="mid")
    f.rect(hw + 14, 0, hw, 22, fill="#1565C0", rx=5); f.text(hw + 14 + hw / 2, 11, "TERCIARIZAÇÃO (estrutura da economia)", 6.8, 800, "#FFFFFF", "middle", valign="mid")
    f.rect(0, 24, hw, 132, fill="#FFF8F2", stroke="#F2D6BF", sw=0.8, rx=4); f.rect(hw + 14, 24, hw, 132, fill="#F4F9FE", stroke="#CFE2F3", sw=0.8, rx=4)
    f.box(14, 38, 124, 30, "Empresa contratante", fill="laranja", pt=6.6, weight=800)
    f.box(208, 38, 124, 30, "Empresa terceirizada", fill="laranja", pt=6.6, weight=800)
    f.arrow(140, 53, 204, 53, OR_D, 1.8, 7); f.text(172, 40, "contrato", 5.8, 700, OR_D, "middle")
    for k in range(3):
        px = 232 + k * 34
        f.circle(px, 96, 6, fill="#E65100"); f.line(px, 102, px, 118, "#E65100", 2); f.line(px - 6, 108, px + 6, 108, "#E65100", 2)
    f.line(270, 70, 270, 88, OR_D, 1.2, dash="3 2")
    f.para(14, 80, 160, "Reduz custos e transfere responsabilidades trabalhistas; pode precarizar salários e direitos.", 6.0, 500, INK, lh=1.2)
    f.para(14, 134, hw - 28, "O trabalhador tem vínculo com a terceirizada, não com a contratante.", 5.9, 700, OR_D, "start", lh=1.15)
    x0 = hw + 14
    f.text(x0 + hw / 2, 29, "Participação dos setores (esquema ilustrativo)", 6.0, 700, "#0D47A1", "middle")
    sets = [[("terciário", 25, "#1565C0"), ("secundário", 15, "#E65100"), ("primário", 60, "#8D5B2E")],
            [("terciário", 45, "#1565C0"), ("secundário", 35, "#E65100"), ("primário", 20, "#8D5B2E")],
            [("terciário", 70, "#1565C0"), ("secundário", 22, "#E65100"), ("primário", 8, "#8D5B2E")]]
    base = 128
    for i, st in enumerate(sets):
        bx = x0 + 18 + i * 110
        y = base
        for nm, v, c in st:
            h = v * 0.88
            f.rect(bx, y - h, 90, h, fill=c)
            if v >= 14:
                f.text(bx + 45, y - h / 2, nm, 6.0, 700, "#FFFFFF", "middle", valign="mid")
            y -= h
        f.text(bx + 45, base + 3, ["início (economia agrária)", "meio (auge industrial)", "hoje (economia de serviços)"][i], 5.4, 800, INK, "middle")
    f.text(x0 + hw / 2, 142, "Cresce o peso de comércio e serviços no PIB e no emprego", 5.8, 800, "#0D47A1", "middle")
    f.rect(0, 162, W, 48, fill="#F5F7FA", rx=4)
    f.para(8, 167, W - 16, "**Terceirização:** transferência de atividades a outra empresa. **Terciarização:** aumento do peso do setor terciário (comércio e serviços) na economia. No Brasil, a Lei 13.429/2017 e a Reforma Trabalhista (Lei 13.467/2017) ampliaram a terceirização; em 2018, o STF a validou também para atividades-fim. **Não confundir:** terceirização é uma forma de contratar; terciarização é uma mudança estrutural.", 6.3, 500, INK, lh=1.22)
    save_svg("terc_terc", f.render())


# ------------------------------------------------------------------ E5
def integracao():
    f = Fig(FULL, 200, "integracao_degraus", "Etapas da integração econômica regional")
    W = FULL
    f.text(0, 0, "Quanto mais alto o degrau, maior a integração e a perda de autonomia nacional (supranacionalidade)", 7.4, 800, "#37474F")
    steps = [("1. ZONA DE LIVRE COMÉRCIO", "Elimina tarifas entre os membros; cada país mantém a sua tarifa externa.", "USMCA (ex-NAFTA): EUA, México e Canadá", "#2E7D32"),
             ("2. UNIÃO ADUANEIRA", "Livre comércio interno + **Tarifa Externa Comum (TEC)**.", "Mercosul (imperfeita: há exceções à TEC)", "#1565C0"),
             ("3. MERCADO COMUM", "União aduaneira + livre circulação de **pessoas, capitais e serviços**.", "União Europeia (mercado único)", "#C04A00"),
             ("4. UNIÃO ECONÔMICA E MONETÁRIA", "Mercado comum + **moeda única**, banco central e políticas econômicas coordenadas.", "UE: países da zona do euro", "#7B3FA0")]
    sw, gp = 168, 12.7
    base = 164
    for i, (t, d, ex, c) in enumerate(steps):
        x = i * (sw + gp)
        h = 84 + i * 19
        y = base - h
        f.rect(x, y, sw, h, fill=c, rx=5)
        th = f.para(x + 8, y + 7, sw - 16, t, 6.8, 800, "#FFFFFF", lh=1.15)
        f.para(x + 8, y + 7 + th + 4, sw - 16, d, 6.2, 500, "#FFFFFF", lh=1.2)
        f.para(x + 8, base - 26, sw - 16, ex, 6.0, 800, "#FFFFFF", lh=1.15)
    f.rect(0, 170, W, 28, fill="#F5F7FA", rx=4)
    f.para(8, 175, W - 16, "**Protecionismo:** tarifas e barreiras não tarifárias (cotas, subsídios, exigências técnicas e sanitárias)  ×  **livre-comércio** (a OMC busca reduzir as barreiras).", 6.4, 700, "#37474F", "middle", lh=1.2)
    save_svg("integracao_degraus", f.render())


# ------------------------------------------------------------------ E6
def energia():
    f = Fig(FULL, 256, "matriz_energia", "Matriz energética e matriz elétrica do Brasil, 2025 (BEN 2026)")
    W = FULL
    hw = (W - 20) / 2
    en = [("Petróleo e derivados", 33.7, 0), ("Biomassa da cana", 15.8, 1), ("Hidráulica", 10.7, 1), ("Gás natural", 10.3, 0), ("Licor preto e outras renováveis", 8.9, 1), ("Lenha e carvão vegetal", 8.3, 1),
          ("Carvão mineral", 4.5, 0), ("Eólica", 3.0, 1), ("Solar", 2.7, 1), ("Urânio", 1.3, 0), ("Outras não renováveis", 0.8, 0)]
    el = [("Hidráulica", 51.2, 1), ("Eólica", 14.9, 1), ("Solar", 11.4, 1), ("Biomassa", 8.4, 1), ("Gás natural", 7.5, 0), ("Carvão e derivados", 2.2, 0), ("Nuclear", 2.0, 0), ("Derivados de petróleo", 1.5, 0), ("Importação*", 0.9, 1)]

    def panel(x0, title, sub, data, vmax):
        f.text(x0, 0, title, 8.0, 800, OR_D); f.text(x0, 12, sub, 6.2, 600, MUTED)
        y = 30
        for nm, v, ren in data:
            c = "#2E7D32" if ren else "#6D4C41"
            f.text(x0, y + 6, nm, 6.2, 600, INK, valign="mid")
            bx = x0 + 128
            w = (hw - 128 - 34) * v / vmax
            f.rect(bx, y, w, 12, fill=c)
            f.text(bx + w + 3, y + 6, f"{v:.1f}%".replace(".", ","), 6.2, 800, c, valign="mid")
            y += 17.2
    panel(0, "Matriz ENERGÉTICA (oferta interna de energia)", "total: 328,5 Mtep · renováveis 49,4%", en, 34)
    panel(hw + 20, "Matriz ELÉTRICA (oferta interna de eletricidade)", "total: 783,3 TWh · renováveis 86,8%", el, 52)
    lx = hw + 20
    f.rect(lx, 200, 10, 8, fill="#2E7D32"); f.text(lx + 14, 199, "renovável", 6.2, 700, INK)
    f.rect(lx + 70, 200, 10, 8, fill="#6D4C41"); f.text(lx + 84, 199, "não renovável", 6.2, 700, INK)
    f.para(lx, 214, hw, "* A EPE inclui a importação (≈ 0,9%) entre as fontes renováveis no cálculo de 86,8%.", 5.6, 500, MUTED, lh=1.2)
    f.para(0, 226, W, "Fonte: EPE, Balanço Energético Nacional 2026 (ano-base 2025). Energia ≠ eletricidade: a eletricidade é só uma parte da matriz energética (que inclui transporte, indústria e calor). Na matriz energética pesam o petróleo (transportes) e a biomassa; na elétrica, a hidráulica; eólica + solar somam ≈ 26% (2025).", 6.0, 600, "#5D3A1A", lh=1.22)
    save_svg("matriz_energia", f.render())


def transportes():
    H = 196
    f = Fig(HALF, H, "matriz_transportes", "Matriz de transporte de cargas")
    W = HALF
    f.text(0, 0, "Transporte de cargas: participação por modal", 7.8, 800, "#37474F")
    f.text(0, 12, "CNT, Boletim Unificado (mar/2022); t·km útil", 6.0, 500, MUTED)
    data = [("Rodoviário", 64.9, "≈ 65%", "#546E7A"), ("Aquaviário", 15.7, "≈ 16%", "#1565C0"), ("Ferroviário", 15.0, "≈ 15%", "#8D5B2E"), ("Dutoviário e aéreo (soma)", 4.4, "≈ 4–5%", "#F9A825")]
    y = 30
    for nm, v, lab, c in data:
        f.text(0, y, nm, 6.4, 700, INK)
        w = (W - 64) * v / 70
        f.rect(0, y + 11, w, 14, fill=c, rx=2)
        f.text(w + 5, y + 18, lab, 6.8, 800, "#37474F", valign="mid")
        y += 34
    f.para(0, 164, W, "O Brasil depende das **rodovias** (mais caras e poluentes em longas distâncias) para escoar grãos e minérios; ferrovias e hidrovias são subutilizadas. É um dos componentes do **“Custo Brasil”**.", 6.2, 500, INK, lh=1.22)
    save_svg("matriz_transportes", f.render())


def compressao():
    H = 182
    f = Fig(HALF, H, "compressao_espaco_tempo", "Compressão espaço-tempo")
    W = HALF
    f.text(0, 0, "Compressão espaço-tempo (D. Harvey)", 7.8, 800, OR_D)
    f.text(0, 12, "Rio de Janeiro ↔ Lisboa (≈ 7.700 km): a distância não muda; o tempo, sim", 6.0, 500, MUTED)
    rows = [("Nau/caravela (séc. XVI)", "≈ 1,5–3 meses", 190, "#6D4C41"), ("Navio a vapor (início do séc. XX)", "≈ 2–3 semanas", 100, "#1565C0"), ("Avião a jato (hoje)", "≈ 10 horas", 24, "#E65100"), ("Internet / videoconferência", "instantâneo", 5, "#7B3FA0")]
    y = 34
    for nm, t, w, c in rows:
        f.text(0, y, nm, 6.4, 700, INK)
        f.rect(0, y + 11, w, 14, fill=c, rx=3)
        f.text(w + 6, y + 18, t, 6.6, 800, c, valign="mid")
        y += 30
    f.para(0, y + 4, W, "Tempos aproximados e ilustrativos. A “aldeia global” é desigual: nem todos têm acesso às redes.", 5.8, 500, MUTED, lh=1.2)
    save_svg("compressao_espaco_tempo", f.render())


def desindustrializacao():
    H = 226
    f = Fig(HALF, H, "desindustrializacao", "Desindustrialização clássica e precoce")
    W = HALF
    f.text(0, 0, "Desindustrialização: clássica × precoce (esquema conceitual)", 7.2, 800, OR_D)
    x0, x1, y0, y1 = 26, W - 8, 34, 134
    f.line(x0, y1, x1, y1, "#37474F", 1.0); f.line(x0, y0 - 4, x0, y1, "#37474F", 1.0)
    f.text(x0 + 4, y0 - 12, "peso da indústria (emprego/PIB) ↑", 5.4, 700, MUTED); f.text(x1, y1 + 3, "renda per capita →", 5.6, 700, MUTED, "end")

    def arc(peak_x, peak_y, wid):
        pts = []
        for k in range(0, 61):
            t = k / 60
            xx = x0 + (x1 - x0) * t
            yy = y1 - (y1 - peak_y - 6) * math.exp(-((t - peak_x) / wid) ** 2) - 4
            pts.append((xx, yy))
        return pts
    a = arc(0.72, y0 + 4, 0.30); b = arc(0.40, y0 + 34, 0.22)
    f.poly(a, stroke="#1565C0", sw=2.4, close=False); f.poly(b, stroke="#C62828", sw=2.4, close=False)
    f.circle(x0 + (x1 - x0) * 0.72, y0 + 8, 3, fill="#1565C0"); f.circle(x0 + (x1 - x0) * 0.40, y0 + 36, 3, fill="#C62828")
    f.line(x0, y1 + 14, x0 + 16, y1 + 14, "#1565C0", 2.4); f.text(x0 + 22, y1 + 14, "países ricos: auge com renda alta", 5.9, 800, "#0D47A1", valign="mid")
    f.line(x0, y1 + 26, x0 + 16, y1 + 26, "#C62828", 2.4); f.text(x0 + 22, y1 + 26, "Brasil: auge e queda com renda média (precoce)", 5.9, 800, "#B71C1C", valign="mid")
    f.para(0, y1 + 38, W, "**Clássica:** fábricas migram para a periferia, mas o país mantém comando, tecnologia e serviços sofisticados. **Precoce:** a indústria encolhe antes de se atingir alta renda e maturidade tecnológica; “Custo Brasil”, câmbio e importações favorecem a **reprimarização** (exportar produtos primários).", 5.9, 500, INK, lh=1.22)
    save_svg("desindustrializacao", f.render())


def desemprego():
    H = 206
    f = Fig(HALF, H, "desemprego_tipos", "Desemprego estrutural e conjuntural")
    W = HALF
    f.text(0, 0, "Desemprego: conjuntural × estrutural (esquema)", 7.4, 800, OR_D)
    x0, x1, y0, y1 = 26, W - 8, 36, 118
    f.rect(x0 + 100, y0 - 2, 36, y1 - y0 + 2, fill="#ECEFF1")
    f.line(x0, y1, x1, y1, "#37474F", 1.0); f.line(x0, y0 - 4, x0, y1, "#37474F", 1.0)
    f.text(x0 + 4, y0 - 15, "vagas de trabalho ↑", 5.6, 700, MUTED); f.text(x1, y1 + 3, "tempo →", 5.6, 700, MUTED, "end")
    pts1 = [(x0, y0 + 14), (x0 + 60, y0 + 12), (x0 + 100, y0 + 50), (x0 + 130, y0 + 56), (x0 + 190, y0 + 22), (x1, y0 + 12)]
    pts2 = [(x0, y0 + 14), (x0 + 60, y0 + 12), (x0 + 100, y0 + 36), (x0 + 130, y0 + 50), (x0 + 190, y0 + 58), (x1, y0 + 62)]
    f.poly(pts1, stroke="#1565C0", sw=2.4, close=False); f.poly(pts2, stroke="#C62828", sw=2.4, close=False)
    f.text(x0 + 118, y0 + 66, "crise", 5.8, 800, "#37474F", "middle")
    f.text(x1, y0 - 2, "conjuntural: as vagas voltam", 5.8, 800, "#0D47A1", "end")
    f.text(x1, y1 - 12, "estrutural: não voltam (automação)", 5.8, 800, "#B71C1C", "end")
    f.para(0, y1 + 14, W, "**Conjuntural (cíclico):** causado por crise econômica passageira; a retomada do PIB recria vagas. **Estrutural:** mudança tecnológica ou da organização produtiva elimina ocupações (ex.: cobradores de ônibus, digitadores); exige requalificação.", 6.0, 500, INK, lh=1.22)
    save_svg("desemprego_tipos", f.render())


def balanca():
    H = 168
    f = Fig(HALF, H, "balanca_comercial", "Balança comercial do Brasil")
    W = HALF
    f.text(0, 0, "Balança comercial do Brasil (US$ bilhões)", 7.8, 800, OR_D)
    f.text(0, 12, "MDIC, divulgação de 6/1/2026 (valores correntes)", 6.0, 500, MUTED)
    y1 = 124
    sc = 0.30
    # painel 1: 2025
    f.text(0, 24, "2025", 6.6, 800, INK)
    xs = [(6, "Exportações", 348.676, "#E65100"), (66, "Importações", 280.382, "#546E7A"), (126, "Saldo (superávit)", 68.293, "#1565C0")]
    for x, nm, v, c in xs:
        h = v * sc
        f.rect(x, y1 - h, 46, h, fill=c, rx=2)
        f.text(x + 23, y1 - h - 9, f"{v:.1f}".replace(".", ","), 6.8, 800, c, "middle")
        f.para(x - 8, y1 + 5, 62, nm, 6.0, 700, INK, "middle", lh=1.1)
    f.line(0, y1, 186, y1, "#37474F", 1.0)
    # painel 2: saldo por ano
    x0 = 214
    f.text(x0, 24, "Saldo comercial", 6.6, 800, INK)
    for k, (an, v) in enumerate([("2023", 98.903), ("2024", 74.177), ("2025", 68.293)]):
        x = x0 + k * 44
        h = v * sc
        f.rect(x, y1 - h, 34, h, fill="#1565C0", rx=2, opacity=(0.55 if k < 2 else 1))
        f.text(x + 17, y1 - h - 9, f"{v:.1f}".replace(".", ","), 6.4, 800, "#0D47A1", "middle")
        f.text(x + 17, y1 + 5, an, 6.2, 700, INK, "middle")
    f.line(x0 - 6, y1, W, y1, "#37474F", 1.0)
    f.para(0, 148, W, "Balança comercial = exportações − importações. Superávit: exporta mais do que importa.", 5.9, 500, MUTED, lh=1.2)
    save_svg("balanca_comercial", f.render())


def build():
    timeline(); modelos(); cadeia_global(); dit(); terc(); integracao(); energia(); transportes(); compressao(); desindustrializacao(); desemprego(); balanca()
