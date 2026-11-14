"""Módulo A — diagramas: camadas da Terra, convecção, limites de placas, ciclo das rochas."""
import math
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, col
from common import save_svg

WATER = "#CFE6F7"
SEA = "#A9D3F0"
MANTLE = "#F6D3AE"
MANTLE_D = "#EDB57E"
CRUST_C = "#B98B5E"     # crosta continental
CRUST_O = "#4F6272"     # crosta oceânica
LITHO = "#9FADB9"       # manto litosférico
RED = "#D84315"
BLUE = "#1565C0"


def band(pts, th, side=1):
    """Gera polígono de faixa com espessura th a partir de uma polilinha (lado: +1 abaixo/direita, -1 acima)."""
    n = len(pts)
    nor = []
    for i in range(n):
        if i == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nor.append((-dy / L * side, dx / L * side))
    top = list(pts)
    bot = [(p[0] + nx * th, p[1] + ny * th) for p, (nx, ny) in zip(pts, nor)]
    return top + bot[::-1]


def lead(f, x1, y1, x2, y2, color=INK, dot=True, sw=0.8):
    f.line(x1, y1, x2, y2, color, sw)
    if dot:
        f.circle(x1, y1, 1.8, fill=color)


# ---------------------------------------------------------------------------------
def camadas_terra():
    f = Fig(FULL, 232, "camadas_terra", "Corte transversal da Terra com suas camadas")
    cx, cy, R = 118, 112, 102
    k = R / 6371.0
    # camadas (raios em km)
    layers = [(6371, "#7B4B2A"), (6271, "#E07B39"), (5701, "#C8502D"), (3480, "#F4B63F"), (1220, "#FBE08A")]
    # ordem: crosta+litosfera (exagerada) > manto superior > manto inferior > núcleo externo > núcleo interno
    f.circle(cx, cy, R, fill="#7B4B2A")
    f.circle(cx, cy, R - 6, fill="#E8893F")          # manto superior/astenosfera
    f.circle(cx, cy, 5701 * k, fill="#C8502D")        # manto inferior
    f.circle(cx, cy, 3480 * k, fill="#F4B63F")        # núcleo externo
    f.circle(cx, cy, 1220 * k, fill="#FBE08A")        # núcleo interno
    f.circle(cx, cy, R, fill="none", stroke="#FFFFFF", sw=1.4)
    # rótulos dentro do círculo
    f.text(cx, cy, "NÚCLEO\nINTERNO", 5.2, 800, "#6A4A00", "middle", valign="mid")
    f.text(cx - 2, cy + 40, "núcleo externo", 5.6, 800, "#7A4A00", "middle", valign="mid")
    f.text(cx - 20, cy - 74, "MANTO", 7.2, 800, "#FFFFFF", "middle", valign="mid", spacing="1.5")
    # setas de calor/convecção dentro do manto (discretas)
    # pontos de ligação (ângulos em graus, sentido anti-horário a partir do leste; y para cima negativo)
    def pt(ang, r):
        a = math.radians(ang)
        return cx + r * math.cos(a), cy - r * math.sin(a)
    items = [
        ("Crosta e litosfera", "#7B4B2A", pt(58, R - 2), 2,
         "**Sólidas e rígidas.** Crosta: ≈ 5–10 km (oceânica) a 30–70 km (continental). Litosfera (≈ 100 km): crosta + topo do manto, partida em **placas tectônicas**."),
        ("Astenosfera", "#C25E1B", pt(30, R - 14), 48,
         "**≈ 100–400 km.** Rocha sólida, quente e dúctil, que se deforma devagar; as placas “deslizam” sobre ela."),
        ("Manto", "#A8401F", pt(5, 4300 * k), 94,
         "**≈ 2.900 km de espessura (~84% do volume).** Rocha **sólida** que flui lentamente em escala de milhões de anos (convecção); **não é um oceano de magma**."),
        ("Núcleo externo", "#9A6200", pt(-22, 2400 * k), 140,
         "**2.900–5.150 km, ferro e níquel líquidos.** Seu movimento gera o campo magnético que protege a Terra do vento solar."),
        ("Núcleo interno", "#7A5C00", pt(-48, 700 * k), 186,
         "**5.150–6.371 km, ferro-níquel sólido** (pressão altíssima); mais de ≈ 5.000 °C."),
    ]
    lx = 270
    for name, c, (px, py), ty, desc in items:
        f.line(px, py, lx - 8, ty + 8, "#FFFFFF" if False else "#1D2330", 0.7)
        f.circle(px, py, 2.2, fill="#FFFFFF", stroke="#1D2330", sw=0.8)
        f.text(lx, ty, name, 8.4, 800, c)
        f.para(lx, ty + 12, FULL - lx - 6, desc, 7.1, 400, INK, lh=1.2)
    f.text(8, 218, "Núcleo e manto em escala (1 cm = ≈ 570 km); crosta e litosfera foram exageradas para serem visíveis.", 6.0, 400, MUTED, italic=True)
    save_svg("camadas_terra", f.render())


# ---------------------------------------------------------------------------------
def conveccao():
    f = Fig(HALF, 168, "conveccao", "Correntes de convecção no manto e movimento das placas")
    W = HALF
    f.rect(6, 44, W - 12, 100, fill=MANTLE, stroke="#E2B78E", sw=0.8, rx=3)
    f.poly([(8, 28), (146, 28), (146, 44), (8, 44)], fill=LITHO, stroke="#7C8B97", sw=0.8)
    f.poly([(154, 28), (250, 28), (296, 74), (284, 86), (244, 44), (154, 44)], fill=LITHO, stroke="#7C8B97", sw=0.8)
    f.poly([(146, 44), (154, 44), (152, 30), (148, 30)], fill=RED)
    f.poly([(141, 28), (159, 28), (150, 19)], fill="#6B7A87")
    for i in range(8):
        x = 24 + i * 42
        f.path(f"M{x},144 q3,-4 0,-8 q-3,-4 0,-8", stroke="#E53935", sw=1.2, opacity=0.8)
    f.curve_arrow(150, 122, 148, 88, 150, 52, RED, 2.2, 8)
    f.curve_arrow(144, 54, 100, 50, 46, 66, "#EF6C00", 2.2, 8)
    f.curve_arrow(42, 72, 28, 98, 56, 122, BLUE, 2.2, 8)
    f.curve_arrow(66, 130, 100, 134, 136, 128, "#6D7A86", 2.0, 7)
    f.curve_arrow(156, 54, 200, 50, 244, 64, "#EF6C00", 2.2, 8)
    f.curve_arrow(250, 72, 262, 98, 238, 122, BLUE, 2.2, 8)
    f.curve_arrow(226, 130, 196, 134, 162, 128, "#6D7A86", 2.0, 7)
    f.arrow(124, 22, 76, 22, INK, 2.0, 8)
    f.arrow(176, 22, 224, 22, INK, 2.0, 8)
    f.text(150, 0, "Dorsal: magma sobe e forma nova crosta", 6.4, 800, RED, "middle")
    f.text(14, 31, "Placa A", 6.6, 800, "#37474F")
    f.text(176, 31, "Placa B", 6.6, 800, "#37474F")
    f.text(338, 96, "Subducção:\nplaca fria e\ndensa afunda", 6.4, 800, BLUE, "end", lh=1.12)
    f.text(198, 92, "manto sólido que\nflui lentamente", 6.0, 600, "#8A5A2B", "middle", italic=True, lh=1.12)
    f.text(W / 2, 129, "calor interno do núcleo e decaimento radioativo", 5.8, 800, "#B71C1C", "middle")
    f.line(14, 160, 30, 160, RED, 2.2); f.text(34, 155, "quente sobe", 6.0, 700, RED)
    f.line(104, 160, 120, 160, BLUE, 2.2); f.text(124, 155, "frio desce", 6.0, 700, BLUE)
    f.line(184, 160, 200, 160, "#EF6C00", 2.2); f.text(204, 155, "fluxo sob a placa", 6.0, 700, "#EF6C00")
    save_svg("conveccao", f.render())


# ---------------------------------------------------------------------------------
def lim_andes():
    W, H = TWO_THIRD, 262
    f = Fig(W, H, "lim_andes", "Subducção da Placa de Nazca sob a Placa Sul-Americana e formação dos Andes")
    f.rect(0, 0, W, H, fill="#FFFFFF")
    f.rect(0, 62, W, H - 62, fill=MANTLE)
    f.poly([(0, 62), (212, 62), (190, 76), (150, 112), (110, 100), (0, 94)], fill=SEA)
    top = [(150, 112), (176, 90), (212, 64), (252, 46), (292, 30), (330, 26), (366, 36), (410, 52), (W, 58)]
    bottom = [(W, 100), (410, 104), (370, 110), (330, 118), (292, 112), (250, 104), (200, 100), (160, 108)]
    f.poly(top + bottom, fill=CRUST_C, stroke="#8C6039", sw=0.9)
    f.poly([(318, 29), (330, 26), (342, 29), (330, 34)], fill="#FFFFFF")
    slab_top = [(0, 94), (60, 97), (110, 102), (150, 112), (210, 140), (270, 170), (330, 198), (372, 220)]
    f.poly(band(slab_top, 20), fill=LITHO, stroke="#6E7F8C", sw=0.9)
    f.poly(band(slab_top, 6), fill=CRUST_O)
    f.path("M300,196 C 304,170 314,140 320,118", stroke="#E53935", sw=2.0, dash="3 2")
    f.ellipse(322, 100, 22, 9, fill="#E53935", opacity=0.9)
    f.path("M322,92 C 322,70 330,50 332,32", stroke="#E53935", sw=1.8)
    f.poly([(318, 38), (332, 22), (346, 38)], fill="#6D4C41")
    f.poly([(326, 29), (332, 22), (338, 29)], fill="#FFFFFF")
    f.path("M332,23 q-3,-8 2,-13 q4,-4 0,-9", stroke="#78909C", sw=1.4, opacity=0.8)
    f.poly([(284, 50), (296, 36), (308, 50)], fill="#6D4C41")
    for (x, y) in [(160, 119), (178, 127), (198, 137), (222, 148), (246, 160), (270, 172), (294, 184), (318, 195)]:
        f.circle(x, y - 3, 2.6, fill="#FFEB3B", stroke="#B71C1C", sw=0.9)
    f.arrow(26, 80, 82, 86, INK, 2.2, 9)
    # rótulos
    f.text(6, 66, "OCEANO PACÍFICO", 6.6, 800, "#0D47A1")
    f.text(6, 128, "Placa de Nazca\n(oceânica: fina e densa)", 6.5, 800, "#37474F", lh=1.15)
    f.text(W - 8, 62, "Placa Sul-Americana\n(continental: espessa,\nmenos densa)", 6.5, 800, "#2B1A0E", "end", lh=1.15)
    f.text(W - 8, 2, "Arco vulcânico andino", 6.4, 800, "#B71C1C", "end")
    f.line(W - 112, 8, 346, 24, "#B71C1C", 0.7)
    f.text(250, 6, "Cordilheira dos Andes\n(dobramentos modernos)", 6.8, 800, "#5D3A1A", "end", lh=1.15)
    f.line(254, 22, 290, 40, "#5D3A1A", 0.7)
    f.text(396, 118, "câmara\nmagmática", 6.2, 800, "#B71C1C", "start", lh=1.1)
    f.line(394, 124, 346, 108, "#B71C1C", 0.7)
    f.text(150, 66, "Fossa\nPeru–Chile", 6.4, 800, "#0D47A1", "middle", lh=1.1)
    f.line(150, 90, 150, 110, "#0D47A1", 0.7)
    f.text(396, 150, "Manto\n(astenosfera)", 6.6, 800, "#8A5A2B", "start", lh=1.15)
    f.text(10, 176, "Subducção: a placa oceânica\n(mais densa) afunda sob a\ncontinental e funde em\nprofundidade", 6.6, 800, BLUE, "start", lh=1.15)
    f.arrow(96, 218, 134, 186, BLUE, 0.01, 0.01, opacity=0.0)
    f.circle(14, 244, 3, fill="#FFEB3B", stroke="#B71C1C", sw=0.9)
    f.text(22, 239, "foco de terremoto (mais profundo para a direita)", 6.3, 600, "#37474F")
    f.text(W - 6, H - 12, "esquema fora de escala (relevo e espessuras exagerados)", 5.8, 400, MUTED, "end", italic=True)
    save_svg("lim_andes", f.render())


def _panel(name, label, h=172):
    f = Fig(HALF, h, name, label)
    return f


def lim_divergente():
    f = _panel("lim_divergente", "Limite divergente: dorsal oceânica", 188)
    W = HALF
    f.rect(0, 0, W, 188, fill="#FFFFFF")
    f.rect(0, 60, W, 128, fill=MANTLE)                       # manto (fundo)
    L = [(0, 88), (70, 78), (130, 68), (160, 64), (168, 70), (172, 76)]
    f.rect(0, 30, W, 52, fill=SEA)                            # oceano
    pl = band(L, 26)
    pr = [(W - x, y) for x, y in pl]
    f.poly(pl, fill=LITHO, stroke="#6E7F8C", sw=0.9)
    f.poly(pr, fill=LITHO, stroke="#6E7F8C", sw=0.9)
    f.poly(band(L, 7), fill=CRUST_O)
    f.poly([(W - x, y) for x, y in band(L, 7)], fill=CRUST_O)
    f.poly([(170, 76), (178, 76), (182, 118), (166, 118)], fill=RED)
    f.ellipse(174, 128, 26, 11, fill="#E53935", opacity=0.95)
    f.curve_arrow(174, 170, 174, 152, 174, 140, RED, 2.0, 7)
    f.curve_arrow(156, 134, 126, 136, 96, 146, "#EF6C00", 2.0, 7)
    f.curve_arrow(192, 134, 222, 136, 252, 146, "#EF6C00", 2.0, 7)
    f.arrow(128, 104, 74, 104, "#FFFFFF", 2.4, 9)
    f.arrow(220, 104, 274, 104, "#FFFFFF", 2.4, 9)
    f.text(100, 112, "Placa A", 6.6, 800, "#FFFFFF", "middle")
    f.text(248, 112, "Placa B", 6.6, 800, "#FFFFFF", "middle")
    f.text(W / 2, 3, "DIVERGENTE: placas se afastam", 7.6, 800, BLUE, "middle")
    f.text(8, 38, "mar", 6.2, 700, "#0D47A1", italic=True)
    f.text(W - 8, 34, "Dorsal oceânica (cadeia submarina)", 6.4, 800, "#37474F", "end")
    f.line(W - 80, 46, 178, 70, "#37474F", 0.7)
    f.text(W - 8, 136, "magma sobe, esfria e\nforma nova crosta", 6.4, 800, RED, "end", lh=1.12)
    f.text(W / 2, 174, "Ex.: Dorsal Mesoatlântica (afasta América do Sul e África)", 5.9, 600, "#37474F", "middle")
    save_svg("lim_divergente", f.render())


def lim_transformante():
    f = _panel("lim_transformante", "Limite transformante: falha de deslizamento lateral", 176)
    W = HALF
    f.rect(0, 0, W, 176, fill="#FFFFFF")
    f.text(W / 2, 3, "TRANSFORMANTE: deslizamento lateral", 7.6, 800, "#8A6508", "middle")
    # blocos (vista de cima)
    f.poly([(14, 30), (168, 30), (172, 60), (166, 90), (172, 120), (168, 150), (14, 150)], fill="#E9DEC7", stroke="#8C7A52", sw=0.9)
    f.poly([(180, 30), (334, 30), (334, 150), (176, 150), (180, 120), (174, 90), (180, 60)], fill="#D6E3D0", stroke="#6B8A60", sw=0.9)
    # fratura / zona de falha
    f.path("M174,26 L170,60 L176,90 L170,120 L174,154", stroke="#B71C1C", sw=1.6)
    # rio deslocado
    f.path("M14,74 C 70,66 120,84 169,76", stroke="#1E88E5", sw=3.0)
    f.path("M178,104 C 230,96 280,114 334,106", stroke="#1E88E5", sw=3.0)
    f.path("M169,76 L178,104", stroke="#1E88E5", sw=1.6, dash="3 2")
    f.text(88, 84, "rio (antes da falha)", 6.0, 600, "#0D47A1", "middle", italic=True)
    f.text(256, 86, "mesmo rio, deslocado", 6.0, 600, "#0D47A1", "middle", italic=True)
    # setas
    f.arrow(30, 140, 30, 112, INK, 2.4, 9)
    f.arrow(318, 40, 318, 68, INK, 2.4, 9)
    f.text(44, 128, "Placa do Pacífico\n(rumo NO)", 6.4, 800, "#37474F", lh=1.12)
    f.text(250, 44, "Placa Norte-Americana\n(rumo SE, relativo)", 6.4, 800, "#37474F", "middle", lh=1.12)
    # ondas sísmicas
    for r in (6, 11, 16):
        f.circle(174, 90, r, fill="none", stroke="#E53935", sw=1.0, opacity=0.9 - r / 30)
    f.circle(174, 90, 2.6, fill="#E53935")
    f.text(190, 124, "tensão acumulada\n→ terremoto", 6.2, 800, "#B71C1C", lh=1.12)
    f.text(W / 2, 160, "Sem criação nem destruição de crosta · Ex.: Falha de San Andreas (Califórnia, EUA)", 5.9, 600, "#37474F", "middle")
    f.text(W - 8, 18, "vista de cima (planta)", 5.8, 400, MUTED, "end", italic=True)
    save_svg("lim_transformante", f.render())


def lim_cc():
    f = _panel("lim_cc", "Limite convergente continental–continental: colisão", 176)
    W = HALF
    f.rect(0, 0, W, 176, fill="#FFFFFF")
    f.rect(0, 98, W, 78, fill=MANTLE)
    top = [(0, 74), (80, 74), (118, 62), (150, 40), (174, 20), (198, 38), (230, 60), (268, 72), (W, 74)]
    bot = [(W, 112), (268, 116), (230, 128), (196, 150), (174, 160), (150, 148), (118, 128), (80, 114), (0, 112)]
    f.poly(top + bot, fill=CRUST_C, stroke="#8C6039", sw=0.9)
    f.poly([(164, 28), (174, 20), (184, 30), (174, 34)], fill="#FFFFFF")
    # dobras
    for yoff, amp in [(0, 1.0), (14, 0.8), (28, 0.6)]:
        f.path(f"M10,{86 + yoff} C 60,{86 + yoff} 90,{82 + yoff} 120,{80 - amp * 6 + yoff} S 160,{70 + yoff + amp * 8} 174,{72 + yoff - amp * 14} S 210,{76 + yoff + amp * 6} 250,{82 + yoff} S 310,{86 + yoff} {W - 10},{86 + yoff}",
               stroke="#6D4C41", sw=0.9, opacity=0.75)
    f.arrow(30, 92, 92, 92, INK, 2.4, 9)
    f.arrow(W - 30, 92, W - 92, 92, INK, 2.4, 9)
    f.text(W / 2, 3, "CONVERGENTE continental–continental", 7.6, 800, RED, "middle")
    f.text(12, 56, "Placa Indiana", 6.6, 800, "#5D3A1A")
    f.text(W - 12, 56, "Placa Eurasiática", 6.6, 800, "#5D3A1A", "end")
    f.text(174, 10 + 6, "", 6, 400)
    f.text(W - 8, 12, "Himalaia (dobramento moderno)\nEverest ≈ 8.849 m", 6.4, 800, "#5D3A1A", "end", lh=1.12)
    f.line(214, 30, 188, 26, "#5D3A1A", 0.7)
    f.text(214, 144, "raiz crustal espessa", 6.2, 700, "#5D3A1A")
    f.text(W / 2, 166, "Nenhuma placa afunda (ambas leves): sem vulcanismo relevante; terremotos frequentes", 5.9, 600, "#37474F", "middle")
    save_svg("lim_cc", f.render())


def lim_oo():
    f = _panel("lim_oo", "Limite convergente oceânica–oceânica: arco de ilhas", 188)
    W = HALF
    f.rect(0, 0, W, 188, fill="#FFFFFF")
    f.rect(0, 74, W, 114, fill=MANTLE)
    f.rect(0, 40, W, 50, fill=SEA)
    top_r = [(150, 88), (190, 82), (226, 70), (252, 64), (W, 74)]
    f.poly(band(top_r, 30), fill=LITHO, stroke="#6E7F8C", sw=0.9)
    f.poly(band(top_r, 7), fill=CRUST_O)
    f.poly([(214, 74), (238, 34), (262, 70)], fill="#6D4C41")
    f.poly([(256, 70), (272, 46), (288, 72)], fill="#6D4C41")
    f.ellipse(246, 104, 18, 8, fill="#E53935", opacity=0.92)
    f.path("M246,96 C 246,80 238,60 238,40", stroke="#E53935", sw=1.6)
    slab = [(0, 80), (60, 84), (110, 92), (150, 108), (190, 130), (230, 154), (262, 176)]
    f.poly(band(slab, 20), fill=LITHO, stroke="#6E7F8C", sw=0.9)
    f.poly(band(slab, 6), fill=CRUST_O)
    f.path("M200,144 C 216,130 232,116 244,108", stroke="#E53935", sw=1.6, dash="3 2")
    f.arrow(24, 62, 74, 68, INK, 2.2, 9)
    f.text(W / 2, 3, "CONVERGENTE oceânica–oceânica", 7.6, 800, RED, "middle")
    f.text(8, 46, "mar", 6.2, 700, "#0D47A1", italic=True)
    f.text(8, 134, "Placa mais antiga\ne densa (subduz)", 6.4, 800, "#37474F", lh=1.12)
    f.text(112, 56, "Fossa oceânica", 6.4, 800, "#0D47A1", "middle")
    f.line(120, 64, 146, 100, "#0D47A1", 0.7)
    f.text(W - 6, 16, "Arco de ilhas vulcânicas", 6.4, 800, "#B71C1C", "end")
    f.line(W - 60, 26, 272, 44, "#B71C1C", 0.7)
    f.text(W - 8, 128, "magma sobe\n(fusão da laje\ne do manto)", 6.2, 800, "#B71C1C", "end", lh=1.12)
    f.text(W / 2, 176, "Ex.: Fossa das Marianas (≈ 11 km de profundidade), Aleutas, Antilhas", 5.9, 600, "#37474F", "middle")
    save_svg("lim_oo", f.render())


# ---------------------------------------------------------------------------------
def ciclo_rochas():
    f = Fig(FULL, 308, "ciclo_rochas", "Ciclo das rochas")
    W = FULL
    nodes = {
        "mag": (355, 40, "MAGMA", "rocha fundida (manto e crosta profunda)", "#D84315", 170),
        "ign": (612, 124, "ROCHAS MAGMÁTICAS", "granito (intrusiva, resfriamento lento)\nbasalto (extrusiva, resfriamento rápido)", "#B23C00", 196),
        "sed0": (528, 258, "SEDIMENTOS", "areia, argila, restos orgânicos", "#8D5B2E", 176),
        "sed": (182, 258, "ROCHAS SEDIMENTARES", "arenito, calcário, folhelho", "#6D4C41", 176),
        "met": (98, 124, "ROCHAS METAMÓRFICAS", "gnaisse, mármore, quartzito", "#546E7A", 180),
    }
    bh = 50
    def box(k):
        x, y, n, d, c, w = nodes[k]
        f.rect(x - w / 2, y - bh / 2, w, bh, fill="#FFFFFF", stroke=c, sw=1.8, rx=8)
        f.text(x, y - 15, n, 7.6, 800, c, "middle", lh=1.0)
        f.text(x, y - 3, d, 6.1, 600, "#37474F", "middle", lh=1.12)
    # setas (bordas das caixas)
    def A(x1, y1, cx, cy, x2, y2, c):
        f.curve_arrow(x1, y1, cx, cy, x2, y2, c, 2.4, 9)
    A(440, 40, 560, 36, 600, 96, "#D84315")                      # magma -> magmáticas
    A(606, 150, 584, 198, 566, 232, "#8D5B2E")                   # magmáticas -> sedimentos
    A(440, 258, 355, 300, 270, 258, "#6D4C41")                   # sedimentos -> sedimentares
    A(150, 232, 96, 200, 98, 150, "#546E7A")                     # sedimentares -> metamórficas
    A(98, 98, 120, 40, 268, 40, "#D84315")                       # metamórficas -> magma
    # atalhos tracejados
    f.arrow(512, 138, 198, 138, "#7B1FA2", 1.5, 7, dash="4 3")
    f.curve_arrow(170, 150, 250, 214, 438, 240, "#7B1FA2", 1.5, 7, dash="4 3")
    for k in nodes:
        box(k)
    # rótulos dos processos
    f.text(520, 8, "resfriamento e cristalização", 6.8, 800, "#D84315", "middle")
    f.text(706, 182, "intemperismo, erosão\ne transporte", 6.6, 800, "#8D5B2E", "end", lh=1.12)
    f.text(355, 292, "deposição, compactação e cimentação (litificação)", 6.8, 800, "#6D4C41", "middle")
    f.text(20, 196, "calor e pressão\n(metamorfismo)", 6.6, 800, "#546E7A", "start", lh=1.12)
    f.text(190, 8, "fusão (temperaturas muito altas)", 6.8, 800, "#D84315", "middle")
    # centro
    f.text(355, 78, "CICLO DAS ROCHAS", 11, 800, "#1F2A44", "middle")
    f.text(355, 98, "não há “ponto de partida” nem sequência obrigatória:\nqualquer rocha pode ser erodida, metamorfizada ou fundida", 6.6, 600, MUTED, "middle", lh=1.2, italic=True)
    f.text(355, 146, "atalho: magmática → metamórfica (calor e pressão)", 6.3, 700, "#7B1FA2", "middle")
    f.text(300, 176, "atalho: metamórfica → sedimentos\n(intemperismo e erosão)", 6.3, 700, "#7B1FA2", "middle", lh=1.12)
    save_svg("ciclo_rochas", f.render())


def build():
    camadas_terra()
    conveccao()
    lim_andes()
    lim_divergente()
    lim_transformante()
    lim_cc()
    lim_oo()
    ciclo_rochas()
