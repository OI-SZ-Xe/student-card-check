# -*- coding: utf-8 -*-
import io
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if 'shot-mode == "interrogate"' not in m:
    m = m.replace('''			elif _shot_mode == "tutorial":''', '''			elif _shot_mode == "interrogate":
				_desk._open_interrogation()
			elif _shot_mode == "tutorial":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("interrogate shot")
