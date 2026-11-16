"""svgkit — mini-biblioteca para figuras SVG de Física (vetores, campos, circuitos, gráficos).

Princípios
----------
* Cada figura é um objeto ``Fig(w, h)`` em coordenadas de "pixel CSS" (1 unidade ≈ 0,2646 mm
  quando a figura é exibida na largura para a qual foi projetada).
* Rótulos usam as métricas reais dos fontes (``metrics.json``, medidas no Chromium), o que permite
  posicionamento exato e um *lint* automático: sobreposição rótulo×rótulo, rótulo×traço e rótulo
  fora do quadro são detectados no momento da geração.
* Mini‑marcação de texto:  ``$I_{eq}$`` = variável em itálico matemático com índice;
  fora de ``$…$`` o texto é sans‑serif comum (unidades, palavras).  ``\\vec F`` desenha seta sobre a letra.
"""
from __future__ import annotations
import json, math, pathlib, re
from dataclasses import dataclass, field

_HERE = pathlib.Path(__file__).parent
_M = json.loads((_HERE / "metrics.json").read_text(encoding="utf-8"))

# ───────────────────────── paleta semântica (cores mantêm o mesmo significado na apostila) ──────────
INK, MUTED, RULE, SOFT, WHITE = "#1B2438", "#5B6578", "#C9D0DC", "#EEF1F6", "#FFFFFF"
POS, POS_D, POS_L = "#E5484D", "#BF2B31", "#FDE6E7"      # cargas/polos positivos
NEG, NEG_D, NEG_L = "#2563EB", "#1D4ED8", "#E3EBFD"      # cargas negativas, elétrons
CUR, CUR_D, CUR_L = "#F08C00", "#B25B00", "#FFF0D6"      # corrente convencional / trajetos
MAG, MAG_D, MAG_L = "#7C3AED", "#6D28D9", "#EEE6FD"      # campo magnético, indução
ENE, ENE_D, ENE_L = "#16A34A", "#15803D", "#E1F4E8"      # energia, potência
EFD, EFD_D, EFD_L = "#0891B2", "#0E7490", "#DBF2F7"      # campo elétrico, equipotenciais
GRY, GRY_M, GRY_L, GRY_XL = "#6B7280", "#9AA3B2", "#C5CBD6", "#E8EBF1"   # neutros, condutores, estruturas

# escala cromática de potencial elétrico (frio → quente): menor V … maior V
POT_SCALE = ["#2563EB", "#0891B2", "#16A34A", "#F08C00", "#E5484D"]


def lerp_color(a: str, b: str, t: float) -> str:
    ra, ga, ba = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
    rb, gb, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
    return "#%02X%02X%02X" % (round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t))


def pot_color(v: float, vmin: float, vmax: float) -> str:
    """Cor de um potencial v na escala frio→quente."""
    t = 0.0 if vmax == vmin else min(1.0, max(0.0, (v - vmin) / (vmax - vmin)))
    n = len(POT_SCALE) - 1
    i = min(n - 1, int(t * n))
    return lerp_color(POT_SCALE[i], POT_SCALE[i + 1], t * n - i)


def f2(x: float) -> str:
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ───────────────────────── texto: mini‑marcação → runs ─────────────────────────────
GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "varepsilon": "ε", "epsilon": "ε", "theta": "θ",
         "lambda": "λ", "mu": "μ", "nu": "ν", "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "φ",
         "varphi": "φ", "omega": "ω", "psi": "ψ", "chi": "χ", "eta": "η", "xi": "ξ", "zeta": "ζ", "kappa": "κ"}
GREEK_UP = {"Delta": "Δ", "Omega": "Ω", "Phi": "Φ", "Sigma": "Σ", "Pi": "Π", "Theta": "Θ", "Lambda": "Λ"}
SYMS = {"cdot": "·", "times": "×", "pm": "±", "approx": "≈", "to": "→", "infty": "∞", "circ": "°", "deg": "°",
        "neq": "≠", "le": "≤", "ge": "≥", "propto": "∝", "parallel": "∥", "perp": "⊥", "leftrightarrow": "↔",
        "rightarrow": "→", "leftarrow": "←", "uparrow": "↑", "downarrow": "↓", "ell": "ℓ", "sum": "Σ", "parallel_": "∥"}


@dataclass
class Run:
    text: str
    font: str = "sans"      # sans | math | main
    scale: float = 1.0
    dy: float = 0.0         # em (positivo = para baixo)
    vec: bool = False
    bold: bool = False
    pad: float = 0.0        # espaço antes do run (em)
    over: bool = False      # dentro de \sqrt{…}: recebe traço superior
    rad: bool = False       # marca o início do radical


_SPECIAL_ADV = {"\u2009": 0.2, "\u2002": 0.5, "\u2005": 0.25, "\u00a0": 0.2}
REL_SYMS = {"approx", "neq", "le", "ge", "propto", "to", "rightarrow", "leftarrow", "leftrightarrow"}
BIN_SYMS = {"cdot", "times", "pm"}


def _adv(font: str, bold: bool, ch: str) -> float:
    if ch in _SPECIAL_ADV:
        return _SPECIAL_ADV[ch]
    key = {"sans": "sans600" if bold else "sans400", "math": "math", "main": "mainb" if bold else "main"}[font]
    t = _M[key]
    if ch in t:
        return t[ch]
    alt = _M["main"].get(ch) or _M["sans400"].get(ch)
    return alt if alt is not None else 0.55


def _group(s: str, i: int):
    if i >= len(s):
        return "", i
    if s[i] == "{":
        depth, j = 1, i + 1
        while j < len(s) and depth > 0:
            depth += (s[j] == "{") - (s[j] == "}")
            j += 1
        return s[i + 1:j - 1], j
    if s[i] == "\\":
        m = re.match(r"\\([A-Za-z]+|.)", s[i:])
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def parse_math(s: str, upright: bool = False) -> list[Run]:
    runs: list[Run] = []
    pend = [0.0]          # espaço a aplicar antes do próximo run

    def add(r: Run):
        r.pad += pend[0]
        pend[0] = 0.0
        runs.append(r)

    def binary_ok() -> bool:
        return bool(runs) and runs[-1].text not in ("(", "[", "=", "+", "−", "×", "·", "/", "±", "<", ">", "≈", "≤", "≥")

    i = 0
    while i < len(s):
        ch = s[i]
        if ch in "_^":
            content, i = _group(s, i + 1)
            force = None
            if content[:1] == "!":
                force, content = "up", content[1:]
            elif content[:1] == "~":
                force, content = "it", content[1:]
            plain = re.sub(r"\\[A-Za-z]+", "X", content)
            if force is None:
                is_var = bool(re.fullmatch(r"[A-Za-zα-ωΑ-Ω]", plain)) or bool(re.fullmatch(r"[A-Z]{2}", plain))
                up = not is_var
            else:
                up = force == "up"
            sub = parse_math(content, upright=up)
            for r in sub:
                r.scale *= 0.72
                r.dy += 0.27 if ch == "_" else -0.40
            if sub:
                sub[0].pad += pend[0]
                pend[0] = 0.0
            runs += sub
        elif ch == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            name = m.group(1)
            i += len(m.group(0))
            if name.isalpha():
                while i < len(s) and s[i] == " ":
                    i += 1
            if name == "vec":
                content, i = _group(s, i)
                sub = parse_math(content, upright)
                if sub:
                    sub[0].vec = True
                    sub[0].pad += pend[0]
                    pend[0] = 0.0
                runs += sub
            elif name in ("mathrm", "text"):
                content, i = _group(s, i)
                sub = parse_math(content, True)
                if sub:
                    sub[0].pad += pend[0]
                    pend[0] = 0.0
                runs += sub
            elif name in ("cos", "sin", "tan", "log", "ln", "sen", "tg", "cot"):
                add(Run(name, "main", pad=0.17))
                pend[0] = 0.17
            elif name == "sqrt":
                content, i = _group(s, i)
                sub = parse_math(content, upright)
                add(Run("", "main", pad=0.0, rad=True, over=True))
                runs[-1].pad += 0.0
                for r in sub:
                    r.over = True
                if sub:
                    sub[0].pad += 0.62
                runs += sub
            elif name in GREEK:
                add(Run(GREEK[name], "main" if upright else "math"))
            elif name in GREEK_UP:
                add(Run(GREEK_UP[name], "main"))
            elif name in SYMS:
                if name in REL_SYMS:
                    r = Run(SYMS[name], "main", pad=0.28)
                    add(r)
                    pend[0] = 0.28
                elif name in BIN_SYMS and binary_ok():
                    r = Run(SYMS[name], "main", pad=0.22)
                    add(r)
                    pend[0] = 0.22
                else:
                    add(Run(SYMS[name], "main"))
            elif name == ",":
                pend[0] += 0.17
            elif name in (";", ":"):
                pend[0] += 0.25
            elif name == " ":
                pend[0] += 0.3
            else:
                add(Run(name, "main"))
        elif ch == "{":
            content, i = _group(s, i)
            sub = parse_math(content, upright)
            if sub:
                sub[0].pad += pend[0]
                pend[0] = 0.0
            runs += sub
        elif ch.isalpha() and not upright:
            add(Run(ch, "math"))
            i += 1
        elif ch in "=<>":
            add(Run(ch, "main", pad=0.28))
            pend[0] = 0.28
            i += 1
        elif ch == "-":
            if binary_ok():
                add(Run("−", "main", pad=0.22))
                pend[0] = 0.22
            else:
                add(Run("−", "main"))
            i += 1
        elif ch == "+":
            if binary_ok():
                add(Run("+", "main", pad=0.22))
                pend[0] = 0.22
            else:
                add(Run("+", "main"))
            i += 1
        elif ch == " ":
            i += 1                      # espaços em modo matemático são ignorados (como no TeX)
        else:
            add(Run(ch, "main"))
            i += 1
    return runs


def parse(s: str, bold: bool = False) -> list[Run]:
    runs: list[Run] = []
    for k, seg in enumerate(s.split("$")):
        if k % 2 == 0:
            if seg:
                runs.append(Run(seg, "sans", bold=bold))
        else:
            runs += parse_math(seg)
    # fundir runs adjacentes idênticos
    out: list[Run] = []
    for r in runs:
        if out and (out[-1].font, out[-1].scale, out[-1].dy, out[-1].bold) == (r.font, r.scale, r.dy, r.bold) \
                and not r.vec and not out[-1].vec and r.pad == 0:
            out[-1].text += r.text
        else:
            out.append(r)
    return out


def text_width(s: str, size: float = 12, bold: bool = False) -> float:
    return sum((_adv(r.font, r.bold or bold, c) * r.scale + (r.pad if k == 0 else 0)) * size
               for r in parse(s, bold) for k, c in enumerate(r.text))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ───────────────────────── geometria auxiliar ─────────────────────────────────────
def _seg_hits_box(x1, y1, x2, y2, box) -> bool:
    bx0, by0, bx1, by1 = box
    # Liang–Barsky
    dx, dy = x2 - x1, y2 - y1
    p = (-dx, dx, -dy, dy)
    q = (x1 - bx0, bx1 - x1, y1 - by0, by1 - y1)
    u0, u1 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) < 1e-12:
            if qi < 0:
                return False
        else:
            t = qi / pi
            if pi < 0:
                u0 = max(u0, t)
            else:
                u1 = min(u1, t)
            if u0 > u1:
                return False
    return True


IGNORE_TAGS = {"grid", "bg", "halo"}


class Fig:
    def __init__(self, w: float, h: float, name: str = "", title: str = ""):
        self.w, self.h, self.name, self.title = w, h, name, title
        self.parts: list[str] = []
        self.labels: list[dict] = []
        self.strokes: list[tuple] = []
        self.defs: list[str] = []

    # ── registro ────────────────────────────────────────────────────────────────
    def raw(self, s: str):
        self.parts.append(s)

    def _seg(self, x1, y1, x2, y2, tag=""):
        self.strokes.append((x1, y1, x2, y2, tag))

    def _polyseg(self, pts, tag="", close=False):
        for a, b in zip(pts, pts[1:]):
            self._seg(a[0], a[1], b[0], b[1], tag)
        if close and len(pts) > 2:
            self._seg(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], tag)

    # ── primitivas ──────────────────────────────────────────────────────────────
    def line(self, x1, y1, x2, y2, c=INK, w=1.6, dash=None, cap="round", op=None, tag=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        self.raw(f'<line x1="{f2(x1)}" y1="{f2(y1)}" x2="{f2(x2)}" y2="{f2(y2)}" stroke="{c}" stroke-width="{w}" '
                 f'stroke-linecap="{cap}"{d}{o}/>')
        self._seg(x1, y1, x2, y2, tag)

    def pl(self, pts, c=INK, w=1.6, fill="none", close=False, dash=None, op=None, fop=None, tag="", join="round"):
        if len(pts) < 2:
            return
        tagname = "polygon" if close else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        fo = f' fill-opacity="{fop}"' if fop is not None else ""
        pstr = " ".join(f"{f2(x)},{f2(y)}" for x, y in pts)
        stroke = f'stroke="{c}" stroke-width="{w}"' if c else 'stroke="none"'
        self.raw(f'<{tagname} points="{pstr}" fill="{fill}" {stroke} stroke-linejoin="{join}" '
                 f'stroke-linecap="round"{d}{o}{fo}/>')
        if c:
            self._polyseg(pts, tag, close)

    def path(self, d, c=INK, w=1.6, fill="none", dash=None, op=None, fop=None, tag="", samples=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        fo = f' fill-opacity="{fop}"' if fop is not None else ""
        stroke = f'stroke="{c}" stroke-width="{w}"' if c else 'stroke="none"'
        self.raw(f'<path d="{d}" fill="{fill}" {stroke} stroke-linejoin="round" stroke-linecap="round"{ds}{o}{fo}/>')
        if samples and c:
            self._polyseg(samples, tag)

    def rect(self, x, y, w, h, fill="none", c=None, sw=1.2, rx=0, dash=None, op=None, fop=None, tag=""):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        fo = f' fill-opacity="{fop}"' if fop is not None else ""
        stroke = f'stroke="{c}" stroke-width="{sw}"' if c else 'stroke="none"'
        self.raw(f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" rx="{rx}" fill="{fill}" '
                 f'{stroke}{ds}{o}{fo}/>')
        if c:
            self._polyseg([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], tag, True)

    def circ(self, x, y, r, fill="none", c=INK, w=1.5, dash=None, op=None, fop=None, tag=""):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        fo = f' fill-opacity="{fop}"' if fop is not None else ""
        stroke = f'stroke="{c}" stroke-width="{w}"' if c else 'stroke="none"'
        self.raw(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(r)}" fill="{fill}" {stroke}{ds}{o}{fo}/>')
        if c and r > 1.2:
            n = 20
            self._polyseg([(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n))
                           for k in range(n)], tag, True)

    def ell(self, x, y, rx, ry, fill="none", c=INK, w=1.5, dash=None, op=None, tag="", rot=0):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        tr = f' transform="rotate({f2(rot)} {f2(x)} {f2(y)})"' if rot else ""
        stroke = f'stroke="{c}" stroke-width="{w}"' if c else 'stroke="none"'
        self.raw(f'<ellipse cx="{f2(x)}" cy="{f2(y)}" rx="{f2(rx)}" ry="{f2(ry)}" fill="{fill}" {stroke}{ds}{o}{tr}/>')
        if c:
            n = 24
            ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            pts = []
            for k in range(n):
                t = 2 * math.pi * k / n
                px, py = rx * math.cos(t), ry * math.sin(t)
                pts.append((x + px * ca - py * sa, y + px * sa + py * ca))
            self._polyseg(pts, tag, True)

    def dot(self, x, y, r=3.4, c=INK):
        self.raw(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(r)}" fill="{c}"/>')

    def head(self, x, y, ang, c=INK, size=9, hw=0.36, tag=""):
        """Ponta de seta (triângulo cheio) com vértice em (x,y), direção ``ang`` (rad, tela)."""
        ca, sa = math.cos(ang), math.sin(ang)
        bx, by = x - size * ca, y - size * sa
        px, py = -sa * size * hw, ca * size * hw
        self.raw(f'<polygon points="{f2(x)},{f2(y)} {f2(bx + px)},{f2(by + py)} {f2(bx - px)},{f2(by - py)}" '
                 f'fill="{c}" stroke="{c}" stroke-width="0.6" stroke-linejoin="round"/>')
        self._seg(x, y, bx, by, tag)

    def arrow(self, x1, y1, x2, y2, c=INK, w=2.0, head=9.5, hw=0.36, dash=None, both=False, tag=""):
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1e-6:
            return
        ang = math.atan2(y2 - y1, x2 - x1)
        hs = min(head, L * 0.6)
        sx, sy = x1, y1
        ex, ey = x2 - (hs * 0.78) * math.cos(ang), y2 - (hs * 0.78) * math.sin(ang)
        if both:
            sx, sy = x1 + (hs * 0.78) * math.cos(ang), y1 + (hs * 0.78) * math.sin(ang)
        self.line(sx, sy, ex, ey, c, w, dash, tag=tag)
        self.head(x2, y2, ang, c, hs, hw)
        if both:
            self.head(x1, y1, ang + math.pi, c, hs, hw)

    def arrow_poly(self, pts, c=INK, w=2.0, head=9.5, dash=None, both=False):
        """Seta que segue uma poli‑linha; cabeça no último ponto."""
        if len(pts) < 2:
            return
        ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        body = list(pts[:-1]) + [(pts[-1][0] - head * 0.78 * math.cos(ang), pts[-1][1] - head * 0.78 * math.sin(ang))]
        self.pl(body, c, w, dash=dash)
        self.head(pts[-1][0], pts[-1][1], ang, c, head)

    def mid_head(self, pts, t=0.5, c=INK, size=9, hw=0.38, rev=False, tag=""):
        """Cabeça de seta posicionada na fração t do comprimento da poli‑linha."""
        L = [0.0]
        for a, b in zip(pts, pts[1:]):
            L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        target = L[-1] * t
        for i in range(1, len(pts)):
            if L[i] >= target:
                a, b = pts[i - 1], pts[i]
                seg = max(L[i] - L[i - 1], 1e-9)
                u = (target - L[i - 1]) / seg
                x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
                ang = math.atan2(b[1] - a[1], b[0] - a[0]) + (math.pi if rev else 0)
                # a ponta fica deslocada para frente para que o centro do triângulo caia em (x,y)
                self.head(x + 0.45 * size * math.cos(ang), y + 0.45 * size * math.sin(ang), ang, c, size, hw, tag)
                return (x, y, ang)
        return None

    def arc(self, cx, cy, r, a0, a1, c=INK, w=1.5, arrow=False, dash=None, head=8, rev_arrow=False):
        """Arco em graus (convenção matemática: anti‑horário, y para cima). a0→a1 percorrido no sentido do sinal."""
        n = max(8, int(abs(a1 - a0) / 6))
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        if arrow:
            self.arrow_poly(pts, c, w, head, dash)
        else:
            self.pl(pts, c, w, dash=dash)
        if rev_arrow:
            ang = math.atan2(pts[0][1] - pts[1][1], pts[0][0] - pts[1][0])
            self.head(pts[0][0], pts[0][1], ang, c, head)
        return pts

    # ── texto ───────────────────────────────────────────────────────────────────
    def text(self, x, y, s, size=12, c=INK, anchor="middle", weight=400, rot=0, halo=False, lint=True,
             italic=False, cls=""):
        """Escreve ``s`` com linha de base em y. Retorna a caixa (x0,y0,x1,y1)."""
        bold = weight >= 600
        runs = parse(s, bold)
        widths = []
        for r in runs:
            widths.append((sum(_adv(r.font, r.bold or bold, ch) for ch in r.text) * r.scale + r.pad) * size)
        W = sum(widths)
        x0 = x - W / 2 if anchor == "middle" else (x - W if anchor == "end" else x)
        cur = 0.0
        tsp, extra = [], []
        xx = x0
        top, bot = 1e9, -1e9
        rads = []        # (x_inicio, x_fim, y_base, fs)
        cur_rad = None
        for r, wd in zip(runs, widths):
            fs = size * r.scale
            dy = r.dy * size
            tsp_dy = dy - cur
            cur = dy
            cl = {"sans": "", "math": "mi", "main": "mr"}[r.font]
            at = f' class="{cl}"' if cl else ""
            fsz = f' font-size="{f2(fs)}"' if r.scale != 1 else ""
            dya = f' dy="{f2(tsp_dy)}"' if abs(tsp_dy) > 1e-6 else ""
            if r.pad:
                dya += f' dx="{f2(r.pad * size)}"'
            fw = ' font-weight="600"' if (r.bold or bold) and r.font == "sans" else ""
            tsp.append(f'<tspan{at}{fsz}{dya}{fw} xml:space="preserve">{esc(r.text)}</tspan>')
            desc = 0.22 if any(ch in 'gjpqyQ,;()[]{}|µρβγφψ∫' for ch in r.text) else 0.03
            top = min(top, y + dy - 0.74 * fs)
            bot = max(bot, y + dy + desc * fs)
            if r.rad:
                cur_rad = [xx, xx, y + dy, fs]
            if r.over and cur_rad is not None:
                cur_rad[1] = xx + wd
            if (not r.over) and cur_rad is not None:
                rads.append(tuple(cur_rad))
                cur_rad = None
            if r.vec:
                lead = r.text[0]
                wl = _adv(r.font, False, lead) * fs
                xx += r.pad * size
                ay = y + dy - (0.80 if lead.isupper() or lead in "ℓ" else 0.64) * fs
                extra.append((xx + 0.14 * fs, ay, xx + wl + 0.10 * fs))
                top = min(top, ay - 3)
            xx += wd
        if cur_rad is not None:
            rads.append(tuple(cur_rad))
        for (rx0, rx1, yb, fs_) in rads:
            ty = yb - 0.80 * fs_
            self.pl([(rx0 + 0.02 * fs_, yb - 0.30 * fs_), (rx0 + 0.13 * fs_, yb - 0.37 * fs_),
                     (rx0 + 0.31 * fs_, yb + 0.10 * fs_), (rx0 + 0.55 * fs_, ty), (rx1 + 0.12 * fs_, ty)],
                    c, max(0.9, fs_ * 0.075), tag="halo")
            top = min(top, ty - 1)
            W = max(W, rx1 + 0.12 * fs_ - x0)
        wgt = ' font-weight="600"' if bold else ""
        if bold and weight >= 700:
            wgt = ' font-weight="700"'
        rt = f' transform="rotate({f2(rot)} {f2(x)} {f2(y)})"' if rot else ""
        hl = ' class="halo"' if halo else ""
        extcls = f' class="{cls}"' if cls and not halo else hl
        itl = ' font-style="italic"' if italic else ""
        self.raw(f'<text x="{f2(x0)}" y="{f2(y)}" font-size="{f2(size)}" fill="{c}"{wgt}{itl}{extcls}{rt}>' + "".join(tsp) + "</text>")
        for ax0, ay, ax1 in extra:
            self.line(ax0, ay, ax1, ay, c, max(0.8, size * 0.075), cap="butt", tag="halo")
            self.head(ax1 + 0.5, ay, 0, c, size * 0.34, 0.5, tag="halo")
        box = (x0, top, x0 + W, bot)
        if rot:
            a = math.radians(rot)
            pts = [(x + (px - x) * math.cos(a) - (py - y) * math.sin(a), y + (px - x) * math.sin(a) + (py - y) * math.cos(a))
                   for px, py in [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]]
            box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        self.labels.append({"text": re.sub(r"\s+", " ", s), "box": box, "lint": lint, "halo": halo})
        return box

    def tb(self, x, y, s, **kw):
        """Texto centrado verticalmente em y (útil dentro de caixas)."""
        size = kw.get("size", 12)
        return self.text(x, y + 0.34 * size, s, **kw)

    def charge(self, x, y, q, r=11, label=None, lab_dx=0, lab_dy=0, lw=2.2):
        """Carga puntiforme: círculo com + (coral) ou − (azul)."""
        pos = q > 0
        col, fil = (POS, POS_L) if pos else (NEG, NEG_L)
        self.circ(x, y, r, fil, col, 2, tag="bg")
        a = r * 0.52
        self.line(x - a, y, x + a, y, col, lw, tag="bg")
        if pos:
            self.line(x, y - a, x, y + a, col, lw, tag="bg")

    def ground(self, x, y, c=INK, w=1.8):
        self.line(x, y, x, y + 7, c, w)
        for k, hw in enumerate((11, 7.5, 4)):
            self.line(x - hw, y + 7 + k * 4.2, x + hw, y + 7 + k * 4.2, c, w)

    def cross_dot(self, x, y, kind, r=9, c=INK, w=1.7, fill=WHITE):
        """⊙ (kind='out', saindo) ou ⊗ (kind='in', entrando)."""
        self.circ(x, y, r, fill, c, w, tag="bg")
        if kind == "out":
            self.dot(x, y, r * 0.30, c)
        else:
            a = r * 0.58
            self.line(x - a, y - a, x + a, y + a, c, w, tag="bg")
            self.line(x - a, y + a, x + a, y - a, c, w, tag="bg")

    def hatch_defs(self):
        pass

    # ── lint ────────────────────────────────────────────────────────────────────
    def lint(self):
        issues = []
        L = self.labels
        for i, a in enumerate(L):
            if not a["lint"]:
                continue
            x0, y0, x1, y1 = a["box"]
            if x0 < -0.5 or y0 < -0.5 or x1 > self.w + 0.5 or y1 > self.h + 0.5:
                issues.append(f"fora do quadro: «{a['text']}» {tuple(round(v) for v in a['box'])}")
            for b in L[i + 1:]:
                if not b["lint"]:
                    continue
                u0, v0, u1, v1 = b["box"]
                if min(x1, u1) - max(x0, u0) > 0.8 and min(y1, v1) - max(y0, v0) > 1.5:
                    issues.append(f"rótulos sobrepostos: «{a['text']}» × «{b['text']}»")
            if a["halo"]:
                continue
            shrink = (x0 + 0.8, y0 + 1.6, x1 - 0.8, y1 - 1.2)
            hit, first = 0, None
            for (sx1, sy1, sx2, sy2, tag) in self.strokes:
                if tag in IGNORE_TAGS:
                    continue
                if _seg_hits_box(sx1, sy1, sx2, sy2, shrink):
                    hit += 1
                    first = first or (round(sx1), round(sy1), round(sx2), round(sy2))
            if hit:
                issues.append(f"traço cruza rótulo «{a['text']}» ({hit} seg., ex. {first}) box={tuple(round(v) for v in a['box'])}")
        return issues

    # ── saída ───────────────────────────────────────────────────────────────────
    def svg(self, standalone=False, aria=None):
        ttl = esc(aria or self.title or self.name)
        body = "\n".join(self.parts)
        dfs = "".join(self.defs)
        if standalone:
            style = ("<style>@import url('../src/fonts.css');@import url('../assets/katex/katex.min.css');"
                     "text{font-family:'Source Sans 3','DejaVu Sans',sans-serif;font-kerning:none;font-variant-ligatures:none}"
                     ".mi{font-family:KaTeX_Math;font-style:italic}.mr{font-family:KaTeX_Main}"
                     ".halo{paint-order:stroke;stroke:#fff;stroke-width:3.2px;stroke-linejoin:round}</style>")
            return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(self.w)} {f2(self.h)}" '
                    f'width="{f2(self.w)}" height="{f2(self.h)}" role="img" aria-label="{ttl}">{style}'
                    f'<rect width="100%" height="100%" fill="#fff"/><defs>{dfs}</defs>\n{body}\n</svg>')
        return (f'<svg class="fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(self.w)} {f2(self.h)}" '
                f'role="img" aria-label="{ttl}" data-w="{f2(self.w)}" data-h="{f2(self.h)}"><defs>{dfs}</defs>\n{body}\n</svg>')


# ───────────────────────── gráfico cartesiano ──────────────────────────────────────────
class Plot:
    """Eixos com unidades, grade leve e conversão dados→pixel."""

    def __init__(self, f: Fig, x0, y0, w, h, xlim, ylim, xlabel="", ylabel="", xticks=(), yticks=(),
                 grid=True, xlab_dy=0, ylab_dx=0, arrows=True, tick_size=10.5, label_size=12, origin_label=True):
        self.f, self.x0, self.y0, self.w, self.h = f, x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim
        self.ts = tick_size
        # grade
        if grid:
            for t, _ in xticks:
                if t != xlim[0]:
                    f.line(self.X(t), y0, self.X(t), y0 - h, GRY_XL, 0.9, tag="grid")
            for t, _ in yticks:
                if t != ylim[0]:
                    f.line(x0, self.Y(t), x0 + w, self.Y(t), GRY_XL, 0.9, tag="grid")
        # eixos
        ext = 12 if arrows else 0
        f.arrow(x0, y0, x0 + w + ext, y0, INK, 1.6, 8, 0.34) if arrows else f.line(x0, y0, x0 + w, y0, INK, 1.6)
        f.arrow(x0, y0, x0, y0 - h - ext, INK, 1.6, 8, 0.34) if arrows else f.line(x0, y0, x0, y0 - h, INK, 1.6)
        for t, lab in xticks:
            px = self.X(t)
            f.line(px, y0, px, y0 + 4, INK, 1.2)
            if lab != "":
                f.text(px, y0 + 4 + tick_size + 2.5, lab, tick_size, MUTED)
        for t, lab in yticks:
            py = self.Y(t)
            f.line(x0 - 4, py, x0, py, INK, 1.2)
            if lab != "":
                f.text(x0 - 7, py + tick_size * 0.34, lab, tick_size, MUTED, anchor="end")
        self.xlabel, self.ylabel = xlabel, ylabel
        self.label_size = label_size

    def X(self, x):
        return self.x0 + (x - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * self.w

    def Y(self, y):
        return self.y0 - (y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * self.h

    def pts(self, data):
        return [(self.X(x), self.Y(y)) for x, y in data]

    def line(self, data, c=INK, w=2.2, dash=None, op=None):
        self.f.pl(self.pts(data), c, w, dash=dash, op=op)

    def curve(self, fn, a, b, n=80, c=INK, w=2.2, dash=None):
        data = [(a + (b - a) * k / n, fn(a + (b - a) * k / n)) for k in range(n + 1)]
        self.f.pl(self.pts(data), c, w, dash=dash)

    def area(self, data, base=0.0, fill=ENE, op=0.22, edge=None):
        pts = self.pts(data + [(data[-1][0], base), (data[0][0], base)])
        self.f.pl(pts, edge, 1.0, fill=fill, close=True, fop=op, tag="bg")

    def point(self, x, y, c=INK, r=4.2, fill=WHITE):
        self.f.circ(self.X(x), self.Y(y), r, fill, c, 2.0, tag="bg")

    def guide(self, x=None, y=None, c=GRY, dash="4 3", w=1.1, x_from=None, y_from=None):
        if x is not None and y is not None:
            self.f.line(self.X(x), self.Y(y), self.X(x), self.y0, c, w, dash, tag="bg")
            self.f.line(self.X(x), self.Y(y), self.x0, self.Y(y), c, w, dash, tag="bg")
        elif x is not None:
            self.f.line(self.X(x), self.y0, self.X(x), self.Y(self.ylim[1] if y_from is None else y_from), c, w, dash, tag="bg")
        elif y is not None:
            self.f.line(self.x0, self.Y(y), self.X(self.xlim[1] if x_from is None else x_from), self.Y(y), c, w, dash, tag="bg")

    def axis_labels(self, xlabel=None, ylabel=None, xdx=0, xdy=0, ydx=0, ydy=0, size=None):
        f = self.f
        s = size or self.label_size
        xl = xlabel if xlabel is not None else self.xlabel
        yl = ylabel if ylabel is not None else self.ylabel
        if xl:
            f.text(self.x0 + self.w + 15 + xdx, self.y0 + 4.5 + xdy, xl, s, INK, anchor="start")
        if yl:
            f.text(self.x0 + ydx, self.y0 - self.h - 17 + ydy, yl, s, INK, anchor="middle")


# ───────────────────────── linhas de campo (integração numérica) ──────────────────────────
def trace_field(charges, start, sign=+1, step=3.0, maxn=900, bounds=(0, 0, 400, 300), stop_r=9.0, extra_field=None):
    """Integra uma linha de campo de cargas puntiformes [(x,y,q),…] a partir de ``start``.
    sign=+1 segue E; sign=-1 segue −E. Interrompe perto de cargas, ao sair de ``bounds`` ou em maxn passos."""
    x, y = start
    pts = [(x, y)]

    def E(px, py):
        ex = ey = 0.0
        for cx, cy, q in charges:
            dx, dy = px - cx, py - cy
            r2 = dx * dx + dy * dy + 1e-9
            r3 = r2 * math.sqrt(r2)
            ex += q * dx / r3
            ey += q * dy / r3
        if extra_field:
            a, b = extra_field(px, py)
            ex += a
            ey += b
        n = math.hypot(ex, ey) + 1e-12
        return sign * ex / n, sign * ey / n

    for _ in range(maxn):
        k1 = E(x, y)
        k2 = E(x + step * 0.5 * k1[0], y + step * 0.5 * k1[1])
        x += step * k2[0]
        y += step * k2[1]
        pts.append((x, y))
        if not (bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]):
            break
        if any(math.hypot(x - cx, y - cy) < stop_r for cx, cy, q in charges if (q * sign) < 0):
            break
    return pts


def resample(pts, ds=1.0):
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= ds:
            out.append(b)
            acc = 0.0
    out.append(pts[-1])
    return out


def field_lines(f: Fig, charges, bounds, n_per_unit=8, c=EFD, w=1.5, r0=13, arrows=(0.5,), stop_r=10, size=8,
                clip=None, step=3.0, sources=None):
    """Desenha linhas de campo a partir das cargas (todas as positivas emitem n linhas ∝ |q|;
    se não houver positivas, as negativas recebem linhas desenhadas ‘para trás’)."""
    lines = []
    srcs = sources if sources is not None else [ch for ch in charges if ch[2] > 0]
    sign = +1
    if not srcs:
        srcs = [ch for ch in charges if ch[2] < 0]
        sign = -1
    for (cx, cy, q) in srcs:
        n = max(4, int(round(n_per_unit * abs(q))))
        for k in range(n):
            a = 2 * math.pi * (k + 0.5) / n
            st = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
            pts = trace_field(charges, st, sign, step, 1200, bounds, stop_r)
            pts = [(cx + (r0 - 1) * math.cos(a), cy + (r0 - 1) * math.sin(a))] + pts
            if clip:
                pts = clip(pts)
            f.pl(pts, c, w, tag="bg", op=0.95)
            for t in arrows:
                f.mid_head(pts, t, c, size, rev=(sign < 0), tag="bg")
            lines.append(pts)
    return lines
