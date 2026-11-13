# -*- coding: utf-8 -*-
from lib import *
from figs import *

# ======================= CAPA =======================
def cover():
    s = Svg(714, 400)
    water_field(s, 0, 0, 714, 100, 24, 5)
    yt, yb = bilayer(s, 0, 118, 714, 25, L=64, gap=8, r=6.6)
    water_field(s, 0, yb + 16, 714, 100, 24, 9)
    s.label(10, 92, 'ÁGUA (meio polar)', 10, BLUE_D, '#fff', 800, 'start')
    s.label(10, yb + 108, 'ÁGUA (meio polar)', 10, BLUE_D, '#fff', 800, 'start')
    s.label(357, (yt+yb)/2+4, 'região interna apolar · cadeias hidrocarbonadas', 10.5, AMBER_D, '#FFF8E1', 700)
    art = s.render()
    legend = ''.join(f'<div style="display:flex;gap:2.2mm;align-items:flex-start"><div style="width:5mm;height:5mm;border-radius:1.2mm;background:{c};flex:none;margin-top:.5mm"></div><div><b style="font-size:8.6pt">{t}</b><div style="font-size:7.6pt;color:#CBD3E3;line-height:1.3">{d}</div></div></div>'
        for c, t, d in [(BLUE, 'AZUL', 'polaridade, água, hidrofilicidade'), (AMBER, 'ÂMBAR', 'apolar, cadeias hidrocarbonadas, lipofilicidade'),
                        (PURPLE, 'ROXO', 'estruturas e grupos funcionais orgânicos'), (GREEN, 'VERDE', 'Biologia, meio ambiente, sustentabilidade'),
                        (ORANGE, 'LARANJA', 'reações e transformações químicas'), (RED, 'VERMELHO', 'erros frequentes, alertas e exceções')])
    return f'''
<div style="margin:-11mm -13mm -10mm; padding: 16mm 13mm 12mm; background: linear-gradient(180deg,#14203B 0%,#1B2A4E 62%,#14203B 100%); color:#fff; height:297mm; display:flex; flex-direction:column; gap:7mm">
  <div style="font-size:8pt; letter-spacing:.2em; font-weight:700; color:#9FB4DC">APOSTILA VISUAL · CIÊNCIAS DA NATUREZA · ENEM</div>
  <div>
    <div style="font-size:50pt; font-weight:900; line-height:.98; letter-spacing:-.02em">Química<br>para o ENEM</div>
    <div style="font-size:13pt; font-weight:500; color:#C9D6F2; margin-top:5mm; max-width:150mm; line-height:1.3">Polaridade, grupos funcionais, soluções, reações e energia explicados por <b style="color:#fff">relações, esquemas e gráficos</b>, não por listas para decorar.</div>
  </div>
  <div style="background:#fff; border-radius:3mm; padding:3mm 0 0; overflow:hidden">{art}
    <div style="padding:2mm 4mm 3mm; color:#1B2236; font-size:8.2pt; font-weight:600; text-align:center">Uma mesma lógica química, do óleo e da água à membrana celular.</div></div>
  <div style="font-size:9.5pt; font-weight:700; letter-spacing:.04em; color:#fff">CONCEITO <span style="color:#7F95C4">→</span> REPRESENTAÇÃO VISUAL <span style="color:#7F95C4">→</span> ASSOCIAÇÃO <span style="color:#7F95C4">→</span> APLICAÇÃO <span style="color:#7F95C4">→</span> QUESTÃO</div>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:3.4mm 6mm; margin-top:auto">{legend}</div>
  <div style="font-size:7.2pt; color:#8FA3CE; border-top:.3mm solid #34456F; padding-top:2.4mm; display:flex; justify-content:space-between"><span>Edição de 13/11/2026 · prioridades baseadas em levantamentos 2009–2025 (ver fontes e limites)</span><span>Estruturas moleculares geradas e verificadas por RDKit</span></div>
</div>'''
page('I', '', '', cover(), cls='cover', key='capa')

# ======================= RAIO-X =======================
def sas_chart():
    rows = [('Funções orgânicas', 36, 'purple', 'C'), ('Reações orgânicas', 28, 'purple', 'D'), ('Aplicações da cinética química', 25, 'orange', 'H'),
            ('Pilhas', 19, 'orange', 'J'), ('Separação de misturas', 19, 'ink', 'F'), ('Tecnologias ambientais', 18, 'green', 'F'),
            ('Controle de poluição', 17, 'green', 'F'), ('Concentração de soluções', 17, 'ink', 'E'), ('Poluição da água', 16, 'green', 'F'),
            ('Tipos de reações químicas', 15, 'orange', 'G')]
    W = 440; s = Svg(W, 28*len(rows) + 30)
    x0 = 168; sc = 150/36
    for i, (name, n, col, mod) in enumerate(rows):
        y = 8 + i*28
        s.text(x0-8, y+15, name, 10.2, INK, 'end', 600)
        s.rect(x0, y+3, n*sc, 17, COL[col][0], rx=2)
        s.text(x0+n*sc+6, y+16, f'{n} · {n/599*100:.1f}%'.replace('.', ','), 10, INK, 'start', 700)
        s.text(W-4, y+16, f'Mód. {mod}', 9.5, GRAY, 'end', 600)
    top = sum(r[1] for r in rows)
    s.text(x0, 28*len(rows)+22, f'Soma dos 10 assuntos: {top} de 599 itens = {top/599*100:.0f}%'.replace('.', ','), 10, GRAY, 'start', 600)
    return s.render()

def aprova_chart():
    rows = [('Moléculas e propriedades', 8.6), ('Estequiometria', 7.9), ('Propriedades dos comp. orgânicos', 6.6), ('Separação de misturas', 6.6),
            ('Funções inorgânicas', 6.6), ('Eletroquímica', 6.6), ('Hidrocarbonetos', 5.9), ('Átomos', 5.9), ('Soluções', 5.3), ('Reações químicas', 5.3),
            ('Cinética química', 5.3), ('Reações orgânicas', 5.3), ('Equilíbrio químico', 4.6), ('Química ambiental', 3.9), ('Termoquímica', 3.3), ('Isomeria', 3.3)]
    W = 300; s = Svg(W, 18*len(rows) + 6)
    x0 = 168; sc = 100/8.6
    for i, (name, v) in enumerate(rows):
        y = 3 + i*18
        s.text(x0-6, y+11, name, 9.2, INK, 'end', 500)
        s.rect(x0, y+2, v*sc, 11, '#8C97AB', rx=2)
        s.text(x0+v*sc+5, y+11.5, f'{v:.1f}%'.replace('.', ','), 9.2, INK, 'start', 700)
    return s.render()

raiox = f'''
<div class="cols2" style="grid-template-columns: 1.12fr 1fr; align-items:start">
  <div><h2>① SAS Educação · Raio-X ENEM 2009–2025</h2>
    <div class="small" style="margin-bottom:1mm">Química: <b>599 itens</b> classificados. Barras: nº de itens e % sobre os 599. Cores = tema.</div>{sas_chart()}
    <div style="display:flex;gap:2mm;flex-wrap:wrap;margin-top:1mm">{tag('purple','orgânica')}{tag('orange','reações / transformações')}{tag('green','ambiental')}{tag('ink','misturas e soluções')}</div></div>
  <div><h2>② Aprova Total · Dossiê ENEM 2025</h2>
    <div class="small" style="margin-bottom:1mm">Provas regulares <b>2016–2025</b>; % sobre as questões de Química. <b>Outra taxonomia, outro período: não somar com ①.</b></div>{aprova_chart()}</div>
</div>
<div class="cols2" style="grid-template-columns: 1fr 1fr">
  {box('ink','O que os dados dizem (e o que não dizem)',
   '<ul><li><b>A prova é dispersa:</b> os 10 maiores assuntos do SAS somam só 35% dos itens. Estudar “só o top 10” deixa dois terços de fora.</li>'
   '<li><b>Orgânica pesa em ambas as fontes.</b> SAS: funções + reações = 64 itens (≥10,7%). Aprova Total: 4 temas orgânicos somam ≈21% (soma interna à fonte).</li>'
   '<li><b>Polaridade é a base de tudo:</b> “Moléculas e propriedades” lidera no Aprova Total e é pré-requisito de solubilidade, separação, orgânica e ambiental.</li>'
   '<li><b>Frequência histórica ≠ probabilidade futura.</b> Orienta prioridade; não promete o que cairá em 2026 ou depois.</li></ul>')}
  {box('red','Limites metodológicos',
   '<ul><li>As duas fontes não publicam como classificaram cada item; os recortes (2009–2025 × 2016–2025) e os rótulos diferem.</li>'
   '<li>Os PDFs de provas e a Matriz do Inep <b>não puderam ser baixados</b> neste ambiente; a página institucional da Matriz foi lida, mas o confronto <b>questão a questão</b> com os cadernos oficiais <b>não foi feito</b>.</li>'
   '<li>Não há dados da prova de 2026 (ainda não aplicada na data desta edição).</li>'
   '<li><b>Fora do escopo pedido:</b> “Átomos” (5,9% no Aprova Total) e radioatividade (citada por Valim): estude à parte.</li></ul>')}
</div>
<div><h2>Da evidência ao capítulo: três critérios de seleção</h2>
<table><tr><th>Bloco da apostila</th><th>① Incidência</th><th>② Pré-requisito de…</th><th>③ Rendimento em acertos</th><th>Decisão</th></tr>
<tr><td><b>A–B</b> Polaridade, forças, solubilidade</td><td>Aprova: 8,6% + 6,6%</td><td>orgânica, separação, ambiental, membrana</td><td>alto: raciocínio causal reaproveitado</td><td>{tag('blue','prioridade máxima · 11 pp.')}</td></tr>
<tr><td><b>C–D</b> Funções, reações, polímeros</td><td>SAS: 36 + 28 itens</td><td>bioquímica, sabão, plásticos</td><td>alto: reconhecimento visual rápido</td><td>{tag('purple','prioridade máxima · 8 pp.')}</td></tr>
<tr><td><b>E, G</b> Soluções, estequiometria</td><td>Aprova: 7,9% + 5,3%; SAS: 17 itens</td><td>todo cálculo químico</td><td>médio-alto: contas guiadas por método</td><td>{tag('ink','intermediário · 4 pp.')}</td></tr>
<tr><td><b>F</b> Separação e Química ambiental</td><td>SAS: 19 + (18 + 17 + 16)</td><td>polaridade, soluções</td><td>alto: interpretação de processos</td><td>{tag('green','intermediário · 4 pp.')}</td></tr>
<tr><td><b>H–K</b> Cinética, equilíbrio, pilhas, termo</td><td>SAS: 25 cinética, 19 pilhas</td><td>reações, energia</td><td>médio: gráficos e esquemas</td><td>{tag('orange','compacto · 6 pp.')}</td></tr></table></div>
<div class="small">Matriz de Referência (Inep, 2026): eixos cognitivos incluem <i>compreensão de fenômenos</i> e <i>resolução de situações-problema</i>; por isso cada tema aqui segue: conceito → visual → associação → aplicação → questão. Fontes completas e status de acesso: última página.</div>
'''
page('I', 'Pesquisa · Fase 1', 'O que a pesquisa mostrou, e como isso decidiu esta apostila', raiox, key='raiox')

# ======================= MAPA CONCEITUAL =======================
def concept_map():
    s = Svg(714, 392)
    def node(x, y, w, h, title, sub, kind, key=None):
        c = COL[kind]
        s.rect(x, y, w, h, c[2], c[0], 6, 1.8)
        s.text(x+w/2, y+16, title, 10.4, c[1], 'middle', 800)
        s.text(x+w/2, y+30, sub, 8.8, INK, 'middle', 500, lh=1.18)
    W, H = 150, 52
    X = [8, 192, 376, 556]; Y = [6, 100, 194, 288]
    node(X[0], Y[0], W, H, 'Ligações', 'elétrons de valência\neletronegatividade', 'blue')
    node(X[1], Y[0], W, H, 'Geometria e polaridade', 'simetria · soma dos dipolos', 'blue')
    node(X[2], Y[0], W, H, 'Forças intermoleculares', 'London · dipolo · lig. de H', 'blue')
    node(X[3], Y[0], W, H, 'Solubilidade', 'semelhante dissolve semelhante', 'blue')
    node(X[0], Y[1], W, H, 'Soluções', 'C, M, diluição, mistura', 'ink')
    node(X[1], Y[1], W, H, 'Funções orgânicas', 'grupos polares × cadeias apolares', 'purple')
    node(X[2], Y[1], W, H, 'Separação de misturas', 'PE · destilação · extração', 'ink')
    node(X[3], Y[1], W, H, 'Anfifílicos', 'sabão · detergente · micelas', 'amber')
    node(X[0], Y[2], W, H, 'Estequiometria', 'mol · limitante · rendimento', 'orange')
    node(X[1], Y[2], W, H, 'Reações orgânicas', 'esterificação · saponificação', 'orange')
    node(X[2], Y[2], W, H, 'Química ambiental', 'água · ar · eutrofização', 'green')
    node(X[3], Y[2], W, H, 'Fosfolipídios', 'bicamada · membrana celular', 'green')
    node(X[0], Y[3], W, H, 'Termoquímica', 'ΔH · combustíveis', 'orange')
    node(X[1], Y[3], W, H, 'Cinética', 'Ea · catalisador · enzimas', 'orange')
    node(X[2], Y[3], W, H, 'Equilíbrio, pH', 'Le Chatelier · ácidos e bases', 'orange')
    node(X[3], Y[3], W, H, 'Oxirredução', 'pilhas · eletrólise · corrosão', 'orange')
    def arr(x1, y1, x2, y2, lab=None, lx=0, ly=0, color='ink'):
        s.arrow(x1, y1, x2, y2, color, 1.7)
        if lab: s.label((x1+x2)/2+lx, (y1+y2)/2+ly+4, lab, 8.6, GRAY, '#fff', 600)
    c = lambda i: X[i] + W/2
    arr(X[0]+W, Y[0]+26, X[1], Y[0]+26)
    arr(X[1]+W, Y[0]+26, X[2], Y[0]+26)
    arr(X[2]+W, Y[0]+26, X[3], Y[0]+26)
    arr(c(3), Y[0]+H, c(3), Y[1], 'lipofilicidade', 0, 0)
    arr(X[1]+W/2, Y[0]+H, X[1]+W/2, Y[1], 'polaridade', 0, 0)
    arr(X[2]+W/2-30, Y[0]+H, X[2]+W/2-30, Y[1], 'PE', 0, 0)
    arr(c(3)+30, Y[1]+H, c(3)+30, Y[2], 'mesma lógica', 0, 0, 'green')
    arr(X[1]+W/2, Y[1]+H, X[1]+W/2, Y[2], 'grupos reagem', 0, 0)
    arr(X[2]+W/2, Y[1]+H, X[2]+W/2, Y[2], 'tratamento', 0, 0)
    s.path(f'M{X[1]+W},{Y[2]+14} L{X[1]+W+10},{Y[2]+14} L{X[1]+W+10},{Y[1]+H+22} L{X[3]+W/2-30},{Y[1]+H+22} L{X[3]+W/2-30},{Y[1]+H+2}', stroke=ORANGE, sw=1.8, marker='orange')
    s.label(X[2]+W/2, Y[1]+H+20, 'saponificação → sabão', 8.6, ORANGE_D, '#fff', 700)
    arr(c(0), Y[1]+H, c(0), Y[2], 'mol, n')
    arr(c(0), Y[2]+H, c(0), Y[3], 'energia')
    arr(X[1]+W/2, Y[2]+H, X[1]+W/2, Y[3], 'velocidade')
    arr(X[1]+W, Y[3]+26, X[2], Y[3]+26)
    arr(X[2]+W/2, Y[3], X[2]+W/2, Y[2]+H, 'chuva ácida, CO₂', 0, 0, 'green')
    arr(X[2]+W, Y[3]+26, X[3], Y[3]+26)
    arr(X[0]+W, Y[1]+26, X[1], Y[1]+26)
    s.text(8, 372, 'Setas = “leva a / é pré-requisito de”. Azul: polaridade · roxo: orgânica · laranja: reações · verde: Biologia/ambiente.', 9, GRAY, 'start', 500)
    return s.render()

toc_items = [('A', 'Ligações, polaridade e forças intermoleculares', 'A1', 'blue'), ('B', 'Solubilidade, hidrofobicidade e membrana', 'B1', 'blue'),
             ('C', 'Funções orgânicas', 'C1', 'purple'), ('D', 'Reações orgânicas, biomoléculas e polímeros', 'D1', 'orange'),
             ('E', 'Soluções e cálculos', 'E1', 'ink'), ('F', 'Separação de misturas e Química ambiental', 'F1', 'green'),
             ('G', 'Estequiometria', 'G1', 'orange'), ('H', 'Cinética química', 'H1', 'orange'), ('I', 'Equilíbrio, ácidos, bases e pH', 'I1', 'orange'),
             ('J', 'Eletroquímica', 'J1', 'orange'), ('K', 'Termoquímica', 'K1', 'orange'), ('★', 'Questões, fórmulas e fontes', 'R1', 'ink')]
toc = ''.join(f'<div style="display:flex;gap:2mm;align-items:center;padding:.9mm 0;border-bottom:.25mm dotted {LGRAY}"><span class="chip" style="--c:{COL[k][0]};--cd:{COL[k][1]};--cl:{COL[k][2]};min-width:6mm;text-align:center">{l}</span><span style="flex:1;font-weight:600">{t}</span><b>p. @@P:{key}@@</b></div>' for l, t, key, k in toc_items)
mapa = f'''
<div>{concept_map()}</div>
<div class="cols2" style="grid-template-columns: 1fr 1fr">
  <div><h2>Sumário</h2>{toc}</div>
  <div><h2>Como usar esta apostila</h2>
    <ul><li><b>Leia a pergunta do título primeiro.</b> Cada página responde: o que é? como reconhecer? por que funciona? qual a consequência? como o ENEM cobra? qual o erro comum?</li>
    <li><b>Siga as cores:</b> uma região polar é sempre <span class="t-blue b">azul</span>; uma cadeia apolar, sempre <span class="t-amber b">âmbar</span>; grupos funcionais, <span class="t-purple b">roxos</span>. Além da cor, há rótulos, símbolos e hachuras (pontos = polar; listras = apolar).</li>
    <li><b>Responda os “Teste-se” antes de olhar a resposta</b> (recuperação ativa): é o que fixa o conteúdo.</li>
    <li><b>Siga o fio condutor do mapa:</b> polaridade → forças → solubilidade → membrana; éster → esterificação → triglicerídeo → sabão.</li></ul></div>
</div>'''
page('I', 'Visão geral', 'O mapa do conteúdo: tudo se liga à polaridade e à transferência de energia', mapa, key='mapa')
