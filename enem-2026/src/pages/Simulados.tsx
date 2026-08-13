import { useMemo, useState } from "react";
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from "recharts";
import { Plus, Trash2, Timer } from "lucide-react";
import type { Simulado } from "../types";
import { useStore } from "../store/store";
import { simuladoEvolution } from "../lib/stats";
import { todayISO, formatDateBR, formatDateShortBR } from "../lib/date";
import { Card, SectionTitle, Button, Sheet, EmptyState, Stat } from "../components/ui";

const AREA_FIELDS: { key: keyof Pick<Simulado, "linguagens" | "humanas" | "natureza" | "matematica">; label: string; color: string }[] = [
  { key: "linguagens", label: "Linguagens", color: "#ff5a3c" },
  { key: "humanas", label: "Humanas", color: "#e8b84b" },
  { key: "natureza", label: "Natureza", color: "#3ddc97" },
  { key: "matematica", label: "Matemática", color: "#3ba7e8" },
];

export function Simulados() {
  const simulados = useStore((s) => s.simulados);
  const logSimulado = useStore((s) => s.logSimulado);
  const deleteSimulado = useStore((s) => s.deleteSimulado);
  const registerActivity = useStore((s) => s.registerActivity);
  const [open, setOpen] = useState(false);

  const evolution = useMemo(() => simuladoEvolution(simulados), [simulados]);

  return (
    <div className="space-y-5 animate-slide-up">
      <SectionTitle
        eyebrow="Formato oficial · 13h30"
        title="Simulados"
        right={
          <Button size="sm" onClick={() => setOpen(true)}>
            <Plus size={14} /> Novo
          </Button>
        }
      />

      {simulados.length === 0 ? (
        <Card className="p-2">
          <EmptyState
            title="Nenhum simulado registrado"
            description="Meta: pelo menos 1 por mês, mais nos últimos 30 dias. Sempre cronometrado no horário e duração oficiais."
          />
        </Card>
      ) : (
        <>
          <Card className="p-4">
            <div className="grid grid-cols-3 gap-4">
              <Stat label="Simulados" value={simulados.length} />
              <Stat label="Último resultado" value={`${evolution[evolution.length - 1].totalPct}%`} tone="signal" />
              <Stat
                label="1º → último"
                value={`${evolution[0].totalPct >= 0 ? "" : ""}${evolution[evolution.length - 1].totalPct - evolution[0].totalPct >= 0 ? "+" : ""}${
                  evolution[evolution.length - 1].totalPct - evolution[0].totalPct
                }pp`}
                tone={evolution[evolution.length - 1].totalPct - evolution[0].totalPct >= 0 ? "mint" : "signal"}
              />
            </div>
          </Card>

          {evolution.length >= 2 && (
            <Card className="p-4">
              <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
                Evolução por área
              </div>
              <div className="h-56 -ml-2">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={evolution}>
                    <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />
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
                    />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    {AREA_FIELDS.map((f) => (
                      <Line
                        key={f.key}
                        type="monotone"
                        dataKey={f.key}
                        name={f.label}
                        stroke={f.color}
                        strokeWidth={2}
                        dot={{ r: 3 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          <div className="space-y-2.5">
            {[...simulados]
              .sort((a, b) => b.date.localeCompare(a.date))
              .map((s) => {
                const areas = [s.linguagens, s.humanas, s.natureza, s.matematica];
                const acertos = areas.reduce((sum, a) => sum + a.acertos, 0);
                const total = areas.reduce((sum, a) => sum + a.total, 0);
                return (
                  <Card key={s.id} className="p-4 flex items-center justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium text-base-100 num">{formatDateBR(s.date)}</div>
                      <div className="flex items-center gap-2 text-xs text-base-400 mt-1">
                        <Timer size={12} /> <span className="num">{s.tempoMinutos} min</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="num text-lg font-semibold text-base-50">
                        {total > 0 ? Math.round((acertos / total) * 100) : 0}%
                      </div>
                      <div className="text-[10px] text-base-500 num">
                        {acertos}/{total}
                      </div>
                    </div>
                    <button
                      onClick={() => deleteSimulado(s.id)}
                      className="text-base-500 hover:text-signal-soft p-1.5"
                      aria-label="Remover simulado"
                    >
                      <Trash2 size={14} />
                    </button>
                  </Card>
                );
              })}
          </div>
        </>
      )}

      <Sheet open={open} onClose={() => setOpen(false)} title="Registrar simulado">
        <SimuladoForm
          onSubmit={(data) => {
            logSimulado(data);
            registerActivity(data.date);
            setOpen(false);
          }}
        />
      </Sheet>
    </div>
  );
}

function SimuladoForm({ onSubmit }: { onSubmit: (data: Omit<Simulado, "id">) => void }) {
  const [date, setDate] = useState(todayISO());
  const [tempoMinutos, setTempoMinutos] = useState(330);
  const [scores, setScores] = useState<Record<string, { acertos: number; total: number }>>({
    linguagens: { acertos: 0, total: 45 },
    humanas: { acertos: 0, total: 45 },
    natureza: { acertos: 0, total: 45 },
    matematica: { acertos: 0, total: 45 },
  });

  function updateScore(key: string, field: "acertos" | "total", value: number) {
    setScores((prev) => ({ ...prev, [key]: { ...prev[key], [field]: Math.max(0, value) } }));
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div>
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
          <label className="text-xs text-base-400 block mb-1.5">Tempo total (min)</label>
          <input
            type="number"
            value={tempoMinutos}
            min={0}
            onChange={(e) => setTempoMinutos(Number(e.target.value))}
            className="w-full bg-base-800 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-base-100 num focus:outline-none focus:ring-2 focus:ring-signal/40"
          />
        </div>
      </div>

      <div className="space-y-3">
        {AREA_FIELDS.map((f) => (
          <div key={f.key} className="flex items-center gap-2">
            <span className="text-xs text-base-300 w-24 shrink-0">{f.label}</span>
            <input
              type="number"
              value={scores[f.key].acertos}
              min={0}
              onChange={(e) => updateScore(f.key, "acertos", Number(e.target.value))}
              className="w-16 bg-base-800 border border-white/10 rounded-lg px-2 py-1.5 text-sm text-base-100 num text-center focus:outline-none focus:ring-2 focus:ring-signal/40"
            />
            <span className="text-base-500 text-xs">/</span>
            <input
              type="number"
              value={scores[f.key].total}
              min={0}
              onChange={(e) => updateScore(f.key, "total", Number(e.target.value))}
              className="w-16 bg-base-800 border border-white/10 rounded-lg px-2 py-1.5 text-sm text-base-100 num text-center focus:outline-none focus:ring-2 focus:ring-signal/40"
            />
          </div>
        ))}
      </div>

      <Button
        className="w-full"
        onClick={() =>
          onSubmit({
            date,
            tempoMinutos,
            linguagens: scores.linguagens,
            humanas: scores.humanas,
            natureza: scores.natureza,
            matematica: scores.matematica,
          })
        }
      >
        Salvar simulado
      </Button>
    </div>
  );
}
