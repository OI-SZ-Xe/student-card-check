# -*- coding: utf-8 -*-
import io

vp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
v = io.open(vp, encoding="utf-8").read()

# consistent expiry: June 30 of graduation year (birth + grade + 6)
old_expiry = '''	var expiry := date_add(today, rng.randi_range(45, 420))'''
new_expiry = '''	var expiry := "%d-06-30" % (birth_year + grade + 6)'''
assert old_expiry in v
v = v.replace(old_expiry, new_expiry)

# if expiry forged, shift year by +/-1
v = v.replace('''	if rng.randf() < 0.07 * (1.0 + forgery_bonus):
		expiry = date_add(today, -rng.randi_range(1, 45))
		forged.append("expiry")''', '''	if rng.randf() < 0.07 * (1.0 + forgery_bonus):
		var true_expiry := expiry
		expiry = "%d-06-30" % (birth_year + grade + 6 + (1 if rng.randf() < 0.5 else -1))
		forged.append("expiry")''')

# record + excuse before return
v = v.replace('''	v["forged_fields"] = forged
	v["required"] = required_docs(day, is_exp, purpose, doc_rules)
	return v''', '''	var record := {
		"name": nm,
		"birth": "%d-%02d-%02d" % [RuleEngine.expected_birth_year(grade), 0, 0],
		"school": String(sch.get("name", "")),
		"id": sid,
		"old_names": [],
		"old_schools": [],
		"photo_seed": face_seed,
		"transfers": [],
		"valid": true
	}
	record["birth"] = "%d-" % RuleEngine.expected_birth_year(grade) + String(birth).substr(5)
	if "birth" in forged:
		record["birth"] = "%d-" % (RuleEngine.expected_birth_year(grade)) + String(birth).substr(5)
		record["id"] = prefix + String(sid).substr(4)
	if "id" in forged:
		record["id"] = prefix + String(sid).substr(4)
	if "photo" in forged:
		record["photo_seed"] = int(photo["seed"]) + 17
	if purpose == "转学":
		record["old_schools"] = [String(sch.get("name", ""))]
		record["transfers"] = [{"day": day, "from": String(sch.get("name", "")), "to": "深圳实验中学"}]
	if rng.randf() < 0.25:
		record["old_names"] = [String(nm).substr(0, 1) + "小" + String(nm).substr(1)]

	var excuse := {"kind": "none", "text": "没有问题，您查吧。", "obvious": false}
	if not forged.is_empty():
		var roll := rng.randf()
		if roll < 0.5:
			var lies := [
				"我爸是教育局的，您就别查了。",
				"昨天刚去派出所改的出生日期，系统还没更新。",
				"学号是我自己填的，怎么了？",
				"照片是去年的，人瘦了看不出来吗？"
			]
			excuse = {"kind": "lie", "text": String(lies[rng.randi() % lies.size()]), "obvious": true}
		else:
			var plausible := [
				{"kind": "surgery", "text": "上个月做了正颌手术，脸型和照片不太一样。"},
				{"kind": "rename", "text": "我改过名字，户口本上还是旧的。"},
				{"kind": "reissue", "text": "学生证补办过，有效期印错了。"},
				{"kind": "transfer_delay", "text": "转学手续还没走完，学校那边慢。"}
			]
			var pick: Dictionary = plausible[rng.randi() % plausible.size()]
			excuse = {"kind": String(pick.kind), "text": String(pick.text), "obvious": false}

	v["record"] = record
	v["excuse"] = excuse
	v["forged_fields"] = forged
	v["required"] = required_docs(day, is_exp, purpose, doc_rules)
	return v''')

# record birth should be the TRUE birth: rebuild before forging? keep simple: use expected year + same month/day
io.open(vp, "w", encoding="utf-8", newline="\n").write(v)
print("visitor record/excuse")
