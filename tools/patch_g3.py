# -*- coding: utf-8 -*-
import io
# corridor at native panel size
cp = r"F:\请出示学生证\tools\gen_corridor.py"
c = io.open(cp, encoding="utf-8").read()
c = c.replace("W, H = 780, 360", "W, H = 792, 372")
c = c.replace("for x in range(0, W, 130):", "for x in range(0, W, 132):")
c = c.replace("img = img.resize((W * 2, H * 2), Image.NEAREST)", "img.save(os.path.join(OUT, 'corridor.png'))")
c = c.replace("img.save(os.path.join(OUT, \"corridor.png\"))\nprint", "print")
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

# softer scanlines
ip = r"F:\请出示学生证\scripts\ui\CrtOverlay.gd"
i = io.open(ip, encoding="utf-8").read()
i = i.replace("float scan = 0.972 + 0.028 * sin(uv.y * 820.0);", "float scan = 0.985 + 0.015 * sin(uv.y * 420.0);")
io.open(ip, "w", encoding="utf-8", newline="\n").write(i)
print("corridor native + softer scanlines")
