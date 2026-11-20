# -*- coding: utf-8 -*-
import os
from PIL import Image
OUT = r"F:\请出示学生证\art\portraits"
cols, rows = 6, 4
cw, ch = 192, 240
sheet = Image.new("RGB", (cols * cw, rows * ch), "#101312")
for i in range(24):
    im = Image.open(os.path.join(OUT, "p%d.png" % i))
    sheet.paste(im, ((i % cols) * cw, (i // cols) * ch))
sheet.save(r"F:\请出示学生证\docs\shots\portrait_sheet.png")
print("sheet ok")
