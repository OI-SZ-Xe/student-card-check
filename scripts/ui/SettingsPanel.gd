class_name SettingsPanel
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal closed

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.7)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 28)
	paper.position = Vector2(660, 260)
	paper.size = Vector2(600, 520)
	add_child(paper)
	var head := Ui.label("设 置", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(36, 26)
	head.size = Vector2(240, 38)
	paper.add_child(head)
	var rows := [
		["master", "总音量"],
		["music", "音乐"],
		["sfx", "音效"],
		["ambience", "环境音"]
	]
	var y := 100
	for row in rows:
		var key := String(row[0])
		var lab := Ui.label(String(row[1]), 17, Ui.INK, Ui.font_serif())
		lab.position = Vector2(36, y)
		lab.size = Vector2(110, 26)
		paper.add_child(lab)
		var slider := HSlider.new()
		slider.min_value = 0.0
		slider.max_value = 1.0
		slider.step = 0.01
		slider.value = float(Settings.volumes.get(key, 0.8))
		slider.position = Vector2(150, y + 4)
		slider.size = Vector2(300, 22)
		var val := Ui.label("%d%%" % int(slider.value * 100.0), 14, Ui.INK_SOFT, Ui.font_mono())
		val.position = Vector2(470, y + 2)
		val.size = Vector2(60, 22)
		slider.value_changed.connect(func(v: float) -> void:
			Settings.set_volume(key, v)
			val.text = "%d%%" % int(v * 100.0)
		)
		paper.add_child(slider)
		paper.add_child(val)
		y += 66
	var close := Ui.button("关闭", 18, Ui.INK, Ui.PAPER)
	close.position = Vector2(200, 420)
	close.size = Vector2(200, 48)
	close.pressed.connect(func() -> void: closed.emit())
	paper.add_child(close)