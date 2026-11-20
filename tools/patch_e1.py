# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()

if "const ACHIEVEMENTS" not in s:
    s = s.replace("var stocks: Array = []", '''const ACHIEVEMENTS := [
	{"key": "firstArrest", "name": "执法如山", "desc": "首次逮捕伪造者"},
	{"key": "firstCall", "name": "第一次通话", "desc": "首次使用电话核实"},
	{"key": "firstCompare", "name": "第一次比对", "desc": "首次使用对照模式"},
	{"key": "firstConfiscation", "name": "铁面无私", "desc": "首次没收伪造介绍信"},
	{"key": "confiscator", "name": "铁面无私·改", "desc": "没收一封正常介绍信"},
	{"key": "tenCorrect", "name": "十连正确", "desc": "累计正确审核 10 次"},
	{"key": "perfectDay", "name": "完美执勤", "desc": "某天零差错"},
	{"key": "corrupt", "name": "腐败的检察员", "desc": "第一次收受贿赂"},
	{"key": "undercover", "name": "暗中支持", "desc": "第一次帮助学生斗争委员会"},
	{"key": "whistleblower", "name": "举报者", "desc": "累计举报 3 次"},
	{"key": "survivalist", "name": "老油条", "desc": "活到第 30 天"},
	{"key": "fugitive", "name": "逃亡者", "desc": "触发逃亡结局"},
	{"key": "revolutionary", "name": "革命先驱", "desc": "触发革命结局"},
	{"key": "loyalist", "name": "忠诚卫士", "desc": "触发忠诚结局"}
]

var flavor := ""

var stocks: Array = []''')
    s = s.replace("\tstocks = []", "\tflavor = \"\"\n\tstocks = []")
    s = s.replace('''	pending_org = events.get(day, {})''', '''	pending_org = events.get(day, {})
	if not pending_org.is_empty():
		add_mail("学生斗争委员会", String(pending_org.get("subject", "")), String(pending_org.get("body", "")), "org")''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Terminal: achievements page from list + org mail handle button + signal
tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
t = t.replace("signal time_cost(seconds: float)", "signal time_cost(seconds: float)\nsignal org_requested(mail_id: int)")
old_achv = '''func _site_achv() -> void:
	if State.achievements.is_empty():
		_body.add_child(_line("尚无成就。", DIM, 17))
		return
	for k in State.achievements.keys():
		_body.add_child(_line("· %s" % String(State.achievements[k]), GREEN, 17))'''
new_achv = '''func _site_achv() -> void:
	var got := 0
	for a in State.ACHIEVEMENTS:
		var unlocked: bool = State.achievements.has(String(a.key))
		if unlocked:
			got += 1
		var mark := "■" if unlocked else "□"
		var col := GREEN if unlocked else DIM
		_body.add_child(_line("%s %s　—　%s" % [mark, String(a.name), String(a.desc)], col, 16))
	_body.add_child(_line("已解锁 %d / %d" % [got, State.ACHIEVEMENTS.size()], AMBER, 15))'''
assert old_achv in t
t = t.replace(old_achv, new_achv)

old_mail_btn = '''		b.pressed.connect(func() -> void: _show_mail(m))
		_body.add_child(b)'''
new_mail_btn = '''		b.pressed.connect(func() -> void: _show_mail(m))
		_body.add_child(b)
		if String(m.get("kind", "")) == "org":
			var handle := Ui.button("处理这封邮件", 14, Color("#1a2a1a"), AMBER)
			handle.custom_minimum_size = Vector2(240, 34)
			var mid := int(m.get("id", 0))
			handle.pressed.connect(func() -> void: org_requested.emit(mid))
			_body.add_child(handle)'''
assert old_mail_btn in t
t = t.replace(old_mail_btn, new_mail_btn)
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)
print("E: achievements list + org mail entry")
