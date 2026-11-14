"""Módulo C — mapa da expansão da fronteira agrícola (base real IBGE/MMA + esquemas)."""
from geo import *
from figs.f_a2_mapas_fisica import sa_base, set_ll_extent, xy, flow_arrow, patch_ll
from shapely.ops import unary_union


def mapa():
    W, H = 124, 120
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-75, -34.5, -33, 6)
    sa_base(ax, crs, box_ll, brazil_states=True, land_fc="#ECE8DC", br_fc="#F7F4EC")
    bi = biomes().to_crs(crs)
    bi["geometry"] = bi.geometry.simplify(4000)
    g = {r["bioma"]: r.geometry for _, r in bi.iterrows()}
    # contexto (cores suaves)
    gpd.GeoSeries([g["Amazônia"]]).plot(ax=ax, fc="#CFE7C6", ec="none", zorder=3)
    gpd.GeoSeries([g["Cerrado"]]).plot(ax=ax, fc="#F3E2A0", ec="#C9A93A", lw=0.6, zorder=3)
    for b in ("Caatinga", "Mata Atlântica", "Pampa", "Pantanal"):
        gpd.GeoSeries([g[b]]).plot(ax=ax, fc="#E8E4D8", ec="none", zorder=3)
    st = states_br().to_crs(crs)
    st["geometry"] = st.geometry.simplify(3000)
    st.boundary.plot(ax=ax, color="#B9B2A0", lw=0.3, zorder=4)
    # MATOPIBA (aproximação): Cerrado dentro de MA, TO, PI, BA
    four = unary_union(list(st[st["postal"].isin(["MA", "TO", "PI", "BA"])].geometry))
    mat = g["Cerrado"].intersection(four)
    mpl.rcParams["hatch.linewidth"] = 0.5
    gpd.GeoSeries([mat]).plot(ax=ax, fc="#F7B267", ec="#E65100", lw=0.9, alpha=0.85, hatch="////", zorder=5)
    # Arco do desmatamento: faixa ao longo do limite Amazônia–Cerrado (limite real dos biomas)
    arc = g["Amazônia"].boundary.intersection(g["Cerrado"].buffer(45000))
    arcs = gpd.GeoSeries([arc])
    arcs.plot(ax=ax, color="#C62828", lw=7, alpha=0.30, zorder=6, capstyle="round")
    arcs.plot(ax=ax, color="#C62828", lw=1.0, alpha=0.9, zorder=6.1)
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=ax, color="#37474F", lw=0.7, zorder=8)
    # setas de avanço
    flow_arrow(ax, crs, [(-50.5, -25.8), (-51.8, -21.5), (-53.4, -17.2)], "#8D5B2E", lw=2.6, head=11, edge="white", zorder=14)
    flow_arrow(ax, crs, [(-53.2, -14.0), (-49.5, -11.6), (-46.2, -9.4)], "#E65100", lw=2.6, head=11, edge="white", zorder=14)
    flow_arrow(ax, crs, [(-56.2, -12.4), (-55.8, -9.4), (-55.0, -6.2)], "#C62828", lw=2.6, head=11, edge="white", zorder=14)

    def tx(lo, la, s, size=5.2, color=INK, weight=700, bg=0.82, ha="center", rot=0):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=color, weight=weight, bg=bg, ha=ha, rot=rot)
    tx(-63, -4.0, "AMAZÔNIA", 6.6, "#1B5E20", 800, 0.0)
    tx(-49.6, -15.8, "CERRADO", 6.4, "#7A5A00", 800, 0.0)
    tx(-56.5, -19.0, "1970–80: Cerrado\n(calagem, soja da Embrapa)", 5.0, "#5D3A1A", 800, 0.85, ha="right")
    tx(-47.0, -6.3, "MATOPIBA\n(aprox., 1990 → hoje)", 5.0, "#B23C00", 800, 0.85, ha="center")
    tx(-58.0, -7.0, "Arco do\ndesmatamento", 5.0, "#B71C1C", 800, 0.85, ha="right")
    tx(-50.8, -29.8, "origem: Sul e\nSudeste (SP, PR, RS)", 5.0, "#4E342E", 700, 0.85)
    for uf, (lo, la) in {"MT": (-55.5, -13.0), "GO": (-49.8, -16.4), "MS": (-54.5, -20.6), "TO": (-48.3, -10.2), "MA": (-45.4, -5.2), "PI": (-42.9, -7.6), "BA": (-42.0, -12.8), "PA": (-52.5, -4.2), "RO": (-62.8, -10.8)}.items():
        x, y = xy(crs, lo, la)
        ax.text(x, y, uf, fontsize=4.6, color="#6D7A86", ha="center", va="center", zorder=7)
    legend_box(ax, [("Cerrado (bioma IBGE)", "patch", "#F3E2A0", "#C9A93A"), ("MATOPIBA (aprox.: Cerrado em MA, TO, PI e BA)", "hatch", "#E65100", "////", "#F7B267"),
                    ("Arco do desmatamento (faixa ao longo do limite Amazônia–Cerrado)", "line", "#C62828", 4.0),
                    ("Setas: sentido geral da expansão (esquemático)", "line", "#37474F", 1.6)], loc="lower left", fs=4.9, bbox=(0.0, 0.0), handlelength=1.4, labelspacing=0.3, borderpad=0.4)
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Expansão da fronteira agrícola brasileira", sub="Biomas: IBGE/MMA. MATOPIBA e arco: aproximações; setas esquemáticas", size=7.0)
    north_arrow(ax, fig, x=0.955, y=0.78, size=0.055)
    scalebar(ax, fig, 1000, x=0.60, y=0.045, label_fs=5.2)
    to_svg(fig, "map_fronteira")


def build():
    mapa()
