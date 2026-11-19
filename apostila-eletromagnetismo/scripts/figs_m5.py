"""Módulo V — Dispositivos e tecnologias (páginas 23 a 26)."""
import math
import numpy as np
from svglib import Svg, Plot, STROKE, num, rich_width

X_, Y_, Z_ = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])


# ======================================================================================= p23 · motor (corte) + comutador
def motor_section(W=336, H=200):
    s = Svg(W, H, 'motor_section')
    cx, cy, R = 118, 100, 52
    psi = math.radians(35)
    u = np.array([math.cos(psi), math.sin(psi), 0.0])
    B = X_.copy()
    # correntes: lado direito sai da página (+z), lado esquerdo entra (−z)
    I_r, I_l = +Z_, -Z_
    F_r, F_l = np.cross(I_r, B), np.cross(I_l, B)
    assert np.allclose(F_r, Y_) and np.allclose(F_l, -Y_)                 # binário: sobe à direita, desce à esquerda
    n_hat = np.array([math.sin(psi), -math.cos(psi), 0.0])                # normal (momento magnético da espira)
    tau = np.cross(n_hat, B)                                              # τ = m × B
    assert tau[2] > 0                                                     # anti-horário
    phi = math.degrees(math.acos(np.dot(n_hat, B)))
    # polos e campo
    s.rect(10, 38, 24, 124, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.2); s.text(22, 106, 'N', 14, 'white', weight=700)
    s.rect(W - 130, 38, 24, 124, 0, fill='#FFFFFF', stroke=STROKE['red'], sw=1.6); s.text(W - 118, 106, 'S', 14, 'red', weight=700)
    for yy in (52, 76, 100, 124, 148):
        s.arrow((38, yy), (W - 136, yy), 'blue', 1.2, head=6, opacity=0.5)
    s.vtext(W - 150, 48, 'B', size=12, color='blue', plate=True)
    # espira
    pr = (cx + R * u[0], cy - R * u[1]); pl = (cx - R * u[0], cy + R * u[1])
    s.line(pl, pr, 'orange', 2.6)
    s.sym_out(pr, 7.4, 'orange', 1.9); s.sym_in(pl, 7.4, 'orange', 1.9)
    s.circle((cx, cy), 3.2, fill='ink', stroke=None)
    # forças
    s.arrow((pr[0], pr[1] - 10), (pr[0], pr[1] - 44), 'green', 3.0, head=9.5)
    s.arrow((pl[0], pl[1] + 10), (pl[0], pl[1] + 44), 'green', 3.0, head=9.5)
    s.vtext(pr[0] + 14, pr[1] - 30, 'F', size=12, color='green', plate=True)
    s.vtext(pl[0] - 14, pl[1] + 38, 'F', size=12, color='green', plate=True)
    # normal e ângulo φ
    s.arrow((cx, cy), (cx + 38 * n_hat[0], cy - 38 * n_hat[1]), 'ink', 2.2, head=8)
    s.vtext(cx + 48 * n_hat[0] + 6, cy - 48 * n_hat[1] + 12, 'n', size=11.5, color='ink', arrow=False)
    s.path(f'M {cx + 22} {cy} A 22 22 0 0 1 {cx + 22 * n_hat[0]:.2f} {cy - 22 * n_hat[1]:.2f}', stroke='gray', w=1.1)
    s.text(cx + 30, cy + 12, 'φ', 10.5, 'gray', weight=700)
    # rotação
    s.carrow([(cx + 80 * math.cos(math.radians(a)), cy - 80 * math.sin(math.radians(a))) for a in range(-20, 36, 5)], 'gray', 1.6, head=8)
    s.text(cx + 92, cy - 42, 'gira', 8.4, 'gray', anchor='start', weight=700)
    s.text(8, 16, 'motor: espira com corrente em B', 9.4, 'navy', anchor='start', weight=700)
    s.text(8, 28, 'F = N B I ℓ em cada lado → binário', 8.4, 'green', anchor='start', weight=700)
    s.text(8, 188, 'τ = N B I A sen φ', 9.6, 'green', anchor='start', weight=700)
    # comutador (inset)
    kx, ky = 280, 58
    s.text(kx + 0, 22, 'comutador', 8.6, 'navy', weight=700)
    s.circle((kx, ky + 10), 17, fill='none', stroke='#C3CBD6', w=7)
    s.path(f'M {kx - 17} {ky + 10} A 17 17 0 0 1 {kx + 17} {ky + 10}', stroke=STROKE['ink'], w=6, fill='none')
    s.line((kx - 3, ky - 12), (kx + 3, ky - 12), 'ink', 5)
    s.line((kx - 3, ky + 32), (kx + 3, ky + 32), 'ink', 5)
    s.text(kx, ky + 54, 'anel partido +', 8.2, 'gray'); s.text(kx, ky + 64, 'escovas', 8.2, 'gray')
    s.text(kx, ky + 80, 'invertem I a cada', 8.2, 'ink'); s.text(kx, ky + 90, 'meia volta: o torque', 8.2, 'ink'); s.text(kx, ky + 100, 'mantém o sentido', 8.2, 'ink')
    s.save()
    return phi


# ======================================================================================= p24 · gerador (duas posições)
def generator_two(W=680, H=176):
    s = Svg(W, H, 'generator_two')
    pw = W / 2
    B = X_.copy()
    for k, (deg, title, t2) in enumerate(((0, 'plano ⊥ B (θ = 0°)', 'Φ máximo · ε = 0'), (90, 'plano ∥ B (θ = 90°)', 'Φ = 0 · |ε| máxima'))):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 17, title, 9.4, 'navy', weight=700)
        cx, cy, R = x0 + pw / 2, 88, 46
        for yy in (44, 66, 110, 132):
            s.arrow((x0 + 28, yy), (x0 + pw - 28, yy), 'blue', 1.2, head=6, opacity=0.5)
        s.arrow((x0 + 28, 88), (x0 + pw - 28, 88), 'blue', 1.2, head=6, opacity=0.5) if deg == 0 else None
        s.vtext(x0 + pw - 40, 62, 'B', size=12, color='blue', plate=True)
        th = math.radians(deg)
        # lados em ±R perpendicular ao plano da espira; plano a θ com a normal... posição inicial: plano ⊥ B (lados em (0, ±R)) para θ=0
        a = th + math.pi / 2                                          # ângulo do lado "superior" (anti-horário, ωt = θ)
        sides = [np.array([R * math.cos(a), R * math.sin(a), 0.0]), -np.array([R * math.cos(a), R * math.sin(a), 0.0])]
        omega = np.array([0, 0, 1.0])
        emfs = []
        for r_vec in sides:
            v = np.cross(omega, r_vec) / R                              # velocidade do lado (rotação anti-horária)
            e = np.cross(v, B)                                           # v × B : empurra cargas positivas ao longo de ±z
            emfs.append(e[2])
            P = (cx + r_vec[0], cy - r_vec[1])
            if abs(e[2]) > 1e-9:
                (s.sym_out if e[2] > 0 else s.sym_in)(P, 7.2, 'purple', 1.9)
            else:
                s.circle(P, 5.4, fill='white', stroke='orange', w=1.8)
            s.arrow(P, (P[0] + 28 * v[0], P[1] - 28 * v[1]), 'cyan', 2.2, head=8)
        pa, pb = (cx + sides[0][0], cy - sides[0][1]), (cx + sides[1][0], cy - sides[1][1])
        s.line(pa, pb, 'orange', 2.4)
        s.circle((cx, cy), 3.0, fill='ink', stroke=None)
        if k == 0:
            assert abs(emfs[0]) < 1e-9 and abs(emfs[1]) < 1e-9
        else:
            assert abs(emfs[0] + emfs[1]) < 1e-9 and abs(emfs[0]) > 0.9           # FEMs opostas nos dois lados => somam no circuito
        s.carrow([(cx + 62 * math.cos(math.radians(a_)), cy - 62 * math.sin(math.radians(a_))) for a_ in range(150, 211, 6)], 'gray', 1.6, head=7)
        s.carrow([(cx + 62 * math.cos(math.radians(a_)), cy - 62 * math.sin(math.radians(a_))) for a_ in range(-30, 31, 6)], 'gray', 1.6, head=7)
        s.text(cx - 76, cy - 4, 'ω', 11, 'gray', anchor='end', weight=700)
        s.text(x0 + pw / 2, 164, t2, 8.8, 'green', weight=700)
    s.save()
    return s


# ======================================================================================= p24 · tensão alternada (60 Hz)
def ac_voltage(W=336, H=160):
    s = Svg(W, H, 'ac_voltage')
    f, N, Bf, A = 60.0, 100, 0.50, 0.010
    emax = N * Bf * A * 2 * math.pi * f
    pl = Plot(s, 50, 14, W - 64, H - 52, (0, 33.4), (-220, 225), xticks=[0, 8.33, 16.67, 25.0, 33.33], yticks=[-188, 0, 188],
              xlabel='tempo (ms)', ylabel='ε (V)', xlab_dy=30, ylab_dx=-38, xfmt=lambda v: num(v, 1), yfmt=lambda v: num(v, 0))
    t = np.linspace(0, 33.34, 500)
    pl.curve(t, emax * np.sin(2 * math.pi * f * t / 1000), 'purple', 2.4)
    erms = emax / math.sqrt(2)
    for y in (erms, -erms):
        s.line((pl.X(0), pl.Y(y)), (pl.X(33.4), pl.Y(y)), 'gray', 1.0, dash='4 3')
    s.text(pl.X(33.2), pl.Y(erms) - 4, 'ε_{ef} = 133 V', 8.2, 'gray', anchor='end', weight=700)
    s.text(pl.X(33.2), pl.Y(200), 'ε_{máx} = 188 V', 8.4, 'purple', anchor='end', weight=700)
    xa, xb, yb_ = 4.17, 20.83, 208
    s.line((pl.X(xa), pl.Y(yb_)), (pl.X(xb), pl.Y(yb_)), 'ink', 1.0); s.line((pl.X(xa), pl.Y(yb_) - 3), (pl.X(xa), pl.Y(yb_) + 3), 'ink', 1.0); s.line((pl.X(xb), pl.Y(yb_) - 3), (pl.X(xb), pl.Y(yb_) + 3), 'ink', 1.0)
    s.text(pl.X(12.5), pl.Y(yb_) + 13, 'T = 16,7 ms (f = 60 Hz)', 8.2, 'ink', weight=700)
    s.save()
    return emax, erms


# ======================================================================================= p23/p24 · motor × gerador
def motor_vs_gen(W=680, H=128):
    s = Svg(W, H, 'motor_vs_gen')
    bw, bh, gap = 92, 40, 14
    def blk(x, y, t1, t2, color, fill):
        s.rect(x, y, bw, bh, 5, fill=fill, stroke=color, sw=1.6)
        s.text(x + bw / 2, y + 17, t1, 9, 'ink', weight=700)
        s.text(x + bw / 2, y + 30, t2, 8.2, 'gray')
    for k, (title, items, color, fill) in enumerate((
            ('MOTOR', [('Energia elétrica', 'da fonte (I)'), ('Forças sobre I em B', 'F = N B I ℓ → torque'), ('Rotação', 'energia mecânica')], 'green', 'green'),
            ('GERADOR', [('Rotação', 'turbina, vento, água'), ('Fluxo varia', 'ΔΦ/Δt → FEM'), ('Energia elétrica', 'tensão alternada')], 'purple', 'purple'))):
        x0 = 4 + k * (W / 2)
        s.text(x0 + 160, 16, title, 11, color, weight=800, anchor='middle')
        for i, (a, b) in enumerate(items):
            blk(x0 + 8 + i * (bw + gap + 6), 28, a, b, color, fill)
            if i < 2:
                s.arrow((x0 + 8 + i * (bw + gap + 6) + bw + 1, 48), (x0 + 8 + (i + 1) * (bw + gap + 6) - 1, 48), 'ink', 2.0, head=8)
        s.text(x0 + 160, 84, ['Entrada: elétrica · Saída: mecânica', 'Entrada: mecânica · Saída: elétrica'][k], 9, 'ink', weight=700)
        s.text(x0 + 160, 98, ['Efeito principal: força sobre corrente (p. 14)', 'Efeito principal: indução de Faraday (p. 17)'][k], 8.4, 'gray')
        s.text(x0 + 160, 112, ['Ao girar, também induz FEM contrária (Lenz)', 'Com carga elétrica, exige torque na turbina (Lenz)'][k], 8.4, color, weight=700)
    s.line((W / 2, 8), (W / 2, H - 8), 'faint', 1.0)
    s.save()
    return s


# ======================================================================================= p25 · transformadores
def transformer(W=680, H=166):
    s = Svg(W, H, 'transformer')
    pw = W / 2
    for k, (np_, ns_, title, ineq) in enumerate(((3, 9, 'ELEVADOR (N_{s} > N_{p})', 'U_{s} > U_{p}  ·  I_{s} < I_{p}'), (9, 3, 'ABAIXADOR (N_{s} < N_{p})', 'U_{s} < U_{p}  ·  I_{s} > I_{p}'))):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 17, title, 9.6, 'navy', weight=700)
        L, T, Rr, Bm = x0 + 98, 34, x0 + 242, 116                              # contorno do núcleo
        s.polyline([(L, T), (Rr, T), (Rr, Bm), (L, Bm), (L, T)], '#C3CBD6', 18.0, join='miter')
        s.arrow((L + 36, T), (L + 80, T), 'blue', 2.0, head=8)
        s.text((L + Rr) / 2, T + 44, 'fluxo alternado Φ no núcleo', 8.4, 'blue', weight=700)
        # enrolamentos
        def coil(x, n):
            span = (Bm - T - 24)
            for i in range(n):
                yy = T + 14 + span * (i + 0.5) / n
                s.line((x - 12, yy - 3), (x + 12, yy + 3), 'orange', 2.2)
        coil(L, np_); coil(Rr, ns_)
        # fonte CA (primário) e carga (secundário)
        s.polyline([(L - 12, T + 20), (x0 + 40, T + 20), (x0 + 40, T + 30)], 'ink', 1.5)
        s.circle((x0 + 40, T + 44), 14, fill='white', stroke='ink', w=1.6)
        s.path(f'M {x0 + 33} {T + 44} q 3.5 -8 7 0 t 7 0', stroke='ink', w=1.6)
        s.polyline([(x0 + 40, T + 58), (x0 + 40, Bm - 20), (L - 12, Bm - 20)], 'ink', 1.5)
        s.polyline([(Rr + 12, T + 20), (Rr + 46, T + 20)], 'ink', 1.5)
        s.resistor((Rr + 46, T + 20), (Rr + 46, Bm - 20), n=5, amp=6, color='ink', w=1.6)
        s.polyline([(Rr + 46, Bm - 20), (Rr + 12, Bm - 20)], 'ink', 1.5)
        s.text(x0 + 40, Bm + 16, 'U_{p}, I_{p}', 9, 'orange', weight=700)
        s.text(Rr + 46, Bm + 16, 'U_{s}, I_{s}', 9, 'orange', weight=700)
        s.text(L - 20, (T + Bm) / 2 + 4, 'N_{p}', 9.4, 'orange', anchor='end', weight=700)
        s.text(Rr + 20, (T + Bm) / 2 + 4, 'N_{s}', 9.4, 'orange', anchor='start', weight=700)
        s.text(x0 + pw / 2, H - 14, ineq, 9.6, 'green', weight=700)
        s.text(x0 + pw / 2, H - 4, 'U_{p}/U_{s} = N_{p}/N_{s}  ·  P_{p} = P_{s}', 8.2, 'ink')
    s.save()
    return s


# ======================================================================================= p26 · transmissão
def transmission_chain(W=680, H=128):
    s = Svg(W, H, 'transmission_chain')
    P, R_line = 2.0e6, 5.0
    rows = []
    for U in (2.0e4, 2.0e5):
        I = P / U
        rows.append((U, I, R_line * I ** 2))
    assert abs(rows[0][2] - 5.0e4) < 1 and abs(rows[1][2] - 5.0e2) < 1e-6
    # blocos
    xs = [10, 140, 270, 470, 580]
    labs = [('Usina', 'gerador'), ('Elevador', 'sobe U'), ('Linha de transmissão', 'R = 5,0 Ω'), ('Abaixador', 'reduz U'), ('Consumo', 'cidade')]
    wds = [100, 100, 170, 100, 90]
    for x, (a, b), w in zip(xs, labs, wds):
        s.rect(x, 20, w, 34, 5, fill='gray', stroke='gray', sw=1.4)
        s.text(x + w / 2, 35, a, 9, 'ink', weight=700); s.text(x + w / 2, 47, b, 8.2, 'gray')
    for i in range(4):
        s.arrow((xs[i] + wds[i] + 1, 37), (xs[i + 1] - 1, 37), 'ink', 2.0, head=8)
    s.text(W / 2, 12, 'mesma potência entregue, P = 2,0 MW', 9.2, 'navy', weight=700)
    for j, (U, I, loss) in enumerate(rows):
        y = 78 + j * 24
        s.text(10, y, ['U = 20 kV →', 'U = 200 kV →'][j].replace(' →', ''), 9, 'orange', anchor='start', weight=700)
        s.text(120, y, f'I = P/U = {int(I)} A', 9, 'orange', anchor='start', weight=700)
        txt = f'perda na linha = R I² = {loss / 1000:.1f} kW'.replace('.', ',')
        s.text(260, y, txt, 9, 'red', anchor='start', weight=700)
        s.text(260 + rich_width(txt, 9, 700) + 8, y, ['(2,5% da potência)', '(0,025% da potência)'][j], 8.4, 'gray', anchor='start')
    s.text(W / 2, H - 4, 'tensão 10× maior ⇒ corrente 10× menor ⇒ perda por efeito Joule 100× menor', 9, 'green', weight=700)
    s.save()
    return rows


# ======================================================================================= p26 · captador de guitarra
def guitar_pickup(W=336, H=150):
    s = Svg(W, H, 'guitar_pickup')
    cx = 110
    s.rect(cx - 12, 70, 24, 40, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.2); s.text(cx, 96, 'N', 12, 'white', weight=700)
    for yy in range(72, 110, 5):
        s.ellipse((cx, yy), 24, 3, fill='none', stroke='orange', w=1.6)
    # corda (aço) vibrando acima do ímã
    s.polyline([(20, 40), (cx, 38), (W - 140, 40)], 'ink', 2.0)
    s.polyline([(20, 40), (cx, 28), (W - 140, 40)], 'ink', 1.2, dash='3 3', opacity=0.6)
    s.polyline([(20, 40), (cx, 49), (W - 140, 40)], 'ink', 1.2, dash='3 3', opacity=0.6)
    s.text(cx, 16, 'corda de aço (ferromagnética)', 8.4, 'ink', weight=700)
    for ang in (-24, 0, 24):
        a = math.radians(90 - ang)
    s.arrow((cx - 6, 66), (cx - 6, 50), 'blue', 1.4, head=6); s.arrow((cx + 6, 66), (cx + 6, 50), 'blue', 1.4, head=6)
    s.text(cx + 48, 62, 'B no ímã', 8.2, 'blue', anchor='start', weight=700)
    # sinal
    x0 = W - 128
    pl = Plot(s, x0, 28, 118, 64, (0, 2), (-1.3, 1.3), xticks=[], yticks=[], xlabel='tempo', ylabel='', grid=False, xlab_dy=18)
    t = np.linspace(0, 2, 200)
    pl.curve(t, np.sin(2 * math.pi * 3 * t) * np.exp(-0.4 * t), 'purple', 2.0)
    s.text(x0 + 59, 20, 'ε na bobina', 8.6, 'purple', weight=700)
    s.text(8, H - 20, 'a corda vibra: o fluxo na bobina varia e a FEM tem a', 8.4, 'ink', anchor='start', weight=700)
    s.text(8, H - 8, 'frequência da corda; corda de náilon: sem sinal', 8.4, 'ink', anchor='start')
    s.save()
    return s


# ======================================================================================= p26 · ressonância magnética (esquema)
def mri_scheme(W=336, H=170):
    s = Svg(W, H, 'mri_scheme')
    # corpo do equipamento (corte longitudinal)
    s.rect(14, 22, 230, 110, 8, fill='#EEF1F5', stroke='gray', sw=1.6)
    s.rect(30, 46, 198, 62, 0, fill='white', stroke='gray', sw=1.2)
    for x in range(30, 230, 14):
        s.sym_out((x + 7, 34), 4.2, 'orange', 1.2); s.sym_in((x + 7, 120), 4.2, 'orange', 1.2)
    s.text(129, 14, 'ímã supercondutor (solenoide)', 8.4, 'orange', weight=700)
    # paciente (silhueta)
    s.rect(52, 70, 150, 16, 8, fill='#D9DEE6', stroke='gray', sw=1.0)
    s.circle((60, 78), 11, fill='#D9DEE6', stroke='gray', w=1.0)
    # B0 ao longo do eixo
    for yy in (56, 98):
        s.arrow((34, yy), (222, yy), 'blue', 1.6, head=7, opacity=0.8)
    s.vtext(236, 58, 'B', sub='0', size=11.5, color='blue', plate=True)
    # bobina de RF (roxa: detecta por indução)
    s.rect(108, 62, 54, 34, 0, fill='none', stroke='purple', sw=2.0, dash='5 3')
    s.text(135, 112, 'bobina de RF', 8.2, 'purple', weight=700)
    s.text(135, 150, 'gradientes: B varia com a posição', 8.2, 'gray')
    # legenda lateral
    x0 = 254
    for i, (t, c) in enumerate((('1 alinha', 'blue'), ('2 pulso RF', 'purple'), ('3 sinal RF', 'purple'), ('4 imagem', 'green'))):
        s.text(x0, 54 + i * 16, t, 8.6, c, anchor='start', weight=700)
    s.text(x0, 130, 'sem radiação', 8.2, 'ink', anchor='start'); s.text(x0, 141, 'ionizante', 8.2, 'ink', anchor='start')
    s.save()
    return s


# ======================================================================================= p26 · levitação magnética (esquema)
def maglev(W=336, H=150):
    s = Svg(W, H, 'maglev')
    # via (trilho ferromagnético acima), eletroímãs do veículo abaixo
    s.rect(30, 20, 276, 14, 0, fill='#C3CBD6', stroke='gray', sw=1.4)
    s.text(168, 12, 'via (ferromagnética)', 8.4, 'gray', weight=700)
    s.rect(54, 52, 228, 34, 6, fill='#EEF1F5', stroke='ink', sw=1.6)
    s.text(168, 74, 'veículo', 10, 'ink', weight=700)
    for x in (80, 256):
        s.rect(x - 12, 40, 24, 12, 0, fill='orange', stroke='orange', sw=1.0)
        s.arrow((x, 52), (x, 28), 'green', 3.0, head=9)
    s.vtext(106, 46, 'F', sub='mag', size=11, color='green', plate=True)
    s.arrow((168, 86), (168, 120), 'ink', 3.0, head=9)
    s.vtext(184, 112, 'P', size=11.5, color='ink')
    s.arrow((290, 69), (326, 69), 'cyan', 2.6, head=9)
    s.vtext(316, 62, 'v', size=11, color='cyan', anchor='middle')
    s.line((54, 34), (54, 40), 'gray', 1.0)
    s.text(8, H - 16, 'esquema simplificado (atração, EMS): a corrente dos eletroímãs', 8.2, 'ink', anchor='start')
    s.text(8, H - 5, 'é regulada para manter a folga entre o veículo e a via.', 8.2, 'ink', anchor='start')
    s.save()
    return s


# ======================================================================================= p27 · mapa de fenômenos
def phenomena_map(W=336, H=190):
    s = Svg(W, H, 'phenomena_map')
    nodes = {'I': (64, 38, 'Corrente I', 'orange'), 'B': (272, 38, 'Campo B', 'blue'), 'F': (272, 150, 'Força / torque', 'green'), 'E': (64, 150, 'FEM ε / I induzida', 'purple')}
    for key, (x, y, t, c) in nodes.items():
        s.rect(x - 52, y - 16, 104, 32, 6, fill=c, stroke=c, sw=1.6)
        s.text(x, y + 4, t, 9.2, c if c != 'orange' else 'orange', weight=700)
    s.arrow((118, 38), (218, 38), 'ink', 2.0, head=8)
    s.text(168, 30, 'Oersted/Ampère', 8.2, 'ink', weight=700); s.text(168, 52, 'I cria B', 8.2, 'gray')
    s.arrow((272, 56), (272, 132), 'ink', 2.0, head=8)
    s.text(280, 86, 'Lorentz', 8.2, 'ink', anchor='start', weight=700); s.text(280, 98, 'B age sobre I', 8.2, 'gray', anchor='start'); s.text(280, 110, 'motor', 8.2, 'green', anchor='start', weight=700)
    s.arrow((218, 150), (118, 150), 'ink', 2.0, head=8)
    s.text(168, 142, 'Faraday', 8.2, 'ink', weight=700); s.text(168, 164, 'ΔΦ/Δt induz ε', 8.2, 'gray')
    s.text(168, 176, 'gerador, transformador', 8.2, 'purple', weight=700)
    s.arrow((64, 132), (64, 56), 'ink', 2.0, head=8)
    s.text(56, 86, 'Lenz', 8.2, 'ink', anchor='end', weight=700); s.text(56, 98, 'I′ se opõe', 8.2, 'gray', anchor='end'); s.text(56, 110, 'à variação', 8.2, 'gray', anchor='end')
    s.save()
    return s


# ======================================================================================= p27 · fluxograma de decisão
def decision_flowchart(W=680, H=262):
    s = Svg(W, H, 'decision_flowchart')
    s.rect(W / 2 - 90, 4, 180, 24, 6, fill='navy', stroke='navy', sw=1.6)
    s.text(W / 2, 20, 'O que a questão pede?', 10.5, 'navy', weight=800)
    fam = [
        ('CAMPO B (fontes)', 'blue', [
            ('sentido de B (corrente → campo)', '1ª regra da mão direita'),
            ('B de 1 fio longo', 'B = μ_{0}I/(2πr)'),
            ('B no centro de espira / bobina', 'B = Nμ_{0}I/(2R)'),
            ('B no interior de solenoide', 'B = μ_{0}nI,  n = N/L'),
            ('vários fios; simetria', 'soma VETORIAL; Ampère')]),
        ('FORÇA MAGNÉTICA', 'green', [
            ('força sobre carga', 'F = q v × B;  |q|vB sen θ'),
            ('trajetória circular ou hélice', 'r = m v_{⊥}/(|q|B);  p = v_{∥}T'),
            ('força sobre fio / torque', 'F = BIL sen θ;  τ = NBIA sen φ'),
            ('força entre fios paralelos', 'B de um fio → força no outro'),
            ('(todas) sentido da força', 'v × B ou tapa; q < 0 inverte')]),
        ('INDUÇÃO E DISPOSITIVOS', 'purple', [
            ('fluxo', 'Φ = BA cos θ (θ com a NORMAL)'),
            ('FEM induzida / corrente', 'ε = −NΔΦ/Δt;  I = |ε|/R'),
            ('sentido da corrente', 'Lenz: oposição à VARIAÇÃO'),
            ('haste em trilhos', 'confira a geometria; ε = BLv'),
            ('gerador · transformador', 'ε_{máx} = NBAω;  U_{p}/U_{s} = N_{p}/N_{s}')])]
    cw, gap = 212, 16
    for k, (title, color, leaves) in enumerate(fam):
        x = 4 + k * (cw + gap)
        s.line((W / 2, 28), (W / 2, 36), 'gray', 1.4)
        s.line((x + cw / 2, 36), (W / 2, 36), 'gray', 1.4)
        s.line((x + cw / 2, 36), (x + cw / 2, 40), 'gray', 1.4)
        s.rect(x, 40, cw, 24, 6, fill=color, stroke=color, sw=1.8)
        s.text(x + cw / 2, 56, title, 9.6, color, weight=800)
        s.line((x + 10, 64), (x + 10, 64 + 5 * 38 - 24), 'gray', 1.2)
        for i, (q, a) in enumerate(leaves):
            y = 72 + i * 38
            s.line((x + 10, y + 14), (x + 20, y + 14), 'gray', 1.2)
            s.rect(x + 20, y, cw - 20, 32, 4, fill='white', stroke=color, sw=1.2)
            s.text(x + 28, y + 12, q, 8.2, 'gray', anchor='start')
            s.text(x + 28, y + 25, a, 8.8, 'ink', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p28 · figura do item de Lenz
def mini_lenz(W=240, H=88):
    s = Svg(W, H, 'mini_lenz')
    from svglib import Obl
    pole, appr = 'S', False
    Bext = -X_                                   # polo S voltado ao anel: linhas entram no ímã
    Bind = -Bext if appr else Bext
    assert Bind[0] < 0                           # B_ind aponta para o ímã => anti-horário visto do lado do ímã
    c = Obl(0.8, 24, 1.0, 170, 46)
    ring = [c.P((0, 26 * math.sin(t), 26 * math.cos(t))) for t in np.linspace(0, 2 * math.pi, 90)]
    s.polyline(ring, 'orange', 2.4)
    s.magnet(14, 36, 56, 20, n_left=True, size=11)         # N à esquerda, S voltado ao anel (direita)
    s.arrow((70, 28), (36, 28), 'cyan', 2.2, head=8)
    s.vtext(54, 22, 'v', size=10.5, color='cyan', arrow=False, anchor='middle')
    s.text(W - 6, 14, 'observador do lado do ímã', 8, 'gray', anchor='end', weight=700)
    s.save()
    return s


if __name__ == '__main__':
    print('motor φ =', round(motor_section(), 1), '°')
    generator_two()
    print('ac emax, erms =', [round(v, 1) for v in ac_voltage()])
    motor_vs_gen(); transformer()
    print('transmissão:', transmission_chain())
    guitar_pickup(); mri_scheme(); maglev(); phenomena_map(); decision_flowchart(); mini_lenz()
