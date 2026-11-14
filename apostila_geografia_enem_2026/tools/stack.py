#!/usr/bin/env python3
"""Empilha PNGs de preview numa folha única: tools/stack.py out.png width in1.png in2.png ..."""
import sys
from PIL import Image
out, width, *ins = sys.argv[1:]
width = int(width)
ims = []
for p in ins:
    im = Image.open(p).convert("RGB")
    r = width / im.width
    ims.append(im.resize((width, int(im.height * r)), Image.LANCZOS))
H = sum(i.height for i in ims) + 6 * (len(ims) - 1)
sheet = Image.new("RGB", (width, H), (255, 255, 255))
y = 0
for im in ims:
    sheet.paste(im, (0, y)); y += im.height + 6
sheet.save(out); print(sheet.size)
