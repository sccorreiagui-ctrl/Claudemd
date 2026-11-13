# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import num, fbal
import math

num('pH [H+]=1e-3', -math.log10(1e-3), 3); num('pH com log2=0,30: 2e-3', -(math.log10(2) + (-3)), 2.7, 0.01)
num('pOH 1e-4 → pH', 14 - 4, 10); num('[H+] pH 5', 10**-5, 1e-5); num('HCl 0,01 mol/L', -math.log10(0.01), 2); num('razão [H+] pH3/pH6', 10**-3/10**-6, 1000)
fbal('Haber', [(1, 'N2'), (3, 'H2')], [(2, 'NH3')]); fbal('neutralização HCl + NaOH → NaCl + H2O', [(1, 'HCl'), (1, 'NaOH')], [(1, 'NaCl'), (1, 'H2O')])
fbal('ácido carbônico: CO2 + H2O → H2CO3', [(1, 'CO2'), (1, 'H2O')], [(1, 'H2CO3')]); fbal('amônia em água', [(1, 'NH3'), (1, 'H2O')], [(1, 'NH4OH')])

def eq_graphs():
    s = Svg(700, 200)
    # c x t
    a = Axes(s, 44, 12, 200, 130, (0, 10), (0, 1.0)); a.frame(None, [0, 0.5, 1.0], 'tempo', 'concentração', size=9, ylabel_dx=34, xlabel_dy=26)
    A = [(x, 0.4 + 0.6*math.exp(-x*0.9)) for x in [i*0.2 for i in range(0, 51)]]; B = [(x, 0.6*(1 - math.exp(-x*0.9))) for x in [i*0.2 for i in range(0, 51)]]
    a.line(A, INK, 2.6); a.line(B, ORANGE, 2.6)
    s.line(a.X(5), a.y0, a.X(5), a.y0+a.h, RED, 1.4, '4 3'); s.text(a.X(5)+4, a.y0+10, 't(eq)', 9, RED_D, 'start', 800)
    s.text(a.X(0.4), a.Y(0.98), 'A (reagente)', 9, INK, 'start', 800); s.text(a.X(6.3), a.Y(0.64), 'B (produto)', 9, ORANGE_D, 'start', 800)
    s.text(a.X(6), a.Y(0.33), 'constantes,', 9, INK, 'start', 800); s.text(a.X(6), a.Y(0.25), 'não iguais!', 9, RED_D, 'start', 900)
    # v x t
    b = Axes(s, 296, 12, 170, 130, (0, 10), (0, 1.0)); b.frame(None, [], 'tempo', 'velocidade', size=9, ylabel_dx=18, xlabel_dy=26)
    b.line([(x, 0.4 + 0.6*math.exp(-x*0.9)) for x in [i*0.2 for i in range(0, 51)]], BLUE, 2.4); b.line([(x, 0.4*(1 - math.exp(-x*0.9))) for x in [i*0.2 for i in range(0, 51)]], PURPLE, 2.4)
    s.line(b.X(5), b.y0, b.X(5), b.y0+b.h, RED, 1.4, '4 3')
    s.text(b.X(0.6), b.Y(0.95), 'v direta', 9, BLUE_D, 'start', 800); s.text(b.X(6), b.Y(0.28), 'v inversa', 9, PURPLE_D, 'start', 800); s.text(b.X(5.4), b.Y(0.55), 'v₁ = v₂', 9.4, RED_D, 'start', 900)
    # perturbação
    c = Axes(s, 520, 12, 170, 130, (0, 10), (0, 1.0)); c.frame(None, [], 'tempo', '', size=9, xlabel_dy=26)
    def p(f): return [(x, f(x)) for x in [i*0.2 for i in range(0, 51)]]
    c.line(p(lambda x: 0.4 if x < 4 else (0.7 - 0.2*(1 - math.exp(-(x-4)*0.8)) if x >= 4.2 else 0.7)), INK, 2.4)
    c.line(p(lambda x: 0.6 if x < 4 else 0.6 + 0.2*(1 - math.exp(-(x-4)*0.8))), ORANGE, 2.4)
    s.line(c.X(4), c.y0, c.X(4), c.y0+c.h, GREEN, 1.6, '4 3'); s.text(c.X(4)-4, c.y0+10, 'adiciona A', 9, GREEN_D, 'end', 800)
    s.text(c.X(6.6), c.Y(0.58), 'A cai', 9, INK, 'start', 800); s.text(c.X(6.6), c.Y(0.84), 'B sobe', 9, ORANGE_D, 'start', 800)
    s.text(a.x0+a.w/2, 192, '① Equilíbrio dinâmico', 10, INK, 'middle', 900); s.text(b.x0+b.w/2, 192, '② Velocidades se igualam', 10, INK, 'middle', 900); s.text(c.x0+c.w/2, 192, '③ Perturbação (Le Chatelier)', 10, INK, 'middle', 900)
    return s.render()

def p_I1():
    rows = [('↑ [reagente]', '→ direita', 'consome o que foi adicionado'), ('↑ [produto] ou retirar reagente', '← esquerda', 'consome o produto em excesso'), ('↑ temperatura', 'sentido <b>endotérmico</b>', 'absorve calor'),
            ('↓ temperatura', 'sentido <b>exotérmico</b>', 'libera calor'), ('↑ pressão (gases)', 'lado com <b>menos mol de gás</b>', 'reduz a pressão'), ('catalisador', '<b>não desloca</b>', 'acelera os dois sentidos; só chega mais cedo')]
    t = ''.join(f'<tr><td>{a}</td><td><b class="t-orange">{b}</b></td><td>{c}</td></tr>' for a, b, c in rows)
    return f'''
<div><h2>Equilíbrio químico em três gráficos</h2>{eq_graphs()}
<div class="cap">① Reagente cai, produto sobe, e depois ambos ficam <b>constantes</b> (não iguais). ② No equilíbrio as velocidades se igualam e a reação continua nos dois sentidos: equilíbrio <b>dinâmico</b>. ③ Ao adicionar A, o sistema reage para consumir o excesso e atinge um novo equilíbrio.</div></div>
<div class="cols2" style="grid-template-columns:1.1fr 1fr">
 <div><h2>Princípio de Le Chatelier</h2><div class="small" style="margin-bottom:1mm">“O sistema em equilíbrio, ao ser perturbado, desloca-se no sentido que <b>atenua</b> a perturbação.”</div>
 <table><tr><th>Perturbação</th><th>Desloca para</th><th>Porque</th></tr>{t}</table>
 <div class="cap">A constante <b>Kc</b> = [produtos]ᶜ ÷ [reagentes]ᵃ (sólidos e líquidos puros não entram) só muda com a <b>temperatura</b>.</div></div>
 <div>{box('orange','Aplicação industrial: síntese da amônia (Haber-Bosch)','N₂ + 3 H₂ ⇌ 2 NH₃  <b>ΔH &lt; 0</b><br>• ↑ <b>pressão</b>: 4 mol de gás → 2 mol: favorece NH₃ (≈ 150–300 atm).<br>• ↓ <b>T</b> favorece NH₃ (exotérmica), mas deixa a reação <b>lenta</b>: usa-se ≈ 400–500 °C e <b>catalisador de ferro</b>: compromisso entre rendimento e velocidade.<br>• Retirar NH₃ (liquefação) desloca para a direita.')}
 <div style="margin-top:1.6mm">{box('green','Ambiente e biologia','<b>CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻</b>: mais CO₂ atmosférico → oceanos mais ácidos → conchas e corais (CaCO₃) se dissolvem. <b>Refrigerante</b>: CO₂(aq) ⇌ CO₂(g); abrir a garrafa desloca para a direita.')}</div></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('red','Erros comuns','<ul><li>Equilíbrio = “concentrações iguais”. <b>Não</b>: são <b>constantes</b>.</li><li>Catalisador <b>não</b> altera o rendimento do equilíbrio.</li><li>Aumentar a pressão desloca só se há <b>variação de mol de gás</b>.</li></ul>')}
 {quiz([('Em CO(g) + 2 H₂(g) ⇌ CH₃OH(g), aumentar a pressão desloca para…', 'direita (3 mol de gás → 1 mol).'), ('Ao aquecer um equilíbrio exotérmico, o rendimento do produto…', 'diminui (desloca para o sentido endotérmico, o inverso).')])}
</div>'''
page('I2', 'Módulo I · 1 de 2', 'Equilíbrio químico e Le Chatelier', p_I1(), key='I1')

def ph_ruler():
    s = Svg(700, 196)
    for i in range(14):
        x = 14 + i*48.4
        f = ORANGE_L if i < 7 else '#DDE1E8'
        s.rect(x, 62, 48.4, 30, f, '#fff', 0, 1)
    s.rect(14, 62, 48.4*7, 30, 'url(#hatch-orange)', ORANGE, 0, 1.6); s.rect(14+48.4*7, 62, 48.4*7, 30, '#DDE1E8', INK, 0, 1.6)
    s.text(14+48.4*3.5, 82, 'ÁCIDO  ([H⁺] > [OH⁻])', 11, ORANGE_D, 'middle', 900); s.text(14+48.4*10.5, 82, 'BÁSICO  ([OH⁻] > [H⁺])', 11, INK, 'middle', 900)
    s.label(14+48.4*7, 56, 'NEUTRO (25 °C)', 9, INK, '#fff', 900)
    ex = [(1.5, 'suco gástrico', 0), (2.3, 'limão', 1), (3.0, 'vinagre', 2), (5.0, 'café', 1), (5.6, 'chuva normal', 0), (7.0, 'água pura', 1), (7.4, 'sangue', 0), (8.1, 'água do mar', 2), (10.5, 'leite de magnésia', 1), (12, 'água sanitária*', 0), (13.5, 'soda cáustica', 1)]
    for v, nme, tier in ex:
        x = 14 + v*48.4
        if tier == 1: s.line(x, 92, x, 126, GRAY, 1); s.text(x, 138, nme, 8.8, INK, 'middle', 700)
        elif tier == 2: s.line(x, 92, x, 150, GRAY, 1); s.text(x, 162, nme, 8.8, INK, 'middle', 700)
        else: s.line(x, 62, x, 34, GRAY, 1); s.text(x, 28, nme, 8.8, INK, 'middle', 700)
    for k in range(15):
        s.label(14 + k*48.4, 110, str(k), 10, INK, '#fff', 800)
    s.text(14, 184, '[H⁺] = 10⁻ᵖᴴ mol/L: cada unidade de pH = 10× mais ou menos H⁺', 10, GRAY, 'start', 800)
    s.text(686, 184, '*valores típicos aproximados', 8.8, GRAY, 'end', 600)
    return s.render()

def log_bars():
    s = Svg(330, 140)
    ax = Axes(s, 40, 10, 270, 90, (0, 4), (0, 1.2)); 
    s.line(40, 100, 310, 100, INK, 1.4); s.line(40, 10, 40, 100, INK, 1.4)
    for i, (ph, lab) in enumerate([(3, 'pH 3'), (4, 'pH 4'), (5, 'pH 5'), (6, 'pH 6')]):
        x = 60 + i*66; h = 10**(6-ph) / 1000 * 88 if False else (88 * (1.0 if ph == 3 else (0.1 if ph == 4 else (0.01 if ph == 5 else 0.001))))
        s.rect(x, 100-max(h, 1.2), 40, max(h, 1.2), 'url(#hatch-orange)', ORANGE_D, 2, 1.4)
        s.text(x+20, 114, lab, 9.4, INK, 'middle', 800); s.text(x+20, 100-max(h, 1.2)-4, f'10⁻{ph}', 9, INK, 'middle', 800)
    s.text(175, 134, '[H⁺] em escala linear: pH 3 tem 1000× mais H⁺ que pH 6', 9.4, ORANGE_D, 'middle', 800)
    return s.render()

def p_I2():
    return f'''
<div><h2>A régua de pH: logarítmica</h2>{ph_ruler()}</div>
<div class="cols2" style="grid-template-columns:330px 1fr; align-items:start">
  <div><h2>Por que logarítmica?</h2>{log_bars()}</div>
  <div><h2>Fórmulas e exemplos</h2>
  <div style="display:flex;gap:2mm;flex-wrap:wrap"><span class="eq">pH = −log [H⁺]</span><span class="eq">pOH = −log [OH⁻]</span><span class="eq">Kw = [H⁺]·[OH⁻] = 10⁻¹⁴</span><span class="eq">pH + pOH = 14</span></div>
  <ul style="margin-top:1.4mm"><li>[H⁺] = 10⁻³ mol/L → <b>pH 3</b>. pH 5 → [H⁺] = 10⁻⁵.</li><li>HCl 0,01 mol/L (ácido forte, 100% ionizado): [H⁺] = 10⁻² → <b>pH 2</b>.</li><li>[OH⁻] = 10⁻⁴ → pOH 4 → <b>pH 10</b>.</li><li>[H⁺] = 2×10⁻³ (dado log 2 = 0,30): pH = 3 − 0,30 = <b>2,7</b>.</li></ul>
  <div class="small">Valores condicionados a <b>25 °C</b> (Kw varia com a temperatura).</div></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 <div><h2>Ácidos e bases</h2>
 <table><tr><th>Teoria</th><th>Ácido</th><th>Base</th></tr><tr><td>Arrhenius</td><td>libera H⁺ em água</td><td>libera OH⁻ em água</td></tr><tr><td>Brønsted-Lowry</td><td><b>doa</b> H⁺ (próton)</td><td><b>recebe</b> H⁺ (NH₃ + H₂O ⇌ NH₄⁺ + OH⁻)</td></tr></table>
 <div class="small" style="margin-top:1mm"><b>Forte × fraco</b> = grau de <b>ionização</b>, não concentração. Fortes: HCl, HNO₃, H₂SO₄, NaOH, KOH. Fracos: CH₃COOH, H₂CO₃, HCN, NH₃.</div>
 {box('orange','Neutralização','<b>H⁺ + OH⁻ → H₂O</b> · HCl + NaOH → NaCl + H₂O. Ácido + base → <b>sal</b> + água. O pH final depende do <b>excesso</b> (Módulo E2).')}</div>
 <div><h2>Funções inorgânicas e equilíbrio iônico</h2>
 <table><tr><th>Função</th><th>Exemplos e papel</th></tr><tr><td><b>Óxido ácido</b></td><td>CO₂, SO₂, SO₃, NO₂ + H₂O → ácidos (<b>chuva ácida</b>)</td></tr><tr><td><b>Óxido básico</b></td><td>CaO, Na₂O + H₂O → bases (<b>calagem</b> do solo)</td></tr><tr><td><b>Sal</b></td><td>NaCl, CaCO₃, NaHCO₃ (antiácido)</td></tr></table>
 {box('purple','Ácido fraco e tampão','CH₃COOH ⇌ H⁺ + CH₃COO⁻ · <b>Ka</b> = [H⁺][A⁻] ÷ [HA] ≈ 1,8×10⁻⁵ (poucos íons). Adicionar acetato desloca o equilíbrio para a esquerda: <b>efeito do íon comum</b>. O <b>sangue</b> é tamponado (CO₂/HCO₃⁻): pH ≈ 7,4.')}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('red','Erros comuns','<ul><li>pH 3 não é “o dobro” de pH 6: é <b>1000×</b> mais H⁺ (escala logarítmica).</li><li>Ácido forte ≠ ácido concentrado.</li><li>pH 7 só é neutro a <b>25 °C</b>.</li></ul>')}
 {quiz([('Por quantas vezes a [H⁺] de pH 2 supera a de pH 5?', '10³ = 1000 vezes.'), ('Qual o pH de NaOH 0,001 mol/L?', '[OH⁻] = 10⁻³ → pOH 3 → pH 11.')])}
</div>'''
page('I2', 'Módulo I · 2 de 2', 'Ácidos, bases e pH: uma régua logarítmica', p_I2(), key='I2')
