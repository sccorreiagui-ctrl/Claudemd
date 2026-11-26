#!/usr/bin/env python3
"""Validação independente (SymPy) das 15 questões da apostila CTG.

Executar:  python3 scripts/validate.py
Sai com código != 0 se qualquer verificação falhar.
Cada bloco confere (a) a resposta impressa na apostila e (b) fatos usados nos
desenhos (pés de perpendiculares, pontos de tangência etc.).
"""
import sys
from sympy import (Rational as R, Matrix, symbols, solve, sqrt, simplify, Eq,
                   Abs, expand, Poly, discriminant, nsimplify, S)

x, y, m, p = symbols("x y m p", real=True)
fails = []
n_checks = 0


def check(name, cond, detail=""):
    global n_checks
    n_checks += 1
    ok = bool(cond)
    print(("  OK   " if ok else "  FALHA ") + name + (f"   {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def line_through(P, Q):
    """equação geral a x + b y + c = 0 (inteiros, normalizada) da reta PQ"""
    a = P[1] - Q[1]
    b = Q[0] - P[0]
    c = P[0] * Q[1] - Q[0] * P[1]
    return a, b, c


def on_line(L, P):
    return L[0] * P[0] + L[1] * P[1] + L[2] == 0


def dist_pt_line(P, L):
    a, b, c = L
    return Abs(a * P[0] + b * P[1] + c) / sqrt(a**2 + b**2)


def foot(P, L):
    a, b, c = L
    t = S(a * P[0] + b * P[1] + c) / S(a**2 + b**2)
    return (P[0] - a * t, P[1] - b * t)


def dist(P, Q):
    return sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)


def proportional(L1, L2):
    return Matrix([[L1[0], L1[1], L1[2]], [L2[0], L2[1], L2[2]]]).rank() == 1


print("== PONTO E RETA ==")
# ---- R1
print("R1")
A = (-1, 2 * (-1) + 5)
yB = 1
xB = solve(Eq(yB, -x + 4), x)[0]
B = (xB, yB)
check("A = (-1,3)", A == (-1, 3))
check("B = (3,1)", B == (3, 1))
mAB = R(B[1] - A[1], B[0] - A[0])
check("m = -1/2", mAB == R(-1, 2))
L = line_through(A, B)
check("AB ∝ x+2y-5=0", proportional(L, (1, 2, -5)))
check("A,B em x+2y-5=0", on_line((1, 2, -5), A) and on_line((1, 2, -5), B))

# ---- R2
print("R2")
a, b, c = 6, 3, -12
check("m = -a/b = -2", R(-a, b) == -2)
check("n = -c/b = 4", R(-c, b) == 4)
check("perp: m' = 1/2", R(-1) / R(-a, b) == R(1, 2))
check("s: y = x/2 passa por P(2,1)", R(1, 2) * 2 == 1)
F = foot((2, 1), (6, 3, -12))
check("pé da perpendicular (8/5, 4/5)", F == (R(8, 5), R(4, 5)), str(F))
check("pé está em y=x/2", F[1] == F[0] / 2)

# ---- R3
print("R3")
A, B, P = (-2, 1), (4, 3), (1, 4)
mAB = R(3 - 1, 4 + 2)
check("m_AB = 1/3", mAB == R(1, 3))
check("AB: x-3y+5=0", on_line((1, -3, 5), A) and on_line((1, -3, 5), B))
check("AB (cíclico) ∝ x-3y+5", proportional(line_through(A, B), (1, -3, 5)))
check("m_perp = -3", -1 / mAB == -3)
check("perp: 3x+y-7=0 passa por P", on_line((3, 1, -7), P))
check("perpendicularidade a1a2+b1b2=0", 1 * 3 + (-3) * 1 == 0)
F = foot(P, (1, -3, 5))
check("pé (8/5, 11/5)", F == (R(8, 5), R(11, 5)), str(F))
check("P=(1,4) NÃO é ponto médio de AB (1,2)", ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2) == (1, 2))

# ---- R4 (corrigido)
print("R4 (corrigido)")
A, B, C = (0, 1), (8, 5), (0, 6)
mAB = R(5 - 1, 8 - 0)
check("m_AB = 1/2", mAB == R(1, 2))
LAB = (1, -2, 2)  # x - 2y + 2 = 0  <=> y = x/2 + 1
check("AB: x-2y+2=0", on_line(LAB, A) and on_line(LAB, B))
H = foot(C, LAB)
check("H = (2,2)", H == (2, 2), str(H))
check("CH ⟂ AB", (C[0] - H[0]) * (B[0] - A[0]) + (C[1] - H[1]) * (B[1] - A[1]) == 0)
check("altura: y = -2x + 6", (-2 * C[0] + 6 == C[1]) and (-2 * H[0] + 6 == H[1]))
M = (S(A[0] + B[0]) / 2, S(A[1] + B[1]) / 2)
check("M = (4,3)", M == (4, 3))
check("H ≠ M", H != M)
check("CH = 2√5", simplify(dist(C, H) - 2 * sqrt(5)) == 0)
check("CH = dist(C, reta AB)", simplify(dist_pt_line(C, LAB) - 2 * sqrt(5)) == 0)
# mediatriz de AB: perpendicular por M
check("mediatriz: 2x+y-11=0 por M", on_line((2, 1, -11), M))
# mediana CM
# versão ANTIGA (C=(2,7)): altura = mediana
C0 = (2, 7)
H0 = foot(C0, LAB)
check("[versão antiga C=(2,7)] H = M = (4,3) -> descartada", H0 == M == (4, 3))

# ---- R5
print("R5")
P = (3, 4)
check("d(P,O) = 5", dist(P, (0, 0)) == 5)
check("d(P,r) = 1", dist_pt_line(P, (3, -4, 12)) == 1)
F = foot(P, (3, -4, 12))
check("pé (12/5, 24/5) na reta", F == (R(12, 5), R(24, 5)) and on_line((3, -4, 12), F), str(F))
check("|PF| = 1", dist(P, F) == 1)

# ---- R6
print("R6")
r = (3, -4, 7)
cs = solve(Eq(Abs(x - 7) / 5, 5), x)
check("c = 32 e c = -18", sorted(cs) == [-18, 32], str(cs))
for cc in (32, -18):
    # ponto de r, deslocado 5 unidades pela normal, cai na paralela
    P0 = (-1, 1)
    check(f"(-1,1) ∈ r", on_line(r, P0))
    n = (R(3, 5), R(-4, 5))
    sign = 1 if cc == -18 else -1
    Q = (P0[0] + sign * 5 * n[0], P0[1] + sign * 5 * n[1])
    check(f"3x-4y{cc:+d}=0 contém Q={Q} a distância 5", on_line((3, -4, cc), Q) and dist(P0, Q) == 5)

# ---- R7
print("R7")
r_, s_, t_ = (3, -2, 12), (1, 3, 4), (4, 1, -6)


def inter(L1, L2):
    sol = solve([L1[0] * x + L1[1] * y + L1[2], L2[0] * x + L2[1] * y + L2[2]], [x, y])
    return (sol[x], sol[y])


A = inter(r_, s_); Bp = inter(s_, t_); Cp = inter(t_, r_)
check("A = r∩s = (-4,0)", A == (-4, 0), str(A))
check("B = s∩t = (2,-2)", Bp == (2, -2), str(Bp))
check("C = t∩r = (0,6)", Cp == (0, 6), str(Cp))
# determinante (regra cíclica) - convenção: |x y 1|
Mx = Matrix([[A[0], A[1], 1], [Bp[0], Bp[1], 1], [Cp[0], Cp[1], 1]])
check("|det| = 44", abs(Mx.det()) == 44, str(Mx.det()))
check("Área = 22", abs(Mx.det()) / 2 == 22)
# soma cíclica descendo e subindo
down = A[0] * Bp[1] + Bp[0] * Cp[1] + Cp[0] * A[1]
up = A[1] * Bp[0] + Bp[1] * Cp[0] + Cp[1] * A[0]
check("cíclico: descendo=20, subindo=-24", (down, up) == (20, -24), f"{down},{up}")
# verificação alternativa: base AB sobre s, altura = d(C,s)
AB = dist(A, Bp)
h = dist_pt_line(Cp, s_)
check("alt.: ½·|AB|·d(C,s) = 22", simplify(AB * h / 2 - 22) == 0, f"|AB|={AB}, h={simplify(h)}")
check("AB ⊂ s", on_line(s_, A) and on_line(s_, Bp))

print("\n== CIRCUNFERÊNCIA ==")
# ---- C1
print("C1")
C0, Rr = (2, -3), 4
ext = [(C0[0] + Rr, C0[1]), (C0[0] - Rr, C0[1]), (C0[0], C0[1] + Rr), (C0[0], C0[1] - Rr)]
check("extremos", ext == [(6, -3), (-2, -3), (2, 1), (2, -7)], str(ext))
check("todos pertencem à circunferência", all((q[0] - 2)**2 + (q[1] + 3)**2 == 16 for q in ext))

# ---- C2
print("C2")
eq = x**2 + y**2 - 6 * x + 4 * y - 3
check("(x-3)²+(y+2)²-16 = geral", expand((x - 3)**2 + (y + 2)**2 - 16 - eq) == 0)
check("centro (3,-2)  R² = 9+4+3 = 16", (R(6, 2), R(-4, 2)) == (3, -2) and 3**2 + 2**2 + 3 == 16)

# ---- C3
print("C3")
Cc, Rr = (1, -2), 5
for name, cc, dexp, pos in [("s", 20, 3, "secante"), ("t", 30, 5, "tangente"), ("u", 40, 7, "externa")]:
    d = dist_pt_line(Cc, (3, 4, cc))
    got = "secante" if d < Rr else "tangente" if d == Rr else "externa"
    check(f"{name}: d={d} → {got}", d == dexp and got == pos)
Ft = foot(Cc, (3, 4, 30))
check("ponto de tangência de t = (-2,-6)", Ft == (-2, -6) and (Ft[0] - 1)**2 + (Ft[1] + 2)**2 == 25, str(Ft))
# número de soluções via discriminante conferindo o critério
for cc, nsol in [(20, 2), (30, 1), (40, 0)]:
    ysub = solve(Eq(3 * x + 4 * y + cc, 0), y)[0]
    q = Poly(expand((x - 1)**2 + (ysub + 2)**2 - 25), x)
    disc = discriminant(q.as_expr(), x)
    check(f"Δ de 3x+4y+{cc}=0 coerente com d (nº de interseções={nsol})",
          (disc > 0 and nsol == 2) or (disc == 0 and nsol == 1) or (disc < 0 and nsol == 0), f"Δ={disc}")

# ---- C3-teoria (pontos P,Q,R da pág. 8)
print("C3-teoria (pontos P,Q,R)")
f = lambda X, Y: (X - 1)**2 + (Y - 2)**2 - 25
check("P(4,6) pertence", f(4, 6) == 0)
check("Q(1,5) interno", f(1, 5) == -16)
check("R(7,2) externo", f(7, 2) == 11)

# ---- C4
print("C4")
sol = solve(Eq((x - 1)**2 + (6 - 2)**2, 25), x)
check("x ∈ {-2, 4}", sorted(sol) == [-2, 4], str(sol))

# ---- C5
print("C5")
Cc, P = (1, 2), (4, 6)
check("P pertence (CP=5)", dist(Cc, P) == 5)
check("tangente 3x+4y-36=0 por P", on_line((3, 4, -36), P))
check("d(C,t) = 5 = R", dist_pt_line(Cc, (3, 4, -36)) == 5)
check("raio ⟂ tangente: (3,4)·(3,4)... m_CP·m_t = -1", R(4, 3) * R(-3, 4) == -1)
# discriminante = 0
ysub = solve(Eq(3 * x + 4 * y - 36, 0), y)[0]
dd = discriminant(expand((x - 1)**2 + (ysub - 2)**2 - 25), x)
check("Δ = 0 para a tangente", dd == 0, str(dd))

# ---- C6
print("C6")
Cc, Rr = (5, 0), 4
L = (1, -2, 2)
d = dist_pt_line(Cc, L)
check("d = 7/√5", simplify(d - 7 / sqrt(5)) == 0)
corda = 2 * sqrt(Rr**2 - d**2)
check("corda = 2√155/5", simplify(corda - 2 * sqrt(155) / 5) == 0, str(simplify(corda)))
# conferir resolvendo o sistema
ys = solve(Eq((2 * y - 2 - 5)**2 + y**2, 16), y)
pts = [(2 * yy - 2, yy) for yy in ys]
check("interseções reais (2 pontos)", len(pts) == 2)
check("|AB| do sistema = 2√155/5", simplify(dist(pts[0], pts[1]) - 2 * sqrt(155) / 5) == 0)
Mc = foot(Cc, L)
check("ponto médio da corda = pé (18/5,14/5)", Mc == (R(18, 5), R(14, 5)), str(Mc))
check("R² = d² + (c/2)²", simplify(d**2 + (corda / 2)**2 - Rr**2) == 0)

# ---- C7
print("C7")
Cc, Rr, P = (6, 1), 3, (0, 4)
check("P externo: CP²=45 > 9", dist(Cc, P)**2 == 45)
sol = solve(Eq(Abs(6 * m + 3), 3 * sqrt(m**2 + 1)), m)
check("m ∈ {0, -4/3}", sorted(sol) == [R(-4, 3), 0], str(sol))
check("(6m+3)² = 9(m²+1) ⇒ 27m²+36m=0", expand((6 * m + 3)**2 - 9 * (m**2 + 1) - (27 * m**2 + 36 * m)) == 0)
check("y=4: d(C)=3", dist_pt_line(Cc, (0, 1, -4)) == 3)
check("4x+3y-12=0: d(C)=3", dist_pt_line(Cc, (4, 3, -12)) == 3)
check("ambas passam por P", on_line((0, 1, -4), P) and on_line((4, 3, -12), P))
check("x=0 NÃO é tangente (d=6≠3)", dist_pt_line(Cc, (1, 0, 0)) == 6)
T1 = foot(Cc, (0, 1, -4)); T2 = foot(Cc, (4, 3, -12))
check("tangência em (6,4) e (18/5,-4/5)", T1 == (6, 4) and T2 == (R(18, 5), R(-4, 5)), f"{T1} {T2}")
check("T1,T2 na circunferência", all((t[0] - 6)**2 + (t[1] - 1)**2 == 9 for t in (T1, T2)))

# ---- C8
print("C8")
center = (3, -1)
check("(x-3)²+(y+1)² = 10-p", expand((x - 3)**2 + (y + 1)**2 - (10 - p) - (x**2 + y**2 - 6 * x + 2 * y + p)) == 0)
d = dist_pt_line(center, (3, 4, -10))
check("d = 1", d == 1)
check("10-p = 1 ⇒ p = 9", solve(Eq(10 - p, 1), p) == [9])
ysub = (10 - 3 * x) / 4
quad = expand(16 * (x**2 + ysub**2 - 6 * x + 2 * ysub + p))
check("16·(…) = 25x²-180x+180+16p", expand(quad - (25 * x**2 - 180 * x + 180 + 16 * p)) == 0, str(quad))
disc = discriminant(25 * x**2 - 180 * x + 180 + 16 * p, x)
check("Δ = 14400-1600p", expand(disc - (14400 - 1600 * p)) == 0, str(expand(disc)))
check("Δ=0 ⇒ p=9", solve(Eq(disc, 0), p) == [9])
Ft = foot(center, (3, 4, -10))
check("ponto de tangência (18/5,-1/5)", Ft == (R(18, 5), R(-1, 5)), str(Ft))

print("\n== TEORIA (exemplos) ==")
check("diâmetro A(-1,2),B(5,6): C=(2,4), R²=13", ((-1+5)//2, (2+6)//2) == (2, 4) and R((5+1)**2 + (6-2)**2, 4) == 13 and (-1-2)**2 + (2-4)**2 == 13)
check("C(1,-1) por (4,3): R²=25", (4-1)**2 + (3+1)**2 == 25)
check("C(2,1) tangente a 3x-4y+8=0: R=2", dist_pt_line((2, 1), (3, -4, 8)) == 2)
check("x²+y²-4x=0: C=(2,0), R²=4", (R(4, 2), 0) == (2, 0) and 2**2 + 0 - 0 == 4)
check("x²+y²+6y+10=0: R²=-1 (vazio)", 0**2 + (-3)**2 - 10 == -1)
check("x²+y²-2x+4y+5=0: C=(1,-2), R²=0 (ponto)", 1**2 + (-2)**2 - 5 == 0)
check("(1,-1) em x²+y²-6x+4y-3: valor -11 = d²-R² = 5-16", (1 + 1 - 6 - 4 - 3) == -11 == ((1-3)**2 + (-1+2)**2) - 16)
check("tangência aos eixos: C=(3,-2): R=3 toca (0,-2); R=2 toca (3,0)", (0-3)**2 + (-2+2)**2 == 9 and (3-3)**2 + (0+2)**2 == 4)
check("exemplos R4-inicial: M=(3;2,5), G=(8/3,4)", ((1+5)/2, (1+4)/2) == (3, 2.5))
check("treino: m,n de 2x+4y-8, x-3y+6, 5x+y", (R(-2, 4), R(8, 4)) == (R(-1, 2), 2) and (R(1, 3), 2) == (R(1, 3), R(6, 3)) and -5 == -R(5, 1))
check("treino R5: d((1,2),(4,6))=5, |1-4|=3, 10/√5=2√5", dist((1, 2), (4, 6)) == 5 and simplify(10 / sqrt(5) - 2 * sqrt(5)) == 0)
check("p9: x²+y²=25 e y=x+7 → Δ=1, pontos (-3,4),(-4,3), d=7/√2<5", (7**2 - 4*12) == 1 and all(q[0]**2 + q[1]**2 == 25 and q[1] == q[0] + 7 for q in [(-3, 4), (-4, 3)]) and 7 / 2**0.5 < 5)
check("autoteste: (3,5); m=2; d=2", 2 * 3 - 1 == 5 and R(-4, -2) == 2 and dist_pt_line((0, 0), (3, 4, -10)) == 2)
check("3-4-5: d((1,1),(5,4)) = 5", dist((1, 1), (5, 4)) == 5)
check("baricentro formula: ((0+8+0)/3,(1+5+6)/3)=(8/3,4)", (R(8, 3), 4) == (R(0 + 8 + 0, 3), R(1 + 5 + 6, 3)))
check("normalizar: 2x²+2y²-8x+4y-10=0 → x²+y²-4x+2y-5=0 ; C=(2,-1) R=√10",
      (R(4, 2), R(2, -2)) == (2, -1) and 2**2 + (-1)**2 + 5 == 10)

print(f"\nTotal de verificações: {n_checks}; falhas: {len(fails)}")
if fails:
    print("FALHAS:", *fails, sep="\n  - ")
    sys.exit(1)
print("TODAS AS VERIFICAÇÕES PASSARAM.")
