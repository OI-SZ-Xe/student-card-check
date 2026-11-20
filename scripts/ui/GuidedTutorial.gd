class_name GuidedTutorial
extends Control

signal finished

var _i := 0
var _title: Label
var _text: Label
var _tip: Panel
var _hl: Panel

const STEPS := [
	{"r": Rect2(120, 486, 560, 430), "t": "第一步：拿证件", "d": "点一下证件，它会被抽到窗口前；其它材料是一张张单独的卡片，可以拖开看。", "p": Vector2(760, 520)},
	{"r": Rect2(740, 496, 410, 236), "t": "第二步：开对照", "d": "点「对照模式」，再点证件上的两行字段，就能并排比对。", "p": Vector2(300, 300)},
	{"r": Rect2(120, 486, 1030, 478), "t": "第三步：盖章", "d": "先点一枚印章，再点一下证件，章就盖下去了。", "p": Vector2(300, 520)},

]

func _ready() -> void:
	z_index = 250
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hl = Panel.new()
	_hl.add_theme_stylebox_override("panel", Ui.style(Color(0, 0, 0, 0), Color("#d9b45c"), 3, 2, 0))
	_hl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_hl)
	_tip = Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 18)
	_tip.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_tip)
	_title = Ui.label("", 22, Ui.INK, Ui.font_serif())
	_title.position = Vector2(20, 14)
	_title.size = Vector2(380, 30)
	_tip.add_child(_title)
	_text = Ui.label("", 15, Ui.INK, Ui.font_serif())
	_text.position = Vector2(20, 52)
	_text.size = Vector2(380, 80)
	_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_tip.add_child(_text)
	var next := Ui.button("下一步", 16, Ui.INK, Ui.PAPER)
	next.position = Vector2(20, 140)
	next.size = Vector2(150, 42)
	next.pressed.connect(_advance_step)
	_tip.add_child(next)
	var skip := Ui.button("跳过", 14, Color(0, 0, 0, 0), Ui.INK_SOFT)
	skip.position = Vector2(180, 140)
	skip.size = Vector2(90, 42)
	skip.pressed.connect(func() -> void: finished.emit())
	_tip.add_child(skip)
	_show(0)

var _done := false

func _advance() -> void:
	if _done:
		return
	if _i >= STEPS.size() - 1:
		_done = true
		finished.emit()
		return
	_show(_i + 1)

func _show(i: int) -> void:
	_i = i
	var s: Dictionary = STEPS[i]
	var r: Rect2 = s.r
	_hl.position = r.position
	_hl.size = r.size
	_tip.position = s.p
	_tip.size = Vector2(420, 200)
	_title.text = String(s.t)
	_text.text = String(s.d)
	var dots := ""
	for k in STEPS.size():
		dots += "●" if k == i else "○"
	_text.text = String(s.d) + "\n\n" + dots


func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch and event.pressed:
		if _hl != null and _hl.get_global_rect().has_point(event.position):
			_advance()
		return
	if not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	if _hl == null:
		return
	if _hl.get_global_rect().has_point(event.position):
		_advance()

func _advance_step() -> void:
	_advance()
