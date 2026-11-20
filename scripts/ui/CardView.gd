class_name CardView
extends Panel

signal field_picked(field_id: String)
signal stamped(text: String, color: Color)
signal card_pressed()
signal letter_opened()
signal confiscate_pressed()

const CARD_W := 560
const CARD_H := 430

var visitor: Dictionary = {}
var today := ""
var compare_mode := false
var picked := ""
var suspicious: Array = []
var _stamp: Label = null
var _stamp_frame: Panel = null
var _dragging := false
var _drag_offset := Vector2.ZERO

func _ready() -> void:
	custom_minimum_size = Vector2(CARD_W, CARD_H)
	size = Vector2(CARD_W, CARD_H)
	mouse_filter = Control.MOUSE_FILTER_STOP
	pivot_offset = size * 0.5
	add_theme_stylebox_override("panel", Ui.style(Ui.PAPER, Ui.PAPER_EDGE, 2, 1, 0))

func set_visitor(v: Dictionary, today_iso: String) -> void:
	visitor = v
	today = today_iso
	rebuild()

func clear() -> void:
	visitor = {}
	rebuild()

func rebuild() -> void:
	for c in get_children():
		c.queue_free()
	if visitor.is_empty():
		return
	var paper_tex := TextureRect.new()
	paper_tex.texture = load("res://art/tex/paper.png")
	paper_tex.stretch_mode = TextureRect.STRETCH_TILE
	paper_tex.position = Vector2.ZERO
	paper_tex.size = Vector2(CARD_W, CARD_H)
	paper_tex.modulate = Color(1, 1, 1, 0.55)
	paper_tex.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(paper_tex)
	var head := Ui.label("深圳实验中学 · 校门通行", 12, Ui.INK_SOFT, Ui.font_serif())
	head.position = Vector2(18, 12)
	head.size = Vector2(360, 18)
	head.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(head)
	var title := Ui.label("学 生 证", 26, Ui.INK, Ui.font_serif())
	title.position = Vector2(18, 30)
	title.size = Vector2(330, 34)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(title)
	var line := ColorRect.new()
	line.color = Ui.PAPER_EDGE
	line.position = Vector2(16, 66)
	line.size = Vector2(340, 2)
	line.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(line)

	var photo_seed := int(visitor.get("photo", {}).get("seed", 1))
	var photo := Portrait.new()
	photo.setup(photo_seed, true, bool(visitor.get("photo_mirrored", false)))
	photo.position = Vector2(392, 74)
	photo.size = Vector2(136, 168)
	photo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(photo)
	var photo_btn := Button.new()
	photo_btn.flat = true
	photo_btn.focus_mode = Control.FOCUS_NONE
	photo_btn.position = Vector2(392, 74)
	photo_btn.size = Vector2(136, 168)
	photo_btn.set_meta("field_id", "photo")
	photo_btn.mouse_filter = Control.MOUSE_FILTER_IGNORE
	photo_btn.pressed.connect(func() -> void: field_picked.emit("photo"))
	add_child(photo_btn)
	var photo_tag := Ui.label("证件照", 12, Ui.INK_SOFT, Ui.font_serif())
	photo_tag.position = Vector2(392, 246)
	photo_tag.size = Vector2(136, 18)
	photo_tag.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(photo_tag)

	var rows: Array = [
		["name", "姓名", String(visitor.get("name", ""))],
		["grade", "年级", "%d年级" % int(visitor.get("grade", 0))],
		["birth", "出生日期", String(visitor.get("birth", ""))],
		["id", "学号", String(visitor.get("student_id", ""))],
		["expiry", "有效期", String(visitor.get("expiry", ""))],
		["today", "今日", String(today)],
		["school", "学校", String(visitor.get("school", ""))]
	]
	var y := 76
	for r in rows:
		_add_row(String(r[0]), String(r[1]), String(r[2]), y, 32)
		y += 36

	var div := ColorRect.new()
	div.color = Color(Ui.PAPER_EDGE, 0.7)
	div.position = Vector2(16, y + 2)
	div.size = Vector2(508, 1)
	div.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(div)
	y += 10

	var extras := _extra_rows()
	for e in extras:
		_add_row(String(e[0]), String(e[1]), String(e[2]), y, 28, 15)
		y += 30

	var sid_text := String(visitor.get("student_id", "0000"))
	var serial := Ui.label("NO. %s" % sid_text, 11, Ui.INK_SOFT, Ui.font_mono())
	serial.position = Vector2(392, 270)
	serial.size = Vector2(150, 16)
	serial.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(serial)

	if visitor.has("transfer_letter"):
		var lbtn := Ui.button("查看介绍信", 13, Ui.PAPER_DARK, Ui.INK)
		lbtn.position = Vector2(392, 286)
		lbtn.size = Vector2(136, 32)
		lbtn.pressed.connect(func() -> void: letter_opened.emit())
		add_child(lbtn)
		if State.day >= 25:
			var cbtn := Ui.button("没收介绍信", 13, Color("#c8a24a"), Ui.INK)
			cbtn.position = Vector2(392, 324)
			cbtn.size = Vector2(136, 32)
			cbtn.pressed.connect(func() -> void: confiscate_pressed.emit())
			add_child(cbtn)

	_stamp_frame = Ui.panel(Color(0, 0, 0, 0), Color(Ui.RED, 0.9), 4, 0, 0)
	_stamp_frame.position = Vector2(60, 322)
	_stamp_frame.size = Vector2(250, 78)
	_stamp_frame.rotation = -0.17
	_stamp_frame.visible = false
	_stamp_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stamp = Ui.label("", 34, Ui.RED, Ui.font_serif())
	_stamp.position = Vector2(0, 12)
	_stamp.size = Vector2(250, 54)
	_stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_stamp.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stamp_frame.add_child(_stamp)
	add_child(_stamp_frame)

	_refresh_row_state()

func _extra_rows() -> Array:
	return []
func _add_row(field_id: String, label_text: String, value_text: String, y: int, height: int, size_value: int = 17) -> void:
	var b := Button.new()
	b.position = Vector2(16, y)
	b.size = Vector2(340, height)
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 2, 0))
	b.add_theme_stylebox_override("hover", Ui.style(Color(0.35, 0.26, 0.10, 0.12), Color(0, 0, 0, 0), 0, 2, 0))
	b.add_theme_stylebox_override("pressed", Ui.style(Color(0.35, 0.26, 0.10, 0.22), Color(0, 0, 0, 0), 0, 2, 0))
	b.add_theme_stylebox_override("focus", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	var l := Ui.label(label_text, 14, Ui.INK_SOFT, Ui.font_serif())
	l.position = Vector2(8, (height - 20) / 2)
	l.size = Vector2(104, 20)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(l)
	var bad := suspicious.has(field_id)
	var vcol := Ui.RED if bad else Ui.INK
	var v := Ui.label(value_text, size_value, vcol, Ui.font_mono())
	v.position = Vector2(116, (height - 22) / 2)
	v.size = Vector2(216, 24)
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(v)
	if bad:
		var mark := Ui.label("!", 18, Ui.RED, Ui.font_mono())
		mark.position = Vector2(318, (height - 22) / 2)
		mark.mouse_filter = Control.MOUSE_FILTER_IGNORE
		b.add_child(mark)
	b.set_meta("field_id", field_id)
	b.pressed.connect(func() -> void: field_picked.emit(field_id))
	add_child(b)

func _refresh_row_state() -> void:
	for c in get_children():
		if c is Button and c.has_meta("field_id"):
			c.mouse_filter = Control.MOUSE_FILTER_STOP if compare_mode else Control.MOUSE_FILTER_IGNORE
			var fid := String(c.get_meta("field_id"))
			var bg := Color(0, 0, 0, 0)
			if compare_mode and fid == picked:
				bg = Color(0.65, 0.45, 0.10, 0.22)
			c.add_theme_stylebox_override("normal", Ui.style(bg, Color(0, 0, 0, 0), 0, 2, 0))

func set_compare_mode(on: bool) -> void:
	compare_mode = on
	if not on:
		picked = ""
	_refresh_row_state()

func set_picked(field_id: String) -> void:
	picked = field_id
	_refresh_row_state()

func set_suspicious(fields: Array) -> void:
	suspicious = fields.duplicate()
	rebuild()

func play_stamp(text: String, color: Color) -> void:
	stamped.emit(text, color)
	if _stamp == null or _stamp_frame == null:
		return
	_stamp.text = text
	_stamp.add_theme_color_override("font_color", color)
	_stamp_frame.add_theme_stylebox_override("panel", Ui.style(Color(0, 0, 0, 0), Color(color, 0.9), 4, 0, 0))
	_stamp_frame.visible = true
	_stamp_frame.pivot_offset = _stamp_frame.size * 0.5
	_stamp_frame.scale = Vector2(2.4, 2.4)
	_stamp_frame.modulate = Color(1, 1, 1, 0.25)
	var t := create_tween()
	t.set_parallel(true)
	t.tween_property(_stamp_frame, "scale", Vector2.ONE, 0.20).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	t.tween_property(_stamp_frame, "modulate", Color(1, 1, 1, 1), 0.12)
	Sfx.play("stamp", -4.0)

func shake() -> void:
	var base := position
	var t := create_tween()
	t.tween_property(self, "position", base + Vector2(6, 0), 0.04)
	t.tween_property(self, "position", base + Vector2(-5, 0), 0.04)
	t.tween_property(self, "position", base, 0.05)

func _gui_input(event: InputEvent) -> void:
	if compare_mode:
		return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_dragging = true
			_drag_offset = get_global_mouse_position() - global_position
			move_to_front()
		elif _dragging:
			_dragging = false
			card_pressed.emit()
	elif event is InputEventMouseMotion and _dragging:
		global_position = get_global_mouse_position() - _drag_offset
