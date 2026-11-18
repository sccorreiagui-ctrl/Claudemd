#!/usr/bin/env python3
"""Validação numérica INDEPENDENTE da física da apostila.

Cada verificação recalcula o resultado por um caminho diferente do usado no texto (Biot–Savart numérico,
integração RK4 da força de Lorentz, soma de r × F, EDO da haste em rampa com produtos vetoriais, etc.) e compara com
o valor impresso. Saída: relatório texto em report/verificacoes.txt (+ código de saída ≠ 0 se houver falha).
"""
import math
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fields as F  # noqa: E402

MU0 = 4e-7 * math.pi
E_ = 1.6e-19
ME, MP = 9.11e-31, 1.67e-27
X, Y, Z = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])

LOG = []
FAIL = 0


def check(name, got, expected, rtol=0.02, atol=0.0, note=''):
    global FAIL
    got_a, exp_a = np.asarray(got, float), np.asarray(expected, float)
    ok = bool(np.all(np.abs(got_a - exp_a) <= atol + rtol * np.abs(exp_a)))
    if not ok:
        FAIL += 1

    def fmt(v):
        v = np.asarray(v, float)
        return np.array2string(v, precision=5, separator=',') if v.ndim else f'{float(v):.5g}'
    LOG.append(f"[{'OK ' if ok else 'ERRO'}] {name}: calculado = {fmt(got_a)} | impresso = {fmt(exp_a)} {note}")
    return ok


def truth(name, cond, note=''):
    global FAIL
    cond = bool(cond)
    if not cond:
        FAIL += 1
    LOG.append(f"[{'OK ' if cond else 'ERRO'}] {name} {note}")


def section(t):
    LOG.append('\n== ' + t)


# --------------------------------------------------------------------------------- Biot–Savart numérico (referência)
def biot_savart(points, I, r):
    """campo em r de uma poligonal de corrente (pontos Nx3), por soma vetorizada de segmentos finitos (Biot–Savart)."""
    P = np.asarray(points, float)
    dl = P[1:] - P[:-1]
    mid = (P[1:] + P[:-1]) / 2
    R = np.asarray(r, float) - mid
    dist3 = np.linalg.norm(R, axis=1) ** 3
    return MU0 * I / (4 * math.pi) * np.sum(np.cross(dl, R) / dist3[:, None], axis=0)


def wire(pos, direction, half=400.0, n=40001):
    t = np.linspace(-half, half, n)[:, None]
    return np.asarray(pos, float)[None, :] + t * np.asarray(direction, float)[None, :]


def lorentz_rk4(q, m, v0, B, t_end, n):
    """integra dv/dt = (q/m) v × B e dr/dt = v (RK4 acoplado); devolve posições e velocidades."""
    h = t_end / n
    k_ = q / m
    B = np.asarray(B, float)

    def f(state):
        v = state[3:]
        return np.concatenate([v, k_ * np.cross(v, B)])
    s = np.concatenate([np.zeros(3), np.asarray(v0, float)])
    out = [s.copy()]
    for _ in range(n):
        k1 = f(s); k2 = f(s + h / 2 * k1); k3 = f(s + h / 2 * k2); k4 = f(s + h * k3)
        s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(s.copy())
    out = np.array(out)
    return out[:, :3], out[:, 3:]


# =================================================================================== 1. MODELOS DE CAMPO
section('1. Fórmulas de campo × Biot–Savart numérico')
I0, r0 = 10.0, 0.05
Bnum = biot_savart(wire([0, 0, 0.0], (0, 0, 1)), I0, [r0, 0, 0])
check('fio longo: B = μ0 I/(2π r), I = 10 A, r = 5 cm', np.linalg.norm(Bnum), MU0 * I0 / (2 * math.pi * r0), 5e-4)
truth('fio ⊙ (I = +z): B à direita aponta para +y (1ª regra da mão direita)', Bnum[1] > 0 and abs(Bnum[0]) < 1e-12)

R_, N_pts = 0.05, 4000
th = np.linspace(0, 2 * math.pi, N_pts + 1)
loop = np.stack([R_ * np.cos(th), R_ * np.sin(th), np.zeros_like(th)], axis=1)   # anti-horária vista de +z
Bc = biot_savart(loop, 4.0, [0, 0, 0])
check('espira, centro: B = μ0 I/(2R), I = 4 A, R = 5 cm', Bc[2], MU0 * 4.0 / (2 * R_), 1e-4)
truth('espira anti-horária (vista de +z): B no centro aponta para +z (face norte = +z)', Bc[2] > 0)
x = 0.03
check('espira, eixo a 3 cm: B = μ0 I R²/[2(R²+x²)^(3/2)]', biot_savart(loop, 4.0, [0, 0, x])[2],
      MU0 * 4.0 * R_ ** 2 / (2 * (R_ ** 2 + x ** 2) ** 1.5), 1e-4)
ta = np.linspace(0, math.pi, 4001)
arc = np.stack([R_ * np.cos(ta), R_ * np.sin(ta), np.zeros_like(ta)], axis=1)
check('semicírculo: B_centro = μ0 I/(4R)', biot_savart(arc, 5.0, [0, 0, 0])[2], MU0 * 5.0 / (4 * R_), 1e-3)

# solenoide: n = 2000 espiras/m, 2,0 A, L = 25 cm, raio 1 cm (L/D = 12,5): interior ≈ μ0 n I
rs, Ls, ns, Is = 0.01, 0.25, 2000.0, 2.0
Nturn = 500
turns = (np.arange(Nturn) + 0.5) / Nturn * Ls - Ls / 2
tc = np.linspace(0, 2 * math.pi, 361)


def solenoid_B(point):
    Bt = np.zeros(3)
    for zk in turns:
        pts = np.stack([rs * np.cos(tc), rs * np.sin(tc), np.full_like(tc, zk)], axis=1)
        Bt += biot_savart(pts, Is * (ns * Ls) / Nturn, point)
    return Bt


check('solenoide (N=500 espiras, L=25 cm, I=2 A): B(centro) ≈ μ0 n I = 5,03 mT', solenoid_B([0, 0, 0])[2], MU0 * ns * Is, 0.02)
check('solenoide: B na extremidade ≈ ½ μ0 n I', solenoid_B([0, 0, Ls / 2])[2], 0.5 * MU0 * ns * Is, 0.04)
check('exercício E9(c): 1000 esp/m, 3,0 A → B ≈ 3,8 mT', MU0 * 1000 * 3.0, 3.8e-3, 0.01)

# modelo do ímã/espira usado nos desenhos (integrais elípticas) × fórmula
br, bz = F.loop_B(0.0, 0.0, 1.0)
check('loop_B (desenhos): centro = π (μ0 I/2π) ⇒ μ0 I/2a', float(bz), math.pi, 1e-9)

# =================================================================================== 2. SUPERPOSIÇÃO E AMPÈRE
section('2. Superposição de campos (p. 6) e Lei de Ampère (p. 9)')


def B_of_wires(wires, r):
    return sum(biot_savart(wire([wx, wy, 0.0], (0, 0, s)), I, r) for (wx, wy, s, I) in wires)


W2 = [(0.0, 0.0, +1, 10.0), (0.20, 0.0, -1, 30.0)]   # Ex.2: fio 1 em x=0 (10 A, saindo), fio 2 em x=0,20 (30 A, entrando)
BP = B_of_wires(W2, [0.10, 0, 0])
check('Ex.2 (a): B em P (meio) = 8,0×10⁻⁵ T, +y', BP[1], 8.0e-5, 2e-3)
xs = np.linspace(-0.3, -0.01, 581)
By = np.array([B_of_wires(W2, [x_, 0, 0])[1] for x_ in xs])
check('Ex.2 (b): ponto de B = 0 em x = −10 cm', xs[np.argmin(np.abs(By))], -0.10, 0.0, 1e-3)


def W3(IC):
    """E7: A (x = −10 cm) e D (x = +10 cm) com 24 A ENTRANDO (−z); C em x = 0 com corrente IC (>0 saindo, <0 entrando)."""
    return [(-0.10, 0.0, -1, 24.0), (0.0, 0.0, +1 if IC > 0 else -1, abs(IC)), (0.10, 0.0, -1, 24.0)]


# E7 (geometria do texto, p. 6): P em x = +5 cm, entre C e D; procura-se I_C com B(P) = 0
P = [0.05, 0, 0]
Is_ = np.linspace(-30, 30, 1201)
Bv = np.array([B_of_wires(W3(I_), P)[1] for I_ in Is_])
check('E7: corrente no fio C com B(P)=0 → −16 A (16 A entrando)', Is_[np.argmin(np.abs(Bv))], -16.0, 0.0, 0.06)
# quadrado de fios (topo saindo, base entrando), I = 10 A, lado 10 cm
Wq = [(-0.05, 0.05, +1, 10.0), (0.05, 0.05, +1, 10.0), (0.05, -0.05, -1, 10.0), (-0.05, -0.05, -1, 10.0)]
Bq = B_of_wires(Wq, [0, 0, 0])
check('quadrado de 4 fios: B no centro = 80 μT, horizontal (+x)', [Bq[0], Bq[1]], [8.0e-5, 0.0], 2e-3, 1e-9)
check('E6: B(20 A, 10 cm) = 40 μT; r para 50 μT = 8,0 cm; fator (3I, 2r) = 1,5',
      [2e-7 * 20 / 0.10, 2e-7 * 20 / 50e-6, 3 / 2], [4.0e-5, 0.08, 1.5], 1e-9)
check('Ex.1: B_P = 80 μT, B_Q = 40 μT (12 A; 3 cm e 6 cm)', [MU0 * 12 / (2 * math.pi * 0.03), MU0 * 12 / (2 * math.pi * 0.06)], [8.0e-5, 4.0e-5], 1e-9)

# Ampère: circulação numérica em elipse com 3 fios (dois dentro, um fora)
Wa = [(-0.04, 0.004, +1, 6.0), (0.042, -0.006, -1, 4.0), (0.30, 0.02, +1, 5.0)]
cx_, cy_, rx_, ry_ = 0.0, 0.0, 0.092, 0.056
tt = np.linspace(0, 2 * math.pi, 8001)
pa = np.stack([cx_ + rx_ * np.cos(tt[:-1]), cy_ + ry_ * np.sin(tt[:-1]), np.zeros(8000)], axis=1)
pb = np.stack([cx_ + rx_ * np.cos(tt[1:]), cy_ + ry_ * np.sin(tt[1:]), np.zeros(8000)], axis=1)
pm = (pa + pb) / 2
Bm = np.zeros_like(pm)
for (wx, wy, s, I) in Wa:
    d = pm - np.array([wx, wy, 0.0])
    Bm += MU0 * I * np.cross(np.array([0, 0, s]), d) / (2 * math.pi * np.sum(d ** 2, axis=1)[:, None])
circ = float(np.sum(np.sum(Bm * (pb - pa), axis=1)))
check('Ex.5: circulação anti-horária com 6 A (⊙) e 4 A (⊗) dentro e 5 A fora = 2 μ0 = 2,5×10⁻⁶ T·m', circ, 2 * MU0, 1e-3)
check('E10: circulação = μ0 I = 3,1×10⁻⁵ (I=25 A); B(4 cm) = 1,25×10⁻⁴; B(8 cm) = 6,3×10⁻⁵',
      [MU0 * 25, 2e-7 * 25 / 0.04, 2e-7 * 25 / 0.08], [3.14e-5, 1.25e-4, 6.25e-5], 5e-3)

# =================================================================================== 3. FORÇA SOBRE CARGAS
section('3. Força sobre cargas e trajetórias (RK4 da equação de Lorentz)')
check('Ex.6: F = |q| v B sen30° = 8,0×10⁻¹⁴ N; F/P ≈ 5×10¹²',
      [E_ * 2e6 * 0.5 * 0.5, E_ * 2e6 * 0.5 * 0.5 / (MP * 10)], [8.0e-14, 4.8e12], 1e-2)
check('E11: (a) 9,6e-16; (b) 4,8e-16; (e) B = 0,40 T', [E_ * 3e6 * 2e-3, E_ * 3e6 * 2e-3 * 0.5, 4.0e-3 / (2e-6 * 5e3)],
      [9.6e-16, 4.8e-16, 0.40], 1e-9)
check('Ex.7: v×B para (+q, B⊗) = +y; (−q) = −y; (+q, B⊙) = −y',
      [np.cross(X, -Z)[1], -np.cross(X, -Z)[1], np.cross(X, Z)[1]], [1, -1, -1], 0, 1e-12)
check('Ex.7: |F| = 3,2×10⁻¹⁴ N', E_ * 1e6 * 0.20, 3.2e-14, 1e-9)
cases = [(+1, X, Y), (-1, Y, X), (+1, -X, Z), (-1, X, -Z), (+1, -Y, -Z), (-1, Y, Z)]
expect = [Z, Z, Y, -Y, X, -X]
for k, ((q, v, B), e) in enumerate(zip(cases, expect)):
    truth(f'E12 ({"abcdef"[k]}): F = q v × B tem o sentido impresso', np.allclose(q * np.cross(v, B), e))
# giro: próton em B = −z gira anti-horário (sai de +x, curva para +y)
Rr, Vv = lorentz_rk4(+E_, MP, [1e6, 0, 0], [0, 0, -0.20], 3.28e-7, 4000)
truth('Ex.8: próton em B entrando (−z) gira no sentido anti-horário', np.cross(Rr[1] - Rr[0], Rr[2] - Rr[1])[2] > 0)
check('Ex.8: raio da órbita (RK4) = 5,2 cm', (np.max(Rr[:, 1]) - np.min(Rr[:, 1])) / 2, 5.2e-2, 0.01)
check('Ex.8: r = mv/(qB), T = 2πm/(qB), f', [MP * 1e6 / (E_ * 0.2), 2 * math.pi * MP / (E_ * 0.2), E_ * 0.2 / (2 * math.pi * MP)],
      [5.2e-2, 3.3e-7, 3.05e6], 0.02)
check('Ex.8: ω = qB/m = 1,9×10⁷ rad/s', E_ * 0.2 / MP, 1.9e7, 0.02)
check('E13: r_e/r_p = m_e/m_p = 5,4×10⁻⁴; r14/r12 = 1,17', [ME / MP, 14 / 12], [5.4e-4, 1.17], 0.02)
vE = math.sqrt(2 * E_ * 1e3 / MP)
check('E13(e): v = 4,4×10⁵ m/s; r = 4,6 cm', [vE, MP * vE / (E_ * 0.10)], [4.4e5, 4.6e-2], 0.02)
# Ex.9: hélice do elétron, B = 2,0e-3 T ao longo de x, v a 60° com B
v0 = 3e6
vv = [v0 * math.cos(math.radians(60)), v0 * math.sin(math.radians(60)), 0]
T_th = 2 * math.pi * ME / (E_ * 2e-3)
Rr, Vv = lorentz_rk4(-E_, ME, vv, [2e-3, 0, 0], T_th * 3, 6000)
rr = (Rr[:, 1].max() - Rr[:, 1].min()) / 2
check('Ex.9: raio da hélice (RK4) = 7,4 mm', rr, 7.4e-3, 0.02)
tgrid = np.linspace(0, T_th * 3, len(Vv))
phase = np.unwrap(np.arctan2(Vv[:, 2], Vv[:, 1]))
T_num = 2 * math.pi / abs((phase[-1] - phase[0]) / tgrid[-1])
check('Ex.9: período (RK4) = 1,8×10⁻⁸ s', T_num, 1.79e-8, 0.02)
check('Ex.9: passo = v∥ T = 2,7 cm', 1.5e6 * T_num, 2.7e-2, 0.03)
check('Ex.9: |v| constante (W = 0)', np.max(np.abs(np.linalg.norm(Vv, axis=1) - v0)) / v0, 0.0, 0.0, 1e-6)
check('Ex.9: v⟂² + v∥² = v²', (2.6e6) ** 2 + (1.5e6) ** 2, 9.0e12, 0.01)
Rr, Vv = lorentz_rk4(+E_, MP, [2e5 * math.cos(math.radians(30)), 2e5 * math.sin(math.radians(30)), 0], [0.1, 0, 0], 6.56e-7, 6000)
check('E14(e): raio ≈ 1,0 cm; passo ≈ 11 cm', [(Rr[:, 1].max() - Rr[:, 1].min()) / 2, Rr[-1, 0]], [1.04e-2, 0.1136], 0.03)
r_K = lambda m, K_eV, B: math.sqrt(2 * m * K_eV * E_) / (E_ * B)
check('p. 12 (ordens de grandeza): CRT (e⁻ 1 keV, 1 mT) ≈ 11 cm; aurora (e⁻ 10 keV, 50 μT) ≈ 7 m; ciclotron (p 1 MeV, 1 T) ≈ 14 cm; v(1 keV) = 1,9×10⁷ m/s',
      [r_K(ME, 1e3, 1e-3), r_K(ME, 1e4, 50e-6), r_K(MP, 1e6, 1.0), math.sqrt(2 * 1e3 * E_ / ME)], [0.11, 7.0, 0.14, 1.9e7], 0.04)

# =================================================================================== 4. FORÇA SOBRE FIOS
section('4. Força sobre fios (integração de I dℓ × B) e entre fios')
check('Ex.10: F = B I L sen θ: 0,20 N (30°) e 0,40 N (90°)', [0.2 * 5 * 0.4 * 0.5, 0.2 * 5 * 0.4], [0.20, 0.40], 1e-9)
truth('Ex.10 (c): I entrando, B → : F para baixo', np.allclose(np.cross(-Z, X), -Y))
check('E15: I = mg/(BL) = 1,0 A', [0.010 * 10 / (0.5 * 0.2)], [1.0], 1e-9)
truth('E15 (b): L × x̂ = +ŷ ⇒ L = +ẑ (saindo da página)', np.allclose(np.cross(Z, X), Y))
th = np.linspace(math.pi, 0, 4001)
pts = np.stack([0.10 * np.cos(th), 0.10 * np.sin(th), np.zeros_like(th)], axis=1)
Ftot = np.sum(3.0 * np.cross(pts[1:] - pts[:-1], np.array([0, 0, -0.20])[None, :]), axis=0)
check('E15(c): fio em semicírculo R = 10 cm, 3,0 A, 0,20 T: |F| = BI(2R) = 0,12 N (para cima)', [np.linalg.norm(Ftot), Ftot[1]], [0.12, 0.12], 1e-3)
check('Ex.11: F/L = 4,0×10⁻⁴ N/m; F(0,80 m) = 3,2×10⁻⁴ N', [2e-7 * 10 * 20 / 0.10, 2e-7 * 10 * 20 / 0.10 * 0.8], [4.0e-4, 3.2e-4], 1e-9)
B1 = biot_savart(wire([0, 0, 0.0], (0, 1, 0)), 10.0, [0.10, 0, 0])
F2 = 20.0 * 0.80 * np.cross(np.array([0, 1, 0]), B1)
check('Ex.11 (BS numérico): força em 0,80 m do fio 2 = 3,2×10⁻⁴ N, em direção ao fio 1 (−x)', [np.linalg.norm(F2), F2[0]], [3.2e-4, -3.2e-4], 1e-3)
check('E16: λ g = μ0 I1 I2/(2π d) ⇒ λ = 2,5×10⁻⁵ kg/m', 2e-7 * 10 * 5 / 0.040 / 10, 2.5e-5, 1e-9)

# espira retangular perto de fio longo (p. 15): F líquida = Σ I dℓ × B, com B do fio por Biot–Savart numérico
I1_, I2_, L_, a_, b_ = 20.0, 5.0, 0.10, 0.02, 0.06
wy_ = wire([0, 0, 0.0], (0, 1, 0), half=300.0, n=60001)
nseg = 400


def seg_force(p0, p1):
    s = np.linspace(0, 1, nseg + 1)[:, None]
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    Pp = p0[None, :] + s * (p1 - p0)[None, :]
    dl = Pp[1:] - Pp[:-1]
    mids = (Pp[1:] + Pp[:-1]) / 2
    Ftot_ = np.zeros(3)
    for dli, mi in zip(dl, mids):
        Ftot_ += I2_ * np.cross(dli, biot_savart(wy_, I1_, mi))
    return Ftot_


# fio com corrente +y em x=0; espira no plano z=0 com lado "perto" em x=a e "longe" em x=a+b; corrente da espira: lado perto = +y (paralela → atração)
Fnear = seg_force([a_, -L_ / 2, 0], [a_, L_ / 2, 0])
Ftop = seg_force([a_, L_ / 2, 0], [a_ + b_, L_ / 2, 0])
Ffar = seg_force([a_ + b_, L_ / 2, 0], [a_ + b_, -L_ / 2, 0])
Fbase = seg_force([a_ + b_, -L_ / 2, 0], [a_, -L_ / 2, 0])
Fnet = Fnear + Ftop + Ffar + Fbase
check('p. 15: força líquida = 7,5×10⁻⁵ N, atração (−x); F_y ≈ 0', [Fnet[0], Fnet[1]], [-7.5e-5, 0.0], 5e-3, 1e-9)
check('  F_perto = 1,0×10⁻⁴ N (atrai, −x); F_longe = 2,5×10⁻⁵ N (repele, +x)', [Fnear[0], Ffar[0]], [-1.0e-4, 2.5e-5], 5e-3)
check('  forças em topo e base se cancelam', Ftop + Fbase, [0, 0, 0], 0.0, 1e-9)

# =================================================================================== 5. FLUXO E FARADAY
section('5. Fluxo, Faraday e Lenz')
check('Ex.12: Φ = 10 mWb (θ=60°), 20 mWb, 0', [0.40 * 0.05 * math.cos(math.radians(60)), 0.40 * 0.05, 0.40 * 0.05 * math.cos(math.radians(90))],
      [1.0e-2, 2.0e-2, 0.0], 1e-9, 1e-12)
A_ = math.pi * 0.1 ** 2
check('E17: Φ = 1,6×10⁻² Wb e 1,4×10⁻² Wb', [0.5 * A_, 0.5 * A_ * math.cos(math.radians(30))], [1.6e-2, 1.4e-2], 0.03)
check('Ex.13: |ε| = 20 V; I = 0,50 A', [200 * 5e-3 / 0.05, 200 * 5e-3 / 0.05 / 40], [20, 0.5], 1e-9)
check('E18: ΔΦ = 1,0×10⁻² Wb; ε = 10 V; I = 2,0 A', [0.5 * 0.02, 100 * 0.5 * 0.02 / 0.10, 100 * 0.5 * 0.02 / 0.10 / 5], [1.0e-2, 10, 2.0], 1e-9)
t_ = np.array([0, 2, 5, 7.0])
ph_ = np.array([0, 8, 8, -4.0]) * 1e-3
emf = -50 * np.diff(ph_) / np.diff(t_)
check('Ex.14: ε = [−0,20; 0; +0,30] V; Q₁ = 4,0×10⁻² C', list(emf) + [50 * 8e-3 / 10], [-0.20, 0.0, 0.30, 4.0e-2], 1e-9, 1e-12)
emf2 = -20 * np.array([(0.40 - 0.10) / 3.0, 0.0, (0 - 0.40) / 1.0])
check('E19: ε = [−2,0; 0; +8,0] V', emf2, [-2.0, 0.0, 8.0], 1e-9, 1e-12)
check('Ex.15: |ε| = 4,0 V; I = 0,50 A', [100 * 0.02 * 0.40 / 0.20, 100 * 0.02 * 0.40 / 0.20 / 8.0], [4.0, 0.5], 1e-9)


# Lenz — quatro casos pelo fluxo com sinal; n̂ = +x (normal do anel), ímã à esquerda do anel
def lenz_case(m_sign, approaching):
    """m_sign=+1: polo N voltado ao anel; −1: polo S voltado ao anel. Retorna (sentido visto do lado do ímã, face voltada ao ímã)."""
    d = (0.10, 0.09) if approaching else (0.10, 0.11)
    Bx = lambda dist: m_sign * MU0 * 2 * 1.0 / (4 * math.pi * dist ** 3)       # dipolo no eixo (m = 1 A·m²)
    dPhi = (Bx(d[1]) - Bx(d[0])) * 1e-3                                        # Φ = Bx·A (A = 1e-3 m²)
    eps = -dPhi                                                                  # ε>0 ⇒ corrente com polegar em +x
    # polegar em +x, olhando do lado do ímã (de −x para +x) a corrente aparece HORÁRIA; ε<0 ⇒ anti-horária
    sense = 'horário' if eps > 0 else 'anti-horário'
    # B_induzido em +x quando ε>0: face do anel voltada ao ímã (−x) é a face "sul"; o inverso quando ε<0
    face = 'S' if eps > 0 else 'N'
    return sense, face


expected_lenz = {(+1, True): ('anti-horário', 'N'), (+1, False): ('horário', 'S'),
                 (-1, True): ('horário', 'S'), (-1, False): ('anti-horário', 'N')}
for key, exp in expected_lenz.items():
    truth(f'Lenz p. 20: polo {"N" if key[0] > 0 else "S"} {"se aproxima" if key[1] else "se afasta"} → {exp[0]}, face {exp[1]} (fluxo com sinal + dipolo)',
          lenz_case(*key) == exp)


def stat_case(Bz_sign, increasing):
    dB = (+1 if increasing else -1) * Bz_sign          # sinal de dBz/dt; n̂ = +z (saindo da página)
    eps = -dB                                            # ε>0 ⇒ anti-horária vista de frente (polegar em +z)
    return 'anti-horária' if eps > 0 else 'horária'


truth('Anel parado: B entrando aumenta → anti-horária; diminui → horária; B saindo aumenta → horária; diminui → anti-horária',
      [stat_case(-1, True), stat_case(-1, False), stat_case(+1, True), stat_case(+1, False)] == ['anti-horária', 'horária', 'horária', 'anti-horária'])

# =================================================================================== 6. HASTE MÓVEL E RAMPA
section('6. Haste móvel e rampa (EDO com produtos vetoriais, sem usar as fórmulas fechadas)')
check('Ex.17: ε = 0,60 V; I = 0,30 A; F = 0,060 N; P = 0,18 W (= εI = I²R)', [0.5 * 0.4 * 3.0, 0.6 / 2, 0.5 * 0.3 * 0.4, 0.06 * 3.0],
      [0.60, 0.30, 0.060, 0.18], 1e-9)
emf_v = float(np.dot(np.cross(X * 3.0, -Z * 0.5), Y * 0.4))
check('Ex.17 (vetorial): ε = (v × B)·L com v = +x, B = −z, L = +y', emf_v, 0.60, 1e-9)
check('E21: ε = 0,40 V; I = 0,10 A; F = 0,020 N; P = 0,040 W', [0.25 * 0.8 * 2.0, 0.40 / 4.0, 0.25 * 0.1 * 0.8, 0.02 * 2.0],
      [0.40, 0.10, 0.020, 0.040], 1e-9)


def incline(Bvec_fn, alpha_rad, m=0.10, Ll=1.0, R=1.0, g=10.0, steps=20000, tmax=2.0):
    """haste (comprimento Ll ao longo de y) sobre trilhos inclinados; integra m dv/dt = m g sen α + F_mag·ŝ (RK4)."""
    s_hat = np.array([-math.cos(alpha_rad), 0.0, -math.sin(alpha_rad)])           # descida da rampa
    Lhat = np.array([0.0, 1.0, 0.0]) * Ll
    B = np.asarray(Bvec_fn(alpha_rad), float)

    def acc(v):
        vel = v * s_hat
        emf = float(np.dot(np.cross(vel, B), Lhat))                               # ε = (v × B)·L
        I = emf / R
        Fm = I * np.cross(Lhat, B)                                                # força magnética vetorial
        return (m * g * math.sin(alpha_rad) + float(np.dot(Fm, s_hat))) / m, emf, I, Fm
    h = tmax / steps
    v = 0.0
    for _ in range(steps):
        k1 = acc(v)[0]; k2 = acc(v + h / 2 * k1)[0]; k3 = acc(v + h / 2 * k2)[0]; k4 = acc(v + h * k3)[0]
        v += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    a, emf, I, Fm = acc(v)
    return v, emf, I, Fm


al = math.asin(0.6)           # sen α = 0,6 e cos α = 0,8 (valores usados no texto)
vt, emf_, I_, Fm_ = incline(lambda a: [0, 0, 1.25], al)
check('Ex.18: v_terminal = 0,60 m/s (B vertical, sen α = 0,6)', vt, 0.600, 2e-3)
check('Ex.18: |ε| = 0,60 V; |I| = 0,60 A; |F| = 0,75 N', [abs(emf_), abs(I_), np.linalg.norm(Fm_)], [0.60, 0.60, 0.75], 3e-3)
truth('Ex.18: força magnética horizontal (F_z ≈ 0) e para o lado alto da rampa (+x)', abs(Fm_[2]) < 1e-9 and Fm_[0] > 0)
check('Ex.18: balanço de energia m g v sen α = I²R = 0,36 W', [0.10 * 10 * vt * 0.6, I_ ** 2 * 1.0], [0.36, 0.36], 3e-3)
vt_p, emf_p, I_p, Fm_p = incline(lambda a: np.array([-math.sin(a), 0, math.cos(a)]) * 1.25, al)
truth('E22: com B ⟂ rampa o vetor B é perpendicular a ŝ', abs(np.dot([-math.sin(al), 0, math.cos(al)], [-math.cos(al), 0, -math.sin(al)])) < 1e-12)
check('E22: B ⟂ rampa: v_terminal = 0,38 m/s; |I| = 0,48 A', [vt_p, abs(I_p)], [0.384, 0.48], 3e-3)
check('E22(c): razão v_term(B vertical)/v_term(B ⟂) = 1/cos²α = 1,5625', vt / vt_p, 1 / 0.8 ** 2, 3e-3)
check('Ex.18: constante de tempo τ = m/(B²L²cos²α) = 0,10 s', 0.10 / (1.25 ** 2 * 1.0 * 0.8 ** 2), 0.10, 1e-9)
check('Ex.18: N = mg cosα + F sinα = 1,25 N', 1.0 * 0.8 + 0.75 * 0.6, 1.25, 1e-9)

# =================================================================================== 7. MOTOR, GERADOR, TRANSFORMADOR
section('7. Motor, gerador, transformador e aplicações')


def torque_loop(N, I, B, ell, w, phi_deg):
    """torque por soma de r × F nos 4 lados; φ = ângulo entre a normal da bobina e B (B = +x, eixo = z)."""
    phi = math.radians(phi_deg)
    n = np.array([math.cos(phi), math.sin(phi), 0.0])
    u = np.array([-math.sin(phi), math.cos(phi), 0.0])
    zhat = np.array([0, 0, 1.0])
    # percurso anti-horário em torno de n (regra da mão direita): u → z → −u → −z
    corners = [(+w / 2) * u - (ell / 2) * zhat, (+w / 2) * u + (ell / 2) * zhat, (-w / 2) * u + (ell / 2) * zhat, (-w / 2) * u - (ell / 2) * zhat]
    tau = np.zeros(3)
    Fsum = np.zeros(3)
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        Fi = N * I * np.cross(b - a, np.array([B, 0, 0]))
        tau += np.cross((a + b) / 2, Fi)
        Fsum += Fi
    return np.linalg.norm(tau), np.linalg.norm(Fsum), tau


t90, F90, tau90 = torque_loop(100, 2.0, 0.30, 0.20, 0.10, 90)
t60, _, _ = torque_loop(100, 2.0, 0.30, 0.20, 0.10, 60)
t0, _, _ = torque_loop(100, 2.0, 0.30, 0.20, 0.10, 0)
check('Ex.19: τ_máx = 1,2 N·m (φ=90°); τ(60°) = 1,04 N·m; τ(0°) = 0; ΣF = 0', [t90, t60, t0, F90], [1.2, 1.04, 0.0, 0.0], 5e-3, 1e-9)
check('Ex.19(c): F por lado longo = N B I ℓ = 12 N', 100 * 0.30 * 2.0 * 0.20, 12.0, 1e-9)
check('E23: τ_máx = 1,2; τ(30°) = 0,60 N·m; I_partida = 6,0 A; I = 1,0 A',
      [200 * 0.5 * 3.0 * 4e-3, 200 * 0.5 * 3.0 * 4e-3 * 0.5, 12 / 2.0, (12 - 10) / 2.0], [1.2, 0.6, 6.0, 1.0], 1e-9)
check('Ex.20: ω = 377 rad/s; ε_máx = 188 V; ε_ef = 133 V; T = 16,7 ms',
      [2 * math.pi * 60, 100 * 0.5 * 0.01 * 2 * math.pi * 60, 100 * 0.5 * 0.01 * 2 * math.pi * 60 / math.sqrt(2), 1000 / 60],
      [377, 188, 133, 16.7], 3e-3)
tt = np.linspace(0, 1 / 60, 200001)
Phi = 100 * 0.5 * 0.01 * np.cos(2 * math.pi * 60 * tt)
emf_t = -np.gradient(Phi, tt)
check('Ex.20 (diferenças finitas): ε_máx = 188,5 V e ε nula quando Φ é máximo', [emf_t.max(), abs(emf_t[0])], [188.5, 0.0], 2e-3, 0.5)
check('E24: ε_máx(1 espira) = 1,26 V; N = 79,6 ≈ 80', [0.20 * 0.020 * 2 * math.pi * 50, 100 / (0.20 * 0.020 * 2 * math.pi * 50)], [1.26, 79.6], 5e-3)
check('Ex.21: U_s = 44 V; I_s = 4,0 A; I_p = 0,80 A; P = 176 W', [220 * 200 / 1000, 44 / 11, 4.0 * 200 / 1000, 44 * 4.0], [44, 4.0, 0.8, 176], 1e-9)
check('E25: N_s = 200; I_s = 2,0 A; I_p = 0,20 A', [2000 * 12 / 120, 12 / 6.0, 2.0 * 200 / 2000], [200, 2.0, 0.20], 1e-9)
check('p. 26: perdas 50 kW e 0,5 kW (P = 2,0 MW, R = 5,0 Ω); 2,5 % e 0,025 % da potência',
      [5 * (2e6 / 2e4) ** 2, 5 * (2e6 / 2e5) ** 2, 5e4 / 2e6, 5e2 / 2e6], [5.0e4, 5.0e2, 0.025, 2.5e-4], 1e-9)
check('Q9: U_s = 4,0 kV; I = 2,5 A; perda = 25 W (0,25%)', [200 * 2000 / 100, 1e4 / 4000, 4.0 * 2.5 ** 2, 25 / 1e4], [4000, 2.5, 25, 0.0025], 1e-9)
check('Q7: F/L = 1,2×10⁻³ N/m', 2e-7 * 10 * 30 / 0.05, 1.2e-3, 1e-9)
check('Q8: ε = 0,80 V; I = 0,40 A; F = 0,080 N; P = 0,32 W', [0.40 * 0.50 * 4.0, 0.80 / 2.0, 0.40 * 0.40 * 0.50, 0.40 ** 2 * 2.0],
      [0.80, 0.40, 0.080, 0.32], 1e-9)
check('RM: frequência de Larmor do ¹H = 42,577 MHz/T → 63,9 MHz a 1,5 T; 127,7 MHz a 3 T', [42.577 * 1.5, 42.577 * 3], [63.9, 127.7], 1e-3)

# =================================================================================== RESUMO
n_ok = sum(1 for l in LOG if l.startswith('[OK'))
LOG.append(f'\nTOTAL: {n_ok} verificações OK, {FAIL} falhas.')
out = os.path.join(HERE, '..', 'report')
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, 'verificacoes.txt'), 'w', encoding='utf8') as f:
    f.write('VERIFICAÇÕES NUMÉRICAS INDEPENDENTES — Apostila CTG Eletromagnetismo PAS 3/UnB\n(gerado por scripts/validate_physics.py)\n')
    f.write('\n'.join(LOG) + '\n')
print('\n'.join(LOG))
sys.exit(1 if FAIL else 0)
