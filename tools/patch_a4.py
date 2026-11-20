# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()

if "var wanted" not in s:
    s = s.replace("var d12_done := false", "var d12_done := false\nvar wanted: Array = []\nvar mails: Array = []\nvar mail_seq := 1\nvar achievements: Dictionary = {}")

# init in reset
s = s.replace("\td12_done = false", "\td12_done = false\n\twanted = []\n\tmails = []\n\tmail_seq = 1\n\tachievements = {}")

# generate wanted + mail inside start_day (after quota calc)
old = '''	quota_required = maxi(0, day - 5)'''
new = '''	quota_required = maxi(0, day - 5)
	_generate_wanted()
	_push_briefing_mail()'''
assert old in s
s = s.replace(old, new)

s += '''

func _generate_wanted() -> void:
	wanted = []
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	var count := rng.randi_range(1, 2)
	var surnames: Array = Data.names.get("surnames", ["陈"])
	var given: Array = Data.names.get("given", ["明"])
	for i in count:
		var nm := String(surnames[rng.randi() % surnames.size()]) + String(given[rng.randi() % given.size()])
		var grade := rng.randi_range(7, 9)
		wanted.append({"name": nm, "id": RuleEngine.expected_prefix(grade) + "%04d" % rng.randi_range(0, 9999)})

func is_wanted(v: Dictionary) -> bool:
	for w in wanted:
		if String(w.get("name", "")) == String(v.get("name", "")) and String(w.get("id", "")) == String(v.get("student_id", "")):
			return true
	return false

func rules_versions() -> Array:
	var out: Array = []
	out.append({"v": 1, "day": 1, "title": "第 1 版", "lines": [
		"学生证须在有效期内，过期即拒。",
		"出生年份须与年级对应：七年级 2013、八年级 2012、九年级 2011。",
		"学号前四位须为入学年份：七年级 2025、八年级 2024、九年级 2023。"
	]})
	if day >= 3:
		out.append({"v": 2, "day": 3, "title": "第 2 版", "lines": [
			"实验学生须出示校园卡，状态须为有效。",
			"外校学生须出示一次性通行证，须在有效期内。"
		]})
	if day >= 8:
		out.append({"v": 3, "day": 8, "title": "第 3 版", "lines": [
			"一次性通行证作废。",
			"外校学生须出示纪检部准入证，须含学号、姓名、学校与来意。"
		]})
	if day >= 15:
		out.append({"v": 4, "day": 15, "title": "第 4 版", "lines": [
			"转学目的须提供转学介绍信。",
			"介绍信须有转出、转入双方教导主任签字。"
		]})
	if day >= 20:
		out.append({"v": 5, "day": 20, "title": "第 5 版", "lines": [
			"全体人员须出示健康证明。",
			"健康状态非「健康」者一律拒绝。"
		]})
	if day >= 25:
		out.append({"v": 6, "day": 25, "title": "第 6 版", "lines": [
			"伪造介绍信一律没收，不予退还。",
			"没收正常介绍信罚款 25 元，须登记在案。"
		]})
	return out

func _push_briefing_mail() -> void:
	var docs: Array = []
	for d in Data.doc_rules:
		if day >= int(d.get("day", 1)):
			docs.append(String(d.get("name", "")))
	var body := "第 %d 天执勤简报\\n余额：%d 元\\n今日核验：%s\\n拒签指标：%s" % [
		day, money, "、".join(docs),
		("至少拒绝 %d 人" % quota_required) if quota_required > 0 else "无"
	]
	mails.append({"id": mail_seq, "day": day, "kind": "brief", "from": "学生会纪检部", "subject": "第 %d 天执勤简报" % day, "body": body})
	mail_seq += 1
	if mails.size() > 12:
		mails = mails.slice(mails.size() - 12, mails.size())

func add_mail(from_who: String, subject: String, body: String, kind: String = "info") -> void:
	mails.append({"id": mail_seq, "day": day, "kind": kind, "from": from_who, "subject": subject, "body": body})
	mail_seq += 1

func unlock(ach_key: String, ach_name: String) -> bool:
	if achievements.has(ach_key):
		return false
	achievements[ach_key] = ach_name
	return true
'''
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("state extended")
