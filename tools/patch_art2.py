# -*- coding: utf-8 -*-
import io
# softer CRT
cp = r"F:\请出示学生证\scripts\ui\CrtOverlay.gd"
c = io.open(cp, encoding="utf-8").read()
c = c.replace("float scan = 0.93 + 0.07 * sin(uv.y * 1180.0);", "float scan = 0.972 + 0.028 * sin(uv.y * 820.0);")
c = c.replace("c *= 1.0 - smoothstep(0.34, 0.94, d) * 0.36;", "c *= 1.0 - smoothstep(0.36, 0.96, d) * 0.30;")
c = c.replace("c += (n - 0.5) * 0.016;", "c += (n - 0.5) * 0.012;")
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

# bevel buttons
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
old = '''	b.add_theme_stylebox_override("normal", style(bg, bg.lightened(0.12), 1, 2, 9))
	b.add_theme_stylebox_override("hover", style(bg.lightened(0.08), bg.lightened(0.28), 1, 2, 9))
	b.add_theme_stylebox_override("pressed", style(bg.darkened(0.18), bg.lightened(0.2), 1, 2, 9))
	b.add_theme_stylebox_override("disabled", style(Color(bg, 0.30), Color(bg, 0.18), 1, 2, 9))'''
new = '''	var normal := style(bg, bg.lightened(0.22), 1, 0, 9)
	normal.shadow_color = Color(0, 0, 0, 0.45)
	normal.shadow_size = 2
	normal.shadow_offset = Vector2(1, 2)
	var hover := style(bg.lightened(0.10), bg.lightened(0.34), 1, 0, 9)
	hover.shadow_color = Color(0, 0, 0, 0.40)
	hover.shadow_size = 2
	hover.shadow_offset = Vector2(1, 2)
	var pressed := style(bg.darkened(0.22), bg.darkened(0.05), 1, 0, 9)
	var disabled := style(Color(bg, 0.35), Color(bg, 0.22), 1, 0, 9)
	b.add_theme_stylebox_override("normal", normal)
	b.add_theme_stylebox_override("hover", hover)
	b.add_theme_stylebox_override("pressed", pressed)
	b.add_theme_stylebox_override("disabled", disabled)'''
assert old in u
u = u.replace(old, new)
io.open(up, "w", encoding="utf-8", newline="\n").write(u)
print("crt softened + beveled buttons")
