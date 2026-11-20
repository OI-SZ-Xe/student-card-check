# -*- coding: utf-8 -*-
import io, json

# --- VisitorFactory: clean wrong-principal selection (no Data access) ---
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
old = '''			if rng.randf() < 0.28:
				var other: Array = []
				for k in principals.keys():
					if String(k) != from_school:
						other.append(String(principals[k]))
				if other.size() > 0:
					sig_from = String(other[rng.randi() % other.size()])
					defect = "wrong_signature"
					if rng.randf() < 0.5:
						from_sig = String(Data.school(String(other[rng.randi() % other.size()])).get("sig", from_sig))
				else:
					defect = "no_emboss"'''
new = '''			if rng.randf() < 0.28:
				var others: Array = []
				for s2 in schools:
					if String(s2.get("name", "")) != from_school:
						others.append(s2)
				if others.size() > 0:
					var wrong: Dictionary = others[rng.randi() % others.size()]
					sig_from = String(wrong.get("principal", ""))
					from_sig = String(wrong.get("sig", from_sig))
					defect = "wrong_signature"
				else:
					defect = "no_emboss"'''
assert old in f
f = f.replace(old, new)
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)

# --- RuleEngine: variant-aware reasons ---
rp = r"F:\请出示学生证\scripts\systems\RuleEngine.gd"
r = io.open(rp, encoding="utf-8").read()
old2 = '''		if bool(tl.get("forged", false)):
			reasons.append("介绍信钢印缺失，压痕不连续")
			fields.append("transfer_letter")'''
new2 = '''		var variant := String(tl.get("variant_from", "genuine"))
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
			fields.append("transfer_letter")'''
assert old2 in r
r = r.replace(old2, new2)
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# --- manual.json: add forgery sample page ---
mp = r"F:\请出示学生证\data\manual.json"
manual = json.load(io.open(mp, encoding="utf-8-sig"))
page = {
    "title": "六 · 附 伪造签名对照",
    "type": "forgery",
    "note": "同一枚签名，四种毁法。紫外线下看压痕，放大镜下看墨色与网点；镜像要拿样本对照，人眼对字形方向很迟钝。"
}
idx = next(i for i, p in enumerate(manual) if p.get("title", "").startswith("六"))
if not any(p.get("type") == "forgery" for p in manual):
    manual.insert(idx + 1, page)
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(manual, ensure_ascii=False, indent=2))

print("factory/rule/manual patched")
