# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	term.start_site = site
	add_child(term)''', '''	term.start_site = site
	add_child(term)
	term.z_index = 200
	term.visible = true
	term.size = Vector2(1920, 1080)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("terminal z200")
