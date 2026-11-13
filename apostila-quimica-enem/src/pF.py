# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import fbal, fmass, num
import math

# ================ ícones de laboratório ================
def lab_filtracao():
    s = Svg(190, 150)
    s.poly([(34, 20), (116, 20), (86, 66), (64, 66)], '#fff', GRAY, 2, close=True)
    s.poly([(42, 24), (108, 24), (80, 62), (70, 62)], '#F4F1E8', GRAY, 1.2, close=True)
    for x, y in [(66, 34), (82, 40), (74, 50), (90, 30), (58, 30)]: s.circ(x, y, 2.4, AMBER_D)
    s.rect(70, 66, 10, 12, '#fff', GRAY, 0, 1.6)
    mini_beaker(s, 36, 80, 78, 56, [(1, 'url(#dots-blue)', '')]); s.text(75, 148, 'filtração', 10, INK, 'middle', 800)
    for y in (84, 94): s.circ(75, y, 1.6, BLUE_D)
    s.text(124, 40, 'resíduo', 8.8, AMBER_D, 'start', 800); s.text(124, 52, 'sólido', 8.8, AMBER_D, 'start', 800)
    return s.render()
def lab_decant():
    s = Svg(150, 150)
    mini_beaker(s, 34, 14, 82, 106, [(0.22, 'url(#hatch-amber)', ''), (0.62, 'url(#dots-blue)', ''), (0.16, '#C9B58A', '')])
    s.text(75, 44, 'óleo', 9.6, AMBER_D, 'middle', 800); s.text(75, 80, 'água', 9.6, BLUE_D, 'middle', 800); s.text(75, 106, 'sedim.', 8.2, INK, 'middle', 800)
    s.text(75, 140, 'decantação / funil', 10, INK, 'middle', 800)
    return s.render()
def lab_centrifuga():
    s = Svg(150, 150)
    s.circ(75, 64, 46, '#F4F6FA', GRAY, 2); s.circ(75, 64, 4, GRAY)
    for a in (0, 120, 240):
        r = math.radians(a - 90); x1, y1 = 75 + 10*math.cos(r), 64 + 10*math.sin(r); x2, y2 = 75 + 40*math.cos(r), 64 + 40*math.sin(r)
        s.line(x1, y1, x2, y2, INK, 9, cap='butt'); s.line(x1+(x2-x1)*0.55, y1+(y2-y1)*0.55, x2, y2, AMBER_D, 7, cap='butt')
    s.path('M38,20 A46,46 0 0 1 112,22', stroke=ORANGE, sw=2.2, marker='orange')
    s.text(75, 136, 'centrifugação', 10, INK, 'middle', 800); s.text(75, 148, 'o mais denso vai ao fundo', 8.4, GRAY, 'middle', 600)
    return s.render()

def chroma():
    s = Svg(330, 200)
    s.rect(30, 156, 150, 34, 'url(#dots-blue)', GRAY, 4, 2)   # solvente
    s.path('M20,14 L20,184 Q20,194 30,194 L180,194 Q190,194 190,184 L190,14', stroke=GRAY, sw=2.4)
    s.rect(70, 14, 70, 150, '#FFFDF6', INK, 2, 1.8)
    s.line(70, 30, 140, 30, ORANGE, 1.6, '4 3'); s.text(146, 33, 'frente do solvente', 9.2, ORANGE_D, 'start', 800)
    s.line(70, 148, 140, 148, GRAY, 1.4, '3 3'); s.text(146, 151, 'linha de aplicação', 9.2, GRAY, 'start', 700)
    for x, y, col, r in [(84, 48, AMBER, 6), (105, 88, PURPLE, 7), (126, 128, GREEN, 6)]: s.circ(x, y, r, col, INK, 1.2)
    for x in (84, 105, 126): s.circ(x, 148, 3.4, GRAY)
    s.line(84, 148, 84, 54, INK, 1, '2 2', marker='ink')
    s.text(84, 66, 'A', 9, INK, 'middle', 900); s.text(105, 108, 'B', 9, INK, 'middle', 900); s.text(126, 146, 'C', 9, INK, 'middle', 900)
    s.text(196, 50, 'A: pouco retido', 9, AMBER_D, 'start', 700); s.text(196, 62, '→ sobe mais', 9, AMBER_D, 'start', 700)
    s.text(196, 100, 'B: intermediário', 9, PURPLE_D, 'start', 700)
    s.text(196, 128, 'C: muito retido na', 9, GREEN_D, 'start', 700); s.text(196, 140, 'fase estacionária', 9, GREEN_D, 'start', 700); s.text(196, 152, '→ sobe menos', 9, GREEN_D, 'start', 700)
    s.text(196, 178, 'Rf = d(composto)', 10, INK, 'start', 900); s.text(196, 191, '÷ d(solvente)', 10, INK, 'start', 900)
    s.text(76, 10, 'fase estacionária (papel/sílica)', 9, INK, 'start', 700)
    return s.render()

def p_F1():
    rows = [('sólido + sólido', 'peneiração', 'tamanho dos grãos', 'areia + cascalho'), ('sólido + sólido', 'separação magnética', 'magnetismo', 'ferro + areia'),
            ('sólido + sólido', 'dissolução fracionada', 'solubilidade', 'sal + areia (água, depois filtra)'), ('sólido + líquido', 'decantação, filtração, centrifugação', 'densidade · tamanho · rotação', 'água barrenta'),
            ('líquido + líquido imiscíveis', 'funil de separação', 'imiscibilidade/densidade', 'óleo + água'), ('sólido dissolvido + líquido', 'destilação simples · evaporação', 'PE muito diferentes', 'água do mar'),
            ('líquido + líquido miscíveis', 'destilação fracionada', 'PE próximos', 'petróleo, etanol + água'), ('gás + gás', 'liquefação fracionada', 'PE (do ar líquido)', 'N₂, O₂ e Ar do ar'),
            ('componentes de uma mistura', 'extração por solvente', '<b>polaridade</b>', 'café, óleos essenciais'), ('traços de componentes', 'cromatografia', 'afinidade com fases', 'pigmentos, anabolizantes')]
    het = ''.join(f'<tr><td style="background:{"#fff" if i < 5 else BLUE_L}"><b>{a}</b></td><td><b class="t-blue">{b}</b></td><td>{c}</td><td>{d}</td></tr>' for i, (a, b, c, d) in enumerate(rows))
    return f'''
<div><h2>Qual método? A propriedade que difere manda</h2>
<table><tr><th>Mistura</th><th>Método</th><th>Propriedade explorada</th><th>Exemplo</th></tr>{het}</table>
<div class="cap">Linhas brancas: misturas <b>heterogêneas</b> (mais de uma fase). Linhas azuladas: <b>homogêneas</b> (uma fase) ou análises. Mistura heterogênea é separada por processos <b>físicos mecânicos</b>; homogênea, por mudança de fase ou solubilidade.</div></div>
<div class="cols3" style="grid-template-columns:repeat(3,1fr)">{lab_filtracao()}{lab_decant()}{lab_centrifuga()}</div>
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
  <div><h2>Cromatografia: quem “gosta mais” do quê</h2>{chroma()}</div>
  <div>{box('ink','Extração por solvente = polaridade em ação','Escolhe-se um solvente que dissolva <b>só o que interessa</b>: cafeína e açúcares do café em água quente; óleos essenciais em solvente apolar; iodo da água usando um líquido apolar (o I₂ passa para a fase apolar). Depois se separam as fases (funil) ou se evapora o solvente.')}
  <div style="margin-top:2mm">{box('green','ENEM na prática','Enunciados costumam descrever a separação e perguntar o <b>método</b> pela propriedade usada (ex.: centrifugação de isótopos de UF₆ gasoso por diferença de massa, ENEM 2022 via Aprova Total) ou o <b>estágio</b> de uma estação onde ocorre determinada separação.')}</div>
  <div style="margin-top:2mm">{box('red','Erros comuns','<ul><li>Decantação <b>não</b> separa líquidos miscíveis.</li><li>Filtração separa sólido de líquido, mas <b>não</b> remove sal dissolvido.</li><li>Evaporação perde o solvente; destilação o <b>recupera</b>.</li></ul>')}</div></div>
</div>'''
page('F', 'Módulo F · 1 de 4', 'Separação de misturas: qual método usar?', p_F1(), key='F1')

# ================ F2: destilação ================
def still(frac=False):
    s = Svg(340, 260)
    def g(inner, rot, cx, cy): s.add(f'<g transform="rotate({rot} {cx} {cy})">{inner}</g>')
    top = 70 if frac else 120          # y do bocal
    cx = 100
    # chama
    s.poly([(cx-14, 250), (cx, 224), (cx+14, 250)], '#FFC94D', ORANGE, 1.6, close=True); s.rect(cx-22, 250, 44, 6, GRAY, None, 2)
    # balão
    s.circ(cx, 190, 38, '#fff', INK, 2.2)
    s.path(f'M{cx-37},192 A37,37 0 0 0 {cx+37},192 Z', 'url(#dots-blue)', 'none', 0)
    s.rect(cx-9, top, 18, 190-38-top+8, '#fff', INK, 0, 2.2)
    s.rect(cx-14, top-8, 28, 8, '#C9A66B', INK, 2, 1.4)  # rolha
    s.circ(cx-14, 200, 2.4, BLUE_D); s.circ(cx+10, 208, 2.4, BLUE_D); s.circ(cx+2, 190, 2.4, BLUE_D)
    if frac:
        s.rect(cx-10, 44, 20, 80, '#fff', INK, 0, 2.2)
        for y in range(52, 122, 9): s.circ(cx, y, 3.4, LGRAY, GRAY, 1)
        s.text(cx-16, 70, 'coluna de', 9, PURPLE_D, 'end', 800); s.text(cx-16, 81, 'fracionamento', 9, PURPLE_D, 'end', 800)
        s.line(cx, 24, cx, 54, INK, 2.4); s.circ(cx, 58, 4, RED, INK, 1.2); s.text(cx+8, 24, 'termômetro', 9, INK, 'start', 700)
        yb = 44; s.rect(cx-14, 36, 28, 8, '#C9A66B', INK, 2, 1.4)
        s.path(f'M{cx+10},{yb+6} L150,{yb+6}', stroke=INK, sw=2.4)
        cond_y = yb + 6
    else:
        s.line(cx, top-30, cx, top+16, INK, 2.4); s.circ(cx, top+12, 4, RED, INK, 1.2); s.text(cx+8, top-24, 'termômetro', 9, INK, 'start', 700)
        s.path(f'M{cx+9},{top+4} L150,{top+4}', stroke=INK, sw=2.4); cond_y = top + 4
    # condensador (rotacionado)
    inner = Svg(0, 0)
    L = 140
    inner.rect(150, cond_y-9, L, 18, '#EAF3FD', INK, 3, 2); inner.rect(156, cond_y-3, L-12, 6, '#fff', GRAY, 3, 1.2)
    g(''.join(inner.p), 22, 150, cond_y)
    ex = 150 + L*math.cos(math.radians(22)); ey = cond_y + L*math.sin(math.radians(22))
    s.line(ex-6, ey+2, ex-2, ey+22, INK, 2.2)
    s.poly([(ex-18, ey+54), (ex+8, ey+54), (ex+2, ey+30), (ex-12, ey+30)], '#fff', INK, 2, close=True)
    s.circ(ex-5, ey+46, 1.8, BLUE_D); s.circ(ex-9, ey+49, 1.8, BLUE_D)
    s.text(ex-8, ey+72, 'destilado', 9.4, BLUE_D, 'middle', 800)
    # água
    s.arrow(ex-4, ey-24, ex-14, ey-8, 'blue', 2); s.text(ex-40, ey-28, 'água entra', 8.8, BLUE_D, 'start', 800)
    s.arrow(172, cond_y-2, 166, cond_y-22, 'blue', 2); s.text(172, cond_y-26, 'água sai', 8.8, BLUE_D, 'start', 800)
    s.text(cx, 270 if False else 244, '', 9)
    s.text(cx+44, 206, 'mistura', 9, INK, 'start', 800)
    return s.render()

def stills():
    return f'''<div class="cols2" style="grid-template-columns:1fr 1fr"><div class="card"><h3>{tag('blue','simples')} Destilação simples</h3>{still(False)}</div><div class="card"><h3>{tag('purple','fracionada')} Destilação fracionada</h3>{still(True)}</div></div>'''

def temp_curves():
    s = Svg(340, 156)
    a = Axes(s, 40, 10, 130, 88, (0, 10), (60, 110)); a.frame(None, [80, 100], 'volume destilado', 'T vapor (°C)', size=8.6, ylabel_dx=32, xlabel_dy=24)
    a.line([(0, 98), (0.6, 100), (9.5, 100), (10, 100)], BLUE, 2.4); s.text(a.X(5), a.Y(100)-6, 'só a água destila', 8.8, BLUE_D, 'middle', 800)
    b = Axes(s, 210, 10, 120, 88, (0, 10), (60, 110)); b.frame(None, [80, 100], 'volume destilado', '', size=8.6, xlabel_dy=24)
    b.line([(0, 70), (0.4, 78), (4, 78.4), (4.6, 90), (5.2, 99), (10, 100)], PURPLE, 2.4)
    s.text(b.X(2.2), b.Y(78)-6, 'etanol', 8.8, PURPLE_D, 'middle', 800); s.text(b.X(7.6), b.Y(100)+12, 'água', 8.8, PURPLE_D, 'middle', 800)
    s.text(105, 148, 'água + sal', 9, GRAY, 'middle', 700); s.text(270, 148, 'etanol + água', 9, GRAY, 'middle', 700)
    return s.render()

def petroleo():
    s = Svg(230, 250)
    s.rect(70, 14, 70, 200, '#F4F6FA', INK, 8, 2)
    fr = [('gases (GLP)', 'C₁–C₄', '< 40 °C', 24, '#E7E9EE'), ('gasolina', 'C₅–C₁₀', '40–180', 56, AMBER_L), ('querosene', 'C₁₁–C₁₃', '180–250', 88, AMBER_L), ('diesel', 'C₁₃–C₁₇', '250–350', 122, '#FFE0A0'), ('lubrificantes', 'C₁₈–C₂₀', '350–400', 154, '#FFD27A'), ('asfalto (resíduo)', '> C₂₀', '> 400', 186, '#E6C48A')]
    for n, c, t, y, col in fr:
        s.rect(70, y, 70, 32, col, INK, 0, 1.4); s.text(150, y+13, n, 9.6, INK, 'start', 800); s.text(150, y+26, f'{c} · {t}', 8.6, GRAY, 'start', 600)
    s.arrow(54, 190, 54, 24, 'orange', 2.4); s.text(50, 112, 'temperatura menor', 8.6, ORANGE_D, 'middle', 800, rot=-90)
    s.text(70, 230, 'cadeias maiores → mais London', 9, AMBER_D, 'start', 800); s.text(70, 243, '→ PE maior → saem embaixo', 9, AMBER_D, 'start', 800)
    return s.render()

def p_F2():
    return f'''
<div><h2>Destilação simples × fracionada</h2>{stills()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 <div><table><tr><th></th><th>Simples</th><th>Fracionada</th></tr>
 <tr><td><b>Mistura</b></td><td>sólido dissolvido em líquido</td><td>líquidos miscíveis de PE <b>próximos</b></td></tr>
 <tr><td><b>Diferença</b></td><td>vaporiza só o líquido</td><td><b>coluna</b>: vaporiza e condensa várias vezes (pratos/esferas): enriquece o mais volátil</td></tr>
 <tr><td><b>Exemplos</b></td><td>água do mar → água; água destilada</td><td>petróleo, ar líquido, etanol + água</td></tr>
 <tr><td><b>Princípio</b></td><td colspan="2">diferença de <b>ponto de ebulição</b> (forças intermoleculares: Módulo A)</td></tr></table>
 <div class="cap">Condensador: a água entra pela parte <b>de baixo</b> e sai por cima, para o tubo ficar sempre cheio. Etanol + água forma <i>azeótropo</i> (≈ 96% de etanol): a destilação não passa disso.</div></div>
 <div>{temp_curves()}<div class="cap">Substância pura: T constante enquanto destila. Mistura de líquidos: patamares, um por componente (o mais volátil primeiro).</div></div>
</div>
<div class="cols2" style="grid-template-columns:240px 1fr; align-items:start">
 <div><h2>Refino do petróleo</h2>{petroleo()}</div>
 <div style="padding-top:6mm">{box('amber','Por que o petróleo se separa em frações?','Petróleo é mistura de <b>hidrocarbonetos</b> (apolares). Só há London: quanto <b>maior a cadeia</b>, maior o PE (gráfico dos alcanos, Módulo A). Na torre, o mais leve (gases, gasolina) sobe e condensa no topo; o mais pesado (asfalto) sai pela base.')}
 <div style="margin-top:2mm">{box('red','Erros comuns','<ul><li>“Destilação fracionada separa sólidos.” <b>Não</b>: separa <b>líquidos</b> miscíveis.</li><li>Termômetro <b>abaixo</b> da saída para o condensador mede a temperatura do vapor <b>errada</b>: o bulbo fica na altura do bocal lateral.</li><li>Petróleo ≠ combustível pronto: as frações passam por <b>craqueamento e refino</b> (reações químicas).</li></ul>')}</div>
 <div style="margin-top:2mm">{quiz([('Que método separa etanol (PE 78 °C) de água (100 °C)?', 'Destilação fracionada (líquidos miscíveis de PE próximos).')])}</div></div>
</div>'''
page('F', 'Módulo F · 2 de 4', 'Destilação simples × fracionada e o refino do petróleo', p_F2(), key='F2')

# ================ F3: tratamento de água e esgoto ================
def agua_flow():
    s = Svg(700, 190)
    steps = [('Captação', 'manancial; grades\nretêm sólidos\ngrandes', 'ink', 'físico'), ('Coagulação\ne floculação', 'Al₂(SO₄)₃ + Ca(OH)₂\n→ flocos de Al(OH)₃', 'orange', 'químico'),
             ('Decantação', 'flocos com sujeira\nvão ao fundo', 'ink', 'físico'), ('Filtração', 'areia, cascalho e\ncarvão retêm\no restante', 'ink', 'físico'),
             ('Desinfecção', 'cloro (Cl₂ ou NaClO)\nelimina micro-\norganismos', 'orange', 'químico'), ('Correção de pH\ne fluoretação', 'cal/soda ajustam\no pH; flúor\nprevine cáries', 'orange', 'químico')]
    w = 104; gap = 12.4
    for i, (t, d, k, ty) in enumerate(steps):
        x = 2 + i*(w+gap); c = COL[k]
        s.rect(x, 12, w, 118, c[2], c[0], 8, 2.2)
        s.text(x+w/2, 32 if '\n' in t else 38, t, 10.4, c[1], 'middle', 900, lh=1.15)
        s.text(x+w/2, 66, d, 8.8, INK, 'middle', 600, lh=1.22)
        s.rect(x+w/2-24, 108, 48, 14, '#fff', c[0], 7, 1.2); s.text(x+w/2, 118.5, ty, 8.6, c[1], 'middle', 800)
        s.text(x+9, 24, str(i+1), 11, GRAY, 'middle', 900)
        if i < len(steps)-1: s.arrow(x+w+1, 70, x+w+gap-1, 70, 'ink', 2)
    s.arrow(4, 150, 696, 150, 'green', 2.2)
    s.text(4, 170, 'Entrada: água bruta (turva, com micro-organismos)', 9.6, GRAY, 'start', 700); s.text(696, 170, 'Saída: água potável → reservatório → distribuição', 9.6, GRAY, 'end', 700)
    return s.render()

def esgoto_flow():
    s = Svg(700, 164)
    steps = [('Gradeamento', 'retém lixo', 'ink'), ('Caixa de areia', 'areia sedimenta', 'ink'), ('Decantador\nprimário', 'lodo primário', 'ink'), ('Tratamento\nbiológico', 'micro-organismos\ndegradam matéria\norgânica', 'green'), ('Decantador\nsecundário', 'separa biomassa', 'ink'), ('Desinfecção', 'cloro ou UV', 'orange')]
    w = 104; gap = 15.2
    for i, (t, d, k) in enumerate(steps):
        x = 2 + i*(w+gap); c = COL[k]
        s.rect(x, 8, w, 72, c[2], c[0], 8, 2.2); s.text(x+w/2, 30 if '\n' in t else 38, t, 10, c[1], 'middle', 900, lh=1.15); s.text(x+w/2, 62 if '\n' not in d else 56, d, 8.6, INK, 'middle', 600, lh=1.2)
        if i < len(steps)-1: s.arrow(x+w+1, 44, x+w+gap-1, 44, 'ink', 2)
    s.text(350, 108, 'Aeróbio (lodos ativados): O₂ injetado → CO₂ + H₂O + biomassa', 9.6, GREEN_D, 'middle', 800)
    s.text(350, 124, 'Anaeróbio (biodigestor, sem O₂): matéria orgânica → CH₄ + CO₂ (biogás, fonte de energia)', 9.6, GREEN_D, 'middle', 800)
    s.text(350, 148, 'Saída: efluente tratado → corpo receptor (rio)', 9.6, GRAY, 'middle', 700)
    return s.render()

def p_F3():
    fbal('coagulação: Al2(SO4)3 + 3 Ca(OH)2 → 2 Al(OH)3 + 3 CaSO4', [(1, 'Al2(SO4)3'), (3, 'Ca(OH)2')], [(2, 'Al(OH)3'), (3, 'CaSO4')])
    fbal('cloração: Cl2 + H2O → HClO + HCl', [(1, 'Cl2'), (1, 'H2O')], [(1, 'HClO'), (1, 'HCl')])
    fbal('biogás: C6H12O6 → 3 CH4 + 3 CO2', [(1, 'C6H12O6')], [(3, 'CH4'), (3, 'CO2')])
    return f'''
<div><h2>Estação de tratamento de água (ETA)</h2>{agua_flow()}<div class="small" style="margin-top:-1mm">{tag('orange','laranja')} etapas com <b>transformação química</b> · cinza: processos <b>físicos</b>.</div></div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('orange','O que acontece na coagulação','Sulfato de alumínio + base (cal) formam <b>Al(OH)₃</b> gelatinoso e insolúvel: Al₂(SO₄)₃ + 3 Ca(OH)₂ → 2 Al(OH)₃ ↓ + 3 CaSO₄. Os flocos <b>adsorvem</b> partículas e coloides (que são tão pequenos que nunca decantariam sozinhos) e depois <b>decantam</b>.')}
 {box('orange','O que acontece na cloração','Cl₂ + H₂O ⇌ HClO + HCl. O <b>ácido hipocloroso</b> (HClO) é o desinfetante, que oxida e inativa os micro-organismos. Por isso o pH deve ser mantido controlado: HClO predomina em pH menos básico.')}
</div>
<div><h2>Estação de tratamento de esgoto (ETE)</h2>{esgoto_flow()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('green','Por que tratar o esgoto?','O esgoto tem alta <b>DBO</b> (demanda bioquímica de oxigênio): os micro-organismos que degradam a matéria orgânica consomem O₂ da água. Sem tratamento, o O₂ dissolvido cai (Módulo B) e ocorre <b>eutrofização</b> (página seguinte). Além disso, o lodo anaeróbio rende biogás (CH₄), combustível renovável.')}
 {box('red','Erros comuns','<ul><li>Filtração <b>não</b> elimina micro-organismos: é a <b>desinfecção</b> que o faz.</li><li>Coagulação ≠ decantação: a primeira é <b>reação química</b> (forma o floco); a segunda, separação física.</li><li>Água <b>tratada</b> não é água <b>destilada</b>: contém sais dissolvidos, cloro residual, flúor.</li></ul>')}
</div>
{quiz([('Em qual etapa da ETA ocorre uma reação química que forma um sólido insolúvel?', 'Coagulação/floculação: Al³⁺ + OH⁻ → Al(OH)₃ ↓.'), ('Por que o esgoto lançado sem tratamento mata peixes?', 'A matéria orgânica é degradada por micro-organismos que consomem o O₂ dissolvido.')])}'''
page('F', 'Módulo F · 3 de 4', 'Do manancial à torneira, e do vaso ao rio: tratamento de água e esgoto', p_F3(), key='F3')

# ================ F4: química ambiental ================
def eutro_flow():
    s = Svg(700, 120)
    steps = [('Excesso de N e P', 'esgoto, fertilizantes,\ndetergentes com fosfato', 'green'), ('Algas e cianobactérias\nse multiplicam', 'floração: água verde', 'green'), ('Morte e\ndecomposição', 'bactérias aeróbias\nconsomem O₂', 'orange'),
             ('O₂ dissolvido cai', 'peixes morrem', 'red'), ('Anaerobiose', 'H₂S, CH₄, mau cheiro', 'red')]
    w = 120; gap = 25
    for i, (t, d, k) in enumerate(steps):
        x = 2 + i*(w+gap); c = COL[k]
        s.rect(x, 6, w, 76, c[2], c[0], 8, 2.2); s.text(x+w/2, 24, t, 9.8, c[1], 'middle', 900, lh=1.15); s.text(x+w/2, 58 if '\n' not in t else 62, d, 8.6, INK, 'middle', 600, lh=1.2)
        if i < len(steps)-1: s.arrow(x+w+1, 44, x+w+gap-1, 44, 'ink', 2)
    s.text(350, 104, '↻ O ciclo se agrava: peixes mortos e algas mortas fornecem mais matéria orgânica', 9.6, RED_D, 'middle', 800)
    return s.render()

def p_F4():
    fbal('SO2 → SO3', [(2, 'SO2'), (1, 'O2')], [(2, 'SO3')]); fbal('SO3 + H2O → H2SO4', [(1, 'SO3'), (1, 'H2O')], [(1, 'H2SO4')])
    fbal('N2 + O2 → 2 NO (motor)', [(1, 'N2'), (1, 'O2')], [(2, 'NO')]); fbal('3 NO2 + H2O → 2 HNO3 + NO', [(3, 'NO2'), (1, 'H2O')], [(2, 'HNO3'), (1, 'NO')])
    fbal('chuva normal: CO2 + H2O → H2CO3', [(1, 'CO2'), (1, 'H2O')], [(1, 'H2CO3')]); fbal('mármore × chuva ácida: CaCO3 + H2SO4 → CaSO4 + CO2 + H2O', [(1, 'CaCO3'), (1, 'H2SO4')], [(1, 'CaSO4'), (1, 'CO2'), (1, 'H2O')])
    fbal('precipitação de metal: Pb(NO3)2 + Na2S → PbS + 2 NaNO3', [(1, 'Pb(NO3)2'), (1, 'Na2S')], [(1, 'PbS'), (2, 'NaNO3')])
    poluentes = [('CO', 'combustão incompleta', 'liga-se à hemoglobina (tóxico)'), ('SO₂', 'queima de carvão e óleo com S', 'chuva ácida; irritante respiratório'), ('NOₓ', 'motores (N₂ + O₂ em alta T), queimadas', 'chuva ácida, <i>smog</i>, ozônio'),
                 ('O₃ (baixa atm.)', 'formado por NOₓ + COV + luz', 'poluente secundário, irritante'), ('CFC', 'refrigeração, aerossóis antigos', 'destrói O₃ estratosférico; Protocolo de Montreal'), ('CO₂ e CH₄', 'combustíveis fósseis, pecuária, aterros', 'efeito estufa (absorvem IV)')]
    t = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in poluentes)
    return f'''
<div class="cols2" style="grid-template-columns:1.05fr 1fr">
 <div><h2>Poluentes atmosféricos</h2><table><tr><th>Poluente</th><th>Origem</th><th>Efeito</th></tr>{t}</table></div>
 <div><h2>Chuva ácida: as reações</h2>
 {box('orange','Enxofre e nitrogênio viram ácidos','<b>S + O₂ → SO₂</b> · 2 SO₂ + O₂ → 2 SO₃ · <b>SO₃ + H₂O → H₂SO₄</b><br><b>N₂ + O₂ → 2 NO</b> (motor, alta T) · 2 NO + O₂ → 2 NO₂ · 3 NO₂ + H₂O → 2 HNO₃ + NO<br>A chuva “normal” já é ácida (pH ≈ 5,6): CO₂ + H₂O ⇌ H₂CO₃.')}
 <div style="margin-top:1.6mm">{box('red','Consequências e correção','Mármore e calcário <b>corroem</b>: CaCO₃ + H₂SO₄ → CaSO₄ + CO₂ + H₂O. Solos e lagos acidificam: <b>calagem</b> (CaO ou CaCO₃) neutraliza. Na fonte: dessulfurização de combustíveis e conversores catalíticos.')}</div></div>
</div>
<div><h2>Eutrofização: o ciclo que esgota o oxigênio</h2>{eutro_flow()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('blue','Efeito estufa × aquecimento global','Gases como <b>CO₂, CH₄, N₂O e vapor d’água</b> absorvem radiação infravermelha emitida pela Terra e a reemitem: o efeito estufa natural mantém o planeta habitável (≈ 15 °C). A queima de combustíveis fósseis e o desmatamento <b>intensificam</b> o efeito, elevando a concentração de CO₂ e a temperatura média.')}
 {box('purple','Camada de ozônio: catálise que destrói','Na estratosfera, o O₃ absorve UV-B. Sob UV, o CFC libera Cl•: <b>Cl• + O₃ → ClO• + O₂</b>; <b>ClO• + O → Cl• + O₂</b>. O Cl• é regenerado (<b>catalisador</b>, Módulo H): um átomo destrói milhares de O₃. Não confundir com o O₃ de baixa altitude, que é poluente.')}
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('green','Contaminação e remediação',
 '<ul><li><b>Biorremediação:</b> bactérias degradam hidrocarbonetos (derrames de petróleo).</li><li><b>Fitorremediação:</b> plantas absorvem metais do solo.</li><li><b>Adsorção:</b> carvão ativado retém orgânicos apolares.</li><li><b>Precipitação:</b> Pb²⁺ + S²⁻ → PbS ↓ remove metais pesados da água.</li><li><b>Neutralização:</b> base ou calcário contra efluentes ácidos.</li></ul>')}
 <div>{box('amber','Bioacumulação e biomagnificação','Poluentes <b>lipofílicos</b> (DDT, PCBs, aldrin) e Hg orgânico não são excretados e se acumulam na gordura: a concentração <b>aumenta a cada nível da cadeia alimentar</b> (Módulo B).')}
 <div style="margin-top:1.6mm">{quiz([('Por que o H₂SO₄ da chuva ácida corrói o mármore (CaCO₃)?', 'O ácido reage com o carbonato: forma sal solúvel (CaSO₄), CO₂ e água.'), ('Por que o excesso de fósforo na água pode matar peixes?', 'Estimula algas; ao morrer, sua decomposição consome O₂ dissolvido (eutrofização).')])}</div></div>
</div>'''
page('F', 'Módulo F · 4 de 4', 'Química ambiental: ar, chuva ácida, eutrofização e remediação', p_F4(), key='F4')
