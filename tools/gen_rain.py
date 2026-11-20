# -*- coding: utf-8 -*-
import os, random
from PIL import Image
OUT = r"F:\请出示学生证\art\props"
W, H = 400, 200
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = img.load()
random.seed(5)
for i in range(260):
    x = random.randrange(-40, W)
    y = random.randrange(0, H)
    ln = random.randrange(10, 26)
    for k in range(ln):
        xx, yy = x + k // 3, y + k
        if 0 <= xx < W and 0 <= yy < H:
            px[xx, yy] = (200, 220, 210, random.randrange(18, 44))
img.save(os.path.join(OUT, "rain.png"))
print("rain ok")
