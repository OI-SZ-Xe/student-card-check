class_name EduTerminal
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal closed
signal time_cost(seconds: float)
signal org_requested(mail_id: int)

const GREEN := Color("#9ad7a2")
const DIM := Color("#5c8a66")
const AMBER := Color("#d9b45c")
const RED := Color("#c86a5a")
const BG := Color("#060d09")
const PANEL := Color("#0a1610")
const EDGE := Color("#2e5a3a")

var visitor: Dictionary = {}
var start_site := "schools"
var _nav: VBoxContainer = null
var _title: Label = null
var _body: VBoxContainer = null
var _status: Label = null
var _active := "schools"

const SITES := [
	["schools", "学校信息库"],
	["phone", "教育局电话簿"],
	["rules", "准入规定"],
	["wanted", "协查通报"],
	["archive", "档案查询"],
	["mail", "收件箱"],
	["exchange", "证券交易所"],
	["black", "黑市"],
	["browser", "浏览器"],
	["achv", "成就"]
]

func _ready() -> void:
	var lf := FileAccess.open("user://debug.log", FileAccess.READ_WRITE)
	if lf == null:
		lf = FileAccess.open("user://debug.log", FileAccess.WRITE)
	if lf != null:
		lf.seek_end()
		lf.store_line("terminal ready site=%s" % start_site)
		lf.close()
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	z_index = 150
	visible = true
	z_index = 150
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build()
	print("TERM ready z=", z_index, " size=", size, " children=", get_child_count())
	_show(start_site)

func _build() -> void:
	var dim := ColorRect.new()
	dim.z_index = -1
	dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	dim.color = Color(0.02, 0.03, 0.02, 0.92)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)

	var term := Ui.panel(PANEL, EDGE, 2, 0, 0)
	term.position = Vector2(150, 90)
	term.size = Vector2(1620, 900)
	add_child(term)
	print("TERM panel pos=", term.position, " size=", term.size, " vis=", term.visible)

	var head := ColorRect.new()
	head.color = Color("#0d2016")
	head.position = Vector2(0, 0)
	head.size = Vector2(1620, 54)
	term.add_child(head)
	var title := Ui.label("教育局内部网络 · 终端 07 · 校门检查站", 18, GREEN, Ui.font_mono())
	title.position = Vector2(20, 14)
	title.size = Vector2(800, 26)
	term.add_child(title)
	var date := Ui.label("%s　%s" % [State.date, State.weekday_cn(State.date)], 16, DIM, Ui.font_mono())
	date.position = Vector2(1160, 15)
	date.size = Vector2(300, 24)
	date.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	term.add_child(date)
	var close := Ui.button("断开 (Esc)", 14, Color("#12281a"), GREEN)
	close.position = Vector2(1462, 8)
	close.size = Vector2(140, 38)
	close.pressed.connect(func() -> void: closed.emit())
	term.add_child(close)

	var nav := ColorRect.new()
	nav.color = Color("#08120c")
	nav.position = Vector2(0, 54)
	nav.size = Vector2(320, 800)
	term.add_child(nav)
	_nav = VBoxContainer.new()
	_nav.position = Vector2(16, 70)
	_nav.size = Vector2(288, 700)
	_nav.add_theme_constant_override("separation", 4)
	term.add_child(_nav)
	for site in SITES:
		var b := Button.new()
		b.text = "› " + String(site[1])
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.custom_minimum_size = Vector2(288, 46)
		b.focus_mode = Control.FOCUS_NONE
		b.add_theme_font_override("font", Ui.font_mono())
		b.add_theme_font_size_override("font_size", 17)
		b.add_theme_color_override("font_color", GREEN)
		b.add_theme_color_override("font_hover_color", AMBER)
		b.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 10))
		b.add_theme_stylebox_override("hover", Ui.style(Color(0.1, 0.2, 0.12, 0.6), Color(0, 0, 0, 0), 0, 0, 10))
		b.add_theme_stylebox_override("pressed", Ui.style(Color(0.12, 0.26, 0.16, 0.8), Color(0, 0, 0, 0), 0, 0, 10))
		b.add_theme_stylebox_override("focus", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
		var key := String(site[0])
		b.pressed.connect(func() -> void: _show(key))
		_nav.add_child(b)

	var divider := ColorRect.new()
	divider.color = EDGE
	divider.position = Vector2(320, 54)
	divider.size = Vector2(2, 800)
	term.add_child(divider)

	_title = Ui.label("", 24, AMBER, Ui.font_mono())
	_title.position = Vector2(352, 76)
	_title.size = Vector2(1200, 32)
	term.add_child(_title)

	var scroll := ScrollContainer.new()
	scroll.position = Vector2(352, 122)
	scroll.size = Vector2(1230, 660)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	term.add_child(scroll)
	_body = VBoxContainer.new()
	_body.add_theme_constant_override("separation", 10)
	_body.custom_minimum_size = Vector2(1200, 0)
	scroll.add_child(_body)

	var status_bar := ColorRect.new()
	status_bar.color = Color("#0d2016")
	status_bar.position = Vector2(0, 854)
	status_bar.size = Vector2(1620, 46)
	term.add_child(status_bar)
	_status = Ui.label("本次访问已记录在案。", 14, DIM, Ui.font_mono())
	_status.position = Vector2(20, 866)
	_status.size = Vector2(1200, 22)
	term.add_child(_status)

func _clear() -> void:
	for c in _body.get_children():
		c.queue_free()
	for i in _nav.get_children():
		if i is Button:
			var active: bool = String(i.text).find(_nav_title(_active)) >= 0
			i.add_theme_color_override("font_color", AMBER if active else GREEN)

func _nav_title(key: String) -> String:
	for s in SITES:
		if String(s[0]) == key:
			return String(s[1])
	return ""

func _line(text: String, color: Color = GREEN, size: int = 16) -> Control:
	var l := Ui.label(text, size, color, Ui.font_mono())
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.custom_minimum_size = Vector2(1180, 0)
	return l

func _show(site: String) -> void:
	_active = site
	_clear()
	_title.text = "// " + _nav_title(site)
	Sfx.play("click", -12.0)
	match site:
		"schools":
			_site_schools()
		"phone":
			_site_phone()
		"rules":
			_site_rules()
		"wanted":
			_site_wanted()
		"archive":
			_site_archive()
		"mail":
			_site_mail()
		"exchange":
			_site_exchange()
		"black":
			_site_black()
		"browser":
			_site_browser()
		"achv":
			_site_achv()

func _block(bg: Color = Color(0.06, 0.12, 0.08, 0.8), edge: Color = EDGE) -> VBoxContainer:
	var pc := PanelContainer.new()
	pc.add_theme_stylebox_override("panel", Ui.style(bg, edge, 1, 0, 12))
	pc.custom_minimum_size = Vector2(1180, 0)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 4)
	pc.add_child(vb)
	_body.add_child(pc)
	return vb

func _site_schools() -> void:
	for sch in Data.schools:
		var nm := String(sch.get("name", ""))
		var vb := _block()
		vb.add_child(_line("■ " + nm, AMBER, 18))
		vb.add_child(_line("校长：%s　　教导主任：%s" % [String(sch.get("principal", "")), String(sch.get("dean", ""))], GREEN, 16))
		vb.add_child(_line("总机：%s" % String(Data.phones.get(nm, "——")), DIM, 15))
		vb.add_child(_line("地址：%s" % _address_of(nm), DIM, 15))

func _address_of(school_name: String) -> String:
	var map := {
		"深圳实验中学": "福田区百花六路 7 号",
		"深圳中学": "罗湖区人民北路 66 号",
		"深圳高级中学": "福田区春田路 2 号",
		"深圳外国语学校": "盐田区盐田路 1 号",
		"教育局直属中学": "南山区后海大道 48 号"
	}
	return String(map.get(school_name, "——"))

func _site_phone() -> void:
	_body.add_child(_line("教育局档案核实：%s" % String(Data.phones.get("教育局", "——")), AMBER, 18))
	_body.add_child(_line("纪检部监督举报：%s" % String(Data.phones.get("纪检部", "——")), AMBER, 18))
	_body.add_child(_line("新人培训（仅首日）：%s" % String(Data.phones.get("新人培训", "——")), DIM))
	_body.add_child(_line(""))
	for sch in Data.schools:
		var nm := String(sch.get("name", ""))
		_body.add_child(_line("%s　总机 %s" % [nm, String(Data.phones.get(nm, "——"))]))
	_body.add_child(_line(""))
	_body.add_child(_line("注：号码每日轮换，以当日印刷版为准。", DIM, 14))

func _site_rules() -> void:
	var versions := State.rules_versions()
	for i in versions.size():
		var v: Dictionary = versions[i]
		var active := i == versions.size() - 1
		var vb := _block(Color(0.08, 0.14, 0.1, 0.85) if active else Color(0.04, 0.07, 0.05, 0.7))
		var tag := "　【现行】" if active else "　（已废止）"
		vb.add_child(_line("%s　第 %d 天起%s" % [String(v.get("title", "")), int(v.get("day", 1)), tag], AMBER if active else DIM, 18))
		for l in v.get("lines", []):
			vb.add_child(_line("· " + String(l), GREEN if active else DIM, 15))

func _site_wanted() -> void:
	if State.wanted.is_empty():
		_body.add_child(_line("协查通报：暂无。", DIM, 17))
		return
	_body.add_child(_line("今日协查通报（%d 人）" % State.wanted.size(), RED, 19))
	for w in State.wanted:
		var vb := _block(Color(0.12, 0.06, 0.06, 0.8), Color(0.4, 0.2, 0.18))
		vb.add_child(_line("姓名：%s" % String(w.get("name", "")), GREEN, 18))
		vb.add_child(_line("学号：%s" % String(w.get("id", "")), DIM, 16))
		vb.add_child(_line("处置：拒绝进入；放行者罚款 100 元并记录。", DIM, 14))

func _site_archive() -> void:
	State.db_checked_this = true
	_body.add_child(_line("输入学号或姓名，调阅教育局备案。每次查询计 3 秒。", DIM, 15))
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 10)
	var input := LineEdit.new()
	input.placeholder_text = "学号 / 姓名"
	input.custom_minimum_size = Vector2(420, 44)
	input.add_theme_font_override("font", Ui.font_mono())
	input.add_theme_font_size_override("font_size", 18)
	input.add_theme_color_override("font_color", GREEN)
	input.add_theme_stylebox_override("normal", Ui.style(Color(0.03, 0.07, 0.05), EDGE, 1, 0, 8))
	input.add_theme_stylebox_override("focus", Ui.style(Color(0.05, 0.1, 0.07), AMBER, 1, 0, 8))
	if State.has_upgrade("autoFill") and not visitor.is_empty():
		input.text = String(visitor.get("name", ""))
	row.add_child(input)
	var btn := Ui.button("查询", 16, Color("#12281a"), GREEN)
	btn.custom_minimum_size = Vector2(120, 44)
	btn.pressed.connect(func() -> void: _query_archive(input.text))
	row.add_child(btn)
	_body.add_child(row)
	var result := Ui.rich("", 16, GREEN)
	result.custom_minimum_size = Vector2(1180, 120)
	_body.add_child(result)
	_body.set_meta("result", result)
	input.text_submitted.connect(func(t: String) -> void: _query_archive(t))

func _query_archive(text: String) -> void:
	var q := text.strip_edges()
	var result: RichTextLabel = _body.get_meta("result", null)
	if result == null:
		return
	if q == "":
		result.text = "请输入学号或姓名。"
		return
	time_cost.emit(3.0)
	if visitor.is_empty():
		result.text = "当前无受检人员。"
		return
	var sid := String(visitor.get("student_id", ""))
	var nm := String(visitor.get("name", ""))
	if q == sid:
		var forged: Array = visitor.get("forged_fields", [])
		if forged.has("id"):
			result.text = "[color=#c86a5a]查无此学号。该号段未在教育局备案。[/color]"
		else:
			result.text = "在册：%s　%d 年级　备案照片一致。" % [nm, int(visitor.get("grade", 0))]
	elif q == nm:
		var rec: Dictionary = State.archive.get(nm, {})
		result.text = "姓名：%s\n来访：%d 次\n被拒：%d 次" % [nm, int(rec.get("visits", 0)), int(rec.get("stops", 0))]
	else:
		result.text = "查无记录。"

func _site_mail() -> void:
	if State.mails.is_empty():
		_body.add_child(_line("收件箱为空。", DIM, 17))
		return
	for i in range(State.mails.size() - 1, -1, -1):
		var m: Dictionary = State.mails[i]
		var b := Button.new()
		b.text = "第 %d 天　%s　—　%s" % [int(m.get("day", 0)), String(m.get("from", "")), String(m.get("subject", ""))]
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.custom_minimum_size = Vector2(1180, 40)
		b.focus_mode = Control.FOCUS_NONE
		b.add_theme_font_override("font", Ui.font_mono())
		b.add_theme_font_size_override("font_size", 15)
		b.add_theme_color_override("font_color", GREEN)
		b.add_theme_stylebox_override("normal", Ui.style(Color(0.04, 0.09, 0.06), EDGE, 1, 0, 8))
		b.add_theme_stylebox_override("hover", Ui.style(Color(0.08, 0.16, 0.1), AMBER, 1, 0, 8))
		b.pressed.connect(func() -> void: _show_mail(m))
		_body.add_child(b)
		if String(m.get("kind", "")) == "org":
			var handle := Ui.button("处理这封邮件", 14, Color("#1a2a1a"), AMBER)
			handle.custom_minimum_size = Vector2(240, 34)
			var mid := int(m.get("id", 0))
			handle.pressed.connect(func() -> void: org_requested.emit(mid))
			_body.add_child(handle)

func _show_mail(m: Dictionary) -> void:
	var vb := _block(Color(0.03, 0.07, 0.05))
	vb.add_child(_line("发件人：%s" % String(m.get("from", "")), AMBER, 16))
	vb.add_child(_line("主题：%s" % String(m.get("subject", "")), GREEN, 16))
	vb.add_child(_line(String(m.get("body", "")), GREEN, 15))

func _site_achv() -> void:
	var got := 0
	for a in State.ACHIEVEMENTS:
		var unlocked: bool = State.achievements.has(String(a.key))
		if unlocked:
			got += 1
		var mark := "■" if unlocked else "□"
		var col := GREEN if unlocked else DIM
		_body.add_child(_line("%s %s　—　%s" % [mark, String(a.name), String(a.desc)], col, 16))
	_body.add_child(_line("已解锁 %d / %d" % [got, State.ACHIEVEMENTS.size()], AMBER, 15))

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		closed.emit()


func _site_exchange() -> void:
	if State.stocks.is_empty():
		State._init_market()
	_body.add_child(_line("余额 %d 元　·　%s" % [State.money, State.stock_news], AMBER, 16))
	for i in State.stocks.size():
		var st: Dictionary = State.stocks[i]
		var ch := State.market_change(st)
		var held := 0
		for p in st.positions:
			held += int(p.get("shares", 0))
		var col := GREEN if ch >= 0.0 else RED
		_body.add_child(_line("%-10s %s　现价 %.2f　%+.2f%%　持仓 %d 股" % [String(st.name), String(st.code), float(st.price), ch, held], col, 16))

	var trade := HBoxContainer.new()
	trade.add_theme_constant_override("separation", 8)
	var stock_opt := OptionButton.new()
	for st in State.stocks:
		stock_opt.add_item("%s %s" % [String(st.name), String(st.code)])
	stock_opt.custom_minimum_size = Vector2(220, 40)
	trade.add_child(stock_opt)
	var lev_opt := OptionButton.new()
	for lv in [1, 2, 3, 5]:
		lev_opt.add_item("%dx" % lv)
	lev_opt.custom_minimum_size = Vector2(90, 40)
	trade.add_child(lev_opt)
	var price_in := LineEdit.new()
	price_in.placeholder_text = "价格"
	price_in.custom_minimum_size = Vector2(110, 40)
	price_in.text = "%.2f" % float(State.stocks[0].price)
	trade.add_child(price_in)
	var shares_in := LineEdit.new()
	shares_in.placeholder_text = "数量(10股/份)"
	shares_in.custom_minimum_size = Vector2(140, 40)
	shares_in.text = "10"
	trade.add_child(shares_in)
	for ctrl in [stock_opt, lev_opt]:
		ctrl.add_theme_color_override("font_color", GREEN)
		ctrl.add_theme_stylebox_override("normal", Ui.style(Color(0.05, 0.1, 0.07), EDGE, 1, 0, 6))
		ctrl.add_theme_stylebox_override("hover", Ui.style(Color(0.07, 0.13, 0.09), AMBER, 1, 0, 6))
		ctrl.add_theme_stylebox_override("pressed", Ui.style(Color(0.07, 0.13, 0.09), AMBER, 1, 0, 6))
	for ctrl in [price_in, shares_in]:
		ctrl.add_theme_font_override("font", Ui.font_mono())
		ctrl.add_theme_font_size_override("font_size", 16)
		ctrl.add_theme_color_override("font_color", GREEN)
		ctrl.add_theme_stylebox_override("normal", Ui.style(Color(0.05, 0.1, 0.07), EDGE, 1, 0, 6))
	var buy := Ui.button("买入", 15, Color("#12281a"), GREEN)
	buy.custom_minimum_size = Vector2(100, 40)
	trade.add_child(buy)
	_body.add_child(trade)

	stock_opt.item_selected.connect(func(idx: int) -> void:
		if State.has_upgrade("autoTrade"):
			price_in.text = "%.2f" % float(State.stocks[idx].price)
			shares_in.text = "10"
	)
	buy.pressed.connect(func() -> void:
		var idx := stock_opt.selected
		var lev: int = [1, 2, 3, 5][lev_opt.selected]
		var price := float(price_in.text)
		var shares := int(shares_in.text)
		if price < 0.5 or shares <= 0:
			_status.text = "价格或数量无效。"
			return
		var res := State.buy_stock(idx, shares, lev, price)
		_status.text = String(res.get("msg", ""))
		_show("exchange")
	)

	_body.add_child(_line("持仓", AMBER, 17))
	var any := false
	for i in State.stocks.size():
		var st: Dictionary = State.stocks[i]
		for j in st.positions.size():
			var pos: Dictionary = st.positions[j]
			any = true
			var pnl := State.position_pnl(st, pos)
			var row := HBoxContainer.new()
			row.add_theme_constant_override("separation", 12)
			var lab := Ui.label("%s　%d 股 @ %.2f　%dx　浮动 %+.2f" % [String(st.name), int(pos.shares), float(pos.buy), int(pos.leverage), pnl], 15, GREEN if pnl >= 0.0 else RED, Ui.font_mono())
			lab.custom_minimum_size = Vector2(760, 30)
			row.add_child(lab)
			var sell := Ui.button("卖出", 14, Color("#12281a"), GREEN)
			sell.custom_minimum_size = Vector2(90, 32)
			var si: int = i
			var sj: int = j
			sell.pressed.connect(func() -> void:
				State.sell_stock(si, sj, float(State.stocks[si].price))
				_show("exchange")
			)
			row.add_child(sell)
			_body.add_child(row)
	if not any:
		_body.add_child(_line("暂无持仓。", DIM, 15))
	_body.add_child(_line("保证金 = 价 × 股数 ÷ 杠杆；亏损吞掉保证金即强制平仓。", DIM, 14))


func _site_black() -> void:
	if State.day < 20:
		_body.add_child(_line("黑市尚未开张。第 20 天后再来。", DIM, 17))
		return
	_body.add_child(_line("校园东侧 · 旧器材室 · 现金交易，不问来路", AMBER, 16))
	_body.add_child(_line("余额 %d 元" % State.money, GREEN, 15))
	var items := [
		["fake_id", "伪造介绍信", 50, "一套足以骗过新学校的介绍信，字迹是仿的。"],
		["ticket", "高铁票", 100, "深圳北 → 衡水北。后天 05:40，站票。"]
	]
	for it in items:
		var key := String(it[0])
		var owned: bool = State.has_fake_id if key == "fake_id" else State.has_ticket
		var vb := _block(Color(0.07, 0.1, 0.08, 0.85))
		vb.add_child(_line("%s　—　%d 元%s" % [String(it[1]), int(it[2]), "（已购买）" if owned else ""], GREEN if not owned else DIM, 17))
		vb.add_child(_line(String(it[3]), DIM, 14))
		if not owned:
			var b := Ui.button("购买", 15, Color("#12281a"), GREEN)
			b.custom_minimum_size = Vector2(160, 38)
			var price := int(it[2])
			b.pressed.connect(func() -> void:
				if State.money < price:
					_status.text = "钱不够。"
					return
				State.money -= price
				if key == "fake_id":
					State.has_fake_id = true
				else:
					State.has_ticket = true
				_status.text = "成交。东西在器材室第三排柜子里。"
				Sfx.play("paper", -12.0)
				_show("black")
			)
			vb.add_child(b)
	_body.add_child(_line("逃出去还差一封正常的转学介绍信——得顶着 25 元罚款，从检查站里收走。", DIM, 14))

func _site_browser() -> void:
	_body.add_child(_line("校门检查站 · 内部浏览器", AMBER, 16))
	_body.add_child(_line("书签栏：%s" % ("教育局档案" if State.has_upgrade("fastBookmark") else "（未购买快速收藏夹）"), DIM, 14))
	var sites := [
		["archive", "教育局档案", "调阅学生备案，准确但慢"],
		["schools", "学校信息库", "校长与教导主任名单"],
		["rules", "准入规定", "今日核验项目"]
	]
	for s in sites:
		var b := Ui.button("%s　—　%s" % [String(s[1]), String(s[2])], 16, Color("#12281a"), GREEN)
		b.custom_minimum_size = Vector2(520, 44)
		var key := String(s[0])
		b.pressed.connect(func() -> void:
			await _loading("正在打开 %s ……" % String(s[1]), 0.5 if State.has_upgrade("fastNet") else 1.0)
			_show(key)
		)
		_body.add_child(b)




func _loading(text: String, seconds: float) -> void:
	var bar := ProgressBar.new()
	bar.custom_minimum_size = Vector2(600, 14)
	bar.max_value = 1.0
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.4), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(GREEN, Color(0, 0, 0, 0), 0, 0, 0))
	_body.add_child(_line(text, AMBER, 15))
	_body.add_child(bar)
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, seconds)
	await get_tree().create_timer(seconds, true).timeout
	if is_instance_valid(bar):
		bar.queue_free()
