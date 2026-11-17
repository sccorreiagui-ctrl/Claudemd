module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, photo } = H;
  const body = `
${gov({
    nome: 'Artur da Costa e Silva', anos: '1967–1969', sub: 'ARENA · 15/03/1967 → 31/08/1969 (afastado)', foto: 'costaesilva',
    ficha: {
      chegada: `${chip('ind')} Marechal da <b>linha dura</b>, candidato único da ARENA, <b>eleito pelo Congresso em 3/out/1966</b>; assume em 15/mar/1967 com a Constituição de 1967.`,
      contexto: 'Regime consolidado, mas contestado: <b>arrocho salarial</b>, juventude e operários mobilizados; <b>1968</b> é um ano de protestos pelo mundo (Maio de 68, Vietnã); economia em recuperação sob Delfim Netto.',
      termino: `${chip('junta', 'Impedimento')} Em 27/ago/1969 sofre uma trombose cerebral; em 31/ago os três ministros militares assumem como <b>Junta</b>, impedindo a posse do vice civil, Pedro Aleixo (p. 15).`,
      sucessao: 'A Junta Militar governa até 30/out/1969, quando <b>Médici</b> é escolhido pela cúpula militar e referendado pelo Congresso (p. 15).',
    },
  })}

<div class="row r2">
  ${sec('3 · Medidas e acontecimentos', 'eco', ul([
    '<b>Delfim Netto</b> na Fazenda: crédito farto e incentivo à indústria; início do <b>“Milagre”</b> (PIB: 9,8% em 1968 e 9,5% em 1969; p. 17).',
    '<b>Frente Ampla</b> (Lacerda, JK e Jango) proibida em abr/1968.',
    '<b>Movimento estudantil e operário</b> em 1968: greves de Contagem (abr) e Osasco (jul), repressão e prisões.',
    'Cria o <b>MOBRAL</b> (1967), de alfabetização de adultos.',
  ], 'eco'))}
  ${sec('4 · O ano de 1968: protesto e repressão', 'rep', flow([
    { t: 'causa', k: 'soc', h: '28/mar', p: 'a PM mata o estudante Edson Luís no restaurante Calabouço (RJ); protestos em todo o país.' },
    { t: 'fato', k: 'soc', h: '26/jun', p: '<b>Passeata dos Cem Mil</b> no Rio contra a ditadura, após a “Sexta-feira Sangrenta” (21/jun).' },
    { t: 'fato', k: 'rep', h: '12/out', p: 'a polícia prende centenas de estudantes no congresso clandestino da UNE, em Ibiúna (SP).' },
  ]))}
</div>

${sec('O caminho até o AI-5', 'cris', flow([
    { t: 'causa', k: 'rep', h: 'Linha dura', p: 'quer fechar o regime e reprimir a oposição e a luta armada que começa.' },
    { t: 'fato', k: 'cris', h: '2/set', p: 'O deputado Márcio Moreira Alves critica a violência militar e sugere boicote aos desfiles do 7 de Setembro.' },
    { t: 'fato', k: 'cris', h: '12/dez', p: 'A Câmara nega licença para processá-lo (216 × 141).' },
    { t: 'cons', k: 'rep', h: '13/dez/1968', p: '<b>AI-5</b> e recesso do Congresso.' },
  ], { h: true }))}

${sec('AI-5 (13/dez/1968): como alterou o regime', 'rep', `<table class="t rep">
  <tr><th>Poder do governo</th><th>O que significava</th></tr>
  <tr><td class="k">Recesso do Congresso</td><td>O presidente podia fechar Câmara, Senado e assembleias (o Congresso ficou fechado até out/1969) e legislar por decreto</td></tr>
  <tr><td class="k">Cassações</td><td>Cassar mandatos e suspender direitos políticos por 10 anos, sem controle judicial</td></tr>
  <tr><td class="k">Habeas corpus</td><td><b>Suspenso</b> em crimes políticos e contra a segurança nacional: prisões sem controle da Justiça. A tortura <b>não foi legalizada</b> pelo ato, mas a ausência de controle judicial favoreceu sua prática</td></tr>
  <tr><td class="k">Intervenção e censura</td><td>Intervenção em estados e municípios; <b>censura prévia</b> a imprensa, música, teatro e cinema</td></tr>
</table>`)}

${(() => { const ph = photo('passeata', { h: 42, cap: '<b>Protesto estudantil contra a ditadura</b>, Rio de Janeiro, 1968 (acervo Correio da Manhã).' }); return ph ? `<div class="row r2-12">${ph}${call('soc', 'Passeata dos Cem Mil (26/jun/1968)', 'Manifestação no Rio de Janeiro, após a “Sexta-feira Sangrenta”, reuniu estudantes, artistas, intelectuais, religiosos e mães: foi o auge da mobilização civil contra a ditadura antes do AI-5. Seis meses depois, o regime fechou os canais legais de protesto.')}</div>` : ''; })()}

${sec('Linha do tempo do governo Costa e Silva', 'gray', tl({
    start: { d: '15/mar/1967', t: 'Posse; Constituição de 1967 em vigor' },
    events: [
      { d: '28/mar/1968', t: 'Morte de Edson Luís', k: 'cris' },
      { d: 'abr/1968', t: 'Frente Ampla proibida; greve de Contagem', k: 'rep' },
      { d: '26/jun/1968', t: 'Passeata dos Cem Mil', k: 'soc' },
      { d: '12/out/1968', t: 'UNE presa em Ibiúna', k: 'rep' },
      { d: '13/dez/1968', t: 'AI-5; Congresso fechado', k: 'rep' },
    ],
    end: { d: '31/ago/1969', t: 'Afastamento; Junta Militar' },
  }))}

${rev([
    ['Como o AI-5 alterou o regime político?', 'Deu ao Executivo poderes ilimitados: fechar o Congresso, cassar, intervir, censurar e suspender o habeas corpus em crimes políticos, abrindo a fase mais repressiva da ditadura.'],
    ['Por que o discurso de Márcio Moreira Alves foi o estopim?', 'A Câmara recusou licença para processá-lo; os militares da linha dura usaram o episódio como pretexto para fechar o regime.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Costa e Silva; Atos Institucionais); Câmara dos Deputados (AI-5; votação de 12/dez/1968); Arquivo Nacional; Comissão Nacional da Verdade (2014).</div>
`;
  return page(14, { per: 'dit', assunto: 'Governo Costa e Silva, 1968 e AI-5', intervalo: '1967–1969' }, body);
};
