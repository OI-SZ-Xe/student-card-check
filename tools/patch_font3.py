# -*- coding: utf-8 -*-
import io
# fix font metrics: draw by baseline
p = r"F:\请出示学生证\tools\gen_font.py"
s = io.open(p, encoding="utf-8").read()
old = '''        tmp = Image.new("L", (size * 2, size * 2), 0)
        td = ImageDraw.Draw(tmp)
        td.text((pad, pad), ch, font=font, fill=255)
        bbox = tmp.getbbox()
        if bbox is None:
            adv = int(round(font.getlength(ch)))
            metrics.append((ch, 0, 0, 0, 0, 0, 0, adv))
            continue
        glyph = tmp.crop(bbox).point(lambda v: 255 if v > 128 else 0)
        gw, gh = glyph.size
        atlas.paste(glyph, (cx, cy))
        xoff = bbox[0] - pad
        yoff = bbox[1] - pad'''
new = '''        tmp = Image.new("L", (size * 2, size * 3), 0)
        td = ImageDraw.Draw(tmp)
        td.text((pad, pad + ascent), ch, font=font, fill=255, anchor="ls")
        bbox = tmp.getbbox()
        if bbox is None:
            adv = int(round(font.getlength(ch)))
            metrics.append((ch, 0, 0, 0, 0, 0, 0, adv))
            continue
        glyph = tmp.crop(bbox).point(lambda v: 255 if v > 128 else 0)
        gw, gh = glyph.size
        atlas.paste(glyph, (cx, cy))
        xoff = bbox[0] - pad
        yoff = bbox[1] - pad'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# phone position
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace("phone_prop.position = Vector2(252, 2)", "phone_prop.position = Vector2(152, 2)")
d = d.replace("phone_prop.size = Vector2(48, 48)", "phone_prop.size = Vector2(40, 40)")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("font metrics + phone fixed")
