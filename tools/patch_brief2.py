# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
if "var _briefing_open" not in s:
    s = s.replace("var skip_briefing := false", "var skip_briefing := false\nvar _briefing_open := false")
s = s.replace('''func _show_briefing() -> void:
	_paused = true''', '''func _show_briefing() -> void:
	if _briefing_open:
		return
	_briefing_open = true
	_paused = true''')
s = s.replace('''func _on_briefing_closed(b: Briefing) -> void:
	if is_instance_valid(b):
		b.queue_free()
	_paused = false''', '''func _on_briefing_closed(b: Briefing) -> void:
	_briefing_open = false
	if is_instance_valid(b):
		b.queue_free()
	_paused = false''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("briefing reentry guard")
