"""Converte Inter (OTF/CFF) para TrueType em subconjunto: o Chromium então incorpora fontes TrueType compactas (e não Type 3 por página)."""
import os
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools import subset

SRC = '/usr/share/fonts/opentype/inter/'
MAP = {'400': 'Inter-Regular', '500': 'Inter-Medium', '600': 'Inter-SemiBold', '700': 'Inter-Bold', '800': 'Inter-ExtraBold', '900': 'Inter-Black', '400i': 'Inter-Italic'}
UNI = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + list(range(0x370, 0x400)) + list(range(0x2000, 0x2070)) + list(range(0x2070, 0x20A0)) + [0x20AC] + \
      list(range(0x2190, 0x2200)) + list(range(0x2200, 0x2300)) + [0x25A0, 0x25CF, 0x25B2, 0x25BC, 0x2022, 0x2713, 0x2717]

def to_quad(gs, max_err=1.0):
    out = {}
    for g in gs.keys():
        pen = TTGlyphPen(gs); gs[g].draw(Cu2QuPen(pen, max_err, reverse_direction=True)); out[g] = pen.glyph()
    return out

def otf_to_ttf(f):
    order = f.getGlyphOrder()
    f['loca'] = newTable('loca'); f['glyf'] = glyf = newTable('glyf'); glyf.glyphOrder = order
    glyf.glyphs = to_quad(f.getGlyphSet()); del f['CFF ']
    if 'VORG' in f: del f['VORG']
    glyf.compile(f)
    hmtx = f['hmtx']
    for n, g in glyf.glyphs.items():
        if hasattr(g, 'xMin'): hmtx[n] = (hmtx[n][0], g.xMin)
    f['maxp'] = m = newTable('maxp'); m.tableVersion = 0x00010000
    m.maxZones = 1; m.maxTwilightPoints = 0; m.maxStorage = 0; m.maxFunctionDefs = 0; m.maxInstructionDefs = 0; m.maxStackElements = 0; m.maxSizeOfInstructions = 0
    m.maxComponentElements = max(len(getattr(g, 'components', [])) for g in glyf.glyphs.values())
    m.compile(f)
    p = f['post']; p.formatType = 2.0; p.extraNames = []; p.mapping = {}; p.glyphOrder = order
    f.sfntVersion = '\000\001\000\000'

def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    for w, name in MAP.items():
        dst = os.path.join(outdir, f'InterT-{w}.ttf')
        if os.path.exists(dst): continue
        f = TTFont(SRC + name + '.otf')
        opts = subset.Options(); opts.layout_features = ['kern', 'liga', 'calt', 'ccmp', 'locl', 'mark', 'mkmk']; opts.name_IDs = ['*']; opts.notdef_outline = True
        sub = subset.Subsetter(opts); sub.populate(unicodes=UNI); sub.subset(f)
        otf_to_ttf(f); f.save(dst)
    return outdir

if __name__ == '__main__':
    build(os.path.join(os.path.dirname(__file__), '..', 'build', 'fonts'))
