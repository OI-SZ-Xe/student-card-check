# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:''', '''func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:''')
s = s.replace("State.time_left = max(0.0, State.time_left - delta)", "if not State.time_frozen:\n\t\tState.time_left = max(0.0, State.time_left - delta)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed dup input + freeze")
