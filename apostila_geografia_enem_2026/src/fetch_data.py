#!/usr/bin/env python3
"""Baixa os dados geoespaciais reais usados nos mapas (cache em data/raw).

Hosts acessíveis neste ambiente: raw.githubusercontent.com (espelhos oficiais/abertos).
Fontes primárias:
  - Natural Earth (domínio público) – repositório oficial nvkelso/natural-earth-vector
  - Bird (2003), PB2002 – limites de placas tectônicas (espelho fraxen/tectonicplates)
  - IBGE/MMA – Mapa de Biomas do Brasil (1:5.000.000), espelho SamanthaReiis/Biomas-Brasileiros
"""
import subprocess, sys, pathlib

RAW = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILES = {
    # Natural Earth
    "ne_110m_admin_0_countries.geojson": NE + "ne_110m_admin_0_countries.geojson",
    "ne_50m_admin_0_countries.geojson": NE + "ne_50m_admin_0_countries.geojson",
    "ne_10m_admin_0_countries.geojson": NE + "ne_10m_admin_0_countries.geojson",
    "ne_50m_admin_1_states_provinces.geojson": NE + "ne_50m_admin_1_states_provinces.geojson",
    "ne_10m_admin_1_states_provinces.geojson": NE + "ne_10m_admin_1_states_provinces.geojson",
    "ne_10m_admin_0_boundary_lines_land.geojson": NE + "ne_10m_admin_0_boundary_lines_land.geojson",
    "ne_10m_admin_0_boundary_lines_maritime_indicator.geojson": NE + "ne_10m_admin_0_boundary_lines_maritime_indicator.geojson",
    "ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson": NE + "ne_10m_admin_0_boundary_lines_maritime_indicator_chn.geojson",
    "ne_10m_geography_marine_polys.geojson": NE + "ne_10m_geography_marine_polys.geojson",
    "ne_10m_geography_regions_polys.geojson": NE + "ne_10m_geography_regions_polys.geojson",
    "ne_10m_rivers_lake_centerlines.geojson": NE + "ne_10m_rivers_lake_centerlines.geojson",
    "ne_50m_rivers_lake_centerlines.geojson": NE + "ne_50m_rivers_lake_centerlines.geojson",
    "ne_50m_lakes.geojson": NE + "ne_50m_lakes.geojson",
    "ne_10m_admin_0_boundary_lines_disputed_areas.geojson": NE + "ne_10m_admin_0_boundary_lines_disputed_areas.geojson",
    "ne_10m_populated_places_simple.geojson": NE + "ne_10m_populated_places_simple.geojson",
    "ne_50m_land.geojson": NE + "ne_50m_land.geojson",
    "ne_110m_land.geojson": NE + "ne_110m_land.geojson",
    # Placas tectônicas (Bird, 2003)
    "PB2002_boundaries.json": "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json",
    "PB2002_plates.json": "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_plates.json",
    "PB2002_steps.json": "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_steps.json",
    # Biomas IBGE/MMA
    "biomas_2005.shp": "https://raw.githubusercontent.com/SamanthaReiis/Biomas-Brasileiros/master/Shapefiles/MMA/biomas_2005.shp",
    "biomas_2005.shx": "https://raw.githubusercontent.com/SamanthaReiis/Biomas-Brasileiros/master/Shapefiles/MMA/biomas_2005.shx",
    "biomas_2005.dbf": "https://raw.githubusercontent.com/SamanthaReiis/Biomas-Brasileiros/master/Shapefiles/MMA/biomas_2005.dbf",
}

def main(only=None):
    for name, url in FILES.items():
        if only and not any(o in name for o in only):
            continue
        out = RAW / name
        if out.exists() and out.stat().st_size > 1000:
            print(f"ok (cache)  {name}  {out.stat().st_size/1e6:.2f} MB")
            continue
        r = subprocess.run(["curl", "-sS", "-L", "-m", "300", "--retry", "3", "-o", str(out), "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        size = out.stat().st_size if out.exists() else 0
        status = "OK " if code == "200" and size > 200 else "ERR"
        print(f"{status} {code}  {name}  {size/1e6:.2f} MB")
        if status == "ERR" and out.exists():
            out.unlink()

if __name__ == "__main__":
    main(sys.argv[1:] or None)
