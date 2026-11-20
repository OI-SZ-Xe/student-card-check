# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\tz_index = _modal_z\n", "\tz_index = 150\n")
s = s.replace('''	var dim := ColorRect.new()
	dim.color = Color(0.02, 0.03, 0.02, 0.92)''', '''	var dim := ColorRect.new()
	dim.z_index = -1
	dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	dim.color = Color(0.02, 0.03, 0.02, 0.92)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("dim behind content")
