# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import os
OUT = r"F:\请出示学生证\art\props"
W, H = 90, 60
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([2, 10, 88, 56], radius=4, fill="#2b3430", outline="#121814", width=2)
d.rectangle([10, 18, 80, 30], fill="#0d1512", outline="#0a0f0c")
d.rectangle([10, 18, 80, 21], fill="#1b2620")
d.ellipse([68, 38, 80, 50], fill="#3f6b46", outline="#121814")
d.rectangle([14, 38, 50, 50], fill="#3a4a3c", outline="#121814")
d.line([16, 44, 48, 44], fill="#6d8a6e")
img = img.resize((W * 2, H * 2), Image.NEAREST)
img.save(os.path.join(OUT, "reader.png"))
print("reader.png")
