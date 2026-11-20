# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw

OUT = r"F:\请出示学生证\art\icons"
os.makedirs(OUT, exist_ok=True)

def canvas():
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)

def save(img, name):
    img.resize((40, 40), Image.NEAREST).save(os.path.join(OUT, name + ".png"))

# compare: two overlapping rectangles
img, d = canvas()
d.rectangle([2, 5, 11, 14], outline="#cfe0c8", width=1)
d.rectangle([8, 7, 17, 16], outline="#9fbf9a", width=1)
save(img, "compare")

# magnifier
img, d = canvas()
d.ellipse([3, 3, 12, 12], outline="#cfe0c8", width=2)
d.line([12, 12, 17, 17], fill="#cfe0c8", width=2)
save(img, "magnifier")

# uv lamp
img, d = canvas()
d.rectangle([5, 8, 14, 15], fill="#cfe0c8")
d.line([9, 2, 9, 6], fill="#f0e0a0", width=1)
d.line([4, 4, 6, 6], fill="#f0e0a0", width=1)
d.line([14, 4, 12, 6], fill="#f0e0a0", width=1)
d.rectangle([7, 10, 12, 13], fill="#5a7a52")
save(img, "uv")

# phone
img, d = canvas()
d.rectangle([4, 2, 9, 17], fill="#cfe0c8")
d.rectangle([11, 5, 16, 15], fill="#9fbf9a")
d.point((13, 7), fill="#2a3a2a")
save(img, "phone")

# book / manual
img, d = canvas()
d.rectangle([3, 3, 16, 17], outline="#cfe0c8", width=1)
d.line([6, 7, 13, 7], fill="#9fbf9a")
d.line([6, 10, 13, 10], fill="#9fbf9a")
d.line([6, 13, 11, 13], fill="#9fbf9a")
save(img, "book")

# bag / shop
img, d = canvas()
d.rectangle([4, 7, 15, 17], outline="#cfe0c8", width=1)
d.arc([6, 3, 13, 11], 180, 360, fill="#cfe0c8")
save(img, "shop")

# arrest / cuffs
img, d = canvas()
d.ellipse([2, 6, 8, 12], outline="#e0c090", width=1)
d.ellipse([10, 6, 16, 12], outline="#e0c090", width=1)
d.line([8, 9, 10, 9], fill="#e0c090")
save(img, "arrest")

# exchange / chart
img, d = canvas()
d.line([3, 16, 17, 16], fill="#9fbf9a")
d.line([3, 12, 7, 8, 11, 11, 16, 4], fill="#cfe0c8", width=1)
save(img, "exchange")

print("icons written")
