import {
  addDays as fnsAddDays,
  differenceInCalendarDays,
  format,
  parseISO,
} from "date-fns";
import { ptBR } from "date-fns/locale";

export const ENEM_DIA1 = parseISO("2026-11-08T13:30:00");
export const ENEM_DIA2 = parseISO("2026-11-15T13:30:00");

export function todayISO(): string {
  return format(new Date(), "yyyy-MM-dd");
}

export function toISO(d: Date): string {
  return format(d, "yyyy-MM-dd");
}

export function addDaysISO(iso: string, days: number): string {
  return toISO(fnsAddDays(parseISO(iso), days));
}

export function daysBetween(fromISO: string, toISOStr: string): number {
  return differenceInCalendarDays(parseISO(toISOStr), parseISO(fromISO));
}

export function isOverdue(nextReviewISO: string | null, refISO = todayISO()): boolean {
  if (!nextReviewISO) return false;
  return daysBetween(refISO, nextReviewISO) <= 0;
}

export function formatDateBR(iso: string): string {
  return format(parseISO(iso), "dd/MM/yyyy");
}

export function formatDateShortBR(iso: string): string {
  return format(parseISO(iso), "dd/MM");
}

export function formatWeekdayBR(iso: string): string {
  return format(parseISO(iso), "EEEEEE", { locale: ptBR });
}

export interface Countdown {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  totalMs: number;
}

export function countdownTo(target: Date, now = new Date()): Countdown {
  const totalMs = Math.max(0, target.getTime() - now.getTime());
  const days = Math.floor(totalMs / (1000 * 60 * 60 * 24));
  const hours = Math.floor((totalMs / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((totalMs / (1000 * 60)) % 60);
  const seconds = Math.floor((totalMs / 1000) % 60);
  return { days, hours, minutes, seconds, totalMs };
}

/** Calcula streak (dias consecutivos com atividade) contando de hoje pra trás. */
export function computeStreak(activityDatesISO: string[]): number {
  if (activityDatesISO.length === 0) return 0;
  const set = new Set(activityDatesISO);
  const today = todayISO();
  let cursor = set.has(today) ? today : addDaysISO(today, -1);
  if (!set.has(cursor)) return 0;
  let streak = 0;
  while (set.has(cursor)) {
    streak += 1;
    cursor = addDaysISO(cursor, -1);
  }
  return streak;
}
