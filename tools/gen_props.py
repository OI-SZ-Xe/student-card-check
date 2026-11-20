# -*- coding: utf-8 -*-
import os, random
from PIL import Image, ImageDraw

OUT = r"F:\请出示学生证\art\props"
os.makedirs(OUT, exist_ok=True)
rng = random.Random(3)

def wood(w, h, base="#3b3a2f"):
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img)
    for y in range(h):
        for x in range(w):
            n = rng.randint(-5, 5)
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (max(0, r + n), max(0, g + n), max(0, b + n)))
    for i in range(w // 12):
        x = rng.randrange(w)
        d.line([(x, 0), (x + rng.randrange(-8, 8), h)], fill="#343328")
    return img

# tool tray
W, H = 410, 236
img = wood(W, H, "#33352c")
d = ImageDraw.Draw(img)
slots = [(18, 42, 198, 84), (212, 42, 392, 84), (18, 94, 198, 136), (212, 94, 392, 136), (18, 146, 198, 188), (212, 146, 392, 188)]
for s in slots:
    d.rectangle(s, fill="#242a24", outline="#4a544a")
    d.line([(s[0] + 2, s[3] - 2), (s[2] - 2, s[3] - 2)], fill="#1b201b")
img.save(os.path.join(OUT, "tool_tray.png"))

# stamp sprites
def stamp(color_hex, name):
    W, H = 180, 110
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # base
    d.rectangle([16, 66, 164, 96], fill="#5a4a36", outline="#2e2419")
    d.rectangle([16, 64, 164, 72], fill="#6b5943")
    # handle
    d.rectangle([74, 16, 106, 66], fill="#4a3a28", outline="#2a1f15")
    d.ellipse([62, 4, 118, 30], fill="#7a6448", outline="#33281b")
    # ink ring
    d.ellipse([30, 74, 60, 92], outline=color_hex, width=3)
    d.ellipse([120, 74, 150, 92], outline=color_hex, width=3)
    img.save(os.path.join(OUT, name))

stamp("#5fae72", "stamp_green.png")
stamp("#c0503f", "stamp_red.png")

# phone sprite
img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([16, 40, 104, 104], radius=10, fill="#2f3a33", outline="#121814", width=2)
for i in range(10):
    cx = 32 + (i % 3) * 26
    cy = 54 + (i // 3) * 16
    d.ellipse([cx, cy, cx + 12, cy + 12], fill="#8fa08c")
d.ellipse([70, 18, 112, 40], fill="#3b4740", outline="#121814")
img.save(os.path.join(OUT, "phone.png"))

# drawer front
img = wood(220, 90, "#43392c")
d = ImageDraw.Draw(img)
d.rectangle([6, 6, 214, 84], outline="#241c13", width=2)
d.rectangle([88, 40, 132, 52], fill="#8a7a5a", outline="#241c13")
img.save(os.path.join(OUT, "drawer.png"))
print("props generated")
