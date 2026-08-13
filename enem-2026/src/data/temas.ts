import type { Area, Tema, Tier } from "../types";

function slugify(area: Area, nome: string): string {
  const base = `${area}-${nome}`
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
  return base;
}

type RawTema = [Area, string, Tier, number | null, string, string];

// Dataset verificado: Aprova Total 2016–2025, Estratégia Vestibulares, SAS/CNN, Assaad.
const RAW: RawTema[] = [
  ["Matemática", "Matemática básica / aritmética", "alta", 37.3, "Razão/proporção/regra de três (o mais cobrado), porcentagem, decimais, escalas.", "Aprova Total 2016–2025 · Estratégia 26,36%"],
  ["Matemática", "Estatística e leitura de gráficos", "alta", 11.2, "Interpretação de gráficos/tabelas, média, moda, mediana.", "Aprova Total 2016–2025"],
  ["Matemática", "Funções", "alta", 10.2, "Afim e quadrática dominam. Exponencial e log aparecem menos.", "Aprova Total 11,2% · Estratégia 10,11%"],
  ["Matemática", "Geometria espacial", "media", 11.2, "Prismas e cilindros mais que pirâmides/esferas/cones.", "Aprova Total 2016–2025"],
  ["Matemática", "Geometria plana", "media", 7.7, "Áreas, polígonos, Teorema de Pitágoras.", "Aprova Total 2016–2025"],
  ["Matemática", "Probabilidade", "media", 4.1, "Espaço amostral e casos favoráveis.", "Estratégia Vestibulares"],
  ["Matemática", "Análise combinatória", "media", 2.05, "Assaad diverge: 2–3 questões/ano, alta complexidade.", "Estratégia · Assaad"],
  ["Matemática", "Progressões (PA/PG)", "baixa", 2.47, "", "Estratégia Vestibulares"],
  ["Matemática", "Trigonometria", "baixa", 0.42, "Somando funções trig. e arcos, ainda baixíssima.", "Estratégia Vestibulares"],
  ["Matemática", "Matrizes e determinantes", "baixa", 0.21, "A menor incidência da Matemática — mas baixa complexidade quando cai.", "Estratégia · Assaad"],

  ["Biologia", "Ecologia", "alta", 26, "Impactos ambientais >> ciclos biogeoquímicos > relações ecológicas, biomas.", "Aprova Total 26% · Estratégia 37,42%"],
  ["Biologia", "Fisiologia humana", "media", 7.7, "Sistemas digestório, circulatório, endócrino.", "Aprova Total · Estratégia"],
  ["Biologia", "Citologia / membrana plasmática", "media", 9.32, "2º lugar na Estratégia; Aprova não rankeia — categorização diferente.", "Estratégia Vestibulares"],
  ["Biologia", "Bioenergética / metabolismo", "media", 7.1, "Respiração celular > fotossíntese > fermentação.", "Aprova Total 2016–2025"],
  ["Biologia", "Evolução", "media", 7.45, "Teorias evolutivas, especiação.", "Estratégia Vestibulares"],
  ["Biologia", "Botânica", "media", 7.1, "", "Aprova Total 2016–2025"],
  ["Biologia", "Zoologia", "media", 8.3, "Estratégia mede só 2,8% — categorização diverge.", "Aprova Total · Estratégia"],
  ["Biologia", "Microbiologia / doenças", "media", 6.5, "Vacinas, soros, doenças virais.", "Aprova Total 2016–2025"],
  ["Biologia", "Genética", "baixa", 3.57, "Baixa em volume, alta complexidade: Mendel, heredogramas, Hardy-Weinberg.", "Estratégia · Assaad"],
  ["Biologia", "Histologia", "baixa", 1.24, "", "Estratégia Vestibulares"],
  ["Biologia", "Reprodução", "baixa", 0.93, "", "Estratégia Vestibulares"],
  ["Biologia", "Classificação / taxonomia", "baixa", 0.62, "", "Estratégia Vestibulares"],
  ["Biologia", "Vírus (isolado)", "baixa", 0.62, "", "Estratégia Vestibulares"],
  ["Biologia", "Embriologia", "baixa", 0.47, "", "Estratégia Vestibulares"],

  ["Física", "Eletrodinâmica", "alta", 21.1, "Circuitos/resistores >> potência elétrica > 1ª Lei de Ohm. Chuveiro, kWh.", "Aprova Total 21,1% · Estratégia 19,44%"],
  ["Física", "Termologia", "alta", 16.0, "Transmissão de calor, calor sensível, potência térmica, 2ª lei.", "Aprova Total 16% · Estratégia 13,17%"],
  ["Física", "Ondulatória", "alta", 13.7, "Fenômenos ondulatórios, equação fundamental, Doppler.", "Aprova Total 13,7% · Estratégia 14,69%"],
  ["Física", "Mecânica / Cinemática", "media", 11.4, "MU, MUV, Torricelli, Newton, trabalho/energia.", "Aprova (cinem.) 11,4% · Estratégia (agregada) 26,13%"],
  ["Física", "Óptica", "media", 9.1, "Refração, reflexão, lentes/espelhos, olho humano.", "Aprova Total 9,1% · Estratégia 6,05%"],
  ["Física", "Eletromagnetismo", "baixa", 2.81, "No máximo 1 questão — priorize só mirando nota alta.", "Estratégia · Assaad"],
  ["Física", "Física moderna", "baixa", 1.73, "", "Estratégia Vestibulares"],
  ["Física", "Eletrostática / gravitação / hidrostática", "baixa", null, "Baixas isoladamente em todas as fontes.", "Aprova / Estratégia"],

  ["Química", "Química geral / propriedades da matéria", "alta", 32.91, "Forças intermoleculares, propriedades, separação de misturas.", "Estratégia (macro) · Aprova 8,6%+6,6%"],
  ["Química", "Físico-química", "alta", 30.19, "Estequiometria (7,9%), eletroquímica (6,6–8,4%), termoquímica, equilíbrio.", "Estratégia (macro) · Aprova Total"],
  ["Química", "Química orgânica", "alta", 16.77, "Propriedades (6,6%), introdução, reações. Um dos mais incidentes segundo Assaad.", "Estratégia 16,77% · Aprova 6,6%"],
  ["Química", "Química ambiental", "alta", 14.68, "Efeito estufa, chuva ácida, camada de ozônio, poluição.", "Estratégia Vestibulares"],
  ["Química", "Funções inorgânicas", "media", 6.6, "Ácidos, bases, sais, neutralização.", "Aprova Total 2016–2025"],
  ["Química", "Equilíbrio, soluções e termoquímica", "media", null, "Hidrólise salina, pH, titulação, Lei de Hess, cinética.", "Estratégia Vestibulares"],
  ["Química", "Reações orgânicas avançadas", "baixa", null, "Média-alta incidência mas altíssima complexidade — a mais difícil da prova.", "Assaad"],
  ["Química", "Eletroquímica com Lei de Faraday", "baixa", null, "Cálculo de eletrólise — alta complexidade quando cai.", "Assaad"],
  ["Química", "Coligativas / radioatividade / isomeria / gases / Kps", "baixa", null, "Baixas isoladamente em todas as fontes.", "Estratégia / Aprova Total"],

  ["Linguagens", "Gêneros textuais e interpretação", "alta", 44.1, "Interpretação contextualizada — não gramática isolada.", "Aprova Total 44,1% · SAS: maior tema"],
  ["Linguagens", "Inglês — interpretação/compreensão", "alta", 93.6, "Domina esmagadoramente sobre vocabulário e coesão.", "Aprova Total 93,6% · Estratégia 80,95%"],
  ["Linguagens", "Literatura contemporânea", "alta", 30.8, "O ENEM migrou do clássico para o contemporâneo.", "Aprova Total 2016–2025"],
  ["Linguagens", "Artes / manifestações artísticas", "alta", 21.2, "", "Aprova Total 2016–2025"],
  ["Linguagens", "Modernismo", "alta", 19.9, "", "Aprova Total 2016–2025"],
  ["Linguagens", "Introdução à Língua Portuguesa", "media", 22.1, "", "Aprova Total 2022"],
  ["Linguagens", "Escolas literárias", "media", 13.0, "", "Aprova Total 2016–2025"],
  ["Linguagens", "Variação linguística", "media", 10.7, "Linguagem culta vs. coloquial.", "Aprova Total 2016–2025"],
  ["Linguagens", "Poesia", "media", 8.9, "", "Aprova Total 2016–2025"],
  ["Linguagens", "Funções da linguagem", "media", 5.9, "", "Aprova Total 2016–2025"],
  ["Linguagens", "Inglês — vocabulário e coesão", "baixa", 6.4, "", "Aprova 6,4% · Estratégia 10,88%"],
  ["Linguagens", "Teoria literária pura / gramática descontextualizada", "baixa", 0.56, "O ENEM quase nunca cobra regra isolada sem contexto.", "Estratégia Vestibulares"],

  ["Humanas", "Brasil Colônia", "alta", 11.8, "Tema nº1 de História segundo o SAS.", "Aprova Total 11,8% · SAS/CNN nº1"],
  ["Humanas", "Era Vargas / Estado Novo / Populismo", "alta", 10.3, "", "Aprova Total 2016–2025"],
  ["Humanas", "Idade Média", "alta", 10.3, "", "Aprova Total 2016–2025"],
  ["Humanas", "Idade Moderna / Grandes Navegações", "alta", 9.6, "", "Aprova Total 2016–2025"],
  ["Humanas", "Tempo Presente / atualidades", "alta", 9.6, "", "Aprova Total 2016–2025"],
  ["Humanas", "Idade Contemporânea (revoluções, guerras)", "alta", null, "Bloco de altíssima recorrência segundo o SAS.", "SAS/CNN Brasil"],
  ["Humanas", "População e demografia", "alta", 15.48, "Tema nº1 de Geografia na Estratégia.", "Estratégia Vestibulares"],
  ["Humanas", "Questões ambientais", "alta", 13.16, "", "Estratégia Vestibulares"],
  ["Humanas", "Espaço agrário", "alta", 12.4, "", "Aprova Total 12,4% · Estratégia 13,47%"],
  ["Humanas", "Espaço urbano / urbanização", "alta", 11.8, "", "Aprova Total 2016–2025"],
  ["Humanas", "Geopolítica / globalização", "alta", 11.2, "", "Aprova Total 2016–2025"],
  ["Humanas", "Filosofia Antiga / Grega", "alta", 28.1, "Sócrates, Platão, Aristóteles.", "Aprova Total 2016–2025"],
  ["Humanas", "Política e Ética (Filosofia)", "alta", 24.84, "Recorte temático da Estratégia.", "Estratégia Vestibulares"],
  ["Humanas", "Filosofia Moderna", "alta", 18.8, "Descartes, racionalismo/empirismo.", "Aprova Total 2016–2025"],
  ["Humanas", "Cultura e sociedade (Sociologia)", "alta", 19, "Indústria cultural, patrimônio, etnocentrismo.", "Aprova Total 2016–2025"],
  ["Humanas", "Movimentos sociais (Sociologia)", "alta", 18.1, "Feminismo, movimento negro.", "Aprova Total 2016–2025"],
  ["Humanas", "Estado e cidadania (Sociologia)", "alta", 15.2, "", "Aprova Total 2016–2025"],
  ["Humanas", "Primeira República", "media", 7.4, "", "Aprova Total 2016–2025"],
  ["Humanas", "Geologia", "media", 6.5, "", "Aprova Total 2016–2025"],
  ["Humanas", "Clima e domínios morfoclimáticos", "media", 4.7, "", "Aprova Total 2016–2025"],
  ["Humanas", "Áreas da filosofia / mal e justiça", "media", 14.1, "Foucault, Rawls.", "Estratégia Vestibulares"],
  ["Humanas", "Sociologia brasileira / contemporânea", "media", 13.3, "", "Aprova Total 2016–2025"],
  ["Humanas", "História regional / África isolada", "baixa", 0.84, "Decoreba de datas sem processo não é cobrada.", "Estratégia Vestibulares"],
  ["Humanas", "Filosofia medieval / lógica / biografias", "baixa", 1.27, "", "Estratégia Vestibulares"],
  ["Humanas", "Sociologia clássica pura (Durkheim/Weber/Marx isolados)", "baixa", 3.32, "", "Estratégia Vestibulares"],
];

export const TEMAS: Tema[] = RAW.map(([area, nome, tier, percentual, subtopicos, fonte]) => ({
  id: slugify(area, nome),
  area,
  nome,
  tier,
  percentual,
  subtopicos,
  fonte,
}));

export const AREAS: Area[] = ["Linguagens", "Humanas", "Matemática", "Biologia", "Física", "Química"];

export const AREA_GRUPO: Record<Area, "Dia 1" | "Dia 2"> = {
  Linguagens: "Dia 1",
  Humanas: "Dia 1",
  Matemática: "Dia 2",
  Biologia: "Dia 2",
  Física: "Dia 2",
  Química: "Dia 2",
};

export function temasPorArea(area: Area): Tema[] {
  return TEMAS.filter((t) => t.area === area);
}

export function getTema(id: string): Tema | undefined {
  return TEMAS.find((t) => t.id === id);
}

export const TIER_WEIGHT: Record<Tier, number> = { alta: 3, media: 2, baixa: 1 };
export const TIER_LABEL: Record<Tier, string> = { alta: "Alta", media: "Média", baixa: "Baixa" };
