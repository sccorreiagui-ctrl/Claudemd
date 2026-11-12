"""Capítulo 7 – Geometria espacial (tópicos 33–37)."""
import math
from lib import *
from svg import Fig, Plot, box3d, cylinder, cone

LABEL = 'CAP. 7 · GEOMETRIA ESPACIAL'


def fig_solidos():
    f = Fig(350, 150)
    # cubo
    box3d(f, 14, 50, 54, 54, 22, 17, fill='lblue')
    f.label(41, 118, '*a*', size=11, col='navy', bold=True); f.label(8, 80, '*a*', size=11, col='navy', anchor='end', bold=True)
    f.line(14, 104, 14 + 54 + 22, 104 - 17 - 54, col='orange', w=1.8, dash='4 3') if False else None
    f.text(48, 140, 'CUBO', size=10, col='navy', bold=True)
    # paralelepípedo
    x, y, w, h, dx, dy = 130, 56, 74, 42, 30, 22
    box3d(f, x, y, w, h, dx, dy, fill='lgreen')
    f.line(x, y + h, x + w + dx, y - dy, col='orange', w=2, dash='4 3')
    f.label(x + w / 2, y + h + 14, '*a*', size=11, col='navy', bold=True); f.label(x - 6, y + h / 2 + 4, '*b*', size=11, col='navy', anchor='end', bold=True)
    f.label(x + w + dx + 6, y - dy / 2 + h / 2 - 10, '*c*', size=11, col='navy', anchor='start', bold=True)
    f.label(x + w / 2 - 6, y + h / 2 - 8, '*D*', size=11, col='orange', bold=True)
    f.text(x + 52, 140, 'PARALELEPÍPEDO', size=10, col='navy', bold=True)
    # prisma triangular reto
    x0, y0 = 266, 112
    fr = [(x0, y0), (x0 + 52, y0), (x0 + 22, y0 - 46)]
    bk = [(p[0] + 26, p[1] - 20) for p in fr]
    f.poly([fr[0], fr[2], bk[2], bk[0]], fill='lpurple', stroke='navy', sw=1.4)
    f.poly([fr[1], fr[2], bk[2], bk[1]], fill='lpurple', stroke='navy', sw=1.4)
    f.poly([fr[0], fr[1], bk[1], bk[0]], fill='lpurple', stroke='navy', sw=1.4, op=.0)
    f.poly(bk, fill='none', stroke='navy', sw=1, dash='3 3')
    f.poly(fr, fill='lblue', stroke='navy', sw=1.8)
    f.text(x0 + 24, y0 - 14, '*A*_b', size=10, col='navy', bold=True)
    f.label(x0 + 46, y0 - 36, '*h*', size=11, col='orange', anchor='start', bold=True)
    f.line(x0 + 22, y0 - 46, x0 + 22 + 26, y0 - 46 - 20, col='orange', w=1.8)
    f.text(x0 + 36, 140, 'PRISMA', size=10, col='navy', bold=True)
    return f.svg()


def fig_cilindro():
    f = Fig(250, 176)
    cx, yt, rx, ry, h = 58, 36, 40, 12, 92
    cylinder(f, cx, yt, rx, ry, h, fill='lblue')
    f.line(cx, yt, cx + rx, yt, col='green', w=2.2); f.label(cx + 20, yt - 4, '*r*', size=11, col='green', bold=True)
    f.dot(cx, yt, 2.6, 'navy')
    f.line(cx + rx + 12, yt, cx + rx + 12, yt + h, col='orange', w=1.5, arrow=True, arrow0=True)
    f.label(cx + rx + 18, yt + h / 2 + 4, '*h*', size=11, col='orange', anchor='start', bold=True)
    f.text(cx, 22, 'CILINDRO RETO', size=10, col='navy', bold=True)
    # planificação lateral
    x0 = 150
    f.rect(x0, yt + 4, 90, h - 6, fill='lorange', stroke='navy', sw=1.6)
    f.text(x0 + 45, yt + 4 + (h - 6) / 2, '*A*_lat', size=10.5, col='navy', bold=True)
    f.text(x0 + 45, yt + h + 18, '2π*r*', size=11, col='green', bold=True)
    f.text(x0 + 45, 22, 'lateral planificada', size=9.6, col='grey')
    f.text(125, 168, '*A*_lat = 2π*r*·*h*  ·  *V* = π*r*²·*h*', size=10, col='green', bold=True)
    return f.svg(width='100%')


def fig_cone():
    f = Fig(250, 176)
    cx, yt, rx, ry, h = 54, 36, 40, 12, 92
    f.path(f'M{cx - rx},{yt} L{cx - rx},{yt + h} A{rx},{ry} 0 0 0 {cx + rx},{yt + h} L{cx + rx},{yt}', stroke='mgrey', sw=1.2, dash='3 3')
    f.ell(cx, yt, rx, ry, stroke='mgrey', sw=1.2, dash='3 3')
    cone(f, cx, yt, rx, ry, h, fill='lpurple')
    f.line(cx, yt, cx, yt + h, col='orange', w=1.8, dash='4 3'); f.label(cx - 6, yt + h / 2 + 4, '*h*', size=11, col='orange', anchor='end', bold=True)
    f.line(cx, yt + h, cx + rx, yt + h, col='green', w=2.2); f.label(cx + 20, yt + h - 4, '*r*', size=11, col='green', bold=True)
    f.label(cx + rx / 2 + 12, yt + h / 2 - 2, '*g*', size=11, col='navy', anchor='start', bold=True)
    f.text(cx, 22, 'CONE RETO', size=10, col='navy', bold=True)
    g = math.hypot(h, rx)
    th = 360 * rx / g
    x0, y0, R = 165, 40, 84
    f.sector(x0, y0, R, 270 - th / 2, 270 + th / 2, fill='lpurple', stroke='navy', sw=1.6)
    f.line(x0, y0, x0 + R * math.cos(math.radians(270 - th / 2)), y0 - R * math.sin(math.radians(270 - th / 2)), col='navy', w=1.6)
    f.label(x0 - 26, y0 + 40, '*g*', size=11, col='navy', bold=True)
    f.text(x0, y0 + R + 14, 'arco = 2π*r*', size=10.5, col='green', bold=True)
    f.text(x0, 22, 'lateral planificada (setor)', size=9.6, col='grey')
    f.text(125, 172, '*V* = ⅓π*r*²*h*  ·  *A*_lat = π*r g*  ·  *g*² = *h*² + *r*²', size=9.4, col='green', bold=True)
    return f.svg(width='100%')


def fig_esfera():
    f = Fig(230, 150)
    cx, cy, r = 70, 72, 52
    f.circ(cx, cy, r, fill='lblue', stroke='navy', sw=2)
    f.path(f'M{cx - r},{cy} A{r},{16} 0 0 0 {cx + r},{cy}', stroke='navy', sw=1.6)
    f.path(f'M{cx - r},{cy} A{r},{16} 0 0 1 {cx + r},{cy}', stroke='navy', sw=1.2, dash='3 3')
    f.line(cx, cy, cx + r * 0.7, cy - r * 0.7, col='green', w=2.4); f.dot(cx, cy, 3, 'navy')
    f.label(cx + 22, cy - 14, '*r*', size=11.5, col='green', bold=True)
    f.text(160, 38, 'ESFERA', size=10, col='navy', bold=True)
    f.text(160, 66, '*V* = ⁴⁄₃ π*r*³', size=11.5, col='green', bold=True)
    f.text(160, 88, '*A* = 4π*r*²', size=11.5, col='green', bold=True)
    f.text(160, 112, 'hemisfério: *V* = ⅔π*r*³', size=9.4, col='grey')
    f.text(160, 126, '*A*_total = 3π*r*²', size=9.4, col='grey')
    return f.svg(width='100%')


def fig_troncos():
    f = Fig(350, 176)
    # tronco de cone
    cx, yt, r, R, h = 78, 66, 26, 52, 70
    yb = yt + h
    apex = (cx, yt - h * r / (R - r))
    f.path(f'M{cx},{apex[1]} L{cx - r},{yt} M{cx},{apex[1]} L{cx + r},{yt}', stroke='mgrey', sw=1.2, dash='3 3')
    f.path(f'M{cx - r},{yt} L{cx - R},{yb} A{R},14 0 0 0 {cx + R},{yb} L{cx + r},{yt} Z', fill='lblue', stroke='navy', sw=1.8)
    f.ell(cx, yt, r, 8, fill='white', stroke='navy', sw=1.8)
    f.path(f'M{cx - R},{yb} A{R},14 0 0 1 {cx + R},{yb}', stroke='navy', sw=1.1, dash='3 3')
    f.line(cx, yt, cx + r, yt, col='green', w=2); f.label(cx + 13, yt - 3, '*r*', size=10.5, col='green', bold=True)
    f.line(cx, yb, cx + R, yb, col='green', w=2); f.label(cx + 26, yb - 4, '*R*', size=10.5, col='green', bold=True)
    f.line(cx, yt, cx, yb, col='orange', w=1.6, dash='4 3'); f.label(cx - 4, (yt + yb) / 2 + 4, '*h*', size=10.5, col='orange', anchor='end', bold=True)
    f.text(cx, 14, 'TRONCO DE CONE', size=10, col='navy', bold=True)
    f.text(cx - 34, apex[1] + 6, 'cone completo', size=8.6, col='grey', anchor='middle') if False else None
    f.text(cx, 168, '*V* = π*h*/3 · (*R*² + *Rr* + *r*²)', size=9.6, col='green', bold=True)
    # tronco de pirâmide
    c0 = (262, 118); c1 = (262, 52)
    rel = [(-54, 12), (28, 12), (54, -10), (-28, -10)]
    B = [(c0[0] + a, c0[1] + b) for a, b in rel]
    T = [(c1[0] + 0.5 * a, c1[1] + 0.5 * b) for a, b in rel]
    f.poly([B[0], B[1], T[1], T[0]], fill='lgreen', stroke='navy', sw=1.5)
    f.poly([B[1], B[2], T[2], T[1]], fill='lgreen', stroke='navy', sw=1.5)
    f.poly([B[0], B[1], B[2], B[3]], fill='none', stroke='navy', sw=1, dash='3 3')
    f.poly([B[0], B[1], B[2], B[3]], fill='lblue', op=.0)
    f.poly(T, fill='white', stroke='navy', sw=1.8)
    f.poly([B[0], B[1], B[2], B[3]], stroke='navy', sw=1.4, fill='none', op=0)
    f.line(c1[0], c1[1], c0[0], c0[1], col='orange', w=1.6, dash='4 3'); f.label(c0[0] + 7, (c0[1] + c1[1]) / 2 + 4, '*h*', size=10.5, col='orange', anchor='start', bold=True)
    f.text(c1[0] + 4, c1[1] + 2, '*A*_b', size=9.6, col='navy', bold=True)
    f.text(c0[0] + 2, c0[1] + 6, '*A*_B', size=9.6, col='navy', bold=True)
    f.text(262, 14, 'TRONCO DE PIRÂMIDE', size=10, col='navy', bold=True)
    f.text(262, 168, '*V* = π*h*/3 · ... → *h*/3 · (*A*_B + √(*A*_B*A*_b) + *A*_b)', size=8.8, col='green', bold=True) if False else None
    f.text(262, 168, '*V* = *h*/3 · (*A*_B + √(*A*_B·*A*_b) + *A*_b)', size=9.2, col='green', bold=True)
    return f.svg()


def fig_copo():
    f = Fig(230, 170)
    cx, yt, rx, ry, h = 76, 30, 36, 11, 110
    f.path(f'M{cx - rx},{yt} L{cx - rx},{yt + h} A{rx},{ry} 0 0 0 {cx + rx},{yt + h} L{cx + rx},{yt}', fill='white', stroke='navy', sw=1.8)
    wh = 80
    f.path(f'M{cx - rx},{yt + h - wh} L{cx - rx},{yt + h} A{rx},{ry} 0 0 0 {cx + rx},{yt + h} L{cx + rx},{yt + h - wh} A{rx},{ry} 0 0 1 {cx - rx},{yt + h - wh}', fill='lblue', stroke='blue', sw=1.2)
    f.ell(cx, yt + h - wh, rx, ry, fill='mblue', stroke='blue', sw=1.2, op=.9)
    f.ell(cx, yt, rx, ry, fill='none', stroke='navy', sw=1.8)
    f.circ(cx, yt + h - 36, 36 * .98, fill='lpurple', stroke='purple', sw=1.6, op=.95)
    f.text(cx, yt + h - 32, 'esfera', size=9.6, col='purple', bold=True)
    f.line(cx + rx + 12, yt, cx + rx + 12, yt + h, col='grey', w=1.2, arrow=True, arrow0=True); f.label(cx + rx + 17, yt + 20, '10 cm', size=9.6, col='grey', anchor='start')
    f.line(cx + rx + 28, yt + h - wh, cx + rx + 28, yt + h, col='blue', w=1.2, arrow=True, arrow0=True); f.label(cx + rx + 33, yt + h - 38, '8 cm', size=9.6, col='blue', anchor='start')
    f.dim(cx - rx, yt + h + 22, cx + rx, yt + h + 22, '6 cm', col='grey', text_dy=-4)
    return f.svg(width='100%')


def p_prismas():
    band = chapter_band(7, 'Geometria espacial', 'tópicos 33 · 34 · 35 · 36 · 37')
    c33 = card('Prismas, cubo e paralelepípedo', 33, 'A', cols(
        stack(
            formula((r'V=A_b\cdot h\qquad A_{\text{lat}}=P_b\cdot h', 'prisma reto'),
                    (r'A_t=2A_b+A_{\text{lat}}', ''),
                    (r'\text{cubo: }V=a^3,\ A_t=6a^2,\ D=a\sqrt3', 'D = diagonal'),
                    (r'\text{paralelepípedo: }V=abc,\ A_t=2(ab+ac+bc)', ''),
                    (r'D=\sqrt{a^2+b^2+c^2}', 'diagonal do paralelepípedo'), label='PRISMAS'),
            gap='1.2mm'),
        stack(fig(fig_solidos(), None),
              when('<b>Caixa, tijolo, piscina, contêiner, bloco, embalagem</b>, “capacidade”. Sempre: \\(V=\\text{área da base}\\times\\text{altura}\\). '
                   'Dimensões em metros → m³ → litros (×1000).'), gap='1.2mm'),
        ratio='1.05fr 1fr', gap='3.5mm', align='start') +
        cols(err('<b>Volume</b> (m³) ≠ <b>área</b> (m²): pintar paredes → área; encher → volume. Dobrando todas as arestas, a área <b>quadruplica</b> e o volume <b>octuplica</b>.'),
             mem('Qualquer sólido “reto” (prisma, cilindro) é <b>base × altura</b>: o que muda é a <u>área da base</u>.'), gap='3mm'))

    c34 = card('Cilindro e cone retos', 34, 'A', cols(fig(fig_cilindro(), None), fig(fig_cone(), None), gap='3mm') +
               cols(formula((r'V_{\text{cil}}=\pi r^2h\quad A_{\text{lat}}=2\pi rh\quad A_t=2\pi r(r+h)', ''),
                            (r'V_{\text{cone}}=\tfrac13\pi r^2h\quad A_{\text{lat}}=\pi rg\quad A_t=\pi r(r+g)', ''), label='CILINDRO · CONE'),
                    stack(mem('<b>Cone = ⅓ do cilindro</b> de mesma base e altura (3 cones enchem 1 cilindro). Vale também para pirâmide × prisma.'),
                          err('Usar o <b>diâmetro</b> no lugar de r; esquecer o <b>⅓</b> do cone; usar a <u>altura</u> h no lugar da <u>geratriz</u> g na área lateral.'), gap='1.3mm'),
                    ratio='1.3fr 1fr', gap='3mm', align='start'))
    c35 = card('Relação entre raio, altura e geratriz do cone reto', 35, 'C', cols(
        formula((r'g^2=h^2+r^2', 'Pitágoras no triângulo da secção'), label='CONE'),
        mini('Cone com r = 3 e h = 4:', '', r'\(g=\sqrt{16+9}=5\); \(V=\tfrac13\pi\cdot9\cdot4=12\pi\)', '; \\(A_{\\text{lat}}=\\pi\\cdot3\\cdot5=15\\pi\\).'),
        ratio='1fr 1.3fr', gap='3mm', align='center'))
    r = rec(('Cilindro r = 2, h = 5: V e A_lat?', 'V = 20π · A_lat = 20π'),
            ('Caixa 2 m × 3 m × 1 m: volume em litros?', '6 m³ = 6 000 L'),
            ('Cone e cilindro de mesma base e altura: V cone ÷ V cil?', '1/3'))
    return band + c33 + c34 + c35 + r


def p_esfera():
    c36 = card('Esfera', 36, 'B', cols(
        fig(fig_esfera(), None),
        stack(when('Bola, cúpula, tanque esférico, planeta, gota. <b>Seção</b> da esfera por um plano é um <b>círculo</b>: se o plano está a distância d do centro, o círculo tem raio \\(\\sqrt{r^2-d^2}\\).'),
              mem('<b>Esfera inscrita num cilindro</b> (altura 2r): \\(V_{\\text{esf}}=\\tfrac23V_{\\text{cil}}\\) — e a área da esfera = área lateral do cilindro (4πr²).'),
              err('Dobrar o raio: volume <b>×8</b> (r³) e área <b>×4</b> (r²).'), gap='1.3mm'),
        ratio='1fr 1.2fr', gap='3.5mm', align='center'))
    c37 = card('Volume de figuras truncadas: tronco de cone e tronco de pirâmide', 37, 'C', cols(
        fig(fig_troncos(), None),
        stack(
            formula((r'V_{\text{tronco}}=\dfrac{h}{3}\big(A_B+\sqrt{A_B\,A_b}+A_b\big)', 'pirâmide ou cone'), label='TRONCO'),
            mem('<b>Sem decorar:</b> complete o sólido até o vértice, calcule o <u>grande</u> e <u>subtraia o pequeno</u> (semelhante, razão \\(k\\)): lados ×k, áreas ×k², <b>volumes ×k³</b>.'),
            mini('Tronco de cone R = 6, r = 3, h = 4:', '', r'cone completo: \(H=8\) (semelhança) → \(\tfrac13\pi\cdot36\cdot8-\tfrac13\pi\cdot9\cdot4=96\pi-12\pi\)', '= 84π (= fórmula: \\(\\tfrac{4\\pi}{3}\\cdot63\\)).'),
            gap='1.3mm'),
        ratio='1.2fr 1fr', gap='3.5mm', align='center'))

    e12 = ex(12, 'Copo, água e esfera: o que transborda?',
             'Um copo cilíndrico de 6 cm de diâmetro e 10 cm de altura contém água até 8 cm de altura. Uma esfera maciça de raio 3 cm é totalmente mergulhada no copo. '
             'Quantos mililitros de água transbordam? (Use π = 3,14.)',
             '<b>Cilindro</b> (capacidade e volume de água) e <b>esfera</b> (volume deslocado). A esfera cabe e fica submersa (diâmetro 6 cm &lt; 8 cm de água). Conversão: 1 cm³ = 1 mL.',
             r'\(r=3\ \text{cm}\): \(V_{\text{água}}=\pi\cdot9\cdot8=72\pi\); \(\ V_{\text{esfera}}=\tfrac43\pi\cdot27=36\pi\); \(\ V_{\text{copo}}=\pi\cdot9\cdot10=90\pi\).'
             r'<br>Volume total após mergulhar: \(72\pi+36\pi=108\pi\ \Rightarrow\ \text{transbordo}=108\pi-90\pi=18\pi\).'
             r'<br>\(18\cdot3{,}14=56{,}52\ \text{cm}^3\).',
             r'Transbordam ≈ <b>56,5 mL</b>.',
             shortcut=r'Não precisa de π até o fim: o transbordo é \(18\pi\) (nível sobe \(\tfrac{36\pi}{9\pi}=4\) cm: de 8 para 12 cm, 2 cm acima da borda; \(2\cdot9\pi=18\pi\) ✔).')
    mn = cols(
        mini('Caixa d’água cúbica:', 'aresta de 1,5 m.', r'\(V=1{,}5^3=3{,}375\ \text{m}^3\)', '= 3 375 L.'),
        mini('Semelhança:', 'maquete de silo na escala 1 : 50 tem 4 L de volume.', r'\(V_{\text{real}}=4\cdot50^3\ \text{L}=500\,000\ \text{L}\)', '= 500 m³.'), gap='3mm')
    r = rec(('Esfera de raio 3: V e A?', 'V = 36π · A = 36π'),
            ('Cubo cuja diagonal mede 6√3: aresta?', 'D = a√3 → a = 6'),
            ('Tronco: como evitar decorar a fórmula?', 'sólido completo − sólido pequeno (k³)'))
    return c36 + c37 + cols(e12, fig(fig_copo(), None), ratio='1.7fr 1fr', gap='3mm', align='center') + mn + r


def pages():
    return [p_prismas(), p_esfera()]
