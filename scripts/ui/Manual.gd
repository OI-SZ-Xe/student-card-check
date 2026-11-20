class_name Manual
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal closed

var _pages: Array = []
var _index := 0
var _body: VBoxContainer = null
var _title: Label = null
var _page_label: Label = null
var _index_box: VBoxContainer = null

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_pages = Data.manual

	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.05, 0.04, 0.72)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	var book := Ui.panel(Color("#e2d6b4"), Color("#8d7c52"), 3, 1, 0)
	book.position = Vector2(250, 120)
	book.size = Vector2(1420, 840)
	add_child(book)

	var spine := ColorRect.new()
	spine.color = Color(0.35, 0.28, 0.18, 0.35)
	spine.position = Vector2(330, 24)
	spine.size = Vector2(3, 792)
	book.add_child(spine)

	var head := Ui.label("校门检查员仿真手册", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(30, 20)
	head.size = Vector2(500, 40)
	book.add_child(head)
	var edition := Ui.label("学生会纪检部 编印 · 2026 年 3 月修订 · 内部资料", 12, Ui.INK_SOFT, Ui.font_mono())
	edition.position = Vector2(30, 58)
	edition.size = Vector2(600, 18)
	book.add_child(edition)

	var scroll := ScrollContainer.new()
	scroll.position = Vector2(24, 96)
	scroll.size = Vector2(300, 660)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	book.add_child(scroll)
	_index_box = VBoxContainer.new()
	_index_box.add_theme_constant_override("separation", 4)
	_index_box.custom_minimum_size = Vector2(290, 0)
	scroll.add_child(_index_box)

	var line := ColorRect.new()
	line.color = Color(0.35, 0.28, 0.18, 0.3)
	line.position = Vector2(344, 96)
	line.size = Vector2(2, 660)
	book.add_child(line)

	_title = Ui.label("", 22, Ui.INK, Ui.font_serif())
	_title.position = Vector2(372, 88)
	_title.size = Vector2(1000, 30)
	book.add_child(_title)

	var cscroll := ScrollContainer.new()
	cscroll.position = Vector2(372, 126)
	cscroll.size = Vector2(1020, 600)
	cscroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	book.add_child(cscroll)
	_body = VBoxContainer.new()
	_body.add_theme_constant_override("separation", 10)
	_body.custom_minimum_size = Vector2(1000, 0)
	cscroll.add_child(_body)

	var prev := Ui.button("上一页", 16, Ui.INK_SOFT, Ui.PAPER)
	prev.position = Vector2(372, 742)
	prev.size = Vector2(140, 44)
	prev.pressed.connect(func() -> void: _go(-1))
	book.add_child(prev)
	var next := Ui.button("下一页", 16, Ui.INK_SOFT, Ui.PAPER)
	next.position = Vector2(524, 742)
	next.size = Vector2(140, 44)
	next.pressed.connect(func() -> void: _go(1))
	book.add_child(next)
	_page_label = Ui.label("", 14, Ui.INK_SOFT, Ui.font_mono())
	_page_label.position = Vector2(684, 754)
	_page_label.size = Vector2(200, 20)
	book.add_child(_page_label)

	var close := Ui.button("合上手册 (Esc)", 16, Ui.INK, Ui.PAPER)
	close.position = Vector2(1180, 742)
	close.size = Vector2(210, 44)
	close.pressed.connect(func() -> void: closed.emit())
	book.add_child(close)

	_build_index()
	_show(0)

func _build_index() -> void:
	for c in _index_box.get_children():
		c.queue_free()
	for i in _pages.size():
		var b := Button.new()
		b.text = String(_pages[i].get("title", "第 %d 页" % (i + 1)))
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.focus_mode = Control.FOCUS_NONE
		b.custom_minimum_size = Vector2(286, 40)
		b.add_theme_font_override("font", Ui.font_serif())
		b.add_theme_font_size_override("font_size", 15)
		b.add_theme_color_override("font_color", Ui.INK)
		b.add_theme_color_override("font_hover_color", Ui.RED)
		b.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 2, 8))
		b.add_theme_stylebox_override("hover", Ui.style(Color(0.35, 0.28, 0.18, 0.12), Color(0, 0, 0, 0), 0, 2, 8))
		b.add_theme_stylebox_override("focus", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
		var idx := i
		b.pressed.connect(func() -> void: _show(idx))
		_index_box.add_child(b)

func _go(delta: int) -> void:
	_show(clampi(_index + delta, 0, _pages.size() - 1))

func _show(idx: int) -> void:
	if _pages.is_empty():
		return
	_index = clampi(idx, 0, _pages.size() - 1)
	var page: Dictionary = _pages[_index]
	_title.text = String(page.get("title", ""))
	_page_label.text = "%d / %d" % [_index + 1, _pages.size()]
	for c in _body.get_children():
		c.queue_free()
	Sfx.play("paper", -14.0)
	var kind := String(page.get("type", "text"))
	match kind:
		"text":
			_body.add_child(_para(String(page.get("body", ""))))
		"steps":
			for item in page.get("items", []):
				_body.add_child(_bullet(String(item)))
		"table":
			_body.add_child(_table(page))
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		"signatures":
			_body.add_child(_signatures())
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		"phones":
			_body.add_child(_phones())
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		"endings":
			_body.add_child(_endings())
		"achv":
			_body.add_child(_achv())
		"forgery":
			_body.add_child(_forgery())
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		"upgrades":
			_body.add_child(_upgrades())
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		_:
			_body.add_child(_para("本页暂未编入。"))

func _para(text: String) -> Control:
	var r := Ui.rich(text, 17, Ui.INK)
	r.custom_minimum_size = Vector2(1000, 0)
	return r

func _bullet(text: String) -> Control:
	return _para("· " + text)

func _note(text: String) -> Control:
	var r := Ui.rich(text, 14, Ui.INK_SOFT)
	r.custom_minimum_size = Vector2(1000, 0)
	return r

func _cell(text: String, header: bool, width: int) -> Panel:
	var p := Ui.panel(Color(0.4, 0.33, 0.2, 0.16) if header else Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.28), 1, 0, 8)
	p.custom_minimum_size = Vector2(width, 40)
	var l := Ui.label(text, 15, Ui.INK if header else Ui.INK_SOFT, Ui.font_serif() if header else Ui.font_mono())
	l.position = Vector2(10, 9)
	l.size = Vector2(width - 20, 22)
	l.autowrap_mode = TextServer.AUTOWRAP_ARBITRARY
	l.clip_text = true
	p.add_child(l)
	return p

func _table(page: Dictionary) -> Control:
	var head: Array = page.get("head", [])
	var cols := maxi(1, head.size())
	var col_w := int(980.0 / float(cols))
	var grid := GridContainer.new()
	grid.columns = cols
	grid.add_theme_constant_override("h_separation", 2)
	grid.add_theme_constant_override("v_separation", 2)
	for h in head:
		grid.add_child(_cell(String(h), true, col_w))
	for row in page.get("rows", []):
		for cell in row:
			grid.add_child(_cell(String(cell), false, col_w))
	return grid

func _signatures() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	for sch in Data.schools:
		for role in ["principal", "dean"]:
			var sig_key := "sig" if role == "principal" else "dean_sig"
			var sid := String(sch.get(sig_key, ""))
			var data := Data.sig(sid)
			if data.is_empty():
				continue
			var row := Ui.panel(Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.2), 1, 0, 10)
			row.custom_minimum_size = Vector2(1000, 104)
			var sig := Signature.new()
			sig.setup(data, 1.0)
			sig.position = Vector2(8, 4)
			sig.size = Vector2(268, 92)
			row.add_child(sig)
			var role_cn := "校长" if role == "principal" else "教导主任"
			var nm := Ui.label("%s　%s　%s" % [String(data.get("name", "")), role_cn, String(sch.get("name", ""))], 18, Ui.INK, Ui.font_serif())
			nm.position = Vector2(296, 14)
			nm.size = Vector2(520, 24)
			row.add_child(nm)
			var st := Ui.label(String(data.get("style", "")), 13, Ui.INK_SOFT, Ui.font_serif())
			st.position = Vector2(296, 42)
			st.size = Vector2(640, 40)
			st.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			row.add_child(st)
			var ink := Ui.label("墨色 %s" % String(data.get("ink", "")), 11, Ui.INK_SOFT, Ui.font_mono())
			ink.position = Vector2(296, 80)
			ink.size = Vector2(220, 18)
			row.add_child(ink)
			box.add_child(row)
	return box

func _phones() -> Control:
	var box := VBoxContainer.new()
	for key in Data.phones.keys():
		var row := Ui.label("%s　%s" % [String(key), String(Data.phones[key])], 17, Ui.INK, Ui.font_mono())
		box.add_child(row)
	return box

func _upgrades() -> Control:
	var box := VBoxContainer.new()
	for u in Data.upgrades:
		var owned := State.has_upgrade(String(u.get("id", "")))
		var row := Ui.rich("[b]%s[/b]　%d 元%s\n%s\n" % [String(u.get("name", "")), int(u.get("price", 0)), "（已装备）" if owned else "", String(u.get("desc", ""))], 15, Ui.INK)
		row.custom_minimum_size = Vector2(1000, 0)
		box.add_child(row)
	return box


func _forgery() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	var variants := [
		["", "真迹：墨色均匀，压痕连续"],
		["_miss", "缺笔：第三笔断裂，断口整齐"],
		["_light", "浅墨：墨色偏灰，网点稀疏"],
		["_plain", "无钢印：纸面无凸起压痕"],
		["_mirror", "镜像：字形左右相反"]
	]
	for item in variants:
		var row := Ui.panel(Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.2), 1, 0, 8)
		row.custom_minimum_size = Vector2(1000, 96)
		var path := "res://art/signatures/wang_ming%s.png" % String(item[0])
		if ResourceLoader.exists(path):
			var sg := Signature.new()
			sg.setup({"img": path}, 1.0)
			sg.position = Vector2(8, 4)
			sg.size = Vector2(240, 84)
			row.add_child(sg)
		var l := Ui.label(String(item[1]), 15, Ui.INK, Ui.font_serif())
		l.position = Vector2(272, 34)
		l.size = Vector2(700, 26)
		row.add_child(l)
		box.add_child(row)
	return box


func _endings() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	var rows := [
		["debt", "负债", "任意一天余额低于 0 元，立即隔离审查。"],
		["corrupt", "腐败", "收受贿赂累计 3 次，被移交司法机关。"],
		["escape", "逃亡", "第 25 天后，手上有正常的转学介绍信、伪造介绍信与高铁票，顶栏出现「启动逃亡」。"],
		["revolution", "革命", "帮助学生斗争委员会累计 5 次以上，终局未向他们开枪。"],
		["gun", "忠诚·枪毙", "帮助过组织但没到 5 次，或怀疑度过高，终局被校园安全部带走。"],
		["stable", "忠诚·平稳", "一次没帮组织、拒签达标、怀疑度低，继续担任科员。"]
	]
	for r in rows:
		var got: bool = State.endings_seen.has(String(r[0]))
		var tag := "　【已解锁】" if got else "　【未解锁】"
		var item := _para("[b]%s[/b]%s\n%s" % [String(r[1]), tag, String(r[2])])
		box.add_child(item)
	return box

func _achv() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	for a in State.ACHIEVEMENTS:
		var got: bool = State.achievements.has(String(a.key))
		var line := "%s　%s　—　%s" % ["■" if got else "□", String(a.name), String(a.desc)]
		box.add_child(_para(line))
	return box