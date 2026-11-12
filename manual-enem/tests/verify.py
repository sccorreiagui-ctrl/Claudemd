"""Verificação independente dos resultados numéricos do manual (rodar: python3 tests/verify.py)."""
import math
from fractions import Fraction as F

ok = lambda c, m: print(('OK   ' if c else 'FALHA'), m) or (_ for _ in ()).throw(AssertionError(m)) if not c else print('OK   ', m)

# Cap.1
V = 2.0 * 1.5 * 1.2; ok(abs(V - 3.6) < 1e-9, 'E1 volume 3,6 m³'); ok(abs(0.75 * 3600 / 12 - 225) < 1e-9, 'E1 t = 225 min = 3h45')
ok(abs(2430 / (0.75 * 0.9) - 3600) < 1e-6 and abs(1 - .675 - .325) < 1e-9, 'E2 preço 3600 e desconto 32,5%')
ok(abs(4000 * 1.05**2 * (1 + .02 * 5) - 4851) < 1e-6, 'E3 montante 4851')
ok(abs(6 * 5 * ... if False else 5 * (2000 / 1200) * (6 / 10) - 5) < 1e-9, 'regra de três composta = 5 h')
ok(abs(800 / 200**2 - 0.02) < 1e-12 and 800 / 200**2 * 1e4 == 200, 'maquete 200 cm²')
ok(abs(1.02**12 - 1.268) < 1e-3, 'taxa equivalente 26,8%')
ok(abs(80 / 0.75 - 106.67) < 0.01, 'lucro sobre venda 106,67')
ok(1000 * 1.1**10 > 2593 and 1000 * 1.1**10 < 2594, 'juros compostos 10 períodos 2.594')
ok(300 == 1500 / (12 - 7) and 12 * 300 == 1500 + 7 * 300, 'equilíbrio lucro x=300')
# Cap.2
d = [4]*3 + [6]*6 + [7]*5 + [9]*4 + [10]*2
ok(sum(d) == 139 and len(d) == 20 and sum(d) / 20 == 6.95, 'E4 média 6,95')
s = sorted(d); ok((s[9] + s[10]) / 2 == 7, 'E4 mediana 7'); ok(max(set(d), key=d.count) == 6, 'E4 moda 6'); ok((139 + 8) / 21 == 7, 'E4 21º = 8')
ok(F(4, 10) * F(6, 9) * 2 == F(8, 15) and F(math.comb(4, 1) * math.comb(6, 1), math.comb(10, 2)) == F(8, 15), 'E5 = 8/15')
ok(F(12, 90) + F(24, 90) + F(24, 90) + F(30, 90) == 1, 'árvore soma 1')
dd = [3, 4, 4, 5, 6, 8, 14]; ok(sum(dd) == 44 and sorted(dd)[3] == 5, 'dot plot')
ok(math.comb(5, 2) / 2**5 == 5 / 16, 'moeda 5/16'); ok(math.factorial(4) // 2 == 12, 'anagramas ENEM')
ok(abs(10 / 6 - 2 + .3333) < 1e-3, 'valor esperado -0,33')
# Cap.3
ok(all((a - 3) == 0 or True for a in [1]) and (2*3*3 - 7*3 + 3 == 0) and abs(2*.25 - 3.5 + 3) < 1e-9, '2x²-7x+3: raízes 3 e 1/2')
ok((40 - 10) * (200 + 100) == 9000, 'E7 receita 9000'); R = lambda x: (40 - 2*x) * (200 + 20*x)
ok(max(R(x/100) for x in range(0, 2000)) == 9000 and R(5) == 9000 and R(-10) == 0 and R(20) == 0, 'E7 vértice x=5')
ok(-5*2**2 + 20*2 == 20 and -5*4**2 + 20*4 == 0, 'bola 20 m / 4 s'); ok(10 * (40 - 20) == 200, 'cerca 200 m²')
ok((43 - 22) / (12 - 5) == 3 and 22 - 15 == 7 and 7 + 3*5 == 12 + 2*5 == 22, 'E6 táxi'); ok(2*3+3 == 5*3-6 + 0 or (2*3+3 == 9 and 5*3-6 == 9), 'retas cruzam x=3')
ok(99**2 == 9801 and 51*49 == 2499, 'notáveis cálculo mental'); ok(30 + 20 == 50 and 20*30 + 10*20 == 800, 'ingressos')
# vértice x²-4x+3 e -x²+2x+3
ok((1-4+3, 9-12+3) == (0, 0) and 4 - 8 + 3 == -1 and -1 + 2 + 3 == 4, 'parábolas das figuras')
# Cap.4
ok(sum([2,5,8,11,14,17]) == 57 and 6*19/2 == 57, 'Gauss 57')
n = 9; ok(n*(n+7)/4 == 36 and 2 + .5*(n-1) == 6, 'E8 PA n=9, a9=6'); ok(3 + 19*4 == 79 and 20*82/2 == 820, 'PA a20,S20'); ok((98-14)//7 + 1 == 13, '13 múltiplos de 7')
ok(abs(10 + 2 * 6 / (1 - .6) - 40) < 1e-9 and abs(10 * 1.6 / .4 - 40) < 1e-9, 'E9 bola 40 m'); ok(2*3**4 == 162 and 8 / (1 - .5) == 16, 'PG')
ok(abs(20000 * 1.03**5 - 23185.5) < 1, 'população'); ok(abs(40000 * .9**3 - 29160) < 1e-6, 'depreciação'); ok(96/12 == 8 and 12/4 == 3, 'PG dois termos')
ok(1+3+5+7+9 == 25, 'ímpares'); ok(abs(1.05**3 - 1.157625) < 1e-9, 'fator 5% em 3 anos')
# Cap.5
for n_, Si, ai, d_ in [(5,540,108,5),(6,720,120,9),(8,1080,135,20),(10,1440,144,35),(12,1800,150,54),(9,1260,140,27)]:
    ok((n_-2)*180 == Si and Si / n_ == ai and n_*(n_-3)//2 == d_, f'polígono n={n_}')
ok(360/(180-150) == 12 and 12*9//2 == 54, 'ângulo interno 150° -> 54 diagonais')
ok(math.hypot(3, 4) == 5 and math.sqrt(25 - 9) == 4, 'Pitágoras 3-4-5')
A = 6 * 36 * 1.7 / 4; ok(abs(A - 91.8) < 1e-9 and abs(A - 3.1*4 - 79.4) < 1e-9 and abs(79.4 * 25 - 1985) < 1e-9, 'E10 hexágono R$ 1985')
ok(abs(100 * 2*math.pi*.3 - 188.5) < .1 and abs(60 * 3.14 - 188.4) < 1e-9, 'roda 188 m'); ok(abs(.75 * 64 * 3.14 - 150.72) < 1e-9, 'praça 150,72')
ok(1.8 * 4 / 1.2 == 6, 'sombra 6 m'); ok(abs(1/6 * 3 * 36 - 18) < 1e-9, 'setor 60° r=6 π=3')
# Cap.6
h = 20 * math.sqrt(3); x = h / math.sqrt(3)
ok(abs(math.tan(math.radians(60)) - h / x) < 1e-9 and abs(math.tan(math.radians(30)) - h / (x + 40)) < 1e-9 and abs(h - 34.64) < .01 and abs(x - 20) < 1e-9, 'E11 torre 34,6 m')
ok(abs(6*8/10 - 4.8) < 1e-9 and abs(4.8**2 - 6.4*3.6) < 1e-9 and abs(6**2 - 10*3.6) < 1e-9, 'relações métricas 6-8-10')
ok(abs(math.degrees(math.asin(.25)) - 14.48) < .01, 'rampa 14,5°'); ok(abs(math.degrees(math.atan(.08)) - 4.57) < .01, 'rampa 8% = 4,6°')
ok(abs(30*math.tan(math.radians(60)) + 1.6 - 53.55) < .05 and abs(30*1.73 + 1.6 - 53.5) < 1e-9, 'prédio 53,5 m')
ok(abs(math.sqrt(30**2 + 40**2 - 2*30*40*.5) - 36.06) < .01, 'navios 36 km')
ok(abs(10*math.sin(math.radians(60))/math.sin(math.radians(45)) - 5*math.sqrt(6)) < 1e-9 and abs(5*math.sqrt(6) - 12.25) < .01, 'lei dos senos 5√6')
ok(abs(math.sin(math.radians(120)) - math.sin(math.radians(60))) < 1e-12 and abs(math.cos(math.radians(120)) + .5) < 1e-12, 'obtusos')
ok(math.sqrt(5**2 + 5**2 - 2*5*5*.5) == 5 and .5*6*8*.5 == 12, 'LAL 5,5,60° e área 12')
# Cap.7
ok(abs((72 + 36 - 90) * 3.14 - 56.52) < 1e-9, 'E12 transbordo 56,5 mL'); ok(abs(4/3 * 27 - 36) < 1e-12 and 9*8 == 72 and 9*10 == 90, 'copo/esfera')
ok(abs(math.pi/3 * 4 * (36 + 18 + 9) - 84*math.pi) < 1e-9 and 96 - 12 == 84, 'tronco de cone 84π'); ok(1.5**3 == 3.375 and 4 * 50**3 == 500000, 'cubo 3375 L; maquete 500 m³')
ok(math.hypot(3, 4) == 5 and 12 * 3 == 36, 'cone r=3 h=4 g=5, V=12π (1/3·9·4)')
# Cap.8
ok(math.hypot(6, 8) == 10 and (1+7)/2 == 4 and (2+10)/2 == 6, 'distância 10, M(4,6)')
M = ((-1 + 7)/2, (2 + 8)/2); r = math.hypot(8, 6)/2
ok(M == (3, 5) and r == 5 and (6-3)**2 + (9-5)**2 == 25 and (1-3)**2 + (1-5)**2 == 20, 'E13 circunferência')
ok(math.log10(12) - (2*.30 + .48) < .01 and abs(math.log10(5) - .70) < .01, 'log 12 = 1,08, log 5'); ok(abs(8 / .30 - 26.67) < .01 and abs(8*math.log2(10) - 26.58) < .1, 'meia-vida 26,7 h')
ok(abs(math.log(2)/math.log(1.05) - 14.2) < .05, 'dobrar a 5% a.m. ≈ 14 meses'); ok(8**(2/3) - 4 < 1e-9 and 2**5 * 2**-2 * 4 == 32, 'potências'); ok(3**4 == 81 and 4**1.5 == 8, 'log/expo')
# Estratégia 26
ok(math.lcm(15, 20) == 60 and math.gcd(120, 180) == 60 and abs(.85**3 - .614125) < 1e-9, 'MMC/MDC/PG 0,614')
print('\nTodas as verificações passaram.')
