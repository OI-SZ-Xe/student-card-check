# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
bad = '''func _query_archive(text: String) -> void:
	var nm := String(visitor.get("name", ""))
	var sid := String(visitor.get("student_id", ""))
	if text.strip_edges() != "" and (text.strip_edges() == nm or text.strip_edges() == sid):
		State.db_checked_this = true'''
if bad in s:
    s = s.replace(bad, "func _query_archive(text: String) -> void:")
s = s.replace('''func _site_archive() -> void:''', '''func _site_archive() -> void:
	State.db_checked_this = true''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("reverted, flag on open")
