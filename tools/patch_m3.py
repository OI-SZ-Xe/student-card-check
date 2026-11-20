# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if 'shot-mode == "settings"' not in m:
    m = m.replace('''			elif _shot_mode == "ending":''', '''			elif _shot_mode == "settings":
				_desk._open_settings()
			elif _shot_mode == "ending":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("settings shot mode")
