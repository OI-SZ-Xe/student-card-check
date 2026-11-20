# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''				if key != "" and not State.has_upgrade(key):
					State.unlock(key)''', '''				if key != "" and not State.has_upgrade(key):
					State.upgrades.append(key)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("upgrade cheat fixed")
