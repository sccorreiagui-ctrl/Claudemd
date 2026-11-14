"""Caminhos e utilitários comuns."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
FIG_DIR = ROOT / "assets" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_svg(name: str, svg: str):
    """Grava SVG limpo (sem cabeçalho XML/DOCTYPE) em assets/figures/<name>.svg."""
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.S)
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    (FIG_DIR / f"{name}.svg").write_text(svg.strip(), encoding="utf-8")
    return FIG_DIR / f"{name}.svg"
