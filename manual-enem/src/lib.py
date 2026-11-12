"""Componentes editoriais reutilizáveis (cartões, caixas, exemplos, colunas).

Convenção de cores (significado fixo em todo o manual):
  navy   = títulos e identidade        blue   = explicação / quando usar
  green  = fórmula essencial / resposta orange = erro comum / atenção
  purple = memorização / relação chave
Matemática inline: \\( ... \\)   |   em destaque: \\[ ... \\]   (KaTeX; "$" fica livre para "R$")
"""

PRIO = {'A': 'ESSENCIAL', 'B': 'IMPORTANTE', 'C': 'COMPLEMENTAR'}


def card(title, num=None, prio='A', body='', cls='', style=''):
    """Cartão de tópico. num = nº do tópico na lista de 40 (ex.: 9 ou '18–23'); None = conteúdo complementar."""
    topics = ''
    if num is None:
        n = '<span class="tn plus">+</span>'
    else:
        n = f'<span class="tn">{num}</span>'
        topics = f' data-topics="{num}"'
    return (f'<div class="card {cls}" style="{style}"{topics}>'
            f'<div class="th">{n}<span class="tt">{title}</span>'
            f'<span class="pr p{prio}">{prio} · {PRIO[prio]}</span></div>'
            f'<div class="cb">{body}</div></div>')


def formula(*lines, label=None, cls=''):
    """Caixa verde de fórmulas. Cada linha: tex puro (display) ou (tex, nota)."""
    rows = []
    for ln in lines:
        if isinstance(ln, tuple):
            tex, note = ln
            rows.append(f'<div class="frow"><span class="ftex">\\[{tex}\\]</span><span class="fnote">{note}</span></div>')
        else:
            rows.append(f'<div class="frow"><span class="ftex">\\[{ln}\\]</span></div>')
    lab = f'<div class="lab lg">{label}</div>' if label else ''
    return f'<div class="formula {cls}">{lab}{"".join(rows)}</div>'


def inl(*lines, label=None):
    """Fórmulas inline compactas (linhas) em caixa verde."""
    lab = f'<div class="lab lg">{label}</div>' if label else ''
    rows = ''.join(f'<div class="irow">{l}</div>' for l in lines)
    return f'<div class="formula inl">{lab}{rows}</div>'


def vars_(text):
    return f'<div class="vars">{text}</div>'


def when(text, label='QUANDO USAR'):
    return f'<div class="box when"><span class="lab">{label}</span>{text}</div>'


def err(text, label='ERRO COMUM'):
    return f'<div class="box err"><span class="lab">{label}</span>{text}</div>'


def mem(text, label='MEMORIZE'):
    return f'<div class="box mem"><span class="lab">{label}</span>{text}</div>'


def note(text, label='OBSERVE'):
    return f'<div class="box nt"><span class="lab">{label}</span>{text}</div>'


def fig(svg, cap=None, cls=''):
    cp = f'<div class="cap">{cap}</div>' if cap else ''
    return f'<div class="figbox {cls}">{svg}{cp}</div>'


def cols(*items, ratio=None, gap=None, cls='', align='start'):
    n = len(items)
    tpl = ratio if ratio else ' '.join(['1fr'] * n)
    g = f'gap:{gap};' if gap else ''
    return f'<div class="cols {cls}" style="grid-template-columns:{tpl};{g}align-items:{align}">{"".join(items)}</div>'


def stack(*items, gap='2mm', cls=''):
    return f'<div class="stack {cls}" style="gap:{gap}">{"".join(items)}</div>'


def ex(num, title, problem, ident, steps, answer, shortcut=None, size=''):
    """Exemplo resolvido no formato SITUAÇÃO · IDENTIFICAÇÃO · RESOLUÇÃO · ATALHO · RESPOSTA."""
    sc = f'<div class="exrow sc"><span class="exl">ATALHO</span><div>{shortcut}</div></div>' if shortcut else ''
    return (f'<div class="example {size}"><div class="exh"><span class="exn">EXEMPLO {num}</span>'
            f'<span class="ext">{title}</span></div>'
            f'<div class="exrow"><span class="exl">SITUAÇÃO</span><div>{problem}</div></div>'
            f'<div class="exrow id"><span class="exl">IDENTIFICAÇÃO</span><div>{ident}</div></div>'
            f'<div class="exrow rs"><span class="exl">RESOLUÇÃO</span><div>{steps}</div></div>'
            f'{sc}'
            f'<div class="exans"><span class="exl">RESPOSTA</span><div>{answer}</div></div></div>')


def mini(title, problem, steps, answer):
    """Mini-aplicação (1–3 linhas) – usada quando um exemplo completo não se justifica."""
    return (f'<div class="miniex"><span class="mxl">APLIQUE</span><div><b>{title}</b> {problem} '
            f'<span class="mxs">{steps}</span> <span class="mxa">{answer}</span></div></div>')


def rec(*qa, title='TESTE RÁPIDO'):
    """Recuperação ativa: perguntas curtas com resposta em cinza-roxo (cubra e tente antes de ler)."""
    rows = ''.join(f'<div class="qrow"><span class="q">{q}</span><span class="a">→ {a}</span></div>' for q, a in qa)
    return f'<div class="box rec"><span class="lab">{title} · cubra a resposta</span>{rows}</div>'


def tbl(head, rows, cls='', widths=None):
    ws = ''
    if widths:
        ws = '<colgroup>' + ''.join(f'<col style="width:{w}">' for w in widths) + '</colgroup>'
    h = ''.join(f'<th>{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in rows)
    return f'<table class="tb {cls}">{ws}<thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'


def chapter_band(num, title, subtitle=''):
    sub = f'<span class="cbs">{subtitle}</span>' if subtitle else ''
    return (f'<div class="chband"><span class="cbn">CAPÍTULO {num}</span>'
            f'<span class="cbt">{title}</span>{sub}</div>')


def page(n, chapter, body, extra_cls=''):
    return (f'<section class="page {extra_cls}" id="p{n}" data-page="{n}">'
            f'<header class="ph"><span class="phc">{chapter}</span>'
            f'<span class="phm">MANUAL ESTRATÉGICO DE MATEMÁTICA · ENEM 2026</span></header>'
            f'<div class="body">{body}</div>'
            f'<footer class="pf"><span class="pfl">revise com método · erre agora, acerte na prova</span>'
            f'<span class="pfn">{n}</span></footer></section>')
