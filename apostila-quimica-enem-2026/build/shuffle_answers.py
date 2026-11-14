"""Redistribui a posição do gabarito nas questões (uso único; o resultado fica gravado nas páginas).

Cada alternativa correta passa a levar data-ok="1" (invisível no PDF); o build lê esse atributo
para gerar o gabarito, de modo que gabarito e alternativas nunca divirjam.
Modos: swap (troca a correta com a alternativa da letra-alvo), keep (só marca), rev (inverte a ordem
da lista, para listas numéricas) e desc (ordena descendente a lista numérica dada na ordem fornecida).
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "..", "src", "pages")

# chave: (letra correta ATUAL, modo, letra-alvo ou None)
PLAN = {
    "alcoois_sol": ("B", "swap", "D"), "mais_soluvel": ("B", "swap", "A"), "hidretos": ("B", "swap", "C"),
    "o2_usina": ("B", "swap", "D"), "membrana": ("B", "swap", "A"), "fenol_naoh": ("B", "swap", "B"),
    "propanona": ("B", "swap", "D"), "amina_basica": ("B", "swap", "A"), "eugenol": ("B", "swap", "C"),
    "acucares": ("A", "swap", "D"), "acido_ester": ("B", "swap", "B"), "bromo": ("B", "swap", "A"),
    "oxida_sec": ("B", "swap", "D"), "agua_dura": ("B", "swap", "C"), "pet": ("B", "swap", "B"),
    "lactico": ("B", "swap", "A"),
    "kno3": ("B", "rev", None), "diluicao": ("B", "keep", None), "titula_h2so4": ("B", "rev", None),
    "h2o2": ("B", "keep", None), "minerio": ("A", "keep", None),
    "coligativa": ("D", "keep", None), "azeotropo": ("C", "swap", "A"), "separacao": ("B", "swap", "C"),
    "chuva_normal": ("A", "swap", "B"), "dbo": ("B", "swap", "A"), "biomag": ("C", "keep", None),
    "catalisador": ("B", "swap", "D"), "haber": ("B", "swap", "B"), "ph_hcl": ("C", "keep", None),
    "hess": ("B", "keep", None), "daniell": ("B", "swap", "A"), "eletrolise": ("D", "keep", None),
    "meiavida": ("C", "meia", None), "periodicas": ("A", "swap", "D"), "tiporeacao": ("C", "swap", "B"),
}

SPAN = re.compile(r'<span(?: data-ok="1")?><b>([A-E])</b>(.*?)</span>', re.S)


def process(text, key, cur, mode, tgt):
    m = re.search(r"\{\{q:%s\}\}" % key, text)
    if not m:
        return text, False
    a = text.index('<div class="alts', m.end())
    b = text.index("</div>", a)
    seg = text[a:b]
    head_end = seg.index(">") + 1
    head, body = seg[:head_end], seg[head_end:]
    alts = [t for _, t in SPAN.findall(body)]
    letters = "ABCDE"
    ci = letters.index(cur)
    assert len(alts) > ci, key
    if mode == "meia":                       # 25, 50, 12,5, 6,25 -> 50, 25, 12,5, 6,25
        alts = [alts[1], alts[0], alts[2], alts[3]]
        ci = 2
    elif mode == "rev":
        alts = alts[::-1]
        ci = len(alts) - 1 - ci
    elif mode == "swap":
        ti = letters.index(tgt)
        alts[ci], alts[ti] = alts[ti], alts[ci]
        ci = ti
    new_body = "".join('<span%s><b>%s</b>%s</span>' % (' data-ok="1"' if i == ci else "", letters[i], t)
                       for i, t in enumerate(alts))
    return text[:a] + head + new_body + text[b:], True


def main():
    done = set()
    for f in sorted(glob.glob(os.path.join(PAGES, "p*.html"))):
        t = open(f, encoding="utf-8").read()
        changed = False
        for key, (cur, mode, tgt) in PLAN.items():
            if "{{q:%s}}" % key in t:
                if 'data-ok="1"' in t[t.index("{{q:%s}}" % key):t.index("{{q:%s}}" % key) + 3000].split("{{q:")[0]:
                    print("já processada:", key)
                    continue
                t, ok = process(t, key, cur, mode, tgt)
                changed |= ok
                done.add(key)
        if changed:
            open(f, "w", encoding="utf-8").write(t)
    missing = set(PLAN) - done
    print("processadas:", len(done), "faltando:", missing)


if __name__ == "__main__":
    main()
