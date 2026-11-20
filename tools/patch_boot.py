# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''			await _loading("正在打开 %s ……" % String(s[1]), 1.8)''', '''			await _loading("正在打开 %s ……" % String(s[1]), 1.0)''')
if "_boot()" not in s:
    s = s.replace('''func _ready() -> void:''', '''func _ready() -> void:
	_boot()''')
    s += '''

func _boot() -> void:
	var layer := Control.new()
	layer.z_index = 60
	layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(layer)
	var dim := ColorRect.new()
	dim.color = Color(0.01, 0.03, 0.02, 0.96)
	dim.size = Vector2(1920, 1080)
	layer.add_child(dim)
	var box := Ui.panel(Color("#08120c"), Color("#2e5a3a"), 2, 2, 26)
	box.position = Vector2(560, 420)
	box.size = Vector2(800, 240)
	layer.add_child(box)
	var t := Ui.label("教育局办公系统 v3.1", 26, GREEN, Ui.font_mono())
	t.position = Vector2(28, 24)
	t.size = Vector2(700, 34)
	box.add_child(t)
	var l := Ui.label("正在连接校园内网 …… 正在校验终端证书 ……", 14, DIM, Ui.font_mono())
	l.position = Vector2(28, 70)
	l.size = Vector2(740, 20)
	box.add_child(l)
	var bar := ProgressBar.new()
	bar.position = Vector2(28, 108)
	bar.size = Vector2(744, 16)
	bar.max_value = 1.0
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.6), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(GREEN, Color(0, 0, 0, 0), 0, 0, 0))
	box.add_child(bar)
	var tip := Ui.label("5 秒后进入，可点击跳过", 12, DIM, Ui.font_mono())
	tip.position = Vector2(28, 140)
	tip.size = Vector2(600, 18)
	box.add_child(tip)
	var skip := Ui.button("跳过", 14, Color("#12281a"), GREEN)
	skip.position = Vector2(660, 168)
	skip.size = Vector2(110, 36)
	box.add_child(skip)
	var done := [false]
	var finish := func() -> void:
		if done[0]:
			return
		done[0] = true
		layer.queue_free()
	skip.pressed.connect(finish)
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, 5.0)
	await get_tree().create_timer(5.0).timeout
	finish.call()
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("terminal boot 5s")
