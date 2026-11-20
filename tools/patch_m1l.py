# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\tests\run_tests.gd"
s = io.open(p, encoding="utf-8").read()
old = '''	v["transfer_letter"] = {
		"from_school": "深圳实验中学",
		"to_school": "深圳实验中学",
		"sig_from": "王明",
		"sig_to": "王明",
		"forged": true
	}
	var res2 := RuleEngine.evaluate(v, "2026-03-01", make_ctx())
	ok(not bool(res2.get("allow", true)), "forged letter rejected")
	ok(has_reason(res2, "钢印"), "forged letter reason")'''
new = '''	v["transfer_letter"] = {
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
	ok(has_reason(res5, "墨色"), "light ink reason")'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("tests updated")
