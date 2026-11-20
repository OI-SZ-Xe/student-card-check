# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if 'terminal_achv' not in m:
    m = m.replace('''			elif _shot_mode == "exchange":''', '''			elif _shot_mode == "terminal_achv":
				_desk.debug_terminal("achv")
			elif _shot_mode == "terminal_mail":
				_desk.debug_terminal("mail")
			elif _shot_mode == "exchange":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("achv shot mode")
