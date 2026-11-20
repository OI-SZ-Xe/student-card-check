# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(p, encoding="utf-8").read()
old = '\tdraw_colored_polygon(_face_points(cx, head_y, rx, ry, float(_f.get("jaw", 0.6))), skin)\n\t_ellipse(Vector2(cx, head_y + ry * 0.72), rx * 0.52, ry * 0.20, Color(skin.darkened(0.22), 0.18))'
new = '''\tdraw_colored_polygon(_face_points(cx, head_y, rx, ry, float(_f.get("jaw", 0.6))), skin)
	_ellipse(Vector2(cx - rx * 0.66, head_y + ry * 0.24), rx * 0.26, ry * 0.32, Color(skin.darkened(0.12), 0.30))
	_ellipse(Vector2(cx + rx * 0.66, head_y + ry * 0.24), rx * 0.26, ry * 0.32, Color(skin.darkened(0.12), 0.30))
	_ellipse(Vector2(cx, head_y + ry * 0.86), rx * 0.34, ry * 0.12, Color(skin.darkened(0.22), 0.35))
	_ellipse(Vector2(cx, head_y - ry * 0.46), rx * 0.38, ry * 0.20, Color(1, 1, 1, 0.05))
	_ellipse(Vector2(cx, head_y + ry * 0.30), rx * 0.78, ry * 0.50, Color(0, 0, 0, 0.04))'''
assert old in s
s = s.replace(old, new)

# eye socket shadow before sclera
old_eye = '''		# eye
		_ellipse(Vector2(ex, eye_y), w * 0.034 * es, h * 0.018 * es, Color("#f6f1e6"))'''
new_eye = '''		# eye
		_ellipse(Vector2(ex, eye_y - h * 0.012), w * 0.038 * es, h * 0.016 * es, Color(skin.darkened(0.16), 0.45))
		_ellipse(Vector2(ex, eye_y), w * 0.034 * es, h * 0.018 * es, Color("#f6f1e6"))'''
assert old_eye in s
s = s.replace(old_eye, new_eye)

# lip highlight
s = s.replace('draw_arc(Vector2(cx, my + h * 0.020), mw * 0.55, 0.20 * PI, 0.80 * PI, 14, Color(skin.darkened(0.18), 0.5), maxf(1.0, w * 0.005))',
              'draw_arc(Vector2(cx, my + h * 0.020), mw * 0.55, 0.20 * PI, 0.80 * PI, 14, Color(skin.darkened(0.18), 0.5), maxf(1.0, w * 0.005))\n\tdraw_arc(Vector2(cx, my + h * 0.014), mw * 0.70, 0.25 * PI, 0.75 * PI, 14, Color(1, 1, 1, 0.10), maxf(1.0, w * 0.004))')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("shading pass")
