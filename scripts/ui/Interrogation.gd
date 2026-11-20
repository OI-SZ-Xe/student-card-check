class_name Interrogation
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal action(kind: String)
signal spend(seconds: float)
signal supplied

var visitor: Dictionary = {}
var today := ""
var called := false
var db_checked := false
var _log: RichTextLabel
var _rng := RandomNumberGenerator.new()

func _ready() -> void:
	z_index = _modal_z
	_rng.randomize()
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.78)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 26)
	paper.position = Vector2(520, 180)
	paper.size = Vector2(880, 720)
	add_child(paper)
	var head := Ui.label("询 问", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(36, 24)
	head.size = Vector2(300, 40)
	paper.add_child(head)
	var name_line := Ui.label("%s　%s　%s" % [String(visitor.get("name", "")), String(visitor.get("school", "")), String(visitor.get("purpose", ""))], 14, Ui.INK_SOFT, Ui.font_mono())
	name_line.position = Vector2(36, 68)
	name_line.size = Vector2(700, 20)
	paper.add_child(name_line)

	var issues := _issues()
	var issue_text := "你注意到的问题：\n"
	if issues.is_empty():
		issue_text += "　暂时没有发现明显疑点。"
	else:
		for s in issues:
			issue_text += "　· " + String(s) + "\n"
	var issue_label := Ui.rich(issue_text, 15, Ui.INK)
	issue_label.position = Vector2(36, 100)
	issue_label.size = Vector2(808, 120)
	issue_label.scroll_active = false
	paper.add_child(issue_label)

	var excuse: Dictionary = visitor.get("excuse", {})
	var quote := Ui.rich("学生：「%s」" % String(excuse.get("text", "……")), 17, Ui.INK)
	quote.position = Vector2(36, 228)
	quote.size = Vector2(808, 56)
	quote.scroll_active = false
	paper.add_child(quote)

	_log = Ui.rich("", 15, Ui.INK)
	_log.position = Vector2(36, 292)
	_log.size = Vector2(808, 200)
	_log.scroll_active = false
	paper.add_child(_log)

	var docs: Dictionary = visitor.get("docs", {})
	for k in docs.keys():
		if bool(docs[k].get("missing", false)):
			var sup := Ui.button("要求补交材料", 16, Color(0.24, 0.28, 0.18), Ui.WHITE)
			sup.position = Vector2(528, 512)
			sup.size = Vector2(230, 48)
			var key := String(k)
			sup.pressed.connect(func() -> void:
				spend.emit(5.0)
				if bool(docs[key].get("can_supply", false)):
					docs[key]["missing"] = false
					_log.text += "\n他翻了翻书包，把材料补上了。"
					supplied.emit()
				else:
					_log.text += "\n他拿不出来：「真的没带，我明天再来。」"
			)
			paper.add_child(sup)

	var guide := Ui.rich("核实手段要自己动手：\n　· 电话：按 P 打开话机，拨学校或教育局号码，听完回复\n　· 档案：打开电脑 → 浏览器 → 教育局档案，输入姓名查询（慢，但准）", 15, Ui.INK)
	guide.position = Vector2(36, 500)
	guide.size = Vector2(808, 120)
	guide.scroll_active = false
	paper.add_child(guide)

	var approve := Ui.button("采信放行", 16, Color(0.18, 0.34, 0.22), Ui.WHITE)
	approve.position = Vector2(36, 588)
	approve.size = Vector2(230, 52)
	approve.pressed.connect(func() -> void: action.emit("approve"))
	paper.add_child(approve)

	var reject := Ui.button("拒 绝", 16, Color(0.40, 0.18, 0.16), Ui.WHITE)
	reject.position = Vector2(282, 588)
	reject.size = Vector2(230, 52)
	reject.pressed.connect(func() -> void: action.emit("reject"))
	paper.add_child(reject)

	var arrest := Ui.button("逮 捕", 16, Color(0.30, 0.16, 0.12), Ui.WHITE)
	arrest.position = Vector2(528, 588)
	arrest.size = Vector2(230, 52)
	arrest.pressed.connect(func() -> void: action.emit("arrest"))
	paper.add_child(arrest)

	var close := Ui.button("先不处理", 14, Color(0, 0, 0, 0), Ui.INK_SOFT)
	close.position = Vector2(700, 654)
	close.size = Vector2(150, 34)
	close.pressed.connect(func() -> void: action.emit("close"))
	paper.add_child(close)

	var hint := Ui.label("理由一眼假就拒绝；证件造假就逮捕；拿不准就打电话或查档案。", 13, Ui.INK_SOFT, Ui.font_mono())
	hint.position = Vector2(36, 660)
	hint.size = Vector2(640, 20)
	paper.add_child(hint)

func _issues() -> Array:
	var ctx := {"required": visitor.get("required", []), "doc_names": {}, "principals": {}, "check_photo": true}
	var res := RuleEngine.evaluate(visitor, today, ctx)
	var out: Array = []
	for r in res.get("reasons", []):
		out.append(String(r))
	return out

func _verify_phone() -> void:
	if called:
		return
	called = true
	spend.emit(8.0)
	var forged: Array = visitor.get("forged_fields", [])
	var truthful := _rng.randf() < 0.75
	var bad := (not forged.is_empty()) if truthful else forged.is_empty()
	_log.text += "\n电话：转出学校值班室翻了翻册子，说这位同学的档案%s。" % ("对不上" if bad else "没问题")
	_log.text += "\n（电话核查有误差，不一定准。）"

func _query_db() -> void:
	if db_checked:
		return
	db_checked = true
	spend.emit(25.0)
	var rec: Dictionary = visitor.get("record", {})
	var lines := "\n教育局档案（准确）：\n"
	lines += "　姓名：%s　曾用名：%s\n" % [String(rec.get("name", "")), "、".join(rec.get("old_names", [])) if not rec.get("old_names", []).is_empty() else "无"]
	lines += "　出生：%s　学号：%s\n" % [String(rec.get("birth", "")), String(rec.get("id", ""))]
	lines += "　就读：%s　转学记录：%d 条" % [String(rec.get("school", "")), (rec.get("transfers", []) as Array).size()]
	var forged: Array = visitor.get("forged_fields", [])
	if forged.is_empty():
		lines += "\n　与证件核对：一致。"
	else:
		lines += "\n　与证件核对：不一致（%s）。" % "、".join(forged)
	_log.text += lines