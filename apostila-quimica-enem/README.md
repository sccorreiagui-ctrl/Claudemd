# Apostila visual de Química para o ENEM

PDF final: [`Apostila_Visual_Quimica_ENEM.pdf`](Apostila_Visual_Quimica_ENEM.pdf) — 38 páginas A4 (limite: 40).
Relatório de verificações automáticas: [`controle_qualidade.txt`](controle_qualidade.txt).

## Como regenerar

Requisitos: Python 3.11+, Node.js com `playwright` (Chromium) e `pdftoppm` (opcional, para prévias).

```bash
pip install -r requirements.txt
cd src && python3 build.py      # gera build/apostila.html e Apostila_Visual_Quimica_ENEM.pdf
```

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `src/lib.py` | paleta semântica, CSS, primitivas SVG, componentes de página |
| `src/molsvg.py` | estruturas moleculares (RDKit) com grupos funcionais destacados e verificados por SMARTS |
| `src/chk.py` | verificações automáticas: balanceamento, massas, cálculos dos exemplos |
| `src/figs.py` | figuras reutilizáveis (lipídios, bicamada, micela, vesícula) |
| `src/fonts.py` | converte Inter (OTF) em TrueType subconjunto para um PDF leve |
| `src/p00_intro.py`, `pA.py` … `pR.py` | conteúdo por módulo (A–K, revisão) |
| `build/render.js` | HTML → PDF (Chromium) e detecção de texto estourado/cortado |

Código de cores: azul = polaridade/água; âmbar = apolar/lipofilia; roxo = orgânica/grupos funcionais;
verde = Biologia/ambiente; laranja = reações; vermelho = erros e alertas.

## Limites conhecidos

Ver a última página do PDF (fontes e status de acesso). Em especial: os PDFs de provas e da Matriz do Inep
não puderam ser baixados no ambiente de geração; nenhuma questão oficial foi conferida no caderno.
