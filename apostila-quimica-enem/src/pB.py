# -*- coding: utf-8 -*-
from lib import *
from figs import *
from molsvg import mol_svg, semantic_hl, phospholipid_hl, match, parse
from pA import atom, water_mol
import math, random

def ms(smi, w, h, **kw):
    return mol_svg(smi, w, h, **kw)[0]

# ======================= B1 =======================
def polarity_scale():
    s = Svg(700, 92)
    cells = [('hexano', 'gasolina', 'a'), ('óleo', 'vegetal', 'a'), ('CCl₄', 'benzeno', 'a'), ('éter', 'dietílico', 'm'), ('acetona', '', 'm'), ('etanol', '', 'p'), ('água', '', 'p'), ('NaCl', '(íons)', 'p')]
    w = 84; x0 = 14
    for i, (a, b, k) in enumerate(cells):
        x = x0 + i*(w+2)
        fill = {'a': 'url(#hatch-amber)', 'm': '#EEF0F4', 'p': 'url(#dots-blue)'}[k]; st = {'a': AMBER_D, 'm': GRAY, 'p': BLUE_D}[k]
        s.rect(x, 24, w, 34, fill, st, 5, 1.6)
        s.label(x+w/2, 46, a, 10.5, st, '#fff', 800)
        if b: s.text(x+w/2, 72, b, 9, INK, 'middle', 600)
    s.text(14, 14, 'APOLAR', 10, AMBER_D, 'start', 900); s.text(686, 14, 'POLAR', 10, BLUE_D, 'end', 900); s.text(350, 14, 'intermediário', 9.4, GRAY, 'middle', 700)
    s.arrow(100, 87, 600, 87, 'ink', 1.4); s.text(350, 84, '', 8)
    return s.render()

def beaker_fig(kind):
    s = Svg(150, 128)
    if kind == 'oil':
        mini_beaker(s, 25, 14, 100, 92, [(0.4, 'url(#hatch-amber)', 'óleo'), (0.6, 'url(#dots-blue)', 'água')])
        s.line(27, 14+92*0.18+(92-4-92*0.18)*0.4, 123, 14+92*0.18+(92-4-92*0.18)*0.4, INK, 1.4)
        s.text(75, 46, 'óleo', 10, AMBER_D, 'middle', 800); s.text(75, 86, 'água', 10, BLUE_D, 'middle', 800)
        s.text(75, 122, 'imiscíveis: 2 fases', 9.4, RED_D, 'middle', 800)
    elif kind == 'eth':
        mini_beaker(s, 25, 14, 100, 92, [(1, 'url(#dots-blue)', '')])
        s.text(75, 56, 'água +', 10, BLUE_D, 'middle', 800); s.text(75, 70, 'etanol', 10, BLUE_D, 'middle', 800)
        s.text(75, 122, 'miscíveis: 1 fase', 9.4, GREEN_D, 'middle', 800)
    else:
        mini_beaker(s, 25, 14, 100, 92, [(1, 'url(#hatch-amber)', '')])
        s.text(75, 56, 'óleo +', 10, AMBER_D, 'middle', 800); s.text(75, 70, 'hexano', 10, AMBER_D, 'middle', 800)
        s.text(75, 122, 'miscíveis: 1 fase', 9.4, GREEN_D, 'middle', 800)
    return s.render()

def hydration():
    s = Svg(410, 262)
    s.text(6, 14, '① retículo cristalino', 10, INK, 'start', 800); s.text(176, 14, '② íons hidratados em solução', 10, INK, 'start', 800)
    for r in range(4):
        for c in range(4):
            x, y = 26 + c*30, 40 + r*30; pos = (r + c) % 2 == 0
            s.circ(x, y, 9.5 if pos else 13, '#fff' if pos else LGRAY, INK, 1.4); s.text(x, y+4, '+' if pos else '−', 11, INK, 'middle', 800)
    s.arrow(150, 96, 184, 96, 'ink', 2)
    def wat_to(x, y, tx, ty, away=False):
        ux, uy = tx-x, ty-y
        if away: ux, uy = -ux, -uy
        water_mol(s, x, y, math.degrees(math.atan2(ux, -uy)), 1.7)
    cx, cy = 232, 86
    s.circ(cx, cy, 10.5, '#fff', INK, 1.6); s.text(cx, cy+4, '+', 12, INK, 'middle', 800)
    for dx, dy in [(0, -34), (34, 0), (0, 34), (-34, 0)]: wat_to(cx+dx, cy+dy, cx, cy)
    cx2, cy2 = 336, 86
    s.circ(cx2, cy2, 14, LGRAY, INK, 1.6); s.text(cx2, cy2+5, '−', 14, INK, 'middle', 800)
    for dx, dy in [(0, -38), (38, 0), (0, 38), (-38, 0)]: wat_to(cx2+dx, cy2+dy, cx2, cy2, away=True)
    s.text(cx, 146, 'Na⁺: extremidade', 9.4, BLUE_D, 'middle', 800); s.text(cx, 158, 'O (δ−) voltada', 9.4, BLUE_D, 'middle', 800); s.text(cx, 170, 'para o cátion', 9.4, BLUE_D, 'middle', 800)
    s.text(cx2, 146, 'Cl⁻: extremidade', 9.4, BLUE_D, 'middle', 800); s.text(cx2, 158, 'H (δ+) voltada', 9.4, BLUE_D, 'middle', 800); s.text(cx2, 170, 'para o ânion', 9.4, BLUE_D, 'middle', 800)
    s.text(6, 188, 'Íon-dipolo substitui a atração íon-íon:', 10, INK, 'start', 800)
    s.text(6, 203, '• romper o retículo custa energia (energia reticular);', 9.4, INK, 'start', 500)
    s.text(6, 217, '• a hidratação libera energia (íon-dipolo + LH);', 9.4, INK, 'start', 500)
    s.text(6, 231, '• se a hidratação “paga” o retículo, o sal se dissolve.', 9.4, INK, 'start', 500)
    s.text(6, 252, 'Exceções (retículo muito forte): AgCl, BaSO₄, CaCO₃.', 9.4, RED_D, 'start', 800)
    return s.render()

def matrix():
    def cell(ok, why): 
        c = (GREEN_L, GREEN_D, '✔') if ok else (RED_L, RED_D, '✖')
        return f'<td style="background:{c[0]};text-align:center"><b style="color:{c[1]};font-size:11pt">{c[2]}</b><div style="font-size:7.2pt;color:{INK}">{why}</div></td>'
    return f'''<table style="table-layout:fixed"><tr><th style="width:30%">Soluto ↓ / Solvente →</th><th class="center"><span style="color:#9CC6FF">água</span> (polar)</th><th class="center"><span style="color:#FFD36B">hexano</span> (apolar)</th></tr>
    <tr><td><b>iônico</b><br>NaCl</td>{cell(True,'íon-dipolo')}{cell(False,'sem atração que pague o retículo')}</tr>
    <tr><td><b>polar</b><br>açúcar, etanol</td>{cell(True,'dipolo + LH')}{cell(False,'só London: não compensa')}</tr>
    <tr><td><b>apolar</b><br>óleo, I₂</td>{cell(False,'LH da água se mantêm: expulsa')}{cell(True,'London ≈ London')}</tr></table>'''

def p_B1():
    return f'''
<div class="cols2" style="grid-template-columns: 1.05fr 1fr">
  <div><h2>Vocabulário em três linhas</h2>
   <p><b>Soluto</b> é o que se dissolve; <b>solvente</b>, o que dissolve (em geral, o componente em maior quantidade); <b>solução</b>, a mistura homogênea. <b>Miscíveis</b>: formam uma só fase em qualquer proporção. <b>Imiscíveis</b>: formam duas fases.</p>
   <p>A dissolução acontece quando as <b>novas interações soluto–solvente</b> compensam as que foram rompidas (soluto–soluto e solvente–solvente). Daí a regra:</p>
   <div class="center" style="font-size:12pt;font-weight:900;padding:1.4mm;border:.5mm solid {INK};border-radius:2mm">SEMELHANTE DISSOLVE SEMELHANTE</div></div>
  <div style="display:flex;gap:1mm;justify-content:space-around">{beaker_fig('oil')}{beaker_fig('eth')}{beaker_fig('hex')}</div>
</div>
<div><h2>A polaridade ordena os solventes</h2>{polarity_scale()}</div>
<div class="cols2" style="grid-template-columns: 400px 1fr; align-items:start">
  <div><h2>Como a água dissolve um sal</h2>{hydration()}</div>
  <div><h2>Previsão rápida</h2>{matrix()}
   <div class="cap">É uma <b>tendência</b>, não uma lei: tamanho da molécula, LH e energia do retículo também pesam.</div>
   {box('red','Erros comuns','<ul><li>“Óleo e água não se misturam porque se <i>repelem</i>.” A água prefere se unir a si mesma (LH); o óleo é <b>excluído</b>.</li><li>“Dissolver é reagir.” Em geral é <b>físico</b>: o NaCl continua sendo NaCl (íons separados).</li></ul>')}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
{box('blue','Regras gerais de solubilidade de sais em água (útil para precipitações)','<ul><li><b>Sempre solúveis:</b> sais de Na⁺, K⁺, NH₄⁺ e nitratos (NO₃⁻).</li><li><b>Cloretos:</b> solúveis, exceto de Ag⁺, Pb²⁺ e Hg₂²⁺.</li><li><b>Sulfatos:</b> solúveis, exceto de Ba²⁺, Pb²⁺ (e Ca²⁺ pouco).</li><li><b>Carbonatos, fosfatos, hidróxidos:</b> em geral <b>insolúveis</b>, exceto os de metais alcalinos (e NH₄⁺).</li></ul>')}
{box('ink','ENEM na prática: roteiro em 4 passos','<ol><li>Classifique o <b>soluto</b> (iônico, polar, apolar) e o <b>solvente</b>.</li><li>Procure interações possíveis: íon-dipolo, LH, London.</li><li>Compare o <b>tamanho da cadeia</b> e o nº de grupos polares.</li><li>Conclua: “onde se acumula/dissolve/é extraído?”</li></ol>')}</div>
{quiz([('Por que o I₂ (apolar) se dissolve bem em hexano e mal em água?', 'Hexano e I₂ fazem London; a água, para acomodar o I₂, teria de romper LH sem ganhar interação equivalente.'), ('Por que o etanol é miscível em água?', 'O grupo –OH faz LH com a água e a cadeia curta (2 C) pouco atrapalha.')])}'''
page('B', 'Módulo B · 1 de 6', 'Quem dissolve quem? Semelhante dissolve semelhante', p_B1(), key='B1')

# ======================= B2 =======================
def alcohol_row():
    items = [('metanol', 'CO'), ('etanol', 'CCO'), ('propan-1-ol', 'CCCO'), ('butan-1-ol', 'CCCCO'), ('pentan-1-ol', 'CCCCCO'), ('hexan-1-ol', 'CCCCCCO')]
    cells = ''
    for n, smi in items:
        svg, d, m = mol_svg(smi, 112, 58, hl_atoms=semantic_hl(smi), bw=1.8, fs=12, pad=0.14, rot=0)
        cells += f'<div class="mol">{svg}<b style="color:{INK}">{n}</b></div>'
    return f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1mm">{cells}</div>'

def alcohol_chart():
    s = Svg(440, 230)
    ax = Axes(s, 52, 14, 372, 170, (0, 6), (0, 10))
    ax.frame(None, [0, 2, 4, 6, 8, 10], '', 'Solubilidade em água (g/100 mL, ~20 °C)', size=9.6, ylabel_dx=40)
    data = [('C1', None), ('C2', None), ('C3', None), ('C4', 7), ('C5', 2.2), ('C6', 0.6)]
    for i, (n, v) in enumerate(data):
        x = ax.X(i+0.5); w = 40
        if v is None:
            s.rect(x-w/2, ax.Y(10), w, ax.Y(0)-ax.Y(10), 'url(#dots-blue)', BLUE_D, 3, 1.4)
            s.label(x, ax.Y(10)+22, '∞', 16, BLUE_D, '#fff', 900); s.label(x, ax.Y(10)+42, 'miscível', 8.6, BLUE_D, '#fff', 800)
        else:
            s.rect(x-w/2, ax.Y(v), w, ax.Y(0)-ax.Y(v), 'url(#hatch-amber)', AMBER_D, 3, 1.4)
            s.text(x, ax.Y(v)-5, f'≈{v}'.replace('.', ','), 10, INK, 'middle', 800)
        s.text(x, 202, n, 10, INK, 'middle', 800)
    s.text(224, 222, 'nº de carbonos da cadeia (grupo –OH constante) →', 9.6, INK, 'middle', 700)
    return s.render()

def vit_row():
    a = ms('CC1=C(C(CCC1)(C)C)/C=C/C(=C/C=C/C(=C/CO)/C)/C', 300, 130, hl_atoms=semantic_hl('CC1=C(C(CCC1)(C)C)/C=C/C(=C/C=C/C(=C/CO)/C)/C'), bw=1.7, fs=11, pad=0.08)
    asc = 'OC[C@H](O)[C@H]1OC(=O)C(O)=C1O'
    c = ms(asc, 200, 130, hl_atoms=semantic_hl(asc), bw=1.7, fs=11, pad=0.1)
    return f'<div style="display:flex;gap:4mm;align-items:center"><div class="mol">{a}<b>vitamina A (retinol)</b><br>1 –OH · cadeia grande → <b class="t-amber">lipossolúvel</b></div><div class="mol">{c}<b>vitamina C (ác. ascórbico)</b><br>4 –OH → <b class="t-blue">hidrossolúvel</b></div></div>'

def p_B2():
    return f'''
<div><h2>Um mesmo grupo polar (–OH), cadeias cada vez maiores</h2>{alcohol_row()}
<div class="cap"><span class="chip" style="--c:{BLUE};--cd:{BLUE_D};--cl:{BLUE_L}">azul</span> grupo polar (faz LH com a água) · <span class="chip" style="--c:{AMBER};--cd:{AMBER_D};--cl:{AMBER_L}">âmbar</span> cadeia apolar (só London). Cada C a mais engrossa a parte que a água “não quer”.</div></div>
<div class="cols2" style="grid-template-columns: 440px 1fr; align-items:start">
  <div>{alcohol_chart()}<div class="cap">Valores aproximados de tabelas de solubilidade (butan-1-ol ≈7; pentan-1-ol ≈2; hexan-1-ol ≈0,6 g/100 mL).</div></div>
  <div><h2>Cabo de guerra molecular</h2>
   <ul><li><b class="t-blue">Grupo polar</b> (–OH, –COOH, –NH₂…): puxa para a água (LH).</li><li><b class="t-amber">Cadeia carbônica</b>: puxa para meios apolares.</li><li><b>Poucos C + grupo polar</b>: vence a água (metanol, etanol, glicerol, glicose).</li><li><b>Muitos C + 1 grupo polar</b>: vence o apolar (álcoois de cadeia longa, ácido esteárico).</li><li><b>Vários grupos polares</b> (glicerol, glicose, sacarose): muito solúveis em água.</li><li>Ramificação compacta ↑ solubilidade: o <i>terc</i>-butanol é miscível em água; o butan-1-ol, não.</li></ul></div>
</div>
<div class="cols2" style="grid-template-columns:1.1fr 1fr">
  {box('red','Limites da regra: o que NÃO ensinar',
   '<ul><li><b>Apolar ≠ gordura.</b> CH₄, CO₂, CCl₄, I₂ e hexano são apolares; gorduras são <i>triacilgliceróis</i> (ésteres) de cadeias longas. “Lipofílico” é uma tendência, não sinônimo de “lipídio”.</li><li><b>“Tem oxigênio ⇒ dissolve em água”: falso.</b> O triglicerídeo tem 6 O e é insolúvel; o ácido esteárico (C₁₈) também. Conta a <b>proporção</b> entre região polar e cadeia, e se há LH.</li><li><b>Éteres, ésteres e cetonas</b> só <i>aceitam</i> LH da água (não doam): são menos solúveis que álcoois de mesmo tamanho.</li><li><b>Íons podem ser pouco solúveis</b> (AgCl, BaSO₄): conta o retículo.</li></ul>')}
  <div>{box('green','Biologia e ambiente: o que é lipossolúvel se acumula',
   'Vitaminas A, D, E e K (lipossolúveis) ficam no tecido adiposo e no fígado: excesso <b>acumula</b>. Vitaminas C e do complexo B (hidrossolúveis) saem na urina. Poluentes de baixa polaridade (DDT, aldrin, PCBs) <b>bioacumulam</b> em gorduras e se magnificam na cadeia alimentar. <i>ENEM 2023 (via Aprova Total): aldrin concentra-se no leite, rico em gordura.</i>')}
  <div style="margin-top:2mm">{vit_row()}</div></div>
</div>'''
page('B', 'Módulo B · 2 de 6', 'Cadeia apolar × grupo polar: quem manda na solubilidade?', p_B2(), key='B2')

# ======================= B3 =======================
def beaker_sat():
    s = Svg(330, 126)
    def b(x, solid, label, sub, fillstyle='url(#dots-blue)'):
        mini_beaker(s, x, 8, 90, 78, [(1, fillstyle, '')])
        if solid:
            s.poly([(x+16, 82), (x+30, 72), (x+46, 82), (x+62, 74), (x+76, 82)], '#fff', INK, 1.4, close=True)
        for (dx, dy) in ([(30, 42), (60, 52), (45, 30), (70, 34)] if label != 'insaturada' else [(40, 44), (62, 36)]):
            s.circ(x+dx, dy+8, 2.2, INK)
        s.text(x+45, 104, label, 10, INK, 'middle', 800); s.text(x+45, 117, sub, 8.6, GRAY, 'middle', 600)
    b(2, False, 'insaturada', 'aceita mais soluto'); b(118, True, 'saturada', 'com corpo de fundo'); b(234, False, 'supersaturada', 'instável: cristaliza')
    return s.render()

def sol_chart():
    s = Svg(430, 300)
    ax = Axes(s, 54, 14, 360, 236, (0, 100), (0, 260))
    ax.frame([0, 20, 40, 60, 80, 100], [0, 50, 100, 150, 200, 250], 'Temperatura (°C)', 'Solubilidade (g de soluto / 100 g de água)', size=9.6, ylabel_dx=42, xlabel_dy=32)
    kno3 = [(0, 13), (20, 32), (40, 64), (60, 110), (80, 169), (100, 246)]
    nacl = [(0, 35.7), (20, 35.9), (40, 36.4), (60, 37.1), (80, 38.0), (100, 39.2)]
    ax.line(kno3, ORANGE, 2.6); ax.line(nacl, INK, 2.6)
    for x, y in kno3: ax.marker(x, y, 'd', ORANGE, 3.6, '#fff')
    for x, y in nacl: ax.marker(x, y, 's', INK, 3.4, '#fff')
    s.label(ax.X(36), ax.Y(168), 'KNO₃: cresce muito', 10, ORANGE_D, '#fff', 800, 'start')
    s.label(ax.X(52), ax.Y(22), 'NaCl: quase constante', 10, INK, '#fff', 800, 'start')
    # região
    s.text(ax.X(10), ax.Y(205), 'ACIMA da curva:', 9.4, RED_D, 'start', 800); s.text(ax.X(10), ax.Y(192), 'supersaturada (instável)', 9.4, RED_D, 'start', 700)
    s.text(ax.X(76), ax.Y(120), 'ABAIXO:', 9.4, BLUE_D, 'start', 800); s.text(ax.X(76), ax.Y(108), 'insaturada', 9.4, BLUE_D, 'start', 800)
    # exemplo: 80 g a 60 °C
    ax.marker(60, 80, 'f', BLUE, 5); s.text(ax.X(60)+8, ax.Y(80)+14, 'A: 80 g a 60 °C', 9.4, BLUE_D, 'start', 800)
    ax.marker(20, 80, 'f', RED, 5); s.text(ax.X(20)+9, ax.Y(80)+4, 'B: 80 g a 20 °C', 9.4, RED_D, 'start', 800)
    s.line(ax.X(20), ax.Y(80), ax.X(20), ax.Y(32), RED, 1.6, '4 3'); s.text(ax.X(20)-4, ax.Y(56), '48 g', 9.6, RED_D, 'end', 800); s.text(ax.X(20)-4, ax.Y(44), 'precipitam', 8.8, RED_D, 'end', 700)
    return s.render()

def o2_chart():
    s = Svg(300, 190)
    ax = Axes(s, 48, 12, 236, 130, (0, 40), (0, 16))
    ax.frame([0, 10, 20, 30, 40], [0, 4, 8, 12, 16], 'Temperatura da água (°C)', 'O₂ dissolvido (mg/L)', size=9.4, ylabel_dx=36, xlabel_dy=30)
    d = [(0, 14.6), (10, 11.3), (20, 9.1), (30, 7.6), (40, 6.5)]
    ax.line(d, GREEN, 2.6)
    for x, y in d: ax.marker(x, y, 'o', GREEN, 3.8, '#fff')
    s.text(ax.X(14), ax.Y(14.2), 'água quente tem menos O₂', 9.4, GREEN_D, 'start', 800)
    return s.render()

def p_B3():
    return f'''
<div class="cols2" style="grid-template-columns: 430px 1fr; align-items:start">
  <div><h2>Curvas de solubilidade: como ler</h2>{sol_chart()}<div class="cap">Dados de tabelas de livros-texto, arredondados. Cada ponto da curva é uma solução <b>saturada</b> àquela temperatura.</div></div>
  <div>{beaker_sat()}
   <h3 style="margin-top:1mm">Exemplo resolvido</h3>
   <div style="font-size:8.2pt">Dissolvem-se <b>80 g de KNO₃</b> em 100 g de água a 60 °C (ponto <b class="t-blue">A</b>).<ol style="margin-top:1mm"><li>A 60 °C o limite é ≈ 110 g: <b>insaturada</b> (cabem mais ≈ 30 g).</li><li>Resfriando a 20 °C (ponto <b class="t-red">B</b>) o limite cai para ≈ 32 g.</li><li>Excesso: 80 − 32 = <b>≈ 48 g precipitam</b> (corpo de fundo).</li></ol></div>
   {box('red','Erros comuns','<ul><li>“Solubilidade sempre aumenta com a temperatura.” <b>Não</b>: aumenta para a maioria dos sólidos, mas <b>diminui para gases</b> (e alguns sais).</li><li>Confundir <b>concentrada</b> com <b>saturada</b>: concentração é quantidade de soluto; saturação é estar no limite.</li></ul>')}
  </div>
</div>
<div class="cols3" style="grid-template-columns: 300px 1fr 1fr">
  <div><h2>Gases: o contrário</h2>{o2_chart()}</div>
  <div>{box('green','Conexão ambiental','Descarga de água aquecida (usinas, indústrias) reduz o O₂ dissolvido e sufoca peixes. Se há excesso de matéria orgânica (esgoto), a decomposição consome ainda mais O₂: <b>eutrofização</b> (Módulo F).')}</div>
  <div>{box('orange','Pressão e gás (lei de Henry)','Refrigerante: CO₂ dissolvido sob pressão. Ao abrir a garrafa, a pressão cai, a solubilidade diminui e o gás escapa (bolhas). Quente, escapa mais rápido.')}
  </div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
{box('orange','Aplicação: cristalização fracionada','100 g de KNO₃ + 30 g de NaCl dissolvem-se em 100 g de água a 100 °C (limites: 246 g e ≈39 g). Resfriando a 20 °C (limites ≈32 g e ≈36 g): <b>68 g de KNO₃ cristalizam</b> (100 − 32) e os 30 g de NaCl <b>continuam dissolvidos</b> (30 &lt; 36). É uma separação por diferença de solubilidade com a temperatura.')}
{quiz([('Massa máxima de KNO₃ que se dissolve em 250 g de água a 40 °C?', 'Limite ≈64 g/100 g → 64 × 2,5 = 160 g.'), ('Uma solução está exatamente sobre a curva do NaCl. É saturada?', 'Sim: está no limite de solubilidade àquela temperatura.')])}</div>'''
page('B', 'Módulo B · 3 de 6', 'Saturação e curvas de solubilidade', p_B3(), key='B3')

# ======================= B4 =======================
def surf_fig():
    s = Svg(700, 290)
    smi = 'CCCCCCCCCCCCCCCCCC(=O)[O-]'
    svg, d, m = mol_svg(smi, 340, 90, hl_atoms=semantic_hl(smi, polar_atoms=('O',)), bw=1.9, fs=12, pad=0.05)
    s.text(6, 14, 'estearato de sódio (um sabão): C₁₇H₃₅COO⁻ Na⁺', 10, INK, 'start', 800)
    s.embed(svg, 0, 22)
    s.rect(20, 118, 166, 20, AMBER_L, AMBER, 4, 1.4); s.text(103, 132, 'cauda apolar (17 C)', 9.4, AMBER_D, 'middle', 800)
    s.rect(240, 118, 98, 20, BLUE_L, BLUE, 4, 1.4); s.text(289, 132, 'cabeça polar', 9.4, BLUE_D, 'middle', 800)
    lipid(s, 70, 186, 1, 46, 9, (False, False))
    s.text(104, 190, '= anfifílica', 11, INK, 'start', 900); s.text(104, 204, '(ou anfipática)', 9.4, GRAY, 'start', 600)
    s.text(6, 270, 'Uma ponta tem afinidade pela água, a outra a evita.', 9.6, INK, 'start', 700)
    water_field(s, 358, 6, 336, 252, 24, 12)
    s.rect(358, 6, 336, 252, 'none', BLUE, 8, 1.5)
    micelle(s, 440, 120, R=54, n=16, L=34, r=6, oil=True)
    s.label(440, 124, 'óleo', 10, AMBER_D, '#FFF3D0', 800)
    s.label(440, 206, 'micela com óleo no interior', 9.6, INK, '#fff', 800)
    s.arrow(502, 120, 556, 120, 'ink', 2)
    for cx, cy, R in [(610, 80, 32), (646, 170, 24)]:
        s.circ(cx, cy, R-4, '#FFE19A', AMBER_D, 1.2)
        n = int(R/3.0)
        for i in range(n):
            a = 2*math.pi*i/n; s.circ(cx + R*math.cos(a), cy + R*math.sin(a), 4.4, 'url(#dots-blue)', BLUE, 1.2)
    s.label(612, 238, 'emulsão: gotas dispersas', 9.6, INK, '#fff', 800)
    return s.render()

def p_B4():
    return f'''
<div><h2>Anfifílico: uma molécula, duas afinidades</h2>{surf_fig()}</div>
<div class="cols3">
 {box('blue','1 · Sujeira gordurosa','A gordura é apolar: a água sozinha não a remove (LH da água &gt; interação água–gordura).')}
 {box('amber','2 · Caudas entram na gordura','As <b>caudas apolares</b> mergulham no óleo (London); as <b>cabeças polares</b> ficam voltadas para a água.')}
 {box('green','3 · Micelas e enxágue','A gota é cercada por cabeças hidrofílicas: fica <b>dispersa</b> na água e é arrastada. Isso é <b>emulsificação</b>, não dissolução.')}
</div>
<div class="cols2">
 <div><h2>Sabão × detergente sintético</h2>
 <table><tr><th></th><th>Sabão</th><th>Detergente sintético</th></tr>
 <tr><td><b>Cabeça</b></td><td>carboxilato (–COO⁻)</td><td>sulfonato / sulfato (–SO₃⁻, –OSO₃⁻)</td></tr>
 <tr><td><b>Origem</b></td><td>saponificação de gorduras</td><td>derivados do petróleo</td></tr>
 <tr><td><b>Água dura</b> (Ca²⁺, Mg²⁺)</td><td>precipita: (RCOO)₂Ca ↓ → pouca espuma</td><td>não precipita: continua agindo</td></tr>
 <tr><td><b>Ambiente</b></td><td>biodegradável</td><td>cadeia <b>linear</b> é biodegradável; <b>ramificada</b> resiste e gerou espuma em rios</td></tr></table>
 <div class="cap">Em pH muito ácido, o carboxilato do sabão vira ácido graxo (RCOOH), que é insolúvel e perde a ação.</div></div>
 <div>{box('ink','Onde mais há emulsificação?','<b>Maionese</b>: a lecitina da gema (fosfolipídio) estabiliza gotas de óleo em água. <b>Leite</b>: gotas de gordura em água, com proteínas. <b>Bile</b>: sais biliares emulsificam gorduras no intestino, aumentando a superfície para a lipase agir (cinética, Módulo H).')}
 {box('red','Erros comuns','<ul><li>“O detergente <i>dissolve</i> a gordura.” Ele a <b>emulsiona</b> em micelas.</li><li>“O sabão limpa por reagir com a gordura.” É ação <b>física</b>; a saponificação é o modo de <i>fabricar</i> o sabão.</li></ul>')}</div>
</div>
{quiz([('Por que o sabão faz pouca espuma em água dura?', 'Ca²⁺ e Mg²⁺ precipitam o carboxilato como sal insolúvel (RCOO)₂Ca.'), ('Em uma micela em água, onde ficam as caudas?', 'No interior (longe da água); as cabeças ficam na superfície, em contato com a água.')])}'''
page('B', 'Módulo B · 4 de 6', 'Anfifílicos: sabão, detergente, micelas e emulsão', p_B4(), key='B4')

# ======================= B5 =======================
POPC = 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC[N+](C)(C)C)OC(=O)CCCCCCC/C=C\\CCCCCCCC'
def popc_fig():
    hl, tail = phospholipid_hl(POPC)
    svg, d, m = mol_svg(POPC, 430, 200, hl_atoms=hl, bw=1.7, fs=10, pad=0.03)
    s = Svg(430, 214)
    s.embed(svg, 0, 14)
    def P(i): p = d.GetDrawCoords(i); return p.x, p.y + 14
    nidx = [a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == 'N'][0]
    x, y = P(nidx); s.text(x+44, y-2, 'colina (+)', 9.4, BLUE_D, 'start', 800)
    pidx = [a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == 'P'][0]
    x, y = P(pidx); s.text(x-96, y+4, 'fosfato (−)', 9.4, BLUE_D, 'start', 800)
    s.text(8, 10, 'fosfatidilcolina (exemplo: POPC)', 10, INK, 'start', 800)
    s.rect(8, 168, 10, 10, PURPLE_L, PURPLE, 2, 1.3); s.text(22, 177, 'éster (liga o ác. graxo ao glicerol)', 9, PURPLE_D, 'start', 700)
    s.rect(8, 183, 10, 10, AMBER_L, AMBER, 2, 1.3); s.text(22, 192, 'caudas: ácidos graxos (apolares)', 9, AMBER_D, 'start', 700)
    s.rect(8, 198, 10, 10, BLUE_L, BLUE, 2, 1.3); s.text(22, 207, 'cabeça polar: fosfato + colina', 9, BLUE_D, 'start', 700)
    # rótulos das caudas
    tx = [a.GetIdx() for a in m.GetAtoms() if a.GetIdx() in tail]
    return s.render(), d, m

def bilayer_fig():
    W, H = 700, 372
    s = Svg(W, H)
    water_field(s, 0, 0, W, 92, 26, 2)
    L, r = 56, 6.6
    ytop = 114
    n = 26; step = W/n
    ybot = ytop + 2*L + 2*r + 8
    skip = (452, 518)
    for i in range(n):
        x = step*(i+0.5)
        if skip[0] < x < skip[1]: continue
        lipid(s, x, ytop, 1, L, r, (False, i % 3 == 0)); lipid(s, x, ybot, -1, L, r, (False, (i+1) % 3 == 0))
    water_field(s, 0, ybot+24, W, 92, 26, 8)
    cxp = (skip[0]+skip[1])/2
    s.rect(skip[0]-6, ytop-14, 24, ybot-ytop+28, GREEN_L, GREEN_D, 8, 1.6); s.rect(skip[1]-18, ytop-14, 24, ybot-ytop+28, GREEN_L, GREEN_D, 8, 1.6)
    s.text(cxp, ytop+ (ybot-ytop)/2 - 2, 'canal', 9.2, GREEN_D, 'middle', 800); s.text(cxp, ytop+(ybot-ytop)/2+10, 'proteico', 9.2, GREEN_D, 'middle', 800)
    s.circ(cxp, 40, 8, '#fff', INK, 1.4); s.text(cxp, 44, '+', 11, INK, 'middle', 800)
    s.arrow(cxp, 52, cxp, ybot+52, 'green', 2.4)
    s.label(cxp+8, 30, '✔ Na⁺ passa pelo canal', 9.4, GREEN_D, '#fff', 800, 'start')
    s.label(10, 22, 'MEIO EXTRACELULAR · água (polar)', 10.5, BLUE_D, '#fff', 800, 'start'); s.label(10, ybot+90, 'CITOPLASMA · água (polar)', 10.5, BLUE_D, '#fff', 800, 'start')
    s.label(10, ytop+L+r+4, 'interior hidrofóbico (apolar)', 10.5, AMBER_D, '#FFF8E1', 800, 'start')
    s.label(10, ytop-18, 'cabeças hidrofílicas (polares)', 9.4, BLUE_D, '#fff', 800, 'start')
    # O2 passa pela região lipídica
    s.circ(180, 52, 7, '#fff', INK, 1.4); s.text(180, 55.5, 'O₂', 7.4, INK, 'middle', 800)
    s.arrow(180, 62, 180, ybot+58, 'ink', 1.6)
    s.label(188, 62, '✔ O₂ e CO₂ atravessam', 9.4, GREEN_D, '#fff', 800, 'start'); s.label(188, 76, '(pequenos e apolares)', 8.8, GREEN_D, '#fff', 700, 'start')
    # glicose barrada
    gx = 340
    s.poly([(gx-12, 46), (gx, 39), (gx+12, 46), (gx+12, 60), (gx, 67), (gx-12, 60)], '#fff', INK, 1.5, close=True); s.text(gx, 57, 'Glc', 8, INK, 'middle', 800)
    s.arrow(gx, 70, gx, ytop-14, 'red', 2.4)
    s.text(gx, ytop-9, '✖', 13, RED_D, 'middle', 900)
    s.label(gx+18, 54, '✖ glicose e íons:', 9.4, RED_D, '#fff', 800, 'start'); s.label(gx+18, 68, 'não cruzam o interior apolar', 9.4, RED_D, '#fff', 800, 'start')
    s.label(gx+18, 82, '(precisam de proteínas)', 9.4, RED_D, '#fff', 800, 'start')
    return s.render()

def packing_fig():
    s = Svg(330, 134)
    # saturadas retas, insaturadas com dobra
    for i in range(5):
        x = 30 + i*20
        s.line(x, 30, x, 100, AMBER, 3.2); s.circ(x, 24, 5.4, 'url(#dots-blue)', BLUE, 1.4)
    s.text(78, 116, 'saturadas: retas,', 9.2, AMBER_D, 'middle', 800); s.text(78, 127, 'bem empacotadas', 9.2, AMBER_D, 'middle', 800); s.text(78, 12, 'MENOR fluidez', 9.4, INK, 'middle', 800)
    for i in range(5):
        x = 200 + i*26
        s.poly([(x, 30), (x, 52), (x+8, 60), (x, 68), (x, 100)], stroke=AMBER, sw=3.2); s.circ(x, 24, 5.4, 'url(#dots-blue)', BLUE, 1.4)
    s.text(252, 116, 'insaturadas (cis): dobradas,', 9.2, AMBER_D, 'middle', 800); s.text(252, 127, 'mais espaçadas', 9.2, AMBER_D, 'middle', 800); s.text(252, 12, 'MAIOR fluidez', 9.4, INK, 'middle', 800)
    return s.render()

def p_B5():
    fig, d, m = popc_fig()
    return f'''
<div class="cols2" style="grid-template-columns: 430px 1fr; align-items:start">
  <div>{fig}</div>
  <div><h2>Um fosfolipídio, três partes</h2>
   <ol><li><b class="t-blue">Cabeça polar</b>: fosfato (−) e colina (+) fazem íon-dipolo e LH com a água → <b>hidrofílica</b>.</li><li><b class="t-purple">Glicerol + ligações éster</b>: unem as partes (a “esqueleto”).</li><li><b class="t-amber">Duas caudas</b> de ácidos graxos: só London → <b>hidrofóbicas</b>. Uma é saturada (reta), a outra pode ser <b>insaturada</b> (dobra <i>cis</i>).</li></ol>
   <div class="cap">Comparado ao sabão (1 cauda, forma de cone), o fosfolipídio tem 2 caudas (forma de cilindro): isso favorece a <b>bicamada</b> em vez da micela (próxima página).</div></div>
</div>
<div><h2>A bicamada em água: orientação e permeabilidade seletiva</h2>{bilayer_fig()}</div>
<div class="cols2" style="grid-template-columns:1.1fr 1fr">
  <div>{box('green','Como ler a figura','Água dos <b>dois lados</b> → as cabeças ficam voltadas para fora (para a água) em cada folheto, e as caudas se escondem no centro. O interior apolar é uma barreira para o que é polar ou carregado: por isso a membrana é <b>seletivamente permeável</b>. Íons e glicose precisam de <b>proteínas</b> (canais e transportadores).')}
  <div class="small" style="margin-top:1.5mm">Modelo mosaico fluido: a membrana real também tem proteínas, colesterol e glicolipídios. Figura esquemática, sem escala.</div></div>
  <div><h3>Fluidez e insaturação</h3>{packing_fig()}
  <div class="cap">ENEM 2019 (via Aprova Total): caudas insaturadas reduzem o contato entre fosfolipídios → <b>maior fluidez</b>. Temperatura baixa → menor fluidez.</div></div>
</div>'''
page('B', 'Módulo B · 5 de 6', 'Fosfolipídios e a bicamada: a química da membrana celular', p_B5(), key='B5')

# ======================= B6 =======================
def trio():
    s = Svg(700, 214)
    def panel(x, title):
        s.rect(x, 4, 224, 206, '#fff', LGRAY, 8, 1.4); s.text(x+112, 22, title, 10.5, INK, 'middle', 800)
    # 1 óleo + água
    panel(4, '① óleo + água')
    mini_beaker(s, 44, 32, 144, 142, [(0.38, 'url(#hatch-amber)', ''), (0.62, 'url(#dots-blue)', '')])
    s.text(116, 72, 'óleo (apolar)', 10, AMBER_D, 'middle', 800); s.text(116, 126, 'água (polar)', 10, BLUE_D, 'middle', 800)
    s.text(116, 192, 'agrupam-se por semelhança', 9.4, INK, 'middle', 700); s.text(116, 204, 'duas fases', 9.4, RED_D, 'middle', 800)
    # 2 detergente
    panel(238, '② + detergente: micela')
    water_field(s, 244, 30, 212, 140, 24, 21)
    s.circ(350, 100, 50, '#fff', None); micelle(s, 350, 100, R=40, n=12, L=28, r=5.2, oil=True)
    s.text(350, 190, 'cone + 1 cauda → esfera', 9.4, INK, 'middle', 700); s.text(350, 203, 'interior apolar', 9.4, AMBER_D, 'middle', 800)
    # 3 bicamada
    panel(472, '③ fosfolipídio: bicamada')
    water_field(s, 478, 30, 212, 140, 28, 31)
    s.circ(584, 100, 74, '#fff', None); s.circ(584, 100, 36, '#EAF3FD', None); vesicle(s, 584, 100, R=64, th=28, n_out=26, n_in=16)
    s.text(584, 100+3, 'água', 9.6, BLUE_D, 'middle', 800)
    s.text(584, 190, 'cilindro + 2 caudas → folha', 9.4, INK, 'middle', 700); s.text(584, 203, 'lipossomo / membrana', 9.4, GREEN_D, 'middle', 800)
    s.arrow(232, 107, 242, 107, 'ink', 1.6)
    return s.render()

def p_B6():
    return f'''
<div><div style="font-size:9.4pt;font-weight:600;padding:1.4mm 2.4mm;background:{BG};border-radius:1.6mm;margin-bottom:2mm"><b>A lógica única:</b> o que é <span class="t-amber b">apolar</span> se agrupa longe da água; o que é <span class="t-blue b">polar</span> fica em contato com ela. Moléculas com <b>as duas</b> partes se organizam na interface.</div>{trio()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 <div><h2>Micela × bicamada</h2>
 <table><tr><th></th><th>Micela</th><th>Bicamada</th></tr>
 <tr><td><b>Molécula típica</b></td><td>sabão, detergente</td><td>fosfolipídio</td></tr>
 <tr><td><b>Caudas</b></td><td>1 (forma de cone)</td><td>2 (forma de cilindro)</td></tr>
 <tr><td><b>Estrutura</b></td><td>esfera de <b>1 camada</b></td><td>folha de <b>2 camadas</b> (fecha em vesícula)</td></tr>
 <tr><td><b>Interior</b></td><td>apolar: abriga óleo</td><td>apolar, entre dois folhetos; água dentro e fora</td></tr>
 <tr><td><b>Formação</b></td><td>acima da conc. micelar crítica</td><td>espontânea em água</td></tr>
 <tr><td><b>Função</b></td><td>limpeza, emulsificação</td><td>compartimentalização, barreira seletiva</td></tr></table></div>
 <div><h2>Substâncias na mesma lógica (com ressalvas)</h2>
 <table><tr><th>Substância</th><th>Perfil</th><th>Comportamento em água</th></tr>
 <tr><td>água</td><td>polar</td><td>LH entre si; dissolve polares e íons</td></tr>
 <tr><td>etanol</td><td>polar + cadeia curta</td><td>miscível; <b>não</b> faz micela (cauda curta demais)</td></tr>
 <tr><td>óleo (triacilglicerol)</td><td>apolar</td><td>separa; menos denso, flutua</td></tr>
 <tr><td>ácido graxo livre</td><td>anfifílico, mas –COOH fraco</td><td>mal solúvel; forma película na superfície. O <b>sal</b> (sabão) forma micelas</td></tr>
 <tr><td>detergente</td><td>anfifílico, 1 cauda</td><td>micelas</td></tr></table></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('red','Ressalvas científicas','<ul><li>“Hidrofóbico” não é “medo” da água: o agrupamento ocorre porque a água, ao se reorganizar em LH entre si, tem ganho de energia livre (efeito hidrofóbico).</li><li>Polar/apolar é uma <b>escala</b>; as classificações acima são tendências.</li><li>Micelas só se formam acima de uma concentração mínima.</li></ul>')}
 {quiz([('Por que a membrana tem duas camadas e não uma micela?', 'O fosfolipídio tem duas caudas (cilindro); a geometria favorece folhas, não esferas.'), ('Por que o etanol dissolve manchas “mistas” mas não forma espuma como o detergente?', 'Cauda curta: dissolve por polaridade intermediária, sem agregar em micelas.')])}
</div>'''
page('B', 'Módulo B · 6 de 6', 'Do óleo e da água à membrana celular: uma mesma lógica química', p_B6(), key='B6')
