# -*- coding: utf-8 -*-
"""Figuras reutilizáveis: lipídios, bicamada, micela, água, béquer."""
import math, random
from lib import *

def lipid(s, x, y, d=1, L=40, r=6.2, kink=(False, True), head_fill='url(#dots-blue)', sw=2.0):
    """Fosfolipídio esquemático: cabeça polar (círculo azul pontilhado) e duas caudas apolares (âmbar).
    d=+1 caudas para baixo; d=-1 para cima. kink: (cauda1, cauda2) insaturada com dobra cis."""
    for dx, k in ((-2.9, kink[0]), (2.9, kink[1])):
        px, py = x + dx, y + d*r*0.8
        pts = [(px, py)]
        n = 8; seg = L / n
        for i in range(1, n+1):
            off = 0
            if k and i in (4, 5): off = 3.6 * (1 if i == 4 else -1) * 1.0
            pts.append((px + off, py + d*seg*i))
        s.poly(pts, stroke=AMBER, sw=sw)
    s.circ(x, y, r, head_fill, BLUE, 1.8)

def bilayer(s, x0, y0, width, n, L=40, gap=10, r=6.2, kink_every=3):
    """Bicamada: folheto superior (cabeças em cima) e inferior (cabeças embaixo). Retorna (y_topo_cabeca, y_base)."""
    step = width / n
    ytop = y0
    ybot = y0 + 2*L + 2*r + gap
    for i in range(n):
        x = x0 + step*(i+0.5)
        kk = (False, i % kink_every == 0)
        lipid(s, x, ytop, 1, L, r, kk)
        lipid(s, x + step*0.0, ybot, -1, L, r, (False, (i+1) % kink_every == 0))
    return ytop, ybot

def water_mol(s, x, y, rot=0, sc=1.0):
    """Molécula de água (O azul, 2 H claros) via <use> para manter o PDF leve."""
    s.add(f'<use href="#wm" transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sc})"/>')

def water_field(s, x0, y0, w, h, step=22, seed=3):
    """Fundo de água (padrão ladrilhado reutilizável: mantém o PDF leve)."""
    s.rect(x0, y0, w, h, 'url(#waterbg)')

def micelle(s, cx, cy, R=44, n=14, L=30, r=5.4, core_text=None, oil=False):
    """Micela esférica: cabeças para fora (água), caudas para dentro."""
    if oil: s.circ(cx, cy, R - 6, '#FFF3D0', AMBER_D, 1.2)
    for i in range(n):
        a = 2*math.pi*i/n
        hx, hy = cx + R*math.cos(a), cy + R*math.sin(a)
        tx, ty = cx + (R - L - 4)*math.cos(a), cy + (R - L - 4)*math.sin(a)
        s.line(hx - math.cos(a)*r*0.5, hy - math.sin(a)*r*0.5, tx, ty, AMBER, 2.6)
    for i in range(n):
        a = 2*math.pi*i/n
        hx, hy = cx + R*math.cos(a), cy + R*math.sin(a)
        s.circ(hx, hy, r, 'url(#dots-blue)', BLUE, 1.6)
    if core_text: s.text(cx, cy + 3, core_text, 9.5, AMBER_D, 'middle', 700)

def beaker(s, x, y, w, h, fill_level=0.72, liquid='#EAF3FD', stroke=GRAY):
    s.path(f'M{x},{y} L{x},{y+h} Q{x},{y+h+6} {x+8},{y+h+6} L{x+w-8},{y+h+6} Q{x+w},{y+h+6} {x+w},{y+h} L{x+w},{y}', stroke=stroke, sw=2)
    ly = y + h*(1 - fill_level)
    return ly

def vesicle(s, cx, cy, R=62, th=30, n_out=22, n_in=14, r=5.2):
    """Lipossomo: bicamada fechada; água dentro e fora."""
    Ri = R - th
    for i in range(n_out):
        a = 2*math.pi*i/n_out
        s.line(cx + (R - r)*math.cos(a), cy + (R - r)*math.sin(a), cx + (R - th/2 + 1)*math.cos(a), cy + (R - th/2 + 1)*math.sin(a), AMBER, 2)
    for i in range(n_in):
        a = 2*math.pi*(i + 0.5)/n_in
        s.line(cx + (Ri + r)*math.cos(a), cy + (Ri + r)*math.sin(a), cx + (Ri + th/2 - 1)*math.cos(a), cy + (Ri + th/2 - 1)*math.sin(a), AMBER, 2)
    for i in range(n_out):
        a = 2*math.pi*i/n_out; s.circ(cx + R*math.cos(a), cy + R*math.sin(a), r, 'url(#dots-blue)', BLUE, 1.5)
    for i in range(n_in):
        a = 2*math.pi*(i + 0.5)/n_in; s.circ(cx + Ri*math.cos(a), cy + Ri*math.sin(a), r, 'url(#dots-blue)', BLUE, 1.5)

def mini_beaker(s, x, y, w, h, layers):
    """layers: lista de (fração, fill, label) de cima para baixo (dentro do béquer)."""
    top = y + h*0.18
    yy = top
    total = sum(f for f, _, _ in layers)
    for f, fill, lab in layers:
        hh = (y + h - 4 - top) * f / total
        s.rect(x+2, yy, w-4, hh, fill, op=1)
        yy += hh
    s.path(f'M{x},{y} L{x},{y+h-6} Q{x},{y+h} {x+8},{y+h} L{x+w-8},{y+h} Q{x+w},{y+h} {x+w},{y+h-6} L{x+w},{y}', stroke=GRAY, sw=2.2)
