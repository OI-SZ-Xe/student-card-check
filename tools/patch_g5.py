# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	if not State.has_upgrade("archive"):
		return "档案索引卡：未购置"''', '''	if not State.has_upgrade("archive"):
		return ""''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("archive hint hidden")
