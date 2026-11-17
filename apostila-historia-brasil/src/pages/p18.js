module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const body = `
${gov({
    nome: 'Ernesto Geisel', anos: '1974–1979', sub: 'ARENA · 15/03/1974 → 15/03/1979', foto: 'geisel',
    ficha: {
      chegada: `${chip('ind')} General castelista (ESG), <b>eleito pelo Colégio Eleitoral</b> em 15/jan/1974: 400 votos × 76 em Ulysses Guimarães (“anticandidato” do MDB). Posse em 15/mar/1974.`,
      contexto: '<b>Choque do petróleo</b> (out/1973: preço do barril quadruplica) esgota o Milagre; inflação sobe a 34,6% (1974); oposição cresce; <b>linha dura</b> controla o aparato repressivo.',
      termino: 'Entregou o cargo em 15/mar/1979, com o AI-5 já revogado (vigência da revogação em 1/jan/1979), mas com inflação alta e dívida externa de cerca de US$ 52 bi (1978).',
      sucessao: `${chip('ind')} <b>João Figueiredo</b>, escolhido por Geisel e eleito pelo Colégio Eleitoral em 15/out/1978 (355 × 226 do general Euler Bentes Monteiro, MDB). Posse em 15/mar/1979.`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Economia e política externa', 'eco', med([
    ['II PND', 'eco', '<b>II Plano Nacional de Desenvolvimento</b> (1975–79): em vez de ajustar, investe em energia, siderurgia, petroquímica e bens de capital para <b>reduzir dependência de importações</b>; financiado por dívida externa.'],
    ['Energia', 'eco', '<b>Proálcool</b> (1975) e hidrelétricas (Itaipu); <b>acordo nuclear Brasil–Alemanha</b> (1975); contratos de risco com a Petrobras.'],
    ['Exterior', 'int', '<b>“Pragmatismo responsável”</b>: relações com a <b>China Popular</b> (1974), reconhecimento de Angola (1975), rompimento do acordo militar com os EUA (1977).'],
  ]))}
  <div class="col">
    ${sec('Abertura “lenta, gradual e segura”', 'soc', ul([
    'Projeto de <b>distensão</b> articulado por Geisel e Golbery (Casa Civil): reduzir a tutela militar sem perder o controle.',
    '<b>Revogação do AI-5</b>: Emenda nº 11 (out/1978; vigência em 1/jan/1979).',
  ], 'soc'))}
  </div>
</div>

${sec('4 · Oposição, “linha dura” e recuos', 'rep', `<table class="t rep">
  <tr><th>Data</th><th>Fato</th><th>Efeito</th></tr>
  <tr><td class="k">15/nov/1974</td><td>Eleições: o MDB elege <b>16 das 22</b> vagas do Senado e amplia a bancada na Câmara</td><td>Voto de protesto contra a ditadura; ARENA reage</td></tr>
  <tr><td class="k">25/out/1975</td><td><b>Vladimir Herzog</b>, jornalista, é morto no DOI-CODI de São Paulo; a versão oficial de suicídio é contestada</td><td>Culto ecumênico na Sé e comoção; golpe na linha dura</td></tr>
  <tr><td class="k">17/jan/1976</td><td>O operário <b>Manoel Fiel Filho</b> morre no mesmo DOI-CODI</td><td>Geisel demite o general Ednardo D’Ávila Mello do II Exército</td></tr>
  <tr><td class="k">jul/1976</td><td><b>Lei Falcão</b>: propaganda eleitoral só com nome, número e currículo</td><td>Tenta frear o MDB nas eleições municipais</td></tr>
  <tr><td class="k">14/abr/1977</td><td><b>Pacote de Abril</b>: Congresso fechado por duas semanas; <b>senadores “biônicos”</b> (1/3 do Senado eleito <u>indiretamente</u> pelas assembleias), eleição indireta de governadores, mandato de 6 anos para o próximo presidente</td><td>Garante maioria à ARENA; protesto da oposição</td></tr>
  <tr><td class="k">12/out/1977</td><td>Geisel demite o ministro do Exército, Sylvio Frota, candidato da linha dura</td><td>Reafirma o controle sobre o aparato militar</td></tr>
</table>`)}

${sec('II PND e dívida: o ciclo 1974–1979', 'eco', flow([
    { t: 'causa', k: 'int', h: 'Choque do petróleo', p: 'custo do barril sobe; o Brasil importava a maior parte do que consumia.' },
    { t: 'fato', k: 'eco', h: 'II PND', p: 'crédito externo financia investimentos em energia e indústria pesada.' },
    { t: 'cons', k: 'rep', h: 'Dívida e inflação', p: 'dívida externa sobe de US$ 14,9 bi (1973) a US$ 52 bi (1978); inflação passa de 34,6% (1974) a 40,8% (1978).' },
  ], { h: true }))}

${sec('Linha do tempo do governo Geisel', 'gray', tl({
    start: { d: '15/mar/1974', t: 'Posse de Geisel' },
    events: [
      { d: '15/nov/1974', t: 'MDB vence no Senado', k: 'soc' },
      { d: '25/out/1975', t: 'Morte de Herzog', k: 'rep' },
      { d: '1976', t: 'Lei Falcão', k: 'rep' },
      { d: '14/abr/1977', t: 'Pacote de Abril', k: 'rep' },
      { d: '13/out/1978', t: 'Emenda revoga o AI-5', k: 'soc' },
    ],
    end: { d: '15/mar/1979', t: 'Posse de Figueiredo' },
  }))}

${rev([
    ['Qual a diferença entre a abertura de Geisel e a de Figueiredo?', 'A de Geisel foi controlada e tutelada: concessões pontuais, sem desmontar o aparato, com recuos (Pacote de Abril). A de Figueiredo ampliou o processo (Anistia, pluripartidarismo), mas sob pressão social crescente e crise econômica (p. 19).'],
    ['O que eram os senadores “biônicos”?', 'Um terço do Senado, escolhido <b>indiretamente</b> por colégio eleitoral estadual a partir de 1978 (Pacote de Abril), para garantir maioria à ARENA.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Geisel; Herzog); Câmara dos Deputados (Emenda nº 8/1977, Emenda nº 11/1978); Senado Federal; Comissão Nacional da Verdade; Ipeadata (dívida e IGP-DI).</div>
`;
  return page(18, { per: 'dit', assunto: 'Governo Geisel', intervalo: '1974–1979' }, body);
};
