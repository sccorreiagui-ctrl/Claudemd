import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Flame, ArrowRight, AlertTriangle } from "lucide-react";
import { useStore } from "../store/store";
import { AREAS, TEMAS, temasPorArea } from "../data/temas";
import { countdownTo, ENEM_DIA1, ENEM_DIA2, todayISO, isOverdue } from "../lib/date";
import { areaMastery, overallMastery } from "../lib/stats";
import { suggestNextTema } from "../lib/srs";
import { Card, ProgressRing, Stat, Button } from "../components/ui";

const AREA_COLOR: Record<string, string> = {
  Linguagens: "#ff5a3c",
  Humanas: "#e8b84b",
  Matemática: "#3ba7e8",
  Biologia: "#3ddc97",
  Física: "#f2cd76",
  Química: "#6fc0f0",
};

export function Home() {
  const temaStates = useStore((s) => s.temaStates);
  const streakFn = useStore((s) => s.streak);
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const target = now < ENEM_DIA1 ? ENEM_DIA1 : ENEM_DIA2;
  const label = now < ENEM_DIA1 ? "Dia 1 · Linguagens + Humanas + Redação" : "Dia 2 · Natureza + Matemática";
  const cd = countdownTo(target, now);

  const mastery = overallMastery(TEMAS, temaStates);
  const streak = streakFn();

  const overdueCount = TEMAS.filter((t) => isOverdue(temaStates[t.id]?.nextReviewDate ?? null, todayISO())).length;
  const suggestion = suggestNextTema(TEMAS, temaStates);

  return (
    <div className="space-y-5 animate-slide-up">
      <Card className="p-6 relative overflow-hidden">
        <div
          className="absolute -top-24 -right-24 w-64 h-64 rounded-full opacity-30 blur-3xl pointer-events-none"
          style={{ background: "radial-gradient(circle, #ff5a3c, transparent 70%)" }}
        />
        <div className="relative">
          <div className="text-[11px] font-mono uppercase tracking-[0.16em] text-signal-soft mb-2">
            {label}
          </div>
          <div className="flex items-end gap-1 mb-1">
            <span className="num text-6xl sm:text-7xl font-bold text-base-50 leading-none">{cd.days}</span>
            <span className="text-base-300 font-medium mb-1.5 ml-1">dias</span>
          </div>
          <div className="flex items-center gap-3 num text-sm text-base-400 mb-5">
            <span>{String(cd.hours).padStart(2, "0")}h</span>
            <span>{String(cd.minutes).padStart(2, "0")}m</span>
            <span>{String(cd.seconds).padStart(2, "0")}s</span>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/[0.06]">
            <div className="flex items-center gap-3">
              <ProgressRing value={mastery} size={56} stroke={5} color="#ff5a3c" />
              <div>
                <div className="num text-base-50 font-semibold text-sm">{mastery}%</div>
                <div className="text-[10px] text-base-400 uppercase tracking-wide leading-tight">
                  Domínio
                  <br />
                  operacional
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Flame size={22} className={streak > 0 ? "text-signal-soft" : "text-base-500"} />
              <div>
                <div className="num text-base-50 font-semibold text-sm">{streak}</div>
                <div className="text-[10px] text-base-400 uppercase tracking-wide leading-tight">
                  Dias
                  <br />
                  seguidos
                </div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle size={20} className={overdueCount > 0 ? "text-gold-soft" : "text-base-500"} />
              <div>
                <div className="num text-base-50 font-semibold text-sm">{overdueCount}</div>
                <div className="text-[10px] text-base-400 uppercase tracking-wide leading-tight">
                  Revisões
                  <br />
                  vencidas
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {suggestion && (
        <Card className="p-4 flex items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-0.5">
              {suggestion.reason === "revisao_vencida"
                ? `Revisão vencida há ${suggestion.overdueDays}d`
                : suggestion.reason === "novo"
                ? "Próximo do Núcleo S"
                : "Reforço"}
            </div>
            <div className="font-display font-semibold text-base-50 truncate">{suggestion.tema.nome}</div>
            <div className="text-xs text-base-400">{suggestion.tema.area}</div>
          </div>
          <Link to="/ciclo">
            <Button size="sm">
              Estudar <ArrowRight size={14} />
            </Button>
          </Link>
        </Card>
      )}

      <div>
        <div className="text-[11px] font-mono uppercase tracking-[0.14em] text-base-400 mb-3">
          Domínio por área
        </div>
        <div className="grid grid-cols-3 sm:grid-cols-6 gap-3">
          {AREAS.map((area) => {
            const m = areaMastery(area, temaStates);
            const count = temasPorArea(area).length;
            return (
              <Link
                key={area}
                to="/conteudo"
                className="panel rounded-2xl p-3 flex flex-col items-center gap-2 hover:bg-white/[0.04] transition-colors"
              >
                <ProgressRing value={m} size={52} stroke={5} color={AREA_COLOR[area]} />
                <div className="text-center">
                  <div className="text-[11px] font-medium text-base-100 leading-tight">{area}</div>
                  <div className="text-[10px] text-base-500 num">{count} temas</div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      <Card className="p-4">
        <div className="grid grid-cols-3 gap-4">
          <Stat label="Temas mapeados" value={TEMAS.length} />
          <Stat
            label="Alta recorrência"
            value={TEMAS.filter((t) => t.tier === "alta").length}
            tone="signal"
          />
          <Stat
            label="Dominados"
            value={Object.values(temaStates).filter((s) => s.status === "dominado").length}
            tone="mint"
          />
        </div>
      </Card>
    </div>
  );
}
