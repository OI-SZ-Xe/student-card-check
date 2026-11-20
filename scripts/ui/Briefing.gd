class_name Briefing
extends Control

signal closed

var _armed := false

var day := 1
var date_iso := ""
var headline := ""
var quota := 0

func _ready() -> void:
	await get_tree().create_timer(0.4).timeout
	_armed = true
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.05, 0.06, 0.05, 0.62)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(dim)

	var paper := Ui.panel(Ui.PAPER, Ui.PAPER_EDGE, 2, 1, 28)
	paper.position = Vector2(560, 200)
	paper.size = Vector2(800, 640)
	paper.pivot_offset = Vector2(400, 360)
	add_child(paper)

	var mast := Ui.label("校 园 日 报", 42, Ui.INK, Ui.font_serif())
	mast.position = Vector2(48, 26)
	mast.size = Vector2(600, 52)
	paper.add_child(mast)
	var sub := Ui.label("第 %d 天 · %s · 学生会纪检部执勤简报" % [day, State.weekday_cn(date_iso) + " " + date_iso], 14, Ui.INK_SOFT, Ui.font_mono())
	sub.position = Vector2(50, 78)
	sub.size = Vector2(700, 20)
	paper.add_child(sub)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(48, 104)
	rule.size = Vector2(704, 3)
	paper.add_child(rule)

	var today_label := Ui.label("今日核验要点", 20, Ui.INK, Ui.font_serif())
	today_label.position = Vector2(48, 120)
	today_label.size = Vector2(300, 26)
	paper.add_child(today_label)

	var body := Ui.rich("", 16, Ui.INK)
	body.position = Vector2(48, 150)
	body.size = Vector2(704, 210)
	body.scroll_active = false
	body.text = _rules_text()
	paper.add_child(body)

	var news := Ui.rich("", 15, Ui.INK_SOFT)
	news.position = Vector2(48, 380)
	news.size = Vector2(704, 100)
	news.text = "[b]今日头条[/b]　%s\n[b]部内通知[/b]　%s" % [headline, _notice()]
	paper.add_child(news)

	var rent_note := "首日入住临时宿舍，免扣房租水电" if day <= 1 else "房租水电已扣"
	var money := Ui.label("当前余额 %d 元　·　%s　·　简单模式补贴已入账" % [State.money, rent_note], 13, Ui.INK_SOFT, Ui.font_mono())
	money.position = Vector2(48, 500)
	money.size = Vector2(704, 20)
	paper.add_child(money)

	var start := Ui.button("开始今日执勤", 20, Ui.INK, Ui.PAPER)
	start.position = Vector2(268, 546)
	start.size = Vector2(264, 52)
	start.pressed.connect(_on_start)
	paper.add_child(start)

	var seal := Ui.label("纪 检 部", 26, Color(Ui.RED, 0.75), Ui.font_serif())
	seal.position = Vector2(596, 534)
	seal.size = Vector2(140, 40)
	seal.rotation = -0.12
	paper.add_child(seal)

	modulate = Color(1, 1, 1, 0)
	create_tween().tween_property(self, "modulate", Color(1, 1, 1, 1), 0.22)

func _rules_text() -> String:
	var lines: Array = []
	for d in Data.doc_rules:
		var unlock := int(d.get("day", 1))
		var mark := "今日启用" if unlock == day else ("已启用" if unlock < day else "未启用")
		var scope := String(d.get("scope", "all"))
		var scope_cn := "全部人员"
		if scope == "experiment":
			scope_cn = "实验学生"
		elif scope == "external":
			scope_cn = "外校学生"
		elif scope == "transfer":
			scope_cn = "转学目的"
		lines.append("· %s（%s，%s）" % [String(d.get("name", "")), scope_cn, mark])
	if quota > 0:
		lines.append("· 安全部要求：今日至少拒绝 %d 人。做不到的部分，自己想办法。" % quota)
	return "\n".join(lines)

func _notice() -> String:
	if quota > 0:
		return "校园安全部：拒签指标今日起生效，未达标者按失职记录。"
	if day == 1:
		return "新同事请先阅读桌面上的《校门检查员仿真手册》，按 M 键随时翻阅。"
	return "请保持检查亭整洁，印章归位，抽屉上锁。"

func _on_start() -> void:
	Sfx.play("paper", -10.0)
	closed.emit()


func _input(event: InputEvent) -> void:
	if not _armed:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_armed = false
		closed.emit()
