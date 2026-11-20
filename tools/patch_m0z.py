# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()
start = s.index("func _shot_guidance() -> void:")
end = s.index("func _shot_title() -> void:")
new = '''func _shot_guidance() -> void:
	var cards := [
		["01", "先看有效期，再抬头看人。", "证件是死的，站在窗口前的人是活的。"],
		["02", "称呼同学，不要称呼编号。", "你手里的是学生证，不是档案。"],
		["03", "遇到冲突，先退回窗口，再按对讲机。", "你的职责是核验，不是制服。"]
	]
	for i in cards.size():
		var c: Array = cards[i]
		if _skip or _ended: return
		_clear()
		var bg := ColorRect.new()
		bg.color = Color(0.075, 0.075, 0.07)
		bg.size = Vector2(1920, 1080)
		_scene.add_child(bg)
		_film_frame()
		var num := Ui.label(String(c[0]), 112, Color(0.60, 0.16, 0.12, 0.9), Ui.font_mono())
		num.position = Vector2(196, 396)
		num.size = Vector2(180, 130)
		_scene.add_child(num)
		var main := Ui.label(String(c[1]), 48, Color(0.93, 0.90, 0.79), Ui.font_serif())
		main.position = Vector2(392, 408)
		main.size = Vector2(1330, 80)
		_scene.add_child(main)
		var sub := Ui.label(String(c[2]), 23, Color(0.60, 0.60, 0.52), Ui.font_serif())
		sub.position = Vector2(396, 500)
		sub.size = Vector2(1200, 40)
		_scene.add_child(sub)
		var seal := Ui.panel(Color(0, 0, 0, 0), Color(0.62, 0.16, 0.12, 0.75), 3, 1, 0)
		seal.position = Vector2(1560, 700)
		seal.size = Vector2(150, 150)
		seal.rotation = -0.10
		_scene.add_child(seal)
		var seal_text := Ui.label("纪检部\\n审片", 22, Color(0.66, 0.18, 0.13, 0.85), Ui.font_serif())
		seal_text.position = Vector2(18, 44)
		seal_text.size = Vector2(114, 66)
		seal_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		seal.add_child(seal_text)
		var tag := Ui.label("第 %d 讲 / 共 3 讲　　纪检部学生指导短片" % (i + 1), 15, Color(0.42, 0.44, 0.38), Ui.font_mono())
		tag.position = Vector2(196, 946)
		tag.size = Vector2(900, 22)
		_scene.add_child(tag)
		await _wait(2.4)
		if _skip or _ended: return
	await _wait(0.2)

'''
s = s[:start] + new + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guidance cards patched")
