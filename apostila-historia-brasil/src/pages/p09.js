module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, hbars } = H;
  const body = `
${gov({
    nome: 'Jânio Quadros', anos: '1961', sub: 'PTN, apoio da UDN · 31/01/1961 → 25/08/1961 (7 meses)', foto: 'janio',
    ficha: {
      chegada: `${chip('dir')} Eleição de <b>3/out/1960</b>: Jânio 48,3% × Lott 32,9% × Adhemar de Barros 18,8%. Campanha moralista, com a <b>vassoura</b> como símbolo. O vice, <b>Jango</b>, foi eleito em voto separado (41,6%). Posse em Brasília.`,
      contexto: 'Inflação de <b>30,5%</b> (1960), déficit público e dívida externa herdados da industrialização acelerada; <b>Guerra Fria</b> e Revolução Cubana (1959) polarizam o continente; Jânio não tinha maioria no Congresso (PSD e PTB).',
      termino: `${chip('ren')} <b>25/ago/1961:</b> envia carta de renúncia ao Congresso, alegando “forças terríveis”; o Congresso a aceita sem debate. Jânio deixa o país.`,
      sucessao: `<b>Ranieri Mazzilli</b>, presidente da Câmara, assume <b>interinamente</b> (25/ago). Os ministros militares vetam a posse do vice, Jango, que estava na China: crise sucessória (p. 10).`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Principais medidas e acontecimentos', 'inst', med([
    ['Economia', 'eco', '<b>Austeridade</b> alinhada ao FMI: Instrução 204 da SUMOC (mar/1961) unifica o câmbio e elimina subsídios ao trigo e ao petróleo, encarecendo pão e gasolina; corte de gastos e crédito; renegociação da dívida externa.'],
    ['Moralismo', 'inst', 'Combate a privilégios e “corrupção”; “bilhetinhos” a ministros; proíbe rinhas de galo, corridas de cavalos em dias úteis, biquínis em concursos e lança-perfume.'],
    ['Política externa', 'int', '<b>Política Externa Independente (PEI)</b>: comércio com todos os blocos, apoio à autodeterminação de Cuba, recusa do alinhamento automático aos EUA; condecora <b>Che Guevara</b> com a Ordem do Cruzeiro do Sul (19/ago/1961).'],
  ]))}
  <div class="col">
    ${sec('PEI: iniciativa ≠ relação formalizada', 'int', `<table class="t int">
      <tr><th>País</th><th>O que ocorreu</th></tr>
      <tr><td class="k">URSS</td><td>Jânio planejou reatar; relações restabelecidas só em <b>nov/1961</b>, no governo Goulart</td></tr>
      <tr><td class="k">China (RPC)</td><td>Missão comercial de Jango (ago/1961); relações formais só em <b>1974</b> (Geisel)</td></tr>
      <tr><td class="k">Cuba</td><td>Defesa da autodeterminação e condenação da invasão da Baía dos Porcos</td></tr>
    </table>`)}
  </div>
</div>

${sec('4 · Crise e renúncia', 'cris', flow([
    { t: 'causa', k: 'eco', h: 'Impopularidade', p: 'arrocho e encarecimento do pão e da gasolina atingem trabalhadores e classe média.' },
    { t: 'causa', k: 'int', h: 'PEI e Che Guevara', p: 'a condecoração irrita Forças Armadas, Igreja e UDN.' },
    { t: 'fato', k: 'cris', h: '24/ago', p: 'Lacerda denuncia na TV e no rádio um suposto plano de golpe de Jânio.' },
    { t: 'cons', k: 'cris', h: '25/ago', p: 'Jânio renuncia; Mazzilli assume interinamente.' },
  ], { h: true }))}

<div class="row r2">
  ${call('cris', 'Por que Jânio renunciou? Hipóteses', '<b>Não há prova documental conclusiva.</b> A interpretação mais citada é uma <b>manobra política</b>: renunciar esperando que Congresso, militares e povo recusassem a renúncia, devolvendo-lhe poderes ampliados. Outras leituras apontam <b>isolamento político</b> (sem base no Congresso) e pressões militares. É <u>hipótese historiográfica</u>, não fato estabelecido; o certo é que a renúncia foi aceita e Jânio não voltou.')}
  <div class="col">
    ${chart('Eleição presidencial de 3/out/1960', 'votos válidos (%) — TSE', hbars([['Jânio Quadros', 48.26, '#1e3a5f'], ['Henrique Lott', 32.94, '#7d8da3'], ['Adhemar de Barros', 18.8, '#b7c1ce']], { max: 55 }))}
  </div>
</div>

${sec('Linha do tempo do governo Jânio', 'gray', tl({
    start: { d: '31/jan/1961', t: 'Posse em Brasília' },
    events: [
      { d: '13/mar', t: 'Instrução 204: câmbio unificado, subsídios cortados', k: 'eco' },
      { d: '17–19/abr', t: 'Invasão da Baía dos Porcos (Cuba) condenada', k: 'int' },
      { d: '19/ago', t: 'Condecoração de Che Guevara', k: 'int' },
      { d: '24/ago', t: 'Lacerda denuncia “golpe”', k: 'cris' },
    ],
    end: { d: '25/ago/1961', t: 'Renúncia' },
  }))}

${succ({
    title: 'Mapa da sucessão de 1961 (detalhes na p. 10)', tag: 'renúncia → interinidade', one: true,
    nodes: [{ n: 'Jânio Quadros', s: '31/jan → 25/ago/1961' }, { n: 'Ranieri Mazzilli', s: 'pres. da Câmara · interino', c: 'interim' }, { n: 'João Goulart', s: 'vice · posse 7/set/1961', c: 'now' }],
    steps: [
      ['ren', '<b>25/ago/1961.</b> Jânio renuncia; <b>Mazzilli</b> assume interinamente, mas o poder efetivo está com os ministros militares.'],
      ['const', '<b>7/set/1961.</b> Posse de Jango como presidente, <b>sob parlamentarismo</b>, após o veto militar ser derrotado.'],
    ],
  })}

${rev([
    ['Quais as principais medidas de Jânio e por que o governo se desgastou?', 'Austeridade (câmbio unificado, fim de subsídios), moralismo e política externa independente; desagradaram trabalhadores, elites e militares, e ele não tinha maioria no Congresso.'],
    ['O Brasil reatou relações com a URSS sob Jânio?', 'Não. A iniciativa foi dele, mas o restabelecimento ocorreu em nov/1961, no governo Goulart; com a China, só em 1974.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (verbete Jânio Quadros; Renúncia de 1961); Senado Federal; TSE (eleição de 1960); Ministério das Relações Exteriores (histórico de relações diplomáticas).</div>
`;
  return page(9, { per: 'r46', assunto: 'Governo Jânio Quadros', intervalo: '1961' }, body);
};
