"""Verificação dos DADOS das figuras (os mesmos números que os scripts de figura usam)."""
import os, sys, math
from fractions import Fraction
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'figs'))
import figs_p as fp
import figs_c as fc

x = sp.symbols('x')
n = 0
def ok(name, cond):
    global n
    assert cond, 'FALHOU: ' + name
    n += 1

# --- Ruffini: grade das figuras == divisão simbólica
for coefs, a in [([1, -4, 5, -2], 3), ([1, 2, -5, -6], 2), ([1, 4, 3], -1), ([1, 0, -3, 2, 0, 4], -1), ([4, -6, 2, -1], Fraction(3, 2))]:
    b, _ = fp.ruffini_values(coefs, a)
    q, r = sp.div(sp.Poly(coefs, x), sp.Poly([1, -sp.Rational(a.numerator, a.denominator) if isinstance(a, Fraction) else -a], x))
    ok(f'ruffini {coefs} raiz {a}', [sp.Rational(v.numerator, v.denominator) for v in b[:-1]] == q.all_coeffs() and sp.Rational(b[-1].numerator, b[-1].denominator) == r.as_expr())

# --- Divisão pela chave: passos == divisão simbólica
for P, D in [([1, -3, 5, -3], [1, -1]), ([6, -3, 3, -1, 1], [2, 1, -3])]:
    steps = fp.long_division(P, D)
    Qc = [s[0] for s in steps]
    q, r = sp.div(sp.Poly(P, x), sp.Poly(D, x))
    ok(f'chave {P}/{D}: quociente', [sp.Rational(c.numerator, c.denominator) for c in Qc] == q.all_coeffs())
    last = steps[-1][3]
    rem = sum(sp.Rational(c.numerator, c.denominator) * x**(len(last) - 1 - i) for i, c in enumerate(last))
    ok(f'chave {P}/{D}: resto', sp.expand(rem - r.as_expr()) == 0)

# --- polígonos das raízes: pontos == raízes de z^n = k
for nn, k, R_ in [(3, 1, 1), (4, 1, 1), (6, 1, 1), (3, 8, 2), (4, -16, 2)]:
    z = sp.symbols('z')
    roots = sp.Poly(z**nn - k, z).nroots(n=30)
    th0 = 0 if k > 0 else math.pi / nn
    pts = [R_ * complex(math.cos(th0 + 2 * math.pi * j / nn), math.sin(th0 + 2 * math.pi * j / nn)) for j in range(nn)]
    ok(f'raízes z^{nn}={k}', all(min(abs(complex(r) - p) for p in pts) < 1e-9 for r in roots))
r3 = sp.Poly(sp.symbols('z')**3 + 1, sp.symbols('z')).nroots(n=30)
pts = [complex(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (60, 180, 300)]
ok('fig_roots3: cis60,180,300', all(min(abs(complex(r) - p) for p in pts) < 1e-9 for r in r3))

# --- ângulos principais dos quatro complexos da figura de quadrantes
for z, deg in [(complex(math.sqrt(3), 1), 30), (complex(-1, 1), 135), (complex(-1, -1), 225), (complex(1, -1), 315)]:
    a = math.degrees(math.atan2(z.imag, z.real)) % 360
    ok(f'arg {z}', abs(a - deg) < 1e-9)

# --- figuras de rotação / produto polar
z = 2 + 1j
ok('rot i·z', abs(1j * z - (-1 + 2j)) < 1e-12 and abs((1 + 1j) * z - (1 + 3j)) < 1e-12)
Z, W = 2 * complex(math.cos(math.radians(30)), math.sin(math.radians(30))), math.sqrt(2) * complex(math.cos(math.radians(45)), math.sin(math.radians(45)))
P = Z * W
ok('fig_polarmult |ZW|=2√2, arg=75°', abs(abs(P) - 2 * math.sqrt(2)) < 1e-12 and abs(math.degrees(math.atan2(P.imag, P.real)) - 75) < 1e-9)
ok('fig_sum/diff', (4 + 3j) + (1 + 2j) == 5 + 5j and (4 + 3j) - (1 + 2j) == 3 + 1j and abs(abs(3 + 1j) - math.sqrt(10)) < 1e-12)
ok('fig_locus círculo centro (2,1) r=3 contém (5,1) e (2,4)', abs(abs((5 + 1j) - (2 + 1j)) - 3) < 1e-12 and abs(abs((2 + 4j) - (2 + 1j)) - 3) < 1e-12)
ok('fig_modulus 3-4-5', math.hypot(3, 4) == 5)
ok('fig_polar z=1+√3 i: ρ=2, θ=60°', abs(abs(1 + 1j * math.sqrt(3)) - 2) < 1e-12 and abs(math.degrees(math.atan2(math.sqrt(3), 1)) - 60) < 1e-9)

# --- gráficos matplotlib: raízes e sinais
f = lambda t: (t + 1) * (t - 1) * (t - 2)
ok('fig_graph_roots raízes', f(-1) == 0 and f(1) == 0 and f(2) == 0)
g = lambda t: (t + 2) * (t - 1) ** 2 * (t - 3) ** 3
eps = 1e-3
ok('fig_mult_poly: sinais perto de cada raiz', g(-2 - eps) > 0 > g(-2 + eps) and g(1 - eps) < 0 and g(1 + eps) < 0 and g(3 - eps) < 0 < g(3 + eps))
print(f'{n} verificações de figuras OK')
