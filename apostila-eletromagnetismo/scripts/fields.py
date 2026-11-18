"""Modelos numéricos de campo magnético usados nos diagramas (e verificados em validate_physics.py).

Campo de espira circular: integrais elípticas completas (solução exata de Biot–Savart no plano ρ–z).
Ímã em barra e solenoide: empilhamento de espiras (ímã uniformemente magnetizado ≡ solenoide de mesmo comprimento),
o que fornece linhas de B FECHADAS, com B interno de S→N, sem monopolos fictícios.
"""
import math
import numpy as np
from scipy.special import ellipk, ellipe


def loop_B(rho, z, a=1.0):
    """(Bρ, Bz) em unidades de μ0·I/(2π) para espira de raio a em z=0; corrente anti-horária vista de +z."""
    rho = np.abs(np.asarray(rho, float))
    z = np.asarray(z, float)
    den1 = np.sqrt((a + rho) ** 2 + z ** 2)
    den2 = (a - rho) ** 2 + z ** 2
    k2 = np.clip(4 * a * rho / den1 ** 2, 0.0, 1 - 1e-13)
    K, E = ellipk(k2), ellipe(k2)
    Bz = (K + (a ** 2 - rho ** 2 - z ** 2) / den2 * E) / den1
    with np.errstate(divide='ignore', invalid='ignore'):
        Br = np.where(rho < 1e-9, 0.0, (z / np.where(rho < 1e-9, 1, rho)) * (-K + (a ** 2 + rho ** 2 + z ** 2) / den2 * E) / den1)
    return Br, Bz


def stack_B(rho, z, a, L, n=160):
    """n espiras igualmente espaçadas em [-L/2, L/2]; retorna (Bρ, Bz) normalizados pela média (direção correta)."""
    zs = np.linspace(-L / 2, L / 2, n)
    Br = 0.0
    Bz = 0.0
    for zk in zs:
        br, bz = loop_B(rho, np.asarray(z) - zk, a)
        Br = Br + br
        Bz = Bz + bz
    return Br / n, Bz / n


def make_planar(Bfun):
    """campo no plano que contém o eixo: x com sinal (ρ=|x|), eixo = z."""
    def f(x, z):
        br, bz = Bfun(abs(x), z)
        return float(math.copysign(1.0, x if x != 0 else 1.0) * br), float(bz)
    return f


def trace(field, p0, ds=0.02, nmax=40000, bounds=(-1e9, 1e9, -1e9, 1e9), direction=1, close_tol=None, min_steps=80):
    """integra dp/ds = ±B/|B| (RK4). Termina ao sair de 'bounds' ou ao fechar a curva."""
    def f(q):
        bx, bz = field(q[0], q[1])
        n = math.hypot(bx, bz) + 1e-30
        return direction * np.array([bx / n, bz / n])
    p = np.array(p0, float)
    pts = [p.copy()]
    for i in range(nmax):
        k1 = f(p); k2 = f(p + ds / 2 * k1); k3 = f(p + ds / 2 * k2); k4 = f(p + ds * k3)
        p = p + ds / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(p.copy())
        if not (bounds[0] <= p[0] <= bounds[1] and bounds[2] <= p[1] <= bounds[3]):
            break
        if close_tol and i > min_steps and np.hypot(*(p - np.asarray(p0))) < close_tol:
            pts.append(np.asarray(p0, float))
            break
    return np.array(pts)


def full_line(field, seed, ds=0.02, bounds=(-1e9, 1e9, -1e9, 1e9)):
    """linha completa por 'seed', orientada no sentido de B (inclui trecho para trás)."""
    fwd = trace(field, seed, ds, bounds=bounds, direction=1, close_tol=ds * 1.2)
    closed = np.hypot(*(fwd[-1] - np.asarray(seed))) < ds * 1.5 and len(fwd) > 90
    if closed:
        return fwd, True
    bwd = trace(field, seed, ds, bounds=bounds, direction=-1)
    return np.vstack([bwd[::-1], fwd[1:]]), False


# ------------------------------------------------------------------------------ dipolo (Terra)
def dipole_lines(n_lines=7, rmax=(0.55, 0.8, 1.15, 1.6, 2.2, 3.0, 4.2), npts=181, eps=0.04):
    """linhas de campo de um dipolo com m apontando para +z (no plano x–z).
    r = r0·sin²θ (θ medido a partir de +z). B sai pelo lado de +z (polo N do dipolo) e entra pelo lado de −z.
    Retorna lista de curvas (x, z) orientadas no sentido de B, para os dois lados (x>0 e x<0)."""
    out = []
    for r0 in rmax:
        th = np.linspace(eps, math.pi - eps, npts)
        r = r0 * np.sin(th) ** 2
        x, z = r * np.sin(th), r * np.cos(th)
        # em θ pequeno (perto de +z) o campo aponta para fora (+r); logo a linha vai de θ=0 até θ=π no lado x>0
        out.append((x, z))
        out.append((-x, z))
    return out


# ------------------------------------------------------------------------------ autotestes
if __name__ == '__main__':
    br, bz = loop_B(0.0, 0.0, 1.0)
    print('espira, centro: Bz·(2π/μ0I) =', float(bz), ' esperado π =', math.pi)
    # solenoide longo: B/(μ0 N I / L) -> 1
    a, L, n = 1.0, 40.0, 400
    br, bz = stack_B(0.0, 0.0, a, L, n)
    print('solenoide longo (L/a=40): B/(μ0 n I) =', float(bz * L / (2 * math.pi)))
    br, bz = stack_B(0.0, L / 2, a, L, n)
    print('   na extremidade (eixo): B/(μ0 n I) =', float(bz * L / (2 * math.pi)), '(esperado ≈ 0,5)')
