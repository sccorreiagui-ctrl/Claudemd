module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, flowLegend, tl, rev, chip } = H;
  const body = `
<div class="ptitle"><h1>Vargas de 1934 a 1945: do voto ao Estado Novo e à queda</h1><span class="per">1934–1945</span></div>

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Getúlio Vargas — Governo Constitucional', anos: '1934–1937', sub: '20/jul/1934 → 10/nov/1937',
    ficha: {
      chegada: `${chip('ind')} Eleito pela Constituinte em <b>17/jul/1934</b>; mandato até 1938, sem reeleição imediata.`,
      contexto: 'Constituição nova; economia em recuperação; <b>fascismo e comunismo</b> dividem o país.',
      termino: '<b>10/nov/1937:</b> às vésperas da eleição de 1938, fecha o Congresso e outorga nova Constituição.',
      sucessao: `${chip('golpe', 'Golpe do próprio presidente')} Não há sucessão: Vargas permanece e a eleição de 1938 é cancelada.`,
    },
  })}

<div class="row r2">
  <div class="col">
    ${sec('3 · Constituição de 1934 (inspirada em Weimar)', 'inst', ul([
    '<b>Voto secreto</b>, direto e <b>feminino</b>; <b>Justiça Eleitoral</b> e <b>Justiça do Trabalho</b>.',
    '<b>Direitos trabalhistas</b> (salário mínimo, jornada de 8h, férias); ensino primário gratuito; nacionalização das riquezas do subsolo.',
    'Mandato de 4 anos, sem reeleição imediata.',
  ]))}
    ${sec('Linha do tempo do Governo Constitucional', 'gray', tl({
    start: { d: '20/jul/1934', t: 'Posse constitucional' },
    events: [
      { d: 'abr/1935', t: 'Lei de Segurança Nacional', k: 'rep' },
      { d: 'nov/1935', t: 'Levante comunista', k: 'cris' },
      { d: '1936', t: 'Tribunal de Segurança Nacional', k: 'rep' },
    ],
    end: { d: '10/nov/1937', t: 'Golpe: Estado Novo' },
  }))}
  </div>
  <table class="t">
    <tr><th></th><th>AIB (1932)</th><th>ANL (1935)</th></tr>
    <tr><td class="k">Líder</td><td>Plínio Salgado</td><td>Luís Carlos Prestes (presidente de honra)</td></tr>
    <tr><td class="k">Ideia</td><td>Integralismo, inspirado no fascismo: “Deus, Pátria e Família”; camisas-verdes</td><td>Frente antifascista (comunistas, socialistas, tenentes, liberais): “Pão, Terra e Liberdade”</td></tr>
    <tr><td class="k">Propostas</td><td>Estado forte, anticomunismo, corporativismo</td><td>Reforma agrária, suspensão da dívida externa, direitos democráticos</td></tr>
    <tr><td class="k">Destino</td><td>Extinta com os partidos (1937); golpe integralista fracassa (1938)</td><td>Fechada por decreto (jul/1935); Prestes preso (1936)</td></tr>
  </table>
</div>
${sec('4 · Crise: levante de 1935 e Plano Cohen', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Polarização', p: 'AIB × ANL; Lei de Segurança Nacional; ANL fechada.' },
    { t: 'fato', k: 'rep', h: 'Nov/1935', p: 'levante comunista em Natal, Recife e Rio é reprimido; estado de guerra e prisões.' },
    { t: 'fato', k: 'rep', h: '30/set/1937', p: '“Plano Cohen”: documento forjado (autoria atribuída ao integralista Mourão Filho).' },
    { t: 'cons', k: 'rep', h: '10/nov/1937', p: 'golpe e Estado Novo.' },
  ], { h: true }))}

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Getúlio Vargas — Estado Novo', anos: '1937–1945', sub: '10/nov/1937 → 29/out/1945 · ditadura',
    ficha: {
      chegada: `${chip('golpe')} Golpe de <b>10/nov/1937</b> com apoio da cúpula militar (Góis Monteiro, Dutra); <b>sem eleição</b>.`,
      contexto: 'Ascensão do <b>fascismo</b> na Europa; indústria nascente; <b>II Guerra Mundial</b> (1939–1945) redefine as alianças.',
      termino: `${chip('dep')} <b>29/out/1945:</b> generais, liderados por Góis Monteiro, depõem Vargas, que não resiste.`,
      sucessao: '<b>José Linhares</b> (STF) assume em 30/out; eleição em <b>2/dez/1945</b>: Dutra vence (p. 04).',
    },
  })}

<div class="row r2-53">
  ${sec('3 · Medidas do Estado Novo', 'inst', med([
    ['Instituições', 'inst', '<b>Constituição de 1937 (“Polaca”)</b>: Executivo forte, Congresso e partidos extintos; <b>DASP</b> (1938) cria o concurso público.'],
    ['Repressão', 'rep', '<b>DIP</b> (1939): censura e propaganda do “pai dos pobres”; polícia política de Filinto Müller; Tribunal de Segurança Nacional.'],
    ['Trabalhismo', 'soc', 'Salário mínimo (1940), imposto sindical (1940), Justiça do Trabalho (1941) e <b>CLT (1º/mai/1943)</b>: direitos concedidos “de cima”, com sindicatos atrelados ao Ministério do Trabalho (<i>peleguismo</i>).'],
    ['Economia', 'eco', 'Substituição de importações: <b>CNP</b> (1938), <b>CSN</b> (1941; Volta Redonda), <b>Vale do Rio Doce</b> (1942) e Fábrica Nacional de Motores (1943).'],
  ]))}
  ${sec('Guerra, democratização e queda', 'int', flow([
    { t: 'causa', k: 'int', h: 'II Guerra', p: 'Brasil declara guerra ao Eixo (ago/1942); a <b>FEB</b> luta na Itália (1944–45).' },
    { t: 'fato', k: 'cris', h: 'Contradição', p: 'ditadura em casa, luta contra o fascismo fora; liberais pedem eleições.' },
    { t: 'fato', k: 'soc', h: '1945', p: 'eleições marcadas, anistia, novos partidos e <b>Queremismo</b>.' },
    { t: 'cons', k: 'cris', h: '29/out', p: 'Benjamin Vargas na polícia do DF dispara a deposição.' },
  ]))}
</div>

${sec('Linha do tempo do Estado Novo', 'gray', tl({
    start: { d: '10/nov/1937', t: 'Golpe e Constituição de 1937' },
    events: [
      { d: '1938', t: 'DASP e CNP', k: 'inst' },
      { d: '1939', t: 'DIP: censura e propaganda', k: 'rep' },
      { d: '1940', t: 'Salário mínimo', k: 'soc' },
      { d: 'ago/1942', t: 'Declaração de guerra ao Eixo', k: 'int' },
      { d: '1/mai/1943', t: 'CLT', k: 'soc' },
      { d: 'jul/1944', t: 'FEB embarca para a Itália', k: 'int' },
    ],
    end: { d: '29/out/1945', t: 'Vargas deposto' },
  }))}

${rev([
    ['Por que o Plano Cohen importa para entender o golpe de 1937?', 'Fabricou uma ameaça comunista iminente e justificou o golpe antes da eleição de 1938.'],
    ['Por que a II Guerra enfraqueceu o Estado Novo?', 'A FEB combatia ditaduras na Europa enquanto o Brasil vivia uma.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Era Vargas); Câmara dos Deputados e Senado (Constituições de 1934 e 1937); Planalto (CLT, Decreto-Lei 5.452/1943).</div>
`;
  return page(3, { per: 'vargas', assunto: 'Governo Constitucional e Estado Novo', intervalo: '1934–1945' }, body);
};
