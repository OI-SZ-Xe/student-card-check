# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
old = '''func _input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	if _hl == null:
		return
	if _hl.get_global_rect().has_point(event.position):
		_advance()'''
new = '''func _input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	if _hl == null:
		return
	if _hl.get_global_rect().has_point(event.position):
		_advance()
		return
	# 高亮区之外一律吞掉，引导期间不许乱点
	get_viewport().set_input_as_handled()'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("input interception")
