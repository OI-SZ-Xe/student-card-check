# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\Main.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''			"new":
				menu.queue_free()''', '''			"new":
				menu.queue_free()
				Meta.tutorial_done = false''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("tutorial per run")
