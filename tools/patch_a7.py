# -*- coding: utf-8 -*-
import io
tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
t = t.replace('var visitor: Dictionary = {}', 'var visitor: Dictionary = {}\nvar start_site := "schools"')
t = t.replace('\t_build()\n\t_show("schools")', '\t_build()\n\t_show(start_site)')
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''func debug_terminal(site: String) -> void:
	_paused = true
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
if old in d:
    d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("terminal debug direct")
