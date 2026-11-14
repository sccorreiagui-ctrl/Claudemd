"""geo — utilitários cartográficos (GeoPandas + Matplotlib → SVG com texto real).

- Dados reais em data/raw (ver fetch_data.py). Nada de contornos inventados.
- Figuras são desenhadas em tamanho real (polegadas = mm/25,4); fontes em pt = pt impresso.
"""
from __future__ import annotations
import io, math, re, warnings
from functools import lru_cache
import numpy as np
import geopandas as gpd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Polygon as MplPolygon, Rectangle
from matplotlib.lines import Line2D
from shapely.geometry import box, Point, LineString, Polygon, MultiPolygon, shape
from shapely.ops import unary_union
from shapely import affinity
from common import RAW, save_svg, ROOT

warnings.filterwarnings("ignore")

for f in (ROOT / "assets" / "fonts").glob("Inter-*.ttf"):
    fm.fontManager.addfont(str(f))
mpl.rcParams.update({
    "svg.fonttype": "none", "font.family": "Inter", "font.size": 6.5, "axes.unicode_minus": False,
    "path.simplify": True, "path.simplify_threshold": 0.2, "axes.linewidth": 0.4,
})

# --------- paleta cartográfica ---------
WATER = "#DCEAF5"
LAND = "#F1EDE4"
LAND2 = "#E7E2D6"
BORDER = "#9CA7B3"
INK = "#1D2330"
MUTED = "#5B6475"
CORES = {
    "verde": "#2E7D32", "azul": "#1565C0", "terra": "#8D5B2E", "laranja": "#E65100", "roxo": "#7B3FA0",
    "vermelho": "#C62828", "cinza": "#546E7A", "navy": "#1F2A44", "ouro": "#B8860B",
}

# --------- projeções ---------
EQEARTH = "+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs"
ROBIN = "+proj=robin +lon_0=0 +datum=WGS84 +units=m +no_defs"
MERC = "+proj=merc +lon_0=0 +datum=WGS84 +units=m +no_defs"
BRASIL_AEA = "+proj=aea +lat_1=-2 +lat_2=-22 +lat_0=-12 +lon_0=-54 +datum=WGS84 +units=m +no_defs"
SAM_AEA = "+proj=aea +lat_1=-5 +lat_2=-35 +lat_0=-15 +lon_0=-60 +datum=WGS84 +units=m +no_defs"


def laea(lat0, lon0):
    return f"+proj=laea +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m +no_defs"


# --------- dados ---------
@lru_cache(maxsize=None)
def countries(res="50m") -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / f"ne_{res}_admin_0_countries.geojson")


@lru_cache(maxsize=None)
def land(res="50m"):
    return gpd.read_file(RAW / f"ne_{res}_land.geojson")


@lru_cache(maxsize=None)
def states_br() -> gpd.GeoDataFrame:
    s = gpd.read_file(RAW / "ne_50m_admin_1_states_provinces.geojson")
    return s[s["admin"] == "Brazil"].copy()


@lru_cache(maxsize=None)
def biomes() -> gpd.GeoDataFrame:
    import os
    os.environ["SHAPE_RESTORE_SHX"] = "YES"
    b = gpd.read_file(RAW / "biomas_2005.shp").set_crs(4674, allow_override=True).to_crs(4326)
    b["bioma"] = b["CD_LEGEN1"].str.title().replace({"Amazônia": "Amazônia", "Mata Atlântica": "Mata Atlântica"})
    return b


@lru_cache(maxsize=None)
def rivers(res="10m") -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / f"ne_{res}_rivers_lake_centerlines.geojson")


@lru_cache(maxsize=None)
def lakes() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "ne_50m_lakes.geojson")


@lru_cache(maxsize=None)
def places() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "ne_10m_populated_places_simple.geojson")


@lru_cache(maxsize=None)
def disputed() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "ne_10m_admin_0_boundary_lines_disputed_areas.geojson")


@lru_cache(maxsize=None)
def nine_dash() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson")


@lru_cache(maxsize=None)
def plate_steps() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "PB2002_steps.json")


@lru_cache(maxsize=None)
def plate_polys() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "PB2002_plates.json")


@lru_cache(maxsize=None)
def plate_bounds() -> gpd.GeoDataFrame:
    return gpd.read_file(RAW / "PB2002_boundaries.json")


def by_name(gdf, col, names):
    if isinstance(names, str):
        names = [names]
    return gdf[gdf[col].isin(names)]


def proj(gdf, crs, simplify=None):
    g = gdf.to_crs(crs)
    if simplify:
        g = g.copy()
        g["geometry"] = g.geometry.simplify(simplify, preserve_topology=True)
    return g


# --------- figura ---------
def new_fig(w_mm, h_mm, bg=WATER):
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_aspect("equal")
    if bg:
        fig.patch.set_facecolor(bg)
    return fig, ax


def set_extent(ax, bounds, pad=0.0):
    minx, miny, maxx, maxy = bounds
    dx, dy = (maxx - minx) * pad, (maxy - miny) * pad
    ax.set_xlim(minx - dx, maxx + dx)
    ax.set_ylim(miny - dy, maxy + dy)


def fit_extent(ax, fig, bounds, margin=0.02):
    """Ajusta limites para preencher a figura mantendo proporção (centraliza)."""
    minx, miny, maxx, maxy = bounds
    W, H = fig.get_size_inches()
    ar = W / H
    dx, dy = maxx - minx, maxy - miny
    dx *= (1 + 2 * margin); dy *= (1 + 2 * margin)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    if dx / dy > ar:
        dy = dx / ar
    else:
        dx = dy * ar
    ax.set_xlim(cx - dx / 2, cx + dx / 2)
    ax.set_ylim(cy - dy / 2, cy + dy / 2)


def to_svg(fig, name, w_mm=None, salt=None):
    """Salva SVG limpo (viewBox, 100% de largura, texto real)."""
    mpl.rcParams["svg.hashsalt"] = salt or name
    buf = io.StringIO()
    fig.savefig(buf, format="svg", facecolor=fig.get_facecolor())
    plt.close(fig)
    s = buf.getvalue()
    s = shrink_svg(s)
    s = re.sub(r'<svg([^>]*?)\swidth="[^"]*"\sheight="[^"]*"', r"<svg\1", s, count=1)
    s = s.replace("<svg ", '<svg role="img" aria-label="%s" style="width:100%%;height:auto;display:block" ' % name.replace("_", " "), 1)
    save_svg(name, s)
    return s


def shrink_svg(s: str, nd: int = 1) -> str:
    """Reduz casas decimais em dados de caminho (d="...") e pontos para diminuir o tamanho do arquivo."""
    num = re.compile(r"-?\d+\.\d{3,}")
    def fix_d(m):
        return m.group(1) + num.sub(lambda k: f"{float(k.group(0)):.{nd}f}", m.group(2)) + '"'
    s = re.sub(r'(\sd=")([^"]*)"', fix_d, s)
    s = re.sub(r'(\spoints=")([^"]*)"', fix_d, s)
    s = re.sub(r"\n\s*\n", "\n", s)
    return s


def label(ax, x, y, s, size=6.2, color=INK, weight=500, ha="center", va="center", bg=0.72, rot=0, style="normal", pad=0.18, zorder=30):
    kw = dict(fontsize=size, color=color, fontweight=weight, ha=ha, va=va, rotation=rot, style=style, zorder=zorder, linespacing=1.15)
    if bg:
        kw["bbox"] = dict(boxstyle=f"round,pad={pad}", fc="white", ec="none", alpha=bg)
    return ax.text(x, y, s, **kw)


def north_arrow(ax, fig, x=0.95, y=0.90, size=0.045, color=INK):
    """Seta de norte em coordenadas da figura (0–1). Apenas para mapas com norte para cima."""
    ax.annotate("", xy=(x, y + size), xytext=(x, y), xycoords="figure fraction",
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9, mutation_scale=6), zorder=40)
    ax.text(x, y + size + 0.012, "N", transform=fig.transFigure, ha="center", va="bottom", fontsize=7, fontweight=700, color=color, zorder=40)


def scalebar(ax, fig, km, x=0.06, y=0.05, unit_m=1000.0, color=INK, label_fs=6, n=2, bg=True):
    """Barra de escala gráfica (metros no CRS projetado) ancorada em coordenadas da figura."""
    xmin, xmax = ax.get_xlim()
    W = fig.get_size_inches()[0]
    frac = (km * unit_m) / (xmax - xmin)  # fração da largura
    x0 = x
    # fundo
    if bg:
        ax.add_patch(Rectangle((x0 - 0.012, y - 0.022), frac + 0.04, 0.062, transform=fig.transFigure, fc="white", ec="none", alpha=0.75, zorder=38))
    seg = frac / n
    for i in range(n):
        ax.add_patch(Rectangle((x0 + i * seg, y), seg, 0.011, transform=fig.transFigure, fc=(color if i % 2 == 0 else "white"), ec=color, lw=0.5, zorder=40))
    ax.text(x0, y + 0.017, "0", transform=fig.transFigure, fontsize=label_fs, ha="center", va="bottom", color=color, zorder=40)
    ax.text(x0 + frac, y + 0.017, f"{km:,} km".replace(",", "."), transform=fig.transFigure, fontsize=label_fs, ha="center", va="bottom", color=color, zorder=40)


def map_title(ax, fig, s, sub=None, x=0.012, y=0.985, size=7.6):
    ax.text(x, y, s, transform=fig.transFigure, ha="left", va="top", fontsize=size, fontweight=800, color=INK, zorder=45,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.8))
    if sub:
        ax.text(x, y - 0.048, sub, transform=fig.transFigure, ha="left", va="top", fontsize=5.6, color=MUTED, zorder=45,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.78))


def legend_box(ax, items, loc="lower left", fs=5.8, ncol=1, title=None, frame_alpha=0.88, bbox=None, handlelength=1.5, **kw):
    """items: [(rótulo, tipo, cor, (extra))] tipo: 'patch'|'line'|'dash'|'point'|'hatch'."""
    from matplotlib.patches import Patch
    hs = []
    for it in items:
        lab, kind, c = it[:3]
        if kind == "patch":
            hs.append(Patch(fc=c, ec=(it[3] if len(it) > 3 else "none"), lw=0.4, label=lab))
        elif kind == "hatch":
            hs.append(Patch(fc=(it[4] if len(it) > 4 else "white"), ec=c, hatch=it[3], lw=0.4, label=lab))
        elif kind == "line":
            hs.append(Line2D([0], [0], color=c, lw=(it[3] if len(it) > 3 else 1.2), label=lab))
        elif kind == "dash":
            hs.append(Line2D([0], [0], color=c, lw=(it[3] if len(it) > 3 else 1.0), ls=(0, (3, 2)), label=lab))
        elif kind == "point":
            hs.append(Line2D([0], [0], marker="o", color="none", markerfacecolor=c, markeredgecolor="white", markersize=(it[3] if len(it) > 3 else 4), label=lab))
        elif kind == "tri":
            hs.append(Line2D([0], [0], marker="^", color="none", markerfacecolor=c, markeredgecolor="white", markersize=5, label=lab))
    kwargs = dict(loc=loc, fontsize=fs, ncol=ncol, frameon=True, framealpha=frame_alpha, edgecolor="#C9D0DB", fancybox=True,
                  borderpad=0.5, labelspacing=0.35, handlelength=handlelength, handletextpad=0.5, columnspacing=1.0, title=title)
    if bbox:
        kwargs["bbox_to_anchor"] = bbox
    kwargs.update(kw)
    leg = ax.legend(handles=hs, **kwargs)
    leg.set_zorder(50)
    if title:
        leg.get_title().set_fontsize(fs + 0.3)
        leg.get_title().set_fontweight(700)
    return leg


def arrow_geo(ax, p0, p1, color=INK, lw=1.4, rad=0.0, style="-|>", ms=7, alpha=1.0, ls="-", zorder=35):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, connectionstyle=f"arc3,rad={rad}",
                        alpha=alpha, linestyle=ls, zorder=zorder, shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def lonlat_to(crs, lon, lat):
    from pyproj import Transformer
    t = Transformer.from_crs(4326, crs, always_xy=True)
    return t.transform(lon, lat)


def place_xy(name, crs, country=None):
    p = places()
    q = p[p["name"] == name]
    if country:
        q = q[q["adm0name"] == country]
    q = q.sort_values("pop_max", ascending=False).iloc[0]
    return lonlat_to(crs, q["longitude"], q["latitude"])
