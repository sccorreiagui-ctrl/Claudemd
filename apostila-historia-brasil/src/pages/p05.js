module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, flowLegend, tl, rev, chip } = H;
  const body = `
${gov({
    nome: 'Eurico Gaspar Dutra', anos: '1946–1951', sub: 'PSD · mandato de 5 anos (31/01/1946 → 31/01/1951)', foto: 'dutra',
    ficha: {
      chegada: '<b>Eleição direta</b> de 2/dez/1945: Dutra (PSD) obteve <b>55,4%</b> dos votos válidos, contra o brigadeiro Eduardo Gomes (UDN, 34,7%) e Yedo Fiúza (PCB, 9,7%). Vargas declarou apoio a Dutra no fim da campanha. Tomou posse em 31/jan/1946, <b>antes</b> da nova Constituição.',
      contexto: 'Pós-guerra e início da <b>Guerra Fria</b>. O país saía do Estado Novo: Constituinte em funcionamento, partidos recém-criados e o PCB legalizado. O Banco Central ainda não existia; o Tesouro dispunha de <b>reservas em divisas</b> acumuladas com as exportações da guerra.',
      termino: 'Cumpriu o mandato de cinco anos <b>sem ruptura institucional</b> (com JK, foi um dos dois únicos presidentes de 1946–1964 a concluí-lo). Entregou a faixa em 31/jan/1951.',
      sucessao: `${chip('dir')} Eleição de 3/out/1950: <b>Getúlio Vargas</b> (PTB, apoio do PSP) com 48,7% × Eduardo Gomes (UDN) 29,7% × Cristiano Machado (PSD) 21,5%. Posse de Vargas em 31/jan/1951.`,
    },
  })}

<div class="row r2-53">
  <div class="col">
    ${sec('3 · Principais medidas e acontecimentos', 'inst', med([
    ['Política', 'inst', 'A <b>Constituição de 18/set/1946</b> (p. 04) vigora durante todo o mandato. O PCB perde o registro (TSE, <b>mai/1947</b>) e seus parlamentares são cassados (<b>jan/1948</b>). Cassinos fechados em abr/1946.'],
    ['Trabalho', 'rep', 'Mantém a CLT, mas <b>reprime greves</b> (decreto-lei de 1946) e intervém em numerosos sindicatos, sob o discurso anticomunista.'],
    ['Economia', 'eco', 'Liberação das importações (1946–47) consome as reservas; em 1947, <b>controle cambial e licenciamento de importações</b>. <b>Plano SALTE</b> (Saúde, Alimentação, Transporte e Energia): enviado ao Congresso em 1948, lei de 1950; pouca execução.'],
    ['Exterior', 'int', 'Alinhamento aos EUA: <b>ruptura com a URSS</b> (out/1947), TIAR (1947) e OEA (1948). O Brasil esperava ajuda financeira, mas os EUA priorizaram a Europa (Plano Marshall).'],
    ['Petróleo', 'eco', 'Campanha <b>“O Petróleo é Nosso”</b> (1948) mobiliza estudantes, militares nacionalistas e o PCB; a pressão prepara a Petrobras (1953, p. 06).'],
  ]))}
  </div>
  <div class="col">
    ${sec('Causa e consequência: economia', 'eco', flow([
    { t: 'causa', k: 'eco', h: 'Reservas da guerra', p: '+ demanda reprimida por bens de consumo' },
    { t: 'fato', k: 'eco', h: '1946–47', p: 'importações liberadas, câmbio valorizado' },
    { t: 'fato', k: 'eco', h: 'Divisas esgotadas', p: 'déficit externo e pressão cambial' },
    { t: 'cons', k: 'eco', h: '1947 em diante', p: 'controle cambial e licenças: favorece a industrialização por substituição de importações' },
  ]))}
    ${flowLegend()}
  </div>
</div>

<div class="row r2-12">
  ${sec('Guerra Fria → política interna', 'int', flow([
    { t: 'causa', k: 'int', h: 'Bloco EUA × URSS', p: '(Doutrina Truman, 1947)' },
    { t: 'fato', k: 'int', h: 'Alinhamento', p: 'TIAR, OEA, anticomunismo' },
    { t: 'cons', k: 'rep', h: 'No Brasil', p: 'PCB na ilegalidade; ruptura com a URSS' },
  ]))}
  <div class="col">
    ${sec('4 · Crises e oposições', 'cris', ul([
    '<b>Direita udenista</b> cobra mais alinhamento; <b>trabalhadores</b> reagem ao arrocho e às intervenções sindicais (o salário mínimo perdeu poder de compra com a inflação).',
    '<b>Nacionalistas</b> (militares do Clube Militar, estudantes) questionam a política petrolífera e a abertura ao capital externo.',
    '<b>Vargas</b>, fora do poder, reorganiza o PTB e volta à cena com apoio popular e do PSP de Adhemar de Barros — o que explica a vitória de 1950.',
  ], 'cris'))}
    ${call('', 'Atenção ENEM', 'A Constituição de 1946 restabeleceu a democracia (separação de Poderes, federação, eleições diretas, direito de greve previsto), mas <b>analfabetos não votavam</b> e o PCB foi posto na ilegalidade: era uma democracia <b>com restrições</b>.')}
  </div>
</div>

${sec('Linha do tempo do governo', 'gray', tl({
    start: { d: '31/jan/1946', t: 'Posse de Dutra (PSD)' },
    events: [
      { d: '18/set/1946', t: 'Constituição promulgada', k: 'inst' },
      { d: 'mai/1947', t: 'PCB perde o registro', k: 'rep' },
      { d: 'out/1947', t: 'Ruptura com a URSS', k: 'int' },
      { d: '1948', t: 'Plano SALTE vai ao Congresso; mandatos do PCB cassados', k: 'eco' },
      { d: '3/out/1950', t: 'Vargas vence a eleição', k: 'cris' },
    ],
    end: { d: '31/jan/1951', t: 'Fim do mandato; posse de Vargas' },
  }))}

${rev([
    ['Por que o governo Dutra rompeu com a URSS e cassou o PCB?', 'Alinhamento ao bloco dos EUA na Guerra Fria e anticomunismo interno; o PCB crescera (≈10% dos votos em 1945 e bancada constituinte).'],
    ['Por que o Plano SALTE rendeu pouco?', 'Recursos públicos escassos, reservas já gastas e financiamento externo que não veio.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (DHBB, verbetes Dutra, Plano SALTE, PCB); Senado Federal (Constituição de 1946); Planalto (Lei 1.102/1950); TSE.</div>
`;
  return page(5, { per: 'r46', assunto: 'Governo Eurico Gaspar Dutra', intervalo: '1946–1951' }, body);
};
