# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	_build()
	_show(start_site)''', '''	_build()
	print("TERM ready z=", z_index, " size=", size, " children=", get_child_count())
	_show(start_site)''')
s = s.replace('''	add_child(term)
''', '''	add_child(term)
	print("TERM panel pos=", term.position, " size=", term.size, " vis=", term.visible)
''', 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("debug prints")
