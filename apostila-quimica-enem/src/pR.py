# -*- coding: utf-8 -*-
from lib import *
from molsvg import mol_svg
from chk import num, fbal, fmass
import math

num('Q3: etanol 4,6 kg → mol', 4600/46, 100); num('Q3: CO2 (kg)', 200*44/1000, 8.8)
num('Q4: ΔE Zn/Ag', 0.80 - (-0.76), 1.56)

def q(n, topic, text, opts, extra=''):
    o = ''.join(f'<div style="display:flex;gap:1.6mm;margin-top:.5mm"><b>{chr(65+i)})</b><span>{t}</span></div>' for i, t in enumerate(opts))
    return f'<div style="margin-bottom:1.2mm"><div style="display:flex;gap:1.6mm;align-items:center"><span class="step">{n}</span><b>{topic}</b></div><div style="font-size:8.4pt;margin-top:.6mm">{text}</div>{extra}<div style="font-size:8.2pt">{o}</div></div>'

def p_R1():
    van = mol_svg('COc1cc(C=O)ccc1O', 200, 110, bw=1.9, fs=13, pad=0.16)[0]
    qs = [
     q(1, 'Polaridade e destino ambiental (original)', 'Um inseticida organoclorado apresenta molécula simétrica, com várias ligações C–Cl, e é praticamente insolúvel em água. Após seu uso em uma lavoura, ele foi detectado em um lago vizinho. Em qual material o composto tende a se concentrar?',
       ['Água do lago, por formação de ligações de hidrogênio.', 'Sais dissolvidos, por interações íon-dipolo.', 'Gordura dos peixes, por interações do tipo London com moléculas de baixa polaridade.', 'Gases dissolvidos, por ligações iônicas.', 'Esqueleto dos peixes, por ligações metálicas com o cálcio.']),
     q(2, 'Funções orgânicas (original)', 'A vanilina, responsável pelo aroma de baunilha, tem a estrutura ao lado. As funções oxigenadas presentes são:',
       ['álcool, éster e aldeído.', 'fenol, éter e aldeído.', 'fenol, éster e cetona.', 'álcool, éter e cetona.', 'ácido carboxílico, éter e fenol.'], f'<div class="center">{van}</div>'),
     q(3, 'Estequiometria (original)', 'Em uma viagem, um veículo flex consome <b>4,6 kg de etanol</b> (C₂H₅OH; 46 g/mol). Considerando combustão completa, a massa aproximada de CO₂ (44 g/mol) liberada é:',
       ['4,4 kg', '6,6 kg', '8,8 kg', '13,2 kg', '17,6 kg']),
     q(4, 'Eletroquímica (original)', 'Montou-se uma pilha com eletrodos de zinco e de prata. Dados: E°(Zn²⁺/Zn) = −0,76 V; E°(Ag⁺/Ag) = +0,80 V. Sobre essa pilha, é correto afirmar:',
       ['A prata é o ânodo e a diferença de potencial é 0,04 V.', 'O zinco é o ânodo e a diferença de potencial é 1,56 V.', 'O zinco é o cátodo e a diferença de potencial é 1,56 V.', 'Os elétrons fluem da prata para o zinco, com 0,04 V.', 'A prata é o ânodo e sua massa diminui.']),
     q(5, 'Equilíbrio e ambiente (original)', 'O aumento do CO₂ atmosférico desloca, nos oceanos, o equilíbrio CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻. Conchas de CaCO₃ reagem com H⁺ (CaCO₃ + H⁺ ⇌ Ca²⁺ + HCO₃⁻). Como consequência:',
       ['o pH aumenta e a formação de conchas é favorecida.', 'o pH diminui e a dissolução do CaCO₃ é favorecida.', 'o pH não varia, pois a água do mar é neutra.', 'o pH diminui e a precipitação do CaCO₃ é favorecida.', 'o pH aumenta e o equilíbrio desloca-se para a esquerda.'])]
    gab = '''<ol style="font-size:8.2pt;padding-left:4mm">
<li><b>C.</b> As ligações C–Cl são polares, mas a simetria anula os dipolos: molécula de <b>baixa polaridade</b>. Interage por London com meios apolares, como as gorduras (bioacumulação). A, B, D e E invocam interações que exigem polaridade, íons ou metais.</li>
<li><b>B.</b> O –OH ligado ao anel é <b>fenol</b>; o –OCH₃ (O entre C e anel) é <b>éter</b>; –CHO é <b>aldeído</b>. Não há C=O com O–R (éster) nem C=O entre dois C (cetona).</li>
<li><b>C.</b> n = 4600 ÷ 46 = 100 mol de etanol. C₂H₅OH + 3 O₂ → <b>2</b> CO₂ + 3 H₂O → 200 mol de CO₂ × 44 g/mol = 8 800 g = <b>8,8 kg</b>.</li>
<li><b>B.</b> O de menor E° (Zn) oxida: é o ânodo. ΔE° = E°cátodo − E°ânodo = 0,80 − (−0,76) = <b>1,56 V</b>. Os elétrons vão do Zn para a Ag; a massa de Ag aumenta (Ag⁺ + e⁻ → Ag).</li>
<li><b>B.</b> Mais CO₂ → mais H₂CO₃ → mais H⁺: <b>pH diminui</b>. Mais H⁺ desloca CaCO₃ + H⁺ ⇌ Ca²⁺ + HCO₃⁻ para a direita: <b>conchas se dissolvem</b> (Le Chatelier).</li></ol>'''
    return f'''<div class="cols2" style="grid-template-columns:1fr 1fr;gap:5mm"><div>{qs[0]}{qs[1]}</div><div>{qs[2]}{qs[3]}{qs[4]}</div></div>
{box('ink','Gabarito comentado','' + gab)}
<div class="small">Questões <b>originais</b>, elaboradas no estilo do ENEM (contextualizadas, com raciocínio causal). Não reproduzem itens oficiais. Referências a itens oficiais ao longo da apostila (2019, 2022, 2023, 2024) vêm do levantamento do Aprova Total e <b>não foram conferidas nos cadernos oficiais</b>.</div>'''
page('R', 'Revisão · 1 de 2', 'Questões finais no estilo ENEM, com gabarito comentado', p_R1(), key='R1')

# ======================= R2 =======================
def formulas():
    rows = [('Soluções', 'C = m/V (g/L) · M = n/V (mol/L) · n = m/MM · C = M·MM · C₁V₁ = C₂V₂ · ppm = mg/L'), ('Estequiometria', 'n = m/MM · V = n × 22,4 L (CNTP) · η = real/teórico × 100 · m pura = m amostra × pureza'),
            ('Gases', 'PV = nRT (R = 0,082 atm·L/mol·K; T em kelvin) · mesma T e P: proporção de volumes = proporção de mols'), ('pH', 'pH = −log[H⁺] · pOH = −log[OH⁻] · Kw = [H⁺][OH⁻] = 10⁻¹⁴ · pH + pOH = 14 (25 °C)'),
            ('Equilíbrio', 'Kc = [prod]ᶜ[prod]ᵈ/[reag]ᵃ[reag]ᵇ · Le Chatelier: o sistema atenua a perturbação · catalisador não desloca'), ('Eletroquímica', 'ΔE° = E°cátodo − E°ânodo · Q = i·t · n(e⁻) = Q/96 500 · ânodo = oxidação, cátodo = redução'),
            ('Termoquímica', 'ΔH = H(prod) − H(reag) · Lei de Hess (soma de ΔH) · ΔH ≈ Σ(lig. rompidas) − Σ(lig. formadas)'), ('Cinética', 'v = |Δ[ ]|/Δt · fatores: [ ], T, superfície, catalisador (↓Eₐ, ΔH igual)')]
    return '<table><tr><th style="width:24mm">Tema</th><th>Fórmulas e relações</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in rows) + '</table>'

def p_R2():
    src = [('SAS Educação, <i>Raio-X ENEM 2009–2025</i> (PDF, mar/2026): 599 itens de Química', '<b>lido integralmente</b> (10 p.). Não descreve a metodologia de classificação.'),
           ('Aprova Total, “Química no Enem: assuntos que mais aparecem” (atual. 12/11/2026) · Dossiê ENEM 2025 (2016–2025)', '<b>lido integralmente</b>. Percentuais sobre questões de Química, outra taxonomia: não somados com o SAS.'),
           ('Inep, <i>Matrizes de Referência do ENEM</i> (publ. 17/07/2026)', 'página institucional lida; o PDF <b>não pôde ser baixado</b>.'),
           ('Inep, <i>Provas e Gabaritos</i>', 'página lida; conteúdo das provas carrega por JavaScript e os PDFs <b>não puderam ser baixados</b>: nenhum item oficial foi conferido.'),
           ('P. Valim (Ciência em Ação), “A Química no ENEM 2021” e “Geometria Molecular (2/3)”', '<b>transcrições lidas</b>; usadas para conferir abordagem didática.'),
           ('Prof. Gabriel Cabral, “REVISÃO ENEM: Química”', 'conteúdo exclusivo para membros: <b>apenas metadados</b> acessados; não usado como fonte.'),
           ('Brasil Escola e materiais de outras instituições', '<b>não consultados diretamente</b>. Valores de tabelas (PE, solubilidade, E°, ΔH, EN) são de livros-texto, arredondados, <b>sem conferência contra fonte primária</b> neste ambiente.')]
    t = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in src)
    n_pages = len(PAGES) + 1
    return f'''
<div><h2>Folha de fórmulas</h2>{formulas()}</div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('ink','Quatro raciocínios que resolvem a maioria das questões','<ol><li><b>Polaridade → interação → propriedade</b> (solubilidade, PE, extração, bioacumulação).</li><li><b>Reconhecer o grupo funcional</b> e prever a reação (éster ↔ ácido + álcool).</li><li><b>Em mol, a equação é proporção</b> (estequiometria, soluções, Faraday).</li><li><b>Perturbou? Compare sentido e energia</b> (Le Chatelier, Ea, ΔH, ânodo e cátodo).</li></ol>')}
 {box('red','O que NÃO está nesta apostila','Átomos e modelos atômicos (5,9% no Aprova Total), radioatividade, gases (além do básico), coligativas, funções inorgânicas além do essencial, nomenclatura sistemática (IUPAC). Estude à parte, se a sua prova-alvo exigir.')}
</div>
<div><h2>Fontes consultadas e status de acesso</h2><table><tr><th>Fonte</th><th>O que foi feito</th></tr>{t}</table></div>
<div class="cols2" style="grid-template-columns:1fr 1fr">
 {box('green','Controle de qualidade (automático)',f'<ul><li><b>{n_pages} páginas</b> A4 (limite: 40).</li><li><b>{len(QC)} verificações automáticas</b> executadas na geração: grupos funcionais casados por SMARTS em cada estrutura, valências (RDKit), balanceamento de equações e cálculos dos exemplos.</li><li>Estruturas por <b>RDKit</b> e diagramas em SVG vetorial; texto estourado verificado por página.</li></ul>')}
 {box('amber','Limitações','<ul><li>Sem confronto questão a questão com provas oficiais.</li><li>Sem dados de 2026 (prova não aplicada na data).</li><li>Frequência histórica orienta; <b>não prevê</b> o que cairá. Figuras esquemáticas.</li></ul>')}
</div>'''
page('R', 'Revisão · 2 de 2', 'Folha de fórmulas, fontes e controle de qualidade', p_R2(), key='R2')
