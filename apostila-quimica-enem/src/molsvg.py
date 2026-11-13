"""Desenho de moléculas verificável (RDKit) com grupos funcionais destacados."""
import re
from rdkit import Chem
from rdkit.Chem import Draw, rdDepictor, Descriptors, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D

PURPLE = (0.48, 0.25, 0.75)
PURPLE_L = (0.78, 0.62, 0.92)
BLUE_L = (0.62, 0.78, 0.95)
AMBER_L = (1.0, 0.82, 0.35)
GREEN_L = (0.6, 0.85, 0.7)
ORANGE_L = (1.0, 0.7, 0.45)
RED_L = (0.97, 0.6, 0.62)
COLORS = dict(purple=PURPLE_L, blue=BLUE_L, amber=AMBER_L, green=GREEN_L, orange=ORANGE_L, red=RED_L)

def parse(smiles, labels=None):
    m = Chem.MolFromSmiles(smiles)
    assert m is not None, f"SMILES inválido: {smiles}"
    if labels:
        for idx, lab in labels.items():
            m.GetAtomWithIdx(idx).SetProp('atomLabel', lab)
    return m

def formula(smiles):
    m = Chem.MolFromSmiles(smiles)
    return rdMolDescriptors.CalcMolFormula(m)

def mass(smiles):
    return Descriptors.MolWt(Chem.MolFromSmiles(smiles))

def match(m, smarts):
    """Retorna matches; se o SMARTS tiver átomos mapeados (:1), devolve só os mapeados."""
    p = Chem.MolFromSmarts(smarts)
    assert p is not None, smarts
    mapped = [a.GetIdx() for a in p.GetAtoms() if a.GetAtomMapNum() > 0]
    res = m.GetSubstructMatches(p)
    if mapped:
        res = tuple(tuple(mt[i] for i in mapped) for mt in res)
    return res

def mol_svg(smiles, w=200, h=130, hl=None, labels=None, bw=2.0, fs=15, rot=0, hl_atoms=None, pins=None, pad=0.12, notes=None):
    """hl: lista de (smarts, cor) ; hl_atoms: {idx: cor} direto ; pins: lista de (smarts, n)"""
    m = parse(smiles, labels)
    rdDepictor.SetPreferCoordGen(True)
    rdDepictor.Compute2DCoords(m)
    if rot:
        import math
        from rdkit.Geometry import Point3D
        conf = m.GetConformer()
        c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        for i in range(m.GetNumAtoms()):
            p = conf.GetAtomPosition(i)
            conf.SetAtomPosition(i, Point3D(p.x*c - p.y*sn, p.x*sn + p.y*c, 0))
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.useBWAtomPalette()
    o.bondLineWidth = bw
    o.padding = pad
    o.clearBackground = False
    o.fixedFontSize = fs
    o.minFontSize = fs
    o.maxFontSize = fs
    o.additionalAtomLabelPadding = 0.08
    o.highlightRadius = 0.24
    o.fillHighlights = True
    o.multipleBondOffset = 0.14
    atoms, bonds, acol, bcol = [], [], {}, {}
    for sm, col in (hl or []):
        c = COLORS.get(col, col)
        for mt in match(m, sm):
            for a in mt:
                atoms.append(a); acol[a] = c
            for b in m.GetBonds():
                if b.GetBeginAtomIdx() in mt and b.GetEndAtomIdx() in mt:
                    bonds.append(b.GetIdx()); bcol[b.GetIdx()] = c
    for a, col in (hl_atoms or {}).items():
        c = COLORS.get(col, col) if isinstance(col, str) else col
        atoms.append(a); acol[a] = c
    for b in m.GetBonds():
        if b.GetBeginAtomIdx() in acol and b.GetEndAtomIdx() in acol and acol[b.GetBeginAtomIdx()] == acol[b.GetEndAtomIdx()]:
            bonds.append(b.GetIdx()); bcol[b.GetIdx()] = acol[b.GetBeginAtomIdx()]
    d.DrawMolecule(m, highlightAtoms=atoms, highlightAtomColors=acol, highlightBonds=bonds, highlightBondColors=bcol)
    extra = ''
    if pins:
        allpts = [d.GetDrawCoords(i) for i in range(m.GetNumAtoms())]
        mx = sum(p.x for p in allpts)/len(allpts); my = sum(p.y for p in allpts)/len(allpts)
        import math as _m
        for n, idxs in pins:
            pts = [d.GetDrawCoords(i) for i in idxs]
            cx = sum(p.x for p in pts)/len(pts); cy = sum(p.y for p in pts)/len(pts)
            vx, vy = cx - mx, cy - my; L = _m.hypot(vx, vy) or 1
            px, py = cx + vx/L*26, cy + vy/L*26
            extra += (f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="#7B3FBF" stroke-width="1.2" stroke-dasharray="2 2"/>'
                      f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="none" stroke="#7B3FBF" stroke-width="1.6" stroke-dasharray="3 2"/>'
                      f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="#fff" stroke="#7B3FBF" stroke-width="1.6"/>'
                      f'<text x="{px:.1f}" y="{py+4:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#5E2A9E" font-family="InterT, Inter">{n}</text>')
    for sm, text, (dx, dy), col in (notes or []):
        idxs = match(m, sm)[0] if isinstance(sm, str) else sm
        pts = [d.GetDrawCoords(i) for i in idxs]
        cx = sum(p.x for p in pts)/len(pts); cy = sum(p.y for p in pts)/len(pts)
        tx, ty = cx+dx, cy+dy
        extra += (f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{col}" stroke-width="1" stroke-dasharray="2 2"/>'
                  f'<text x="{tx:.1f}" y="{ty + (-3 if dy<0 else 10):.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{col}" font-family="InterT, Inter">{text}</text>')
    d.FinishDrawing()
    svg = d.GetDrawingText()
    svg = re.sub(r'<\?xml[^>]*\?>\s*', '', svg)
    svg = re.sub(r"<rect style='opacity:1\.0;fill:#FFFFFF;stroke:none'[^>]*/>", '', svg)
    svg = svg.replace('</svg>', extra + '</svg>')
    return svg, d, m

if __name__ == '__main__':
    tests = [
        ('CCO', [('[CX4][OX2H]', 'purple')]),
        ('CC(=O)Oc1ccccc1C(=O)O', [('[CX3](=O)[OX2][c]', 'purple'), ('[CX3](=O)[OX2H1]', 'orange')]),
        ('CNC[C@H](O)c1ccc(O)c(O)c1', [('[OX2H][c]', 'purple')]),
        ('C/C=C/C', []),
        ('N[C@@H](C)C(=O)O', []),
    ]
    html = '<html><body style="font-family:Inter">'
    for s, hl in tests:
        svg, d, m = mol_svg(s, 240, 160, hl=hl)
        html += f'<div style="display:inline-block;border:1px solid #ccc;margin:4px">{svg}<br>{s} {formula(s)} {mass(s):.2f}</div>'
    html += '</body></html>'
    open('../build/moltest.html', 'w').write(html)
    print('ok')

# ---------- colorização semântica (polar/apolar/éster) ----------
GRAYC = (0.82, 0.84, 0.88)
def semantic_hl(smiles, tail_from=r'[CX3](=O)[OX2]', polar_atoms=('O', 'N', 'P'), ester=True, chain_c=True):
    """Retorna {idx: cor}: heteroátomos polares = azul; carbonos de cadeia apolar = âmbar; éster = roxo."""
    m = Chem.MolFromSmiles(smiles); out = {}
    for a in m.GetAtoms():
        if a.GetSymbol() in polar_atoms: out[a.GetIdx()] = 'blue'
    if chain_c:
        for a in m.GetAtoms():
            if a.GetSymbol() == 'C' and a.GetIdx() not in out: out[a.GetIdx()] = 'amber'
    return out

def phospholipid_hl(smiles):
    m = Chem.MolFromSmiles(smiles); out = {}
    est = m.GetSubstructMatches(Chem.MolFromSmarts('[CX3:1](=[O:2])[OX2:3][CX4:4]'))
    tail = set()
    for c, o, o2, cg in est:
        for a in (c, o, o2): out[a] = 'purple'
        out[cg] = GRAYC
        stack = [n.GetIdx() for n in m.GetAtomWithIdx(c).GetNeighbors() if n.GetSymbol() == 'C' and n.GetIdx() not in (o, o2)]
        while stack:
            i = stack.pop()
            if i in tail: continue
            tail.add(i)
            for n in m.GetAtomWithIdx(i).GetNeighbors():
                if n.GetSymbol() == 'C' and n.GetIdx() not in tail and n.GetIdx() != c: stack.append(n.GetIdx())
    for i in tail: out[i] = 'amber'
    for a in m.GetAtoms():
        if a.GetIdx() not in out: out[a.GetIdx()] = 'blue' if a.GetSymbol() != 'C' or a.GetDegree() >= 1 else 'blue'
    return out, tail
