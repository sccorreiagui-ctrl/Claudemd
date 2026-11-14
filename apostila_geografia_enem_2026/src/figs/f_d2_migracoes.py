"""Módulo D — mapa esquemático das migrações internas brasileiras (base real: estados Natural Earth)."""
from geo import *
from figs.f_a2_mapas_fisica import sa_base, set_ll_extent, xy, flow_arrow


def mapa():
    W, H = 92, 104
    fig, ax = new_fig(W, H, bg=WATER)
    crs = BRASIL_AEA
    box_ll = (-76, -35.5, -32, 6.5)
    sa_base(ax, crs, box_ll, brazil_states=True, land_fc="#ECE8DC", br_fc="#F7F4EC")
    bz = countries("50m"); bz = bz[bz["NAME"] == "Brazil"].to_crs(crs)
    bz.boundary.plot(ax=ax, color="#37474F", lw=0.7, zorder=8)
    # Nordeste -> Sudeste (1950–1980)
    flow_arrow(ax, crs, [(-40.5, -9.0), (-42.5, -14.0), (-45.0, -19.0), (-46.6, -23.3)], "#7B3FA0", lw=3.0, head=11, edge="white", zorder=14)
    flow_arrow(ax, crs, [(-37.5, -7.5), (-40.0, -12.5), (-43.0, -20.5), (-44.0, -22.6)], "#7B3FA0", lw=2.2, head=9, edge="white", zorder=14)
    # Sul/Sudeste -> Centro-Oeste e Norte (1970–)
    flow_arrow(ax, crs, [(-52.0, -26.0), (-53.5, -20.0), (-55.5, -14.0), (-58.0, -10.0)], "#E65100", lw=2.6, head=10, edge="white", zorder=14)
    flow_arrow(ax, crs, [(-50.0, -22.5), (-52.0, -16.0), (-52.0, -9.0), (-52.0, -5.0)], "#E65100", lw=2.2, head=9, edge="white", zorder=14)
    # Migração de retorno ao Nordeste (1990–)
    flow_arrow(ax, crs, [(-46.5, -22.0), (-44.0, -16.0), (-41.0, -10.8), (-38.8, -8.0)], "#2E7D32", lw=2.0, head=9, edge="white", zorder=14, dash=(4, 2))
    def tx(lo, la, s, c, size=5.0, ha="center"):
        x, y = xy(crs, lo, la)
        label(ax, x, y, s, size=size, color=c, weight=800, bg=0.88, ha=ha)
    tx(-56.0, -25.5, "Sul → Centro-Oeste e Norte\n(1970 →)", "#B23C00", ha="right")
    tx(-33.5, -16.0, "Nordeste → Sudeste\n(1950–80)", "#4A148C", ha="right")
    tx(-33.8, -4.0, "retorno ao\nNordeste (1990 →)", "#1B5E20", ha="right")
    for nm, (lo, la) in {"São Paulo": (-46.6, -23.6), "Rio de Janeiro": (-43.2, -22.9), "Brasília": (-47.9, -15.8), "Manaus": (-60.0, -3.1)}.items():
        x, y = xy(crs, lo, la)
        ax.plot(x, y, marker="o", ms=3.2, mfc="#37474F", mec="white", mew=0.5, zorder=16)
        label(ax, x, y - 1.6e5, nm, size=4.8, color="#263238", weight=700, bg=0.8, ha="center")
    legend_box(ax, [("Emigração tradicional do Nordeste", "line", "#7B3FA0", 3), ("Fronteira agrícola e colonização", "line", "#E65100", 3),
                    ("Migração de retorno", "dash", "#2E7D32", 2)], loc="lower left", fs=4.9, bbox=(0.0, 0.0), handlelength=1.6, labelspacing=0.3, borderpad=0.4)
    set_ll_extent(ax, crs, box_ll, fig, 0.0)
    map_title(ax, fig, "Migrações internas no Brasil (esquema)", sub="Direção e sentido gerais dos fluxos; não é medição", size=6.8)
    north_arrow(ax, fig, x=0.93, y=0.80, size=0.055)
    scalebar(ax, fig, 1000, x=0.54, y=0.055, label_fs=5.2)
    to_svg(fig, "map_migracoes")


def build():
    mapa()
