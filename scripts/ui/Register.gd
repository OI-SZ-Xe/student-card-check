class_name Register
extends Control

signal submitted(player_name: String, player_class: String, talent: String)

var _name_input: LineEdit = null
var _class_input: LineEdit = null
var _hint: Label = null
var _talent := "economic"
var _talent_btns: Array = []

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := ColorRect.new()
	bg.color = Color("#0a0c0a")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	var paper := Ui.panel(Color("#e9dfc2"), Color("#8d7c52"), 2, 1, 32)
	paper.position = Vector2(600, 250)
	paper.size = Vector2(760, 600)
	add_child(paper)

	var head := Ui.label("入 职 登 记 表", 34, Ui.INK, Ui.font_serif())
	head.position = Vector2(48, 34)
	head.size = Vector2(500, 44)
	paper.add_child(head)
	var sub := Ui.label("学生会纪检部 · 校门检查站 · 2026 年春季", 14, Ui.INK_SOFT, Ui.font_mono())
	sub.position = Vector2(48, 82)
	sub.size = Vector2(600, 20)
	paper.add_child(sub)
	var rule := ColorRect.new()
	rule.color = Ui.PAPER_EDGE
	rule.position = Vector2(48, 112)
	rule.size = Vector2(664, 2)
	paper.add_child(rule)

	var label_name := Ui.label("姓　　名", 18, Ui.INK, Ui.font_serif())
	label_name.position = Vector2(48, 146)
	label_name.size = Vector2(120, 26)
	paper.add_child(label_name)
	_name_input = _make_input("请输入你的姓名")
	_name_input.position = Vector2(180, 140)
	_name_input.size = Vector2(500, 44)
	paper.add_child(_name_input)

	var label_class := Ui.label("班　　级", 18, Ui.INK, Ui.font_serif())
	label_class.position = Vector2(48, 210)
	label_class.size = Vector2(120, 26)
	paper.add_child(label_class)
	_class_input = _make_input("例如：八年级（3）班")
	_class_input.position = Vector2(180, 204)
	_class_input.size = Vector2(500, 44)
	paper.add_child(_class_input)

	_hint = Ui.label("", 14, Ui.RED, Ui.font_serif())
	_hint.position = Vector2(48, 260)
	_hint.size = Vector2(660, 22)
	paper.add_child(_hint)

	if Meta.runs > 0:
		var tname := _talent_name(Meta.last_talent)
		var ng_text := "第 %d 周目：伪造率 +15%%" % (Meta.runs + 1)
		if tname != "无":
			ng_text = "第 %d 周目：继承上周目天赋「%s」，伪造率 +15%%" % [Meta.runs + 1, tname]
		var ng := Ui.label(ng_text, 14, Ui.RED, Ui.font_serif())
		ng.position = Vector2(48, 336)
		ng.size = Vector2(660, 22)
		paper.add_child(ng)
		_talent = Meta.last_talent if Meta.last_talent != "" else _talent
	var note := Ui.rich("此表信息将打印在《纪检部入职考核表》与《录取通知》上。\n姓名与班级会写入你的执勤档案，无法更改。", 15, Ui.INK_SOFT)
	note.position = Vector2(48, 296)
	note.size = Vector2(660, 90)
	note.scroll_active = false
	paper.add_child(note)

	var talent_label := Ui.label("入职特长（三选一）", 18, Ui.INK, Ui.font_serif())
	talent_label.position = Vector2(48, 372)
	talent_label.size = Vector2(300, 24)
	paper.add_child(talent_label)
	var talents := [["economic", "经济头脑"], ["justice", "正义感"], ["insight", "洞察力"]]
	for i in talents.size():
		var tb := Ui.button(String(talents[i][1]), 15, Ui.PAPER_DARK, Ui.INK)
		tb.position = Vector2(48 + i * 210, 402)
		tb.size = Vector2(196, 40)
		var key := String(talents[i][0])
		tb.pressed.connect(func() -> void: _pick_talent(key))
		paper.add_child(tb)
		_talent_btns.append(tb)

	var btn := Ui.button("确认并提交", 20, Ui.INK, Ui.PAPER)
	btn.position = Vector2(250, 462)
	btn.size = Vector2(260, 54)
	btn.pressed.connect(_submit)
	paper.add_child(btn)

	var foot := Ui.label("深圳实验中学 学生会 · 内部资料", 12, Ui.INK_SOFT, Ui.font_mono())
	foot.position = Vector2(48, 540)
	foot.size = Vector2(500, 18)
	paper.add_child(foot)

	_name_input.text_submitted.connect(func(_t: String) -> void: _class_input.grab_focus())
	_class_input.text_submitted.connect(func(_t: String) -> void: _submit())
	_name_input.grab_focus()

func _make_input(placeholder: String) -> LineEdit:
	var e := LineEdit.new()
	e.placeholder_text = placeholder
	e.add_theme_font_override("font", Ui.font_mono())
	e.add_theme_font_size_override("font_size", 20)
	e.add_theme_color_override("font_color", Ui.INK)
	e.add_theme_color_override("font_placeholder_color", Color(0.45, 0.40, 0.32, 0.8))
	e.add_theme_color_override("caret_color", Ui.RED)
	e.add_theme_stylebox_override("normal", Ui.style(Color("#f2e9cd"), Color(0.45, 0.38, 0.26, 0.5), 1, 2, 10))
	e.add_theme_stylebox_override("focus", Ui.style(Color("#f6efd8"), Color(0.62, 0.18, 0.14), 2, 2, 10))
	return e

func _submit() -> void:
	var pname := _name_input.text.strip_edges()
	var pclass := _class_input.text.strip_edges()
	if pname == "":
		_hint.text = "姓名不能为空。"
		return
	if pname.length() > 12:
		_hint.text = "姓名过长，请控制在 12 个字以内。"
		return
	if pclass == "":
		_hint.text = "班级不能为空。"
		return
	Sfx.play("stamp", -8.0)
	submitted.emit(pname, pclass, _talent)


func _pick_talent(key: String) -> void:
	_talent = key
	_refresh_talent()

func _refresh_talent() -> void:
	var keys := ["economic", "justice", "insight"]
	for i in _talent_btns.size():
		var b: Button = _talent_btns[i]
		var on: bool = keys[i] == _talent
		b.add_theme_stylebox_override("normal", Ui.style(Ui.RED if on else Ui.PAPER_DARK, Color(0, 0, 0, 0), 0, 0, 9))
		b.add_theme_color_override("font_color", Ui.PAPER if on else Ui.INK)


func _talent_name(key: String) -> String:
	if key == "justice":
		return "正义感"
	if key == "insight":
		return "洞察力"
	if key == "economic":
		return "经济头脑"
	return "无"
