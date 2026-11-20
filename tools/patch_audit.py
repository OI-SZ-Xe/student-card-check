# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
start = s.find("	var cards: Array = []")
end = s.find("	var i := 0\n	for item in cards:")
new = '''	var cards: Array = []
	var today := State.date
	if docs.has("campus_card") and not bool(docs["campus_card"].get("missing", false)):
		var cc: Dictionary = docs["campus_card"]
		cards.append(["校园卡", [["卡号", String(cc.get("card_no", ""))], ["状态", "正常" if bool(cc.get("valid", true)) else "已挂失"], ["有效期", String(cc.get("valid_until", ""))]]])
	if docs.has("temp_pass") and not bool(docs["temp_pass"].get("missing", false)):
		var tp: Dictionary = docs["temp_pass"]
		var until := String(tp.get("valid_until", ""))
		cards.append(["临时通行证", [["有效期至", until], ["状态", "有效" if until >= today else "已过期"]]])
	if docs.has("security_pass") and not bool(docs["security_pass"].get("missing", false)):
		var sp: Dictionary = docs["security_pass"]
		var purpose := String(sp.get("purpose", ""))
		cards.append(["纪检部准入证", [["来意", purpose if purpose != "" else "（空白）"]]])
	if docs.has("health_cert") and not bool(docs["health_cert"].get("missing", false)):
		var hc: Dictionary = docs["health_cert"]
		cards.append(["健康证明", [["结论", String(hc.get("status", ""))], ["盖章", "校医务室"]]])
	if docs.has("transfer_letter") and not bool(docs["transfer_letter"].get("missing", false)):
		var tl: Dictionary = docs["transfer_letter"]
		var sig_ok := String(tl.get("variant_from", "genuine")) == "genuine" and not bool(tl.get("forged", false))
		cards.append(["转学介绍信", [["转出", String(tl.get("from_school", ""))], ["转入", String(tl.get("to_school", ""))], ["转出签名", "正常" if sig_ok else "异常（见原件）"]]])
	for k3 in docs.keys():
		if bool(docs[k3].get("missing", false)):
			cards.append(["缺少材料", [["项目", k3], ["说明", "学生未提交"]]])
'''
s = s[:start] + new + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("docs logic audited")
