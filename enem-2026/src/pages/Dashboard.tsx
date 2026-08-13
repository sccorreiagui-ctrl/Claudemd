import { useMemo } from "react";
import {
  BarChart,
  Bar,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  PieChart,
  Pie,
  LineChart,
  Line,
  Legend,
} from "recharts";
import { AREAS, TEMAS, temasPorArea } from "../data/temas";
import { useStore } from "../store/store";
import { areaMastery, overallMastery, errorCategoryDistribution, simuladoEvolution, worstTemas } from "../lib/stats";
import { ERROR_CATEGORY_LABEL } from "../types";
import { formatDateShortBR, formatDateBR } from "../lib/date";
import { Card, SectionTitle, ProgressRing, EmptyState } from "../components/ui";

const AREA_COLOR: Record<string, string> = {
  Linguagens: "#ff5a3c",
  Humanas: "#e8b84b",
  Matemática: "#3ba7e8",
  Biologia: "#3ddc97",
  Física: "#f2cd76",
  Química: "#6fc0f0",
};

const ERROR_COLORS = ["#ff5a3c", "#e8b84b", "#3ba7e8", "#3ddc97", "#8598ab", "#f2cd76"];

export function Dashboard() {
  const temaStates = useStore((s) => s.temaStates);
  const logs = useStore((s) => s.questionLogs);
  const simulados = useStore((s) => s.simulados);

  const mastery = overallMastery(TEMAS, temaStates);
  const areaData = useMemo(
    () =>
      AREAS.map((area) => ({
        area,
        mastery: areaMastery(area, temaStates),
        temas: temasPorArea(area).length,
      })),
    [temaStates]
  );

  const errorDist = useMemo(() => errorCategoryDistribution(logs).filter((d) => d.count > 0), [logs]);
  const evolution = useMemo(() => simuladoEvolution(simulados), [simulados]);
  const worst = useMemo(() => worstTemas(TEMAS, logs, 3).slice(0, 3), [logs]);

  return (
    <div className="space-y-5 animate-slide-up">
      <SectionTitle eyebrow="Visão consolidada" title="Painel de evolução" />

      <Card className="p-5 flex items-center gap-5">
        <ProgressRing value={mastery} size={90} stroke={8} />
        <div>
          <div className="font-display font-semibold text-base-50">Domínio operacional geral</div>
          <p className="text-xs text-base-400 mt-1 max-w-xs">
            Média ponderada por tier de incidência entre os 78 temas do Núcleo S.
          </p>
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">Progresso por área</div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={areaData} layout="vertical" margin={{ left: 8 }}>
              <CartesianGrid stroke="rgba(255,255,255,0.05)" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} stroke="#5c7086" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis dataKey="area" type="category" stroke="#8598ab" fontSize={11} tickLine={false} axisLine={false} width={80} />
              <Tooltip
                contentStyle={{ background: "#0e141d", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 10, fontSize: 12 }}
                formatter={(v: number) => [`${v}%`, "Domínio"]}
              />
              <Bar dataKey="mastery" radius={[0, 6, 6, 0]} barSize={18}>
                {areaData.map((d) => (
                  <Cell key={d.area} fill={AREA_COLOR[d.area]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
          Distribuição de categorias de erro
        </div>
        {errorDist.length === 0 ? (
          <EmptyState title="Sem dados ainda" description="Registre erros no Diagnóstico pra ver o que mais te derruba." />
        ) : (
          <div className="flex items-center gap-4">
            <div className="h-40 w-40 shrink-0">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={errorDist} dataKey="count" nameKey="category" innerRadius={38} outerRadius={62} paddingAngle={2}>
                    {errorDist.map((d, i) => (
                      <Cell key={d.category} fill={ERROR_COLORS[i % ERROR_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ background: "#0e141d", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 10, fontSize: 12 }}
                    formatter={(v: number, _n, entry: any) => [`${v} (${entry.payload.pct}%)`, ERROR_CATEGORY_LABEL[entry.payload.category as keyof typeof ERROR_CATEGORY_LABEL]]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-1.5 flex-1 min-w-0">
              {errorDist.map((d, i) => (
                <div key={d.category} className="flex items-center gap-2 text-xs">
                  <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: ERROR_COLORS[i % ERROR_COLORS.length] }} />
                  <span className="text-base-300 truncate flex-1">{ERROR_CATEGORY_LABEL[d.category]}</span>
                  <span className="num text-base-400">{d.pct}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>

      <Card className="p-4">
        <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
          Evolução de nota estimada (simulados)
        </div>
        {evolution.length < 2 ? (
          <EmptyState
            title="Poucos simulados"
            description="Registre pelo menos 2 simulados pra visualizar a curva de evolução."
          />
        ) : (
          <div className="h-52 -ml-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={evolution}>
                <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="date" tickFormatter={formatDateShortBR} stroke="#5c7086" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis domain={[0, 100]} stroke="#5c7086" fontSize={10} tickLine={false} axisLine={false} width={28} />
                <Tooltip
                  contentStyle={{ background: "#0e141d", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 10, fontSize: 12 }}
                  labelFormatter={(v) => formatDateBR(v as string)}
                />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Line type="monotone" dataKey="totalPct" name="Nota geral" stroke="#ff5a3c" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </Card>

      {worst.length > 0 && (
        <Card className="p-4">
          <div className="text-[11px] font-mono uppercase tracking-wide text-base-400 mb-3">
            Foco recomendado agora
          </div>
          <div className="space-y-2">
            {worst.map((w) => (
              <div key={w.temaId} className="flex items-center justify-between text-sm">
                <span className="text-base-200 truncate">{w.temaNome}</span>
                <span className="num text-signal-soft text-xs">{Math.round(w.accuracy * 100)}% acerto</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
