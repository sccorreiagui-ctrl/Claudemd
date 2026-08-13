import { PropsWithChildren, useEffect } from "react";
import { X } from "lucide-react";
import type { Tier } from "../types";
import { TIER_LABEL } from "../data/temas";

export function Card({
  children,
  className = "",
  as: As = "div",
}: PropsWithChildren<{ className?: string; as?: "div" | "section" }>) {
  return <As className={`panel rounded-2xl ${className}`}>{children}</As>;
}

export function SectionTitle({
  eyebrow,
  title,
  right,
}: {
  eyebrow?: string;
  title: string;
  right?: React.ReactNode;
}) {
  return (
    <div className="flex items-end justify-between gap-3 mb-3">
      <div>
        {eyebrow && (
          <div className="text-[11px] font-mono uppercase tracking-[0.14em] text-base-400 mb-0.5">{eyebrow}</div>
        )}
        <h2 className="font-display font-semibold text-lg text-base-50 tracking-tight">{title}</h2>
      </div>
      {right}
    </div>
  );
}

const TIER_STYLES: Record<Tier, string> = {
  alta: "bg-signal/15 text-signal-soft border-signal/30",
  media: "bg-gold/15 text-gold-soft border-gold/30",
  baixa: "bg-base-600/30 text-base-300 border-base-500/40",
};

export function TierBadge({ tier, compact = false }: { tier: Tier; compact?: boolean }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border font-mono uppercase tracking-wide ${TIER_STYLES[tier]} ${
        compact ? "text-[9px] px-1.5 py-0.5" : "text-[10px] px-2 py-0.5"
      }`}
    >
      {TIER_LABEL[tier]}
    </span>
  );
}

export function Stat({
  label,
  value,
  suffix,
  tone = "default",
  size = "md",
}: {
  label: string;
  value: string | number;
  suffix?: string;
  tone?: "default" | "signal" | "mint" | "gold" | "azure";
  size?: "sm" | "md" | "lg";
}) {
  const toneClass = {
    default: "text-base-50",
    signal: "text-signal-soft",
    mint: "text-mint-soft",
    gold: "text-gold-soft",
    azure: "text-azure-soft",
  }[tone];
  const sizeClass = { sm: "text-xl", md: "text-2xl", lg: "text-4xl" }[size];
  return (
    <div>
      <div className={`num font-semibold ${sizeClass} ${toneClass} leading-none`}>
        {value}
        {suffix && <span className="text-base-400 text-[0.5em] ml-1 align-middle">{suffix}</span>}
      </div>
      <div className="text-[11px] text-base-400 mt-1.5 uppercase tracking-wide">{label}</div>
    </div>
  );
}

export function ProgressRing({
  value,
  size = 88,
  stroke = 8,
  color = "#ff5a3c",
  trackColor = "rgba(255,255,255,0.06)",
  label,
  sublabel,
}: {
  value: number;
  size?: number;
  stroke?: number;
  color?: string;
  trackColor?: string;
  label?: string;
  sublabel?: string;
}) {
  const clamped = Math.max(0, Math.min(100, value));
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (clamped / 100) * c;
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} stroke={trackColor} strokeWidth={stroke} fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={color}
          strokeWidth={stroke}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.6s cubic-bezier(0.34,1.56,0.64,1)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="num font-bold text-base-50" style={{ fontSize: size * 0.22 }}>
          {Math.round(clamped)}
        </span>
        {label && <span className="text-base-400 leading-none mt-0.5" style={{ fontSize: size * 0.1 }}>{label}</span>}
      </div>
      {sublabel && (
        <span className="absolute -bottom-5 text-[10px] text-base-400 whitespace-nowrap">{sublabel}</span>
      )}
    </div>
  );
}

export function Sheet({
  open,
  onClose,
  title,
  children,
}: PropsWithChildren<{ open: boolean; onClose: () => void; title: string }>) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm animate-[pop-in_0.2s_ease-out]" onClick={onClose} />
      <div className="relative w-full sm:max-w-lg max-h-[88vh] overflow-y-auto rounded-t-3xl sm:rounded-3xl bg-base-900 border border-white/10 shadow-2xl animate-slide-up">
        <div className="sticky top-0 z-10 flex items-center justify-between px-5 py-4 border-b border-white/[0.06] bg-base-900/95 backdrop-blur">
          <h3 className="font-display font-semibold text-base-50 pr-4">{title}</h3>
          <button
            onClick={onClose}
            className="shrink-0 rounded-full p-1.5 text-base-300 hover:text-base-50 hover:bg-white/10 transition-colors"
            aria-label="Fechar"
          >
            <X size={18} />
          </button>
        </div>
        <div className="px-5 py-4">{children}</div>
      </div>
    </div>
  );
}

export function Button({
  children,
  onClick,
  variant = "primary",
  type = "button",
  className = "",
  disabled = false,
  size = "md",
}: PropsWithChildren<{
  onClick?: () => void;
  variant?: "primary" | "secondary" | "ghost" | "danger";
  type?: "button" | "submit";
  className?: string;
  disabled?: boolean;
  size?: "sm" | "md";
}>) {
  const variants: Record<string, string> = {
    primary: "bg-signal text-white hover:bg-signal-dim active:scale-[0.98] shadow-glow",
    secondary: "bg-base-700 text-base-50 hover:bg-base-600 active:scale-[0.98]",
    ghost: "bg-transparent text-base-300 hover:text-base-50 hover:bg-white/5",
    danger: "bg-transparent text-signal-soft hover:bg-signal/10",
  };
  const sizes: Record<string, string> = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-4 py-2.5 text-sm",
  };
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-1.5 rounded-xl font-medium transition-all disabled:opacity-40 disabled:pointer-events-none ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </button>
  );
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="text-center py-10 px-4">
      <p className="text-base-200 font-medium mb-1">{title}</p>
      <p className="text-base-400 text-sm max-w-xs mx-auto">{description}</p>
    </div>
  );
}
