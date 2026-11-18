"""Mapas de decisão (fluxogramas) da apostila."""
from svgkit import Fig, PAL


def decision_map(rows, accent, accent_l, title_l, title_r, W=736):
    """rows: lista de (situação[list str], método[list str]); 2 colunas, row-major por coluna."""
    n = len(rows)
    half = (n + 1) // 2
    ch, gap, top = 46, 7, 22
    H = top + half * (ch + gap) + 2
    f = Fig(W, H)
    colw = (W - 20) / 2
    f.text(8, 12, '~' + title_l, 9.5, accent, anchor='start', weight=800)
    f.text(8 + colw + 14, 12, '~' + title_r, 9.5, accent, anchor='start', weight=800)
    for i, (sit, met) in enumerate(rows):
        c = 0 if i < half else 1
        r = i if i < half else i - half
        x0 = 3 + c * (colw + 14)
        y0 = top + r * (ch + gap)
        sw, aw = colw * 0.37, 16
        mw = colw - sw - aw
        f.rect(x0, y0, sw, ch, 'gray_l', 'gray_m', 1.0, rx=4)
        for j, ln in enumerate(sit):
            f.text(x0 + sw / 2, y0 + ch / 2 + (j - (len(sit) - 1) / 2) * 12.5 + 3.6, ln if ln.startswith(('~',)) else '~' + ln, 10.2, 'ink', weight=700)
        f.arrow(x0 + sw + 1, y0 + ch / 2, x0 + sw + aw - 1, y0 + ch / 2, accent, 1.8, 6)
        f.rect(x0 + sw + aw, y0, mw, ch, accent_l, accent, 1.2, rx=4)
        for j, ln in enumerate(met):
            f.text(x0 + sw + aw + mw / 2, y0 + ch / 2 + (j - (len(met) - 1) / 2) * 12.5 + 3.6, ln if ln.startswith('~') else ln, 9.8, 'ink')
    return f


def fig_flow_c():
    rows = [
        (['Somar / subtrair'], ['~forma algébrica: real com real,', '~imaginário com imaginário']),
        (['Multiplicar', 'poucos fatores'], ['~distributiva e troca de i² por −1']),
        (['Dividir'], ['~multiplicar por conjugado do denominador;', '~o novo denominador é |w|²']),
        (['Potência de i'], ['~resto de n ÷ 4:  iⁿ = iʳ']),
        (['Módulo, distância,', 'círculo'], ['~√(a²+b²);  |z − w| = distância;', '~|z − z₀| = r é circunferência']),
        (['Argumento /', 'forma polar'], ['~sinais de cos θ e sen θ → quadrante;', '~θ₀ na tabela → θ']),
        (['Girar, multiplicar', 'ou dividir em cadeia'], ['~forma polar: módulos multiplicam,', '~argumentos somam']),
        (['zⁿ com n grande'], ['~De Moivre 1: ρⁿ cis(nθ); reduzir', '~nθ à 1ª volta']),
        (['wⁿ = k'], ['~De Moivre 2: n raízes, módulo ⁿ√ρ,', '~passo 360°/n (polígono regular)']),
        (['Δ < 0 em', 'ax² + bx + c = 0'], ['~Bhaskara com √Δ = i√|Δ|:', '~raízes complexas conjugadas']),
    ]
    return decision_map(rows, PAL['cyan'], PAL['cyan_l'], 'SE O PROBLEMA PEDE…  →  USE…', 'SE O PROBLEMA PEDE…  →  USE…')


def fig_flow_p():
    rows = [
        (['Valor numérico P(a)'], ['~substituição; P(0) = termo indep.;', '~P(1) = soma dos coeficientes']),
        (['Resto da divisão por', 'x − a  (ou ax + b)'], ['~Teorema do Resto: R = P(a)', '~(ou R = P(−b/a))']),
        (['x − a é fator?', 'P divisível por x − a?'], ['~D\'Alembert: P(a) = 0', '~⟺ a é raiz ⟺ resto nulo']),
        (['Dividir por x − a'], ['~Briot-Ruffini (zeros nos', '~termos ausentes!)']),
        (['Dividir por polinômio', 'de grau ≥ 2'], ['~método da chave; parar quando', '~gr R < gr D']),
        (['Candidatos a raiz', 'racional'], ['~p/q: p | a₀, q | aₙ; testar com', '~Ruffini (são só candidatos)']),
        (['Conheço uma raiz r'], ['~reduzir o grau: P = (x − r)·Q', '~e resolver Q']),
        (['Raiz não real,', 'coeficientes reais'], ['~conjugada também é raiz;', '~fator x² − 2ax + a² + b²']),
        (['Soma / produto das', 'raízes, coeficientes'], ['~Girard: S₁ = −aₙ₋₁/aₙ;', '~produto = (−1)ⁿ a₀/aₙ']),
        (['ax⁴ + bx² + c = 0'], ['~y = x²; resolver em y; voltar:', '~x = ± √y (todas, inclusive não reais)']),
    ]
    return decision_map(rows, PAL['violet'], PAL['violet_l'], 'SE O PROBLEMA PEDE…  →  USE…', 'SE O PROBLEMA PEDE…  →  USE…')


def fig_flow_eq():
    W, H = 736, 150
    f = Fig(W, H)
    steps = [
        ('1', 'Fatore o que der', ['x em evidência,', 'agrupamento,', 'produtos notáveis']),
        ('2', 'Ache uma raiz', ['P(0)=0?  P(1)=0?', 'P(−1)=0?  Teste os', 'candidatos p/q']),
        ('3', 'Reduza o grau', ['Ruffini: P = (x−r)·Q;', 'repita se a raiz for', 'múltipla']),
        ('4', 'Resolva o resto', ['grau 2: Bhaskara', '(Δ<0: conjugadas);', 'biquadr.: y = x²']),
        ('5', 'Confira', ['Girard: soma e', 'produto; substitua', 'uma raiz em P(x)']),
    ]
    bw, gap = 128, 20
    for i, (n, t, ls) in enumerate(steps):
        x = 8 + i * (bw + gap)
        f.rect(x, 6, bw, 108, 'violet_l' if i != 4 else 'green_l', 'violet' if i != 4 else 'green', 1.3, rx=5)
        f.circle(x + 15, 24, 9.5, 'violet' if i != 4 else 'green', 'white', 1)
        f.text(x + 15, 28, '~' + n, 11, 'white', weight=800)
        f.text(x + 30, 28, '~' + t, 10.4, 'ink', anchor='start', weight=800)
        for j, l in enumerate(ls):
            f.text(x + bw / 2, 55 + j * 16, '~' + l, 9.4, 'ink')
        if i < 4:
            f.arrow(x + bw + 2, 60, x + bw + gap - 2, 60, 'violet', 2.0, 7)
    f.text(W / 2, 132, '~Se nenhuma raiz racional aparecer, a equação pode ter raízes irracionais ou complexas:', 8.8, 'gray')
    f.text(W / 2, 144, '~nem toda cúbica tem raiz racional (ex.: x³ = 2).', 8.8, 'gray')
    return f


ALL = [fig_flow_c, fig_flow_p, fig_flow_eq]
