# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	reader.position = Vector2(590, 206)
	reader.size = Vector2(96, 64)''', '''	reader.position = Vector2(432, 206)
	reader.size = Vector2(96, 64)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("reader moved")
