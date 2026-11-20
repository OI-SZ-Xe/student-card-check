# -*- coding: utf-8 -*-
import io, re
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
start = s.find("func _boot() -> void:")
if start != -1:
    end = s.find("\nfunc ", start + 10)
    if end == -1:
        end = len(s)
    s = s[:start] + s[end:]
s += '''

func _boot() -> void:
	var wait := 1.0 if State.has_upgrade("fastNet") else 5.0
	var layer := Control.new()
	layer.z_index = 60
	layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(layer)
	var dim := ColorRect.new()
	dim.color = Color(0.01, 0.03, 0.02, 0.97)
	dim.size = Vector2(1920, 1080)
	layer.add_child(dim)
	var box := Ui.panel(Color("#08120c"), Color("#2e5a3a"), 2, 2, 26)
	box.position = Vector2(560, 420)
	box.size = Vector2(800, 220)
	layer.add_child(box)
	var t := Ui.label("教育局办公系统 v3.1", 26, GREEN, Ui.font_mono())
	t.position = Vector2(28, 22)
	t.size = Vector2(700, 34)
	box.add_child(t)
	var l := Ui.label("正在连接校园内网 …… 正在校验终端证书 ……", 14, DIM, Ui.font_mono())
	l.position = Vector2(28, 68)
	l.size = Vector2(740, 20)
	box.add_child(l)
	var bar := ProgressBar.new()
	bar.position = Vector2(28, 104)
	bar.size = Vector2(744, 16)
	bar.max_value = 1.0
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.6), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(GREEN, Color(0, 0, 0, 0), 0, 0, 0))
	box.add_child(bar)
	var tip := Ui.label("正在加载，请稍候", 12, DIM, Ui.font_mono())
	tip.position = Vector2(28, 136)
	tip.size = Vector2(400, 18)
	box.add_child(tip)
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, wait)
	var timer := Timer.new()
	timer.one_shot = true
	timer.wait_time = wait
	add_child(timer)
	timer.timeout.connect(func() -> void:
		layer.queue_free()
		timer.queue_free()
	)
	timer.start()
'''
# call boot after build
if "_boot()" not in s.split("func _ready")[1].split("func ")[0]:
    s = s.replace("func _ready() -> void:", "func _ready() -> void:\n\t_boot()", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("boot timer version")
