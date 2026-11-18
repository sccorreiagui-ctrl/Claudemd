"""Módulo IV (parte A) — fluxo, Faraday, gráficos e método de Lenz (páginas 16 a 19)."""
import math
import numpy as np
from svglib import Svg, Cam, Plot, STROKE, num

X_, Y_, Z_ = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])


# ======================================================================================= p16 · geometria do fluxo
def flux_geometry(W=336, H=206):
    s = Svg(W, H, 'flux_geometry')
    cam = Cam(az=-30, el=24, scale=62, ox=150, oy=128)
    th = math.radians(40)
    n = Y_.copy()
    b = np.array([math.sin(th), math.cos(th), 0.0])
    assert abs(math.degrees(math.acos(np.dot(b, n))) - 40) < 1e-9
    corners = [np.array(c) for c in ((-1.15, 0, -0.75), (1.15, 0, -0.75), (1.15, 0, 0.75), (-1.15, 0, 0.75))]
    pts_in = [(x, z) for x in (-0.6, 0.6) for z in (-0.35, 0.35)]
    # B abaixo do plano
    for (x, z) in pts_in:
        p0 = np.array([x, 0, z]) - 1.1 * b
        s.line(cam.P(p0), cam.P(np.array([x, 0, z])), 'blue', 1.6, opacity=0.9)
    # espira (superfície)
    s.polygon([cam.P(c) for c in corners], fill='#DDE6F4', stroke='gray', w=1.8, opacity=0.55)
    # B acima do plano
    for (x, z) in pts_in:
        p1 = np.array([x, 0, z]) + 1.1 * b
        s.arrow(cam.P(np.array([x, 0, z])), cam.P(p1), 'blue', 1.6, head=7.5)
    c0 = np.zeros(3)
    s.arrow(cam.P(c0), cam.P(n * 1.35), 'ink', 2.4, head=8.5)
    pn = cam.P(n * 1.35)
    s.vtext(pn[0] - 12, pn[1] - 2, 'n', size=12.5, color='ink', arrow=False)
    s.text(pn[0] - 5, pn[1] - 3, '̂', 12, 'ink') if False else None
    pb = cam.P(np.array([0.6, 0, 0.35]) + 1.1 * b)
    s.vtext(pb[0] + 14, pb[1] + 2, 'B', size=13, color='blue', plate=True)
    arc = [cam.P(0.62 * (math.cos(t) * n + math.sin(t) * np.array([1.0, 0, 0]))) for t in np.linspace(0, th, 18)]
    s.polyline(arc, 'gray', 1.3)
    s.text(cam.P(0.9 * (math.cos(th / 2) * n + math.sin(th / 2) * X_))[0] + 6, cam.P(0.9 * (math.cos(th / 2) * n + math.sin(th / 2) * X_))[1], 'θ', 11, 'gray', weight=700)
    s.text(cam.P(np.array([-1.0, 0, 0.7]))[0] - 4, cam.P(np.array([-1.0, 0, 0.7]))[1] + 15, 'área A', 8.8, 'gray', anchor='start', weight=700)
    s.text(8, 15, 'Φ = B A cos θ', 10.5, 'navy', anchor='start', weight=700)
    s.text(8, 28, 'θ = ângulo entre B e a NORMAL', 8.4, 'red', anchor='start', weight=700)
    s.text(8, 40, '(não o ângulo com o plano)', 8.2, 'red', anchor='start')
    s.save()
    return s


# ======================================================================================= p16 · casos de fluxo
def flux_cases(W=680, H=134):
    s = Svg(W, H, 'flux_cases')
    pw = W / 4
    cases = [(0, 'θ = 0°', 'Φ = +B A  (máximo)'), (60, 'θ = 60°', 'Φ = B A cos 60° = B A/2'), (90, 'θ = 90°', 'Φ = 0  (B no plano)'), (180, 'θ = 180°', 'Φ = −B A  (mínimo)')]
    for k, (deg, t1, t2) in enumerate(cases):
        x0 = pw * k
        s.rect(x0 + 3, 3, pw - 6, H - 6, 4, fill='white', stroke='light', sw=1.0)
        s.text(x0 + pw / 2, 17, t1, 9.4, 'navy', weight=700)
        cx, cy = x0 + pw / 2, 74
        th = math.radians(deg)
        b = np.array([math.sin(th), math.cos(th)])                    # B em (x, y para cima); n = +y
        n = np.array([0.0, 1.0])
        assert abs(np.dot(b, n) - math.cos(th)) < 1e-12
        for off in (-44, -22, 0, 22, 44):
            p0 = (cx + off - b[0] * 34, cy + b[1] * 34)
            p1 = (cx + off + b[0] * 34, cy - b[1] * 34)
            s.arrow(p0, p1, 'blue', 1.5, head=7, opacity=0.9)
        s.line((cx - 56, cy), (cx + 56, cy), 'gray', 4.0)
        s.arrow((cx - 56, cy), (cx - 56, cy - 30), 'ink', 2.2, head=8)
        s.text(cx - 62, cy - 22, 'n', 10.5, 'ink', anchor='end', weight=700, family='sans') if False else None
        s.vtext(cx - 64, cy - 24, 'n', size=11.5, color='ink', arrow=False)
        s.text(cx + pw / 2 - 12, cy - 38, 'B', 11, 'blue', anchor='end', weight=700) if False else None
        s.text(cx, H - 11, t2, 8.8, 'green', weight=700)
    s.save()
    return s


# ======================================================================================= p16 · Φ(θ)
def phi_theta(W=336, H=150):
    s = Svg(W, H, 'phi_theta')
    pl = Plot(s, 46, 12, W - 60, H - 50, (0, 360), (-1.15, 1.15), xticks=[0, 90, 180, 270, 360], yticks=[-1, 0, 1],
              xlabel='ângulo θ entre B e a normal (graus)', ylabel='Φ / (B A)', xlab_dy=30, ylab_dx=-34,
              yfmt=lambda v: num(v, 0), xfmt=lambda v: num(v, 0))
    th = np.linspace(0, 360, 361)
    pl.curve(th, np.cos(np.radians(th)), 'blue', 2.3)
    for t, v in ((0, 1), (90, 0), (180, -1), (270, 0), (360, 1)):
        pl.dot(t, v, 'blue')
    s.text(pl.X(8), pl.Y(1) + 3, 'máx', 8.2, 'blue', anchor='start', weight=700)
    s.text(pl.X(180), pl.Y(-1) - 6, 'mín (−BA)', 8.2, 'blue', weight=700)
    s.text(pl.X(90), pl.Y(0) - 7, 'nulo', 8.2, 'blue', weight=700)
    s.save()
    return s


# ======================================================================================= p17 · bobina e ímã
def faraday_setup(W=336, H=140):
    s = Svg(W, H, 'faraday_setup')
    cy = 58
    s.magnet(20, cy - 14, 84, 28, n_left=False, size=13)          # N voltado para a bobina
    s.arrow((34, cy - 26), (92, cy - 26), 'cyan', 2.4, head=8.5)
    s.vtext(63, cy - 33, 'v', size=11.5, color='cyan', anchor='middle')
    # bobina: 6 espiras
    xs = [196 + 11 * i for i in range(6)]
    for x in xs:
        s.ellipse((x, cy), 6.5, 30, fill='none', stroke='orange', w=2.0)
    # linhas de campo atravessando a bobina
    for off in (-14, 0, 14):
        s.arrow((110, cy + off), (192, cy + off), 'blue', 1.3, head=6.5, opacity=0.75)
        s.arrow((262, cy + off), (292, cy + off), 'blue', 1.3, head=6.5, opacity=0.75)
    s.vtext(300, cy - 10, 'B', size=12, color='blue', plate=True)
    # voltímetro
    vx, vy = 232, 124
    s.circle((vx, vy), 11, fill='white', stroke='ink', w=1.6)
    s.text(vx, vy + 4, 'V', 11, 'ink', weight=700)
    s.polyline([(xs[0], cy + 30), (xs[0], vy), (vx - 11, vy)], 'ink', 1.4)
    s.polyline([(xs[-1], cy + 30), (xs[-1], vy), (vx + 11, vy)], 'ink', 1.4)
    s.text(vx + 20, vy + 4, 'ε induzida', 8.8, 'purple', anchor='start', weight=700)
    s.text(xs[2] + 6, 14, 'N espiras', 9.4, 'orange', weight=700)
    s.line((xs[0] - 6, 22), (xs[-1] + 6, 22), 'orange', 1.0)
    s.text(8, 98, 'ΔΦ/Δt: variação do fluxo', 8.6, 'ink', anchor='start', weight=700)
    s.text(8, 110, 'em cada espira', 8.6, 'ink', anchor='start', weight=700)
    s.text(8, 128, 'ε = − N ΔΦ/Δt', 10.5, 'purple', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p17 · duas bobinas (anel de Faraday)
def two_coils(W=680, H=158):
    s = Svg(W, H, 'two_coils')
    # anel de ferro com dois enrolamentos
    ring = [(70, 24), (210, 24), (210, 116), (70, 116), (70, 24)]
    s.polyline(ring, '#C3CBD6', 20.0, join='miter')
    for yy in range(34, 108, 9):
        s.line((58, yy), (82, yy + 5), 'orange', 2.0)
        s.line((198, yy), (222, yy + 5), 'orange', 2.0)
    s.arrow((120, 24), (160, 24), 'blue', 2.0, head=8)
    s.text(140, 14, 'Φ no ferro', 8.6, 'blue', weight=700)
    # primário: pilha e chave
    s.polyline([(58, 38), (30, 38), (30, 60)], 'ink', 1.6)
    s.battery((30, 70), False, 12)
    s.polyline([(30, 78), (30, 108), (58, 108)], 'ink', 1.6)
    s.line((30, 38), (30, 38), 'ink', 1.0)
    s.text(30, 134, 'primário', 8.2, 'orange', weight=700)
    # chave
    s.circle((30, 46), 2.4, fill='ink', stroke=None)
    # secundário: voltímetro
    s.polyline([(222, 38), (250, 38), (250, 56)], 'ink', 1.6)
    s.circle((250, 68), 12, fill='white', stroke='ink', w=1.6); s.text(250, 72, 'V', 11, 'ink', weight=700)
    s.polyline([(250, 80), (250, 108), (222, 108)], 'ink', 1.6)
    s.text(272, 72, 'secundário', 8.2, 'orange', anchor='start', weight=700)
    # gráficos
    x0 = 340
    pl1 = Plot(s, x0 + 26, 14, 290, 48, (0, 10), (-0.15, 1.3), xticks=[], yticks=[0, 1], xlabel='', ylabel='', ytick_labels=False, grid=False)
    pl1.curve([0, 3, 3, 7, 7, 10], [0, 0, 1, 1, 0, 0], 'orange', 2.6)
    s.text(x0, 42, 'I_{p}', 9.4, 'orange', anchor='start', weight=700)
    s.text(pl1.X(5), pl1.Y(1) - 5, 'corrente contínua constante', 8.2, 'orange', weight=700)
    s.text(pl1.X(3) - 4, pl1.Y(0) + 11, 'liga', 8.2, 'gray', anchor='end'); s.text(pl1.X(7) + 4, pl1.Y(0) + 11, 'desliga', 8.2, 'gray', anchor='start')
    pl2 = Plot(s, x0 + 26, 82, 290, 48, (0, 10), (-1.4, 1.4), xticks=[], yticks=[0], xlabel='tempo', ylabel='', ytick_labels=False, grid=False, xlab_dy=19)
    pl2.curve([0, 2.8, 3, 3.3, 3.5, 6.5, 7, 7.3, 7.5, 10], [0, 0, -1, -0.15, 0, 0, 1, 0.15, 0, 0], 'purple', 2.6)
    s.text(x0, 112, 'ε_{s}', 9.4, 'purple', anchor='start', weight=700)
    s.text(pl2.X(3) - 6, pl2.Y(-1) + 10, 'ΔΦ > 0: ε < 0', 8.2, 'purple', anchor='end', weight=700)
    s.text(pl2.X(7) + 6, pl2.Y(1) + 4, 'ΔΦ < 0: ε > 0', 8.2, 'purple', anchor='start', weight=700)
    s.text(pl2.X(5), pl2.Y(0) - 6, 'Φ constante: ε = 0', 8.2, 'purple', weight=700)
    s.save()
    return s


# ======================================================================================= p17 · Φ(t) do exemplo
def phi_t_ex17(W=336, H=150):
    s = Svg(W, H, 'phi_t_ex17')
    pl = Plot(s, 48, 12, W - 62, H - 52, (0, 0.06), (0, 10), xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06], yticks=[0, 2, 4, 6, 8, 10],
              xlabel='tempo (s)', ylabel='Φ por espira (mWb)', xlab_dy=30, ylab_dx=-35,
              xfmt=lambda v: num(v, 2), yfmt=lambda v: num(v, 0))
    pl.curve([0, 0.05], [3.0, 8.0], 'blue', 2.6)
    pl.dot(0, 3.0, 'blue'); pl.dot(0.05, 8.0, 'blue')
    s.line((pl.X(0), pl.Y(3)), (pl.X(0.05), pl.Y(3)), 'gray', 1.2, dash='4 3')
    s.line((pl.X(0.05), pl.Y(3)), (pl.X(0.05), pl.Y(8)), 'gray', 1.2, dash='4 3')
    s.text(pl.X(0.025), pl.Y(3) + 13, 'Δt = 0,050 s', 8.6, 'gray', weight=700)
    s.text(pl.X(0.05) + 5, pl.Y(5.5) + 3, 'ΔΦ = 5,0 mWb', 8.6, 'gray', anchor='start', weight=700)
    s.text(pl.X(0.003), pl.Y(9.2), 'inclinação ΔΦ/Δt = 0,10 Wb/s', 8.8, 'blue', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p18 · Φ(t) e ε(t) por partes
def phi_emf_piecewise(W=680, H=190):
    s = Svg(W, H, 'phi_emf_piecewise')
    N = 50
    ts = [0, 2, 5, 7]
    ph = [0.0, 8.0, 8.0, -4.0]                           # mWb
    pl1 = Plot(s, 52, 14, W / 2 - 66, H - 58, (0, 7), (-6, 10), xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[-4, 0, 4, 8],
               xlabel='tempo (s)', ylabel='Φ por espira (mWb)', xlab_dy=30, ylab_dx=-37, xfmt=lambda v: num(v, 0), yfmt=lambda v: num(v, 0))
    pl1.curve(ts, ph, 'blue', 2.6)
    for t, p in zip(ts, ph):
        pl1.dot(t, p, 'blue', 3.2)
    s.text(pl1.X(1), pl1.Y(4) - 9, 'sobe', 8.4, 'blue', weight=700)
    s.text(pl1.X(3.5), pl1.Y(8) - 8, 'constante', 8.4, 'blue', weight=700)
    s.text(pl1.X(6) + 6, pl1.Y(2), 'desce', 8.4, 'blue', anchor='start', weight=700)
    # ε = −N dΦ/dt  (V)
    slopes = [(ph[i + 1] - ph[i]) / (ts[i + 1] - ts[i]) * 1e-3 for i in range(3)]      # Wb/s
    emf = [-N * m for m in slopes]
    assert np.allclose(emf, [-0.20, 0.0, 0.30])
    x0 = W / 2 + 36
    pl2 = Plot(s, x0 + 12, 14, W / 2 - 66, H - 58, (0, 7), (-0.4, 0.4), xticks=[0, 1, 2, 3, 4, 5, 6, 7], yticks=[-0.2, 0, 0.2],
               xlabel='tempo (s)', ylabel='ε (V), N = 50', xlab_dy=30, ylab_dx=-40, xfmt=lambda v: num(v, 0), yfmt=lambda v: num(v, 1))
    for i in range(3):
        s.line((pl2.X(ts[i]), pl2.Y(emf[i])), (pl2.X(ts[i + 1]), pl2.Y(emf[i])), STROKE['purple'], 3.0)
        if i < 2:
            s.line((pl2.X(ts[i + 1]), pl2.Y(emf[i])), (pl2.X(ts[i + 1]), pl2.Y(emf[i + 1])), STROKE['purple'], 1.2, dash='3 3')
    s.text(pl2.X(1), pl2.Y(-0.2) + 15, '−0,20 V', 8.6, 'purple', weight=700)
    s.text(pl2.X(3.5), pl2.Y(0) - 7, '0 (fluxo constante)', 8.6, 'purple', weight=700)
    s.text(pl2.X(6), pl2.Y(0.3) - 6, '+0,30 V', 8.6, 'purple', weight=700)
    s.save()
    return emf


# ======================================================================================= p18 · Φ e ε senoidais
def sin_flux_emf(W=336, H=172):
    s = Svg(W, H, 'sin_flux_emf')
    pl = Plot(s, 46, 26, W - 60, H - 66, (0, 1), (-1.2, 1.2), xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[-1, 0, 1],
              xlabel='tempo (em períodos, t/T)', ylabel='valor normalizado', xlab_dy=30, ylab_dx=-34,
              xfmt=lambda v: num(v, 2), yfmt=lambda v: num(v, 0))
    t = np.linspace(0, 1, 401)
    pl.curve(t, np.cos(2 * math.pi * t), 'blue', 2.3)
    pl.curve(t, np.sin(2 * math.pi * t), 'purple', 2.3, dash='6 3')
    pl.dot(0, 1, 'blue'); pl.dot(0.25, 1, 'purple'); pl.dot(0.5, -1, 'blue'); pl.dot(0.75, -1, 'purple')
    s.line((50, 150), (74, 150), 'blue', 2.3) if False else None
    s.text(W / 2, 11, 'Φ = Φ_{máx} cos ωt (azul)  ·  ε = N Φ_{máx} ω sen ωt (roxo, tracejado)', 8.2, 'ink', weight=700)
    s.text(pl.X(0.25) + 4, pl.Y(0) + 14, 'Φ = 0: ε máxima', 8.2, 'purple', anchor='start', weight=700)
    s.text(pl.X(0.5) + 4, pl.Y(0) - 8, 'Φ máx: ε = 0', 8.2, 'blue', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p19 · método de Lenz (fluxograma)
def lenz_flow(W=680, H=184):
    s = Svg(W, H, 'lenz_flow')
    bw, bh = 200, 58
    xs = [8, 240, 472]
    y1, y2 = 8, 104

    def box(x, y, num_, title, body, color):
        s.rect(x, y, bw, bh, 5, fill={'blue': 'blue', 'purple': 'purple', 'orange': 'orange', 'green': 'green', 'gray': 'gray'}[color], stroke=color, sw=1.6)
        s.circle((x + 16, y + 17), 10, fill=STROKE[color], stroke=None)
        s.text(x + 16, y + 21, str(num_), 11, 'white', weight=700)
        s.text(x + 32, y + 21, title, 9.6, color if color != 'gray' else 'navy', anchor='start', weight=700)
        for i, ln in enumerate(body):
            s.text(x + 12, y + 36 + i * 11, ln, 8.4, 'ink', anchor='start')

    box(xs[0], y1, 1, 'Campo externo', ['qual é o sentido de B que atravessa', 'a espira? (use ⊙ e ⊗)'], 'blue')
    box(xs[1], y1, 2, 'Normal da superfície', ['escolha n (um lado da espira);', 'só serve de referência de sinal'], 'gray')
    box(xs[2], y1, 3, 'O fluxo aumenta ou diminui?', ['olhe o módulo |Φ| (e o sinal,', 'se usar Φ com sinal)'], 'gray')
    box(xs[2], y2, 4, 'Campo induzido', ['Φ aumenta: B_{ind} OPOSTO a B_{ext}', 'Φ diminui: B_{ind} no MESMO sentido'], 'purple')
    box(xs[1], y2, 5, 'Corrente induzida', ['mão direita: polegar em B_{ind} no', 'interior; dedos = sentido de I'], 'orange')
    box(xs[0], y2, 6, 'Confira a energia', ['o efeito resiste à mudança?', '(repele a aproximação ✓)'.replace(' ✓', '')], 'green')
    # setas
    s.arrow((xs[0] + bw + 2, y1 + bh / 2), (xs[1] - 2, y1 + bh / 2), 'ink', 2.0, head=8)
    s.arrow((xs[1] + bw + 2, y1 + bh / 2), (xs[2] - 2, y1 + bh / 2), 'ink', 2.0, head=8)
    s.arrow((xs[2] + bw / 2, y1 + bh + 2), (xs[2] + bw / 2, y2 - 2), 'ink', 2.0, head=8)
    s.arrow((xs[2] - 2, y2 + bh / 2), (xs[1] + bw + 2, y2 + bh / 2), 'ink', 2.0, head=8)
    s.arrow((xs[1] - 2, y2 + bh / 2), (xs[0] + bw + 2, y2 + bh / 2), 'ink', 2.0, head=8)
    s.text(W / 2, H - 5, 'Faraday dá o MÓDULO de ε (quão rápido varia Φ); Lenz dá o SENTIDO (oposição à variação).', 9, 'navy', weight=700)
    s.save()
    return s


if __name__ == '__main__':
    flux_geometry(); flux_cases(); phi_theta(); faraday_setup(); two_coils(); phi_t_ex17()
    print('emf piecewise (V):', phi_emf_piecewise())
    sin_flux_emf(); lenz_flow()
