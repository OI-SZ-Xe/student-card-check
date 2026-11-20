# -*- coding: utf-8 -*-
import io

# --- Portrait proportions ---
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\tvar head_y: float = h * 0.395\n\tvar rx: float = w * 0.180 * float(_f.get(\"face\", 1.0))\n\tvar ry: float = h * 0.222\n\tvar top: float = h * 0.705",
              "\tvar head_y: float = h * 0.385\n\tvar rx: float = w * 0.195 * float(_f.get(\"face\", 1.0))\n\tvar ry: float = h * 0.205\n\tvar top: float = h * 0.735")
old_collar = '''	var collar := PackedVector2Array([
		Vector2(cx - w * 0.115, top - h * 0.005),
		Vector2(cx - w * 0.02, top + h * 0.19),
		Vector2(cx, top + h * 0.15),
		Vector2(cx + w * 0.02, top + h * 0.19),
		Vector2(cx + w * 0.115, top - h * 0.005)
	])'''
new_collar = '''	var collar := PackedVector2Array([
		Vector2(cx - w * 0.100, top - h * 0.005),
		Vector2(cx - w * 0.014, top + h * 0.105),
		Vector2(cx, top + h * 0.088),
		Vector2(cx + w * 0.014, top + h * 0.105),
		Vector2(cx + w * 0.100, top - h * 0.005)
	])'''
assert old_collar in s
s = s.replace(old_collar, new_collar)
s = s.replace('''		draw_colored_polygon(PackedVector2Array([
			Vector2(cx - w * 0.022, top + h * 0.02),
			Vector2(cx + w * 0.022, top + h * 0.02),
			Vector2(cx + w * 0.012, top + h * 0.16),
			Vector2(cx, top + h * 0.19),
			Vector2(cx - w * 0.012, top + h * 0.16)
		]), Color("#8f2f22"))''', '''		draw_colored_polygon(PackedVector2Array([
			Vector2(cx - w * 0.020, top + h * 0.015),
			Vector2(cx + w * 0.020, top + h * 0.015),
			Vector2(cx + w * 0.010, top + h * 0.105),
			Vector2(cx, top + h * 0.128),
			Vector2(cx - w * 0.010, top + h * 0.105)
		]), Color("#8f2f22"))''')
s = s.replace("\tdraw_rect(Rect2(cx - w * 0.052, h * 0.54, w * 0.104, h * 0.20), skin.darkened(0.16))",
              "\tdraw_rect(Rect2(cx - w * 0.046, h * 0.545, w * 0.092, h * 0.19), skin.darkened(0.16))")
# hair: more volume, lower hairline
s = s.replace('''	for i in 15:
		var a: float = PI + PI * float(i) / 14.0
		hair_pts.append(Vector2(cx + cos(a) * rx * 1.07, head_y + sin(a) * ry * 1.05 - ry * 0.01))''', '''	for i in 15:
		var a: float = PI + PI * float(i) / 14.0
		hair_pts.append(Vector2(cx + cos(a) * rx * 1.12, head_y + sin(a) * ry * 1.14 - ry * 0.02))''')
s = s.replace('''	hair_pts.append(Vector2(cx + rx * 0.92, head_y - ry * 0.26))
	hair_pts.append(Vector2(cx + rx * 0.52, head_y - ry * 0.40))
	hair_pts.append(Vector2(cx + rx * 0.18 + part, head_y - ry * 0.50))
	hair_pts.append(Vector2(cx - rx * 0.28, head_y - ry * 0.47))
	hair_pts.append(Vector2(cx - rx * 0.68, head_y - ry * 0.33))
	hair_pts.append(Vector2(cx - rx * 1.02, head_y - ry * 0.09))''', '''	hair_pts.append(Vector2(cx + rx * 0.94, head_y - ry * 0.16))
	hair_pts.append(Vector2(cx + rx * 0.54, head_y - ry * 0.30))
	hair_pts.append(Vector2(cx + rx * 0.18 + part, head_y - ry * 0.38))
	hair_pts.append(Vector2(cx - rx * 0.28, head_y - ry * 0.35))
	hair_pts.append(Vector2(cx - rx * 0.70, head_y - ry * 0.24))
	hair_pts.append(Vector2(cx - rx * 1.04, head_y - ry * 0.02))''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# --- Main: portrait test grid ---
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
old = '''		if _shot_mode == "afterintro":'''
new = '''		if _shot_mode == "portraits":
			var grid := Control.new()
			grid.size = Vector2(1920, 1080)
			add_child(grid)
			var bgp := ColorRect.new()
			bgp.color = Color(0.10, 0.11, 0.10)
			bgp.size = Vector2(1920, 1080)
			grid.add_child(bgp)
			for i in 8:
				var pr := Portrait.new()
				pr.setup(1000 + i * 37, false, false)
				pr.position = Vector2(120 + (i % 4) * 440, 150 + (i / 4) * 400)
				pr.size = Vector2(240, 320)
				grid.add_child(pr)
				var pr2 := Portrait.new()
				pr2.setup(1000 + i * 37, true, false)
				pr2.position = Vector2(380 + (i % 4) * 440, 150 + (i / 4) * 400)
				pr2.size = Vector2(160, 200)
				grid.add_child(pr2)
			await get_tree().create_timer(0.8).timeout
			await RenderingServer.frame_post_draw
			var pi_img := get_viewport().get_texture().get_image()
			pi_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "afterintro":'''
assert old in m
m = m.replace(old, new)
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("portrait tweaks + test mode")
