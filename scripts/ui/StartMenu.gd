class_name StartMenu
extends Control

signal choice(kind: String)

func _ready() -> void:
	z_index = 200
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := ColorRect.new()
	bg.color = Color("#101613")
	bg.size = Vector2(1920, 1080)
	add_child(bg)
	var title := Ui.label("请 出 示 学 生 证", 64, Color("#e4dbc2"), Ui.font_serif())
	title.position = Vector2(0, 220)
	title.size = Vector2(1920, 90)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(title)
	var sub := Ui.label("学生纪律检查委员会 · 校门检查站", 18, Color("#7d8a7a"), Ui.font_serif())
	sub.position = Vector2(0, 318)
	sub.size = Vector2(1920, 28)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(sub)
	var items := [["new", "开始执勤"], ["continue", "读取存档"], ["endless", "无尽模式"], ["settings", "设置"], ["quit", "退出"]]
	var y := 430
	for it in items:
		var b := Ui.button(String(it[1]), 20, Color("#1b2620"), Color("#e4dbc2"))
		b.position = Vector2(760, y)
		b.size = Vector2(400, 56)
		b.add_theme_stylebox_override("normal", Ui.style(Color("#1b2620"), Color("#5a6a52"), 1, 0, 10))
		var key := String(it[0])
		if key == "continue" and not SaveManager.has(1):
			b.disabled = true
			b.text = "读取存档（空）"
		if key == "endless" and State.endings_seen.is_empty() and Meta.endings.is_empty():
			b.disabled = true
			b.text = "无尽模式（通关后解锁）"
		b.pressed.connect(func() -> void:
			if key == "settings":
				var sp := SettingsPanel.new()
				add_child(sp)
				sp.closed.connect(func() -> void: sp.queue_free())
				return
			choice.emit(key)
		)
		add_child(b)
		y += 76
	var foot := Ui.label("v1.0　校园安全部", 13, Color("#4f5a4c"), Ui.font_mono())
	foot.position = Vector2(0, 980)
	foot.size = Vector2(1920, 22)
	foot.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(foot)
