# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func debug_org(" not in d:
    d += '''

func debug_org() -> void:
	State.pending_org = {
		"subject": "印刷费",
		"body": "检察员同学：\\n\\n我们要印一批刊物，缺五十元。\\n你可以不出面，钱放在窗台上就行。\\n\\n——学生斗争委员会",
		"cost": 50, "help": 1, "risk": 4
	}
	_paused = false
	_open_org()
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if '"org"' not in m:
    m = m.replace('''			elif _shot_mode == "terminal":''', '''			elif _shot_mode == "org":
				_desk.debug_org()
			elif _shot_mode == "terminal":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("org debug")
