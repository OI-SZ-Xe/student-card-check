# -*- coding: utf-8 -*-
import os, random
from PIL import Image, ImageDraw

OUT = r"F:\请出示学生证\art\props"
os.makedirs(OUT, exist_ok=True)
rng = random.Random(9)
W, H = 792, 372
img = Image.new("RGB", (W, H), "#2a3830")
d = ImageDraw.Draw(img)

# back wall panels
for x in range(0, W, 132):
    d.rectangle([x, 0, x + 126, 250], fill="#2f3d34")
    d.line([x + 126, 0, x + 126, 250], fill="#243029")
# ceiling light pools
for cx in range(80, W, 190):
    d.ellipse([cx - 60, -40, cx + 60, 40], fill="#3d4c40")
    d.ellipse([cx - 26, -8, cx + 26, 18], fill="#6d7a5e")
# floor
d.rectangle([0, 250, W, H], fill="#232c26")
for y in range(250, H, 14):
    d.line([0, y, W, y], fill="#1d251f")
# skirting
d.rectangle([0, 244, W, 252], fill="#1b221d")
# door on the left
d.rectangle([36, 60, 176, 250], fill="#3a4739")
d.rectangle([44, 68, 168, 250], fill="#42523f")
d.rectangle([120, 150, 132, 162], fill="#8a8a68")
d.line([44, 68, 168, 68], fill="#55684f")
# notice board
d.rectangle([300, 66, 470, 176], fill="#5a4a34")
d.rectangle([306, 72, 464, 170], fill="#d8cba4")
for i in range(6):
    px = 316 + (i % 3) * 48
    py = 82 + (i // 3) * 44
    d.rectangle([px, py, px + 36, py + 30], fill="#e8e0c4")
    d.line([px + 4, py + 8, px + 30, py + 8], fill="#8a8264")
    d.line([px + 4, py + 16, px + 26, py + 16], fill="#8a8264")
# clock
d.ellipse([600, 60, 660, 120], fill="#d8d2b8")
d.ellipse([606, 66, 654, 114], fill="#2a342c")
d.line([630, 90, 630, 74], fill="#d8d2b8")
d.line([630, 90, 644, 96], fill="#d8d2b8")
# poster
d.rectangle([520, 70, 578, 180], fill="#7a3a2c")
d.rectangle([526, 76, 572, 128], fill="#c9b58a")
d.line([530, 140, 568, 140], fill="#c9b58a")
d.line([530, 150, 560, 150], fill="#c9b58a")
# scuffs
for i in range(40):
    x = rng.randrange(W)
    y = rng.randrange(250, H)
    d.line([x, y, x + rng.randrange(2, 10), y], fill="#1a221c")
img.save(os.path.join(OUT, 'corridor.png'))
print("corridor ok")
