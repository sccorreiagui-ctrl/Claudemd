module.exports = (H) => {
  const { page, sec, call, rev, chip } = H;

  // ===== trilho de transições (SVG em mm) =====
  const W = 186, X0 = 4, X1 = 182, Y0 = 1930, Y1 = 2011;
  const X = (y) => X0 + ((y - Y0) / (Y1 - Y0)) * (X1 - X0);
  const COL = { D: '#2a7a4b', I: '#1e3a5f', C: '#6d8fb8', R: '#f2a21e', X: '#b3261e', G: '#7a1712', M: '#6b7685', P: '#b66a00', J: '#7a1712' };
  const T = [
    [1930.84, 'G', '1930'], [1934.55, 'I', '1934'], [1937.86, 'G', '1937'], [1945.83, 'X', '1945'], [1946.08, 'D', ''],
    [1951.08, 'D', '1951'], [1954.65, 'M', '1954–56'], [1955.85, 'C', ''], [1956.08, 'D', ''], [1961.08, 'D', '1961'],
    [1961.65, 'R', ''], [1961.69, 'C', ''], [1964.25, 'G', '1964'], [1967.2, 'I', '1967'], [1969.66, 'J', '1969'],
    [1974.2, 'I', '1974'], [1979.2, 'I', '1979'], [1985.2, 'I', '1985'], [1990.2, 'D', '1990'], [1992.75, 'P', '1992'],
    [1995.0, 'D', '1995'], [2003.0, 'D', '2003'],
  ];
  const AY = 11;
  let s = `<svg viewBox="0 0 ${W} 22" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">`;
  [[1930.84, 1945.83, '#1e3a5f'], [1945.83, 1964.27, '#2a7a4b'], [1964.27, 1985.2, '#b3261e'], [1985.2, 2011, '#2a7a4b']].forEach(([a, b, c]) => {
    s += `<rect x="${X(a)}" y="${AY - 0.55}" width="${X(b) - X(a) - 0.2}" height="1.1" fill="${c}" opacity=".55"/>`;
  });
  T.forEach(([y, k, lab], i) => {
    const x = X(y);
    s += `<circle cx="${x}" cy="${AY}" r="1.6" fill="${COL[k]}" stroke="#fff" stroke-width=".4"/>`;
    if (lab) s += `<text x="${x}" y="${i % 2 === 0 ? AY - 3 : AY + 5.4}" text-anchor="middle" font-size="2.2" font-weight="700" fill="${COL[k]}">${lab}</text>`;
  });
  s += `<text x="${X0}" y="20.6" font-size="2" fill="#586373">1930</text><text x="${X1}" y="20.6" font-size="2" text-anchor="end" fill="#586373">2010</text></svg>`;

  const leg = [['D', 'eleição direta'], ['I', 'eleição indireta'], ['C', 'sucessão constitucional'], ['R', 'renúncia'], ['X', 'deposição/impedimento'], ['G', 'golpe'], ['M', 'morte'], ['P', 'impeachment']]
    .map(([k, t]) => `<span style="display:inline-flex;align-items:center;gap:.9mm;margin-right:2.4mm"><i style="display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%;background:${COL[k]}"></i>${t}</span>`).join('');

  const row = (ano, de, tipos, por) => `<tr><td class="k">${ano}</td><td>${de}</td><td>${tipos}</td><td>${por}</td></tr>`;
  const table = `<table class="t" style="font-size:6.8pt;table-layout:fixed"><colgroup><col style="width:17mm"><col style="width:46mm"><col style="width:57mm"><col></colgroup>
    <tr><th>Ano</th><th>Transição</th><th>Tipo</th><th>Por quê / contexto</th></tr>
    ${row('1930', 'Washington Luís → Junta → Vargas', chip('golpe', 'Revolução'), 'racha oligárquico, crise do café, eleição contestada')}
    ${row('1937', 'Vargas → Vargas (Estado Novo)', chip('golpe', 'Golpe'), 'Plano Cohen forjado; fim da eleição de 1938')}
    ${row('1945', 'Vargas → Linhares → Dutra', chip('dep') + ' ' + chip('dir'), 'FEB e Queremismo; generais depõem; eleição em 2/dez')}
    ${row('1954', 'Vargas → Café Filho', chip('morte') + ' ' + chip('const', 'Constitucional'), 'atentado da Rua Tonelero e ultimato militar')}
    ${row('1955–56', 'Café Filho → Luz → Nereu → JK', chip('const', 'Constitucional') + ' ' + chip('dep', 'Impedimento') + ' ' + chip('dir'), 'conspiração contra a posse; movimento de Lott')}
    ${row('1961', 'Jânio → Mazzilli → Jango', chip('ren') + ' ' + chip('const', 'Constitucional'), 'renúncia; veto militar; Legalidade; parlamentarismo')}
    ${row('1964', 'Jango → Mazzilli → Castelo Branco', chip('golpe') + ' ' + chip('ind'), 'crise, Guerra Fria, apoio civil-militar; AI-1')}
    ${row('1967', 'Castelo Branco → Costa e Silva', chip('ind'), 'linha dura; candidato único da ARENA')}
    ${row('1969', 'Costa e Silva → Junta → Médici', chip('junta') + ' ' + chip('ind'), 'AVC; veto à posse do vice Pedro Aleixo')}
    ${row('1974 · 1979', 'Médici → Geisel → Figueiredo', chip('ind'), 'Colégio Eleitoral; abertura “lenta, gradual e segura”')}
    ${row('1985', 'Figueiredo → (Tancredo, eleito) → Sarney', chip('ind') + ' ' + chip('morte') + ' ' + chip('const', 'Constitucional'), 'Diretas Já derrotadas; Tancredo não tomou posse')}
    ${row('1990', 'Sarney → Collor', chip('dir'), 'primeira eleição presidencial direta desde 1960')}
    ${row('1992', 'Collor → Itamar Franco', chip('imp'), 'denúncias, CPI e Caras-pintadas')}
    ${row('1995 · 2003', 'Itamar → FHC → Lula', chip('dir'), 'Plano Real; alternância entre presidentes eleitos')}
  </table>`;

  const def = (t, d) => `<div class="ob" style="--c:var(--inst)"><b class="t">${t}</b>${d}</div>`;
  const body = `
<div class="ptitle"><h1>Revisão final: linha do tempo, transições e conceitos</h1><span class="per">1930–2010</span></div>

<div class="chart" style="padding:2mm 2.4mm 1.4mm">
  <div class="ct">Todas as mudanças de governo, por tipo (cor do ponto)</div>
  <div class="cs">Linha: azul = Era Vargas · verde = períodos democráticos · vermelho = Ditadura Militar. Os anos indicam a transição.</div>
  ${s}
  <div class="legend" style="flex-wrap:wrap;margin-top:1mm">${leg}</div>
</div>

${sec('Principais transições presidenciais', 'cris', table)}

${sec('Conceitos comparativos', 'inst', `<div class="row r3" style="gap:1.6mm">
  ${def('Eleição direta × indireta', '<b>Direta</b>: o eleitor vota (1945–1960; 1989 em diante). <b>Indireta</b>: Congresso ou Colégio Eleitoral (1934; 1964–1985).')}
  ${def('Sucessão constitucional', 'Assume quem a Constituição indica: vice, presidente da Câmara, do Senado ou do STF (Café Filho, Luz, Nereu, Mazzilli, Linhares).')}
  ${def('Interino × efetivo', 'Interino exerce o cargo temporariamente; <b>efetivo</b> é o titular (Itamar em 1992; Sarney em 1985).')}
  ${def('Renúncia × deposição', '<b>Renúncia</b>: ato voluntário (Jânio, Collor). <b>Deposição</b>: afastamento forçado (Vargas em 1945; Jango em 1964).')}
  ${def('Golpe × impeachment', '<b>Golpe</b>: ruptura da ordem constitucional (1930, 1937, 1964; 1969 dentro do regime). <b>Impeachment</b>: processo previsto na Constituição (1992).')}
  ${def('Plebiscito e referendo', 'Consultas populares: <b>1963</b> (referendo; presidencialismo, ≈83%) e <b>1993</b> (plebiscito; república e presidencialismo).')}
</div>`)}

${rev([
    ['1. Por que a crise de 1954 terminou no suicídio de Vargas?', 'Atentado → inquérito sobre a guarda pessoal → ultimato militar e da oposição; o suicídio reverteu o clima e adiou o golpe.'],
    ['2. Qual foi o papel de Lott em 1955?', 'Mobilizou o Exército em 11/nov para garantir a posse de JK e Jango, derrubando Luz.'],
    ['3. Por que Jango assumiu sob parlamentarismo?', 'Solução negociada para vencer o veto militar sem guerra civil (EC nº 4, 2/set/1961).'],
    ['4. Como o AI-5 alterou o regime?', 'Poderes ilimitados ao Executivo: fechar o Congresso, cassar, intervir, censurar e suspender o habeas corpus em crimes políticos.'],
    ['5. Como crescimento e desigualdade coexistiram no Milagre?', 'PIB de ~11% a.a., mas arrocho salarial e concentração de renda (Gini 0,50 → 0,56) e dívida crescente.'],
    ['6. Qual a diferença entre a abertura de Geisel e a de Figueiredo?', 'Geisel: controlada, com recuos (Pacote de Abril); Figueiredo: anistia e pluripartidarismo, sob pressão social e crise.'],
    ['7. Por que as Diretas Já não resultaram em eleição direta?', 'A emenda teve 298 votos e precisava de 320 (2/3); a eleição de 1985 foi indireta.'],
  ], 'Revisão ativa — responda antes de ler o gabarito')}
<div class="src">Síntese elaborada a partir das páginas anteriores; datas e votações conforme CPDOC/FGV, Câmara dos Deputados, Senado Federal e TSE.</div>
`;
  return page(24, { per: 'geral', assunto: 'Síntese final, transições e revisão ativa', intervalo: '1930–2010' }, body);
};
