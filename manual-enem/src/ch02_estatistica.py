"""Capítulo 2 – Estatística, gráficos, probabilidade e análise combinatória (tópico 5 + complementares)."""
import math
from lib import *
from svg import Fig, Plot, fmt

LABEL = 'CAP. 2 · ESTATÍSTICA, GRÁFICOS E PROBABILIDADE'

DATA = [3, 4, 4, 5, 6, 8, 14]


def fig_dots():
    f = Fig(340, 146)
    x0, sc = 16, 22
    X = lambda v: x0 + (v - 2) * sc
    base = 100
    f.line(X(2) - 6, base, X(15) + 8, base, col='ink', w=1.4, arrow=True)
    for v in range(2, 16):
        f.line(X(v), base - 3, X(v), base + 3, col='ink', w=1)
        f.text(X(v), base + 14, str(v), size=9.5, col='grey')
    from collections import Counter
    for v, k in Counter(DATA).items():
        for j in range(k):
            f.circ(X(v), base - 9 - j * 15, 6.2, fill='mblue', stroke='navy', sw=1.3)
    mean = sum(DATA) / len(DATA)
    f.line(X(4), 34, X(4), base, col='blue', w=1.8, dash='4 3')
    f.line(X(5), 34, X(5), base, col='green', w=1.8, dash='4 3')
    f.line(X(mean), 34, X(mean), base, col='purple', w=1.8, dash='4 3')
    f.label(X(4) - 3, 28, 'moda 4', size=10, col='blue', anchor='end', bold=True)
    f.label(X(5), 14, 'mediana 5', size=10, col='green', bold=True)
    f.label(X(mean) + 3, 28, 'média ≈ 6,3', size=10, col='purple', anchor='start', bold=True)
    f.poly([(X(mean), base + 19), (X(mean) - 7, base + 31), (X(mean) + 7, base + 31)], fill='purple')
    f.text(X(mean), base + 44, 'ponto de equilíbrio (média)', size=9.5, col='purple')
    f.text(X(15) + 6, 56, 'dados: 3, 4, 4, 5, 6, 8, 14', size=9.5, col='navy', anchor='end')
    f.text(X(15) + 6, 69, '(soma 44, n = 7)', size=9.5, col='grey', anchor='end')
    return f.svg()


def fig_charts():
    f = Fig(342, 112)
    W = 82
    def panel(i, title, sub):
        x = i * (W + 4)
        f.rect(x, 0, W, 112, fill='white', stroke='mblue', sw=1, rx=5)
        f.text(x + W / 2, 14, title, size=9.8, col='navy', bold=True)
        f.text(x + W / 2, 105, sub, size=8.6, col='grey')
        return x
    x = panel(0, 'BARRAS', 'categorias')
    for k, h in enumerate((30, 50, 38, 62)):
        f.rect(x + 10 + k * 17, 88 - h, 12, h, fill='mblue', stroke='navy', sw=1)
    f.line(x + 8, 88, x + W - 6, 88, col='ink', w=1.2)
    x = panel(1, 'SETORES', '25% = 90°')
    cx, cy, r = x + W / 2, 56, 28
    f.sector(cx, cy, r, 0, 90, fill='lpurple', stroke='navy'); f.sector(cx, cy, r, 90, 360, fill='lblue', stroke='navy')
    f.text(cx + 11, cy - 8, '25%', size=9, col='purple', bold=True); f.text(cx - 6, cy + 10, '75%', size=9, col='navy', bold=True)
    x = panel(2, 'LINHAS', 'evolução no tempo')
    pts = [(x + 10, 80), (x + 26, 62), (x + 42, 70), (x + 58, 44), (x + 74, 34)]
    f.poly(pts, stroke='green', sw=2.2, close=False)
    for px, py in pts:
        f.dot(px, py, 2.8, 'green')
    f.line(x + 8, 88, x + W - 6, 88, col='ink', w=1.2)
    x = panel(3, 'HISTOGRAMA', 'frequência/classe')
    for k, h in enumerate((14, 34, 56, 40, 20)):
        f.rect(x + 8 + k * 13.2, 88 - h, 13.2, h, fill='lgreen', stroke='green', sw=1)
    f.line(x + 6, 88, x + W - 6, 88, col='ink', w=1.2)
    return f.svg()


def fig_disp():
    f = Fig(342, 100)
    def panel(x, heights, title, col):
        f.text(x + 80, 12, title, size=10, col=col, bold=True)
        for k, h in enumerate(heights):
            f.rect(x + 8 + k * 16, 80 - h * 5.2, 14, h * 5.2, fill='lblue', stroke='navy', sw=1)
        f.line(x + 4, 80, x + 156, 80, col='ink', w=1.2)
        f.line(x + 8 + 4.5 * 16 - 1, 18, x + 8 + 4.5 * 16 - 1, 80, col='purple', w=1.6, dash='4 3')
        f.text(x + 8 + 4.5 * 16, 94, 'média (igual nos dois)', size=8.6, col='purple')
    panel(0, [0, 1, 3, 7, 9, 7, 3, 1, 0], 'σ pequeno: dados regulares', 'green')
    panel(176, [4, 5, 5, 6, 6, 6, 5, 5, 4], 'σ grande: dados espalhados', 'blue')
    return f.svg()


def fig_venn():
    f = Fig(200, 118)
    f.circ(76, 56, 38, fill='lblue', stroke='blue', sw=1.8, op=.9)
    f.circ(124, 56, 38, fill='lorange', stroke='orange', sw=1.8, op=.55)
    # interseção
    f.path('M100,24 A38,38 0 0 1 100,88 A38,38 0 0 1 100,24 Z', fill='lgreen', stroke='green', sw=1.6)
    f.text(56, 60, '*A*', size=14, col='navy', bold=True); f.text(146, 60, '*B*', size=14, col='navy', bold=True)
    f.text(100, 60, '*A*∩*B*', size=10, col='green', bold=True)
    f.text(100, 112, '*P*(*A*∪*B*) = *P*(*A*) + *P*(*B*) − *P*(*A*∩*B*)', size=10, col='navy', bold=True)
    return f.svg()


def fig_tree():
    f = Fig(340, 190)
    f.text(6, 12, '2 sorteados (4 H e 6 M), sem reposição', size=9.6, col='navy', bold=True, anchor='start')
    root = (20, 100)
    nodes = {'H': (130, 56), 'M': (130, 144)}
    leaves = {'HH': (250, 26), 'HM': (250, 66), 'MH': (250, 126), 'MM': (250, 166)}
    f.circ(*root, 5, fill='navy')
    probs1 = {'H': '4/10', 'M': '6/10'}
    for k, (x, y) in nodes.items():
        f.line(root[0] + 4, root[1], x - 6, y, col='mgrey', w=1.6)
        f.pill((root[0] + x) / 2 + (-4 if k == 'H' else -4), (root[1] + y) / 2 + (-6 if k == 'H' else 6), probs1[k], fill='lblue', col='navy', size=9.5)
        f.circ(x, y, 12, fill='lpurple' if k == 'H' else 'lgreen', stroke='purple' if k == 'H' else 'green', sw=1.6)
        f.text(x, y + 4, k, size=11, col='navy', bold=True)
    probs2 = {'HH': '3/9', 'HM': '6/9', 'MH': '4/9', 'MM': '5/9'}
    prod = {'HH': '12/90', 'HM': '24/90', 'MH': '24/90', 'MM': '30/90'}
    for k, (x, y) in leaves.items():
        px, py = nodes[k[0]]
        f.line(px + 12, py, x - 12, y, col='mgrey', w=1.6)
        f.pill((px + x) / 2 + 6, (py + y) / 2 + (-5 if y < py else 5), probs2[k], fill='lblue', col='navy', size=9.2)
        diff = k in ('HM', 'MH')
        f.circ(x, y, 12, fill='lgreen' if diff else 'white', stroke='green' if diff else 'mgrey', sw=1.8 if diff else 1.2)
        f.text(x, y + 4, k[1], size=11, col='navy', bold=True)
        f.text(x + 20, y + 4, prod[k], size=10, col='green' if diff else 'grey', anchor='start', bold=diff)
    f.text(300, 100, 'soma = 90/90', size=9, col='grey')
    f.text(300, 112, '(=1)', size=9, col='grey')
    return f.svg()


def fig_comb():
    f = Fig(342, 124)
    f.rect(96, 2, 150, 24, fill='lblue', stroke='blue', sw=1.4, rx=6)
    f.text(171, 18, 'Escolher/organizar p de n elementos', size=10.5, col='navy', bold=True)
    f.line(171, 26, 171, 40, col='navy', w=1.6, arrow=True)
    f.poly([(171, 40), (232, 60), (171, 80), (110, 60)], fill='lpurple', stroke='purple', sw=1.6)
    f.text(171, 64, 'A ordem importa?', size=10.5, col='purple', bold=True)
    f.line(110, 60, 62, 60, col='navy', w=1.6, arrow=True); f.text(86, 54, 'SIM', size=10, col='green', bold=True)
    f.line(232, 60, 280, 60, col='navy', w=1.6, arrow=True); f.text(256, 54, 'NÃO', size=10, col='orange', bold=True)
    f.rect(2, 74, 130, 48, fill='lgreen', stroke='green', sw=1.4, rx=6)
    f.text(67, 90, 'ARRANJO · fila, pódio', size=9.5, col='green', bold=True)
    f.text(67, 108, '*A*(*n*,*p*) = *n*! / (*n*−*p*)!', size=11, col='navy')
    f.rect(210, 74, 130, 48, fill='lgreen', stroke='green', sw=1.4, rx=6)
    f.text(275, 90, 'COMBINAÇÃO · comissão', size=9.5, col='green', bold=True)
    f.text(275, 108, '*C*(*n*,*p*) = *n*! / [*p*!(*n*−*p*)!]', size=10.5, col='navy')
    f.line(62, 60, 62, 74, col='navy', w=1.6, arrow=True); f.line(280, 60, 275, 74, col='navy', w=1.6, arrow=True)
    return f.svg()


def p_estat():
    c5 = card('Média, mediana e moda', 5, 'A', cols(
        stack(
            formula((r'\bar{x}=\dfrac{\sum x_i}{n}', 'média aritmética'),
                    (r'\bar{x}_p=\dfrac{\sum x_i\,f_i}{\sum f_i}', 'ponderada (f = peso ou frequência)'), label='MÉDIA'),
            inl('<b class="g">Mediana:</b> valor central dos dados <u>ordenados</u>. n ímpar → termo da posição \\(\\tfrac{n+1}{2}\\); '
                'n par → média dos termos nas posições \\(\\tfrac{n}{2}\\) e \\(\\tfrac{n}{2}+1\\).',
                '<b class="g">Moda:</b> o <u>valor</u> que mais se repete (pode não existir ou haver mais de uma).',
                r'<b class="g">Desvio padrão:</b> \(\sigma=\sqrt{\dfrac{\sum(x_i-\bar{x})^2}{n}}\) — quanto menor, mais <u>regular</u> o conjunto.',
                label='MEDIANA · MODA · DISPERSÃO'),
            gap='1.4mm'),
        stack(fig(fig_dots(), 'O 14 (valor extremo) puxa a média para a direita; a mediana quase não se move.'),
              mem('<b>Média = ponto de equilíbrio</b> (gangorra) · <b>mediana = divide os dados ao meio</b> · <b>moda = “pico”</b>.'), gap='1.4mm'),
        ratio='1.02fr 1fr', gap='3.5mm', align='start') +
        cols(when('“<b>valor médio</b>”, “o que se esperar”, “o valor que divide…”, “mais frequente”, regularidade/consistência de resultados.'),
             err('Mediana <u>sem ordenar</u>; confundir <b>moda</b> (o valor) com sua <b>frequência</b>; ponderada: dividir por n em vez de por \\(\\sum f_i\\). '
                 'Somar uma constante a todos os dados soma a mesma constante à média.'),
             ratio='1fr 1.25fr', gap='3mm'))

    disp = cols(fig(fig_disp(), 'Mesma média, dispersões diferentes: o desvio padrão mede o espalhamento.'),
                stack(mini('Ponderada:', 'notas 6 (peso 2) e 9 (peso 3).', r'\(\tfrac{6\cdot2+9\cdot3}{2+3}=\tfrac{39}{5}\)', '= 7,8.'),
                      mini('Mediana (n par):', 'dados 2, 5, 7, 9.', r'média dos centrais: \(\tfrac{5+7}{2}\)', '= 6.'), gap='1.6mm'),
                ratio='1.5fr 1fr', gap='3mm', align='center')
    gr = card('Interpretação de gráficos e tabelas', None, 'A', cols(
        stack(fig(fig_charts()), gap='1mm'),
        stack(
            '<ul class="tight small" style="font-size:7.9pt;color:var(--ink)">'
            '<li><b>Leia o eixo:</b> título, unidade, escala. Eixo que não começa em zero <u>exagera</u> diferenças.</li>'
            '<li><b>Absoluto × relativo:</b> “subiu 30 mil” ≠ “subiu 30%”. Para comparar crescimento, use \\(\\tfrac{\\text{variação}}{\\text{inicial}}\\).</li>'
            '<li><b>Setores:</b> 360° = 100% → 1% = 3,6°. <b>Tabela de frequência:</b> \\(f_r=\\tfrac{f}{N}\\); frequência acumulada localiza a mediana.</li>'
            '<li><b>Histograma:</b> classes contínuas; a moda está na classe de maior barra.</li></ul>',
            gap='1mm'),
        ratio='1.12fr 1fr', gap='3mm', align='center'))

    e4 = ex(4, 'Tabela de frequências: média, mediana, moda e a nota que falta',
            'As notas de 20 alunos em um simulado foram: nota 4 (3 alunos), 6 (6 alunos), 7 (5 alunos), 9 (4 alunos) e 10 (2 alunos). '
            'Determine média, mediana e moda. Em seguida, calcule a nota que um 21º aluno precisaria tirar para que a média da turma passasse a ser exatamente 7,0.',
            '<b>Média ponderada</b> (as frequências são os pesos), <b>mediana</b> (posições centrais da lista ordenada) e <b>moda</b> (maior frequência).',
            r'\(\Sigma=4\cdot3+6\cdot6+7\cdot5+9\cdot4+10\cdot2=12+36+35+36+20=139\ \Rightarrow\ \bar{x}=\tfrac{139}{20}=6{,}95\)'
            r'<br><b>Mediana:</b> n = 20 → média das posições 10ª e 11ª. Acumulado: 3 (nota 4), 9 (até a nota 6), 14 (até a nota 7) → 10ª e 11ª são 7 → mediana 7.'
            r'<br><b>Moda:</b> a maior frequência é 6 alunos → nota 6.'
            r'<br><b>21º aluno:</b> \(\dfrac{139+x}{21}=7\ \Rightarrow\ 139+x=147\ \Rightarrow\ x=8\).',
            r'Média <b>6,95</b> · mediana <b>7</b> · moda <b>6</b> · o 21º aluno precisa tirar <b>8</b>.',
            shortcut=r'Para a média passar de 6,95 para 7,00 com 21 alunos, a soma total deve ser \(7\cdot21=147\) → faltam \(147-139=8\) pontos ✔.')

    r = rec(('Dados 2, 3, 3, 8, 9: média, mediana, moda?', '5 · 3 · 3'),
            ('Média de 4 provas é 7. Quanto somou? Se a 5ª for 9, nova média?', '28 · 37/5 = 7,4'),
            ('Setores: 15% corresponde a qual ângulo?', '15 × 3,6 = 54°'))
    return c5 + disp + gr + e4 + r


def p_prob():
    c1 = card('Probabilidade básica', None, 'A', cols(
        stack(
            formula((r'P(A)=\dfrac{n(A)}{n(\Omega)}=\dfrac{\text{casos favoráveis}}{\text{casos possíveis}}', '0 ≤ P ≤ 1 (eventos equiprováveis)'),
                    (r'P(\text{não }A)=1-P(A)', 'complementar'),
                    (r'P(A\cap B)=P(A)\cdot P(B)', 'independentes: “e”, em sequência'),
                    (r'P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}', 'condicional: já sabendo B'), label='PROBABILIDADE'),
            gap='1.2mm'),
        stack(fig(fig_venn()),
              when('<b>“ou”</b> → soma (subtraindo a interseção). <b>“e”</b> → multiplica. <b>“pelo menos um”</b> → \\(1-P(\\text{nenhum})\\). '
                   'Sem reposição: a 2ª probabilidade <u>muda</u>.'), gap='1.4mm'),
        ratio='1.2fr 1fr', gap='3.5mm', align='center') +
        err('Somar probabilidades de etapas <u>em sequência</u> (o correto é multiplicar) e esquecer de <b>reduzir o espaço amostral</b> quando não há reposição. '
            'Probabilidade nunca passa de 1: se deu 1,2 ou 120%, algo está errado.'))

    c2 = card('Princípio multiplicativo e análise combinatória', None, 'B', cols(
        stack(
            formula((r'n_1\cdot n_2\cdots n_k', 'etapas independentes: multiplique as opções'),
                    (r'P_n=n!\qquad P_n^{a,b}=\dfrac{n!}{a!\,b!}', 'permutação (com repetição)'),
                    (r'A_{n,p}=\dfrac{n!}{(n-p)!}\quad C_{n,p}=\dfrac{n!}{p!\,(n-p)!}', 'arranjo e combinação'),
                    label='CONTAGEM'),
            mem('<b>C(n,p) = A(n,p) ÷ p!</b>: a combinação desconta as p! ordens de um mesmo grupo. Propriedade útil: \\(C_{n,p}=C_{n,n-p}\\).'),
            gap='1.4mm'),
        fig(fig_comb(), 'Mesmo conjunto, ordem diferente: conta de novo (arranjo) ou conta uma vez (combinação)?'),
        ratio='1.05fr 1fr', gap='3.5mm', align='center'))

    e5 = ex(5, 'Probabilidade sem reposição: dois jeitos de resolver',
            'Uma comissão de 2 pessoas é sorteada em um grupo de 4 homens e 6 mulheres. Qual a probabilidade de a comissão ter exatamente um homem e uma mulher?',
            '<b>Probabilidade</b> de eventos em sequência <u>sem reposição</u> (árvore) ou <b>combinação</b> (grupo, a ordem não importa). Os dois caminhos devem coincidir.',
            r'<b>Árvore:</b> \(P=\underbrace{\tfrac{4}{10}\cdot\tfrac{6}{9}}_{HM}+\underbrace{\tfrac{6}{10}\cdot\tfrac{4}{9}}_{MH}=\tfrac{24}{90}+\tfrac{24}{90}=\tfrac{48}{90}=\tfrac{8}{15}\)'
            r'<br><b>Combinação:</b> \(P=\dfrac{C_{4,1}\cdot C_{6,1}}{C_{10,2}}=\dfrac{4\cdot6}{45}=\dfrac{24}{45}=\dfrac{8}{15}\)',
            r'\(P=\dfrac{8}{15}\approx 53{,}3\%\).',
            shortcut=r'Confira a árvore: \(\tfrac{12}{90}+\tfrac{24}{90}+\tfrac{24}{90}+\tfrac{30}{90}=1\) ✔ (HH, HM, MH, MM).')

    tr = fig(fig_tree(), 'Cada ramo multiplica; ramos de um mesmo caminho “e”, caminhos diferentes “ou” (somam).')
    mn = cols(
        mini('Moeda 5 vezes:', 'exatamente 2 caras.', r'\(C_{5,2}\cdot(\tfrac{1}{2})^5=\tfrac{10}{32}\)', '= 5/16.'),
        mini('Anagramas de ENEM:', 'letras E, N, E, M (o E repete 2 vezes).', r'\(P_4^{2}=\tfrac{4!}{2!}=\tfrac{24}{2}\)', '= 12 anagramas.'), gap='3mm')
    mn2 = cols(
        mini('Condicional:', '60% usam bicicleta; 20% usam bicicleta e moram longe.', r'\(P(\text{longe}\mid\text{bike})=\tfrac{0{,}20}{0{,}60}\)', '= 1/3.'),
        mini('Valor esperado:', 'aposta de R$ 2 paga R$ 10 se sair 6 (prob. 1/6).', r'\(E=10\cdot\tfrac{1}{6}-2\)', '≈ −R$ 0,33 por jogo.'), gap='3mm')
    r = rec(('Senha de 4 dígitos distintos (0–9): quantas?', '10·9·8·7 = 5 040 (arranjo)'),
            ('Escolher 3 representantes entre 8 colegas: quantos grupos?', 'C(8,3) = 56'),
            ('Dado: P(sair número maior que 4)?', '2/6 = 1/3'))
    return c1 + c2 + cols(e5, tr, ratio='1.45fr 1fr', gap='3mm', align='start') + mn + mn2 + r


def pages():
    return [p_estat(), p_prob()]
