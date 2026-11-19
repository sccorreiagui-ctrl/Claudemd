"""Módulo II — Fontes de campo magnético (páginas 4 a 9).
Sentidos de B e de I são calculados por produto vetorial (numpy) — nenhuma seta é desenhada "de cabeça"."""
import math
import numpy as np
from svglib import Svg, Cam, Plot, STROKE, num
import fields as F


def circ3d(s, cam, center, radius, normal, color, w=1.3, n=120, arrow_t=0.311, I_dir=None, head=7.0):
    """círculo 3D em torno de um eixo; a seta segue I_dir × r (regra da mão direita). Parte de trás tracejada."""
    ax = {'y': ((1, 0, 0), (0, 0, 1)), 'x': ((0, 1, 0), (0, 0, 1)), 'z': ((1, 0, 0), (0, 1, 0))}[normal]
    u, v, c0 = np.array(ax[0], float), np.array(ax[1], float), np.array(center, float)
    pts = [c0 + radius * (math.cos(2 * math.pi * k / n) * u + math.sin(2 * math.pi * k / n) * v) for k in range(n + 1)]
    segs, cur, cur_front = [], [], None
    for p in pts:
        fr = cam.depth(p) >= cam.depth(c0)
        if cur_front is not None and fr != cur_front:
            cur.append(p); segs.append((cur_front, cur)); cur = [p]
        else:
            cur.append(p)
        cur_front = fr
    segs.append((cur_front, cur))
    for fr, sg in segs:
        P = [cam.P(p) for p in sg]
        if fr:
            s.polyline(P, color, w)
        else:
            s.polyline(P, color, w * 0.85, dash='3 3', opacity=0.7)
    t0 = 2 * math.pi * arrow_t
    p = c0 + radius * (math.cos(t0) * u + math.sin(t0) * v)
    tang = np.cross(np.array(I_dir, float), p - c0)
    tang /= np.linalg.norm(tang)
    s._head(cam.P(p - tang * radius * 0.14), cam.P(p), color, head, None, w)
    return cam.P(p), cam.P(p + tang)


# ======================================================================================= p04 · Oersted
def oersted(W=336, H=176):
    s = Svg(W, H, 'oersted')
    pw = W / 2
    for k in (0, 1):
        x0 = k * pw
        cx, cy = x0 + pw / 2, 92
        s.text(x0 + pw / 2, 13, ['1) sem corrente: agulha na direção N–S', '2) corrente para o norte'][k], 8.8, 'ink', weight=700)
        s.circle((cx, cy), 38, fill='white', stroke='gray', w=1.3)
        ang = 90 if k == 0 else 135
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        nx, ny = -uy, ux
        L, w_ = 30, 6.5
        s.polygon([(cx + ux * L, cy + uy * L), (cx + nx * w_, cy + ny * w_), (cx - nx * w_, cy - ny * w_)], fill=STROKE['red'], stroke=STROKE['red'], w=0.8)
        s.polygon([(cx - ux * L, cy - uy * L), (cx + nx * w_, cy + ny * w_), (cx - nx * w_, cy - ny * w_)], fill='#FFFFFF', stroke=STROKE['red'], w=1.2)
        s.circle((cx, cy), 2.0, fill='gray', stroke=None)
        if k == 0:
            s.line((cx, 24), (cx, H - 30), 'mid', 3.0)
        else:
            s.line((cx, H - 30), (cx, 24), 'orange', 3.4)
            s.arrow((cx, 62), (cx, 28), 'orange', 3.4, head=9)
            s.vtext(cx + 10, 44, 'I', size=12, color='orange', arrow=False)
        for lab, dx, dy in (('N', 0, -43), ('S', 0, 53), ('L', 49, 3.5), ('O', -49, 3.5)):
            s.text(cx + dx, cy + dy, lab, 9, 'gray', weight=700, plate=True)
    s.text(pw * 1.5, H - 6, 'a ponta N gira para o oeste (O)', 8.6, 'green', weight=700)
    s.text(pw * 0.5, H - 6, 'fio (sem corrente) acima da agulha', 8.6, 'gray')
    s.line((pw, 6), (pw, H - 6), 'faint', 1.0)
    s.save()
    return s


# ======================================================================================= p04 · 1ª regra da mão direita
def rhr1(W=336, H=190):
    s = Svg(W, H, 'rhr1')
    cam = Cam(az=22, el=24, scale=60, ox=100, oy=98)
    Iy = (0, 1, 0)
    s.line(cam.P((0, -1.2, 0)), cam.P((0, 1.3, 0)), 'orange', 3.6)
    s.arrow(cam.P((0, 0.8, 0)), cam.P((0, 1.45, 0)), 'orange', 3.6, head=10)
    tip = cam.P((0, 1.45, 0))
    s.vtext(tip[0] + 11, tip[1] + 6, 'I', size=13, color='orange', arrow=False)
    circ3d(s, cam, (0, 0.5, 0), 0.62, 'y', 'blue', 1.5, I_dir=Iy, head=8)
    p_arrow, _ = circ3d(s, cam, (0, -0.45, 0), 0.98, 'y', 'blue', 1.5, I_dir=Iy, head=8)
    # confere por cálculo: no ponto mais próximo do observador, o movimento na tela é para a DIREITA (anti-horário visto de cima)
    t0 = 2 * math.pi * 0.311
    p = np.array([0.98 * math.cos(t0), -0.45, 0.98 * math.sin(t0)])
    tg = np.cross(np.array(Iy, float), p - np.array([0, -0.45, 0]))
    assert cam.P(p + 0.1 * tg / np.linalg.norm(tg))[0] > cam.P(p)[0], 'sentido de B incoerente com a regra da mão direita'
    s.vtext(p_arrow[0] + 14, p_arrow[1] + 14, 'B', size=12.5, color='blue', plate=True)
    s.text(8, H - 22, 'polegar: sentido de I', 8.8, 'orange', anchor='start', weight=700)
    s.text(8, H - 10, 'dedos curvados: sentido de B', 8.8, 'blue', anchor='start', weight=700)
    # cortes transversais
    cx0 = 262
    s.text(cx0, 14, 'visto de frente', 8.8, 'ink', weight=700)
    for j, kind in enumerate(('out', 'in')):
        cy = 54 + j * 84
        for r in (14, 28):
            s.circle((cx0, cy), r, fill='none', stroke='blue', w=1.3)
        Iz = np.array([0, 0, 1.0]) if kind == 'out' else np.array([0, 0, -1.0])
        for r in (14, 28):
            a_mid = math.radians(40)
            rv = np.array([math.cos(a_mid), math.sin(a_mid), 0.0])
            tg = np.cross(Iz, rv)
            sgn = 1 if tg[1] > 0 else -1                 # anti-horário (tg_y>0 no ponto a 40°) => ângulo cresce
            s.arc_arrow((cx0, cy), r, 40 - 16 * sgn, 40 + 16 * sgn, 'blue', 1.5, head=8.5)
        (s.sym_out if kind == 'out' else s.sym_in)((cx0, cy), 6.0, 'orange', 1.6)
        s.text(cx0, cy + 44, 'I saindo' if kind == 'out' else 'I entrando', 8.4, 'orange', weight=700)
    s.save()
    return s


# ======================================================================================= p04 · treino da regra (6 painéis)
def rhr_drill(W=680, H=104):
    """seis situações; o sentido de B em P é obtido por I × r (produto vetorial) e devolvido em ANSWERS."""
    s = Svg(W, H, 'rhr_drill')
    pw = W / 6
    # (direção de I, posição de P relativa ao fio, em unidades de 'x direita, y cima, z saindo')
    cases = [((0, 1, 0), (1, 0, 0)), ((0, -1, 0), (1, 0, 0)), ((1, 0, 0), (0, 1, 0)),
             ((-1, 0, 0), (0, 1, 0)), ((0, 0, 1), (1, 0, 0)), ((0, 0, -1), (0, 1, 0))]
    answers = []
    for k, (Idir, rel) in enumerate(cases):
        cx, cy = pw * k + pw / 2, 52
        B = np.cross(np.array(Idir, float), np.array(rel, float))
        if abs(B[2]) > 0.5:
            ans = 'saindo (⊙)' if B[2] > 0 else 'entrando (⊗)'
        else:
            ans = {(0, 1): 'para cima', (0, -1): 'para baixo', (1, 0): 'para a direita', (-1, 0): 'para a esquerda'}[(int(round(B[0])), int(round(B[1])))]
        answers.append(ans)
        s.rect(pw * k + 4, 4, pw - 8, H - 8, 4, fill='white', stroke='light', sw=1.0)
        s.text(pw * k + 12, 17, '(' + 'abcdef'[k] + ')', 9.4, 'navy', anchor='start', weight=700)
        if abs(Idir[2]) > 0.5:                         # fio perpendicular à página
            (s.sym_out if Idir[2] > 0 else s.sym_in)((cx, cy), 8, 'orange', 1.9)
            P = (cx + rel[0] * 36, cy - rel[1] * 36)
        else:
            L = 38
            a = (cx - Idir[0] * L, cy + Idir[1] * L)
            b = (cx + Idir[0] * L, cy - Idir[1] * L)
            s.arrow(a, b, 'orange', 3.2, head=9)
            P = (cx + rel[0] * 30, cy - rel[1] * 30)
        s.circle(P, 3.4, fill='ink', stroke=None)
        s.text(P[0] + (7 if rel[0] >= 0 else -7), P[1] + (4 if rel[1] <= 0 else -6), 'P', 9.4, 'ink', weight=700, anchor='start' if rel[0] >= 0 else 'end')
    s.save()
    return answers


# ======================================================================================= p05 · fio visto no plano
def wire_planar(W=336, H=150):
    s = Svg(W, H, 'wire_planar')
    cx = W / 2
    s.arrow((cx, H - 14), (cx, 10), 'orange', 3.6, head=10)
    s.vtext(cx + 11, 22, 'I', size=13, color='orange', arrow=False)
    sizes = {1: 8.6, 2: 6.6, 3: 5.4}
    for k, lab in ((1, 'r'), (2, '2r'), (3, '3r')):
        dx = 44 * k
        s.sym_in((cx + dx, 66), sizes[k], 'blue', 1.5)
        s.sym_out((cx - dx, 66), sizes[k], 'blue', 1.5)
        s.line((cx, 112), (cx + dx, 112), 'gray', 1.0)
        s.line((cx + dx, 108), (cx + dx, 116), 'gray', 1.0)
        s.text(cx + dx, 128, lab, 9, 'gray')
        s.text(cx + dx, 44, ['B', 'B/2', 'B/3'][k - 1], 9, 'blue', weight=700)
        s.text(cx - dx, 44, ['B', 'B/2', 'B/3'][k - 1], 9, 'blue', weight=700)
    s.text(cx + 100, 22, 'à direita:', 8.6, 'blue')
    s.text(cx + 100, 32, 'entrando no plano', 8.6, 'blue', weight=700)
    s.text(cx - 100, 22, 'à esquerda:', 8.6, 'blue')
    s.text(cx - 100, 32, 'saindo do plano', 8.6, 'blue', weight=700)
    s.save()
    return s


# ======================================================================================= p05 · corte do fio
def wire_xsec(W=336, H=160):
    s = Svg(W, H, 'wire_xsec')
    for k, kind in enumerate(('out', 'in')):
        cx, cy = W * (0.25 + 0.5 * k), 82
        s.text(cx, 13, ['I saindo da página', 'I entrando na página'][k], 9, 'orange', weight=700)
        Iz = np.array([0, 0, 1.0]) if kind == 'out' else np.array([0, 0, -1.0])
        for r in (30, 56):
            s.circle((cx, cy), r, fill='none', stroke='blue', w=1.2, opacity=0.55)
        for ang_deg in (0, 90, 180, 270):
            a = math.radians(ang_deg)
            rv = np.array([56 * math.cos(a), 56 * math.sin(a), 0.0])
            tg = np.cross(Iz, rv); tg /= np.linalg.norm(tg)
            P = (cx + rv[0], cy - rv[1])
            Q = (P[0] + tg[0] * 30, P[1] - tg[1] * 30)
            s.arrow(P, Q, 'blue', 2.2, head=8.5)
        (s.sym_out if kind == 'out' else s.sym_in)((cx, cy), 7.5, 'orange', 1.8)
        s.line((cx, cy), (cx + 30 * math.cos(math.radians(-40)), cy - 30 * math.sin(math.radians(-40))), 'gray', 1.0)
        s.text(cx + 7, cy + 24, 'r', 9.5, 'gray', weight=700)
    s.vtext(W * 0.25 + 56 + 8, 82 - 34, 'B', size=12, color='blue', plate=True)
    s.vtext(W * 0.75 - 56 - 10, 82 - 34, 'B', size=12, color='blue', plate=True)
    s.text(W * 0.25, H - 7, 'B em sentido anti-horário', 8.6, 'blue', weight=700)
    s.text(W * 0.75, H - 7, 'B em sentido horário', 8.6, 'blue', weight=700)
    s.save()
    return s


# ======================================================================================= p05 · B(r)
def B_vs_r(W=336, H=158):
    s = Svg(W, H, 'B_vs_r')
    pl = Plot(s, 46, 12, W - 60, H - 52, (0, 10.5), (0, 220), xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 50, 100, 150, 200],
              xlabel='distância ao fio, r (cm)', ylabel='B (μT)', xlab_dy=30, ylab_dx=-34)
    xs = np.linspace(0.9, 10.4, 200)
    pl.curve(xs, 2e-7 * 10 / (xs * 1e-2) * 1e6, 'blue', 2.2)
    s.line((pl.X(0), pl.Y(50)), (pl.X(10.5), pl.Y(50)), 'gray', 1.0, dash='4 3')
    s.text(pl.X(10.4), pl.Y(50) - 4, 'campo da Terra ≈ 50 μT', 8.2, 'gray', anchor='end')
    for r in (2, 4, 8):
        pl.dot(r, 2e-7 * 10 / (r * 1e-2) * 1e6, 'blue')
    s.text(pl.X(2) + 7, pl.Y(100) - 6, '2 cm: 100 μT', 8.2, 'blue', anchor='start', weight=700)
    s.text(pl.X(4) + 7, pl.Y(50) + 16, '4 cm: 50 μT', 8.2, 'blue', anchor='start', weight=700)
    s.text(pl.X(8) + 2, pl.Y(25) + 16, '8 cm: 25 μT', 8.2, 'blue', anchor='middle', weight=700)
    s.text(W - 8, 22, 'I = 10 A', 9, 'orange', anchor='end', weight=700)
    s.text(W - 8, 34, 'B = μ_{0}I/(2πr)', 9, 'ink', anchor='end')
    s.save()
    return s


# ======================================================================================= p06 · dois fios (exemplo)
def two_wires_ex(W=336, H=186):
    s = Svg(W, H, 'two_wires_ex')
    sc, x1, cy = 6.6, 112.0, 112.0
    X = lambda cm: x1 + sc * cm
    ppu = 0.75                                    # px por μT
    s.line((8, cy), (W - 8, cy), 'light', 1.0, dash='3 3')
    s.sym_out((X(0), cy), 7.5, 'orange', 1.8); s.sym_in((X(20), cy), 7.5, 'orange', 1.8)
    s.text(X(0), cy + 22, 'fio 1: 10 A, saindo', 8.6, 'orange', weight=700)
    s.text(X(20), cy + 22, 'fio 2: 30 A, entrando', 8.6, 'orange', weight=700)
    # P (x = 10 cm): B1 = 20 μT, B2 = 60 μT, ambos para cima
    P = (X(10), cy)
    s.circle(P, 3.4, fill='ink', stroke=None)
    s.text(P[0], cy + 36, 'P (x = 10 cm)', 8.6, 'ink', weight=700)
    s.arrow((P[0] - 18, cy - 4), (P[0] - 18, cy - 4 - 20 * ppu), 'blue', 1.6, head=6.5)
    s.arrow((P[0], cy - 4), (P[0], cy - 4 - 60 * ppu), 'blue', 1.6, head=6.5)
    s.arrow((P[0] + 20, cy - 4), (P[0] + 20, cy - 4 - 80 * ppu), 'blue', 2.8, head=9)
    s.vtext(P[0] - 18, cy - 4 - 20 * ppu - 6, 'B', sub='1', size=11, color='blue', plate=True)
    s.vtext(P[0] + 1, cy - 4 - 60 * ppu - 7, 'B', sub='2', size=11, color='blue', plate=True)
    s.vtext(P[0] + 20, cy - 4 - 80 * ppu - 7, 'B', sub='res', size=11, color='blue', plate=True)
    s.text(P[0] + 28, cy - 4 - 80 * ppu + 12, '80 μT', 8.2, 'blue', anchor='start', weight=700)
    # Q (x = −10 cm): B1 = 20 μT (baixo), B2 = 20 μT (cima)
    Q = (X(-10), cy)
    s.circle(Q, 3.4, fill='ink', stroke=None)
    s.arrow((Q[0] - 9, cy + 4), (Q[0] - 9, cy + 4 + 20 * ppu), 'blue', 1.6, head=6.5)
    s.arrow((Q[0] + 9, cy - 4), (Q[0] + 9, cy - 4 - 20 * ppu), 'blue', 1.6, head=6.5)
    s.vtext(Q[0] - 24, cy + 4 + 20 * ppu - 4, 'B', sub='1', size=11, color='blue')
    s.vtext(Q[0] + 24, cy - 4 - 20 * ppu + 4, 'B', sub='2', size=11, color='blue')
    s.text(Q[0], 26, 'Q (x = −10 cm): B = 0', 9.2, 'green', weight=700)
    s.text(Q[0], 38, 'B₁ e B₂ se anulam'.replace('B₁', 'B1').replace('B₂', 'B2'), 8.2, 'green')
    yb = cy + 56
    for a, b, lab in ((-10, 0, '10 cm'), (0, 20, '20 cm')):
        s.line((X(a), yb), (X(b), yb), 'gray', 1.0)
        s.line((X(a), yb - 3), (X(a), yb + 3), 'gray', 1.0); s.line((X(b), yb - 3), (X(b), yb + 3), 'gray', 1.0)
        s.text((X(a) + X(b)) / 2, yb + 12, lab, 8.2, 'gray')
    s.save()
    return s


# ======================================================================================= p06 · perfil By(x)
def By_profile(W=336, H=172):
    s = Svg(W, H, 'By_profile')
    pl = Plot(s, 46, 30, W - 60, H - 70, (-12, 12), (-200, 200), xticks=[-10, -5, 0, 5, 10], yticks=[-200, -100, 0, 100, 200],
              xlabel='posição x no plano dos fios (cm)', ylabel='B_{y} (μT)', xlab_dy=30, ylab_dx=-34)
    k, a = 2.0, 0.05                              # k = μ0 I/2π = 2 μT·m (I = 10 A); fios em ±5 cm
    xs = np.linspace(-0.12, 0.12, 3000)
    same = k * (1 / (xs + a) + 1 / (xs - a))      # ambos saindo: B_y = k/(x − x_i)
    opp = k * (1 / (xs + a) - 1 / (xs - a))       # esquerdo saindo, direito entrando
    pl.curve(xs * 100, same, 'blue', 2.0)
    pl.curve(xs * 100, opp, 'blue', 2.0, dash='5 3')
    for xv in (-5, 5):
        s.circle((pl.X(xv), pl.Y(0)), 4.0, fill='#FFF0DF', stroke=STROKE['orange'], w=1.4)
        s.text(pl.X(xv), pl.Y(0) + 16, 'fio', 7.8, 'orange')
    pl.dot(0, 0, 'green'); pl.dot(0, 2 * k / a, 'green')
    s.line((50, 10), (74, 10), 'blue', 2.0); s.text(79, 13.4, 'mesmo sentido: B = 0 no meio', 8.2, 'blue', anchor='start', weight=700)
    s.line((50, 22), (74, 22), 'blue', 2.0, dash='5 3'); s.text(79, 25.4, 'sentidos opostos: B dobra no meio', 8.2, 'blue', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p06 · três fios (exercício)
def three_wires(W=336, H=100):
    s = Svg(W, H, 'three_wires')
    sc, x0, cy = 8.0, 168.0, 42.0
    X = lambda cm: x0 + sc * cm
    s.line((16, cy), (W - 16, cy), 'light', 1.0, dash='3 3')
    s.sym_in((X(-10), cy), 7.5, 'orange', 1.8); s.sym_in((X(10), cy), 7.5, 'orange', 1.8)
    s.circle((X(0), cy), 7.5, fill='#FFF0DF', stroke=STROKE['orange'], w=1.8, dash='3 2')
    s.text(X(0), cy + 3.6, '?', 10, 'orange', weight=700)
    s.circle((X(5), cy), 3.4, fill='ink', stroke=None)
    s.text(X(5), cy - 12, 'P', 10, 'ink', weight=700)
    s.text(X(-10), cy - 14, '24 A', 8.8, 'orange', weight=700)
    s.text(X(10), cy - 14, '24 A', 8.8, 'orange', weight=700)
    s.text(X(0), cy - 14, 'I_{C}', 8.8, 'orange', weight=700)
    s.text(X(-10), cy + 22, 'A', 9, 'gray', weight=700); s.text(X(0), cy + 22, 'C', 9, 'gray', weight=700); s.text(X(10), cy + 22, 'D', 9, 'gray', weight=700)
    yb = cy + 40
    for a, b in ((-10, 0), (0, 5), (5, 10)):
        s.line((X(a), yb), (X(b), yb), 'gray', 1.0)
        s.line((X(a), yb - 3), (X(a), yb + 3), 'gray', 1.0); s.line((X(b), yb - 3), (X(b), yb + 3), 'gray', 1.0)
    s.text((X(-10) + X(0)) / 2, yb + 12, '10 cm', 8.2, 'gray'); s.text((X(0) + X(5)) / 2, yb + 12, '5 cm', 8.2, 'gray'); s.text((X(5) + X(10)) / 2, yb + 12, '5 cm', 8.2, 'gray')
    s.save()
    return s


# ======================================================================================= p06 · quatro fios num quadrado
def square_wires(W=232, H=118):
    s = Svg(W, H, 'square_wires')
    cx, cy, a = 78, 59, 34                      # centro e meio-lado (px)
    # correntes: topo saindo (+z), base entrando (−z); posições em (x, y) com y para cima
    wires = [((-1, 1), +1), ((1, 1), +1), ((1, -1), -1), ((-1, -1), -1)]
    s.rect(cx - a, cy - a, 2 * a, 2 * a, 0, fill='none', stroke='light', sw=1.0, dash='3 3')
    Bsum = np.zeros(2)
    I, d = 10.0, 0.05                           # 10 A; meio-lado 5,0 cm
    for (px, py), sgn in wires:
        r_vec = np.array([-px, -py, 0.0]) * d   # do fio até O
        B = 2e-7 * I / np.linalg.norm(r_vec) * np.cross(np.array([0, 0, sgn], float), r_vec / np.linalg.norm(r_vec))
        Bsum += B[:2]
        P = (cx + px * a, cy - py * a)
        (s.sym_out if sgn > 0 else s.sym_in)(P, 7, 'orange', 1.8)
        # vetor (escala: 1 μT = 0,7 px)
        v = B[:2] * 1e6 * 0.55
        s.arrow((cx, cy), (cx + v[0], cy - v[1]), 'blue', 1.5, head=6.5, opacity=0.85)
    assert abs(Bsum[0] - 8.0e-5) < 1e-9 and abs(Bsum[1]) < 1e-12, Bsum
    s.arrow((cx, cy), (cx + 8.0e-5 * 1e6 * 0.55, cy), 'blue', 2.8, head=9)
    s.circle((cx, cy), 2.6, fill='ink', stroke=None)
    s.text(cx - 9, cy + 15, 'O', 9.6, 'ink', weight=700)
    s.vtext(cx + 8.0e-5 * 1e6 * 0.55 + 8, cy - 5, 'B', size=12, color='blue', plate=True)
    s.text(W - 4, 16, 'topo: saindo', 8.4, 'orange', anchor='end', weight=700)
    s.text(W - 4, 28, 'base: entrando', 8.4, 'orange', anchor='end', weight=700)
    s.text(W - 4, 44, 'cada fio: 10 A', 8.4, 'ink', anchor='end')
    s.text(W - 4, 56, 'lado: 10 cm', 8.4, 'ink', anchor='end')
    s.text(W - 4, 72, 'B no centro:', 8.4, 'blue', anchor='end', weight=700)
    s.text(W - 4, 84, '80 μT →'.replace(' →', ', horizontal'), 8.4, 'blue', anchor='end', weight=700)
    s.save()
    return s


# ======================================================================================= p07 · espira (corte com linhas de campo)
def loop_section(W=336, H=184):
    s = Svg(W, H, 'loop_section')
    cx, cy = W / 2, H / 2 + 2
    a = 40.0
    field = F.make_planar(lambda rho, z: F.loop_B(rho, z, a))
    to_img = lambda xp, z: (cx + z, cy - xp)          # B ao longo de +z aponta para a direita
    bnd = (-(H / 2 - 6), (H / 2 - 6), -(W / 2 - 6), (W / 2 - 6))
    for r0 in (0.2 * a, 0.45 * a, 1.5 * a, 2.1 * a):
        for sg in (+1, -1):
            pts, _ = F.full_line(field, (sg * r0, 0.0), ds=0.8, bounds=bnd)
            P = [to_img(p[0], p[1]) for p in pts]
            s.polyline(P, 'blue', 1.15, opacity=0.9)
            s.arrow_at(P, 0.5 if r0 > a else 0.12, 'blue', 1.15, head=6.2)
    s.line((6, cy), (W - 6, cy), 'blue', 1.15, opacity=0.9)
    s.arrow((cx + 70, cy), (cx + 92, cy), 'blue', 1.15, head=6.2)
    s.arrow((cx - 92, cy), (cx - 70, cy), 'blue', 1.15, head=6.2)
    s.line((cx, cy - a), (cx, cy + a), 'orange', 2.2, dash='2 3')
    s.sym_out((cx, cy - a), 7.2, 'orange', 1.8); s.sym_in((cx, cy + a), 7.2, 'orange', 1.8)
    s.arrow((cx - 16, cy), (cx + 16, cy), 'blue', 2.6, head=9)
    s.vtext(cx + 2, cy + 18, 'B', size=12.5, color='blue', plate=True)
    s.text(W - 8, 18, 'face NORTE', 9.4, 'red', anchor='end', weight=700, plate=True)
    s.text(W - 8, 29, 'as linhas saem', 8.2, 'red', anchor='end', plate=True)
    s.text(8, 18, 'face SUL', 9.4, 'red', anchor='start', weight=700, plate=True)
    s.text(8, 29, 'as linhas entram', 8.2, 'red', anchor='start', plate=True)
    s.text(cx + 14, cy - a - 8, 'corrente saindo', 8.2, 'orange', anchor='start', plate=True)
    s.text(cx + 14, cy + a + 15, 'corrente entrando', 8.2, 'orange', anchor='start', plate=True)
    s.text(cx - 14, cy - a - 8, 'plano da espira', 8, 'gray', anchor='end', plate=True)
    s.save()
    return s


# ======================================================================================= p07 · regra do relógio
def loop_faces(W=336, H=118):
    s = Svg(W, H, 'loop_faces')
    for k, ccw in enumerate((True, False)):
        cx, cy, R = W * (0.25 + 0.5 * k), 56, 34
        s.circle((cx, cy), R, fill='none', stroke='orange', w=2.6)
        sgn = 1 if ccw else -1
        for ang in (60, 240):
            a = math.radians(ang)
            tx, ty = -math.sin(a) * sgn, -math.cos(a) * sgn        # tangente em coordenadas de imagem (y para baixo)
            P = (cx + R * math.cos(a), cy - R * math.sin(a))
            s._head((P[0] - tx * 5, P[1] - ty * 5), (P[0] + tx * 3, P[1] + ty * 3), 'orange', 9, None, 2.6)
        (s.sym_out if ccw else s.sym_in)((cx, cy), 9, 'blue', 2.0)
        s.text(cx, cy - R - 8, ['visto de frente: anti-horário', 'visto de frente: horário'][k], 8.8, 'orange', weight=700)
        s.rect(cx - 30, cy + R + 8, 60, 16, 3, fill=STROKE['red'] if ccw else '#FFFFFF', stroke=STROKE['red'], sw=1.5)
        s.text(cx, cy + R + 20, 'face NORTE' if ccw else 'face SUL', 8.8, 'white' if ccw else 'red', weight=700)
    s.save()
    return s


# ======================================================================================= p08 · solenoide (corte)
def solenoid_section(W=336, H=176):
    s = Svg(W, H, 'solenoid_section')
    cx, cy = W / 2, H / 2
    a, L = 27.0, 132.0
    Bf = lambda rho, z: F.stack_B(rho, z, a, L, 160)
    field = F.make_planar(Bf)
    to_img = lambda xp, z: (cx + z, cy - xp)
    bnd = (-(H / 2 - 4), (H / 2 - 4), -(W / 2 - 4), (W / 2 - 4))
    for q in (0.3, 0.58, 0.82):                      # espaçamento igual em ρ no interior: campo uniforme
        for sg in (+1, -1):
            pts, _ = F.full_line(field, (sg * q * a, 0.0), ds=0.9, bounds=bnd)
            P = [to_img(p[0], p[1]) for p in pts]
            s.polyline(P, 'blue', 1.1, opacity=0.9)
            s.arrow_at(P, 0.5, 'blue', 1.1, head=6.0)
    for sg in (+1, -1):
        pts, _ = F.full_line(field, (sg * 0.94 * a, 0.0), ds=0.9, bounds=bnd)
        s.polyline([to_img(p[0], p[1]) for p in pts], 'blue', 1.1, opacity=0.9)
    s.line((4, cy), (cx - L / 2, cy), 'blue', 1.1, opacity=0.9)
    s.line((cx + L / 2, cy), (W - 4, cy), 'blue', 1.1, opacity=0.9)
    s.arrow((cx + L / 2 + 24, cy), (cx + L / 2 + 44, cy), 'blue', 1.1, head=6)
    s.arrow((cx - L / 2 - 44, cy), (cx - L / 2 - 24, cy), 'blue', 1.1, head=6)
    s.rect(cx - L / 2, cy - a, L, 2 * a, 0, fill='none', stroke='gray', sw=1.0, dash='3 3')
    n = 11
    for i in range(n):
        x = cx - L / 2 + (i + 0.5) * L / n
        s.sym_out((x, cy - a), 4.6, 'orange', 1.4); s.sym_in((x, cy + a), 4.6, 'orange', 1.4)
    s.arrow((cx - 36, cy), (cx + 36, cy), 'blue', 2.4, head=8.5)
    s.vtext(cx + 4, cy + 16, 'B', size=12, color='blue', plate=True)
    s.text(cx + L / 2 + 14, cy - a - 6, 'N', 11, 'red', weight=700, anchor='start', plate=True)
    s.text(cx - L / 2 - 14, cy - a - 6, 'S', 11, 'red', weight=700, anchor='end', plate=True)
    s.text(cx, 14, 'interior: B intenso e quase uniforme', 8.4, 'blue', weight=700, plate=True)
    s.text(cx, H - 6, 'exterior: B fraco (como o de um ímã em barra)', 8.2, 'gray', plate=True)
    s.save()
    return s


# ======================================================================================= p08 · perfil do campo no eixo
def solenoid_profile(W=336, H=150):
    s = Svg(W, H, 'solenoid_profile')
    a, L = 1.0, 5.0                               # comprimento = 2,5 diâmetros
    pl = Plot(s, 46, 12, W - 58, H - 48, (-4.5, 4.5), (0, 1.15), xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1.0],
              xlabel='posição ao longo do eixo (em raios)', ylabel='B / (μ_{0}nI)', xlab_dy=30, ylab_dx=-34,
              yfmt=lambda v: num(v, 1), xfmt=lambda v: num(v, 0))
    xs = np.linspace(-4.5, 4.5, 400)
    B = 0.5 * ((xs + L / 2) / np.sqrt((xs + L / 2) ** 2 + a ** 2) - (xs - L / 2) / np.sqrt((xs - L / 2) ** 2 + a ** 2))
    pl.curve(xs, B, 'blue', 2.2)
    s.rect(pl.X(-L / 2), pl.Y(0) - 7, pl.X(L / 2) - pl.X(-L / 2), 7, 0, fill='#FFF0DF', stroke=STROKE['orange'], sw=1.2)
    s.text(pl.X(0), pl.Y(1.0) - 9, 'centro: B ≈ μ_{0}nI', 8.4, 'blue', weight=700, plate=True)
    for xe in (-L / 2, L / 2):
        pl.dot(xe, float(0.5 * (L / math.sqrt(L ** 2 + a ** 2))), 'blue')
    s.text(pl.X(-L / 2) - 7, pl.Y(0.49) + 3, '≈ 0,5', 8.4, 'blue', anchor='end', weight=700)
    s.text(pl.X(L / 2) + 7, pl.Y(0.49) + 3, '≈ 0,5', 8.4, 'blue', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p09 · Ampère (três fios e um caminho)
def ampere_loops(W=336, H=176):
    s = Svg(W, H, 'ampere_loops')
    cx, cy, rx, ry = 124, 90, 92, 56
    pts = [(cx + rx * math.cos(t), cy - ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 240)]
    s.polyline(pts, 'gray', 1.8, dash='6 4')
    for fr in (0.13, 0.63):
        s.arrow_at(pts, fr, 'gray', 1.8, head=9)
    s.text(cx, cy - ry - 8, 'caminho fechado C (anti-horário)', 9, 'gray', weight=700)
    w1, w2, w3 = (cx - 40, cy + 4), (cx + 42, cy - 6), (W - 34, cy + 22)
    s.sym_out(w1, 8, 'orange', 1.9); s.sym_in(w2, 8, 'orange', 1.9); s.sym_out(w3, 8, 'orange', 1.9)
    s.text(w1[0], w1[1] + 23, '6 A', 9, 'orange', weight=700); s.text(w2[0], w2[1] + 23, '4 A', 9, 'orange', weight=700)
    s.text(w3[0], w3[1] + 23, '5 A (fora de C)', 8.6, 'orange', weight=700)
    s.vtext(w1[0] - 14, w1[1] - 11, 'I', sub='1', size=11, color='orange', arrow=False)
    s.vtext(w2[0] + 14, w2[1] - 11, 'I', sub='2', size=11, color='orange', arrow=False)
    s.vtext(w3[0] + 14, w3[1] - 11, 'I', sub='3', size=11, color='orange', arrow=False)
    s.sym_out((W - 104, 12), 4.8, 'orange', 1.3); s.text(W - 96, 15.4, 'saindo: (+)', 8.4, 'ink', anchor='start', weight=700)
    s.sym_in((W - 104, 26), 4.8, 'orange', 1.3); s.text(W - 96, 29.4, 'entrando: (−)', 8.4, 'ink', anchor='start', weight=700)
    s.text(cx, H - 6, 'fios envolvidos por C: I_{env} = (+6) + (−4) = +2 A', 8.8, 'green', weight=700)
    s.save()
    return s


# ======================================================================================= p09 · Ampère com simetria
def ampere_sym(W=336, H=124):
    s = Svg(W, H, 'ampere_sym')
    cx, cy = 72, 70
    s.circle((cx, cy), 44, fill='none', stroke='gray', w=1.6, dash='6 4')
    sy = [(cx + 44 * math.cos(t), cy - 44 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 120)]
    s.arrow_at(sy, 0.25, 'gray', 1.6, head=8)
    s.sym_out((cx, cy), 6.8, 'orange', 1.8)
    for ang in (30, 150, 270):                       # B tangente (anti-horário para I saindo)
        a = math.radians(ang)
        P = (cx + 44 * math.cos(a), cy - 44 * math.sin(a))
        t = (-math.sin(a), -math.cos(a))
        s.arrow(P, (P[0] + t[0] * 24, P[1] + t[1] * 24), 'blue', 2.0, head=7.5)
    s.line((cx, cy), (cx + 44 * math.cos(math.radians(-40)), cy - 44 * math.sin(math.radians(-40))), 'gray', 1.0)
    s.text(cx + 12, cy + 24, 'r', 9.5, 'gray', weight=700)
    s.text(cx, 11, 'fio: B tangente e constante em C', 8.4, 'ink', weight=700)
    # solenoide: caminho retangular que atravessa os fios do topo (⊙)
    x0, ytop, ybot = 176, 46, 104
    s.rect(x0, ytop, 152, ybot - ytop, 0, fill='none', stroke='gray', sw=1.0, dash='3 3')
    for i in range(10):
        x = x0 + 8 + i * 15.1
        s.sym_out((x, ytop), 4.2, 'orange', 1.3); s.sym_in((x, ybot), 4.2, 'orange', 1.3)
    xa, xb, yo, yi = 206.65, 297.25, 30, 76
    rc = [(xa, yi), (xb, yi), (xb, yo), (xa, yo), (xa, yi)]
    s.polyline(rc, 'gray', 1.8, dash='6 4')
    s.arrow((xa + 40, yi), (xa + 56, yi), 'gray', 1.8, head=8)
    s.arrow((xb, yi - 14), (xb, yi - 24), 'gray', 1.8, head=8)
    s.arrow((xa + 52, yo), (xa + 36, yo), 'gray', 1.8, head=8)
    s.arrow((xa, yo + 22), (xa, yo + 32), 'gray', 1.8, head=8)
    s.arrow((xa + 8, yi + 12), (xb - 8, yi + 12), 'blue', 2.2, head=8)
    s.text(x0 + 76, H - 5, 'B no interior, ao longo do trecho L', 8.2, 'blue', weight=700)
    s.text(x0 + 76, 11, 'solenoide: só o lado interno conta', 8.4, 'ink', weight=700)
    s.text(xa - 4, yo + 3, 'fora: B ≈ 0', 8, 'gray', anchor='end')
    s.save()
    return s


if __name__ == '__main__':
    print('rhr_drill respostas:', rhr_drill())
    for fn in (oersted, rhr1, wire_planar, wire_xsec, B_vs_r, two_wires_ex, By_profile, three_wires, square_wires, loop_section, loop_faces,
               solenoid_section, solenoid_profile, ampere_loops, ampere_sym):
        fn()
