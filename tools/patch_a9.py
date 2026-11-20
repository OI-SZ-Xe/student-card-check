# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()

helper = '''func _block(bg: Color = Color(0.06, 0.12, 0.08, 0.8), edge: Color = EDGE) -> VBoxContainer:
	var pc := PanelContainer.new()
	pc.add_theme_stylebox_override("panel", Ui.style(bg, edge, 1, 0, 12))
	pc.custom_minimum_size = Vector2(1180, 0)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 4)
	pc.add_child(vb)
	_body.add_child(pc)
	return vb

func _site_schools() -> void:'''
s = s.replace("func _site_schools() -> void:", helper, 1)

# rewrite body of _site_schools
start = s.index("func _site_schools() -> void:")
end = s.index("func _address_of(")
new_schools = '''func _site_schools() -> void:
	for sch in Data.schools:
		var nm := String(sch.get("name", ""))
		var vb := _block()
		vb.add_child(_line("■ " + nm, AMBER, 18))
		vb.add_child(_line("校长：%s　　教导主任：%s" % [String(sch.get("principal", "")), String(sch.get("dean", ""))], GREEN, 16))
		vb.add_child(_line("总机：%s" % String(Data.phones.get(nm, "——")), DIM, 15))
		vb.add_child(_line("地址：%s" % _address_of(nm), DIM, 15))

'''
s = s[:start] + new_schools + s[end:]

# rules
start = s.index("func _site_rules() -> void:")
end = s.index("func _site_wanted() -> void:")
new_rules = '''func _site_rules() -> void:
	var versions := State.rules_versions()
	for i in versions.size():
		var v: Dictionary = versions[i]
		var active := i == versions.size() - 1
		var vb := _block(Color(0.08, 0.14, 0.1, 0.85) if active else Color(0.04, 0.07, 0.05, 0.7))
		var tag := "　【现行】" if active else "　（已废止）"
		vb.add_child(_line("%s　第 %d 天起%s" % [String(v.get("title", "")), int(v.get("day", 1)), tag], AMBER if active else DIM, 18))
		for l in v.get("lines", []):
			vb.add_child(_line("· " + String(l), GREEN if active else DIM, 15))

'''
s = s[:start] + new_rules + s[end:]

# wanted
start = s.index("func _site_wanted() -> void:")
end = s.index("func _site_archive() -> void:")
new_wanted = '''func _site_wanted() -> void:
	if State.wanted.is_empty():
		_body.add_child(_line("协查通报：暂无。", DIM, 17))
		return
	_body.add_child(_line("今日协查通报（%d 人）" % State.wanted.size(), RED, 19))
	for w in State.wanted:
		var vb := _block(Color(0.12, 0.06, 0.06, 0.8), Color(0.4, 0.2, 0.18))
		vb.add_child(_line("姓名：%s" % String(w.get("name", "")), GREEN, 18))
		vb.add_child(_line("学号：%s" % String(w.get("id", "")), DIM, 16))
		vb.add_child(_line("处置：拒绝进入；放行者罚款 100 元并记录。", DIM, 14))

'''
s = s[:start] + new_wanted + s[end:]

# mail detail block
old_mail = '''func _show_mail(m: Dictionary) -> void:
	var box := Ui.panel(Color(0.03, 0.07, 0.05), EDGE, 1, 0, 14)
	box.custom_minimum_size = Vector2(1180, 0)
	box.add_child(_line("发件人：%s" % String(m.get("from", "")), AMBER, 16))
	box.add_child(_line("主题：%s" % String(m.get("subject", "")), GREEN, 16))
	box.add_child(_line(String(m.get("body", "")), GREEN, 15))
	_body.add_child(box)'''
new_mail = '''func _show_mail(m: Dictionary) -> void:
	var vb := _block(Color(0.03, 0.07, 0.05))
	vb.add_child(_line("发件人：%s" % String(m.get("from", "")), AMBER, 16))
	vb.add_child(_line("主题：%s" % String(m.get("subject", "")), GREEN, 16))
	vb.add_child(_line(String(m.get("body", "")), GREEN, 15))'''
assert old_mail in s
s = s.replace(old_mail, new_mail)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("terminal blocks fixed")
