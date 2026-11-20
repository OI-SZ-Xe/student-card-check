# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\Main.gd"
s = io.open(p, encoding="utf-8").read()
if "shot_delay" not in s:
    s = s.replace('var _shot_mode := "desk"', 'var _shot_mode := "desk"\nvar _shot_delay := -1.0')
    s = s.replace('''		elif arg.begins_with("--shot-mode="):
			_shot_mode = arg.substr(12)''', '''		elif arg.begins_with("--shot-mode="):
			_shot_mode = arg.substr(12)
		elif arg.begins_with("--shot-delay="):
			_shot_delay = float(arg.substr(13))''')
    s = s.replace('''		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			add_child(_intro)
			await get_tree().create_timer(7.5).timeout''', '''		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			add_child(_intro)
			await get_tree().create_timer(_shot_delay if _shot_delay > 0.0 else 7.5).timeout''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("delay arg added")
