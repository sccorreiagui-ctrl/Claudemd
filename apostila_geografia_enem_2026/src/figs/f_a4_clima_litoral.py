"""Módulo A — El Niño/La Niña, climogramas (dados INMET 1991–2020) e dinâmica costeira."""
import json
from svgkit import Fig, FULL, HALF, THIRD, TWO_THIRD, C, INK, MUTED, LINE, wrap
from common import save_svg, PROC

SEA = "#A9D3F0"
SKY = "#EAF4FC"
WARM = "#FF8A65"
COLD = "#64B5F6"


def _cloud(f, x, y, s=1.0, fill="#B0BEC5"):
    f.path(f"M{x},{y} a{14*s},{11*s} 0 0 1 {24*s},{-7*s} a{16*s},{13*s} 0 0 1 {30*s},{4*s} a{10*s},{9*s} 0 0 1 {8*s},{14*s} l{-62*s},0 a{8*s},{7*s} 0 0 1 0,{-10*s} z", fill=fill, stroke="#78909C", sw=1)


def pacifico(name, el_nino):
    W = HALF
    f = Fig(W, 198, name, "El Niño" if el_nino else "Condições normais e La Niña")
    f.rect(0, 0, W, 198, fill="#FFFFFF")
    f.rect(0, 16, W, 60, fill=SKY)
    f.rect(30, 76, 288, 80, fill=COLD)                       # águas frias profundas
    # camada quente (superfície): espessura varia
    if el_nino:
        top = [(30, 76), (318, 76), (318, 112), (200, 108), (110, 98), (30, 92)]
    else:
        top = [(30, 76), (318, 76), (318, 86), (230, 90), (130, 98), (30, 110)]
    f.poly(top, fill=WARM)
    # terra: Ásia/Oceania (esq.) e América do Sul (dir.)
    f.poly([(0, 62), (22, 60), (30, 76), (30, 156), (0, 156)], fill="#C9A77C", stroke="#8C6039", sw=0.9)
    f.poly([(318, 76), (326, 56), (336, 44), (348, 40), (348, 156), (318, 156)], fill="#C9A77C", stroke="#8C6039", sw=0.9)
    f.poly([(326, 56), (336, 44), (348, 40), (348, 56)], fill="#8C6039")
    f.text(15, 108, "Ásia e\nOceania", 5.0, 800, "#FFFFFF", "middle", lh=1.1)
    f.text(333, 108, "América\ndo Sul", 5.0, 800, "#FFFFFF", "middle", lh=1.1)
    f.line(30, 76, 318, 76, "#1E88E5", 1.2)
    f.text(W / 2, 3, "EL NIÑO: Pacífico leste mais quente" if el_nino else "NORMAL / LA NIÑA (normal intensificada)", 7.2, 800, "#C62828" if el_nino else "#0D47A1", "middle")
    # ventos alísios
    if el_nino:
        f.arrow(290, 26, 236, 26, "#546E7A", 1.5, 7)
        f.text(262, 30, "alísios fracos", 5.8, 800, "#546E7A", "middle")
    else:
        f.arrow(300, 28, 176, 28, "#37474F", 3.4, 11)
        f.text(170, 24, "alísios fortes", 5.9, 800, "#37474F", "end")
    # nuvens/chuva e ar ascendente
    cx = 238 if el_nino else 82
    _cloud(f, cx - 30, 54, 0.9)
    f.raindrops(cx - 22, 57, 5, "#1565C0", 8, 9)
    f.arrow(cx + 14, 74, cx + 14, 58, "#E53935", 2.2, 7)
    # lado seco (sol)
    sx = 82 if el_nino else 262
    f.sun(sx, 44, 7)
    f.arrow(sx, 54, sx, 72, "#8C6039", 1.8, 6)
    f.text(sx + 12, 58, "ar desce,\nseco", 5.6, 800, "#8C6039", "start", lh=1.05)
    # ressurgência
    if el_nino:
        f.arrow(300, 140, 300, 114, COLD, 1.4, 6, dash="3 2", opacity=0.9)
        f.text(262, 146, "ressurgência fraca", 5.8, 800, "#FFFFFF", "middle")
    else:
        f.arrow(300, 140, 300, 90, "#0D47A1", 2.6, 8)
        f.text(262, 146, "ressurgência (água fria)", 5.8, 800, "#FFFFFF", "middle")
    # termoclina e rótulos
    if el_nino:
        f.path("M30,92 C 110,98 200,108 318,112", stroke="#FFFFFF", sw=1.0, dash="4 3")
        f.text(96, 84, "água quente espalha-se para leste", 6.0, 800, "#3E2723", "start")
    else:
        f.path("M30,110 C 130,98 230,90 318,86", stroke="#FFFFFF", sw=1.0, dash="4 3")
        f.text(46, 92, "água quente acumulada a oeste", 6.0, 800, "#3E2723", "start")
    f.text(172, 126, "termoclina (limite água quente/fria)", 5.6, 700, "#FFFFFF", "middle")
    # resumo
    if el_nino:
        f.para(8, 162, W - 16, "Chuva desloca-se para o Pacífico central/leste; seca na Indonésia e Austrália; pesca peruana prejudicada.", 6.1, 600, INK, lh=1.2)
    else:
        f.para(8, 162, W - 16, "Chuva forte a oeste (Indonésia e Austrália); costa peruana com águas frias e muito peixe. La Niña = esse padrão ainda mais forte.", 6.1, 600, INK, lh=1.2)
    save_svg(name, f.render())


def climograma(name, st, data):
    T, P = data["T"], data["P"]
    W, H = HALF, 146
    f = Fig(W, H, name, f"Climograma de {st}")
    f.rect(0, 0, W, H, fill="#FFFFFF")
    f.text(4, 1, st, 8.4, 800, "#0D47A1")
    f.text(W - 4, 3, data["clima"], 6.4, 800, "#37474F", "end")
    ptot = f"{data['P_anual']:,.0f}".replace(",", ".")
    f.text(4, 15, f"P anual ≈ {ptot} mm · T média ≈ {str(data['T_media']).replace('.', ',')} °C · amplitude térmica ≈ {str(data['amplitude']).replace('.', ',')} °C", 6.2, 700, INK)
    x0, x1, y0, y1 = 36, W - 34, 38, 132
    wpl = x1 - x0
    # grade e eixos
    for v in (0, 100, 200, 300, 400):
        y = y1 - (y1 - y0) * v / 400
        f.line(x0, y, x1, y, "#DDE3EA" if v else "#37474F", 0.6 if v else 0.9)
        f.text(x0 - 4, y, str(v), 5.8, 600, "#1565C0", "end", valign="mid")
    for v in (0, 10, 20, 30, 40):
        y = y1 - (y1 - y0) * v / 40
        f.text(x1 + 4, y, str(v), 5.8, 600, "#C62828", "start", valign="mid")
    f.text(x0 - 4, y0 - 9, "mm", 5.8, 800, "#1565C0", "end")
    f.text(x1 + 4, y0 - 9, "°C", 5.8, 800, "#C62828", "start")
    slot = wpl / 12
    pts = []
    for i in range(12):
        bx = x0 + i * slot + (slot - 13) / 2
        h = (y1 - y0) * P[i] / 400
        f.rect(bx, y1 - h, 13, h, fill="#42A5F5", stroke="#1565C0", sw=0.5)
        ty = y1 - (y1 - y0) * T[i] / 40
        pts.append((x0 + i * slot + slot / 2, ty))
        f.text(x0 + i * slot + slot / 2, y1 + 3, "JFMAMJJASOND"[i], 6.2, 700, INK, "middle")
    f.poly(pts, stroke="#D32F2F", sw=1.8, close=False)
    for (x, y) in pts:
        f.circle(x, y, 2.2, fill="#D32F2F", stroke="#FFFFFF", sw=0.7)
    save_svg(name, f.render())


def costa_mangue():
    W = THIRD
    f = Fig(W, 196, "costa_mangue", "Manguezal")
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.rect(0, 22, W, 100, fill=SKY)
    f.rect(0, 92, 90, 30, fill="#90CAF9")
    f.rect(70, 108, W - 70, 40, fill="#6D5A45")                        # lodo
    f.poly([(0, 122), (90, 112), (130, 108), (W, 108), (W, 148), (0, 148)], fill="#7B6650")
    f.text(W / 2, 3, "MANGUEZAL", 7.4, 800, "#2E7D32", "middle")
    for (x, h) in [(100, 38), (130, 44), (162, 40), (196, 36)]:
        f.rect(x - 1.5, 108 - h, 3, h, fill="#4E342E")
        f.circle(x, 108 - h - 7, 12, fill="#2E7D32")
        for dx in (-9, -3, 4, 10):
            f.path(f"M{x+dx*0.7},{108-h+2} Q {x+dx*1.6},{108-h/2} {x+dx*2.2},112", stroke="#4E342E", sw=1.1)
    f.text(W / 2, 128, "raízes-escora e respiratórias", 6.0, 800, "#2E7D32", "middle")
    f.text(8, 98, "maré", 6.0, 700, "#0D47A1", italic=True)
    f.text(W / 2, 152, "Foz de rios: água doce + salgada (salobra),\nsolo lodoso e pobre em oxigênio. Berçário de\npeixes e crustáceos; protege a costa (APP).", 5.9, 600, INK, "middle", lh=1.2)
    save_svg("costa_mangue", f.render())


def costa_restinga():
    W = THIRD
    f = Fig(W, 196, "costa_restinga", "Restinga, duna e lagoa")
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.rect(0, 22, W, 100, fill=SKY)
    f.rect(0, 100, 62, 22, fill="#64B5F6")
    f.poly([(62, 122), (62, 100), (78, 96), (96, 70), (122, 62), (148, 84), (160, 98), (W, 100), (W, 122)], fill="#F2D49B", stroke="#C9A25B", sw=0.8)
    f.rect(160, 100, W - 160, 22, fill="#4DB6AC")
    for xx in (70, 84, 168, 184, 200):
        f.path(f"M{xx},100 q-2,-6 -5,-8 M{xx},100 q2,-7 4,-9", stroke="#6A9A3A", sw=1.2)
    f.text(W / 2, 3, "RESTINGA · DUNA · LAGOA", 7.0, 800, "#8A6508", "middle")
    f.text(30, 84, "mar", 6.0, 700, "#0D47A1", italic=True)
    f.text(124, 40, "duna (areia móvel)", 5.9, 800, "#8A6508", "middle", halo="#EAF4FC")
    f.text(194, 104, "lagoa costeira", 5.6, 800, "#FFFFFF", "middle")
    f.text(110, 126, "restinga: vegetação baixa", 5.8, 800, "#4F6D2A", "middle")
    f.text(W / 2, 150, "Cordão arenoso (restinga) isola lagoas; ventos\nmovimentam dunas; vegetação fixa a areia.\nAmbientes frágeis (ocupação e mineração).", 5.9, 600, INK, "middle", lh=1.2)
    save_svg("costa_restinga", f.render())


def costa_falesia():
    W = THIRD
    f = Fig(W, 196, "costa_falesia", "Falésia, praia e recife")
    f.rect(0, 0, W, 196, fill="#FFFFFF")
    f.rect(0, 22, W, 100, fill=SKY)
    f.rect(0, 100, 130, 22, fill="#64B5F6")
    f.poly([(130, 122), (130, 100), (136, 40), (W, 40), (W, 122)], fill="#C8714A", stroke="#8C4A2A", sw=0.8)
    for yy in (56, 72, 88):
        f.path(f"M136,{yy} L{W},{yy+2}", stroke="#E7A57F", sw=3.0, opacity=0.9)
    f.poly([(100, 122), (130, 108), (138, 122)], fill="#F2D49B")
    f.path("M120,102 q6,-8 14,-4", stroke="#FFFFFF", sw=2.0)
    f.path("M126,106 q-4,0 -6,4", stroke="#8C4A2A", sw=1.4)
    f.poly([(40, 100), (52, 96), (60, 100)], fill="#8D6E63")
    f.text(W / 2, 3, "FALÉSIA E PRAIA", 7.2, 800, "#8C4A2A", "middle")
    f.text(W - 6, 24, "falésia: escarpa\nrecuada pela abrasão", 5.8, 800, "#FFFFFF", "end", lh=1.1)
    f.text(50, 84, "ondas", 6.0, 700, "#0D47A1", italic=True)
    f.arrow(80, 92, 118, 100, "#1E88E5", 1.8, 6)
    f.text(100, 128, "praia", 5.9, 800, "#8A6508", "middle")
    f.text(W / 2, 150, "Ondas erodem o sopé (abrasão); a falésia recua e\ndeixa plataforma de abrasão. Recifes e arenitos\nde praia protegem trechos da costa nordestina.", 5.9, 600, INK, "middle", lh=1.2)
    save_svg("costa_falesia", f.render())


def build():
    pacifico("pacifico_normal", False)
    pacifico("pacifico_elnino", True)
    d = json.load(open(PROC / "climogramas_inmet_1991_2020.json"))["estacoes"]
    for key, nm in [("Manaus (AM)", "clim_manaus"), ("Brasília (DF)", "clim_brasilia"), ("Petrolina (PE)", "clim_petrolina"), ("Porto Alegre (RS)", "clim_portoalegre")]:
        climograma(nm, key, d[key])
    costa_mangue(); costa_restinga(); costa_falesia()
