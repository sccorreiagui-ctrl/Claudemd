"""Estruturas moleculares verificáveis (SMILES -> SVG vetorial) com RDKit.

Cada molécula é definida por um SMILES; a fórmula molecular é calculada pelo RDKit e pode ser
conferida com `formula=` (gera erro se a legenda divergir da estrutura). Grupos funcionais são
destacados por padrões SMARTS: se o padrão não existir na molécula, o build falha (auditoria).
"""
import math
import re

from rdkit import Chem
from rdkit.Chem import Descriptors, rdDepictor, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D

from svglib import C, FONT_STACK, n, tw, esc

rdDepictor.SetPreferCoordGen(True)

INK = C["ink"]
_PAIR = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")


class MolImg:
    def __init__(self, inner, x0, y0, w, h, formula, mass, coords, smiles):
        self.inner = inner
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.formula = formula
        self.mass = mass
        self.coords = coords
        self.smiles = smiles

    def svg(self, scale=1.0, cls=""):
        w, h = self.w * scale, self.h * scale
        c = f' class="{cls}"' if cls else ""
        return (f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="{n(self.x0)} {n(self.y0)} {n(self.w)} {n(self.h)}" '
                f'width="{n(w)}" height="{n(h)}" font-family="{FONT_STACK}" style="display:block;max-width:100%;height:auto">'
                f'{self.inner}</svg>')

    def at(self, x, y, scale=1.0, anchor="center"):
        """Aninha a molécula dentro de outro SVG; (x,y)=centro (anchor center) ou canto superior esquerdo."""
        w, h = self.w * scale, self.h * scale
        if anchor == "center":
            x, y = x - w / 2, y - h / 2
        return (f'<svg x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" '
                f'viewBox="{n(self.x0)} {n(self.y0)} {n(self.w)} {n(self.h)}" overflow="visible">{self.inner}</svg>')


def formula_of(smiles):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise ValueError("SMILES inválido: " + smiles)
    return rdMolDescriptors.CalcMolFormula(m)


def mol(smiles, bond=30, hl=None, hl_color=None, labels=None, formula=None, margin=9, font=0.62, lw=1.8,
        mark=None, rotate=0, hl_alpha=0.26, hl_w=None, seed_coords=None, add_h=None, flip_x=False):
    """Desenha a molécula.

    hl     : lista de SMARTS (ou (SMARTS, cor)) a destacar (cor padrão = roxo semântico)
    labels : {índice_do_átomo_fictício: 'R'}; átomos '*' recebem 'R' por padrão
    mark   : lista de (SMARTS, 'rótulo') para marcadores numerados fora da molécula
    add_h  : lista de índices de átomos que devem mostrar H explícito
    """
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise ValueError("SMILES inválido: " + smiles)
    fml = rdMolDescriptors.CalcMolFormula(m)
    if formula is not None and Chem.MolToSmiles(m) and fml != formula:
        raise ValueError(f"Fórmula divergente para {smiles}: esperado {formula}, RDKit calculou {fml}")
    for a in m.GetAtoms():
        if a.GetAtomicNum() == 0:
            a.SetProp("atomLabel", (labels or {}).get(a.GetIdx(), "R"))
    rdDepictor.Compute2DCoords(m)
    if rotate:
        # gira coordenadas manualmente (graus)
        conf = m.GetConformer()
        th = math.radians(rotate)
        for i in range(m.GetNumAtoms()):
            p = conf.GetAtomPosition(i)
            x, y = p.x, p.y
            conf.SetAtomPosition(i, (x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th), 0))
    if flip_x:
        conf = m.GetConformer()
        for i in range(m.GetNumAtoms()):
            p = conf.GetAtomPosition(i)
            conf.SetAtomPosition(i, (-p.x, p.y, 0))
    d = rdMolDraw2D.MolDraw2DSVG(900, 700)
    o = d.drawOptions()
    o.clearBackground = False
    o.fixedBondLength = bond
    o.bondLineWidth = lw
    o.baseFontSize = font
    o.useBWAtomPalette()
    o.additionalAtomLabelPadding = 0.05
    o.padding = 0.08
    o.multipleBondOffset = 0.14
    o.minFontSize = 8
    d.DrawMolecule(m)
    d.FinishDrawing()
    svg = d.GetDrawingText()
    inner = svg.split("<!-- END OF HEADER -->", 1)[1].rsplit("</svg>", 1)[0]
    inner = inner.replace("#000000", INK)
    coords = [(d.GetDrawCoords(i).x, d.GetDrawCoords(i).y) for i in range(m.GetNumAtoms())]

    # bounding box a partir dos elementos reais desenhados
    xs, ys = [], []
    for dm in re.finditer(r"d='([^']*)'", inner):
        nums = re.findall(r"-?\d+(?:\.\d+)?", dm.group(1))
        for i in range(0, len(nums) - 1, 2):
            xs.append(float(nums[i]))
            ys.append(float(nums[i + 1]))
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)

    shapes = []

    def _atoms_of(smarts_list, first_only=False):
        res = []
        for item in smarts_list:
            smarts, color = (item if isinstance(item, tuple) else (item, hl_color or C["purple"]))
            patt = Chem.MolFromSmarts(smarts)
            if patt is None:
                raise ValueError("SMARTS inválido: " + smarts)
            matches = m.GetSubstructMatches(patt)
            if not matches:
                raise ValueError(f"Grupo '{smarts}' não encontrado em {smiles}")
            for mt in (matches[:1] if first_only else matches):
                res.append((mt, color, smarts))
        return res

    hl_sets = _atoms_of(hl) if hl else []
    wline = hl_w or bond * 0.78
    for mt, color, _s in hl_sets:
        s = set(mt)
        g = [f'<g opacity="{n(hl_alpha)}">']
        for b in m.GetBonds():
            a1, a2 = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
            if a1 in s and a2 in s:
                (xa, ya), (xb, yb) = coords[a1], coords[a2]
                g.append(f'<line x1="{n(xa)}" y1="{n(ya)}" x2="{n(xb)}" y2="{n(yb)}" stroke="{color}" '
                         f'stroke-width="{n(wline)}" stroke-linecap="round"/>')
        for i in mt:
            xa, ya = coords[i]
            g.append(f'<circle cx="{n(xa)}" cy="{n(ya)}" r="{n(wline / 2)}" fill="{color}"/>')
        g.append("</g>")
        shapes.append("".join(g))
        for i in mt:
            x0 = min(x0, coords[i][0] - wline / 2)
            x1 = max(x1, coords[i][0] + wline / 2)
            y0 = min(y0, coords[i][1] - wline / 2)
            y1 = max(y1, coords[i][1] + wline / 2)

    # marcadores numerados
    if mark:
        cx_m = sum(c[0] for c in coords) / len(coords)
        cy_m = sum(c[1] for c in coords) / len(coords)
        for smarts, lab in mark:
            patt = Chem.MolFromSmarts(smarts)
            mt = m.GetSubstructMatches(patt)
            if not mt:
                raise ValueError(f"Marcador '{smarts}' não encontrado em {smiles}")
            mt = mt[0]
            gx = sum(coords[i][0] for i in mt) / len(mt)
            gy = sum(coords[i][1] for i in mt) / len(mt)
            dx, dy = gx - cx_m, gy - cy_m
            L = math.hypot(dx, dy) or 1.0
            dx, dy = (dx / L, dy / L) if L > 1e-6 else (0.0, -1.0)
            px, py = gx + dx * (bond * 1.05), gy + dy * (bond * 1.05)
            shapes.append(f'<circle cx="{n(px)}" cy="{n(py)}" r="8.2" fill="{C["purple_d"]}"/>'
                          f'<text x="{n(px)}" y="{n(py + 3.6)}" font-size="10.5" font-weight="700" fill="#fff" '
                          f'text-anchor="middle" font-family="{FONT_STACK}">{esc(lab)}</text>')
            x0, x1 = min(x0, px - 9), max(x1, px + 9)
            y0, y1 = min(y0, py - 9), max(y1, py + 9)

    inner = "".join(shapes) + inner
    x0 -= margin
    y0 -= margin
    x1 += margin
    y1 += margin
    return MolImg(inner, x0, y0, x1 - x0, y1 - y0, fml, Descriptors.MolWt(m), coords, smiles)


# --------------------------------------------------------------------------- esquemas de reação
def scheme(items, gap=14, height=None, pad=4, arrow_len=64, color=None):
    """Compõe moléculas, textos e setas numa única linha (SVG).

    items: lista de
       ('mol', MolImg [, escala])
       ('op', '+')
       ('arrow', 'rótulo acima', 'rótulo abaixo', kind)   kind: 'r' (→), 'eq' (⇌), 'ox' etc.
       ('text', 'texto', tamanho)
    Retorna (svg_string, largura, altura).
    """
    color = color or C["ink"]
    measured = []
    maxh = 0
    for it in items:
        k = it[0]
        if k == "mol":
            sc = it[2] if len(it) > 2 else 1.0
            mi = it[1]
            measured.append((it, mi.w * sc, mi.h * sc))
            maxh = max(maxh, mi.h * sc)
        elif k == "op":
            measured.append((it, tw(it[1], 17, 600), 20))
        elif k == "arrow":
            top = it[1] or ""
            bot = it[2] if len(it) > 2 else ""
            w = max(arrow_len, tw(top, 9.6, 600) + 8, tw(bot, 9.6, 600) + 8)
            measured.append((it, w, 30))
        elif k == "text":
            sz = it[2] if len(it) > 2 else 12
            measured.append((it, tw(it[1], sz, 600), sz + 2))
        elif k == "space":
            measured.append((it, it[1], 1))
    H = height or maxh + 2 * pad
    W = sum(w for _, w, _ in measured) + gap * (len(measured) - 1) + 2 * pad
    cy = H / 2
    out = []
    x = pad
    for it, w, h in measured:
        k = it[0]
        if k == "mol":
            sc = it[2] if len(it) > 2 else 1.0
            out.append(it[1].at(x + w / 2, cy, sc))
        elif k == "op":
            out.append(f'<text x="{n(x + w / 2)}" y="{n(cy + 6)}" font-size="17" font-weight="600" fill="{C["muted"]}" '
                       f'text-anchor="middle">{esc(it[1])}</text>')
        elif k == "arrow":
            top = it[1] or ""
            bot = it[2] if len(it) > 2 else ""
            kind = it[3] if len(it) > 3 else "r"
            x1, x2 = x + 3, x + w - 3
            col = C["orange"] if kind in ("r", "eq", "both") else color
            if kind == "eq":
                out.append(f'<line x1="{n(x1)}" y1="{n(cy - 3.2)}" x2="{n(x2)}" y2="{n(cy - 3.2)}" stroke="{col}" stroke-width="1.8" stroke-linecap="round"/>'
                           f'<path d="M{n(x2 - 6)} {n(cy - 7.4)} L{n(x2)} {n(cy - 3.2)}" stroke="{col}" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
                           f'<line x1="{n(x1)}" y1="{n(cy + 3.2)}" x2="{n(x2)}" y2="{n(cy + 3.2)}" stroke="{col}" stroke-width="1.8" stroke-linecap="round"/>'
                           f'<path d="M{n(x1 + 6)} {n(cy + 7.4)} L{n(x1)} {n(cy + 3.2)}" stroke="{col}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
            else:
                out.append(f'<line x1="{n(x1)}" y1="{n(cy)}" x2="{n(x2 - 5)}" y2="{n(cy)}" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'
                           f'<polygon points="{n(x2)},{n(cy)} {n(x2 - 8)},{n(cy - 4.2)} {n(x2 - 8)},{n(cy + 4.2)}" fill="{col}"/>')
            from svglib import tspans
            if top:
                out.append(f'<text x="{n(x + w / 2)}" y="{n(cy - 11)}" font-size="9.6" font-weight="600" fill="{C["orange_d"]}" '
                           f'text-anchor="middle">{tspans(top, 9.6)}</text>')
            if bot:
                out.append(f'<text x="{n(x + w / 2)}" y="{n(cy + 19)}" font-size="9.6" font-weight="600" fill="{C["orange_d"]}" '
                           f'text-anchor="middle">{tspans(bot, 9.6)}</text>')
        elif k == "text":
            sz = it[2] if len(it) > 2 else 12
            from svglib import tspans
            out.append(f'<text x="{n(x + w / 2)}" y="{n(cy + sz * 0.35)}" font-size="{sz}" font-weight="600" fill="{C["ink"]}" '
                       f'text-anchor="middle">{tspans(it[1], sz)}</text>')
        x += w + gap
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(W)} {n(H)}" width="{n(W)}" height="{n(H)}" '
           f'font-family="{FONT_STACK}" style="display:block;max-width:100%;height:auto">{"".join(out)}</svg>')
    return svg, W, H


def scheme_inner(items, **kw):
    """Como scheme(), mas devolve só o conteúdo aninhável (svg aninhado) e o tamanho."""
    s, W, H = scheme(items, **kw)
    return s, W, H
