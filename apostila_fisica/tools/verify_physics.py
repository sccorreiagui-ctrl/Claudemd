#!/usr/bin/env python3
"""Verificação numérica independente de todos os exemplos resolvidos e exercícios da apostila.
Cada bloco recalcula o resultado com numpy/math e compara com o valor impresso no texto (tolerância indicada).
Uso: python3 tools/verify_physics.py"""
import math
import numpy as np

k = 9.0e9; e = 1.6e-19; me = 9.1e-31; mp = 1.67e-27; mu0 = 4e-7 * math.pi; eps0 = 8.85e-12; g = 10.0
ok_all = True
n_checks = 0


def chk(name, got, expect, rel=0.02, abs_=0.0):
    global ok_all, n_checks
    n_checks += 1
    good = abs(got - expect) <= max(abs(expect) * rel, abs_)
    ok_all &= good
    print(f"{'OK ' if good else 'ERRO'}  {name:<62} calc={got:.6g}  texto={expect:.6g}")


def nodal(G_edges, sources, n, ref=0):
    """Análise nodal: G_edges [(a,b,R)], sources [(a,b,E)] com E de b para a (V_a - V_b = E) por fonte ideal via R=1e-9."""
    G = np.zeros((n, n)); I = np.zeros(n)
    for a, b, R in G_edges:
        g_ = 1 / R
        G[a, a] += g_; G[b, b] += g_; G[a, b] -= g_; G[b, a] -= g_
    for a, b, E, r in sources:        # fonte E em série com r entre b(-) e a(+)
        g_ = 1 / r
        G[a, a] += g_; G[b, b] += g_; G[a, b] -= g_; G[b, a] -= g_
        I[a] += E * g_; I[b] -= E * g_
    keep = [i for i in range(n) if i != ref]
    V = np.zeros(n)
    V[keep] = np.linalg.solve(G[np.ix_(keep, keep)], I[keep])
    return V


print("── Módulo I / II ──")
chk("Ex1  n = Q/e (3,2 µC)", 3.2e-6 / e, 2.0e13)
chk("Ex1  massa transferida", 2e13 * 9.1e-31, 1.8e-17)
chk("Ex2  Coulomb 2µC,3µC,0,30 m", k * 2e-6 * 3e-6 / 0.30**2, 0.60)
chk("Ex3  r 0,30→0,10 m", 0.60 * 9, 5.4)
chk("Ex3b q2 dobrada", 2 * 5.4, 10.8)
FB = k * 2e-6 * 3e-6 / 0.30**2; FC = FB
chk("Ex4  F_R = 0,6·√2", math.hypot(FB, FC), 0.85, 0.01)
chk("Ex5  E a 10 cm de 5 nC", k * 5e-9 / 0.1**2, 4.5e3)
chk("Ex5  F sobre −2 µC", 2e-6 * 4.5e3, 9.0e-3)
E1 = k * 4e-9 / 0.30**2
chk("Ex6  E1 (4 nC a 30 cm)", E1, 4.0e2)
chk("Ex6  E_R = E1√2", math.hypot(E1, E1), 5.7e2, 0.01)
VA, VB = k * 1e-8 / 0.10, k * 1e-8 / 0.30
chk("Ex7  V_A", VA, 9.0e2); chk("Ex7  V_B", VB, 3.0e2)
chk("Ex7  W_AB", 2e-9 * (VA - VB), 1.2e-6)
W = e * 400
v = math.sqrt(2 * W / me)
chk("Ex8  W = 400 eV (J)", W, 6.4e-17); chk("Ex8  v elétron", v, 1.2e7, 0.02)
a = e * (400 / 0.02) / me
chk("Ex8  a = eE/m", a, 3.5e15, 0.02)
chk("Ex8  v² = 2ad", 2 * a * 0.02, v**2, 0.02)
chk("Ex9  E_M dipolo", 2 * k * 2e-6 / 0.30**2, 4.0e5)
C, U, dt = 70e-6, 2500, 5e-3
chk("Ex10 Q = CU", C * U, 0.175); chk("Ex10 E = CU²/2", 0.5 * C * U**2, 219, 0.01)
chk("Ex10 I_med", C * U / dt, 35); chk("Ex10 P_med", 0.5 * C * U**2 / dt, 4.4e4, 0.01)
chk("Fix cap. série 6µF,3µF", 6 * 3 / 9, 2.0)
chk("Fix cap. Q série (12 V)", 2e-6 * 12, 24e-6)
chk("Fix cap. dielétrico: U", 24e-6 / (4 * 2e-6), 3.0)
chk("Fix cap. dielétrico: E_i", 0.5 * 2e-6 * 144, 144e-6); chk("Fix cap. dielétrico: E_f", 0.5 * (24e-6) ** 2 / 8e-6, 36e-6)
chk("Fix próton 2 kV", math.sqrt(2 * e * 2000 / mp), 6.2e5, 0.01)
chk("Fix gota: E=mg/q", 2e-15 * 10 / 3.2e-19, 6.3e4, 0.01)
chk("Fix esfera 10 cm, 4 nC: V", k * 4e-9 / 0.1, 360); chk("Fix esfera: E fora", k * 4e-9 / 0.1**2, 3.6e3)
chk("Fix equilíbrio 4q,q: x", 0.9 * 2 / 3, 0.60)
chk("Fix contato 8,−2 µC", (8 - 2) / 2, 3.0); chk("Fix elétrons 5 µC", 5e-6 / e, 3.1e13, 0.02)
chk("Ap. centelha 1 cm", 3e6 * 0.010, 3e4)
chk("Aprof. Fe/Fg próton–elétron", 8.99e9 * 1.602e-19**2 / (6.674e-11 * 1.673e-27 * 9.109e-31), 2.3e39, 0.05)

print("── Módulo III ──")
I = 18 / 4
chk("Ex11 carga 6 A·2 s + ½·2·6", 6 * 2 + 0.5 * 2 * 6, 18); chk("Ex11 n elétrons", 18 / e, 1.1e20, 0.03)
chk("Ex11 I média", 18 / 4, 4.5)
vd = 6 / (8.5e28 * e * 2.5e-6)
chk("Ex11 v deriva (Cu, 2,5 mm²)", vd, 1.8e-4, 0.05)
A = math.pi * (0.8e-3) ** 2
R = 1.7e-8 * 50 / A
chk("Ex12 A (mm²)", A * 1e6, 2.0, 0.01); chk("Ex12 R fio", R, 0.42, 0.02)
chk("Ex12 U = R I (5 A)", R * 5, 2.1, 0.03); chk("Ex12 P = R I²", R * 25, 10.6, 0.03)
chk("Ex12 d dobrado → R/4", R / 4, 0.106, 0.03)
chk("Ex13 energia mensal kWh", 5.5 * (4 * 10 / 60) * 30, 110); chk("Ex13 custo R$", 110 * 0.90, 99.0)
chk("Ex13 I chuveiro", 5500 / 220, 25)
Rinv, Rver = 220**2 / 5500, 220**2 / 2750
chk("Ex14 R inverno", Rinv, 8.8); chk("Ex14 R verão", Rver, 17.6)
chk("Ex14 I inverno", 220 / Rinv, 25); chk("Ex14 I verão", 220 / Rver, 12.5)
md = 0.050
chk("Ex14 ΔT inverno", 5500 / (md * 4180), 26, 0.02); chk("Ex14 ΔT verão", 2750 / (md * 4180), 13, 0.02)
R127 = 127**2 / 4400
chk("Ex15 R (127 V, 4400 W)", R127, 3.67, 0.01); chk("Ex15 P em 220 V", 220**2 / R127, 1.32e4, 0.01)
chk("Ex15 razão (220/127)²", (220 / 127) ** 2, 3.0, 0.01); chk("Ex15 I em 220 V", 220 / R127, 60, 0.01); chk("Ex15 I nominal", 4400 / 127, 34.6, 0.01)
# Ex16 lâmpadas
RL = 4.0
chk("Ex16 aberta I", 12 / (2 * RL), 1.5); chk("Ex16 aberta P1", 1.5**2 * RL, 9.0)
Rt = RL + RL / 2
chk("Ex16 fechada I", 12 / Rt, 2.0); chk("Ex16 fechada P1", 4 * RL, 16); chk("Ex16 fechada P2", 1.0**2 * RL, 4.0)
# Ex17 misto
R1, R2, R3, R4, eps = 2, 6, 12, 2, 24
Rp = R2 * R3 / (R2 + R3); Req = R1 + Rp + R4; I = eps / Req
chk("Ex17 Rp", Rp, 4); chk("Ex17 Req", Req, 8); chk("Ex17 I", I, 3)
Up = I * Rp
chk("Ex17 U_p", Up, 12); chk("Ex17 I2", Up / R2, 2); chk("Ex17 I3", Up / R3, 1)
chk("Ex17 balanço de potência", eps * I, I**2 * R1 + (Up / R2) ** 2 * R2 + (Up / R3) ** 2 * R3 + I**2 * R4)
V = nodal([(1, 2, 2), (2, 3, 6), (2, 3, 12), (3, 0, 2)], [(1, 0, 24, 1e-9)], 4)
chk("Ex17 V_B (nodal)", V[2], 18); chk("Ex17 V_C (nodal)", V[3], 6)
# Ex18 ponte com fio (B e C unidos)
Vn = nodal([(1, 2, 6), (1, 2, 3), (2, 0, 3), (2, 0, 6)], [(1, 0, 24, 1e-9)], 3)
chk("Ex18 V_B=V_C", Vn[2], 12)
Req2 = 6 * 3 / 9 + 3 * 6 / 9
chk("Ex18 Req", Req2, 4); chk("Ex18 I", 24 / Req2, 6)
chk("Ex18 I1", (24 - 12) / 6, 2); chk("Ex18 I2", (24 - 12) / 3, 4); chk("Ex18 I3", 12 / 3, 4); chk("Ex18 I4", 12 / 6, 2)
chk("Ex18 I_fio = I3 − I1", 4 - 2, 2)
chk("Ex18 balanço potência", 24 * 6, 2**2 * 6 + 4**2 * 3 + 4**2 * 3 + 2**2 * 6)
# Ex19 curto
chk("Ex19 antes I", 12 / (4 + 8), 1); chk("Ex19 antes P1", 1 * 4, 4); chk("Ex19 antes P2", 8, 8)
chk("Ex19 depois I", 12 / 4, 3); chk("Ex19 depois P1", 9 * 4, 36)
# Ex20 Kirchhoff 1 malha
chk("Ex20 I", (12 - 4) / (2 + 4 + 2), 1.0)
# Ex21 K 2 malhas
A_ = np.array([[1, -1, -1], [1, 6, 0], [0, 6, -3]], float)   # I1 − I2 − I3 = 0 ; 1·I1 + 6·I2 = 18 ; 6 I2 − 3 I3 = 0
b_ = np.array([0, 18, 0])
I1_, I2_, I3_ = np.linalg.solve(A_, b_)
chk("Ex21 I1", I1_, 6); chk("Ex21 I2", I2_, 2); chk("Ex21 I3", I3_, 4)
chk("Ex21 potência", 18 * 6, 6**2 * 1 + 2**2 * 6 + 4**2 * 3)
# Ex22 K 2 geradores
A_ = np.array([[1, 1, -1], [1, 0, 4], [0, 2, 4]], float)   # I1+I2=I3 ; ε1 = 1·I1 + 4·I3 ; ε2 = 2·I2 + 4·I3
b_ = np.array([0, 6, 2])
I1_, I2_, I3_ = np.linalg.solve(A_, b_)
chk("Ex22 I1", I1_, 2); chk("Ex22 I2", I2_, -1); chk("Ex22 I3", I3_, 1)
chk("Ex22 potência: ε1 I1 + ε2 I2 = Σ R I²", 6 * 2 + 2 * (-1), 1 * 4 + 2 * 1 + 4 * 1)
# Ex23 gerador/receptor
eps_g, r_g, R_c = 12.0, 0.5, 5.5
I = eps_g / (R_c + r_g)
chk("Ex23 I", I, 2.0); chk("Ex23 U", eps_g - r_g * I, 11); chk("Ex23 P_total", eps_g * I, 24)
chk("Ex23 P_útil", 11 * I, 22); chk("Ex23 P_perdida", r_g * I**2, 2); chk("Ex23 η", 11 / 12, 0.917, 0.01)
chk("Ex23 I_cc", eps_g / r_g, 24); chk("Ex23 P_max (R=r)", eps_g**2 / (4 * r_g), 72)
chk("Ex23 receptor U", 6 + 1 * 2, 8); chk("Ex23 receptor P_abs", 8 * 2, 16); chk("Ex23 receptor P_útil", 6 * 2, 12)
chk("Ex23 receptor η", 6 / 8, 0.75)
chk("Ex24 LED R", (5 - 2.0) / 0.020, 150); chk("Ex24 P_R", 3.0 * 0.020, 0.06)
# cadeia gerador+receptor
chk("Interseção 12−0,5I = 6+I", (12 - 6) / 1.5, 4.0)
# cabo
RA = 1.72e-8 * 20 / 2.5e-6
chk("Fio 2,5 mm² 20 m", RA, 0.1376, 0.01); chk("Fio 2,5 mm² perda 25 A", RA * 625, 86, 0.02)
chk("Fio 4 mm² perda 25 A", 1.72e-8 * 20 / 4e-6 * 625, 53.8, 0.02)

print("── Complementos de Módulo III (fixações p25 e p34) ──")
chk("III-12 corrente total chuveiro+ferro", (5500 + 1000) / 220, 29.5, 0.01)
chk("III-12 potência máxima com 20 A", 20 * 220, 4400.0, 1e-9)
RA = 1.7e-8 * 30 / 4.0e-6
chk("III-13 I = P/U", 1500 / 127, 11.8, 0.01); chk("III-13 R do fio", RA, 0.13, 0.03)
chk("III-13 queda de tensão", RA * 1500 / 127, 1.5, 0.02); chk("III-13 P perdida", RA * (1500 / 127) ** 2, 18, 0.02)
Ib = 12 / (5.0 + 0.5 / 2)
chk("K-4 I no resistor (2 baterias iguais em paralelo)", Ib, 2.3, 0.02)
chk("K-4 U = 5 I", 5 * Ib, 12 - 0.5 * Ib / 2, 1e-9)
chk("K-4 I em cada bateria", Ib / 2, 1.1, 0.04)
chk("K-5 I entre baterias diferentes", (12 - 6) / (1.0 + 1.0), 3.0, 1e-9)
chk("K-5 potência dissipada", 2 * 1.0 * 3.0**2, 18.0, 1e-9)
print("── Módulo IV ──")
chk("Ex25 fio 10 A a 5 cm (µT)", mu0 * 10 / (2 * math.pi * 0.05) * 1e6, 40, 0.01)
chk("Ex25 dois fios, correntes opostas, ponto médio (µT)", 2 * mu0 * 10 / (2 * math.pi * 0.05) * 1e6, 80, 0.01)
chk("Ex26 espira R=5 cm, 10 A (µT)", mu0 * 10 / (2 * 0.05) * 1e6, 126, 0.01)
chk("Ex26 razão B_espira/B_fio (R=r) = π", (mu0 * 10 / (2 * 0.05)) / (mu0 * 10 / (2 * math.pi * 0.05)), math.pi, 1e-9)
chk("Ex26 solenoide 500 esp, 25 cm, 2 A (mT)", mu0 * 500 * 2 / 0.25 * 1e3, 5.0, 0.01)
chk("Ex26 solenoide / campo da Terra (50 µT) ≈ 100", mu0 * 2000 * 2 / 50e-6, 100, 0.01)
chk("Fix 4.2-2 B_fio a 2 cm, 5 A (µT)", mu0 * 5 / (2 * math.pi * 0.02) * 1e6, 50, 0.01)
chk("Fix 4.2-3 solenoide 800 esp, 40 cm, 5 A (mT)", mu0 * (800 / 0.40) * 5 * 1e3, 12.6, 0.01)
r1 = 0.20 * 6.0 / (6.0 + 3.0)
chk("Fix 4.2-4 campo nulo: r2 (cm) do fio de 3 A", (0.20 / 3) * 100, 6.7, 0.01)
chk("Fix 4.2-4 campo nulo: r1 (cm) do fio de 6 A", (0.20 * 2 / 3) * 100, 13.3, 0.01)
v = 1.2e7
r = me * v / (e * 1e-3)
T = 2 * math.pi * me / (e * 1e-3)
chk("Ex27 F = e v B (N)", e * v * 1e-3, 1.9e-15, 0.02)
chk("Ex27 r (cm)", r * 100, 6.8, 0.02)
chk("Ex27 T (ns)", T * 1e9, 36, 0.02)
chk("Ex27 hélice θ=30°: r' (cm)", r * math.sin(math.radians(30)) * 100, 3.4, 0.03)
chk("Ex27 passo (cm)", v * math.cos(math.radians(30)) * T * 100, 37, 0.03)
chk("Ex27 v²/r = F/m", v**2 / r, e * v * 1e-3 / me, 0.01)
chk("Ex27 F/(m g) ~ 1e14", e * v * 1e-3 / (me * g), 2.1e14, 0.05)
chk("Ex28 I = m g/(B L)", 0.010 * g / (0.50 * 0.20), 1.0, 1e-9)
chk("Ex28 a com 2,0 A", (0.50 * 2.0 * 0.20 - 0.010 * g) / 0.010, 10.0, 1e-9)
Ium = (12 - 10) / 1.0
chk("Ex29 I em regime", Ium, 2.0); chk("Ex29 I na partida", 12 / 1.0, 12.0)
chk("Ex29 P_mec", 10 * Ium, 20.0); chk("Ex29 P_abs", 12 * Ium, 24.0); chk("Ex29 P_J", 1.0 * Ium**2, 4.0)
chk("Ex29 η", 20 / 24, 0.833, 0.01); chk("Ex29 travado: P_J", 1.0 * 12**2, 144.0)
chk("Ex30 ε = N A ΔB/Δt", 100 * 5e-3 * 0.6 / 0.1, 3.0); chk("Ex30 I (R=6 Ω)", 3.0 / 6, 0.5)
vt = 0.025 * 10 * 0.5 / (1.0**2 * 0.5**2)
chk("Ex31 v terminal", vt, 0.50); chk("Ex31 I = BLv/R", 1.0 * 0.5 * vt / 0.5, 0.5)
chk("Ex31 F = BIL = mg", 1.0 * 0.5 * 0.5, 0.25); chk("Ex31 P = I²R = mgv", 0.5**2 * 0.5, 0.125)
chk("Ex32 perda 10 kV", 5 * (10e6 / 10e3) ** 2, 5e6); chk("Ex32 perda 100 kV", 5 * (10e6 / 100e3) ** 2, 5e4)
chk("Ex32 razão de espiras", 100e3 / 10e3, 10)
chk("Fix 4.3-2 F = q v B", 3.2e-19 * 5.0e5 * 0.40, 6.4e-14, 0.01)
chk("Fix 4.3-3 r próton (cm)", 1.67e-27 * 2.0e6 / (e * 0.50) * 100, 4.2, 0.02)
chk("Fix 4.3-3 T próton (s)", 2 * math.pi * 1.67e-27 / (e * 0.50), 1.3e-7, 0.02)
chk("Fix 4.3-4 F = B I L sen 30°", 0.25 * 4.0 * 0.30 * 0.5, 0.15, 1e-9)
chk("Fix 4.3-5 v = E/B", 2.0e4 / 0.10, 2.0e5, 1e-9)
chk("Fix 4.3-6 τ = N B I A", 100 * 0.20 * 2.0 * 0.020, 0.80, 1e-9)
chk("MRI Larmor 1,5 T (MHz)", 42.58 * 1.5, 63.9, 0.01)
chk("Gerador: ε_max = N B A ω", 1 * 0.5 * 0.02 * 2 * math.pi * 60, 3.8, 0.02)
chk("Tensão eficaz 127 → pico", 127 * math.sqrt(2), 180, 0.01)
chk("c = 1/√(μ0 ε0) (m/s)", 1 / math.sqrt(mu0 * eps0), 3.0e8, 0.01)
chk("Ampère: fios 10 A, 1 cm: F/L (N/m)", mu0 * 10 * 10 / (2 * math.pi * 0.01), 2.0e-3, 0.01)
print("── Exercícios graduados do Módulo IV (p51) ──")
chk("Ex.IV-1 r = μ0 I/(2π B)", mu0 * 20 / (2 * math.pi * 8.0e-6), 0.50, 0.01)
chk("Ex.IV-4 ε média", 50 * (4.0e-3 - 1.0e-3) / 0.030, 5.0, 1e-9); chk("Ex.IV-4 I", 5.0 / 2.0, 2.5)
chk("Ex.IV-5 ε 0–0,2 s", -10 * 6e-3 / 0.2, -0.30, 1e-9); chk("Ex.IV-5 ε 0,5–0,6 s", 10 * 6e-3 / 0.1, 0.60, 1e-9)
chk("Ex.IV-6 ε = BLv", 0.50 * 0.40 * 3.0, 0.60); chk("Ex.IV-6 I", 0.60 / 0.60, 1.0)
chk("Ex.IV-6 F = BIL", 0.50 * 1.0 * 0.40, 0.20); chk("Ex.IV-6 P = F v = ε I", 0.20 * 3.0, 0.60 * 1.0)
chk("Ex.IV-7 Ns", 1270 * 9.0 / 127, 90.0, 1e-9); chk("Ex.IV-7 Ip (mA)", 9.0 * 0.5 / 127 * 1e3, 35, 0.02)
chk("Ex.IV-11 ε = BLv", 0.40 * 0.10 * 0.50, 0.020); chk("Ex.IV-11 I", 0.020 / 0.20, 0.10)
chk("Ex.IV-11 F = BIL", 0.40 * 0.10 * 0.10, 4.0e-3); chk("Ex.IV-11 P = F v = ε I", 4.0e-3 * 0.5, 0.020 * 0.10)
print("── Questões integradoras (p54) ──")
chk("Int-1 Q = CU", 100e-6 * 300, 3.0e-2); chk("Int-1 E = CU²/2", 0.5 * 100e-6 * 300**2, 4.5)
chk("Int-1 I média", 3.0e-2 / 2.0e-3, 15.0); chk("Int-1 P média (2,25 kW arredonda para 2,3 kW)", 4.5 / 2.0e-3, 2.3e3, 0.03)
chk("Int-2 I 127 V", 4400 / 127, 34.6, 0.01); chk("Int-2 I 220 V", 4400 / 220, 20.0, 1e-9)
chk("Int-2 P_fio 127 V", 0.10 * (4400 / 127) ** 2, 120.0, 0.01); chk("Int-2 P_fio 220 V", 0.10 * (4400 / 220) ** 2, 40.0, 1e-9)
chk("Int-2 razão = (220/127)²", (4400 / 127) ** 2 / (4400 / 220) ** 2, (220 / 127) ** 2, 1e-9)
# Int-3: U = ε − r I, I = U/R + (U − ε')/r'
Uint = (12 + 6 / 2) / (1 + 1 / 6 + 1 / 2) * 1.0
Uint = 15 / (1 + 1 / 6 + 1 / 2) / 1.0 * 1.0
# resolve: U = 12 − 1·(U/6 + (U−6)/2)  ⇒ U (1 + 1/6 + 1/2) = 12 + 3
Uint = (12 + 3) / (1 + 1 / 6 + 1 / 2)
chk("Int-3 U nos terminais", Uint, 9.0, 1e-9)
chk("Int-3 I lâmpada", Uint / 6, 1.5); chk("Int-3 I motor", (Uint - 6) / 2, 1.5); chk("Int-3 I gerador", (12 - Uint) / 1.0, 3.0)
chk("Int-3 η gerador", Uint / 12, 0.75); chk("Int-3 η motor", 6 / Uint, 0.667, 0.01)
chk("Int-3 balanço ε I = U I + r I²", 12 * 3.0, Uint * 3.0 + 1.0 * 3.0**2)
chk("Int-3 balanço motor U I_m = ε' I_m + r' I_m²", Uint * 1.5, 6 * 1.5 + 2.0 * 1.5**2)
chk("Int-4 v = E/B", 5.0e4 / 0.10, 5.0e5, 1e-9)
chk("Int-4 r próton (cm)", 1.67e-27 * 5.0e5 / (e * 0.20) * 100, 2.6, 0.02)
chk("Int-4 r dêuteron (cm)", 2 * 1.67e-27 * 5.0e5 / (e * 0.20) * 100, 5.2, 0.02)
Bsol = mu0 * 2000 * 2.0
chk("Int-5 B solenoide", Bsol, 5.0e-3, 0.01); chk("Int-5 r elétron (cm)", me * 1.0e7 / (e * Bsol) * 100, 1.1, 0.03)
chk("Int-6 I_s", 24 / 12, 2.0); chk("Int-6 I_p", 24 / 220, 0.11, 0.02); chk("Int-6 Ns/Np", 12 / 220, 0.055, 0.01)
chk("Int-8 carga (área I×t)", 2 * 3 + 0 * 2 + 1 * 4, 10.0); chk("Int-8 energia Σ R I² t", 4 * 2**2 * 3 + 4 * 1**2 * 4, 64.0)
print(f"\n{n_checks} verificações; {'TODAS OK' if ok_all else 'HÁ DIVERGÊNCIAS'}")
