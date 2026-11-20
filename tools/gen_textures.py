# -*- coding: utf-8 -*-
import os, random
from PIL import Image, ImageDraw, ImageFilter

OUT = r"F:\请出示学生证\art\tex"
os.makedirs(OUT, exist_ok=True)
rng = random.Random(7)

# desk: cold metal / painted wood
W = H = 256
img = Image.new("RGB", (W, H), "#39423f")
px = img.load()
for y in range(H):
    for x in range(W):
        n = rng.randint(-7, 7)
        px[x, y] = (57 + n, 66 + n, 63 + n)
img = img.filter(ImageFilter.GaussianBlur(0.4))
d = ImageDraw.Draw(img)
for i in range(90):
    x = rng.randrange(W)
    y = rng.randrange(H)
    ln = rng.randrange(6, 40)
    d.line([(x, y), (x + ln, y + rng.choice([0, 1, -1]))], fill=(48, 56, 54))
for i in range(26):
    x = rng.randrange(W)
    y = rng.randrange(H)
    d.line([(x, y), (x + rng.randrange(3, 12), y + rng.randrange(3, 12))], fill=(44, 52, 50))
img = img.filter(ImageFilter.GaussianBlur(0.3))
img.save(os.path.join(OUT, "desk.png"))

# paper: warm fiber
W = H = 256
img = Image.new("RGB", (W, H), "#e4dbc2")
px = img.load()
for y in range(H):
    for x in range(W):
        n = rng.randint(-5, 5)
        px[x, y] = (228 + n, 219 + n, 194 + n)
d = ImageDraw.Draw(img)
for i in range(320):
    x = rng.randrange(W)
    y = rng.randrange(H)
    d.point((x, y), fill=(206, 198, 172))
for i in range(40):
    x = rng.randrange(W)
    y = rng.randrange(H)
    d.line([(x, y), (x + rng.randrange(2, 7), y)], fill=(214, 206, 180))
img = img.filter(ImageFilter.GaussianBlur(0.2))
img.save(os.path.join(OUT, "paper.png"))
print("textures ok")
