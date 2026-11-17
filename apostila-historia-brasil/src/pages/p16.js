module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const body = `
${gov({
    nome: 'Emílio Garrastazu Médici', anos: '1969–1974', sub: 'ARENA · 30/10/1969 → 15/03/1974', foto: 'medici',
    ficha: {
      chegada: `${chip('ind')} Escolhido pelo Alto Comando militar; “eleito” pelo Congresso reaberto em 25/out/1969 (293 votos; abstenção do MDB); posse em 30/out/1969.`,
      contexto: '<b>AI-5</b> em vigor; luta armada urbana; economia em expansão (início do “Milagre”, p. 17) e clima de otimismo alimentado pela propaganda.',
      termino: 'Mandato de 4 anos e 4 meses encerrado em 15/mar/1974, no auge da popularidade oficial, mas com a repressão acusada de milhares de violações.',
      sucessao: `${chip('ind')} <b>Ernesto Geisel</b>, eleito pelo Colégio Eleitoral em 15/jan/1974 (400 votos × 76 em Ulysses Guimarães, “anticandidato” do MDB). Posse em 15/mar.`,
    },
  })}

<div class="row r2">
  ${sec('3 · “Anos de Chumbo”: repressão sistemática', 'rep', ul([
    '<b>DOI-CODI</b> e <b>DOPS</b> prendem, torturam e executam opositores; surgem os <b>desaparecidos políticos</b>.',
    'A Comissão Nacional da Verdade (2014) reconheceu <b>434 mortos e desaparecidos</b> políticos entre 1946 e 1988; a maioria sob a ditadura, concentrada nos anos 1969–1976.',
    'Censura prévia e <b>exílio</b> de artistas e políticos.',
  ], 'rep'))}
  ${sec('Propaganda e ufanismo', 'cris', ul([
    '<b>AERP</b>: slogans como “Brasil, ame-o ou deixe-o”, “Pra frente, Brasil” e “Ninguém segura este país”.',
    '<b>Copa de 1970</b>: o tricampeonato foi explorado politicamente pelo governo.',
    '<b>Integração nacional</b>: Transamazônica e PIN (1970); MOBRAL; Funrural (1971); mar territorial de 200 milhas (1970).',
  ], 'cris'))}
</div>

<div class="row r2-12">
  ${sec('Luta armada e repressão', 'rep', flow([
    { t: 'causa', k: 'rep', h: 'AI-5', p: 'fecha os canais legais de oposição.' },
    { t: 'fato', k: 'cris', h: 'Luta armada', p: 'ALN (Marighella, morto em 4/nov/1969), VPR e MR-8 (Lamarca, morto em 1971) assaltam bancos e sequestram diplomatas.' },
    { t: 'fato', k: 'rep', h: 'Resposta', p: 'DOI-CODI, tortura e execuções.' },
    { t: 'cons', k: 'rep', h: '1972–74', p: 'organizações urbanas desarticuladas; Araguaia é o último foco.' },
  ]))}
  <div class="col">
    ${sec('Oposição e resistência', 'soc', ul([
    '<b>Guerrilha do Araguaia</b> (1972–1975): o PCdoB instala um foco rural no sul do Pará; o Exército o destrói em três campanhas, com execuções de militantes.',
    '<b>Resistência cultural</b>: Tropicália e MPB de protesto (Chico Buarque, Caetano, Gil, exilados em 1969–70), Cinema Novo, teatro e o jornal <i>O Pasquim</i> (1969).',
    '<b>Igreja</b> (Dom Paulo Evaristo Arns, Dom Hélder Câmara) e advogados denunciam torturas; <b>MDB</b> cresce com votos de protesto (eleições de 1970: votos nulos e brancos em alta).',
  ], 'soc'))}
  </div>
</div>

${sec('Propaganda × realidade', 'cris', `<table class="t cris">
  <tr><th>O que o governo dizia</th><th>O que mostram os dados e a pesquisa histórica</th></tr>
  <tr><td>“Ninguém segura este país”: o Brasil do “Milagre”</td><td>PIB de 10,4% a 14,0% ao ano (1970–73), mas concentração de renda (Gini ≈ 0,50 → 0,56) e arrocho salarial (p. 17)</td></tr>
  <tr><td>“Brasil, ame-o ou deixe-o”: ordem e segurança</td><td>CNV: 434 mortos e desaparecidos políticos (1946–1988), sendo 210 desaparecidos; censura e exílio</td></tr>
</table>`)}

${call('int', 'Contexto internacional', '<b>Guerra Fria</b>: o regime se dizia bastião anticomunista; o crédito internacional farto financiou o crescimento e preparou o endividamento revelado após o choque do petróleo de 1973 (p. 17–18).')}

${sec('Linha do tempo do governo Médici', 'gray', tl({
    start: { d: '30/out/1969', t: 'Posse; Congresso reaberto' },
    events: [
      { d: '4/nov/1969', t: 'Marighella morto em São Paulo', k: 'rep' },
      { d: '1970', t: 'DOI-CODI; Copa do México; Transamazônica', k: 'cris' },
      { d: '1971', t: 'Lamarca morto; Funrural', k: 'rep' },
      { d: 'abr/1972', t: 'Início da Guerrilha do Araguaia', k: 'rep' },
      { d: '1973', t: 'Anticandidatura de Ulysses; choque do petróleo', k: 'soc' },
    ],
    end: { d: '15/mar/1974', t: 'Posse de Geisel' },
  }))}

${rev([
    ['Por que o governo Médici ficou conhecido como “Anos de Chumbo”?', 'Pela repressão sistemática (tortura, mortes e desaparecimentos) sob o AI-5, combinada com censura e propaganda ufanista.'],
    ['Como o regime tratou a luta armada e a oposição?', 'Reprimiu as organizações armadas com o aparato DOI-CODI/DOPS e desarticulou-as; ao mesmo tempo, a resistência cultural, religiosa e eleitoral (MDB) cresceu.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Médici; Guerrilha do Araguaia); Comissão Nacional da Verdade, Relatório Final (2014); Arquivo Nacional; Câmara dos Deputados.</div>
`;
  return page(16, { per: 'dit', assunto: 'Governo Médici', intervalo: '1969–1974' }, body);
};
