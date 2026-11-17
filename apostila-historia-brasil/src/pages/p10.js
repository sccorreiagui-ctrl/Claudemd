module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const body = `
<div class="ptitle"><h1>Crise sucessória de 1961: Mazzilli, Legalidade e parlamentarismo</h1><span class="per">ago–set/1961</span></div>

${succ({
    title: 'Mapa da sucessão de 1961', tag: 'renúncia → veto militar → solução de compromisso',
    nodes: [
      { n: 'Jânio Quadros', s: 'renuncia em 25/ago/1961' },
      { n: 'Ranieri Mazzilli', s: 'pres. da Câmara · 25/ago → 7/set/1961', c: 'interim' },
      { n: 'João Goulart (Jango)', s: 'vice · posse em 7/set/1961', c: 'now' },
    ],
    steps: [
      ['ren', '<b>25/ago/1961.</b> A renúncia vai ao Congresso; assume <b>Ranieri Mazzilli</b>, presidente da Câmara, por sucessão constitucional <u>interina</u> (o vice estava na China).'],
      ['golpe', '<b>Veto militar:</b> os ministros Odílio Denys (Guerra), Sílvio Heck (Marinha) e Gabriel Grün Moss (Aeronáutica) declaram inconveniente a volta de Jango. Para muitos historiadores, foi tentativa de golpe.'],
      ['const', '<b>7/set/1961.</b> Após a Legalidade e a <b>Emenda Constitucional nº 4</b> (2/set), Jango toma posse como presidente, <b>com poderes reduzidos</b> (parlamentarismo).'],
    ], one: true,
  })}

${gov({
    kick: 'Governo interino', compact: true, c4: true, nome: 'Ranieri Mazzilli', anos: '1961', sub: '25/ago → 7/set/1961 (13 dias)',
    ficha: {
      chegada: `${chip('const', 'Sucessão constitucional')} Presidente da Câmara (PSD), assume na vacância; <b>não foi eleito</b> para a Presidência.`,
      contexto: 'Presidência vaga; vice no exterior; ministros militares vetam a posse de Jango e o Brasil flerta com a <b>guerra civil</b>.',
      termino: 'Sem poder real (decisões nos ministérios militares), transmite o cargo a Jango em 7/set/1961.',
      sucessao: `${chip('const', 'Posse de Jango')} sob parlamentarismo, após acordo no Congresso.`,
    },
  })}

<div class="row r2-53">
  ${sec('Como a crise se resolveu: causas, fatos e consequências', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Veto militar', p: 'Jango era visto por militares e UDN como esquerdista ligado ao trabalhismo e à China comunista.' },
    { t: 'fato', k: 'soc', h: '27/ago: Cadeia da Legalidade', p: 'Brizola, governador do RS, mobiliza rádios e povo e defende a Constituição.' },
    { t: 'fato', k: 'cris', h: '28/ago', p: 'O general Machado Lopes (III Exército) adere à Legalidade: risco de guerra civil.' },
    { t: 'fato', k: 'inst', h: '2/set', p: 'Congresso aprova a <b>EC nº 4</b>: parlamentarismo como solução de compromisso (Tancredo negocia com Jango).' },
    { t: 'cons', k: 'inst', h: '7/set', p: 'Jango assume: o Brasil evita o golpe, mas fica com um presidente de poderes limitados.' },
  ]))}
  <div class="col">
    ${sec('Presidencialismo × parlamentarismo (1961)', 'inst', `<table class="t">
      <tr><th></th><th>Antes</th><th>Depois (EC 4)</th></tr>
      <tr><td class="k">Chefe de Estado</td><td>Presidente</td><td>Presidente (Jango)</td></tr>
      <tr><td class="k">Chefe de governo</td><td>Presidente</td><td>Primeiro-ministro</td></tr>
      <tr><td class="k">Responsabilidade</td><td>Perante o eleitor</td><td>Perante a Câmara (pode derrubar o gabinete)</td></tr>
    </table>`)}
    ${call('', 'Primeiros-ministros', '<b>Tancredo Neves</b> (set/1961) → <b>Brochado da Rocha</b> (jul/1962) → <b>Hermes Lima</b> (set/1962). Instável: três gabinetes em 16 meses.')}
  </div>
</div>

${sec('Linha do tempo da crise', 'gray', tl({
    start: { d: '25/ago/1961', t: 'Jânio renuncia; Mazzilli assume' },
    events: [
      { d: '25–28/ago', t: 'Veto dos ministros militares', k: 'rep' },
      { d: '27/ago', t: 'Cadeia da Legalidade (Brizola)', k: 'soc' },
      { d: '28/ago', t: 'III Exército adere à Legalidade', k: 'soc' },
      { d: '2/set', t: 'Emenda do parlamentarismo (EC nº 4)', k: 'inst' },
    ],
    end: { d: '7/set/1961', t: 'Posse de Jango' },
  }))}

${sec('Duas crises sucessórias comparadas: 1955 × 1961', 'cris', `<table class="t cris">
  <tr><th></th><th>1955 (JK e Jango)</th><th>1961 (Jango)</th></tr>
  <tr><td class="k">Origem</td><td>Eleição contestada pela UDN e por setores militares</td><td>Renúncia inesperada de Jânio e veto à posse do vice</td></tr>
  <tr><td class="k">Quem tentou impedir a posse</td><td>Carlos Luz e conspiradores civis e militares</td><td>Ministros militares (Denys, Heck, Grün Moss)</td></tr>
  <tr><td class="k">Papel das Forças Armadas</td><td>Divididas: Lott age pela posse</td><td>Divididas: o III Exército adere à Legalidade</td></tr>
  <tr><td class="k">Solução</td><td>Impedimento de Luz e estado de sítio</td><td>Emenda parlamentarista (EC nº 4)</td></tr>
  <tr><td class="k">Resultado</td><td>JK toma posse com poderes plenos</td><td>Jango toma posse com poderes reduzidos</td></tr>
</table>`)}

<div class="row r2">
  ${call('rep', 'Por que isso importa para 1964?', 'Em 1961 a <b>legalidade venceu</b>, mas os militares aprenderam que podiam <b>vetar</b> um presidente civil e Jango foi enfraquecido desde o início. A crise é chamada por historiadores de “ensaio geral” do golpe de 1964; a solução parlamentarista tampouco apaziguou o país.')}
  ${rev([
    ['Por que Jango assumiu inicialmente sob parlamentarismo?', 'Para superar o veto militar e evitar a guerra civil: o Congresso aprovou a EC nº 4, mantendo Jango na Presidência, mas com poderes limitados ao Primeiro-Ministro.'],
    ['Qual foi o papel da Campanha da Legalidade?', 'Mobilizou povo, rádios, Brigada Militar e o III Exército em defesa da posse constitucional, tornando o veto insustentável.'],
  ])}
</div>
<div class="src">Fontes: CPDOC/FGV (verbetes Ranieri Mazzilli, Jango, Legalidade); Câmara dos Deputados (Emenda Constitucional nº 4/1961); Senado Federal. O projeto de “Operação Mosquito” (abater o avião de Jango) é relatado por testemunhos e não é consenso historiográfico, por isso não consta.</div>
`;
  return page(10, { per: 'r46', assunto: 'Crise sucessória de 1961 e parlamentarismo', intervalo: '1961' }, body);
};
