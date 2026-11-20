# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	_paused = true
	State.time_left = maxf(0.0, State.time_left - 2.0)
	var term := EduTerminal.new()''', '''	_spawn_terminal(site)

func _spawn_terminal(site: String) -> void:
	_paused = true
	State.time_left = maxf(0.0, State.time_left - 2.0)
	var term := EduTerminal.new()''')
s = s.replace('''	_paused = false
	State.time_left = maxf(0.0, State.time_left - 3.0)
	_open_terminal(site)''', '''	_paused = false
	State.time_left = maxf(0.0, State.time_left - 3.0)
	_spawn_terminal(site)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("browser loop fixed")
