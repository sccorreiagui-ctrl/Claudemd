import { useState } from "react";
import { CheckCircle2 } from "lucide-react";
import type { ErrorCategory } from "../types";
import { ERROR_CATEGORY_LABEL, ERROR_CATEGORY_ORDER } from "../types";
import { AREAS, TEMAS, temasPorArea } from "../data/temas";
import { useStore } from "../store/store";
import { applyQuestionLog, initialTemaState } from "../lib/srs";
import { todayISO, formatDateBR } from "../lib/date";
import { Button } from "./ui";

export function Counter({
  value,
  onChange,
  tone,
}: {
  value: number;
  onChange: (n: number) => void;
  tone: "mint" | "signal";
}) {
  const toneClass = tone === "mint" ? "text-mint-soft" : "text-signal-soft";
  return (
    <div className="flex items-center gap-2 bg-base-800 border border-white/10 rounded-xl px-2 py-1.5">
      <button
        type="button"
        onClick={() => onChange(Math.max(0, value - 1))}
        className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-base-200 font-medium"
      >
        −
      </button>
      <span className={`num flex-1 text-center font-semibold ${toneClass}`}>{value}</span>
      <button
        type="button"
        onClick={() => onChange(value + 1)}
        className="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/10 text-base-200 font-medium"
      >
        +
      </button>
    </div>
  );
}

export function QuestionLogForm({
  defaultTemaId,
  onLogged,
  submitLabel = "Registrar lote",
}: {
  defaultTemaId?: string;
  onLogged?: () => void;
  submitLabel?: string;
}) {
  const temaStates = useStore((s) => s.temaStates);
  const logQuestions = useStore((s) => s.logQuestions);
  const registerActivity = useStore((s) => s.registerActivity);

  const [temaId, setTemaId] = useState(defaultTemaId ?? TEMAS[0].id);
  const [date, setDate] = useState(todayISO());
  const [acertos, setAcertos] = useState(0);
  const [erros, setErros] = useState(0);
  const [errorCats, setErrorCats] = useState<ErrorCategory[]>([]);
  const [result, setResult] = useState<{ nextReview: string; accuracy: number } | null>(null);

  function setErrosCount(n: number) {
    const clamped = Math.max(0, n);
    setErros(clamped);
    setErrorCats((prev) => {
      const next = [...prev];
      while (next.length < clamped) next.push("conteudo");
      return next.slice(0, clamped);
    });
  }

  function submit() {
    if (acertos + erros === 0) return;
    const prevState = temaStates[temaId] ?? initialTemaState(temaId);
    const nextState = applyQuestionLog(prevState, { date, acertos, erros });
    logQuestions({ temaId, date, acertos, erros, errorCategories: errorCats });
    registerActivity(date);
    const accuracy = Math.round((acertos / (acertos + erros)) * 100);
    setResult({ nextReview: formatDateBR(nextState.nextReviewDate!), accuracy });
    setAcertos(0);
    setErros(0);
    setErrorCats([]);
    onLogged?.();
  }

  const selectedTema = TEMAS.find((t) => t.id === temaId)!;

  return (
    <div className="space-y-4">
      <div>
        <label className="text-xs text-base-400 block mb-1.5">Tema</label>
        <select
          value={temaId}
          onChange={(e) => setTemaId(e.target.value)}
          className="w-full bg-base-800 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-base-100 focus:outline-none focus:ring-2 focus:ring-signal/40"
        >
          {AREAS.map((area) => (
            <optgroup key={area} label={area}>
              {temasPorArea(area).map((t) => (
                <option key={t.id} value={t.id}>
                  {t.nome}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="col-span-2">
          <label className="text-xs text-base-400 block mb-1.5">Data</label>
          <input
            type="date"
            value={date}
            max={todayISO()}
            onChange={(e) => setDate(e.target.value)}
            className="w-full bg-base-800 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-base-100 num focus:outline-none focus:ring-2 focus:ring-signal/40"
          />
        </div>
        <div>
          <label className="text-xs text-base-400 block mb-1.5">Acertos</label>
          <Counter value={acertos} onChange={setAcertos} tone="mint" />
        </div>
        <div>
          <label className="text-xs text-base-400 block mb-1.5">Erros</label>
          <Counter value={erros} onChange={setErrosCount} tone="signal" />
        </div>
      </div>

      {erros > 0 && (
        <div className="space-y-2 pt-2 border-t border-white/[0.06]">
          <label className="text-xs text-base-400 block">Por que errou cada uma?</label>
          {errorCats.map((cat, i) => (
            <div key={i} className="flex items-center gap-2">
              <span className="text-[10px] num text-base-500 w-5">#{i + 1}</span>
              <select
                value={cat}
                onChange={(e) => {
                  const next = [...errorCats];
                  next[i] = e.target.value as ErrorCategory;
                  setErrorCats(next);
                }}
                className="flex-1 bg-base-800 border border-white/10 rounded-lg px-2.5 py-2 text-xs text-base-100 focus:outline-none focus:ring-2 focus:ring-signal/40"
              >
                {ERROR_CATEGORY_ORDER.map((c) => (
                  <option key={c} value={c}>
                    {ERROR_CATEGORY_LABEL[c]}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      )}

      <Button className="w-full" onClick={submit} disabled={acertos + erros === 0}>
        {submitLabel} · {selectedTema.nome}
      </Button>

      {result && (
        <div className="flex items-center gap-2 bg-mint/10 border border-mint/25 rounded-xl px-3 py-2.5 animate-pop-in">
          <CheckCircle2 size={16} className="text-mint-soft shrink-0" />
          <p className="text-xs text-base-200">
            Registrado — {result.accuracy}% de acerto. Próxima revisão agendada para{" "}
            <span className="num text-mint-soft">{result.nextReview}</span>.
          </p>
        </div>
      )}
    </div>
  );
}
