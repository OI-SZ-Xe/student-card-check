# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	term.org_requested.connect(_on_org_requested)''', '''	if not term.org_requested.is_connected(_on_org_requested):
		term.org_requested.connect(_on_org_requested)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

sp = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s = io.open(sp, encoding="utf-8").read()
s = s.replace('''			_hint.text = "夜间巡逻''', '''			if _hint != null:
				_hint.text = "夜间巡逻''')
s = s.replace('''			_hint.text = "有人闯进检查站''', '''			if _hint != null:
				_hint.text = "有人闯进检查站''')
s = s.replace('''			_hint.text = "校门总攻''', '''			if _hint != null:
				_hint.text = "校门总攻''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("fixes")
