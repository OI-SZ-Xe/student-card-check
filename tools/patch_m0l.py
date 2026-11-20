# -*- coding: utf-8 -*-
import io
d = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(d, encoding="utf-8").read()
s += '''

func debug_save_load() -> void:
	_save_game()
	_load_game()
'''
io.open(d, "w", encoding="utf-8", newline="\n").write(s)

m = r"F:\请出示学生证\scripts\Main.gd"
t = io.open(m, encoding="utf-8").read()
t = t.replace('''			elif _shot_mode == "settle":
				_desk.debug_end_day()''', '''			elif _shot_mode == "settle":
				_desk.debug_end_day()
			elif _shot_mode == "saveload":
				_desk.debug_save_load()''')
io.open(m, "w", encoding="utf-8", newline="\n").write(t)
print("debug save/load added")
