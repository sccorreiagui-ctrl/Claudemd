#!/usr/bin/env python3
r"""Monta build/apostila.html a partir de src/pages/*.html + figuras Python.

Sintaxe nas páginas:
  <!--mod=II|sec=Lei de Coulomb|kind=page-->   (primeira linha)
  <fig name="nome" cls="line">Legenda opcional (aceita \\( math \\))</fig>   ou   <fig name="nome"/>
  {{lvl:2}}                                    (indicador de nível 1–3)
  {{toc}}                                      (somente na página de sumário)
Matemática: \( ... \) e \[ ... \]  (KaTeX).  Títulos de seção: <h2 class="sec" data-toc="7.3|Lei de Coulomb">.
"""
import re, sys, json, pathlib, html, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import figures  # noqa: E402
figures.load_all()

PAGES = sorted((ROOT / "src" / "pages").glob("p*.html"))
OUT = ROOT / "build" / "apostila.html"
SVG_DIR = ROOT / "figures_svg"
MODS = {"I": "Módulo I · Fundamentos", "II": "Módulo II · Eletrostática", "III": "Módulo III · Eletrodinâmica",
        "IV": "Módulo IV · Magnetismo e eletromagnetismo", "R": "Revisão final"}
LVL_NAMES = {1: "Fundamental", 2: "Intermediário", 3: "Avançado"}

fig_n = [0]
used_figs = []
issues_all = []


def lvl_svg(n):
    cs = "".join(f'<circle cx="{4 + 11 * i}" cy="4" r="3" class="{"on" if i < n else ""}"/>' for i in range(3))
    return f'<svg class="lvl" viewBox="0 0 30 8" role="img" aria-label="nível {n}">{cs}</svg>'


def render_fig(name, caption="", opts="", page_label=""):
    if name not in figures.REGISTRY:
        raise KeyError(f"figura não registrada: {name}")
    obj = figures.REGISTRY[name]()
    obj.name = name
    for msg in obj.lint():
        issues_all.append(f"[{page_label}] fig:{name}: {msg}")
    used_figs.append((name, obj))
    cap = ""
    if caption:
        fig_n[0] += 1
        cap = f'<figcaption><b>Fig. {fig_n[0]}</b>{caption}</figcaption>' 
    cls = ("f " + opts).strip()
    return f'<figure class="{cls}">{obj.svg()}{cap}</figure>'


def process(text, label):
    def f_fig(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        return render_fig(attrs["name"], (m.group(2) or "").strip(), attrs.get("cls", ""), label)
    text = re.sub(r"<fig\s+([^>]*?)\s*(?:/>|>(.*?)</fig>)", f_fig, text, flags=re.S)
    text = re.sub(r"\{\{lvl:(\d)\}\}", lambda m: lvl_svg(int(m.group(1))), text)
    return text


def parse_meta(raw):
    m = re.match(r"\s*<!--(.*?)-->\s*", raw, re.S)
    meta = {}
    if m:
        for kv in m.group(1).split("|"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    return meta, raw


def main():
    t0 = time.time()
    pages = []
    toc = []  # (level, num, text, page)
    for idx, pf in enumerate(PAGES, start=1):
        raw = pf.read_text(encoding="utf-8")
        meta, body = parse_meta(raw)
        label = f"p{idx:02d} {pf.stem}"
        body = process(body, label)
        for m in re.finditer(r'data-toc-mod="([^"]*)"', body):
            rom, _, name = m.group(1).partition("|")
            toc.append(("mod", rom, name, idx))
        for m in re.finditer(r'data-toc="([^"]*)"', body):
            num, _, name = m.group(1).partition("|")
            toc.append(("sec", num, name, idx))
        pages.append((idx, pf.stem, meta, body))

    def toc_html():
        out = ['<div class="toc">']
        for kind, num, name, pg in toc:
            if kind == "mod":
                out.append(f'<div class="tm"><span>{num}</span><span>{name}</span><span class="pg">{pg}</span></div>')
            else:
                out.append(f'<div class="te"><span class="n">{num}</span><span>{name}</span><span class="dots"></span>'
                           f'<span class="pg">{pg}</span></div>')
        out.append("</div>")
        return "\n".join(out)

    secs = []
    for idx, stem, meta, body in pages:
        body = body.replace("{{toc}}", toc_html())
        kind = meta.get("kind", "page")
        mod = meta.get("mod", "")
        if kind == "cover":
            secs.append(f'<section class="page cover-page" id="pg{idx}" data-mod="I">{body}</section>')
            continue
        modname = MODS.get(mod, "")
        sec = meta.get("sec", "")
        head = (f'<header class="run"><span>Física Elétrica · ENEM + PAS 3 · 2026</span>'
                f'<span><span class="m">{html.escape(modname)}</span>{(" · " + html.escape(sec)) if sec else ""}</span></header>')
        foot = (f'<footer class="run"><span class="pn">{idx}</span>'
                f'<span>Apostila de Física Elétrica · do básico ao avançado</span></footer>')
        secs.append(f'<section class="page" id="pg{idx}" data-mod="{mod}">{head}<div class="body"><div class="flow{" " + meta["flow"] if "flow" in meta else ""}">{body}</div></div>{foot}</section>')

    macros = {
        "\\un": "\\,\\mathrm{#1}", "\\sen": "\\operatorname{sen}", "\\ud": "\\mathrm{d}",
        "\\Ev": "\\vec{E}", "\\Bv": "\\vec{B}", "\\Fv": "\\vec{F}", "\\vv": "\\vec{v}", "\\Uv": "\\vec{u}",
        "\\ohm": "\\,\\Omega", "\\eps": "\\varepsilon", "\\dd": "\\mathrm{d}", "\\ve": "\\varepsilon",
        "\\tg": "\\operatorname{tg}", "\\neq": "\\mathrel{\\char\"2260}", "\\ne": "\\mathrel{\\char\"2260}",
    }
    doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Apostila de Física Elétrica — ENEM + PAS 3 (UnB) — do básico ao avançado</title>
<meta name="author" content="Apostila de Física Elétrica 2026">
<meta name="description" content="Eletrostática, eletrodinâmica, magnetismo e eletromagnetismo: curso compacto do básico ao avançado (ENEM e PAS 3/UnB).">
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<link rel="stylesheet" href="../src/style.css">
<script src="../assets/katex/katex.min.js"></script>
<script src="../assets/katex/auto-render.min.js"></script>
<script>
window.__ready = false;
document.addEventListener('DOMContentLoaded', async () => {{
  renderMathInElement(document.body, {{
    delimiters: [{{left:'\\\\[', right:'\\\\]', display:true}}, {{left:'\\\\(', right:'\\\\)', display:false}}],
    throwOnError: false, output: 'html', strict: 'ignore', trust: false,
    macros: {json.dumps(macros)}
  }});
  try {{ await document.fonts.ready; }} catch(e) {{}}
  window.__ready = true;
}});
</script></head>
<body>
<main>
{chr(10).join(secs)}
</main>
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    SVG_DIR.mkdir(exist_ok=True)
    for name, obj in used_figs:
        (SVG_DIR / f"{name}.svg").write_text(obj.svg(standalone=True), encoding="utf-8")
    print(f"build ok: {len(pages)} páginas, {len(used_figs)} figuras, {time.time() - t0:.1f}s -> {OUT}")
    if issues_all:
        print(f"\n⚠ {len(issues_all)} avisos de lint de figuras:")
        for s in issues_all:
            print("  ", s)


if __name__ == "__main__":
    main()
