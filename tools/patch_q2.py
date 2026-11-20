# -*- coding: utf-8 -*-
import io
rp = r"F:\请出示学生证\scripts\systems\RuleEngine.gd"
r = io.open(rp, encoding="utf-8").read()

# transfer requires phone + db when enforced
r = r.replace('''	if v.has("transfer_letter") and v.get("transfer_letter") != null:''', '''	if bool(ctx.get("enforce_transfer_checks", false)) and String(v.get("purpose", "")) == "转学":
		if not bool(ctx.get("called", false)):
			reasons.append("转学未向转出学校电话核实")
			fields.append("transfer_letter")
		if not bool(ctx.get("db_checked", false)):
			reasons.append("转学未查询教育局档案")
			fields.append("transfer_letter")

	if v.has("transfer_letter") and v.get("transfer_letter") != null:''')

# extra compare cases
r = r.replace('''		"birth|id":''', '''		"birth|expiry":
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
		"birth|id":''')
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "enforce_transfer_checks" not in d:
    d = d.replace('''	var ctx := {''', '''	var ctx := {
		"enforce_transfer_checks": true,
		"called": _called_this,
		"db_checked": _db_checked_this,''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("rule engine compare + transfer checks")
