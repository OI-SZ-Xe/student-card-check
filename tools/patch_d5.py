# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func debug_bribe(" not in d:
    d += '''

func debug_bribe() -> void:
	_paused = false
	_open_bribe()
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if '"exchange"' not in m:
    m = m.replace('''			elif _shot_mode == "org":''', '''			elif _shot_mode == "exchange":
				_desk.debug_terminal("exchange")
			elif _shot_mode == "bribe":
				_desk.debug_bribe()
			elif _shot_mode == "org":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("debug modes")
