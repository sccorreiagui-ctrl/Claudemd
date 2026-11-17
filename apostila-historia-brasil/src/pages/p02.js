module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, flowLegend, tl, rev, chip } = H;
  const body = `
<div class="ptitle"><h1>Crise de 1929, Revolução de 1930 e Governo Provisório</h1><span class="per">1929–1934</span></div>

<div class="row r2">
  ${sec('Por que a crise de 1929 atingiu o Brasil?', 'int', flow([
    { t: 'causa', k: 'int', h: 'Quebra da Bolsa de Nova York (out/1929)', p: 'superprodução, crédito em colapso e queda do consumo nos EUA e na Europa.' },
    { t: 'fato', k: 'eco', h: 'Café em queda', p: 'principal produto de exportação (cerca de 70% do valor nos anos 1920): preço e vendas despencam.' },
    { t: 'fato', k: 'eco', h: 'Fim da sustentação artificial', p: 'o esquema de “valorização” (Convênio de Taubaté, 1906) dependia de crédito externo e de comprar estoques.' },
    { t: 'cons', k: 'cris', h: 'Crise cafeeira', p: 'cafeicultores endividados e Estado sem divisas: a base econômica da oligarquia paulista se enfraquece.' },
  ]))}
  <div class="col">
    ${sec('Por que ocorreu a Revolução de 1930? (várias causas)', 'cris', ul([
    '<b>Política:</b> Washington Luís (SP) rompe o revezamento do <i>café com leite</i> ao indicar o paulista <b>Júlio Prestes</b> em vez de um mineiro.',
    '<b>Econômica:</b> crise do café e da oligarquia paulista.',
    '<b>Social:</b> classes médias urbanas e <b>tenentes</b> querem voto secreto, justiça eleitoral e reformas.',
    '<b>Eleitoral:</b> eleição de <b>1/mar/1930</b> (Prestes 57,7% × Vargas 39,3%), com denúncias de fraude.',
    '<b>Estopim:</b> assassinato de <b>João Pessoa</b> (26/jul/1930), candidato a vice da Aliança Liberal.',
  ], 'cris'))}
    <div class="row r2" style="gap:1.6mm">
      <div class="ob k-c-rep fill" style="--c:var(--rep)"><b class="t">Situação</b>Washington Luís e o PRP; presidentes de estado aliados; candidato: <b>Júlio Prestes</b>.</div>
      <div class="ob k-c-soc fill" style="--c:var(--soc)"><b class="t">Aliança Liberal</b>RS, MG e PB; <b>Vargas</b> e João Pessoa; tenentes e classes médias.</div>
    </div>
  </div>
</div>

${gov({
    kick: 'Governo', compact: true, nome: 'Getúlio Vargas — Governo Provisório', anos: '1930–1934', sub: '3/nov/1930 → jul/1934 · sem eleição presidencial',
    ficha: {
      chegada: `${chip('golpe', 'Revolução / ruptura armada')} Levante de <b>3/out/1930</b>; em <b>24/out</b> o Alto Comando militar depõe Washington Luís; a Junta (Tasso Fragoso, Mena Barreto, Isaías de Noronha) entrega o poder a Vargas em <b>3/nov/1930</b>.`,
      contexto: 'Economia abalada pela crise do café; <b>Constituição de 1891</b> ainda formal; oligarquias estaduais fortes; tenentes pressionando; desconfiança entre regiões, sobretudo de São Paulo.',
      termino: 'A Assembleia Constituinte promulga a <b>Constituição de 16/jul/1934</b>; o Governo Provisório se encerra com a eleição do presidente.',
      sucessao: `${chip('ind')} <b>17/jul/1934:</b> a própria Constituinte elege Vargas para o mandato constitucional (até 1938): início do <b>Governo Constitucional</b> (p. 03).`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Principais medidas', 'inst', med([
    ['Política', 'inst', 'Fecha Congresso e assembleias, <b>revoga a Constituição de 1891</b> e governa por decretos; nomeia <b>interventores</b> nos estados (muitos tenentes). <b>Código Eleitoral (fev/1932):</b> voto secreto, <b>voto feminino</b> e Justiça Eleitoral.'],
    ['Trabalho', 'soc', '<b>Ministério do Trabalho, Indústria e Comércio</b> (nov/1930); lei de sindicalização (1931) liga o sindicato único ao Estado; carteira profissional e jornada de 8 horas.'],
    ['Educação e saúde', 'soc', '<b>Ministério da Educação e Saúde Pública</b> (nov/1930); reforma do ensino secundário e superior (Francisco Campos, 1931).'],
    ['Economia', 'eco', '<b>Conselho Nacional do Café</b> (1931): compra e destruição de estoques para sustentar o preço. Começa a industrialização por substituição de importações.'],
  ]))}
  <div class="col">
    ${sec('4 · Crise: Revolução Constitucionalista (1932)', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Perda de poder de SP', p: 'interventores de fora e demora em constitucionalizar o país.' },
    { t: 'fato', k: 'cris', h: '9/jul–2/out/1932', p: 'São Paulo se levanta e é derrotado militarmente.' },
    { t: 'cons', k: 'cris', h: 'Vitória política parcial', p: 'Constituinte em 1933 e interventor civil paulista.' },
  ]))}
  </div>
</div>

${sec('Linha do tempo do Governo Provisório', 'gray', tl({
    start: { d: '3/nov/1930', t: 'Vargas assume o poder' },
    events: [
      { d: '1931', t: 'Conselho Nacional do Café; sindicato atrelado ao Estado', k: 'eco' },
      { d: 'fev/1932', t: 'Código Eleitoral: voto secreto e feminino', k: 'soc' },
      { d: 'jul–out/1932', t: 'Revolução Constitucionalista', k: 'cris' },
      { d: 'mai/1933', t: 'Eleição da Constituinte', k: 'inst' },
      { d: '16/jul/1934', t: 'Constituição promulgada', k: 'inst' },
    ],
    end: { d: '17/jul/1934', t: 'Vargas eleito pela Constituinte' },
  }))}

<div class="row r2-12">
  ${call('int', 'Contexto internacional', 'A <b>Crise de 1929</b> reduz o comércio mundial e leva países a protegerem suas economias. No Brasil, produzir internamente o que não se podia importar estimula a <b>indústria</b>.')}
  ${rev([
    ['Qual a relação entre a crise de 1929 e a Revolução de 1930?', 'A crise enfraqueceu a economia cafeeira e a oligarquia paulista; somada ao racha do café com leite e à eleição contestada, criou condições para a revolução — não foi a causa única.'],
    ['Por que a Revolução de 1932 foi derrotada mas teve efeitos?', 'São Paulo ficou isolado, mas o governo convocou a Constituinte (1933) e nomeou interventor civil paulista.'],
  ])}
</div>
<div class="src">Fontes: CPDOC/FGV (Era Vargas, 1930–1937); Senado Federal e Câmara dos Deputados (Constituição de 1934); TSE (Código Eleitoral de 1932). Valores eleitorais de 1930 conforme CPDOC.</div>
`;
  return page(2, { per: 'vargas', assunto: 'Crise de 1929, Revolução de 1930 e Governo Provisório', intervalo: '1929–1934' }, body);
};
