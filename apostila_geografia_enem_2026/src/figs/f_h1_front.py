"""Capa e página-guia: mapa de capa (Natural Earth, estilo escuro) e gráfico de incidência dos temas no ENEM."""
from geo import *
from figs.f_a2_mapas_fisica import world_outline
from svgkit import Fig, HALF, FULL, INK, MUTED
from common import save_svg


def capa_mapa():
    W, H = 210, 150
    bg = "#0E1730"
    fig, ax = new_fig(W, H, bg=bg)
    crs = EQEARTH
    outline, tr = world_outline(crs)
    ex, ey = outline.exterior.xy
    ax.fill(ex, ey, fc="#111D42", ec="#27407F", lw=0.5, zorder=0)
    c = countries("50m")
    c = c[c["ADM0_A3"] != "ATA"]
    cp = proj(c, crs, simplify=9000)
    cp = cp.assign(geometry=cp.geometry.buffer(0).intersection(outline))
    cp.plot(ax=ax, fc="#233A73", ec="#3B5AA6", lw=0.18, zorder=1)
    cp[cp["ADM0_A3"] == "BRA"].plot(ax=ax, fc="#FFB74D", ec="#0E1730", lw=0.25, zorder=3)
    for la in range(-60, 90, 30):
        xs, ys = tr.transform(np.linspace(-180, 180, 120), np.full(120, la))
        ax.plot(xs, ys, color="#2F4A8F", lw=0.25, ls=(0, (2, 2)), zorder=2)
    for lo in range(-150, 181, 30):
        xs, ys = tr.transform(np.full(80, lo), np.linspace(-85, 85, 80))
        ax.plot(xs, ys, color="#2F4A8F", lw=0.25, ls=(0, (2, 2)), zorder=2)
    xs, _ = tr.transform([-180, 180], [0, 0]); ax.set_xlim(xs[0] - 5e4, xs[1] + 5e4)
    _, ys = tr.transform([0, 0], [-58, 84]); ax.set_ylim(ys[0] - 5e4, ys[1] + 5e4)
    to_svg(fig, "capa_mapa")


def incidencia():
    rows = [("Espaço agrário", 12.4, "#8D5B2E", "pp. 13–19"), ("Urbano", 11.8, "#7B3FA0", "pp. 20–23"), ("Geopolítica", 11.2, "#C62828", "pp. 31–34"),
            ("Geologia", 6.5, "#8D5B2E", "pp. 3–5"), ("Domínios morfoclimáticos", 4.7, "#2E7D32", "pp. 10–11"), ("Climatologia", 4.7, "#1565C0", "pp. 7–8"),
            ("Transportes, comércio e serviços", 4.7, "#E65100", "pp. 28, 30"), ("Questões ambientais", 4.1, "#2E7D32", "pp. 12, 15, 21"), ("Migrações", 4.1, "#7B3FA0", "p. 24"),
            ("Cartografia e geoprocessamento", 3.5, "#546E7A", "pp. 35–37"), ("Solos", 3.5, "#8D5B2E", "pp. 6, 12, 16"), ("Energia", 3.5, "#E65100", "p. 30")]
    H = 24 + len(rows) * 16 + 24
    f = Fig(HALF, H, "incidencia_enem", "Incidência de temas de Geografia no ENEM, 2016–2025")
    W = HALF
    f.text(0, 0, "Quanto cai: temas de Geografia no ENEM (2016–2025)", 7.4, 800, INK)
    f.text(0, 11, "% das questões de Geografia · levantamento Aprova Total, conforme informado no projeto", 5.6, 500, MUTED)
    y = 28
    for nm, v, c, pg in rows:
        f.text(0, y + 5, nm, 6.0, 700, INK, valign="mid")
        bx = 138
        w = (W - bx - 70) * v / 12.4
        f.rect(bx, y, w, 11, fill=c, rx=2)
        f.text(bx + w + 4, y + 5.5, f"{v:.1f}%".replace(".", ","), 6.2, 800, c, valign="mid")
        f.text(W, y + 5.5, pg, 5.6, 600, MUTED, "end", valign="mid")
        y += 16
    f.text(0, y + 4, "Ordem de prioridade nesta apostila: mais páginas para os temas mais cobrados. Cores = módulo.", 5.6, 600, MUTED)
    save_svg("incidencia_enem", f.render())


def build():
    capa_mapa()
    incidencia()
