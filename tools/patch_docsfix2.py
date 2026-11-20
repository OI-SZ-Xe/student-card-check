# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
if "_build_docs()" not in s.split("func _spawn_visitor")[1].split("func ")[0]:
    s = s.replace('''	card.set_visitor(v, State.date)''', '''	card.set_visitor(v, State.date)
	_build_docs()''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("docs on spawn")
