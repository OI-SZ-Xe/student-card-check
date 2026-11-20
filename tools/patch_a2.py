# -*- coding: utf-8 -*-
import io

# VisitorFactory: deans
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
f = f.replace('var from_sig := String(sch.get("sig", ""))', 'var from_sig := String(sch.get("dean_sig", ""))')
f = f.replace('var sig_to := String(principals.get("深圳实验中学", ""))', 'var sig_to := String(principals.get("深圳实验中学", ""))')
f = f.replace('var to_sig := "wang_ming"', 'var to_sig := "dean_sy"')
f = f.replace('sig_from = String(wrong.get("principal", ""))', 'sig_from = String(wrong.get("dean", ""))')
f = f.replace('from_sig = String(wrong.get("sig", from_sig))', 'from_sig = String(wrong.get("dean_sig", from_sig))')
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)

# Desk: build deans map
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	for s in Data.schools:
		_principals[String(s.get("name", ""))] = String(s.get("principal", ""))'''
new = '''	for s in Data.schools:
		_principals[String(s.get("name", ""))] = String(s.get("dean", s.get("principal", "")))'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# RuleEngine wording
rp = r"F:\请出示学生证\scripts\systems\RuleEngine.gd"
r = io.open(rp, encoding="utf-8").read()
r = r.replace("介绍信转出校长签名不符（应为%s，实为%s）", "介绍信转出教导主任签名不符（应为%s，实为%s）")
r = r.replace("介绍信转入校长签名不符（应为%s）", "介绍信转入教导主任签名不符（应为%s）")
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# Manual: show deans alongside principals
mp = r"F:\请出示学生证\scripts\ui\Manual.gd"
m = io.open(mp, encoding="utf-8").read()
old2 = '''	for s in Data.schools:
		var sid := String(s.get("sig", ""))
		var data := Data.sig(sid)'''
new2 = '''	for s in Data.schools:
		for role in ["principal", "dean"]:
			var sig_key := "sig" if role == "principal" else "dean_sig"
			var name_key := "principal" if role == "principal" else "dean"
			var sid := String(s.get(sig_key, ""))
			var data := Data.sig(sid)'''
assert old2 in m
m = m.replace(old2, new2)
old3 = '''		var nm := Ui.label("%s　%s" % [String(data.get("name", "")), String(s.get("name", ""))], 18, Ui.INK, Ui.font_serif())'''
new3 = '''		var role_cn := "校长" if role == "principal" else "教导主任"
		var nm := Ui.label("%s　%s　%s" % [String(data.get("name", "")), role_cn, String(s.get("name", ""))], 18, Ui.INK, Ui.font_serif())'''
assert old3 in m
m = m.replace(old3, new3)
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("dean wiring done")
