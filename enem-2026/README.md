# Reta Final — Central de Intensivão ENEM 2026

Ferramenta pessoal (não é produto) pra organizar os últimos meses antes do ENEM 2026
(provas em 08/11 e 15/11/2026) em torno de três eixos: **priorização por incidência
histórica**, **repetição espaçada com base científica** e **diagnóstico de erros por
categoria**.

O app não contém questões — você resolve questões em outras fontes (provas do INEP,
plataformas de cursinho) e usa o app pra organizar o processo: o que estudar, quando
revisar de novo, e um log rápido de cada leva de questões pra virar diagnóstico real.

## Metodologia implementada

- **Retrieval practice**: o ciclo de estudo sempre termina em "responder questões e
  registrar o resultado", nunca em "reler conteúdo" (Roediger & Karpicke; Dunlosky et
  al., 2013).
- **Repetição espaçada adaptativa**: intervalos 1 → 3 → 7 → 14 → 30 dias (Cepeda et
  al., 2006). Erro relevante (acerto < 70%) reseta pra 1 dia; acerto fácil (≥ 90%) pula
  2 degraus; acerto com esforço (70–90%) avança 1 degrau. Ver `src/lib/srs.ts`.
- **Error log categorizado**: cada questão errada é marcada com uma causa — falta de
  conteúdo, interpretação, cálculo/execução, gestão de tempo, distração/atenção ou
  estratégia — pra gerar direcionamento real, não só "errei essa".
- **Priorização por incidência, não pelo edital inteiro**: 78 temas classificados em
  ALTA/MÉDIA/BAIXA recorrência (dataset cruzado entre Aprova Total, Estratégia
  Vestibulares, SAS/CNN e Assaad). Baixa prioridade nunca é escondida, só rebaixada.
  Ver `src/data/temas.ts`.
- **Simulados cronometrados**: módulo de registro no formato e horário oficiais
  (13h30, 5h30/5h), com evolução por área ao longo dos 3 meses.

## Stack

- Vite + React 18 + TypeScript
- Tailwind CSS (identidade visual própria — sem tema padrão)
- Zustand com persistência em `localStorage` (sem backend, 100% local)
- Recharts para os gráficos de evolução e distribuição de erro
- React Router (`HashRouter`, compatível com hospedagem estática)

## Rodando localmente

```bash
cd enem-2026
npm install
npm run dev
```

Abre em `http://localhost:5173`. Mobile-first — melhor experiência testando em viewport
estreita ou no celular mesmo.

## Build de produção

```bash
npm run build
```

Gera `dist/` como um site 100% estático (pode ser hospedado em qualquer lugar — Vercel,
Netlify, GitHub Pages, ou aberto localmente).

## Persistência de dados

Todo o histórico (estados de repetição espaçada por tema, log de questões, simulados,
streak) fica em `localStorage`, chave `enem-2026-reta-final`. Não há backend — os dados
não saem do navegador. Isso significa:

- Recomendado sempre usar o mesmo navegador/dispositivo pra manter o histórico dos 3
  meses.
- Limpar dados de navegação do site apaga o progresso — não há como recuperar.
- Se quiser migrar de dispositivo, dá pra copiar o valor da chave `enem-2026-reta-final`
  do `localStorage` manualmente (DevTools → Application → Local Storage).

## Estrutura

```
src/
  types.ts               # tipos: Tema, TemaState, QuestionLog, Simulado, ErrorCategory
  data/temas.ts           # dataset dos 78 temas (área, tier, %, subtópicos, fonte)
  lib/
    date.ts                # countdown, streak, datas ISO
    srs.ts                 # motor de repetição espaçada + engine de priorização
    stats.ts               # agregações pro diagnóstico e painel
  store/store.ts          # estado global (Zustand + persist)
  components/
    ui.tsx                  # Card, ProgressRing, TierBadge, Sheet, Button...
    Shell.tsx                # navegação (bottom nav mobile / top nav desktop)
    QuestionLogForm.tsx      # formulário de registro de questões (usado em Ciclo e Diagnóstico)
  pages/
    Home.tsx                 # contagem regressiva, domínio geral, streak, anéis por área
    Conteudo.tsx              # mapa de conteúdo priorizado por área/tier
    Ciclo.tsx                 # fluxo diário: sugestão → estudo → questões → registro
    Diagnostico.tsx           # error log categorizado + análises
    Simulados.tsx              # registro de simulados + evolução por área
    Dashboard.tsx               # painel consolidado
```

## Vocabulário

- **Domínio operacional**: não é "acertar questão", é dominar o processo de um tema —
  medido pelo progresso no ciclo de repetição espaçada + acurácia.
- **Núcleo S**: conteúdo obrigatório de alta incidência histórica (tier ALTA no
  dataset).
- **Reta final**: os últimos meses antes da prova, tratados como fase de execução, não
  de descoberta.
