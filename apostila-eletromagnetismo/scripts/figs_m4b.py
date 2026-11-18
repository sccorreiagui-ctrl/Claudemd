"""Módulo IV (parte B) — aplicações de Lenz, haste móvel e plano inclinado (páginas 20 a 22).
Os sentidos de campo induzido e de corrente são deduzidos no código (Lenz + produtos vetoriais) e conferidos por asserts."""
import math
import numpy as np
from svglib import Svg, Obl, Plot, STROKE, num

X_, Y_, Z_ = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])


def lenz_Bind(Bext_dir, abs_flux_increasing):
    """regra de Lenz: B_ind se opõe à VARIAÇÃO de |Φ|."""
    return -Bext_dir if abs_flux_increasing else Bext_dir


# ======================================================================================= p20 · quatro casos
def lenz_four(W=680, H=214):
    s = Svg(W, H, 'lenz_four')
    pw = W / 4
    cases = [('N', True, 'polo N se aproxima'), ('N', False, 'polo N se afasta'), ('S', True, 'polo S se aproxima'), ('S', False, 'polo S se afasta')]
    table = []
    for k, (pole, appr, title) in enumerate(cases):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 16, title, 9.2, 'navy', weight=700)
        # B_ext no anel: de N para fora do ímã (+x); para S, em direção ao ímã (−x)
        Bext = X_ if pole == 'N' else -X_
        Bind = lenz_Bind(Bext, appr)
        # sentido da corrente: ψ crescente  ⇒  B = −x  (anti-horário visto do lado do ímã); ψ decrescente ⇒ B = +x
        sense = +1 if Bind[0] < 0 else -1
        ccw = sense > 0
        ring_face = 'N' if Bind[0] < 0 else 'S'                       # face voltada para o ímã (−x)
        repels = (ring_face == pole)
        assert repels == appr                                           # repele na aproximação, atrai no afastamento
        table.append((title, 'anti-horário' if ccw else 'horário', ring_face, 'repulsão' if repels else 'atração'))
        c = Obl(0.8, 24, 1.0, x0 + 138, 96)
        R = 30.0
        # anel (plano yz) — frente/trás
        ring = [c.P((0, R * math.sin(t), R * math.cos(t))) for t in np.linspace(0, 2 * math.pi, 100)]
        s.polyline(ring, 'orange', 2.6)
        for psi_deg in (50, 230):
            ps = math.radians(psi_deg)
            tang = sense * np.array([0, math.cos(ps), -math.sin(ps)])              # d/dψ de (R sinψ, R cosψ)
            p = np.array([0, R * math.sin(ps), R * math.cos(ps)])
            # confere por produto vetorial: r × t aponta para −x se ψ cresce
            assert (np.cross(p, tang)[0] < 0) == (Bind[0] < 0)
            q0, q1 = c.P(p - 5 * tang), c.P(p + 4 * tang)
            s._head(q0, q1, 'orange', 9, None, 2.6)
        # ímã (à esquerda); polo voltado para o anel
        mx = x0 + 40 if appr else x0 + 12
        mw, mh = 54, 20
        s.magnet(mx, 86, mw, mh, n_left=not (pole == 'N'), size=11)        # o polo voltado ao anel fica à direita
        if appr:
            s.arrow((mx + 4, 74), (mx + 4 + 34, 74), 'cyan', 2.2, head=8)
        else:
            s.arrow((mx + 40, 74), (mx + 6, 74), 'cyan', 2.2, head=8)
        s.vtext(mx + 22, 68, 'v', size=10.5, color='cyan', anchor='middle', arrow=False)
        # B_ext e B_ind no centro do anel
        cc = c.P((0, 0, 0))
        s.arrow((cc[0] - 18 * Bext[0] * -1 if False else cc[0], cc[1] + 52), (cc[0] + 28 * Bext[0], cc[1] + 52), 'blue', 2.2, head=8) if False else None
        yb = 150
        s.arrow((x0 + pw / 2 - 18 * Bext[0], yb), (x0 + pw / 2 + 18 * Bext[0], yb), 'blue', 2.4, head=8.5)
        s.text(x0 + 10, yb + 4, 'B_{ext}', 8.8, 'blue', anchor='start', weight=700)
        s.arrow((x0 + pw / 2 - 18 * Bind[0], yb + 18), (x0 + pw / 2 + 18 * Bind[0], yb + 18), 'purple', 2.4, head=8.5, dash='4 3')
        s.text(x0 + 10, yb + 22, 'B_{ind}', 8.8, 'purple', anchor='start', weight=700)
        s.text(x0 + pw - 10, yb + 4, '|Φ| ' + ('aumenta' if appr else 'diminui'), 8.4, 'ink', anchor='end', weight=700)
        s.text(x0 + pw / 2 + 8, 196, ('corrente ' + ('anti-horária' if ccw else 'horária') + ' (lado do ímã)'), 8.2, 'orange', weight=700)
        ix, iy = x0 + 14, 194
        s.circle((ix, iy), 7, fill='none', stroke='orange', w=1.6)
        aa = math.radians(60); sg2 = 1 if ccw else -1
        s._head((ix + 7 * math.cos(aa) + sg2 * math.sin(aa) * 3, iy - 7 * math.sin(aa) + sg2 * math.cos(aa) * 3), (ix + 7 * math.cos(aa) - sg2 * math.sin(aa) * 3, iy - 7 * math.sin(aa) - sg2 * math.cos(aa) * 3), 'orange', 6, None, 1.6) if False else None
        s.text(x0 + pw / 2, 207, ('face do anel: ' + ring_face + ' → ' + ('repele' if repels else 'atrai') + ' o ímã'), 8.2, 'red', weight=700)
    s.save()
    return table


# ======================================================================================= p20 · anel parado, B(t) varia
def lenz_stationary(W=680, H=140):
    s = Svg(W, H, 'lenz_stationary')
    pw = W / 4
    cases = [(-Z_, True, 'B entrando, aumenta'), (-Z_, False, 'B entrando, diminui'), (Z_, True, 'B saindo, aumenta'), (Z_, False, 'B saindo, diminui')]
    out = []
    for k, (Bext, inc, title) in enumerate(cases):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 16, title, 9.2, 'navy', weight=700)
        Bind = lenz_Bind(Bext, inc)
        ccw = Bind[2] > 0                                            # ⊙ no interior ⇒ anti-horário (mão direita)
        out.append(('anti-horária' if ccw else 'horária'))
        cx, cy, R = x0 + pw / 2, 74, 34
        s.symgrid(x0 + 14, 30, x0 + pw - 14, 118, 26, 26, 'in' if Bext[2] < 0 else 'out', 'blue', r=4.6 if inc else 3.6, w=1.1, opacity=0.5, skip=lambda x, y: math.hypot(x - cx, y - cy) < R + 4)
        s.circle((cx, cy), R, fill='none', stroke='orange', w=2.8)
        sgn = 1 if ccw else -1
        for ang in (60, 240):
            a = math.radians(ang)
            tx, ty = -math.sin(a) * sgn, -math.cos(a) * sgn
            P = (cx + R * math.cos(a), cy - R * math.sin(a))
            s._head((P[0] - tx * 5, P[1] - ty * 5), (P[0] + tx * 3, P[1] + ty * 3), 'orange', 9, None, 2.6)
        (s.sym_out if Bind[2] > 0 else s.sym_in)((cx, cy), 8.5, 'purple', 2.0)
        s.text(cx, cy + R + 22, 'corrente ' + ('anti-horária' if ccw else 'horária'), 8.4, 'orange', weight=700)
    s.save()
    return out


# ======================================================================================= p21 · haste móvel
def moving_rod(W=336, H=186):
    s = Svg(W, H, 'moving_rod')
    xl, xr, yt, yb = 56, 316, 34, 134
    xr_rod = 206
    L = yb - yt
    v, B = X_.copy(), -Z_
    drive = np.cross(v, B)                       # força sobre cargas positivas: v × B
    assert np.allclose(drive, Y_)                # corrente na haste sobe
    F = np.cross(drive, B)                       # I L × B  (L ∥ corrente)
    assert np.allclose(F, -X_)                   # freia a haste
    s.symgrid(xl + 22, yt + 16, xr_rod - 12, yb - 10, 30, 28, 'in', 'blue', r=4.6, w=1.1, opacity=0.5, skip=lambda x, y: 118 < x < 200 and 94 < y < 124)
    s.symgrid(xr_rod + 18, yt + 16, xr - 16, yb - 10, 30, 28, 'in', 'blue', r=4.6, w=1.1, opacity=0.22)
    s.line((xl, yt), (xr, yt), 'ink', 2.4); s.line((xl, yb), (xr, yb), 'ink', 2.4)
    s.resistor((xl, yt), (xl, yb), n=5, amp=6.5, color='ink', w=2.2)
    s.text(xl - 9, (yt + yb) / 2 + 3, 'R', 11, 'ink', anchor='end', weight=700)
    s.line((xr_rod, yt - 4), (xr_rod, yb + 4), 'gray', 6.0)
    s.circle((xr_rod, yt), 3.4, fill='gray', stroke='white', w=1.0); s.circle((xr_rod, yb), 3.4, fill='gray', stroke='white', w=1.0)
    s.arrow((xr_rod + 8, (yt + yb) / 2), (xr_rod + 50, (yt + yb) / 2), 'cyan', 3.0, head=10)
    s.vtext(xr_rod + 62, (yt + yb) / 2 + 5, 'v', size=12.5, color='cyan', plate=True)
    s.arrow((xr_rod - 8, (yt + yb) / 2 + 24), (xr_rod - 46, (yt + yb) / 2 + 24), 'green', 3.0, head=10)
    s.vtext(xr_rod - 58, (yt + yb) / 2 + 28, 'F', sub='mag', size=11.5, color='green', plate=True)
    # corrente anti-horária: sobe na haste, vai para a esquerda em cima, desce em R, volta pela base
    s.arrow((xr_rod - 4, yb - 14), (xr_rod - 4, yt + 18), 'orange', 2.6, head=8.5) if False else None
    s.arrow((xr_rod - 12, yt), (xr_rod - 60, yt), 'orange', 2.6, head=8.5)
    s.arrow((xl + 40, yb), (xl + 92, yb), 'orange', 2.6, head=8.5)
    s.arrow((xl, yt + 14), (xl, yt + 34), 'orange', 2.6, head=8.5) if False else None
    s.arrow((xr_rod - 3, yb - 20), (xr_rod - 3, yb - 44), 'orange', 2.6, head=8.5) if False else None
    s.vtext(xl + 66, yb + 15, 'I', size=11.5, color='orange', arrow=False)
    s.line((xr + 6, yt), (xr + 6, yb), 'gray', 1.0)
    s.line((xr + 2, yt), (xr + 10, yt), 'gray', 1.0); s.line((xr + 2, yb), (xr + 10, yb), 'gray', 1.0)
    s.text(xr + 6, (yt + yb) / 2 + 3, 'L', 10, 'gray', weight=700) if False else None
    s.text(xr - 6, (yt + yb) / 2 + 3, 'L', 10, 'gray', anchor='start', weight=700)
    s.line((xl, yb + 22), (xr_rod, yb + 22), 'gray', 1.0)
    s.line((xl, yb + 18), (xl, yb + 26), 'gray', 1.0); s.line((xr_rod, yb + 18), (xr_rod, yb + 26), 'gray', 1.0)
    s.text((xl + xr_rod) / 2, yb + 36, 'x (a área do circuito é A = L·x)', 8.4, 'gray', weight=700)
    s.text(8, 14, 'B entrando · haste com v para a direita', 8.8, 'navy', anchor='start', weight=700)
    s.text(W - 8, 14, 'ε = B L v', 10, 'purple', anchor='end', weight=700)
    s.text(W - 8, 26, 'corrente anti-horária', 8.4, 'orange', anchor='end', weight=700)
    s.save()
    return s



# ======================================================================================= p21 · leitura de Lorentz (separação de cargas na haste)
def rod_lorentz(W=336, H=112):
    s = Svg(W, H, 'rod_lorentz')
    v, B = X_.copy(), -Z_
    f_pos = np.cross(v, B)                        # força magnética por unidade de carga positiva: v × B
    assert np.allclose(f_pos, Y_)                 # cargas + sobem; elétrons descem
    E_in = -f_pos                                 # equilíbrio q E + q v × B = 0  ⇒  E = −v × B (aponta para baixo)
    assert np.allclose(E_in, -Y_)
    xr0, xr1, yt, yb = 44.0, 68.0, 12.0, 100.0
    s.symgrid(8, 14, 150, 100, 28, 26, 'in', 'blue', r=4.2, w=1.0, opacity=0.3,
              skip=lambda x, y: (xr0 - 14 < x < xr1 + 12) or (xr1 + 6 < x < 140 and 44 < y < 68))
    s.rect(xr0, yt, xr1 - xr0, yb - yt, 5, fill='#D9DEE6', stroke='gray', sw=1.4)
    for yy in (26, 38):
        s.text((xr0 + xr1) / 2, yy + 4, '+', 13, 'red', weight=700)
    for yy in (72, 84):
        s.text((xr0 + xr1) / 2, yy + 4, '−', 13, 'red', weight=700)
    s.circle(((xr0 + xr1) / 2, 61), 5.4, fill='white', stroke=STROKE['red'], w=1.3)
    s.text((xr0 + xr1) / 2, 64.6, '+', 9, 'red', weight=700)
    s.arrow(((xr0 + xr1) / 2, 54), ((xr0 + xr1) / 2, 44), 'green', 2.4, head=7)
    s.arrow((xr1 + 8, 56), (xr1 + 46, 56), 'cyan', 2.8, head=9.5)
    s.vtext(xr1 + 58, 61, 'v', size=12, color='cyan', plate=True)
    s.arrow((xr0 - 10, 34), (xr0 - 10, 80), 'ink', 1.8, head=7)
    s.vtext(xr0 - 20, 60, 'E', size=11.5, color='ink')
    x0 = 160.0
    s.text(x0, 20, 'Leitura de Lorentz', 9.4, 'navy', anchor='start', weight=700)
    s.text(x0, 36, 'q v × B: cargas + sobem, elétrons descem', 8.4, 'green', anchor='start', weight=700)
    s.text(x0, 52, 'topo (+) e base (−): surge E para baixo', 8.4, 'red', anchor='start', weight=700)
    s.text(x0, 68, 'equilíbrio: q E = q v B  ⇒  E = v B', 8.4, 'ink', anchor='start')
    s.text(x0, 86, 'ε = E L = B L v', 10, 'purple', anchor='start', weight=700)
    s.save()
    return s

# ======================================================================================= p22 · rampa (vista lateral)
def incline_side(W=336, H=186):
    s = Svg(W, H, 'incline_side')
    alpha = math.radians(37)
    m, g, Bf, Ll, Rr = 0.10, 10.0, 1.25, 1.00, 1.00
    ca, sa = 0.8, 0.6
    vt = m * g * Rr * sa / (Bf ** 2 * Ll ** 2 * ca ** 2)
    I = Bf * Ll * vt * ca / Rr
    Fm = Bf * I * Ll
    P = m * g
    N = P * ca + Fm * sa
    assert abs(vt - 0.6) < 1e-9 and abs(I - 0.6) < 1e-9 and abs(Fm * ca - P * sa) < 1e-9
    sc = 44.0                                     # px por newton
    # rampa subindo para a direita
    ox, oy = 30, 172
    Lr = 250
    ex, ey = ox + Lr * math.cos(alpha), oy - Lr * math.sin(alpha)
    s.polygon([(ox, oy), (ex, oy), (ex, ey)], fill='#F1F3F6', stroke='gray', w=1.6)
    s.path(f'M {ox + 46} {oy} A 46 46 0 0 0 {ox + 46 * math.cos(alpha):.2f} {oy - 46 * math.sin(alpha):.2f}', stroke='gray', w=1.2)
    s.text(ox + 62, oy - 6, 'α = 37°', 9.2, 'gray', anchor='start', weight=700)
    # haste (seção circular) sobre a rampa
    tx, ty = math.cos(alpha), -math.sin(alpha)                      # ao longo da rampa (subindo), imagem
    nx, ny = -math.sin(alpha), -math.cos(alpha)                     # normal para fora (imagem)
    pos = (ox + 130 * math.cos(alpha), oy - 130 * math.sin(alpha))
    r = 8
    cpos = (pos[0] + nx * r, pos[1] + ny * r)
    s.circle(cpos, r, fill='#E4E8EE', stroke='ink', w=1.6)
    s.sym_in(cpos, 4.6, 'orange', 1.4, fill='none')
    # B vertical (azul) ao fundo
    for bx in (ox + 40, ox + 110):
        yy = oy - (bx - ox) * math.tan(alpha)
        s.arrow((bx, yy - 14), (bx, yy - 62), 'blue', 1.4, head=6.5, opacity=0.45)
    s.vtext(ox + 30, oy - 30 * math.tan(alpha) - 70, 'B', size=12, color='blue', plate=True)
    # forças em c: P (baixo), N (normal), F (horizontal, para a direita = lado alto)
    s.arrow(cpos, (cpos[0], cpos[1] + P * sc), 'ink', 2.6, head=9)
    s.vtext(cpos[0] + 8, cpos[1] + P * sc + 4, 'P', size=11.5, color='ink', arrow=True, anchor='start') if False else None
    s.arrow(cpos, (cpos[0] + nx * N * sc, cpos[1] + ny * N * sc), 'ink', 2.6, head=9)
    s.arrow(cpos, (cpos[0] + Fm * sc, cpos[1]), 'green', 3.0, head=10)
    # componentes: F cos α (ao longo), F sen α (perpendicular, para dentro da rampa) e P sen α (ao longo, para baixo)
    s.arrow(cpos, (cpos[0] + Fm * ca * sc * tx, cpos[1] + Fm * ca * sc * ty), 'green', 1.8, head=7, dash='4 3')
    s.arrow(cpos, (cpos[0] - P * sa * sc * tx, cpos[1] - P * sa * sc * ty), 'ink', 1.8, head=7, dash='4 3')
    s.vtext(cpos[0] + Fm * sc + 8, cpos[1] - 4, 'F', sub='mag', size=11, color='green', plate=True)
    s.vtext(cpos[0] + 14, cpos[1] + P * sc + 6, 'P', size=11, color='ink', plate=True)
    s.vtext(cpos[0] + nx * N * sc - 14, cpos[1] + ny * N * sc - 2, 'N', size=11, color='ink', plate=True)
    xt = ex + 10                                  # faixa livre à direita da rampa
    s.text(xt, 70, 'equilíbrio', 9.0, 'navy', anchor='start', weight=700)
    s.text(xt, 81, '(v constante)', 8.2, 'navy', anchor='start')
    s.text(xt, 99, 'P = 1,00 N', 8.2, 'ink', anchor='start')
    s.text(xt, 110, 'F = B I L = 0,75 N', 8.2, 'ink', anchor='start')
    s.text(xt, 121, 'N = 1,25 N', 8.2, 'ink', anchor='start')
    s.text(xt, 137, 'ao longo da rampa:', 8.2, 'green', anchor='start', weight=700)
    s.text(xt, 148, 'F cos α = P sen α', 8.2, 'green', anchor='start', weight=700)
    s.text(xt, 159, '= 0,60 N', 8.2, 'green', anchor='start', weight=700)
    s.save()
    return vt, I, Fm, N


# ======================================================================================= p22 · rampa (vista superior)
def incline_top(W=336, H=150):
    s = Svg(W, H, 'incline_top')
    xl, xr, yt, yb = 56, 304, 34, 112
    v_h = -X_                                    # componente horizontal da velocidade (descendo a rampa, para a esquerda)
    B = Z_                                       # B vertical, saindo da página na vista de cima
    drive = np.cross(v_h, B)
    assert np.allclose(drive, Y_)                # corrente na haste "sobe" na vista (horário visto de cima)
    s.symgrid(xl + 40, yt + 14, xr - 14, yb - 8, 34, 26, 'out', 'blue', r=4.6, w=1.1, opacity=0.5)
    s.line((xl, yt), (xr, yt), 'ink', 2.4); s.line((xl, yb), (xr, yb), 'ink', 2.4)
    s.resistor((xr, yt), (xr, yb), n=5, amp=6.5, color='ink', w=2.2)
    s.text(xr + 8, (yt + yb) / 2 + 4, 'R', 11, 'ink', anchor='start', weight=700)
    xrod = 150
    s.line((xrod, yt - 4), (xrod, yb + 4), 'gray', 6.0)
    s.arrow((xrod - 8, (yt + yb) / 2), (xrod - 50, (yt + yb) / 2), 'cyan', 3.0, head=10)
    s.vtext(xrod - 62, (yt + yb) / 2 + 5, 'v', size=12, color='cyan', plate=True)
    s.arrow((xrod + 14, yt), (xrod + 66, yt), 'orange', 2.6, head=8.5)
    s.arrow((xrod + 66, yb), (xrod + 14, yb), 'orange', 2.6, head=8.5)
    s.text(8, 14, 'vista de cima: B vertical (saindo da página)', 8.8, 'navy', anchor='start', weight=700)
    s.text(8, H - 22, 'a haste desce a rampa, a área aumenta,', 8.4, 'ink', anchor='start')
    s.text(8, H - 11, 'corrente horária (vista de cima)', 8.4, 'orange', anchor='start', weight=700)
    s.text(xr - 4, 14, 'resistor no alto da rampa', 8.2, 'gray', anchor='end') if False else None
    s.save()
    return s


# ======================================================================================= p22 · velocidade terminal
def v_terminal(W=336, H=150):
    s = Svg(W, H, 'v_terminal')
    vt, tau = 0.60, 0.10
    pl = Plot(s, 46, 14, W - 60, H - 52, (0, 0.5), (0, 0.72), xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.2, 0.4, 0.6],
              xlabel='tempo (s)', ylabel='v (m/s)', xlab_dy=30, ylab_dx=-34, xfmt=lambda v: num(v, 1), yfmt=lambda v: num(v, 1))
    t = np.linspace(0, 0.5, 300)
    # integração numérica (RK4) da equação do movimento como conferência
    def acc(vv):
        m, g, k = 0.10, 10.0, 1.0
        return g * 0.6 - (k / m) * vv
    vv, ts_, vs_ = 0.0, [0.0], [0.0]
    h = 0.0005
    for _ in range(int(0.5 / h)):
        k1 = acc(vv); k2 = acc(vv + h / 2 * k1); k3 = acc(vv + h / 2 * k2); k4 = acc(vv + h * k3)
        vv += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        ts_.append(ts_[-1] + h); vs_.append(vv)
    assert abs(np.interp(0.5, ts_, vs_) - vt * (1 - math.exp(-0.5 / tau))) < 1e-4
    pl.curve(t, vt * (1 - np.exp(-t / tau)), 'cyan', 2.4)
    s.line((pl.X(0), pl.Y(vt)), (pl.X(0.5), pl.Y(vt)), 'gray', 1.0, dash='4 3')
    s.text(pl.X(0.5) - 4, pl.Y(vt) - 6, 'v_{terminal} = 0,60 m/s', 8.4, 'gray', anchor='end', weight=700)
    pl.dot(tau, vt * (1 - math.exp(-1)), 'cyan')
    s.text(pl.X(tau) + 7, pl.Y(vt * (1 - math.exp(-1))) + 14, 'τ = 0,10 s: 63% de v_{terminal}', 8.2, 'cyan', anchor='start', weight=700)
    s.save()
    return s


if __name__ == '__main__':
    print('lenz_four:', lenz_four())
    print('lenz_stationary:', lenz_stationary())
    moving_rod(); rod_lorentz()
    print('incline (vt, I, F, N):', incline_side())
    incline_top(); v_terminal()
