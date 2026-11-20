# -*- coding: utf-8 -*-
import io

# State flags
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var called_this" not in s:
    s = s.replace("var forgery_bonus := 0.0", "var forgery_bonus := 0.0\nvar called_this := false\nvar db_checked_this := false")
    s = s.replace("State.called_this", "State.called_this")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Desk: use State flags, reset per visitor, phone verdict sets flag
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('"called": _called_this,\n\t\t"db_checked": _db_checked_this', '"called": State.called_this,\n\t\t"db_checked": State.db_checked_this')
d = d.replace('''	_called_this = false
	_db_checked_this = false''', '''	State.called_this = false
	State.db_checked_this = false''')
d = d.replace('''	if target == "教育局":
		var sid := String(_visitor.get("student_id", ""))''', '''	if target == "教育局" or target == "深圳实验中学" or target != "":
		State.called_this = true
		var forged: Array = _visitor.get("forged_fields", [])
		var truthful := randf() < 0.75
		var bad := (not forged.is_empty()) if truthful else forged.is_empty()
		reply = "%s 值班室：这位同学的档案%s。" % [target if target != "" else "学校", "对不上" if bad else "没问题"]
		_msg("电话：" + reply + "（电话核查不一定准）", Color("#cfe0f0"))
		_unlock_ach("firstCall", "第一次通话")
		Sfx.play("click", -10.0)
		if is_instance_valid(overlay):
			overlay.queue_free()
			_paused = false
		return
	if target == "教育局":
		var sid := String(_visitor.get("student_id", ""))''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Interrogation: remove inline phone/db buttons, replace hint
ip = r"F:\请出示学生证\scripts\ui\Interrogation.gd"
it = io.open(ip, encoding="utf-8").read()
it = it.replace('''	var phone := Ui.button("电话核查（8 秒）", 16, Color(0.20, 0.26, 0.22), Ui.WHITE)
	phone.position = Vector2(36, 512)
	phone.size = Vector2(230, 48)
	phone.pressed.connect(_verify_phone)
	paper.add_child(phone)

	var db := Ui.button("查教育局档案（25 秒）", 16, Color(0.18, 0.22, 0.30), Ui.WHITE)
	db.position = Vector2(282, 512)
	db.size = Vector2(270, 48)
	db.pressed.connect(_query_db)
	paper.add_child(db)
''', '''	var guide := Ui.rich("核实手段要自己动手：\\n　· 电话：按 P 打开话机，拨学校或教育局号码，听完回复\\n　· 档案：打开电脑 → 浏览器 → 教育局档案，输入姓名查询（慢，但准）", 15, Ui.INK)
	guide.position = Vector2(36, 500)
	guide.size = Vector2(808, 120)
	guide.scroll_active = false
	paper.add_child(guide)
''')
io.open(ip, "w", encoding="utf-8", newline="\n").write(it)

# Terminal archive: accurate record + db flag + autoFill
tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
t = t.replace('''	row.add_child(input)''', '''	if State.has_upgrade("autoFill") and not visitor.is_empty():
		input.text = String(visitor.get("name", ""))
	row.add_child(input)''')
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)
print("manual checks wired")
