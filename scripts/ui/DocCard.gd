class_name DocCard
extends Control

signal dropped(card: Control)

var _stamp: Label = null

var title := ""
var rows: Array = []
var _dragging := false
var _off := Vector2.ZERO

func setup(t: String, r: Array) -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	title = t
	rows = r
	_build()

func _build() -> void:
	custom_minimum_size = Vector2(330, 150)
	size = Vector2(330, 150)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 14)
	paper.mouse_filter = Control.MOUSE_FILTER_IGNORE
	paper.size = size
	add_child(paper)
	var h := Ui.label(title, 17, Ui.INK, Ui.font_serif())
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.position = Vector2(14, 10)
	h.size = Vector2(300, 24)
	paper.add_child(h)
	var y := 40
	for r in rows:
		var line := Ui.label("%s：%s" % [String(r[0]), String(r[1])], 13, Ui.INK_SOFT, Ui.font_mono())
		line.mouse_filter = Control.MOUSE_FILTER_IGNORE
		line.position = Vector2(14, y)
		line.size = Vector2(300, 20)
		paper.add_child(line)
		y += 22

func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_dragging = true
			_off = get_global_mouse_position() - global_position
			move_to_front()
		else:
			_dragging = false
			dropped.emit(self)
	elif event is InputEventMouseMotion and _dragging:
		position = get_global_mouse_position() - _off


func play_stamp(text: String, color: Color) -> void:
	if _stamp == null:
		_stamp = Ui.label("", 24, color, Ui.font_serif())
		_stamp.position = Vector2(40, 40)
		_stamp.size = Vector2(240, 40)
		_stamp.rotation = -0.16
		add_child(_stamp)
	_stamp.text = text
	_stamp.add_theme_color_override("font_color", color)
	_stamp.modulate = Color(1, 1, 1, 0.2)
	var t := create_tween()
	t.tween_property(_stamp, "modulate", Color(1, 1, 1, 1), 0.15)
	Sfx.play("stamp", -6.0)
