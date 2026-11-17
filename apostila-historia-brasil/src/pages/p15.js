module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const node = (k, t, txt) => `<div class="ob fill k-c-${k}" style="--c:var(--${k})"><b class="t">${t}</b>${txt}</div>`;
  const body = `
<div class="ptitle"><h1>Junta Militar de 1969, aparelho repressivo e censura</h1><span class="per">1969–1974</span></div>

${succ({
    title: 'Mapa da sucessão de 1969', tag: 'golpe dentro da ditadura',
    nodes: [
      { n: 'Costa e Silva', s: 'até 31/ago/1969 (AVC)' },
      { n: 'Junta Militar', s: '31/ago → 30/out/1969', c: 'junta' },
      { n: 'Emílio G. Médici', s: 'posse em 30/out/1969', c: 'now' },
    ],
    steps: [
      ['junta', '<b>31/ago/1969.</b> Impedido por doença, Costa e Silva é afastado. A Constituição (1967) mandava assumir o <b>vice, Pedro Aleixo</b>, civil e contrário ao AI-5; os ministros militares o <b>impedem</b> e assumem como Junta (AI-12).'],
      ['ind', '<b>7/out:</b> o Alto Comando das Forças Armadas escolhe <b>Médici</b>. <b>25/out:</b> o Congresso, reaberto para isso, “elege-o” (293 votos; 76 abstenções do MDB). Posse em 30/out; a Emenda nº 1 (17/out) já reformara a Constituição.'],
    ], one: true,
  })}

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Junta Militar de 1969', anos: '1969', sub: '31/ago → 30/out/1969 (2 meses)',
    ficha: {
      chegada: `${chip('junta')} Aurélio de Lyra Tavares (Exército), Augusto Rademaker (Marinha) e Márcio de Souza e Mello (Aeronáutica) assumem <b>sem eleição</b>, após vetarem a posse de Pedro Aleixo.`,
      contexto: '<b>AI-5</b> em vigor; Congresso fechado; luta armada urbana em ascensão; Costa e Silva incapacitado.',
      termino: 'Cumpre o papel de transição interna: escolhe o general Médici e reabre o Congresso só para referendá-lo.',
      sucessao: `${chip('ind')} <b>Médici</b>, “eleito” pelo Congresso em 25/out/1969, toma posse em 30/out.`,
    },
  })}

<div class="row r2-53">
  ${sec('Medidas da Junta (Atos Institucionais)', 'rep', ul([
    '<b>AI-12</b>: legitima a Junta no lugar do presidente doente; <b>AI-13</b>: banimento; <b>AI-14</b>: pena de morte e prisão perpétua para “guerra revolucionária”.',
    'Nova <b>Lei de Segurança Nacional</b> (set/1969) e <b>Emenda Constitucional nº 1</b> (out/1969), que reforma a Constituição.',
    '<b>Sequestro do embaixador dos EUA</b>, Charles Elbrick (4/set), por MR-8 e ALN: libertado em troca de 15 presos políticos, banidos do país.',
  ], 'rep'))}
  ${call('rep', 'Atenção', 'Esta é uma <b>mudança de governo dentro do próprio regime</b>: um “golpe” interno, não uma eleição nem uma sucessão constitucional. O vice civil foi afastado por vontade das Forças Armadas.')}
</div>

${sec('Como funcionava o aparelho repressivo', 'rep', `<div class="row r3" style="gap:1.8mm">
  ${node('inst', 'Informação', '<b>SNI</b> (1964) e serviços de informação das Forças: CIE (Exército), CENIMAR (Marinha), CISA (Aeronáutica); assessorias de segurança (ASI) em órgãos públicos e universidades.')}
  ${node('rep', 'Operação', '<b>OBAN</b> (1969, SP), origem do <b>DOI-CODI</b> (1970): centros do Exército que prendiam e interrogavam; <b>DOPS</b>: polícias políticas estaduais.')}
  ${node('rep', 'Justiça e leis', '<b>Lei de Segurança Nacional</b>, Justiça Militar para civis e AI-5 (sem habeas corpus em crimes políticos).')}
</div>
<div class="small mute" style="margin-top:1.4mm">Base ideológica: <b>Doutrina de Segurança Nacional</b> (ESG), que via o “inimigo interno”.</div>`)}

${sec('Censura e controle das ideias', 'rep', med([
    ['Imprensa', 'rep', '<b>Censura prévia</b> com censores nas redações; jornais publicaram <b>receitas de bolo e poemas</b> no lugar de matérias vetadas (O Estado de S. Paulo, Jornal da Tarde).'],
    ['Cultura', 'rep', '<b>DCDP</b> (Polícia Federal) censura músicas, peças, filmes e TV; o Decreto-lei 1.077 (1970) estende a censura prévia a livros e revistas “contrários à moral e aos bons costumes”.'],
    ['Propaganda', 'cris', '<b>AERP</b> (Assessoria de Relações Públicas): campanhas ufanistas, como “Brasil, ame-o ou deixe-o” (p. 16).'],
  ]))}

${rev([
    ['Por que Pedro Aleixo foi impedido de assumir em 1969?', 'Era civil e se opusera ao AI-5; os ministros militares não aceitaram a volta de um civil e preferiram uma Junta, que escolheu Médici.'],
    ['Como a censura e o aparelho repressivo se complementavam?', 'O SNI e os serviços de informação identificavam “subversivos”; DOI-CODI e DOPS prendiam e interrogavam; a censura impedia a divulgação dos fatos.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Junta Militar de 1969; SNI; DOI-CODI); Câmara dos Deputados e Planalto (AI-12 a AI-14; Emenda nº 1/1969); Arquivo Nacional (acervos do SNI e da censura); Comissão Nacional da Verdade (2014).</div>
`;
  return page(15, { per: 'dit', assunto: 'Junta Militar de 1969, repressão e censura', intervalo: '1969' }, body);
};
