# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# reset flags per visitor
d = d.replace('''	_awaiting_next = false''', '''	_awaiting_next = false
	_called_this = false
	_db_checked_this = false''')

# z order + interrogation button
d = d.replace('''	add_child(panel)
	var t := Ui.label("印 章 台"''', '''	panel.z_index = 20
	add_child(panel)
	var t := Ui.label("印 章 台"''')
d = d.replace('''	add_child(tools)
	var tray := TextureRect.new()''', '''	tools.z_index = 10
	add_child(tools)
	var tray := TextureRect.new()''')

d = d.replace('''	var tut_btn := Ui.button("教学", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))''', '''	var ask_btn := Ui.button("询问", 14, Color(0.26, 0.20, 0.14), Color("#f0e0c8"))
	ask_btn.position = Vector2(590, 180)
	ask_btn.size = Vector2(88, 34)
	ask_btn.pressed.connect(_open_interrogation)
	panel.add_child(ask_btn)
	var tut_btn := Ui.button("教学", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))''')

if "func _open_interrogation(" not in d:
    d += '''

func _open_interrogation() -> void:
	if _visitor.is_empty() or _awaiting_next:
		return
	_paused = true
	var dlg := Interrogation.new()
	dlg.visitor = _visitor
	dlg.today = State.date
	add_child(dlg)
	dlg.spend.connect(func(sec: float) -> void:
		State.time_left = maxf(0.0, State.time_left - sec)
	)
	dlg.action.connect(func(kind: String) -> void:
		_called_this = dlg.called
		_db_checked_this = dlg.db_checked
		dlg.queue_free()
		_paused = false
		match kind:
			"approve":
				_judge("approve")
			"reject":
				_judge("reject")
			"arrest":
				_arrest()
			_:
				pass
	)
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("interrogation wired")
