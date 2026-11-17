module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, barChart } = H;
  const { IGPDI } = require('../lib/data.js');
  const ys = ['1989', '1990', '1991', '1992', '1993', '1994', '1995'];
  const infSvg = barChart({ w: 88, h: 36, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', colors: { 1995: '#2a7a4b', 1994: '#2a7a4b' }, ymin: 0, ymax: 3000, ticks: [0, 1000, 2000, 3000], show: ys, dec: 0, pad: { l: 8, r: 1, t: 4, b: 6 } });
  const body = `
<div class="ptitle"><h1>Collor e Itamar Franco: do impeachment ao Plano Real</h1><span class="per">1990–1994</span></div>

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Fernando Collor de Mello', anos: '1990–1992', sub: 'PRN · 15/03/1990 → 29/12/1992',
    ficha: {
      chegada: `${chip('dir')} Eleito em 1989 (2º turno: <b>53,0%</b> × Lula 47,0%) com discurso de “caçador de marajás”; <b>primeira eleição presidencial direta desde 1960</b>.`,
      contexto: 'Hiperinflação (<b>1.783%</b> em 1989), dívida e crise do Estado; fim da Guerra Fria e da URSS; ideias de abertura e privatização.',
      medidas: '<b>Plano Collor</b> (16/mar/1990): bloqueio de cerca de 80% dos ativos financeiros e nova moeda (cruzeiro); reforma administrativa, <b>abertura comercial</b>, privatizações; <b>Mercosul</b> (1991).',
      crises: 'Recessão (PIB −4,3% em 1990); denúncias de Pedro Collor sobre o esquema <b>PC Farias</b> (mai/1992); CPI; <b>Caras-pintadas</b>.',
      termino: `${chip('imp')} Câmara autoriza o processo (<b>29/set/1992</b>: 441 × 38); afastado em 2/out. Em <b>29/dez</b> renuncia, mas o Senado o condena (inelegível por 8 anos).`,
      sucessao: `${chip('const')} <b>Itamar Franco</b> (vice) assume como <b>interino</b> em 2/out/1992 e é <b>efetivado</b> em 29/dez/1992.`,
    },
  })}
${tl({
    start: { d: '15/mar/1990', t: 'Posse de Collor' },
    events: [
      { d: '16/mar/1990', t: 'Plano Collor: confisco e nova moeda', k: 'eco' },
      { d: 'mar/1991', t: 'Tratado de Assunção (Mercosul)', k: 'int' },
      { d: '24/mai/1992', t: 'Denúncias de Pedro Collor', k: 'cris' },
      { d: '29/set/1992', t: 'Câmara autoriza o processo', k: 'cris' },
    ],
    end: { d: '29/dez/1992', t: 'Renúncia; Senado condena' },
  })}

${call('cris', 'Impeachment ≠ golpe ≠ renúncia', '<b>Impeachment</b> é processo político-jurídico <u>previsto na Constituição</u> (a Câmara autoriza, o Senado julga). <b>Renúncia</b> é ato voluntário: Collor renunciou durante o julgamento, mas o Senado concluiu o processo e aplicou a inabilitação. Não houve ruptura institucional.')}

${gov({
    kick: 'Governo', compact: true, c4: true, nome: 'Itamar Franco', anos: '1992–1994', sub: '2/10/1992 (interino) · 29/12/1992 (efetivo) → 31/12/1994',
    ficha: {
      chegada: `${chip('const')} Vice-presidente: <b>interino</b> a partir de 2/out/1992 e <b>efetivo</b> em 29/dez/1992, após a renúncia de Collor; sem eleição para o cargo.`,
      contexto: 'Inflação de <b>1.157%</b> em 1992 e <b>2.708%</b> em 1993; crise política; recessão recente.',
      medidas: '<b>Plano Real</b>, da equipe de <b>FHC</b> (Fazenda desde mai/1993): URV (1/mar/1994) e <b>real</b> (1/jul/1994); <b>plebiscito</b> de 21/abr/1993 mantém república e presidencialismo.',
      crises: 'Trocas de ministros da Fazenda até FHC; “Anões do Orçamento” (1993).',
      termino: 'Concluiu o mandato em 31/dez/1994, com inflação em queda e alta popularidade.',
      sucessao: `${chip('dir')} Eleição de 3/out/1994: <b>FHC</b> (PSDB) vence no 1º turno com 54,3% (Lula 27,0%). Posse em 1/jan/1995.`,
    },
  })}
${tl({
    start: { d: '2/out/1992', t: 'Assume como interino' },
    events: [
      { d: '29/dez/1992', t: 'Efetivado presidente', k: 'cris' },
      { d: '21/abr/1993', t: 'Plebiscito: república e presidencialismo', k: 'inst' },
      { d: '1/mar/1994', t: 'URV', k: 'eco' },
      { d: '1/jul/1994', t: 'Nasce o Real', k: 'eco' },
    ],
    end: { d: '31/dez/1994', t: 'Fim do mandato' },
  })}

<div class="row r2">
  ${chart('Inflação anual (IGP-DI), 1989–1995', '% dez/dez · FGV (Ipeadata). Verde = anos do Plano Real.', infSvg)}
  ${succ({
    title: 'Mapa da sucessão de 1992', tag: 'impeachment', one: true,
    nodes: [{ n: 'Collor', s: 'até 2/out/1992' }, { n: 'Itamar Franco', s: 'interino → efetivo em 29/dez/1992', c: 'now' }],
    steps: [['imp', '<b>29/set–2/out/1992.</b> Câmara autoriza; Collor é afastado e Itamar assume. <b>29/dez:</b> renúncia de Collor e condenação pelo Senado; Itamar é efetivado.']],
  })}
</div>

${rev([
    ['Como terminou o governo Collor?', 'Impeachment: afastado em 2/out/1992; renunciou em 29/dez, mas o Senado o condenou e o tornou inelegível por 8 anos.'],
    ['Por que o Plano Real teve êxito onde planos anteriores falharam?', 'Combinou URV (alinhou preços), moeda nova, âncora cambial e ajuste fiscal, sem congelamento nem confisco.'],
  ])}
<div class="src">Fontes: Câmara dos Deputados e Senado Federal (processo de Collor, 1992); TSE (eleições de 1989 e 1994; plebiscito de 1993); CPDOC/FGV; Banco Central; Ipeadata.</div>
`;
  return page(22, { per: 'nova', assunto: 'Governos Collor e Itamar Franco', intervalo: '1990–1994' }, body);
};
