class_name FaceCompare
extends Control

signal closed

var visitor: Dictionary = {}

func _ready() -> void:
	z_index = 260
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.82)
	dim.size = Vector2(1920, 1080)
	add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 26)
	paper.position = Vector2(560, 200)
	paper.size = Vector2(800, 700)
	add_child(paper)
	var t := Ui.label("对 照 脸", 28, Ui.INK, Ui.font_serif())
	t.position = Vector2(36, 24)
	t.size = Vector2(300, 38)
	paper.add_child(t)
	var card_seed := int(visitor.get("photo", {}).get("seed", 1))
	var live_seed := int(visitor.get("face_seed", card_seed))
	var left := Portrait.new()
	left.setup(card_seed, true, bool(visitor.get("photo_mirrored", false)))
	left.position = Vector2(70, 100)
	left.size = Vector2(250, 310)
	paper.add_child(left)
	var right := Portrait.new()
	right.setup(live_seed, true, false)
	right.position = Vector2(480, 100)
	right.size = Vector2(250, 310)
	paper.add_child(right)
	var l1 := Ui.label("证件照", 15, Ui.INK, Ui.font_serif())
	l1.position = Vector2(70, 420)
	l1.size = Vector2(250, 22)
	l1.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	paper.add_child(l1)
	var l2 := Ui.label("本人", 15, Ui.INK, Ui.font_serif())
	l2.position = Vector2(480, 420)
	l2.size = Vector2(250, 22)
	l2.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	paper.add_child(l2)
	var tip := Ui.rich("看：五官比例、痣的位置、耳形、发际线。\n镜像翻拍会左右颠倒——证件照上的分缝和本人相反。", 15, Ui.INK_SOFT)
	tip.position = Vector2(70, 456)
	tip.size = Vector2(660, 80)
	tip.scroll_active = false
	paper.add_child(tip)
	var b := Ui.button("关 上", 17, Ui.INK, Ui.PAPER)
	b.position = Vector2(290, 570)
	b.size = Vector2(220, 48)
	b.pressed.connect(func() -> void: closed.emit())
	paper.add_child(b)
