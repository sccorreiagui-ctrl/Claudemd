export type Area =
  | "Matemática"
  | "Biologia"
  | "Física"
  | "Química"
  | "Linguagens"
  | "Humanas";

export type Tier = "alta" | "media" | "baixa";

export interface Tema {
  id: string;
  area: Area;
  nome: string;
  tier: Tier;
  percentual: number | null;
  subtopicos: string;
  fonte: string;
}

export type ErrorCategory =
  | "conteudo"
  | "interpretacao"
  | "calculo"
  | "tempo"
  | "atencao"
  | "estrategia";

export const ERROR_CATEGORY_LABEL: Record<ErrorCategory, string> = {
  conteudo: "Falta de conteúdo",
  interpretacao: "Interpretação",
  calculo: "Cálculo/execução",
  tempo: "Gestão de tempo",
  atencao: "Distração/atenção",
  estrategia: "Estratégia",
};

export const ERROR_CATEGORY_ORDER: ErrorCategory[] = [
  "conteudo",
  "interpretacao",
  "calculo",
  "tempo",
  "atencao",
  "estrategia",
];

/** Um lote de questões resolvido fora do app e registrado depois. */
export interface QuestionLog {
  id: string;
  temaId: string;
  date: string; // ISO yyyy-mm-dd
  acertos: number;
  erros: number;
  errorCategories: ErrorCategory[]; // uma entrada por questão errada
  createdAt: string; // ISO datetime
}

export type TemaStatus = "nao_iniciado" | "aprendendo" | "revisao" | "dominado";

/** Estado de repetição espaçada de um tema. */
export interface TemaState {
  temaId: string;
  status: TemaStatus;
  intervalStep: number; // índice em INTERVALOS, -1 = não iniciado
  lastReviewDate: string | null; // ISO date
  nextReviewDate: string | null; // ISO date
  totalAcertos: number;
  totalErros: number;
  history: { date: string; acertos: number; erros: number }[];
}

export interface Simulado {
  id: string;
  date: string; // ISO date
  linguagens: { acertos: number; total: number };
  humanas: { acertos: number; total: number };
  natureza: { acertos: number; total: number };
  matematica: { acertos: number; total: number };
  tempoMinutos: number;
  observacoes?: string;
}

/** Registro leve para o streak — qualquer interação de estudo no dia. */
export interface ActivityDay {
  date: string; // ISO date
}
