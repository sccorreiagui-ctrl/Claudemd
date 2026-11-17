module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ } = H;
  const body = `
${gov({
    nome: 'Humberto de Alencar Castelo Branco', anos: '1964–1967', sub: 'ARENA · 15/04/1964 → 15/03/1967', foto: 'castelo',
    ficha: {
      chegada: `${chip('ind')} Marechal da ala “castelista” (ESG), <b>eleito pelo Congresso em 11/abr/1964</b> (361 votos), sob o <b>AI-1</b>, para completar o mandato de Jango; posse em 15/abr. O mandato foi prorrogado até 15/mar/1967 (emenda de jul/1964).`,
      contexto: 'Inflação de <b>92%</b> em 1964 (IGP-DI) e PIB de 3,4%; militares divididos entre <b>castelistas</b> (intervenção temporária, “limpeza” e volta à normalidade) e <b>linha dura</b> (continuísmo e punição).',
      termino: 'Entregou o cargo em 15/mar/1967, já sob a <b>Constituição de 1967</b>. A promessa de devolver o poder aos civis em 1966 não foi cumprida, frustrando civis que apoiaram o golpe.',
      sucessao: `${chip('ind')} <b>Costa e Silva</b>, candidato único da ARENA e expoente da linha dura, eleito pelo Congresso em 3/out/1966; o MDB protestou e não apresentou candidato.`,
    },
  })}

${sec('3 · Atos Institucionais: o regime se institucionaliza', 'rep', `<table class="t rep">
  <tr><th>Ato</th><th>Data</th><th>O que fez</th><th>Efeito</th></tr>
  <tr><td class="k">AI-1</td><td>9/abr/1964</td><td>Eleição indireta do presidente; poder de <b>cassar mandatos e suspender direitos políticos por 10 anos</b>; inquéritos policial-militares (IPMs)</td><td>Cassações (Jango, Jânio, Brizola, Arraes, Prestes, Celso Furtado; JK em jun/1964); Congresso e Constituição de 1946 mantidos</td></tr>
  <tr><td class="k">AI-2</td><td>27/out/1965</td><td>Extingue os partidos; eleição indireta para presidente; amplia o STF; civis julgados pela Justiça Militar</td><td><b>Bipartidarismo</b> (ARENA × MDB) e fim das eleições diretas para presidente</td></tr>
  <tr><td class="k">AI-3</td><td>5/fev/1966</td><td>Eleição indireta de governadores; prefeitos de capitais nomeados</td><td>Controle dos estados</td></tr>
  <tr><td class="k">AI-4</td><td>7/dez/1966</td><td>Convoca o Congresso para votar um novo texto constitucional</td><td><b>Constituição de 1967</b> (jan/1967) reforça o Executivo e a segurança nacional</td></tr>
</table>`)}

<div class="row r2-53">
  ${sec('Medidas econômicas e de controle', 'eco', med([
    ['PAEG', 'eco', '<b>Plano de Ação Econômica do Governo</b> (Roberto Campos e Bulhões): combate à inflação com contenção de crédito e do déficit e <b>arrocho salarial</b>. Inflação cai de 92% (1964) para 25% (1967).'],
    ['Reformas', 'inst', '<b>Banco Central</b> (1964), correção monetária, <b>BNH</b> (1964), Código Tributário (1966) e <b>FGTS</b> (1966), que substitui a estabilidade decenal no emprego.'],
    ['Controle', 'rep', '<b>SNI</b> criado em jun/1964 (Golbery); extinção da UNE (Lei Suplicy, nov/1964); intervenção em sindicatos; Lei de Imprensa e Lei de Segurança Nacional (1967).'],
    ['Exterior', 'int', 'Alinhamento aos EUA: ruptura com Cuba (1964); tropas à República Dominicana (1965).'],
  ]))}
  ${sec('Do multipartidarismo ao bipartidarismo', 'inst', `
    <div class="ob" style="--c:var(--inst)"><b class="t">Partidos de 1945–1965</b>PSD, UDN, PTB, PSP, PDC e outros extintos pelo <b>AI-2</b> e pelo Ato Complementar nº 4</div>
    <div class="darr">▼ ▼</div>
    <div class="row r2" style="gap:1.6mm">
      <div class="ob fill k-c-inst" style="--c:var(--inst)"><b class="t">ARENA</b>governista; reúne a maioria da UDN e do PSD</div>
      <div class="ob fill k-c-soc" style="--c:var(--soc)"><b class="t">MDB</b>oposição consentida; PTB e parte do PSD</div>
    </div>`)}
</div>

${sec('4 · Crise de 1965 e o AI-2', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Eleições estaduais (3/out/1965)', p: 'oposição vence na Guanabara e em Minas Gerais.' },
    { t: 'fato', k: 'rep', h: 'Pressão da linha dura', p: 'oficiais exigem endurecimento; o governo cede.' },
    { t: 'cons', k: 'rep', h: 'AI-2 (27/out)', p: 'partidos extintos, eleição indireta e Justiça Militar ampliada.' },
  ], { h: true }))}

${sec('Dois projetos militares em disputa', 'inst', `<table class="t">
  <tr><th></th><th>Castelistas (ESG, “Sorbonne”)</th><th>Linha dura</th></tr>
  <tr><td class="k">Projeto</td><td>Regime de exceção temporário: “limpar” a política e devolver o poder aos civis</td><td>Permanecer no poder e radicalizar a punição aos adversários</td></tr>
  <tr><td class="k">1964–67</td><td>Controlam a Presidência (Castelo Branco, Golbery)</td><td>Pressionam por cassações, IPMs e pelo AI-2</td></tr>
  <tr><td class="k">Depois</td><td>Voltam ao poder com Geisel (1974) e a abertura</td><td>Dominam 1967–1974 (Costa e Silva, AI-5, Médici)</td></tr>
</table>`)}

${sec('Linha do tempo do governo Castelo Branco', 'gray', tl({
    start: { d: '15/abr/1964', t: 'Posse (eleito em 11/abr)' },
    events: [
      { d: 'jun/1964', t: 'SNI criado; JK cassado', k: 'rep' },
      { d: 'nov/1964', t: 'UNE extinta; Estatuto da Terra', k: 'rep' },
      { d: '27/out/1965', t: 'AI-2: bipartidarismo', k: 'rep' },
      { d: '1966', t: 'FGTS, Código Tributário e AI-3', k: 'eco' },
      { d: '24/jan/1967', t: 'Constituição de 1967', k: 'inst' },
    ],
    end: { d: '15/mar/1967', t: 'Posse de Costa e Silva' },
  }))}

${rev([
    ['Por que a ditadura criou o bipartidarismo?', 'Para manter aparência de legalidade, com uma oposição tolerada (MDB), mas sob controle dos Atos Institucionais.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (verbete Castelo Branco; Atos Institucionais); Câmara dos Deputados e Planalto (AI-1 a AI-4, Constituição de 1967); IBGE e Ipeadata (PIB e IGP-DI).</div>
`;
  return page(13, { per: 'dit', assunto: 'Governo Castelo Branco', intervalo: '1964–1967' }, body);
};
