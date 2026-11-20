# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
m = m.replace('''	if is_instance_valid(_intro):
		_intro.queue_free()
		_intro = null''', '''	if is_instance_valid(_intro):
		var old := _intro
		_intro = null
		old.visible = false
		old.process_mode = Node.PROCESS_MODE_DISABLED
		get_tree().create_timer(1.0).timeout.connect(func() -> void:
			if is_instance_valid(old):
				old.queue_free()
		)''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

gp = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
g = io.open(gp, encoding="utf-8").read()
if "InputEventScreenTouch" not in g:
    g = g.replace('''func _input(event: InputEvent) -> void:''', '''func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch and event.pressed:
		if _hl != null and _hl.get_global_rect().has_point(event.position):
			_advance()
		return''')
io.open(gp, "w", encoding="utf-8", newline="\n").write(g)
print("crash guard + touch guide")
