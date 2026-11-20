# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw
OUT = r"F:\请出示学生证\art\props"
W, H = 300, 170
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
people = [(20, 96), (86, 104), (152, 92), (222, 100)]
for i, (x, h) in enumerate(people):
    col = (0.10, 0.13, 0.11, 0.85) if i % 2 == 0 else (0.08, 0.11, 0.09, 0.8)
    c = tuple(int(v * 255) for v in col)
    top = H - h
    # head
    d.ellipse([x + 8, top, x + 24, top + 16], fill=c)
    # body
    d.rectangle([x + 4, top + 16, x + 28, top + h - 30], fill=c)
    # legs
    d.rectangle([x + 7, top + h - 30, x + 14, H], fill=c)
    d.rectangle([x + 18, top + h - 30, x + 25, H], fill=c)
    # bag on some
    if i in (1, 3):
        d.rectangle([x - 2, top + 24, x + 8, top + 50], fill=c)
img.save(os.path.join(OUT, "queue.png"))
print("queue ok")
