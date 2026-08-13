import type { Area, ErrorCategory, QuestionLog, Simulado, Tema, TemaState } from "../types";
import { ERROR_CATEGORY_ORDER } from "../types";
import { TIER_WEIGHT, temasPorArea } from "../data/temas";
import { masteryScore } from "./srs";

export function overallMastery(temas: Tema[], states: Record<string, TemaState>): number {
  if (temas.length === 0) return 0;
  let weightedSum = 0;
  let weightTotal = 0;
  for (const tema of temas) {
    const w = TIER_WEIGHT[tema.tier];
    weightedSum += masteryScore(states[tema.id]) * w;
    weightTotal += w;
  }
  return weightTotal > 0 ? Math.round(weightedSum / weightTotal) : 0;
}

export function areaMastery(area: Area, states: Record<string, TemaState>): number {
  return overallMastery(temasPorArea(area), states);
}

export interface TemaAccuracy {
  temaId: string;
  temaNome: string;
  area: Area;
  acertos: number;
  erros: number;
  total: number;
  accuracy: number;
}

/** Temas ordenados do pior desempenho pro melhor (mínimo de tentativas pra entrar no ranking). */
export function worstTemas(temas: Tema[], logs: QuestionLog[], minTentativas = 3): TemaAccuracy[] {
  const byTema = new Map<string, { acertos: number; erros: number }>();
  for (const log of logs) {
    const cur = byTema.get(log.temaId) ?? { acertos: 0, erros: 0 };
    cur.acertos += log.acertos;
    cur.erros += log.erros;
    byTema.set(log.temaId, cur);
  }
  const rows: TemaAccuracy[] = [];
  for (const [temaId, { acertos, erros }] of byTema.entries()) {
    const tema = temas.find((t) => t.id === temaId);
    if (!tema) continue;
    const total = acertos + erros;
    if (total < minTentativas) continue;
    rows.push({ temaId, temaNome: tema.nome, area: tema.area, acertos, erros, total, accuracy: acertos / total });
  }
  return rows.sort((a, b) => a.accuracy - b.accuracy);
}

export interface ErrorDistributionRow {
  category: ErrorCategory;
  count: number;
  pct: number;
}

export function errorCategoryDistribution(logs: QuestionLog[]): ErrorDistributionRow[] {
  const counts: Record<ErrorCategory, number> = {
    conteudo: 0,
    interpretacao: 0,
    calculo: 0,
    tempo: 0,
    atencao: 0,
    estrategia: 0,
  };
  let totalErros = 0;
  for (const log of logs) {
    for (const cat of log.errorCategories) {
      counts[cat] += 1;
      totalErros += 1;
    }
  }
  return ERROR_CATEGORY_ORDER.map((category) => ({
    category,
    count: counts[category],
    pct: totalErros > 0 ? Math.round((counts[category] / totalErros) * 1000) / 10 : 0,
  }));
}

export interface AccuracyPoint {
  date: string;
  acertos: number;
  erros: number;
  accuracy: number;
}

/** Série temporal de acurácia agregada por dia (todos os temas, ou um específico). */
export function accuracyTrend(logs: QuestionLog[], temaId?: string): AccuracyPoint[] {
  const filtered = temaId ? logs.filter((l) => l.temaId === temaId) : logs;
  const byDate = new Map<string, { acertos: number; erros: number }>();
  for (const log of filtered) {
    const cur = byDate.get(log.date) ?? { acertos: 0, erros: 0 };
    cur.acertos += log.acertos;
    cur.erros += log.erros;
    byDate.set(log.date, cur);
  }
  return Array.from(byDate.entries())
    .map(([date, { acertos, erros }]) => ({
      date,
      acertos,
      erros,
      accuracy: acertos + erros > 0 ? Math.round((acertos / (acertos + erros)) * 100) : 0,
    }))
    .sort((a, b) => a.date.localeCompare(b.date));
}

export interface SimuladoScoreRow {
  id: string;
  date: string;
  linguagens: number;
  humanas: number;
  natureza: number;
  matematica: number;
  totalPct: number;
  tempoMinutos: number;
}

export function simuladoEvolution(simulados: Simulado[]): SimuladoScoreRow[] {
  return [...simulados]
    .sort((a, b) => a.date.localeCompare(b.date))
    .map((s) => {
      const areas = [s.linguagens, s.humanas, s.natureza, s.matematica];
      const totalAcertos = areas.reduce((sum, a) => sum + a.acertos, 0);
      const totalQuestoes = areas.reduce((sum, a) => sum + a.total, 0);
      return {
        id: s.id,
        date: s.date,
        linguagens: s.linguagens.total > 0 ? Math.round((s.linguagens.acertos / s.linguagens.total) * 100) : 0,
        humanas: s.humanas.total > 0 ? Math.round((s.humanas.acertos / s.humanas.total) * 100) : 0,
        natureza: s.natureza.total > 0 ? Math.round((s.natureza.acertos / s.natureza.total) * 100) : 0,
        matematica: s.matematica.total > 0 ? Math.round((s.matematica.acertos / s.matematica.total) * 100) : 0,
        totalPct: totalQuestoes > 0 ? Math.round((totalAcertos / totalQuestoes) * 100) : 0,
        tempoMinutos: s.tempoMinutos,
      };
    });
}

export function totalQuestoesRespondidas(logs: QuestionLog[]): number {
  return logs.reduce((sum, l) => sum + l.acertos + l.erros, 0);
}

export function globalAccuracy(logs: QuestionLog[]): number {
  const acertos = logs.reduce((sum, l) => sum + l.acertos, 0);
  const total = totalQuestoesRespondidas(logs);
  return total > 0 ? Math.round((acertos / total) * 100) : 0;
}

export function dominantErrorCategory(logs: QuestionLog[]): ErrorDistributionRow | null {
  const dist = errorCategoryDistribution(logs);
  const withCount = dist.filter((d) => d.count > 0);
  if (withCount.length === 0) return null;
  return withCount.reduce((max, d) => (d.count > max.count ? d : max), withCount[0]);
}
