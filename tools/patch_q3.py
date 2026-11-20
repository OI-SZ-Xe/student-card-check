# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	return {
		"required": Data.required_docs(State.day, _visitor),
		"doc_names": names,
		"principals": _principals,
		"check_photo": true
	}'''
new = '''	return {
		"required": Data.required_docs(State.day, _visitor),
		"doc_names": names,
		"principals": _principals,
		"check_photo": true,
		"enforce_transfer_checks": true,
		"called": _called_this,
		"db_checked": _db_checked_this
	}'''
assert old in d
d = d.replace(old, new)
if "var _called_this" not in d:
    d = d.replace("var _awaiting_next := false", "var _awaiting_next := false\nvar _called_this := false\nvar _db_checked_this := false")
    d = d.replace('''	_called_this = false''', '')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("ctx flags")
