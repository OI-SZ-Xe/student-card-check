# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''func debug_terminal(site: String) -> void:
	_paused = false
	_open_terminal(site)'''
new = '''func debug_terminal(site: String) -> void:
	_paused = false
	State.time_left = 600.0
	var term := EduTerminal.new()
	term.visitor = _visitor
	term.start_site = site
	add_child(term)
	term.time_cost.connect(_on_terminal_cost)
	term.closed.connect(_close_modal.bind(term))'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("debug terminal direct v2")
