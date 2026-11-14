#!/usr/bin/env python3
"""Converte Inter (OTF/CFF, licença OFL) em TTF subsetado (contornos TrueType) + WOFF2 em assets/fonts.
Motivo: Chromium embute OTF/CFF como Type 3 no PDF; TrueType é embutido como fonte real (texto pesquisável, arquivo menor)."""
import pathlib
from fontTools import subset
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

SRC = pathlib.Path("/usr/share/fonts/opentype/inter")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"
OUT.mkdir(parents=True, exist_ok=True)
UNICODES = ("U+0020-007E,U+00A0-017F,U+0192,U+02C6,U+02DC,U+2000-206F,U+2070-209F,U+20A0-20CF,U+2100-214F,"
            "U+2190-21FF,U+2200-22FF,U+2300-23FF,U+25A0-25FF,U+2600-26FF,U+2700-27BF,U+FEFF,U+FFFD")
FILES = {
    "Inter-Regular": ("Inter", 400, "normal"), "Inter-Medium": ("Inter", 500, "normal"),
    "Inter-SemiBold": ("Inter", 600, "normal"), "Inter-Bold": ("Inter", 700, "normal"),
    "Inter-ExtraBold": ("Inter", 800, "normal"), "Inter-Italic": ("Inter", 400, "italic"),
    "Inter-BoldItalic": ("Inter", 700, "italic"),
    "InterDisplay-Bold": ("Inter Display", 700, "normal"), "InterDisplay-ExtraBold": ("Inter Display", 800, "normal"),
}

def otf_to_ttf(font):
    font.recalcBBoxes = True
    order = font.getGlyphOrder()
    gs = font.getGlyphSet()
    glyf = newTable("glyf"); glyf.glyphOrder = order
    quad = {}
    for g in order:
        pen = TTGlyphPen(gs)
        gs[g].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        quad[g] = pen.glyph()
    glyf.glyphs = quad
    font["loca"] = newTable("loca"); font["glyf"] = glyf
    del font["CFF "]
    if "VORG" in font: del font["VORG"]
    glyf.compile(font)
    maxp = newTable("maxp"); maxp.tableVersion = 0x00010000
    for a in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions"):
        setattr(maxp, a, 1 if a == "maxZones" else 0)
    maxp.maxComponentElements = 0; maxp.numGlyphs = len(order)
    font["maxp"] = maxp
    post = font["post"]; post.formatType = 2.0; post.extraNames = []; post.mapping = {}; post.glyphOrder = order
    font.sfntVersion = "\x00\x01\x00\x00"

css = []
for stem, (fam, wt, sty) in FILES.items():
    opts = subset.Options(); opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "case", "tnum", "zero"]
    opts.name_IDs = [1, 2, 3, 4, 6]; opts.notdef_outline = True; opts.hinting = False
    f = subset.load_font(str(SRC / f"{stem}.otf"), opts)
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNICODES)); s.subset(f)
    otf_to_ttf(f)
    f.save(OUT / f"{stem}.ttf")
    f.flavor = "woff2"; f.save(OUT / f"{stem}.woff2")
    css.append(f"@font-face {{ font-family: '{fam}'; font-weight: {wt}; font-style: {sty}; font-display: block;\n"
               f"  src: url('../assets/fonts/{stem}.woff2') format('woff2'), url('../assets/fonts/{stem}.ttf') format('truetype'); }}")
    print(stem, (OUT / f"{stem}.ttf").stat().st_size // 1024, "KB ttf")
(pathlib.Path(__file__).resolve().parent.parent / "assets" / "css" / "fonts.css").write_text("\n".join(css) + "\n")
