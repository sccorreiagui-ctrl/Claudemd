module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, vtl, rev, chip, succ, chart, hbars } = H;
  const col = (g, t) => `<div class="col" style="gap:1.6mm">${gov(g)}${vtl(t)}</div>`;
  const body = `
<div class="ptitle"><h1>Suicídio de Vargas e transição 1954–1956</h1><span class="per">1954–1956</span></div>

${succ({
    title: 'Mapa da sucessão: Vargas → Café Filho → Carlos Luz → Nereu Ramos → JK', tag: 'cinco presidentes em 17 meses',
    nodes: [
      { n: 'Vargas', s: 'até 24/ago/1954' },
      { n: 'Café Filho', s: 'vice · 24/ago/54 → 8/nov/55', c: 'interim' },
      { n: 'Carlos Luz', s: 'pres. da Câmara · 8 → 11/nov/55', c: 'interim' },
      { n: 'Nereu Ramos', s: 'pres. do Senado · 11/nov/55 → 31/jan/56', c: 'interim' },
      { n: 'JK', s: 'eleito · 31/jan/1956', c: 'now' },
    ],
    steps: [
      ['morte', '<b>24/ago/1954.</b> Suicídio de Vargas; o vice <b>Café Filho</b> assume por sucessão constitucional.'],
      ['const', '<b>8/nov/1955.</b> Café Filho se licencia por motivo de saúde; assume o presidente da Câmara, <b>Carlos Luz</b>.'],
      ['dep', '<b>11/nov/1955.</b> O Exército, liderado por Lott, ocupa pontos-chave; o Congresso declara o impedimento de Luz e empossa <b>Nereu Ramos</b>. Em 21/nov, Café Filho tenta reassumir e também é impedido.'],
      ['dir', '<b>31/jan/1956.</b> Posse de <b>JK</b> e <b>Jango</b>, eleitos em 3/out/1955 por voto direto, sob estado de sítio.'],
    ],
  })}

<div class="row r3">
  ${col({
    kick: 'Governo', compact: true, c1: true, nome: 'Café Filho', anos: '1954–1955', sub: '24/ago/1954 → 8/nov/1955',
    ficha: {
      chegada: `${chip('const')} Vice-presidente (PSP) eleito em 1950; assume no dia do suicídio de Vargas.`,
      contexto: 'País comovido e polarizado; golpe udenista adiado; inflação em alta.',
      medidas: 'Ministério com UDN e militares antigetulistas; ortodoxia financeira (Gudin); <b>Instrução 113 da SUMOC</b> (jan/1955) facilita a entrada de equipamentos de empresas estrangeiras.',
      crises: 'Eleição de JK; Lacerda e setores militares tentam impedir a posse.',
      termino: 'Licencia-se em 8/nov/1955; é depois impedido de voltar.',
      sucessao: `${chip('const')} Carlos Luz, presidente da Câmara.`,
    },
  }, {
    start: { d: '24/ago/54', t: 'Assume' },
    events: [{ d: 'jan/55', t: 'Instrução 113', k: 'eco' }, { d: '3/out/55', t: 'JK e Jango eleitos', k: 'soc' }, { d: '1/nov/55', t: 'Discurso do cel. Mamede', k: 'cris' }],
    end: { d: '8/nov/55', t: 'Licença por saúde' },
  })}
  ${col({
    kick: 'Governo', compact: true, c1: true, nome: 'Carlos Luz', anos: '1955', sub: '8/nov → 11/nov/1955 (3 dias)',
    ficha: {
      chegada: `${chip('const')} Presidente da Câmara (PSD-MG), substitui o presidente licenciado.`,
      contexto: 'Tensão máxima: legalistas (Lott) × conspiradores contra a posse de JK.',
      medidas: 'Recusa punir o coronel Mamede e aceita a demissão de Lott (10/nov).',
      crises: 'Madrugada de 11/nov: o Exército, sob Lott, assume o controle; Luz, ministros e Lacerda fogem no cruzador <i>Tamandaré</i>.',
      termino: `${chip('dep', 'Impedimento')} Câmara (185×72) e Senado (43×8) votam o impedimento em 11/nov.`,
      sucessao: 'Nereu Ramos, presidente do Senado.',
    },
  }, {
    start: { d: '8/nov', t: 'Luz assume' },
    events: [{ d: '10/nov', t: 'Lott pede demissão', k: 'cris' }, { d: '11/nov', t: 'Exército ocupa pontos-chave; fuga no Tamandaré', k: 'cris' }],
    end: { d: '11/nov', t: 'Impedimento no Congresso' },
  })}
  ${col({
    kick: 'Governo', compact: true, c1: true, nome: 'Nereu Ramos', anos: '1955–1956', sub: '11/nov/1955 → 31/jan/1956',
    ficha: {
      chegada: `${chip('inter')} Presidente do Senado, empossado pelo Congresso após o impedimento de Luz.`,
      contexto: 'Sob tutela militar legalista; Café Filho ainda reivindica o cargo.',
      medidas: '<b>Estado de sítio</b> (24/nov) para garantir a ordem; mantém Lott no Ministério da Guerra.',
      crises: '21/nov: Café Filho anuncia que reassume; Câmara (179×94) e Senado (35×16) declaram o seu impedimento.',
      termino: 'Entrega o cargo em 31/jan/1956, como previsto.',
      sucessao: `${chip('dir')} <b>JK</b> e <b>Jango</b>, eleitos em 3/out/1955.`,
    },
  }, {
    start: { d: '11/nov', t: 'Nereu assume' },
    events: [{ d: '21/nov', t: 'Café Filho tenta voltar; Congresso o impede', k: 'cris' }, { d: '24/nov', t: 'Estado de sítio', k: 'rep' }],
    end: { d: '31/jan/56', t: 'Posse de JK' },
  })}
</div>

${sec('Crise de novembro de 1955: causas, fatos e consequências', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Eleição contestada', p: 'UDN e militares antigetulistas alegam falta de “maioria absoluta”, exigência que a Constituição não fazia.' },
    { t: 'fato', k: 'cris', h: '1/nov', p: 'Cel. Mamede discursa contra a posse no enterro do gen. Canrobert; Lott exige punição.' },
    { t: 'fato', k: 'cris', h: '8–10/nov', p: 'Café Filho se licencia; Luz recusa punir Mamede; Lott se demite.' },
    { t: 'fato', k: 'rep', h: '11/nov', p: '<b>Contragolpe preventivo</b>: Exército ocupa pontos-chave; Congresso depõe Luz.' },
    { t: 'cons', k: 'soc', h: '31/jan/1956', p: 'posse constitucional de JK e Jango.' },
  ], { h: true }))}

<div class="row r2">
  ${chart('Eleição presidencial de 3/out/1955', 'votos válidos (%) — TSE · vice: Jango 44,3% × Milton Campos 41,7%', hbars([['JK (PSD/PTB)', 35.68, '#2a7a4b'], ['Juarez Távora (UDN)', 30.27, '#7d8da3'], ['Adhemar de Barros (PSP)', 25.77, '#9aa8ba'], ['Plínio Salgado (PRP)', 8.28, '#c3ccd8']], { max: 40 }), '<div class="src" style="margin-top:1mm">Maioria simples bastava: JK venceu com 35,7%. O contragolpe é chamado “preventivo” porque se antecipou a uma ruptura que se supunha em curso.</div>')}
  ${rev([
    ['Qual foi o papel de Lott em 1955?', 'Ministro da Guerra, mobilizou o Exército em 11/nov para impedir a conspiração contra a posse de JK e Jango: garantiu a ordem constitucional, mas pela via militar (leitura debatida pelos historiadores).'],
    ['Por que a UDN contestou a eleição de JK?', 'Alegou falta de “maioria absoluta” (a Constituição de 1946 exigia só maioria simples) e apoio comunista.'],
  ])}
</div>
<div class="src">Fontes: CPDOC/FGV (verbetes Café Filho, Carlos Luz, Nereu Ramos, Lott); Câmara dos Deputados; TSE. Placares de 11/nov e 21/nov conforme registro dos Anais.</div>
`;
  return page(7, { per: 'r46', assunto: 'Café Filho, Carlos Luz, Nereu Ramos e o movimento de Lott', intervalo: '1954–1956' }, body);
};
