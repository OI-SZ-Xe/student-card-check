# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''func debug_gun(auto_resolve: bool = false) -> void:
	_open_gun_event()
	if auto_resolve:
		await get_tree().create_timer(1.0).timeout
		for c in get_children():
			if c is SchoolRush:
				c._resolve()'''
new = '''func debug_gun(auto_resolve: bool = false) -> void:
	_open_gun_event()
	if auto_resolve:
		for c in get_children():
			if c is SchoolRush:
				c._resolve()'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

sp = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s = io.open(sp, encoding="utf-8").read()
old2 = '''	_hint = Ui.label("3 发橡皮弹 · 点击射击 · 误伤学生或校警要担责", 17, Color(0.72, 0.76, 0.66), Ui.font_serif())
	_hint.position = Vector2(0, 960)
	_hint.size = Vector2(1920, 26)
	_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(_hint)'''
new2 = '''	var bar := ColorRect.new()
	bar.color = Color(0.03, 0.04, 0.03, 0.85)
	bar.position = Vector2(0, 1000)
	bar.size = Vector2(1920, 80)
	add_child(bar)
	_hint = Ui.label("3 发橡皮弹 · 点击射击 · 误伤学生或校警要担责", 17, Color(0.72, 0.76, 0.66), Ui.font_serif())
	_hint.position = Vector2(0, 1030)
	_hint.size = Vector2(1920, 26)
	_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(_hint)

	var stamp := Ui.label("2026-03-12　07:00:12", 15, Color(0.72, 0.78, 0.68), Ui.font_mono())
	stamp.position = Vector2(1560, 48)
	stamp.size = Vector2(320, 22)
	stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	add_child(stamp)

	var gate_sign := Ui.label("深 圳 实 验 中 学　东 门", 20, Color(0.55, 0.60, 0.50), Ui.font_serif())
	gate_sign.position = Vector2(60, 560)
	gate_sign.size = Vector2(460, 28)
	add_child(gate_sign)'''
assert old2 in s
s = s.replace(old2, new2)
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("hint bar + timestamp")
