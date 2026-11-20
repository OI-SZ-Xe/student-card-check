# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\Main.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''		var reg := preload("res://scripts/ui/Register.gd").new()
		add_child(reg)
		reg.submitted.connect(_on_registered)
		return''', '''		_show_menu()
		return''')
s = s.replace('''	_intro = null
	_show_menu()''', '''	_intro = null
	_start_desk(false)''')
s = s.replace('''			"new":
				menu.queue_free()''', '''			"new":
				menu.queue_free()
				var reg := preload("res://scripts/ui/Register.gd").new()
				add_child(reg)
				reg.submitted.connect(_on_registered)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("routing fixed: boot menu, intro->desk, new->register")
