# -*- coding: utf-8 -*-
from lib import *
from figs import *
from molsvg import mol_svg, match, parse
import math

# ---------- helpers de desenho molecular esquemático ----------
def atom(s, x, y, lab, r=10, fill='#fff', stroke=INK, size=12, w=700, color=INK):
    s.circ(x, y, r, fill, stroke, 1.3); s.text(x, y+size*0.35, lab, size, color, 'middle', w)

def dip(s, x1, y1, x2, y2, color=BLUE, sw=2.6, cross=5):
    """Vetor dipolo: cruz no polo positivo (início), seta no negativo (fim)."""
    dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy); ux, uy = dx/L, dy/L; px, py = -uy, ux
    s.line(x1 - px*cross, y1 - py*cross, x1 + px*cross, y1 + py*cross, color, sw)
    s.arrow(x1, y1, x2, y2, 'blue' if color == BLUE else 'ink', sw)

def bond(s, x1, y1, x2, y2, kind='plain'):
    if kind == 'plain': s.line(x1, y1, x2, y2, '#7A8497', 2.2)
    elif kind == 'wedge':
        dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy); px, py = -dy/L*4.5, dx/L*4.5
        s.poly([(x1, y1), (x2+px, y2+py), (x2-px, y2-py)], '#7A8497', '#7A8497', 1, close=True)
    elif kind == 'dash':
        for i in range(1, 7):
            t = i/7; xx, yy = x1+(x2-x1)*t, y1+(y2-y1)*t; dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy)
            px, py = -dy/L*(1+4*t), dx/L*(1+4*t)
            s.line(xx-px, yy-py, xx+px, yy+py, '#7A8497', 1.8)
    elif kind == 'double':
        dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy); px, py = -dy/L*2.6, dx/L*2.6
        s.line(x1+px, y1+py, x2+px, y2+py, '#7A8497', 2); s.line(x1-px, y1-py, x2-px, y2-py, '#7A8497', 2)

def lone(s, x, y, rot=0):
    """par livre: dois pontos"""
    a = math.radians(rot); dx, dy = 3.2*math.cos(a), 3.2*math.sin(a)
    s.circ(x-dx, y-dy, 1.9, INK); s.circ(x+dx, y+dy, 1.9, INK)

def along(p, q, t0, t1):
    return (p[0]+(q[0]-p[0])*t0, p[1]+(q[1]-p[1])*t0, p[0]+(q[0]-p[0])*t1, p[1]+(q[1]-p[1])*t1)

def verdict(s, x, y, polar, w=96):
    col = (BLUE, BLUE_D, BLUE_L) if polar else (AMBER, AMBER_D, AMBER_L)
    s.rect(x-w/2, y-14, w, 20, col[2], col[0], 10, 1.6)
    s.text(x, y, ('POLAR  μ ≠ 0' if polar else 'APOLAR  μ = 0'), 10.5, col[1], 'middle', 800)

# ======================= A1 =======================
def p_lig():
    # --- iônica
    s = Svg(222, 124)
    s.circ(40, 32, 15, '#fff', INK, 1.6); s.text(40, 36, 'Na', 11, INK, 'middle', 700); s.circ(40+15, 32, 3, INK)
    s.path('M60,22 Q90,2 112,20', stroke=INK, sw=1.4, marker='ink'); s.text(87, 12, 'e⁻', 10, INK, 'middle', 700)
    s.circ(140, 32, 20, '#fff', INK, 1.6); s.text(140, 36, 'Cl', 12, INK, 'middle', 700)
    s.text(40, 62, 'metal perde e⁻', 9, GRAY, 'middle', 600); s.text(150, 66, 'ametal ganha e⁻', 9, GRAY, 'middle', 600)
    for r in range(2):
        for c in range(5):
            x, y = 50 + c*30, 82 + r*23; pos = (r + c) % 2 == 0
            s.circ(x, y, 8 if pos else 10.5, '#fff' if pos else LGRAY, INK, 1.3); s.text(x, y+4, '+' if pos else '−', 11, INK, 'middle', 800)
    s.text(111, 120, 'Na⁺ e Cl⁻: retículo cristalino', 9.5, INK, 'middle', 700)
    ion = s.render()
    # --- covalente
    s = Svg(222, 124)
    s.circ(86, 24, 20, 'none', INK, 1.4); s.circ(126, 24, 20, 'none', INK, 1.4); s.circ(106, 21, 2.3, INK); s.circ(106, 27, 2.3, INK)
    s.text(70, 28, 'H', 11, INK, 'middle', 700); s.text(142, 28, 'H', 11, INK, 'middle', 700)
    s.text(111, 58, 'H₂: partilha igual → apolar', 9.4, AMBER_D, 'middle', 800)
    s.circ(80, 90, 16, 'none', INK, 1.4); s.circ(124, 90, 22, BLUE_L, BLUE, 1.6); s.circ(80, 90, 16, 'none', INK, 1.4)
    s.circ(104, 87, 2.3, INK); s.circ(106, 94, 2.3, INK)
    s.text(66, 94, 'H', 11, INK, 'middle', 700); s.text(133, 94, 'Cl', 11, INK, 'middle', 700)
    s.text(58, 76, 'δ+', 10, BLUE_D, 'middle', 800); s.text(150, 72, 'δ−', 10, BLUE_D, 'middle', 800)
    s.text(111, 120, 'HCl: partilha desigual → polar', 9.4, BLUE_D, 'middle', 800)
    cov = s.render()
    # --- metálica
    s = Svg(222, 124)
    import random; rnd = random.Random(4)
    for r in range(3):
        for c in range(5):
            x, y = 34 + c*38, 22 + r*30
            s.circ(x, y, 10, '#fff', INK, 1.4); s.text(x, y+3.5, '+', 11, INK, 'middle', 800)
    for _ in range(26):
        s.circ(rnd.uniform(18, 205), rnd.uniform(10, 100), 2, BLUE)
    s.arrow(20, 114, 80, 114, 'blue', 2); s.text(90, 118, 'elétrons livres → corrente', 9.2, BLUE_D, 'start', 700)
    s.text(111, 8, '', 8, INK)
    met = s.render()
    cards = ''.join(f'<div class="card"><h3>{t}</h3><div style="margin:1mm 0">{svg}</div><div style="font-size:8pt">{d}</div></div>' for t, svg, d in [
        (f'{tag("ink","1")} Iônica', ion, '<b>metal + ametal</b>: transferência de e⁻. Sólidos de PF alto, quebradiços; conduzem corrente <b>fundidos ou dissolvidos</b>. A fórmula (NaCl) é uma <i>proporção</i>, não uma molécula.'),
        (f'{tag("ink","2")} Covalente', cov, '<b>ametal + ametal (e H)</b>: compartilhamento de e⁻. Forma <b>moléculas</b> (ou redes, como diamante e SiO₂). A partilha pode ser igual ou desigual.'),
        (f'{tag("ink","3")} Metálica', met, '<b>metal + metal</b>: cátions num “mar” de elétrons livres. Conduz corrente e calor, é dúctil e maleável.')])
    # --- régua de eletronegatividade
    e = Svg(714, 114)
    ax = Axes(e, 40, 52, 634, 10, (0.8, 4.2), (0, 1))
    e.rect(40, 52, 634, 10, 'url(#dots-blue)', BLUE, 5, 1.2)
    for el, v, dy in [('Na', 0.9, 0), ('H', 2.1, 0), ('P', 2.1, 1), ('C', 2.5, 0), ('S', 2.5, 1), ('Br', 2.8, 0), ('N', 3.0, 0), ('Cl', 3.0, 1), ('O', 3.5, 0), ('F', 4.0, 0)]:
        x = ax.X(v)
        y0 = 2 if dy == 0 else 76
        e.line(x, 34 if dy == 0 else 62, x, 52 if dy == 0 else 76, GRAY, 1.2)
        e.rect(x-17, y0, 34, 32, BLUE_L if v >= 3 else '#fff', BLUE if v >= 3 else INK, 6, 1.4)
        e.text(x, y0+14, el, 11.5, INK, 'middle', 800); e.text(x, y0+27, f'{v:.1f}'.replace('.', ','), 10, BLUE_D, 'middle', 800)
    e.text(42, 80, 'menos atração por e⁻', 9.4, GRAY, 'start', 600)
    e.arrow(150, 80, 560, 80, 'blue', 1.6); e.text(672, 80, 'mais atração', 9.4, GRAY, 'end', 600)
    scale = e.render()
    # --- ΔEN
    z = Svg(450, 118)
    z.rect(6, 22, 106, 26, AMBER_L, AMBER, 4, 1.6); z.rect(112, 22, 190, 26, BLUE_L, BLUE, 0, 1.6); z.rect(302, 22, 140, 26, '#E7E9EE', GRAY, 4, 1.6)
    z.text(59, 39, 'ΔEN ≈ 0', 11, AMBER_D, 'middle', 800); z.text(207, 39, '0 < ΔEN ≲ 1,7', 11, BLUE_D, 'middle', 800); z.text(372, 39, 'ΔEN ≳ 1,7', 11, INK, 'middle', 800)
    z.text(59, 12, 'COVALENTE APOLAR', 8.6, AMBER_D, 'middle', 800); z.text(207, 12, 'COVALENTE POLAR', 8.6, BLUE_D, 'middle', 800); z.text(372, 12, 'IÔNICA (convenção)', 8.6, INK, 'middle', 800)
    z.text(59, 64, 'H–H, Cl–Cl, O=O', 9.4, INK, 'middle', 600); z.text(59, 77, 'C–H (ΔEN 0,4)*', 9.4, INK, 'middle', 600)
    z.text(207, 64, 'H–Cl (0,9)  N–H (0,9)  C–O (1,0)', 9.4, INK, 'middle', 600); z.text(207, 77, 'O–H (1,4)  C–Cl (0,5)  H–F (1,9)', 9.4, INK, 'middle', 600)
    z.text(372, 64, 'Na–Cl (2,1)', 9.4, INK, 'middle', 600); z.text(372, 77, 'K–F · Mg–O', 9.4, INK, 'middle', 600)
    z.arrow(8, 92, 440, 92, 'ink', 1.6); z.text(8, 110, 'compartilhamento igual', 9, GRAY, 'start', 600); z.text(440, 110, 'transferência de e⁻', 9, GRAY, 'end', 600)
    z.text(224, 110, 'o limite 1,7 é convenção: a passagem é gradual', 9, GRAY, 'middle', 600)
    zone = z.render()
    # --- dipolo H-Cl
    d = Svg(210, 128)
    atom(d, 40, 54, 'H', 14, '#fff', INK, 13); atom(d, 150, 54, 'Cl', 18, BLUE_L, BLUE, 13)
    d.line(54, 54, 132, 54, '#7A8497', 2.4); dip(d, 52, 54, 128, 54, BLUE, 3)
    d.text(40, 30, 'δ+', 12, BLUE_D, 'middle', 800); d.text(150, 26, 'δ−', 12, BLUE_D, 'middle', 800)
    d.text(100, 82, 'vetor μ: da região δ+ para δ−', 9.2, INK, 'middle', 700)
    d.text(100, 96, '(cruz no polo positivo,', 8.8, GRAY, 'middle', 500); d.text(100, 108, 'seta no mais eletronegativo)', 8.8, GRAY, 'middle', 500)
    dv = d.render()
    return f'''
<div class="cols3">{cards}</div>
<div><h2>Eletronegatividade (escala de Pauling, valores usados nos livros didáticos)</h2>{scale}
<div class="cap">Cresce para a <b>direita</b> e para <b>cima</b> na tabela (exceto gases nobres): o flúor é o mais eletronegativo. O ENEM fornece a tabela e cobra a <i>tendência</i>.</div></div>
<div class="cols2" style="grid-template-columns: 450px 1fr">
  <div><h2>Diferença de eletronegatividade (ΔEN) → tipo de ligação</h2>{zone}<div class="cap">*C–H é tratada como praticamente apolar: por isso hidrocarbonetos são apolares.</div></div>
  <div><h2>Ligação polar</h2>{dv}</div>
</div>
<div><h2>O tipo de ligação explica as propriedades</h2>
<table><tr><th>Substância</th><th>Ligação / unidades</th><th>PF e PE</th><th>Condutividade elétrica</th><th>Solubilidade típica</th></tr>
<tr><td>NaCl, CaO</td><td>iônica · íons em retículo</td><td>altos</td><td>só fundido ou dissolvido</td><td>água (polar)</td></tr>
<tr><td>H₂O, CO₂, açúcar</td><td>covalente · moléculas</td><td>baixos a médios (forças intermoleculares)</td><td>não conduz*</td><td>depende da polaridade (Módulo B)</td></tr>
<tr><td>Cu, Fe, Al</td><td>metálica · cátions + e⁻ livres</td><td>em geral altos</td><td>conduz (sólido e líquido)</td><td>insolúveis nos solventes comuns</td></tr>
<tr><td>diamante, SiO₂</td><td>covalente em rede</td><td>muito altos</td><td>não conduz (grafite conduz)</td><td>insolúveis</td></tr></table>
<div class="cap" style="margin-top:.5mm">*Moléculas que se ionizam em água (HCl, NH₃) formam soluções que conduzem corrente.</div></div>
<div class="cols2" style="grid-template-columns:1.1fr 1fr">
{box('red','Erros comuns', '<ul><li><b>“Covalente = compartilhamento igual”:</b> só se os átomos forem iguais (ou ΔEN ≈ 0). Em HCl o par fica mais perto do Cl.</li><li><b>“NaCl é uma molécula”:</b> compostos iônicos formam retículo; não existe “molécula de NaCl” no sólido.</li><li>Ligação polar <b>não</b> garante molécula polar (próxima página).</li></ul>')}
{quiz([('Qual ligação é mais polar: O–H ou C–H?', 'O–H (ΔEN 1,4 × 0,4).'), ('Por que o NaCl dissolvido conduz corrente e o sólido não?', 'No sólido os íons estão presos no retículo; dissolvidos, ficam livres.')])}
</div>'''
page('A', 'Módulo A · 1 de 5', 'Como os átomos se unem? A eletronegatividade decide', p_lig(), key='A1')

# ======================= A2 =======================
def molfig(kind):
    s = Svg(228, 160)
    if kind == 'H2O':
        O = (104, 50); H1 = (70, 94); H2 = (138, 94)
        bond(s, *O, *H1); bond(s, *O, *H2)
        dip(s, *along(H1, O, 0.22, 0.78)[:2], *along(H1, O, 0.22, 0.78)[2:]); dip(s, *along(H2, O, 0.22, 0.78)[:2], *along(H2, O, 0.22, 0.78)[2:])
        atom(s, *O, 'O', 11, '#fff', INK, 12); atom(s, *H1, 'H', 9, '#fff', INK, 11); atom(s, *H2, 'H', 9, '#fff', INK, 11)
        lone(s, 92, 30, -30); lone(s, 116, 30, 30)
        s.text(104, 18, 'δ−', 11, BLUE_D, 'middle', 800); s.text(54, 112, 'δ+', 11, BLUE_D, 'middle', 800); s.text(154, 112, 'δ+', 11, BLUE_D, 'middle', 800)
        s.arrow(196, 100, 196, 46, 'blue', 4.2); s.text(196, 118, 'resultante', 9.6, BLUE_D, 'middle', 700)
        s.text(114, 132, 'angular · 104,5°', 10, INK, 'middle', 700); verdict(s, 114, 152, True)
    if kind == 'CO2':
        C = (114, 58); O1 = (40, 58); O2 = (188, 58)
        bond(s, *C, *O1, 'double'); bond(s, *C, *O2, 'double')
        dip(s, 108, 58, 62, 58); dip(s, 120, 58, 166, 58)
        atom(s, *C, 'C', 11, '#fff', INK, 12); atom(s, *O1, 'O', 11, '#fff', INK, 12); atom(s, *O2, 'O', 11, '#fff', INK, 12)
        s.text(40, 34, 'δ−', 11, BLUE_D, 'middle', 800); s.text(188, 34, 'δ−', 11, BLUE_D, 'middle', 800); s.text(114, 34, 'δ+', 11, BLUE_D, 'middle', 800)
        s.text(114, 96, 'resultante = 0', 11, AMBER_D, 'middle', 800); s.text(114, 110, '(vetores iguais e opostos)', 9, GRAY, 'middle', 600)
        s.text(114, 132, 'linear · 180°', 10, INK, 'middle', 700); verdict(s, 114, 152, False)
    if kind == 'NH3':
        N = (104, 44); H1 = (62, 90); H2 = (146, 90); H3 = (106, 108)
        bond(s, *N, *H1); bond(s, *N, *H2); bond(s, *N, *H3, 'wedge')
        for H in (H1, H2, H3):
            a = along(H, N, 0.3, 0.75); dip(s, *a)
        atom(s, *N, 'N', 11, '#fff', INK, 12)
        for H in (H1, H2, H3): atom(s, *H, 'H', 9, '#fff', INK, 11)
        lone(s, 104, 22, 0); s.text(104, 12, 'δ−', 11, BLUE_D, 'middle', 800)
        s.arrow(196, 96, 196, 42, 'blue', 4.2); s.text(196, 114, 'resultante', 9.6, BLUE_D, 'middle', 700)
        s.text(110, 132, 'piramidal · 107°', 10, INK, 'middle', 700); verdict(s, 114, 152, True)
    if kind in ('CH4', 'CCl4', 'CH3Cl'):
        C = (104, 62); P = {'up': (104, 14), 'dl': (58, 84), 'wf': (130, 102), 'db': (150, 36)}
        X = {'CH4': ['H']*4, 'CCl4': ['Cl']*4, 'CH3Cl': ['Cl', 'H', 'H', 'H']}[kind]
        for (k, p), l in zip(P.items(), X):
            bond(s, *C, *p, {'up': 'plain', 'dl': 'plain', 'wf': 'wedge', 'db': 'dash'}[k])
        for (k, p), l in zip(P.items(), X):
            a = along(C, p, 0.3, 0.7) if l == 'Cl' else along(p, C, 0.3, 0.6)
            if l == 'Cl': dip(s, a[0], a[1], a[2], a[3])
            else: dip(s, a[0], a[1], a[2], a[3], BLUE, 1.3, 3) if kind == 'CH4' else dip(s, a[0], a[1], a[2], a[3], BLUE, 1.6, 3)
        atom(s, *C, 'C', 11, '#fff', INK, 12)
        for (k, p), l in zip(P.items(), X): atom(s, *p, l, 10 if l == 'H' else 12, '#fff', INK, 11)
        if kind == 'CH4':
            s.text(190, 58, 'resultante', 9.6, AMBER_D, 'middle', 800); s.text(190, 70, '= 0', 10.5, AMBER_D, 'middle', 800); s.text(190, 84, 'C–H quase', 8.6, GRAY, 'middle', 600); s.text(190, 95, 'apolar', 8.6, GRAY, 'middle', 600)
        if kind == 'CCl4':
            s.text(190, 58, 'resultante', 9.6, AMBER_D, 'middle', 800); s.text(190, 70, '= 0', 10.5, AMBER_D, 'middle', 800); s.text(190, 84, '4 vetores', 8.6, GRAY, 'middle', 600); s.text(190, 95, 'se anulam', 8.6, GRAY, 'middle', 600)
        if kind == 'CH3Cl':
            s.arrow(200, 90, 200, 28, 'blue', 4.2); s.text(198, 106, 'resultante', 9.2, BLUE_D, 'middle', 700); s.text(122, 12, 'δ−', 11, BLUE_D, 'middle', 800)
        s.text(110, 132, 'tetraédrica · 109,5°' + (' (assimétrica)' if kind == 'CH3Cl' else (' (simétrica)' if kind == 'CCl4' else '')), 9.4, INK, 'middle', 700)
        verdict(s, 114, 152, kind == 'CH3Cl')
    return s.render()

def geom_table():
    rows = [('2', '0', 'Linear', '180°', 'CO₂, BeH₂, HCN'), ('3', '0', 'Trigonal plana', '120°', 'BF₃, SO₃'), ('3', '1', 'Angular', '≈ 119° (SO₂)', 'SO₂, O₃'),
            ('4', '0', 'Tetraédrica', '109,5°', 'CH₄, CCl₄, CH₃Cl'), ('4', '1', 'Piramidal', '≈ 107°', 'NH₃, PH₃'), ('4', '2', 'Angular', '≈ 104,5°', 'H₂O, H₂S')]
    t = ''.join(f'<tr><td class="center b">{a}</td><td class="center b">{b}</td><td><b>{c}</b></td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in rows)
    return f'<table><tr><th>nuvens*</th><th>pares livres</th><th>geometria</th><th>ângulo</th><th>exemplos</th></tr>{t}</table><div class="cap">*nuvens eletrônicas ao redor do átomo central = ligantes + pares livres (ligação dupla ou tripla conta como <b>uma</b> nuvem). Pares livres ocupam espaço e “empurram” os ligantes (repulsão entre nuvens).</div>'

def geom_strip():
    s = Svg(330, 112)
    specs = [('Linear', 180, [(-1, 0), (1, 0)], 0), ('Trigonal\nplana', 120, [(0, -1), (-0.87, 0.5), (0.87, 0.5)], 0), ('Angular', 104.5, [(-0.79, 0.61), (0.79, 0.61)], 2),
             ('Piramidal', 107, [(-0.9, 0.55), (0.9, 0.55), (0.0, 0.95)], 1), ('Tetraédrica', 109.5, [(0, -1), (-0.9, 0.5), (0.9, 0.5), (0.0, 0.85)], 0)]
    for i, (n, ang, lig, lp) in enumerate(specs):
        cx = 33 + i*66; cy = 44; R = 24
        for dx, dy in lig: s.line(cx, cy, cx+dx*R, cy+dy*R, '#7A8497', 2)
        for dx, dy in lig: s.circ(cx+dx*R, cy+dy*R, 5.5, '#fff', INK, 1.4)
        s.circ(cx, cy, 7, PURPLE_L, PURPLE, 1.6)
        if lp == 1: s.circ(cx-3, cy-13, 1.8, INK); s.circ(cx+3, cy-13, 1.8, INK)
        if lp == 2: s.circ(cx-8, cy-12, 1.8, INK); s.circ(cx-3, cy-14, 1.8, INK); s.circ(cx+3, cy-14, 1.8, INK); s.circ(cx+8, cy-12, 1.8, INK)
        s.text(cx, 86, n, 9, INK, 'middle', 800, lh=1.15); s.text(cx, 108, f'{ang:g}°'.replace('.', ','), 9.4, GRAY, 'middle', 700)
    return s.render()

def p_geo():
    names = [('H2O', 'H₂O  água'), ('CO2', 'CO₂  gás carbônico'), ('NH3', 'NH₃  amônia'), ('CH4', 'CH₄  metano'), ('CCl4', 'CCl₄  tetracloreto de carbono'), ('CH3Cl', 'CH₃Cl  clorometano')]
    cells = ''.join(f'<div class="card" style="padding:1.2mm 1mm"><div class="center" style="font-weight:800;font-size:8.8pt">{n}</div>{molfig(k)}</div>' for k, n in names)
    return f'''
<div class="cols2" style="grid-template-columns: 1.05fr 1fr; align-items:center">
  <div>{geom_table()}</div>
  <div>{geom_strip()}{box('blue','Ideia central',
   '<b>Polaridade da molécula = soma vetorial dos dipolos das ligações.</b><br>Cada ligação polar é um vetor (→ aponta para o mais eletronegativo). A geometria decide se os vetores <b>se cancelam</b> (molécula apolar) ou <b>sobram</b> (molécula polar, com polo δ− e polo δ+).')}</div>
</div>
<div><h2>Seis moléculas, seis somas vetoriais</h2><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:2.5mm">{cells}</div>
<div class="cap">Setas azuis finas: dipolos de cada ligação (cruz no δ+). Seta azul grossa: resultante. Esquemas de geometria sem escala; em tetraedros, cunha = para a frente, tracejado = para trás.</div></div>
<div class="cols2">
{box('red','Erro comum', '<b>CO₂ tem ligações polares e molécula apolar.</b> O par C=O é polar (ΔEN = 1,0), mas a molécula é linear: os dois vetores têm o mesmo módulo e sentidos opostos. O mesmo vale para CCl₄: quatro ligações polares, molécula apolar.')}
{box('ink','ENEM na prática', 'O enunciado quase nunca pergunta “é polar?”. Ele pergunta o que a polaridade <b>causa</b>: solubilidade em água ou em óleo, PE comparativo, extração. Classifique primeiro; conclua depois.')}
</div>'''
page('A', 'Módulo A · 2 de 5', 'Que formato tem a molécula, e os dipolos se cancelam?', p_geo(), key='A2')

# ======================= A3 =======================
def flow():
    s = Svg(700, 414)
    def pill(x, y, w, h, t, kind, size=10.5):
        c = COL[kind]; s.rect(x, y, w, h, c[2], c[0], h/2, 1.8); s.text(x+w/2, y+h/2+4, t, size, c[1], 'middle', 800)
    def dia(cx, cy, w, h, t):
        s.poly([(cx, cy-h/2), (cx+w/2, cy), (cx, cy+h/2), (cx-w/2, cy)], '#fff', INK, 1.8, close=True)
        s.text(cx, cy-(len(t.split('\n'))-1)*5.5+3.5, t, 9.6, INK, 'middle', 700, lh=1.18)
    def res(x, y, w, h, t, ex, polar):
        c = (BLUE, BLUE_D, BLUE_L) if polar else (AMBER, AMBER_D, AMBER_L)
        s.rect(x, y, w, h, c[2], c[0], 8, 2)
        s.text(x+w/2, y+18, t, 12, c[1], 'middle', 900); s.text(x+w/2, y+34, ex, 9.2, INK, 'middle', 600, lh=1.2)
    pill(190, 4, 160, 26, 'Molécula (fórmula estrutural)', 'ink')
    s.arrow(270, 30, 270, 46, 'ink', 1.8)
    dia(270, 90, 250, 84, 'Há ligações polares?\n(átomos com EN diferentes)')
    s.arrow(395, 90, 450, 90, 'ink', 1.8); s.text(412, 82, 'NÃO', 9.5, RED_D, 'middle', 800)
    res(450, 62, 140, 56, 'APOLAR', 'H₂, O₂, N₂, hidrocarbonetos', False)
    s.arrow(270, 132, 270, 160, 'ink', 1.8); s.text(282, 150, 'SIM', 9.5, GREEN_D, 'start', 800)
    dia(270, 192, 250, 62, 'Só 2 átomos?')
    s.arrow(395, 192, 450, 192, 'ink', 1.8); s.text(412, 184, 'SIM', 9.5, GREEN_D, 'middle', 800)
    res(450, 164, 140, 56, 'POLAR', 'HCl, HF, CO, NO', True)
    s.arrow(270, 223, 270, 244, 'ink', 1.8); s.text(282, 238, 'NÃO', 9.5, RED_D, 'start', 800)
    s.rect(130, 244, 280, 44, '#fff', INK, 6, 1.8)
    s.text(270, 262, 'Descubra a geometria: nº de nuvens no átomo central', 9.8, INK, 'middle', 700); s.text(270, 277, '(ligantes + pares livres) e desenhe os vetores', 9.8, INK, 'middle', 700)
    s.arrow(270, 288, 270, 308, 'ink', 1.8)
    dia(270, 342, 270, 64, 'Os vetores se cancelam?\n(simetria: soma vetorial = 0)')
    s.arrow(405, 342, 450, 330, 'ink', 1.8); s.text(426, 334, 'SIM', 9.5, GREEN_D, 'middle', 800)
    res(450, 304, 140, 52, 'APOLAR', 'CO₂, BF₃, CCl₄, CS₂, SO₃', False)
    s.path('M135,342 L40,342 L40,386 L450,386', stroke=INK, sw=1.8, marker='ink'); s.text(98, 334, 'NÃO', 9.5, RED_D, 'middle', 800)
    res(450, 362, 140, 52, 'POLAR', 'H₂O, NH₃, SO₂, CH₃Cl, CHCl₃', True)
    # atalhos
    s.rect(606, 62, 92, 156, GREEN_L, GREEN, 6, 1.4)
    s.text(652, 78, 'ATALHO', 9, GREEN_D, 'middle', 900); s.text(652, 92, 'seguro', 9, GREEN_D, 'middle', 900)
    s.text(652, 110, 'Central SEM\npar livre:', 8.8, INK, 'middle', 700, lh=1.2); s.text(652, 140, 'ligantes todos\niguais → apolar', 8.8, INK, 'middle', 500, lh=1.2)
    s.text(652, 172, 'algum diferente\n→ polar', 8.8, INK, 'middle', 500, lh=1.2)
    s.rect(606, 232, 92, 128, RED_L, RED, 6, 1.4)
    s.text(652, 248, 'ATENÇÃO', 9, RED_D, 'middle', 900); s.text(652, 266, 'Par livre no\ncentral →\nquase sempre\npolar', 8.8, INK, 'middle', 700, lh=1.2)
    s.text(652, 328, 'NH₃: ligantes\niguais, mas\né polar!', 8.8, RED_D, 'middle', 800, lh=1.2)
    return s.render()

def p_fluxo():
    return f'''
<div>{flow()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr"><div><div class="b" style="margin-bottom:1mm">Regiões <span class="t-blue">polares</span> (comuns em orgânicas)</div><div style="display:flex;gap:1.4mm;flex-wrap:wrap">{tag('blue','–OH')}{tag('blue','–COOH')}{tag('blue','C=O')}{tag('blue','–NH₂')}{tag('blue','–CONH–')}{tag('blue','–O–  (pouco)')}{tag('blue','C–Cl')}</div></div>
<div><div class="b" style="margin-bottom:1mm">Regiões <span class="t-amber">apolares</span></div><div style="display:flex;gap:1.4mm;flex-wrap:wrap">{tag('amber','–CH₃')}{tag('amber','–CH₂–')}{tag('amber','cadeia carbônica longa')}{tag('amber','anel benzênico')}</div></div></div>
<div class="cols2" style="grid-template-columns:1.05fr 1fr">
  <div>{box('purple','Moléculas orgânicas grandes: raciocine por regiões',
   'Não há um único “sim/não”. Localize: (1) heteroátomos e grupos polares (–OH, –COOH, –NH₂, C=O) → <b>região polar</b>; (2) cadeias de C–H → <b>região apolar</b>. Predomínio de cadeia → molécula majoritariamente apolar; polar na ponta + cadeia longa → <b>anfifílica</b> (Módulo B). Quanto mais heteroátomos por carbono, maior a polaridade (dica do levantamento Aprova Total).')}
  {box('red','Erros comuns',
   '<ul><li>“Ligações polares ⇒ molécula polar.” <b>Falso</b> (CO₂, CCl₄, BF₃).</li><li>“Três ligantes iguais ⇒ apolar.” <b>Falso</b> se há par livre (NH₃).</li><li>Regras de bolso valem para o átomo central <b>com ou sem</b> pares livres: sempre confira a geometria.</li></ul>')}</div>
  <div>{quiz([('Classifique: BF₃, SO₂, CHCl₃, C₂H₄, HCN.', 'BF₃ apolar (trigonal plana simétrica) · SO₂ polar (angular) · CHCl₃ polar (tetraedro assimétrico) · C₂H₄ apolar · HCN polar (linear, mas ligantes diferentes).'),
   ('CH₂Cl₂ é polar? Por quê?', 'Sim: tetraedro com ligantes diferentes (2 H e 2 Cl): os vetores não se anulam.'),
   ('Qual solvente dissolve melhor o CCl₄: água ou hexano?', 'Hexano (apolar dissolve apolar).')])}
  {box('ink','ENEM na prática','Um enunciado descreve uma substância como “simétrica e de baixa polaridade” (ex.: inseticida organoclorado, ENEM 2023, citado pelo Aprova Total) e pergunta onde ela se acumula: <b>nas gorduras</b>, não na água. Polaridade → solubilidade → destino ambiental.')}</div>
</div>'''
page('A', 'Módulo A · 3 de 5', 'Molécula polar ou apolar? Um roteiro em quatro perguntas', p_fluxo(), key='A3')

# ======================= A4 =======================
def force_fig(kind):
    s = Svg(226, 150)
    if kind == 'london':
        for cx, sig in ((58, 'A'), (164, 'B')):
            s.ell(cx, 56, 40, 26, AMBER_L, AMBER, 1.8)
        s.ell(40, 56, 22, 22, 'url(#hatch-amber)', 'none', 0)
        s.ell(58, 56, 40, 26, 'none', AMBER_D, 1.8); s.ell(164, 56, 40, 26, 'none', AMBER_D, 1.8)
        s.circ(58, 56, 5, '#fff', INK, 1.4); s.circ(164, 56, 5, '#fff', INK, 1.4)
        s.text(30, 60, 'δ−', 10, AMBER_D, 'middle', 800); s.text(86, 60, 'δ+', 10, AMBER_D, 'middle', 800)
        s.text(136, 60, 'δ−', 10, AMBER_D, 'middle', 800); s.text(192, 60, 'δ+', 10, AMBER_D, 'middle', 800)
        s.line(98, 56, 122, 56, INK, 2, '3 3'); s.text(110, 80, 'atração', 9, INK, 'middle', 700)
        s.text(58, 100, 'dipolo instantâneo', 9, INK, 'middle', 600); s.text(164, 100, 'dipolo induzido', 9, INK, 'middle', 600)
        s.text(110, 128, 'a nuvem eletrônica se deforma', 9.2, INK, 'middle', 600); s.text(110, 141, 'por instantes e induz a vizinha', 9.2, INK, 'middle', 600)
    elif kind == 'dd':
        # duas moléculas HCl alinhadas
        for x in (30, 130):
            s.ell(x+22, 56, 34, 26, BLUE_L, BLUE, 1.6)
            atom(s, x, 56, 'H', 9, '#fff', INK, 10); atom(s, x+38, 56, 'Cl', 12, '#fff', INK, 10)
            s.text(x, 34, 'δ+', 9.6, BLUE_D, 'middle', 800); s.text(x+38, 30, 'δ−', 9.6, BLUE_D, 'middle', 800)
            s.line(x+9, 56, x+26, 56, '#7A8497', 2)
        s.line(78, 64, 120, 64, INK, 1.8, '3 3'); s.text(98, 82, 'δ− ··· δ+', 9.4, INK, 'middle', 800)
        s.text(110, 112, 'polo + de uma molécula atrai', 9.2, INK, 'middle', 600); s.text(110, 125, 'o polo − da vizinha', 9.2, INK, 'middle', 600)
    else:
        O1 = (56, 70); Ha = (30, 98); Hb = (96, 70); O2 = (160, 70); Hc = (184, 98); Hd = (186, 42)
        for O, H in ((O1, Ha), (O1, Hb), (O2, Hc), (O2, Hd)): bond(s, *O, *H)
        s.line(106, 70, 148, 70, PURPLE_D, 2.8, '5 3')
        atom(s, *O1, 'O', 11, BLUE_L, BLUE, 11); atom(s, *O2, 'O', 11, BLUE_L, BLUE, 11)
        for H in (Ha, Hb, Hc, Hd): atom(s, *H, 'H', 8, '#fff', INK, 9.5)
        s.text(56, 46, 'δ−', 9.6, BLUE_D, 'middle', 800); s.text(96, 52, 'δ+', 9.6, BLUE_D, 'middle', 800); s.text(160, 46, 'δ−', 9.6, BLUE_D, 'middle', 800)
        s.label(127, 92, 'O–H···O', 10, PURPLE_D, '#fff', 800)
        s.text(110, 128, 'H ligado a F, O ou N é atraído', 9.2, INK, 'middle', 600); s.text(110, 141, 'por par livre de F, O ou N vizinho', 9.2, INK, 'middle', 600)
    return s.render()

def hydride_chart():
    s = Svg(350, 236)
    ax = Axes(s, 52, 10, 286, 182, (1.6, 5.4), (-180, 120))
    ax.frame([2, 3, 4, 5], [-160, -120, -80, -40, 0, 40, 80, 120], 'Período do elemento central (massa molar crescente →)', 'Ponto de ebulição (°C)', size=9.6, ylabel_dx=42)
    ax.s.line(ax.x0, ax.Y(0), ax.x0+ax.w, ax.Y(0), GRAY, 0.9, '3 3')
    data = {'Grupo 14 (CH₄…SnH₄)': ([-162, -112, -89, -52], INK, 's', 'ink'), 'Grupo 15 (NH₃…SbH₃)': ([-33, -88, -63, -17], PURPLE, '^', 'purple'),
            'Grupo 16 (H₂O…H₂Te)': ([100, -60, -41, -2], BLUE, 'o', 'blue'), 'Grupo 17 (HF…HI)': ([20, -85, -67, -35], ORANGE, 'd', 'orange')}
    for name, (vals, col, shp, k) in data.items():
        pts = list(zip([2, 3, 4, 5], vals)); ax.line(pts, col, 2.2)
        for x, y in pts: ax.marker(x, y, shp, col, 4.2, '#fff')
    s.label(ax.X(2)+24, ax.Y(100)-4, 'H₂O (100 °C)', 9.6, BLUE_D, '#fff', 800, 'start')
    s.label(ax.X(2)+6, ax.Y(20)+22, 'HF', 9.6, '#B94A07', '#fff', 800, 'start')
    s.label(ax.X(2)+4, ax.Y(-33)+22, 'NH₃', 9.6, PURPLE_D, '#fff', 800, 'start')
    s.label(ax.X(2)+22, ax.Y(-162)-10, 'CH₄', 9.6, INK, '#fff', 800, 'start')
    # legenda
    lx = 66; ly = 160
    for i, (name, (vals, col, shp, k)) in enumerate(data.items()):
        yy = 14 + i*0; 
    items = list(data.items())
    for i, (name, (vals, col, shp, k)) in enumerate(items):
        x = 150; y = 28 + i*15
        s.line(x, y, x+20, y, col, 2.2); ax_dummy = Axes(s, 0, 0, 1, 1, (0, 1), (0, 1))
        s.circ(x+10, y, 3.6, '#fff', col, 1.6) if shp == 'o' else (s.rect(x+6.5, y-3.5, 7, 7, '#fff', col, sw=1.6) if shp == 's' else (s.poly([(x+10, y-5), (x+15, y+4), (x+5, y+4)], '#fff', col, 1.6, close=True) if shp == '^' else s.poly([(x+10, y-5), (x+15, y), (x+10, y+5), (x+5, y)], '#fff', col, 1.6, close=True)))
        s.text(x+26, y+3.5, name, 8.8, INK, 'start', 600)
    return s.render()

def alkane_chart():
    s = Svg(330, 236)
    ax = Axes(s, 50, 10, 266, 182, (0.5, 8.5), (-180, 140))
    ax.frame(list(range(1, 9)), [-160, -120, -80, -40, 0, 40, 80, 120], 'Nº de átomos de carbono (alcano linear)', 'PE (°C)', size=9.6, ylabel_dx=38)
    ax.s.line(ax.x0, ax.Y(0), ax.x0+ax.w, ax.Y(0), GRAY, 0.9, '3 3')
    d = [(1, -162), (2, -89), (3, -42), (4, -1), (5, 36), (6, 69), (7, 98), (8, 126)]
    ax.line(d, AMBER_D, 2.4)
    for x, y in d: ax.marker(x, y, 'o', AMBER_D, 4.2, AMBER_L)
    for (x, y), n in zip(d, ['CH₄', 'C₂H₆', 'C₃H₈', 'C₄H₁₀', 'C₅H₁₂', 'C₆H₁₄', 'C₇H₁₆', 'C₈H₁₈']):
        s.text(ax.X(x), ax.Y(y) + (-9 if x >= 5 else 17), n, 8.6, INK, 'middle', 700) if x not in (1,) else s.text(ax.X(x)+12, ax.Y(y)-9, n, 8.6, INK, 'start', 700)
    s.text(ax.X(5.2), ax.Y(-120), 'só London: PE sobe', 9.4, AMBER_D, 'start', 800); s.text(ax.X(5.2), ax.Y(-137), 'com o tamanho da cadeia', 9.4, AMBER_D, 'start', 800)
    return s.render()

def forces_table():
    rows = [('CH₄, C₆H₁₄, I₂, CO₂', 'London', 'apolares'), ('HCl, CH₃Cl, SO₂, acetona', 'London + dipolo-dipolo', 'polares sem H–F/O/N'),
            ('H₂O, NH₃, HF', 'London + dipolo + <b>LH</b>', 'H–F/O/N'), ('etanol, ác. acético, metilamina', 'London + dipolo + <b>LH</b> (+ cadeia apolar)', 'O–H, N–H'),
            ('éter dimetílico, acetona', 'London + dipolo (<b>sem</b> LH)', 'H só em C: não faz LH')]
    t = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    return f'<table><tr><th>Substância</th><th>Forças que atuam</th><th>Motivo</th></tr>{t}</table>'

def p_forcas():
    cards = ''.join(f'<div class="card" style="--c:{c[0]}">{tagh}<div style="margin:1mm 0">{force_fig(k)}</div><div style="font-size:8pt">{txt}</div></div>' for k, tagh, c, txt in [
        ('london', f'<h3>{tag("amber","1 · fraca")} Dipolo instantâneo (London)</h3>', COL['amber'], '<b>Todas as moléculas.</b> É a <b>única</b> em apolares (CH₄, I₂, CO₂, hidrocarbonetos, gases nobres). Cresce com <b>massa/tamanho</b> e <b>área de contato</b>.'),
        ('dd', f'<h3>{tag("blue","2 · média")} Dipolo permanente</h3>', COL['blue'], '<b>Moléculas polares</b> sem H–F/O/N: HCl, CH₃Cl, acetona, SO₂. Soma-se à de London.'),
        ('hb', f'<h3>{tag("purple","3 · forte")} Ligação de hidrogênio</h3>', COL['purple'], '<b>H–F, H–O ou H–N</b> + par livre de F/O/N vizinho: H₂O, NH₃, HF, álcoois, ácidos carboxílicos, aminas, amidas. É interação <b>entre</b> moléculas, não ligação química.')])
    iso = Svg(330, 104)
    for i, (n, bp) in enumerate([('pentano', 36), ('2-metilbutano', 28), ('2,2-dimetilpropano', 9.5)]):
        y = 6 + i*29
        iso.text(2, y+12, n, 9.6, INK, 'start', 600); iso.rect(122, y, bp*4, 16, 'url(#hatch-amber)', AMBER_D, 2, 1.2)
        iso.text(122+bp*4+5, y+13, f'{bp:g} °C'.replace('.', ','), 9.6, INK, 'start', 800)
    iso.text(2, 100, 'mesma fórmula (C₅H₁₂), menos contato → menos London → menor PE', 8.8, GRAY, 'start', 600)
    return f'''
<div class="cols3">{cards}</div>
<div class="cols2" style="grid-template-columns: 350px 1fr">
  <div><h2>Hidretos: massa maior, PE maior… com 3 exceções</h2>{hydride_chart()}
   <div class="cap">Valores de livros-texto, arredondados. O PE sobe com a massa (mais London), exceto no 1º elemento de N, O e F: ali a <b>ligação de hidrogênio</b> eleva o PE. CH₄ não faz LH e segue a tendência.</div></div>
  <div><h2>Alcanos: só London</h2>{alkane_chart()}
   <div class="cap">Valores de livros-texto, arredondados. Cadeia maior → mais contato entre moléculas → mais London → PE maior.</div></div>
</div>
<div class="cols2" style="grid-template-columns: 1fr 1fr">
  <div><h2>Quais forças atuam?</h2>{forces_table()}
   <h3 style="margin-top:2mm">Ramificação diminui o contato (isômeros C₅H₁₂)</h3>{iso.render()}</div>
  <div>
    <div style="display:grid;grid-template-columns:auto 1fr;gap:1mm 2.4mm;align-items:center;font-size:8.3pt;margin-bottom:2mm"><b class="t-purple">↑ força</b><span>↑ PF e PE · ↓ volatilidade e pressão de vapor · ↑ viscosidade · ↑ tensão superficial</span>
      <b class="t-purple">↑ solubilidade</b><span>se soluto e solvente fazem interações do mesmo tipo (Módulo B)</span></div>
    {box('red','Erros comuns','<ul><li>“Ligação de hidrogênio é uma ligação covalente.” <b>Não</b>: é atração entre moléculas.</li><li>“H ligado a C faz LH.” <b>Não</b>: precisa ser H–F, H–O ou H–N.</li><li>Comparar só “quem tem LH”: se não há LH, compare <b>massa e superfície</b> (London).</li></ul>')}
  </div>
</div>'''
page('A', 'Módulo A · 4 de 5', 'Por que moléculas se atraem? Três interações', p_forcas(), key='A4')

# ======================= A5 =======================
def water_lattice():
    s = Svg(330, 190)
    # líquido (esquerda) e gelo (direita)
    s.text(80, 14, 'ÁGUA LÍQUIDA', 10, BLUE_D, 'middle', 800); s.text(250, 14, 'GELO', 10, BLUE_D, 'middle', 800)
    liq = [(40, 52, 20), (84, 40, 140), (120, 74, 260), (62, 96, 80), (104, 118, 200), (30, 134, 310), (76, 156, 20)]
    for (x, y, r) in liq: water_mol(s, x, y, r, 1.5)
    for a, b in [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (3, 5)]:
        s.line(liq[a][0], liq[a][1], liq[b][0], liq[b][1], PURPLE, 1.6, '3 3', op=0.8)
    s.text(80, 184, 'ligações de H se formam e se', 9, INK, 'middle', 600); s.text(80, 195, 'desfazem; moléculas mais próximas', 9, INK, 'middle', 600)
    cx, cy, R = 250, 94, 48
    pts = [(cx + R*math.cos(math.radians(60*i-90)), cy + R*math.sin(math.radians(60*i-90))) for i in range(6)]
    for i in range(6):
        a, b = pts[i], pts[(i+1) % 6]; s.line(a[0], a[1], b[0], b[1], PURPLE, 2, '3 3')
    for i, (x, y) in enumerate(pts): water_mol(s, x, y, 60*i, 1.5)
    s.text(cx, cy-2, 'espaço', 9.4, GRAY, 'middle', 700); s.text(cx, cy+10, 'vazio', 9.4, GRAY, 'middle', 700)
    s.text(250, 168, 'hexágonos abertos: arranjo rígido,', 9, INK, 'middle', 600); s.text(250, 180, 'menos denso que o líquido', 9, INK, 'middle', 600)
    s.rect(0, 0, 330, 190, 'none')
    return s.render().replace('height="190"', 'height="200"').replace('0 0 330 190', '0 0 330 200')

def bp_chart():
    s = Svg(440, 250)
    items = [('propano', 'CCC', -42, False, 'C₃H₈ · 44'), ('éter dimetílico', 'COC', -24, False, 'C₂H₆O · 46'), ('etanal', 'CC=O', 20, False, 'C₂H₄O · 44'),
             ('etanol', 'CCO', 78, True, 'C₂H₆O · 46'), ('ác. acético', 'CC(=O)O', 118, True, 'C₂H₄O₂ · 60')]
    ax = Axes(s, 46, 100, 384, 120, (0, 5), (-60, 130))
    ax.frame(None, [-40, 0, 40, 80, 120], '', 'PE (°C)', size=9.6, ylabel_dx=38)
    s.line(ax.x0, ax.Y(0), ax.x0+ax.w, ax.Y(0), INK, 1.4)
    for i, (n, smi, bp, lh, mm) in enumerate(items):
        x = ax.X(i+0.5); w = 46
        y0, y1 = ax.Y(0), ax.Y(bp)
        s.rect(x-w/2, min(y0, y1), w, abs(y1-y0), 'url(#hatch-purple)' if lh else 'url(#hatch-amber)', PURPLE_D if lh else AMBER_D, 2, 1.3)
        s.text(x, (y1-5) if bp > 0 else (y1+13), f'{bp} °C', 10, INK, 'middle', 800)
        svg, d, m = mol_svg(smi, 86, 62, hl=[('[OX2H]', 'purple')] if lh else [], bw=1.8, fs=11, pad=0.1)
        s.embed(svg, x-43, 2)
        s.text(x, 80, n, 9.2, INK, 'middle', 700); s.text(x, 91, mm, 8.4, GRAY, 'middle', 600)
        s.text(x, 240, 'faz LH' if lh else 'sem LH', 9, PURPLE_D if lh else AMBER_D, 'middle', 800)
    return s.render()

def dna_fig():
    s = Svg(330, 118)
    def pair(x, a, b, n, lab):
        s.rect(x, 18, 36, 28, GREEN_L, GREEN, 5, 1.6); s.rect(x+104, 18, 36, 28, GREEN_L, GREEN, 5, 1.6)
        s.text(x+18, 37, a, 13, GREEN_D, 'middle', 900); s.text(x+122, 37, b, 13, GREEN_D, 'middle', 900)
        for i in range(n): s.line(x+37, 26+i*8*(2.0/ n*1.0 if n==2 else 1)+ (4 if n==2 else 0), x+103, 26+i*8*(2.0/ n*1.0 if n==2 else 1)+(4 if n==2 else 0), PURPLE_D, 2.4, '5 3')
        s.text(x+70, 66, lab, 9.4, PURPLE_D, 'middle', 800)
    pair(4, 'A', 'T', 2, '2 LH'); pair(176, 'G', 'C', 3, '3 LH')
    s.text(165, 92, 'Pares de bases do DNA', 9.6, INK, 'middle', 800)
    s.text(165, 106, 'aquecer rompe LH: a dupla hélice se separa', 9.0, GRAY, 'middle', 600)
    return s.render()

def p_agua():
    return f'''
<div class="cols2" style="grid-template-columns: 330px 1fr; align-items:start">
  <div>{water_lattice()}</div>
  <div><h2>Cada propriedade da água tem causa e consequência</h2>
   <table><tr><th>Propriedade</th><th>Causa</th><th>Consequência</th></tr>
   <tr><td><b>PE alto</b> (100 °C; H₂S: −60 °C)</td><td>até 4 LH por molécula</td><td>água líquida na Terra</td></tr>
   <tr><td><b>Calor específico alto</b> (4,18 J/g·°C)</td><td>energia vai rompendo LH</td><td>clima ameno, termorregulação</td></tr>
   <tr><td><b>Gelo menos denso</b></td><td>LH impõem hexágonos abertos</td><td>gelo flutua; lagos não congelam por inteiro</td></tr>
   <tr><td><b>Tensão superficial alta</b></td><td>coesão entre moléculas da superfície</td><td>gotas; insetos andam sobre a água</td></tr>
   <tr><td><b>Bom solvente de polares</b></td><td>dipolo + LH com o soluto</td><td>meio da vida; hidratação de íons (B1)</td></tr></table>
  </div>
</div>
<div><h2>Mesma massa, PE muito diferentes: a prova dos nove da ligação de hidrogênio</h2>{bp_chart()}
<div class="cap">Valores aproximados de livros-texto. Etanol e éter dimetílico são <b>isômeros</b> (C₂H₆O): mesma massa, PE de 78 °C e −24 °C. O que mudou? O etanol tem O–H e faz LH; o éter, não.</div></div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
  <div>{box('green','Conexão com Biologia: LH sustentam o DNA e as proteínas','As duas fitas do DNA se mantêm por ligações de hidrogênio entre bases (A–T: 2; G–C: 3). Proteínas dobram-se em hélices e folhas por LH. Interações fracas, mas numerosas: estáveis o bastante e reversíveis.')}<div style="margin-top:2mm">{dna_fig()}</div></div>
  <div>{box('ink','Roteiro para comparar PE (ou PF) em uma questão','<ol><li><b>Há ligação de hidrogênio?</b> (H–F/O/N) → PE maior.</li><li>Ambas fazem LH? Compare <b>quantidade</b> de LH e a massa (ác. acético &gt; etanol).</li><li>Sem LH: <b>polar</b> (dipolo) &gt; apolar de massa semelhante.</li><li>Apolares: maior <b>massa/superfície</b> → maior PE; ramificação ↓ PE.</li></ol>')}
  <div style="margin-top:2mm">{quiz([('Por que o PE do ácido acético (118 °C) supera o do etanol (78 °C)?', 'Faz mais LH (O–H e C=O) e forma dímeros; massa maior.'), ('Por que o gelo flutua?', 'Em LH hexagonais abertas, o gelo é menos denso que a água líquida.')])}</div></div>
</div>'''
page('A', 'Módulo A · 5 de 5', 'A água é especial: a ligação de hidrogênio em ação', p_agua(), key='A5')
