# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\project.godot"
s = io.open(p, encoding="utf-8").read()
s = s.replace('window/stretch/aspect="expand"', 'window/stretch/aspect="keep"')
s = s.replace('window/stretch/scale_mode="integer"\n', '')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("stretch fixed")
