"""circuit — símbolos de circuitos elétricos sobre svgkit.Fig (ANSI/zigue‑zague, usado nos livros brasileiros)."""
from __future__ import annotations
import math
from .svgkit import *  # noqa: F401,F403
from .svgkit import _adv

SCREEN = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}


class Circ(Fig):
    # ── geometria local ─────────────────────────────────────────────────────────
    @staticmethod
    def _ax(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        return L, dx / L, dy / L

    @staticmethod
    def _pt(p, ux, uy, u, v):
        return (p[0] + u * ux - v * uy, p[1] + u * uy + v * ux)

    @staticmethod
    def _side(ux, uy, want):
        """sinal s tal que a normal local (−uy, ux)·s aponta para a direção de tela ``want``."""
        nx, ny = -uy, ux
        return 1 if nx * want[0] + ny * want[1] >= 0 else -1

    # ── fios ───────────────────────────────────────────────────────────────────
    def wire(self, pts, c=INK, w=2.0):
        self.pl(pts, c, w)

    def node(self, x, y, c=INK, r=3.7):
        self.dot(x, y, r, c)

    def badge(self, x, y, s, c=INK, r=9.5, size=12, tc=WHITE):
        self.circ(x, y, r, c, c, 1, tag="bg")
        self.text(x, y + 0.34 * size, s, size, tc, weight=700, lint=False)

    def _leads(self, p, a, b, q, wc, ww):
        c1, c2 = (wc, wc) if isinstance(wc, str) else wc
        self.pl([p, a], c1, ww)
        self.pl([b, q], c2, ww)

    def _label(self, cx, cy, ex, ey, name, val, lab, size, color, gap=4.5, stack=False, ldx=0, ldy=0, halo=False,
               bold=False):
        """Posiciona rótulo em coordenadas de tela ao redor de (cx,cy) com semi‑extensões (ex,ey)."""
        if name is None and val is None:
            return
        if name is not None and val is not None:
            if stack:
                lines = [name, val]
            else:
                lines = [f"{name} = {val}"]
        else:
            lines = [name if name is not None else val]
        n = len(lines)
        lh = size * 1.12
        for i, ln in enumerate(lines):
            # deslocamento vertical da linha i (para 'n' empilha para cima)
            if lab in ("n", "ne", "nw"):
                y = cy - ey - gap - (n - 1 - i) * lh
                x = cx + (ex + gap if lab == "ne" else (-ex - gap if lab == "nw" else 0))
                anc = "middle" if lab == "n" else ("start" if lab == "ne" else "end")
            elif lab in ("s", "se", "sw"):
                y = cy + ey + gap + 0.74 * size + i * lh
                x = cx + (ex + gap if lab == "se" else (-ex - gap if lab == "sw" else 0))
                anc = "middle" if lab == "s" else ("start" if lab == "se" else "end")
            elif lab == "e":
                x = cx + ex + gap
                y = cy + 0.34 * size + (i - (n - 1) / 2) * lh
                anc = "start"
            else:  # 'w'
                x = cx - ex - gap
                y = cy + 0.34 * size + (i - (n - 1) / 2) * lh
                anc = "end"
            self.text(x + ldx, y + ldy, ln, size, color, anchor=anc, halo=halo, weight=600 if bold else 400)

    @staticmethod
    def _ext(ux, uy, half_len, ext):
        """(ex, ey) semi‑extensões de tela."""
        if abs(ux) >= abs(uy):
            return half_len, ext
        return ext, half_len

    # ── componentes ─────────────────────────────────────────────────────────────
    def res(self, p, q, name=None, val=None, lab="n", c=INK, length=46, amp=7.5, w=1.9, wc=INK, ww=2.0,
            size=12.5, lc=None, stack=False, gap=5, ldx=0, ldy=0, halo=False):
        L, ux, uy = self._ax(p, q)
        u0 = (L - length) / 2
        a, b = self._pt(p, ux, uy, u0, 0), self._pt(p, ux, uy, u0 + length, 0)
        self._leads(p, a, b, q, wc, ww)
        fr = [0, 1 / 12, 3 / 12, 5 / 12, 7 / 12, 9 / 12, 11 / 12, 1]
        vv = [0, 1, -1, 1, -1, 1, -1, 0]
        self.pl([self._pt(p, ux, uy, u0 + length * f, amp * v) for f, v in zip(fr, vv)], c, w)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        ex, ey = self._ext(ux, uy, length / 2, amp)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or c, gap, stack, ldx, ldy, halo)
        return cx, cy

    def bat(self, p, q, pos="q", name=None, val=None, lab="n", cells=1, signs=True, gap=7.5, wc=INK, ww=2.0,
            size=12.5, lc=None, stack=False, ldx=0, ldy=0, sgap=0, halo=False, pl=13, ps=7.5):
        """Pilha/bateria; ``pos`` indica o terminal positivo ('p' ou 'q')."""
        L, ux, uy = self._ax(p, q)
        if lab in ("w", "e") and name is not None and val is not None:
            stack = True
        n = 2 * cells
        us = [L / 2 + (k - (n - 1) / 2) * gap for k in range(n)]
        pos_k = [(k % 2 == 1) if pos == "q" else (k % 2 == 0) for k in range(n)]
        a, b = self._pt(p, ux, uy, us[0], 0), self._pt(p, ux, uy, us[-1], 0)
        self._leads(p, a, b, q, wc, ww)
        for u, isp in zip(us, pos_k):
            hl = pl if isp else ps
            c = POS if isp else NEG
            self.line(*self._pt(p, ux, uy, u, -hl), *self._pt(p, ux, uy, u, hl), c, 2.6 if isp else 4.4, cap="butt")
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        half = (us[-1] - us[0]) / 2 + 3
        ex, ey = self._ext(ux, uy, half, pl)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4.5, stack, ldx, ldy, halo)
        if signs:
            want = tuple(-v for v in SCREEN.get(lab[0] if lab[0] in "ns" else lab[-1], (0, -1)))
            s = self._side(ux, uy, want)
            vv = s * (pl + 8 + sgap)
            first_pos = pos_k[0]
            for u, isp in ((us[0] - 6.5, first_pos), (us[-1] + 6.5, pos_k[-1])):
                x, y = self._pt(p, ux, uy, u, vv)
                self.text(x, y + 4.2, "+" if isp else "−", 13, POS_D if isp else NEG_D, weight=700, lint=False)
        return cx, cy

    def sw(self, p, q, closed=False, name=None, val=None, lab="n", length=42, ang=30, up="n", wc=INK, ww=2.0,
           size=12.5, lc=None, stack=False, ldx=0, ldy=0, halo=False):
        L, ux, uy = self._ax(p, q)
        u0 = (L - length) / 2
        a, b = self._pt(p, ux, uy, u0, 0), self._pt(p, ux, uy, u0 + length, 0)
        self._leads(p, a, b, q, wc, ww)
        s = self._side(ux, uy, SCREEN[up])
        if closed:
            self.line(a[0], a[1], b[0], b[1], INK, 2.0)
            hy = 0
        else:
            t = math.radians(ang)
            tip = self._pt(p, ux, uy, u0 + length * 0.97 * math.cos(t), s * length * 0.97 * math.sin(t))
            self.line(a[0], a[1], tip[0], tip[1], INK, 2.0)
            hy = length * 0.5 * math.sin(t)
        for pt in (a, b):
            self.circ(pt[0], pt[1], 3.3, WHITE, INK, 1.7, tag="bg")
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        ex, ey = self._ext(ux, uy, length / 2, 5 if closed else length * 0.5 * math.sin(math.radians(ang)) + 3)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4, stack, ldx, ldy, halo)
        return cx, cy

    def lamp(self, p, q, name=None, val=None, lab="n", r=12.5, lum=None, wc=INK, ww=2.0, size=12.5, lc=None,
             stack=False, ldx=0, ldy=0, halo=False, fill=WHITE):
        L, ux, uy = self._ax(p, q)
        a, b = self._pt(p, ux, uy, L / 2 - r, 0), self._pt(p, ux, uy, L / 2 + r, 0)
        self._leads(p, a, b, q, wc, ww)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        self.circ(cx, cy, r, fill, INK, 1.9, tag="bg")
        d = r * 0.7071
        self.line(cx - d, cy - d, cx + d, cy + d, INK, 1.7, tag="bg")
        self.line(cx - d, cy + d, cx + d, cy - d, INK, 1.7, tag="bg")
        rr = r
        if lum:
            rl = {1: 4, 2: 7, 3: 10}[lum]
            for k in range(8):
                t = math.pi / 8 + k * math.pi / 4
                self.line(cx + (r + 3.5) * math.cos(t), cy + (r + 3.5) * math.sin(t),
                          cx + (r + 3.5 + rl) * math.cos(t), cy + (r + 3.5 + rl) * math.sin(t), ENE, 2.0, tag="bg")
            rr = r + 3.5 + rl
        ex, ey = self._ext(ux, uy, rr, rr)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 3.5, stack, ldx, ldy, halo)
        return cx, cy

    def cap(self, p, q, name=None, val=None, lab="n", gap=8, half=11.5, pos=None, wc=INK, ww=2.0, size=12.5,
            lc=None, stack=False, ldx=0, ldy=0, halo=False):
        L, ux, uy = self._ax(p, q)
        a, b = self._pt(p, ux, uy, L / 2 - gap / 2, 0), self._pt(p, ux, uy, L / 2 + gap / 2, 0)
        self._leads(p, a, b, q, wc, ww)
        cols = (INK, INK)
        if pos == "q":
            cols = (NEG, POS)
        elif pos == "p":
            cols = (POS, NEG)
        for (u, c) in ((L / 2 - gap / 2, cols[0]), (L / 2 + gap / 2, cols[1])):
            self.line(*self._pt(p, ux, uy, u, -half), *self._pt(p, ux, uy, u, half), c, 2.8, cap="butt")
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        ex, ey = self._ext(ux, uy, gap / 2 + 2, half)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4.5, stack, ldx, ldy, halo)
        return cx, cy

    def meter(self, p, q, kind="A", name=None, val=None, lab="n", r=13.5, wc=INK, ww=2.0, size=12.5, lc=None,
              stack=False, ldx=0, ldy=0, halo=False):
        L, ux, uy = self._ax(p, q)
        a, b = self._pt(p, ux, uy, L / 2 - r, 0), self._pt(p, ux, uy, L / 2 + r, 0)
        self._leads(p, a, b, q, wc, ww)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        self.circ(cx, cy, r, WHITE, INK, 1.9, tag="bg")
        self.text(cx, cy + 4.8, kind, 14, INK, weight=700, lint=False)
        ex, ey = self._ext(ux, uy, r, r)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4, stack, ldx, ldy, halo)
        return cx, cy

    def box(self, p, q, txt, name=None, val=None, lab="n", length=48, height=26, fill=SOFT, wc=INK, ww=2.0,
            size=12.5, lc=None, stack=False, ldx=0, ldy=0, halo=False, tsize=12.5, circle=False):
        L, ux, uy = self._ax(p, q)
        horiz = abs(ux) >= abs(uy)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        if circle:
            r = height / 2 + 2
            a, b = self._pt(p, ux, uy, L / 2 - r, 0), self._pt(p, ux, uy, L / 2 + r, 0)
            self._leads(p, a, b, q, wc, ww)
            self.circ(cx, cy, r, fill, INK, 1.9, tag="bg")
            self.text(cx, cy + 0.34 * tsize, txt, tsize, INK, weight=600, lint=False)
            ex, ey = self._ext(ux, uy, r, r)
        else:
            a, b = self._pt(p, ux, uy, L / 2 - length / 2, 0), self._pt(p, ux, uy, L / 2 + length / 2, 0)
            self._leads(p, a, b, q, wc, ww)
            wbox, hbox = (length, height) if horiz else (height, length)
            self.rect(cx - wbox / 2, cy - hbox / 2, wbox, hbox, fill, INK, 1.9, rx=3, tag="bg")
            self.text(cx, cy + 0.34 * tsize, txt, tsize, INK, weight=600, lint=False)
            ex, ey = wbox / 2, hbox / 2
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4.5, stack, ldx, ldy, halo)
        return cx, cy

    def led(self, p, q, name=None, val=None, lab="n", size_t=11, wc=INK, ww=2.0, size=12.5, lc=None, ldx=0, ldy=0,
            stack=False, halo=False):
        """LED: o sentido p→q é o de condução (ânodo em p)."""
        L, ux, uy = self._ax(p, q)
        a, b = self._pt(p, ux, uy, L / 2 - size_t, 0), self._pt(p, ux, uy, L / 2 + size_t, 0)
        self._leads(p, a, b, q, wc, ww)
        t1 = self._pt(p, ux, uy, L / 2 - size_t, -size_t * 0.95)
        t2 = self._pt(p, ux, uy, L / 2 - size_t, size_t * 0.95)
        t3 = self._pt(p, ux, uy, L / 2 + size_t * 0.55, 0)
        self.pl([t1, t2, t3], INK, 1.9, fill=SOFT, close=True, tag="bg")
        bar1 = self._pt(p, ux, uy, L / 2 + size_t * 0.55, -size_t * 0.95)
        bar2 = self._pt(p, ux, uy, L / 2 + size_t * 0.55, size_t * 0.95)
        self.line(*bar1, *bar2, INK, 2.4, cap="butt")
        s = self._side(ux, uy, (0, -1))
        for k in (0, 1):
            st = self._pt(p, ux, uy, L / 2 - size_t * 0.2 + k * 8, s * size_t * 1.15)
            en = self._pt(p, ux, uy, L / 2 + size_t * 0.5 + k * 8, s * size_t * 2.15)
            self.arrow(st[0], st[1], en[0], en[1], ENE, 1.6, 6.5, 0.45)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        ex, ey = self._ext(ux, uy, size_t * 1.2, size_t * 2.2)
        self._label(cx, cy, ex, ey, name, val, lab, size, lc or INK, 4, stack, ldx, ldy, halo)
        return cx, cy

    def fuse(self, p, q, name=None, val=None, lab="n", length=34, h=11, wc=INK, ww=2.0, size=12.5, ldx=0, ldy=0):
        L, ux, uy = self._ax(p, q)
        a, b = self._pt(p, ux, uy, L / 2 - length / 2, 0), self._pt(p, ux, uy, L / 2 + length / 2, 0)
        self._leads(p, a, b, q, wc, ww)
        cx, cy = self._pt(p, ux, uy, L / 2, 0)
        horiz = abs(ux) >= abs(uy)
        wb, hb = (length, h) if horiz else (h, length)
        self.rect(cx - wb / 2, cy - hb / 2, wb, hb, WHITE, INK, 1.9, rx=1.5, tag="bg")
        self.line(a[0], a[1], b[0], b[1], INK, 1.5, tag="bg")
        ex, ey = self._ext(ux, uy, length / 2, h / 2)
        self._label(cx, cy, ex, ey, name, val, lab, size, INK, 4.5, False, ldx, ldy, False)
        return cx, cy

    # ── setas de corrente e de tensão ───────────────────────────────────────────
    def iarr(self, p, q, t=0.5, name=None, c=CUR, side=None, size=12.5, length=22, off=8, w=2.6, head=10,
             ldx=0, ldy=0, lc=None, halo=True):
        L, ux, uy = self._ax(p, q)
        cx, cy = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        sx, sy = cx - ux * length / 2, cy - uy * length / 2
        ex, ey = cx + ux * length / 2, cy + uy * length / 2
        self.arrow(sx, sy, ex, ey, c, w, head, 0.40, tag="bg")
        if name:
            if side is None:
                side = "n" if abs(ux) >= abs(uy) else "e"
            d = SCREEN[side]
            if side in ("n", "s"):
                x, y, anc = cx + ldx, (cy - off - 3 if side == "n" else cy + off + 0.74 * size + 2) + ldy, "middle"
            elif side == "e":
                x, y, anc = cx + off + 3 + ldx, cy + 0.34 * size + ldy, "start"
            else:
                x, y, anc = cx - off - 3 + ldx, cy + 0.34 * size + ldy, "end"
            self.text(x, y, name, size, lc or CUR_D, anchor=anc, halo=halo, weight=600)

    def ddp(self, p, q, name, side="n", off=20, c=INK, size=12.5, signs=True, w=1.4, tick=5):
        """Indicação de DDP: seta fina paralela a p→q (aponta para o maior potencial, q), com + e −."""
        L, ux, uy = self._ax(p, q)
        d = SCREEN[side]
        s = self._side(ux, uy, d)
        a = self._pt(p, ux, uy, 0, s * off)
        b = self._pt(p, ux, uy, L, s * off)
        self.line(*p, *a, c, 0.9, "2 2", tag="bg")
        self.line(*q, *b, c, 0.9, "2 2", tag="bg")
        self.arrow(a[0], a[1], b[0], b[1], c, w, 7, 0.36)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if side in ("n", "s"):
            y = my - 5 if side == "n" else my + 5 + 0.74 * size
            self.text(mx, y, name, size, c, halo=True)
        else:
            self.text(mx + (7 if side == "e" else -7), my + 0.34 * size, name, size, c,
                      anchor="start" if side == "e" else "end", halo=True)

    def loop_arrow(self, cx, cy, rx, ry, a0=30, a1=330, c=GRY, w=1.6, ccw=True, dash=None, head=8):
        """Arco elíptico com seta indicando percurso (ccw=True: anti‑horário)."""
        n = 40
        seq = [a0 + (a1 - a0) * k / n for k in range(n + 1)]
        if not ccw:
            seq = seq[::-1]
        pts = [(cx + rx * math.cos(math.radians(a)), cy - ry * math.sin(math.radians(a))) for a in seq]
        self.arrow_poly(pts, c, w, head, dash)
        return pts
