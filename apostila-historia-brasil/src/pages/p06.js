module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, chart, barChart } = H;
  const { PIB, IGPDI } = require('../lib/data.js');
  const ys = ['1951', '1952', '1953', '1954'];
  const pibSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => PIB[y]), color: '#0b7a8a', ymin: 0, ymax: 10, ticks: [0, 5, 10], show: ys, ylab: '', pad: { l: 5, r: 1, t: 4, b: 6 } });
  const infSvg = barChart({ w: 46, h: 34, keys: ys, vals: ys.map((y) => IGPDI[y]), color: '#b66a00', ymin: 0, ymax: 30, ticks: [0, 10, 20, 30], show: ys, ylab: '', pad: { l: 5, r: 1, t: 4, b: 6 } });
  const body = `
${gov({
    nome: 'Getúlio Vargas — segundo governo', anos: '1951–1954', sub: 'PTB · 31/01/1951 → 24/08/1954', foto: 'vargas',
    ficha: {
      chegada: `${chip('dir')} Eleição de <b>3/out/1950</b>: Vargas (PTB, apoiado pelo PSP) 48,7% × Eduardo Gomes (UDN) 29,7% × Cristiano Machado (PSD) 21,5%. A UDN contestou a validade alegando falta de maioria absoluta (a Constituição não a exigia).`,
      contexto: 'Inflação e pressão cambial herdadas do fim do governo Dutra; <b>nacionalismo econômico</b> em alta (petróleo); oposição udenista, de Carlos Lacerda e de parte dos militares ao retorno de Vargas.',
      termino: `${chip('morte')} <b>24/ago/1954:</b> cercado por ultimato militar e pela crise do atentado da Rua Tonelero, Vargas se mata no Catete e deixa a <b>Carta-testamento</b>.`,
      sucessao: `${chip('const')} O vice <b>Café Filho</b> (PSP) assume no mesmo dia, para completar o mandato até 31/jan/1956 (mas não o conclui: p. 07).`,
    },
  })}

<div class="row r2-53">
  ${sec('3 · Principais medidas e acontecimentos', 'eco', med([
    ['Modelo', 'eco', '<b>Nacional-desenvolvimentismo</b>: Estado indutor da industrialização, com controle nacional sobre recursos estratégicos e limite à remessa de lucros ao exterior.'],
    ['Petróleo', 'eco', '<b>Petrobras</b> (Lei 2.004, 3/out/1953): monopólio estatal da pesquisa, lavra, refino e transporte, fruto da campanha “O Petróleo é Nosso”.'],
    ['Finanças', 'inst', '<b>BNDE</b> (jun/1952) financia infraestrutura e indústria de base; Banco do Nordeste (1952); CAPES (1951). O projeto da <b>Eletrobras</b> foi enviado ao Congresso em 1954, mas a empresa só seria criada em 1961 e instalada em 1962 (governo Goulart).'],
    ['Trabalho', 'soc', '<b>Greve dos 300 mil</b> (SP, mar–abr/1953). João Goulart, ministro do Trabalho (jun/1953–fev/1954), aproxima governo e sindicatos; em <b>1/mai/1954</b> o salário mínimo sobe 100%.'],
    ['Câmbio', 'eco', 'Crise cambial de 1953 e Instrução 70 da SUMOC (leilões e câmbio múltiplo).'],
  ]))}
  <div class="col">
    ${call('cris', 'Carta-testamento (trechos)', '“Mais uma vez, as forças e os interesses contra o povo coordenaram-se novamente e se desencadeiam sobre mim.” … “Serenamente dou o primeiro passo no caminho da eternidade e <b>saio da vida para entrar na História</b>.”')}
    <div class="row r2" style="gap:1.4mm">
      ${chart('PIB real', '% a.a. · IBGE', pibSvg)}
      ${chart('Inflação', '% dez/dez · IGP-DI', infSvg)}
    </div>
  </div>
</div>

${sec('4 · Crise de 1954: da oposição ao suicídio', 'cris', flow([
    { t: 'causa', k: 'cris', h: 'Oposição crescente', p: '“Mar de lama”, Lacerda e UDN; Manifesto dos Coronéis (fev/1954) contra o aumento do salário mínimo.' },
    { t: 'fato', k: 'rep', h: '5/ago', p: 'Atentado da Rua Tonelero: Lacerda ferido; morre o major Rubens Vaz (Aeronáutica).' },
    { t: 'fato', k: 'cris', h: 'Inquérito do Galeão', p: 'IPM liga o crime a Gregório Fortunato, chefe da guarda pessoal de Vargas.' },
    { t: 'fato', k: 'cris', h: 'Pressão', p: 'UDN, imprensa e manifestos militares (22/ago) exigem o afastamento de Vargas.' },
    { t: 'cons', k: 'cris', h: '24/ago', p: 'suicídio; revolta popular contra jornais de oposição e a embaixada dos EUA; Café Filho assume.' },
  ], { h: true }))}

${sec('Linha do tempo do segundo governo', 'gray', tl({
    start: { d: '31/jan/1951', t: 'Posse de Vargas' },
    events: [
      { d: 'jun/1952', t: 'BNDE criado', k: 'eco' },
      { d: 'mar–abr/1953', t: 'Greve dos 300 mil', k: 'soc' },
      { d: '3/out/1953', t: 'Lei da Petrobras', k: 'eco' },
      { d: 'fev/1954', t: 'Manifesto dos Coronéis; Jango deixa o Trabalho', k: 'cris' },
      { d: '1/mai/1954', t: 'Salário mínimo +100%', k: 'soc' },
      { d: '5/ago/1954', t: 'Atentado da Rua Tonelero', k: 'rep' },
    ],
    end: { d: '24/ago/1954', t: 'Suicídio de Vargas' },
  }))}

${succ({
    title: 'Mapa da sucessão de 1954', tag: 'detalhes na p. 07', one: true,
    nodes: [{ n: 'Getúlio Vargas', s: '1951 → 24/ago/1954' }, { n: 'Café Filho', s: 'vice · 24/ago/1954 → 8/nov/1955', c: 'now' }],
    steps: [['morte', 'Vargas se mata em 24/ago/1954. O vice-presidente <b>Café Filho</b> assume imediatamente, por sucessão constitucional; o golpe que setores udenistas e militares articulavam perde força diante da comoção popular.']],
  })}

${rev([
    ['Por que a crise de 1954 terminou no suicídio de Vargas?', 'Acuado pela oposição civil e militar após o atentado e o inquérito que atingiu sua guarda pessoal, Vargas rejeitou renunciar; o suicídio reverteu o clima político e adiou o golpe.'],
    ['Qual o legado econômico do período?', 'Petrobras, BNDE e a ideia de Estado indutor da industrialização, o <b>nacional-desenvolvimentismo</b>, que JK ampliaria com abertura ao capital estrangeiro.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (A Era Vargas, 1954; verbete Carta-testamento); Planalto (Lei 2.004/1953); Rio Memórias (motins de 25/ago/1954); IBGE e Ipeadata (PIB e IGP-DI/FGV).</div>
`;
  return page(6, { per: 'r46', assunto: 'Segundo governo Vargas e a crise de 1954', intervalo: '1951–1954' }, body);
};
