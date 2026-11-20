# -*- coding: utf-8 -*-
import io
# soften emboss
p = r"F:\请出示学生证\tools\gen_signatures.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace('hi = alpha.filter(ImageFilter.MaxFilter(3)).point(lambda v: int(v * 0.35))', 'hi = alpha.filter(ImageFilter.MaxFilter(3)).point(lambda v: int(v * 0.18))')
s = s.replace('sh = alpha.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: int(v * 0.18))', 'sh = alpha.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: int(v * 0.10))')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# VisitorFactory: signature variants
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
old = '''		var from_school := String(sch.get("name", ""))
		var expect_from := String(principals.get(from_school, ""))
		var sig_from := expect_from
		var sig_to := String(principals.get("深圳实验中学", ""))
		var letter_forged := rng.randf() < 0.30
		var defect := ""
		if letter_forged:
			if rng.randf() < 0.55:
				var other: Array = []
				for k in principals.keys():
					if String(k) != from_school:
						other.append(String(principals[k]))
				if other.size() > 0:
					sig_from = String(other[rng.randi() % other.size()])
					defect = "wrong_signature"
				else:
					defect = "no_emboss"
			else:
				defect = "no_emboss"
			forged.append("transfer_letter")
		v["transfer_letter"] = {
			"from_school": from_school,
			"to_school": "深圳实验中学",
			"sig_from": sig_from,
			"sig_to": sig_to,
			"forged": letter_forged and defect == "no_emboss",
			"defect": defect
		}'''
new = '''		var from_school := String(sch.get("name", ""))
		var from_sig := String(sch.get("sig", ""))
		var expect_from := String(principals.get(from_school, ""))
		var sig_from := expect_from
		var sig_to := String(principals.get("深圳实验中学", ""))
		var to_sig := "wang_ming"
		var letter_forged := rng.randf() < 0.32
		var variant_from := "genuine"
		var variant_to := "genuine"
		var defect := ""
		if letter_forged:
			if rng.randf() < 0.28:
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
		}'''
assert old in f
f = f.replace(old, new)
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)
print("factory patched")
