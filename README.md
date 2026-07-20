# Claudemd

Repositório para Claude code. Geração de projetos de alto nível!

## Sistema de Automação de Orçamentos — Rigel Engenharia e Impermeabilizações

Aplicação web para montar orçamentos por formulário (sem editar planilhas), sugerir o
último preço usado por item, calcular totais/split material-serviço e gerar a planilha
Excel (e PDF) final no padrão visual da empresa — só depois de uma aprovação humana.

Ver a especificação completa na descrição da tarefa que originou este projeto.

### Funcionalidades

- Formulário de orçamento (cliente, obra, condições) com categorias e itens dinâmicos.
- Sugestão automática do último preço usado por item, com alerta ignorável em caso de divergência.
- Catálogo de serviços com autocomplete ao digitar a descrição de um item (evita redigitar
  os textos técnicos longos e melhora a precisão da sugestão de preço).
- Templates de categoria (Banheiro, Subsolo/Cisterna, Cobertura, Reservatório etc.) para
  montar categorias inteiras com um clique.
- Percentual material/serviço configurável por orçamento **e**, quando necessário, por item
  individual (ex.: um item 100% mão de obra).
- Duplicar orçamento (cópia independente) e criar nova revisão (cópia ligada ao orçamento
  aprovado de origem, com numeração "Rev NN" automática).
- Aprovação humana obrigatória: bloqueia edição e grava os preços usados na memória do sistema.
- Geração de Excel (openpyxl) e PDF (reportlab) no padrão visual da empresa.

### Stack

- **Backend:** Python + FastAPI + SQLAlchemy + SQLite
- **Geração de Excel:** openpyxl · **Geração de PDF:** reportlab
- **Frontend:** HTML + JS puro (sem build step), servido como arquivos estáticos pelo próprio FastAPI

### Estrutura

```
backend/
  app/
    main.py              # app FastAPI, cria as tabelas, roda o seed inicial e serve o frontend
    database.py           # engine/sessão SQLite
    models.py             # tabelas: orcamentos, orcamento_categorias, orcamento_itens,
                           # itens_preco, servico_catalogo, categoria_templates(_itens)
    schemas.py             # schemas Pydantic (request/response)
    crud.py                # regras de negócio (totais, sugestão de preço, aprovação,
                           # duplicar/nova revisão, catálogo, templates)
    seed.py                 # popula catálogo de serviços e templates com dados reais das propostas
    numero_por_extenso.py  # valor em reais por extenso (usado no Excel/PDF)
    excel_generator.py     # monta o .xlsx final a partir do orçamento
    pdf_generator.py       # monta o .pdf final a partir do orçamento (mesmo layout do Excel)
    routers/
      orcamentos.py         # CRUD de orçamento/categoria/item, aprovar, duplicar, nova
                             # revisão, baixar excel/pdf, categoria a partir de template
      itens_preco.py         # consulta de sugestão de preço
      catalogo.py             # autocomplete de serviços e listagem de templates de categoria
  tests/test_api.py        # testes de API (pytest)
  requirements.txt
  requirements-dev.txt      # requirements.txt + pytest/httpx
frontend/
  index.html / app.js / style.css   # formulário interativo (sem build step)
```

### Como rodar localmente

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Acesse `http://localhost:8000`. O banco SQLite é criado automaticamente em
`backend/data/orcamentos.db` (ignorado pelo git) na primeira execução.

Para hospedar na rede local da empresa, rode o comando acima na máquina compartilhada e
acesse pelo IP dela (`http://<ip-da-máquina>:8000`) a partir dos outros computadores.
**Faça backup periódico de `backend/data/orcamentos.db`** — é o único lugar onde a
memória de preços fica armazenada.

### Testes

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

### Fluxo funcional

1. Criar orçamento → preencher dados do cliente/obra.
2. Adicionar categorias e itens. Ao sair do campo de descrição, o sistema busca o
   último preço usado para aquele item e preenche automaticamente; se o preço for
   alterado manualmente, um alerta (não bloqueante) é exibido.
3. Totais (geral, material, serviço) são recalculados automaticamente — considerando o
   percentual de material do orçamento, ou o override definido em um item específico.
4. Baixar Excel ou PDF para revisão.
5. Aprovar — bloqueia edição e grava os preços unitários usados na memória do sistema
   (tabela `itens_preco`), para alimentar as sugestões dos próximos orçamentos.
6. A partir de um orçamento aprovado, é possível criar uma **nova revisão** (cópia
   editável ligada ao original, com "Rev NN" incrementado automaticamente) ou apenas
   **duplicar** qualquer orçamento como um novo rascunho independente.

### Pendência conhecida

O percentual material/serviço (60%/40% nos três modelos analisados) foi implementado
como campo editável por orçamento, com valor padrão 60/40. Se a empresa confirmar que é
sempre fixo, o campo pode virar uma constante do sistema.
