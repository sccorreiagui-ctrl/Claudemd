module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, barChart } = H;
  const { PIB, IGPDI } = require('../lib/data.js');
  const ys = ['1979', '1980', '1981', '1982', '1983', '1984', '1985'];
  const pibSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => PIB[y]), color: '#0b7a8a', colors: { 1981: '#b3261e', 1983: '#b3261e' }, ymin: -6, ymax: 12, ticks: [-5, 0, 5, 10], show: ['1981', '1983', '1985'], pad: { l: 5, r: 1, t: 4, b: 6 } });
  const infSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', ymin: 0, ymax: 250, ticks: [0, 100, 200], show: ['1979', '1985'], dec: 0, pad: { l: 5, r: 1, t: 4, b: 6 } });
  const box = (k, t, txt) => `<div class="ob fill k-c-${k}" style="--c:var(--${k})"><b class="t">${t}</b>${txt}</div>`;
  const body = `
${gov({
    nome: 'João Baptista Figueiredo', anos: '1979–1985', sub: 'ARENA/PDS · 15/03/1979 → 15/03/1985', foto: 'figueiredo',
    ficha: {
      chegada: `${chip('ind')} Último general-presidente, <b>eleito pelo Colégio Eleitoral</b> em 15/out/1978 (355 × 226 de Euler Bentes Monteiro, do MDB), sucessor escolhido por Geisel. Posse em 15/mar/1979, com mandato de 6 anos.`,
      contexto: '<b>Segundo choque do petróleo</b> (1979), juros internacionais altos e dívida externa de US$ 55,8 bi; greves do ABC (1978–80); sociedade civil organizada pressiona por <b>anistia</b> e <b>eleições</b>.',
      termino: 'Em 15/mar/1985, <b>não passou a faixa</b> ao sucessor civil e deixou o Planalto sem a cerimônia. Governo marcado por recessão, inflação de 235% (1985) e dívida de US$ 105 bi.',
      sucessao: `${chip('ind')} O Colégio Eleitoral elege <b>Tancredo Neves</b> (15/jan/1985); ele adoece na véspera e <b>José Sarney</b> assume (p. 20).`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Abertura e reformas políticas', 'soc', med([
    ['Anistia', 'soc', '<b>Lei 6.683</b> (28/ago/1979): anistia a crimes políticos e “conexos” de 1961 a 1979; volta dos exilados (Brizola, Arraes, Prestes e outros).'],
    ['Partidos', 'inst', '<b>Reforma partidária</b> (dez/1979) extingue ARENA e MDB: surgem PDS, PMDB, PT, PDT, PTB e PP (organograma ao lado).'],
    ['Eleições', 'soc', '<b>Eleições diretas para governadores</b> em 1982: oposição vence em SP, MG e RJ.'],
  ]))}
  ${sec('Pluripartidarismo (1979–80)', 'inst', `
    <div class="row r2" style="gap:1.4mm"><div class="col" style="gap:1.2mm">
      ${box('inst', 'ARENA', '→ <b>PDS</b> (governista)')}
      ${box('soc', 'MDB', '→ <b>PMDB</b> (Ulysses)')}
    </div><div class="col" style="gap:1.2mm">
      ${box('soc', 'Novos', '<b>PT</b> (Lula, ABC), <b>PDT</b> (Brizola), <b>PTB</b> (Ivete Vargas), <b>PP</b> (Tancredo; funde-se ao PMDB em 1982)')}
    </div></div>`)}
</div>

${sec('Lei da Anistia (1979): fatos × interpretação', 'cris', `<div class="row r2" style="gap:2.4mm">
  <div><b class="t-soc">Fatos históricos</b><ul class="l k-soc tight"><li>O movimento (Comitê Brasileiro pela Anistia) pedia “anistia ampla, geral e irrestrita”.</li><li>A lei foi <b>parcial</b>: excluiu condenados por terrorismo, assalto, sequestro e atentado pessoal, e abrangeu “crimes conexos”.</li><li>Permitiu o retorno de exilados e a libertação de presos políticos.</li></ul></div>
  <div><b class="t-cris">Interpretação em disputa</b><ul class="l k-cris tight"><li>A leitura de que “crimes conexos” alcança também agentes do Estado que torturaram foi consagrada pelo <b>STF</b> (ADPF 153, 2010).</li><li>A <b>Corte Interamericana</b> (Gomes Lund, 2010) a considerou incompatível com a Convenção Americana.</li><li>A Comissão Nacional da Verdade (2014) pediu a responsabilização; o debate continua.</li></ul></div>
</div>`)}

<div class="row r2-53">
  ${sec('4 · Crises e oposição', 'rep', ul([
    '<b>Greves do ABC</b> (1978–80, Lula): reaparece o novo sindicalismo; intervenção no sindicato e prisão de líderes (1980).',
    '<b>Terrorismo da linha dura</b>: carta-bomba na OAB (27/ago/1980) e <b>Riocentro</b> (30/abr/1981): uma bomba explode prematuramente <b>dentro de um carro</b> de militares do DOI-CODI na véspera do show do Dia do Trabalho; o IPM atribuiu o ataque à esquerda, versão desmentida depois.',
    '<b>Crise da dívida</b>: moratória do México (ago/1982) fecha o crédito; o Brasil recorre ao FMI; recessão e inflação.',
  ], 'rep'))}
  <div class="col">
    <div class="row r2" style="gap:1.4mm">
      ${chart('PIB real', '% a.a. · IBGE', pibSvg)}
      ${chart('Inflação', '% dez/dez · IGP-DI', infSvg)}
    </div>
  </div>
</div>

${sec('A abertura de Geisel × a de Figueiredo', 'soc', `<table class="t soc">
  <tr><th></th><th>Geisel (1974–79)</th><th>Figueiredo (1979–85)</th></tr>
  <tr><td class="k">Ritmo</td><td>“Lenta, gradual e segura”, controlada pelo governo</td><td>Mais ampla, pressionada pela sociedade</td></tr>
  <tr><td class="k">Instrumentos</td><td>Fim do AI-5; recuos (Lei Falcão, Pacote de Abril)</td><td>Anistia, pluripartidarismo, eleições diretas de governadores</td></tr>
  <tr><td class="k">Contexto</td><td>Fim do Milagre; linha dura ainda forte</td><td>Crise da dívida, greves e campanha das Diretas</td></tr>
</table>`)}

${sec('Linha do tempo do governo Figueiredo', 'gray', tl({
    start: { d: '15/mar/1979', t: 'Posse de Figueiredo' },
    events: [
      { d: '28/ago/1979', t: 'Lei da Anistia', k: 'soc' },
      { d: 'dez/1979', t: 'Fim do bipartidarismo', k: 'inst' },
      { d: '30/abr/1981', t: 'Atentado do Riocentro', k: 'rep' },
      { d: 'nov/1982', t: 'Eleições diretas de governadores', k: 'soc' },
      { d: '25/abr/1984', t: 'Emenda das Diretas rejeitada', k: 'cris' },
    ],
    end: { d: '15/mar/1985', t: 'Fim do mandato' },
  }))}

${rev([
    ['Por que o fim do bipartidarismo interessava ao governo?', 'Dividir a oposição reunida no MDB e manter o PDS forte; mas também abriu espaço para PT, PDT e PTB e para a reorganização da sociedade.'],
    ['O que a Lei da Anistia permitiu e o que gera debate?', 'Permitiu a volta dos exilados e libertações; o debate é sobre se “crimes conexos” inclui agentes torturadores, o que a Justiça interpretou de forma controversa.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (Figueiredo; Anistia; Riocentro); Planalto (Lei 6.683/1979 e Lei 6.767/1979); STF (ADPF 153); Corte IDH (Gomes Lund × Brasil, 2010); Comissão Nacional da Verdade (2014); Ipeadata.</div>
`;
  return page(19, { per: 'dit', assunto: 'Governo Figueiredo', intervalo: '1979–1985' }, body);
};
