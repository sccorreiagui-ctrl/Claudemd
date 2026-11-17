module.exports = (H) => {
  const { page, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const box = (k, t, txt) => `<div class="ob fill k-c-${k}" style="--c:var(--${k})"><b class="t">${t}</b>${txt}</div>`;
  const body = `
<div class="ptitle"><h1>Guerra Fria, polarização e o golpe civil-militar de 1964</h1><span class="per">1959–1964</span></div>

<div class="row r2-12">
  ${sec('Do contexto mundial ao Brasil', 'int', flow([
    { t: 'causa', k: 'int', h: 'Guerra Fria', p: 'após a <b>Revolução Cubana</b> (1959) e a crise dos mísseis (1962), os EUA temem “outra Cuba” na América Latina.' },
    { t: 'fato', k: 'int', h: 'Anticomunismo', p: 'Aliança para o Progresso (1961); doutrina de segurança nacional da ESG; apoio a opositores de Jango (IPES/IBAD).' },
    { t: 'fato', k: 'cris', h: 'No Brasil', p: 'Reformas de Base, CGT, Ligas e a política externa independente são lidas como ameaça.' },
    { t: 'cons', k: 'rep', h: 'Coalizão golpista', p: 'civis, militares e apoio externo.' },
  ]))}
  <div class="col">
    <h2>Várias causas, não uma só</h2>
    <div class="row r3" style="gap:1.6mm">
      ${box('eco', 'Econômica', 'Inflação de 79,9% em 1963; PIB de 0,6%; fracasso do Plano Trienal; conflito sobre remessa de lucros.')}
      ${box('inst', 'Política', 'Congresso hostil; polarização e instabilidade desde 1961; reformas por decreto ou plebiscito.')}
      ${box('rep', 'Militar', 'Quebra de hierarquia (sargentos, marinheiros); anticomunismo da ESG; conspiração de oficiais.')}
      ${box('cris', 'Social e ideológica', 'Mobilização de camponeses e operários; medo da “comunização” na classe média, na Igreja e na imprensa.')}
      ${box('eco', 'Empresarial', 'IPES/IBAD financiam campanha contra Jango; empresários temem reformas e sindicatos.')}
      ${box('int', 'Internacional', 'Guerra Fria; embaixada dos EUA acompanha e se prepara para apoiar os golpistas.')}
    </div>
  </div>
</div>

${sec('A escalada de março de 1964', 'cris', tl({
    start: { d: '13/mar', t: 'Comício da Central do Brasil: decretos de reforma (SUPRA, refinarias)', k: 'soc' },
    events: [
      { d: '19/mar', t: 'Marcha da Família com Deus pela Liberdade (SP)', k: 'rep' },
      { d: '25–26/mar', t: 'Revolta dos marinheiros (RJ)', k: 'cris' },
      { d: '30/mar', t: 'Jango fala a sargentos no Automóvel Clube', k: 'cris' },
      { d: '31/mar', t: 'Mourão Filho parte de Juiz de Fora (MG) rumo ao Rio', k: 'rep' },
      { d: '1/abr', t: 'Jango deixa o Rio; tropas aderem', k: 'cris' },
    ],
    end: { d: '2/abr', t: 'Presidência declarada vaga', k: 'rep' },
  }))}

<div class="row r2">
  ${call('int', 'Operação Brother Sam: mobilização ≠ participação', 'Plano de apoio dos EUA (embaixador <b>Lincoln Gordon</b>): combustível, armas e uma força naval com o porta-aviões <i>USS Forrestal</i>. A força foi mandada seguir em <b>31/mar–1/abr</b> e <b>desativada em 2–3/abr</b>, quando o golpe já vencia, sem chegar a operar no Brasil. Os documentos desclassificados mostram <b>disposição de apoiar</b> os golpistas, não ação militar direta.')}
  <div class="col">
    <table class="t rep">
      <tr><th>Quem apoiou o golpe</th><th>Atores</th></tr>
      <tr><td class="k">Civis</td><td>UDN e parte do PSD; governadores Magalhães Pinto (MG), Lacerda (GB), Adhemar de Barros (SP); empresariado; grande imprensa; Igreja; classe média</td></tr>
      <tr><td class="k">Militares</td><td>Oficiais da ESG (Castelo Branco, Golbery); Mourão Filho; Costa e Silva; cúpula das Forças Armadas</td></tr>
      <tr><td class="k">Exterior</td><td>Governo dos EUA</td></tr>
    </table>
  </div>
</div>

${succ({
    title: 'Mapa da sucessão de 1964', tag: 'golpe → interinidade → eleição indireta',
    nodes: [
      { n: 'João Goulart', s: 'até 1–2/abr/1964' },
      { n: 'Ranieri Mazzilli', s: 'pres. da Câmara · 2 → 15/abr/1964', c: 'interim' },
      { n: 'Castelo Branco', s: 'eleito em 11/abr · posse em 15/abr', c: 'now' },
    ],
    steps: [
      ['golpe', '<b>31/mar–2/abr/1964.</b> Golpe civil-militar. Na madrugada de 2/abr, o presidente do Senado declara <b>vaga a Presidência</b>, ainda com Jango em território brasileiro (ele partiu para o exílio no Uruguai em 4/abr); Mazzilli assume.'],
      ['ind', '<b>9/abr:</b> Ato Institucional (AI-1). <b>11/abr:</b> o Congresso, sob pressão militar, elege indiretamente o marechal <b>Castelo Branco</b> para completar o mandato; posse em 15/abr (p. 13).'],
    ],
  })}

${sec('Como a historiografia explica 1964', 'inst', `<table class="t">
  <tr><th>Leitura</th><th>Ênfase</th><th>Expoentes</th></tr>
  <tr><td class="k">Golpe empresarial-militar</td><td>Ação de IPES/IBAD, empresários e militares para conter reformas e sindicatos</td><td>René Dreifuss</td></tr>
  <tr><td class="k">Colapso da democracia</td><td>Radicalização e escolhas de atores políticos que inviabilizaram acordos</td><td>Argelina Figueiredo; Wanderley G. dos Santos</td></tr>
  <tr><td class="k">Golpe e “mito” do governo comunista</td><td>Reformas legítimas e uma ameaça comunista exagerada para justificar o golpe</td><td>Jorge Ferreira</td></tr>
</table>`)}

${rev([
    ['Por que o golpe de 1964 não se explica por uma única causa?', 'Combinou crise econômica, radicalização política, quebra de hierarquia militar, mobilização anticomunista de civis e empresários, e o contexto da Guerra Fria com interesse dos EUA.'],
    ['Qual a diferença entre a mobilização dos EUA e sua participação operacional?', 'Os EUA prepararam apoio naval e logístico (Brother Sam), mas desmobilizaram a força em 2–3/abr, sem atuar; o golpe foi executado por brasileiros, com apoio civil e prontidão externa.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Golpe de 1964; Operação Brother Sam); Arquivo Nacional; documentos desclassificados do governo dos EUA (LBJ Library); Câmara dos Deputados. “Golpe civil-militar” é a designação mais aceita; o regime a chamava de “Revolução”.</div>
`;
  return page(12, { per: 'r46', assunto: 'Guerra Fria, polarização e golpe de 1964', intervalo: '1959–1964' }, body);
};
