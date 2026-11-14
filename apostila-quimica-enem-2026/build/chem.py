"""Conversor de fórmulas químicas em HTML limpo (sem KaTeX/mhchem).

Sintaxe (inspirada no mhchem):
    \\ce{H2SO4}                -> H<sub>2</sub>SO<sub>4</sub>
    \\ce{Ca^2+}                -> Ca<sup>2+</sup>
    \\ce{SO4^2-}               -> SO<sub>4</sub><sup>2−</sup>
    \\ce{Na+ + Cl-}            -> carga quando '+'/'-' colado na fórmula e seguido de espaço/fim
    \\ce{2H2 + O2 -> 2H2O}     -> seta SVG vetorial
    \\ce{A <=> B}              -> setas de equilíbrio
    \\ce{A ->[Δ] B}            -> rótulo sobre a seta
    \\ce{CaCO3(s)}             -> estados (aq) (s) (l) (g) em tamanho reduzido
    \\ce{^235U}  \\ce{^{14}C}   -> isótopos (sobrescrito antes do símbolo)
"""
import re

MINUS = "−"

_ARROW_R = ('<svg class="ar" viewBox="0 0 24 10" width="22" height="9" aria-hidden="true">'
            '<path d="M1 5H21" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
            '<path d="M17 1.4L22.2 5L17 8.6" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
_ARROW_L = ('<svg class="ar" viewBox="0 0 24 10" width="22" height="9" aria-hidden="true">'
            '<path d="M3 5H23" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
            '<path d="M7 1.4L1.8 5L7 8.6" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
_ARROW_EQ = ('<svg class="ar" viewBox="0 0 24 12" width="22" height="11" aria-hidden="true">'
             '<path d="M1 3.6H21.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
             '<path d="M17.6 0.6L21.6 3.6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
             '<path d="M23 8.4H2.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
             '<path d="M6.4 11.4L2.4 8.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>')
_ARROW_BOTH = ('<svg class="ar" viewBox="0 0 26 10" width="24" height="9" aria-hidden="true">'
               '<path d="M3 5H23" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
               '<path d="M7 1.4L1.8 5L7 8.6M19 1.4L24.2 5L19 8.6" fill="none" stroke="currentColor" '
               'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

ARROWS = {"->": _ARROW_R, "<-": _ARROW_L, "<=>": _ARROW_EQ, "<->": _ARROW_BOTH}

_ARROW_RE = re.compile(r"(<=>|<->|->|<-)((?:\[[^\]]*\]){0,2})")
_STATE_RE = re.compile(r"\((aq|s|l|g)\)")


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _sup(content):
    content = content.replace("-", MINUS)
    return f"<sup>{_esc(content)}</sup>"


def _format_token(seg):
    """Formata um trecho sem setas."""
    out = []
    i = 0
    n = len(seg)
    prev = ""  # tipo do caractere anterior: 'L' letra, 'C' fecha ) ] , 'D' dígito normal, 'S' sub/sup, ''
    while i < n:
        c = seg[i]
        m = _STATE_RE.match(seg, i)
        if m:
            out.append(f'<span class="st">({m.group(1)})</span>')
            i = m.end()
            prev = "C"
            continue
        if c == "^":
            j = i + 1
            if j < n and seg[j] == "{":
                k = seg.index("}", j)
                content = seg[j + 1:k]
                i = k + 1
            else:
                mm = re.match(r"\d*[+\-−]?", seg[j:])
                content = mm.group(0)
                i = j + len(content)
            out.append(_sup(content))
            prev = "S"
            continue
        if c == "_":
            j = i + 1
            if j < n and seg[j] == "{":
                k = seg.index("}", j)
                content = seg[j + 1:k]
                i = k + 1
            else:
                mm = re.match(r"[A-Za-z0-9]+", seg[j:])
                content = mm.group(0)
                i = j + len(content)
            out.append(f"<sub>{_esc(content)}</sub>")
            prev = "S"
            continue
        if c.isdigit():
            j = i
            while j < n and seg[j].isdigit():
                j += 1
            run = seg[i:j]
            if prev in ("L", "C"):
                out.append(f"<sub>{run}</sub>")
                prev = "S"
            else:
                out.append(run)
                prev = "D"
            i = j
            continue
        if c in "+-" and prev in ("L", "C", "S", "D") and (i + 1 >= n or seg[i + 1] in " ]),") and prev != "D":
            out.append(_sup(c))
            prev = "S"
            i += 1
            continue
        if c == "-":
            out.append(MINUS if (i == 0 and n == 1) else "-")
            prev = ""
            i += 1
            continue
        if c.isalpha():
            prev = "L"
        elif c in ")]":
            prev = "C"
        elif c in "(.[·•":
            prev = ""
        else:
            prev = ""
        out.append(_esc(c))
        i += 1
    return "".join(out)


def ce(s):
    """Converte a fonte química em HTML."""
    s = s.strip()
    parts = []
    pos = 0
    for m in _ARROW_RE.finditer(s):
        if m.start() > pos:
            parts.append(("t", s[pos:m.start()]))
        labels = re.findall(r"\[([^\]]*)\]", m.group(2))
        parts.append(("a", m.group(1), labels))
        pos = m.end()
    if pos < len(s):
        parts.append(("t", s[pos:]))
    html = []
    for p in parts:
        if p[0] == "t":
            # separa por espaços mantendo-os; cada token fica não-quebrável
            toks = re.split(r"(\s+)", p[1])
            for tk in toks:
                if not tk:
                    continue
                if tk.isspace():
                    html.append(" ")
                elif tk in "+":
                    html.append("+")
                else:
                    html.append(f'<span class="f">{_format_token(tk)}</span>')
        else:
            arrow = ARROWS[p[1]]
            labels = p[2]
            if labels:
                top = labels[0]
                bot = labels[1] if len(labels) > 1 else ""
                top_html = _format_token(top) if top else ""
                bot_html = f'<span class="lab">{_format_token(bot)}</span>' if bot else ""
                html.append(f'<span class="arw"><span class="lab">{top_html}</span>{arrow}{bot_html}</span>')
            else:
                html.append(arrow)
    return f'<span class="ce">{"".join(html)}</span>'


def _find_brace_end(s, start):
    """start aponta para '{' ; retorna índice do '}' correspondente."""
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("chave não fechada em: " + s[start:start + 60])


def replace_ce(text):
    """Substitui todas as ocorrências de \\ce{...} no texto."""
    out = []
    i = 0
    key = "\\ce{"
    while True:
        j = text.find(key, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        k = _find_brace_end(text, j + 3)
        out.append(ce(text[j + 4:k]))
        i = k + 1
    return "".join(out)


if __name__ == "__main__":
    tests = [
        "H2SO4", "Ca(OH)2", "Al2(SO4)3", "SO4^2-", "Fe^3+", "Na+ + Cl-", "2H2 + O2 -> 2H2O",
        "CH3COOH + CH3CH2OH <=> CH3COOCH2CH3 + H2O", "CaCO3(s) ->[Δ] CaO(s) + CO2(g)",
        "^{235}U + n -> ^{141}Ba", "[H^+]", "CuSO4·5H2O", "e-", "H3O+",
    ]
    for t in tests:
        print(t, "=>", ce(t)[:300])
