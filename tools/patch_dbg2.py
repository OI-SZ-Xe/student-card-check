# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "DBG day done" not in d:
    d = d.replace('''	State.start_day()
	_refresh_hud()''', '''	State.start_day()
	print("DBG day done")
	_refresh_hud()
	print("DBG hud done")''')
    d = d.replace('''	if skip_briefing:
		_begin_shift()''', '''	print("DBG pre shift")
	if skip_briefing:
		_begin_shift()''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("more dbg")
