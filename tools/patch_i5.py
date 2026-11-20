# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('_bystanders.append(_make_actor("student", Vector2(600, 860), 88, 196))', '_bystanders.append(_make_actor("student", Vector2(600, 706), 88, 196))')
s = s.replace('_bystanders.append(_make_actor("student", Vector2(620, 850), 90, 200))', '_bystanders.append(_make_actor("student", Vector2(620, 700), 90, 200))')
s = s.replace('_bystanders.append(_make_actor("student", Vector2(560, 820), 90, 200))\n\t_bystanders.append(_make_actor("student", Vector2(700, 866), 96, 210))\n\t_bystanders.append(_make_actor("student", Vector2(420, 860), 88, 196))',
              '_bystanders.append(_make_actor("student", Vector2(560, 700), 90, 200))\n\t_bystanders.append(_make_actor("student", Vector2(700, 712), 96, 210))\n\t_bystanders.append(_make_actor("student", Vector2(420, 704), 88, 196))')
# night overlay for d19/d26
if "night_overlay" not in s:
    s = s.replace('''	_apply_scenario()''', '''	_apply_scenario()
	if scenario in ["d19", "d26"]:
		var night := ColorRect.new()
		night.name = "night_overlay"
		night.color = Color(0.01, 0.02, 0.02, 0.45)
		night.position = Vector2.ZERO
		night.size = Vector2(1920, 1080)
		night.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(night)
		move_child(night, get_child_count() - 1)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("positions + night overlay")
