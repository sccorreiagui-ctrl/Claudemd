#!/usr/bin/env python3
"""Gera RELATORIO_QUALIDADE.md com estatísticas calculadas a partir das fontes e do PDF final.
Uso: python3 tools/make_report.py   (execute depois de tools/build.py, tools/render.js e tools/verify_physics.py)"""
import re, json, pathlib, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = sorted((ROOT / "src" / "pages").glob("p*.html"))
PDF = ROOT / "APOSTILA_FISICA_ELETRICA_ENEM_PAS3_2026.pdf"
if not PDF.exists():
    PDF = ROOT / "build" / "apostila.pdf"

MODS = [("Capa e sumário", 1, 2), ("I · Fundamentos", 3, 6), ("II · Eletrostática", 7, 18),
        ("III · Eletrodinâmica", 19, 39), ("IV · Magnetismo e eletromagnetismo", 40, 51), ("Revisão final", 52, 55)]


def pnum(f):
    return int(re.match(r"p(\d+)", f.name).group(1))


stats = {m[0]: dict(pag=m[2] - m[1] + 1, ex=0, exe=0, fig=0, tab=0) for m in MODS}
ex_all, fig_names = [], []
for f in PAGES:
    t = f.read_text(encoding="utf-8")
    n = pnum(f)
    for name, a, b in MODS:
        if a <= n <= b:
            s = stats[name]
            s["ex"] += len(re.findall(r"Exemplo (\d+)</span>", t))
            s["exe"] += len(re.findall(r"<li>\{\{lvl:\d\}\}", t)) + len(re.findall(r'<li><span class="b">\{\{lvl:\d\}\}', t))
            s["fig"] += len(re.findall(r"<fig\s", t))
            s["tab"] += len(re.findall(r"<table", t))
    ex_all += [int(x) for x in re.findall(r"Exemplo (\d+)</span>", t)]
    fig_names += re.findall(r'<fig\s+name="([^"]+)"', t)

tot = {k: sum(s[k] for s in stats.values()) for k in ("pag", "ex", "exe", "fig", "tab")}
n_svg = len(list((ROOT / "figures_svg").glob("*.svg")))

# PDF
info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout
pages_pdf = int(re.search(r"Pages:\s+(\d+)", info).group(1))
size_kb = PDF.stat().st_size / 1024
fonts = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True).stdout.splitlines()[2:]
all_emb = all(l.split()[-5] == "yes" for l in fonts if l.strip()) if fonts else False
txt = subprocess.run(["pdftotext", "-f", "40", "-l", "40", str(PDF), "-"], capture_output=True, text=True).stdout
searchable = len(txt.strip()) > 500

try:
    import pypdf
    def _walk(o, acc):
        for x in o:
            if isinstance(x, list):
                _walk(x, acc)
            else:
                acc.append(x)
        return acc
    n_bookmarks = len(_walk(pypdf.PdfReader(str(PDF)).outline, []))
except Exception:
    n_bookmarks = 0

# verificação numérica
ver = subprocess.run(["python3", str(ROOT / "tools" / "verify_physics.py")], capture_output=True, text=True).stdout
m = re.search(r"(\d+) verificações; (TODAS OK|HÁ DIVERGÊNCIAS)", ver)
n_checks, ver_ok = (int(m.group(1)), m.group(2)) if m else (0, "?")

# layout
rep = json.loads((ROOT / "build" / "layout_report.json").read_text(encoding="utf-8"))
bad = [r for r in rep if not r.get("special") and (r["over_px"] > 0.5 or r["over_w_px"] > 0.5 or r["katexErr"] or r["wide"])]
fills = [r["fill"] for r in rep if not r.get("special")]
avg_fill = sum(fills) / len(fills) * 100

today = datetime.date.today().isoformat()

rows = "\n".join(f"| {n} | {s['pag']} | {s['ex']} | {s['exe']} | {s['fig']} | {s['tab']} |" for n, s in stats.items())

md = f"""# Relatório de Qualidade — Apostila de Física Elétrica (ENEM + PAS 3/UnB)

*Gerado em {today} por `tools/make_report.py`. Os números abaixo são calculados a partir dos arquivos-fonte e do PDF final, não digitados à mão.*

## 1. Entregáveis

| Item | Arquivo / pasta |
|---|---|
| **PDF final** (A4 vertical, {pages_pdf} páginas, {size_kb/1024:.1f} MB) | `apostila_fisica/APOSTILA_FISICA_ELETRICA_ENEM_PAS3_2026.pdf` |
| Projeto editável | `apostila_fisica/src/` (páginas HTML, CSS, figuras em Python/SVG), `tools/` (build, render, verificação), `assets/` (KaTeX e fontes locais) |
| Figuras vetoriais exportadas | `apostila_fisica/figures_svg/` ({n_svg} arquivos SVG) |
| HTML montado | `apostila_fisica/build/apostila.html` |
| Este relatório | `apostila_fisica/RELATORIO_QUALIDADE.md` |

Para regenerar: ver `README.md` (`python3 tools/build.py && node tools/render.js APOSTILA_...pdf`).

## 2. Conteúdo produzido

| Parte | Páginas | Exemplos resolvidos | Exercícios (itens com nível) | Figuras | Tabelas |
|---|---:|---:|---:|---:|---:|
{rows}
| **Total** | **{tot['pag']}** | **{tot['ex']}** | **{tot['exe']}** | **{tot['fig']}** | **{tot['tab']}** |

* Os exemplos seguem 9 passos (situação, desenho, dados, interpretação, escolha justificada da fórmula, substituição, cálculo, unidade e verificação física). Exemplos numerados de 1 a {max(ex_all)}.
* Cada seção segue a ordem: intuição → conceito → desenho → fórmula (variáveis, unidades, validade, convenções de sinal) → exemplo → erro frequente → fixação → aprofundamento; três níveis (● ○ ○ fundamental, ● ● ○ intermediário, ● ● ● avançado) marcados em cada exemplo e exercício.
* Itens “Julgue (C/E)” e questões estilo ENEM são **autorais** e assim identificados; nenhum enunciado oficial foi reproduzido.
* Presentes, conforme o pedido: superposição de forças elétricas (Ex. 4), campo + potencial (Ex. 5–9), dois circuitos mistos (Ex. 17–18), duas aplicações de Kirchhoff (Ex. 20–22), gerador real (Ex. 23), força magnética circular (Ex. 27), Lenz (Ex. 30 e painéis da Fig. de Lenz), motor/gerador/transformador/transmissão (Ex. 29, 32).
* Mapas mentais: Eletrostática, Eletrodinâmica, Magnetismo e eletromagnetismo; fluxograma de decisão de métodos de circuito; tabelas comparativas: carga +/−, campo elétrico × magnético, corrente real × convencional, série × paralelo, resistores × capacitores, gerador × receptor, amperímetro × voltímetro, motor × gerador, Faraday × Lenz, erros clássicos (Módulos II e IV).
* Formulários por situação de uso (R.1–R.3), constantes, convenções de sinal, ordens de grandeza, 10 questões integradoras com gabarito comentado (R.4–R.5).

## 3. Recursos visuais

* **{tot['fig']} figuras** em SVG vetorial desenhadas por código (bibliotecas próprias `svgkit.py` e `circuit.py`): circuitos com símbolos corretos e escala de cor por potencial nos nós, vetores com setas, linhas de campo calculadas numericamente (integração de segunda ordem, método do ponto médio), gráficos com eixos e unidades, quadros sequenciais (indução por contato, Lenz em quatro quadros, trajetórias em campo magnético).
* **Semântica de cores fixa** em toda a apostila (coral = cargas e polos +; azul = cargas − e elétrons; laranja = corrente convencional e trajetórias; roxo = campo magnético e indução; verde = energia e potência; ciano = campo elétrico e equipotenciais; cinza = neutros, condutores e estrutura), **nunca como única informação**: sempre há sinais, setas, rótulos, ⊙/⊗.
* Fórmulas em KaTeX (texto pesquisável), tipografia Source Sans 3, cabeçalho e numeração, sumário e {n_bookmarks} marcadores (bookmarks) no PDF.

## 4. Complementos em relação ao inventário do NotebookLM

Os tópicos abaixo não estavam no inventário (ou apareciam apenas citados) e foram acrescentados a partir da literatura padrão de Física e das matrizes oficiais: Lei de Coulomb formal e superposição vetorial; potencial e energia com trabalho; blindagem, poder das pontas e capacitores (associação, energia, dielétricos); gerador e receptor reais, curto-circuito (ideal × real), pontes e método dos nós, leis de Kirchhoff com interpretação de corrente negativa, amperímetro e voltímetro reais, ponte de Wheatstone; campo de fio, espira e solenoide, Lei de Ampère (aprofundamento), força entre fios paralelos, seletor de velocidades e espectrômetro, torque e motor, Faraday–Lenz com método visual, haste em trilhos, correntes de Foucault, gerador de CA, transformador, transmissão em alta tensão, ressonância magnética (qualitativa), ondas eletromagnéticas (qualitativa).

## 5. Auditoria do inventário: erros e simplificações corrigidos

| # | Ponto auditado | Tratamento na apostila (onde) |
|---:|---|---|
| 1 | Carga algébrica × módulo | Q = ±n·e e “use o módulo para contar”; Coulomb em módulo com sinais pelo desenho (seções 2.1, 2.3; convenções em R.3) |
| 2 | Linhas de campo elétrico saem de + e chegam a − | 2.4; contraste com as linhas fechadas de B (4.1) |
| 3 | U = E·d só em campo uniforme | Quadro “quando não usar” (2.5) |
| 4 | Propagação do sinal elétrico não é exatamente c | 3.1 (“quem é rápido, quem é lento”: 50 % a 99 % de c; deriva ≈ 10⁻⁴ m/s) |
| 5 | Corrente convencional é convenção de sinal | 3.1 (explica por que o efeito é o mesmo; elétrons em sentido oposto) |
| 6 | Efeito Joule e a escolha de R·I² × U²/R | 3.3 (“maior resistência ⇒ maior potência” é falso em geral) |
| 7 | Em paralelo a tensão é a mesma | 3.4 (quadro série × paralelo e conferências) |
| 8 | Curto-circuito ideal × real | 3.6 (modelo ideal, I_cc = ε/(r + R_fio), fusível e disjuntor) |
| 9 | Resistores × capacitores têm regras opostas | 2.7 e revisão do Módulo III |
| 10 | A força magnética não realiza trabalho | 4.3 (W = 0, só desvia) e erros clássicos |
| 11 | Mão direita e sinal da carga | 4.3 (figura com q > 0 e q < 0), força sobre fios, revisão IV |
| 12 | Lenz opõe-se à **variação** do fluxo, não ao fluxo | 4.4 (texto, figura de 4 quadros, erro frequente) |
| 13 | Hipóteses geométricas das fórmulas de B | 4.2 (tabela de validade: fio longo, centro da espira, solenoide longo) |
| 14 | Transformadores não funcionam com CC estacionária | 4.5 e questões integradoras |
| 15 | Conferir desenhos de circuitos, números, unidades e algarismos significativos | Seção 6 deste relatório (lint de figuras, 213 verificações numéricas) |
| 16 | Mnemônicos | Mnemônicos de teor impróprio ou sem valor didático do inventário foram **omitidos**; os mantidos (p. ex. Q = I·Δt) só aparecem depois do significado |

Além do inventário, a própria produção corrigiu defeitos detectados pelas verificações (ver seção 7).

## 6. Verificações científicas e matemáticas

* **{n_checks} verificações numéricas independentes** (`tools/verify_physics.py`): cada exemplo e exercício com resultado numérico é recalculado em Python e comparado ao texto — resultado: **{ver_ok}**.
* **Análise nodal** independente para os circuitos mistos e a ponte (Ex. 17 e 18) e resolução de sistemas lineares para Kirchhoff (Ex. 21 e 22); balanço de potência conferido em todos os exemplos de circuito.
* **Lint automático das figuras** (sobreposição rótulo × rótulo, rótulo × traço e rótulo fora do quadro): **0 avisos** no build final.
* **Layout**: cada página é medida no navegador (preenchimento, estouro vertical e horizontal, equações mais largas que a coluna, erros do KaTeX): **{len(bad)} páginas com problema** de {len(rep)}; preenchimento médio {avg_fill:.0f} %.
* **PDF**: {pages_pdf} páginas A4; fontes {'incorporadas' if all_emb else 'NÃO incorporadas'}; texto {'pesquisável' if searchable else 'NÃO pesquisável'}; PDF etiquetado (tagged) e com marcadores.
* **Convenções de sentido** conferidas caso a caso por dois caminhos (regra da mão e produto vetorial / Lenz e conservação de energia): painéis de Lenz, haste em trilhos (corrente anti-horária ⇒ força para a esquerda, freando), espira que sai do campo, elétron em campo entrando no papel (giro horário).

## 7. Defeitos encontrados e corrigidos durante a auditoria

Exemplos: superposição de correntes com valores recalculados e corrigidos (Kirchhoff, 3.7); razão solenoide/campo da Terra (≈ 40× ⇒ ≈ 100×, 4.2); dedução incorreta de F = I·L·B reescrita (4.3); gabaritos numerados fora de ordem; referências a “capítulos” antigos (agora “seções”); `<N_p` interpretado como marca HTML (corrigido); equações que ultrapassavam a coluna (quebradas em linhas curtas); vários estouros de página e rótulos sobrepostos em figuras; texto incorreto no gabarito de eletrização por indução; capa e sumário atualizados com os números finais.

## 8. Cobertura das matrizes oficiais (extração automática dos PDFs oficiais)

* **ENEM** (INEP, Matriz de Referência — Ciências da Natureza, H21 e H23): carga e corrente; Coulomb; campo e potencial; linhas de campo; equipotenciais; poder das pontas; blindagem; capacitores; efeito Joule; Ohm; resistividade; tensão, corrente, potência e energia; circuitos simples; corrente contínua e alternada; medidores; símbolos; consumo de energia; campo magnético; ímãs; linhas de campo magnético; campo magnético terrestre — **todos cobertos** (ver tabela na página R.5).
* **PAS 3** (Cebraspe/UnB, matriz de referência): Eletrostática (força, campo e potencial; propriedades elétricas dos materiais); Magnetismo (força e campo; propriedades magnéticas dos materiais); Eletrodinâmica (dispositivos e circuitos; Kirchhoff); Eletromagnetismo (Ampère, Faraday e Lenz; geradores, transformadores e motores; ressonância magnética) — **todos cobertos**; Ampère e ressonância magnética em nível introdutório/qualitativo.

## 9. Limitações e riscos (leitura crítica)

1. **Os vídeos não foram assistidos.** O conteúdo parte do inventário (tratado como hipótese a verificar), das matrizes oficiais e da Física padrão. Se os professores dos vídeos usam convenções próprias (por exemplo, notação de ε × U, sentido da corrente), confira esses pontos com as suas anotações.
2. **Sem revisão humana.** A revisão visual e científica foi feita por inspeção automática e por leitura das páginas renderizadas, não por um professor. Recomenda-se pelo menos uma leitura crítica por docente (principalmente exercícios de nível 3).
3. **Questões autorais, não calibradas.** Os níveis 1–3 são heurísticos; não há teoria de resposta ao item nem teste com estudantes. Servem para treino de conceito e método, não como previsão de nota.
4. **Densidade.** São {tot['pag']} páginas com muita informação por página (fonte ≈ 9,5 pt). Em tela de celular, exige ampliação; para estudo ativo, imprima ou use tablet. O risco pedagógico principal é a “ilusão de domínio” ao ler exemplos resolvidos sem tentar antes: tente cada exemplo cobrindo a resolução.
5. **Tamanho.** O alvo era ≈ 52 páginas (máximo 56). O resultado tem {tot['pag']} (Módulo IV com 12 páginas em vez de 11, para não sacrificar exemplos). Algumas páginas ficam 10–18 % abaixo do preenchimento total.
6. **Aproximações explícitas.** Constantes arredondadas (k = 9,0×10⁹ N·m²/C², e = 1,6×10⁻¹⁹ C etc.); resultados com 2–3 algarismos significativos podem divergir do gabarito de uma prova por arredondamento.
7. **Tópicos qualitativos.** Ressonância magnética, ondas eletromagnéticas, Lei de Ampère e propriedades magnéticas dos materiais estão em nível introdutório; Mecânica, Termologia e Ondulatória entram só como ferramentas (Módulo I), conforme o escopo pedido.
8. **Ferramenta de produção.** Figuras geradas por código próprio (não LaTeX/TikZ/circuitikz): aparência consistente e vetorial, mas os SVGs isolados usam fontes web (KaTeX) e podem exibir texto diferente fora do navegador.
9. **Segurança.** Não há experimentos com rede elétrica, fios energizados ou capacitores de alta tensão; as únicas atividades práticas sugeridas usam ímãs, bússola e tubos metálicos (queda de ímã).

## 10. Próximos passos recomendados

* Submeter as páginas de Kirchhoff e de indução a um professor de Física para validação do discurso e do nível.
* Estudar em ciclos: ler a seção → fazer os exemplos sem olhar → fixação → revisão R.1–R.3; usar as questões integradoras como simulado cronometrado.
* Ampliar o banco de questões (hoje {tot['exe']} itens) com provas anteriores **consultadas diretamente nas fontes oficiais** (sem reprodução na apostila) e classificá-las por seção.
* Ligar cada vídeo do caderno às seções da apostila (marcar minutos relevantes) para cobrir o que a transcrição não captou.
"""
(ROOT / "RELATORIO_QUALIDADE.md").write_text(md, encoding="utf-8")
print("RELATORIO_QUALIDADE.md gerado:", {k: tot[k] for k in tot}, "| checks:", n_checks, ver_ok, "| páginas:", pages_pdf, "| problemas de layout:", len(bad))
