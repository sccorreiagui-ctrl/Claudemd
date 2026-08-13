import type { Tema, TemaState, TemaStatus } from "../types";
import { TIER_WEIGHT } from "../data/temas";
import { addDaysISO, daysBetween, isOverdue, todayISO } from "./date";

/** Padrão de repetição espaçada: 1 → 3 → 7 → 14 → 30 dias (Cepeda et al., 2006). */
export const INTERVALS = [1, 3, 7, 14, 30];

const ERRO_THRESHOLD = 0.7; // abaixo disso, o tema "venceu" e o intervalo reseta
const FACIL_THRESHOLD = 0.9; // acima disso, acerto fácil — intervalo cresce mais

export function initialTemaState(temaId: string): TemaState {
  return {
    temaId,
    status: "nao_iniciado",
    intervalStep: -1,
    lastReviewDate: null,
    nextReviewDate: null,
    totalAcertos: 0,
    totalErros: 0,
    history: [],
  };
}

function statusForStep(step: number): TemaStatus {
  if (step >= INTERVALS.length) return "dominado";
  if (step <= 1) return "aprendendo";
  return "revisao";
}

/**
 * Aplica um novo lote de questões (acertos/erros) ao estado de repetição espaçada
 * de um tema. Erro relevante reseta o intervalo pra 1 dia; acerto fácil pula 2
 * degraus; acerto com esforço avança 1 degrau. Ao completar todos os degraus com
 * bom desempenho, o tema vira "dominado" (revisão de manutenção a cada 30 dias).
 */
export function applyQuestionLog(
  state: TemaState,
  log: { date: string; acertos: number; erros: number }
): TemaState {
  const total = log.acertos + log.erros;
  const accuracy = total > 0 ? log.acertos / total : 0;

  const wasStarted = state.status !== "nao_iniciado";
  let step = wasStarted ? state.intervalStep : 0;

  if (wasStarted) {
    if (accuracy < ERRO_THRESHOLD) {
      step = 0;
    } else if (accuracy >= FACIL_THRESHOLD) {
      step = Math.min(step + 2, INTERVALS.length);
    } else {
      step = Math.min(step + 1, INTERVALS.length);
    }
  }

  const status = statusForStep(step);
  const nextReviewDate =
    status === "dominado"
      ? addDaysISO(log.date, 30)
      : addDaysISO(log.date, INTERVALS[step]);

  return {
    ...state,
    status,
    intervalStep: step,
    lastReviewDate: log.date,
    nextReviewDate,
    totalAcertos: state.totalAcertos + log.acertos,
    totalErros: state.totalErros + log.erros,
    history: [...state.history, { date: log.date, acertos: log.acertos, erros: log.erros }],
  };
}

export interface Suggestion {
  tema: Tema;
  reason: "revisao_vencida" | "novo" | "reforco";
  overdueDays?: number;
}

/**
 * Sugere o próximo tema de estudo combinando: revisões vencidas (prioridade
 * máxima, mais atrasada primeiro) > temas novos por tier de incidência > reforço
 * de temas já dominados há mais tempo, se não sobrar mais nada.
 */
export function suggestNextTema(
  temas: Tema[],
  states: Record<string, TemaState>,
  refISO = todayISO()
): Suggestion | null {
  if (temas.length === 0) return null;

  const overdue = temas
    .map((tema) => ({ tema, state: states[tema.id] }))
    .filter(({ state }) => state && state.status !== "dominado" && isOverdue(state.nextReviewDate, refISO))
    .sort((a, b) => {
      const daysA = daysBetween(a.state.nextReviewDate!, refISO);
      const daysB = daysBetween(b.state.nextReviewDate!, refISO);
      if (daysB !== daysA) return daysB - daysA;
      return TIER_WEIGHT[b.tema.tier] - TIER_WEIGHT[a.tema.tier];
    });

  if (overdue.length > 0) {
    const top = overdue[0];
    return {
      tema: top.tema,
      reason: "revisao_vencida",
      overdueDays: daysBetween(top.state.nextReviewDate!, refISO),
    };
  }

  const novos = temas
    .filter((tema) => !states[tema.id] || states[tema.id].status === "nao_iniciado")
    .sort((a, b) => {
      if (TIER_WEIGHT[b.tier] !== TIER_WEIGHT[a.tier]) return TIER_WEIGHT[b.tier] - TIER_WEIGHT[a.tier];
      return (b.percentual ?? 0) - (a.percentual ?? 0);
    });

  if (novos.length > 0) {
    return { tema: novos[0], reason: "novo" };
  }

  const reforco = temas
    .map((tema) => ({ tema, state: states[tema.id] }))
    .filter(({ state }) => state)
    .sort((a, b) => {
      const dateA = a.state.lastReviewDate ?? "0000-00-00";
      const dateB = b.state.lastReviewDate ?? "0000-00-00";
      return dateA.localeCompare(dateB);
    });

  if (reforco.length > 0) {
    return { tema: reforco[0].tema, reason: "reforco" };
  }

  return null;
}

/** Score de domínio 0–100 de um tema, combinando progresso no ciclo de revisão e precisão. */
export function masteryScore(state: TemaState | undefined): number {
  if (!state || state.status === "nao_iniciado") return 0;
  if (state.status === "dominado") return 100;
  const stepProgress = (state.intervalStep + 1) / (INTERVALS.length + 1);
  const total = state.totalAcertos + state.totalErros;
  const accuracy = total > 0 ? state.totalAcertos / total : 0;
  return Math.round((stepProgress * 0.7 + accuracy * 0.3) * 100);
}
