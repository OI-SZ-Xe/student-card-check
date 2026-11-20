# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# quota at end day
old_quota = '''func _end_day() -> void:
	State.running = false
	var s := State.finish_day()'''
new_quota = '''func _end_day() -> void:
	State.running = false
	if State.quota_required > 0:
		if State.quota_done >= State.quota_required:
			State.quota_met_days += 1
		else:
			State.quota_missed += 1
			State.add_suspicion(3)
			State.add_mail("校园安全部", "第 %d 天拒签未达标" % State.day, "本日应拒签 %d 人，实际 %d 人。已记录在案。" % [State.quota_required, State.quota_done], "warn")
	var s := State.finish_day()'''
assert old_quota in d
d = d.replace(old_quota, new_quota)

# endings selection + texts
old_sel = '''	var k := kind
	if k == "":
		if State.corruption >= 3:
			k = "corrupt"
		elif State.suspicion >= 60:
			k = "gun"
		elif State.money < 0:
			k = "debt"
		else:
			k = "stable"'''
new_sel = '''	var k := kind
	if k == "":
		if State.money < 0:
			k = "debt"
		elif State.corruption >= 3:
			k = "corrupt"
		elif State.escape_ready:
			k = "escape"
		elif State.trust >= 5:
			k = "revolution"
		elif State.trust > 0:
			k = "gun"
		elif State.suspicion >= 70:
			k = "gun"
		else:
			k = "stable"'''
assert old_sel in d
d = d.replace(old_sel, new_sel)

old_titles = '''	var titles := {
		"debt": "负债结局",
		"corrupt": "腐败结局",
		"gun": "忠诚线结局（枪毙）",
		"stable": "忠诚线结局（平稳）"
	}'''
new_titles = '''	var titles := {
		"debt": "负债结局",
		"corrupt": "腐败结局",
		"gun": "忠诚线结局（枪毙）",
		"stable": "忠诚线结局（平稳）",
		"escape": "逃亡结局",
		"revolution": "革命线结局"
	}'''
assert old_titles in d
d = d.replace(old_titles, new_titles)

old_texts = '''	var texts := {
		"debt": "由于长期负债，你被纪检部隔离审查，最终失去了学生身份……",'''
new_texts = '''	var texts := {
		"escape": "你带着一封真的介绍信、一张假证和一张高铁票离开了深圳。8 小时后，浑身酸痛的你看到了新学校：河北衡水第二中学。有些迟疑的学生会干部批准你进入。喘口气吧。但是记住：「衡水二中至高无上！」",
		"revolution": "同志，您好！今天是光荣的一天。学生斗争委员会的革命成功了。校园里推行了民主改革，你被任命为新一届学生会纪检部部长。校园里充满希望，但这条路同样充满挑战。现在，光荣属于新深圳实验。",
		"debt": "由于长期负债，你被纪检部隔离审查，最终失去了学生身份……",'''
assert old_texts in d
d = d.replace(old_texts, new_texts)

# escape button in refresh hud
old_hud_end = '''	_fill_rules()
	_fill_stats()'''
new_hud_end = '''	_fill_rules()
	_fill_stats()
	var esc := get_node_or_null("EscapeBtn")
	var can_escape := State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.money >= 150 and not State.escape_ready
	if can_escape and esc == null:
		var b := Ui.button("启动逃亡", 14, Color(0.35, 0.22, 0.16), Ui.WHITE)
		b.name = "EscapeBtn"
		b.position = Vector2(1608, 3)
		b.size = Vector2(120, 30)
		b.pressed.connect(_try_escape)
		add_child(b)
	elif not can_escape and esc != null:
		esc.queue_free()'''
assert old_hud_end in d
d = d.replace(old_hud_end, new_hud_end)

# achievements hooks
d = d.replace('''		State.money += bonus
		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_msg("逮捕完成''', '''		State.money += bonus
		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_unlock_ach("firstArrest", "执法如山")
		_msg("逮捕完成''')
d = d.replace('''		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_msg("已没收伪造的转学介绍信''', '''		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_unlock_ach("firstConfiscation", "铁面无私")
		_msg("已没收伪造的转学介绍信''')

# unlock function append-message version
old_unlock = '''func _unlock_ach(key: String, ach_name: String) -> void:
	if State.unlock(key, ach_name):
		_msg("成就解锁：%s" % ach_name, Color("#ffd98a"))'''
new_unlock = '''func _unlock_ach(key: String, ach_name: String) -> void:
	if State.unlock(key, ach_name):
		var cur: String = ""
		if _msg_label != null:
			cur = _msg_label.text
		var line := "成就解锁：%s" % ach_name
		_msg((line if cur == "" else cur + "　｜　" + line), Color("#ffd98a"))'''
assert old_unlock in d
d = d.replace(old_unlock, new_unlock)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("quota/endings/escape/achievements wired")
