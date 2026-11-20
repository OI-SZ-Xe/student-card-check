# -*- coding: utf-8 -*-
import io
# 1) extra small sizes
p = r"F:\请出示学生证\tools\gen_font.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("SIZES = [13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]",
              "SIZES = [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# 2) Ui: register new sizes + smart wrap for rich
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
u = u.replace("for sz in [13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]:",
              "for sz in [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]:")
u = u.replace("\tr.fit_content = true\n\tr.scroll_active = false", "\tr.fit_content = true\n\tr.scroll_active = false\n\tr.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART")
io.open(up, "w", encoding="utf-8", newline="\n").write(u)
print("small sizes + wrap")
