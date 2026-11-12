"""Capítulo 1 – Matemática básica, proporcionalidade, porcentagem e finanças (tópicos 1, 2, 3, 4, 40)."""
import math
from lib import *
from svg import Fig, Plot, box3d, fmt

LABEL = 'CAP. 1 · MATEMÁTICA BÁSICA, PROPORCIONALIDADE E FINANÇAS'


# =====================================================================  FIGURAS
def fig_regra3():
    d = Plot(160, 140, 0, 4.4, 0, 7.4, l=26, r=8, t=18, b=22)
    d.grid(1, 2)
    d.axes(xlab='litros', ylab='R$', xticks=(1, 2, 3), yticks=(2, 4, 6), size=9)
    d.poly([(d.X(0), d.Y(0)), (d.X(3.7), d.Y(7.4))], stroke='blue', sw=2.6, close=False)
    for x in (1, 2, 3):
        d.pt(x, 2 * x, 'blue')
    d.text(80, 11, 'DIRETA', size=10.5, col='blue', bold=True)
    i = Plot(160, 140, 0, 7.4, 0, 7.4, l=26, r=8, t=18, b=22)
    i.grid(1, 2)
    i.axes(xlab='operários', ylab='dias', xticks=(1, 2, 3, 6), yticks=(2, 4, 6), size=9)
    i.curve(lambda x: 6 / x, 0.82, 7.2, col='purple', w=2.6, ylim=(0, 7.4))
    for x in (1, 2, 3, 6):
        i.pt(x, 6 / x, 'purple')
    i.text(80, 11, 'INVERSA', size=10.5, col='purple', bold=True)
    f = Fig(330, 140)
    f.group(d, 0, 0).group(i, 170, 0)
    return f.svg()


def fig_escala():
    f = Fig(342, 124)
    # --- mapa e régua (escala 1:50 000)
    f.rect(2, 4, 160, 70, fill='lgreen', stroke='mgreen', sw=1, rx=5)
    f.path('M12,56 C40,56 38,24 70,30 C102,36 110,60 148,22', stroke='mgrey', sw=5, op=.9)
    f.path('M12,56 C40,56 38,24 70,30 C102,36 110,60 148,22', stroke='white', sw=2, dash='5 4')
    f.circ(14, 56, 5, fill='blue', stroke='white', sw=1.5); f.circ(148, 23, 5, fill='blue', stroke='white', sw=1.5)
    f.label(28, 70, 'A', size=10.5, col='navy', bold=True); f.label(148, 16, 'B', size=10.5, col='navy', bold=True)
    f.rect(2, 84, 160, 12, fill='white', stroke='navy', sw=1.2)
    for k in range(5):
        f.line(2 + k * 40, 84, 2 + k * 40, 96, col='navy', w=1.2)
        f.text(2 + k * 40, 109, str(k), size=9.5, col='navy')
    f.line(2, 90, 162, 90, col='orange', w=3)
    f.text(82, 121, '4 cm no mapa', size=9.5, col='orange', bold=True)
    # --- quadrados e cubos (razão de semelhança k = 2)
    def sq(x, y, s, n):
        f.rect(x, y, s, s, fill='lblue', stroke='navy', sw=1.4)
        for k in range(1, n):
            f.line(x + k * s / n, y, x + k * s / n, y + s, col='navy', w=.9)
            f.line(x, y + k * s / n, x + s, y + k * s / n, col='navy', w=.9)
    f.text(262, 12, 'comprimento ×2', size=10.5, col='navy', bold=True)
    base = 70
    sq(184, base - 16, 16, 1); sq(212, base - 32, 32, 2)
    f.text(214, 90, 'área ×4 (2²)', size=10, col='purple', bold=True)
    s1, s2, dx1, dx2 = 14, 28, 6, 12
    box3d(f, 274, base - s1, s1, s1, dx1, dx1 * .7, fill='lpurple')
    x, y, s, dx, dy = 296, base - s2, s2, dx2, dx2 * .7
    box3d(f, x, y, s, s, dx, dy, fill='lpurple', hidden=False)
    for a in ((x + s / 2, y, x + s / 2, y + s), (x, y + s / 2, x + s, y + s / 2), (x + s / 2, y, x + s / 2 + dx, y - dy),
              (x + dx / 2, y - dy / 2, x + s + dx / 2, y - dy / 2), (x + s, y + s / 2, x + s + dx, y + s / 2 - dy),
              (x + s + dx / 2, y - dy / 2, x + s + dx / 2, y + s - dy / 2)):
        f.line(*a, w=.9, col='purple')
    f.text(300, 90, 'volume ×8 (2³)', size=10, col='purple', bold=True)
    f.text(262, 108, '', size=1)
    return f.svg()


def fig_tanque():
    f = Fig(250, 150)
    f.rect(70, 40, 120, 90, fill='white', stroke='navy', sw=2.4)
    f.rect(72, 72, 116, 56, fill='lblue')
    f.line(72, 72, 188, 72, col='blue', w=1.4, dash='4 3')
    f.text(130, 108, 'V (m³ ou L)', size=11, col='navy', bold=True)
    # entradas
    f.line(100, 4, 100, 40, col='green', w=3.2, arrow=True); f.line(160, 4, 160, 40, col='green', w=3.2, arrow=True)
    f.label(88, 16, '*Q*_1', size=10.5, col='green', anchor='end', bold=True); f.label(172, 16, '*Q*_2', size=10.5, col='green', anchor='start', bold=True)
    # saída
    f.line(190, 120, 238, 120, col='orange', w=3.2, arrow=True)
    f.label(214, 112, '*Q*_3', size=10.5, col='orange', bold=True)
    f.text(130, 146, '*Q*_líq = *Q*_1 + *Q*_2 − *Q*_3', size=10.5, col='navy', bold=True)
    return f.svg()


def fig_mmc():
    f = Fig(342, 124)
    # régua dos múltiplos de 4 e 6 (0..36)
    x0, sc = 12, 8.8
    f.text(6, 12, 'Múltiplos de 4 e de 6 até 36 → o primeiro encontro (≠0) é o MMC', size=10, col='navy', bold=True, anchor='start')
    f.line(x0, 40, x0 + 36 * sc, 40, col='mblue', w=1.6); f.line(x0, 68, x0 + 36 * sc, 68, col='mpurple', w=1.6)
    for m in range(0, 37, 4):
        f.circ(x0 + m * sc, 40, 3.6, fill='blue')
    for m in range(0, 37, 6):
        f.circ(x0 + m * sc, 68, 3.6, fill='purple')
    for m in (12, 24, 36):
        f.line(x0 + m * sc, 34, x0 + m * sc, 74, col='green', w=2, dash='3 3')
        f.text(x0 + m * sc, 88, str(m), size=10.5, col='green', bold=True)
    f.text(6, 36, '', size=1)
    f.label(x0 - 2, 31, '4', size=10, col='blue', anchor='start', bold=True); f.label(x0 - 2, 90, '6', size=10, col='purple', anchor='start', bold=True)
    f.text(x0 + 12 * sc, 104, 'MMC(4, 6) = 12', size=10.5, col='green', bold=True)
    f.text(x0 + 30 * sc, 104, 'mmc · mdc = 4 · 6', size=10, col='grey')
    return f.svg()


def fig_mdc():
    f = Fig(190, 128)
    s = 40
    for i in range(3):
        for j in range(2):
            f.rect(10 + i * s, 8 + j * s, s, s, fill='lpurple' if (i + j) % 2 == 0 else 'lblue', stroke='navy', sw=1.2)
            f.text(10 + i * s + s / 2, 8 + j * s + s / 2 + 4, '6', size=10.5, col='navy')
    f.dim(10, 102, 10 + 3 * s, 102, '18 m', col='grey', text_dy=14)
    f.line(138, 8, 138, 88, col='grey', w=1.1, arrow=True, arrow0=True)
    f.text(160, 52, '12 m', size=10, col='grey')
    return f.svg()


def fig_unidades():
    f = Fig(342, 138)
    names = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm']
    w = 44
    for k, n in enumerate(names):
        f.rect(4 + k * w, 24, w - 3, 26, fill='lblue' if n != 'm' else 'lgreen', stroke='navy', sw=1.2, rx=3)
        f.text(4 + k * w + (w - 3) / 2, 42, n, size=11, col='navy', bold=True)
    f.line(8, 64, 4 + 7 * w - 8, 64, col='green', w=2.2, arrow=True)
    f.text(160, 78, '→ unidade menor: MULTIPLICA (×10 por casa)', size=9.8, col='green', bold=True)
    f.line(4 + 7 * w - 8, 88, 8, 88, col='purple', w=2.2, arrow=True)
    f.text(160, 102, '← unidade maior: DIVIDE (÷10 por casa)', size=9.8, col='purple', bold=True)
    f.text(6, 12, 'COMPRIMENTO: cada casa = 10', size=10, col='navy', bold=True, anchor='start')
    f.text(6, 122, 'ÁREA: cada casa = 10² = 100   ·   VOLUME: cada casa = 10³ = 1000', size=10, col='orange', bold=True, anchor='start')
    f.text(6, 135, '(o fator de comprimento é elevado ao quadrado / ao cubo)', size=9, col='grey', anchor='start')
    return f.svg()


def fig_cubo_litro():
    f = Fig(190, 118)
    box3d(f, 10, 36, 50, 50, 24, 18, fill='lblue')
    f.text(36, 102, '10 cm', size=10, col='grey')
    f.text(96, 46, '1 dm³', size=11.5, col='navy', bold=True, anchor='start')
    f.text(96, 62, '= 1 L', size=11.5, col='green', bold=True, anchor='start')
    f.text(96, 78, '= 1000 cm³', size=10.5, col='navy', anchor='start')
    box3d(f, 100, 98, 9, 9, 4, 3, fill='lgreen', hidden=False)
    f.text(120, 106, '1 cm³ = 1 mL', size=10, col='green', bold=True, anchor='start')
    return f.svg()


def fig_oga():
    f = Fig(342, 104)
    x0, x1 = 20, 322
    f.line(x0, 52, x1, 52, col='ink', w=1.6)
    mid = x0 + (x1 - x0) * math.log10(math.sqrt(10))
    f.rect(x0, 36, mid - x0, 16, fill='lgreen'); f.rect(mid, 36, x1 - mid, 16, fill='lpurple')
    for xx, t in ((x0, '10³'), (x1, '10⁴')):
        f.line(xx, 30, xx, 60, col='ink', w=1.8); f.text(xx, 76, t, size=11.5, col='navy', bold=True)
    f.line(mid, 24, mid, 62, col='orange', w=2, dash='3 3')
    f.text(mid, 18, '√10 ≈ 3,16 × 10³', size=10.5, col='orange', bold=True)
    f.text((x0 + mid) / 2, 48, 'OG = 10³', size=10, col='green', bold=True)
    f.text((mid + x1) / 2, 48, 'OG = 10⁴', size=10, col='purple', bold=True)
    for v, lab, anc, dx in ((2900, '2,9×10³', 'end', -3), (3500, '3,5×10³', 'start', 3)):
        xv = x0 + (x1 - x0) * (math.log10(v) - 3)
        f.dot(xv, 52, 3.8, 'navy'); f.line(xv, 56, xv + dx, 90, col='mgrey', w=1); f.text(xv + dx * 1.4, 100, lab, size=9.5, col='navy', anchor=anc)
    return f.svg()


def fig_pct_flow():
    f = Fig(342, 112)
    def box(x, y, w, h, t1, t2, fill, col):
        f.rect(x, y, w, h, fill=fill, stroke=col, sw=1.6, rx=6)
        f.text(x + w / 2, y + 17, t1, size=11.5, col=col, bold=True)
        f.text(x + w / 2, y + 31, t2, size=9, col='grey')
    box(4, 20, 80, 38, 'R$ 200', 'preço inicial', 'lblue', 'navy')
    box(130, 20, 80, 38, 'R$ 240', '+20%', 'lgreen', 'green')
    box(256, 20, 80, 38, 'R$ 192', '−20% sobre 240', 'lorange', 'orange')
    f.line(86, 39, 128, 39, col='green', w=2.4, arrow=True); f.pill(107, 28, '× 1,20', fill='lgreen', col='green', size=9.5)
    f.line(212, 39, 254, 39, col='orange', w=2.4, arrow=True); f.pill(233, 28, '× 0,80', fill='lorange', col='orange', size=9.5)
    f.path('M44,60 Q44,84 120,84 L252,84 Q296,84 296,62', stroke='purple', sw=2, dash='4 3', arrow=True)
    f.pill(170, 90, '1,20 × 0,80 = 0,96  →  queda de 4%', fill='lpurple', col='purple', size=10.5)
    f.text(170, 8, 'fatores se MULTIPLICAM (nunca some 20% − 20%)', size=9.8, col='navy', bold=True)
    return f.svg()


def fig_pct_back():
    f = Fig(190, 128)
    def box(x, y, t, fill, col):
        f.rect(x, y, 46, 26, fill=fill, stroke=col, sw=1.6, rx=5); f.text(x + 23, y + 17, t, size=11, col=col, bold=True)
    box(4, 24, '100', 'lblue', 'navy'); box(72, 24, '80', 'lorange', 'orange'); box(140, 24, '100', 'lblue', 'navy')
    f.line(50, 37, 70, 37, col='orange', w=2.2, arrow=True); f.line(118, 37, 138, 37, col='green', w=2.2, arrow=True)
    f.pill(60, 18, '−20%', fill='lorange', col='orange', size=9.5); f.pill(128, 18, '+25%', fill='lgreen', col='green', size=9.5)
    f.text(60, 62, '× 0,80', size=10, col='orange', bold=True); f.text(128, 62, '× 1,25', size=10, col='green', bold=True)
    f.text(95, 86, 'fator de volta = 1 ÷ fator de ida', size=10, col='purple', bold=True)
    f.text(95, 102, '1 ÷ 0,80 = 1,25  →  +25%', size=10, col='purple')
    f.text(95, 118, 'Para voltar de −20% precisa subir 25%.', size=9.6, col='grey')
    return f.svg()


def fig_lucro():
    p = Plot(330, 200, 0, 640, -1500, 7800, l=46, r=10, t=14, b=26)
    p.grid(100, 2000)
    p.axes(xlab='x', ylab='R$', xticks=(100, 200, 300, 400, 500, 600), yticks=(2000, 4000, 6000), size=9.5,
           yfmt=lambda v: f'{int(v):,}'.replace(',', '.'))
    R = lambda x: 12 * x
    C = lambda x: 1500 + 7 * x
    p.poly([(p.X(0), p.Y(C(0))), (p.X(300), p.Y(3600)), (p.X(0), p.Y(0))], fill='lorange', op=.75)
    p.poly([(p.X(300), p.Y(3600)), (p.X(640), p.Y(C(640))), (p.X(640), p.Y(R(640)))], fill='lgreen', op=.9)
    p.curve(C, 0, 640, col='orange', w=2.6); p.curve(R, 0, 640, col='green', w=2.6)
    p.pt(300, 3600, 'navy', 4.6)
    p.label(p.X(300) - 8, p.Y(3600) - 9, 'equilíbrio: x = 300', size=10.5, col='navy', anchor='end', bold=True)
    p.label(p.X(420), p.Y(R(420)) - 8, 'R = 12x', size=10.5, col='green', anchor='end', bold=True)
    p.label(p.X(430), p.Y(C(430)) + 17, 'C = 1500 + 7x', size=10.5, col='orange', anchor='start', bold=True)
    p.text(p.X(150), p.Y(2060), 'prejuízo', size=10, col='orange', bold=True)
    p.text(p.X(560), p.Y(5950), 'lucro', size=10, col='green', bold=True)
    return p.svg()


def fig_juros():
    p = Plot(330, 205, 0, 10.8, 800, 2900, l=44, r=10, t=14, b=26)
    p.grid(2, 400)
    p.axes(xlab='t', ylab='M (R$)', xticks=(2, 4, 6, 8, 10), yticks=(1000, 1400, 1800, 2200, 2600), size=9.5, origin=False,
           yfmt=lambda v: f'{int(v):,}'.replace(',', '.'))
    p.curve(lambda t: 1000 + 100 * t, 0, 10, col='blue', w=2.6)
    p.curve(lambda t: 1000 * 1.1 ** t, 0, 10, col='purple', w=2.6)
    for t in range(0, 11):
        p.pt(t, 1000 + 100 * t, 'blue', 2.6); p.pt(t, 1000 * 1.1 ** t, 'purple', 2.6)
    p.label(p.X(10) - 4, p.Y(2593.7) - 8, '2.594', size=10, col='purple', anchor='end', bold=True)
    p.label(p.X(10) - 2, p.Y(2000) + 15, '2.000', size=10, col='blue', anchor='end', bold=True)
    p.text(p.X(0.3), p.Y(2760), 'compostos: M = 1000 · 1,1ᵗ', size=10, col='purple', bold=True, anchor='start')
    p.text(p.X(0.3), p.Y(2640), '(× 1,10 a cada período)', size=9.2, col='purple', anchor='start')
    p.text(p.X(10.6), p.Y(1280), 'simples: M = 1000(1 + 0,1t)', size=10, col='blue', bold=True, anchor='end')
    p.text(p.X(10.6), p.Y(1160), '(+ 100 a cada período)', size=9.2, col='blue', anchor='end')
    return p.svg()


# =====================================================================  PÁGINAS
def p_prop():
    band = chapter_band(1, 'Matemática básica, proporcionalidade e finanças', 'tópicos 1 · 2 · 3 · 4 · 40')

    c3 = card('Razão, proporção e regra de três', None, 'A', cols(
        stack(
            formula((r'\dfrac{a}{b}=\dfrac{c}{d}\ \Rightarrow\ a\cdot d=b\cdot c', 'produto cruzado'),
                    (r'\dfrac{y_1}{x_1}=\dfrac{y_2}{x_2}', '<b>direta</b>: razão y/x constante'),
                    (r'x_1\,y_1=x_2\,y_2', '<b>inversa</b>: produto x·y constante'), label='PROPORÇÃO · REGRA DE TRÊS'),
            when('Teste: <b>dobrando A, B dobra?</b> → direta. <b>B cai à metade?</b> → inversa. '
                 'Composta: compare <u>cada</u> grandeza com a da incógnita (direta mantém, inversa inverte) e multiplique as razões.'),
            err('Usar regra direta onde é inversa: mais operários, máquinas ou velocidade → <u>menos</u> dias/tempo.'),
            gap='1.6mm'),
        stack(
            fig(fig_regra3(), 'Direta: pontos alinhados com a origem (y/x constante). Inversa: hipérbole (x·y constante).'),
            mini('6 máquinas fazem 1 200 peças em 5 h.', 'Quantas horas levam 10 máquinas para 2 000 peças?',
                 r'peças: direta; máquinas: inversa → \(h=5\cdot\tfrac{2000}{1200}\cdot\tfrac{6}{10}\).', '= 5 h.'),
            gap='1.6mm'),
        ratio='1fr 1fr', gap='3.5mm', align='center'))

    c1 = card('Escala', 1, 'A', cols(
        stack(
            formula((r'E=\dfrac{\text{medida no desenho}}{\text{medida real}}\quad(\text{mesma unidade})', ''),
                    (r'E_{\text{área}}=E^2,\qquad E_{\text{volume}}=E^3', 'razões de semelhança'), label='ESCALA 1 : N'),
            when('<b>Mapa, planta, maquete, miniatura</b>, “escala 1 : 50 000”. Lê-se: 1 cm no desenho = 50 000 cm reais = <b>500 m</b>.'),
            err('Misturar unidades (cm × km). Lembre: ÷ 100 000 leva cm → km. “Escala maior” = denominador <u>menor</u> (1:100 é maior que 1:1000).'),
            gap='1.6mm'),
        stack(
            fig(fig_escala(), '4 cm no mapa 1 : 50 000 → 4 × 50 000 = 200 000 cm = <b>2 km</b>. Se o comprimento ×2, área ×4 e volume ×8.'),
            mini('Maquete 1 : 200.', 'Prédio de 60 m de altura e 800 m² de planta.',
                 r'altura: \(6000\div200=30\) cm; planta: \(800\ \text{m}^2\div 200^2=0{,}02\ \text{m}^2\).', '30 cm e 200 cm².'),
            gap='1.6mm'),
        ratio='1fr 1fr', gap='3.5mm', align='center'))

    c2 = card('Vazão', 2, 'A', cols(
        stack(
            formula((r'Q=\dfrac{V}{t}\ \Rightarrow\ V=Q\cdot t,\quad t=\dfrac{V}{Q}', 'volume ÷ tempo'),
                    (r'Q=A\cdot v', 'área da seção × velocidade do fluido'), label='VAZÃO'),
            when('“<b>litros por minuto</b>”, torneira, ralo, bomba, rio, tubulação, “tempo para encher/esvaziar”. '
                 'Vazões que <u>enchem somam</u>; as que <u>esvaziam subtraem</u>.'),
            err('Unidades diferentes (L/min com m³/h) e esquecer o ralo aberto. Converta tudo <u>antes</u> (1 m³ = 1000 L).'),
            gap='1.6mm'),
        fig(fig_tanque()),
        ratio='1.3fr .7fr', gap='3.5mm', align='center'))

    e1 = ex(1, 'Reservatório: vazão + volume + porcentagem + unidades',
            'Um reservatório em forma de paralelepípedo mede 2,0 m × 1,5 m × 1,2 m e está vazio. Duas torneiras enchem-no, com vazões de '
            '6 L/min e 9 L/min, mas o ralo está aberto e escoa 3 L/min. Em quanto tempo o reservatório atinge 75% da capacidade?',
            '<b>Vazão</b> (V = Q·t) com vazões somadas/subtraídas; o volume vem de <b>paralelepípedo</b> e há <b>porcentagem</b> e <b>conversão m³ → L</b>.',
            r'\(V=2{,}0\cdot1{,}5\cdot1{,}2=3{,}6\ \text{m}^3=3\,600\ \text{L}\); \(75\%\ \Rightarrow\ 0{,}75\cdot3600=2\,700\ \text{L}\).'
            r'<br>\(Q_{\text{líq}}=6+9-3=12\ \text{L/min}\ \Rightarrow\ t=\dfrac{2700}{12}=225\ \text{min}\).',
            r'\(225\ \text{min}=3\ \text{h}+45\ \text{min}\): <b>3 h 45 min</b> (= 3,75 h).',
            shortcut=r'Confira: \(12\ \text{L/min}\times 60=720\ \text{L/h}\); em 3,75 h → \(720\cdot3{,}75=2700\) L ✔.')
    return band + c3 + c1 + c2 + e1


def p_mmc():
    mm = card('MMC e MDC', None, 'B', cols(
        stack(
            formula((r'\mmc(a,b)\cdot\mdc(a,b)=a\cdot b', 'só para 2 números'), label='RELAÇÃO ÚTIL'),
            '<p class="small"><b>Fatorando:</b> MMC = todos os fatores primos com o <u>maior</u> expoente; MDC = só os comuns com o <u>menor</u> expoente.<br>'
            r'Ex.: \(12=2^2\cdot3\) e \(18=2\cdot3^2\) → MMC \(=2^2\cdot3^2=36\); MDC \(=2\cdot3=6\); \(36\cdot6=216=12\cdot18\) ✔</p>',
            gap='1.2mm'),
        fig(fig_mmc(), None),
        ratio='.82fr 1.18fr', gap='3mm', align='center') +
        cols(fig(fig_mdc(), 'MDC(12, 18) = 6 → 6 ladrilhos'),
             stack(when('<b>MMC</b> (menor múltiplo comum): eventos que <u>se repetem</u> e voltam a coincidir — “a cada 12 e 18 dias”, '
                        '“quando <i>juntos de novo</i>?”, “menor quantidade que dá para…”.', label='USE MMC QUANDO'),
                   when('<b>MDC</b> (maior divisor comum): <u>dividir/cortar em partes iguais, as maiores possíveis</u>, sem sobra — '
                        'ladrilhos, grupos iguais, “maior tamanho de…”.', label='USE MDC QUANDO'),
                   mini('Faróis a cada 12 s e 18 s,', 'juntos agora:', 'MMC(12, 18) = 36.', 'de novo em 36 s.'), gap='1.6mm'),
             ratio='.8fr 1.2fr', gap='3mm', align='center'))

    un = card('Conversão de unidades', 40, 'A', cols(
        stack(
            fig(fig_unidades()),
            tbl(['Grandeza', 'Conversões essenciais'],
                [['Massa', r'1 t = 1000 kg · 1 kg = 1000 g'],
                 ['Tempo', r'1 h = 60 min = 3600 s · 1 dia = 24 h'],
                 ['Velocidade', r'\(1\ \text{m/s}=3{,}6\ \text{km/h}\)  (÷3,6 para voltar)'],
                 ['Área', r'1 m² = 10 000 cm² · 1 ha = 10 000 m² · 1 km² = 10⁶ m²'],
                 ['Volume', r'1 m³ = 1000 L · 1 L = 1000 mL · 1 mL = 1 cm³'],
                 ['Densidade', r'1 g/cm³ = 1000 kg/m³ (água: 1 kg por litro)']], widths=['22%', '78%']), gap='1.6mm'),
        stack(fig(fig_cubo_litro()),
              err('<b>Área e volume</b> não convertem como comprimento: 1 m² = <b>10 000</b> cm² (não 100); 1 m³ = <b>10⁶</b> cm³ (não 100).'),
              mem('<b>1 dm³ = 1 L = 1000 cm³</b> liga volume (geometria) a capacidade (litros). Quase toda questão de “caixa d’água” usa essa ponte.'),
              gap='1.6mm'),
        ratio='1.35fr 1fr', gap='3.5mm', align='start'))

    nc = card('Notação científica e ordem de grandeza', 40, 'B', cols(
        stack(
            formula((r'N=a\times10^{n},\quad 1\le a\lt10,\ n\in\mathbb{Z}', 'notação científica'), label='NOTAÇÃO CIENTÍFICA'),
            '<p class="small">Vírgula andou <b>para a esquerda</b> → expoente <b>positivo</b>: \\(38\\,000\\,000=3{,}8\\times10^{7}\\). '
            'Vírgula andou <b>para a direita</b> → expoente <b>negativo</b>: \\(0{,}00047=4{,}7\\times10^{-4}\\).<br>'
            '<b>Produto:</b> multiplica os \\(a\\) e <u>soma</u> os expoentes · <b>Quociente:</b> divide os \\(a\\) e <u>subtrai</u> os expoentes.</p>',
            gap='1.2mm'),
        stack(fig(fig_oga()),
              '<p class="small"><b>Ordem de grandeza (OG)</b> = potência de 10 mais próxima. Em \\(a\\times10^{n}\\): se \\(a\\lt\\sqrt{10}\\approx3{,}16\\) → OG = \\(10^{n}\\); '
              'se \\(a\\ge3{,}16\\) → OG = \\(10^{n+1}\\).</p>', gap='1mm'),
        ratio='1fr 1.15fr', gap='3.5mm', align='center') +
        cols(err('Arredondar a OG usando 5 como limite: o ponto médio na escala de potências é <b>3,16</b>, não 5. '
                 'Ex.: \\(4{,}7\\times10^{-4}\\) tem OG \\(10^{-3}\\).'),
             mini('Ex.:', r'\((2\times10^{5})\cdot(3\times10^{-2})=6\times10^{3}\) e \(\dfrac{8\times10^{9}}{4\times10^{4}}=2\times10^{5}\).',
                  'A população da Terra, \\(8\\times10^{9}\\), tem OG \\(10^{10}\\) (pois 8 ≥ 3,16).', ''), gap='3mm'))

    r = rec(('MMC ou MDC: “cortar cabos iguais, o maior possível”?', 'MDC'),
            ('2,5 × 10⁻³ tem vírgula andando para…?', 'direita 3 casas: 0,0025'),
            ('1 L é quantos cm³? E 5 m³ são quantos litros?', '1000 cm³ · 5000 L'))
    return mm + un + nc + r


def p_pct():
    pc = card('Porcentagem e fatores percentuais', 40, 'A', cols(
        stack(
            formula((r'p\%\ \text{de}\ X=\dfrac{p}{100}\cdot X', ''),
                    (r'\text{aumento de }p\%:\ \ \times\Big(1+\dfrac{p}{100}\Big)', 'fator > 1'),
                    (r'\text{desconto de }p\%:\ \ \times\Big(1-\dfrac{p}{100}\Big)', 'fator < 1'),
                    (r'\text{variação}=\dfrac{\text{final}-\text{inicial}}{\text{inicial}}', 'em relação ao ANTERIOR'),
                    label='FATORES MULTIPLICATIVOS'),
            gap='1.4mm'),
        stack(tbl(['Variação', 'Fator', 'Variação', 'Fator'],
                  [['+10%', '1,10', '−10%', '0,90'], ['+25%', '1,25', '−25%', '0,75'], ['+3,5%', '1,035', '−35%', '0,65'],
                   ['+100% (dobra)', '2,00', '−50% (metade)', '0,50'], ['+200% (triplica)', '3,00', '−100%', '0']], cls='c'), gap='1mm'),
        ratio='1.15fr 1fr', gap='3.5mm', align='center') +
        fig(fig_pct_flow(), 'Acréscimo de 20% seguido de desconto de 20% <b>não</b> volta ao preço inicial: o desconto incide sobre um valor maior.') +
        cols(tbl(['%', 'fração', 'cálculo mental'],
                 [['50%', '1/2', '÷ 2'], ['25%', '1/4', '÷ 4'], ['20%', '1/5', '÷ 5'], ['10%', '1/10', '÷ 10 (tire um zero)'],
                  ['5%', '1/20', 'metade de 10%'], ['15%', '—', '10% + 5%'], ['75%', '3/4', '3 × (÷ 4)'], ['12,5%', '1/8', '÷ 8']], cls='c'),
             stack(fig(fig_pct_back()),
                   mini('Variação:', 'população de 40 000 para 46 000 hab.', r'\(	frac{46000-40000}{40000}=0{,}15\)', '= +15%.'), gap='1.6mm'),
             ratio='1fr 1.15fr', gap='3.5mm', align='start') +
        cols(when('“<b>x% a mais/menos</b>”, descontos/aumentos <b>sucessivos</b>, “em relação ao valor anterior”, inflação, reajuste. '
                  '<b>Valor original</b>: divida o final pelo fator.'),
             err('<b>Somar</b> percentuais sucessivos (+10% e +10% = <b>+21%</b>, não 20%) e “desfazer” um desconto com o mesmo percentual de acréscimo. '
                 'Também: de 20% para 30% são +10 <i>pontos percentuais</i> = +50% em termos relativos.'), gap='3mm'))

    e2 = ex(2, 'Descontos sucessivos: descubra o preço original',
            'Uma loja anuncia um notebook com 25% de desconto. No caixa, um cupom dá mais 10% de desconto <u>sobre o valor já reduzido</u>. '
            'Um cliente paga R$ 2.430,00. Qual era o preço original e qual foi o desconto total?',
            '<b>Fatores sucessivos</b>: cada desconto multiplica o valor anterior; o preço pago é o resultado final e o original é a incógnita.',
            r'\(\text{fator total}=0{,}75\cdot0{,}90=0{,}675\)'
            r'\[P_{\text{orig}}\cdot0{,}675=2430\ \Rightarrow\ P_{\text{orig}}=\dfrac{2430}{0{,}675}=3\,600\]'
            r'Desconto total: \(1-0{,}675=0{,}325=32{,}5\%\) (e não 25% + 10% = 35%).',
            r'Preço original <b>R$ 3.600,00</b>; desconto total de <b>32,5%</b> (R$ 1.170,00).',
            shortcut=r'Confira ao contrário: \(3600\cdot0{,}75=2700\) e \(2700\cdot0{,}90=2430\) ✔.')

    rr = rec(('Aumento de 8% seguido de 8% de desconto: fator?', '1,08 × 0,92 = 0,9936 (queda de 0,64%)'),
             ('Preço final R$ 168 após 20% de desconto: preço original?', '168 ÷ 0,80 = R$ 210'),
             ('Salário sobe 20% e depois 10%: aumento total?', '1,20 × 1,10 = 1,32 → +32%'))
    return pc + e2 + rr


def p_fin():
    lu = card('Lucro', 4, 'B', cols(
        stack(
            formula((r'L=R-C', 'lucro = receita − custo'),
                    (r'R=p\cdot x,\qquad C=C_F+c_v\cdot x', 'x = quantidade; p = preço; cᵥ = custo variável/un.'),
                    (r'\text{equilíbrio:}\ R=C\ \Rightarrow\ x=\dfrac{C_F}{p-c_v}', ''), label='LUCRO E EQUILÍBRIO'),
            when('Fabricar e vender: custo fixo + custo por unidade, preço de venda, “a partir de quantas unidades há lucro?”.'),
            err('“Lucro de 20%” sobre o <b>custo</b> → venda = 1,20 · custo. Sobre a <b>venda</b> → custo = 0,80 · venda. Leia a base!'),
            gap='1.5mm'),
        fig(fig_lucro(), 'Custo fixo R$ 1.500; custo variável R$ 7; preço R$ 12 → ponto de equilíbrio em x = 1500/(12 − 7) = 300 unidades.'),
        ratio='1fr 1.1fr', gap='3.5mm', align='center'))

    js = card('Juros simples e juros compostos', 3, 'A', cols(
        stack(
            formula((r'J=C\cdot i\cdot t\quad M=C(1+i\,t)', '<b>simples</b>: linear (PA)'),
                    (r'M=C\,(1+i)^{t}', '<b>compostos</b>: exponencial (PG)'), label='JUROS'),
            vars_('<b>C</b> capital · <b>i</b> taxa (decimal) · <b>t</b> tempo na <u>mesma unidade</u> da taxa · <b>M</b> montante = C + J.'),
            when('<b>Simples:</b> “juros simples”, taxa fixa sobre o capital inicial. <b>Compostos:</b> “juros sobre juros”, capitalização mensal, '
                 'dívida do cartão, poupança. Taxas equivalentes: \\(1+i_{\\text{ano}}=(1+i_{\\text{mês}})^{12}\\).'),
            err('Taxa ao ano com tempo em meses (converta). Em compostos, <b>não</b> multiplique i·t. '
                'Se o texto der \\(\\log\\) ou tabela de potências, é para achar \\(t\\): \\(t=\\dfrac{\\log(M/C)}{\\log(1+i)}\\).'),
            gap='1.4mm'),
        fig(fig_juros(), 'R$ 1.000 a 10% por período: simples (reta) × compostos (curva). A partir do 2º período compostos rendem mais.'),
        ratio='1fr 1.1fr', gap='3.5mm', align='center'))

    extra = cols(
        mini('Taxa equivalente:', '2% ao mês, composto.', r'\((1{,}02)^{12}\approx1{,}268\)', '→ ≈ 26,8% ao ano (não 24%).'),
        mini('Lucro sobre custo × venda:', 'custo R$ 80.', r'sobre o custo (25%): \(80\cdot1{,}25=100\); sobre a venda (25%): \(V=\tfrac{80}{0{,}75}\approx106{,}67\).', ''),
        gap='3mm')
    e3 = ex(3, 'Duas aplicações em sequência: compostos e depois simples',
            'Ana aplica R$ 4.000,00 a juros compostos de 5% ao mês durante 2 meses. Em seguida, resgata todo o montante e o reaplica a '
            'juros simples de 2% ao mês durante 5 meses. Qual é o montante final?',
            '<b>Duas fases</b>: a primeira em <b>juros compostos</b> (\\(M=C(1+i)^t\\)); a segunda em <b>juros simples</b> (\\(M=C(1+it)\\)); o montante da 1ª é o capital da 2ª.',
            r'1ª fase: \(M_1=4000\cdot1{,}05^2=4000\cdot1{,}1025=4\,410\)'
            r'<br>2ª fase: \(M_2=4410\cdot(1+0{,}02\cdot5)=4410\cdot1{,}10=4\,851\)',
            r'Montante final de <b>R$ 4.851,00</b> (rendimento total de R$ 851,00, isto é, 21,275%).',
            shortcut=r'Não some os rendimentos percentuais: \(1{,}1025\times1{,}10=1{,}21275\) → \(+21{,}275\%\) (e não 10,25% + 10%).')

    rr = rec(('J simples: C = 2000, i = 3% a.m., t = 4 meses?', 'J = 2000 · 0,03 · 4 = R$ 240'),
             ('Dívida de R$ 100 a 10% a.m. composto, 2 meses?', '100 · 1,1² = R$ 121'),
             ('Equilíbrio: preço 20, custo variável 12, fixo 4000?', 'x = 4000 ÷ 8 = 500 unidades'))
    return lu + js + e3 + extra + rr


def pages():
    return [p_prop(), p_mmc(), p_pct(), p_fin()]
