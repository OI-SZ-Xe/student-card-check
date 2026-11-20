# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Briefing.gd"
s = io.open(p, encoding="utf-8").read()
if "_armed" not in s:
    s = s.replace("signal closed", "signal closed\n\nvar _armed := false")
    s = s.replace("func _ready() -> void:", "func _ready() -> void:\n\tawait get_tree().create_timer(0.4).timeout\n\t_armed = true")
    s += '''

func _input(event: InputEvent) -> void:
	if not _armed:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_armed = false
		closed.emit()
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("briefing click-anywhere close")
