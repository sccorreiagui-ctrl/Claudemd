"""Módulo III — Força magnética (páginas 10 a 15).
Todos os sentidos de força vêm de F = q (v × B) calculado com numpy; asserts garantem a coerência do desenho."""
import math
import numpy as np
from svglib import Svg, Cam, Plot, STROKE, num

X_, Y_, Z_ = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])   # direita, cima, saindo da página


def force(q, v, B):
    return q * np.cross(v, B)


# ======================================================================================= p10 · F × θ
def F_vs_theta(W=336, H=156):
    s = Svg(W, H, 'F_vs_theta')
    pl = Plot(s, 46, 12, W - 60, H - 52, (0, 180), (0, 1.12), xticks=[0, 30, 60, 90, 120, 150, 180], yticks=[0, 0.5, 1.0],
              xlabel='ângulo θ entre v e B (graus)', ylabel='F / F_{máx}', xlab_dy=30, ylab_dx=-34,
              yfmt=lambda v: num(v, 1), xfmt=lambda v: num(v, 0))
    th = np.linspace(0, 180, 361)
    pl.curve(th, np.sin(np.radians(th)), 'green', 2.4)
    for t in (30, 90, 150):
        pl.dot(t, math.sin(math.radians(t)), 'green')
    for t in (0, 180):
        pl.dot(t, 0.0, 'red')
    s.text(pl.X(90), pl.Y(1.0) - 8, 'θ = 90°: F máxima (v ⟂ B)', 8.4, 'green', weight=700, plate=True)
    s.text(pl.X(30) + 6, pl.Y(0.5) - 8, '30°: F = F_{máx}/2', 8.2, 'green', anchor='start', weight=700, plate=True) if False else None
    s.text(pl.X(8), pl.Y(0.0) - 8, 'v ∥ B: F = 0', 8.2, 'red', anchor='start', weight=700)
    s.text(pl.X(172), pl.Y(0.0) - 8, 'v ∥ B (oposto): F = 0', 8.2, 'red', anchor='end', weight=700)
    s.text(pl.X(30) - 5, pl.Y(0.5) - 6, '0,5', 8.2, 'green', anchor='end', weight=700)
    s.save()
    return s


# ======================================================================================= p10 · carga em B (θ)
def charge_in_B(W=336, H=150):
    s = Svg(W, H, 'charge_in_B')
    theta = math.radians(40)
    O = np.array([86.0, 110.0])
    v = np.array([math.cos(theta), math.sin(theta), 0.0]); B = X_.copy()
    Fv = force(+1, v, B)
    assert Fv[2] < 0                                   # q>0: F entra na página
    # campo B (azul) ao longo de +x
    for yy in (110, 70, 30):
        s.arrow((16, yy), (W - 16, yy), 'blue', 1.3, head=6.5, opacity=0.55 if yy != 110 else 1.0)
    s.vtext(W - 22, 104, 'B', size=12.5, color='blue', plate=True)
    # componentes de v
    L = 96
    tip = (O[0] + L * v[0], O[1] - L * v[1])
    s.line(O, (O[0] + L * v[0], O[1]), 'cyan', 1.4, dash='4 3'); s.line((O[0] + L * v[0], O[1]), tip, 'cyan', 1.4, dash='4 3')
    s.arrow(O, tip, 'cyan', 2.6, head=9)
    s.vtext(tip[0] + 10, tip[1] - 2, 'v', size=12.5, color='cyan', plate=True)
    s.text(O[0] + L * v[0] / 2, O[1] + 13, 'v cos θ  (∥ B)', 8.2, 'cyan', weight=700)
    s.text(tip[0] + 8, O[1] - L * v[1] / 2 + 14, 'v sen θ (⟂ B)', 8.2, 'cyan', anchor='start', weight=700)
    s.path(f'M {O[0] + 36} {O[1]} A 36 36 0 0 0 {O[0] + 36 * math.cos(theta):.2f} {O[1] - 36 * math.sin(theta):.2f}', stroke='gray', w=1.1)
    s.text(O[0] + 48, O[1] - 7, 'θ', 10.5, 'gray', weight=700)
    s.charge((O[0], O[1]), '+', 7.5, 'red')
    # F: ⊗ (entrando) para q > 0
    s.sym_in((O[0] - 38, O[1] - 38), 8.5, 'green', 2.0)
    s.vtext(O[0] - 56, O[1] - 36, 'F', size=12.5, color='green')
    s.text(O[0] - 38, O[1] - 54, 'F entrando na página (q > 0)', 8.2, 'green', anchor='start', weight=700) if False else None
    s.text(8, 15, 'F = |q| v B sen θ', 9.6, 'green', anchor='start', weight=700)
    s.text(8, 27, 'F ⟂ v e F ⟂ B', 8.4, 'green', anchor='start')
    s.save()
    return s


# ======================================================================================= p10 · desvio de um feixe de elétrons
def electron_beam(W=336, H=120):
    s = Svg(W, H, 'electron_beam')
    q, v, B = -1.0, X_.copy(), -Z_
    F = force(q, v, B)
    assert F[1] < 0                                    # elétron, B entrando: força para baixo
    x0, y0, w, Rc = 100.0, 54.0, 66.0, 230.0
    s.rect(x0, 14, w, H - 28, 0, fill='blue', stroke='blue', sw=1.0, dash='4 3')
    s.symgrid(x0 + 12, 28, x0 + w - 8, H - 24, 22, 22, 'in', 'blue', r=4.2, w=1.0, opacity=0.65)
    s.text(x0 + w / 2, 11, 'B entrando', 8.6, 'blue', weight=700)
    # canhão e anteparo
    s.rect(6, y0 - 10, 26, 20, 3, fill='gray', stroke='gray', sw=1.0)
    s.text(19, y0 + 4, 'e⁻', 9.5, 'white', weight=700)
    xs = 292
    s.line((xs, 18), (xs, H - 12), 'ink', 3.0)
    s.text(xs + 6, 14, 'tela', 8.2, 'gray', anchor='start')
    # trajetória: reta, arco (curva para baixo), reta
    phi = math.asin(w / Rc)
    arc = [(x0 + Rc * math.sin(t), y0 + Rc * (1 - math.cos(t))) for t in np.linspace(0, phi, 40)]
    xe, ye = arc[-1]
    yf = ye + (xs - xe) * math.tan(phi)
    s.line((32, y0), (x0, y0), 'cyan', 2.4)
    s.polyline(arc, 'cyan', 2.4)
    s.line((xe, ye), (xs, yf), 'cyan', 2.4)
    s.arrow_at([(32, y0), (x0, y0)], 0.55, 'cyan', 2.4, head=8)
    s.line((xe, y0), (xs, y0), 'gray', 1.2, dash='4 3')              # sem campo
    s.circle((xs, y0), 3.4, fill='gray', stroke='white', w=1.0)
    s.circle((xs, yf), 3.8, fill=STROKE['cyan'], stroke='white', w=1.0)
    s.text(xs - 8, y0 - 7, 'sem B', 8.2, 'gray', anchor='end')
    s.text(xs - 8, yf + 14, 'com B', 8.2, 'cyan', anchor='end', weight=700)
    s.arrow((x0 + 34, y0 + 4), (x0 + 34, y0 + 26), 'green', 2.6, head=8.5)
    s.vtext(x0 + 46, y0 + 24, 'F', size=11.5, color='green', plate=True)
    s.vtext(58, y0 - 8, 'v', size=11.5, color='cyan', plate=True)
    s.save()
    return s


# ======================================================================================= p11 · tríade da regra
def rule_triad(W=336, H=186):
    s = Svg(W, H, 'rule_triad')
    cam = Cam(az=-32, el=22, scale=66, ox=108, oy=122)
    O = np.zeros(3)
    v, B = X_.copy(), Y_.copy()
    Fv = force(+1, v, B)
    assert np.allclose(Fv, Z_)                         # v × B = +z (para o observador)
    pO = cam.P(O)
    for ax, lab in ((X_, 'x'), (Y_, 'y'), (Z_, 'z')):
        s.line(pO, cam.P(ax * 1.55), 'light', 1.0)
    s.arrow(pO, cam.P(v * 1.45), 'cyan', 3.0, head=10)
    s.arrow(pO, cam.P(B * 1.45), 'blue', 3.0, head=10)
    s.arrow(pO, cam.P(Fv * 1.45), 'green', 3.2, head=10)
    s.line(pO, cam.P(-Fv * 1.0), 'green', 2.0, dash='4 3')
    pv, pB, pF = cam.P(v * 1.45), cam.P(B * 1.45), cam.P(Fv * 1.45)
    s.vtext(pv[0] + 12, pv[1] + 4, 'v', size=13, color='cyan')
    s.vtext(pB[0] + 3, pB[1] - 9, 'B', size=13, color='blue')
    s.vtext(pF[0] - 14, pF[1] + 6, 'F', size=13, color='green')
    s.text(pF[0] - 30, pF[1] + 19, 'q > 0:  F ∥ v × B', 8.6, 'green', anchor='start', weight=700)
    pm = cam.P(-Fv * 1.0)
    s.text(pm[0] + 8, pm[1] + 4, 'q < 0: sentido oposto', 8.2, 'green', anchor='start', weight=700)
    # arco: dedos varrendo de v para B
    pts = [cam.P(0.55 * (math.cos(t) * v + math.sin(t) * B)) for t in np.linspace(0.12, math.pi / 2 - 0.12, 20)]
    s.carrow(pts, 'gray', 1.6, head=7)
    s.text(pO[0] + 40, pO[1] - 60, 'dedos: de v para B', 8.4, 'gray', anchor='start', weight=700)
    s.text(W - 6, 15, 'regra da mão direita (força)', 9.6, 'navy', anchor='end', weight=700)
    s.text(W - 6, 28, 'dedos ao longo de v, curvando-se', 8.4, 'ink', anchor='end')
    s.text(W - 6, 39, 'para B; o polegar dá v × B', 8.4, 'ink', anchor='end')
    s.text(W - 6, H - 8, 'eixos: x → direita, y → cima, z → você', 8, 'gray', anchor='end')
    s.save()
    return s


# ======================================================================================= p11 · quatro casos
def four_cases(W=680, H=112):
    s = Svg(W, H, 'four_cases')
    pw = W / 4
    cases = [(+1, -Z_, 'q > 0,  B entrando'), (+1, +Z_, 'q > 0,  B saindo'), (-1, -Z_, 'q < 0,  B entrando'), (-1, +Z_, 'q < 0,  B saindo')]
    v = X_.copy()
    out = []
    for k, (q, B, title) in enumerate(cases):
        Fv = force(q, v, B)
        up = Fv[1] > 0
        out.append('para cima' if up else 'para baixo')
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 17, title, 9, 'navy', weight=700)
        kind = 'in' if B[2] < 0 else 'out'
        s.symgrid(x0 + 14, 34, x0 + pw - 14, 100, 26, 22, kind, 'blue', r=4.4, w=1.1, opacity=0.45)
        cx, cy = x0 + pw / 2 - 12, 66
        s.charge((cx, cy), '+' if q > 0 else '−', 7.5, 'red')
        s.arrow((cx + 9, cy), (cx + 50, cy), 'cyan', 2.4, head=8.5)
        s.vtext(cx + 62, cy + 4, 'v', size=12, color='cyan', plate=True)
        dy = -1 if up else 1
        s.arrow((cx, cy + dy * 10), (cx, cy + dy * 36), 'green', 3.0, head=9.5)
        s.vtext(cx + 12, cy + dy * 32 + 4, 'F', size=12, color='green', plate=True)
    s.save()
    return out


# ======================================================================================= p11 · treino (6 painéis)
def force_drill(W=680, H=104):
    s = Svg(W, H, 'force_drill')
    pw = W / 6
    # (sinal de q, v, B) com v no plano; B no plano (±x, ±y) ou perpendicular (±z)
    cases = [(+1, X_, Y_), (-1, Y_, X_), (+1, -X_, Z_), (-1, X_, -Z_), (+1, -Y_, -Z_), (-1, Y_, Z_)]
    answers = []
    for k, (q, v, B) in enumerate(cases):
        F = force(q, v, B)
        if abs(F[2]) > 0.5:
            ans = 'saindo (⊙)' if F[2] > 0 else 'entrando (⊗)'
        else:
            ans = {(0, 1): 'para cima', (0, -1): 'para baixo', (1, 0): 'para a direita', (-1, 0): 'para a esquerda'}[(int(round(F[0])), int(round(F[1])))]
        answers.append(ans)
        x0 = pw * k
        s.rect(x0 + 4, 3, pw - 8, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + 12, 16, '(' + 'abcdef'[k] + ')', 9.4, 'navy', anchor='start', weight=700)
        cx, cy = x0 + pw / 2, 62
        if abs(B[2]) > 0.5:
            s.symgrid(x0 + 14, 30, x0 + pw - 14, 100, 24, 22, 'in' if B[2] < 0 else 'out', 'blue', r=4.2, w=1.1, opacity=0.5)
        else:
            for off in (-30, 0, 30):
                if abs(B[1]) > 0.5:
                    xx = cx + off * 1.4
                    s.arrow((xx, cy + 36 * (1 if B[1] < 0 else -1) * -1 if False else cy + 34), (xx, cy - 34), 'blue', 1.3, head=6, opacity=0.55) if B[1] > 0 else s.arrow((xx, cy - 34), (xx, cy + 34), 'blue', 1.3, head=6, opacity=0.55)
                else:
                    yy = cy + off * 1.0
                    s.arrow((cx - 44, yy), (cx + 44, yy), 'blue', 1.3, head=6, opacity=0.55) if B[0] > 0 else s.arrow((cx + 44, yy), (cx - 44, yy), 'blue', 1.3, head=6, opacity=0.55)
        s.charge((cx, cy), '+' if q > 0 else '−', 7.5, 'red')
        s.arrow((cx, cy), (cx + v[0] * 34, cy - v[1] * 34), 'cyan', 2.4, head=8.5)
    s.save()
    return answers


# ======================================================================================= p12 · órbita circular
def orbit(W=336, H=190):
    s = Svg(W, H, 'orbit')
    cx, cy, R = 122, 98, 58
    s.symgrid(14, 22, W - 14, H - 14, 30, 26, 'in', 'blue', r=4.6, w=1.1, opacity=0.30, skip=lambda x, y: math.hypot(x - cx, y - cy) < R + 24 or (x > W - 150 and y < 60))
    s.circle((cx, cy), R, fill='none', stroke='gray', w=1.4, dash='5 4')
    B = -Z_
    for ang in (20, 150, 260):
        a = math.radians(ang)
        pos = np.array([math.cos(a), math.sin(a), 0.0])
        v = np.array([-math.sin(a), math.cos(a), 0.0])            # anti-horário
        F = force(+1, v, B)
        assert np.allclose(F, -pos, atol=1e-9)                     # F aponta para o centro
        P = (cx + R * pos[0], cy - R * pos[1])
        s.arrow(P, (P[0] + 36 * v[0], P[1] - 36 * v[1]), 'cyan', 2.4, head=8.5)
        s.arrow(P, (P[0] + 34 * F[0], P[1] - 34 * F[1]), 'green', 2.8, head=9)
        s.charge(P, '+', 7.0, 'red')
    a = math.radians(20)
    s.vtext(cx + R * math.cos(a) + 36 * (-math.sin(a)) + 12, cy - R * math.sin(a) - 36 * math.cos(a) - 2, 'v', size=12, color='cyan', plate=True)
    s.vtext(cx + R * math.cos(a) - 34 * math.cos(a) - 4, cy - R * math.sin(a) + 34 * math.sin(a) + 20, 'F', size=12, color='green', plate=True)
    s.circle((cx, cy), 2.6, fill='ink', stroke=None)
    s.line((cx, cy), (cx + R * math.cos(math.radians(-45)), cy - R * math.sin(math.radians(-45))), 'gray', 1.2)
    s.text(cx + 20, cy + 33, 'r', 10.5, 'gray', weight=700)
    s.text(W - 6, 24, 'B entrando', 9, 'blue', anchor='end', weight=700, plate=True)
    s.text(W - 6, 36, 'q > 0: anti-horário', 8.4, 'ink', anchor='end', plate=True)
    s.text(W - 6, 48, 'q < 0: horário', 8.4, 'ink', anchor='end', plate=True)
    s.text(W - 6, H - 10, 'F = m v²/r  e  F = |q| v B', 8.4, 'green', anchor='end', weight=700, plate=True)
    s.save()
    return s


# ======================================================================================= p12 · espectrômetro
def spectrometer(W=336, H=170):
    s = Svg(W, H, 'spectrometer')
    x0, y0 = 240, 136                                       # fenda de entrada
    s.symgrid(18, 14, W - 18, 126, 28, 26, 'in', 'blue', r=4.4, w=1.1, opacity=0.30)
    s.line((14, y0), (W - 14, y0), 'ink', 3.0)
    s.text(W - 16, y0 + 14, 'detector', 8.2, 'gray', anchor='end')
    s.arrow((x0, y0 + 26), (x0, y0 + 4), 'cyan', 2.4, head=8.5)
    s.vtext(x0 + 14, y0 + 20, 'v', size=12, color='cyan')
    B = -Z_
    for r, lab, col in ((38, 'r₁', 'gray'), (62, 'r₂', 'gray')):
        # íons +: entram para cima, F = q v × B aponta para a esquerda (confere em v=+y)
        assert np.allclose(force(+1, Y_, B), -X_)
        pts = [(x0 - r + r * math.cos(t), y0 - r * math.sin(t)) for t in np.linspace(0, math.pi, 60)]
        s.polyline(pts, 'green', 2.2)
        s.arrow_at(pts, 0.5, 'green', 2.2, head=8)
        s.circle((x0 - 2 * r, y0), 3.4, fill=STROKE['red'], stroke='white', w=1.0)
    s.text(x0 - 38, y0 - 44, 'r₁', 9.5, 'gray', weight=700) if False else None
    s.text(x0 - 38 - 2, y0 - 38 - 8, 'íon mais leve', 8.2, 'green', weight=700, plate=True)
    s.text(x0 - 62 - 2, y0 - 62 - 8, 'íon mais pesado', 8.2, 'green', weight=700, plate=True)
    s.text(x0 - 76, y0 + 13, '2r₁', 8.4, 'ink', weight=700); s.text(x0 - 124, y0 + 13, '2r₂', 8.4, 'ink', weight=700)
    s.text(6, 14, 'espectrômetro de massa', 9.2, 'navy', anchor='start', weight=700)
    s.text(6, 26, 'mesma carga e velocidade:', 8.2, 'ink', anchor='start')
    s.text(6, 36, 'r = mv/(|q|B) ∝ m', 8.2, 'ink', anchor='start')
    s.save()
    return s


# ======================================================================================= p13 · trajetórias
def _helix_pts(r, vpar, omega, t0, t1, n=200):
    """hélice em torno do eixo x (B = +x), q > 0: (v∥·t, r sen ωt, r cos ωt)."""
    ts = np.linspace(t0, t1, n)
    return np.array([[vpar * t, r * math.sin(omega * t), r * math.cos(omega * t)] for t in ts])


def trajectories(W=680, H=172):
    from svglib import Obl
    s = Svg(W, H, 'trajectories')
    pw = W / 3
    titles = ['θ = 0° ou 180°: v ∥ B', 'θ = 90°: v ⟂ B', '0° < θ < 90°: hélice']
    for k in range(3):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 17, titles[k], 9.4, 'navy', weight=700)
    # (a) v ∥ B
    c = Obl(0.7, 24, 1.0, 26, 92)
    for off in (-22, 22):
        s.arrow(c.P((0, off, 0)), c.P((196, off, 0)), 'blue', 1.3, head=6.5, opacity=0.55)
    s.arrow(c.P((0, 0, 0)), c.P((160, 0, 0)), 'cyan', 2.6, head=9)
    s.charge(c.P((0, 0, 0)), '+', 7.0, 'red')
    s.vtext(c.P((160, 0, 0))[0] - 6, c.P((160, 0, 0))[1] - 11, 'v', size=12, color='cyan', plate=True)
    s.vtext(c.P((196, 22, 0))[0] - 4, c.P((196, 22, 0))[1] - 8, 'B', size=12, color='blue', plate=True)
    s.text(pw / 2, 146, 'F = 0: movimento retilíneo uniforme', 8.6, 'green', weight=700)
    # (b) v ⟂ B
    c2 = Obl(0.8, 24, 1.0, pw + 108, 92)
    r = 36.0
    ring = [c2.P((0, r * math.sin(t), r * math.cos(t))) for t in np.linspace(0, 2 * math.pi, 120)]
    s.polyline(ring, 'gray', 1.4, dash='5 4')
    s.arrow(c2.P((-62, 0, 0)), c2.P((84, 0, 0)), 'blue', 1.3, head=6.5, opacity=0.6)
    s.vtext(c2.P((84, 0, 0))[0] + 2, c2.P((84, 0, 0))[1] - 8, 'B', size=12, color='blue', plate=True)
    al = math.radians(60)
    pos = np.array([0.0, r * math.sin(al), r * math.cos(al)])
    v = np.array([0.0, math.cos(al), -math.sin(al)])
    F = force(+1, v, X_)
    assert np.allclose(F[1:], -np.array([math.sin(al), math.cos(al)]), atol=1e-9) and abs(F[0]) < 1e-12   # F aponta para o eixo
    P = c2.P(pos)
    s.arrow(P, c2.P(pos + 26 * v), 'cyan', 2.4, head=8.5)
    s.arrow(P, c2.P(pos + 26 * F), 'green', 2.6, head=9)
    s.charge(P, '+', 6.6, 'red')
    pv, pf = c2.P(pos + 26 * v), c2.P(pos + 26 * F)
    s.vtext(pv[0] + 10, pv[1] - 2, 'v', size=12, color='cyan', plate=True)
    s.vtext(pf[0] - 10, pf[1] + 12, 'F', size=12, color='green', plate=True)
    s.text(pw + pw / 2, 146, 'F centrípeta: movimento circular uniforme', 8.6, 'green', weight=700)
    # (c) hélice
    c3 = Obl(0.8, 24, 1.0, 2 * pw + 18, 96)
    rr, p_ = 24.0, 40.0                           # raio e passo (px)
    om = 2 * math.pi / p_
    pts3 = _helix_pts(rr, 1.0, om, 0, 3.4 * p_, 320)
    P3 = [c3.P(q) for q in pts3]
    s.polyline(P3, 'cyan', 1.8)
    s.arrow(c3.P((-6, 0, 0)), c3.P((196, 0, 0)), 'blue', 1.2, head=6.5, opacity=0.55)
    s.vtext(c3.P((196, 0, 0))[0] - 2, c3.P((196, 0, 0))[1] - 9, 'B', size=12, color='blue', plate=True)
    t_m = 2.28 * p_
    pm = np.array([t_m, rr * math.sin(om * t_m), rr * math.cos(om * t_m)])
    vm = np.array([1.0, rr * om * math.cos(om * t_m), -rr * om * math.sin(om * t_m)])
    Fm = force(+1, vm, X_)
    assert abs(np.dot(Fm, vm)) < 1e-9 and abs(Fm[0]) < 1e-12                # F ⟂ v e F ⟂ B
    vm_u = vm / np.linalg.norm(vm) * 30
    Fm_u = Fm / np.linalg.norm(Fm) * 24
    s.line(c3.P(pm), c3.P(pm + np.array([vm_u[0], 0, 0])), 'cyan', 1.1, dash='3 3')
    s.arrow(c3.P(pm), c3.P(pm + vm_u), 'cyan', 2.4, head=8.5)
    s.arrow(c3.P(pm), c3.P(pm + Fm_u), 'green', 2.6, head=9)
    s.charge(c3.P(pm), '+', 6.2, 'red')
    s.vtext(c3.P(pm + vm_u)[0] + 10, c3.P(pm + vm_u)[1] - 2, 'v', size=12, color='cyan', plate=True)
    s.vtext(c3.P(pm + Fm_u)[0] - 4, c3.P(pm + Fm_u)[1] + 15, 'F', size=12, color='green', plate=True)
    # vista ao longo de B: F ⟂ v⟂ (ângulo reto visível)
    ix, iy, ir = 2 * pw + 40, 52, 17
    s.circle((ix, iy), ir, fill='white', stroke='gray', w=1.2, dash='3 3')
    a2 = math.radians(40)
    vperp = np.array([-math.sin(a2), math.cos(a2)])                      # tangente no ponto (cos a2, sin a2)
    pt = (ix + ir * math.cos(a2), iy - ir * math.sin(a2))
    Fv2 = force(+1, np.array([0.0, vperp[0], vperp[1]]), X_)           # componentes (y, z) -> aqui só direção radial para o centro
    s.arrow(pt, (pt[0] + 15 * vperp[0], pt[1] - 15 * vperp[1]), 'cyan', 2.0, head=7)
    s.arrow(pt, (ix + 4 * math.cos(a2), iy - 4 * math.sin(a2)), 'green', 2.0, head=7)
    s.line((pt[0] - 6 * math.cos(a2) + 6 * vperp[0] * 0, pt[1] + 6 * math.sin(a2)), (pt[0] - 6 * math.cos(a2) + 6 * vperp[0], pt[1] + 6 * math.sin(a2) - 6 * vperp[1]), 'gray', 0.9)
    s.circle((ix, iy), 1.8, fill='ink', stroke=None)
    s.text(ix + 26, iy - 4, 'vista ao longo de B:', 7.8, 'gray', anchor='start')
    s.text(ix + 26, iy + 6, 'F ⟂ v⟂ (e F ⟂ B)', 7.8, 'gray', anchor='start')
    s.text(2 * pw + pw / 2, 146, 'v∥ (MRU) + v⟂ (MCU): movimento helicoidal', 8.6, 'green', weight=700)
    s.text(2 * pw + pw / 2, 160, 'F ⟂ v em todos os pontos da trajetória', 8.2, 'ink')
    s.save()
    return s


# ======================================================================================= p14 · fio entre os polos
def wire_poles(W=336, H=150):
    s = Svg(W, H, 'wire_poles')
    B, I = X_.copy(), -Z_
    F = np.cross(I, B)                                 # força sobre o fio: I × B
    assert np.allclose(F, -Y_)                         # para baixo
    cx, cy = W / 2, 74
    s.rect(20, 28, 54, 92, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.4)
    s.text(47, 82, 'N', 20, 'white', weight=700)
    s.rect(W - 74, 28, 54, 92, 0, fill='#FFFFFF', stroke=STROKE['red'], sw=1.6)
    s.text(W - 47, 82, 'S', 20, 'red', weight=700)
    for yy in (46, 74, 102):
        s.arrow((82, yy), (W - 82, yy), 'blue', 1.5, head=7, opacity=0.8)
    s.vtext(W / 2 + 70, 60, 'B', size=12.5, color='blue', plate=True)
    s.sym_in((cx, cy), 8.5, 'orange', 2.0)
    s.vtext(cx - 20, cy - 12, 'I', size=11.5, color='orange', arrow=False)
    s.arrow((cx, cy + 12), (cx, cy + 44), 'green', 3.2, head=10)
    s.vtext(cx + 14, cy + 40, 'F', size=12.5, color='green', plate=True)
    s.text(cx, 18, 'fio entre os polos de um ímã', 9, 'navy', weight=700)
    s.text(cx, H - 6, 'I entrando, B para a direita → F para baixo (F = I L × B)', 8.4, 'green', weight=700)
    s.save()
    return s


# ======================================================================================= p14 · fio inclinado
def wire_angle(W=336, H=140):
    s = Svg(W, H, 'wire_angle')
    th = math.radians(30)
    L_ = np.array([math.cos(th), math.sin(th), 0.0]); B = X_.copy()
    F = np.cross(L_, B)
    assert F[2] < 0                                    # entrando na página
    for yy in (24, 66, 108):
        s.arrow((12, yy), (W - 12, yy), 'blue', 1.3, head=6.5, opacity=0.55)
    s.vtext(W - 22, 60, 'B', size=12.5, color='blue', plate=True)
    O = (60, 108); ln = 170
    E = (O[0] + ln * L_[0], O[1] - ln * L_[1])
    s.line(O, E, 'orange', 3.4)
    s.arrow((O[0] + 100 * L_[0], O[1] - 100 * L_[1]), (O[0] + 150 * L_[0], O[1] - 150 * L_[1]), 'orange', 3.6, head=11)
    s.vtext(O[0] + 134 * L_[0] - 12, O[1] - 134 * L_[1] - 6, 'I', size=12, color='orange', arrow=False)
    s.line(O, (O[0] + ln * L_[0], O[1]), 'gray', 1.0, dash='3 3'); s.line((O[0] + ln * L_[0], O[1]), E, 'gray', 1.0, dash='3 3')
    s.path(f'M {O[0] + 44} {O[1]} A 44 44 0 0 0 {O[0] + 44 * math.cos(th):.2f} {O[1] - 44 * math.sin(th):.2f}', stroke='gray', w=1.1)
    s.text(O[0] + 56, O[1] - 7, 'θ', 10.5, 'gray', weight=700)
    M = (O[0] + ln * L_[0] / 2, O[1] - ln * L_[1] / 2)
    s.sym_in((M[0] - 18, M[1] - 30), 8.5, 'green', 2.0)
    s.vtext(M[0] - 2, M[1] - 27, 'F', size=12.5, color='green')
    s.text(E[0] + 6, O[1] + 12, 'comprimento efetivo: L sen θ', 8.2, 'gray', anchor='end') if False else None
    s.text(W - 8, H - 22, 'F = B I L sen θ', 9.6, 'green', anchor='end', weight=700, plate=True)
    s.text(W - 8, H - 10, 'F entrando na página (I × B)', 8.4, 'green', anchor='end', plate=True)
    s.save()
    return s


# ======================================================================================= p15 · fios paralelos
def parallel_wires(W=336, H=186):
    s = Svg(W, H, 'parallel_wires')
    out = []
    for k, (I2, title) in enumerate(((+Y_, 'mesmo sentido: ATRAÇÃO'), (-Y_, 'sentidos opostos: REPULSÃO'))):
        x0 = k * W / 2
        x1, x2, y0, y1 = x0 + 52, x0 + 122, 34, 150
        s.text(x0 + W / 4, 14, title, 8.8, 'navy', weight=700)
        I1 = +Y_
        # B1 no fio 2 (à direita do fio 1): I1 × r̂, com r̂ = +x
        B1 = np.cross(I1, X_)                          # −z (entrando)
        F2 = np.cross(I2, B1)                          # sobre o fio 2
        F1 = -F2                                       # 3ª lei
        attract = F2[0] < 0
        out.append('atração' if attract else 'repulsão')
        for xw, Id in ((x1, I1), (x2, I2)):
            sgn = 1 if Id[1] > 0 else -1
            s.arrow((xw, 92 + sgn * 54), (xw, 92 - sgn * 54), 'orange', 3.4, head=10)
        for yy in (52, 92, 132):
            (s.sym_in if B1[2] < 0 else s.sym_out)((x2 + 18, yy), 6.2, 'blue', 1.6)
        s.vtext(x2 + 36, 60, 'B', sub='1', size=11, color='blue')
        s.text(x2 + 27, 72, 'campo do', 7.4, 'blue'); s.text(x2 + 27, 81, 'fio 1', 7.4, 'blue')
        # forças (verdes)
        s.arrow((x1, 120), (x1 + 30 * np.sign(F1[0]), 120), 'green', 3.0, head=9)
        s.arrow((x2, 120), (x2 + 30 * np.sign(F2[0]), 120), 'green', 3.0, head=9)
        s.vtext(x1 + 15 * np.sign(F1[0]), 108, 'F', sub='1', size=11, color='green', anchor='middle')
        s.vtext(x2 + 15 * np.sign(F2[0]), 108, 'F', sub='2', size=11, color='green', anchor='middle')
        s.vtext(x1 - 14, 50, 'I', sub='1', size=11, color='orange', arrow=False)
        s.vtext(x2 - 14, 50, 'I', sub='2', size=11, color='orange', arrow=False)
        s.line((x1, 172), (x2, 172), 'gray', 1.0); s.line((x1, 168), (x1, 176), 'gray', 1.0); s.line((x2, 168), (x2, 176), 'gray', 1.0)
        s.text((x1 + x2) / 2, 184, 'd', 9.5, 'gray', weight=700)
    s.line((W / 2, 22), (W / 2, H - 8), 'faint', 1.0)
    s.save()
    return out


# ======================================================================================= p14 · fio em arco (força = corda)
def wire_arc(W=336, H=132):
    s = Svg(W, H, 'wire_arc')
    cx, cy, R = 120, 100, 52
    s.symgrid(14, 18, W - 14, H - 10, 28, 24, 'in', 'blue', r=4.2, w=1.0, opacity=0.30, skip=lambda x, y: x > 215 and y < 70)
    # integra dF = I dℓ × B ao longo do arco (sentido horário: da esquerda, por cima, até a direita)
    B = -Z_
    I = 3.0
    ts = np.linspace(math.pi, 0, 400)
    pts = np.array([[R * math.cos(t), R * math.sin(t), 0.0] for t in ts])
    dl = np.diff(pts, axis=0)
    Ftot = sum(I * np.cross(d, B) for d in dl) * 0.20      # B = 0,20 T
    chord = np.array([2 * R, 0.0, 0.0])
    assert np.allclose(Ftot / 0.20 / I, np.cross(chord, B), atol=1e-6)       # F = I (corda) × B
    assert Ftot[1] > 0                                                      # para cima
    arc = [(cx + R * math.cos(t), cy - R * math.sin(t)) for t in ts]
    s.polyline(arc, 'orange', 3.4)
    s.arrow_at(arc, 0.30, 'orange', 3.4, head=10)
    s.arrow_at(arc, 0.72, 'orange', 3.4, head=10)
    s.line((cx - R, cy), (cx + R, cy), 'gray', 1.3, dash='5 4')
    s.arrow((cx, cy - 6), (cx, cy - 40), 'green', 3.2, head=10)
    s.vtext(cx + 14, cy - 30, 'F', size=12.5, color='green', plate=True)
    s.line((cx - R, cy + 12), (cx + R, cy + 12), 'gray', 1.0)
    s.line((cx - R, cy + 8), (cx - R, cy + 16), 'gray', 1.0); s.line((cx + R, cy + 8), (cx + R, cy + 16), 'gray', 1.0)
    s.text(cx, cy + 25, 'corda = 2R', 8.8, 'gray', weight=700)
    s.text(cx - R - 8, cy - 14, 'I', size=11, color='orange') if False else None
    s.text(W - 8, 20, 'fio em arco, I = 3,0 A', 8.8, 'orange', anchor='end', weight=700)
    s.text(W - 8, 32, 'B = 0,20 T entrando', 8.6, 'blue', anchor='end', weight=700)
    s.text(W - 8, 44, 'F = B I (2R), para cima', 8.8, 'green', anchor='end', weight=700)
    s.save()
    return float(np.linalg.norm(Ftot))


# ======================================================================================= p15 · espira retangular perto de um fio
def loop_near_wire(W=336, H=168):
    s = Svg(W, H, 'loop_near_wire')
    sc = 11.0                                              # px por cm
    xw = 46.0
    a_cm, b_cm, L_cm = 2.0, 6.0, 10.0
    x_near, x_far = xw + a_cm * sc, xw + (a_cm + b_cm) * sc
    y_top, y_bot = 14.0, 14.0 + L_cm * sc
    xp0, xp1 = 196.0, W - 4.0                              # painel "forças à escala"
    s.symgrid(xw + 12, 12, xp0 - 8, y_bot + 12, 26, 24, 'in', 'blue', r=3.8, w=0.9, opacity=0.25,
              skip=lambda x, y: (x_near - 8 < x < x_far + 8 and y_top - 8 < y < y_bot + 8) or (x_far + 14 < x < x_far + 46 and y_top - 8 < y < y_bot + 8))
    s.arrow((xw, y_bot + 6), (xw, 6), 'orange', 3.6, head=10)
    s.vtext(xw - 14, 24, 'I', sub='1', size=11, color='orange', arrow=False)
    # espira (horária): lado próximo sobe, topo vai para a direita, lado distante desce, base vai para a esquerda
    sides = {'perto': (np.array([0, 1.0, 0]), (x_near, y_bot), (x_near, y_top)),
             'topo': (np.array([1.0, 0, 0]), (x_near, y_top), (x_far, y_top)),
             'longe': (np.array([0, -1.0, 0]), (x_far, y_top), (x_far, y_bot)),
             'base': (np.array([-1.0, 0, 0]), (x_far, y_bot), (x_near, y_bot))}
    B = -Z_                                                # campo do fio à direita dele: entrando
    res = {}
    for nm, (Id, p0, p1) in sides.items():
        res[nm] = np.cross(Id, B)
        s.arrow(p0, p1, 'orange', 2.6, head=8.5)
    assert res['perto'][0] < 0 and res['longe'][0] > 0 and res['topo'][1] > 0 and res['base'][1] < 0
    ym = (y_top + y_bot) / 2
    s.arrow((x_near, ym), (x_near - 16, ym), 'green', 2.6, head=7.5)          # só o sentido (comprimentos à escala no painel)
    s.arrow((x_far, ym), (x_far + 9, ym), 'green', 2.6, head=7.5)
    xm = (x_near + x_far) / 2
    s.arrow((xm, y_top), (xm, y_top - 12), 'green', 2.4, head=8)
    s.arrow((xm, y_bot), (xm, y_bot + 12), 'green', 2.4, head=8)
    s.vtext(xm + 10, ym + 14, 'I', sub='2', size=11, color='orange', arrow=False)
    # cotas
    yc = y_bot + 24
    for xa, xb, lab in ((xw, x_near, 'a'), (x_near, x_far, 'b')):
        s.line((xa, yc), (xb, yc), 'gray', 1.0); s.line((xa, yc - 3), (xa, yc + 3), 'gray', 1.0); s.line((xb, yc - 3), (xb, yc + 3), 'gray', 1.0)
        s.text((xa + xb) / 2, yc + 12, lab, 9, 'gray', weight=700)
    xl = x_far + 30
    s.line((xl, y_top), (xl, y_bot), 'gray', 1.0)
    s.line((xl - 4, y_top), (xl + 4, y_top), 'gray', 1.0); s.line((xl - 4, y_bot), (xl + 4, y_bot), 'gray', 1.0)
    s.text(xl + 11, ym + 3, 'L', 9, 'gray', weight=700)
    # painel: forças nos lados verticais, à escala (1,0×10^-4 N = 40 px)
    mu = 2e-7
    I1, I2, L, a, b = 20.0, 5.0, 0.10, 0.02, 0.06
    Fp = mu * I1 * I2 * L / a
    Fl = mu * I1 * I2 * L / (a + b)
    Fr = Fp - Fl
    assert abs(Fp - 1.0e-4) < 1e-12 and abs(Fl - 2.5e-5) < 1e-12 and abs(Fr - 7.5e-5) < 1e-12
    k = 40 / 1.0e-4
    s.rect(xp0, y_top - 6, xp1 - xp0, (y_bot - y_top) + 12, 5, fill='paper', stroke='light', sw=1.0)
    s.text((xp0 + xp1) / 2, y_top + 8, 'forças nos lados verticais (à escala)', 7.8, 'gray')
    xo = xp0 + 78
    s.line((xo, y_top + 18), (xo, y_bot - 4), 'light', 1.0, dash='3 3')
    rows = [(y_top + 36, 'F_{perto} = 1,0×10^{-4} N', -Fp * k, 'green', 2.8), (y_top + 66, 'F_{longe} = 2,5×10^{-5} N', +Fl * k, 'green', 2.8),
            (y_top + 96, 'resultante: 7,5×10^{-5} N (atração)', -Fr * k, 'green', 4.0)]
    for yy, lab, dx, col, wd in rows:
        s.text(xp0 + 6, yy - 8, lab, 8.2, 'green', anchor='start', weight=700)
        s.arrow((xo, yy), (xo + dx, yy), col, wd, head=8.5 if wd < 3.5 else 10)
    s.save()
    return mu * I1 * I2 * L * (1 / a - 1 / (a + b))


if __name__ == '__main__':
    F_vs_theta(); charge_in_B(); electron_beam(); rule_triad()
    print('four_cases:', four_cases())
    print('force_drill:', force_drill())
    orbit(); spectrometer(); trajectories(); wire_poles(); wire_angle()
    print('parallel_wires:', parallel_wires())
    print('wire_arc |F| (N):', wire_arc(), ' loop_near_wire F (N):', loop_near_wire())
