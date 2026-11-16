#!/usr/bin/env python3
"""Gera 4 propostas de capa (PNG) para a apostila de Física Elétrica. Uso: python3 tools/capas_ideias.py"""
import sys, math, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lib.svgkit import trace_field
OUT = ROOT / "capas_ideias"; OUT.mkdir(exist_ok=True)
W, H = 794, 1123
FONT = f"file://{ROOT}/assets/fonts/"
CSS = f"""
@font-face{{font-family:SS;src:url({FONT}source-sans-3-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:SS;src:url({FONT}source-sans-3-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:SS;src:url({FONT}source-sans-3-latin-ext-700-normal.woff2);font-weight:700;unicode-range:U+0100-02AF}}
*{{box-sizing:border-box;margin:0}} body{{width:{W}px;height:{H}px;font-family:SS,sans-serif;position:relative;overflow:hidden}}
svg{{position:absolute;left:0;top:0}} .t{{position:absolute;left:56px;right:56px}}
"""
def field_paths(charges, bounds, n=14, r0=16, col="#fff", w=2, op=.9, step=3.0):
    s = ""
    for (cx, cy, q) in charges:
        if q <= 0: continue
        for k in range(n):
            a = 2*math.pi*(k+.5)/n
            pts = trace_field(charges, (cx+r0*math.cos(a), cy+r0*math.sin(a)), +1, step, 1500, bounds, 14)
            s += f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round"/>'
    return s
def charge(x, y, plus, r=26, c1="#E5484D", c2="#2563EB"):
    c = c1 if plus else c2
    g = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{c}" stroke-width="5"/><line x1="{x-r*.5}" y1="{y}" x2="{x+r*.5}" y2="{y}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
    if plus: g += f'<line x1="{x}" y1="{y-r*.5}" x2="{x}" y2="{y+r*.5}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
    return g
def texts(color, sub, accent, top="ENEM · PAS 3 · UnB · 2026", dark_tag="#fff"):
    return f"""<div class="t" style="top:58px;font-weight:700;letter-spacing:.3em;font-size:15px;color:{sub}">{top}</div>
<div class="t" style="top:96px;font-weight:700;font-size:112px;line-height:.92;letter-spacing:-.03em;color:{color}">Física<br>Elétrica</div>
<div class="t" style="top:330px;font-size:34px;font-weight:400;color:{color};opacity:.9">do básico ao avançado</div>
<div class="t" style="bottom:70px;font-size:17px;line-height:1.5;color:{sub}"><b style="color:{accent};letter-spacing:.12em;font-size:15px">ELETROSTÁTICA · ELETRODINÂMICA · MAGNETISMO E ELETROMAGNETISMO</b><br>Curso compacto com exemplos resolvidos, exercícios graduados e formulários por situação de uso.</div>"""
def page(name, body, bg):
    html = f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body style='background:{bg}'>{body}</body></html>"
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")

# A — Campo de um dipolo (escuro, neon ciano/coral)
ch = [(250, 800, +1), (545, 800, -1)]
svg = f'<svg width="{W}" height="{H}"><defs><filter id="g"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><radialGradient id="r" cx=".5" cy=".72" r=".7"><stop offset="0" stop-color="#1E3A8A"/><stop offset="1" stop-color="#070B24"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#r)"/><g filter="url(#g)">{field_paths(ch,(0,420,W,H),n=18,col="#22D3EE",w=2.4)}</g>{charge(250,800,True)}{charge(545,800,False)}</svg>'
page("A_campo_dipolo", svg + texts("#fff", "#9FB3E8", "#22D3EE"), "#070B24")
# B — Solenoide + linhas de B (claro, roxo/laranja)
cx0, cx1, yc = 150, 644, 650
coil = ""
n = 12; pit = (cx1-cx0)/n
for k in range(n):
    xa = cx0+k*pit
    coil += f'<line x1="{xa+pit*.5:.1f}" y1="{yc+80}" x2="{xa+pit:.1f}" y2="{yc-80}" stroke="#C9B8F5" stroke-width="5" stroke-linecap="round"/>'
for k in range(n):
    xa = cx0+k*pit
    coil += f'<line x1="{xa:.1f}" y1="{yc-80}" x2="{xa+pit*.5:.1f}" y2="{yc+80}" stroke="#F08C00" stroke-width="9" stroke-linecap="round"/>'
loops = ""
for hh, dx in ((100, 50), (150, 100), (200, 150)):
    for sg in (-1, 1):
        pts = " ".join(f"{(cx0+cx1)/2+((cx1-cx0)/2+dx)*math.cos(math.radians(t)):.1f},{yc+sg*hh*math.sin(math.radians(t)):.1f}" for t in range(0, 181, 4))
        loops += f'<polyline points="{pts}" fill="none" stroke="#7C3AED" stroke-width="4" stroke-opacity=".85" stroke-linecap="round"/>'
inner = "".join(f'<line x1="{cx0+20}" y1="{yc+d}" x2="{cx1-20}" y2="{yc+d}" stroke="#6D28D9" stroke-width="5"/>' for d in (-40, 0, 40))
svg = f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#F5F3FF"/><circle cx="650" cy="150" r="260" fill="#EEE6FD"/>{loops}{coil}{inner}<rect x="{cx1+18}" y="{yc-30}" width="52" height="60" rx="8" fill="#6D28D9"/><text x="{cx1+44}" y="{yc+14}" font-size="38" font-weight="700" fill="#fff" text-anchor="middle" font-family="SS">N</text><rect x="{cx0-70}" y="{yc-30}" width="52" height="60" rx="8" fill="#EEE6FD" stroke="#6D28D9" stroke-width="4"/><text x="{cx0-44}" y="{yc+14}" font-size="38" font-weight="700" fill="#6D28D9" text-anchor="middle" font-family="SS">S</text></svg>'
page("B_solenoide_magnetismo", svg + texts("#1B1340", "#5B4B8A", "#6D28D9"), "#F5F3FF")
# C — Raio + átomo (escuro, âmbar)
orb = ""
for rx, ry, rot in ((200, 70, 0), (200, 70, 60), (200, 70, 120)):
    orb += f'<ellipse cx="397" cy="760" rx="{rx}" ry="{ry}" transform="rotate({rot} 397 760)" fill="none" stroke="#FBBF24" stroke-width="3" stroke-opacity=".8"/>'
els = "".join(f'<circle cx="{397+200*math.cos(math.radians(a))*math.cos(math.radians(r))-70*math.sin(math.radians(a))*math.sin(math.radians(r)):.1f}" cy="{760+200*math.cos(math.radians(a))*math.sin(math.radians(r))+70*math.sin(math.radians(a))*math.cos(math.radians(r)):.1f}" r="11" fill="#60A5FA"/>' for a, r in ((20, 0), (200, 60), (110, 120)))
bolt = "M560,380 L470,610 L545,610 L440,860 L690,540 L590,540 L650,380 Z"
svg = f'<svg width="{W}" height="{H}"><defs><filter id="g"><feGaussianBlur stdDeviation="8"/></filter><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset="1" stop-color="#F59E0B"/></linearGradient></defs><rect width="{W}" height="{H}" fill="#0F172A"/><g transform="translate(0,-10)">{orb}</g><circle cx="397" cy="750" r="30" fill="#E5484D"/><line x1="380" y1="750" x2="414" y2="750" stroke="#fff" stroke-width="6"/><line x1="397" y1="733" x2="397" y2="767" stroke="#fff" stroke-width="6"/>{els.replace("cy=\"","cy=\"")}<path d="{bolt}" fill="url(#b)" transform="translate(-120,330) scale(.55)" stroke="#FEF3C7" stroke-width="4"/></svg>'
page("C_raio_atomo", svg + texts("#fff", "#94A3B8", "#FBBF24"), "#0F172A")
# D — Onda eletromagnética (claro, azul elétrico)
E = " ".join(f"{70+k*6:.0f},{800-110*math.sin(k/9)}" for k in range(0, 116))
Bw = " ".join(f"{70+k*6:.0f},{800-34*math.sin(k/9)}" for k in range(0, 116))
vec = ""
for k in range(0, 116, 5):
    x = 70+k*6; ye = 800-110*math.sin(k/9); yb = 800-48*math.sin(k/9)*0
    vec += f'<line x1="{x}" y1="800" x2="{x}" y2="{ye:.1f}" stroke="#0891B2" stroke-width="3"/>'
    vec += f'<line x1="{x}" y1="800" x2="{x+32*math.sin(k/9):.1f}" y2="{800+22*math.sin(k/9):.1f}" stroke="#7C3AED" stroke-width="3"/>'
svg = f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="14" fill="#1D4ED8"/><circle cx="640" cy="230" r="330" fill="#EFF6FF"/><line x1="50" y1="800" x2="744" y2="800" stroke="#94A3B8" stroke-width="2"/>{vec}<polyline points="{E}" fill="none" stroke="#0891B2" stroke-width="6" stroke-linecap="round"/><text x="70" y="660" font-family="SS" font-size="22" font-weight="700" fill="#0E7490">campo elétrico E</text><text x="560" y="960" font-family="SS" font-size="22" font-weight="700" fill="#6D28D9">campo magnético B</text></svg>'
page("D_onda_eletromagnetica", svg + texts("#0B1B4D", "#475569", "#1D4ED8"), "#fff")

js = """const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:%d,height:%d},deviceScaleFactor:1.5});
for(const f of fs.readdirSync('%s').filter(x=>x.endsWith('.html'))){await pg.goto('file://%s/'+f);await pg.waitForTimeout(400);await pg.screenshot({path:'%s/'+f.replace('.html','.png')});}await b.close();})();""" % (W, H, OUT, OUT, OUT)
(ROOT / "tools" / "_shot.js").write_text(js)
subprocess.run(["node", str(ROOT / "tools" / "_shot.js")], cwd=ROOT, check=True)
(ROOT / "tools" / "_shot.js").unlink()
print([f.name for f in sorted(OUT.glob("*.png"))])
