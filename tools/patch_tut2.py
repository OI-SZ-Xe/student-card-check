# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if 'shot-mode == "tutorial"' not in m:
    m = m.replace('''			elif _shot_mode == "settings":''', '''			elif _shot_mode == "tutorial":
				_desk._open_tutorial()
			elif _shot_mode == "settings":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("tutorial shot")
