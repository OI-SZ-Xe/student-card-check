class_name OrgEvent
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal chosen(kind: String)

var data: Dictionary = {}

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.72)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)

	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 30)
	paper.position = Vector2(500, 210)
	paper.size = Vector2(920, 640)
	add_child(paper)

	var head := Ui.label("学 生 斗 争 委 员 会", 26, Ui.INK, Ui.font_serif())
	head.position = Vector2(44, 30)
	head.size = Vector2(600, 34)
	paper.add_child(head)
	var sub := Ui.label("主题：%s" % String(data.get("subject", "")), 15, Ui.INK_SOFT, Ui.font_mono())
	sub.position = Vector2(44, 70)
	sub.size = Vector2(700, 22)
	paper.add_child(sub)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(44, 102)
	rule.size = Vector2(832, 2)
	paper.add_child(rule)

	var body := Ui.rich(String(data.get("body", "")), 17, Ui.INK)
	body.position = Vector2(44, 124)
	body.size = Vector2(832, 300)
	body.scroll_active = false
	paper.add_child(body)

	var opts := [
		["help", "帮他们", "信任 +%d" % int(data.get("help", 1))],
		["report", "举报给纪检部", "怀疑度 -2，嘉奖 +10"],
		["delete", "删除邮件", "什么都不做"]
	]
	if int(data.get("cost", 0)) > 0:
		opts[0][2] = "花费 %d 元，信任 +%d" % [int(data.get("cost", 0)), int(data.get("help", 1))]
	var y := 452
	for o in opts:
		var b := Ui.button("%s　—　%s" % [String(o[1]), String(o[2])], 17, Ui.INK, Ui.PAPER)
		b.position = Vector2(44, y)
		b.size = Vector2(832, 52)
		var key := String(o[0])
		b.pressed.connect(func() -> void: chosen.emit(key))
		paper.add_child(b)
		y += 60