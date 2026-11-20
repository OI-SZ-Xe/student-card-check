# -*- coding: utf-8 -*-
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"F:\请出示学生证\art\signatures"
os.makedirs(OUT, exist_ok=True)

FONTS = {
    "xingkai": r"C:\Windows\Fonts\STXINGKA.TTF",
    "kaiti": r"C:\Windows\Fonts\STKAITI.TTF",
    "simkai": r"C:\Windows\Fonts\simkai.ttf",
}

SPECS = [
    dict(id="wang_ming", text="王明", font="xingkai", size=188, ink="#1b2a4a",
         slant=-5, gap=-14, rot=(-3, 3), dy=(-6, 6), flourish=True, weight=1),
    dict(id="li_hua", text="李华", font="xingkai", size=196, ink="#20262e",
         slant=9, gap=-26, rot=(-2, 5), dy=(-4, 8), flourish=False, weight=1),
    dict(id="zhang_li", text="张丽", font="kaiti", size=150, ink="#232a34",
         slant=1, gap=2, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
    dict(id="chen_fang", text="陈芳", font="simkai", size=140, ink="#2a2f38",
         slant=2, gap=4, rot=(-1, 1), dy=(-2, 2), flourish=False, weight=1, initials="C.F."),
    dict(id="zhao_qiang", text="赵强", font="xingkai", size=190, ink="#11161f",
         slant=-3, gap=-8, rot=(-2, 2), dy=(-4, 4), flourish=True, weight=3),
]

W, H = 900, 300

def draw_char(ch, font, ink, rot, weight):
    bbox = font.getbbox(ch)
    pad = 60
    w = bbox[2] - bbox[0] + pad * 2
    h = bbox[3] - bbox[1] + pad * 2
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = pad - bbox[0], pad - bbox[1]
    for k in range(max(1, weight)):
        d.text((ox + k, oy + k), ch, font=font, fill=ink)
    layer = layer.rotate(rot, resample=Image.BICUBIC, expand=False)
    bbox2 = layer.getbbox()
    if bbox2:
        layer = layer.crop(bbox2)
    return layer

def ink_wash(img, ink_hex, emboss=True):
    alpha = img.split()[3].filter(ImageFilter.GaussianBlur(0.7))
    bleed = alpha.filter(ImageFilter.GaussianBlur(1.6)).point(lambda v: int(v * 0.30))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))

    if emboss:
        hi = alpha.filter(ImageFilter.MaxFilter(3)).point(lambda v: int(v * 0.18))
        hi_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
        hi_img.putalpha(hi)
        out.alpha_composite(hi_img, (0, 0))

    bleed_img = Image.new("RGBA", img.size, ink_hex + "ff")
    bleed_img.putalpha(bleed)
    out.alpha_composite(bleed_img)

    ink_img = Image.new("RGBA", img.size, ink_hex + "ff")
    ink_img.putalpha(alpha)
    out.alpha_composite(ink_img)

    if emboss:
        sh = alpha.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: int(v * 0.10))
        sh_img = Image.new("RGBA", img.size, (0, 0, 0, 255))
        sh_img.putalpha(sh)
        out.alpha_composite(sh_img, (1, 2))

    return out

random.seed(11)

def compose(spec):
    font = ImageFont.truetype(FONTS[spec["font"]], spec["size"])
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 70
    baseline_y = 90
    for ch in spec["text"]:
        rot = random.uniform(*spec["rot"])
        dy = random.uniform(*spec["dy"])
        layer = draw_char(ch, font, spec["ink"], rot, spec["weight"])
        canvas.alpha_composite(layer, (x, int(baseline_y + dy)))
        x += layer.width + spec["gap"]
    if spec.get("initials"):
        small = ImageFont.truetype(FONTS["simkai"], 34)
        d = ImageDraw.Draw(canvas)
        d.text((x + 10, baseline_y + 130), spec["initials"], font=small, fill=spec["ink"] + "cc")
    if spec["flourish"]:
        d = ImageDraw.Draw(canvas)
        y0 = baseline_y + 210
        pts = []
        for k in range(41):
            t = k / 40.0
            pts.append((60 + t * (x - 40), y0 - 14 * t + 3.5 * math.sin(t * math.pi * 2.0)))
        for w in range(5, 0, -1):
            d.line(pts, fill=spec["ink"] + "ff", width=w, joint="curve")
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop((max(0, bbox[0] - 20), max(0, bbox[1] - 20), min(W, bbox[2] + 20), min(H, bbox[3] + 20)))
    sh = math.tan(math.radians(spec["slant"]))
    canvas = canvas.transform((canvas.width, canvas.height), Image.AFFINE,
                              (1, sh, -sh * canvas.height / 2, 0, 1, 0), resample=Image.BICUBIC)
    return canvas

PUNCH = {
    "wang_ming": (0.54, 0.26, 0.74, 0.56),
    "li_hua": (0.52, 0.30, 0.74, 0.60),
    "zhang_li": (0.54, 0.30, 0.76, 0.62),
    "chen_fang": (0.50, 0.30, 0.72, 0.60),
    "zhao_qiang": (0.54, 0.24, 0.76, 0.56),
}

def punch(img, key):
    out = img.copy()
    w, h = out.size
    b = PUNCH.get(key, (0.45, 0.2, 0.62, 0.5))
    box = (int(w * b[0]), int(h * b[1]), int(w * b[2]), int(h * b[3]))
    mask = Image.new("L", out.size, 255)
    d = ImageDraw.Draw(mask)
    d.rectangle(box, fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    out.putalpha(Image.composite(out.split()[3], Image.new("L", out.size, 0), mask))
    return out

def lighten(img):
    out = img.copy()
    alpha = out.split()[3].point(lambda v: int(v * 0.42))
    out.putalpha(alpha)
    gray = Image.new("RGBA", out.size, "#5b6270ff")
    gray.putalpha(alpha)
    return gray

DEANS = [
    dict(id="dean_sy", text="周慧", font="kaiti", size=142, ink="#243044",
         slant=-2, gap=2, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
    dict(id="dean_sz", text="吴敏", font="simkai", size=146, ink="#2b3038",
         slant=4, gap=0, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
    dict(id="dean_sg", text="何静", font="kaiti", size=138, ink="#1f2a33",
         slant=-3, gap=3, rot=(-1, 1), dy=(-2, 2), flourish=False, weight=1),
    dict(id="dean_wgy", text="许强", font="xingkai", size=176, ink="#151c26",
         slant=-4, gap=-6, rot=(-2, 2), dy=(-4, 4), flourish=True, weight=2),
    dict(id="dean_jyj", text="谢岚", font="kaiti", size=140, ink="#2a2f36",
         slant=2, gap=1, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
]

SPECS = SPECS + DEANS

for spec in SPECS:
    base = ink_wash(compose(spec), spec["ink"], True)
    base.save(os.path.join(OUT, spec["id"] + ".png"))

    plain = ink_wash(compose(spec), spec["ink"], False)
    plain.save(os.path.join(OUT, spec["id"] + "_plain.png"))

    punch(base, spec["id"]).save(os.path.join(OUT, spec["id"] + "_miss.png"))
    lighten(base).save(os.path.join(OUT, spec["id"] + "_light.png"))
    base.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(OUT, spec["id"] + "_mirror.png"))
    print("variants", spec["id"], base.size)
