module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, barChart, hbars } = H;
  const { PIB, IGPDI } = require('../lib/data.js');
  const ys = ['1960', '1961', '1962', '1963', '1964'];
  const pibSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => PIB[y]), color: '#0b7a8a', ymin: 0, ymax: 12, ticks: [0, 6, 12], show: ys, pad: { l: 5, r: 1, t: 4, b: 6 } });
  const infSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', ymin: 0, ymax: 100, ticks: [0, 50, 100], show: ys, pad: { l: 5, r: 1, t: 4, b: 6 } });
  const body = `
${gov({
    nome: 'João Goulart (Jango)', anos: '1961–1964', sub: 'PTB · 7/09/1961 → 1–2/04/1964', foto: 'jango',
    ficha: {
      chegada: `${chip('const', 'Vice eleito')} Vice-presidente (PTB), eleito em 1960 por voto separado (41,6%). Assume em 7/set/1961 sob <b>parlamentarismo</b> (p. 10). Em 6/jan/1963 um <b>referendo</b> devolve o presidencialismo (≈83%).`,
      contexto: 'Crise política e econômica: <b>PIB</b> cai de 8,6% (1961) para 0,6% (1963) e a <b>inflação</b> sobe; Guerra Fria e Revolução Cubana; mobilização de trabalhadores, estudantes e camponeses; <b>Aliança para o Progresso</b> (EUA).',
      termino: `${chip('golpe')} <b>31/mar–2/abr/1964:</b> golpe civil-militar. Jango deixa o poder sem resistência armada e segue para o exílio no Uruguai (p. 12).`,
      sucessao: `Em 2/abr o Congresso declara vaga a Presidência e <b>Ranieri Mazzilli</b> assume interinamente; em 11/abr é eleito, por voto indireto, o general <b>Castelo Branco</b>.`,
    },
  })}

<div class="row r2-53">
  <div class="col">
    ${sec('3 · Principais medidas e propostas', 'soc', med([
    ['Estabilização', 'eco', '<b>Plano Trienal</b> (1963–65), de Celso Furtado e San Tiago Dantas: conter a inflação sem sacrificar o crescimento. Abandonado em meados de 1963 diante de greves, inflação e falta de apoio político.'],
    ['Direitos', 'soc', '<b>13º salário</b> (1962); <b>Estatuto do Trabalhador Rural</b> (1963); <b>Lei de Remessa de Lucros</b> (1962) limita o envio de lucros de multinacionais.'],
    ['Instituições', 'inst', '<b>Eletrobras</b> instalada em 1962; referendo de 1963 restitui o presidencialismo.'],
    ['Exterior', 'int', 'Política Externa Independente: relações com a <b>URSS</b> restabelecidas em nov/1961.'],
  ]))}
    ${sec('Reformas de Base (propostas)', 'soc', ul([
    '<b>Agrária</b>: desapropriar latifúndios pagando em títulos da dívida, o que exigia mudar a Constituição (indenização prévia em dinheiro).',
    '<b>Urbana, tributária, bancária e universitária</b>; <b>voto de analfabetos e de praças</b>; legalização do PCB.',
  ], 'soc'))}
  </div>
  <div class="col">
    <div class="row r2" style="gap:1.4mm">
      ${chart('PIB real', '% a.a. · IBGE', pibSvg)}
      ${chart('Inflação', '% dez/dez · IGP-DI', infSvg)}
    </div>
    ${chart('Referendo de 6/jan/1963', '% dos votos válidos — TSE', hbars([['Presidencialismo', 83, '#1e3a5f'], ['Parlamentarismo', 17, '#b7c1ce']], { max: 100 }))}
  </div>
</div>

${sec('4 · Crises e oposição: radicalização dos dois lados', 'cris', flow([
    { t: 'causa', k: 'eco', h: 'Crise econômica', p: 'inflação alta e PIB em queda; Plano Trienal fracassa.' },
    { t: 'fato', k: 'soc', h: 'Esquerda', p: 'Brizola, CGT, Ligas Camponesas e UNE exigem reformas imediatas (lema: “na lei ou na marra”).' },
    { t: 'fato', k: 'rep', h: 'Direita', p: 'UDN, Lacerda, IPES/IBAD, imprensa e Igreja denunciam o “perigo comunista”.' },
    { t: 'fato', k: 'cris', h: 'Crise militar', p: 'Revolta dos sargentos (set/1963) e dos marinheiros (mar/1964).' },
    { t: 'cons', k: 'rep', h: '1964', p: 'o golpe (p. 12).' },
  ], { h: true }))}

${sec('Reformas de Base: o que propunham e quem reagia', 'soc', `<table class="t soc">
  <tr><th>Reforma</th><th>Proposta</th><th>Quem reagia e por quê</th></tr>
  <tr><td class="k">Agrária</td><td>Desapropriar latifúndios improdutivos (decreto da SUPRA, 13/mar/1964)</td><td>Proprietários rurais e UDN: ameaça à propriedade</td></tr>
  <tr><td class="k">Eleitoral</td><td>Voto de analfabetos e de praças; elegibilidade de sargentos</td><td>Oficiais: ameaça à hierarquia e ao controle do voto</td></tr>
  <tr><td class="k">Econômica</td><td>Limitar remessa de lucros; encampar refinarias privadas</td><td>Multinacionais, empresários e EUA</td></tr>
  <tr><td class="k">Urbana e bancária</td><td>Acesso à moradia; controle do crédito</td><td>Bancos, proprietários urbanos</td></tr>
</table>`)}

${sec('Linha do tempo do governo Goulart', 'gray', tl({
    start: { d: '7/set/1961', t: 'Posse sob parlamentarismo' },
    events: [
      { d: '23/nov/1961', t: 'Reatamento com a URSS', k: 'int' },
      { d: '1962', t: '13º salário, Remessa de Lucros, Eletrobras', k: 'soc' },
      { d: '6/jan/1963', t: 'Referendo: volta o presidencialismo', k: 'inst' },
      { d: 'set/1963', t: 'Revolta dos sargentos em Brasília', k: 'cris' },
      { d: '13/mar/1964', t: 'Comício da Central do Brasil', k: 'soc' },
    ],
    end: { d: '1–2/abr/1964', t: 'Golpe; Jango deposto', k: 'rep' },
  }))}

${rev([
    ['O que foi o Plano Trienal e por que fracassou?', 'Plano de combate à inflação com reformas, que não obteve apoio do empresariado, dos sindicatos nem do Congresso; a inflação continuou em alta e o plano foi abandonado.'],
    ['O que eram as Reformas de Base e por que provocavam reação?', 'Conjunto de reformas (agrária, urbana, bancária, voto do analfabeto etc.) vistas por parte da elite e dos militares como ameaça à ordem e à propriedade.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (verbete Goulart; Reformas de Base); Planalto (Leis 4.090/1962 e 4.131/1962); TSE (referendo de 1963: ≈83% dos votos válidos pelo presidencialismo); IBGE e Ipeadata.</div>
`;
  return page(11, { per: 'r46', assunto: 'Governo João Goulart (Jango)', intervalo: '1961–1964' }, body);
};
