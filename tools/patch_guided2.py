# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
if "func _input(" not in s:
    s += '''

func _input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	if _hl == null:
		return
	if _hl.get_global_rect().has_point(event.position):
		_advance()

func _advance_step() -> void:
	_advance()
'''
    s = s.replace('''	next.pressed.connect(_advance)''', '''	next.pressed.connect(_advance_step)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("advance on target click")
