"""Módulo G — Cartografia: planisfério de coordenadas e fusos, fusos do Brasil, projeções com indicatrizes de Tissot,
curvas de nível (relevo hipotético, ilustrativo) e cartograma de anamorfose (população por UF, IBGE 2022)."""
import json, math
from geo import *
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon as MPoly, Circle
from pyproj import Transformer
from figs.f_a2_mapas_fisica import xy, set_ll_extent

C_RED, C_BLUE = "#C62828", "#1565C0"


# ============================================================ planisfério com coordenadas e fusos
def coordenadas():
    W, H = 188, 71
    fig, ax = new_fig(W, H, bg="#FFFFFF")
    lat0, lat1 = -62, 84
    ax.set_xlim(-180, 180); ax.set_ylim(lat0, lat1)
    ax.add_patch(plt.Rectangle((-180, lat0), 360, lat1 - lat0, fc=WATER, ec="none", zorder=0))
    # faixas de fuso (15°), centradas nos múltiplos de 15
    for k in range(-12, 13):
        c = 15 * k
        if k % 2 == 0:
            ax.add_patch(plt.Rectangle((c - 7.5, lat0), 15, lat1 - lat0, fc="#FFFFFF", ec="none", alpha=0.35, zorder=1))
    c = countries("110m")
    c = c[c["ADM0_A3"] != "ATA"]
    c.plot(ax=ax, fc="#EDE9DD", ec=BORDER, lw=0.2, zorder=2)
    bz = c[c["NAME"] == "Brazil"]
    bz.plot(ax=ax, fc="#DCE8C9", ec="#37474F", lw=0.5, zorder=3)
    # paralelos e meridianos
    for la in range(-60, 90, 30):
        ax.plot([-180, 180], [la, la], color="#8FA3B5", lw=0.3, zorder=4)
    for lo in range(-180, 181, 30):
        ax.plot([lo, lo], [lat0, lat1], color="#8FA3B5", lw=0.3, zorder=4)
    ax.plot([-180, 180], [0, 0], color=C_RED, lw=1.0, zorder=5)
    for la in (23.43, -23.43):
        ax.plot([-180, 180], [la, la], color="#E65100", lw=0.7, ls=(0, (4, 2)), zorder=5)
    for la in (66.56, -66.56):
        ax.plot([-180, 180], [la, la], color="#1565C0", lw=0.7, ls=(0, (4, 2)), zorder=5)
    ax.plot([0, 0], [lat0, lat1], color="#2E7D32", lw=1.0, zorder=5)
    # rótulos das linhas (à direita)
    def tag(la, s, color, ha="left", x=181.5):
        ax.text(x, la, s, fontsize=4.6, color=color, fontweight=700, ha=ha, va="center", clip_on=False)
    tag(0, "Equador (0°)", C_RED); tag(23.43, "Trópico de Câncer\n23°26′ N", "#B23C00"); tag(-23.43, "Trópico de Capricórnio\n23°26′ S", "#B23C00")
    tag(66.56, "Círculo Polar Ártico\n66°34′ N", "#0D47A1"); tag(-66.56 + 4, "", "#0D47A1")
    ax.text(1.5, lat1 - 2.5, "Meridiano de Greenwich (0°)", fontsize=4.8, color="#1B5E20", fontweight=700, ha="left", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    # latitudes / longitudes nas bordas
    for la in range(-60, 90, 30):
        ax.text(-182, la, f"{abs(la)}°{'N' if la > 0 else ('S' if la < 0 else '')}", fontsize=4.4, ha="right", va="center", color=INK, clip_on=False)
    for lo in range(-150, 181, 30):
        s = f"{abs(lo)}°" + ("L" if lo > 0 and lo < 180 else ("O" if lo < 0 else ""))
        ax.text(lo, lat0 - 1.2, s, fontsize=4.4, ha="center", va="top", color=INK, clip_on=False)
    # UTC no alto (fusos)
    for k in range(-12, 13):
        s = "0" if k == 0 else (f"+{k}" if k > 0 else f"−{abs(k)}")
        ax.text(15 * k, lat1 + 0.8, s, fontsize=4.4, ha="center", va="bottom", color="#37474F", fontweight=700, clip_on=False)
    ax.text(-188, lat1 + 0.8, "UTC", fontsize=4.4, ha="right", va="bottom", color="#37474F", fontweight=800, clip_on=False)
    # pontos de exemplo
    pts = [("Brasília\n15,8° S · 47,9° O", -47.9, -15.8, "left", 5, -9), ("Londres\n51,5° N · 0°", 0.0, 51.5, "right", -4, 6), ("Tóquio\n35,7° N · 139,7° L", 139.7, 35.7, "left", 4, 6)]
    for nm, lo, la, ha, dx, dy in pts:
        ax.plot(lo, la, marker="o", ms=3.4, mfc="#C62828", mec="white", mew=0.6, zorder=12)
        ax.text(lo + dx, la + dy, nm, fontsize=4.6, fontweight=700, color=INK, ha=ha, va="center", zorder=13,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85))
    ax.text(-178, lat1 - 3, "Hemisfério Norte", fontsize=5, fontweight=800, color="#37474F", ha="left", va="center", zorder=9)
    ax.text(-178, lat0 + 3, "Hemisfério Sul", fontsize=5, fontweight=800, color="#37474F", ha="left", va="center", zorder=9)
    ax.text(-90, lat0 + 3, "Hemisfério Ocidental (O)", fontsize=4.8, fontweight=700, color="#37474F", ha="center", va="center", zorder=9)
    ax.text(90, lat0 + 3, "Hemisfério Oriental (L)", fontsize=4.8, fontweight=700, color="#37474F", ha="center", va="center", zorder=9)
    ax.text(180, lat0 - 8.5, "Linha Internacional da Data ≈ 180°", fontsize=4.4, fontweight=700, color="#37474F", ha="right", va="center", clip_on=False)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_position([0.055, 0.085, 0.80, 0.80])
    fig.text(0.008, 0.985, "Planisfério: coordenadas geográficas e fusos horários (UTC)", fontsize=7.2, fontweight=800, color=INK, ha="left", va="top")
    fig.text(0.992, 0.02, "Projeção cilíndrica equidistante (plate carrée) · cada fuso = 15° = 1 hora · Brasil em verde-claro", fontsize=4.4, color=MUTED, ha="right", va="bottom")
    to_svg(fig, "map_coordenadas")


# ============================================================ fusos do Brasil
def fusos_brasil():
    W, H = 92, 78
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-75, -34.5, -28.5, 6.5)
    sa_land = countries("50m")
    bb = box(*box_ll)
    cc = sa_land.assign(geometry=sa_land.geometry.intersection(bb))
    cc = cc[~cc.geometry.is_empty].to_crs(crs)
    cc["geometry"] = cc.geometry.simplify(3000)
    cc.plot(ax=ax, fc="#ECE8DC", ec=BORDER, lw=0.3, zorder=1)
    st = states_br()
    fus = {"AC": -5, "AM": -4, "RR": -4, "RO": -4, "MT": -4, "MS": -4}
    cor = {-3: "#F2F2F2", -4: "#C3CAD4", -5: "#7C8797"}
    st = st.assign(utc=[fus.get(u, -3) for u in st["postal"]])
    sp = st.to_crs(crs); sp["geometry"] = sp.geometry.simplify(2500)
    for u, g in sp.groupby("utc"):
        g.plot(ax=ax, fc=cor[u], ec="#6D7A86", lw=0.35, zorder=3)
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=ax, color="#37474F", lw=0.7, zorder=8)
    for _, r in sp.iterrows():
        pt = r.geometry.representative_point()
        ax.text(pt.x, pt.y, r["postal"], fontsize=4.4, color="#263238", fontweight=700, ha="center", va="center", zorder=9)
    # ilhas oceânicas (UTC−2): Fernando de Noronha
    x, y = xy(crs, -32.42, -3.85)
    ax.plot(x, y, marker="o", ms=4.2, mfc="#1F2A44", mec="white", mew=0.6, zorder=12)
    label(ax, x - 9e4, y + 2.8e5, "Fernando de Noronha\ne ilhas oceânicas\nUTC−2", size=4.3, color="#1F2A44", weight=800, bg=0.88, ha="right")
    # sudoeste do AM
    x, y = xy(crs, -70.6, -6.9)
    label(ax, x + 2.4e5, y - 3.6e5, "sudoeste do AM:\nUTC−5", size=4.1, color="#37474F", weight=800, bg=0.88, ha="left")
    ax.annotate("", xy=(x, y), xytext=(x + 2.3e5, y - 3.0e5), arrowprops=dict(arrowstyle="-|>", color="#37474F", lw=0.5, mutation_scale=4), zorder=14)
    legend_box(ax, [("UTC−3 (horário de Brasília)", "patch", cor[-3], "#6D7A86"), ("UTC−4", "patch", cor[-4], "#6D7A86"), ("UTC−5", "patch", cor[-5], "#6D7A86"), ("UTC−2 (ilhas oceânicas)", "point", "#1F2A44")],
               loc="lower left", fs=4.7, bbox=(0.0, 0.0), borderpad=0.4, labelspacing=0.3, title="Fusos legais do Brasil")
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Fusos horários do Brasil", sub="Por Unidade da Federação (aproximação)", size=6.6)
    north_arrow(ax, fig, x=0.93, y=0.76, size=0.06)
    to_svg(fig, "map_fusos_brasil")


# ============================================================ projeções + Tissot
def _tissot(tr, lon0, lat0, r_deg=4.5, n=40):
    th = np.linspace(0, 2 * np.pi, n)
    r = np.deg2rad(r_deg)
    p0 = np.deg2rad(lat0)
    lat = np.arcsin(np.sin(p0) * np.cos(r) + np.cos(p0) * np.sin(r) * np.cos(th))
    lon = np.deg2rad(lon0) + np.arctan2(np.sin(th) * np.sin(r) * np.cos(p0), np.cos(r) - np.sin(p0) * np.sin(lat))
    x, y = tr.transform(np.rad2deg(lon), np.rad2deg(lat))
    return np.c_[x, y]


def projecoes():
    W, H = 188, 104
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=100)
    fig.patch.set_facecolor("#FFFFFF")
    cdf = countries("110m")
    cdf = cdf[cdf["ADM0_A3"] != "ATA"]
    specs = [
        ("A  Mercator", "cilíndrica · conforme", "+proj=merc +lon_0=0 +datum=WGS84 +units=m +no_defs", (-180, -75, 180, 80), 0),
        ("B  Gall–Peters", "cilíndrica · equivalente", "+proj=cea +lon_0=0 +lat_ts=45 +datum=WGS84 +units=m +no_defs", (-180, -75, 180, 80), 1),
        ("C  Azimutal equidistante (polar)", "plana · equidistante a partir do polo", "+proj=aeqd +lat_0=90 +lon_0=0 +datum=WGS84 +units=m +no_defs", (-180, -5, 180, 90), 2),
        ("D  Cônica de Lambert", "cônica · conforme", "+proj=lcc +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=0 +datum=WGS84 +units=m +no_defs", (-180, -10, 180, 85), 3),
    ]
    pw, ph = 0.488, 0.452
    pos = [(0.008, 0.535), (0.504, 0.535), (0.008, 0.045), (0.504, 0.045)]
    for (ti, sub, pj, (lo0, la0, lo1, la1), idx), (px, py) in zip(specs, pos):
        ax = fig.add_axes([px, py, pw, ph])
        ax.set_axis_off(); ax.set_aspect("equal")
        tr = Transformer.from_crs(4326, pj, always_xy=True)
        bbx = box(lo0, la0, lo1, la1)
        cc = cdf.assign(geometry=cdf.geometry.intersection(bbx))
        cc = cc[~cc.geometry.is_empty].to_crs(pj)
        # fundo (contorno da área)
        ring = []
        for t in np.linspace(0, 1, 60):
            ring.append((lo0 + (lo1 - lo0) * t, la0))
        for t in np.linspace(0, 1, 60):
            ring.append((lo1, la0 + (la1 - la0) * t))
        for t in np.linspace(1, 0, 60):
            ring.append((lo0 + (lo1 - lo0) * t, la1))
        for t in np.linspace(1, 0, 60):
            ring.append((lo0, la0 + (la1 - la0) * t))
        rx, ry = tr.transform([p[0] for p in ring], [p[1] for p in ring])
        ax.add_patch(MPoly(np.c_[rx, ry], fc=WATER, ec="#B5C4D1", lw=0.4, zorder=0))
        cc.plot(ax=ax, fc="#EDE9DD", ec=BORDER, lw=0.15, zorder=1)
        for nm, col in (("Greenland", C_RED), ("Africa", C_BLUE)):
            sel = cdf[cdf["NAME"] == nm]
            if nm == "Africa":
                sel = cdf[cdf["CONTINENT"] == "Africa"]
            sel = sel.assign(geometry=sel.geometry.intersection(bbx))
            sel = sel[~sel.geometry.is_empty].to_crs(pj)
            sel.plot(ax=ax, fc=col, ec="white", lw=0.1, alpha=0.88, zorder=2)
        # graticule
        for la in range(-60, 90, 30):
            if la < la0 + 1 or la > la1 - 1:
                continue
            xs, ys = tr.transform(np.linspace(lo0, lo1, 90), np.full(90, la))
            ok = np.isfinite(xs) & np.isfinite(ys)
            ax.plot(xs[ok], ys[ok], color="#8FA3B5", lw=0.2, zorder=3)
        for lo in range(-150, 181, 30):
            la_s = np.linspace(max(la0, -85), min(la1, 89.9), 60)
            xs, ys = tr.transform(np.full(60, lo), la_s)
            ok = np.isfinite(xs) & np.isfinite(ys)
            ax.plot(xs[ok], ys[ok], color="#8FA3B5", lw=0.2, zorder=3)
        # indicatrizes de Tissot
        lats = [-60, -30, 0, 30, 60] if idx < 2 else ([15, 40, 65] if idx == 3 else [15, 40, 65])
        lons = list(range(-150, 181, 60))
        for la in lats:
            for lo in lons:
                if idx == 0 and abs(la) > 70:
                    continue
                poly = _tissot(tr, lo, la, r_deg=5.0)
                if not np.isfinite(poly).all():
                    continue
                ax.add_patch(MPoly(poly, fc="#FFB300", ec="#8A5A00", lw=0.25, alpha=0.75, zorder=4))
        ax.autoscale_view()
        ax.set_xlim(min(rx) - 5e4, max(rx) + 5e4); ax.set_ylim(min(ry) - 5e4, max(ry) + 5e4)
        ax.text(0.01, 0.995, ti, transform=ax.transAxes, fontsize=6.4, fontweight=800, color=INK, ha="left", va="top", zorder=20,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
        ax.text(0.01, 0.90, sub, transform=ax.transAxes, fontsize=4.8, color=MUTED, ha="left", va="top", zorder=20,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    handles = [plt.Rectangle((0, 0), 1, 1, fc=C_RED), plt.Rectangle((0, 0), 1, 1, fc=C_BLUE), plt.Rectangle((0, 0), 1, 1, fc="#FFB300", ec="#8A5A00")]
    fig.legend(handles, ["Groenlândia (≈ 2,2 milhões km²)", "África (≈ 30,4 milhões km²: ≈ 14 vezes maior)", "Círculos de Tissot: todos teriam o mesmo tamanho e forma no globo"],
               loc="lower center", ncol=3, fontsize=4.9, frameon=False, bbox_to_anchor=(0.5, -0.005), handlelength=1.2, columnspacing=1.5)
    to_svg(fig, "map_projecoes")


# ============================================================ curvas de nível (relevo hipotético)
def curvas_nivel():
    W, H = 188, 62
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=100)
    fig.patch.set_facecolor("#FFFFFF")
    nx, ny = 301, 201
    x = np.linspace(0, 900, nx); y = np.linspace(0, 600, ny)
    X, Y = np.meshgrid(x, y)
    def g(cx, cy, sx, sy, a):
        return a * np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2))
    Z = 30 + 0.03 * X + g(250, 330, 120, 150, 140) + g(660, 250, 110, 120, 95) + g(430, 520, 130, 60, 30)
    axp = fig.add_axes([0.005, 0.06, 0.49, 0.80])
    axp.set_aspect("equal"); axp.set_axis_off(); axp.set_anchor("NW")
    axp.add_patch(plt.Rectangle((0, 0), 900, 600, fc="#F7F4EC", ec="#37474F", lw=0.6, zorder=0))
    levels = np.arange(20, 220, 10)
    cs = axp.contour(X, Y, Z, levels=levels, colors="#8D5B2E", linewidths=[0.55 if lv % 50 else 1.0 for lv in levels], zorder=2)
    axp.clabel(cs, levels=[lv for lv in levels if lv % 50 == 0], fontsize=4.4, fmt="%d m", inline=True, inline_spacing=2)
    # curso d'água: mínimo em x entre os dois morros (x∈[420,520]) para cada y
    ys = np.linspace(40, 590, 30)
    xs = []
    for yy in ys:
        row = Z[int(yy / 600 * (ny - 1))]
        seg = (x > 440) & (x < 540)
        xs.append(x[seg][np.argmin(row[seg])])
    axp.plot(xs, ys, color="#1565C0", lw=1.2, zorder=3)
    # linha do perfil
    A = (40, 330); B = (860, 260)
    axp.plot([A[0], B[0]], [A[1], B[1]], color=C_RED, lw=0.9, ls=(0, (4, 2)), zorder=5)
    axp.text(A[0] - 6, A[1], "A", fontsize=7, fontweight=800, color=C_RED, ha="right", va="center")
    axp.text(B[0] + 6, B[1], "B", fontsize=7, fontweight=800, color=C_RED, ha="left", va="center")
    # anotações
    def note(px, py, s, tx, ty, ha="left"):
        axp.annotate(s, xy=(px, py), xytext=(tx, ty), fontsize=4.5, fontweight=700, color=INK, ha=ha, va="center",
                     arrowprops=dict(arrowstyle="-", color="#37474F", lw=0.4), bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.9), zorder=10)
    note(250, 330, "curvas fechadas e\nconcêntricas: morro", 150, 520)
    note(125, 330, "curvas próximas:\nencosta íngreme", 20, 100)
    note(640, 450, "curvas afastadas:\nencosta suave", 640, 560)
    note(xs[8], ys[8], "curso d'água no vale", 700, 60)
    axp.set_xlim(-30, 930); axp.set_ylim(-5, 605)
    # escala gráfica (1:10.000 → 100 m = 1 cm)
    axp.plot([30, 230], [-0, -0], color=INK, lw=0, zorder=0)
    fig.text(0.008, 0.985, "Planta (vista de cima): curvas de nível a cada 10 m", fontsize=6.4, fontweight=800, color=INK, ha="left", va="top")
    fig.text(0.01, 0.005, "Relevo hipotético, ilustrativo · escala aprox. 1:10.000 (1 cm = 100 m) · equidistância 10 m", fontsize=4.6, color=MUTED, ha="left", va="bottom")
    # perfil
    axq = fig.add_axes([0.545, 0.19, 0.445, 0.58])
    t = np.linspace(0, 1, 400)
    px = A[0] + (B[0] - A[0]) * t; py = A[1] + (B[1] - A[1]) * t
    from scipy.interpolate import RegularGridInterpolator
    f = RegularGridInterpolator((y, x), Z)
    pz = f(np.c_[py, px])
    d = np.hypot(px - A[0], py - A[1])
    axq.fill_between(d, 0, pz, color="#D8C3A5", zorder=1)
    axq.plot(d, pz, color="#8D5B2E", lw=1.0, zorder=2)
    axq.set_xlim(0, d.max()); axq.set_ylim(0, 220)
    axq.set_xlabel("distância ao longo de A–B (m)", fontsize=4.8)
    axq.set_ylabel("altitude (m)", fontsize=4.8)
    axq.tick_params(labelsize=4.6, length=2, width=0.4)
    for sp in ("top", "right"):
        axq.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        axq.spines[sp].set_linewidth(0.5)
    axq.grid(axis="y", color="#CCD3DB", lw=0.3)
    imax = int(np.argmax(pz))
    axq.annotate("topo do morro\n≈ 170 m", xy=(d[imax], pz[imax]), xytext=(d[imax] - 150, 205), fontsize=4.5, fontweight=700, ha="center",
                 arrowprops=dict(arrowstyle="-", lw=0.4, color="#37474F"))
    iv = int(np.argmin(pz[(d > 380) & (d < 520)])) + int(np.argmax(d > 380))
    axq.annotate("vale", xy=(d[iv], pz[iv]), xytext=(d[iv], 25), fontsize=4.5, fontweight=700, ha="center", color="#1565C0",
                 arrowprops=dict(arrowstyle="-", lw=0.4, color="#1565C0"))
    axq.text(0, 232, "A", fontsize=7, fontweight=800, color=C_RED, ha="left", va="bottom", clip_on=False)
    axq.text(d.max(), 232, "B", fontsize=7, fontweight=800, color=C_RED, ha="right", va="bottom", clip_on=False)
    fig.text(0.545, 0.985, "Perfil topográfico A–B (exagero vertical ≈ 2×)", fontsize=6.4, fontweight=800, color=INK, ha="left", va="top")
    to_svg(fig, "curvas_nivel")


# ============================================================ cartograma de Dorling (população por UF)
def cartograma():
    W, H = 92, 80
    fig, ax = new_fig(W, H, bg="#FFFFFF")
    crs = BRASIL_AEA
    pop = json.load(open(ROOT / "data" / "processed" / "populacao_uf_2022.json", encoding="utf8"))["uf"]
    st = states_br().to_crs(crs)
    st = st[st["postal"].isin(pop.keys())].copy()
    pts = {r["postal"]: r.geometry.representative_point() for _, r in st.iterrows()}
    cx = {k: np.array([p.x, p.y]) for k, p in pts.items()}
    # área ∝ população: raio ∝ √pop
    k = 3.2e5 / math.sqrt(44411238)           # raio de SP ≈ 320 km (em unidades do mapa)
    R = {u: k * math.sqrt(v) * 1.0 for u, v in pop.items()}
    pos = {u: cx[u].copy() for u in pop}
    keys = list(pop.keys())
    for it in range(600):
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                d = pos[a] - pos[b]
                dist = float(np.hypot(*d)) or 1.0
                need = R[a] + R[b] + 6e3
                if dist < need:
                    push = (need - dist) / 2 * d / dist
                    pos[a] += push; pos[b] -= push
        for a in keys:
            pos[a] += (cx[a] - pos[a]) * 0.02
    reg = {}
    for u in ("AC", "AM", "AP", "PA", "RO", "RR", "TO"): reg[u] = ("Norte", "#2E8B57")
    for u in ("AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"): reg[u] = ("Nordeste", "#E65100")
    for u in ("DF", "GO", "MS", "MT"): reg[u] = ("Centro-Oeste", "#B8860B")
    for u in ("ES", "MG", "RJ", "SP"): reg[u] = ("Sudeste", "#7B3FA0")
    for u in ("PR", "RS", "SC"): reg[u] = ("Sul", "#1565C0")
    # contorno do Brasil (referência fraca)
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz["geometry"] = bz.geometry.simplify(4000)
    bz.plot(ax=ax, fc="#F4F1E8", ec="#C9D0DB", lw=0.5, zorder=0)
    for u in sorted(keys, key=lambda z: -R[z]):
        ax.add_patch(Circle(pos[u], R[u], fc=reg[u][1], ec="white", lw=0.5, alpha=0.9, zorder=3))
        if R[u] >= 1.4e5:
            ax.text(pos[u][0], pos[u][1], f"{u}\n{pop[u]/1e6:.1f}".replace(".", ","), fontsize=5.8, fontweight=800, color="white", ha="center", va="center", zorder=5, linespacing=1.05)
        elif R[u] >= 6.5e4:
            ax.text(pos[u][0], pos[u][1], u, fontsize=4.4, fontweight=800, color="white", ha="center", va="center", zorder=5)
        else:
            ax.text(pos[u][0] + R[u] + 1.2e4, pos[u][1], u, fontsize=4.0, fontweight=800, color=reg[u][1], ha="left", va="center", zorder=5)
    xs = [pos[u][0] for u in keys]; ys = [pos[u][1] for u in keys]
    pad = 2.3e5
    fit_extent(ax, fig, (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad + 3.5e5), 0.0)
    # legenda de áreas
    from collections import OrderedDict
    hs = [plt.Line2D([0], [0], marker="o", color="none", mfc=c, mec="white", ms=5, label=nm) for nm, c in OrderedDict((v[0], v[1]) for v in reg.values()).items()]
    leg = ax.legend(handles=hs, loc="lower left", fontsize=4.6, frameon=True, framealpha=0.92, edgecolor="#C9D0DB", title="Regiões", borderpad=0.4, labelspacing=0.3)
    leg.get_title().set_fontsize(4.9); leg.get_title().set_fontweight(700)
    # círculos de referência
    for j, (val, lab) in enumerate([(1e6, "1 milhão"), (10e6, "10 milhões")]):
        r = k * math.sqrt(val)
        cxr = ax.get_xlim()[1] - 2.2e5 - (1 - j) * 0 ; cyr = ax.get_ylim()[0] + 2.0e5 + (r if j == 1 else 0) + (0 if j == 1 else 0)
    r1, r10 = k * math.sqrt(1e6), k * math.sqrt(10e6)
    x0 = ax.get_xlim()[1] - 3.3e5; y0 = ax.get_ylim()[0] + 2.2e5
    ax.add_patch(Circle((x0, y0 + r10), r10, fc="none", ec="#37474F", lw=0.6, zorder=6))
    ax.add_patch(Circle((x0, y0 + r1), r1, fc="none", ec="#37474F", lw=0.6, zorder=6))
    ax.text(x0, y0 + 2 * r10 + 2.5e4, "10 milhões", fontsize=4.4, ha="center", va="bottom", color=INK, fontweight=700, zorder=6)
    ax.text(x0, y0 - 2.5e4, "1 milhão", fontsize=4.4, ha="center", va="top", color=INK, fontweight=700, zorder=6)
    map_title(ax, fig, "Cartograma de anamorfose: população por UF, 2022", sub="Área do círculo ∝ população (milhões de hab.) · IBGE, Censo 2022", size=6.2)
    north_arrow(ax, fig, x=0.93, y=0.78, size=0.06)
    to_svg(fig, "cartograma_pop")


def build():
    coordenadas()
    fusos_brasil()
    projecoes()
    curvas_nivel()
    cartograma()
