"""Gráficos de polinômios gerados a partir das funções reais (matplotlib -> SVG)."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), 'svg')
BLUE, PURPLE, GREEN, ORANGE, RED, GRAY, INK = '#1f5fbf', '#7a3fc2', '#167a44', '#d4690a', '#c62828', '#5f6b7a', '#1a2233'
plt.rcParams.update({'svg.fonttype': 'path', 'font.family': ['Inter', 'DejaVu Sans'], 'mathtext.fontset': 'cm', 'font.size': 8,
                     'axes.edgecolor': '#8a95a5', 'axes.linewidth': 0.8, 'xtick.color': GRAY, 'ytick.color': GRAY})
MM = 1 / 25.4


def style(ax, xlim, ylim, xt=None, yt=None):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
    ax.grid(True, color='#e3e7ed', lw=0.6); ax.set_axisbelow(True)
    ax.tick_params(labelsize=7, length=2.5)
    if xt is not None: ax.set_xticks(xt)
    if yt is not None: ax.set_yticks(yt)
    ax.plot(1, 0, '>', transform=ax.get_yaxis_transform(), clip_on=False, ms=3.5, color=BLUE)
    ax.plot(0, 1, '^', transform=ax.get_xaxis_transform(), clip_on=False, ms=3.5, color=PURPLE)


def fig_graph_roots():
    fig, axs = plt.subplots(1, 2, figsize=(184 * MM, 54 * MM))
    x = np.linspace(-1.7, 2.7, 400)
    P = lambda t: (t + 1) * (t - 1) * (t - 2)
    ax = axs[0]
    ax.plot(x, P(x), color=BLUE, lw=1.7)
    for r in (-1, 1, 2): ax.plot([r], [0], 'o', color=GREEN, ms=5, zorder=5)
    style(ax, (-1.9, 2.9), (-2.6, 3.4), xt=[-1, 0, 1, 2], yt=[-2, 2])
    ax.set_title(r'$P(x)=(x+1)(x-1)(x-2)$: raízes reais $-1,\ 1,\ 2$' + '\n(pontos em que o gráfico encontra o eixo $x$)', fontsize=7.6, color=INK, loc='left')
    ax = axs[1]
    Q = lambda t: t ** 2 + 1
    ax.plot(x, Q(x), color=PURPLE, lw=1.7)
    style(ax, (-1.9, 2.9), (-0.8, 6.0), xt=[-1, 0, 1, 2], yt=[1, 5])
    ax.set_title(r'$Q(x)=x^2+1$: raízes $\pm i$ (não reais)' + '\n(o gráfico NÃO toca o eixo $x$)', fontsize=7.6, color=INK, loc='left')
    fig.tight_layout(pad=0.6, w_pad=1.6)
    fig.savefig(os.path.join(OUT, 'fig_graph_roots.svg'), format='svg'); plt.close(fig)


def fig_mult3():
    fig, axs = plt.subplots(1, 3, figsize=(184 * MM, 37 * MM))
    x = np.linspace(-1.5, 1.5, 400)
    specs = [(lambda t: t, r'$P(x)=x$', 'raiz simples', 'cruza o eixo (muda de sinal)', BLUE),
             (lambda t: t ** 2, r'$P(x)=x^2$', 'raiz dupla', 'toca o eixo e volta (não muda de sinal)', ORANGE),
             (lambda t: t ** 3, r'$P(x)=x^3$', 'raiz tripla', 'cruza o eixo, achatando-se (muda de sinal)', PURPLE)]
    for ax, (fn, name, m, desc, col) in zip(axs, specs):
        ax.plot(x, fn(x), color=col, lw=1.8)
        ax.plot([0], [0], 'o', color=GREEN, ms=5, zorder=5)
        style(ax, (-1.6, 1.6), (-1.35, 1.9), xt=[-1, 1], yt=[-1, 1])
        ax.set_title(f'{name}  ·  {m}\n{desc}', fontsize=7.2, color=INK, loc='left')
    fig.tight_layout(pad=0.6, w_pad=1.2)
    fig.savefig(os.path.join(OUT, 'fig_mult3.svg'), format='svg'); plt.close(fig)


def fig_mult_poly():
    """Três janelas locais do MESMO polinômio P(x) = (x+2)(x-1)^2(x-3)^3, uma por raiz."""
    fig, axs = plt.subplots(1, 3, figsize=(184 * MM, 41 * MM))
    P = lambda t: (t + 2) * (t - 1) ** 2 * (t - 3) ** 3
    wins = [(-2, (-2.4, -1.6), GREEN, 'raiz $-2$: simples', 'sinal: $+\\to-$ (cruza)'),
            (1, (0.35, 1.65), ORANGE, 'raiz $1$: dupla', 'sinal: $-\\to-$ (toca, não cruza)'),
            (3, (2.3, 3.7), PURPLE, 'raiz $3$: tripla', 'sinal: $-\\to+$ (cruza, achatada)')]
    for ax, (r, (a_, b_), col, t1, t2) in zip(axs, wins):
        x = np.linspace(a_, b_, 300)
        ax.plot(x, P(x), color=BLUE, lw=1.8)
        ax.plot([r], [0], 'o', color=col, ms=5.5, zorder=5)
        ax.axhline(0, color=BLUE, lw=0.9)
        ax.set_xlim(a_, b_)
        ys = P(x); lo, hi = min(ys.min(), 0), max(ys.max(), 0); pad = 0.12 * (hi - lo)
        ax.set_ylim(lo - pad, hi + pad)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['bottom'].set_visible(False)
        ax.set_xticks([r]); ax.tick_params(labelsize=7, length=2.5)
        ax.grid(True, color='#e3e7ed', lw=0.6); ax.set_axisbelow(True)
        ax.set_title(t1 + '\n' + t2, fontsize=7.4, color=col, loc='left', fontweight='bold')
    fig.suptitle('Mesmo polinômio  $P(x)=(x+2)(x-1)^2(x-3)^3$, observado perto de cada raiz', fontsize=7.4, color=INK, x=0.01, ha='left', y=0.995)
    fig.tight_layout(pad=0.5, w_pad=1.4, rect=(0, 0, 1, 0.9))
    fig.savefig(os.path.join(OUT, 'fig_mult_poly.svg'), format='svg'); plt.close(fig)


def fig_graph_roots_wrapper(): fig_graph_roots(); return None
def fig_mult3_wrapper(): fig_mult3(); return None
def fig_mult_poly_wrapper(): fig_mult_poly(); return None


ALL = [fig_graph_roots_wrapper, fig_mult3_wrapper, fig_mult_poly_wrapper]
