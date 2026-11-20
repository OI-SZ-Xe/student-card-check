# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
if "func _loading(" not in s:
    s += '''

func _loading(text: String, seconds: float) -> void:
	var layer := Control.new()
	layer.z_index = 50
	layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(layer)
	var dim := ColorRect.new()
	dim.color = Color(0.01, 0.03, 0.02, 0.88)
	dim.size = Vector2(1920, 1080)
	layer.add_child(dim)
	var box := Ui.panel(Color("#08120c"), Color("#2e5a3a"), 2, 2, 24)
	box.position = Vector2(660, 460)
	box.size = Vector2(600, 190)
	layer.add_child(box)
	var lab := Ui.label(text, 20, GREEN, Ui.font_mono())
	lab.position = Vector2(24, 26)
	lab.size = Vector2(552, 30)
	box.add_child(lab)
	var bar := ProgressBar.new()
	bar.position = Vector2(24, 84)
	bar.size = Vector2(552, 14)
	bar.max_value = 1.0
	bar.value = 0.0
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.5), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(GREEN, Color(0, 0, 0, 0), 0, 0, 0))
	box.add_child(bar)
	var hint := Ui.label("教育局内网 · 请稍候", 12, DIM, Ui.font_mono())
	hint.position = Vector2(24, 112)
	hint.size = Vector2(400, 18)
	box.add_child(hint)
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, seconds)
	await get_tree().create_timer(seconds).timeout
	layer.queue_free()
'''
    s = s.replace('''			_body.add_child(_line("正在打开 %s ……" % String(s[1]), AMBER, 16))
			await get_tree().create_timer(1.6).timeout
			_show(key)''', '''			await _loading("正在打开 %s ……" % String(s[1]), 1.8)
			_show(key)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("loading overlay")
