# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\ui\Shop.gd"
s = io.open(sp, encoding="utf-8").read()
s = s.replace('''		if int(u.get("day", 1)) > State.day:
			continue
''', '')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	_dbg("open_terminal site=%s paused=%s visitor_empty=%s" % [site, _paused, _visitor.is_empty()])\n''', '')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("shop day1 + debug off")
