# -*- coding: utf-8 -*-
from lib import *
from molsvg import mol_svg, match, parse, formula, mass, COLORS
from rdkit import Chem
import re

def fml(smi):
    import re as _re
    return _re.sub(r'(\d+)', r'<sub>\1</sub>', formula(smi))

def hs(smiles, w, h, smarts=None, color='purple', labels=None, hl_idx=None, bw=1.9, fs=13, pad=0.14, rot=0):
    """Desenha e VERIFICA: o SMARTS do grupo precisa casar com a estrutura."""
    hl = []
    if smarts:
        m = parse(smiles, labels)
        n = len(match(m, smarts))
        assert n >= 1, f'SMARTS {smarts} não casa em {smiles}'
        hl = [(smarts, color)]
        QC.append(f'OK grupo {smarts} em {smiles}: {n} ocorrência(s) | {formula(smiles) if "*" not in smiles else "genérica"}')
    ha = {i: color for i in (hl_idx or [])}
    return mol_svg(smiles, w, h, hl=hl, hl_atoms=ha, labels=labels, bw=bw, fs=fs, pad=pad, rot=rot)[0]

def fcard(name, group, gen, ex, exname, app, conf, kind='purple'):
    return f'''<div class="card" style="padding:1.6mm 2.2mm">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8mm"><span style="font-size:10pt;font-weight:800">{name}</span>{tag(kind, group)}</div>
<div style="display:grid;grid-template-columns:142px 1fr;gap:1mm;align-items:center"><div class="mol">{gen}<div>representação genérica</div></div><div class="mol">{ex}<b style="color:{INK}">{exname}</b></div></div>
<div style="font-size:8.4pt;margin-top:1mm"><b class="t-green">Onde aparece:</b> {app}</div>
<div style="font-size:8.4pt;margin-top:1mm;background:{RED_L};border-radius:1mm;padding:.8mm 1.4mm"><b class="t-red">⚠ Confusão:</b> {conf}</div></div>'''

# ======================= C1 =======================
def pair(a, b, la, lb, w=150, h=62):
    return (f'<td class="center">{mol_svg(a, w, h, bw=1.8, fs=12)[0]}<b>{la}</b></td><td class="center">{mol_svg(b, w, h, bw=1.8, fs=12)[0]}<b>{lb}</b></td>')

def chain_table():
    rows = [('Normal × ramificada', 'CCCCC', 'pentano: sem ramificação', 'CC(C)CC', '2-metilbutano: ramificação (–CH₃)'),
            ('Saturada × insaturada', 'CCCC', 'butano: só ligações simples', 'C=CCC', 'but-1-eno: dupla C=C'),
            ('Homogênea × heterogênea', 'CCCCC', 'só C na cadeia', 'CCOCC', 'éter dietílico: O entre C (heteroátomo)'),
            ('Alifática × aromática', 'C1CCCCC1', 'ciclo-hexano (alicíclico)', 'c1ccccc1', 'benzeno: anel aromático')]
    for n, a, la, b, lb in rows:
        QC.append(f'OK cadeia {n}: {a} {formula(a)} | {b} {formula(b)}')
    t = ''.join(f'<tr><td style="width:24mm"><b>{n}</b></td>{pair(a, b, la, lb)}</tr>' for n, a, la, b, lb in rows)
    return f'<table style="table-layout:fixed"><tr><th style="width:24mm">Critério</th><th>A</th><th>B</th></tr>{t}</table>'

def hc_cards():
    items = [('Alcano', 'CCC', 'propano', 'CₙH₂ₙ₊₂', 'saturado · GLP (propano + butano)', None),
             ('Alceno', 'C=CC', 'propeno', 'CₙH₂ₙ', 'dupla C=C · eteno → polietileno; hormônio da maturação', 'C=C'),
             ('Alcino', 'C#CC', 'propino', 'CₙH₂ₙ₋₂', 'tripla C≡C · etino (acetileno) em soldas', 'C#C'),
             ('Ciclano', 'C1CCCCC1', 'ciclo-hexano', 'CₙH₂ₙ', 'anel saturado · isômero dos alcenos', None),
             ('Aromático', 'c1ccccc1', 'benzeno', 'C₆H₆', 'anel com elétrons π deslocalizados · tóxico', 'c1ccccc1'),
             ('Diene', 'C=CC=C', 'buta-1,3-dieno', 'CₙH₂ₙ₋₂', '2 duplas · matéria-prima da borracha sintética', 'C=CC=C')]
    for n, s, nm, gen, app, hlp in items: QC.append(f'OK hidrocarboneto {nm} {s}: {formula(s)}')
    cells = ''
    for n, s, nm, gen, app, hlp in items:
        svg = mol_svg(s, 118, 62, hl=[(hlp, 'purple')] if hlp else [], bw=1.9, fs=12, pad=0.12)[0]
        cells += f'<div class="card" style="padding:1mm 1.6mm"><div style="display:flex;justify-content:space-between"><b>{n}</b><span class="small">{gen}</span></div><div class="mol">{svg}<b style="color:{INK}">{nm}</b> · {fml(s)}</div><div style="font-size:7.3pt;margin-top:.4mm">{app}</div></div>'
    return f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1.6mm">{cells}</div>'

def iso_panel():
    def p(a, b, la, lb, w=130, h=62):
        return f'<div style="display:flex;gap:1mm;justify-content:space-around"><div class="mol">{mol_svg(a, w, h, bw=1.8, fs=12)[0]}<b style="color:{INK}">{la}</b></div><div class="mol">{mol_svg(b, w, h, bw=1.8, fs=12)[0]}<b style="color:{INK}">{lb}</b></div></div>'
    pairs = [('CCCC(O)', 'CCC(O)C', 'butan-1-ol', 'butan-2-ol'), ('CCO', 'COC', 'etanol', 'éter dimetílico')]
    for a, b, *_ in pairs: assert formula(a) == formula(b), (a, b)
    QC.append('OK isomeria plana: C4H10O (butan-1-ol/butan-2-ol) e C2H6O (etanol/éter dimetílico) com fórmulas iguais')
    cis = mol_svg('C/C=C\\C', 130, 62, bw=1.8, fs=12)[0]; trans = mol_svg('C/C=C/C', 130, 62, bw=1.8, fs=12)[0]
    ala1 = mol_svg('N[C@@H](C)C(=O)O', 130, 84, bw=1.8, fs=12)[0]; ala2 = mol_svg('N[C@H](C)C(=O)O', 130, 84, bw=1.8, fs=12)[0]
    return f'''<div class="cols2" style="grid-template-columns:1fr 1fr">
<div><h3>Plana (muda a conectividade)</h3>
 <div class="small b" style="margin-top:.5mm">de cadeia · pentano × 2-metilbutano · mesma função, esqueleto diferente</div>
 <div class="small b">de posição · {tag('purple','mesma função, posição diferente')}</div>{p(*pairs[0])}
 <div class="small b">de função · {tag('purple','grupos diferentes')} (álcool × éter: C₂H₆O)</div>{p(*pairs[1])}</div>
<div><h3>Espacial (mesma conectividade)</h3>
 <div class="small b">geométrica (cis-trans) · exige ligantes diferentes em cada C da dupla</div>
 <div style="display:flex;gap:1mm;justify-content:space-around"><div class="mol">{cis}<b style="color:{INK}">cis-but-2-eno (PE ≈ 4 °C)</b></div><div class="mol">{trans}<b style="color:{INK}">trans-but-2-eno (PE ≈ 1 °C)</b></div></div>
 <div class="small b">óptica · carbono quiral (4 ligantes diferentes) → imagens especulares</div>
 <div style="display:flex;gap:1mm;justify-content:space-around"><div class="mol">{ala1}<b style="color:{INK}">L-alanina</b></div><div class="mol">{ala2}<b style="color:{INK}">D-alanina</b></div></div></div></div>'''

def p_C1():
    return f'''
<div class="cols2" style="grid-template-columns:1fr 1.15fr; align-items:start">
  <div><h2>Por que o carbono faz tantas moléculas?</h2><p>O carbono faz <b>4 ligações</b> (tetravalente) e liga-se a outros carbonos em cadeias, anéis e ramificações, com ligações simples, duplas ou triplas. Toda estrutura orgânica obedece à regra: <b>cada C tem 4 ligações; cada H, 1; cada O, 2; cada N, 3</b>. Conferir isso evita erros de leitura.</p>
  {box('red','Erros comuns','<ul><li>Contar H que não aparecem: no desenho de linhas, cada vértice é um C e os H completam as 4 ligações.</li><li><b>Ciclano ≠ benzeno:</b> ciclo-hexano é saturado (C₆H₁₂); benzeno é aromático (C₆H₆).</li><li>Alcenos e ciclanos têm a <b>mesma fórmula</b> CₙH₂ₙ (são isômeros).</li></ul>')}</div>
  <div>{chain_table()}</div>
</div>
<div><h2>Os hidrocarbonetos: só C e H (apolares: Módulos A e B)</h2>{hc_cards()}
<div class="cap">{tag('purple','roxo')} = ligação múltipla ou anel aromático (região reativa). A cadeia de C–H é a parte <span class="t-amber b">apolar</span>.</div></div>
<div><h2>Isomeria: mesma fórmula, estruturas diferentes</h2>{iso_panel()}</div>'''
page('C', 'Módulo C · 1 de 5', 'Cadeias, hidrocarbonetos e isomeria', p_C1(), key='C1')

# ======================= C2 e C3 =======================
def gen(smi, labels, hl_idx, w=140, h=118):
    return mol_svg(smi, w, h, hl_atoms={i: 'purple' for i in hl_idx}, labels=labels, bw=1.9, fs=14, pad=0.16)[0]

def p_C2():
    cards = [
        fcard('Álcool', '–OH em C saturado', gen('*O', {0: 'R'}, [1]), hs('CCO', 200, 118, '[CX4][OX2H:1]'), 'etanol',
              'bebidas, combustível, álcool 70% (antisséptico); <b>glicerol</b> (3 OH)', 'álcool × fenol: o OH está em C <b>saturado</b> (inclusive o benzílico, ligado à cadeia lateral).'),
        fcard('Fenol', '–OH no anel aromático', mol_svg('Oc1ccccc1', 140, 118, hl_atoms={0: 'purple'}, bw=1.9, fs=14, pad=0.16)[0], hs('Oc1ccccc1', 200, 118, '[c][OX2H:1]'), 'fenol',
              'desinfetantes, plásticos (baquelite), <b>vanilina, adrenalina</b> (OH aromático)', 'fenol × álcool: OH <b>diretamente no anel</b>; mais ácido que o álcool (pKₐ ≈ 10 × 16).'),
        fcard('Enol', '–OH em C=C (só p/ diferenciar)', gen('*C(=C)O', {0: 'R'}, [3]), hs('C=CO', 200, 118, '[CX3]=[CX3][OX2H:1]'), 'etenol (instável)',
              'raro e instável: converte-se em aldeído/cetona (tautomeria)', 'enol × álcool × fenol: OH em carbono de <b>dupla não aromática</b>.'),
        fcard('Éter', '–O– entre dois C', gen('*O*', {0: 'R', 2: "R'"}, [1]), hs('CCOCC', 200, 118, '[#6][OX2:1][#6]'), 'éter dietílico',
              'solventes (éter etílico), aditivo MTBE; sem LH com ele mesmo → PE baixo', 'éter × éster: o éter <b>não tem C=O</b>.'),
        fcard('Aldeído', '–CHO (C=O na ponta)', gen('*C(=O)*', {0: 'R', 3: 'H'}, [1, 2]), hs('CC=O', 200, 118, '[CX3H1:1]=[O:2]'), 'etanal',
              'formol (metanal), aroma de amêndoa (benzaldeído), <b>vanilina</b>', 'aldeído × cetona: o C=O do aldeído está na <b>extremidade</b> e liga-se a H. Oxida a ácido com facilidade.'),
        fcard('Cetona', '–CO– entre dois C', gen('*C(=O)*', {0: 'R', 3: "R'"}, [1, 2]), hs('CC(C)=O', 200, 118, '[#6][CX3:1]([#6])=[O:2]'), 'propanona (acetona)',
              'removedor de esmalte, solvente; corpos cetônicos', 'cetona × aldeído: C=O <b>no meio</b> da cadeia (sem H no C=O). Não oxida facilmente.')]
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{"".join(cards)}</div>'
page('C', 'Módulo C · 2 de 5', 'Funções oxigenadas I: álcool, fenol, éter, aldeído e cetona', p_C2(), key='C2')

def p_C3():
    cards = [
        fcard('Ácido carboxílico', '–COOH', gen('*C(=O)O', {0: 'R'}, [1, 2, 3]), hs('CC(=O)O', 200, 118, '[CX3:1](=[O:2])[OX2H1:3]'), 'ácido acético',
              'vinagre, ácido fórmico (formigas), <b>ácidos graxos</b>, aminoácidos', 'ácido × éster: no ácido o O liga-se a <b>H</b> (doa H⁺); no éster, a <b>R</b>.'),
        fcard('Éster', '–COO– (C=O e O–R)', gen('*C(=O)O*', {0: 'R', 4: "R'"}, [1, 2, 3]), hs('CC(=O)OCC', 200, 118, '[#6][CX3:1](=[O:2])[OX2:3][#6]'), 'acetato de etila',
              'aromas de frutas, <b>triglicerídeos</b>, poliéster (PET), biodiesel', 'éster × éter e éster × ácido: tem C=O <b>e</b> um O ligado a outro C.'),
        fcard('Amina', '–N (sem C=O)', gen('*N', {0: 'R'}, [1]), hs('CCN', 200, 118, '[NX3;!$(N-C=O):1]'), 'etilamina',
              'odor de peixe (trimetilamina), dopamina, <b>adrenalina</b>; caráter básico', 'amina × amida: na amina o N <b>não está ligado a C=O</b>.'),
        fcard('Amida', '–CO–N', gen('*C(=O)N', {0: 'R'}, [1, 2, 3]), hs('CC(N)=O', 200, 118, '[NX3:1][CX3:2]=[O:3]'), 'etanamida (acetamida)',
              '<b>ligação peptídica</b> (proteínas), ureia, paracetamol, náilon', 'amida × amina: N <b>ligado a C=O</b>. Não é básica como a amina.'),
        fcard('Haleto orgânico', '–X (F, Cl, Br, I)', mol_svg('**', 140, 118, labels={0: 'R', 1: 'X'}, hl_atoms={1: 'purple'}, bw=1.9, fs=14, pad=0.2)[0], hs('CCCl', 200, 118, '[CX4][Cl:1]'), 'cloroetano',
              'CFC (refrigeração; destroem o O₃), PVC, anestésico local em spray, DDT', 'haleto orgânico (C–X <b>covalente</b>) ≠ sal haleto (NaCl, <b>iônico</b>).', 'purple'),
        fcard('Sulfuradas e outras', '–SH · –SO₂NH₂ · –NO₂', gen('*S', {0: 'R'}, [1]), hs('CCS', 200, 118, '[SX2H:1]'), 'etanotiol (tiol)',
              'odor adicionado ao GLP; sulfonamida e nitro em fármacos (ex.: nimesulida, ENEM 2024 via Aprova Total)', 'não aparecem nas listas de maior incidência: reconheça o grupo, não decore o nome.')]
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{"".join(cards)}</div>'
page('C', 'Módulo C · 3 de 5', 'Funções oxigenadas II e nitrogenadas: ácido, éster, amina, amida e haleto', p_C3(), key='C3')

# ======================= C4 =======================
def p_C4():
    rows = [('Álcool', '–OH', 'OH em C saturado', 'etanol, glicerol'), ('Fenol', '–OH', 'OH ligado ao anel aromático', 'fenol, vanilina*'), ('Éter', '–O–', 'O entre 2 C, sem C=O', 'éter etílico'),
            ('Aldeído', '–CHO', 'C=O na ponta (com H)', 'metanal, vanilina*'), ('Cetona', '–CO–', 'C=O entre 2 C', 'acetona'), ('Ác. carboxílico', '–COOH', 'C=O + OH no mesmo C', 'vinagre'),
            ('Éster', '–COO–', 'C=O + O–C', 'gorduras, aromas'), ('Amina', '–NH₂, –NHR, –NR₂', 'N sem C=O', 'adrenalina*'), ('Amida', '–CONH₂', 'N ligado ao C=O', 'ureia, peptídeos'), ('Haleto', '–F –Cl –Br –I', 'halogênio em C', 'CFC, PVC')]
    t = ''.join(f'<tr><td><b>{a}</b></td><td><b class="t-purple">{b}</b></td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    def row(a, b, la, lb, rule, hla, hlb):
        A = hs(a, 170, 70, hla, bw=1.8, fs=12); B = hs(b, 170, 70, hlb, bw=1.8, fs=12)
        return f'<div style="display:grid;grid-template-columns:172px 172px 1fr;gap:2mm;align-items:center;border-bottom:.25mm solid {LGRAY}"><div class="mol">{A}<b style="color:{INK}">{la}</b></div><div class="mol">{B}<b style="color:{INK}">{lb}</b></div><div style="font-size:8pt">{rule}</div></div>'
    dist = ''.join([
        row('CCO', 'Oc1ccccc1', 'ÁLCOOL (etanol)', 'FENOL', '<b class="t-purple">Álcool × fenol:</b> onde está o OH? Em C <b>saturado</b> → álcool. Direto no <b>anel aromático</b> → fenol.', '[CX4][OX2H:1]', '[c][OX2H:1]'),
        row('CCC=O', 'CC(C)=O', 'ALDEÍDO (propanal)', 'CETONA (propanona)', '<b class="t-purple">Aldeído × cetona:</b> C=O na <b>ponta</b> (tem H) → aldeído. C=O <b>entre dois C</b> → cetona.', '[CX3H1:1]=[O:2]', '[#6][CX3:1]([#6])=[O:2]'),
        row('CCOCC', 'CC(=O)OCC', 'ÉTER (éter dietílico)', 'ÉSTER (acetato de etila)', '<b class="t-purple">Éter × éster:</b> o éster tem <b>C=O</b> ao lado do O. Éter: só “C–O–C”.', '[#6][OX2:1][#6]', '[#6][CX3:1](=[O:2])[OX2:3][#6]'),
        row('CCN', 'CC(N)=O', 'AMINA (etilamina)', 'AMIDA (etanamida)', '<b class="t-purple">Amina × amida:</b> N <b>ligado a C=O</b> → amida. Sem C=O no N → amina.', '[NX3;!$(N-C=O):1]', '[NX3:1][CX3:2]=[O:3]'),
        row('CC(=O)O', 'CC(=O)OC', 'ÁCIDO CARBOXÍLICO', 'ÉSTER (acetato de metila)', '<b class="t-purple">Ácido × éster:</b> ácido tem <b>O–H</b> (doa H⁺, faz LH); éster tem <b>O–C</b> (sem H ácido). A esterificação liga os dois.', '[CX3:1](=[O:2])[OX2H1:3]', '[#6][CX3:1](=[O:2])[OX2:3][#6]')])
    return f'''
<div class="cols2" style="grid-template-columns:1fr 1fr 0fr;display:block"><h2>Tabela de reconhecimento rápido: procure o grupo, leia a pista</h2>
<table><tr><th>Função</th><th>Grupo</th><th>Pista visual</th><th>Onde aparece</th></tr>{t}</table>
<div class="cap">*Moléculas com várias funções (próxima página). Hidrocarbonetos: só C e H.</div></div>
<div><h2>As cinco distinções que as provas mais exploram</h2>{dist}</div>
{box('ink','Método de leitura em 3 passos','<b>① Procure O e N</b> (os “átomos de assinatura”). <b>② Veja a que cada um se liga:</b> C=O? H? anel? outro C? <b>③ Nomeie o grupo.</b> Em molécula grande, faça isso para cada heteroátomo, de uma ponta à outra, marcando o que já leu.')}'''
page('C', 'Módulo C · 4 de 5', 'Reconhecimento rápido e as cinco distinções clássicas', p_C4(), key='C4')

# ======================= C5 =======================
def exercise(smiles, groups, w=250, h=150):
    """groups: lista de (smarts_com_mapa, nome). Retorna svg com pinos numerados e lista de respostas."""
    m = parse(smiles); pins = []; ans = []; n = 1
    for sm, nome in groups:
        ms_ = match(m, sm); assert ms_, (smiles, sm)
        for mt in ms_:
            pins.append((n, list(mt))); ans.append(f'<b>{n}</b> {nome}'); n += 1
    svg = mol_svg(smiles, w, h, pins=pins, bw=1.9, fs=14, pad=0.16)[0]
    QC.append(f'OK exercício {smiles}: ' + '; '.join(re.sub('<[^>]+>', '', a) for a in ans))
    return svg, ans

def p_C5():
    ex = [('Aspirina (AAS)', 'CC(=O)Oc1ccccc1C(=O)O', [('[#6][CX3:1](=[O:2])[OX2:3][c]', 'éster'), ('[CX3:1](=[O:2])[OX2H1:3]', 'ácido carboxílico')]),
          ('Vanilina', 'COc1cc(C=O)ccc1O', [('[CX4][OX2:1][c]', 'éter'), ('[CX3H1:1]=[O:2]', 'aldeído'), ('[c][OX2H:1]', 'fenol')]),
          ('Adrenalina', 'CNC[C@H](O)c1ccc(O)c(O)c1', [('[NX3;!$(N-C=O):1]', 'amina'), ('[CX4][OX2H:1]', 'álcool'), ('[c][OX2H:1]', 'fenol')]),
          ('Paracetamol', 'CC(=O)Nc1ccc(O)cc1', [('[NX3:1][CX3:2]=[O:3]', 'amida'), ('[c][OX2H:1]', 'fenol')]),
          ('Glicina (aminoácido)', 'NCC(=O)O', [('[NX3;!$(N-C=O):1]', 'amina'), ('[CX3:1](=[O:2])[OX2H1:3]', 'ácido carboxílico')]),
          ('Triglicerídeo (modelo curto)', 'CCCC(=O)OCC(OC(=O)CCC)COC(=O)CCC', [('[#6][CX3:1](=[O:2])[OX2:3][CX4]', 'éster')])]
    cards = ''
    for nome, smi, gr in ex:
        svg, ans = exercise(smi, gr, 250, 138)
        cards += f'<div class="card" style="padding:1.2mm 1.6mm"><div style="display:flex;justify-content:space-between"><b>{nome}</b><span class="small">{fml(smi)}</span></div><div class="mol">{svg}</div><div style="font-size:7.4pt;color:{GRAY};border-top:.25mm dashed {LGRAY};padding-top:.6mm">Funções: ① ______ ② ______ {"③ ______" if len(ans) > 2 else ""}{"④ ______" if len(ans) > 3 else ""}</div></div>'
    warm = ''
    for nome, smi, hlq, ans in [('etanol', 'CCO', '[CX4][OX2H:1]', 'álcool'), ('ácido acético', 'CC(=O)O', '[CX3:1](=[O:2])[OX2H1:3]', 'ácido carboxílico'), ('acetona', 'CC(C)=O', '[#6][CX3:1]([#6])=[O:2]', 'cetona'), ('glicerol', 'OCC(O)CO', '[CX4][OX2H:1]', 'álcool (×3)')]:
        _ = hs(smi, 10, 10, hlq)
        warm += f'<div class="card" style="padding:1mm 1.6mm;text-align:center"><div class="mol">{mol_svg(smi, 120, 62, bw=1.8, fs=12)[0]}</div><b>{nome}</b><div class="small">?</div></div>'
    gab = ' · '.join(f'<b>{n}</b>: ' for n, *_ in ex)
    return f'''
<div><h2>Aquecimento: qual é a função?</h2><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2mm">{warm}</div>
<div class="small" style="margin-top:.8mm">Respostas: etanol = álcool · ácido acético = ácido carboxílico · acetona = cetona · glicerol = álcool (3 grupos –OH).</div></div>
<div><h2>Identifique todas as funções (os números marcam os grupos)</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{cards}</div></div>
{box('ink','Gabarito','<b>Aspirina:</b> ① éster, ② ácido carboxílico (anel aromático: não é função). <b>Vanilina:</b> ① éter, ② aldeído, ③ fenol. <b>Adrenalina:</b> ① amina, ② álcool, ③ e ④ fenol (duas hidroxilas aromáticas). <b>Paracetamol:</b> ① amida, ② fenol. <b>Glicina:</b> ① amina, ② ácido carboxílico. <b>Triglicerídeo:</b> ①, ② e ③ éster: três ésteres ligam três ácidos graxos ao glicerol (Módulo D).')}'''
page('C', 'Módulo C · 5 de 5', 'Treino visual: várias funções numa mesma molécula', p_C5(), key='C5')
