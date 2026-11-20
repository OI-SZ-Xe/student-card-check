# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()

# wider silhouette body
old_body = '''\t\tvar pts := PackedVector2Array([
\t\t\tVector2(w * 0.5 - w * 0.17, h * 0.24),
\t\t\tVector2(w * 0.5 + w * 0.17, h * 0.24),
\t\t\tVector2(w * 0.5 + w * 0.30, h * 1.0),
\t\t\tVector2(w * 0.5 - w * 0.30, h * 1.0)
\t\t])'''
new_body = '''\t\tvar pts := PackedVector2Array([
\t\t\tVector2(w * 0.5 - w * 0.19, h * 0.22),
\t\t\tVector2(w * 0.5 + w * 0.19, h * 0.22),
\t\t\tVector2(w * 0.5 + w * 0.44, h * 1.0),
\t\t\tVector2(w * 0.5 - w * 0.44, h * 1.0)
\t\t])'''
assert old_body in s
s = s.replace(old_body, new_body)
s = s.replace('\t\tdraw_circle(Vector2(w * 0.5, h * 0.20), w * 0.17, body_color)',
              '\t\tdraw_circle(Vector2(w * 0.5, h * 0.15), w * 0.19, body_color)')

# caption centered
s = s.replace('\t_caption.position = Vector2(240, 830)\n\t_caption.size = Vector2(1440, 44)',
              '\t_caption.position = Vector2(240, 822)\n\t_caption.size = Vector2(1440, 48)\n\t_caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER')

# ground line + glow before booth
old_add = '''\t_booth = Control.new()'''
new_add = '''\tvar ground := ColorRect.new()
	ground.color = Color(0.16, 0.18, 0.14)
	ground.position = Vector2(0, 862)
	ground.size = Vector2(1920, 4)
	add_child(ground)

	var grad := Gradient.new()
	grad.set_color(0, Color(1.0, 0.85, 0.52, 0.30))
	grad.set_color(1, Color(1.0, 0.85, 0.52, 0.0))
	var gtex := GradientTexture2D.new()
	gtex.gradient = grad
	gtex.fill = GradientTexture2D.FILL_RADIAL
	gtex.fill_from = Vector2(0.5, 0.5)
	gtex.fill_to = Vector2(1.0, 0.5)
	gtex.width = 512
	gtex.height = 512
	var glow := TextureRect.new()
	glow.texture = gtex
	glow.position = Vector2(900, 250)
	glow.size = Vector2(960, 960)
	glow.stretch_mode = TextureRect.STRETCH_SCALE
	glow.modulate = Color(1, 1, 1, 0.55)
	add_child(glow)

	_booth = Control.new()'''
assert old_add in s
s = s.replace(old_add, new_add, 1)

# queue spacing
s = s.replace('\t\ts.position = Vector2(1320 + i * 16, 700)', '\t\ts.position = Vector2(1320 + i * 18, 690)')
s = s.replace('\t\tvar target := Vector2(240 + i * 96, 690 + (i % 2) * 6)', '\t\tvar target := Vector2(220 + i * 104, 676 + (i % 2) * 6)')
s = s.replace('\t\ts.setup(90, 170, cols[i % cols.size()], i == 2)', '\t\ts.setup(112, 196, cols[i % cols.size()], i == 2)')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("intro patched")
