extends SceneTree

var passed := 0
var failed := 0
var rules: Dictionary = {}
var doc_rules: Array = []
var schools: Array = []
var principals: Dictionary = {}

func _initialize() -> void:
	_load_data()
	test_grade_tables()
	test_genuine_allow()
	test_expired()
	test_birth_mismatch()
	test_id_mismatch()
	test_photo()
	test_missing_doc()
	test_transfer_signature()
	test_health()
	test_compare_hint()
	test_factory_determinism()
	test_factory_docs_gating()
	test_factory_forgery_rate()
	print("TESTS PASSED %d / FAILED %d" % [passed, failed])
	quit(1 if failed > 0 else 0)

func _load_data() -> void:
	var raw_rules: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/rules.json"))
	if raw_rules is Dictionary:
		rules = raw_rules
	var raw_docs: Variant = rules.get("docs", [])
	if raw_docs is Array:
		doc_rules = raw_docs
	var raw_schools: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/schools.json"))
	if raw_schools is Array:
		schools = raw_schools
	for s in schools:
		principals[String(s.get("name", ""))] = String(s.get("principal", ""))

func ok(cond: bool, name: String) -> void:
	if cond:
		passed += 1
	else:
		failed += 1
		printerr("FAIL: " + name)

func base_visitor() -> Dictionary:
	return {
		"name": "陈明",
		"grade": 8,
		"birth": "2012-05-04",
		"student_id": "20241234",
		"expiry": "2027-01-20",
		"school": "深圳实验中学",
		"experiment": true,
		"photo": {"seed": 1, "state": "genuine"},
		"purpose": ""
	}

func make_ctx(required: Array = []) -> Dictionary:
	return {
		"required": required,
		"doc_names": {"campus_card": "校园卡", "temp_pass": "临时通行证", "health_cert": "健康证明"},
		"principals": principals,
		"check_photo": true
	}

func has_reason(res: Dictionary, keyword: String) -> bool:
	for r in res.get("reasons", []):
		if String(r).find(keyword) >= 0:
			return true
	return false

func test_grade_tables() -> void:
	ok(RuleEngine.expected_birth_year(7) == 2013, "grade7 birth 2013")
	ok(RuleEngine.expected_birth_year(8) == 2012, "grade8 birth 2012")
	ok(RuleEngine.expected_birth_year(9) == 2011, "grade9 birth 2011")
	ok(RuleEngine.expected_prefix(7) == "2025", "grade7 prefix")
	ok(RuleEngine.expected_prefix(8) == "2024", "grade8 prefix")
	ok(RuleEngine.expected_prefix(9) == "2023", "grade9 prefix")

func test_genuine_allow() -> void:
	var v := base_visitor()
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(bool(res.get("allow", false)) == true, "genuine visitor allowed")
	ok((res.get("reasons", []) as Array).is_empty(), "genuine visitor has no reasons")

func test_expired() -> void:
	var v := base_visitor()
	v["expiry"] = "2025-12-31"
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(bool(res.get("allow", true)) == false, "expired rejected")
	ok(has_reason(res, "过期"), "expired reason mentions 过期")

func test_birth_mismatch() -> void:
	var v := base_visitor()
	v["birth"] = "2013-05-04"
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res.get("allow", true)), "birth mismatch rejected")
	ok(has_reason(res, "出生年"), "birth mismatch reason")

func test_id_mismatch() -> void:
	var v := base_visitor()
	v["student_id"] = "20231234"
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res.get("allow", true)), "id prefix mismatch rejected")
	ok(has_reason(res, "学号前缀"), "id mismatch reason")

func test_photo() -> void:
	var v := base_visitor()
	v["photo"] = {"seed": 99, "state": "swapped"}
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res.get("allow", true)), "swapped photo rejected")
	ok(has_reason(res, "证件照"), "photo reason")
	var v2 := base_visitor()
	v2["photo"] = {"seed": 1, "state": "mirrored"}
	var res2 := RuleEngine.evaluate(v2, "2026-03-01", make_ctx())
	ok(not bool(res2.get("allow", true)), "mirrored photo rejected")

func test_missing_doc() -> void:
	var v := base_visitor()
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx(["campus_card"]))
	ok(not bool(res.get("allow", true)), "missing campus card rejected")
	ok(has_reason(res, "缺少"), "missing doc reason")
	v["campus_card"] = {"valid": false}
	var res2 := RuleEngine.evaluate(v, "2026-03-01", make_ctx(["campus_card"]))
	ok(not bool(res2.get("allow", true)), "invalid campus card rejected")

func test_transfer_signature() -> void:
	var v := base_visitor()
	v["school"] = "深圳中学"
	v["experiment"] = false
	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "李华",
		"sig_to": "王明",
		"forged": false
	}
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res.get("allow", true)), "wrong principal rejected")
	ok(has_reason(res, "签名不符"), "signature reason")
	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "王明",
		"sig_to": "王明",
		"variant_from": "plain",
		"forged": true
	}
	var res2 := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res2.get("allow", true)), "no-emboss letter rejected")
	ok(has_reason(res2, "压痕"), "no-emboss reason")

	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "王明",
		"sig_to": "王明",
		"variant_from": "miss",
		"forged": true
	}
	var res3 := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res3.get("allow", true)), "missing stroke rejected")
	ok(has_reason(res3, "缺笔"), "missing stroke reason")

	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "王明",
		"sig_to": "王明",
		"variant_from": "mirror",
		"forged": true
	}
	var res4 := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(has_reason(res4, "镜像"), "mirror reason")

	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "王明",
		"sig_to": "王明",
		"variant_from": "light",
		"forged": true
	}
	var res5 := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(has_reason(res5, "墨色"), "light ink reason")

func test_health() -> void:
	var v := base_visitor()
	v["health_cert"] = {"status": "感冒", "forged": false}
	var res := RuleEngine.evaluate(v, "2026-03-01", make_ctx(["health_cert"]))
	ok(not bool(res.get("allow", true)), "unhealthy rejected")
	ok(has_reason(res, "健康"), "health reason")

func test_compare_hint() -> void:
	var v := base_visitor()
	var hint := RuleEngine.compare_hint("grade", "birth", v, "2026-03-01")
	ok(hint.find("2012") >= 0, "compare hint contains expected year")
	var hint2 := RuleEngine.compare_hint("expiry", "today", v, "2026-03-01")
	ok(hint2.find("有效") >= 0, "compare hint expiry")

func test_factory_determinism() -> void:
	var names: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/names.json"))
	var r1 := RandomNumberGenerator.new()
	r1.seed = 4242
	var r2 := RandomNumberGenerator.new()
	r2.seed = 4242
	var v1 := VisitorFactory.make(8, "2026-03-08", r1, names, schools, principals, doc_rules)
	var v2 := VisitorFactory.make(8, "2026-03-08", r2, names, schools, principals, doc_rules)
	ok(String(v1.get("student_id", "")) == String(v2.get("student_id", "")), "factory deterministic id")
	ok(String(v1.get("name", "")) == String(v2.get("name", "")), "factory deterministic name")

func test_factory_docs_gating() -> void:
	var names: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/names.json"))
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	var d1 := VisitorFactory.required_docs(1, false, "", doc_rules)
	ok(d1 == ["student_card"], "day1 only student card")
	var d3 := VisitorFactory.required_docs(3, false, "上课", doc_rules)
	ok(d3.has("temp_pass"), "day3 external gets temp pass")
	var d8 := VisitorFactory.required_docs(8, false, "上课", doc_rules)
	ok(d8.has("security_pass"), "day8 external gets security pass")
	var d20 := VisitorFactory.required_docs(20, true, "", doc_rules)
	ok(d20.has("health_cert"), "day20 everyone gets health cert")
	ok(not d20.has("temp_pass"), "experiment student has no temp pass")

func test_factory_forgery_rate() -> void:
	var names: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/names.json"))
	var rng := RandomNumberGenerator.new()
	rng.seed = 2026
	var forged := 0
	for i in 400:
		var v := VisitorFactory.make(20, "2026-03-20", rng, names, schools, principals, doc_rules)
		if not (v.get("forged_fields", []) as Array).is_empty():
			forged += 1
	ok(forged > 40 and forged < 250, "forgery rate plausible (%d/400)" % forged)
