# -*- coding: utf-8 -*-
import io
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
# 今日 row after expiry
c = c.replace('''		["expiry", "有效期", String(visitor.get("expiry", ""))],''', '''		["expiry", "有效期", String(visitor.get("expiry", ""))],
		["today", "今日", String(today)],''')
# photo hit area
c = c.replace('''	var photo_tag := Ui.label("证件照", 12, Ui.INK_SOFT, Ui.font_serif())''', '''	var photo_btn := Button.new()
	photo_btn.flat = true
	photo_btn.focus_mode = Control.FOCUS_NONE
	photo_btn.position = Vector2(392, 74)
	photo_btn.size = Vector2(136, 168)
	photo_btn.set_meta("field_id", "photo")
	photo_btn.mouse_filter = Control.MOUSE_FILTER_IGNORE
	photo_btn.pressed.connect(func() -> void: field_picked.emit("photo"))
	add_child(photo_btn)
	var photo_tag := Ui.label("证件照", 12, Ui.INK_SOFT, Ui.font_serif())''')
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

rp = r"F:\请出示学生证\scripts\systems\RuleEngine.gd"
r = io.open(rp, encoding="utf-8").read()
r = r.replace('''	var grade := int(v.get("grade", 0))
	match key:''', '''	var grade := int(v.get("grade", 0))
	if a == "photo" or b == "photo":
		var other := b if a == "photo" else a
		if other == "today" or other == "name" or other == "grade" or other == "school":
			return "对照证件照与本人：看五官比例、痣的位置、耳形。换脸的人对不上；镜像翻拍会左右颠倒，发型分缝也会反。"
		return "证件照只能和「本人」对照，或者和数据库里的存档照对照（查档案可看）。"
	match key:''')
r = r.replace('''		"birth|id":''', '''		"birth|today":
			var by4 := birth_year_of(String(v.get("birth", "")))
			var ty := int(today.substr(0, 4))
			var age := ty - by4
			return "出生 %d 年，今日 %d 年 → 实岁约 %d 岁；%d 年级应在 %d~%d 岁" % [by4, ty, age, grade, grade + 5, grade + 7]
		"birth|id":''')
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)
print("photo/today compare")
