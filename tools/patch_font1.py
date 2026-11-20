# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\tools\gen_font.py"
s = io.open(p, encoding="utf-8").read()
if 'bake(24, "pixel24")' not in s:
    s = s.replace('bake(16, "pixel16")\nbake(32, "pixel32")', 'bake(16, "pixel16")\nbake(24, "pixel24")\nbake(32, "pixel32")')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
