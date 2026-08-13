import { useMemo, useState } from "react";
import { Lightbulb, BookOpen, PenLine, ClipboardCheck, CalendarClock } from "lucide-react";
import { TEMAS } from "../data/temas";
import { useStore } from "../store/store";
import { suggestNextTema } from "../lib/srs";
import { Card, TierBadge, SectionTitle } from "../components/ui";
import { QuestionLogForm } from "../components/QuestionLogForm";

const STEPS = [
  { icon: Lightbulb, title: "Sistema sugere o tema", desc: "Prioridade de tier + revisões vencidas." },
  { icon: BookOpen, title: "Você estuda", desc: "Aula, livro, cursinho — fora do app." },
  { icon: PenLine, title: "Você resolve questões", desc: "Prova oficial, plataforma — fora do app." },
  { icon: ClipboardCheck, title: "Você registra aqui", desc: "Acertos, erros e a causa de cada erro." },
  { icon: CalendarClock, title: "Sistema agenda a revisão", desc: "1 → 3 → 7 → 14 → 30 dias, adaptativo." },
];

export function Ciclo() {
  const temaStates = useStore((s) => s.temaStates);
  const suggestion = useMemo(() => suggestNextTema(TEMAS, temaStates), [temaStates]);
  // Congela a sugestão usada como default do formulário na montagem da página, pra não
  // remontar (e perder a confirmação) toda vez que um registro muda a sugestão em si.
  const [initialSuggestionId] = useState(() => suggestion?.tema.id);

  return (
    <div className="space-y-5 animate-slide-up">
      <SectionTitle eyebrow="Retrieval practice" title="Ciclo diário de estudo" />

      <Card className="p-4">
        <div className="flex gap-3 overflow-x-auto no-scrollbar pb-1">
          {STEPS.map((step, i) => (
            <div key={i} className="flex flex-col items-center text-center w-[92px] shrink-0">
              <div className="w-9 h-9 rounded-full bg-white/5 border border-white/10 flex items-center justify-center mb-1.5 text-base-300">
                <step.icon size={16} />
              </div>
              <div className="text-[11px] font-medium text-base-200 leading-tight">{step.title}</div>
              <div className="text-[9px] text-base-500 leading-tight mt-0.5">{step.desc}</div>
            </div>
          ))}
        </div>
      </Card>

      {suggestion && (
        <Card className="p-4">
          <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-1.5">
            {suggestion.reason === "revisao_vencida"
              ? `Sugestão · revisão vencida há ${suggestion.overdueDays}d`
              : suggestion.reason === "novo"
              ? "Sugestão · Núcleo S (alta incidência)"
              : "Sugestão · reforço"}
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-display font-semibold text-base-50">{suggestion.tema.nome}</span>
            <TierBadge tier={suggestion.tema.tier} compact />
          </div>
          <p className="text-xs text-base-400 mt-1">{suggestion.tema.area}</p>
        </Card>
      )}

      <Card className="p-4">
        <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-4">Registrar questões</div>
        <QuestionLogForm defaultTemaId={initialSuggestionId} />
      </Card>
    </div>
  );
}
