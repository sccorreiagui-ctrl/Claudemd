module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, chart, barChart } = H;
  const { PIB } = require('../lib/data.js');
  const ys = []; for (let y = 1995; y <= 2010; y++) ys.push(String(y));
  const colors = {}; for (let y = 1995; y <= 2002; y++) colors[y] = '#1e3a5f'; for (let y = 2003; y <= 2010; y++) colors[y] = '#2a7a4b';
  const pib = barChart({
    w: 186, h: 31, keys: ys, vals: ys.map((y) => PIB[y]), color: '#1e3a5f', colors, ymin: -2, ymax: 9, ticks: [0, 3, 6, 9], show: ['1995', '1998', '1999', '2004', '2009', '2010'], ylab: '%',
    bands: [{ from: '1995', to: '2002', label: 'FHC · média ≈ 2,4% a.a.', color: '#1e3a5f' }, { from: '2003', to: '2010', label: 'LULA · média ≈ 4,1% a.a.', color: '#2a7a4b' }],
  });
  const body = `
<div class="ptitle"><h1>Fernando Henrique Cardoso e Lula: estabilização e inclusão</h1><span class="per">1995–2010</span></div>

${chart('PIB real: variação anual, 1995–2010', '% a.a. · IBGE/SCN (Ipeadata). As médias são calculadas sobre a série oficial de cada mandato.', pib)}

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Fernando Henrique Cardoso (FHC)', anos: '1995–2002', sub: 'PSDB · 1/01/1995 → 31/12/2002 (dois mandatos)',
    ficha: {
      chegada: `${chip('dir')} Eleito no 1º turno em 1994 (<b>54,3%</b>) como “pai” do Plano Real; reeleito em 1998 (53,1%) depois da <b>Emenda da Reeleição</b> (EC 16, 1997).`,
      contexto: 'Inflação em queda após o Real (14,8% em 1995); economia aberta e vulnerável a <b>crises externas</b> (México 1994–95, Ásia 1997, Rússia 1998).',
      medidas: '<b>Estabilização</b>: câmbio flutuante (1999), metas de inflação e superávit primário (o “tripé”); <b>privatizações</b> (Vale, Telebras); fim do monopólio do petróleo (ANP); <b>Lei de Responsabilidade Fiscal</b> (2000); FUNDEF; <b>Bolsa Escola</b> (2001).',
      crises: 'Crise cambial de <b>jan/1999</b> (desvalorização do real e acordo com o FMI); desemprego; <b>apagão</b> (2001); críticas de MST, CUT e PT às privatizações; denúncias de compra de votos na reeleição (1997), sem condenação.',
      termino: 'Cumpriu os dois mandatos; deixou inflação sob controle, dívida pública maior e crescimento médio de cerca de 2,4% ao ano (1995–2002).',
      sucessao: `${chip('dir')} Eleição de 2002: <b>Lula</b> (PT) vence o 2º turno com 61,3%. Primeira passagem de faixa entre dois presidentes eleitos pelo voto direto desde 1961.`,
    },
  })}
${tl({
    start: { d: '1/jan/1995', t: 'Posse de FHC' },
    events: [
      { d: '1995–97', t: 'Fim do monopólio do petróleo; EC da Reeleição', k: 'inst' },
      { d: 'mai/1997', t: 'Privatização da Vale', k: 'eco' },
      { d: 'jan/1999', t: 'Câmbio flutuante', k: 'eco' },
      { d: '2000', t: 'Lei de Responsabilidade Fiscal', k: 'inst' },
      { d: '2001', t: 'Apagão; Bolsa Escola', k: 'cris' },
    ],
    end: { d: '31/dez/2002', t: 'Fim do mandato' },
  })}

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Luiz Inácio Lula da Silva', anos: '2003–2010', sub: 'PT · 1/01/2003 → 31/12/2010 (dois mandatos)',
    ficha: {
      chegada: `${chip('dir')} Eleito em 2002 (<b>61,3%</b> no 2º turno) e reeleito em 2006 (60,8%); ex-operário e fundador do PT, após três derrotas (1989, 1994, 1998). Prometeu respeitar contratos na <b>Carta ao Povo Brasileiro</b> (2002).`,
      contexto: 'Desconfiança do mercado (câmbio e risco-país em alta em 2002); fome e desigualdade; economia mundial em expansão (<b>ciclo de commodities</b>).',
      medidas: 'Manutenção do <b>tripé</b>; <b>Bolsa Família</b> (2003–04) e Fome Zero; valorização do salário mínimo; ProUni; <b>PAC</b> (2007); Minha Casa Minha Vida (2009); pré-sal (2007); dívida com o FMI quitada (2005); grau de investimento (2008).',
      crises: '<b>Mensalão</b> (2005): denúncias de pagamentos a parlamentares (julgado pelo STF em 2012); <b>crise global de 2008–09</b>: PIB −0,1% em 2009, com resposta anticíclica e retomada (7,5% em 2010).',
      termino: 'Concluiu dois mandatos com crescimento médio de cerca de 4,1% ao ano (2003–2010) e alta aprovação.',
      sucessao: `${chip('dir')} Eleição de 31/out/2010: <b>Dilma Rousseff</b> (PT) vence o 2º turno com 56,1%. Posse em 1/jan/2011.`,
    },
  })}
${tl({
    start: { d: '1/jan/2003', t: 'Posse de Lula' },
    events: [
      { d: '2003–04', t: 'Bolsa Família', k: 'soc' },
      { d: 'dez/2005', t: 'Quitação antecipada ao FMI', k: 'eco' },
      { d: '2005', t: 'Crise do mensalão', k: 'cris' },
      { d: '2007', t: 'PAC; descoberta do pré-sal', k: 'eco' },
      { d: '2008–09', t: 'Crise financeira global', k: 'int' },
    ],
    end: { d: '31/dez/2010', t: 'Fim do mandato; posse de Dilma' },
  })}

${rev([
    ['O que há de continuidade e de ruptura entre FHC e Lula?', 'Continuidade: estabilidade monetária, tripé macroeconômico e Lei de Responsabilidade Fiscal. Ruptura: ênfase em transferência de renda, valorização do salário mínimo, expansão do crédito e papel maior do Estado como investidor.'],
  ])}
<div class="src">Fontes: TSE (eleições de 1994, 1998, 2002, 2006 e 2010); Planalto; Banco Central; IBGE e Ipeadata (PIB); CPDOC/FGV e Câmara dos Deputados. Valores de inflação e crescimento por mandato calculados sobre as séries oficiais.</div>
`;
  return page(23, { per: 'nova', assunto: 'Governos FHC e Lula', intervalo: '1995–2010' }, body);
};
