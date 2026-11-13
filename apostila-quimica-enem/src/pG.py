# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import fbal, fmass, num
import math

# ---- verificações ----
fbal('combustão do etanol', [(1, 'C2H5OH'), (3, 'O2')], [(2, 'CO2'), (3, 'H2O')])
num('etanol: 23 kg → mol', 23000/fmass('C2H5OH'), 500); num('CO2 formado (mol)', 2*500, 1000); num('CO2 (kg)', 1000*fmass('CO2')/1000, 44); num('CO2 volume CNTP (m³)', 1000*22.4/1000, 22.4)
fbal('Haber: N2 + 3 H2 → 2 NH3', [(1, 'N2'), (3, 'H2')], [(2, 'NH3')])
num('N2 28 g → mol', 28/fmass('N2'), 1); num('H2 10 g → mol', 10/fmass('H2'), 5); num('NH3 teórica (g)', 2*fmass('NH3'), 34); num('rendimento', 17/34*100, 50)
fbal('calcinação: CaCO3 → CaO + CO2', [(1, 'CaCO3')], [(1, 'CaO'), (1, 'CO2')])
num('calcário puro (kg)', 500*0.80, 400); num('n CaCO3 (mol)', 400000/fmass('CaCO3'), 4000); num('CaO teórico (kg)', 4000*fmass('CaO')/1000, 224); num('CaO real 90% (kg)', 224*0.9, 201.6)
num('S no carvão (t)', 1000*0.02, 20); num('SO2 (t)', 20*fmass('SO2')/fmass('S'), 40); num('CaCO3 p/ SO2 (t)', 40/fmass('SO2')*fmass('CaCO3'), 62.5)
num('ENEM 2024 bauxita evitada (t)', 4.0e5*0.974*5, 1.9e6, 0.03)
fbal('balanceamento exemplo: C3H8 + 5 O2 → 3 CO2 + 4 H2O', [(1, 'C3H8'), (5, 'O2')], [(3, 'CO2'), (4, 'H2O')])

def passos():
    s = Svg(700, 120)
    steps = [('1', 'Equação', 'escreva reagentes\ne produtos', 'ink'), ('2', 'Balanceie', 'nº de átomos igual\nnos dois lados', 'orange'), ('3', 'Dados', 'o que é dado?\no que é pedido?', 'ink'), ('4', 'Em mol', 'g ÷ MM · L ÷ 22,4\n· M × V', 'orange'),
             ('5', 'Proporção', 'regra de três\ncom os coeficientes', 'orange'), ('6', 'Resposta', 'volte à unidade\npedida (e confira)', 'green')]
    w = 108; gap = 10.4
    for i, (n, t, d, k) in enumerate(steps):
        x = 2 + i*(w+gap); c = COL[k]
        s.add(f'<polygon points="{x},8 {x+w-10},8 {x+w+4},46 {x+w-10},84 {x},84 {x+14},46" fill="{c[2]}" stroke="{c[0]}" stroke-width="2"/>')
        s.circ(x+24, 26, 10, c[0]); s.text(x+24, 30, n, 11, '#fff', 'middle', 900)
        s.text(x+58, 31, t, 9.6 if len(t) > 9 else 10.6, c[1], 'middle', 900); s.text(x+56, 58, d, 8.4, INK, 'middle', 600, lh=1.2)
    s.text(350, 108, 'Equação → balanceamento → dados → conversão para mol → proporção → resposta com unidade', 10, GRAY, 'middle', 800)
    return s.render()

def ponte():
    s = Svg(330, 130)
    def nd(x, y, w, t1, t2):
        s.rect(x, y, w, 38, ORANGE_L, ORANGE, 8, 2); s.text(x+w/2, y+16, t1, 10.5, ORANGE_D, 'middle', 900); s.text(x+w/2, y+30, t2, 9, INK, 'middle', 600)
    nd(2, 46, 92, 'massa (g)', 'm'); nd(119, 46, 92, 'mol', 'n'); nd(236, 8, 92, 'volume gás (L)', 'CNTP'); nd(236, 86, 92, 'partículas', 'N')
    s.arrow(96, 58, 117, 58, 'ink', 1.8); s.arrow(117, 74, 96, 74, 'ink', 1.8)
    s.text(106, 44, '÷ MM', 8.4, INK, 'middle', 800); s.text(106, 92, '× MM', 8.4, INK, 'middle', 800)
    s.arrow(213, 56, 234, 34, 'ink', 1.8); s.text(222, 30, '× 22,4', 8.4, INK, 'end', 800)
    s.arrow(213, 76, 234, 100, 'ink', 1.8); s.text(222, 112, '× 6,0×10²³', 8.4, INK, 'end', 800)
    s.text(2, 126, 'MM em g/mol: soma das massas atômicas', 8.8, GRAY, 'start', 600)
    return s.render()

def p_G1():
    return f'''
<div>{passos()}</div>
<div class="cols2" style="grid-template-columns:330px 1fr; align-items:start">
  <div><h2>A ponte entre grandezas</h2>{ponte()}<div class="cap">A <b>proporção só vale em mol</b> (ou em volume, para gases na mesma T e P). Massas não se comparam diretamente: 1 g de H₂ e 1 g de O₂ têm números de moléculas muito diferentes.</div></div>
  <div><h2>Balanceando sem sofrer</h2>
   <ol><li>Comece pelo elemento que aparece <b>em menos substâncias</b> (C e metais); deixe O e H por último.</li><li>Ajuste apenas os <b>coeficientes</b>, nunca os índices (H₂O ≠ H₂O₂).</li><li>Confira os átomos dos dois lados.</li></ol>
   <div class="eq" style="margin-top:1mm;font-size:10pt">C₃H₈ + <span class="t-orange">5</span> O₂ → <span class="t-orange">3</span> CO₂ + <span class="t-orange">4</span> H₂O</div>
   <div class="small" style="margin-top:1mm">C: 3 = 3 · H: 8 = 8 · O: 10 = 6 + 4.<br>Volumes de gases (mesma T e P): proporção em volume = proporção em mol. 2 H₂ + O₂ → 2 H₂O(g): 2 V : 1 V : 2 V.</div></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
  {box('orange','Exemplo resolvido (média-alta): combustão do etanol','Quanto CO₂ se libera ao queimar <b>23 kg</b> de etanol (C₂H₅OH; MM = 46 g/mol)?<br><b>① ②</b> C₂H₅OH + 3 O₂ → <b>2</b> CO₂ + 3 H₂O<br><b>③ ④</b> n = 23 000 g ÷ 46 = <b>500 mol</b> de etanol.<br><b>⑤</b> 1 mol etanol : 2 mol CO₂ → <b>1000 mol</b> de CO₂.<br><b>⑥</b> m = 1000 × 44 = <b>44 kg</b> (ou 1000 × 22,4 L = <b>22,4 m³</b> nas CNTP).')}
  {box('green','ENEM na prática: proporção com reciclagem de alumínio','ENEM 2024 (descrito pelo Aprova Total): 50 kg de bauxita → 10 kg de Al (razão 5:1). Reciclando 97,4% de 4,0×10⁵ t de latas, deixam de ser extraídas 4,0×10⁵ × 0,974 × 5 ≈ <b>1,9×10⁶ t</b> de bauxita. Raciocínio: proporção + porcentagem, sem decorar fórmula.')}
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('red','Erros comuns','<ul><li>Usar <b>massa</b> direto na regra de três da equação (coeficientes são em <b>mol</b>).</li><li>Alterar <b>índices</b> ao balancear.</li><li>Esquecer que 22,4 L/mol vale só nas <b>CNTP</b> (0 °C e 1 atm); em 25 °C e 1 atm, ≈ 24,5 L/mol.</li><li>Dar a resposta em mol quando se pede kg.</li></ul>')}
 {quiz([('Quantos mol de O₂ reagem com 2 mol de C₃H₈?', 'C₃H₈ : O₂ = 1 : 5 → 10 mol.'), ('Que volume de CO₂ (CNTP) forma 1 mol de C₃H₈?', '3 mol CO₂ × 22,4 = 67,2 L.')])}
</div>'''
page('G', 'Módulo G · 1 de 2', 'Estequiometria: um método em seis passos', p_G1(), key='G1')

def limit_chart():
    s = Svg(330, 190)
    s.text(8, 14, 'N₂ + 3 H₂ → 2 NH₃  (28 g N₂ + 10 g H₂)', 10, INK, 'start', 800)
    # barras: mol disponível / mol necessário
    ax = Axes(s, 46, 30, 270, 110, (0, 2), (0, 6))
    ax.frame(None, [0, 1, 2, 3, 4, 5, 6], '', 'mol', size=9, ylabel_dx=30)
    for i, (nm, have, need, col) in enumerate([('N₂', 1, 1, 'ink'), ('H₂', 5, 3, 'orange')]):
        x = ax.X(i+0.5); w = 54
        s.rect(x-w/2, ax.Y(have), w, ax.Y(0)-ax.Y(have), COL[col][2], COL[col][0], 3, 1.8)
        s.rect(x-w/2, ax.Y(need), w, ax.Y(0)-ax.Y(need), 'url(#hatch-orange)' if col == 'orange' else 'url(#hatch-amber)', COL[col][1], 3, 1.4)
        s.text(x, ax.Y(have)-5, f'{have} mol', 9.6, INK, 'middle', 800); s.text(x, 156, nm, 11, INK, 'middle', 900)
    s.text(ax.X(0.5), 172, 'só 1 mol: LIMITANTE', 9.2, INK, 'middle', 900); s.text(ax.X(1.5), 172, 'sobram 2 mol (4 g)', 9.2, ORANGE_D, 'middle', 900)
    s.text(8, 186, 'cor lisa = disponível · hachura = necessário p/ consumir todo o N₂ ou H₂', 8.2, GRAY, 'start', 600)
    return s.render()

def p_G2():
    return f'''
<div class="cols2" style="grid-template-columns:330px 1fr; align-items:start">
  <div><h2>Reagente limitante: o primeiro a acabar</h2>{limit_chart()}</div>
  <div><h2>Como achar o limitante (em 3 linhas)</h2>
  <ol><li>Converta tudo para <b>mol</b>.</li><li>Divida cada n pelo <b>coeficiente</b>: N₂: 1 ÷ 1 = <b>1</b>; H₂: 5 ÷ 3 = <b>1,67</b>.</li><li>O <b>menor</b> quociente é o limitante (N₂). Ele manda no produto: 1 mol N₂ → <b>2 mol NH₃ = 34 g</b> (teórico).</li></ol>
  {box('blue','Rendimento e pureza (dois “descontos”)','<span class="eq">η = real ÷ teórico × 100</span><br>Rendimento: se obtiveram <b>17 g</b> de NH₃ em vez de 34 g, η = <b>50%</b>.<br><span class="eq">m pura = m amostra × pureza</span><br>Só a parte <b>pura</b> reage. Pureza é aplicada <b>antes</b> do cálculo; rendimento, <b>depois</b>.')}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('orange','Exemplo industrial (média-alta): cal virgem','Calcário com <b>80%</b> de CaCO₃ (500 kg) é calcinado: CaCO₃ → CaO + CO₂, com rendimento de <b>90%</b>. Massa de CaO?<br><b>①</b> pura: 500 × 0,80 = <b>400 kg</b> = 400 000 g.<br><b>②</b> n = 400 000 ÷ 100 = <b>4 000 mol</b>.<br><b>③</b> 1 : 1 → 4 000 mol de CaO (56 g/mol) = <b>224 kg</b> teórico.<br><b>④</b> 224 × 0,90 ≈ <b>202 kg</b> (201,6).')}
 {box('green','Exemplo ambiental (média-alta): chuva ácida na fonte','Carvão com <b>2% de enxofre</b>; queimam-se 1000 t. S + O₂ → SO₂.<br><b>①</b> S: 1000 × 0,02 = <b>20 t</b>. <b>②</b> S : SO₂ = 32 : 64 → <b>40 t</b> de SO₂.<br><b>③</b> Para retê-lo com calcário (SO₂ + CaCO₃ + ½ O₂ → CaSO₄ + CO₂): n(SO₂) = 40 t ÷ 64 = 0,625 Mmol → <b>62,5 t</b> de CaCO₃.')}
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('red','Erros comuns','<ul><li>Escolher o limitante pela <b>menor massa</b> (precisa ser pelo menor n ÷ coeficiente).</li><li>Aplicar rendimento e pureza <b>na ordem errada</b> ou duas vezes.</li><li>Calcular o produto pelo reagente <b>em excesso</b>.</li></ul>')}
 {quiz([('50 g de CaCO₃ puros produzem quantos litros de CO₂ nas CNTP? (CaCO₃ → CaO + CO₂)', 'n = 50/100 = 0,5 mol → 0,5 × 22,4 = 11,2 L.'), ('Com 2 mol de H₂ e 2 mol de O₂ (2 H₂ + O₂ → 2 H₂O), qual o limitante?', 'H₂ (2/2 = 1 &lt; 2/1 = 2).')])}
</div>'''
page('G', 'Módulo G · 2 de 2', 'Reagente limitante, rendimento e pureza', p_G2(), key='G2')
