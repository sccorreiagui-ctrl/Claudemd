module.exports = (H) => {
  const { page, gov, sec, ul, med, call, flow, tl, rev, chip, succ, hbars, chart } = H;
  const body = `
<div class="ptitle"><h1>Transição de 1945 e Constituição de 1946</h1><span class="per">1945–1946</span></div>

${succ({
    title: 'Mapa da sucessão de 1945', tag: 'fim do Estado Novo',
    nodes: [
      { n: 'Getúlio Vargas', s: 'Estado Novo · 1937–1945' },
      { n: 'José Linhares', s: 'interino · 30/out/1945–31/jan/1946', c: 'interim' },
      { n: 'Eurico G. Dutra', s: 'PSD · 1946–1951', c: 'now' },
    ],
    steps: [
      ['dep', '<b>29/out/1945:</b> o ministro da Guerra, general Góis Monteiro, com apoio dos altos comandos, depõe Vargas depois que ele nomeia o irmão, Benjamin Vargas, para a polícia do Distrito Federal. Vargas não resiste.'],
      ['inter', '<b>30/out/1945:</b> assume José Linhares, presidente do STF: a Carta de 1937 não previa vice-presidente e os militares escolheram o chefe do Judiciário para conduzir a transição.'],
      ['dir', '<b>2/dez/1945:</b> eleição direta do presidente e da Assembleia Constituinte; Dutra (PSD) vence. <b>Posse em 31/jan/1946.</b>'],
    ], one: true,
  })}

${gov({
    kick: 'Governo interino', compact: true, c4: true, nome: 'José Linhares', anos: '1945–1946', sub: '30/out/1945 → 31/jan/1946',
    ficha: {
      chegada: `${chip('inter')} Presidente do STF, assume após a deposição de Vargas; <b>não foi eleito</b> para o cargo.`,
      contexto: 'Estado Novo derrubado; eleições já marcadas (Ato Adicional, fev/1945); partidos novos; <b>PCB legalizado</b>; Queremismo ainda mobiliza trabalhadores.',
      termino: 'Cumpriu a missão de <b>realizar as eleições</b> de 2/dez/1945 e transmitiu o cargo em 31/jan/1946, como previsto.',
      sucessao: `${chip('dir')} <b>Eurico Gaspar Dutra</b> (PSD) vence; Vargas é eleito senador e deputado, mas não disputa a Presidência.`,
    },
  })}
${tl({
    start: { d: '30/out/1945', t: 'Linhares assume' },
    events: [{ d: 'nov/1945', t: 'Campanha eleitoral; Vargas apoia Dutra', k: 'cris' }, { d: '2/dez/1945', t: 'Eleições: Dutra e Constituinte', k: 'soc' }],
    end: { d: '31/jan/1946', t: 'Posse de Dutra' },
  })}

<div class="row r2-12">
  ${chart('Eleição presidencial de 2/dez/1945', 'votos válidos (%) — TSE', hbars([['Dutra (PSD)', 55.39, '#1e3a5f'], ['Eduardo Gomes (UDN)', 34.74, '#7d8da3'], ['Yedo Fiúza (PCB)', 9.71, '#b7c1ce']], { max: 60 }), '<div class="src" style="margin-top:1mm">Primeira eleição presidencial em que as mulheres votaram.</div>')}
  <table class="t">
    <tr><th>Partido</th><th>Origem e base social</th><th>Perfil em 1945</th></tr>
    <tr><td class="k">PSD <span class="mute">(jul/1945)</span></td><td>Interventores e elites ligadas ao Estado Novo; base rural e administrativa</td><td>Governista moderado; candidato: Dutra</td></tr>
    <tr><td class="k">PTB <span class="mute">(set/1945)</span></td><td>Ministério do Trabalho e sindicatos; base operária urbana</td><td>Trabalhismo; liderança de Vargas</td></tr>
    <tr><td class="k">UDN <span class="mute">(abr/1945)</span></td><td>Oposição liberal a Vargas: antigos oligarcas, liberais e classes médias</td><td>Antigetulismo; candidato: Eduardo Gomes</td></tr>
    <tr><td class="k">PCB <span class="mute">(legal em 1945)</span></td><td>Operários e intelectuais; liderança de Prestes</td><td>≈10% dos votos; Prestes eleito senador</td></tr>
  </table>
</div>

${sec('Constituição de 18/set/1946 — promulgada pela Constituinte', 'inst', med([
    ['Estado', 'inst', 'República federativa e <b>presidencialista</b>; três Poderes independentes; presidente com <b>mandato de 5 anos</b>, sem reeleição imediata, eleito por voto direto e <b>maioria simples</b> (não exigia maioria absoluta: ponto-chave em 1955).'],
    ['Democracia', 'soc', 'Voto direto, secreto e obrigatório para <b>alfabetizados</b> maiores de 18 anos (analfabetos, soldados e cabos ficavam sem voto); pluripartidarismo; Justiça Eleitoral; <b>direito de greve</b> reconhecido.'],
    ['Economia', 'eco', '<b>Função social da propriedade</b>, mas desapropriação exigia <b>indenização prévia e em dinheiro</b>: obstáculo à reforma agrária, tema central em 1963–64.'],
    ['Limites', 'rep', 'Vedava partidos cujo programa contrariasse o “regime democrático”: base jurídica para a <b>cassação do PCB em 1947</b> (p. 05).'],
  ]))}

${sec('Três Constituições da Era Vargas e da República de 1946', 'inst', `<table class="t">
  <tr><th>Constituição</th><th>Origem</th><th>Regime e eleições</th><th>Direitos e limites</th></tr>
  <tr><td class="k">1934</td><td>Promulgada por Constituinte</td><td>Democracia liberal com Executivo forte; voto secreto e feminino; mandato de 4 anos</td><td>Direitos trabalhistas; Justiça Eleitoral e do Trabalho</td></tr>
  <tr><td class="k">1937 (“Polaca”)</td><td>Outorgada por Vargas</td><td>Autoritário: Congresso e partidos extintos; eleições suspensas; mandato de 6 anos</td><td>Censura e repressão política; sindicatos controlados</td></tr>
  <tr><td class="k">1946</td><td>Promulgada por Constituinte</td><td>Democracia federativa; voto direto; mandato de 5 anos; vice-presidente separado</td><td>Greve reconhecida; analfabetos sem voto; PCB vetado</td></tr>
</table>`)}

${rev([
    ['Por que a FEB e a Guerra Fria ajudam a explicar 1945?', 'A FEB lutara contra o fascismo e deslegitimou a ditadura interna; ao mesmo tempo, o Queremismo e a ascensão do PCB assustaram generais e UDN, que precipitaram a deposição.'],
    ['O que a Constituição de 1946 tinha de democrático e de restritivo?', 'Democrático: federação, eleições diretas, greve reconhecida. Restritivo: analfabetos sem voto, vedação de partidos “antidemocráticos” e indenização prévia na desapropriação.'],
  ])}
<div class="src">Fontes: CPDOC/FGV (fim do Estado Novo; Linhares); Senado Federal (Constituição de 1946); TSE (eleição de 1945). Vargas foi eleito senador (RS) e deputado por vários estados; optou pelo Senado.</div>
`;
  return page(4, { per: 'r46', assunto: 'Transição de 1945 e Constituição de 1946', intervalo: '1945–1946' }, body);
};
