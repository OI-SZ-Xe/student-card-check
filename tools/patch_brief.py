# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	var b := Briefing.new()
	b.day = State.day''', '''	var b := Briefing.new()
	b.z_index = 120
	b.day = State.day''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("briefing z")
