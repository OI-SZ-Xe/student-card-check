# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''		v["campus_card"] = {"valid": rng.randf() > 0.16}''', '''		v["campus_card"] = {
			"valid": rng.randf() > 0.16,
			"card_no": "C" + String(sid).substr(4),
			"valid_until": expiry
		}''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''		cards.append(["校园卡", [["卡号", "见卡面"], ["状态", "正常 / 异常"], ["有效期", "本学期末"]]])''', '''		var cc: Dictionary = docs["campus_card"]
		cards.append(["校园卡", [["卡号", String(cc.get("card_no", ""))], ["状态", "正常" if bool(cc.get("valid", true)) else "已挂失"], ["有效期", String(cc.get("valid_until", ""))]]])''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("real campus data")
