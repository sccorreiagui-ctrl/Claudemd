"""Módulo E — mapas: polos industriais do Brasil (localização das cidades) e blocos econômicos no mundo.
Bases reais: Natural Earth (países e estados). Composição dos blocos conferida em nov/2026 (ver NOTES_PROJETO.md)."""
from geo import *
from matplotlib.lines import Line2D
from figs.f_a2_mapas_fisica import sa_base, set_ll_extent, xy, world_outline

# ------------------------------------------------------------------ polos industriais (Brasil)
CAT = {
    "auto": ("Indústria automobilística", "#E65100", "s"),
    "petro": ("Refino e petroquímica", "#6D4C41", "o"),
    "sider": ("Siderurgia e metalurgia", "#546E7A", "^"),
    "tech": ("Eletroeletrônica, aeroespacial e tecnologia", "#7B3FA0", "D"),
}
# (nome, lon, lat, categoria, dx_km, dy_km, ha) — localização aproximada das cidades-sede dos polos
HUBS_MAIN = [
    ("Manaus\n(Zona Franca)", -60.02, -3.12, "tech", 0, -260, "center"),
    ("Barcarena\n(alumínio)", -48.65, -1.52, "sider", -80, 190, "right"),
    ("Pecém", -38.84, -3.55, "sider", -130, 0, "right"),
    ("Suape e Goiana", -34.95, -7.98, "petro", -150, 120, "right"),
    ("Camaçari", -38.32, -12.70, "petro", -120, -60, "right"),
    ("Triunfo /\nPorto Alegre", -51.4, -29.9, "petro", -130, -40, "right"),
]
EXTRA_MAIN = [("Goiana", -35.00, -7.56, "auto")]
HUBS_SE = [
    ("Grande SP / ABC", -46.55, -23.65, "auto", -35, -55, "right"),
    ("Campinas", -47.06, -22.91, "tech", -40, 30, "right"),
    ("São José dos Campos\n(aeroespacial)", -45.89, -23.22, "tech", 40, -70, "left"),
    ("Betim", -44.20, -19.97, "auto", -35, 0, "right"),
    ("Vale do Aço", -42.54, -19.47, "sider", 35, 25, "left"),
    ("Volta Redonda", -44.10, -22.52, "sider", 12, 42, "left"),
    ("Duque de Caxias", -43.31, -22.79, "petro", 30, -45, "left"),
    ("Vitória", -40.24, -20.28, "sider", -25, -50, "right"),
    ("Curitiba /\nS. J. dos Pinhais", -49.21, -25.53, "auto", 45, -15, "left"),
]
SE_BOX = (-49.9, -26.6, -38.4, -17.4)


def _fit_ar(ax, b, ar, margin=0.0):
    minx, miny, maxx, maxy = b
    dx, dy = (maxx - minx) * (1 + 2 * margin), (maxy - miny) * (1 + 2 * margin)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    if dx / dy > ar:
        dy = dx / ar
    else:
        dx = dy * ar
    ax.set_xlim(cx - dx / 2, cx + dx / 2); ax.set_ylim(cy - dy / 2, cy + dy / 2)


def _bounds_ll(crs, box_ll):
    lon0, lat0, lon1, lat1 = box_ll
    pts = []
    for t in np.linspace(0, 1, 30):
        pts += [(lon0 + (lon1 - lon0) * t, lat0), (lon0 + (lon1 - lon0) * t, lat1), (lon0, lat0 + (lat1 - lat0) * t), (lon1, lat0 + (lat1 - lat0) * t)]
    P = np.array([lonlat_to(crs, a, b) for a, b in pts])
    return P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()


def mapa_industria():
    W, H = 188, 112
    fig, axm = new_fig(W, H, bg="#FFFFFF")
    crs = BRASIL_AEA
    fx = 0.585                                   # largura do painel principal (fração da figura)
    axm.set_position([0, 0, fx, 1])
    axm.add_patch(Rectangle((0, 0), 1, 1, transform=axm.transAxes, fc=WATER, ec="none", zorder=-5))
    box_ll = (-75, -34.5, -32.5, 6.5)
    sa_base(axm, crs, box_ll, brazil_states=True, land_fc="#ECE8DC", br_fc="#F7F4EC")
    st = states_br().to_crs(crs); st["geometry"] = st.geometry.simplify(2500)
    # Sudeste em destaque suave (concentração histórica da indústria)
    sudeste = st[st["postal"].isin(["SP", "RJ", "MG", "ES"])]
    sudeste.plot(ax=axm, fc="#FBE3CF", ec="none", zorder=2.5)
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=axm, color="#37474F", lw=0.7, zorder=8)
    b = _bounds_ll(crs, box_ll)
    _fit_ar(axm, b, (fx * W) / H, 0.0)

    def hub(ax, nm, lo, la, cat, dx, dy, ha, size, ms, scale_km=1000.0):
        x, y = xy(crs, lo, la)
        c = CAT[cat][1]
        ax.plot(x, y, marker=CAT[cat][2], ms=ms, mfc=c, mec="white", mew=0.6, zorder=16)
        if nm:
            label(ax, x + dx * scale_km, y + dy * scale_km, nm, size=size, color="#263238", weight=700, bg=0.88, ha=ha)
    for nm, lo, la, cat, dx, dy, ha in HUBS_MAIN:
        hub(axm, nm, lo, la, cat, dx, dy, ha, 4.7, 4.6)
    for nm, lo, la, cat in EXTRA_MAIN:
        hub(axm, "", lo, la, cat, 0, 0, "left", 4.7, 4.6)
    # retângulo do zoom
    x0, y0 = xy(crs, SE_BOX[0], SE_BOX[1]); x1, y1 = xy(crs, SE_BOX[2], SE_BOX[3])
    axm.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#B23C00", lw=0.9, ls=(0, (3, 2)), zorder=20))
    # legenda
    hs = [Line2D([0], [0], marker=CAT[k][2], color="none", mfc=CAT[k][1], mec="white", ms=5.2, label=CAT[k][0]) for k in CAT]
    map_title(axm, fig, "Brasil: polos industriais selecionados", sub="Localização aproximada das cidades-sede; não mede produção", size=6.8, x=0.008)
    north_arrow(axm, fig, x=0.52, y=0.80, size=0.055)
    scalebar(axm, fig, 1000, x=0.05, y=0.055, label_fs=5.0)

    # ---------------- zoom Sudeste
    bi = _bounds_ll(crs, SE_BOX)
    asp = (bi[2] - bi[0]) / (bi[3] - bi[1])
    iw = (1 - fx - 0.03) * W
    ih = iw / asp
    ix0 = (fx + 0.015) * W
    iy0 = H - ih - 8
    axi = fig.add_axes([ix0 / W, iy0 / H, iw / W, ih / H])
    axi.set_axis_off(); axi.set_aspect("equal")
    axi.add_patch(Rectangle((0, 0), 1, 1, transform=axi.transAxes, fc=WATER, ec="none", zorder=-5))
    sa_base(axi, crs, SE_BOX, brazil_states=True, land_fc="#ECE8DC", br_fc="#F7F4EC", border_lw=0.3)
    clipb = box(*bi)                                   # recorta a geometria ao zoom (evita SVG com geometria fora do quadro)
    sudeste_i = sudeste.assign(geometry=sudeste.geometry.intersection(clipb))
    sudeste_i.plot(ax=axi, fc="#FBE3CF", ec="none", zorder=2.5)
    st_b = gpd.GeoSeries(st.boundary.intersection(clipb), crs=st.crs)
    st_b.plot(ax=axi, color="#8F9AA6", lw=0.45, zorder=4)
    axi.set_xlim(bi[0], bi[2]); axi.set_ylim(bi[1], bi[3])
    for nm, lo, la in [("SP", -49.0, -21.3), ("MG", -45.2, -18.3), ("RJ", -42.2, -21.2), ("ES", -40.0, -18.5)]:
        x, y = xy(crs, lo, la)
        axi.text(x, y, nm, fontsize=9, fontweight=800, color="#8F9AA6", alpha=0.55, ha="center", va="center", zorder=3)
    for nm, lo, la, cat, dx, dy, ha in HUBS_SE:
        hub(axi, nm, lo, la, cat, dx, dy, ha, 4.6, 5.2)
    axi.add_patch(Rectangle((0, 0), 1, 1, transform=axi.transAxes, fc="none", ec="#B23C00", lw=0.9, ls=(0, (3, 2)), zorder=60, clip_on=False))
    fig.text((ix0 + 1) / W, 1 - 4.0 / H, "Zoom: Sudeste e Paraná", fontsize=6.4, fontweight=800, color="#B23C00", ha="left", va="center")
    # escala do zoom (200 km)
    frac = 200e3 / (bi[2] - bi[0])
    axi.add_patch(Rectangle((0.60, 0.05), frac / 2, 0.022, transform=axi.transAxes, fc="#1D2330", ec="#1D2330", lw=0.4, zorder=61))
    axi.add_patch(Rectangle((0.60 + frac / 2, 0.05), frac / 2, 0.022, transform=axi.transAxes, fc="white", ec="#1D2330", lw=0.4, zorder=61))
    axi.text(0.60, 0.085, "0", transform=axi.transAxes, fontsize=4.8, ha="center", va="bottom", zorder=61)
    axi.text(0.60 + frac, 0.085, "200 km", transform=axi.transAxes, fontsize=4.8, ha="center", va="bottom", zorder=61)
    fig.text((ix0 + 1) / W, (iy0 - 3.5) / H, "Os estados do Sudeste (SP, RJ, MG, ES), em tom claro, concentram\nhistoricamente a maior parte da indústria. O interior e o Nordeste\natraíram fábricas com incentivos fiscais (“guerra fiscal”); a Zona\nFranca de Manaus (1967) abriga a eletroeletrônica do Norte.",
             fontsize=4.9, color=INK, ha="left", va="top", linespacing=1.2)
    leg = fig.legend(handles=hs, loc="lower left", bbox_to_anchor=(ix0 / W, 3.0 / H), fontsize=4.9, frameon=True, framealpha=0.95, edgecolor="#C9D0DB",
                     title="Polos industriais (exemplos)", borderpad=0.5, labelspacing=0.4, handletextpad=0.5)
    leg.get_title().set_fontsize(5.2); leg.get_title().set_fontweight(700)
    # conectores
    inv = fig.transFigure.inverted()
    def fpt(ax, X, Y):
        return inv.transform(ax.transData.transform((X, Y)))
    p_tr = fpt(axm, x1, y1); p_br = fpt(axm, x1, y0)
    q_tl = (ix0 / W, (iy0 + ih) / H); q_bl = (ix0 / W, iy0 / H)
    for p, q in ((p_tr, q_tl), (p_br, q_bl)):
        fig.add_artist(Line2D([p[0], q[0]], [p[1], q[1]], transform=fig.transFigure, color="#B23C00", lw=0.6, ls=(0, (3, 2)), zorder=70))
    to_svg(fig, "map_industria")


# ------------------------------------------------------------------ blocos econômicos
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
USMCA = ["USA", "CAN", "MEX"]
MERCOSUL = ["ARG", "BRA", "PRY", "URY", "BOL"]
ASEAN = ["BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM", "TLS"]
EAEU = ["RUS", "BLR", "KAZ", "ARM", "KGZ"]
BLOCS = [
    ("União Europeia (27 países)", EU27, "#1F5FAE", None),
    ("USMCA (ex-NAFTA)", USMCA, "#C0572B", None),
    ("Mercosul (Estados Partes)", MERCOSUL, "#2E8B57", None),
    ("ASEAN (10 + Timor-Leste)", ASEAN, "#7B3FA0", None),
    ("União Econômica Eurasiática", EAEU, "#8D6E63", "////"),
]


def mapa_blocos():
    W, H = 188, 88
    fig, ax = new_fig(W, H, bg="#FFFFFF")
    crs = EQEARTH
    outline, tr = world_outline(crs)
    ex, ey = outline.exterior.xy
    ax.fill(ex, ey, fc=WATER, ec="#B5C4D1", lw=0.5, zorder=0)
    c = countries("50m")
    c = c[c["ADM0_A3"] != "ATA"]
    cp = proj(c, crs, simplify=9000)
    cp = cp.assign(geometry=cp.geometry.buffer(0).intersection(outline))
    cp.plot(ax=ax, fc=LAND, ec=BORDER, lw=0.22, zorder=1)
    for la in (0, 23.44, -23.44):
        xs, ys = tr.transform(np.linspace(-180, 180, 120), np.full(120, la))
        ax.plot(xs, ys, color="#8FA3B5", lw=0.3, ls=(0, (2, 2)), zorder=2)
    for nm, codes, col, hatch in BLOCS:
        sub = cp[cp["ADM0_A3"].isin(codes)]
        if hatch:
            sub.plot(ax=ax, fc="#EADFD8", ec=col, lw=0.25, hatch=hatch, zorder=3)
        else:
            sub.plot(ax=ax, fc=col, ec="white", lw=0.25, zorder=3)
    cp[cp["ADM0_A3"] == "VEN"].plot(ax=ax, fc="#BFE3CF", ec="#2E8B57", lw=0.3, hatch="....", zorder=3)

    def note(lo, la, s, dx=0, dy=0, ha="center", color=INK, size=5.2, bg=0.9, weight=800):
        x, y = tr.transform(lo, la)
        label(ax, x + dx, y + dy, s, size=size, color=color, weight=weight, bg=bg, ha=ha)

    def leader(lo, la, dx, dy, color="#37474F"):
        x, y = tr.transform(lo, la)
        ax.plot([x, x + dx], [y, y + dy], color=color, lw=0.5, zorder=14)
        ax.plot(x, y, marker="o", ms=1.6, mfc=color, mec="white", mew=0.3, zorder=15)

    note(-100, 49, "USMCA\nEUA · México · Canadá", color="#B34A1F")
    note(-53, -12.5, "Mercosul\nAR · BR · PY · UY · BO", color="#1F6E43")
    note(88, 61, "União Econômica Eurasiática\nRU · BY · KZ · AM · KG", color="#6D4C41", size=4.9)
    leader(11, 49, -1.5e6, 1.3e6); note(11, 49, "União Europeia\n(27 países)", dx=-2.4e6, dy=1.8e6, color="#1F5FAE")
    leader(121, 12.5, 2.3e6, 0.4e6); note(121, 12.5, "ASEAN\n(10 + Timor-Leste)", dx=4.1e6, dy=0.5e6, color="#5E2D80")
    note(20, 4, "África: União Africana (55 membros)\nZLC Continental (AfCFTA): em vigor desde 2019,\nimplementação gradual", color="#37474F", weight=700, size=4.6)
    legend_box(ax, [(b[0], "patch", b[2]) if not b[3] else (b[0], "hatch", b[2], b[3], "#EADFD8") for b in BLOCS] +
               [("Venezuela: Estado Parte do Mercosul,\nsuspensa desde 2016", "hatch", "#2E8B57", "....", "#BFE3CF")],
               loc="lower left", fs=4.9, bbox=(0.0, 0.0), title="Blocos (composição em nov/2026)", borderpad=0.4, labelspacing=0.3)
    xs, _ = tr.transform([-180, 180], [0, 0]); ax.set_xlim(xs[0] - 1e5, xs[1] + 1e5)
    _, ys = tr.transform([0, 0], [-56, 80]); ax.set_ylim(ys[0] - 1e5, ys[1] + 1e5)
    map_title(ax, fig, "Principais blocos econômicos regionais", x=0.008, y=0.99, size=7.6)
    north_arrow(ax, fig, x=0.975, y=0.17, size=0.07)
    ax.text(0.99, 0.012, "Projeção Equal Earth (equivalente) · escala variável · limites: Natural Earth (de fato), sem posição oficial · a Guiana Francesa é região da UE", transform=fig.transFigure,
            ha="right", va="bottom", fontsize=4.4, color=MUTED, zorder=50)
    to_svg(fig, "map_blocos")


def build():
    mapa_industria()
    mapa_blocos()
