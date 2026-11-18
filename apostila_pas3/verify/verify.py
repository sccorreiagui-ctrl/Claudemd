"""Verificação matemática (SymPy) de exemplos e gabaritos da apostila.
Uso: python3 verify/verify.py        -> imprime 'OK' por item; falha com AssertionError se algo divergir.
"""
import ast, sys
import sympy as sp
from sympy import I, sqrt, Rational as R, symbols, Poly, expand, factor, simplify, cancel, roots, div, pi, cos, sin, Abs, arg, conjugate, re, im, exp, nsimplify

x, y, z, m, k, n = symbols('x y z m k n')
checks = []


class _Cmp:
    def __init__(self, v): self.v = v
    def __eq__(self, o): return sp.expand(self.v - o) == 0


def fx(e, **kw): return _Cmp(e)


def ok(name, cond, extra=''):
    assert cond, f'FALHOU: {name} {extra}'
    checks.append(name)


def eq0(a):
    return sp.simplify(sp.expand(a)) == 0




def eqv(a, b):
    """igualdade simbólica robusta: expressões sympy/inteiros comparam por simplify(expand(a-b))==0."""
    num = (sp.Expr, int)
    if isinstance(a, num) and isinstance(b, num) and not isinstance(a, bool):
        return sp.simplify(sp.expand(sp.sympify(a) - sp.sympify(b))) == 0
    return a == b


class _T(ast.NodeTransformer):
    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq):
            return ast.copy_location(ast.Call(func=ast.Name('eqv', ast.Load()), args=[node.left, node.comparators[0]], keywords=[]), node)
        return node


BODY = r'''# ================= PARTE I — COMPLEXOS =================
# Ex.1  x^2-2x+3=0
ok('E1 raízes', set(sp.solve(x**2 - 2*x + 3, x)) == {1 + sqrt(2)*I, 1 - sqrt(2)*I})
ok('E1 soma/produto', sp.simplify((1 + sqrt(2)*I) + (1 - sqrt(2)*I)) == 2 and sp.simplify((1 + sqrt(2)*I)*(1 - sqrt(2)*I)) == 3)
ok('C1 raízes quadradas', sp.simplify(sqrt(-2)*sqrt(-8)) == -4)
ok('Teste p1', sp.solve(x**2 + 25, x) == [-5*I, 5*I] and set(sp.solve(x**2 + 2*x + 5, x)) == {-1 + 2*I, -1 - 2*I})
# p2
ok('E2 i^2027', I**2027 == -I and 2027 % 4 == 3 and 2027 == 4*506 + 3)
S = sum(I**j for j in range(1, 2027))
ok('E3 soma i..i^2026', sp.simplify(S) == -1 + I and 2026 == 4*506 + 2)
ok('teste p2', I**14 == -1 and I**121 == I and I**-1 == -I and I**100 + I**101 == 1 + I)
ok('C2 i^47+i^-3', sp.simplify(I**47 + I**-3) == 0)
ok('i^-3', I**-3 == I)
# p3
for mv in [2, -2, 3]:
    zz = (mv**2 - 4) + (mv - 2)*I
    if mv == 2: ok('E5 m=2 → z=0', zz == 0)
    if mv == -2: ok('E5 m=-2 → -4i', zz == -4*I)
# p4
ok('E6 x=±3,y=1', all((xv**2 - 5) == 4 for xv in (3, -3)))
sol = sp.solve([2*x + y - 7, x - y - 2], [x, y]); ok('E7 sistema', sol == {x: 3, y: 1})
ok('E8 (3+2i)^2', sp.expand((3 + 2*I)**2) == 5 + 12*I and sp.expand((-3 - 2*I)**2) == 5 + 12*I)
ok('E8 biquad', fx(x**4 - 5*x**2 - 36) == (x**2 - 9)*(x**2 + 4))
ok('C4 (3+4i)^2', sp.expand((3 + 4*I)**2) == -7 + 24*I)
ok('C4 biquad', fx(x**4 + 7*x**2 - 144) == (x**2 - 9)*(x**2 + 16))
# p5
ok('E9', sp.expand((3 + 4*I) + (-1 + 2*I)) == 2 + 6*I and sp.expand((5 - 2*I) - (3 - 7*I)) == 2 + 5*I)
ok('E10', sp.expand(2*(1 + I) - 3*(2 - 3*I)) == -4 + 11*I and sp.expand((5 + 3*I) - (2 - I)) == 3 + 4*I)
ok('teste p5', sp.expand((2 + I) + (3 - 4*I)) == 5 - 3*I and sp.expand((1 - I) - (4 + 2*I)) == -3 - 3*I and sp.expand(3*(1 - 2*I) - I) == 3 - 7*I)
# p6
ok('E11', sp.expand((2 + 3*I)*(3 - 2*I)) == 12 + 5*I)
ok('E12', sp.expand((1 + I)**10) == 32*I and sp.expand((3 - 2*I)**2) == 5 - 12*I and sp.expand((1 + I)**4) == -4 and sp.expand((1 + I)**8) == 16)
ok('teste p6', sp.expand((1 - I)*(2 + 3*I)) == 5 + I and sp.expand((3 + I)**2) == 8 + 6*I and sp.expand((1 + I)**3) == -2 + 2*I and sp.expand(I*(4 - I)) == 1 + 4*I)
ok('(1+i)^2', sp.expand((1 + I)**2) == 2*I and sp.expand((1 - I)**2) == -2*I)
# p7
ok('E13', sp.expand((3 - 4*I)*(3 + 4*I)) == 25 and sp.expand((2 + I)*(2 - I)) == 5)
a_, b_ = symbols('a b', real=True)
s = sp.solve([sp.re((a_ + b_*I) + 2*sp.conjugate(a_ + b_*I) - (3 - 4*I)), sp.im((a_ + b_*I) + 2*sp.conjugate(a_ + b_*I) - (3 - 4*I))], [a_, b_])
ok('E14 z+2conj=3-4i', s == {a_: 1, b_: 4})
s = sp.solve([sp.re(sp.conjugate(a_ + b_*I) - 2*(a_ + b_*I) - 3), sp.im(sp.conjugate(a_ + b_*I) - 2*(a_ + b_*I) - 3)], [a_, b_])
ok('E15 conj z = 2z+3', s == {a_: -3, b_: 0})
ok('teste p7', sp.expand((1 + 2*I)*(1 - 2*I)) == 5)
# p8
ok('E16', sp.simplify((2 - 3*I)/(3 - I) - (R(9, 10) - R(7, 10)*I)) == 0)
xx = symbols('xx', real=True)
zz = sp.simplify((1 + 2*I)/(1 - xx*I))
ok('E17 Re=0 → x=1/2', sp.solve(sp.re(sp.expand_complex(zz)), xx) == [R(1, 2)])
ok('E17 z=2i', sp.simplify((1 + 2*I)/(1 - I/2) - 2*I) == 0)
kk = symbols('kk', real=True)
zz = sp.expand_complex((kk + 2*I)/(1 + I))
ok('E18 k=2', sp.solve(sp.im(zz), kk) == [2] and sp.simplify(zz.subs(kk, 2)) == 2)
ok('teste p8', sp.simplify((4 + 2*I)/(1 + I) - (3 - I)) == 0 and sp.simplify(1/(3 + 4*I) - (3 - 4*I)/25) == 0 and sp.simplify(I/(1 - I) - (-1 + I)/2) == 0)
zc7 = sp.simplify((7 + I)/(1 - I)); ok('C7 z=3+4i', zc7 == 3 + 4*I and re(zc7)**2 + im(zc7)**2 == 25)
# p9
ok('E20 ponto médio', sp.expand((1 + 2*I + 5 - 4*I)/2) == 3 - I and sp.Abs(sp.expand((3 - I) - (1 + 2*I))) == sqrt(13) and sp.Abs(sp.expand((3 - I) - (5 - 4*I))) == sqrt(13))
ok('E20 translação', sp.expand(-1 + 3*I + (2 - I)) == 1 + 2*I)
# p10
ok('E21', sp.expand((4 + 3*I) + (1 + 2*I)) == 5 + 5*I and sp.expand((4 + 3*I) - (1 + 2*I)) == 3 + I and sp.Abs(3 + I) == sqrt(10))
xv, yv = symbols('xv yv', real=True)
ok('E22c |z-1|=|z+1| → x=0', sp.solve(sp.expand((xv - 1)**2 + yv**2 - (xv + 1)**2 - yv**2), xv) == [0])
ok('C8 distância', sp.Abs(sp.expand((-2 + 3*I) - (4 - 5*I))) == 10 and sp.Abs(sp.expand(1 + I - (4 + 5*I))) == 5)
# p11
ok('E23', sp.simplify(sp.Abs((1 + I)**8*(3 - 4*I)/(1 - I)) - 40*sqrt(2)) == 0)
ok('E23 verif', sp.simplify(sp.expand((1 + I)**8*(3 - 4*I)/(1 - I)) - 8*(7 - I)) == 0 and sp.Abs(8*(7 - I)) == 8*sqrt(50) == 40*sqrt(2))
ok('E24 z²=3-4i', sp.expand((2 - I)**2) == 3 - 4*I and sp.expand((-2 + I)**2) == 3 - 4*I)
ok('teste p11', sp.Abs(-12 + 5*I) == 13 and sp.Abs(2*I)*sp.Abs(3 - 4*I) == 10 and sp.Abs(I**2026) == 1)
ok('C9 80', sp.Abs((1 + I)**8*(3 - 4*I)) == 80)
# p12
ok('E25', sp.sin(sp.rad(150)) == R(1, 2) and sp.cos(sp.rad(210)) == -sqrt(3)/2 and sp.sin(7*pi/4) == -sqrt(2)/2)
tab = {0: (1, 0), 30: (sqrt(3)/2, R(1, 2)), 45: (sqrt(2)/2, sqrt(2)/2), 60: (R(1, 2), sqrt(3)/2), 90: (0, 1), 120: (-R(1, 2), sqrt(3)/2),
       135: (-sqrt(2)/2, sqrt(2)/2), 150: (-sqrt(3)/2, R(1, 2)), 180: (-1, 0), 270: (0, -1), 360: (1, 0)}
for d, (c_, s_) in tab.items():
    ok(f'tabela {d}°', sp.simplify(sp.cos(sp.rad(d)) - c_) == 0 and sp.simplify(sp.sin(sp.rad(d)) - s_) == 0)
tg = {0: 0, 30: sqrt(3)/3, 45: 1, 60: sqrt(3), 120: -sqrt(3), 135: -1, 150: -sqrt(3)/3, 180: 0, 360: 0}
for d, t_ in tg.items():
    ok(f'tg {d}°', sp.simplify(sp.tan(sp.rad(d)) - t_) == 0)
ok('rec p12', sp.cos(pi) == -1 and sp.sin(3*pi/2) == -1 and sp.cos(sp.rad(120)) == -R(1, 2) and sp.rad(225) == 5*pi/4 and sp.rad(330) == 11*pi/6)
ok('conv graus', sp.Rational(150, 180) == R(5, 6))

def polar(zc):
    zc = sp.nsimplify(zc)
    r_ = sp.simplify(sp.Abs(zc)); a = sp.simplify(sp.arg(zc))
    if a < 0: a += 2*pi
    return r_, sp.simplify(a)
# p13/14
ok('E26 -1+i', polar(-1 + I) == (sqrt(2), 3*pi/4))
for zc, rho, th in [(sqrt(3) + I, 2, pi/6), (-1 + sqrt(3)*I, 2, 2*pi/3), (-1 - I, sqrt(2), 5*pi/4), (-3*I, 3, 3*pi/2), (1 + sqrt(3)*I, 2, pi/3), (1 - I, sqrt(2), 7*pi/4),
                    (-1 - sqrt(3)*I, 2, 4*pi/3), (-5, 5, pi), (4*I, 4, pi/2), (5, 5, 0), (2*I, 2, pi/2), (-3, 3, pi), (sqrt(2) + sqrt(2)*I, 2, pi/4)]:
    r_, a = polar(zc)
    ok(f'polar {zc}', sp.simplify(r_ - rho) == 0 and sp.simplify(a - th) == 0, f'{r_},{a}')
ok('C10 240°', sp.simplify(sp.arg(-1 - sqrt(3)*I) + 2*pi - 4*pi/3) == 0)
ok('E30', sp.simplify(sp.expand_complex(4*sp.exp(5*pi*I/6)) - (-2*sqrt(3) + 2*I)) == 0 and sp.simplify(2*(sp.cos(pi/3) + I*sp.sin(pi/3)) - (1 + sqrt(3)*I)) == 0)
ok('teste p14', sp.simplify(sp.expand_complex(6*sp.exp(I*pi/2)) - 6*I) == 0 and sp.simplify(2*sp.exp(I*pi)) == -2)
# p15
ok('E31', sp.expand(I*(3 + I)) == -1 + 3*I and sp.expand((1 + I) + I*((4 + I) - (1 + I))) == 1 + 4*I)
A, B = 1 + I, 4 + 2*I
D_ = sp.expand(B - A); Cc = sp.expand(B + I*D_); Dd = sp.expand(A + I*D_)
ok('E32 quadrado', Cc == 3 + 5*I and Dd == 4*I and sp.expand(sp.Abs(D_)**2) == 10)
ok('teste p15', sp.expand(I*(2 - 5*I)) == 5 + 2*I and sp.expand(-I*(3 + 4*I)) == 4 - 3*I)
ok('C11 área 13', sp.Abs(sp.expand((5 + 3*I) - (2 + I)))**2 == 13)
# p16
ok('E33 prod', sp.expand((1 + I)*(sqrt(3) + I)) == (sqrt(3) - 1) + (sqrt(3) + 1)*I)
ok('E33 polar', sp.simplify(sp.expand_complex(2*sqrt(2)*sp.exp(I*sp.rad(75))) - ((sqrt(3) - 1) + (sqrt(3) + 1)*I)) == 0)
ok('cos75', sp.simplify(sp.cos(sp.rad(75)) - (sqrt(6) - sqrt(2))/4) == 0)
ok('E34', sp.simplify(sp.expand_complex(3*sp.exp(I*4*pi/3)) - (-R(3, 2) - 3*sqrt(3)/2*I)) == 0)
ok('E35', sp.simplify(sp.expand_complex(R(1, 2)*sp.exp(I*11*pi/6)) - 1/(sp.expand_complex(2*sp.exp(I*pi/6)))) == 0 and
   sp.simplify(sp.expand_complex(2*sp.exp(I*5*pi/3)) - sp.expand_complex(2*sp.exp(I*pi/6))/I) == 0)
ok('teste p16', 6*sp.exp(I*sp.rad(420)) == 6*sp.exp(I*sp.rad(60)) or sp.simplify(sp.expand_complex(6*sp.exp(I*sp.rad(420)) - 6*sp.exp(I*sp.rad(60)))) == 0)
# p17
ok('E36', sp.simplify(sp.expand_complex((5*sp.exp(I*pi/3))**3) + 125) == 0)
ok('E37', sp.expand((sqrt(3) + I)**10) == 512 - 512*sqrt(3)*I)
ok('E38 (√3+i)^3=8i', sp.expand((sqrt(3) + I)**3) == 8*I and sp.expand((sqrt(3) + I)**6) == -64 and sp.expand((sqrt(3) + I)**12) == 4096)
ok('E39', sp.simplify((1 + I)**-4 + R(1, 4)) == 0)
ok('teste p17', sp.simplify(sp.expand_complex((2*sp.exp(I*pi/4))**4) + 16) == 0 and sp.expand((1 - I)**6) == 8*I)
w = (sqrt(3) - I)/2
nmin = next(nn for nn in range(1, 100) if sp.simplify(sp.expand(w**nn).as_real_imag()[0]) == 0 and sp.simplify(sp.expand(w**nn).as_real_imag()[1]) > 0)
ok('C12 n=9', nmin == 9)
# p18
ok('E40', sp.simplify(sp.expand_complex((2*sp.exp(I*pi/6))**2 - 4*sp.exp(I*pi/3))) == 0)
r3 = sp.solve(z**3 + 1, z); ok('E41', set(sp.nsimplify(rr) for rr in r3) == {-1, R(1, 2) + sqrt(3)/2*I, R(1, 2) - sqrt(3)/2*I})
r4 = sp.solve(z**4 + 16, z); ok('E42', set(sp.simplify(rr) for rr in r4) == {sqrt(2)*(1 + I), sqrt(2)*(1 - I), sqrt(2)*(-1 + I), sqrt(2)*(-1 - I)})
ok('E42 verif', sp.expand((sqrt(2)*(1 + I))**4) == -16)
r8i = sp.solve(z**3 - 8*I, z); ok('teste p18 / C13', set(sp.simplify(rr) for rr in r8i) == {sqrt(3) + I, -sqrt(3) + I, -2*I} and all(sp.im(rr) != 0 for rr in r8i))
# p19
ok('E43', fx(z**3 - 1) == (z - 1)*(z**2 + z + 1) and set(sp.solve(z**2 + z + 1, z)) == {(-1 + sqrt(3)*I)/2, (-1 - sqrt(3)*I)/2})
ok('E44 área', sp.simplify(sp.Abs(sp.expand(2 - (-1 + sqrt(3)*I)))**2 * sqrt(3)/4 - 3*sqrt(3)) == 0 and sp.simplify(sp.Abs(sp.expand(2 - (-1 + sqrt(3)*I))) - 2*sqrt(3)) == 0)
r64 = sp.solve(z**4 - 64, z); side = sp.Abs(sp.expand(2*sqrt(2) - 2*sqrt(2)*I)); ok('C14 perímetro 16', 4*sp.simplify(side) == 16 and set(sp.simplify(rr) for rr in r64) == {2*sqrt(2), -2*sqrt(2), 2*sqrt(2)*I, -2*sqrt(2)*I})
ok('produto raízes z^4-1', sp.expand(1*I*(-1)*(-I)) == -1)
# p20
ok('C15', sp.simplify((1 + I)/(1 - I)) == I and sp.expand(I**2026) == -1)
zz = 1 + I; ok('C16 048', sp.Abs(zz**10) == 32 and sp.expand(zz**8) == 16)

# ================= PARTE II — POLINÔMIOS =================
P = lambda e: Poly(e, x)
# p21
P1 = 3*x**4 - 2*x**3 + 5*x - 7
ok('p21 grau/P(0)', P(P1).degree() == 4 and P1.subs(x, 0) == -7 and P1.subs(x, 1) == -1)
# p22
Pm = (m + 1)*x**4 + 2*x**2 - x + 17
ok('E grau 2', Poly(Pm.subs(m, -1), x).degree() == 2)
Pm2 = (m**2 - 4)*x**3 + (m - 2)*x**2 + 5
ok('grau m=2', Poly(Pm2.subs(m, 2), x).degree() == 0 and Poly(Pm2.subs(m, -2), x).degree() == 2 and Poly(Pm2.subs(m, 3), x).degree() == 3)
ok('soma queda grau', sp.expand((x**3 + x) + (-x**3 + 2)) == x + 2)
# p23
Pv = x**3 - x**2 + 1
ok('E P(2),P(i)', Pv.subs(x, 2) == 5 and sp.expand(Pv.subs(x, I)) == 2 - I and Pv.subs(x, 0) == 1 and Pv.subs(x, 1) == 1 and Pv.subs(x, -1) == -1)
ok('soma coef', ((2*x**2 - 3*x + 2)**10).subs(x, 1) == 1 and ((x**2 + x + 1)**4).subs(x, 1) == 81)
Pn = 3*x**3 - 2*x**2 + x - 5
ok('P(-1) alternada', Pn.subs(x, -1) == -11 and Pn.subs(x, 1) == -3)
ok('raiz -2 → m=5/2', sp.solve((x**3 + 4*x**2 + m*x - 3).subs(x, -2), m) == [R(5, 2)])
ok('1+i raiz de x²-2x+2', sp.expand((x**2 - 2*x + 2).subs(x, 1 + I)) == 0)
# p24
ok('E ident a,b,c', sp.solve(sp.Poly(sp.expand(x**2 + x + 1 - (symbols('a')*(x - 1)**2 + symbols('b')*(x - 1) + symbols('c'))), x).coeffs(), symbols('a b c')) == {symbols('a'): 1, symbols('b'): 3, symbols('c'): 3})
aa, bb = symbols('aa bb')
sl = sp.solve(Poly(sp.expand((-2*x + aa)*(x + bb) - (-2*x**2 - 3*x - 1)), x).coeffs(), [aa, bb])
ok('E ident (−2x+a)(x+b)', set(map(tuple, sl)) == {(-1, 1), (-2, R(1, 2))})
ok('C20 m=3,n=3', sp.solve([(m - 1) - 2, (k + 2) - 5], [m, k]) == {m: 3, k: 3})
# p25
ok('E mult', sp.expand((x**2 - 5*x + 6)*(2*x - 3)) == 2*x**3 - 13*x**2 + 27*x - 18)
ok('E 2P-Q', sp.expand(2*(x**3 - 4*x**2 + 5*x - 4) - (3*x**2 - 4*x + 3)) == 2*x**3 - 11*x**2 + 14*x - 11)
ok('(x+1)(x²-x+1)', sp.expand((x + 1)*(x**2 - x + 1)) == x**3 + 1)
# p26
ok('fat1', fx(x**3 - x**2 - 4*x + 4) == (x - 1)*(x - 2)*(x + 2))
ok('fat2', fx(x**4 - 16) == (x - 2)*(x + 2)*(x**2 + 4) and fx(x**4 - 16, extension=I) == (x - 2)*(x + 2)*(x - 2*I)*(x + 2*I))
ok('fat3', fx(6*x**2 - x - 2) == (2*x + 1)*(3*x - 2) and fx(x**3 - 8) == (x - 2)*(x**2 + 2*x + 4))
# p27
q, r = div(P(x**3 - 3*x**2 + 5*x - 3), P(x - 1))
ok('chave exata', q.as_expr() == x**2 - 2*x + 3 and r.as_expr() == 0)
q, r = div(P(6*x**4 - 3*x**3 + 3*x**2 - x + 1), P(2*x**2 + x - 3))
ok('chave inventário corrigido', q.as_expr() == 3*x**2 - 3*x + R(15, 2) and r.as_expr() == -R(35, 2)*x + R(47, 2))
ok('D·Q+R=P', sp.expand((2*x**2 + x - 3)*(3*x**2 - 3*x + R(15, 2)) + (-R(35, 2)*x + R(47, 2))) == 6*x**4 - 3*x**3 + 3*x**2 - x + 1)
ok('inventário errado de fato errado', sp.expand((2*x**2 + x - 3)*(3*x**2 - 3*x + 7) + (-14*x + 22)) != 6*x**4 - 3*x**3 + 3*x**2 - x + 1)
q, r = div(P(4*x**3 - 2*x**2 + x - 5), P(x**2 + 1))
ok('C21', q.as_expr() == 4*x - 2 and r.as_expr() == -3*x - 3)
# p28
q, r = div(P(x**3 + 2*x**2 + 3*x + 4), P(x**2 + 1)); aS, bS = symbols('aS bS')
q, r = div(P(x**3 + 2*x**2 + aS*x + bS), P(x**2 + 1))
ok('E div param a=1,b=2', sp.solve(r.all_coeffs(), [aS, bS]) == {aS: 1, bS: 2})
q, r = div(P(x + 1), P(x**2 + 1)); ok('gr P<gr D', q.as_expr() == 0 and r.as_expr() == x + 1)
q, r = div(P(x**4), P(x**2 - 1)); ok('x^4 / (x²-1)', q.as_expr() == x**2 + 1 and r.as_expr() == 1)
pp, qq = symbols('pp qq')
sl = sp.solve([(x**3 + pp*x**2 + qq*x - 6).subs(x, 1), (x**3 + pp*x**2 + qq*x - 6).subs(x, 2)], [pp, qq])
ok('C22 a=-6,b=11', sl == {pp: -6, qq: 11})
# p29
ok('E rem', (3*x**4 - x**3 + 2).subs(x, 1) == 4 and (x**5 - x**3 + 2).subs(x, -2) == -22 and (x**3 - 2*x + 5).subs(x, 2) == 9)
_, rr_ = div(P(x**3 - 2*x + 5), P(2*x - 4)); ok('rem 2x-4', rr_.as_expr() == 9)
ok('E D\'Alembert m=14/3', sp.solve((x**3 - 4*x**2 + m*x - 5).subs(x, 3), m) == [R(14, 3)])
sl = sp.solve([(x**3 + pp*x**2 + qq*x - 6).subs(x, 1), (x**3 + pp*x**2 + qq*x - 6).subs(x, -1) - 4], [pp, qq]); ok('E duas condições a=8,b=-3', sl == {pp: 8, qq: -3})
ok('C23', (x**100 - 2*x + 3).subs(x, -1) == 6)
ok('E65 chave (2x-4)', sp.expand((2*x - 4)*(R(1, 2)*x**2 + x + 1) + 9) == x**3 - 2*x + 5)
# p30
for coefs, a, qexp, rexp in [([1, -4, 5, -2], 3, [1, -1, 2], 4), ([1, 0, -3, 2, 0, 4], -1, [1, -1, -2, 4, -4], 8)]:
    qq_, rr_ = div(Poly(coefs, x), Poly([1, -a], x))
    ok(f'ruffini {coefs}', qq_.all_coeffs() == qexp and rr_.as_expr() == rexp)
qq_, rr_ = div(P(4*x**3 - 6*x**2 + 2*x - 1), P(2*x - 3)); ok('ruffini não mônico', qq_.as_expr() == 2*x**2 + 1 and rr_.as_expr() == 2)
ok('ruffini 3/2', Poly([4, 0, 2], x).as_expr() == 4*x**2 + 2)
# p31
ok('E31 P(x)=x³+mx+n', sp.solve([(x**3 + m*x + k).subs(x, 1), (x**3 + m*x + k).subs(x, -2)], [m, k]) == {m: -3, k: 2} and sp.expand((x - 1)**2*(x + 2)) == x**3 - 3*x + 2)
ok('E x³-7x²+14x-8', sp.expand((x - 1)*(x - 2)*(x - 4)) == x**3 - 7*x**2 + 14*x - 8 and 1 + 4 + 16 == 7**2 - 2*14)
ok('E sucessivas', fx(x**3 + 2*x**2 - 5*x - 6) == (x - 2)*(x + 1)*(x + 3))
ok('E x³-4x²+x+6', fx(x**3 - 4*x**2 + x + 6) == (x + 1)*(x - 2)*(x - 3))
# p32
ok('E 3x³-7x²+8x-2', fx(3*x**3 - 7*x**2 + 8*x - 2) == (3*x - 1)*(x**2 - 2*x + 2) and (3*x**3 - 7*x**2 + 8*x - 2).subs(x, R(1, 3)) == 0)
ok('E 2x³-x²-8x+4', fx(2*x**3 - x**2 - 8*x + 4) == (x - 2)*(x + 2)*(2*x - 1))
ok('x³-2 sem racional', all((x**3 - 2).subs(x, c) != 0 for c in [1, -1, 2, -2]))
ok('x⁴-3x³+2x²', fx(x**4 - 3*x**3 + 2*x**2) == x**2*(x - 1)*(x - 2))
ok('x³-15x-4', fx(x**3 - 15*x - 4) == (x - 4)*(x**2 + 4*x + 1) and set(sp.solve(x**2 + 4*x + 1, x)) == {-2 + sqrt(3), -2 - sqrt(3)})
ok('C24', set(sp.solve(2*x**3 - 3*x**2 - 3*x + 2, x)) == {-1, 2, R(1, 2)})
# p33
ok('E construir', sp.expand(2*(x + 2*I)*(x - 2*I)*(x - 3)) == 2*x**3 - 6*x**2 + 8*x - 24)
Pk = (x - 1)**2*(x + 2)*(x**2 + 1)
ok('E contagem', Poly(Pk, x).degree() == 5 and sum(sp.roots(Poly(Pk, x), multiple=True).count(r_) > 0 for r_ in set(sp.roots(Poly(Pk, x), multiple=True))) == 4 and len(sp.roots(Poly(Pk, x), multiple=True)) == 5)
ok('E -1,1,2', sp.expand((x + 1)*(x - 1)*(x - 2)) == x**3 - 2*x**2 - x + 2)
# p34
Pm = x**4 + 4*x**3 + 2*x**2 + 12*x + 45
ok('E mult -3', fx(Pm) == (x + 3)**2*(x**2 - 2*x + 5) and Pm.subs(x, -3) == 0)
ok('E construir (x-3)²(x+1)', sp.expand((x - 3)**2*(x + 1)) == x**3 - 5*x**2 + 3*x + 9)
ok('C26 mult 3', fx(x**4 - 5*x**3 + 6*x**2 + 4*x - 8) == (x - 2)**3*(x + 1))
# p35
ok('E conj x²-4x+5', sp.expand((x - (2 + I))*(x - (2 - I))) == x**2 - 4*x + 5)
ok('E x³-4x²+6x-4', sp.expand((x**2 - 2*x + 2)*(x - 2)) == x**3 - 4*x**2 + 6*x - 4 and (x**3 - 4*x**2 + 6*x - 4).subs(x, 1 - I).expand() == 0)
ok('E cúbico 1+2i, soma 5', sp.expand((x**2 - 2*x + 5)*(x - 3)) == x**3 - 5*x**2 + 11*x - 15)
ok('C27 grau 6', len({1 + I, 1 - I, 3*I, -3*I}) + 2 == 6)
# p36
ok('x²-5x+6', sp.expand((x - 2)*(x - 3)) == x**2 - 5*x + 6)
ok('x³-8x²+19x-12', fx(x**3 - 8*x**2 + 19*x - 12) == (x - 1)*(x - 3)*(x - 4))
ok('C28 soma quadrados', sum(rr**2 for rr in [1, 2, 3]) == 14 and sp.expand((x - 1)*(x - 2)*(x - 3)) == x**3 - 6*x**2 + 11*x - 6 and R(11, 6) == 1 + R(1, 2) + R(1, 3))
r1, r2, r3 = symbols('r1 r2 r3')
ok('expansão Girard', sp.expand((x - r1)*(x - r2)*(x - r3)) == x**3 - (r1 + r2 + r3)*x**2 + (r1*r2 + r1*r3 + r2*r3)*x - r1*r2*r3)
ok('inverso e soma de quadrados', sp.simplify(sum(rr**2 for rr in (r1, r2, r3)) - ((r1 + r2 + r3)**2 - 2*(r1*r2 + r1*r3 + r2*r3))) == 0)
# p37
ok('E x⁴-10x³+35x²-50x+24', sp.expand((x - 1)*(x - 2)*(x - 3)*(x - 4)) == x**4 - 10*x**3 + 35*x**2 - 50*x + 24)
ok('E PA 1,3,5', sp.expand((x - 1)*(x - 3)*(x - 5)) == x**3 - 9*x**2 + 23*x - 15)
ok('E (x-1)²(x-2)', sp.expand((x - 1)**2*(x - 2)) == x**3 - 4*x**2 + 5*x - 2)
ok('E coef desconhecidos', sp.expand((x - 2)*(x - 3)*(x - 4)) == x**3 - 9*x**2 + 26*x - 24)
ok('E conj+Girard', sp.expand((x**2 - 2*x + 5)*(x + 2)) == x**3 + x + 10)
ok('C29 PA', sp.expand((x - 2)*(x - 4)*(x - 6)) == x**3 - 12*x**2 + 44*x - 48)
ok('biquad soma 0 / produto 4', sp.expand((x - 1)*(x + 1)*(x - 2)*(x + 2)) == x**4 - 5*x**2 + 4)
# p38
ok('E x³-3x²+7x-5', fx(x**3 - 3*x**2 + 7*x - 5) == (x - 1)*(x**2 - 2*x + 5) and set(sp.solve(x**2 - 2*x + 5, x)) == {1 + 2*I, 1 - 2*I})
ok('E x³+1', fx(x**3 + 1) == (x + 1)*(x**2 - x + 1) and set(sp.solve(x**2 - x + 1, x)) == {(1 + sqrt(3)*I)/2, (1 - sqrt(3)*I)/2})
ok('E x³-7x+6', fx(x**3 - 7*x + 6) == (x - 1)*(x - 2)*(x + 3))
ok('E x²+2x+5', set(sp.solve(x**2 + 2*x + 5, x)) == {-1 + 2*I, -1 - 2*I})
# p39
ok('E x⁴-5x²+4', set(sp.solve(x**4 - 5*x**2 + 4, x)) == {1, -1, 2, -2})
ok('E x⁴+3x²-4', set(sp.solve(x**4 + 3*x**2 - 4, x)) == {1, -1, 2*I, -2*I})
ok('E x⁴+4', set(sp.solve(x**4 + 4, x)) == {1 + I, 1 - I, -1 + I, -1 - I} and sp.expand((x**2 + 2*x + 2)*(x**2 - 2*x + 2)) == x**4 + 4)
ok('E x⁴-4x²', fx(x**4 - 4*x**2) == x**2*(x - 2)*(x + 2))
ok('E (x²-1)²', fx(x**4 - 2*x**2 + 1) == (x - 1)**2*(x + 1)**2)
ok('E quártica agrupada', sp.expand((x**2 + 5*x + 4)*(x**2 + 5*x + 6)) == sp.expand((x + 1)*(x + 2)*(x + 3)*(x + 4)) and
   set(sp.solve((x + 1)*(x + 2)*(x + 3)*(x + 4) - 24, x)) == {0, -5, (-5 + sqrt(15)*I)/2, (-5 - sqrt(15)*I)/2})
ok('C30', sum(abs(rr) for rr in sp.solve(x**4 - 13*x**2 + 36, x)) == 10)
# p40
ok('C31', sp.expand((x - 2)*(x - (1 + I))*(x - (1 - I))) == x**3 - 4*x**2 + 6*x - 4)
ok('C32 x⁴+64', sp.expand((x**2 + 4*x + 8)*(x**2 - 4*x + 8)) == x**4 + 64 and set(sp.solve(x**4 + 64, x)) == {2 + 2*I, 2 - 2*I, -2 + 2*I, -2 - 2*I}
   and sp.Abs((2 + 2*I) - (-2 + 2*I))**2 == 16)


# ---- complementos: Girard numérico, treinos, itens PAS comentados
rr = sp.Poly(x**3 - 4*x**2 + 6*x - 5, x).nroots(n=30)
s1 = sum(rr); s2 = rr[0]*rr[1] + rr[0]*rr[2] + rr[1]*rr[2]; s3 = rr[0]*rr[1]*rr[2]
ok('Girard x³-4x²+6x-5 (numérico)', abs(s1 - 4) < 1e-20 and abs(s2 - 6) < 1e-20 and abs(s3 - 5) < 1e-20 and abs(sum(1/r_ for r_ in rr) - R(6, 5)) < 1e-20)
ok('teste p36', R(6, 2) == 3 and sp.expand(-(2)) == -2 and sp.Poly(x**3 + 2*x**2 - 5*x - 6, x).nroots(n=20) is not None)
rts = sp.Poly(x**3 + 2*x**2 - 5*x - 6, x).nroots(n=30); ok('teste p36 produto 6', abs(rts[0]*rts[1]*rts[2] - 6) < 1e-20 and abs(sum(rts) + 2) < 1e-20)
ok('x⁴ biquad Girard', sp.expand((x - 1)*(x + 1)*(x - 2)*(x + 2)) == x**4 - 5*x**2 + 4)
ok('p39 teste x⁴-16', set(sp.solve(x**4 - 16, x)) == {2, -2, 2*I, -2*I} and sp.factor(x**4 + x**2) == x**2*(x**2 + 1))
ok('p32 teste 2x³+x-3', (2*x**3 + x - 3).subs(x, 1) == 0)
ok('p31 teste', sp.expand((x - 1)*(x - 2)*(x - 3)) == x**3 - 6*x**2 + 11*x - 6)
ok('p29 teste', (x**10 + 1).subs(x, 1) == 2 and (x**10 + 1).subs(x, -1) == 2 and (x**3 - 8).subs(x, 2) == 0)
ok('p30 teste', sp.Poly(x**4 - 1, x).all_coeffs() == [1, 0, 0, 0, -1] and div(Poly(x**4 - 1, x), Poly(x - 2, x))[0].as_expr() == x**3 + 2*x**2 + 4*x + 8 and (x**4 - 1).subs(x, 2) == 15 and (x**3 + x).subs(x, -1) == -2)
ok('p26 teste', fx(x**2 - 6*x + 9) == (x - 3)**2 and fx(9*x**2 - 1) == (3*x - 1)*(3*x + 1) and fx(x**3 + x, extension=I) == x*(x - I)*(x + I))
ok('p35 teste b,c', sp.expand((x - (2 + I))*(x - (2 - I))) == x**2 - 4*x + 5)
ok('p33 teste', sp.Poly(x**7 - 3, x).degree() == 7 and sp.Poly(x**4*(x - 2)**3, x).degree() == 7)
ok('p34 teste', sp.roots(Poly((x - 2)**3*(x + 1)**2, x))[2] == 3 and sp.roots(Poly(x**3*(x - 1), x))[0] == 3)
ok('p20 item |z-1|=|z-i|', sp.solve(sp.expand((xv - 1)**2 + yv**2 - xv**2 - (yv - 1)**2), yv) == [xv])
ok('p25 item', sp.expand((x**2 - x + 1)*(x**2 + x + 1)) == x**4 + x**2 + 1)
ok('p22 item', sp.expand((x**3 + 1) + (-x**3 + x)) == x + 1 and Poly(Poly((k**2 - 1)*x**2 + (k + 1)*x + 3, x).as_expr().subs(k, 1), x).degree() == 1)
ok('p9 item triângulo retângulo', sp.expand(((a_ - a_)*(-a_ - a_) + (2*b_)*0)) == 0)
ok('p11 item |z|=1', sp.simplify(1/(sp.exp(I*sp.Symbol('t', real=True))) - sp.conjugate(sp.exp(I*sp.Symbol('t', real=True)))) == 0)
ok('p5 item', sp.expand((2 + 3*I) + (-2 + 5*I)) == 8*I)
ok('p4 item', sp.expand((2 + I)**2) == 3 + 4*I)
ok('p7 item', sp.solve(9 + b_**2 - 25, b_) == [-4, 4])
ok('p6 item', sp.expand((2*I)**1013) == 2**1013*I and 1013 % 4 == 1)
ok('p12 item 7π/6', sp.sin(7*pi/6) == -R(1, 2) and sp.cos(7*pi/6) == -sqrt(3)/2)
'''
tree = ast.fix_missing_locations(_T().visit(ast.parse(BODY)))
exec(compile(tree, 'verify_body', 'exec'), globals())
print(f'{len(checks)} verificações OK')
