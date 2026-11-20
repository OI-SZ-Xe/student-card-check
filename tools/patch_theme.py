# -*- coding: utf-8 -*-
import io

# phone prop position
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace("phone_prop.position = Vector2(352, 2)", "phone_prop.position = Vector2(252, 2)")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# native window size for crisp text
pp = r"F:\请出示学生证\project.godot"
p = io.open(pp, encoding="utf-8").read()
p = p.replace("window/size/window_width_override=1280", "window/size/window_width_override=1920")
p = p.replace("window/size/window_height_override=720", "window/size/window_height_override=1080")
if "stretch/scale_mode" not in p:
    p = p.replace('window/stretch/aspect="expand"', 'window/stretch/aspect="expand"\nwindow/stretch/scale_mode="integer"')
io.open(pp, "w", encoding="utf-8", newline="\n").write(p)

# App theme for controls
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
if "static func app_theme" not in u:
    u += '''

static func app_theme() -> Theme:
	var t := Theme.new()
	var mono := font_mono()
	var dark := Color("#0b120d")
	var edge := Color("#2e5a3a")
	t.set_stylebox("normal", "LineEdit", style(dark, edge, 1, 0, 8))
	t.set_stylebox("focus", "LineEdit", style(Color("#0e1711"), Color("#d9b45c"), 1, 0, 8))
	t.set_stylebox("read_only", "LineEdit", style(Color("#0a0f0b"), edge, 1, 0, 8))
	t.set_color("font_color", "LineEdit", Color("#9ad7a2"))
	t.set_color("font_placeholder_color", "LineEdit", Color(0.6, 0.72, 0.62, 0.55))
	t.set_color("caret_color", "LineEdit", Color("#d9b45c"))
	t.set_font("font", "LineEdit", mono)
	t.set_font_size("font_size", "LineEdit", 16)

	t.set_stylebox("normal", "OptionButton", style(dark, edge, 1, 0, 6))
	t.set_stylebox("hover", "OptionButton", style(Color("#102016"), Color("#d9b45c"), 1, 0, 6))
	t.set_stylebox("pressed", "OptionButton", style(Color("#102016"), Color("#d9b45c"), 1, 0, 6))
	t.set_stylebox("focus", "OptionButton", style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	t.set_color("font_color", "OptionButton", Color("#9ad7a2"))
	t.set_color("font_hover_color", "OptionButton", Color("#d9b45c"))
	t.set_font("font", "OptionButton", mono)
	t.set_font_size("font_size", "OptionButton", 15)

	t.set_stylebox("panel", "PopupMenu", style(Color("#0b120d"), edge, 1, 0, 6))
	t.set_stylebox("hover", "PopupMenu", style(Color("#13251a"), Color(0, 0, 0, 0), 0, 0, 6))
	t.set_color("font_color", "PopupMenu", Color("#9ad7a2"))
	t.set_color("font_hover_color", "PopupMenu", Color("#d9b45c"))
	t.set_font("font", "PopupMenu", mono)
	t.set_font_size("font_size", "PopupMenu", 15)

	for bar in ["VScrollBar", "HScrollBar"]:
		t.set_stylebox("scroll", bar, style(Color(0, 0, 0, 0.30), Color(0, 0, 0, 0), 0, 0, 0))
		t.set_stylebox("grabber", bar, style(Color("#3d5a44"), Color("#5a7a5e"), 1, 0, 0))
		t.set_stylebox("grabber_highlight", bar, style(Color("#4d6a54"), Color("#7a9a7e"), 1, 0, 0))
		t.set_stylebox("grabber_pressed", bar, style(Color("#2d4a34"), Color("#5a7a5e"), 1, 0, 0))
	return t
'''
io.open(up, "w", encoding="utf-8", newline="\n").write(u)

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "app_theme" not in m:
    m = m.replace("\tadd_child(CrtOverlay.new())", "\ttheme = Ui.app_theme()\n\tadd_child(CrtOverlay.new())")
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("theme + native window + phone fix")
