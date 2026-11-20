class_name BribeEvent
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal chosen(kind: String)

var visitor_name := ""

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
	paper.position = Vector2(600, 280)
	paper.size = Vector2(720, 520)
	add_child(paper)
	var head := Ui.label("贿 赂", 32, Ui.INK, Ui.font_serif())
	head.position = Vector2(40, 28)
	head.size = Vector2(300, 42)
	paper.add_child(head)
	var body := Ui.rich(String(visitor_name) + " 把一张折起来的二十元推到窗口下沿。\n\n「检察员同学，我爸是校董。您就当没看见，行吗？」", 17, Ui.INK)
	body.position = Vector2(40, 88)
	body.size = Vector2(640, 160)
	body.scroll_active = false
	paper.add_child(body)
	var opts := [
		["accept", "收下", "+20 元　腐败 +1"],
		["refuse", "推回去", "照常罚款 −10 元"],
		["arrest", "叫校警", "+20 元　移交安全部"]
	]
	var y := 276
	for o in opts:
		var b := Ui.button("%s　—　%s" % [String(o[1]), String(o[2])], 17, Ui.INK, Ui.PAPER)
		b.position = Vector2(40, y)
		b.size = Vector2(640, 52)
		var key := String(o[0])
		b.pressed.connect(func() -> void: chosen.emit(key))
		paper.add_child(b)
		y += 62