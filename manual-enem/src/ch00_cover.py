"""Capa, sumário (mapa dos 40 tópicos) e guia de revisão."""
import re
from lib import *
from svg import Fig, Plot, polygon_pts

LABEL = 'CAPA'

TOPICS = [
    (1, 'Escala', 'A'), (2, 'Vazão', 'A'), (3, 'Juros simples (e compostos)', 'A'), (4, 'Lucro', 'B'),
    (5, 'Média, mediana e moda', 'A'), (6, 'Produtos notáveis', 'B'), (7, 'Discriminante', 'A'), (8, 'Fórmula de Bhaskara', 'A'),
    (9, 'Função do 1º grau: lei de formação', 'A'), (10, 'Termo geral da PA', 'A'), (11, 'Soma dos termos da PA', 'B'),
    (12, 'Termo geral da PG', 'A'), (13, 'Soma da PG finita', 'B'), (14, 'Soma da PG infinita', 'C'),
    (15, 'Função quadrática: lei de formação', 'A'), (16, 'Forma fatorada da quadrática', 'B'), (17, 'Soma, produto das raízes e vértice', 'A'),
    (18, 'Soma dos ângulos internos', 'B'), (19, 'Ângulo interno (regular)', 'B'), (20, 'Ângulo externo (regular)', 'B'),
    (21, 'Ângulo central (regular)', 'C'), (22, 'Diagonais de um polígono', 'B'), (23, 'Diagonais pelo centro', 'C'),
    (24, 'Teorema de Pitágoras', 'A'), (25, 'Círculo e circunferência', 'A'), (26, 'Áreas das figuras planas', 'A'),
    (27, 'Coroa, setor e segmento circular', 'B'), (28, 'Hexágono, diagonal do quadrado, equilátero', 'B'),
    (29, 'Razões trigonométricas', 'A'), (30, 'Relações métricas do triângulo retângulo', 'B'), (31, 'Ângulos notáveis', 'A'),
    (32, 'Leis dos senos e cossenos; sen²+cos²=1', 'B'), (33, 'Prismas, cubo e paralelepípedo', 'A'), (34, 'Cilindro e cone', 'A'),
    (35, 'Raio, altura e geratriz do cone', 'C'), (36, 'Esfera', 'B'), (37, 'Troncos (cone e pirâmide)', 'C'),
    (38, 'Distância, ponto médio e circunferência', 'B'), (39, 'Potências, radiciação e logaritmos', 'B'),
    (40, 'Percentuais, unidades, notação científica', 'A'),
]
COMPL = ('Regra de três · MMC e MDC · juros compostos · probabilidade · contagem · gráficos e tabelas · equações e sistemas · função exponencial · semelhança · retas')


def _expand(key):
    out = set()
    for part in re.split(r'\s*·\s*', key):
        m = re.match(r'(\d+)[–-](\d+)$', part.strip())
        if m:
            out |= set(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.strip().isdigit():
            out.add(int(part))
    return out


def art():
    f = Fig(150, 80)
    p = Plot(150, 80, -3, 3, -1, 3.2, l=6, r=6, t=4, b=4)
    p.line(p.X(-3), p.Y(0), p.X(3), p.Y(0), col='#6F93C9', w=1)
    p.line(p.X(0), p.Y(-1), p.X(0), p.Y(3.2), col='#6F93C9', w=1)
    p.curve(lambda x: 0.35 * x * x - 0.9, -2.9, 2.9, col='#8FD0AE', w=2.4, ylim=(-1, 3.2))
    p.curve(lambda x: 1.0 * (1 - (x / 1.5) ** 2) ** .5 + 1.2, -1.5, 1.5, col='#B9D3F0', w=0, ylim=(-5, 9)) if False else None
    p.circ(p.X(0.9), p.Y(1.7), 20, stroke='#B9D3F0', sw=1.6, fill='none')
    p.dot(p.X(0.9), p.Y(1.7), 2.4, '#B9D3F0')
    p.line(p.X(0.9), p.Y(1.7), p.X(0.9) + 14.14, p.Y(1.7) - 14.14, col='#B9D3F0', w=1.2)
    pts = polygon_pts(6, p.X(-1.6), p.Y(2.0), 15, rot=0)
    p.poly(pts, stroke='#B9D3F0', sw=1.6, fill='none')
    return p.svg()


def body(tp, total):
    pages_of = {}
    prio_of = {}
    for key, pg in tp:
        for n in _expand(key):
            pages_of.setdefault(n, set()).add(pg)
    banner = (f'<div class="cvban"><div class="k">REVISÃO ESTRATÉGICA · RETA FINAL</div>'
              f'<h1>MANUAL ESTRATÉGICO<br>DE MATEMÁTICA <span>· ENEM 2026</span></h1>'
              f'<div class="sub">Os 40 tópicos que mais pesam na revisão: <b>o que saber, quando usar, como aplicar e como memorizar</b> — com figuras, '
              f'exemplos de nível ENEM e um guia para escolher a fórmula certa. {total} páginas, do essencial ao complementar.</div>'
              f'{art()}</div>')
    legend = ('<div class="cvbox"><h3>COMO LER AS CORES</h3><div class="lg">'
              '<span class="sw" style="background:var(--navy)"></span><span><b>Azul-marinho</b> · títulos e estrutura</span>'
              '<span class="sw" style="background:var(--blue)"></span><span><b>Azul</b> · explicação e “quando usar”</span>'
              '<span class="sw" style="background:var(--green)"></span><span><b>Verde</b> · fórmula essencial e resposta</span>'
              '<span class="sw" style="background:var(--orange)"></span><span><b>Laranja</b> · erro comum e atenção</span>'
              '<span class="sw" style="background:var(--purple)"></span><span><b>Roxo</b> · memorização e teste rápido</span></div></div>')
    method = ('<div class="cvbox"><h3>OS 4 PASSOS DE CADA CONTEÚDO</h3>'
              '<div>① <b>O que saber</b> — fórmula e variáveis.<br>② <b>Quando usar</b> — pistas do enunciado.<br>'
              '③ <b>Como aplicar</b> — exemplos resolvidos (EXEMPLO 1–13) e “aplique”.<br>④ <b>Como memorizar</b> — figuras e associações corretas.</div>'
              '<h3 style="margin-top:1.4mm">PRIORIDADE</h3>'
              '<div><span class="chip" style="background:var(--navy);color:#fff">A · ESSENCIAL</span> mais espaço · '
              '<span class="chip" style="background:var(--mblue);color:var(--navy)">B · IMPORTANTE</span> · '
              '<span class="chip" style="border:1px solid var(--mpurple);color:var(--muted)">C · COMPLEMENTAR</span></div></div>')
    rows = []
    for n, name, pr in TOPICS:
        pgs = sorted(pages_of.get(n, []))
        links = ' · '.join(f'<a href="#p{p}">{p}</a>' for p in pgs) if pgs else '—'
        rows.append(f'<div class="cvr"><span class="no">{n}</span><span>{name}</span><span class="ch {pr}">{pr}</span><span class="pg">p. {links}</span></div>')
    half = 20
    left, right = ''.join(rows[:half]), ''.join(rows[half:])
    mp = (f'<div class="cvmap"><div class="cvh">MAPA DOS 40 TÓPICOS DA IMAGEM (nº · tópico · prioridade · página)</div>'
          f'<div>{left}</div><div>{right}</div></div>')
    comp = (f'<div class="cvbox" style="margin-top:0"><h3>ALÉM DOS 40 (agrupados nos capítulos)</h3>{COMPL}.</div>')
    plano = ('<div class="cvbox" style="border-color:var(--mpurple);background:var(--lpurple)"><h3 style="color:var(--purple)">PLANO DE REVISÃO SUGERIDO</h3>'
             '<div><b>1ª volta (A):</b> todos os cartões “ESSENCIAL” + exemplos. <b>2ª volta (B/C):</b> leia só fórmula + “quando usar”. '
             '<b>Toda semana:</b> cubra as respostas dos <i>testes rápidos</i> e releia o <b>Formulário</b> e o <b>guia de decisão</b> (págs. '
             f'{total - 1}–{total}). Treine com provas anteriores — o manual ensina a <u>escolher</u> a ferramenta, a prática dá velocidade.</div></div>')
    return banner + cols(legend, method, gap='3mm') + mp + comp + plano
