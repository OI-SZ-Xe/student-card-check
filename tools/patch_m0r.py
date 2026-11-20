# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()

# assessment paper tighter
s = s.replace('\tvar paper := _paper(Rect2(400, 110, 1120, 860))', '\tvar paper := _paper(Rect2(400, 150, 1120, 760))')
s = s.replace('\tfoot.position = Vector2(64, 720)', '\tfoot.position = Vector2(64, 566)')
s = s.replace('\tsig.position = Vector2(700, 700)', '\tsig.position = Vector2(690, 540)')
s = s.replace('\tsig_line.position = Vector2(720, 808)', '\tsig_line.position = Vector2(710, 648)')

# film frame helper + application
anchor = "func _shot_notice_header() -> void:"
helper = '''func _film_frame() -> void:
	var col := Color(0.86, 0.84, 0.72, 0.22)
	for yy in [74.0, 1002.0]:
		var bar := ColorRect.new()
		bar.color = col
		bar.position = Vector2(100, yy)
		bar.size = Vector2(1720, 3)
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_scene.add_child(bar)
	for i in 13:
		var y := 96.0 + float(i) * 70.0
		for xx in [62.0, 1838.0]:
			var hole := ColorRect.new()
			hole.color = Color(0.84, 0.82, 0.70, 0.14)
			hole.position = Vector2(xx, y)
			hole.size = Vector2(14, 30)
			hole.mouse_filter = Control.MOUSE_FILTER_IGNORE
			_scene.add_child(hole)

'''
s = s.replace(anchor, helper + anchor, 1)
s = s.replace('''	var leader_tag := Ui.label("纪检部学生指导短片", 22''', '''	_film_frame()
	var leader_tag := Ui.label("纪检部学生指导短片", 22''')
s = s.replace('''		var bg := ColorRect.new()
		bg.color = Color(0.08, 0.08, 0.075)
		bg.size = Vector2(1920, 1080)
		_scene.add_child(bg)''', '''		var bg := ColorRect.new()
		bg.color = Color(0.08, 0.08, 0.075)
		bg.size = Vector2(1920, 1080)
		_scene.add_child(bg)
		_film_frame()''')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# Main: afterintro shot mode
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
old = '''		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()'''
new = '''		if _shot_mode == "afterintro":
			_on_registered("周予安", "八年级（2）班")
			await get_tree().create_timer(0.6).timeout
			for c in get_children():
				if c is Intro:
					c._do_skip()
			await get_tree().create_timer(1.6).timeout
			await RenderingServer.frame_post_draw
			var ai_img := get_viewport().get_texture().get_image()
			ai_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()'''
assert old in m
m = m.replace(old, new)
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("intro layout + film frame + afterintro mode")
