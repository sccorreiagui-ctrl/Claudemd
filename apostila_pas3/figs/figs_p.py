"""Figuras da Parte II — Polinômios (vetoriais)."""
import math
from fractions import Fraction
from svgkit import Fig, Plane, PAL

SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def fr(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def sgn(s):
    return s.replace('-', '−')


# ---------------------------------------------------------------- p21
def fig_poly_anat():
    f = Fig(548, 196)
    xs = [78, 168, 258, 348, 424, 490]
    f.text(34, 62, 'P(x) =', 21, 'ink', anchor='middle')
    terms = [('«blue:3»x^{4}', 0), ('−«blue:2»x^{3}', 1), ('+«blue:0»x^{2}', 2), ('+«blue:5»x', 3), ('−«blue:7»', 4)]
    pos = [(116, 'a'), (200, 'b'), (284, 'c'), (356, 'd'), (428, 'e')]
    f.text(116, 62, '«blue:3»x^{4}', 24, 'ink')
    f.text(200, 62, '− «blue:2»x^{3}', 24, 'ink')
    f.rect(238, 36, 86, 36, 'red_l', 'red', 1.2, rx=4, dash='4 3', op=0.7)
    f.text(281, 62, '+ «red:0»x^{2}', 24, 'ink')
    f.text(372, 62, '+ «blue:5»x', 24, 'ink')
    f.text(446, 62, '− «blue:7»', 24, 'ink')
    # setas de baixo
    f.arrow(116, 118, 104, 78, 'blue', 1.5, 6)
    f.text(116, 130, '~coeficiente dominante', 8.8, 'blue', weight=800)
    f.text(116, 142, '~a₄ = 3 (≠ 0)', 8.8, 'blue')
    f.arrow(200, 168, 205, 78, 'blue', 1.2, 6)
    f.text(200, 180, '~coeficientes: 3, −2, 0, 5, −7', 8.8, 'blue', weight=700)
    f.arrow(281, 118, 281, 80, 'red', 1.5, 6)
    f.text(281, 130, '~termo ausente', 8.8, 'red', weight=800)
    f.text(281, 142, '~(coeficiente 0)', 8.8, 'red')
    f.arrow(446, 118, 446, 80, 'blue', 1.5, 6)
    f.text(446, 130, '~termo independente', 8.8, 'blue', weight=800)
    f.text(446, 142, '~a₀ = −7 = P(0)', 8.8, 'blue')
    # setas de cima
    f.arrow(133, 22, 128, 42, 'orange', 1.5, 6)
    f.text(133, 14, '~grau = 4 (maior expoente com coef. ≠ 0)', 8.8, 'orange', weight=800)
    f.arrow(380, 22, 380, 44, 'gray', 1.4, 6)
    f.text(380, 14, '~variável (incógnita) x', 8.8, 'gray', weight=700)
    return f


# ---------------------------------------------------------------- p22
def fig_slots():
    f = Fig(520, 108)
    coefs = [1, 0, -3, 2, 0, 4]
    exps = [5, 4, 3, 2, 1, 0]
    x0, w = 54, 70
    f.text(26, 56, 'P(x)', 12, 'ink', anchor='middle')
    f.text(26, 70, '~coef.', 8, 'gray')
    for i, (c, e) in enumerate(zip(coefs, exps)):
        x = x0 + i * w
        zero = c == 0
        f.rect(x, 28, w - 8, 36, 'red_l' if zero else 'blue_l', 'red' if zero else 'blue', 1.4, rx=4, dash='4 3' if zero else None)
        f.text(x + (w - 8) / 2, 54, str(c).replace('-', '−'), 19, 'red' if zero else 'blue', weight=700)
        f.text(x + (w - 8) / 2, 20, f'x^{{{e}}}', 12, 'gray')
    f.text(x0 + 2.5 * w - 4, 92, '~x⁵ − 3x³ + 2x² + 4  →  coeficientes 1, 0, −3, 2, 0, 4', 9.4, 'ink', weight=700)
    f.text(x0 + 2.5 * w - 4, 104, '~(zeros nos expoentes que não aparecem: x⁴ e x¹)', 8.4, 'red')
    return f


# ---------------------------------------------------------------- p23
def fig_eval():
    f = Fig(548, 118)
    def box(x, w, fill, stroke, lines, big=None):
        f.rect(x, 16, w, 62, fill, stroke, 1.4, rx=6)
        if big: f.text(x + w / 2, 42, big, 16, 'ink')
        for j, (t, c) in enumerate(lines): f.text(x + w / 2, (60 if big else 38) + j * 13, t, 9, c, weight=700 if j == 0 else None)
    box(6, 116, 'blue_l', 'blue', [('~ENTRADA', 'blue'), ('~valor a atribuir a x', 'gray')], 'x = 2')
    f.arrow(124, 47, 168, 47, 'ink', 2.0, 8)
    box(170, 210, 'gray_l', 'gray', [('~AVALIAÇÃO', 'gray'), ('~troque todo x por 2 e calcule', 'gray')], 'P(x) = x^3 − x^2 + 1')
    f.arrow(382, 47, 424, 47, 'ink', 2.0, 8)
    box(426, 116, 'green_l', 'green', [('~RESULTADO', 'green'), ('~P(2) = 8 − 4 + 1', 'gray')], 'P(2) = 5')
    f.rect(6, 88, 536, 26, 'orange_l', 'orange', 1.2, rx=5)
    f.text(274, 105, '~Se o resultado for ZERO, o valor de entrada é RAIZ:  P(a) = 0  ⟺  a é raiz de P', 9.6, 'ink', weight=700)
    return f


# ---------------------------------------------------------------- p26
def fig_expfac():
    f = Fig(548, 92)
    f.rect(6, 22, 190, 46, 'blue_l', 'blue', 1.4, rx=6)
    f.text(101, 52, '(x − 2)(x + 3)', 17, 'ink')
    f.text(101, 16, '~PRODUTO de fatores', 8.4, 'blue', weight=800)
    f.rect(352, 22, 190, 46, 'orange_l', 'orange', 1.4, rx=6)
    f.text(447, 52, 'x^2 + x − 6', 17, 'ink')
    f.text(447, 16, '~SOMA de termos', 8.4, 'orange', weight=800)
    f.arrow(204, 36, 344, 36, 'green', 2.0, 8)
    f.text(274, 30, '~expandir (distributiva)', 8.8, 'green', weight=800)
    f.arrow(344, 56, 204, 56, 'purple', 2.0, 8)
    f.text(274, 76, '~fatorar (evidência, agrupamento, notáveis, raízes)', 8.8, 'purple', weight=800)
    return f


# ---------------------------------------------------------------- p27 (divisão pela chave, gerada de dados)
def term(c, p, first=False):
    """string com sinal: c*x^p."""
    c = int(c) if Fraction(c).denominator == 1 else Fraction(c)
    ac = abs(c)
    body = ''
    cs = fr(ac) if Fraction(ac).denominator == 1 else '(' + fr(ac) + ')'
    if p == 0: body = fr(ac)
    else:
        body = ('' if ac == 1 else cs) + ('x' if p == 1 else f'x^{{{p}}}')
    if c < 0: return '−' + body
    return body if first else '+' + body


def long_division(P, D):
    """P, D listas de coeficientes (maior grau primeiro). Retorna passos [(q_c,q_p, produto_coefs(lista), resto_coefs)]."""
    P = [Fraction(x) for x in P]; D = [Fraction(x) for x in D]
    nP, nD = len(P) - 1, len(D) - 1
    cur = P[:]
    steps = []
    q = []
    for k in range(nP - nD + 1):
        c = cur[0] / D[0]
        p = len(cur) - 1 - nD
        prod = [c * d for d in D] + [Fraction(0)] * (len(cur) - len(D))
        new = [a - b for a, b in zip(cur, prod)][1:]
        steps.append((c, p, prod[:], new[:]))
        cur = new
        q.append((c, p))
    return steps


def division_panel(f, ox, oy, P, D, upto, caption, colw=29):
    """desenha um painel da divisão até o passo 'upto' (1-based)."""
    nP = len(P) - 1
    steps = long_division(P, D)
    # layout: colunas de nP..0
    xr = lambda p: ox + 8 + (nP - p + 1) * colw  # borda direita da coluna de potência p
    rh = 17
    # dividendo
    y = oy + 36
    for i, c in enumerate(P):
        p = nP - i
        f.text(xr(p), y, term(c, p, first=(i == 0)), 12, 'blue', anchor='end')
    xdiv = xr(0) + 8
    f.line(xdiv, y - 14, xdiv, y + 5, 'ink', 1.4)
    f.line(xdiv, y + 5, xdiv + 84, y + 5, 'ink', 1.4)
    # divisor
    nD = len(D) - 1
    dx = xdiv + 8
    s = ''
    for i, c in enumerate(D):
        s += term(c, nD - i, first=(i == 0))
    f.text(dx, y, s, 12, 'ink', anchor='start')
    # quociente
    qs = ''
    for k in range(upto):
        c, p, _, _ = steps[k]
        qs += term(c, p, first=(k == 0))
    f.text(dx, y + 22, qs, 12, 'green', anchor='start', weight=700)
    # linhas de passos
    yy = y + 20
    deg_cur = nP
    for k in range(upto):
        c, p, prod, new = steps[k]
        # produto (com sinal trocado) alinhado às colunas de deg_cur..
        inv = [-v for v in prod]
        top = deg_cur
        for j, v in enumerate(inv):
            if v == 0 and j >= len(D): continue
            pw = top - j
            if j < len(D):
                f.text(xr(pw), yy, term(v, pw, first=(j == 0)), 11.5, 'red', anchor='end')
        f.line(xr(top) - colw + 4, yy + 5, xr(top - len(D) + 1) + 3, yy + 5, 'gray', 1.0)
        yy += rh
        # novo resto
        newdeg = top - 1
        for j, v in enumerate(new):
            pw = newdeg - j
            f.text(xr(pw), yy, term(v, pw, first=(j == 0)), 11.5, 'ink' if k < upto - 1 or any(new) else 'green', anchor='end', weight=700 if k == upto - 1 else None)
        if k == upto - 1 and not any(new):
            f.text(xr(0), yy, '0', 11.5, 'green', anchor='end', weight=700)
        yy += rh
        deg_cur = newdeg
    # destaque da operação do último passo
    c, p, prod, new = steps[upto - 1]
    lead_p = len(P) - 1 - (upto - 1)
    lt = term(P[0] if upto == 1 else steps[upto - 2][3][0], lead_p, first=True)
    div_txt = f'{lt} ÷ {term(D[0], nD, first=True)} = {term(c, p, first=True)}'
    f.text(ox + 6, oy + 11, '~' + caption, 8.6, 'orange', anchor='start', weight=800)
    f.text(ox + 6, oy + 11 + 0, '', 8)
    return div_txt


def fig_chave():
    P, D = [1, -3, 5, -3], [1, -1]
    W, H = 736, 178
    f = Fig(W, H)
    w = 238
    caps = ['① divida só os termos de maior grau', '② repita com o novo resto', '③ pare: resto nulo (grau < gr D)']
    for k in range(3):
        ox = 2 + k * (w + 8)
        f.rect(ox, 2, w, H - 4, 'white', 'gray_m', 1.0, rx=5)
        div_txt = division_panel(f, ox, 4, P, D, k + 1, caps[k], colw=29)
        f.text(ox + w / 2, H - 9, '~' + 'x³ ÷ x = x²' if k == 0 else '~' + div_txt.replace('^{', '').replace('}', ''), 9, 'orange', weight=800) if False else None
        f.text(ox + w - 6, H - 8, '~vermelho: produto com SINAL TROCADO', 7.4, 'red', anchor='end')
    return f


def fig_chave2():
    """divisão por polinômio de grau 2, com resto não nulo: 6x^4 −3x^3 +3x^2 − x + 1 ÷ (2x^2 + x − 3)."""
    P, D = [6, -3, 3, -1, 1], [2, 1, -3]
    steps = long_division(P, D)
    W, H = 338, 200
    f = Fig(W, H)
    division_panel(f, 0, -14, P, D, 3, '', colw=39)
    f.text(6, 178, '~Q(x) = 3x² − 3x + 15/2', 9.4, 'green', anchor='start', weight=800)
    f.text(6, 192, '~R(x) = −(35/2)x + 47/2   (gr R = 1 < 2: pare)', 9.4, 'green', anchor='start', weight=800)
    return f


# ---------------------------------------------------------------- p29
def fig_remflow():
    f = Fig(330, 196)
    bs = [('1', '~Divisor', 'D(x) = x − a', 'ex.: x + 3  ou  2x − 4', 'blue_l', 'blue'),
          ('2', '~Iguale a zero', 'x − a = 0  ⇒  x = a', 'x + 3: x = −3;  2x − 4: x = 2', 'orange_l', 'orange'),
          ('3', '~Resto', 'R = P(a)', 'P(−3);  P(2)', 'green_l', 'green')]
    for i, (n, t, big, ex, fl, st) in enumerate(bs):
        y = 4 + i * 52
        f.rect(4, y, 322, 42, fl, st, 1.5, rx=6)
        f.circle(20, y + 21, 9, st, 'white', 1)
        f.text(20, y + 25, '~' + n, 10.5, 'white', weight=800)
        f.text(34, y + 25, t, 9.8, st, anchor='start', weight=800)
        f.text(214, y + 20, big, 14, 'ink')
        f.text(214, y + 35, '~' + ex, 8.6, 'gray')
        if i < 2: f.arrow(165, y + 43, 165, y + 52, 'ink', 2.0, 6)
    f.text(165, 170, '~Para ax + b (a ≠ 0): raiz −b/a e resto P(−b/a).', 8.8, 'red', weight=700)
    f.text(165, 183, '~Não confunda o sinal do binômio com a raiz.', 8.8, 'red', weight=700)
    return f


def fig_dalembert():
    f = Fig(400, 214)
    nodes = [(8, 22, 'RAIZ', 'P(a) = 0', 'purple_l', 'purple'), (212, 22, 'RESTO NULO', 'na divisão por x − a', 'orange_l', 'orange'),
             (212, 140, 'DIVISÍVEL', 'P é divisível por x − a', 'green_l', 'green'), (8, 140, 'FATOR', 'P(x) = (x − a)·Q(x)', 'blue_l', 'blue')]
    w, h = 180, 54
    for (x, y, t, s, fl, st) in nodes:
        f.rect(x, y, w, h, fl, st, 1.6, rx=7)
        f.text(x + w / 2, y + 22, '~' + t, 11, st, weight=800)
        f.text(x + w / 2, y + 40, s, 9.4, 'ink')
    f.arrow(190, 49, 210, 49, 'ink', 1.8, 7, both=True)
    f.arrow(302, 78, 302, 138, 'ink', 1.8, 7, both=True)
    f.arrow(210, 167, 190, 167, 'ink', 1.8, 7, both=True)
    f.arrow(98, 138, 98, 78, 'ink', 1.8, 7, both=True)
    f.text(200, 109, '~D\'ALEMBERT', 12, 'ink', weight=800)
    f.text(200, 122, '~(as quatro afirmações são equivalentes)', 7.6, 'gray')
    f.text(200, 10, '~Teorema do Resto: o resto é P(a), nulo ou não', 8.2, 'orange', weight=700)
    return f


# ---------------------------------------------------------------- p30 / p31 (Ruffini)
def ruffini_values(coefs, a):
    a = Fraction(a)
    b = []
    for i, c in enumerate(coefs):
        b.append(Fraction(c) if i == 0 else Fraction(c) + a * b[-1])
    prods = [None] + [a * b[i - 1] for i in range(1, len(coefs))]
    return b, prods


def ruffini_grid(f, ox, oy, coefs, a, stage, title=None, cw=54, rootw=48, show_label=False, qlabel=True):
    """stage: 0=montagem; 1=baixa; k>=2: passos de multiplica/soma; stage=len(coefs): completo."""
    n = len(coefs)
    b, prods = ruffini_values(coefs, a)
    af = Fraction(a)
    y1, y2, y3 = oy + 40, oy + 66, oy + 96
    if title: f.text(ox, oy + 12, '~' + title, 9.6, 'ink', anchor='start', weight=800)
    # raiz
    f.text(ox + rootw / 2, y1, fr(af).replace('-', '−'), 17, 'ink', weight=700)
    xs = [ox + rootw + 8 + i * cw + cw / 2 for i in range(n)]
    f.line(ox + rootw + 2, y1 - 20, ox + rootw + 2, y3 + 14, 'ink', 1.8)
    f.line(ox + rootw + 2, y2 + 10, xs[-1] + cw / 2, y2 + 10, 'ink', 1.8)
    for i, c in enumerate(coefs):
        f.text(xs[i], y1, fr(c).replace('-', '−'), 17, 'blue', weight=700)
    if show_label: f.text(ox + rootw / 2, y1 - 22, '~raiz', 7.4, 'gray')
    # estágios
    done = min(stage, n)   # quantos b calculados
    for i in range(done):
        if i == 0:
            f.text(xs[0], y3, fr(b[0]).replace('-', '−'), 17, 'green', weight=800)
            if stage == 1:
                f.arrow(xs[0], y1 + 6, xs[0], y3 - 20, 'green', 2.0, 7)
                f.text(xs[0] + 8, y2 + 2, '~BAIXA', 8.4, 'green', anchor='start', weight=800)
        else:
            f.text(xs[i], y2 + 3, fr(prods[i]).replace('-', '−'), 11.5, 'blue', weight=700)
            lastc = (i == done - 1 and stage < n + 0 and stage >= 2 and stage == i + 1)
            f.text(xs[i], y3, fr(b[i]).replace('-', '−'), 17, 'orange' if i < n - 1 else 'red', weight=800)
            if i == done - 1 and stage < n + 1 and stage == i + 1:
                f.arrow(xs[i - 1] + 10, y3 - 12, xs[i] - 10, y2 - 4, 'blue', 1.5, 6)   # multiplica
                f.text((xs[i - 1] + xs[i]) / 2 + 2, y2 + 24 + 4, '~' + f'×{fr(af)}'.replace('-', '−') + ' e soma' if False else '', 8)
    if done == n:
        f.rect(xs[-1] - 22, y3 - 20, 44, 30, 'none', 'red', 1.8, rx=5)
        f.text(xs[-1], y3 + 28, '~RESTO', 8.4, 'red', weight=800)
        if n > 1:
            q = ' '.join(fr(v).replace('-', '−') for v in b[:-1])
            f.text(ox + rootw + 8 + (n - 1) * cw / 2, y3 + 28, '~quociente: ' + q, 8.2, 'green', weight=700) if False else None
        if qlabel: f.text(xs[0] - cw / 2, y3 + 28, '~coef. do quociente', 8.2, 'green', anchor='start', weight=700)
    return xs, y1, y2, y3


def fig_ruffini():
    coefs, a = [1, -4, 5, -2], 3
    W, H = 736, 312
    f = Fig(W, H)
    pw, ph = 360, 150
    titles = ['1. BAIXA o 1º coeficiente', '2. MULTIPLICA pela raiz e SOMA', '3. repita: multiplica e soma', '4. último número = RESTO']
    notes = ['1 desce sem alteração', '3·1 = 3;  −4 + 3 = −1', '3·(−1) = −3;  5 − 3 = 2', '3·2 = 6;  −2 + 6 = 4  ⇒  R = 4']
    for k in range(4):
        ox = 8 + (k % 2) * (pw + 8)
        oy = 4 + (k // 2) * (ph + 4)
        f.rect(ox - 4, oy, pw, ph, 'white', 'gray_m', 1.0, rx=5)
        ruffini_grid(f, ox + 6, oy, coefs, a, k + 1, titles[k])
        f.text(ox + 6, oy + ph - 8, '~' + notes[k], 8.6, 'gray', anchor='start')
    return f


def fig_ruffini_succ():
    W, H = 640, 300
    f = Fig(W, H)
    P = [1, 2, -5, -6]
    f.rect(2, 2, W - 4, 128, 'white', 'gray_m', 1.0, rx=5)
    f.text(10, 16, '~1ª divisão:  P(x) ÷ (x − 2)   [raiz 2]', 9.6, 'ink', anchor='start', weight=800)
    xs, y1, y2, y3 = ruffini_grid(f, 10, 10, P, 2, 4, None, cw=60, qlabel=False)
    b1, _ = ruffini_values(P, 2)
    Q1 = [int(v) for v in b1[:-1]]
    f.text(330, 72, '~resto 0  ⇒  x = 2 é raiz', 9.4, 'green', anchor='start', weight=800)
    f.text(330, 90, '~Q₁(x) = x² + 4x + 3  (coeficientes 1, 4, 3)', 9.4, 'ink', anchor='start')
    f.arrow(330, 104, 330, 140, 'green', 1.6, 6)
    f.text(340, 126, '~os coeficientes do quociente viram a nova linha de cima', 8.2, 'green', anchor='start', weight=700)
    f.rect(2, 144, W - 4, 128, 'white', 'gray_m', 1.0, rx=5)
    f.text(10, 158, '~2ª divisão:  Q₁(x) ÷ (x + 1)   [raiz −1]', 9.6, 'ink', anchor='start', weight=800)
    xs2, z1, z2, z3 = ruffini_grid(f, 10, 152, Q1, -1, 3, None, cw=60, qlabel=False)
    f.text(330, 214, '~resto 0  ⇒  x = −1 é raiz', 9.4, 'green', anchor='start', weight=800)
    f.text(330, 232, '~Q₂(x) = x + 3  ⇒  x = −3', 9.4, 'ink', anchor='start')
    f.text(8, 292, '~Logo  P(x) = (x − 2)(x + 1)(x + 3):  raízes 2, −1 e −3', 10.4, 'violet', anchor='start', weight=800)
    return f


# ---------------------------------------------------------------- p33
def fig_decomp():
    f = Fig(548, 150)
    f.text(274, 52, 'P(x) = «blue:2»·(x − «purple:(−2i)»)·(x − «purple:2i»)·(x − «green:3»)', 22, 'ink')
    f.text(70, 18, '~coeficiente dominante', 8.6, 'blue', weight=800)
    f.arrow(112, 24, 166, 38, 'blue', 1.5, 6)
    f.arrow(214, 118, 258, 62, 'purple', 1.5, 6); f.text(206, 130, '~raiz não real r₁ = −2i', 8.6, 'purple', weight=800)
    f.arrow(352, 118, 360, 62, 'purple', 1.5, 6); f.text(352, 130, '~raiz não real r₂ = 2i (conjugada de r₁)', 8.6, 'purple', weight=800)
    f.arrow(466, 100, 440, 62, 'green', 1.5, 6); f.text(486, 112, '~raiz real r₃ = 3', 8.6, 'green', weight=800)
    f.text(274, 92, '~grau 3  ⇒  3 fatores do 1º grau  ⇒  3 raízes (contadas com multiplicidade)', 8.8, 'gray')
    return f


# ---------------------------------------------------------------- p35
def fig_conjroots():
    f = Fig(300, 214)
    pl = Plane(f, 150, 108, 46)
    pl.axes(-0.8, 3.1, -1.9, 1.9, xlab='~Re', ylab='~Im', grid=True, ticks=True, step=1, tick_size=7.6, origin=False, lab_size=8.8)
    f.arrow(150 - 70, 108, 150 + 142, 108, 'blue', 1.4, 6) if False else None
    pl.line(1, 1, 1, -1, 'gray', 1.0, dash='4 3')
    pl.pt(1, 1, 'purple', 3.8); pl.pt(1, -1, 'purple', 3.8); pl.pt(2, 0, 'green', 3.8)
    pl.text(1, 1, '1 + i', 10, 'purple', dx=-7, dy=-6, anchor='end', weight=700, bg='white')
    pl.text(1, -1, '1 − i', 10, 'purple', dx=-7, dy=14, anchor='end', weight=700, bg='white')
    pl.text(2, 0, '2', 10, 'green', dx=2, dy=-8, weight=700, bg='white')
    f.text(150 + 46 * 1.05, 108 - 46 * 0.0 - 62, '~espelho: eixo real', 7.8, 'gray', anchor='start') if False else None
    f.text(150, 208, '~raízes de x³ − 4x² + 6x − 4:  2,  1 + i,  1 − i', 8.6, 'ink', weight=700)
    f.text(246, 68, '~par conjugado', 8.4, 'purple', weight=700)
    f.text(246, 80, '~(simétrico no eixo real)', 7.6, 'gray')
    return f


# ---------------------------------------------------------------- p39
def fig_biquad():
    f = Fig(736, 120)
    boxes = [(4, 150, 'blue_l', 'blue', ['~Equação original', 'x⁴ − 5x² + 4 = 0']),
             (200, 150, 'orange_l', 'orange', ['~Substitua y = x²', 'y² − 5y + 4 = 0']),
             (396, 150, 'green_l', 'green', ['~Resolva em y', 'y = 1  ou  y = 4']),
             (592, 140, 'purple_l', 'purple', ['~VOLTE a x: x² = y', 'x = ±1  ou  x = ±2'])]
    for (x, w, fl, st, ls) in boxes:
        f.rect(x, 14, w, 62, fl, st, 1.6, rx=6)
        f.text(x + w / 2, 36, ls[0], 9.6, st, weight=800)
        f.text(x + w / 2, 62, ls[1], 13, 'ink')
    for x in (156, 352, 548):
        f.arrow(x, 45, x + 42, 45, 'ink', 2.0, 7)
    f.text(274 - 118 + 20, 100, '~(y = x²)', 8, 'gray') if False else None
    f.text(368, 100, '~Resolver em y NÃO encerra: cada y gera duas raízes x = ± √y (reais se y > 0; não reais se y < 0; x = 0 se y = 0).', 8.6, 'red', weight=700)
    return f


ALL = [fig_poly_anat, fig_slots, fig_eval, fig_expfac, fig_chave, fig_chave2, fig_remflow, fig_dalembert,
       fig_ruffini, fig_ruffini_succ, fig_decomp, fig_conjroots, fig_biquad]
