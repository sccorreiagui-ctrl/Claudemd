# -*- coding: utf-8 -*-
from lib import *
from molsvg import mol_svg, match, parse, formula
from chk import balanced, MM
from pC import fml

def M(smi, name, w=118, h=74, hl=None, labels=None, hl_atoms=None, sub=''):
    svg = mol_svg(smi, w, h, hl=hl or [], labels=labels, hl_atoms=hl_atoms, bw=1.8, fs=12, pad=0.1)[0]
    return f'<div class="mol" style="min-width:{w}px">{svg}<b style="color:{INK}">{name}</b>{("<br>"+sub) if sub else ""}</div>'

def plus(): return f'<div style="font-size:15pt;font-weight:800;color:{GRAY}">+</div>'

def arr(top='', bottom='', rev=False, w=92, color=ORANGE):
    s = Svg(w, 54)
    if rev:
        s.arrow(6, 26, w-6, 26, 'orange', 2.2); s.arrow(w-6, 34, 6, 34, 'orange', 2.2)
    else:
        s.arrow(6, 30, w-6, 30, 'orange', 2.6)
    if top: s.text(w/2, 18 if not rev else 14, top, 9.2, ORANGE_D, 'middle', 800)
    if bottom: s.text(w/2, 49, bottom, 9, ORANGE_D, 'middle', 700)
    return s.render()

def rx(*items, gap=1.2):
    return f'<div class="rx" style="gap:{gap}mm;align-items:center">' + ''.join(items) + '</div>'

def rcard(title, kind_tag, body, note=''):
    return f'<div class="card" style="padding:1.6mm 2.2mm"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.6mm"><b style="font-size:9.6pt">{title}</b>{tag("orange", kind_tag)}</div>{body}{("<div style=\'font-size:8.2pt;margin-top:.8mm\'>" + note + "</div>") if note else ""}</div>'

# ======================= D1 =======================
def p_D1():
    ESTER = [('[#6][CX3:1](=[O:2])[OX2:3][#6]', 'purple')]
    ACID = [('[CX3:1](=[O:2])[OX2H1:3]', 'purple')]
    balanced('esterificação: CH3COOH + C2H5OH → CH3COOC2H5 + H2O', [(1, 'CC(=O)O'), (1, 'CCO')], [(1, 'CC(=O)OCC'), (1, 'O')])
    esterif = rx(M('CC(=O)O', 'ácido acético', hl=ACID), plus(), M('CCO', 'etanol', hl=[('[CX4][OX2H:1]', 'purple')]), arr('H⁺, calor', 'reversível', True), M('CC(=O)OCC', 'acetato de etila', hl=ESTER), plus(), M('O', 'água', w=60, h=60))
    balanced('saponificação do triacetato (modelo): C9H14O6 + 3 NaOH → C3H8O3 + 3 CH3COONa', [(1, 'CC(=O)OCC(OC(C)=O)COC(C)=O'), (3, '[Na+].[OH-]')], [(1, 'OCC(O)CO'), (3, 'CC(=O)[O-].[Na+]')])
    balanced('transesterificação (modelo): triacetina + 3 CH3OH → glicerol + 3 acetato de metila', [(1, 'CC(=O)OCC(OC(C)=O)COC(C)=O'), (3, 'CO')], [(1, 'OCC(O)CO'), (3, 'CC(=O)OC')])
    tri = '*C(=O)OCC(OC(=O)*)COC(=O)*'; lab3 = {0: 'R', 9: 'R', 14: 'R'}
    sapon = rx(M(tri, 'triglicerídeo', 150, 96, hl=ESTER, labels=lab3), plus(), M('[Na+].[OH-]', '3 NaOH', 76, 52), arr('calor', 'saponificação'), M('OCC(O)CO', 'glicerol', 96, 80, hl=[('[CX4][OX2H:1]', 'purple')]), plus(), M('*C(=O)[O-].[Na+]', '3 sabão (R–COO⁻ Na⁺)', 130, 80, labels={0: 'R'}))
    trans = rx(M(tri, 'triglicerídeo', 150, 96, hl=ESTER, labels=lab3), plus(), M('CO', '3 metanol', 70, 52), arr('NaOH ou KOH', 'transesterificação'), M('OCC(O)CO', 'glicerol', 96, 80), plus(), M('*C(=O)OC', '3 biodiesel (éster metílico)', 140, 80, hl=ESTER, labels={0: 'R'}))
    dig = rx(M(tri, 'triacilglicerol', 150, 96, hl=ESTER, labels=lab3), plus(), M('O', '3 H₂O', 60, 52), arr('lipase', 'hidrólise enzimática'), M('OCC(O)CO', 'glicerol', 96, 80), plus(), M('*C(=O)O', '3 ácidos graxos (R–COOH)', 140, 80, hl=ACID, labels={0: 'R'}))
    chain = f'''<div style="display:flex;align-items:center;gap:1.5mm;justify-content:center;flex-wrap:nowrap;font-size:8.6pt;font-weight:800">{tag('purple','ácido + álcool')}<span>→</span>{tag('orange','esterificação')}<span>→</span>{tag('purple','éster')}<span>→</span>{tag('purple','triglicerídeo')}<span>→</span>{tag('orange','hidrólise / saponificação')}<span>→</span>{tag('amber','sabão (anfifílico)')}</div>'''
    return f'''
{chain}
{rcard('1 · Esterificação (e seu inverso, a hidrólise ácida)', 'equilíbrio', esterif, 'Ácido + álcool ⇌ éster + <b>água</b>. Reação <b>reversível</b>: retirar a água ou usar excesso de álcool <b>desloca o equilíbrio para o éster</b> (Le Chatelier, Módulo I). Ácidos fortes (H⁺) atuam como catalisador.')}
{rcard('2 · Saponificação: hidrólise básica de um triglicerídeo', 'sabão', sapon, 'Hidrólise com base forte (NaOH ou KOH): <b>irreversível</b>, porque o ácido graxo vira carboxilato (R–COO⁻), que não reage de volta com o álcool. O produto é o <b>sabão</b>: anfifílico (Módulo B).')}
{rcard('3 · Transesterificação: produção de biodiesel', 'biocombustível', trans, 'O glicerol do óleo vegetal é trocado por metanol (ou etanol): saem ésteres de cadeia longa, o <b>biodiesel</b>, e <b>glicerol</b> como subproduto.')}
<div class="cols2" style="grid-template-columns:1.25fr 1fr">
{rcard('4 · Digestão de lipídios', 'biologia', dig, '')}
{box('green','Conexão com Biologia','A <b>bile</b> (anfifílica) emulsifica a gordura em gotículas; a <b>lipase</b> hidrolisa os ésteres: cada gota tem mais superfície, o que acelera a reação (cinética, Módulo H). Produtos: ácidos graxos + glicerol (ou monoacilglicerol).')}
</div>
{box('red','Erros comuns','<ul><li><b>Sabão não é éster:</b> é o <b>sal</b> do ácido graxo (R–COO⁻ Na⁺), produto da hidrólise do éster.</li><li>Saponificação e hidrólise ácida <b>não são iguais</b>: a básica é irreversível e dá sal; a ácida é um equilíbrio e dá ácido + álcool.</li><li>Em R–COO–R′, os dois R podem ser <b>cadeias longas</b>: o grupo é o mesmo do acetato de etila.</li></ul>')}'''
page('D', 'Módulo D · 1 de 3', 'Do éster ao sabão: esterificação, hidrólise, saponificação e biodiesel', p_D1(), key='D1')

# ======================= D2 =======================
def p_D2():
    balanced('combustão do metano', [(1, 'C'), (2, 'O=O')], [(1, 'O=C=O'), (2, 'O')])
    balanced('combustão do etanol', [(1, 'CCO'), (3, 'O=O')], [(2, 'O=C=O'), (3, 'O')])
    balanced('combustão do octano', [(2, 'CCCCCCCC'), (25, 'O=O')], [(16, 'O=C=O'), (18, 'O')])
    balanced('combustão incompleta do metano → CO', [(2, 'C'), (3, 'O=O')], [(2, '[C-]#[O+]'), (4, 'O')])
    balanced('fermentação da glicose', [(1, 'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O')], [(2, 'CCO'), (2, 'O=C=O')])
    balanced('hidrogenação do eteno', [(1, 'C=C'), (1, '[H][H]')], [(1, 'CC')])
    balanced('adição de Br2 ao eteno', [(1, 'C=C'), (1, 'BrBr')], [(1, 'BrCCBr')])
    balanced('substituição: CH4 + Cl2 → CH3Cl + HCl', [(1, 'C'), (1, 'ClCl')], [(1, 'CCl'), (1, 'Cl')])
    balanced('oxidação etanol → etanal (– 2H)', [(1, 'CCO')], [(1, 'CC=O'), (1, '[H][H]')])
    OX = [('[CX4][OX2H:1]', 'purple')]
    ox1 = rx(M('CCO', 'etanol (1°)', 84, 62, hl=OX), arr('[O]', '', False, 50), M('CC=O', 'etanal', 84, 62, hl=[('[CX3H1:1]=[O:2]', 'purple')]), arr('[O]', '', False, 50), M('CC(=O)O', 'ác. acético', 84, 62, hl=[('[CX3:1](=[O:2])[OX2H1:3]', 'purple')]), gap=0.4)
    ox2 = rx(M('CC(O)C', 'propan-2-ol (2°)', 90, 62, hl=OX), arr('[O]', '', False, 50), M('CC(C)=O', 'propanona', 84, 62, hl=[('[#6][CX3:1]([#6])=[O:2]', 'purple')]), M('CC(C)(C)O', 'terc-butanol (3°)<br><b>não oxida</b>', 90, 62, hl=OX), gap=0.4)
    add = rx(M('C=C', 'eteno', 70, 48, hl=[('C=C', 'purple')]), plus(), M('[H][H]', 'H₂', 44, 36), arr('Ni, calor', 'hidrogenação', False, 78), M('CC', 'etano', 70, 48), gap=0.6)
    add2 = rx(M('C=C', 'eteno', 70, 48, hl=[('C=C', 'purple')]), plus(), M('BrBr', 'Br₂ (alaranjado)', 80, 40), arr('', 'adição', False, 56), M('BrCCBr', '1,2-dibromoetano<br>(incolor)', 100, 52), gap=0.6)
    sub = rx(M('C', 'metano', 52, 40), plus(), M('ClCl', 'Cl₂', 56, 38), arr('luz UV', 'substituição', False, 78), M('CCl', 'clorometano', 70, 48), plus(), M('Cl', 'HCl', 46, 38), gap=0.6)
    flame = Svg(300, 118)
    def fl(x, col, tip, label, sub1):
        flame.path(f'M{x},96 C{x-22},80 {x-18},50 {x},{tip} C{x+18},50 {x+22},80 {x},96 Z', col, INK, 1.4)
        flame.rect(x-26, 96, 52, 8, '#D6DBE4', GRAY, 2, 1.2)
        flame.text(x, 116, label, 9, INK, 'middle', 800)
    fl(60, '#7FB2F0', 34, 'chama azul', ''); fl(220, '#FFC94D', 24, 'chama amarela', '')
    flame.text(60, 20, 'COMPLETA', 10, GREEN_D, 'middle', 900); flame.text(60, 31, 'CO₂ + H₂O', 9.2, INK, 'middle', 800)
    flame.text(220, 12, 'INCOMPLETA', 10, RED_D, 'middle', 900); flame.text(220, 22, 'CO + C (fuligem) + H₂O', 9.2, INK, 'middle', 800)
    flame.text(140, 60, 'pouco O₂', 9.2, RED_D, 'middle', 800); flame.text(140, 72, '→', 14, RED_D, 'middle', 800)
    return f'''
{rcard('Oxidação de álcoois: o nº de H no carbono do –OH decide', 'oxirredução', '<div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm">' + ox1 + ox2 + '</div>', '<b>Primário</b> → aldeído → ácido carboxílico. <b>Secundário</b> → cetona. <b>Terciário</b>: não oxida (sem H no C do –OH). Vinho → vinagre: etanol → ácido acético. <b>Bafômetro</b>: o K₂Cr₂O₇ (alaranjado) oxida o etanol e vira Cr³⁺ (verde).')}
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {rcard('Combustão', 'energia', flame.render(), 'CH₄ + 2 O₂ → CO₂ + 2 H₂O<br>C₂H₅OH + 3 O₂ → 2 CO₂ + 3 H₂O<br>2 C₈H₁₈ + 25 O₂ → 16 CO₂ + 18 H₂O<br>Incompleta (pouco O₂): produz <b>CO</b> (tóxico, liga-se à hemoglobina) e fuligem.')}
 <div>{box('green','Biocombustíveis e fermentação','<b>Fermentação alcoólica</b> (levedura): C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂. O etanol é queimado como combustível: o CO₂ emitido é, em parte, reabsorvido pela cana em crescimento (balanço de carbono menor que o do petróleo, mas não nulo).')}
 <div style="margin-top:2mm">{box('ink','Como reconhecer o tipo de reação','<ul><li><b>Adição:</b> C=C ou C≡C “abre” e ganha átomos.</li><li><b>Substituição:</b> troca um átomo/grupo; há <b>dois</b> produtos.</li><li><b>Eliminação:</b> perde H₂O ou HX e forma C=C (etanol → eteno).</li><li><b>Oxidação:</b> mais ligações C–O ou menos C–H.</li></ul>')}</div></div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {rcard('Adição (em C=C)', 'adição', add + '<div style="height:1mm"></div>' + add2, '<b>Hidrogenação</b> transforma óleo (C=C) em gordura sólida (margarina). <b>Água de bromo</b> descora ao reagir com C=C: teste de insaturação.')}
 {rcard('Substituição (alcanos e aromáticos)', 'substituição', sub, 'Um H é trocado por outro átomo; sai HX. Alcanos precisam de luz ou calor (pouco reativos). Aromáticos preservam o anel: nitração do benzeno (HNO₃ + H₂SO₄ → nitrobenzeno).')}
</div>
{quiz([('O etanol oxida a ácido acético e o propan-2-ol, a propanona. Por que o terc-butanol não reage?', 'O carbono do –OH não tem H para ser removido na oxidação.'), ('Como distinguir, com água de bromo, hexano de hex-1-eno?', 'O hex-1-eno (C=C) descora a água de bromo por adição; o hexano não reage.'), ('Por que a combustão incompleta é mais perigosa em ambiente fechado?', 'Forma CO, gás inodoro que se liga à hemoglobina e impede o transporte de O₂.')])}'''
page('D', 'Módulo D · 2 de 3', 'Oxidação, adição, substituição e combustão: lendo reações orgânicas', p_D2(), key='D2')

# ======================= D3 =======================
def p_D3():
    from chk import atoms
    assert atoms('C=C') == {'C': 2, 'H': 4}; QC.append('OK adição: unidade repetida do polietileno (–CH2–CH2–) tem a mesma composição do monômero C2H4')
    balanced('peptídica: glicina + alanina → dipeptídeo + H2O', [(1, 'NCC(=O)O'), (1, 'N[C@@H](C)C(=O)O')], [(1, 'NCC(=O)N[C@@H](C)C(=O)O'), (1, 'O')])
    mon = [('Eteno (etileno)', 'C=C', 'polietileno (PE)', 'sacolas, filmes, garrafas'), ('Propeno', 'C=CC', 'polipropileno (PP)', 'embalagens, tampas'), ('Cloreto de vinila', 'C=CCl', 'PVC', 'tubos, conexões'),
           ('Estireno', 'C=Cc1ccccc1', 'poliestireno (PS)', 'copos, isopor'), ('Tetrafluoreteno', 'FC(F)=C(F)F', 'PTFE (teflon)', 'antiaderente')]
    for _, s, *_ in mon: QC.append(f'OK monômero de adição {s}: {formula(s)} (contém C=C)')
    cells = ''.join(f'<div class="card" style="padding:1mm 1.4mm;text-align:center"><div class="mol">{mol_svg(s, 96, 58, hl=[("C=C", "purple")], bw=1.8, fs=11, pad=0.1)[0]}<b style="color:{INK}">{n}</b></div><div style="font-size:7.6pt">→ <b>{p}</b><br>{u}</div></div>' for n, s, p, u in mon)
    cond = rx(M('OC(=O)c1ccc(cc1)C(O)=O', 'ác. tereftálico (diácido)', 130, 74, hl=[('[CX3:1](=[O:2])[OX2H1:3]', 'purple')]), plus(), M('OCCO', 'etilenoglicol (diol)', 100, 64, hl=[('[CX4][OX2H:1]', 'purple')]), arr('−H₂O', 'condensação', False, 84), M('*C(=O)c1ccc(cc1)C(=O)OCCO*', 'PET: unidade (…)ₙ', 190, 74, hl=[('[#6][CX3:1](=[O:2])[OX2:3][CX4]', 'purple')], labels={0: '', 15: ''}), gap=1)
    nylon = rx(M('OC(=O)CCCCC(O)=O', 'ác. adípico', 120, 62, hl=[('[CX3:1](=[O:2])[OX2H1:3]', 'purple')]), plus(), M('NCCCCCCN', 'hexametilenodiamina', 130, 62, hl=[('[NX3:1]', 'purple')]), arr('−H₂O', 'condensação', False, 84), M('*C(=O)CCCCC(=O)NCCCCCCN*', 'náilon 6,6: unidade (…)ₙ', 210, 62, hl=[('[NX3:1][CX3:2]=[O:3]', 'purple')], labels={0: '', 14: ''}), gap=1)
    pept = rx(M('NCC(=O)O', 'glicina', 100, 62, hl=[('[CX3:1](=[O:2])[OX2H1:3]', 'orange')]), plus(), M('N[C@@H](C)C(=O)O', 'alanina', 100, 70, hl=[('[NX3;H2:1]', 'orange')]), arr('−H₂O', 'ligação peptídica', False, 98), M('NCC(=O)N[C@@H](C)C(=O)O', 'dipeptídeo Gly-Ala', 170, 70, hl=[('[NX3:1][CX3:2]=[O:3]', 'purple')]), gap=1)
    return f'''
<div><h2>Polímeros de adição: monômeros com C=C que se encadeiam, sem perder átomos</h2><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1.6mm">{cells}</div>
<div class="cap">Cada C=C “abre” e liga-se ao próximo: (–CH₂–CH₂–)ₙ. Cadeia só de C–C (e C–H): <b>apolar e muito resistente</b>.</div></div>
<div class="cols2" style="grid-template-columns:1fr">
{rcard('Polímeros de condensação: perdem uma molécula pequena (H₂O) a cada ligação', 'condensação', cond + '<div style="height:1mm"></div>' + nylon, 'Os elos (éster no PET; amida no náilon) são grupos <b>hidrolisáveis</b>: a mesma química do Módulo D1, repetida n vezes.')}
</div>
<div class="cols2" style="grid-template-columns:1.25fr 1fr">
 {rcard('Proteínas: polímeros de aminoácidos', 'biologia', pept, 'A ligação peptídica é uma <b>amida</b> (Módulo C). A estrutura 3D é mantida por LH, interações apolares e pontes dissulfeto.')}
 <div>{rcard('Carboidratos: polímeros de glicose', 'biologia', f'<div style="display:flex;gap:2mm;align-items:center"><div class="mol" style="flex:none">{mol_svg("OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O", 128, 100, hl=[("[CX4][OX2H:1]", "purple")], bw=1.7, fs=11, pad=0.08)[0]}<b style="color:{INK}">glicose (C₆H₁₂O₆)</b></div><div style="font-size:8.2pt">Ligação glicosídica (–O–) entre glicoses, com perda de H₂O.<br><b>Amido</b> (reserva; digerido por amilases) × <b>celulose</b> (parede celular; ligação β não digerida por humanos).</div></div>', '')}</div>
</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('green','Plásticos, microplásticos e biodegradação',
 '<ul><li><b>Microplásticos</b> (&lt; 5 mm) vêm da fragmentação de plásticos e de cosméticos/tecidos. Como são <b>apolares</b>, adsorvem poluentes orgânicos de baixa polaridade (pesticidas, PCBs): a mesma lógica da lipofilicidade do Módulo B.</li><li><b>Polímeros de adição (C–C)</b> resistem a micro-organismos: persistem por séculos. <b>Poliésteres e poliamidas</b> têm elos hidrolisáveis, porém a hidrólise é lenta em condições naturais.</li><li><b>Reciclagem:</b> PET (1), PEAD (2), PVC (3), PEBD (4), PP (5), PS (6).</li></ul>')}
 {box('red','Erros comuns','<ul><li><b>“Biodegradável” ≠ “de origem biológica”.</b> Há plástico de fonte renovável que não biodegrada e plástico de petróleo biodegradável.</li><li><b>Adição × condensação:</b> se o polímero liberou H₂O (ou HCl), foi <b>condensação</b>. Se o monômero tinha C=C e nada saiu, foi <b>adição</b>.</li><li>Os elos “éster” do PET e do biodiesel são o <b>mesmo grupo funcional</b>.</li></ul>')}
</div>'''
page('D', 'Módulo D · 3 de 3', 'Polímeros e biomoléculas: cadeias de monômeros e o destino dos plásticos', p_D3(), key='D3')
