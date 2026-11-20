# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s = io.open(p, encoding="utf-8").read()

s = s.replace('''func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP''', '''func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP''')

s = s.replace('''	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.07, 0.06)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)''', '''	var bg := ColorRect.new()
	bg.color = Color(0.04, 0.06, 0.05)
	bg.position = Vector2.ZERO
	bg.size = Vector2(1920, 1080)
	add_child(bg)''')

s = s.replace('''	var scan := ColorRect.new()
	scan.set_anchors_preset(Control.PRESET_FULL_RECT)
	scan.mouse_filter = Control.MOUSE_FILTER_IGNORE''', '''	var scan := ColorRect.new()
	scan.position = Vector2.ZERO
	scan.size = Vector2(1920, 1080)
	scan.mouse_filter = Control.MOUSE_FILTER_IGNORE''')

s = s.replace('''	_flash = ColorRect.new()
	_flash.color = Color(1, 0.95, 0.7, 0.0)
	_flash.set_anchors_preset(Control.PRESET_FULL_RECT)''', '''	_flash = ColorRect.new()
	_flash.color = Color(1, 0.95, 0.7, 0.0)
	_flash.position = Vector2.ZERO
	_flash.size = Vector2(1920, 1080)''')

# actor look: muted, more mass
s = s.replace('var c := Color(0.86, 0.90, 0.86, 0.92)', 'var c := Color(0.62, 0.68, 0.60, 0.95)')
s = s.replace('''		draw_colored_polygon(PackedVector2Array([
			Vector2(w * 0.30, h * 0.21), Vector2(w * 0.70, h * 0.21),
			Vector2(w * 0.66, h * 0.58), Vector2(w * 0.34, h * 0.58)
		]), c)''', '''		draw_colored_polygon(PackedVector2Array([
			Vector2(w * 0.24, h * 0.21), Vector2(w * 0.76, h * 0.21),
			Vector2(w * 0.72, h * 0.58), Vector2(w * 0.28, h * 0.58)
		]), c)
		draw_colored_polygon(PackedVector2Array([
			Vector2(w * 0.24, h * 0.23), Vector2(w * 0.72, h * 0.23),
			Vector2(w * 0.64, h * 0.44), Vector2(w * 0.30, h * 0.44)
		]), Color(0.52, 0.57, 0.50, 0.95))''')
s = s.replace('draw_line(Vector2(w * 0.42, h * 0.58), Vector2(w * 0.40 + swing, h * 0.94), c, w * 0.09)',
              'draw_line(Vector2(w * 0.43, h * 0.58), Vector2(w * 0.40 + swing, h * 0.94), c, w * 0.13)')
s = s.replace('draw_line(Vector2(w * 0.58, h * 0.58), Vector2(w * 0.60 - swing, h * 0.94), c, w * 0.09)',
              'draw_line(Vector2(w * 0.57, h * 0.58), Vector2(w * 0.60 - swing, h * 0.94), c, w * 0.13)')
s = s.replace('draw_line(Vector2(w * 0.32, h * 0.26), Vector2(w * 0.16 - swing * 0.6, h * 0.50), c, w * 0.075)',
              'draw_line(Vector2(w * 0.28, h * 0.26), Vector2(w * 0.14 - swing * 0.6, h * 0.50), c, w * 0.11)')
s = s.replace('draw_line(Vector2(w * 0.68, h * 0.26), Vector2(w * 0.84 + swing * 0.6, h * 0.50), c, w * 0.075)',
              'draw_line(Vector2(w * 0.72, h * 0.26), Vector2(w * 0.86 + swing * 0.6, h * 0.50), c, w * 0.11)')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("school rush layout fixed")
