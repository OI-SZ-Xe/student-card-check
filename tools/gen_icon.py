# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S = 256
img = Image.new("RGB", (S, S), "#1d2a23")
d = ImageDraw.Draw(img)
# desk stripes
for y in range(0, S, 8):
    d.line([0, y, S, y], fill="#22302a")
# card
card = Image.new("RGB", (196, 132), "#e4dbc2")
cd = ImageDraw.Draw(card)
cd.rectangle([0, 0, 195, 131], outline="#8d7c52", width=3)
cd.line([12, 30, 120, 30], fill="#8d7c52", width=2)
for i in range(4):
    cd.line([12, 52 + i * 18, 150 - i * 12, 52 + i * 18], fill="#b9ad8c", width=2)
cd.rectangle([150, 40, 184, 100], outline="#a9a184", width=2)
try:
    f = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 40)
    cd.text((14, 6), "学生证", font=f, fill="#20262a")
    f2 = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 22)
    cd.text((152, 62), "07", font=f2, fill="#4c5257")
except Exception:
    pass
card = card.rotate(-6, expand=True, fillcolor="#1d2a23")
img.paste(card, (32, 62))
# stamp
try:
    f3 = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 64)
    d.text((150, 150), "证", font=f3, fill="#a6301f")
except Exception:
    pass
d.rectangle([150, 148, 236, 236], outline="#a6301f", width=4)
img.save(r"F:\请出示学生证\icon_game.png")
print("icon ok")
