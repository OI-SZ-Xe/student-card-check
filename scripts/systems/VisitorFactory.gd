class_name VisitorFactory
extends RefCounted

static var forgery_bonus := 0.0

static func date_add(iso: String, days: int) -> String:
	var unix := Time.get_unix_time_from_datetime_string(iso + "T00:00:00")
	return Time.get_datetime_string_from_unix_time(int(unix) + days * 86400).substr(0, 10)

static func required_docs(day: int, is_exp: bool, purpose: String, doc_rules: Array) -> Array:
	var out: Array = []
	for d in doc_rules:
		if day < int(d.get("day", 1)):
			continue
		var scope := String(d.get("scope", "all"))
		if scope == "experiment" and not is_exp:
			continue
		if scope == "external" and is_exp:
			continue
		if scope == "transfer" and purpose != "转学":
			continue
		out.append(String(d.get("key", "")))
	return out

static func make(day: int, today: String, rng: RandomNumberGenerator, names: Dictionary, schools: Array, principals: Dictionary, doc_rules: Array) -> Dictionary:
	var surnames: Array = names.get("surnames", ["陈"])
	var givens: Array = names.get("given", ["明"])
	var dialogues: Array = names.get("dialogue", ["检察员同学，材料都在这儿了。"])
	var purposes: Array = names.get("purposes", ["上课"])

	var nm := String(surnames[rng.randi() % surnames.size()])
	nm += String(givens[rng.randi() % givens.size()])
	if rng.randf() < 0.35:
		nm += String(givens[rng.randi() % givens.size()])

	var sch: Dictionary = schools[rng.randi() % schools.size()]
	var is_exp := bool(sch.get("experiment", false))
	var grade := 7 + rng.randi() % 3
	var birth_year := RuleEngine.expected_birth_year(grade)
	var birth := "%d-%02d-%02d" % [birth_year, rng.randi_range(1, 12), rng.randi_range(1, 28)]
	var prefix := RuleEngine.expected_prefix(grade)
	var sid := prefix + "%04d" % rng.randi_range(0, 9999)
	var expiry := "%d-06-30" % (birth_year + grade + 6)
	var forged: Array = []

	if rng.randf() < 0.09 * (1.0 + forgery_bonus):
		var delta: Array = [-2, -1, 1, 2]
		birth_year += int(delta[rng.randi() % delta.size()])
		birth = "%d-%02d-%02d" % [birth_year, rng.randi_range(1, 12), rng.randi_range(1, 28)]
		forged.append("birth")

	if rng.randf() < 0.09 * (1.0 + forgery_bonus):
		var shifted := int(prefix) + (1 if rng.randf() < 0.5 else -1)
		sid = "%04d" % shifted + sid.substr(4)
		forged.append("id")

	if rng.randf() < 0.07 * (1.0 + forgery_bonus):
		var true_expiry := expiry
		expiry = "%d-06-30" % (birth_year + grade + 6 + (1 if rng.randf() < 0.5 else -1))
		forged.append("expiry")

	var photo := {"seed": rng.randi_range(1, 999999), "state": "genuine"}
	var face_seed := int(photo["seed"])
	if day >= 5 and rng.randf() < 0.10 * (1.0 + forgery_bonus):
		if rng.randf() < 0.62:
			photo["state"] = "swapped"
			face_seed = rng.randi_range(1, 999999)
		else:
			photo["state"] = "mirrored"
		forged.append("photo")

	var purpose := ""
	if not is_exp:
		purpose = String(purposes[rng.randi() % purposes.size()])

	var v := {
		"name": nm,
		"grade": grade,
		"birth": birth,
		"student_id": sid,
		"expiry": expiry,
		"school": String(sch.get("name", "")),
		"experiment": is_exp,
		"purpose": purpose,
		"photo": photo,
		"face_seed": face_seed,
		"photo_mirrored": String(photo["state"]) == "mirrored",
		"forged_fields": forged,
		"dialogue": String(dialogues[rng.randi() % dialogues.size()]),
		"wanted": false
	}

	if is_exp and day >= 3:
		v["campus_card"] = {
			"valid": rng.randf() > 0.16,
			"card_no": "C" + String(sid).substr(4),
			"holder": nm,
			"valid_until": expiry
		}
		if not bool(v["campus_card"]["valid"]):
			forged.append("campus_card")

	if not is_exp and day >= 3:
		v["temp_pass"] = {"valid_until": date_add(today, rng.randi_range(-18, 70))}
		if String(v["temp_pass"]["valid_until"]) < today:
			forged.append("temp_pass")

	if not is_exp and day >= 8:
		var shown := purpose
		if rng.randf() < 0.12:
			shown = ""
		v["security_pass"] = {"purpose": shown}
		if shown == "":
			forged.append("security_pass")

	if not is_exp and day >= 15 and purpose == "转学":
		var from_school := String(sch.get("name", ""))
		var from_sig := String(sch.get("dean_sig", ""))
		var expect_from := String(principals.get(from_school, ""))
		var sig_from := expect_from
		var sig_to := String(principals.get("深圳实验中学", ""))
		var to_sig := "dean_sy"
		var letter_forged := rng.randf() < 0.32
		var variant_from := "genuine"
		var variant_to := "genuine"
		var defect := ""
		if letter_forged:
			if rng.randf() < 0.28:
				var others: Array = []
				for s2 in schools:
					if String(s2.get("name", "")) != from_school:
						others.append(s2)
				if others.size() > 0:
					var wrong: Dictionary = others[rng.randi() % others.size()]
					sig_from = String(wrong.get("dean", ""))
					from_sig = String(wrong.get("dean_sig", from_sig))
					defect = "wrong_signature"
				else:
					defect = "no_emboss"
			else:
				var variants: Array = ["miss", "light", "plain", "mirror"]
				variant_from = String(variants[rng.randi() % variants.size()])
				defect = variant_from
			forged.append("transfer_letter")
		v["transfer_letter"] = {
			"from_school": from_school,
			"to_school": "深圳实验中学",
			"from_sig_id": from_sig,
			"to_sig_id": to_sig,
			"sig_from": sig_from,
			"sig_to": sig_to,
			"variant_from": variant_from,
			"variant_to": variant_to,
			"forged": letter_forged,
			"defect": defect
		}

	if day >= 20:
		var status := "健康"
		if rng.randf() < 0.22:
			status = ["感冒", "过敏", "低烧"][rng.randi() % 3]
		var cert_forged := status != "健康" and rng.randf() < 0.45
		v["health_cert"] = {"status": status, "forged": cert_forged}
		if status != "健康":
			forged.append("health_cert")

	var record := {
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
	var docs := {
		"student_card": {
			"name": nm, "grade": grade, "birth": birth,
			"student_id": sid, "expiry": expiry,
			"school": String(sch.get("name", "")), "photo": photo
		}
	}
	for k in ["campus_card", "temp_pass", "security_pass", "transfer_letter", "health_cert"]:
		if v.has(k):
			docs[k] = v[k]
	if rng.randf() < 0.12:
		var pool: Array = []
		for k2 in docs.keys():
			if k2 != "student_card":
				pool.append(k2)
		if pool.size() > 0:
			var miss := String(pool[rng.randi() % pool.size()])
			docs[miss]["missing"] = true
			docs[miss]["can_supply"] = rng.randf() < 0.6
	v["docs"] = docs
	v["forged_fields"] = forged
	v["required"] = required_docs(day, is_exp, purpose, doc_rules)
	return v