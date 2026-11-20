# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
if "KEY_F2" not in s:
    s = s.replace('''	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:''', '''	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F2:
		if not _visitor.is_empty():
			_open_face()
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:''')
    s += '''

func _open_face() -> void:
	var fc := FaceCompare.new()
	fc.visitor = _visitor
	add_child(fc)
	fc.closed.connect(func() -> void: fc.queue_free())
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("face compare")
