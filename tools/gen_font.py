# -*- coding: utf-8 -*-
import io, os, glob
from PIL import Image, ImageDraw, ImageFont

SRC = [r"F:\请出示学生证\scripts", r"F:\请出示学生证\data"]
OUT = r"F:\请出示学生证\art\fonts"
os.makedirs(OUT, exist_ok=True)
FONT_PATH = r"C:\Windows\Fonts\simsun.ttc"

chars = set(chr(i) for i in range(32, 127))
chars.update("　、。，．·；：？！“”‘’（）【】《》〈〉—…／￥％＃＆＊＋－＝｜～")
for root in SRC:
    for path in glob.glob(os.path.join(root, "**", "*.*"), recursive=True):
        if not path.endswith((".gd", ".json")):
            continue
        try:
            text = io.open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for ch in text:
            if ord(ch) > 127 or ch.isprintable():
                chars.add(ch)
chars = sorted(chars, key=lambda c: ord(c))
print("chars:", len(chars))

def bake(size: int, name: str) -> None:
    font = ImageFont.truetype(FONT_PATH, size, index=0)
    ascent, descent = font.getmetrics()
    line_h = ascent + descent + 2
    base = ascent + 1
    pad = 2
    rendered = []
    for ch in chars:
        tmp = Image.new("L", (size * 3, size * 4), 0)
        td = ImageDraw.Draw(tmp)
        td.text((pad, pad + base), ch, font=font, fill=255, anchor="ls")
        bbox = tmp.getbbox()
        adv = int(round(font.getlength(ch)))
        if bbox is None:
            rendered.append((ch, None, 0, 0, 0, 0, adv))
            continue
        glyph = tmp.crop(bbox).point(lambda v: 255 if v > 128 else 0)
        xoff = bbox[0] - pad
        yoff = bbox[1] - pad
        rendered.append((ch, glyph, glyph.size[0], glyph.size[1], xoff, yoff, adv))

    def pot(n):
        v = 1
        while v < n:
            v *= 2
        return v

    W0 = 512 if size <= 16 else (1024 if size <= 24 else 2048)
    x = pad
    y = pad
    row_h = 0
    for (_ch, glyph, gw, gh, _xo, _yo, _adv) in rendered:
        if glyph is None:
            continue
        if x + gw + pad > W0:
            x = pad
            y += row_h + pad
            row_h = 0
        row_h = max(row_h, gh)
        x += gw + pad
    H0 = pot(y + row_h + pad)
    W = W0
    H = max(H0, 128)
    atlas = Image.new("L", (W, H), 0)

    metrics = []
    x = pad
    y = pad
    row_h = 0
    for (ch, glyph, gw, gh, xoff, yoff, adv) in rendered:
        if glyph is None:
            metrics.append((ch, 0, 0, 0, 0, 0, 0, adv))
            continue
        if x + gw + pad > W:
            x = pad
            y += row_h + pad
            row_h = 0
        atlas.paste(glyph, (x, y))
        metrics.append((ch, x, y, gw, gh, xoff, yoff, adv))
        x += gw + pad
        row_h = max(row_h, gh)

    rgba = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    rgba.putalpha(atlas)
    rgba.save(os.path.join(OUT, "%s_0.png" % name))

    lines = []
    lines.append('info face="%s" size=%d bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=0,0 outline=0' % (name, size))
    lines.append('common lineHeight=%d base=%d scaleW=%d scaleH=%d pages=1 packed=0' % (line_h, base, W, H))
    lines.append('page id=0 file="%s_0.png"' % name)
    lines.append('chars count=%d' % len(metrics))
    for (ch, gx, gy, gw, gh, xo, yo, adv) in metrics:
        lines.append('char id=%d x=%d y=%d width=%d height=%d xoffset=%d yoffset=%d xadvance=%d page=0 chnl=15' % (ord(ch), gx, gy, gw, gh, xo, yo, adv))
    io.open(os.path.join(OUT, "%s.fnt" % name), "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("baked", name, W, H, len(metrics))

SIZES = [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48]
for sz in SIZES:
    bake(sz, "pixel%d" % sz)
