"""Módulo B — seis desenhos esquemáticos de vegetação (adaptações ao clima, solo e água)."""
import math, random
from svgkit import Fig, THIRD, HALF, C, INK, MUTED
from common import save_svg

SKY = "#EAF4FC"
W, H = THIRD, 200


def base(name, label, ground="#8D6E4A", sky=SKY, gh=44, title="", tcol="#2E7D32"):
    f = Fig(W, H, name, label)
    f.rect(0, 0, W, H, fill="#FFFFFF")
    f.rect(0, 18, W, 132, fill=sky)
    f.rect(0, 150 - gh + 44, W, gh, fill=ground) if False else None
    f.rect(0, 118, W, 32, fill=ground)
    f.text(W / 2, 2, title, 7.4, 800, tcol, "middle")
    return f


def amazonia():
    f = base("veg_amazonia", "Floresta amazônica", "#6B4A2E", "#DDF0E3", title="FLORESTA AMAZÔNICA")
    f.rect(0, 118, W, 5, fill="#3B2716")
    rnd = random.Random(4)
    # estratos: emergentes, dossel, sub-bosque
    for x in (36, 120, 190):
        f.rect(x - 2, 38, 4, 82, fill="#4E342E")
        f.ellipse(x, 36, 26, 11, fill="#2E7D32")
    for x in range(14, 220, 26):
        f.rect(x - 1.5, 62, 3, 58, fill="#5D4037")
        f.ellipse(x, 62, 17, 9, fill="#43A047")
    for x in range(20, 220, 30):
        f.ellipse(x, 100, 11, 8, fill="#66BB6A")
        f.line(x, 100, x, 118, "#5D4037", 1.2)
    # lianas, epífitas, sapopemas
    f.path("M62,66 q-6,24 2,46", stroke="#2E5E1F", sw=1.0)
    f.path("M148,64 q8,22 -2,48", stroke="#2E5E1F", sw=1.0)
    f.poly([(116, 118), (120, 100), (124, 118)], fill="#4E342E")
    f.poly([(106, 118), (118, 96), (120, 118)], fill="#4E342E", opacity=0.0)
    f.text(120, 24, "emergentes (30–50 m)", 5.9, 800, "#1B5E20", "middle", halo="#FFFFFF")
    f.text(8, 82, "dossel", 5.9, 800, "#1B5E20", halo="#FFFFFF")
    f.text(8, 106, "sub-bosque", 5.9, 800, "#1B5E20", halo="#FFFFFF")
    f.raindrops(150, 38, 3, "#1565C0", 7, 8)
    f.text(W / 2, 126, "serapilheira (ciclagem rápida)", 5.9, 800, "#FFFFFF", "middle")
    f.para(6, 154, W - 12, "Floresta ombrófila densa: perene, latifoliada, muito úmida (chuva todo ano, ≈ 2.000–3.000 mm). Estratos, epífitas e raízes tabulares. Solo pobre: a floresta vive da matéria orgânica.", 5.9, 600, INK, lh=1.18)
    save_svg("veg_amazonia", f.render())


def cerrado():
    f = base("veg_cerrado", "Cerrado", "#B5651D", "#FFF8E1", title="CERRADO", tcol="#8A6508")
    f.rect(0, 118, W, 32, fill="#A0561B")
    f.sun(196, 38, 9)
    # gramíneas
    for x in range(6, 224, 7):
        f.path(f"M{x},118 q-2,-9 -4,-12 M{x},118 q2,-10 4,-13", stroke="#C0B24A", sw=1.2)
    # árvores tortuosas
    def twisted(x, h):
        f.path(f"M{x},118 C {x-6},{118-h*0.35} {x+8},{118-h*0.6} {x-2},{118-h}", stroke="#5D4037", sw=3.0)
        f.path(f"M{x-2},{118-h} q-14,-6 -18,-14 M{x-2},{118-h} q10,-6 16,-16 M{x+3},{118-h*0.62} q12,-4 16,-12", stroke="#5D4037", sw=1.8)
        for dx, dy in [(-20, -22), (-14, -28), (14, -28), (18, -20), (0, -34)]:
            f.ellipse(x - 2 + dx * 0.9, 118 - h + dy * 0.6, 9, 4.5, fill="#7C9A3C")
    twisted(56, 40); twisted(120, 48); twisted(176, 36)
    # raízes profundas até o lençol freático
    for x, d in [(56, 28), (120, 34), (176, 26)]:
        f.path(f"M{x},118 C {x-10},{118+d*0.5} {x+8},{118+d*0.9} {x},{118+d}", stroke="#4E342E", sw=1.3)
    f.rect(0, 150, W, 0.1, fill="#FFFFFF")
    f.text(10, 140, "raízes profundas", 5.9, 800, "#FFFFFF")
    f.path("M0,147 q60,-4 114,0 t112,0", stroke="#64B5F6", sw=1.6, dash="4 2")
    f.text(222, 146, "lençol freático", 5.6, 800, "#E3F2FD", "end")
    f.text(60, 70, "casca grossa\n(resiste ao fogo)", 5.6, 800, "#5D4037", "middle", lh=1.1, halo="#FFFFFF")
    f.text(158, 74, "troncos retorcidos,\nfolhas coriáceas", 5.6, 800, "#5D4037", "middle", lh=1.1, halo="#FFFFFF")
    f.para(6, 154, W - 12, "Savana brasileira: duas estações (verão chuvoso, inverno seco). Solos antigos, ácidos e ricos em Al e Fe. Adaptações: raízes profundas, cascas grossas, folhas coriáceas e rebrota após o fogo.", 5.9, 600, INK, lh=1.18)
    save_svg("veg_cerrado", f.render())


def caatinga():
    f = base("veg_caatinga", "Caatinga", "#C9A06A", "#FFF3E0", title="CAATINGA", tcol="#B23C00")
    f.rect(0, 118, W, 32, fill="#BF925A")
    f.sun(190, 40, 10, "#FB8C00")
    # solo rachado
    for (a, b, c_, d) in [(10, 124, 30, 136), (50, 130, 70, 142), (100, 124, 124, 138), (150, 132, 170, 144), (196, 124, 214, 138)]:
        f.path(f"M{a},{b} l{(c_-a)/2},{(d-b)/2+3} l{(c_-a)/2},{(d-b)/2-3}", stroke="#7A5530", sw=1.0)
    # mandacaru
    def cactus(x, h):
        f.rect(x - 4, 118 - h, 8, h, fill="#558B2F", stroke="#33691E", sw=0.8, rx=4)
        f.path(f"M{x-4},{118-h*0.45} h-9 v-{h*0.35} ", stroke="#558B2F", sw=7, cap="round")
        f.path(f"M{x+4},{118-h*0.6} h9 v-{h*0.3} ", stroke="#558B2F", sw=7, cap="round")
    cactus(52, 50); cactus(168, 42)
    # arbustos sem folhas (caducifólias) espinhosos
    for x in (98, 126, 20, 206):
        f.path(f"M{x},118 l0,-22 m0,8 l-9,-10 m9,4 l9,-12 m-9,2 l-5,-8", stroke="#6D4C41", sw=1.5)
    f.text(70, 56, "cactos: armazenam\nágua (caule suculento)", 5.7, 800, "#33691E", "middle", lh=1.1, halo="#FFFFFF")
    f.text(160, 80, "folhas viram espinhos", 5.7, 800, "#33691E", "middle", halo="#FFFFFF")
    f.text(110, 86, "perdem as folhas\nna seca (caducifólia)", 5.7, 800, "#6D4C41", "middle", lh=1.1, halo="#FFFFFF")
    f.para(6, 154, W - 12, "Vegetação xerófila do semiárido: chuvas escassas e irregulares, alta evaporação. Adaptações: espinhos, caules suculentos, raízes extensas e queda das folhas (mata “branca” na seca). Rios intermitentes.", 5.9, 600, INK, lh=1.18)
    save_svg("veg_caatinga", f.render())


def mata_atlantica():
    f = base("veg_mataatl", "Mata Atlântica", "#6B4A2E", "#E3F2E9", title="MATA ATLÂNTICA", tcol="#2E7D32")
    # morros arredondados ("meias-laranjas")
    f.path("M0,118 C 20,70 60,66 84,100 C 100,60 150,56 176,98 C 190,76 214,80 227,100 L227,118 Z", fill="#7CB66B", stroke="#4E8F45", sw=0.8)
    f.path("M0,118 C 24,92 52,92 70,112 C 100,84 140,86 160,112 C 184,96 210,98 227,112 L227,118 Z", fill="#3F8F4A", opacity=0.9)
    # nuvem/neblina (chuva orográfica)
    f.path("M10,52 q8,-8 18,-2 q10,-10 22,0 q10,-6 16,4 l-60,0 z", fill="#FFFFFF", stroke="#B0BEC5", sw=0.8)
    f.path("M120,40 q8,-8 18,-2 q10,-10 22,0 q10,-6 16,4 l-60,0 z", fill="#FFFFFF", stroke="#B0BEC5", sw=0.8)
    f.raindrops(130, 52, 4, "#1565C0", 7, 8)
    # árvores com epífitas
    for x, h in [(40, 40), (104, 46), (160, 40), (206, 36)]:
        f.rect(x - 2, 118 - h, 4, h, fill="#5D4037")
        f.circle(x, 118 - h - 6, 13, fill="#2E7D32")
        f.circle(x - 6, 118 - h * 0.55, 3.2, fill="#E53935")      # bromélia
        f.path(f"M{x-6},{118-h*0.55} l-3,-4 m3,4 l3,-4 m-3,4 l0,-5", stroke="#2E7D32", sw=1.1)
    f.text(58, 22, "relevo de “mares de morros”", 5.9, 800, "#1B5E20", "start", halo="#FFFFFF")
    f.text(76, 78, "epífitas e bromélias", 5.7, 800, "#B71C1C", "start", halo="#FFFFFF")
    f.rect(0, 118, W, 32, fill="#6B4A2E")
    f.text(W / 2, 134, "restam ≈ 12,4% (florestas maduras)", 6.0, 800, "#FFFFFF", "middle")
    f.para(6, 154, W - 12, "Floresta ombrófila densa litorânea: chuva orográfica nas serras, alta umidade e imensa biodiversidade. Bioma mais devastado (café, cana, urbanização); encostas íngremes → deslizamentos.", 5.9, 600, INK, lh=1.18)
    save_svg("veg_mataatl", f.render())


def araucarias():
    f = base("veg_araucaria", "Floresta de araucárias", "#6B4A2E", "#E8EEF8", title="FLORESTA DE ARAUCÁRIAS", tcol="#1B6B4A")
    f.rect(0, 118, W, 32, fill="#7A4B2B")
    def arauc(x, h, s=1.0):
        f.rect(x - 2.5 * s, 118 - h, 5 * s, h, fill="#4E342E")
        # copa em candelabro (galhos que sobem formando taça)
        top = 118 - h
        for dx in (-20, -10, 0, 10, 20):
            f.path(f"M{x},{top+8*s} Q {x+dx*0.6*s},{top-2*s} {x+dx*s},{top-10*s}", stroke="#1B5E20", sw=2.2 * s)
            f.ellipse(x + dx * s, top - 10 * s, 7 * s, 3.2 * s, fill="#2E7D32")
    arauc(52, 78); arauc(128, 90, 1.1); arauc(194, 70, 0.9)
    # sub-bosque (erva-mate / imbuia)
    for x in (20, 88, 160, 214):
        f.circle(x, 108, 10, fill="#66BB6A")
        f.rect(x - 1, 108, 2, 10, fill="#5D4037")
    f.text(128, 22, "pinheiro-do-paraná (copa em candelabro)", 5.8, 800, "#1B6B4A", "middle", halo="#FFFFFF")
    # geada
    for (x, y) in [(20, 40), (196, 30), (30, 62)]:
        f.path(f"M{x-4},{y} h8 M{x},{y-4} v8 M{x-3},{y-3} l6,6 M{x-3},{y+3} l6,-6", stroke="#5C6BC0", sw=0.9)
    f.text(46, 40, "geadas e inverno frio", 5.7, 800, "#3949AB", "start", halo="#FFFFFF")
    f.text(W / 2, 134, "Planalto Meridional (solos de basalto)", 6.0, 800, "#FFFFFF", "middle")
    f.para(6, 154, W - 12, "Floresta ombrófila mista: coníferas + folhosas, clima subtropical com 4 estações. Muito explorada pela madeira e substituída por pinus, soja e pastagens; hoje, ameaçada de extinção.", 5.9, 600, INK, lh=1.18)
    save_svg("veg_araucaria", f.render())


def pampa():
    f = base("veg_pampa", "Campos do Pampa", "#7CA64A", "#E9F3FB", title="CAMPOS DO PAMPA (PRADARIAS)", tcol="#4F7A1F")
    f.path("M0,118 C 40,92 90,96 120,108 C 150,90 200,92 227,104 L227,150 L0,150 Z", fill="#9CCB5A", stroke="#6E9A33", sw=0.8)
    f.path("M0,126 C 50,108 100,114 140,120 C 170,110 200,112 227,118 L227,150 L0,150 Z", fill="#8DBD4C")
    for x in range(8, 224, 9):
        f.path(f"M{x},{120 + (x % 5)} q-1,-6 -3,-8 M{x},{120 + (x % 5)} q1,-7 3,-9", stroke="#4F7A1F", sw=1.0)
    # árvore isolada e gado
    f.tree(160, 108, 0.9)
    def cow(x, y):
        f.rect(x - 7, y - 7, 14, 7, fill="#FFFFFF", stroke="#455A64", sw=0.8, rx=2)
        f.rect(x - 7, y - 7, 5, 5, fill="#37474F", rx=1)
        f.rect(x + 7, y - 9, 4, 4, fill="#FFFFFF", stroke="#455A64", sw=0.7)
        for dx in (-5, -1, 3, 6):
            f.line(x + dx, y, x + dx, y + 4, "#455A64", 1.0)
    cow(60, 112); cow(86, 118); cow(34, 120)
    f.text(120, 74, "coxilhas (colinas suaves)", 5.9, 800, "#4F7A1F", "middle", halo="#FFFFFF")
    f.text(W / 2, 140, "gramíneas · pecuária extensiva", 6.0, 800, "#FFFFFF", "middle")
    f.rect(0, 150, W, 0.1, fill="#FFFFFF")
    f.para(6, 154, W - 12, "Clima subtropical úmido (chuvas bem distribuídas e invernos frios). Campos naturais (pasto). Pisoteio e monocultura expõem areias → arenização (clima úmido, ≠ desertificação).", 5.9, 600, INK, lh=1.18)
    save_svg("veg_pampa", f.render())


def build():
    amazonia(); cerrado(); caatinga(); mata_atlantica(); araucarias(); pampa()
