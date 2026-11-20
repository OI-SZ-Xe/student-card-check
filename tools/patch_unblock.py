# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	if _hl.get_global_rect().has_point(event.position):
		_advance()
		return
	# 高亮区之外一律吞掉，引导期间不许乱点
	get_viewport().set_input_as_handled()''', '''	if _hl.get_global_rect().has_point(event.position):
		_advance()''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guide no longer blocks input")
