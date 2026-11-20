# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	var glass := ColorRect.new()
	glass.color = Color(0.20, 0.26, 0.23, 0.9)
	glass.position = Vector2(14, 14)
	glass.size = Vector2(792, 372)
	glass.mouse_filter = Control.MOUSE_FILTER_IGNORE
	win.add_child(glass)'''
new = '''	var glass := TextureRect.new()
	glass.texture = load("res://art/props/corridor.png")
	glass.stretch_mode = TextureRect.STRETCH_SCALE
	glass.position = Vector2(14, 14)
	glass.size = Vector2(792, 372)
	glass.mouse_filter = Control.MOUSE_FILTER_IGNORE
	win.add_child(glass)
	var tint := ColorRect.new()
	tint.color = Color(0.16, 0.26, 0.22, 0.42)
	tint.position = Vector2.ZERO
	tint.size = Vector2(792, 372)
	tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(tint)'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("corridor wired")
