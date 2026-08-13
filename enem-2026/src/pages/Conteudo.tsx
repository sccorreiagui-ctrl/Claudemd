import { useMemo, useState } from "react";
import { CheckCircle2, Circle, Clock3, BookOpen } from "lucide-react";
import type { Area, Tema } from "../types";
import { AREAS, temasPorArea, TIER_WEIGHT } from "../data/temas";
import { useStore } from "../store/store";
import { masteryScore } from "../lib/srs";
import { isOverdue, todayISO, formatDateBR } from "../lib/date";
import { areaMastery } from "../lib/stats";
import { Card, ProgressRing, TierBadge, Sheet, SectionTitle } from "../components/ui";

const STATUS_ICON: Record<string, JSX.Element> = {
  nao_iniciado: <Circle size={15} className="text-base-500" />,
  aprendendo: <BookOpen size={15} className="text-gold-soft" />,
  revisao: <Clock3 size={15} className="text-azure-soft" />,
  dominado: <CheckCircle2 size={15} className="text-mint-soft" />,
};

const STATUS_LABEL: Record<string, string> = {
  nao_iniciado: "Não iniciado",
  aprendendo: "Aprendendo",
  revisao: "Em revisão",
  dominado: "Dominado",
};

export function Conteudo() {
  const [openArea, setOpenArea] = useState<Area | null>(AREAS[0]);
  const [selected, setSelected] = useState<Tema | null>(null);
  const temaStates = useStore((s) => s.temaStates);

  return (
    <div className="space-y-4 animate-slide-up">
      <SectionTitle
        eyebrow="Núcleo priorizado"
        title="Mapa de conteúdo"
        right={<span className="text-xs text-base-400">78 temas · 6 áreas</span>}
      />
      <p className="text-sm text-base-400 -mt-2">
        Ordenado por recorrência histórica. Alta prioridade primeiro — mas nada é escondido.
      </p>

      <div className="space-y-3">
        {AREAS.map((area) => {
          const temas = [...temasPorArea(area)].sort((a, b) => {
            if (TIER_WEIGHT[b.tier] !== TIER_WEIGHT[a.tier]) return TIER_WEIGHT[b.tier] - TIER_WEIGHT[a.tier];
            return (b.percentual ?? 0) - (a.percentual ?? 0);
          });
          const isOpen = openArea === area;
          const mastery = areaMastery(area, temaStates);
          return (
            <Card key={area} className="overflow-hidden">
              <button
                onClick={() => setOpenArea(isOpen ? null : area)}
                className="w-full flex items-center justify-between gap-3 p-4"
              >
                <div className="flex items-center gap-3">
                  <ProgressRing value={mastery} size={40} stroke={4} />
                  <div className="text-left">
                    <div className="font-display font-semibold text-base-50">{area}</div>
                    <div className="text-[11px] text-base-400 num">{temas.length} temas</div>
                  </div>
                </div>
                <span className={`text-base-400 transition-transform ${isOpen ? "rotate-90" : ""}`}>›</span>
              </button>
              {isOpen && (
                <div className="border-t border-white/[0.06] divide-y divide-white/[0.05]">
                  {temas.map((tema) => {
                    const state = temaStates[tema.id];
                    const status = state?.status ?? "nao_iniciado";
                    const overdue = isOverdue(state?.nextReviewDate ?? null, todayISO()) && status !== "dominado";
                    return (
                      <button
                        key={tema.id}
                        onClick={() => setSelected(tema)}
                        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-white/[0.03] transition-colors"
                      >
                        {STATUS_ICON[status]}
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-base-100 font-medium truncate">{tema.nome}</span>
                            {overdue && (
                              <span className="text-[9px] font-mono uppercase text-gold-soft border border-gold/30 bg-gold/10 rounded-full px-1.5 py-0.5 shrink-0">
                                revisar
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-2 mt-1">
                            <TierBadge tier={tema.tier} compact />
                            {tema.percentual != null && (
                              <span className="text-[10px] num text-base-500">{tema.percentual}%</span>
                            )}
                          </div>
                        </div>
                        <span className="text-[10px] num text-base-500 shrink-0">{masteryScore(state)}%</span>
                      </button>
                    );
                  })}
                </div>
              )}
            </Card>
          );
        })}
      </div>

      <Sheet open={!!selected} onClose={() => setSelected(null)} title={selected?.nome ?? ""}>
        {selected && <TemaDetail tema={selected} />}
      </Sheet>
    </div>
  );
}

function TemaDetail({ tema }: { tema: Tema }) {
  const state = useStore((s) => s.temaStates[tema.id]);
  const status = state?.status ?? "nao_iniciado";
  const total = (state?.totalAcertos ?? 0) + (state?.totalErros ?? 0);
  const accuracy = total > 0 ? Math.round(((state?.totalAcertos ?? 0) / total) * 100) : null;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        <TierBadge tier={tema.tier} />
        <span className="text-xs text-base-400">{tema.area}</span>
        {tema.percentual != null && (
          <span className="text-xs num text-base-300">· {tema.percentual}% de incidência</span>
        )}
      </div>

      {tema.subtopicos && (
        <p className="text-sm text-base-300 leading-relaxed">{tema.subtopicos}</p>
      )}

      <div className="grid grid-cols-3 gap-3 py-3 border-y border-white/[0.06]">
        <div>
          <div className="num text-lg text-base-50 font-semibold">{masteryScore(state)}%</div>
          <div className="text-[10px] text-base-400 uppercase">Domínio</div>
        </div>
        <div>
          <div className="num text-lg text-base-50 font-semibold">{accuracy != null ? `${accuracy}%` : "—"}</div>
          <div className="text-[10px] text-base-400 uppercase">Acurácia</div>
        </div>
        <div>
          <div className="num text-lg text-base-50 font-semibold">{total}</div>
          <div className="text-[10px] text-base-400 uppercase">Questões</div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {STATUS_ICON[status]}
        <span className="text-sm text-base-200">{STATUS_LABEL[status]}</span>
        {state?.nextReviewDate && status !== "dominado" && (
          <span className="text-xs text-base-500 ml-auto">
            Próxima revisão: <span className="num">{formatDateBR(state.nextReviewDate)}</span>
          </span>
        )}
      </div>

      <div className="text-[11px] text-base-500 pt-2 border-t border-white/[0.06]">Fonte: {tema.fonte}</div>

      {state && state.history.length > 0 && (
        <div>
          <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-2">Histórico</div>
          <div className="space-y-1.5">
            {[...state.history].reverse().map((h, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <span className="text-base-400 num">{formatDateBR(h.date)}</span>
                <span className="num text-mint-soft">{h.acertos} certas</span>
                <span className="num text-signal-soft">{h.erros} erradas</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
