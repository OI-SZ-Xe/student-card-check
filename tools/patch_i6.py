# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func debug_black(" not in d:
    d += '''

func debug_black() -> void:
	State.day = 20
	State.money = 400
	debug_terminal("black")
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if 'black20' not in m:
    m = m.replace('''			elif _shot_mode == "black":''', '''			elif _shot_mode == "black20":
				_desk.debug_black()
			elif _shot_mode == "black":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("black20 debug")
