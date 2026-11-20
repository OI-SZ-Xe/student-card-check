class_name RuleEngine
extends RefCounted

const BIRTH := {7: 2013, 8: 2012, 9: 2011}
const PREFIX := {7: "2025", 8: "2024", 9: "2023"}

static func expected_birth_year(grade: int) -> int:
	return int(BIRTH.get(grade, 0))

static func expected_prefix(grade: int) -> String:
	return String(PREFIX.get(grade, ""))

static func birth_year_of(birth: String) -> int:
	if birth.length() < 4:
		return 0
	return int(birth.substr(0, 4))

static func evaluate(v: Dictionary, today: String, ctx: Dictionary) -> Dictionary:
	var reasons: Array[String] = []
	var fields: Array[String] = []

	var required: Array = ctx.get("required", [])
	var doc_names: Dictionary = ctx.get("doc_names", {})
	for key in required:
		var k := String(key)
		var dv: Dictionary = v.get("docs", {})
		if dv.has(k) and bool(dv[k].get("missing", false)):
			reasons.append("未提交%s" % String(doc_names.get(k, k)))
			fields.append(k)
			continue
		if k == "student_card":
			continue
		if not v.has(k) or v.get(k) == null:
			reasons.append("缺少%s" % String(doc_names.get(k, k)))
			fields.append(k)

	if String(v.get("expiry", "")) < today:
		reasons.append("学生证已过期（有效期 %s，今日 %s）" % [String(v.get("expiry", "")), today])
		fields.append("expiry")

	if bool(ctx.get("check_photo", true)):
		var photo: Dictionary = v.get("photo", {})
		var st := String(photo.get("state", "genuine"))
		if st == "swapped":
			reasons.append("证件照与本人不符（换脸）")
			fields.append("photo")
		elif st == "mirrored":
			reasons.append("证件照为镜像翻拍")
			fields.append("photo")

	var grade := int(v.get("grade", 0))
	var expect_year := expected_birth_year(grade)
	var by := birth_year_of(String(v.get("birth", "")))
	if expect_year > 0 and by != expect_year:
		reasons.append("出生年与年级不符（%d 年级应为 %d 年，实为 %d 年）" % [grade, expect_year, by])
		fields.append("birth")

	var pref := expected_prefix(grade)
	var sid := String(v.get("student_id", ""))
	if pref != "" and sid.substr(0, 4) != pref:
		reasons.append("学号前缀与年级不符（应为 %s，实为 %s）" % [pref, sid.substr(0, 4)])
		fields.append("id")

	if v.has("campus_card") and v.get("campus_card") != null:
		var cc: Dictionary = v.get("campus_card", {})
		if not bool(cc.get("valid", true)):
			reasons.append("校园卡状态异常（无效卡）")
			fields.append("campus_card")

	if v.has("temp_pass") and v.get("temp_pass") != null:
		var tp: Dictionary = v.get("temp_pass", {})
		if String(tp.get("valid_until", "")) < today:
			reasons.append("临时通行证已过期（%s）" % String(tp.get("valid_until", "")))
			fields.append("temp_pass")

	if v.has("security_pass") and v.get("security_pass") != null:
		var sp: Dictionary = v.get("security_pass", {})
		if String(sp.get("purpose", "")).strip_edges() == "":
			reasons.append("纪检部准入证未注明来意")
			fields.append("security_pass")

	if bool(ctx.get("enforce_transfer_checks", false)) and String(v.get("purpose", "")) == "转学":
		if not bool(ctx.get("called", false)):
			reasons.append("转学未向转出学校电话核实")
			fields.append("transfer_letter")
		if not bool(ctx.get("db_checked", false)):
			reasons.append("转学未查询教育局档案")
			fields.append("transfer_letter")

	if v.has("transfer_letter") and v.get("transfer_letter") != null:
		var tl: Dictionary = v.get("transfer_letter", {})
		var principals: Dictionary = ctx.get("principals", {})
		var from_school := String(tl.get("from_school", ""))
		var to_school := String(tl.get("to_school", ""))
		var expect_from := String(principals.get(from_school, ""))
		var expect_to := String(principals.get(to_school, ""))
		if expect_from != "" and String(tl.get("sig_from", "")) != expect_from:
			reasons.append("介绍信转出教导主任签名不符（应为%s，实为%s）" % [expect_from, String(tl.get("sig_from", ""))])
			fields.append("transfer_letter")
		if expect_to != "" and String(tl.get("sig_to", "")) != expect_to:
			reasons.append("介绍信转入教导主任签名不符（应为%s）" % expect_to)
			fields.append("transfer_letter")
		var variant := String(tl.get("variant_from", "genuine"))
		if variant == "miss":
			reasons.append("介绍信签名缺笔（笔画断裂）")
			fields.append("transfer_letter")
		elif variant == "light":
			reasons.append("介绍信签名墨色偏灰，网点稀疏")
			fields.append("transfer_letter")
		elif variant == "mirror":
			reasons.append("介绍信签名为镜像翻拍")
			fields.append("transfer_letter")
		elif variant == "plain":
			reasons.append("介绍信签名无钢印压痕")
			fields.append("transfer_letter")
		elif bool(tl.get("forged", false)):
			reasons.append("介绍信签名异常")
			fields.append("transfer_letter")

	if v.has("health_cert") and v.get("health_cert") != null:
		var hc: Dictionary = v.get("health_cert", {})
		if String(hc.get("status", "")) != "健康":
			reasons.append("健康证明状态不合格（%s）" % String(hc.get("status", "")))
			fields.append("health_cert")
		if bool(hc.get("forged", false)):
			reasons.append("健康证明字段有篡改痕迹")
			fields.append("health_cert")

	return {"allow": reasons.is_empty(), "reasons": reasons, "fields": fields}

static func compare_hint(a: String, b: String, v: Dictionary, today: String) -> String:
	var pair := [a, b]
	pair.sort()
	var key := "%s|%s" % [String(pair[0]), String(pair[1])]
	var grade := int(v.get("grade", 0))
	if a == "photo" or b == "photo":
		var other := b if a == "photo" else a
		if other == "today" or other == "name" or other == "grade" or other == "school":
			return "对照证件照与本人：看五官比例、痣的位置、耳形。换脸的人对不上；镜像翻拍会左右颠倒，发型分缝也会反。"
		return "证件照只能和「本人」对照，或者和数据库里的存档照对照（查档案可看）。"
	match key:
		"birth|grade":
			var expect_year := expected_birth_year(grade)
			var by := birth_year_of(String(v.get("birth", "")))
			var ok := expect_year == by
			return "年级 %d 应出生于 %d 年，证件为 %d 年 → %s" % [grade, expect_year, by, "一致" if ok else "不符"]
		"grade|id":
			var pref := expected_prefix(grade)
			var sid := String(v.get("student_id", ""))
			return "年级 %d 的学号应以 %s 开头，证件为 %s → %s" % [grade, pref, sid.substr(0, 4), "一致" if sid.substr(0, 4) == pref else "不符"]
		"expiry|today":
			var exp := String(v.get("expiry", ""))
			return "有效期 %s 与今日 %s 相比 → %s" % [exp, today, "有效" if exp >= today else "已过期"]
		"birth|expiry":
			var by := birth_year_of(String(v.get("birth", "")))
			var exp_year := int(String(v.get("expiry", "0000")).substr(0, 4))
			var want := by + grade + 6
			return "出生 %d 年、%d 年级，学生证应到 %d 年 6 月；证件为 %d 年 → %s（相差 %d 年）" % [by, grade, want, exp_year, "吻合" if exp_year == want else "不符", absi(exp_year - want)]
		"expiry|grade":
			var by2 := birth_year_of(String(v.get("birth", "")))
			var exp2 := int(String(v.get("expiry", "0000")).substr(0, 4))
			var want2 := by2 + grade + 6
			return "%d 年级应在 %d 年毕业，有效期到 %d 年 → %s" % [grade, want2, exp2, "吻合" if exp2 == want2 else "不符"]
		"expiry|student_id":
			var exp3 := int(String(v.get("expiry", "0000")).substr(0, 4))
			var pref3 := int(String(v.get("student_id", "0000")).substr(0, 4))
			return "学号前缀 %d + 年级 %d → 有效期应为 %d 年，证件为 %d 年 → %s" % [pref3, grade, pref3 + grade - 6, exp3, "吻合" if exp3 == pref3 + grade - 6 else "不符"]
		"birth|student_id":
			var by3 := birth_year_of(String(v.get("birth", "")))
			var pref4 := int(String(v.get("student_id", "0000")).substr(0, 4))
			return "出生 %d 年 + 12 年入学 → 学号应为 %d 开头，证件为 %d → %s" % [by3, by3 + 12, pref4, "吻合" if pref4 == by3 + 12 else "不符"]
		"birth|today":
			var by4 := birth_year_of(String(v.get("birth", "")))
			var ty := int(today.substr(0, 4))
			var age := ty - by4
			return "出生 %d 年，今日 %d 年 → 实岁约 %d 岁；%d 年级应在 %d~%d 岁" % [by4, ty, age, grade, grade + 5, grade + 7]
		"birth|id":
			return "出生年与学号前缀无直接换算关系，需分别对照年级表"
		"name|photo":
			return "姓名无法与照片直接比对，请用放大镜核对五官与痣"
		"photo|school":
			return "照片与学校无直接关系，可用于确认校服领型"
		"name|school":
			return "姓名与学校无直接关系"
		"id|name":
			return "学号不包含姓名信息，需通过教育局档案核实"
	return "该两项无法直接比对，需人工判断"
