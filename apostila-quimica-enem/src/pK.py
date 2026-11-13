# -*- coding: utf-8 -*-
from lib import *
from figs import *
from chk import num
import math

num('Hess: C + ½O2 → CO', -394 - (-283), -111); num('energia de ligação H2 + Cl2 → 2HCl', 436 + 243 - 2*431, -183)
comb = [('H₂', 285.8, 2.016, 0), ('CH₄', 890.3, 16.04, 1), ('C₈H₁₈ (octano)', 5471, 114.23, 8), ('C₂H₅OH (etanol)', 1367, 46.07, 2), ('C₆H₁₂O₆ (glicose)', 2803, 180.16, 6)]
rows = [(n, dh/m, nco2/dh*1000) for n, dh, m, nco2 in comb]
for n, e, c in rows: num(f'kJ/g {n}', e, e)

def diag():
    s = Svg(330, 200)
    for k, (x0, title, up) in enumerate([(8, 'EXOTÉRMICA  ΔH < 0', False), (176, 'ENDOTÉRMICA  ΔH > 0', True)]):
        s.line(x0+14, 24, x0+14, 160, INK, 1.8); s.line(x0+14, 160, x0+150, 160, INK, 1.8); s.text(x0+8, 92, 'H', 10, INK, 'middle', 800, rot=-90)
        yr, yp = (60, 116) if not up else (116, 60)
        s.line(x0+30, yr, x0+66, yr, INK, 3); s.line(x0+100, yp, x0+136, yp, INK, 3)
        s.path(f'M{x0+66},{yr} C{x0+80},{yr} {x0+86},{(yr+yp)/2} {x0+100},{yp}', stroke=GRAY, sw=1.6, dash='4 3')
        s.text(x0+48, yr-6, 'reagentes', 8.8, INK, 'middle', 800); s.text(x0+118, yp-6, 'produtos', 8.8, INK, 'middle', 800)
        s.arrow(x0+84, yr+2, x0+84, yp-2 if False else yp, 'green' if not up else 'red', 2.4)
        s.text(x0+70, 24, title, 9.6, GREEN_D if not up else RED_D, 'middle', 900)
        s.text(x0+70, 182, 'libera calor' if not up else 'absorve calor', 9.6, INK, 'middle', 800)
    return s.render()

def bars():
    s = Svg(330, 200)
    ax = Axes(s, 108, 12, 210, 150, (0, 150), (0, 5)); s.line(108, 12, 108, 162, INK, 1.4); s.line(108, 162, 318, 162, INK, 1.4)
    for i, (n, e, c) in enumerate(rows):
        y = 18 + i*29; w = e/150*200
        s.text(102, y+13, n, 9.2, INK, 'end', 700); s.rect(108, y, w, 18, 'url(#hatch-orange)' if i else ORANGE_L, ORANGE_D, 2, 1.4)
        s.text(112+w, y+13, f'{e:.0f}'.replace('.', ','), 9.6, INK, 'start', 800)
    for v in (0, 50, 100, 150): s.text(108+v/150*200, 176, str(v), 8.8, GRAY, 'middle', 700)
    s.text(213, 192, 'energia liberada na combustão (kJ por g)', 9.2, INK, 'middle', 800)
    return s.render()

def p_K1():
    tco2 = ''.join(f'<tr><td>{n}</td><td class="center">{e:.1f}'.replace('.', ',') + f'</td><td class="center">{c:.2f}'.replace('.', ',') + '</td></tr>' for n, e, c in rows)
    return f'''
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
 <div><h2>Entalpia: diagramas</h2>{diag()}</div>
 <div><h2>ΔH e seu sinal</h2><span class="eq">ΔH = H(produtos) − H(reagentes)</span>
 <ul style="margin-top:1.2mm"><li><b>Exotérmica</b> (ΔH &lt; 0): produtos mais “baixos”; libera calor; o ambiente <b>esquenta</b>. Combustão, respiração, neutralização, solidificação, condensação.</li><li><b>Endotérmica</b> (ΔH &gt; 0): absorve calor; o ambiente <b>esfria</b>. Fotossíntese, fusão, vaporização, dissolução de NH₄NO₃ (compressa fria).</li><li>Unidade: <b>kJ/mol</b> da equação como escrita (dobrou os coeficientes, dobra o ΔH).</li></ul>
 {box('red','Erros comuns','<ul><li>Exotérmica ≠ “rápida”: ΔH não diz nada sobre velocidade.</li><li>Sinal: ΔH &lt; 0 <b>não</b> é “perda de importância”: a energia vai do sistema para o ambiente.</li><li>Rompimento de ligação <b>absorve</b> energia; formação <b>libera</b>.</li></ul>')}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('orange','Lei de Hess: some equações, some ΔH','C(grafite) + O₂ → CO₂ &nbsp; ΔH = −394 kJ<br>CO + ½ O₂ → CO₂ &nbsp; ΔH = −283 kJ (inverta → +283)<br>C + ½ O₂ → CO &nbsp; <b>ΔH = −394 + 283 = −111 kJ/mol</b><br>O caminho não importa; só o estado inicial e o final.')}
 {box('purple','Energia de ligação (estimativa)','ΔH ≈ Σ(ligações rompidas, +) − Σ(ligações formadas)<br>H₂ + Cl₂ → 2 HCl: (436 + 243) − 2 × 431 = <b>−183 kJ</b> (exotérmica).<br>Valores médios de livros (kJ/mol): H–H 436 · Cl–Cl 243 · H–Cl 431.')}
</div>
<div class="cols2" style="grid-template-columns:340px 1fr; align-items:start">
 <div><h2>Combustíveis: energia por grama</h2>{bars()}<div class="cap">ΔH de combustão (tabelas, kJ/mol) ÷ massa molar. Hidrogênio libera mais energia por grama; a glicose (nosso combustível) libera cerca de metade do que o etanol libera.</div></div>
 <div><h2>CO₂ por energia obtida</h2><table><tr><th>Combustível</th><th>kJ/g</th><th>mol de CO₂ por MJ</th></tr>{tco2}</table>
 <div class="cap">Calculado: nº de C ÷ ΔH. O etanol emite quase tanto CO₂ por energia quanto o octano; a vantagem é o CO₂ ser <b>reabsorvido</b> pela cana (balanço de carbono), não ser “mais limpo” na queima.</div>
 {quiz([('Qual o sinal do ΔH da formação de ligações?', 'Negativo: libera energia.'), ('Por que a compressa que esfria é endotérmica?', 'A dissolução absorve calor do ambiente (e da pele).')])}</div>
</div>'''
page('K', 'Módulo K · 1 de 1', 'Termoquímica: energia absorvida ou liberada', p_K1(), key='K1')
