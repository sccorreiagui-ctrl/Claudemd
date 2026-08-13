import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { ErrorCategory, QuestionLog, Simulado, TemaState } from "../types";
import { TEMAS } from "../data/temas";
import { applyQuestionLog, initialTemaState } from "../lib/srs";
import { computeStreak, todayISO } from "../lib/date";

function uid(): string {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

interface StoreState {
  temaStates: Record<string, TemaState>;
  questionLogs: QuestionLog[];
  simulados: Simulado[];
  activityDates: string[];

  logQuestions: (input: {
    temaId: string;
    date: string;
    acertos: number;
    erros: number;
    errorCategories: ErrorCategory[];
  }) => void;

  logSimulado: (input: Omit<Simulado, "id">) => void;
  deleteSimulado: (id: string) => void;
  deleteQuestionLog: (id: string) => void;
  resetTema: (temaId: string) => void;
  registerActivity: (date?: string) => void;

  getTemaState: (temaId: string) => TemaState;
  streak: () => number;
}

export const useStore = create<StoreState>()(
  persist(
    (set, get) => ({
      temaStates: {},
      questionLogs: [],
      simulados: [],
      activityDates: [],

      getTemaState: (temaId: string) => {
        return get().temaStates[temaId] ?? initialTemaState(temaId);
      },

      registerActivity: (date = todayISO()) => {
        set((s) => (s.activityDates.includes(date) ? s : { activityDates: [...s.activityDates, date] }));
      },

      logQuestions: ({ temaId, date, acertos, erros, errorCategories }) => {
        const log: QuestionLog = {
          id: uid(),
          temaId,
          date,
          acertos,
          erros,
          errorCategories,
          createdAt: new Date().toISOString(),
        };
        set((s) => {
          const prevState = s.temaStates[temaId] ?? initialTemaState(temaId);
          const nextState = applyQuestionLog(prevState, { date, acertos, erros });
          return {
            questionLogs: [...s.questionLogs, log],
            temaStates: { ...s.temaStates, [temaId]: nextState },
            activityDates: s.activityDates.includes(date) ? s.activityDates : [...s.activityDates, date],
          };
        });
      },

      logSimulado: (input) => {
        const simulado: Simulado = { ...input, id: uid() };
        set((s) => ({
          simulados: [...s.simulados, simulado],
          activityDates: s.activityDates.includes(input.date) ? s.activityDates : [...s.activityDates, input.date],
        }));
      },

      deleteSimulado: (id) => set((s) => ({ simulados: s.simulados.filter((sim) => sim.id !== id) })),

      deleteQuestionLog: (id) =>
        set((s) => ({ questionLogs: s.questionLogs.filter((l) => l.id !== id) })),

      resetTema: (temaId) =>
        set((s) => {
          const { [temaId]: _removed, ...rest } = s.temaStates;
          return {
            temaStates: rest,
            questionLogs: s.questionLogs.filter((l) => l.temaId !== temaId),
          };
        }),

      streak: () => computeStreak(get().activityDates),
    }),
    {
      name: "enem-2026-reta-final",
      version: 1,
    }
  )
);

export function allTemaIds(): string[] {
  return TEMAS.map((t) => t.id);
}
