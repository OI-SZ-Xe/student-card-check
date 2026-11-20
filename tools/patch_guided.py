# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	if not Meta.tutorial_done:
		_open_tutorial()''', '''	if not Meta.tutorial_done:
		_open_guided()''')
s = s.replace('''func _open_tutorial() -> void:
	_paused = true
	var tut := Tutorial.new()''', '''func _open_guided() -> void:
	var g := GuidedTutorial.new()
	add_child(g)
	g.finished.connect(func() -> void:
		Meta.tutorial_done = true
		Meta.save_meta()
		g.queue_free()
	)

func _open_tutorial() -> void:
	_paused = true
	var tut := Tutorial.new()''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guided tutorial wired")
