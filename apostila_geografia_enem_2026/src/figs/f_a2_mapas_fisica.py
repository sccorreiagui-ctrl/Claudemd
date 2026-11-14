"""Módulo A — mapas de Geografia Física (placas, massas de ar, rios voadores, hidrografia)."""
from geo import *
from shapely.ops import linemerge
from pyproj import Transformer

PT = {"PA": "Pacífica", "NA": "Norte-\nAmericana", "SA": "Sul-Americana", "AF": "Africana", "EU": "Eurasiática",
      "AN": "Antártica", "AU": "Australiana", "IN": "Indiana", "NZ": "Nazca", "CO": "Cocos", "CA": "Caribe",
      "AR": "Arábica", "PS": "Filipina", "SO": "Somali"}
C_DIV, C_TRA, C_CON = "#1565C0", "#B8860B", "#C62828"


def world_outline(crs, n=181):
    tr = Transformer.from_crs(4326, crs, always_xy=True)
    lon = np.linspace(-180, 180, n)
    lat = np.linspace(-90, 90, n)
    edge = np.r_[np.c_[lon, np.full_like(lon, 90)], np.c_[np.full(n, 180), lat[::-1]], np.c_[lon[::-1], np.full_like(lon, -90)], np.c_[np.full(n, -180), lat]]
    ex, ey = tr.transform(edge[:, 0], edge[:, 1])
    return Polygon(zip(ex, ey)), tr


def smooth_steps():
    """Classifica cada 'step' PB2002 em div/tra/con e suaviza por maioria numa janela de 5 passos
    (agrupa os pequenos offsets transformantes das dorsais ao sistema divergente)."""
    import pandas as pd
    st = plate_steps().copy()
    st = st[(st["STARTLONG"] - st["FINALLONG"]).abs() < 180]
    cat = {"OSR": "div", "CRB": "div", "OTF": "tra", "CTF": "tra", "SUB": "con", "OCB": "con", "CCB": "con"}
    st["cat"] = st["STEPCLASS"].map(cat)
    out = []
    for pb, g in st.groupby("PLATEBOUND", sort=False):
        g = g.sort_values("SEQNUM")
        c = g["cat"].tolist(); n = len(c); sm = c[:]
        for i in range(n):
            win = c[max(0, i - 2):min(n, i + 3)]
            sm[i] = max(set(win), key=lambda k: (win.count(k), k == c[i]))
        out.append(g.assign(cat=sm))
    return gpd.GeoDataFrame(pd.concat(out), crs=4326)


def placas():
    W, H = 188, 92
    fig, ax = new_fig(W, H, bg="#FFFFFF")
    crs = EQEARTH
    outline, tr = world_outline(crs)
    ex, ey = outline.exterior.xy
    ax.fill(ex, ey, fc=WATER, ec="#B5C4D1", lw=0.5, zorder=0)
    pastel = {"PA": "#E4EEF7", "NA": "#F3E9DA", "SA": "#E5F0DD", "AF": "#F6EBD0", "EU": "#EFE3EF", "AN": "#EEF2F5",
              "AU": "#F7E1DD", "IN": "#F3E4CF", "NZ": "#DDEFEA", "CO": "#EFE7D6", "CA": "#E6EBD8", "AR": "#F4E6D3", "PS": "#E3E8F3",
              "SO": "#F1EBDD"}
    pl = proj(plate_polys(), crs, simplify=25000)
    for _, r in pl.iterrows():
        gg = r.geometry.buffer(0).intersection(outline)
        gpd.GeoSeries([gg]).plot(ax=ax, fc=pastel.get(r["Code"], "#F0F0F0"), ec="none", zorder=1)
    ld = proj(land("110m"), crs, simplify=12000)
    ld = ld.assign(geometry=ld.geometry.buffer(0).intersection(outline))
    ld.plot(ax=ax, fc="none", ec="#7C8895", lw=0.3, zorder=3)
    for la in (0, 23.44, -23.44):
        xs, ys = tr.transform(np.linspace(-180, 180, 120), np.full(120, la))
        ax.plot(xs, ys, color="#8FA3B5", lw=0.3, ls=(0, (2, 2)), zorder=2)
    st = smooth_steps()
    cols = {"div": C_DIV, "tra": C_TRA, "con": C_CON}
    lws = {"div": 1.0, "tra": 0.95, "con": 1.25}
    for k in ("tra", "div", "con"):
        sub = st[st["cat"] == k]
        ml = linemerge(list(sub.geometry))
        g = gpd.GeoSeries([ml], crs=4326).to_crs(crs).simplify(7000)
        g.plot(ax=ax, color=cols[k], lw=lws[k], zorder=5)
    pos = {"PA": (-158, 8), "NA": (-102, 52), "SA": (-64, -37), "AF": (22, 3), "EU": (78, 57), "AN": (24, -79), "AU": (136, -27),
           "IN": (79, 15.5), "NZ": (-92, -26), "CO": (-107, 14), "CA": (-72, 15.5), "AR": (46, 24), "PS": (131, 15), "SO": (52, -4)}
    for k, (lo, la) in pos.items():
        x, y = tr.transform(lo, la)
        small = k in ("CO", "CA", "AR", "PS", "IN", "SO")
        label(ax, x, y, PT[k], size=(5.2 if small else 6.6), weight=(600 if small else 800), color="#2B3A4A", bg=0.0)

    def note(lo, la, s, dx=0, dy=0, ha="center", color=INK, bg=0.8):
        x, y = tr.transform(lo, la)
        label(ax, x + dx, y + dy, s, size=5.2, color=color, weight=600, bg=bg, ha=ha)
    note(-31, 38, "Dorsal\nMesoatlântica")
    note(-122, 36, "Falha de\nSan Andreas", ha="right", dx=-3e5, dy=2e5)
    note(-77, -10, "Andes", ha="right")
    note(88, 30.8, "Himalaia")
    note(142, 48, "Cinturão de Fogo\ndo Pacífico", color=C_CON, dx=1.5e6, dy=0)
    note(-46, -11, "BRASIL: interior da Placa\nSul-Americana (intraplaca)", color="#2E5E1F", bg=0.85)
    legend_box(ax, [("Divergente (afastamento)", "line", C_DIV, 1.6), ("Transformante (deslizamento lateral)", "line", C_TRA, 1.6),
                    ("Convergente (choque / subducção)", "line", C_CON, 1.8)], loc="lower left", fs=5.6, bbox=(0.0, 0.0), title="Tipo de limite")
    map_title(ax, fig, "Placas tectônicas e tipos de limite", x=0.008, y=0.99, size=7.6)
    north_arrow(ax, fig, x=0.975, y=0.14, size=0.07)
    ax.text(0.99, 0.012, "Projeção Equal Earth (equivalente) · escala variável", transform=fig.transFigure, ha="right", va="bottom", fontsize=5, color=MUTED, zorder=50)
    xs, _ = tr.transform([-180, 180], [0, 0]); ax.set_xlim(xs[0] - 1e5, xs[1] + 1e5)
    _, ys = tr.transform([0, 0], [-90, 90]); ax.set_ylim(ys[0] - 2e5, ys[1] + 2e5)
    to_svg(fig, "map_placas")


# ======================================================================================
# helpers para mapas do Brasil / América do Sul
# ======================================================================================
def ellipse_ll(lon0, lat0, a, b, rot=0, n=90):
    t = np.linspace(0, 2 * np.pi, n)
    x, y = a * np.cos(t), b * np.sin(t)
    r = np.deg2rad(rot)
    return lon0 + x * np.cos(r) - y * np.sin(r), lat0 + x * np.sin(r) + y * np.cos(r)


def sa_base(ax, crs, box_ll, brazil_states=True, land_fc="#EFEBE0", br_fc="#F7F4EC", border_lw=0.3):
    bb = box(*box_ll)
    c = countries("50m")
    c = c.assign(geometry=c.geometry.intersection(bb))
    c = c[~c.geometry.is_empty].to_crs(crs)
    c["geometry"] = c.geometry.simplify(2500)
    c.plot(ax=ax, fc=land_fc, ec=BORDER, lw=border_lw, zorder=1)
    if brazil_states:
        s = states_br()
        s = s.assign(geometry=s.geometry.intersection(bb))   # recorta à caixa (evita geometria fora do quadro no SVG)
        s = s[~s.geometry.is_empty].to_crs(crs)
        s["geometry"] = s.geometry.simplify(2500)
        s.plot(ax=ax, fc=br_fc, ec="#C3C9D0", lw=0.25, zorder=2)
    bz = countries("50m")
    bz = bz[bz["NAME"] == "Brazil"]
    bl = gpd.GeoSeries(bz.geometry.boundary.intersection(bb), crs=bz.crs).to_crs(crs).simplify(2500)
    bl.plot(ax=ax, color="#6D7A86", lw=0.6, zorder=3)


def xy(crs, lon, lat):
    return lonlat_to(crs, lon, lat)


def patch_ll(ax, crs, lon, lat, fc, alpha=0.4, ec=None, lw=0.6, zorder=6, hatch=None):
    x, y = lonlat_to(crs, np.asarray(lon), np.asarray(lat))
    ax.add_patch(MplPolygon(np.c_[x, y], closed=True, fc=fc, ec=ec or fc, alpha=alpha, lw=lw, zorder=zorder, hatch=hatch))


def flow_arrow(ax, crs, pts_ll, color, lw=3.0, alpha=0.9, head=9, zorder=12, edge=None, dash=None):
    """Seta suave (spline) por pontos lon/lat."""
    from scipy.interpolate import splprep, splev
    P = np.array([lonlat_to(crs, lo, la) for lo, la in pts_ll])
    if len(P) >= 3:
        tck, _ = splprep([P[:, 0], P[:, 1]], k=min(3, len(P) - 1), s=0)
        u = np.linspace(0, 1, 80)
        X, Y = splev(u, tck)
    else:
        X, Y = np.linspace(P[0, 0], P[1, 0], 40), np.linspace(P[0, 1], P[1, 1], 40)
    kw = dict(solid_capstyle="round", zorder=zorder)
    if dash:
        kw["ls"] = (0, dash)
    if edge:
        ax.plot(X[:-2], Y[:-2], color=edge, lw=lw + 1.2, alpha=alpha, solid_capstyle="round", zorder=zorder - 0.1)
    ax.plot(X[:-2], Y[:-2], color=color, lw=lw, alpha=alpha, **kw)
    if head > 1:
        a = FancyArrowPatch((X[-4], Y[-4]), (X[-1], Y[-1]), arrowstyle="-|>", mutation_scale=head, color=color, lw=0, alpha=alpha, zorder=zorder, shrinkA=0, shrinkB=0)
        ax.add_patch(a)
        if edge:
            b = FancyArrowPatch((X[-4], Y[-4]), (X[-1], Y[-1]), arrowstyle="-|>", mutation_scale=head + 2.5, color=edge, lw=0, alpha=alpha, zorder=zorder - 0.1, shrinkA=0, shrinkB=0)
            ax.add_patch(b)
    return X, Y


def set_ll_extent(ax, crs, box_ll, fig=None, margin=0.0):
    """Limites do eixo pela caixa lon/lat (projetada e densificada)."""
    lon0, lat0, lon1, lat1 = box_ll
    ll = []
    for t in np.linspace(0, 1, 40):
        ll += [(lon0 + (lon1 - lon0) * t, lat0), (lon0 + (lon1 - lon0) * t, lat1), (lon0, lat0 + (lat1 - lat0) * t), (lon1, lat0 + (lat1 - lat0) * t)]
    P = np.array([lonlat_to(crs, a, b) for a, b in ll])
    b = (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())
    fit_extent(ax, fig, b, margin) if fig is not None else set_extent(ax, b)
    return b


# ======================================================================================
# MASSAS DE AR
# ======================================================================================
def massas_ar():
    W, H = 124, 118
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-82, -40, -26, 11)
    sa_base(ax, crs, box_ll)
    masses = {
        "mEc": dict(c="#2E7D32", pos=(-64.5, -4.0), ab=(9.5, 5.2)),
        "mEa": dict(c="#00ACC1", pos=(-35.5, 4.2), ab=(7.5, 3.4)),
        "mTa": dict(c="#1E88E5", pos=(-31.5, -25.0), ab=(8.0, 6.2)),
        "mTc": dict(c="#EF6C00", pos=(-61.0, -23.5), ab=(4.6, 3.6)),
        "mPa": dict(c="#5E35B1", pos=(-55.0, -44.0), ab=(12.5, 6.8)),
    }
    for k, m in masses.items():
        lon, lat = ellipse_ll(m["pos"][0], m["pos"][1], m["ab"][0], m["ab"][1])
        patch_ll(ax, crs, lon, lat, fc=m["c"], alpha=0.30, ec=m["c"], lw=0.9, zorder=6)
    flow_arrow(ax, crs, [(-33.5, 3.0), (-40, 1.0), (-46.5, -1.8)], "#00ACC1", lw=2.0, head=9, edge="white")
    flow_arrow(ax, crs, [(-34.5, -23), (-38.5, -22.5), (-42.8, -21.3)], "#1E88E5", lw=2.0, head=9, edge="white")
    flow_arrow(ax, crs, [(-54.5, -41), (-51.0, -35), (-47.5, -29.5), (-44.5, -24.2)], "#5E35B1", lw=2.0, head=9, edge="white")
    flow_arrow(ax, crs, [(-60.5, -40.5), (-61.5, -32), (-62.5, -22), (-65.0, -13), (-67.5, -9)], "#5E35B1", lw=1.7, head=9, edge="white", dash=(4, 2.2))
    flow_arrow(ax, crs, [(-62.5, -6), (-58.5, -12.5), (-54.5, -19.5)], "#2E7D32", lw=1.7, head=8, edge="white")
    flow_arrow(ax, crs, [(-61.5, -21.5), (-58.2, -17.2)], "#EF6C00", lw=1.5, head=7, edge="white")
    lab = {"mEc": (-66, -2.0), "mEa": (-35.5, 5.4), "mTa": (-30.5, -26.0), "mTc": (-63.7, -25.2), "mPa": (-55, -41.8)}
    for k, (lo, la) in lab.items():
        x, y = xy(crs, lo, la)
        ax.text(x, y, k, fontsize=9, fontweight=800, color=masses[k]["c"], ha="center", va="center", zorder=20,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.7))
    x, y = xy(crs, -66.5, -10.8)
    label(ax, x, y, "friagem\n(inverno)", size=5.4, color="#5E35B1", weight=700, style="italic", bg=0.8)
    fl = [(-58.5, -35.5), (-52.5, -29.5), (-46.5, -25.5), (-40.5, -21.0)]
    fx = np.array([xy(crs, a, b) for a, b in fl])
    ax.plot(fx[:, 0], fx[:, 1], color="#37474F", lw=0.9, ls=(0, (4, 2)), zorder=15)
    x, y = xy(crs, -49.8, -33.4)
    label(ax, x, y, "Frente polar\n(encontro mPa × mTa)", size=5.3, color="#37474F", weight=600, bg=0.82)
    legend_box(ax, [("mEc  quente e úmida", "patch", "#2E7D32"), ("mEa  quente e úmida", "patch", "#00ACC1"), ("mTa  quente e úmida", "patch", "#1E88E5"),
                    ("mTc  quente e seca", "patch", "#EF6C00"), ("mPa  fria e úmida", "patch", "#5E35B1")],
               loc="upper left", fs=5.6, bbox=(0.0, 0.93), title="Massa de ar (áreas-fonte)")
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Massas de ar atuantes no Brasil", sub="Esquema simplificado: áreas-fonte e deslocamentos médios (variam com a estação)")
    north_arrow(ax, fig, x=0.955, y=0.82, size=0.06)
    scalebar(ax, fig, 1000, x=0.62, y=0.045)
    to_svg(fig, "map_massas_ar")


# ======================================================================================
# RIOS VOADORES
# ======================================================================================
def rios_voadores():
    W, H = 100, 104
    fig, ax = new_fig(W, H, bg=WATER)
    crs = SAM_AEA
    box_ll = (-82, -38, -30, 12)
    sa_base(ax, crs, box_ll, brazil_states=False, land_fc="#EFEBE0", br_fc="#F6F2E8")
    bi = biomes().to_crs(crs)
    bi["geometry"] = bi.geometry.simplify(4000)
    bi[bi["bioma"] == "Amazônia"].plot(ax=ax, fc="#9CCB8F", ec="#4E8F45", lw=0.5, alpha=0.9, zorder=4)
    pb = plate_bounds()
    nm = pb["Name"]
    andes = pb[nm.str.contains("NZ") & nm.str.contains("SA|AP|ND")].to_crs(crs)
    for g in andes.geometry:
        xs, ys = g.xy
        ax.plot(xs, ys, color="#6D4C41", lw=4.0, alpha=0.55, solid_capstyle="round", zorder=7)
        ax.plot(xs, ys, color="#4E342E", lw=0.8, alpha=0.9, zorder=7.2)
    blue, edge = "#42A5F5", "#0D47A1"
    flow_arrow(ax, crs, [(-31.0, 2.5), (-38, 0.5), (-47, -2.0), (-55, -3.5)], blue, lw=4.2, head=13, edge=edge)
    flow_arrow(ax, crs, [(-55, -3.5), (-63, -5.0), (-69.5, -8.5)], blue, lw=4.2, head=1, edge=edge)
    flow_arrow(ax, crs, [(-69.5, -8.5), (-66.5, -15), (-62, -21), (-57, -26), (-51.5, -28.7)], blue, lw=4.2, head=13, edge=edge)
    flow_arrow(ax, crs, [(-64.5, -16.5), (-58, -17.2), (-49.5, -18.5)], blue, lw=3.0, head=11, edge=edge)
    for lo, la in [(-60, -2), (-56, -6), (-64, -9), (-52, -9), (-61, -12)]:
        x0, y0 = xy(crs, lo, la)
        ax.annotate("", xy=(x0, y0 + 1.6e5), xytext=(x0, y0 - 0.4e5), arrowprops=dict(arrowstyle="-|>", color="#1B5E20", lw=0.9, mutation_scale=5), zorder=9)

    def tx(lo, la, s, **kw):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, **kw)
    tx(-41.5, 6.0, "Ventos alísios\ntrazem umidade do Atlântico", size=5.4, weight=600, color="#0D47A1", bg=0.8)
    tx(-60.5, -0.2, "Floresta amazônica:\nevapotranspiração", size=5.4, weight=700, color="#1B5E20", bg=0.8)
    tx(-78, -23, "Cordilheira\ndos Andes\n(barreira)", size=5.4, weight=700, color="#4E342E", bg=0.8)
    tx(-45.5, -13.7, "Centro-Oeste\ne Sudeste", size=5.6, weight=800, color="#37474F", bg=0.85)
    tx(-47.6, -31.5, "Sul e\nBacia do Prata", size=5.6, weight=800, color="#37474F", bg=0.85)
    tx(-67.0, -19.8, "“rios\nvoadores”", size=6.2, weight=800, color="#0D47A1", bg=0.85, style="italic")
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Esquema dos “rios voadores”", sub="Fluxo médio de vapor d’água (ilustrativo)")
    north_arrow(ax, fig, x=0.95, y=0.84, size=0.06)
    scalebar(ax, fig, 1000, x=0.60, y=0.05)
    to_svg(fig, "map_rios_voadores")


# ======================================================================================
# HIDROGRAFIA
# ======================================================================================
def hidrografia():
    W, H = 124, 118
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-75, -35, -30, 6)
    sa_base(ax, crs, box_ll, brazil_states=True, land_fc="#EDE9DD", br_fc="#F8F5EC")
    r = rivers("10m").cx[-76:-28, -36:8]
    r = r[r["scalerank"] <= 8]
    rr = r.to_crs(crs)
    for _, row in rr.iterrows():
        sr = row["scalerank"]
        lw = 1.35 if sr <= 3 else (0.9 if sr <= 5 else 0.55)
        for geom in ([row.geometry] if row.geometry.geom_type == "LineString" else list(row.geometry.geoms)):
            xs, ys = geom.xy
            ax.plot(xs, ys, color="#2F7FC1", lw=lw, zorder=5, solid_capstyle="round")
    sf = rr[rr["name"].str.replace(" ", "") == "SãoFrancisco"]
    for geom in sf.geometry:
        for g in ([geom] if geom.geom_type == "LineString" else list(geom.geoms)):
            ax.plot(*g.xy, color="#0D47A1", lw=1.9, zorder=6)
    dams = {"Itaipu": (-25.408, -54.589), "Belo Monte": (-3.127, -51.775), "Tucuruí": (-3.832, -49.647), "Sobradinho": (-9.43, -40.82),
            "Furnas": (-20.667, -46.318), "Sto. Antônio\ne Jirau": (-9.0, -64.2), "Paulo Afonso": (-9.40, -38.21)}
    off = {"Itaipu": (0.7e5, -0.5e5, "left"), "Belo Monte": (-0.3e5, 1.4e5, "center"), "Tucuruí": (0.55e5, -1.0e5, "left"), "Sobradinho": (-0.5e5, 1.0e5, "right"),
           "Furnas": (0.5e5, -0.6e5, "left"), "Sto. Antônio\ne Jirau": (0.0, -1.7e5, "center"), "Paulo Afonso": (0.9e5, -0.9e5, "left")}
    for n, (la, lo) in dams.items():
        x, y = xy(crs, lo, la)
        ax.plot(x, y, marker="s", ms=3.6, mfc="#37474F", mec="white", mew=0.5, zorder=12, ls="none")
        dx, dy, ha = off[n]
        label(ax, x + dx, y + dy, n, size=5.0, color="#263238", weight=600, ha=ha, bg=0.78)
    cx, cy = xy(crs, -39.31, -8.52)
    ax.plot(cx, cy, marker="o", ms=4.2, mfc="#E65100", mec="white", mew=0.6, zorder=13)
    for (lo, la) in [(-38.3, -6.2), (-37.0, -8.3)]:
        x1, y1 = xy(crs, lo, la)
        arrow_geo(ax, (cx, cy), (x1, y1), color="#E65100", lw=1.0, ms=6, ls="--", zorder=13)
    lx, ly = xy(crs, -34.3, -1.6)
    label(ax, lx, ly, "Transposição (PISF)\ncaptação em Cabrobó-PE\n(eixos Norte e Leste)", size=5.0, color="#BF360C", weight=700, ha="center", bg=0.88)
    ax.plot([lx - 0.25e5, cx + 0.2e5], [ly - 0.55e5, cy + 0.2e5], color="#E65100", lw=0.6, zorder=12)

    def txt(lo, la, s, size=5.4, color="#0D47A1", weight=700, rot=0, bg=0.7, style="normal", ha="center"):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=weight, rot=rot, bg=bg, style=style, ha=ha)
    txt(-60.8, -2.55, "Rio Amazonas", rot=5, size=5.8)
    txt(-62.0, -6.9, "Rio Madeira", size=5.0, rot=-35)
    txt(-53.9, -5.3, "Xingu", size=5.0, rot=-80)
    txt(-56.2, -5.1, "Tapajós", size=5.0, rot=-65)
    txt(-48.7, -9.2, "Tocantins–\nAraguaia", size=5.0)
    txt(-43.0, -13.5, "Rio São Francisco", size=5.6, rot=70, color="#0D47A1", weight=800)
    txt(-52.3, -23.0, "Rio Paraná", size=5.2)
    txt(-56.8, -20.3, "Rio Paraguai", size=5.0, rot=-80)
    txt(-54.4, -30.0, "Rio Uruguai", size=5.0, rot=-30)
    txt(-43.2, -6.0, "Parnaíba", size=5.0, rot=-80)
    legend_box(ax, [("Rios principais", "line", "#2F7FC1", 1.2), ("Rio São Francisco", "line", "#0D47A1", 2.0), ("Usina hidrelétrica (ex.)", "point", "#37474F", 4),
                    ("Captação do PISF", "point", "#E65100", 4.5)], loc="lower left", fs=5.5, bbox=(0.0, 0.0))
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Hidrografia brasileira: rios e usinas", sub="Rios: Natural Earth (1:10 mi). Usinas: posições aproximadas (exemplos)")
    north_arrow(ax, fig, x=0.955, y=0.82, size=0.06)
    scalebar(ax, fig, 1000, x=0.62, y=0.045)
    to_svg(fig, "map_hidrografia")


def build():
    placas()
    massas_ar()
    rios_voadores()
    hidrografia()
