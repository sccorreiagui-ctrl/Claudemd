# -*- coding: utf-8 -*-
from lib import *
from figs import mini_beaker
from chk import num, MM
import math

# ---- verificações numéricas dos exemplos ----
num('soro 0,9% → C (g/L)', 0.9/0.1, 9)
num('soro: M = C/MM(NaCl=58,5)', 9/58.5, 0.154)
num('NaOH 250 mL 0,20 mol/L: n', 0.20*0.250, 0.050); num('massa NaOH (MM 40)', 0.050*40.0, 2.0); num('massa com 80% de pureza', 2.0/0.80, 2.5)
num('ppm Pb: 0,30 mg em 2,0 L', 0.30/2.0, 0.15)
num('diluição 100 mL HCl 2 mol/L → 500 mL', 2.0*100/500, 0.40); num('V1 para 250 mL a 0,2 mol/L partindo de 5 mol/L', 0.2*250/5, 10)
num('mistura sem reação (200 mL 0,5 + 300 mL 1,0)', (0.5*0.2 + 1.0*0.3)/0.5, 0.80)
n_oh = 0.50*0.200; n_h = 0.20*0.300; exc = n_oh - n_h
num('mistura com reação: sobra OH-', exc, 0.040); conc = exc/0.500
num('[OH-] final', conc, 0.080); pOH = -math.log10(conc); num('pOH', pOH, 1.10, 0.01); num('pH', 14 - pOH, 12.9, 0.01)
num('dose paracetamol: 150 mg em 200 mg/mL', 150/200, 0.75)

def node(s, x, y, w, h, t1, t2, kind):
    c = COL[kind]; s.rect(x, y, w, h, c[2], c[0], 8, 2); s.text(x+w/2, y+18, t1, 11, c[1], 'middle', 800); s.text(x+w/2, y+34, t2, 9.6, INK, 'middle', 600)

def conv_map():
    s = Svg(700, 190)
    node(s, 6, 74, 150, 46, 'massa de soluto', 'm (g)', 'ink'); node(s, 276, 8, 150, 46, 'quantidade', 'n (mol)', 'orange')
    node(s, 276, 140, 150, 46, 'conc. comum', 'C (g/L)', 'blue'); node(s, 544, 74, 150, 46, 'conc. molar', 'M (mol/L)', 'purple')
    s.arrow(156, 88, 274, 40, 'ink', 2); s.label(214, 56, '÷ MM (g/mol)', 10, INK, '#fff', 800)
    s.arrow(426, 36, 548, 84, 'ink', 2); s.label(498, 52, '÷ V (L)', 10, INK, '#fff', 800)
    s.arrow(156, 108, 274, 156, 'ink', 2); s.label(214, 148, '÷ V (L)', 10, INK, '#fff', 800)
    s.arrow(426, 164, 548, 112, 'ink', 2); s.label(498, 150, '÷ MM (g/mol)', 10, INK, '#fff', 800)
    s.text(350, 100, 'C = M × MM', 13, INK, 'middle', 900); s.text(350, 116, 'mesmos 4 pontos, dois caminhos', 9.2, GRAY, 'middle', 600)
    return s.render()

def fcard2(eq, title, vars_, when, ex, err, kind='ink'):
    return f'''<div class="card" style="padding:1.6mm 2.2mm"><div style="display:flex;justify-content:space-between;align-items:center"><span class="eq">{eq}</span>{tag(kind, title)}</div>
<div style="font-size:8.1pt;margin-top:1mm"><b>Variáveis:</b> {vars_}<br><b>Use quando:</b> {when}</div>
<div style="font-size:8.1pt;margin-top:.8mm;background:{BG};padding:.8mm 1.4mm;border-radius:1mm"><b>Exemplo:</b> {ex}</div>
<div style="font-size:8.1pt;margin-top:.8mm;background:{RED_L};padding:.8mm 1.4mm;border-radius:1mm"><b class="t-red">⚠ Erro:</b> {err}</div></div>'''

def p_E1():
    cards = ''.join([
        fcard2('C = m / V', 'conc. comum', '<b>m</b> massa de soluto (g); <b>V</b> volume da <u>solução</u> (L). C em g/L.', 'o dado vem em massa e volume (rótulos, “g por litro”).', 'soro 0,9% (m/V) = 0,9 g/100 mL → <b>9 g/L</b>.', 'usar o volume do <b>solvente</b>, ou deixar o V em mL.', 'blue'),
        fcard2('n = m / MM', 'mol', '<b>n</b> quantidade (mol); <b>MM</b> massa molar (g/mol), da tabela periódica.', 'passar de gramas para mol e vice-versa.', 'NaCl: MM = 23 + 35,5 = 58,5 g/mol → 9 g = <b>0,15 mol</b>.', 'usar número atômico no lugar de massa atômica.', 'orange'),
        fcard2('M = n / V', 'conc. molar', '<b>n</b> mol de soluto; <b>V</b> volume da solução (L). M em mol/L.', 'o problema fala em mol/L ou reage em proporção de mols.', 'soro: M = 9 / 58,5 ≈ <b>0,15 mol/L</b>. Também: M = C / MM.', 'V em mL: converta (÷ 1000) antes de dividir.', 'purple'),
        fcard2('ppm = mg/L', 'traços', 'mg de soluto por litro (água diluída ≈ 1 kg/L); % m/m = m₁/m × 100.', 'qualidade da água, poluentes, minerais em rótulos.', '0,30 mg de Pb em 2,0 L → <b>0,15 mg/L = 0,15 ppm</b>.', 'trocar mg por g: 1 g/L = 1000 mg/L = 1000 ppm.', 'green')])
    return f'''
<div><h2>Um mapa para não se perder: massa, mol, volume e concentração</h2>{conv_map()}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{cards}</div>
<div style="display:flex;gap:1.6mm;flex-wrap:wrap;align-items:center"><b>Conversões:</b>{tag('ink','1 L = 1000 mL = 1 dm³ = 1000 cm³')}{tag('ink','1 g = 1000 mg')}{tag('ink','1 mol = 6,0 × 10²³ entidades')}{tag('ink','V molar (CNTP) ≈ 22,4 L/mol')}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
{box('orange','Exemplo resolvido (média-alta): preparo e pureza','Quantos gramas de NaOH (MM = 40 g/mol) pesar para preparar <b>250 mL</b> de solução <b>0,20 mol/L</b>, usando reagente com <b>80%</b> de pureza?<br><b>1)</b> V = 0,250 L → n = M·V = 0,20 × 0,250 = <b>0,050 mol</b>.<br><b>2)</b> m = n·MM = 0,050 × 40 = <b>2,0 g</b> de NaOH puro.<br><b>3)</b> Pureza: 2,0 ÷ 0,80 = <b>2,5 g</b> do reagente impuro.')}
<div>{box('ink','Exemplo resolvido (média): rótulo de medicamento','Gotas de paracetamol: 200 mg/mL. Dose: 150 mg. Volume = 150 ÷ 200 = <b>0,75 mL</b>. Em mol (MM = 151 g/mol): n = 0,150 ÷ 151 ≈ <b>1,0 × 10⁻³ mol</b>.')}
<div style="margin-top:2mm">{quiz([('Qual a concentração, em mol/L, de 4,0 g de NaOH em 500 mL de solução?', 'n = 4,0/40 = 0,10 mol; V = 0,5 L → M = 0,20 mol/L.')])}</div></div>
</div>
{box('red','Erros comuns','<ul><li><b>Volume da solução ≠ volume do solvente.</b> A fórmula usa o volume final.</li><li>Misturar unidades: mg com g, mL com L. Escreva as unidades em cada passo.</li><li>Confundir <b>concentração</b> (quantidade por volume) com <b>quantidade</b> (n ou m).</li></ul>')}'''
page('E', 'Módulo E · 1 de 2', 'Concentração de soluções: massa, mol, volume', p_E1(), key='E1')

def dil_fig():
    s = Svg(330, 150)
    import random; rnd = random.Random(7)
    def b(x, w, h, label, nm, pts):
        mini_beaker(s, x, 150-h-24, w, h, [(1, '#EAF3FD', '')])
        for _ in range(pts): s.circ(x+rnd.uniform(10, w-10), 150-h-24+rnd.uniform(h*0.32, h-12), 3, ORANGE_D)
        s.text(x+w/2, 144, label, 9.6, INK, 'middle', 800)
    b(12, 90, 80, 'V₁ · C₁ (concentrada)', 1, 10)
    s.text(150, 70, '+ solvente', 10, BLUE_D, 'middle', 800); s.arrow(118, 82, 182, 82, 'blue', 2.6)
    b(196, 124, 110, 'V₂ · C₂ (diluída)', 2, 10)
    s.text(165, 14, 'mesma quantidade de soluto (10 partículas)', 9.6, ORANGE_D, 'middle', 800)
    return s.render()

def p_E2():
    return f'''
<div class="cols2" style="grid-template-columns:330px 1fr; align-items:start">
  <div><h2>Diluição: só se acrescenta solvente</h2>{dil_fig()}</div>
  <div><div class="center"><span class="eq" style="font-size:14pt">C₁ · V₁ = C₂ · V₂</span></div>
   <p style="margin-top:1.4mm"><b>Por que vale:</b> a quantidade de soluto não muda (n₁ = n₂). Como n = M·V (ou m = C·V), então M₁V₁ = M₂V₂.<br><b>Condições:</b> mesmo soluto e <b>nenhuma reação</b>; V₂ = V₁ + solvente adicionado; usar a <b>mesma unidade</b> de volume dos dois lados.</p>
   <p><b>Exemplo (média):</b> 100 mL de HCl 2 mol/L são levados a 500 mL: M₂ = 2 × 100 ÷ 500 = <b>0,40 mol/L</b>. Fator de diluição = 5.</p>
   <p><b>Exemplo (média):</b> V₁ de HCl 5 mol/L para preparar 250 mL a 0,2 mol/L: V₁ = 0,2 × 250 ÷ 5 = <b>10 mL</b> (e completa-se com água até 250 mL).</p></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('blue','Mistura do mesmo soluto, sem reação','<span class="eq">M = (M₁V₁ + M₂V₂) ÷ (V₁ + V₂)</span><br>Soma-se o <b>n</b> de cada solução e divide-se pelo volume total (admite volumes aditivos).<br><b>Exemplo:</b> 200 mL a 0,50 mol/L + 300 mL a 1,0 mol/L → (0,10 + 0,30) ÷ 0,50 = <b>0,80 mol/L</b>.')}
 {box('orange','Mistura com reação (neutralização): faça a tabela de mols','Misturam-se <b>200 mL de NaOH 0,50 mol/L</b> e <b>300 mL de HCl 0,20 mol/L</b>. Qual o pH?<br><table style="margin-top:1mm"><tr><th></th><th>OH⁻</th><th>H⁺</th></tr><tr><td>início (mol)</td><td>0,100</td><td>0,060</td></tr><tr><td>reage (1:1)</td><td>− 0,060</td><td>− 0,060</td></tr><tr><td>resta (mol)</td><td><b>0,040</b></td><td>0</td></tr></table>[OH⁻] = 0,040 ÷ 0,500 L = <b>0,080 mol/L</b> → pOH = 1,10 → <b>pH ≈ 12,9</b> (básica).')}
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('green','Interpretando rótulos e qualidade da água','<ul><li><b>mg/L ou ppm</b>: sólidos dissolvidos, minerais, contaminantes. 1 g/L = 1000 ppm.</li><li>“<b>pH 7,2</b>”: logarítmico (Módulo I): cada unidade = 10×.</li><li>Rótulo “sódio 12 mg/L”: M(Na⁺) = 0,012 ÷ 23 ≈ <b>5 × 10⁻⁴ mol/L</b>.</li><li><b>DBO e O₂ dissolvido</b> (mg/L): quanto menor o O₂, pior a água (Módulos B e F).</li></ul>')}
 <div>{box('red','Erros comuns','<ul><li>Usar C₁V₁ = C₂V₂ para <b>misturas de solutos diferentes</b> ou com reação: não vale.</li><li>Somar <b>concentrações</b> em vez de <b>mols</b>.</li><li>Em neutralização, esquecer o <b>excesso</b>: ele define o pH.</li></ul>')}
 <div style="margin-top:2mm">{quiz([('Quanta água adicionar a 200 mL de solução 1,0 mol/L para obter 0,25 mol/L?', 'V₂ = 1,0×200/0,25 = 800 mL → adicionar 600 mL.')])}</div></div>
</div>'''
page('E', 'Módulo E · 2 de 2', 'Diluição, mistura e rótulos: o n de soluto manda', p_E2(), key='E2')
