module.exports = (H) => {
  const { page, sec, ul, call, flow, rev, chart, barChart, lineChart } = H;
  const { PIB, IGPDI, DIVIDA } = require('../lib/data.js');
  const yrs = []; for (let y = 1964; y <= 1985; y++) yrs.push(String(y));
  const pib = barChart({
    w: 186, h: 50, keys: yrs, vals: yrs.map((y) => PIB[y]), color: '#0b7a8a',
    colors: { 1964: '#9aa8ba', 1965: '#9aa8ba', 1966: '#9aa8ba', 1967: '#9aa8ba', 1974: '#6a3fa0', 1975: '#6a3fa0', 1976: '#6a3fa0', 1977: '#6a3fa0', 1978: '#6a3fa0', 1979: '#6a3fa0', 1980: '#b66a00', 1981: '#b66a00', 1982: '#b66a00', 1983: '#b66a00', 1984: '#b66a00', 1985: '#b66a00' },
    ymin: -6, ymax: 16, ticks: [-5, 0, 5, 10, 15], show: ['1968', '1973', '1974', '1981', '1983'], ylab: '%',
    bands: [{ from: '1964', to: '1967', label: 'PAEG', color: '#586373' }, { from: '1968', to: '1973', label: 'MILAGRE · média 11,1% a.a.', color: '#0b7a8a' }, { from: '1974', to: '1979', label: 'CHOQUE DO PETRÓLEO · II PND', color: '#6a3fa0' }, { from: '1980', to: '1985', label: 'CRISE DA DÍVIDA', color: '#b66a00' }],
  });
  const dk = Object.keys(DIVIDA);
  const div = lineChart({ w: 90, h: 46, keys: dk, vals: dk.map((k) => DIVIDA[k]), color: '#b3261e', ymin: 0, ymax: 120, ticks: [0, 40, 80, 120], show: ['1969', '1973', '1979', '1985'], labelEvery: 3, dec: 1, pad: { l: 8, r: 6, t: 6, b: 6.5 } });
  const ik = []; for (let y = 1964; y <= 1985; y++) ik.push(String(y));
  const inf = barChart({ w: 90, h: 46, keys: ik, vals: ik.map((y) => IGPDI[y]), color: '#b66a00', ymin: 0, ymax: 250, ticks: [0, 100, 200], show: ['1964', '1973', '1979', '1985'], labelEvery: 3, dec: 0, pad: { l: 8, r: 1, t: 6, b: 6.5 } });
  const body = `
<div class="ptitle"><h1>Milagre Econômico (1968–1973): crescimento, dívida e desigualdade</h1><span class="per">1964–1985</span></div>
<div class="call gray"><b class="hd">Tema econômico, não um governo</b>O “Milagre” ocorreu nos governos <b>Costa e Silva</b> (1968–1969, p. 14) e <b>Médici</b> (1969–1973, p. 16), sob o ministro da Fazenda <b>Antônio Delfim Netto</b> (1967–1974). Os gráficos abaixo usam <b>séries únicas e oficiais</b> (IBGE, FGV, Banco Central), sem misturar períodos.</div>

${chart('PIB real: variação anual, 1964–1985', '% a.a. · IBGE/SCN (Ipeadata). Cores: cinza = PAEG; ciano = Milagre; roxo = anos Geisel; âmbar = crise da dívida.', pib)}

<div class="row r2">
  ${chart('Dívida externa bruta, 1967–1985', 'US$ bilhões · Banco Central (BP), via Ipeadata', div, '<div class="src">1969: US$ 4,6 bi → 1973: US$ 14,9 bi → 1979: US$ 55,8 bi → 1985: US$ 105,2 bi.</div>')}
  ${chart('Inflação anual (IGP-DI), 1964–1985', '% dez/dez · FGV (Ipeadata). Mínima do período: 15,5% em 1973.', inf)}
</div>

${sec('Causas, características e consequências', 'eco', flow([
    { t: 'causa', k: 'eco', h: 'Condições', p: 'reformas do PAEG e capacidade ociosa; <b>crédito farto</b> e ao consumidor; liquidez e comércio mundiais em alta; <b>arrocho salarial</b> e repressão sindical sob o AI-5.' },
    { t: 'fato', k: 'eco', h: 'Milagre (1968–73)', p: 'PIB de 9,8% a 14,0% ao ano (média de 11,1%); indústria e exportações crescem; inflação cai para 15,5% (1973).' },
    { t: 'cons', k: 'rep', h: 'Custos', p: 'endividamento externo, <b>concentração de renda</b>, dependência do petróleo importado e vulnerabilidade ao choque de 1973.' },
  ], { h: true }))}

<div class="row r2">
  ${sec('Obras e integração nacional', 'eco', ul([
    '<b>Ponte Rio–Niterói</b> (1968–1974), <b>Transamazônica</b> (a partir de 1970), Angra 1 (obras desde 1972) e o tratado de <b>Itaipu</b> (1973).',
    'Telecomunicações (<b>Embratel</b>) e expansão da TV; crédito para casa própria (BNH).',
    'Obras de enorme custo, financiadas em parte por dívida externa.',
  ], 'eco'))}
  ${sec('Quem ganhou? A desigualdade', 'rep', `<p>“Fazer o bolo crescer para depois dividi-lo”, frase atribuída a Delfim Netto, resume a lógica oficial: o bolo cresceu, mas a divisão não veio.</p>
  <table class="t rep" style="margin-top:1.2mm"><tr><th>Índice de Gini (concentração de renda)</th><th>1960</th><th>1970</th><th>1980</th></tr>
  <tr><td>Quanto maior, mais desigual</td><td style="white-space:nowrap"><b>≈ 0,50</b></td><td style="white-space:nowrap"><b>≈ 0,56</b></td><td style="white-space:nowrap"><b>≈ 0,59</b></td></tr></table>
  <div class="src">Censos do IBGE; estimativas aproximadas de pesquisadores (Hoffmann, Ipea).</div>`)}
</div>

${rev([
    ['Como crescimento econômico e desigualdade coexistiram durante o Milagre?', 'O PIB cresceu mais de 10% ao ano e a inflação caiu, mas o arrocho salarial, a repressão aos sindicatos e a concentração do crédito elevaram a concentração de renda; os ganhos foram desiguais.'],
    ['Por que o Milagre terminou?', 'Dependia de crédito externo, petróleo barato e arrocho; o choque do petróleo (out/1973) elevou custos e dívida e esgotou o modelo.'],
  ])}
<div class="src">Fontes: IBGE (SCN) e Ipeadata (PIB, IGP-DI/FGV, dívida externa bruta, Banco Central); Atlas Histórico do Brasil/FGV (verbete Milagre Econômico); “Determinantes do milagre econômico brasileiro (1968–1973)”, Revista Brasileira de Economia (SciELO).</div>
`;
  return page(17, { per: 'dit', assunto: 'Milagre Econômico, dívida e desigualdade', intervalo: '1968–1973' }, body);
};
