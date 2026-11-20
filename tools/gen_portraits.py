# -*- coding: utf-8 -*-
import os, random
from PIL import Image, ImageDraw

OUT = r"F:\请出示学生证\art\portraits"
os.makedirs(OUT, exist_ok=True)

W, H = 64, 80
SKIN = ["#d7b491", "#c9a37e", "#b98c66", "#e0c3a2", "#a97b58"]
HAIR = ["#1b1a19", "#2a231d", "#3b2e23", "#4a3a2b", "#5a4a3a"]
UNI = ["#2f3a3a", "#333d44", "#3a3540", "#2d3a33"]
BG_LIVE = "#2a3430"
BG_ID = "#c8b48c"

def pixel(d, x, y, c):
    d.point((x, y), fill=c)

def face(d, cx, top, bottom, width, skin):
    # jaw-tapered head
    h = bottom - top
    for i in range(h):
        t = i / float(h - 1)
        if t < 0.55:
            w = width
        else:
            w = width * (1.0 - 0.55 * ((t - 0.55) / 0.45) ** 1.3)
        x0 = int(cx - w / 2)
        x1 = int(cx + w / 2)
        d.line([(x0, top + i), (x1, top + i)], fill=skin)

def portrait(idx, seed):
    rng = random.Random(seed)
    skin = rng.choice(SKIN)
    hair = rng.choice(HAIR)
    uni = rng.choice(UNI)
    style = rng.randrange(5)
    glasses = rng.random() < 0.22
    mole = rng.random() < 0.28
    tie = rng.random() < 0.85
    eye_gap = rng.choice([7, 8, 9])
    face_w = rng.choice([26, 28, 30])
    skin_dark = "#b08a68"

    for photo in (False, True):
        bg = BG_ID if photo else BG_LIVE
        img = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(img)

        # torso
        d.polygon([(6, 80), (10, 64), (22, 59), (42, 59), (54, 64), (58, 80)], fill=uni)
        d.polygon([(24, 59), (40, 59), (32, 70)], fill="#d9d4c2")
        if tie:
            d.rectangle([31, 61, 33, 74], fill="#7c2c22")
        # neck
        d.rectangle([29, 52, 35, 61], fill=skin_dark)
        # head
        face(d, 32, 12, 56, face_w, skin)
        # ears
        d.rectangle([32 - face_w // 2 - 2, 32, 32 - face_w // 2 - 1, 36], fill=skin_dark)
        d.rectangle([32 + face_w // 2 + 1, 32, 32 + face_w // 2 + 2, 36], fill=skin_dark)

        # hair
        if style == 0:
            d.rectangle([32 - face_w // 2 - 1, 10, 32 + face_w // 2 + 1, 22], fill=hair)
            d.polygon([(32 - face_w // 2 - 1, 22), (32 - face_w // 2 + 3, 18), (32, 20), (32 + face_w // 2 - 2, 18), (32 + face_w // 2 + 1, 22)], fill=hair)
        elif style == 1:
            d.rectangle([32 - face_w // 2 - 1, 9, 32 + face_w // 2 + 1, 24], fill=hair)
            d.polygon([(30, 22), (32 + face_w // 2 + 1, 14), (32 + face_w // 2 + 1, 24)], fill=hair)
        elif style == 2:
            d.rectangle([32 - face_w // 2 - 2, 10, 32 + face_w // 2 + 2, 26], fill=hair)
            d.rectangle([32 - face_w // 2 - 2, 26, 32 + face_w // 2 + 2, 27], fill=hair)
        elif style == 3:
            d.rectangle([32 - face_w // 2 - 1, 10, 32 + face_w // 2 + 1, 21], fill=hair)
            d.ellipse([32 + face_w // 2 - 1, 12, 32 + face_w // 2 + 7, 26], fill=hair)
        else:
            d.rectangle([32 - face_w // 2 - 1, 10, 32 + face_w // 2 + 1, 22], fill=hair)
            d.rectangle([32 - face_w // 2 - 2, 22, 32 - face_w // 2 + 2, 60], fill=hair)
            d.rectangle([32 + face_w // 2 - 2, 22, 32 + face_w // 2 + 2, 60], fill=hair)

        # brows / eyes
        eye_y = 31
        d.line([(32 - eye_gap - 3, 27), (32 - eye_gap + 1, 27)], fill=hair)
        d.line([(32 + eye_gap - 1, 27), (32 + eye_gap + 3, 27)], fill=hair)
        for ex in (32 - eye_gap, 32 + eye_gap):
            d.rectangle([ex - 1, eye_y, ex, eye_y + 1], fill="#171512")
        # nose
        d.line([(32, 34), (32, 39)], fill=skin_dark)
        d.point((31, 40), fill=skin_dark)
        # mouth
        d.line([(29, 45), (35, 45)], fill="#8a5245")
        if mole:
            d.point((32 + face_w // 3, 38), fill="#6b4a3c")
        if glasses:
            d.rectangle([32 - eye_gap - 4, eye_y - 3, 32 - eye_gap + 3, eye_y + 3], outline="#20242a", width=1)
            d.rectangle([32 + eye_gap - 3, eye_y - 3, 32 + eye_gap + 4, eye_y + 3], outline="#20242a", width=1)
            d.line([(32 - eye_gap + 4, eye_y), (32 + eye_gap - 4, eye_y)], fill="#20242a")

        if photo:
            # sepia grade + grain + border
            px = img.load()
            for y in range(H):
                for x in range(W):
                    r, g, b = px[x, y]
                    lum = int(0.299 * r + 0.587 * g + 0.114 * b)
                    nr = min(255, int(lum * 1.06 + 18))
                    ng = min(255, int(lum * 0.94 + 8))
                    nb = min(255, int(lum * 0.72))
                    if rng.random() < 0.10:
                        nr, ng, nb = max(0, nr - 16), max(0, ng - 16), max(0, nb - 14)
                    px[x, y] = (nr, ng, nb)
            d.rectangle([0, 0, W - 1, H - 1], outline="#8a7752", width=1)

        big = img.resize((W * 3, H * 3), Image.NEAREST)
        suffix = "_id" if photo else ""
        big.save(os.path.join(OUT, "p%d%s.png" % (idx, suffix)))

for i in range(24):
    portrait(i, 1000 + i * 37)
print("portraits generated", 24)
