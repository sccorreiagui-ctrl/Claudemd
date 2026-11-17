module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, chart, barChart } = H;
  const { IGPDI } = require('../lib/data.js');
  const ys = ['1985', '1986', '1987', '1988', '1989'];
  const infSvg = barChart({ w: 70, h: 40, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', colors: { 1986: '#0b7a8a' }, ymin: 0, ymax: 2000, ticks: [0, 1000, 2000], show: ys, dec: 0, pad: { l: 8, r: 1, t: 4, b: 6 } });
  const body = `
${gov({
    nome: 'José Sarney', anos: '1985–1990', sub: 'PMDB · 15/03/1985 → 15/03/1990 · início da Nova República', foto: 'sarney',
    ficha: {
      chegada: `${chip('const', 'Vice eleito')} Vice de <b>Tancredo Neves</b> (Aliança Democrática), ex-presidente do PDS. Assume em 15/mar/1985 como vice no exercício e é <b>efetivado presidente</b> em 21/abr/1985, após a morte de Tancredo (p. 20).`,
      contexto: 'Inflação de <b>235%</b> (1985), dívida externa de US$ 105 bi, recessão recente; primeiro governo civil desde 1964, com <b>militares ainda influentes</b> e forte expectativa democrática.',
      termino: 'Mandato de <b>5 anos</b>, fixado pela Constituinte, encerrado em 15/mar/1990, com inflação de <b>1.783%</b> em 1989 e baixa popularidade.',
      sucessao: `${chip('dir')} Primeira eleição direta para presidente desde 1960: <b>Fernando Collor</b> (PRN) 53,0% × Lula (PT) 47,0% no 2º turno de 17/dez/1989. Posse em 15/mar/1990.`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Democratização e Constituição de 1988', 'soc', ul([
    '<b>Emenda 25</b> (mai/1985): eleições diretas para presidente e <b>voto do analfabeto</b>; partidos comunistas legalizados.',
    '<b>Constituinte</b>: o Congresso eleito em 15/nov/1986 é instalado em 1/fev/1987 sob <b>Ulysses Guimarães</b>; relator Bernardo Cabral.',
    '<b>Constituição promulgada em 5/out/1988</b>, a <b>“Constituição Cidadã”</b>, marco da consolidação institucional da Nova República.',
    'Política externa: relações com Cuba restabelecidas (1986) e aproximação com a Argentina, base do futuro <b>Mercosul</b>.',
  ], 'soc'))}
  <div class="col">
    ${chart('Inflação anual (IGP-DI)', '% dez/dez · FGV (Ipeadata); ciano = Cruzado', infSvg)}
  </div>
</div>

${sec('Constituição de 1988: principais inovações', 'inst', med([
    ['Direitos', 'soc', 'Voto aos 16 anos (facultativo) e voto facultativo do analfabeto; licença-maternidade de 120 dias; jornada de 44 h; <b>racismo crime inafiançável e imprescritível</b>; habeas data e mandado de injunção; <b>direitos indígenas</b>.'],
    ['Estado', 'inst', 'Federalismo com mais autonomia aos municípios; <b>Ministério Público</b> fortalecido; fim da censura; presidencialismo mantido (plebiscito de 1993).'],
    ['Social', 'soc', '<b>Seguridade social</b> e <b>SUS</b> (saúde universal); educação como direito.'],
  ]))}

${sec('4 · Planos econômicos e dificuldades', 'eco', flow([
    { t: 'causa', k: 'eco', h: 'Inflação inercial', p: 'preços reajustados pelo passado; dívida e déficit.' },
    { t: 'fato', k: 'eco', h: '<b>Cruzado</b> (28/fev/1986)', p: 'congelamento, nova moeda, gatilho salarial; consumo explode e surgem filas, ágio e desabastecimento.' },
    { t: 'fato', k: 'eco', h: 'Cruzado II, Bresser (1987) e Verão (1989)', p: 'novos choques e congelamentos fracassam; moratória da dívida (fev/1987).' },
    { t: 'cons', k: 'rep', h: 'Fim do governo', p: 'inflação de quatro dígitos (1.783% em 1989) e descrédito do Estado.' },
  ], { h: true }))}

<div class="row r2">
  ${sec('Crises e conflitos', 'cris', ul([
    '<b>Planos fracassados</b> e vitória do PMDB em 1986 seguida de desencanto (Cruzado II, após as eleições).',
    '<b>Conflitos no campo</b>: assassinato de Chico Mendes (22/dez/1988); greves e repressão (CSN, nov/1988).',
    '<b>Centrão</b> disputa pontos da Constituinte; mandato de Sarney (5 anos) decidido pelos constituintes.',
  ], 'cris'))}
  ${call('', 'Nova República', 'Convém marcar o início da Nova República em <b>1985</b> e a <b>Constituição de 1988</b> como o marco de sua consolidação institucional.')}
</div>

${sec('Linha do tempo do governo Sarney', 'gray', tl({
    start: { d: '15/mar/1985', t: 'Assume (vice no exercício); efetivado em 21/abr' },
    events: [
      { d: 'mai/1985', t: 'Emenda 25: diretas e voto do analfabeto', k: 'soc' },
      { d: '28/fev/1986', t: 'Plano Cruzado', k: 'eco' },
      { d: '1/fev/1987', t: 'Constituinte instalada', k: 'inst' },
      { d: '5/out/1988', t: 'Constituição Cidadã', k: 'soc' },
      { d: '17/dez/1989', t: 'Collor vence o 2º turno', k: 'cris' },
    ],
    end: { d: '15/mar/1990', t: 'Posse de Collor' },
  }))}

${rev([
    ['Por que a Constituição de 1988 é um marco da Nova República?', 'Consolidou a democracia e ampliou direitos civis, políticos e sociais, após 21 anos de ditadura; deu base institucional ao regime iniciado em 1985.'],
    ['Por que os planos do governo Sarney falharam?', 'Combatiam a inflação por congelamentos sem ajuste fiscal; o efeito inicial era popular, mas o descongelamento trouxe inflação ainda maior.'],
  ])}
<div class="src">Fontes: Senado Federal e Câmara dos Deputados (Constituição de 1988; Assembleia Constituinte); CPDOC/FGV (Sarney; Plano Cruzado); Planalto (Emendas 25 e 26/1985); Ipeadata (IGP-DI).</div>
`;
  return page(21, { per: 'nova', assunto: 'Governo José Sarney e a Constituição de 1988', intervalo: '1985–1990' }, body);
};
