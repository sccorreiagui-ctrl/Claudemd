import { PropsWithChildren } from "react";
import { NavLink } from "react-router-dom";
import { Home, LayoutGrid, RotateCcw, Stethoscope, Timer, BarChart3 } from "lucide-react";

const NAV = [
  { to: "/", label: "Início", icon: Home, end: true },
  { to: "/conteudo", label: "Conteúdo", icon: LayoutGrid },
  { to: "/ciclo", label: "Ciclo", icon: RotateCcw },
  { to: "/diagnostico", label: "Diagnóstico", icon: Stethoscope },
  { to: "/simulados", label: "Simulados", icon: Timer },
  { to: "/dashboard", label: "Painel", icon: BarChart3 },
];

export function Shell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-40 border-b border-white/[0.06] bg-base-950/80 backdrop-blur-md">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-signal/15 border border-signal/30 flex items-center justify-center">
              <span className="text-signal-soft font-mono text-xs font-bold">N</span>
            </div>
            <span className="font-display font-semibold text-sm tracking-tight text-base-50">
              Reta Final <span className="text-base-400 font-normal">· ENEM 2026</span>
            </span>
          </div>
          <nav className="hidden sm:flex items-center gap-1">
            {NAV.map(({ to, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive ? "bg-white/10 text-base-50" : "text-base-400 hover:text-base-100"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto px-4 pb-24 sm:pb-10 pt-4">{children}</main>

      <nav className="sm:hidden fixed bottom-0 inset-x-0 z-40 border-t border-white/[0.06] bg-base-950/95 backdrop-blur-md pb-[env(safe-area-inset-bottom)]">
        <div className="grid grid-cols-6">
          {NAV.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center gap-1 py-2.5 text-[10px] font-medium transition-colors ${
                  isActive ? "text-signal-soft" : "text-base-400"
                }`
              }
            >
              <Icon size={18} strokeWidth={2.25} />
              <span className="leading-none">{label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}
