# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\t_boot()\n", "")
# cut _boot function entirely
start = s.find("func _boot() -> void:")
if start != -1:
    end = s.find("\nfunc ", start + 10)
    s = s[:start] + (s[end+1:] if end != -1 else "")
# replace _loading with inline bar (no overlay)
start = s.find("func _loading(")
if start != -1:
    end = s.find("\nfunc ", start + 10)
    s = s[:start] + (s[end+1:] if end != -1 else "")
s += '''

func _loading(text: String, seconds: float) -> void:
	var bar := ProgressBar.new()
	bar.custom_minimum_size = Vector2(600, 14)
	bar.max_value = 1.0
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.4), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(GREEN, Color(0, 0, 0, 0), 0, 0, 0))
	_body.add_child(_line(text, AMBER, 15))
	_body.add_child(bar)
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, seconds)
	await get_tree().create_timer(seconds, true).timeout
	if is_instance_valid(bar):
		bar.queue_free()
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("inline loading")
