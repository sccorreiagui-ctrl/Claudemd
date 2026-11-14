"""Módulo G — diagramas de Cartografia: escala (mesma folha, áreas reais diferentes) e GNSS · sensoriamento remoto · SIG."""
import math
from svgkit import Fig, FULL, HALF, INK, MUTED
from common import save_svg

AC = "#37474F"


def escala():
    H = 166
    f = Fig(FULL, H, "escala_exemplo", "Escala: mesma folha, áreas reais diferentes")
    W = FULL
    pw, gap = 226, 16
    ttl = [("ESCALA GRANDE", "1 : 10.000", "1 cm = 100 m", "folha de 6 cm → 600 m", "#2E7D32"),
           ("ESCALA MÉDIA", "1 : 100.000", "1 cm = 1 km", "folha de 6 cm → 6 km", "#1565C0"),
           ("ESCALA PEQUENA", "1 : 1.000.000", "1 cm = 10 km", "folha de 6 cm → 60 km", "#7B3FA0")]
    for i, (a, e, r, area, c) in enumerate(ttl):
        x = i * (pw + gap)
        f.rect(x, 0, pw, 22, fill=c, rx=5)
        f.text(x + 8, 11, a, 6.6, 800, "#FFFFFF", valign="mid")
        f.text(x + pw - 8, 11, e, 8.4, 800, "#FFFFFF", "end", valign="mid")
        f.rect(x, 26, pw, 100, fill="#FAF8F2", stroke="#C9D0DB", sw=1, rx=4)
        # desenho esquemático
        if i == 0:
            for sx in (x + 40, x + 150):
                f.rect(sx - 14, 26, 28, 100, fill="#E0E0E0")
            f.rect(x, 62, pw, 22, fill="#E0E0E0")
            for r_ in range(2):
                for k in range(7):
                    bx = x + 12 + k * 29
                    by = 34 + r_ * 54 if r_ == 0 else 92
                    f.rect(bx, 32 if r_ == 0 else 92, 20, 14, fill="#C9A98A", stroke="#8D5B2E", sw=0.6)
            f.rect(x + 80, 88, 40, 32, fill="#C6E0B4", stroke="#2E7D32", sw=0.6)
            f.text(x + 100, 104, "praça", 5.6, 700, "#1B5E20", "middle", valign="mid")
        elif i == 1:
            f.line(x, 78, x + pw, 78, "#9E9E9E", 3.5); f.line(x + 80, 26, x + 80, 126, "#BDBDBD", 2.4); f.line(x + 170, 26, x + 170, 126, "#BDBDBD", 2.4)
            f.path(f"M{x},44 C{x+70},60 {x+130},40 {x+pw},64", stroke="#1565C0", sw=2.4)
            for bx, by, bw, bh in [(8, 32, 64, 38), (90, 30, 72, 28), (176, 34, 42, 36), (8, 88, 64, 32), (90, 90, 72, 30), (176, 90, 42, 30)]:
                f.rect(x + bx, by, bw, bh, fill="#E6D6C4", stroke="#B79A7E", sw=0.6)
            f.text(x + 14, 118, "bairros e avenidas", 5.6, 700, "#5D3A1A")
        else:
            f.path(f"M{x},50 C{x+60},64 {x+150},40 {x+pw},70", stroke="#1565C0", sw=1.4)
            f.poly([(x + 88, 64), (x + 124, 52), (x + 150, 70), (x + 140, 98), (x + 100, 102), (x + 84, 84)], fill="#BCAAA4", stroke="#6D4C41", sw=0.8)
            f.line(x, 112, x + 88, 80, "#9E9E9E", 2); f.line(x + 150, 70, x + pw, 40, "#9E9E9E", 2); f.line(x + 124, 52, x + 124, 26, "#9E9E9E", 2)
            for dx, dy in [(30, 36), (190, 98), (40, 108), (200, 52)]:
                f.circle(x + dx, dy, 3, fill="#6D4C41")
            f.text(x + 112, 78, "cidade (ponto/mancha)", 5.4, 800, "#3E2723", "middle", valign="mid")
            f.text(x + 196, 116, "rodovias", 5.4, 700, "#5B6475")
        # legenda abaixo
        f.text(x + pw / 2, 130, r, 7.2, 800, c, "middle")
        f.text(x + pw / 2, 141, area, 6.2, 600, INK, "middle")
        f.text(x + pw / 2, 151, ["mais detalhes, menor área", "detalhe intermediário", "menos detalhes, maior área"][i], 6.0, 600, MUTED, "middle")
    f.text(W / 2, 160, "Escala = distância no mapa (d) ÷ distância real (D) · quanto MENOR o denominador, MAIOR a escala", 6.8, 800, AC, "middle")
    save_svg("escala_exemplo", f.render())


def sig():
    H = 178
    f = Fig(FULL, H, "sig_sensoriamento", "GNSS, sensoriamento remoto e SIG")
    W = FULL
    pw, gap = 226, 16
    heads = [("1 · GNSS / GPS", "posição na Terra", "#1565C0"), ("2 · SENSORIAMENTO REMOTO", "dados à distância", "#2E7D32"), ("3 · SIG (GIS)", "camadas e análise", "#E65100")]
    for i, (t, s, c) in enumerate(heads):
        x = i * (pw + gap)
        f.rect(x, 0, pw, 22, fill=c, rx=5)
        f.text(x + 8, 11, t, 6.8, 800, "#FFFFFF", valign="mid")
        f.text(x + pw - 8, 11, s, 6.0, 600, "#FFFFFF", "end", valign="mid")
        f.rect(x, 26, pw, 104, fill="#F7FAFD" if i == 0 else ("#F6FBF6" if i == 1 else "#FFF8F2"), stroke="#D5DBE4", sw=0.8, rx=4)
    # --- 1 GNSS
    x = 0
    f.path(f"M{x+10},130 Q{x+113},84 {x+216},130", stroke="#5B6475", sw=1.2)
    f.rect(x + 11, 118, 204, 12, fill="#CFE3C0", rx=0)
    sats = [(x + 40, 44), (x + 100, 36), (x + 160, 46), (x + 196, 70)]
    rx, ry = x + 113, 104
    f.circle(rx, ry, 4, fill="#C62828"); f.rect(rx - 3, ry - 1, 6, 8, fill="#C62828")
    for sx, sy in sats:
        f.rect(sx - 6, sy - 3, 12, 6, fill="#1565C0", rx=1); f.rect(sx - 14, sy - 1.5, 7, 3, fill="#90CAF9"); f.rect(sx + 7, sy - 1.5, 7, 3, fill="#90CAF9")
        f.line(sx, sy + 3, rx, ry - 4, "#1565C0", 0.9, dash="3 2")
    f.text(rx, 112, "receptor", 5.8, 800, "#B71C1C", "middle")
    f.para(x + 8, 134, pw - 16, "O receptor mede o tempo de viagem do sinal de **≥ 4 satélites** e calcula latitude, longitude e altitude. Sistemas: GPS (EUA), GLONASS (Rússia), Galileo (UE), BeiDou (China).", 6.0, 500, INK, lh=1.2)
    # --- 2 Sensoriamento remoto
    x = pw + gap
    f.circle(x + 190, 44, 9, fill="#FFD54F", stroke="#F9A825", sw=1)
    for a in range(0, 360, 45):
        f.line(x + 190 + 12 * math.cos(math.radians(a)), 44 + 12 * math.sin(math.radians(a)), x + 190 + 17 * math.cos(math.radians(a)), 44 + 17 * math.sin(math.radians(a)), "#F9A825", 1)
    sx, sy = x + 80, 40
    f.rect(sx - 7, sy - 4, 14, 8, fill="#2E7D32", rx=1); f.rect(sx - 20, sy - 2, 11, 4, fill="#A5D6A7"); f.rect(sx + 9, sy - 2, 11, 4, fill="#A5D6A7")
    f.poly([(sx - 6, sy + 5), (sx + 6, sy + 5), (x + 150, 118), (x + 30, 118)], fill="#C8E6C9", opacity=0.45)
    f.line(x + 182, 54, x + 120, 108, "#F9A825", 1.2, dash="3 2"); f.arrow(x + 120, 108, x + 92, 50, "#F9A825", 1.2, 5)
    f.arrow(sx + 12, 48, x + 44, 112, "#C62828", 1.4, 6); f.line(x + 52, 112, sx + 6, 52, "#C62828", 1.0, dash="2 2")
    f.rect(x + 12, 118, 204, 10, fill="#D7CCC8")
    f.tree(x + 44, 118, 0.8)
    f.rect(x + 100, 119, 36, 8, fill="#90CAF9"); f.rect(x + 160, 112, 14, 16, fill="#90A4AE"); f.rect(x + 177, 108, 12, 20, fill="#78909C")
    f.text(x + 150, 62, "sensor passivo:\nluz solar refletida", 5.6, 700, "#B26A00", lh=1.1)
    f.text(x + 14, 60, "sensor ativo\n(radar): emite e\nrecebe o sinal", 5.6, 700, "#8E1B1B", lh=1.1)
    f.para(x + 8, 134, pw - 16, "Cada alvo (vegetação, água, solo, cidade) reflete a energia de um modo. **Resolução espacial:** menor objeto distinguível; **temporal:** intervalo entre passagens. O radar atravessa nuvens.", 6.0, 500, INK, lh=1.2)
    # --- 3 SIG
    x = 2 * (pw + gap)
    layers = [("população", "#CE93D8", 108), ("uso do solo", "#A5D6A7", 90), ("hidrografia", "#90CAF9", 72), ("relevo", "#D7B98E", 54)]
    for nm, c, yy in layers:
        f.poly([(x + 40, yy + 14), (x + 150, yy + 14), (x + 190, yy - 4), (x + 80, yy - 4)], fill=c, stroke="#5B6475", sw=0.8, opacity=0.9)
        f.text(x + 168, yy + 6, nm, 5.8, 800, "#37474F", "start")
    f.text(x + 10, 36, "camadas georreferenciadas\nsobrepostas (overlay)", 5.8, 700, "#B23C00", lh=1.1)
    f.arrow(x + 112, 50, x + 112, 62, "#B23C00", 1.4, 5)
    f.para(x + 8, 134, pw - 16, "O SIG integra bancos de dados e mapas em camadas e permite **cruzar variáveis** (ex.: declividade × chuva × ocupação = áreas de risco). Usos: planejamento urbano, agricultura de precisão, gestão ambiental.", 6.0, 500, INK, lh=1.2)
    save_svg("sig_sensoriamento", f.render())


def build():
    escala()
    sig()
