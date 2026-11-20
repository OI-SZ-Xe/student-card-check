# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Ui.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("fb.hinting = TextServer.HINTING_FULL", "fb.hinting = TextServer.HINTING_NORMAL")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("hinting fixed")
