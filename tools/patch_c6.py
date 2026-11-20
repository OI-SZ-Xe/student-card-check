# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Shop.gd"
s = io.open(p, encoding="utf-8").read()
old = '''	for u in Data.upgrades:
		if int(u.get("day", 1)) > State.day:
			continue
		_grid.add_child(_make_card(u))'''
new = '''	var shown := 0
	for u in Data.upgrades:
		if int(u.get("day", 1)) > State.day:
			continue
		_grid.add_child(_make_card(u))
		shown += 1
	if shown == 0:
		var empty := Ui.label("暂无在售商品。第一批外借工具将在第 3 天到货。", 16, Color(0.8, 0.84, 0.76), Ui.font_serif())
		empty.position = Vector2(10, 20)
		empty.size = Vector2(900, 30)
		_grid.add_child(empty)'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("shop empty state")
