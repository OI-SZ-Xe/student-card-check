# -*- coding: utf-8 -*-
import io

# 1) Ui: shadows for panels, no-AA fonts
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
u = u.replace('''static func panel(bg: Color, border: Color = Color(0, 0, 0, 0), bw: int = 2, radius: int = 2, pad: int = 10) -> Panel:
	var p := Panel.new()
	p.add_theme_stylebox_override("panel", style(bg, border, bw, radius, pad))
	return p''', '''static func panel(bg: Color, border: Color = Color(0, 0, 0, 0), bw: int = 2, radius: int = 2, pad: int = 10) -> Panel:
	var p := Panel.new()
	var sb := style(bg, border, bw, radius, pad)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(2, 3)
	p.add_theme_stylebox_override("panel", sb)
	return p''')
for fn in ["font_ui", "font_serif", "font_mono"]:
    pass
u = u.replace('\t\tf.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"])',
              '\t\tf.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"])\n\t\tf.antialiasing = TextServer.FONT_ANTIALIASING_NONE')
u = u.replace('\t\tf.font_names = PackedStringArray(["SimSun", "Songti SC", "Noto Serif CJK SC", "serif"])',
              '\t\tf.font_names = PackedStringArray(["SimSun", "Songti SC", "Noto Serif CJK SC", "serif"])\n\t\tf.antialiasing = TextServer.FONT_ANTIALIASING_NONE')
u = u.replace('\t\tf.font_names = PackedStringArray(["Consolas", "Courier New", "Noto Sans Mono CJK SC", "monospace"])',
              '\t\tf.font_names = PackedStringArray(["Consolas", "Courier New", "Noto Sans Mono CJK SC", "monospace"])\n\t\tf.antialiasing = TextServer.FONT_ANTIALIASING_NONE')
io.open(up, "w", encoding="utf-8", newline="\n").write(u)

# 2) Desk: window frame + icons
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	var lamp := Ui.label("●", 20, Color(0.6, 0.75, 0.5, 0.8), Ui.font_mono())
	lamp.position = Vector2(748, 14)
	lamp.size = Vector2(30, 26)
	glass.add_child(lamp)''', '''	var lamp := Ui.label("●", 20, Color(0.6, 0.75, 0.5, 0.8), Ui.font_mono())
	lamp.position = Vector2(748, 14)
	lamp.size = Vector2(30, 26)
	glass.add_child(lamp)

	var frame_col := Color("#39443c")
	for r in [Rect2(0, 0, 792, 12), Rect2(0, 360, 792, 12), Rect2(0, 0, 12, 372), Rect2(780, 0, 12, 372)]:
		var bar := ColorRect.new()
		bar.color = frame_col
		bar.position = r.position
		bar.size = r.size
		glass.add_child(bar)
	var mullion := ColorRect.new()
	mullion.color = frame_col
	mullion.position = Vector2(282, 12)
	mullion.size = Vector2(6, 348)
	glass.add_child(mullion)
	var transom := ColorRect.new()
	transom.color = frame_col
	transom.position = Vector2(12, 268)
	transom.size = Vector2(768, 6)
	glass.add_child(transom)
	var plate := Ui.label("检 查 站　07", 13, Color("#8d9a86"), Ui.font_serif())
	plate.position = Vector2(320, 286)
	plate.size = Vector2(200, 20)
	glass.add_child(plate)
	for i in 5:
		var dot := ColorRect.new()
		dot.color = Color(0.55, 0.6, 0.5, 0.35)
		dot.position = Vector2(700 + i * 10, 322)
		dot.size = Vector2(4, 10)
		glass.add_child(dot)
	var reflection := ColorRect.new()
	reflection.color = Color(1, 1, 1, 0.045)
	reflection.position = Vector2(60, 20)
	reflection.size = Vector2(120, 340)
	reflection.rotation = -0.18
	glass.add_child(reflection)''')

# icon helper + apply
if "func _icon_button(" not in d:
    d += '''

func _icon_button(btn: Button, icon_name: String) -> void:
	var path := "res://art/icons/%s.png" % icon_name
	if ResourceLoader.exists(path):
		btn.icon = load(path)
		btn.expand_icon = false
		btn.add_theme_constant_override("icon_max_width", 22)
'''
d = d.replace('''	_compare_btn.pressed.connect(_toggle_compare)''', '''	_icon_button(_compare_btn, "compare")
	_compare_btn.pressed.connect(_toggle_compare)''')
d = d.replace('''	_magnify_btn.pressed.connect(_use_magnifier)''', '''	_icon_button(_magnify_btn, "magnifier")
	_magnify_btn.pressed.connect(_use_magnifier)''')
d = d.replace('''	_uv_btn.pressed.connect(_use_uv)''', '''	_icon_button(_uv_btn, "uv")
	_uv_btn.pressed.connect(_use_uv)''')
d = d.replace('''	phone.pressed.connect(_open_phone)''', '''	_icon_button(phone, "phone")
	phone.pressed.connect(_open_phone)''')
d = d.replace('''	manual_btn.pressed.connect(_open_manual)''', '''	_icon_button(manual_btn, "book")
	manual_btn.pressed.connect(_open_manual)''')
d = d.replace('''	shop_btn.pressed.connect(_open_shop)''', '''	_icon_button(shop_btn, "shop")
	shop_btn.pressed.connect(_open_shop)''')
d = d.replace('''	arrest_btn.pressed.connect(_arrest)''', '''	_icon_button(arrest_btn, "arrest")
	arrest_btn.pressed.connect(_arrest)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("F: window frame, icons, shadows, no-AA")
