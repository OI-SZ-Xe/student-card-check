# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "StartMenu" not in m:
    m = m.replace('''func _start_desk(skip_briefing: bool) -> void:''', '''func _show_menu() -> void:
	var menu := StartMenu.new()
	add_child(menu)
	menu.choice.connect(func(kind: String) -> void:
		match kind:
			"quit":
				get_tree().quit()
			"settings":
				pass
			"new":
				menu.queue_free()
			"continue":
				if SaveManager.load_slot(1):
					menu.queue_free()
					_clear_screens()
					State.endless = false
					_start_desk(true)
			"endless":
				menu.queue_free()
				_clear_screens()
				State.endless = true
				State.day = 30
				State.money = 300
				State.player_name = "科员"
				_start_desk(true)
	)

func _clear_screens() -> void:
	for c in get_children():
		if c is StartMenu or c is CrtOverlay:
			continue
		if c is Control:
			c.queue_free()

func _start_desk(skip_briefing: bool) -> void:''')
    # show menu on boot (after shot-mode block ends)
    m = m.replace('''	_start_desk(false)''', '''	_show_menu()''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var endless" not in s:
    s = s.replace("var forgery_bonus := 0.0", "var forgery_bonus := 0.0\nvar endless := false")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("menu wired")
