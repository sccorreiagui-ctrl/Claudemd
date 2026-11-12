"""Capítulo 9 – Formulário essencial e guia 'Como saber qual fórmula usar?'."""
from lib import *

LABEL = 'REVISÃO FINAL · FORMULÁRIO E GUIA DE DECISÃO'


def G(title, rows, cls=''):
    sep = ' <span class="sepd">│</span> '
    r = ''.join(f'<div class="fgr"><span class="n">{n}</span><span class="f">{f.replace(" · ", sep)}</span></div>' for n, f in rows)
    return f'<div class="fg {cls}"><div class="fgh">{title}</div>{r}</div>'


def p_formulario():
    head = chapter_band('FINAL', 'Formulário essencial de Matemática para o ENEM', 'só o indispensável · por área')
    g1 = G('BÁSICA E FINANÇAS', [
        ('Regra de três', r'\(\tfrac{y_1}{x_1}=\tfrac{y_2}{x_2}\) direta · \(x_1y_1=x_2y_2\) inversa'),
        ('Escala · semelhança', r'\(E=\tfrac{\text{desenho}}{\text{real}}\) · área \(\times k^2\) · volume \(\times k^3\)'),
        ('Vazão', r'\(Q=\tfrac Vt=A\cdot v\) <i>(L/min, m³/h)</i>'),
        ('MMC · MDC', r'\(\mmc\cdot\mdc=a\cdot b\) <i>(2 números)</i>'),
        ('Porcentagem', r'aumento \(\times(1+i)\) · desconto \(\times(1-i)\) · sucessivos: <b>multiplicar</b>'),
        ('Lucro', r'\(L=R-C\) · equilíbrio \(x=\tfrac{C_F}{p-c_v}\)'),
        ('Juros', r'simples \(M=C(1+it)\) · compostos \(M=C(1+i)^t\)'),
        ('Unidades', r'1 m³ = 1000 L · 1 L = 1000 cm³ · 1 m² = 10⁴ cm² · 1 m/s = 3,6 km/h'),
        ('Not. científica', r'\(a\times10^n,\ 1\le a\lt10\) · OG: \(a\lt3{,}16\to10^n\), senão \(10^{n+1}\)')])
    g2 = G('ESTATÍSTICA E CONTAGEM', [
        ('Média', r'\(\bar x=\tfrac{\sum x_i}{n}\) · ponderada \(\tfrac{\sum x_if_i}{\sum f_i}\)'),
        ('Mediana · moda', r'valor central ordenado (n par: média dos 2 centrais) · valor mais frequente'),
        ('Probabilidade', r'\(P=\tfrac{\text{fav.}}{\text{poss.}}\) · \(P(\bar A)=1-P(A)\) · \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\)'),
        ('“e” · “ou”', r'independentes: \(P(A\cap B)=P(A)P(B)\) · condicional \(\tfrac{P(A\cap B)}{P(B)}\)'),
        ('Contagem', r'\(n_1n_2\cdots\) · \(P_n=n!\) · \(A_{n,p}=\tfrac{n!}{(n-p)!}\) · \(C_{n,p}=\tfrac{n!}{p!(n-p)!}\)')], 'purple')
    g3 = G('ÁLGEBRA E FUNÇÕES', [
        ('Notáveis', r'\((a\pm b)^2=a^2\pm2ab+b^2\) · \((a+b)(a-b)=a^2-b^2\)'),
        ('Bhaskara', r'\(\Delta=b^2-4ac\) · \(x=\tfrac{-b\pm\sqrt\Delta}{2a}\) · Δ&lt;0: sem raiz real'),
        ('Função afim', r'\(f=ax+b\) · \(a=\tfrac{\Delta y}{\Delta x}\) · raiz \(-\tfrac ba\) · \(b=f(0)\)'),
        ('Quadrática', r'\(x_v=-\tfrac{b}{2a}\) · \(y_v=-\tfrac{\Delta}{4a}=f(x_v)\) · \(S=-\tfrac ba,\ P=\tfrac ca\)'),
        ('Formas', r'\(a(x-x_1)(x-x_2)\) · \(a(x-x_v)^2+y_v\) · \(a\gt0\): mínimo; \(a\lt0\): máximo'),
        ('Exponencial · log', r'\(f=a\,b^x\) · \(\log_ba=x\iff b^x=a\) · \(\log ab=\log a+\log b\) · \(\log a^n=n\log a\)'),
        ('Potências', r'\(a^ma^n=a^{m+n}\) · \((a^m)^n=a^{mn}\) · \(a^{-n}=\tfrac1{a^n}\) · \(a^{m/n}=\sqrt[n]{a^m}\)')], 'green')
    g4 = G('PROGRESSÕES', [
        ('PA', r'\(a_n=a_1+(n-1)r\) · \(S_n=\tfrac{n(a_1+a_n)}{2}\)'),
        ('PG', r'\(a_n=a_1q^{n-1}\) · \(S_n=\tfrac{a_1(q^n-1)}{q-1}\) · \(S_\infty=\tfrac{a_1}{1-q},\ |q|\lt1\)')])
    g5 = G('GEOMETRIA PLANA', [
        ('Polígonos', r'\(S_i=(n-2)180^\circ\) · \(a_e=a_c=\tfrac{360^\circ}{n}\) · \(a_i=180^\circ-a_e\) · \(d=\tfrac{n(n-3)}{2}\)'),
        ('Pitágoras', r'\(a^2=b^2+c^2\) · diag. quadrado \(\ell\sqrt2\) · \(h_{\triangle}=\tfrac{\ell\sqrt3}{2}\) · \(A_{\triangle}=\tfrac{\ell^2\sqrt3}{4}\)'),
        ('Áreas', r'ret. \(bh\) · tri. \(\tfrac{bh}2\) · trap. \(\tfrac{(B+b)h}{2}\) · losango \(\tfrac{Dd}{2}\) · hexágono \(\tfrac{3\ell^2\sqrt3}{2}\)'),
        ('Círculo', r'\(C=2\pi r\) · \(A=\pi r^2\) · setor \(\tfrac{\theta}{360^\circ}\pi r^2\) · coroa \(\pi(R^2-r^2)\)'),
        ('Relações métricas', r'\(h^2=mn\) · \(b^2=am\) · \(c^2=an\) · \(bc=ah\)')])
    g6 = G('TRIGONOMETRIA', [
        ('Razões', r'\(\sen=\tfrac{op}{hip}\) · \(\cos=\tfrac{adj}{hip}\) · \(\tg=\tfrac{op}{adj}\) · \(\sen^2+\cos^2=1\)'),
        ('Notáveis', r'30°: \(\tfrac12,\tfrac{\sqrt3}2,\tfrac{\sqrt3}3\) · 45°: \(\tfrac{\sqrt2}2,\tfrac{\sqrt2}2,1\) · 60°: \(\tfrac{\sqrt3}2,\tfrac12,\sqrt3\) <i>(sen, cos, tg)</i>'),
        ('Leis', r'\(\tfrac{a}{\sen A}=2R\) · \(a^2=b^2+c^2-2bc\cos A\) · \(A_\triangle=\tfrac12bc\sen A\)')], 'purple')
    g7 = G('GEOMETRIA ESPACIAL', [
        ('Prisma · cubo', r'\(V=A_bh\) · cubo \(a^3,\ 6a^2,\ D=a\sqrt3\) · paralelepípedo \(abc,\ D=\sqrt{a^2+b^2+c^2}\)'),
        ('Cilindro', r'\(V=\pi r^2h\) · \(A_{lat}=2\pi rh\) · \(A_t=2\pi r(r+h)\)'),
        ('Cone', r'\(V=\tfrac13\pi r^2h\) · \(g^2=h^2+r^2\) · \(A_{lat}=\pi rg\)'),
        ('Esfera', r'\(V=\tfrac43\pi r^3\) · \(A=4\pi r^2\)'),
        ('Tronco', r'\(V=\tfrac h3(A_B+\sqrt{A_BA_b}+A_b)\) ou grande − pequeno (\(k^3\))')], 'green')
    g8 = G('GEOMETRIA ANALÍTICA', [
        ('Distância', r'\(d=\sqrt{(\Delta x)^2+(\Delta y)^2}\) · \(M=\big(\tfrac{x_1+x_2}2,\tfrac{y_1+y_2}2\big)\)'),
        ('Circunferência', r'\((x-a)^2+(y-b)^2=r^2\) · reta \(m=\tfrac{\Delta y}{\Delta x}\); \(\parallel:m_1=m_2\); \(\perp:m_1m_2=-1\)')])
    ref = G('NÚMEROS QUE ECONOMIZAM TEMPO', [
        ('Raízes e π', r'\(\sqrt2\approx1{,}41\) · \(\sqrt3\approx1{,}73\) · \(\sqrt5\approx2{,}24\) · \(\pi\approx3{,}14\)'),
        ('Quadrados', r'11²=121 · 12²=144 · 13²=169 · 14²=196 · 15²=225 · 25²=625'),
        ('Potências de 2', r'2⁵=32 · 2⁶=64 · 2⁷=128 · 2⁸=256 · 2¹⁰=1024'),
        ('Logs úteis', r'log 2 ≈ 0,30 · log 3 ≈ 0,48 · log 5 ≈ 0,70 · log 7 ≈ 0,85')], 'purple')
    cols_ = f'<div class="fcols">{g1}{g2}{g3}{g4}{g5}{g6}{g7}{g8}{ref}</div>'
    return head + cols_


def p_decisao():
    head = chapter_band('FINAL', 'Como saber qual fórmula usar?', 'identifique a ferramenta antes de calcular')
    passos = ('<div class="cvbox" style="background:var(--lblue);border-color:var(--mblue)"><b class="n">PROTOCOLO DE 4 PASSOS:</b> '
              '<b>1.</b> leia a <u>pergunta final</u> (o que é pedido?) · <b>2.</b> liste dados e <u>unidades</u> · '
              '<b>3.</b> reconheça o padrão na tabela abaixo · <b>4.</b> calcule e <u>confira</u> (ordem de grandeza, sinal, unidade).</div>')
    rows = [
        ['dobra/triplica/metade; “mais A → menos B”', 'Regra de três', 'direta (mesmo sentido) ou inversa (inverte uma razão)'],
        ['mapa, planta, maquete, “escala 1 : N”', 'Escala', 'desenho ÷ real, mesma unidade; área × k², volume × k³'],
        ['litros por minuto, torneira, ralo, bomba', 'Vazão', 'Q = V/t; somar enchimento e subtrair esvaziamento'],
        ['eventos que se repetem e voltam a coincidir', 'MMC', 'menor múltiplo comum dos períodos'],
        ['dividir em partes iguais, as maiores possíveis', 'MDC', 'maior divisor comum (ladrilhos, grupos, cortes)'],
        ['x% a mais/menos, desconto, reajuste, sucessivos', 'Porcentagem', 'multiplicar pelos fatores 1 ± i (não somar %)'],
        ['capital, juros, montante, parcelas', 'Juros', 'simples: C(1+it); compostos: C(1+i)ᵗ'],
        ['custo fixo + variável, preço de venda, lucro', 'Lucro / afim', 'L = R − C; equilíbrio R = C'],
        ['dados em tabela/gráfico; “valor médio”', 'Média ponderada', 'Σ x·f ÷ Σ f; mediana = centro; moda = mais frequente'],
        ['sorteio, chance, “pelo menos um”', 'Probabilidade', 'favoráveis ÷ possíveis; “e” × · “ou” + · 1 − P(nenhum)'],
        ['quantas maneiras, senhas, filas, comissões', 'Contagem', 'princípio multiplicativo; ordem importa → arranjo; não → combinação'],
        ['valor fixo + taxa constante; reta no gráfico', 'Função afim', 'y = ax + b; a = Δy/Δx; igualar funções para comparar'],
        ['valor máximo/mínimo; altura máxima; lucro máximo', 'Função quadrática', 'vértice: x<sub>v</sub> = −b/2a; y<sub>v</sub> = f(x<sub>v</sub>)'],
        ['“em que instante volta ao solo”, raízes', 'Quadrática', 'f(x) = 0: soma e produto ou Bhaskara'],
        ['aumenta sempre o mesmo valor (fileiras, dias)', 'PA', 'aₙ = a₁ + (n−1)r; Sₙ = n(a₁+aₙ)/2'],
        ['aumenta/diminui x% por período; dobra a cada…', 'PG / exponencial', 'q = 1 ± i; aₙ = a₁qⁿ⁻¹; incógnita no expoente → log'],
        ['“indefinidamente”, infinitos termos', 'PG infinita', 'S = a₁/(1 − q), com |q| &lt; 1'],
        ['ângulo reto, rampa, escada, diagonal, trajeto em L', 'Pitágoras', 'a² = b² + c² (ternos 3-4-5, 5-12-13)'],
        ['altura de prédio/torre, ângulo de elevação', 'Trigonometria', 'tg = oposto/adjacente; 30°, 45°, 60°'],
        ['triângulo qualquer; 2 lados + ângulo entre eles', 'Lei dos cossenos', 'a² = b² + c² − 2bc·cos A'],
        ['lado + ângulo oposto a ele', 'Lei dos senos', 'a/sen A = b/sen B = 2R'],
        ['polígono regular, “ângulo interno de X°”', 'Polígonos', 'aₑ = 360°/n → n; d = n(n−3)/2'],
        ['piso, tinta, grama, terreno (superfície)', 'Áreas', 'decompor ou subtrair; unidade ao quadrado'],
        ['cerca, rodapé, moldura, volta completa', 'Perímetro / C = 2πr', 'soma dos lados; arco = θ/360° · 2πr'],
        ['fatia, setor, anel, calçada ao redor', 'Setor · coroa', 'A = θ/360°·πr² · π(R² − r²)'],
        ['caixa, reservatório, lata, funil, bola, silo', 'Geometria espacial', 'V = A<sub>b</sub>·h (cone/pirâmide ÷ 3); esfera 4/3·πr³'],
        ['coordenadas, alcance de antena, ponto médio', 'Analítica', 'd, M e (x−a)² + (y−b)² = r²'],
        ['números muito grandes/pequenos; “ordem de grandeza”', 'Not. científica', 'a × 10ⁿ; compare a com 3,16'],
        ['m², m³, L, km/h, g/cm³ misturados', 'Unidades', 'converta antes (m³ → ×1000 L; m² → ×10⁴ cm²)'],
    ]
    t = tbl(['Pista do enunciado', 'Conteúdo', 'Estratégia'], rows, widths=['37%', '17%', '46%'])
    r = rec(('Texto fala em “maior lucro possível” com preço × quantidade?', 'quadrática → vértice'),
            ('“A cada 15 e 20 minutos, juntos às 8 h”: quando de novo?', 'MMC = 60 min → 9 h'),
            ('“Cortar tábuas de 120 cm e 180 cm em pedaços iguais, os maiores”: tamanho?', 'MDC = 60 cm'),
            ('Valor cai 15% ao ano: razão da PG e fator em 3 anos?', 'q = 0,85 · 0,85³ ≈ 0,614'),
            title='ÚLTIMA CHECAGEM')
    return head + passos + t + r


def pages():
    return [p_formulario(), p_decisao()]
