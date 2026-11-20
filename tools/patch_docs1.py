# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
s = io.open(p, encoding="utf-8").read()
if "v[\"docs\"]" not in s:
    s = s.replace('''	v["forged_fields"] = forged''', '''	var docs := {
		"student_card": {
			"name": nm, "grade": grade, "birth": birth,
			"student_id": sid, "expiry": expiry,
			"school": String(sch.get("name", "")), "photo": photo
		}
	}
	for k in ["campus_card", "temp_pass", "security_pass", "transfer_letter", "health_cert"]:
		if v.has(k):
			docs[k] = v[k]
	v["docs"] = docs
	v["forged_fields"] = forged''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("docs packaged")
