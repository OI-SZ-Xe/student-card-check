# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()
anchor = "func _shot_notice_header() -> void:"
helpers = '''func _stamp_badge(text: String, color: Color) -> Control:
	var holder := Control.new()
	holder.custom_minimum_size = Vector2(140, 44)
	var box := Ui.panel(Color(0, 0, 0, 0), Color(color, 0.85), 2, 1, 0)
	box.size = Vector2(126, 42)
	box.rotation = -0.05
	holder.add_child(box)
	var l := Ui.label(text, 17, color, Ui.font_serif())
	l.position = Vector2(0, 8)
	l.size = Vector2(126, 26)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(l)
	return holder

func _film_frame() -> void:
	var col := Color(0.86, 0.84, 0.72, 0.22)
	for yy in [74.0, 1002.0]:
		var bar := ColorRect.new()
		bar.color = col
		bar.position = Vector2(100, yy)
		bar.size = Vector2(1720, 3)
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_scene.add_child(bar)
	for i in 13:
		var y := 96.0 + float(i) * 70.0
		for xx in [62.0, 1838.0]:
			var hole := ColorRect.new()
			hole.color = Color(0.84, 0.82, 0.70, 0.14)
			hole.position = Vector2(xx, y)
			hole.size = Vector2(14, 30)
			hole.mouse_filter = Control.MOUSE_FILTER_IGNORE
			_scene.add_child(hole)

'''
if "_stamp_badge" not in s:
    s = s.replace(anchor, helpers + anchor, 1)
else:
    # helpers exist but may still be missing one
    if "func _film_frame()" not in s:
        s = s.replace(anchor, helpers.split("func _film_frame")[0] + "func _film_frame" + helpers.split("func _film_frame")[1] + anchor, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("helpers restored:", "_stamp_badge" in s, "_film_frame" in s)
