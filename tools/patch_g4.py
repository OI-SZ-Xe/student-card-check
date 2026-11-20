# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	var tint := ColorRect.new()
	tint.color = Color(0.16, 0.26, 0.22, 0.42)
	tint.position = Vector2.ZERO
	tint.size = Vector2(792, 372)
	tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(tint)'''
new = '''	var tint := ColorRect.new()
	tint.color = Color(0.12, 0.20, 0.17, 0.35)
	tint.position = Vector2.ZERO
	tint.size = Vector2(792, 372)
	tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(tint)
	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.04, 0.03, 0.55)
	shade.position = Vector2(266, 0)
	shade.size = Vector2(526, 372)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(shade)'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("window shade")
