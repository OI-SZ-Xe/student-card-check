# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\Main.gd"
s = io.open(p, encoding="utf-8").read()
old = '''	if _shot_path != "":
		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			add_child(_intro)'''
new = '''	if _shot_path != "":
		if _shot_mode == "register":
			var reg_shot := preload("res://scripts/ui/Register.gd").new()
			add_child(reg_shot)
			await get_tree().create_timer(1.0).timeout
			await RenderingServer.frame_post_draw
			var reg_img := get_viewport().get_texture().get_image()
			reg_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			_intro.player_name = "周予安"
			_intro.player_class = "八年级（2）班"
			add_child(_intro)'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("shot modes updated")
