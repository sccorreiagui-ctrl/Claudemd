module.exports = (H) => {
  const { page, call } = H;

  // ===== linha do tempo 1930–2010 (SVG em mm) =====
  const W = 186, X0 = 3, X1 = 183, Y0 = 1930, Y1 = 2011;
  const X = (y) => X0 + ((y - Y0) / (Y1 - Y0)) * (X1 - X0);
  const NAVY = '#1e3a5f', G1 = '#2a7a4b', G2 = '#4f9c70', R1 = '#b3261e', R2 = '#cf5a52', RJ = '#7a1712';
  // governos: [rótulo, início, fim, cor, tipo]  (tipo: v = vertical, l = rótulo com chamada)
  const GOVS = [
    ['Getúlio Vargas (Governo Provisório, Constitucional e Estado Novo)', 1930.84, 1945.83, NAVY, 'h'],
    ['Linhares', 1945.83, 1946.08, '#8aa0be', 'l'],
    ['Dutra', 1946.08, 1951.08, G1, 'v'],
    ['Vargas', 1951.08, 1954.65, G2, 'v'],
    ['Café F./Luz/Nereu', 1954.65, 1956.08, '#9bc7ad', 'v'],
    ['JK', 1956.08, 1961.08, G1, 'v'],
    ['Jânio', 1961.08, 1961.65, '#9bc7ad', 'l'],
    ['Jango', 1961.69, 1964.25, G2, 'v'],
    ['Castelo', 1964.29, 1967.2, R1, 'v'],
    ['Costa e Silva', 1967.2, 1969.66, R2, 'v'],
    ['Junta', 1969.66, 1969.83, RJ, 'l'],
    ['Médici', 1969.83, 1974.2, R1, 'v'],
    ['Geisel', 1974.2, 1979.2, R2, 'v'],
    ['Figueiredo', 1979.2, 1985.2, R1, 'v'],
    ['Sarney', 1985.2, 1990.2, G1, 'v'],
    ['Collor', 1990.2, 1992.75, G2, 'v'],
    ['Itamar', 1992.75, 1995.0, '#9bc7ad', 'v'],
    ['FHC', 1995.0, 2003.0, G1, 'v'],
    ['Lula', 2003.0, 2011.0, G2, 'v'],
  ];
  const PER = [
    ['ERA VARGAS 1930–1945', 1930.84, 1945.83, NAVY],
    ['REPÚBLICA DE 1946 · 1946–1964', 1945.83, 1964.27, G1],
    ['DITADURA MILITAR · 1964–1985', 1964.27, 1985.2, R1],
    ['NOVA REPÚBLICA · 1985–', 1985.2, 2011, G1],
  ];
  const EV = [
    [1930.84, 'cris', 'Revolução|de 1930'], [1932.5, 'cris', 'Rev. Consti-|tucionalista'], [1934.54, 'inst', 'Constituição|de 1934'],
    [1937.86, 'rep', 'Estado|Novo'], [1943.33, 'soc', 'CLT'], [1945.83, 'cris', 'Queda de Vargas|(29/out/1945)'],
    [1946.72, 'inst', 'Constituição|de 1946'], [1953.76, 'eco', 'Petrobras'], [1954.65, 'cris', 'Suicídio de|Vargas'],
    [1955.86, 'cris', 'Contragolpe|de Lott'], [1960.3, 'eco', 'Brasília|inaugurada'], [1961.65, 'cris', 'Renúncia de Jânio;|parlamentarismo'],
    [1964.25, 'rep', 'Golpe civil-|militar'], [1968.95, 'rep', 'AI-5'], [1973.8, 'int', 'Choque do|petróleo'],
    [1979.65, 'soc', 'Lei da|Anistia'], [1984.3, 'soc', 'Diretas Já'], [1988.77, 'inst', 'Constituição|de 1988'],
    [1992.99, 'cris', 'Impeachment|de Collor'], [1994.5, 'eco', 'Plano Real'], [2002.83, 'soc', 'Lula eleito'],
  ];
  const COL = { cris: '#b66a00', inst: '#1e3a5f', rep: '#b3261e', soc: '#2a7a4b', int: '#6a3fa0', eco: '#0b7a8a' };
  let s = `<svg viewBox="0 0 ${W} 79" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">`;
  // faixas de período
  PER.forEach(([lab, a, b, c]) => {
    const xa = X(Math.max(a, Y0)), xb = X(b);
    s += `<rect x="${xa}" y="0" width="${xb - xa - 0.3}" height="5.4" rx=".8" fill="${c}"/><text x="${(xa + xb) / 2}" y="3.7" text-anchor="middle" font-size="2.15" font-weight="700" fill="#fff" letter-spacing=".12">${lab}</text>`;
  });
  // governos
  const GY = 7, GH = 25;
  GOVS.forEach(([name, a, b, c, t]) => {
    const xa = X(a), xb = X(b), w = xb - xa;
    s += `<rect x="${xa}" y="${GY}" width="${Math.max(w - 0.25, 0.35)}" height="${GH}" fill="${c}"/>`;
    const dark = ['#9bc7ad', '#8aa0be'].includes(c);
    if (t === 'h') s += `<text x="${xa + 3}" y="${GY + GH / 2 + 0.8}" font-size="2.7" font-weight="700" fill="#fff">GETÚLIO VARGAS</text><text x="${xa + 3}" y="${GY + GH / 2 + 4.0}" font-size="1.95" fill="#dbe6f3">Provisório, Constitucional</text><text x="${xa + 3}" y="${GY + GH / 2 + 6.4}" font-size="1.95" fill="#dbe6f3">e Estado Novo</text>`;
    if (t === 'v') s += `<text transform="translate(${xa + w / 2 + 0.75},${GY + GH - 1.8}) rotate(-90)" font-size="${w < 4 ? 1.7 : 2.05}" font-weight="600" fill="${dark ? '#12301f' : '#fff'}">${name}</text>`;
  });
  // chamadas para governos estreitos
  const call1 = (x, lab, dy, dx = 0, anchor = 'middle') => {
    return `<line x1="${x}" x2="${x + dx}" y1="${GY}" y2="${GY - 0.1}" stroke="#555" stroke-width=".25"/>`;
  };
  // interinos citados sob a barra
  s += `<g font-size="1.8" fill="#444">
    <text x="${X(1946.0) - 6}" y="${GY + GH + 3.2}" text-anchor="end" font-weight="600">Linhares ▲</text>
    <text x="${X(1961.35) - 3}" y="${GY + GH + 3.2}" text-anchor="end" font-weight="600">Jânio ▲</text>
    <text x="${X(1969.75) + 0.2}" y="${GY + GH + 3.2}" text-anchor="middle" font-weight="600" fill="${RJ}">▲ Junta</text>
  </g>`;
  // eixo de anos
  const AY = GY + GH + 5.2;
  s += `<line x1="${X0}" x2="${X1}" y1="${AY}" y2="${AY}" stroke="#8a95a5" stroke-width=".3"/>`;
  for (let y = 1930; y <= 2010; y += 10) {
    s += `<line x1="${X(y)}" x2="${X(y)}" y1="${AY - 1}" y2="${AY + 1}" stroke="#586373" stroke-width=".3"/><text x="${X(y)}" y="${AY + 3.4}" text-anchor="middle" font-size="2.1" font-weight="700" fill="#586373">${y}</text>`;
  }
  // eventos
  const LANE0 = AY + 6.5, STEP = 9.4;
  EV.forEach(([y, k, lab], i) => {
    const lane = i % 4;
    const x = X(y), yl = LANE0 + lane * STEP;
    const anchorEnd = x > 160;
    const lines = lab.split('|');
    s += `<line x1="${x}" x2="${x}" y1="${AY}" y2="${yl - 1}" stroke="${COL[k]}" stroke-width=".28" opacity=".7"/><circle cx="${x}" cy="${AY}" r=".85" fill="${COL[k]}"/>`;
    lines.forEach((ln, j) => {
      s += `<text x="${x + (anchorEnd ? -0.9 : 0.9)}" y="${yl + 1 + j * 2.35}" text-anchor="${anchorEnd ? 'end' : 'start'}" font-size="2.25" font-weight="${j === 0 ? 700 : 500}" fill="${COL[k]}">${ln}</text>`;
    });
  });
  s += '</svg>';

  const body = `
<div class="cover-hero"><div class="stripe"></div><div class="stripe s2"></div>
  <div class="kick">Apostila visual de revisão · ENEM e PAS 3 (UnB) · 2026</div>
  <h1>História do Brasil<br>da Era Vargas à Nova República</h1>
  <div class="sub">Governos, crises e <b>transições presidenciais</b> — com foco na <b>República de 1946</b> e na <b>Ditadura Militar</b> (1946–1985), antecedentes essenciais e síntese até 2010.</div>
  <div class="badges"><span class="badge">24 páginas</span><span class="badge">1 governo = 1 seção</span><span class="badge">causas · eventos · consequências</span></div>
</div>

<div class="row r2-53">
  <div class="col">
    <h2>Objetivo e como estudar</h2>
    <ul class="l tight">
      <li><b>Para quem:</b> quem já conhece a sequência geral dos governos e precisa dominar <b>medidas, crises, causas e consequências</b> — e <b>como cada governo terminou e o seguinte começou</b>.</li>
      <li><b>Cada governo</b> segue a mesma ficha: <b>(1)</b> como chegou ao poder · <b>(2)</b> situação encontrada · <b>(3)</b> medidas · <b>(4)</b> crises · <b>(5)</b> linha do tempo · <b>(6)</b> como terminou · <b>(7)</b> sucessão.</li>
      <li><b>Transições</b> (pp. 04, 07, 10, 12, 15, 20, 22, 24) são o eixo da apostila: cada uma distingue <b>eleição, sucessão constitucional, renúncia, deposição, golpe e eleição indireta</b>.</li>
      <li><b>Revisão ativa:</b> quadros verdes com perguntas e respostas curtas; esquema final na p. 24.</li>
      <li><b>Atenção:</b> datas e números foram conferidos em fontes oficiais; interpretações debatidas aparecem identificadas como tal.</li>
    </ul>
  </div>
  <div class="col">
    <h2>Código de cores</h2>
    <div class="legendgrid" style="grid-template-columns:1fr">
      <div><span class="swatch" style="background:#1e3a5f"></span><b>Azul-escuro</b> · instituições e constituições</div>
      <div><span class="swatch" style="background:#f2a21e"></span><b>Âmbar</b> · crises e mudanças de governo</div>
      <div><span class="swatch" style="background:#b3261e"></span><b>Vermelho</b> · repressão e autoritarismo</div>
      <div><span class="swatch" style="background:#2a7a4b"></span><b>Verde</b> · direitos sociais e democratização</div>
      <div><span class="swatch" style="background:#6a3fa0"></span><b>Roxo</b> · contexto internacional e Guerra Fria</div>
      <div><span class="swatch" style="background:#0b7a8a"></span><b>Ciano</b> · economia e industrialização</div>
    </div>
  </div>
</div>

<div class="chart" style="padding:2mm 2.4mm 1.4mm">
  <div class="ct">Linha do tempo geral da República brasileira, 1930–2010</div>
  <div class="cs">Faixas = períodos; barras = governos (largura proporcional ao mandato). ▲ marca interinos e a Junta de 1969. Cada ponto abaixo é um marco decisivo.</div>
  ${s}
</div>

<div class="row r3">
  ${call('', 'Mapa da apostila', '<b>Era Vargas</b> · pp. 02–03<br><b>República de 1946</b> · pp. 04–12<br><b>Ditadura Militar</b> · pp. 13–20<br><b>Nova República</b> · pp. 21–23<br><b>Revisão geral</b> · p. 24')}
  ${call('cris', 'Regra de ouro', 'Nunca confunda <b>quem governou</b> com <b>quem foi eleito</b>: Café Filho, Carlos Luz, Nereu Ramos, Ranieri Mazzilli, a Junta de 1969 e José Linhares exerceram a Presidência sem terem sido eleitos para ela. <b>Tancredo Neves foi eleito, mas nunca tomou posse.</b>')}
  ${call('int', 'Terminologia', 'Preferimos <b>República de 1946</b> ou <i>Período Democrático (1946–1964)</i> a “República Populista”, rótulo hoje contestado por parte da historiografia. “Golpe de 1964” é <b>civil-militar</b>: houve apoio civil amplo.')}
</div>
<div class="src">Elaborada a partir de inventário de videoaulas (profs. Débora Aladim e Pedro Assaad), conferido e corrigido com CPDOC/FGV, Senado Federal, Câmara dos Deputados, TSE, Arquivo Nacional, IBGE e Ipeadata. Lista completa de fontes e correções: docs/RELATORIO_QUALIDADE.md.</div>
`;
  return page(1, { per: 'geral', assunto: 'Capa e linha do tempo geral', intervalo: '1930–2010' }, body);
};
