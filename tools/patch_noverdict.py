# -*- coding: utf-8 -*-
import io
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
f = f.replace('''			"card_no": "C" + String(sid).substr(4),''', '''			"card_no": "C" + String(sid).substr(4),
			"holder": nm,''')
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)

p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''		cards.append(["校园卡", [["卡号", String(cc.get("card_no", ""))], ["状态", "正常" if bool(cc.get("valid", true)) else "已挂失"], ["有效期", String(cc.get("valid_until", ""))]]])''', '''		cards.append(["校园卡", [["卡号", String(cc.get("card_no", ""))], ["持卡人", String(cc.get("holder", ""))], ["有效期", String(cc.get("valid_until", ""))]]])''')
s = s.replace('''		cards.append(["临时通行证", [["有效期至", until], ["状态", "有效" if until >= today else "已过期"]]])''', '''		cards.append(["临时通行证", [["有效期至", until], ["签发", "校门卫"]]])''')
s = s.replace('''		var sig_ok := String(tl.get("variant_from", "genuine")) == "genuine" and not bool(tl.get("forged", false))
		cards.append(["转学介绍信", [["转出", String(tl.get("from_school", ""))], ["转入", String(tl.get("to_school", ""))], ["转出签名", "正常" if sig_ok else "异常（见原件）"]]])''', '''		cards.append(["转学介绍信", [["转出", String(tl.get("from_school", ""))], ["转入", String(tl.get("to_school", ""))], ["签名", "见原件（L 键）"]]])''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("no verdicts on cards")
