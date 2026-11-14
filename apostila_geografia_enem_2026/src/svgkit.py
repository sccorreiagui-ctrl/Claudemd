"""svgkit — mini biblioteca para desenhar diagramas SVG editoriais (texto selecionável).

Convenções
- Unidades de usuário do SVG = px CSS a 96 dpi (1 mm = 3,7795 px). Largura típica de página de conteúdo: FULL = 710 px (188 mm).
- Tamanhos de fonte são dados em **pt** (7 pt = 9,33 px) e convertidos automaticamente.
- Largura do texto é medida com a própria fonte Inter (PIL) para quebra de linha e dimensionamento de caixas.
- Setas e pontas são polígonos (sem <marker>), evitando colisão de IDs quando vários SVGs ficam inline no mesmo HTML.
"""
from __future__ import annotations
import html
import math
import re
from functools import lru_cache
from PIL import ImageFont

FONT_DIR = "/usr/share/fonts/opentype/inter/"
_FILES = {400: "Inter-Regular.otf", 500: "Inter-Medium.otf", 600: "Inter-SemiBold.otf",
          700: "Inter-Bold.otf", 800: "Inter-ExtraBold.otf"}
_FILES_IT = {400: "Inter-Italic.otf", 500: "Inter-MediumItalic.otf", 600: "Inter-SemiBoldItalic.otf",
             700: "Inter-BoldItalic.otf", 800: "Inter-ExtraBoldItalic.otf"}

PX_MM = 96 / 25.4
PX_PT = 96 / 72
FULL = round(188 * PX_MM)      # 710
HALF = round(92 * PX_MM)       # 348
THIRD = round(60 * PX_MM)      # 227
TWO_THIRD = round(124 * PX_MM)  # 469

# Paleta semântica: (cor principal, fundo claro, tinta escura)
C = {
    "verde": ("#2E7D32", "#E8F5E9", "#1B5E20"),
    "azul": ("#1565C0", "#E3F2FD", "#0D47A1"),
    "terra": ("#8D5B2E", "#F4EBE0", "#5D3A1A"),
    "laranja": ("#E65100", "#FFF0E0", "#B23C00"),
    "roxo": ("#7B3FA0", "#F3E8F9", "#4A148C"),
    "vermelho": ("#C62828", "#FDECEA", "#8E1B1B"),
    "cinza": ("#546E7A", "#ECEFF1", "#37474F"),
    "navy": ("#1F2A44", "#E8ECF5", "#1F2A44"),
    "ouro": ("#B8860B", "#FFF8DC", "#7A5A00"),
}
INK = "#1D2330"
MUTED = "#5B6475"
LINE = "#C9D0DB"
PAPER = "#FFFFFF"
FONT_STACK = "Inter, 'Helvetica Neue', Arial, sans-serif"


def col(name, i=0):
    """Cor da paleta: i=0 principal, 1 fundo claro, 2 tinta escura. Aceita '#hex' direto."""
    if name is None:
        return "none"
    if name.startswith("#") or name in ("none", "white", "black", "currentColor"):
        return name
    return C[name][i]


@lru_cache(maxsize=None)
def _font(weight: int, italic: bool):
    table = _FILES_IT if italic else _FILES
    w = min(table, key=lambda k: abs(k - weight))
    return ImageFont.truetype(FONT_DIR + table[w], 200)


def strip_md(s: str) -> str:
    return s.replace("**", "").replace("__", "")


def _segments(s: str, base_weight: int):
    """Divide 'a **b** c' em [(texto, peso)]. '**' alterna negrito (700)."""
    parts = s.split("**")
    out = []
    for i, p in enumerate(parts):
        if p == "":
            continue
        out.append((p, 800 if i % 2 == 1 and base_weight >= 700 else (700 if i % 2 == 1 else base_weight)))
    return out


def text_width(s: str, pt: float, weight: int = 400, italic: bool = False) -> float:
    """Largura em px de s (aceita marcação **negrito**)."""
    px = pt * PX_PT
    w = 0.0
    for seg, wt in _segments(s, weight):
        w += _font(wt, italic).getlength(seg) / 200 * px
    return w


def wrap(s: str, max_w: float, pt: float, weight: int = 400, italic: bool = False) -> list[str]:
    """Quebra em linhas que cabem em max_w (px). Preserva '\n' e reabre ** entre linhas."""
    lines: list[str] = []
    bold_open = False
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for wd in words:
            trial = (cur + " " + wd) if cur else wd
            if text_width(trial, pt, weight, italic) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        lines.append(cur)
    # rebalancear negrito entre linhas
    fixed = []
    for ln in lines:
        if bold_open:
            ln = "**" + ln
        n = ln.count("**")
        bold_open = (n % 2 == 1)
        if bold_open:
            ln = ln + "**"
        fixed.append(ln)
    return fixed


def _esc(s: str) -> str:
    return html.escape(s, quote=False)


def _tspans(line: str, weight: int) -> str:
    out = []
    for seg, wt in _segments(line, weight):
        if wt != weight:
            out.append(f'<tspan font-weight="{wt}">{_esc(seg)}</tspan>')
        else:
            out.append(_esc(seg))
    return "".join(out)


class Fig:
    def __init__(self, w=FULL, h=300, name="fig", label="", bg=None):
        self.w, self.h = w, h
        self.name = name
        self.label = label
        self.bg = bg
        self.parts: list[str] = []
        self.defs: list[str] = []
        self._uid = 0

    # ---------- infra ----------
    def uid(self, kind="id") -> str:
        self._uid += 1
        return f"{self.name}-{kind}{self._uid}"

    def add(self, s: str):
        self.parts.append(s)

    def raw(self, s: str):
        self.parts.append(s)

    def g(self, transform: str = "", extra: str = ""):
        self.parts.append(f'<g transform="{transform}" {extra}>' if transform else f"<g {extra}>")

    def gend(self):
        self.parts.append("</g>")

    def clip_rect(self, x, y, w, h) -> str:
        cid = self.uid("clip")
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath>')
        return cid

    def hatch(self, color, angle=45, gap=5, sw=1.2, bg=None) -> str:
        pid = self.uid("hatch")
        c = col(color)
        bgrect = f'<rect width="{gap}" height="{gap}" fill="{col(bg)}"/>' if bg else ""
        self.defs.append(
            f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{gap}" height="{gap}" patternTransform="rotate({angle})">'
            f'{bgrect}<line x1="0" y1="0" x2="0" y2="{gap}" stroke="{c}" stroke-width="{sw}"/></pattern>')
        return f"url(#{pid})"

    def dots(self, color, gap=5, r=1, bg=None) -> str:
        pid = self.uid("dots")
        bgrect = f'<rect width="{gap}" height="{gap}" fill="{col(bg)}"/>' if bg else ""
        self.defs.append(
            f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{gap}" height="{gap}">{bgrect}'
            f'<circle cx="{gap/2}" cy="{gap/2}" r="{r}" fill="{col(color)}"/></pattern>')
        return f"url(#{pid})"

    def lin_grad(self, stops, x1=0, y1=0, x2=0, y2=1) -> str:
        gid = self.uid("grad")
        st = "".join(f'<stop offset="{o}" stop-color="{col(c)}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return f"url(#{gid})"

    # ---------- primitivas ----------
    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, rx=0, opacity=None, dash=None, extra=""):
        a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{col(fill)}"'
        if rx:
            a += f' rx="{rx}"'
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + f" {extra}/>")

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1, dash=None, cap="round", opacity=None):
        a = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col(stroke)}" stroke-width="{sw}" stroke-linecap="{cap}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + "/>")

    def poly(self, pts, fill="none", stroke=None, sw=1, close=True, opacity=None, dash=None, join="round"):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        a = f'<{tag} points="{p}" fill="{col(fill)}"'
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}" stroke-linejoin="{join}" stroke-linecap="round"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + "/>")

    def path(self, d, fill="none", stroke=None, sw=1, dash=None, opacity=None, cap="round", extra=""):
        a = f'<path d="{d}" fill="{col(fill)}"'
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + f" {extra}/>")

    def circle(self, cx, cy, r, fill="none", stroke=None, sw=1, opacity=None, dash=None):
        a = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col(fill)}"'
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + "/>")

    def ellipse(self, cx, cy, rx, ry, fill="none", stroke=None, sw=1, opacity=None, rot=0):
        a = f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col(fill)}"'
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if rot:
            a += f' transform="rotate({rot} {cx:.1f} {cy:.1f})"'
        self.add(a + "/>")

    # ---------- texto ----------
    def text(self, x, y, s, pt=7.5, weight=400, fill=INK, anchor="start", lh=1.22, italic=False,
             rot=None, opacity=None, halo=None, valign="top", spacing=None):
        """Texto multilinha. y = topo da primeira linha (valign=top) ou baseline (valign='base')
        ou centro do bloco (valign='mid'). Aceita **negrito**."""
        px = pt * PX_PT
        lines = s.split("\n")
        n = len(lines)
        step = px * lh
        if valign == "top":
            y0 = y + px * 0.80
        elif valign == "mid":
            y0 = y - (n - 1) * step / 2 + px * 0.36
        else:  # baseline da primeira linha
            y0 = y
        attrs = f'font-size="{px:.2f}" fill="{col(fill)}" font-weight="{weight}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        if italic:
            attrs += ' font-style="italic"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        if spacing:
            attrs += f' letter-spacing="{spacing}"'
        if halo:
            attrs += f' stroke="{col(halo)}" stroke-width="{max(2.2, px*0.28):.1f}" stroke-linejoin="round" paint-order="stroke"'
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
        tsp = []
        for i, ln in enumerate(lines):
            dy = 0 if i == 0 else step
            tsp.append(f'<tspan x="{x:.1f}" dy="{dy:.2f}">{_tspans(ln, weight)}</tspan>' if i else
                       f'<tspan x="{x:.1f}" dy="0">{_tspans(ln, weight)}</tspan>')
        self.add(f'<text x="{x:.1f}" y="{y0:.2f}" {attrs}{tr}>{"".join(tsp)}</text>')
        return n * step  # altura ocupada

    def text_h(self, s, pt=7.5, lh=1.22) -> float:
        return len(s.split("\n")) * pt * PX_PT * lh

    def para(self, x, y, w, s, pt=7.5, weight=400, fill=INK, anchor="start", lh=1.25, italic=False, halo=None):
        """Texto com quebra automática em largura w. Retorna a altura usada."""
        lines = wrap(s, w, pt, weight, italic)
        tx = x if anchor == "start" else (x + w / 2 if anchor == "middle" else x + w)
        return self.text(tx, y, "\n".join(lines), pt, weight, fill, anchor, lh, italic, halo=halo)

    # ---------- composições ----------
    def box(self, x, y, w, h, s="", fill="cinza", stroke=None, tcolor=None, pt=7.5, weight=500, rx=5,
            align="middle", pad=6, sw=1.2, dash=None, lh=1.2, valign="mid", light=True):
        """Caixa com texto quebrado automaticamente. fill/stroke: nome da paleta ou #hex.
        light=True usa fundo claro e contorno na cor principal."""
        if fill in C and light:
            bgc, strokec, ink = C[fill][1], C[fill][0], C[fill][2]
        elif fill in C:
            bgc, strokec, ink = C[fill][0], C[fill][0], "#FFFFFF"
        else:
            bgc, strokec, ink = col(fill), col(stroke or "#999"), INK
        if stroke:
            strokec = col(stroke)
        tc = tcolor or ink
        self.rect(x, y, w, h, fill=bgc, stroke=strokec, sw=sw, rx=rx, dash=dash)
        if s:
            lines = wrap(s, w - 2 * pad, pt, weight)
            blk = "\n".join(lines)
            hh = len(lines) * pt * PX_PT * lh
            ty = y + (h - hh) / 2 if valign == "mid" else y + pad
            tx = x + w / 2 if align == "middle" else x + pad
            self.text(tx, ty, blk, pt, weight, tc, align, lh)
        return (x, y, w, h)

    def pill(self, x, y, s, fill="navy", pt=6.8, weight=700, padx=7, h=None, tcolor=None, anchor="start", light=False):
        w = text_width(s, pt, weight) + 2 * padx
        h = h or pt * PX_PT * 1.25 + 6
        if anchor == "middle":
            x = x - w / 2
        elif anchor == "end":
            x = x - w
        if light:
            bg, tc = C[fill][1], C[fill][2]
            self.rect(x, y, w, h, fill=bg, stroke=C[fill][0], sw=0.8, rx=h / 2)
        else:
            bg, tc = col(fill), "#FFFFFF"
            self.rect(x, y, w, h, fill=bg, rx=h / 2)
        self.text(x + w / 2, y + h / 2, s, pt, weight, tcolor or tc, "middle", valign="mid")
        return w, h

    def badge(self, cx, cy, n, fill="navy", r=8, pt=7):
        self.circle(cx, cy, r, fill=col(fill))
        self.text(cx, cy, str(n), pt, 800, "#FFFFFF", "middle", valign="mid")

    def arrow(self, x1, y1, x2, y2, color=INK, sw=1.6, head=7, dash=None, opacity=None):
        """Seta reta com ponta triangular (polígono)."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        bx, by = x2 - ux * head * 0.9, y2 - uy * head * 0.9
        self.line(x1, y1, bx, by, color, sw, dash, "butt", opacity)
        px, py = -uy, ux
        hw = head * 0.55
        self.poly([(x2, y2), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw)], fill=color, opacity=opacity)

    def curve_arrow(self, x1, y1, cx, cy, x2, y2, color=INK, sw=1.6, head=7, dash=None, opacity=None, c2=None):
        """Seta curva (quadrática, ou cúbica se c2=(cx2,cy2))."""
        if c2:
            tx, ty = x2 - c2[0], y2 - c2[1]
        else:
            tx, ty = x2 - cx, y2 - cy
        L = math.hypot(tx, ty) or 1
        ux, uy = tx / L, ty / L
        bx, by = x2 - ux * head * 0.9, y2 - uy * head * 0.9
        if c2:
            d = f"M{x1:.1f},{y1:.1f} C{cx:.1f},{cy:.1f} {c2[0]:.1f},{c2[1]:.1f} {bx:.1f},{by:.1f}"
        else:
            d = f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {bx:.1f},{by:.1f}"
        self.path(d, stroke=color, sw=sw, dash=dash, opacity=opacity, cap="butt")
        px, py = -uy, ux
        hw = head * 0.55
        self.poly([(x2, y2), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw)], fill=color, opacity=opacity)

    def flow(self, items, x, y, w_total, h=34, gap=14, pt=7.2, colors=None, weight=600, arrow_color=MUTED, rx=6):
        """Fluxo horizontal: items = [str | (str, cor)]; caixas de largura igual. Retorna (y_base, centros_x)."""
        n = len(items)
        bw = (w_total - gap * (n - 1)) / n
        centers = []
        for i, it in enumerate(items):
            s, c = (it if isinstance(it, tuple) else (it, (colors[i] if colors else "cinza")))
            bx = x + i * (bw + gap)
            self.box(bx, y, bw, h, s, fill=c, pt=pt, weight=weight, rx=rx, pad=4)
            centers.append(bx + bw / 2)
            if i < n - 1:
                self.arrow(bx + bw + 1.5, y + h / 2, bx + bw + gap - 1.5, y + h / 2, arrow_color, 1.5, 5.5)
        return y + h, centers

    def flow_v(self, items, x, y, w, h=26, gap=12, pt=7.2, weight=600, arrow_color=MUTED, rx=6):
        yy = y
        for i, it in enumerate(items):
            s, c = it
            self.box(x, yy, w, h, s, fill=c, pt=pt, weight=weight, rx=rx, pad=4)
            if i < len(items) - 1:
                self.arrow(x + w / 2, yy + h + 1, x + w / 2, yy + h + gap - 1, arrow_color, 1.5, 5.5)
            yy += h + gap
        return yy - gap

    # ---------- pictogramas simples ----------
    def tree(self, x, y, s=1.0, color="verde", trunk="#8D5B2E", round_crown=True):
        self.rect(x - 1.6 * s, y - 9 * s, 3.2 * s, 9 * s, fill=trunk)
        if round_crown:
            self.circle(x, y - 14 * s, 8 * s, fill=col(color, 0))
        else:
            self.poly([(x, y - 30 * s), (x - 8 * s, y - 8 * s), (x + 8 * s, y - 8 * s)], fill=col(color, 0))

    def cloud(self, x, y, s=1.0, fill="#FFFFFF", stroke=LINE):
        d = (f"M{x-18*s:.1f},{y:.1f} a8,8 0 0 1 4,-14 a11,11 0 0 1 21,-3 a9,9 0 0 1 12,9 a7,7 0 0 1 -2,8 z")
        self.path(d, fill=fill, stroke=stroke, sw=1)

    def sun(self, x, y, r=8, color="#F9A825"):
        for k in range(8):
            a = k * math.pi / 4
            self.line(x + math.cos(a) * (r + 3), y + math.sin(a) * (r + 3), x + math.cos(a) * (r + 7), y + math.sin(a) * (r + 7), color, 1.6)
        self.circle(x, y, r, fill=color)

    def raindrops(self, x, y, n=3, color="#1565C0", dx=7, dy=9):
        for i in range(n):
            self.line(x + i * dx, y + (i % 2) * 3, x + i * dx - 2.5, y + (i % 2) * 3 + dy, color, 1.4)

    # ---------- saída ----------
    def render(self) -> str:
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        bg = f'<rect width="{self.w}" height="{self.h}" fill="{col(self.bg)}"/>' if self.bg else ""
        label = _esc(self.label or self.name)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w:.1f} {self.h:.1f}" role="img" '
                f'aria-label="{label}" style="width:100%;height:auto;display:block" font-family="{FONT_STACK}">'
                f'<title>{label}</title>{defs}{bg}{"".join(self.parts)}</svg>')
