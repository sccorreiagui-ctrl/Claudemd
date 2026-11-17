module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, barChart, hbars } = H;
  const { PIB, IGPDI } = require('../lib/data.js');
  const ys = ['1956', '1957', '1958', '1959', '1960'];
  const pibSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => PIB[y]), color: '#0b7a8a', ymin: 0, ymax: 12, ticks: [0, 6, 12], show: ys, pad: { l: 5, r: 1, t: 4, b: 6 } });
  const infSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', ymin: 0, ymax: 45, ticks: [0, 15, 30, 45], show: ys, pad: { l: 5, r: 1, t: 4, b: 6 } });
  const body = `
${gov({
    nome: 'Juscelino Kubitschek (JK)', anos: '1956–1961', sub: 'PSD · 31/01/1956 → 31/01/1961', foto: 'jk',
    ficha: {
      chegada: `${chip('dir')} Eleição de <b>3/out/1955</b> (coligação PSD/PTB, 35,7%; vice: Jango). A posse foi garantida pelo <b>contragolpe de Lott</b> (p. 07); assumiu em 31/jan/1956.`,
      contexto: 'Instabilidade política após 1954–55; <b>energia e transportes</b> insuficientes; indústria ainda pouco diversificada; inflação de dois dígitos; Guerra Fria no pano de fundo.',
      termino: 'Cumpriu os <b>5 anos</b> do mandato (como Dutra, concluiu-o sem ruptura), deixando <b>inflação alta</b>, dívida externa maior e déficit público.',
      sucessao: `${chip('dir')} Eleição de 3/out/1960: <b>Jânio Quadros</b> (PTN, apoio da UDN) 48,3% × Lott 32,9% × Adhemar 18,8%. Posse em 31/jan/1961, em Brasília.`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Principais medidas e acontecimentos', 'eco', med([
    ['Plano de Metas', 'eco', '<b>“50 anos em 5”</b>: <b>30 metas</b> em cinco setores (energia, transportes, alimentação, indústrias de base, educação) + a <b>meta-síntese: Brasília</b>. Energia, transportes e indústria avançaram; educação e alimentação ficaram para trás.'],
    ['Capital', 'eco', '<b>Tripé</b>: Estado (infraestrutura), capital privado nacional (bens de consumo) e <b>capital estrangeiro</b> (automóveis, mecânica pesada), atraído por incentivos (Instrução 113, GEIA/1956).'],
    ['Transportes', 'eco', '<b>Opção rodoviarista</b>: rodovias (Belém–Brasília) e indústria automobilística (Volkswagen, Willys, Ford, Mercedes-Benz) em vez de ferrovias.'],
    ['Brasília', 'inst', '<b>Novacap</b> (1956); Plano Piloto de <b>Lúcio Costa</b> e arquitetura de <b>Niemeyer</b>; inaugurada em <b>21/abr/1960</b>. Os migrantes que a ergueram, os <b>candangos</b>, acabaram nas cidades-satélites.'],
    ['Regional e exterior', 'int', '<b>SUDENE</b> (dez/1959), de Celso Furtado, para o Nordeste; <b>Operação Pan-Americana</b> (1958) pede ajuda ao desenvolvimento.'],
  ]))}
  <div class="col">
    <div class="row r2" style="gap:1.4mm">
      ${chart('PIB real', '% a.a. · IBGE', pibSvg)}
      ${chart('Inflação', '% dez/dez · IGP-DI', infSvg)}
    </div>
    ${call('', 'Crescer e endividar', 'O PIB cresceu em média cerca de <b>8% a.a.</b> em 1956–1960, mas a inflação saltou de 24% (1956) para 30% (1960): o desenvolvimento veio com desequilíbrio externo e fiscal.')}
  </div>
</div>

<div class="row r2">
  ${sec('4 · Crises e oposição', 'cris', ul([
    '<b>Revoltas de oficiais da Aeronáutica</b>: Jacareacanga (fev/1956) e Aragarças (dez/1959), anistiadas por JK.',
    '<b>Ruptura com o FMI</b> (jun/1959): JK interrompe negociações sobre um plano de estabilização que exigia cortar gastos e crédito, para não frear o Plano de Metas.',
    '<b>Oposição da UDN</b> (Carlos Lacerda) denuncia custos e corrupção na construção de Brasília.',
  ], 'cris'))}
  ${sec('Contradições do desenvolvimento', 'rep', ul([
    '<b>Desigualdade regional</b> (Nordeste × Centro-Sul) e concentração de renda.',
    '<b>Dependência</b> de capital e tecnologia estrangeiros; dívida externa em alta.',
    '<b>Rodovias</b> no lugar de ferrovias; migrantes sem lugar no plano de Brasília.',
  ], 'rep'))}
</div>

${chart('Plano de Metas: para onde iria o investimento previsto', '% do total previsto, por setor (valores aproximados) — CPDOC/FGV', hbars([['Energia', 43.4, '#0b7a8a'], ['Transportes', 29.6, '#0b7a8a'], ['Indústrias de base', 20.4, '#0b7a8a'], ['Educação', 3.4, '#9aa8ba'], ['Alimentação', 3.2, '#9aa8ba']], { max: 50 }), '<div class="src" style="margin-top:1mm">Energia e transportes somavam cerca de três quartos do plano; educação e alimentação, menos de 7%: o desenvolvimento priorizou a infraestrutura e a indústria.</div>')}

${sec('Linha do tempo do governo JK', 'gray', tl({
    start: { d: '31/jan/1956', t: 'Posse de JK' },
    events: [
      { d: 'fev/1956', t: 'Revolta de Jacareacanga; Plano de Metas', k: 'cris' },
      { d: '1957', t: 'Concurso do Plano Piloto de Brasília', k: 'eco' },
      { d: 'jun/1959', t: 'Rompimento com o FMI', k: 'cris' },
      { d: 'dez/1959', t: 'SUDENE; revolta de Aragarças', k: 'eco' },
      { d: '21/abr/1960', t: 'Brasília inaugurada', k: 'eco' },
      { d: '3/out/1960', t: 'Jânio Quadros eleito', k: 'cris' },
    ],
    end: { d: '31/jan/1961', t: 'Posse de Jânio em Brasília' },
  }))}

${rev([
    ['O que foi o Plano de Metas e como se financiou?', 'Programa de industrialização acelerada (“50 anos em 5”), financiado por gasto estatal, capital privado e <b>capital estrangeiro</b>, com forte endividamento e inflação.'],
    ['Que contradições o governo JK deixou?', 'Crescimento industrial e Brasília, mas inflação, dívida externa, desigualdade regional e dependência do capital estrangeiro.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (verbete JK; Plano de Metas); Senado Federal; IBGE e Ipeadata (PIB e IGP-DI); TSE (eleições de 1955 e 1960).</div>
`;
  return page(8, { per: 'r46', assunto: 'Governo Juscelino Kubitschek', intervalo: '1956–1961' }, body);
};
