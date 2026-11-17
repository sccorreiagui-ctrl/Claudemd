module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, hbars } = H;
  const body = `
<div class="ptitle"><h1>Diretas Já, Emenda Dante de Oliveira e a transição de 1985</h1><span class="per">1983–1985</span></div>

${sec('Diretas Já: da proposta à derrota na Câmara', 'soc', flow([
    { t: 'causa', k: 'soc', h: 'Crise e abertura', p: 'recessão, inflação e dívida; vitórias da oposição em 1982; sociedade quer votar para presidente.' },
    { t: 'fato', k: 'soc', h: 'Mar/1983', p: 'o deputado <b>Dante de Oliveira</b> (PMDB-MT) propõe a emenda das eleições diretas.' },
    { t: 'fato', k: 'soc', h: 'Jan–abr/1984', p: 'comícios crescem: Curitiba, <b>Praça da Sé</b> (25/jan), Rio e <b>Anhangabaú</b> (16/abr).' },
    { t: 'fato', k: 'rep', h: '25/abr/1984', p: 'o governo impõe medidas de emergência em Brasília e pressiona a base; Câmara vota.' },
    { t: 'cons', k: 'cris', h: 'Derrota', p: 'faltam 22 votos: continua a eleição indireta.' },
  ], { h: true }))}

<div class="row r2">
  ${chart('Votação da Emenda Dante de Oliveira (25/abr/1984)', 'deputados federais; era preciso 2/3 do total (320 votos) — Câmara dos Deputados / Senado Federal', hbars([['A favor (Sim)', 298, '#2a7a4b', '298'], ['Contra (Não)', 65, '#b3261e', '65'], ['Abstenções', 3, '#9aa8ba', '3'], ['Ausentes', 113, '#c3ccd8', '113'], ['Necessário (2/3)', 320, '#1e3a5f', '320']], { max: 330 }), '<div class="src" style="margin-top:1mm">A emenda teve <b>maioria</b> (298 × 65), mas não os dois terços exigidos: <b>faltaram 22 votos</b>.</div>')}
  <div class="col">
    ${call('cris', 'Por que a emenda caiu?', 'Uma emenda constitucional exigia <b>dois terços</b> dos deputados (320 votos). Com 113 ausências, ela alcançou 298. Como a Constituição vigente determinava a eleição indireta (Colégio Eleitoral), a escolha de 1985 seguiu esse caminho, embora a mobilização popular tenha continuado a pesar.')}
  </div>
</div>

${succ({
    title: 'Mapa da sucessão de 1985', tag: 'Tancredo foi eleito, mas nunca tomou posse',
    nodes: [
      { n: 'João Figueiredo', s: '1979 → 15/mar/1985' },
      { n: 'Tancredo Neves', s: 'eleito em 15/jan/1985; nunca tomou posse', c: 'interim' },
      { n: 'José Sarney', s: 'vice · assume 15/mar/1985 · efetivado 21/abr', c: 'now' },
    ],
    steps: [
      ['ind', '<b>15/jan/1985.</b> O Colégio Eleitoral elege <b>Tancredo Neves</b> (480 votos) contra Paulo Maluf (180; 26 abstenções), pela chapa da <b>Aliança Democrática</b> (PMDB + dissidentes do PDS reunidos na Frente Liberal), com José Sarney, ex-presidente do PDS, como vice.'],
      ['inter', '<b>14–15/mar/1985.</b> Tancredo é internado na véspera da posse. Sarney assume em 15/mar <b>como vice no exercício</b> da Presidência; Figueiredo não entrega a faixa.'],
      ['morte', '<b>21/abr/1985.</b> Morre Tancredo, que <b>nunca foi empossado</b>. Sarney é reconhecido como <b>presidente</b> (entendimento político e jurídico conduzido por Ulysses Guimarães).'],
    ], one: true,
  })}

<div class="row r2-53">
  ${sec('Por que a ditadura terminou por transição negociada?', 'soc', ul([
    '<b>Crise econômica</b> e perda de legitimidade: recessão, inflação e dívida.',
    '<b>Racha das elites</b>: dissidentes do PDS (Frente Liberal) se aliam ao PMDB após a escolha de <b>Maluf</b> (ago/1984).',
    '<b>Pressão social</b>: Diretas Já, sindicatos e Igreja reorganizam a sociedade civil.',
    '<b>Continuidade negociada</b>: eleição indireta, anistia mantida e transição sem rompimento institucional; a Nova República nasce em 15/mar/1985.',
  ], 'soc'))}
  ${call('int', 'Nota de correção', 'O inventário de aulas afirma que os militares “impuseram” a Tancredo manter a Anistia e escolher Sarney. <b>Não há comprovação disso</b>: Sarney foi indicado dentro da aliança entre PMDB e Frente Liberal. O que se documenta é uma transição pactuada, sem “revanchismo”.')}
</div>

${sec('Linha do tempo: Diretas Já e transição', 'gray', tl({
    start: { d: 'mar/1983', t: 'Emenda Dante de Oliveira' },
    events: [
      { d: '12/jan/1984', t: 'Comício em Curitiba', k: 'soc' },
      { d: '25/jan/1984', t: 'Praça da Sé (SP)', k: 'soc' },
      { d: '25/abr/1984', t: 'Emenda derrotada', k: 'cris' },
      { d: 'ago/1984', t: 'PDS escolhe Maluf', k: 'cris' },
      { d: '15/jan/1985', t: 'Tancredo eleito', k: 'soc' },
    ],
    end: { d: '15/mar/1985', t: 'Sarney assume; início da Nova República' },
  }))}

${rev([
    ['Por que as Diretas Já não resultaram imediatamente em eleição presidencial direta?', 'A emenda recebeu 298 votos, 22 a menos que os 320 (2/3) necessários; a eleição de 1985 foi indireta, mas a mobilização popular deslocou apoio a Tancredo e minou o regime.'],
    ['Por que Tancredo nunca foi presidente em exercício?', 'Foi internado na véspera da posse (14/mar/1985) e morreu em 21/abr; Sarney, o vice, assumiu e foi efetivado presidente.'],
  ])}
<div class="src">Fontes: Câmara dos Deputados e Senado Federal (votação de 25/abr/1984: 298 × 65, 3 abstenções, 113 ausências); CPDOC/FGV (Diretas Já; Tancredo Neves; Aliança Democrática); Arquivo Nacional.</div>
`;
  return page(20, { per: 'dit', assunto: 'Diretas Já e transição de 1985', intervalo: '1983–1985' }, body);
};
