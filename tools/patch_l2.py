# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\project.godot"
s = io.open(p, encoding="utf-8").read()
if "Music=" not in s:
    s = s.replace('Meta="*res://scripts/autoload/Meta.gd"', 'Meta="*res://scripts/autoload/Meta.gd"\nMusic="*res://scripts/autoload/Music.gd"')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "Music.play" not in d:
    d = d.replace('''	_build()
	State.start_day()''', '''	_build()
	State.start_day()
	Music.play("bgm_day", 2.0)
	Music.ambience("amb_rain" if State.day % 5 == 0 else "amb_room")''')
    d = d.replace('''	State.add_suspicion(susp)
	if sc == "d30":''', '''	State.add_suspicion(susp)
	Music.play("bgm_day", 1.0)
	if sc == "d30":''')
    d = d.replace('''	_paused = true
	_ending_active = true''', '''	_paused = true
	_ending_active = true
	Music.play("amb_room", 2.0, -20.0)
	Music.ambience("", 1.0)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

sp = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s2 = io.open(sp, encoding="utf-8").read()
if "Music.play" not in s2:
    s2 = s2.replace('''	_apply_scenario()''', '''	Music.play("bgm_tense", 0.4)
	_apply_scenario()''')
    s2 = s2.replace('''func _resolve() -> void:''', '''func _resolve() -> void:
	Music.play("bgm_day", 1.5)''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s2)
print("music wired")
