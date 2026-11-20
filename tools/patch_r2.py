# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''func _query_archive(text: String) -> void:''', '''func _query_archive(text: String) -> void:
	var nm := String(visitor.get("name", ""))
	var sid := String(visitor.get("student_id", ""))
	if text.strip_edges() != "" and (text.strip_edges() == nm or text.strip_edges() == sid):
		State.db_checked_this = true''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("db flag")
