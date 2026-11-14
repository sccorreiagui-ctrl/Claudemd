"""Módulo B — mapas: domínios morfoclimáticos (Ab'Saber, aproximação) × biomas oficiais (IBGE)."""
from geo import *
from figs.f_a2_mapas_fisica import sa_base, set_ll_extent, xy, patch_ll, ellipse_ll
from shapely.geometry import Polygon as ShPoly, LineString as ShLine

# Cores por domínio / bioma equivalente
COL = {
    "Amazônia": "#2E7D32", "Cerrado": "#D9BE4F", "Caatinga": "#E39143", "Mata Atlântica": "#62A85B",
    "Pampa": "#A9D26E", "Pantanal": "#2AA79B", "Araucárias": "#1B6B4A",
}

# Polígono ESQUEMÁTICO da área de araucárias (Planalto Meridional) — usado só para subdividir a Mata Atlântica
ARAUC_LL = [(-54.0, -24.6), (-52.4, -23.9), (-50.8, -24.1), (-49.3, -24.2), (-48.9, -25.3), (-49.0, -26.4), (-49.4, -27.4),
            (-50.1, -28.3), (-50.0, -29.5), (-51.0, -29.9), (-52.5, -29.5), (-53.8, -28.6), (-54.1, -26.6)]
COCAIS_LL = [(-46.6, -3.0), (-43.2, -2.6), (-41.8, -3.7), (-41.4, -6.0), (-42.9, -7.6), (-44.9, -7.0), (-46.2, -5.3)]
AGRESTE_CL = [(-35.8, -6.0), (-36.3, -7.2), (-36.9, -8.6), (-37.8, -9.8), (-38.8, -11.0), (-39.6, -12.2)]


def _brazil_prep(crs):
    bi = biomes().to_crs(crs)
    bi["geometry"] = bi.geometry.simplify(4000)
    return bi


def mapa_dominios():
    W, H = 92, 104
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-76, -35.5, -32, 6.5)
    sa_base(ax, crs, box_ll, brazil_states=False, land_fc="#ECE8DC", br_fc="#F6F2E8")
    bi = _brazil_prep(crs)
    g = {r["bioma"]: r.geometry for _, r in bi.iterrows()}
    ar_x, ar_y = lonlat_to(crs, [p[0] for p in ARAUC_LL], [p[1] for p in ARAUC_LL])
    arauc = ShPoly(zip(ar_x, ar_y)).intersection(g["Mata Atlântica"])
    mares = g["Mata Atlântica"].difference(arauc)
    parts = {"Amazônico": (g["Amazônia"], COL["Amazônia"]), "Cerrados": (g["Cerrado"], COL["Cerrado"]), "Caatingas": (g["Caatinga"], COL["Caatinga"]),
             "Mares de Morros": (mares, COL["Mata Atlântica"]), "Araucárias": (arauc, COL["Araucárias"]), "Pradarias": (g["Pampa"], COL["Pampa"])}
    for k, (geom, c) in parts.items():
        gpd.GeoSeries([geom]).plot(ax=ax, fc=c, ec="white", lw=0.5, zorder=4)
    # faixas de transição (hachura): Pantanal (dado real), Mata dos Cocais e Agreste (traçado esquemático)
    mpl.rcParams["hatch.linewidth"] = 0.6
    gpd.GeoSeries([g["Pantanal"]]).plot(ax=ax, fc="#EAF6F4", ec="#00695C", lw=0.8, hatch="////", zorder=5)
    cx, cy = lonlat_to(crs, [p[0] for p in COCAIS_LL], [p[1] for p in COCAIS_LL])
    ax.add_patch(MplPolygon(np.c_[cx, cy], closed=True, fc="#FFFFFF", ec="#00695C", lw=0.8, alpha=0.55, hatch="////", zorder=6, ls=(0, (3, 2))))
    ag = ShLine([lonlat_to(crs, a, b) for a, b in AGRESTE_CL]).buffer(0.42e5)
    gpd.GeoSeries([ag]).plot(ax=ax, fc="#FFFFFF", ec="#00695C", lw=0.8, alpha=0.65, hatch="////", zorder=6)
    # contornos do Brasil
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=ax, color="#37474F", lw=0.7, zorder=8)

    def tx(lo, la, s, size=6.2, color="#FFFFFF", weight=800, bg=0.0, rot=0, ha="center"):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=weight, bg=bg, rot=rot, ha=ha)
    tx(-63, -5.5, "AMAZÔNICO", 7.2)
    tx(-48.7, -14.2, "CERRADOS", 7.0, "#3A2F00")
    tx(-41.6, -10.2, "CAATINGAS", 5.4, "#3A1D00", rot=0)
    tx(-45.5, -20.8, "MARES DE\nMORROS", 5.8, "#0F3D12")
    tx(-51.6, -26.2, "ARAU-\nCÁRIAS", 5.0, "#FFFFFF")
    tx(-53.5, -31.4, "PRADARIAS", 5.2, "#2D4A0B")
    tx(-57.3, -18.3, "Pantanal", 5.3, "#004D40", bg=0.8, weight=700)
    tx(-44.0, -4.8, "Cocais", 5.0, "#004D40", bg=0.8, weight=700)
    tx(-37.3, -8.2, "Agreste", 4.8, "#004D40", bg=0.8, weight=700, rot=62)
    legend_box(ax, [("Domínio (Ab’Saber)", "patch", "none", "none")][:0] + [
        ("Amazônico", "patch", COL["Amazônia"]), ("Cerrados", "patch", COL["Cerrado"]), ("Caatingas", "patch", COL["Caatinga"]),
        ("Mares de Morros", "patch", COL["Mata Atlântica"]), ("Araucárias (área esquemática)", "patch", COL["Araucárias"]), ("Pradarias", "patch", COL["Pampa"]),
        ("Faixas de transição", "hatch", "#00695C", "////", "#FFFFFF")], loc="lower left", fs=4.9, bbox=(0.0, 0.0), handlelength=1.2, labelspacing=0.3, borderpad=0.4)
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Domínios morfoclimáticos (Ab’Saber)", sub="Aproximação sobre biomas IBGE (Araucárias,\nCocais e Agreste: traçado esquemático)", size=6.8)
    north_arrow(ax, fig, x=0.93, y=0.80, size=0.055)
    scalebar(ax, fig, 1000, x=0.54, y=0.055, label_fs=5.2)
    to_svg(fig, "map_dominios")


def mapa_biomas():
    W, H = 92, 104
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-76, -35.5, -32, 6.5)
    sa_base(ax, crs, box_ll, brazil_states=False, land_fc="#ECE8DC", br_fc="#F6F2E8")
    bi = _brazil_prep(crs)
    area = bi.to_crs(crs).geometry.area
    tot = area.sum()
    for _, r in bi.iterrows():
        gpd.GeoSeries([r.geometry]).plot(ax=ax, fc=COL[r["bioma"]], ec="white", lw=0.5, zorder=4)
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=ax, color="#37474F", lw=0.7, zorder=8)
    pct = {r["bioma"]: 100 * r.geometry.area / tot for _, r in bi.iterrows()}
    pos = {"Amazônia": (-63, -5.5), "Cerrado": (-48.7, -14.4), "Caatinga": (-40.8, -9.0), "Mata Atlântica": (-49.3, -23.0), "Pampa": (-53.6, -31.2), "Pantanal": (-61.6, -18.9)}
    short = {"Amazônia": "AMAZÔNIA", "Cerrado": "CERRADO", "Caatinga": "CAATINGA", "Mata Atlântica": "MATA\nATLÂNTICA", "Pampa": "PAMPA", "Pantanal": "PANTANAL"}
    tc = {"Amazônia": "#FFFFFF", "Cerrado": "#3A2F00", "Caatinga": "#3A1D00", "Mata Atlântica": "#0F3D12", "Pampa": "#2D4A0B", "Pantanal": "#00574D"}
    for b, (lo, la) in pos.items():
        x, y = xy(crs, lo, la)
        size = 7.0 if b in ("Amazônia", "Cerrado") else (5.4 if b in ("Pampa", "Pantanal") else 5.8)
        label(ax, x, y, short[b] + f"\n{pct[b]:.0f}%", size=size, color=tc[b], weight=800, bg=(0.8 if b == "Pantanal" else 0.0))
    legend_box(ax, [(f"{k}", "patch", COL[k]) for k in ("Amazônia", "Cerrado", "Caatinga", "Mata Atlântica", "Pampa", "Pantanal")], loc="lower left", fs=5.0, bbox=(0.0, 0.0), handlelength=1.2, labelspacing=0.3, borderpad=0.4,
               title="Biomas continentais (IBGE)")
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Biomas do Brasil (IBGE)", sub="% da área do país; IBGE/MMA, 1:5.000.000", size=6.8)
    north_arrow(ax, fig, x=0.93, y=0.86, size=0.055)
    scalebar(ax, fig, 1000, x=0.54, y=0.055, label_fs=5.2)
    to_svg(fig, "map_biomas")
    return pct


def build():
    pct = mapa_biomas()
    mapa_dominios()
    print("   áreas % (IBGE/MMA 1:5M):", {k: round(v, 1) for k, v in pct.items()})
