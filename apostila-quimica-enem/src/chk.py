"""Verificações químicas automáticas: balanceamento e massas (RDKit)."""
from collections import Counter
from rdkit import Chem
from rdkit.Chem import Descriptors
from lib import QC

def atoms(smi):
    m = Chem.AddHs(Chem.MolFromSmiles(smi)); c = Counter(a.GetSymbol() for a in m.GetAtoms()); return c

def balanced(name, lhs, rhs):
    """lhs/rhs: lista de (coef, smiles). Levanta erro se não balanceada (conserva elementos; carga ignorada)."""
    L, R = Counter(), Counter()
    for k, s in lhs:
        for e, n in atoms(s).items(): L[e] += k*n
    for k, s in rhs:
        for e, n in atoms(s).items(): R[e] += k*n
    assert L == R, f'{name} NÃO balanceada: {dict(L)} ≠ {dict(R)}'
    QC.append(f'OK equação balanceada: {name}  ({dict(sorted(L.items()))})')
    return True

def MM(smi):
    return Descriptors.MolWt(Chem.MolFromSmiles(smi))

def num(name, value, expected, tol=0.02):
    """Verifica um cálculo do texto contra o valor calculado em código."""
    ok = abs(value - expected) <= tol * abs(expected)
    assert ok, f'{name}: calculado {value} ≠ texto {expected}'
    QC.append(f'OK cálculo: {name} = {value:.4g} (texto: {expected})')
    return value

import re as _re
def parse_formula(f):
    """Conta átomos de uma fórmula como 'Al2(SO4)3' ou 'Ca(OH)2' (sem cargas)."""
    def rec(s):
        tokens = _re.findall(r'\(|\)\d*|[A-Z][a-z]?\d*', s); stack = [Counter()]
        for t in tokens:
            if t == '(': stack.append(Counter())
            elif t.startswith(')'):
                k = int(t[1:] or 1); c = stack.pop()
                for e, n in c.items(): stack[-1][e] += n*k
            else:
                m = _re.match(r'([A-Z][a-z]?)(\d*)', t); stack[-1][m.group(1)] += int(m.group(2) or 1)
        return stack[0]
    return rec(f)

def fbal(name, lhs, rhs):
    """Balanceamento por fórmula: lhs/rhs = [(coef, 'H2SO4'), ...]."""
    L, R = Counter(), Counter()
    for k, f in lhs:
        for e, n in parse_formula(f).items(): L[e] += k*n
    for k, f in rhs:
        for e, n in parse_formula(f).items(): R[e] += k*n
    assert L == R, f'{name} NÃO balanceada: {dict(L)} ≠ {dict(R)}'
    QC.append(f'OK equação balanceada: {name}')

def fmass(f, masses=None):
    mm = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0, 'Mg': 24.0, 'Al': 27.0, 'S': 32.0, 'Cl': 35.5, 'K': 39.0, 'Ca': 40.0, 'Fe': 56.0, 'Cu': 63.5, 'Zn': 65.0, 'Ag': 108.0}
    if masses: mm.update(masses)
    return sum(mm[e]*n for e, n in parse_formula(f).items())
