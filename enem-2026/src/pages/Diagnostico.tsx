import { useMemo, useState } from "react";
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";
import { Plus, Trash2, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { TEMAS } from "../data/temas";
import { useStore } from "../store/store";
import { worstTemas, errorCategoryDistribution, accuracyTrend, globalAccuracy, totalQuestoesRespondidas } from "../lib/stats";
import { ERROR_CATEGORY_LABEL } from "../types";
import { formatDateShortBR, formatDateBR } from "../lib/date";
import { Card, SectionTitle, Button, Sheet, EmptyState } from "../components/ui";
import { QuestionLogForm } from "../components/QuestionLogForm";

export function Diagnostico() {
  const logs = useStore((s) => s.questionLogs);
  const deleteLog = useStore((s) => s.deleteQuestionLog);
  const [logOpen, setLogOpen] = useState(false);

  const worst = useMemo(() => worstTemas(TEMAS, logs), [logs]);
  const errorDist = useMemo(() => errorCategoryDistribution(logs), [logs]);
  const trend = useMemo(() => accuracyTrend(logs), [logs]);
  const globalAcc = globalAccuracy(logs);
  const totalQ = totalQuestoesRespondidas(logs);

  const trendDirection = useMemo(() => {
    if (trend.length < 4) return null;
    const mid = Math.floor(trend.length / 2);
    const first = trend.slice(0, mid).reduce((s, p) => s + p.accuracy, 0) / mid;
    const second = trend.slice(mid).reduce((s, p) => s + p.accuracy, 0) / (trend.length - mid);
    const diff = second - first;
    if (diff > 4) return "subindo";
    if (diff < -4) return "caindo";
    return "estagnada";
  }, [trend]);

  const maxErrorCount = Math.max(1, ...errorDist.map((d) => d.count));

  return (
    <div className="space-y-5 animate-slide-up">
      <SectionTitle
        eyebrow="Error log categorizado"
        title="Diagnóstico"
        right={
          <Button size="sm" onClick={() => setLogOpen(true)}>
            <Plus size={14} /> Log rápido
          </Button>
        }
      />

      {logs.length === 0 ? (
        <Card className="p-2">
          <EmptyState
            title="Nenhum registro ainda"
            description="Registre seu primeiro lote de questões pra começar o diagnóstico. Poucos toques, sem fricção."
          />
        </Card>
      ) : (
        <>
          <Card className="p-4">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <div className="num text-2xl font-semibold text-base-50">{totalQ}</div>
                <div className="text-[11px] text-base-400 uppercase mt-1">Questões</div>
              </div>
              <div>
                <div className="num text-2xl font-semibold text-base-50">{globalAcc}%</div>
                <div className="text-[11px] text-base-400 uppercase mt-1">Acerto global</div>
              </div>
              <div className="flex flex-col justify-center">
                {trendDirection === "subindo" && (
                  <div className="flex items-center gap-1.5 text-mint-soft">
                    <TrendingUp size={18} />
                    <span className="text-sm font-medium">Subindo</span>
                  </div>
                )}
                {trendDirection === "caindo" && (
                  <div className="flex items-center gap-1.5 text-signal-soft">
                    <TrendingDown size={18} />
                    <span className="text-sm font-medium">Caindo</span>
                  </div>
                )}
                {trendDirection === "estagnada" && (
                  <div className="flex items-center gap-1.5 text-gold-soft">
                    <Minus size={18} />
                    <span className="text-sm font-medium">Estagnada</span>
                  </div>
                )}
                {!trendDirection && <span className="text-xs text-base-500">Poucos dados</span>}
                <div className="text-[11px] text-base-400 uppercase mt-1">Tendência</div>
              </div>
            </div>
          </Card>

          {trend.length >= 2 && (
            <Card className="p-4">
              <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
                Evolução da taxa de acerto
              </div>
              <div className="h-40 -ml-2">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trend}>
                    <defs>
                      <linearGradient id="accGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#3ddc97" stopOpacity={0.35} />
                        <stop offset="100%" stopColor="#3ddc97" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis
                      dataKey="date"
                      tickFormatter={formatDateShortBR}
                      stroke="#5c7086"
                      fontSize={10}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis domain={[0, 100]} stroke="#5c7086" fontSize={10} tickLine={false} axisLine={false} width={28} />
                    <Tooltip
                      contentStyle={{ background: "#0e141d", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 10, fontSize: 12 }}
                      labelFormatter={(v) => formatDateBR(v as string)}
                      formatter={(v: number) => [`${v}%`, "Acerto"]}
                    />
                    <Area type="monotone" dataKey="accuracy" stroke="#3ddc97" strokeWidth={2} fill="url(#accGrad)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          <Card className="p-4">
            <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
              Categoria de erro mais recorrente
            </div>
            <div className="space-y-2.5">
              {errorDist.map((d) => (
                <div key={d.category} className="flex items-center gap-3">
                  <span className="text-xs text-base-300 w-32 shrink-0">{ERROR_CATEGORY_LABEL[d.category]}</span>
                  <div className="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-signal"
                      style={{ width: `${(d.count / maxErrorCount) * 100}%` }}
                    />
                  </div>
                  <span className="num text-xs text-base-400 w-10 text-right">{d.count}</span>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
              Temas que você mais erra
            </div>
            {worst.length === 0 ? (
              <p className="text-sm text-base-500">
                Registre pelo menos 3 questões de um tema pra ele entrar no ranking.
              </p>
            ) : (
              <div className="space-y-2.5">
                {worst.slice(0, 8).map((w) => (
                  <div key={w.temaId} className="flex items-center gap-3">
                    <div className="min-w-0 flex-1">
                      <div className="text-xs text-base-200 font-medium truncate">{w.temaNome}</div>
                      <div className="text-[10px] text-base-500">{w.area}</div>
                    </div>
                    <div className="w-20 h-1.5 rounded-full bg-white/5 overflow-hidden shrink-0">
                      <div
                        className={`h-full rounded-full ${w.accuracy < 0.5 ? "bg-signal" : "bg-gold"}`}
                        style={{ width: `${w.accuracy * 100}%` }}
                      />
                    </div>
                    <span className="num text-xs text-base-300 w-10 text-right shrink-0">
                      {Math.round(w.accuracy * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-4">
            <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">Registros recentes</div>
            <div className="space-y-1">
              {[...logs]
                .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
                .slice(0, 12)
                .map((log) => {
                  const tema = TEMAS.find((t) => t.id === log.temaId);
                  return (
                    <div key={log.id} className="flex items-center gap-2 py-1.5 border-b border-white/[0.04] last:border-0">
                      <span className="text-[10px] num text-base-500 w-14 shrink-0">{formatDateShortBR(log.date)}</span>
                      <span className="text-xs text-base-200 flex-1 truncate">{tema?.nome ?? log.temaId}</span>
                      <span className="num text-[11px] text-mint-soft">{log.acertos}✓</span>
                      <span className="num text-[11px] text-signal-soft">{log.erros}✗</span>
                      <button
                        onClick={() => deleteLog(log.id)}
                        className="text-base-500 hover:text-signal-soft p-1"
                        aria-label="Remover registro"
                      >
                        <Trash2 size={13} />
                      </button>
                    </div>
                  );
                })}
            </div>
          </Card>
        </>
      )}

      <Sheet open={logOpen} onClose={() => setLogOpen(false)} title="Log rápido de questões">
        <QuestionLogForm onLogged={() => setLogOpen(false)} submitLabel="Registrar" />
      </Sheet>
    </div>
  );
}
