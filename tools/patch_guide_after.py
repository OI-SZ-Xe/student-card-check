# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	if not Meta.tutorial_done:
		_open_guided()
	Music.play("bgm_day", 2.0)''', '''	Music.play("bgm_day", 2.0)''')
s = s.replace('''	_paused = false
	_begin_shift()''', '''	_paused = false
	_begin_shift()
	if not Meta.tutorial_done:
		_open_guided()''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guide after briefing")
