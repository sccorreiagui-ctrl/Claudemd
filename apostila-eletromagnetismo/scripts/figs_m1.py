"""Módulo I — Fundamentos (páginas 1 a 3)."""
import math
import numpy as np
from svglib import Svg, STROKE
import fields as F



def magnet_lines(s, cx, cy, a, L, W, H, fracs, color, lw=1.15, opacity=0.92, arrow_color=None, head=6.4, margin=4):
    """desenha linhas de B de um ímã em barra (modelo de espiras empilhadas); N à esquerda. Retorna o campo planar."""
    Bfun = lambda rho, z: F.stack_B(rho, z, a, L, 150)
    field = F.make_planar(Bfun)
    to_img = lambda xp, z: (cx - z, cy - xp)
    bnd = (-(cy - margin), (H - cy - margin), -(cx - margin), (W - cx - margin))   # (xp_min, xp_max, z_min, z_max)
    rhos = np.linspace(0, a, 400)
    bz0 = np.array([Bfun(r, 0.0)[1] for r in rhos], float)
    flux = np.cumsum(bz0 * rhos); flux /= flux[-1]
    seeds = [float(np.interp(q, flux, rhos)) for q in fracs]
    for r in seeds:
        for sgn in (+1, -1):
            pts, _ = F.full_line(field, (sgn * r, 0.0), ds=max(0.9, a / 18), bounds=bnd)
            P = [to_img(p[0], p[1]) for p in pts]
            s.polyline(P, color, lw, opacity=opacity)
            s.arrow_at(P, 0.5, arrow_color or color, lw, head=head)
            if r <= seeds[min(2, len(seeds) - 1)]:
                s.arrow_at(P, 0.22, arrow_color or color, lw, head=head)
                s.arrow_at(P, 0.78, arrow_color or color, lw, head=head)
    return field


# ======================================================================================= capa (arte)
def cover_art(W=330, H=180):
    s = Svg(W, H, 'cover_art')
    cx, cy, a, L = 232, 92, 15.0, 62.0
    magnet_lines(s, cx, cy, a, L, W, H, (0.2, 0.42, 0.62, 0.78, 0.9, 0.975), '#7FA6E6', lw=1.1, opacity=0.42, arrow_color='#A9C4F2', head=6)
    s.line((2, cy), (cx - L / 2, cy), '#7FA6E6', 1.1, opacity=0.42)
    s.line((cx + L / 2, cy), (W - 2, cy), '#7FA6E6', 1.1, opacity=0.42)
    s.rect(cx - L / 2, cy - a, L / 2, 2 * a, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.2)
    s.rect(cx, cy - a, L / 2, 2 * a, 0, fill='#0E2A47', stroke='#E58A89', sw=1.2)
    s.text(cx - L / 4, cy + 5, 'N', 13, 'white', weight=700)
    s.text(cx + L / 4, cy + 5, 'S', 13, '#F0B3B2', weight=700)
    s.save()
    return s


# ======================================================================================= p01 · ímã e campo
def magnet_field(W=336, H=198):
    s = Svg(W, H, 'magnet_field')
    cx, cy = W / 2, H / 2
    a, L = 16.0, 112.0                          # meia-espessura e comprimento do ímã (px)

    field = magnet_lines(s, cx, cy, a, L, W, H, (0.20, 0.42, 0.62, 0.78, 0.90, 0.975), 'blue')
    # linha do eixo (fora do ímã): B aponta para a esquerda dos dois lados
    s.line((4, cy), (cx - L / 2, cy), 'blue', 1.15, opacity=0.92)
    s.line((cx + L / 2, cy), (W - 4, cy), 'blue', 1.15, opacity=0.92)
    s.arrow((cx - L / 2 - 14, cy), (cx - L / 2 - 36, cy), 'blue', 1.15, head=6.4)
    s.arrow((W - 22, cy), (W - 44, cy), 'blue', 1.15, head=6.4)
    s.magnet(cx - L / 2, cy - a, L, 2 * a, n_left=True, size=14)
    s.arrow((cx + 24, cy), (cx - 24, cy), 'blue', 1.7, head=7.5)       # B interno: S -> N
    for dx, dy in [(-134, 0), (132, 0), (-44, -58), (54, -56), (-46, 57), (64, 52)]:
        ix, iy = cx + dx, cy + dy
        bx, bz = field(cy - iy, cx - ix)
        s.compass((ix, iy), math.degrees(math.atan2(bx, -bz)), r=8.4)
    ix, iy = cx + 54, cy - 56                      # vetor B tangente
    bx, bz = field(cy - iy, cx - ix)
    n_ = math.hypot(bx, bz); vx, vy = -bz / n_, -bx / n_
    s.arrow((ix + vx * 10, iy + vy * 10), (ix + vx * 44, iy + vy * 44), 'blue', 2.1, head=8.5)
    s.vtext(ix + vx * 44 + 5, iy + vy * 44 - 8, 'B', size=13, color='blue', plate=True)
    s.text(cx - L / 2 - 3, cy + a + 15, 'polo N', 8.6, 'red', weight=700, anchor='end', plate=True)
    s.text(cx + L / 2 + 3, cy + a + 15, 'polo S', 8.6, 'red', weight=700, anchor='start', plate=True)
    s.text(cx, cy + a + 15.5, 'dentro do ímã: de S para N', 8.2, 'blue', plate=True)
    s.save()
    return s


# ======================================================================================= p01 · partir o ímã
def magnet_split(W=336, H=132):
    s = Svg(W, H, 'magnet_split')
    h = 17.0
    bar = lambda x, y, w: s.magnet(x, y, w, h, n_left=True, size=10.5)

    s.text(6, 11, 'ímã inteiro', 8.6, 'gray', anchor='start', weight=700)
    bar(6, 16, 112)
    s.line((62, 10), (62, 38), 'ink', 1.0, dash='3 2.4')
    s.text(66, 11, 'corte', 7.8, 'gray', anchor='start')
    s.text(6, 53, '1º corte: dois ímãs completos', 8.6, 'gray', anchor='start', weight=700)
    bar(6, 58, 54); bar(64, 58, 54)
    s.line((33, 56), (33, 80), 'ink', 1.0, dash='3 2.4')
    s.line((91, 56), (91, 80), 'ink', 1.0, dash='3 2.4')
    s.text(6, 95, '2º corte: quatro ímãs…', 8.6, 'gray', anchor='start', weight=700)
    for k in range(4):
        bar(6 + k * 29.5, 100, 27)
    x0, w0 = 154, W - 154 - 3
    s.rect(x0, 4, w0, H - 8, 3, fill='red', stroke='red', sw=1.0, dash='4 3')
    s.text(x0 + w0 / 2, 21, 'NÃO se obtém um', 9.2, 'red', weight=700)
    s.text(x0 + w0 / 2, 33, 'polo isolado (monopolo)', 9.2, 'red', weight=700)
    s.rect(x0 + 22, 50, 46, h, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.4)
    s.text(x0 + 45, 50 + h / 2 + 4, 'N', 11, 'white', weight=700)
    s.rect(x0 + 96, 50, 46, h, 0, fill='#FFFFFF', stroke=STROKE['red'], sw=1.4)
    s.text(x0 + 119, 50 + h / 2 + 4, 'S', 11, 'red', weight=700)
    for xa in (x0 + 16, x0 + 90):
        s.line((xa, 74), (xa + 58, 46), 'red', 1.8); s.line((xa, 46), (xa + 58, 74), 'red', 1.8)
    s.text(x0 + w0 / 2, 93, 'cada pedaço volta a ter', 8.4, 'ink')
    s.text(x0 + w0 / 2, 104, 'um polo N e um polo S', 8.4, 'ink')
    s.text(x0 + w0 / 2, 118, '(dipolo magnético)', 8.4, 'gray')
    s.save()
    return s


# ======================================================================================= p01 · atração/repulsão
def poles_force(W=336, H=52):
    s = Svg(W, H, 'poles_force')
    h, w = 14.0, 28.0
    groups = [('atração', 'N', 'S', True), ('repulsão', 'N', 'N', False), ('repulsão', 'S', 'S', False)]
    gw = W / 3
    for i, (lab, p1, p2, attract) in enumerate(groups):
        x0 = i * gw + (gw - (2 * w + 24)) / 2
        y = 8
        xl, xr = x0, x0 + w + 24
        s.magnet(xl, y, w, h, n_left=(p1 == 'S'), size=9.5)      # polo voltado para a direita = p1
        s.magnet(xr, y, w, h, n_left=(p2 == 'N'), size=9.5)      # polo voltado para a esquerda = p2
        yc = y + h / 2
        if attract:
            s.arrow((xl + w - 1, yc), (xl + w + 10, yc), 'green', 1.9, head=6.5)
            s.arrow((xr + 1, yc), (xr - 10, yc), 'green', 1.9, head=6.5)
        else:
            s.arrow((xl + 1, yc), (xl - 13, yc), 'green', 1.9, head=6.5)
            s.arrow((xr + w - 1, yc), (xr + w + 13, yc), 'green', 1.9, head=6.5)
        s.text(i * gw + gw / 2, y + h + 14, lab, 9, 'ink', weight=700)
        s.text(i * gw + gw / 2, y + h + 25, 'polos ' + ('opostos' if attract else 'iguais') + ' voltados', 7.6, 'gray')
    s.save()
    return s


# ======================================================================================= p02 · domínios
def domains(W=336, H=128):
    s = Svg(W, H, 'domains')
    pw, ph, gap = 96.0, 68.0, 19.0
    x0, y0 = 3.0, 26.0
    base = [0, 60, 120, 180, -120, -60]           # soma vetorial nula (sem campo)
    titles = ['sem campo externo', 'campo externo fraco', 'campo externo forte']
    states = [(0.0, [1, 1, 1], 'magnetização ≈ 0'), (0.58, [1.3, 1.15, 0.55], 'magnetização pequena'), (1.0, None, 'saturação')]
    for k, (f, colw, lab) in enumerate(states):
        px = x0 + k * (pw + gap)
        s.text(px + pw / 2, 11, titles[k], 8.6, 'ink', weight=700)
        s.rect(px, y0, pw, ph, 0, fill='paper', stroke='gray', sw=1.3)
        if colw:
            tot = sum(colw); cw = [pw * c / tot for c in colw]
            xs = [px]
            for c in cw: xs.append(xs[-1] + c)
            for j in range(3):
                for i in range(2):
                    ang = base[j * 2 + i] * (1 - f)
                    xa, xb = xs[j], xs[j + 1]; ya, yb = y0 + i * ph / 2, y0 + (i + 1) * ph / 2
                    s.rect(xa, ya, xb - xa, yb - ya, 0, fill='none', stroke='mid', sw=0.9)
                    cxm, cym = (xa + xb) / 2, (ya + yb) / 2
                    Ln = min(27, (xb - xa) * 0.66)
                    r = math.radians(ang)
                    s.arrow((cxm - math.cos(r) * Ln / 2, cym + math.sin(r) * Ln / 2), (cxm + math.cos(r) * Ln / 2, cym - math.sin(r) * Ln / 2), 'gray', 1.7, head=6)
        else:
            for yy in (y0 + 17, y0 + 34, y0 + 51):
                s.arrow((px + 14, yy), (px + pw - 14, yy), 'gray', 1.7, head=6)
        s.text(px + pw / 2, y0 + ph + 13, lab, 8.2, 'gray')
    for k in (1, 2):                              # campo aplicado (azul)
        px = x0 + k * (pw + gap)
        s.arrow((px - gap + 3, y0 + ph / 2), (px - 3, y0 + ph / 2), 'blue', 2.0, head=7.5)
    s.save()
    return s


# ======================================================================================= p02 · três respostas
def materials3(W=688, H=226):
    s = Svg(W, H, 'materials3')
    lab_w = 70.0
    colw = (W - lab_w) / 3
    names = [('Ferromagnético', 'Fe, Co, Ni e ligas'), ('Paramagnético', 'Al, Pt, O_{2} líquido'), ('Diamagnético', 'Cu, Au, água, grafite')]
    pw, ph = 128.0, 56.0
    rows_y = [30.0, 94.0]
    rng = np.random.RandomState(7)
    para_ang = [rng.uniform(-180, 180) for _ in range(18)]
    s.text(0, 55, 'sem campo', 8.6, 'gray', anchor='start', weight=700)
    s.text(0, 66, 'externo', 8.6, 'gray', anchor='start', weight=700)
    s.text(0, 111, 'com campo', 8.6, 'blue', anchor='start', weight=700)
    s.text(0, 122, 'externo B', 8.6, 'blue', anchor='start', weight=700)
    for k, (nm, ex) in enumerate(names):
        x = lab_w + k * colw + (colw - pw) / 2
        s.text(lab_w + k * colw + colw / 2, 12, nm, 10, 'navy', weight=700)
        s.text(lab_w + k * colw + colw / 2, 23, ex, 8.2, 'gray')
        for r in (0, 1):
            y = rows_y[r]
            s.rect(x, y, pw, ph, 0, fill='paper', stroke='gray', sw=1.2)
            on = (r == 1)
            if k == 0:   # ferro: 2×2 domínios
                if on:
                    for yy in (y + 14, y + 30, y + 46):
                        s.arrow((x + 14, yy), (x + pw - 14, yy), 'gray', 1.8, head=6.2)
                else:
                    s.line((x + pw / 2, y), (x + pw / 2, y + ph), 'mid', 0.9)
                    s.line((x, y + ph / 2), (x + pw, y + ph / 2), 'mid', 0.9)
                    for q, a_ in enumerate([0, 90, 180, -90]):
                        cxm = x + pw / 4 + (q % 2) * pw / 2; cym = y + ph / 4 + (q // 2) * ph / 2
                        rr = math.radians(a_)
                        s.arrow((cxm - math.cos(rr) * 10, cym + math.sin(rr) * 10), (cxm + math.cos(rr) * 10, cym - math.sin(rr) * 10), 'gray', 1.8, head=6.2)
            elif k == 1:  # para
                for q in range(18):
                    cxm = x + 12 + (q % 6) * 21.6; cym = y + 11 + (q // 6) * 19
                    rr = math.radians(para_ang[q] * (0.34 if on else 1.0)); Ln = 7.5
                    s.arrow((cxm - math.cos(rr) * Ln, cym + math.sin(rr) * Ln), (cxm + math.cos(rr) * Ln, cym - math.sin(rr) * Ln), 'gray', 1.4, head=5.2)
            else:         # dia
                for q in range(18):
                    cxm = x + 12 + (q % 6) * 21.6; cym = y + 11 + (q // 6) * 19
                    s.circle((cxm, cym), 5.2, fill='none', stroke='mid', w=1.0)
                    if on:
                        s.arrow((cxm + 3.4, cym), (cxm - 3.4, cym), 'gray', 1.3, head=4.2)
            if on:
                s.arrow((x - 22, y + ph / 2), (x - 4, y + ph / 2), 'blue', 2.0, head=7.5)
        s.text(x + pw / 2, rows_y[1] + ph + 10.0, ['momentos alinhados: M grande, no sentido de B', 'alinhamento parcial: M pequena, no sentido de B', 'momentos induzidos: M pequena, oposta a B'][k], 7.9, 'gray')
        yf = 182.0                                   # linha da força em campo não uniforme
        s.rect(x - 2, yf - 11, 30, 22, 0, fill=STROKE['red'], stroke=STROKE['red'], sw=1.2)
        s.text(x + 13, yf + 4, 'N', 10.5, 'white', weight=700)
        if k == 0:
            s.rect(x + 56, yf - 8, 16, 16, 0, fill='#E4E8EE', stroke='gray', sw=1.0)
            s.arrow((x + 52, yf), (x + 32, yf), 'green', 2.6, head=8.5)
            s.text(x + 82, yf + 3.5, 'atração forte', 8.4, 'green', anchor='start', weight=700)
        elif k == 1:
            s.rect(x + 56, yf - 8, 16, 16, 0, fill='#E4E8EE', stroke='gray', sw=1.0)
            s.arrow((x + 52, yf), (x + 38, yf), 'green', 1.8, head=7)
            s.text(x + 82, yf + 3.5, 'atração fraca', 8.4, 'green', anchor='start', weight=700)
        else:
            s.rect(x + 40, yf - 8, 16, 16, 0, fill='#E4E8EE', stroke='gray', sw=1.0)
            s.arrow((x + 60, yf), (x + 76, yf), 'green', 1.8, head=7)
            s.text(x + 84, yf + 3.5, 'repulsão fraca', 8.4, 'green', anchor='start', weight=700)
    for i, t in enumerate(['amostra perto', 'de um polo', '(campo não', 'uniforme)']):
        s.text(0, 174 + i * 11, t, 8.6, 'gray', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p03 · Terra
def dipole_B(xm, zm):
    r2 = xm * xm + zm * zm
    r5 = r2 ** 2.5
    return 3 * zm * xm / r5, (3 * zm * zm - r2) / r5


def earth_field(W=352, H=280, tilt_deg=10.0):
    s = Svg(W, H, 'earth_field')
    cx, cy, R = W / 2, H / 2 + 1, 47.0
    t = math.radians(tilt_deg)
    u = (math.sin(t), math.cos(t))          # +z do dipolo (m aponta ao sul geográfico); imagem com y para baixo
    e = (math.cos(t), -math.sin(t))
    img = lambda xm, zm: (cx + R * (xm * e[0] + zm * u[0]), cy + R * (xm * e[1] + zm * u[1]))
    s.line((cx, cy - R * 1.62), (cx, cy + R * 1.62), 'gray', 1.2, dash='5 3')
    ax_t, ax_b = img(0, -1.9), img(0, 1.9)
    s.line(ax_t, ax_b, 'blue', 1.2, dash='2 3')
    for k, r0 in enumerate((1.55, 2.0, 2.6, 3.3)):
        th = np.linspace(0.02, math.pi - 0.02, 400)
        for sg in (+1, -1):
            xm = sg * r0 * np.sin(th) ** 3
            zm = r0 * np.sin(th) ** 2 * np.cos(th)
            vis = [(x_, z_) for x_, z_ in zip(xm, zm) if math.hypot(x_, z_) > 1.02]
            P = [img(x_, z_) for x_, z_ in vis]
            s.polyline(P, 'blue', 1.1, opacity=0.9)
            n = len(P)
            s.arrow_at(P, 0.5, 'blue', 1.1, head=6.4)
            if k < 2:                                  # setas perto dos polos: saem no sul, entram no norte
                s.arrow_at(P, 0.1, 'blue', 1.1, head=6.4)
                s.arrow_at(P, 0.9, 'blue', 1.1, head=6.4)
    s.circle((cx, cy), R, fill='#F3F6FA', stroke='navy', w=1.6)
    for lat in (-60, -30, 0, 30, 60):
        y_ = cy - R * math.sin(math.radians(lat)); half = R * math.cos(math.radians(lat))
        s.line((cx - half, y_), (cx + half, y_), 'light', 0.8)
    s.ellipse((cx, cy), R * 0.42, R, fill='none', stroke='light', w=0.8)
    s.circle((cx, cy - R), 2.6, fill='gray', stroke=None); s.circle((cx, cy + R), 2.6, fill='gray', stroke=None)
    # polos do dipolo equivalente (extremidades do eixo magnético na superfície)
    top, bot = img(0, -1.0), img(0, 1.0)
    s.circle(top, 7.5, fill='#FFFFFF', stroke='red', w=1.8); s.text(top[0], top[1] + 3.6, 'S', 10, 'red', weight=700)
    s.circle(bot, 7.5, fill=STROKE['red'], stroke='red', w=1.8); s.text(bot[0], bot[1] + 3.6, 'N', 10, 'white', weight=700)
    # bússola no hemisfério norte, alinhada ao campo local
    ang_pos = math.radians(58)
    pc = (cx + (R + 14) * math.sin(ang_pos), cy - (R + 14) * math.cos(ang_pos))
    xm = ((pc[0] - cx) * e[0] + (pc[1] - cy) * e[1]) / R
    zm = ((pc[0] - cx) * u[0] + (pc[1] - cy) * u[1]) / R
    bx, bz = dipole_B(xm, zm)
    bi = (bx * e[0] + bz * u[0], bx * e[1] + bz * u[1])
    s.compass(pc, math.degrees(math.atan2(-bi[1], bi[0])), r=8.8)
    s.text(pc[0] + 12, pc[1] + 2, 'bússola', 8, 'gray', anchor='start')
    # rótulos
    s.text(cx + 7, cy - R * 1.62 - 6, 'Polo Norte geográfico', 9, 'navy', anchor='start', weight=700)
    s.text(cx + 7, cy + R * 1.62 + 13, 'Polo Sul geográfico', 9, 'navy', anchor='start', weight=700)
    s.text(cx - 14, cy - R * 1.62 + 24, 'eixo de rotação', 8, 'gray', anchor='end')
    s.text(ax_t[0] - 6, ax_t[1] + 2, 'eixo do dipolo', 8, 'blue', anchor='end')
    s.text(ax_t[0] - 6, ax_t[1] + 12, '(~10°, varia com o tempo)', 8, 'blue', anchor='end')
    s.text(W - 4, 22, 'perto do Polo Norte geográfico:', 8.4, 'red', anchor='end')
    s.text(W - 4, 33, 'polo SUL do ímã equivalente', 8.8, 'red', anchor='end', weight=700)
    s.text(4, H - 24, 'perto do Polo Sul geográfico:', 8.4, 'red', anchor='start')
    s.text(4, H - 13, 'polo NORTE do ímã equivalente', 8.8, 'red', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p03 · ⊙ ⊗ e corrente convencional
def vec_conv(W=336, H=92):
    s = Svg(W, H, 'vec_conv')
    s.sym_out((20, 24), 12, 'blue', 1.8)
    s.text(40, 21, 'saindo do plano', 9.4, 'blue', anchor='start', weight=700)
    s.text(40, 33, 'vê-se a ponta da seta', 8.2, 'gray', anchor='start')
    s.sym_in((20, 66), 12, 'blue', 1.8)
    s.text(40, 63, 'entrando no plano', 9.4, 'blue', anchor='start', weight=700)
    s.text(40, 75, 'veem-se as penas (cauda)', 8.2, 'gray', anchor='start')
    # circuito: + na esquerda da bateria => corrente convencional sai por ela, horária
    x0, x1, y0, y1 = 186, 322, 32, 80
    mid = (x0 + x1) / 2
    s.polyline([(mid - 12, y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1), (mid + 12, y1)], 'ink', 1.6)
    s.battery((mid, y1), True, 15)
    s.text(mid - 9.5, y1 - 12, '+', 10, 'red', weight=700)
    s.text(mid + 9.5, y1 - 12, '−', 10, 'red', weight=700)
    s.arrow((x0 + 40, y0), (x0 + 84, y0), 'orange', 2.2, head=8)
    s.vtext(x0 + 62, y0 - 5, 'I', size=11.5, color='orange', arrow=False)
    s.arrow((x1 - 28, y0 + 14), (x1 - 70, y0 + 14), 'cyan', 1.6, head=7)
    s.text(x1 - 49, y0 + 25, 'elétrons', 8, 'cyan', weight=700)
    s.text(x0 - 4, 10, 'corrente convencional: do + para o −', 8.2, 'orange', anchor='start', weight=700)
    s.save()
    return s


# ======================================================================================= p03 · exercício das bússolas
def compass_pole(W=300, H=118):
    s = Svg(W, H, 'compass_pole')
    cx, cy, L, h = W / 2, 62, 110, 26
    s.rect(cx - L / 2, cy - h / 2, L, h, 0, fill='#E4E8EE', stroke='gray', sw=1.6)
    s.line((cx, cy - h / 2), (cx, cy + h / 2), 'gray', 1.0)
    s.text(cx - L / 4, cy + 5, 'X', 14, 'ink', weight=700)
    s.text(cx + L / 4, cy + 5, 'Y', 14, 'ink', weight=700)
    # campo de um ímã com N à direita: eixo -> direita; acima do ímã -> esquerda
    s.compass((cx - L / 2 - 26, cy), 0, r=10)
    s.compass((cx + L / 2 + 26, cy), 0, r=10)
    s.compass((cx, cy - 36), 180, r=10)
    s.text(cx - L / 2 - 26, cy + 24, 'A', 10, 'gray', weight=700)
    s.text(cx + L / 2 + 26, cy + 24, 'C', 10, 'gray', weight=700)
    s.text(cx + 22, cy - 33, 'B', 10, 'gray', weight=700)
    s.save()
    return s


# ======================================================================================= p03 · soma vetorial (bússola)
def vec_sum(W=176, H=124):
    s = Svg(W, H, 'vec_sum')
    ox, oy = 48, 98
    k = 2.8                                                  # px por µT
    BT, BF = 20.0, 20.0
    # eixos: norte para cima, leste para a direita
    s.line((ox - 6, oy), (ox + 112, oy), 'light', 1.0); s.line((ox, oy + 6), (ox, oy - 86), 'light', 1.0)
    s.text(ox + 114, oy + 12, 'L', 9, 'gray', weight=700); s.text(ox - 9, oy - 86, 'N', 9, 'gray', weight=700)
    s.arrow((ox, oy), (ox, oy - BT * k), 'blue', 2.0, head=8)
    s.arrow((ox, oy), (ox + BF * k, oy), 'blue', 2.0, head=8)
    s.arrow((ox, oy), (ox + BF * k, oy - BT * k), 'blue', 2.6, head=9)
    s.line((ox + BF * k, oy), (ox + BF * k, oy - BT * k), 'blue', 1.0, dash='3 3')
    s.line((ox, oy - BT * k), (ox + BF * k, oy - BT * k), 'blue', 1.0, dash='3 3')
    s.vtext(ox - 22, oy - BT * k / 2 + 4, 'B', sub='T', size=11.5, color='blue')
    s.vtext(ox + BF * k / 2, oy + 17, 'B', sub='fio', size=11.5, color='blue')
    s.vtext(ox + BF * k + 14, oy - BT * k - 6, 'B', sub='res', size=11.5, color='blue')
    # arco do ângulo
    import math
    r = 24
    s.path(f'M {ox} {oy - r} A {r} {r} 0 0 1 {ox + r * math.sin(math.radians(45)):.2f} {oy - r * math.cos(math.radians(45)):.2f}', stroke='gray', w=1.1)
    s.text(ox + 12, oy - 31, '45°', 8.6, 'gray')
    s.save()
    return s


if __name__ == '__main__':
    for fn in (cover_art, magnet_field, magnet_split, poles_force, domains, materials3, earth_field, vec_conv, compass_pole, vec_sum):
        fn()
