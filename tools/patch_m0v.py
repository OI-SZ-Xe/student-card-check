# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(p, encoding="utf-8").read()

# long hair behind torso: move block before torso
hair_block = '''	# long hair behind
	if style == 4:
		draw_colored_polygon(_long_hair(cx, head_y, rx, ry, h), hair)
	if style == 3:
		draw_circle(Vector2(cx + rx * 0.92, head_y - ry * 0.55), w * 0.060, hair)

'''
assert hair_block in s
s = s.replace(hair_block, "")
marker = "\t# torso\n"
s = s.replace(marker, hair_block + marker, 1)

# narrower torso
s = s.replace("\tvar shoulder_w: float = w * 0.56", "\tvar shoulder_w: float = w * 0.42")
s = s.replace("Vector2(cx - shoulder_w * 1.25, h)", "Vector2(cx - shoulder_w * 1.18, h)")
s = s.replace("Vector2(cx + shoulder_w * 1.25, h)", "Vector2(cx + shoulder_w * 1.18, h)")

# bigger eyes
s = s.replace("_ellipse(Vector2(ex, eye_y), w * 0.031 * es, h * 0.016 * es, Color(\"#f4efe3\"))",
              "_ellipse(Vector2(ex, eye_y), w * 0.034 * es, h * 0.018 * es, Color(\"#f6f1e6\"))")
s = s.replace("draw_circle(Vector2(ex, eye_y), w * 0.0125 * es, Color(\"#3d2c1e\"))",
              "draw_circle(Vector2(ex, eye_y), w * 0.0138 * es, Color(\"#3a2a1c\"))")
s = s.replace("draw_circle(Vector2(ex, eye_y), w * 0.0055 * es, Color(\"#120d09\"))",
              "draw_circle(Vector2(ex, eye_y), w * 0.0062 * es, Color(\"#120d09\"))")

# softer mouth
s = s.replace("var mw: float = w * 0.042 * float(_f.get(\"mouth\", 1.0))",
              "var mw: float = w * 0.034 * float(_f.get(\"mouth\", 1.0))")
s = s.replace('draw_arc(Vector2(cx, my + h * 0.004), mw * 0.86, 0.22 * PI, 0.78 * PI, 16, lip, maxf(1.4, w * 0.008))',
              'draw_arc(Vector2(cx, my + h * 0.004), mw * 0.82, 0.25 * PI, 0.75 * PI, 16, lip, maxf(1.2, w * 0.006))')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("portrait pass 3")
