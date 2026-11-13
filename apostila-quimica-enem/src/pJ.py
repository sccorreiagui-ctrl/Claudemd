# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import num, fbal
import math

num('NOx Mn em KMnO4', 7, 1 + 7 - 8 + 0 if False else 7); assert 1 + 7 + 4*(-2) == 0; assert 2 + 2*6 + 7*(-2) == 0; assert 2 + 6 + 4*(-2) == 0
num('ΔE° Daniell', 0.34 - (-0.76), 1.10)
num('Faraday: Q = i·t', 2*965, 1930); num('n(e-)', 1930/96500, 0.020); num('n(Cu)', 0.020/2, 0.010); num('m(Cu)', 0.010*63.5, 0.635)
fbal('Daniell: Zn + CuSO4 → ZnSO4 + Cu', [(1, 'Zn'), (1, 'CuSO4')], [(1, 'ZnSO4'), (1, 'Cu')]); fbal('ferrugem (global): 4 Fe + 3 O2 → 2 Fe2O3', [(4, 'Fe'), (3, 'O2')], [(2, 'Fe2O3')])
fbal('cloro-álcali: 2 NaCl + 2 H2O → H2 + Cl2 + 2 NaOH', [(2, 'NaCl'), (2, 'H2O')], [(1, 'H2'), (1, 'Cl2'), (2, 'NaOH')])

def pilha():
    s = Svg(700, 330)
    L0, R0 = 96, 404
    s.rect(L0, 150, 200, 150, '#EEF1F6', None); s.rect(R0, 150, 200, 150, BLUE_L, None)
    for x0 in (L0, R0): s.path(f'M{x0},108 L{x0},296 Q{x0},306 {x0+10},306 L{x0+190},306 Q{x0+200},306 {x0+200},296 L{x0+200},108', stroke=GRAY, sw=3)
    s.text(L0+100, 322, 'ZnSO₄ (aq): Zn²⁺ e SO₄²⁻', 9.6, INK, 'middle', 700); s.text(R0+100, 322, 'CuSO₄ (aq): Cu²⁺ (azul) e SO₄²⁻', 9.6, INK, 'middle', 700)
    zx, cx = L0+70, R0+100
    s.rect(zx, 80, 30, 190, '#B8BFCC', INK, 2, 2); s.text(zx+15, 262, 'Zn', 11, INK, 'middle', 900)
    s.rect(cx, 80, 30, 190, '#E2A06A', INK, 2, 2); s.text(cx+15, 262, 'Cu', 11, INK, 'middle', 900)
    for (x, y) in [(L0+30, 190), (L0+40, 236), (L0+130, 200), (L0+160, 250), (L0+150, 172)]: s.circ(x, y, 7, '#fff', INK, 1.3); s.text(x, y+3, '2+', 7, INK, 'middle', 800)
    for (x, y) in [(R0+30, 200), (R0+170, 232), (R0+176, 182)]: s.circ(x, y, 7, BLUE, INK, 1.3); s.text(x, y+3, '2+', 7, '#fff', 'middle', 800)
    s.text(zx+15, 296, '[Zn²⁺] aumenta', 9, INK, 'middle', 800); s.text(cx+15, 296, '[Cu²⁺] diminui', 9, BLUE_D, 'middle', 800)
    bx1, bx2 = L0+175, R0+25
    s.path(f'M{bx1},150 L{bx1},100 Q{bx1},86 {bx1+14},86 L{bx2-14},86 Q{bx2},86 {bx2},100 L{bx2},150', stroke=GRAY, sw=14, cap='butt')
    s.path(f'M{bx1},150 L{bx1},100 Q{bx1},86 {bx1+14},86 L{bx2-14},86 Q{bx2},86 {bx2},100 L{bx2},150', stroke='#F6F1D8', sw=10, cap='butt')
    s.text(350, 74, 'ponte salina (KNO₃)', 9.6, INK, 'middle', 800)
    s.arrow(340, 90, bx1+10, 90, 'blue', 1.8); s.arrow(360, 90, bx2-10, 90, 'orange', 1.8)
    s.text(350, 116, '← ânions (NO₃⁻) vão ao ânodo', 8.8, BLUE_D, 'middle', 800); s.text(350, 130, 'cátions (K⁺) vão ao cátodo →', 8.8, ORANGE_D, 'middle', 800)
    s.path(f'M{zx+15},80 L{zx+15},38 L318,38', stroke=INK, sw=2.4); s.path(f'M382,38 L{cx+15},38 L{cx+15},80', stroke=INK, sw=2.4)
    s.circ(350, 38, 32, '#fff', INK, 2.4); s.text(350, 34, '1,10 V', 12, INK, 'middle', 900); s.text(350, 48, 'voltímetro', 8.4, GRAY, 'middle', 700)
    s.arrow(zx+40, 38, zx+110, 38, 'red', 2.4); s.text(zx+76, 28, 'e⁻', 11, RED_D, 'middle', 900); s.arrow(cx-70, 38, cx-4, 38, 'red', 2.4); s.text(cx-36, 28, 'e⁻', 11, RED_D, 'middle', 900)
    s.rect(4, 100, 82, 28, ORANGE_L, ORANGE, 6, 1.6); s.text(45, 112, 'ÂNODO (−)', 9.4, ORANGE_D, 'middle', 900); s.text(45, 123, 'OXIDAÇÃO', 9, ORANGE_D, 'middle', 900)
    s.rect(614, 100, 82, 28, ORANGE_L, ORANGE, 6, 1.6); s.text(655, 112, 'CÁTODO (+)', 9.4, ORANGE_D, 'middle', 900); s.text(655, 123, 'REDUÇÃO', 9, ORANGE_D, 'middle', 900)
    s.text(45, 152, 'Zn →', 10.4, INK, 'middle', 900); s.text(45, 166, 'Zn²⁺ + 2 e⁻', 10, INK, 'middle', 900); s.text(45, 182, 'massa do', 8.8, GRAY, 'middle', 700); s.text(45, 193, 'eletrodo ↓', 8.8, GRAY, 'middle', 700)
    s.text(655, 152, 'Cu²⁺ + 2 e⁻', 10, INK, 'middle', 900); s.text(655, 166, '→ Cu', 10.4, INK, 'middle', 900); s.text(655, 182, 'massa do', 8.8, GRAY, 'middle', 700); s.text(655, 193, 'eletrodo ↑', 8.8, GRAY, 'middle', 700)
    return s.render()

def p_J1():
    return f'''
<div class="cols2" style="grid-template-columns:1fr 1fr">
 <div><h2>Oxirredução: transferência de elétrons</h2>
 <table><tr><th></th><th>Oxidação</th><th>Redução</th></tr><tr><td>elétrons</td><td><b>perde</b></td><td><b>ganha</b></td></tr><tr><td>NOx</td><td><b>aumenta</b></td><td><b>diminui</b></td></tr><tr><td>atua como</td><td><b>agente redutor</b></td><td><b>agente oxidante</b></td></tr></table>
 <div class="small" style="margin-top:1mm">O agente oxidante é quem <b>sofre redução</b> (e o redutor, quem sofre oxidação): o oxidante tira elétrons do outro.</div></div>
 <div><h2>Número de oxidação (NOx): regras</h2>
 <ul style="font-size:8.2pt"><li>Substância simples: <b>0</b> (Cu, O₂). Íon simples: sua <b>carga</b> (Zn²⁺ = +2).</li><li>H: <b>+1</b> (hidretos: −1) · O: <b>−2</b> (peróxidos: −1) · alcalinos +1 · alcalino-terrosos +2 · F: −1.</li><li>A soma dos NOx = <b>carga</b> da espécie.</li></ul>
 <div class="small"><b>KMnO₄:</b> +1 + x + 4(−2) = 0 → <b>Mn +7</b>. <b>K₂Cr₂O₇:</b> 2 + 2x − 14 = 0 → <b>Cr +6</b>. <b>H₂SO₄:</b> 2 + x − 8 = 0 → <b>S +6</b>.</div></div>
</div>
<div><h2>Pilha de Daniell: o grande esquema</h2>{pilha()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('orange','Como ler: notação e potencial','<span class="eq">Zn(s) | Zn²⁺(aq) ‖ Cu²⁺(aq) | Cu(s)</span><br>Reação global (espontânea): <b>Zn + Cu²⁺ → Zn²⁺ + Cu</b>.<br><b>ΔE° = E°cátodo − E°ânodo</b> = 0,34 − (−0,76) = <b>+1,10 V</b>. O de <b>maior</b> E° de redução sofre redução (Cu); o de menor, oxidação (Zn).<br>Os e⁻ vão do <b>ânodo ao cátodo</b> pelo fio; a ponte fecha o circuito com íons e <b>mantém a neutralidade</b>.')}
 <div>{box('red','Erros comuns','<ul><li>Elétrons <b>não</b> passam pela ponte salina: ela conduz por <b>íons</b>.</li><li>Na pilha, o ânodo é o polo <b>negativo</b> (oxidação); na eletrólise, é o <b>positivo</b> (próxima página).</li><li>Confundir <b>oxidante</b> (sofre redução) com <b>oxidado</b>.</li></ul>')}
 <div style="margin-top:1.6mm">{quiz([('Memorize: o ânodo é o eletrodo de…', 'oxidação (“an-ox”); o cátodo, de redução.'), ('Na pilha Zn/Cu, qual eletrodo perde massa?', 'O de Zn (ânodo): Zn → Zn²⁺.')])}</div></div>
</div>'''
page('J', 'Módulo J · 1 de 2', 'Oxirredução e a pilha eletroquímica', p_J1(), key='J1')

def eletrolise_fig():
    s = Svg(330, 210)
    s.rect(20, 80, 180, 100, '#FFE9CE', None); s.path('M20,60 L20,172 Q20,182 30,182 L190,182 Q200,182 200,172 L200,60', stroke=GRAY, sw=3)
    s.text(110, 198, 'NaCl fundido (Na⁺ e Cl⁻)', 9.6, INK, 'middle', 700)
    s.rect(54, 36, 22, 84, '#4B5160', INK, 2, 1.6); s.rect(144, 36, 22, 84, '#4B5160', INK, 2, 1.6)
    s.path('M65,36 L65,14 L240,14', stroke=INK, sw=2.2); s.path('M155,36 L155,22 L168,22', stroke=INK, sw=2.2); s.path('M168,22 L168,14', stroke=INK, sw=2.2)
    s.rect(240, 4, 40, 20, '#fff', INK, 3, 2); s.text(250, 18, '−', 13, INK, 'middle', 900); s.text(270, 18, '+', 13, INK, 'middle', 900)
    s.line(280, 14, 290, 14, INK, 2.2); s.path('M290,14 L290,5 L155,5 L155,36', stroke=INK, sw=2.2)
    s.text(65, 172, 'CÁTODO (−)', 9.4, ORANGE_D, 'middle', 900); s.text(155, 172, 'ÂNODO (+)', 9.4, ORANGE_D, 'middle', 900)
    s.text(65, 138, 'Na⁺ + e⁻ → Na', 9, INK, 'middle', 900); s.text(65, 150, 'redução', 9, ORANGE_D, 'middle', 900)
    s.text(155, 138, '2 Cl⁻ → Cl₂ + 2 e⁻', 9, INK, 'middle', 900); s.text(155, 150, 'oxidação', 9, ORANGE_D, 'middle', 900)
    s.arrow(110, 100, 82, 100, 'ink', 1.6); s.arrow(110, 100, 138, 100, 'ink', 1.6); s.text(110, 96, 'íons', 8.4, GRAY, 'middle', 700)
    for (x, y) in [(172, 60), (178, 46), (184, 70)]: s.circ(x, y, 3.4, '#fff', GRAY, 1.2)
    s.text(238, 60, 'Cl₂ (gás)', 9, GRAY, 'start', 700)
    return s.render()

def corrosao_fig():
    s = Svg(330, 190)
    s.rect(10, 120, 310, 38, '#B8BFCC', INK, 4, 2); s.text(24, 144, 'ferro (Fe)', 10, INK, 'start', 800)
    s.path('M60,120 Q60,52 165,52 Q270,52 270,120 Z', '#DCEBFB', BLUE, 2); s.text(165, 82, 'gota de água', 9.6, BLUE_D, 'middle', 800)
    s.text(165, 66, 'O₂ do ar', 9, GRAY, 'middle', 700)
    s.rect(115, 112, 100, 8, ORANGE, None); s.text(165, 109, '', 8)
    s.text(165, 176, 'ÂNODO (centro, pouco O₂): Fe → Fe²⁺ + 2e⁻', 9.2, ORANGE_D, 'middle', 900)
    s.text(165, 14, 'CÁTODO (borda, muito O₂): O₂ + 2H₂O + 4e⁻ → 4OH⁻', 9.2, ORANGE_D, 'middle', 900)
    s.path('M165,128 Q112,138 80,126', stroke=RED, sw=2, marker='red'); s.path('M165,128 Q218,138 250,126', stroke=RED, sw=2, marker='red'); s.text(165, 150, 'e⁻', 9.6, RED_D, 'middle', 900)
    return s.render()

def p_J2():
    return f'''
<div class="cols2" style="grid-template-columns:1.1fr 1fr">
 <div><h2>Pilha × eletrólise: a mesma química, sentido inverso</h2>
 <table><tr><th></th><th>Pilha</th><th>Eletrólise</th></tr>
 <tr><td><b>Processo</b></td><td>espontâneo</td><td><b>forçado</b> por fonte externa</td></tr>
 <tr><td><b>Energia</b></td><td>química → elétrica</td><td>elétrica → química</td></tr>
 <tr><td><b>Ânodo</b></td><td>polo <b>−</b> · oxidação</td><td>polo <b>+</b> · oxidação</td></tr>
 <tr><td><b>Cátodo</b></td><td>polo <b>+</b> · redução</td><td>polo <b>−</b> · redução</td></tr>
 <tr><td><b>Exemplos</b></td><td>pilhas, baterias em uso</td><td>galvanoplastia, produção de Al e Cl₂, recarga de bateria</td></tr></table>
 <div class="cap">Em ambas: <b>ânodo = oxidação, cátodo = redução</b>. O que muda é o sinal dos polos e quem “empurra” os elétrons.</div></div>
 <div><h2>Eletrólise ígnea do NaCl</h2>{eletrolise_fig()}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('orange','Eletrólise em solução aquosa (cloro-álcali)','2 NaCl + 2 H₂O → H₂ + Cl₂ + 2 NaOH. A água compete: no cátodo, H₂O é reduzida (H₂ + OH⁻) em vez de Na⁺. Produz <b>H₂, Cl₂ e NaOH</b>, matérias-primas industriais.')}
 {box('blue','Quantidade de matéria: a conta de Faraday','<span class="eq">Q = i · t</span> · <span class="eq">n(e⁻) = Q ÷ 96 500</span><br><b>Exemplo (média-alta):</b> i = 2 A durante 965 s depositando Cu (Cu²⁺ + 2e⁻ → Cu): Q = 1930 C → n(e⁻) = <b>0,020 mol</b> → n(Cu) = <b>0,010 mol</b> → m = 0,010 × 63,5 ≈ <b>0,64 g</b>.')}
</div>
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
 <div><h2>Corrosão: uma pilha indesejada</h2>{corrosao_fig()}<div class="cap">Fe²⁺ + OH⁻ → Fe(OH)₂, oxidado a ferrugem (Fe₂O₃·nH₂O). Água e O₂ são necessários; sal acelera (eletrólito).</div></div>
 <div>{box('green','Como proteger (e por quê funciona)','<ul><li><b>Galvanização (Zn):</b> E°(Zn²⁺/Zn) = −0,76 V &lt; E°(Fe²⁺/Fe) = −0,44 V: o Zn oxida primeiro (<b>metal de sacrifício</b>), mesmo riscado. Mg em cascos de navios age igual.</li><li><b>Folha-de-flandres (Sn):</b> E°(Sn²⁺/Sn) = −0,14 V &gt; E°(Fe): protege só enquanto <b>íntegra</b>; riscada, o <b>Fe corrói</b> mais rápido.</li><li><b>Pintura/óleo:</b> barreira física.</li></ul>')}
 {box('red','Erros comuns','<ul><li>Dizer que o metal de sacrifício “resiste mais”: ele é <b>mais reativo</b> (menor E°) e oxida no lugar do ferro.</li><li>Trocar ânodo e cátodo na eletrólise.</li></ul>')}
 {quiz([('Por que uma lata de Sn riscada enferruja mais rápido que o ferro puro?', 'Fe vira ânodo da pilha Fe/Sn (Sn é menos reativo): oxida mais rápido.')])}</div>
</div>'''
page('J', 'Módulo J · 2 de 2', 'Eletrólise × pilha e corrosão', p_J2(), key='J2')
