"""Módulo F — mapas de Geopolítica (bases reais Natural Earth; temas esquemáticos e datados).
Regra editorial: separar fato verificável × reivindicação × status legal; não afirmar soberania de territórios
contestados; datar toda situação política. Frentes de combate e controle efetivo NÃO são desenhados."""
from geo import *
from matplotlib.lines import Line2D
from shapely.ops import split
import math
from figs.f_a2_mapas_fisica import world_outline, xy, flow_arrow

ADM = lambda: countries("10m")


def _world(W, H, lat=(-56, 80)):
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
    xs, _ = tr.transform([-180, 180], [0, 0]); ax.set_xlim(xs[0] - 1e5, xs[1] + 1e5)
    _, ys = tr.transform([0, 0], list(lat)); ax.set_ylim(ys[0] - 1e5, ys[1] + 1e5)
    return fig, ax, crs, tr, cp


def _badge(ax, x, y, n, color="#1D2330", size=6.6):
    ax.plot(x, y, marker="o", ms=size, mfc=color, mec="white", mew=0.7, zorder=30)
    ax.text(x, y, str(n), fontsize=size - 1.6, color="white", fontweight=800, ha="center", va="center", zorder=31)


# ============================================================ Guerra Fria
NATO89 = ["USA", "CAN", "GRL", "ISL", "NOR", "DNK", "GBR", "NLD", "BEL", "LUX", "FRA", "PRT", "ESP", "ITA", "GRC", "TUR"]
PACTO = ["RUS", "UKR", "BLR", "MDA", "EST", "LVA", "LTU", "GEO", "ARM", "AZE", "KAZ", "UZB", "TKM", "TJK", "KGZ",
         "POL", "CZE", "SVK", "HUN", "ROU", "BGR"]
OUTROS_SOC = ["CHN", "CUB", "PRK", "VNM", "LAO", "MNG", "ALB", "SRB", "MNE", "BIH", "HRV", "SVN", "MKD", "KOS"]


def guerra_fria():
    W, H = 188, 80
    fig, ax, crs, tr, cp = _world(W, H, (-47, 78))
    cN, cP, cO = "#1F5FAE", "#B71C1C", "#E39A93"
    cp[cp["ADM0_A3"].isin(NATO89)].plot(ax=ax, fc=cN, ec="white", lw=0.25, zorder=3)
    cp[cp["ADM0_A3"].isin(PACTO)].plot(ax=ax, fc=cP, ec="white", lw=0.25, zorder=3)
    cp[cp["ADM0_A3"].isin(OUTROS_SOC)].plot(ax=ax, fc=cO, ec="white", lw=0.25, zorder=3)
    g = cp[cp["ADM0_A3"] == "DEU"]
    g.plot(ax=ax, fc=cN, ec="white", lw=0.25, zorder=3)
    g.plot(ax=ax, fc="none", ec=cP, lw=0, hatch="////", zorder=4)
    # eventos
    ev = [(1, "Berlim (1961–89)", 13.4, 52.5), (2, "Cuba: crise dos mísseis (1962)", -79.5, 22.0), (3, "Coreia (1950–53)", 127.0, 38.0),
          (4, "Vietnã (1955–75)", 106.0, 15.5), (5, "Afeganistão (1979–89)", 67.7, 33.9)]
    for n, nm, lo, la in ev:
        x, y = tr.transform(lo, la)
        _badge(ax, x, y, n)

    def note(lo, la, s, size=5.4, color=INK, bg=0.0, weight=800, dx=0, dy=0, ha="center"):
        x, y = tr.transform(lo, la)
        label(ax, x + dx, y + dy, s, size=size, color=color, weight=weight, bg=bg, ha=ha)
    note(-100, 40, "EUA\n(OTAN)", color="white", size=6.2)
    note(85, 60, "URSS\n(Pacto de Varsóvia)", color="white", size=6.2)
    note(103, 34.5, "China", color="#5C1B16", size=5.2)
    note(-6, 20, "Demais países: não alinhados ou\nligados a outros tratados\n(ex.: Japão, Austrália)", color="#5B6475", size=4.7, weight=600)
    legend_box(ax, [("OTAN (1949): membros em 1989", "patch", cN), ("Pacto de Varsóvia (1955–91) e URSS", "patch", cP),
                    ("Outros Estados socialistas (fora do Pacto)", "patch", cO), ("Alemanha: dividida em RFA (OTAN) e RDA (Pacto)", "hatch", cP, "////", cN)],
               loc="lower left", fs=4.9, bbox=(0.0, 0.0), title="Alianças formais (c. 1980–89)", borderpad=0.4, labelspacing=0.3)
    # chave dos eventos
    items = [f"{n}  {nm}" for n, nm, lo, la in ev]
    ax.text(0.995, 0.03, "Pontos de tensão\n" + "\n".join(items), transform=fig.transFigure, ha="right", va="bottom", multialignment="left", fontsize=4.9, color=INK, zorder=45,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#C9D0DB", lw=0.5, alpha=0.92), linespacing=1.35)
    map_title(ax, fig, "Mundo bipolar: alianças formais (esquema com fronteiras atuais)", x=0.008, y=0.99, size=7.4)
    north_arrow(ax, fig, x=0.975, y=0.40, size=0.06)
    ax.text(0.99, 0.0, "Equal Earth · escala variável · Estados sucessores da URSS e da Iugoslávia representados por seus limites atuais", transform=fig.transFigure,
            ha="right", va="bottom", fontsize=4.2, color=MUTED, zorder=50)
    to_svg(fig, "map_guerra_fria")


# ============================================================ Mar da China Meridional
def mar_china():
    W, H = 60, 50
    fig, ax = new_fig(W, H, bg=WATER)
    crs = laea(12.5, 112.5)
    box_ll = (97.5, -3.5, 127.5, 29)
    c = ADM()
    bb = box(*box_ll)
    cc = c.assign(geometry=c.geometry.intersection(bb))
    cc = cc[~cc.geometry.is_empty].to_crs(crs)
    cc["geometry"] = cc.geometry.simplify(3000)
    cc.plot(ax=ax, fc="#EDE9DD", ec=BORDER, lw=0.3, zorder=1)
    nd = nine_dash().to_crs(crs)
    for g in nd.geometry:
        parts = g.geoms if hasattr(g, "geoms") else [g]
        for ln in parts:
            xs, ys = ln.xy
            ax.plot(xs, ys, color="#C62828", lw=1.1, ls=(0, (3, 1.6)), zorder=8)

    def pt(lo, la, nm, size=4.4, dx=0, dy=0, ha="center", ms=3.0, mc="#263238", w=700):
        x, y = xy(crs, lo, la)
        ax.plot(x, y, marker="o", ms=ms, mfc=mc, mec="white", mew=0.4, zorder=14)
        if nm:
            label(ax, x + dx * 1e3, y + dy * 1e3, nm, size=size, color="#263238", weight=w, bg=0.85, ha=ha)
    pt(112.0, 16.5, "Paracel", dx=-30, dy=105, ha="center")
    pt(114.5, 9.8, "Spratly", dx=120, dy=-40, ha="left")
    pt(117.8, 15.2, "Scarborough", dx=30, dy=90, ha="center")
    pt(115.9, 9.75, "", ms=2.4)
    pt(108.3, 3.9, "Natuna\n(Indonésia)", dx=-30, dy=-120, ha="center")

    def tx(lo, la, s, size=5.0, color="#37474F", w=800, ha="center", bg=0.0, rot=0):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=w, bg=bg, ha=ha, rot=rot)
    tx(110.0, 24.8, "CHINA", size=5.4)
    tx(106.0, 15.5, "VIETNÃ", size=4.8, rot=78)
    tx(121.2, 15.8, "FILIPINAS", size=4.8, rot=80)
    tx(121.0, 23.7, "Taiwan", size=4.6)
    tx(113.3, 3.2, "MALÁSIA", size=4.6, w=700)
    tx(115.0, 4.6, "Brunei", size=4.2, w=600)
    tx(103.0, -0.5, "INDONÉSIA", size=4.6)
    tx(116.5, 12.2, "MAR DA CHINA\nMERIDIONAL", size=5.2, color="#1565C0", w=800)
    legend_box(ax, [("Linha dos nove traços (reivindicação chinesa)", "dash", "#C62828", 1.3)], loc="lower left", fs=4.5, bbox=(0.0, 0.0), handlelength=1.8, borderpad=0.3)
    set_ll_extent_local(ax, crs, box_ll, fig)
    map_title(ax, fig, "Mar da China Meridional", sub="Reivindicações sobrepostas (esquema)", size=6.4)
    north_arrow(ax, fig, x=0.93, y=0.72, size=0.07)
    scalebar(ax, fig, 500, x=0.64, y=0.05, label_fs=4.6)
    to_svg(fig, "map_mar_china")


def set_ll_extent_local(ax, crs, box_ll, fig):
    from figs.f_a2_mapas_fisica import set_ll_extent
    return set_ll_extent(ax, crs, box_ll, fig, 0.0)


# ============================================================ Ucrânia / Crimeia
def ucrania():
    W, H = 60, 46
    fig, ax = new_fig(W, H, bg=WATER)
    crs = laea(49.0, 32.0)
    box_ll = (21.0, 43.0, 42.0, 54.6)
    c = ADM()
    bb = box(*box_ll)
    cc = c.assign(geometry=c.geometry.intersection(bb))
    cc = cc[~cc.geometry.is_empty].to_crs(crs)
    cc["geometry"] = cc.geometry.simplify(1500)
    cc.plot(ax=ax, fc="#EDE9DD", ec=BORDER, lw=0.3, zorder=1)
    ua = cc[cc["NAME"] == "Ukraine"]
    ua.plot(ax=ax, fc="#E3EAD3", ec="#6D7A86", lw=0.5, zorder=2)
    a1 = gpd.read_file(RAW / "ne_10m_admin_1_states_provinces.geojson")
    claimed = a1[(a1["admin"] == "Ukraine") & (a1["name"].isin(["Donets'k", "Luhans'k", "Zaporizhzhya", "Kherson"]))]
    claimed = claimed.assign(geometry=claimed.geometry.intersection(bb)).to_crs(crs)
    claimed.plot(ax=ax, fc="#FFD9B0", ec="#8D5B2E", lw=0.3, zorder=3)
    claimed.plot(ax=ax, fc="none", ec="#C62828", lw=0, hatch="xx", zorder=4)
    crim = a1[(a1["admin"] == "Russia") & (a1["name"].isin(["Crimea", "Sevastopol"]))]
    crim = crim.assign(geometry=crim.geometry.intersection(bb)).to_crs(crs)
    crim.plot(ax=ax, fc="#FFE9CC", ec="#8D5B2E", lw=0.3, zorder=3)
    crim.plot(ax=ax, fc="none", ec="#1565C0", lw=0, hatch="////", zorder=4)
    gpd.GeoSeries(cc[cc["NAME"] == "Ukraine"].geometry.boundary, crs=crs).plot(ax=ax, color="#37474F", lw=0.7, zorder=6)

    def tx(lo, la, s, size=4.6, color="#263238", w=700, ha="center", bg=0.85):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=w, bg=bg, ha=ha)
    tx(31.5, 49.3, "UCRÂNIA", size=5.6, w=800, bg=0.0)
    tx(27.0, 52.1, "BELARUS", size=4.6, color="#6D7A86", w=700, bg=0.0)
    tx(38.4, 51.7, "RÚSSIA", size=4.8, color="#6D7A86", w=700, bg=0.0)
    tx(34.2, 45.0, "Crimeia", size=4.3, color="#0D47A1", w=800, bg=0.85)
    tx(38.8, 48.6, "Donetsk\nLuhansk", size=4.0, color="#8E1B1B", w=800, bg=0.85, ha="left")
    tx(35.9, 47.3, "Zaporíjia", size=4.0, color="#8E1B1B", w=800, bg=0.85)
    tx(33.0, 46.9, "Kherson", size=4.0, color="#8E1B1B", w=800, bg=0.85, ha="right")
    for nm, lo, la in [("Kyiv", 30.52, 50.45), ("Odesa", 30.73, 46.48), ("Kharkiv", 36.23, 49.99), ("Sevastopol", 33.52, 44.6)]:
        x, y = xy(crs, lo, la)
        ax.plot(x, y, marker="o", ms=2.2, mfc="#263238", mec="white", mew=0.4, zorder=14)
        left = nm not in ("Odesa", "Sevastopol")
        label(ax, x + (4e4 if left else -4e4), y - 3.2e4, nm, size=3.8, color="#263238", weight=600, bg=0.7, ha=("left" if left else "right"))
    legend_box(ax, [("Crimeia e Sevastopol (anexação russa de 2014)", "hatch", "#1565C0", "////", "#FFE9CC"),
                    ("4 regiões (anexação declarada em 2022)", "hatch", "#C62828", "xx", "#FFD9B0")], loc="lower left", fs=3.9, bbox=(0.0, 0.0), borderpad=0.3, handlelength=1.4, labelspacing=0.25)
    set_ll_extent_local(ax, crs, box_ll, fig)
    map_title(ax, fig, "Ucrânia: territórios em disputa", sub="Controle efetivo varia e não é representado", size=6.0)
    north_arrow(ax, fig, x=0.94, y=0.76, size=0.08)
    scalebar(ax, fig, 200, x=0.70, y=0.05, label_fs=4.4)
    to_svg(fig, "map_ucrania")


# ============================================================ Israel e territórios palestinos (referência)
def oriente_medio():
    W, H = 60, 60
    fig, ax = new_fig(W, H, bg=WATER)
    crs = laea(31.4, 35.4)
    box_ll = (33.2, 29.3, 37.6, 34.5)
    c = ADM()
    bb = box(*box_ll)
    cc = c.assign(geometry=c.geometry.intersection(bb))
    cc = cc[~cc.geometry.is_empty]
    base = cc[~cc["NAME"].isin(["Israel", "Palestine"])].to_crs(crs)
    base["geometry"] = base.geometry.simplify(400)
    base.plot(ax=ax, fc="#EDE9DD", ec=BORDER, lw=0.3, zorder=1)
    isr = c[c["NAME"] == "Israel"].geometry.iloc[0]
    # Golã: parte de Israel (NE) a leste da linha reivindicada pela Síria
    d = disputed()
    L = d.loc[17].geometry
    co = list(L.coords)

    def ext(p, q, k=0.03):
        dx, dy = p[0] - q[0], p[1] - q[1]
        n = math.hypot(dx, dy)
        return (p[0] + dx / n * k, p[1] + dy / n * k)
    Le = LineString([ext(co[0], co[1])] + co + [ext(co[-1], co[-2])])
    golan, isr_main = None, isr
    for g in split(isr, Le).geoms:
        if g.centroid.x > 35.65 and g.centroid.y > 32.7:
            golan = g
        else:
            isr_main = g
    pal = c[c["NAME"] == "Palestine"].geometry.iloc[0]
    def draw(geom, **kw):
        gs = gpd.GeoSeries([geom.intersection(bb)], crs=4326).to_crs(crs)
        gs = gs.simplify(250)
        gs.plot(ax=ax, **kw)
    draw(isr_main, fc="#DCE8F4", ec="#37474F", lw=0.5, zorder=3)
    draw(pal, fc="#F4E4C8", ec="#37474F", lw=0.5, zorder=3)
    draw(pal, fc="none", ec="#8D5B2E", lw=0, hatch="////", zorder=4)
    if golan is not None:
        draw(golan, fc="#E9DDF2", ec="#37474F", lw=0.5, zorder=3)
        draw(golan, fc="none", ec="#7B3FA0", lw=0, hatch="....", zorder=4)

    def tx(lo, la, s, size=4.6, color="#263238", w=700, ha="center", bg=0.0, rot=0):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=w, bg=bg, ha=ha, rot=rot)
    tx(34.85, 31.0, "ISRAEL", size=5.4, w=800, color="#1F4E79")
    tx(35.31, 32.12, "Cisjordânia", size=4.2, color="#6B4423", w=800, ha="left", bg=0.85)
    tx(34.3, 31.28, "Faixa de\nGaza", size=4.0, color="#6B4423", w=800, ha="right", bg=0.85)
    tx(35.95, 33.02, "Golã", size=4.2, color="#4A148C", w=800, ha="left", bg=0.85)
    tx(36.6, 31.5, "JORDÂNIA", size=4.8, color="#6D7A86", w=700)
    tx(33.9, 30.0, "EGITO\n(Sinai)", size=4.6, color="#6D7A86", w=700)
    tx(36.4, 33.3, "SÍRIA", size=4.6, color="#6D7A86", w=700)
    tx(35.4, 33.78, "LÍBANO", size=4.0, color="#6D7A86", w=700, ha="left")
    tx(33.6, 32.4, "Mar\nMediterrâneo", size=4.4, color="#1565C0", w=700, ha="left")
    for nm, lo, la, dx, ha in [("Jerusalém", 35.21, 31.77, 4e3, "left"), ("Tel Aviv", 34.78, 32.08, -6e3, "right")]:
        x, y = xy(crs, lo, la)
        ax.plot(x, y, marker="o", ms=2.2, mfc="#263238", mec="white", mew=0.4, zorder=14)
        label(ax, x + dx, y, nm, size=3.9, color="#263238", weight=600, bg=0.75, ha=ha)
    legend_box(ax, [("Territórios palestinos (ONU: ocupados)", "hatch", "#8D5B2E", "////", "#F4E4C8"), ("Golã: Síria reivindica; Israel administra", "hatch", "#7B3FA0", "....", "#E9DDF2")],
               loc="lower right", fs=3.8, bbox=(1.0, 0.0), borderpad=0.3, handlelength=1.4, labelspacing=0.25)
    set_ll_extent_local(ax, crs, box_ll, fig)
    map_title(ax, fig, "Israel e territórios palestinos", sub="Referência (limites de fato, aprox.)", size=5.8)
    north_arrow(ax, fig, x=0.93, y=0.80, size=0.07)
    scalebar(ax, fig, 100, x=0.07, y=0.045, label_fs=4.4)
    to_svg(fig, "map_oriente_medio")


# ============================================================ Rotas e gargalos
CHOKE = [
    (1, "Estreito de Málaca", 1.3, 103.8), (2, "Estreito de Ormuz", 26.5, 56.4), (3, "Bab el-Mandeb", 12.6, 43.3),
    (4, "Canal de Suez", 30.5, 32.35), (5, "Bósforo e Dardanelos", 40.6, 28.9), (6, "Estreito de Gibraltar", 35.97, -5.6),
    (7, "Canal do Panamá", 9.1, -79.7), (8, "Cabo da Boa Esperança", -34.4, 18.5),
]
ROTA_MAR = [(113.4, 22.0), (111.2, 18.0), (109.4, 11.5), (107.0, 6.5), (104.6, 2.7), (103.0, 1.6), (100.0, 3.2), (96.0, 5.6), (90.0, 5.4), (84.0, 4.8), (79.5, 5.2),
       (72.0, 8.4), (63.0, 11.2), (53.0, 12.5), (43.6, 12.7), (40.0, 17.0), (37.0, 22.0), (34.0, 27.0), (32.5, 30.0), (30.2, 33.0), (25.0, 35.2), (20.0, 37.0)]
ROTA_TERRA = [(108.9, 34.3), (103.8, 36.1), (94.0, 40.0), (87.6, 43.8), (76.9, 43.2), (69.2, 41.3), (59.6, 38.0), (51.4, 35.7), (44.0, 38.0), (35.0, 39.5), (29.0, 41.0), (23.3, 42.7), (19.0, 47.5), (11.0, 50.0), (6.8, 51.4)]


def rotas():
    W, H = 188, 90
    fig, ax, crs, tr, cp = _world(W, H, (-56, 80))
    X = lambda lo, la: tr.transform(lo, la)
    flow_arrow(ax, crs, ROTA_MAR, "#1565C0", lw=1.6, head=7, edge="white", zorder=12)
    flow_arrow(ax, crs, ROTA_TERRA, "#E65100", lw=1.6, head=7, edge="white", zorder=12)
    # alternativa pelo Cabo (tracejada)
    flow_arrow(ax, crs, [(43.6, 12.7), (49.5, 6.5), (46.0, -2.0), (42.0, -13.0), (37.0, -26.0), (29.0, -35.0), (19.0, -36.5), (10.0, -30.0), (6.0, -15.0), (3.0, 0.0), (-8.0, 4.0), (-22.0, 12.0), (-24.0, 22.0), (-16.0, 32.0), (-8.5, 36.0)], "#6D7A86", lw=0.9, head=5, edge=None, zorder=10, dash=(3, 2))
    for n, nm, la, lo in CHOKE:
        x, y = X(lo, la)
        _badge(ax, x, y, n, color="#C62828", size=6.8)

    def note(lo, la, s, size=4.8, color=INK, bg=0.85, weight=700, dx=0, dy=0, ha="center"):
        x, y = X(lo, la)
        label(ax, x + dx, y + dy, s, size=size, color=color, weight=weight, bg=bg, ha=ha)
    note(78, -6, "Rota Marítima da Seda\n(esquema)", color="#0D47A1", size=4.7)
    note(60, 47, "Cinturão Econômico\n(terrestre, esquema)", color="#B23C00", dy=0.6e6, size=4.7)
    note(-35, -22, "Alternativa pelo Cabo\n(desvio do Mar Vermelho)", color="#37474F", size=4.5, weight=600)
    items = [f"{n}  {nm}" for n, nm, la, lo in CHOKE]
    ax.text(0.995, 0.03, "Gargalos marítimos\n" + "\n".join(items), transform=fig.transFigure, ha="right", va="bottom", multialignment="left", fontsize=4.9, color=INK, zorder=45,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#C9D0DB", lw=0.5, alpha=0.92), linespacing=1.35)
    legend_box(ax, [("Rota Marítima da Seda (esquemática)", "line", "#1565C0", 1.8), ("Cinturão Econômico (esquemático)", "line", "#E65100", 1.8), ("Desvio pelo Cabo da Boa Esperança", "dash", "#6D7A86", 1.2)],
               loc="lower left", fs=4.9, bbox=(0.0, 0.0), title="Rotas", borderpad=0.4, labelspacing=0.3)
    map_title(ax, fig, "Gargalos marítimos e rotas da Nova Rota da Seda", x=0.008, y=0.99, size=7.4)
    north_arrow(ax, fig, x=0.975, y=0.40, size=0.06)
    ax.text(0.99, 0.0, "Equal Earth · traçados das rotas são esquemáticos, não representam rotas reais · posições aproximadas dos gargalos", transform=fig.transFigure,
            ha="right", va="bottom", fontsize=4.2, color=MUTED, zorder=50)
    to_svg(fig, "map_rotas")


def build():
    guerra_fria()
    mar_china()
    ucrania()
    oriente_medio()
    rotas()
