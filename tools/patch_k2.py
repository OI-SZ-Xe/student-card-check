# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "rain.png" not in d:
    d = d.replace('''	var queue_tex := TextureRect.new()''', '''	if State.day % 5 == 0:
		var rain := TextureRect.new()
		rain.texture = load("res://art/props/rain.png")
		rain.stretch_mode = TextureRect.STRETCH_TILE
		rain.position = Vector2.ZERO
		rain.size = Vector2(792, 372)
		rain.modulate = Color(1, 1, 1, 0.55)
		rain.mouse_filter = Control.MOUSE_FILTER_IGNORE
		glass.add_child(rain)
		var drift := create_tween()
		drift.set_loops()
		drift.tween_property(rain, "position:x", -8.0, 1.2).set_trans(Tween.TRANS_LINEAR)
		drift.tween_property(rain, "position:x", 0.0, 0.001)

	var queue_tex := TextureRect.new()''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("rain overlay")
