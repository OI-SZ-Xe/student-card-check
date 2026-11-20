# -*- coding: utf-8 -*-
import io

p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()

# fields
s = s.replace("var _rng := RandomNumberGenerator.new()", "var _rng := RandomNumberGenerator.new()\nvar player_name := \"检察员\"\nvar player_class := \"八年级（3）班\"")

# helper for stamp badges (insert before _shot_notice_header)
anchor = "func _shot_notice_header() -> void:"
helper = '''func _stamp_badge(text: String, color: Color) -> Control:
	var holder := Control.new()
	holder.custom_minimum_size = Vector2(140, 44)
	var box := Ui.panel(Color(0, 0, 0, 0), Color(color, 0.85), 2, 1, 0)
	box.position = Vector2(0, 0)
	box.size = Vector2(126, 42)
	box.rotation = -0.05
	holder.add_child(box)
	var l := Ui.label(text, 17, color, Ui.font_serif())
	l.position = Vector2(0, 8)
	l.size = Vector2(126, 26)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(l)
	return holder

'''
s = s.replace(anchor, helper + anchor, 1)

# replace _shot_assessment
start = s.index("func _shot_assessment() -> void:")
end = s.index("func _shot_admission() -> void:")
new_assess = '''func _shot_assessment() -> void:
	_clear()
	_black()
	var paper := _paper(Rect2(400, 110, 1120, 860))
	var head := Ui.label("纪检部入职考核表", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(64, 42)
	head.size = Vector2(600, 40)
	paper.add_child(head)
	var no := Ui.label("编号 JD-2026-047　　姓名：%s　　班级：%s" % [player_name, player_class], 15, Ui.INK, Ui.font_mono())
	no.position = Vector2(64, 88)
	no.size = Vector2(900, 22)
	paper.add_child(no)
	var rule := ColorRect.new()
	rule.color = Ui.PAPER_EDGE
	rule.position = Vector2(64, 118)
	rule.size = Vector2(992, 2)
	paper.add_child(rule)

	var rows := VBoxContainer.new()
	rows.position = Vector2(64, 142)
	rows.size = Vector2(992, 520)
	rows.add_theme_constant_override("separation", 14)
	paper.add_child(rows)

	var items := [
		["01", "笔试", "教育法规 · 校园安全条例 · 纪检部工作守则"],
		["02", "面试", "校园安全部主持 · 临场判断与政治觉悟"],
		["03", "政审", "本人及直系亲属无违纪记录"],
		["04", "体检", "色觉正常 · 可长时间注视证件细节"],
		["05", "宣誓", "面向校门宣读《检查员守则》全文"]
	]
	for item in items:
		if _skip or _ended: return
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 18)
		var idx := Ui.label(String(item[0]), 18, Color(0.55, 0.48, 0.36), Ui.font_mono())
		idx.custom_minimum_size = Vector2(44, 0)
		var nm := Ui.label(String(item[1]), 24, Ui.INK, Ui.font_serif())
		nm.custom_minimum_size = Vector2(96, 0)
		var desc := Ui.label(String(item[2]), 15, Ui.INK_SOFT, Ui.font_serif())
		desc.custom_minimum_size = Vector2(560, 0)
		var status := Control.new()
		status.custom_minimum_size = Vector2(140, 44)
		var wait_label := Ui.label("待　核", 17, Ui.INK_SOFT, Ui.font_mono())
		wait_label.position = Vector2(4, 10)
		status.add_child(wait_label)
		row.add_child(idx)
		row.add_child(nm)
		row.add_child(desc)
		row.add_child(status)
		rows.add_child(row)
		await _wait(0.5)
		if _ended: return
		wait_label.text = ""
		var badge := _stamp_badge("合 格", Color(0.66, 0.17, 0.13))
		badge.scale = Vector2(1.7, 1.7)
		badge.modulate = Color(1, 1, 1, 0)
		status.add_child(badge)
		var bt := create_tween()
		bt.set_parallel(true)
		bt.tween_property(badge, "scale", Vector2.ONE, 0.16)
		bt.tween_property(badge, "modulate", Color(1, 1, 1, 1), 0.10)
		Sfx.play("stamp", -14.0)
		await _wait(0.5)

	var foot := Ui.label("审查结论：准予录用　　审核人：校长　王明", 17, Ui.INK, Ui.font_serif())
	foot.position = Vector2(64, 720)
	foot.size = Vector2(700, 26)
	paper.add_child(foot)
	var sig := Signature.new()
	sig.setup(Data.sig("wang_ming"), 1.0)
	sig.position = Vector2(700, 700)
	sig.size = Vector2(300, 110)
	paper.add_child(sig)
	var sig_line := Ui.label("（校长签字）", 12, Ui.INK_SOFT, Ui.font_mono())
	sig_line.position = Vector2(720, 808)
	sig_line.size = Vector2(240, 18)
	paper.add_child(sig_line)
	await _wait(2.4)

'''
s = s[:start] + new_assess + s[end:]

# replace _shot_admission
start2 = s.index("func _shot_admission() -> void:")
end2 = s.index("func _shot_film_leader() -> void:")
new_admit = '''func _shot_admission() -> void:
	_clear()
	_black()
	await _wait(0.25)
	var card := _paper(Rect2(520, 260, 880, 580), Color("#ece2c6"))
	var small := Ui.label("深 圳 实 验 中 学", 18, Color(0.4, 0.36, 0.28), Ui.font_serif())
	small.position = Vector2(56, 44)
	small.size = Vector2(500, 24)
	card.add_child(small)
	var title := Ui.label("录 取 通 知", 46, Ui.INK, Ui.font_serif())
	title.position = Vector2(56, 82)
	title.size = Vector2(700, 60)
	card.add_child(title)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(56, 152)
	rule.size = Vector2(768, 3)
	card.add_child(rule)
	var body := Ui.rich("", 19, Ui.INK)
	body.position = Vector2(56, 186)
	body.size = Vector2(768, 250)
	body.scroll_active = false
	body.text = "兹录取　[b]%s[/b]（%s）为学生会纪检部检查员。\\n\\n请于 2026 年 3 月 1 日 07:00 到校门检查站报到，\\n携带本通知与学生证，着校服，不得迟到。" % [player_name, player_class]
	card.add_child(body)
	var foot := Ui.label("校长　王明", 16, Ui.INK, Ui.font_serif())
	foot.position = Vector2(520, 470)
	foot.size = Vector2(220, 22)
	foot.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	card.add_child(foot)
	var sig := Signature.new()
	sig.setup(Data.sig("wang_ming"), 1.0)
	sig.position = Vector2(430, 366)
	sig.size = Vector2(300, 110)
	card.add_child(sig)

	var stamp := Ui.label("准 予 入 职", 62, Color(0.72, 0.16, 0.12, 0.9), Ui.font_serif())
	stamp.position = Vector2(64, 360)
	stamp.size = Vector2(470, 96)
	stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stamp.rotation = -0.13
	stamp.scale = Vector2(2.8, 2.8)
	stamp.pivot_offset = stamp.size * 0.5
	stamp.modulate = Color(1, 1, 1, 0)
	card.add_child(stamp)
	await _wait(0.5)
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(stamp, "scale", Vector2.ONE, 0.24).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(stamp, "modulate", Color(1, 1, 1, 1), 0.14)
	Sfx.play("stamp", -3.0)
	await _wait(0.32)
	var shake := create_tween()
	shake.tween_property(_scene, "position", Vector2(10, -6), 0.05)
	shake.tween_property(_scene, "position", Vector2(-8, 4), 0.05)
	shake.tween_property(_scene, "position", Vector2.ZERO, 0.07)
	await _wait(2.4)

'''
s = s[:start2] + new_admit + s[end2:]

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("intro patched with player data")
