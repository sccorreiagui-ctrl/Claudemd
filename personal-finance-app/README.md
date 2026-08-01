# Bússola — Controle Financeiro Pessoal

Aplicação 100% front-end (HTML, CSS e JavaScript puros, sem build step) para
organizar a renda mensal em categorias, lançar gastos reais e acompanhar o
planejado x realizado. Não há backend, login ou chamadas externas — todos os
dados ficam salvos no `localStorage` do navegador.

## Rodando localmente

Basta abrir `index.html` em um navegador, ou servir a pasta com qualquer
servidor estático:

```bash
cd personal-finance-app
python3 -m http.server 8080
```

## Publicando de graça

Qualquer serviço de hospedagem estática funciona, sem custo e sem domínio
próprio:

- **GitHub Pages**: em Settings → Pages, aponte para esta pasta (ou publique
  o conteúdo dela na branch `gh-pages`).
- **Netlify / Vercel**: importe o repositório e configure o diretório
  publicado como `personal-finance-app`, sem comando de build.

## Estrutura

```
personal-finance-app/
  index.html   # estrutura da página e modais
  style.css    # tema (claro/escuro), layout responsivo, animações
  app.js       # estado, persistência em localStorage, renderização e gráficos
```

## Funcionalidades

- Múltiplas fontes de renda por mês.
- Categorias livres (criar, renomear, excluir) com valor planejado.
- Lançamento de gastos reais por categoria (data, descrição, valor).
- Dashboard com total recebido, planejado, gasto e saldo livre.
- Alertas visuais quando a alocação ultrapassa a renda, ou um gasto ultrapassa
  o planejado da categoria — nada é bloqueado, apenas destacado.
- Navegação entre meses, cada um com seus próprios dados (categorias do mês
  anterior são copiadas automaticamente, sem os lançamentos).
- Gráfico de barras e de distribuição (pizza), anel de progresso circular,
  contadores animados e demais microinterações.
- Modo claro/escuro.
