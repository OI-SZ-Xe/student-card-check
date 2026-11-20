# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Register.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\tpaper.position = Vector2(600, 240)\n\tpaper.size = Vector2(760, 600)", "\tpaper.position = Vector2(600, 250)\n\tpaper.size = Vector2(760, 540)")
s = s.replace("\tbtn.position = Vector2(300, 440)", "\tbtn.position = Vector2(250, 384)")
s = s.replace("\tfoot.position = Vector2(48, 540)", "\tfoot.position = Vector2(48, 474)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("register layout fixed")
