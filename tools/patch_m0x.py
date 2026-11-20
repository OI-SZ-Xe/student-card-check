# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(p, encoding="utf-8").read()

old = '''	_f = {
		"face": rng.randf_range(0.94, 1.06),
		"jaw": rng.randf_range(0.50, 0.70),'''
new = '''	var shape := rng.randi_range(0, 2)
	var jaw_default := [0.52, 0.60, 0.68][shape]
	_f = {
		"shape": shape,
		"head_scale": rng.randf_range(0.93, 1.07),
		"eye_shape": rng.randi_range(0, 2),
		"brow_thick": rng.randf_range(0.85, 1.45),
		"nose_w": rng.randf_range(0.85, 1.20),
		"lip_full": rng.randf_range(0.85, 1.25),
		"face": rng.randf_range(0.94, 1.06),
		"jaw": clampf(jaw_default + rng.randf_range(-0.04, 0.04), 0.46, 0.72),'''
assert old in s
s = s.replace(old, new)

s = s.replace('\tvar rx: float = w * 0.200 * float(_f.get("face", 1.0))\n\tvar ry: float = h * 0.190',
              '\tvar rx: float = w * 0.200 * float(_f.get("face", 1.0)) * float(_f.get("head_scale", 1.0))\n\tvar ry: float = h * 0.190 * float(_f.get("head_scale", 1.0)) * (0.96 + 0.04 * float(_f.get("shape", 1)))')

# eye shape: height factor
s = s.replace('''		_ellipse(Vector2(ex, eye_y - h * 0.012), w * 0.038 * es, h * 0.016 * es, Color(skin.darkened(0.16), 0.45))
		_ellipse(Vector2(ex, eye_y), w * 0.034 * es, h * 0.018 * es, Color("#f6f1e6"))''',
'''		var eh: float = [0.017, 0.0135, 0.019][int(_f.get("eye_shape", 0))]
		_ellipse(Vector2(ex, eye_y - h * 0.012), w * 0.038 * es, h * 0.016 * es, Color(skin.darkened(0.16), 0.45))
		_ellipse(Vector2(ex, eye_y), w * 0.034 * es, h * eh * es, Color("#f6f1e6"))''')

# brow thickness
s = s.replace('draw_line(Vector2(ex - w * 0.034, by + tilt * h * 0.006 * s), Vector2(ex, by - h * 0.010 * float(_f.get("brow_arch", 0.5))), hair, maxf(1.6, w * 0.012))',
              'draw_line(Vector2(ex - w * 0.034, by + tilt * h * 0.006 * s), Vector2(ex, by - h * 0.010 * float(_f.get("brow_arch", 0.5))), hair, maxf(1.6, w * 0.012 * float(_f.get("brow_thick", 1.0))))')
s = s.replace('draw_line(Vector2(ex, by - h * 0.010 * float(_f.get("brow_arch", 0.5))), Vector2(ex + w * 0.032, by + h * 0.004 - tilt * h * 0.005 * s), hair, maxf(1.6, w * 0.012))',
              'draw_line(Vector2(ex, by - h * 0.010 * float(_f.get("brow_arch", 0.5))), Vector2(ex + w * 0.032, by + h * 0.004 - tilt * h * 0.005 * s), hair, maxf(1.6, w * 0.012 * float(_f.get("brow_thick", 1.0))))')

# mouth width by lip_full
s = s.replace('var mw: float = w * 0.034 * float(_f.get("mouth", 1.0))',
              'var mw: float = w * 0.036 * float(_f.get("mouth", 1.0)) * float(_f.get("lip_full", 1.0))')

# nose width
s = s.replace('draw_circle(Vector2(cx - w * 0.020, eye_y + h * 0.080), w * 0.0055, skin.darkened(0.34))',
              'draw_circle(Vector2(cx - w * 0.020 * float(_f.get("nose_w", 1.0)), eye_y + h * 0.080), w * 0.0055, skin.darkened(0.34))')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("portrait variety pass")
