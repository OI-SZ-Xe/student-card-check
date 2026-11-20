# -*- coding: utf-8 -*-
import io

p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()

old_draw = '''\tfunc _draw() -> void:
\t\tvar w := size.x
\t\tvar h := size.y
\t\tdraw_circle(Vector2(w * 0.5, h * 0.15), w * 0.19, body_color)
\t\tvar pts := PackedVector2Array([
\t\t\tVector2(w * 0.5 - w * 0.19, h * 0.22),
\t\t\tVector2(w * 0.5 + w * 0.19, h * 0.22),
\t\t\tVector2(w * 0.5 + w * 0.44, h * 1.0),
\t\t\tVector2(w * 0.5 - w * 0.44, h * 1.0)
\t\t])
\t\tdraw_colored_polygon(pts, body_color)
\t\tif hat:
\t\t\tdraw_rect(Rect2(w * 0.30, h * 0.02, w * 0.40, h * 0.06), body_color)'''
new_draw = '''\tfunc _draw() -> void:
\t\tvar w := size.x
\t\tvar h := size.y
\t\tdraw_circle(Vector2(w * 0.5, h * 0.10), w * 0.115, body_color)
\t\tdraw_rect(Rect2(w * 0.44, h * 0.17, w * 0.12, h * 0.07), body_color)
\t\tvar torso := PackedVector2Array([
\t\t\tVector2(w * 0.26, h * 0.24),
\t\t\tVector2(w * 0.74, h * 0.24),
\t\t\tVector2(w * 0.70, h * 0.62),
\t\t\tVector2(w * 0.30, h * 0.62)
\t\t])
\t\tdraw_colored_polygon(torso, body_color)
\t\tdraw_rect(Rect2(w * 0.17, h * 0.25, w * 0.10, h * 0.34), body_color)
\t\tdraw_rect(Rect2(w * 0.73, h * 0.25, w * 0.10, h * 0.34), body_color)
\t\tdraw_rect(Rect2(w * 0.32, h * 0.60, w * 0.14, h * 0.40), body_color)
\t\tdraw_rect(Rect2(w * 0.54, h * 0.60, w * 0.14, h * 0.40), body_color)
\t\tif hat:
\t\t\tdraw_rect(Rect2(w * 0.34, h * 0.02, w * 0.32, h * 0.05), body_color)'''
assert old_draw in s, "silhouette draw missing"
s = s.replace(old_draw, new_draw)

# gate before booth
old_add = '''\tvar ground := ColorRect.new()'''
new_add = '''\t_build_gate()

	var ground := ColorRect.new()'''
assert old_add in s
s = s.replace(old_add, new_add, 1)

# add _build_gate function before _build_skyline
anchor = "func _build_skyline() -> void:"
gate_fn = '''func _build_gate() -> void:
	var g := Control.new()
	g.position = Vector2(1010, 150)
	g.size = Vector2(840, 580)
	add_child(g)
	var left := ColorRect.new()
	left.color = Color(0.13, 0.15, 0.12)
	left.position = Vector2(0, 90)
	left.size = Vector2(30, 490)
	g.add_child(left)
	var right := ColorRect.new()
	right.color = Color(0.13, 0.15, 0.12)
	right.position = Vector2(810, 90)
	right.size = Vector2(30, 490)
	g.add_child(right)
	var beam := ColorRect.new()
	beam.color = Color(0.13, 0.15, 0.12)
	beam.position = Vector2(0, 60)
	beam.size = Vector2(840, 34)
	g.add_child(beam)
	var sign := Ui.label("深 圳 实 验 中 学", 30, Color(0.55, 0.58, 0.46), Ui.font_serif())
	sign.position = Vector2(0, 10)
	sign.size = Vector2(840, 40)
	sign.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	g.add_child(sign)

'''
s = s.replace(anchor, gate_fn + anchor, 1)

# sequence: four items, then swearing after stamp
s = s.replace('\tvar items := ["笔试", "面试", "政审", "体检", "宣誓"]',
              '\tvar items := ["笔试", "面试", "政审", "体检"]')
old_tail = '''\tawait _say("你已通过前四项。第五项，现在开始。", 0.2)
\tif _skip or _ended: return
\t_caption.text = ""'''
new_tail = '''\tawait _say("你已通过前四项。第五项，现在开始。", 0.2)
\tif _skip or _ended: return
\tvar last_row := HBoxContainer.new()
\tlast_row.add_theme_constant_override("separation", 18)
\tvar last_mark := Ui.label("■", 24, Color(Ui.RED), Ui.font_mono())
\tvar last_name := Ui.label("宣誓", 24, Color("#d8d2b8"), Ui.font_serif())
\tvar last_state := Ui.label("通过", 18, Color(0.75, 0.55, 0.25), Ui.font_mono())
\tlast_row.add_child(last_mark)
\tlast_row.add_child(last_name)
\tlast_row.add_child(last_state)
\t_list.add_child(last_row)
\tSfx.play("click", -16.0)
\t_caption.text = ""'''
assert old_tail in s
s = s.replace(old_tail, new_tail)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# --- card stamp size ---
c = r"F:\请出示学生证\scripts\ui\CardView.gd"
t = io.open(c, encoding="utf-8").read()
t = t.replace("\t_stamp_frame.position = Vector2(96, 168)\n\t_stamp_frame.size = Vector2(368, 96)\n\t_stamp_frame.rotation = -0.14",
              "\t_stamp_frame.position = Vector2(150, 210)\n\t_stamp_frame.size = Vector2(280, 84)\n\t_stamp_frame.rotation = -0.21")
t = t.replace('\t_stamp = Ui.label("", 46, Ui.RED, Ui.font_serif())\n\t_stamp.position = Vector2(0, 16)\n\t_stamp.size = Vector2(368, 64)',
              '\t_stamp = Ui.label("", 38, Ui.RED, Ui.font_serif())\n\t_stamp.position = Vector2(0, 14)\n\t_stamp.size = Vector2(280, 56)')
io.open(c, "w", encoding="utf-8", newline="\n").write(t)
print("patched round 6")
