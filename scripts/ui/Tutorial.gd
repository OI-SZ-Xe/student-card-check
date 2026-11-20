class_name Tutorial
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal finished

var _page := 0
var _title: Label
var _body: RichTextLabel
var _dots: Label
var _art: Control
var _next: Button
var _bar: ProgressBar

const PAGES := [
	["一 · 窗口", "学生站在玻璃后面。先把证件拿到面前：点一下证件，或直接点它。\n\n证件上的姓名、学校、有效期，都可能和系统里的档案对不上。"],
	["二 · 核对", "右边是《今日核验项目》，写着今天该查哪几项。\n\n点「对照模式」打开并排比对：绿点一致，红点对不上。"],
	["三 · 工具", "放大镜看字迹和照片边缘，紫外灯照防伪，电话向学校核实，手册写着全部规定。\n\n每用一次工具都要花时间——一天只有 600 秒。"],
	["四 · 印章", "核对完选一枚印章：允许、拒绝，或者逮捕。\n\n选完印章再点证件，章才盖下去。盖错要扣钱。"],
	["五 · 目标", "撑过 30 天。别欠钱，别收太多钱，也别把学生打得太狠。\n\n第 12、19、26、30 天会有事情发生——那时候，枪在你手里。"]
]

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.8)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 30)
	paper.position = Vector2(380, 150)
	paper.size = Vector2(1160, 780)
	add_child(paper)
	_title = Ui.label("", 30, Ui.INK, Ui.font_serif())
	_title.position = Vector2(40, 30)
	_title.size = Vector2(700, 40)
	paper.add_child(_title)
	_body = Ui.rich("", 18, Ui.INK)
	_body.position = Vector2(40, 100)
	_body.size = Vector2(600, 420)
	_body.scroll_active = false
	paper.add_child(_body)
	_art = Control.new()
	_art.position = Vector2(700, 110)
	_art.size = Vector2(420, 430)
	paper.add_child(_art)
	_dots = Ui.label("", 14, Ui.INK_SOFT, Ui.font_mono())
	_dots.position = Vector2(40, 560)
	_dots.size = Vector2(300, 20)
	paper.add_child(_dots)
	var prev := Ui.button("上一步", 17, Ui.PAPER_DARK, Ui.INK)
	prev.position = Vector2(40, 600)
	prev.size = Vector2(150, 48)
	prev.pressed.connect(func() -> void: _go(-1))
	paper.add_child(prev)
	_next = Ui.button("下一步", 17, Ui.INK, Ui.PAPER)
	_next.position = Vector2(210, 600)
	_next.size = Vector2(190, 48)
	_next.pressed.connect(func() -> void:
		if _page >= PAGES.size() - 1:
			finished.emit()
		else:
			_go(1)
	)
	paper.add_child(_next)
	var skip := Ui.button("跳过", 16, Color(0, 0, 0, 0), Ui.INK_SOFT)
	skip.position = Vector2(980, 600)
	skip.size = Vector2(120, 48)
	skip.pressed.connect(func() -> void: finished.emit())
	paper.add_child(skip)
	var hint := Ui.label("随时可以跳过；之后在台账里点「教学」能再看。", 13, Ui.INK_SOFT, Ui.font_mono())
	hint.position = Vector2(40, 668)
	hint.size = Vector2(760, 20)
	paper.add_child(hint)
	var bar := ProgressBar.new()
	bar.position = Vector2(40, 520)
	bar.size = Vector2(600, 10)
	bar.max_value = PAGES.size()
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.12), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(Color("#a57c2a"), Color(0, 0, 0, 0), 0, 0, 0))
	paper.add_child(bar)
	_bar = bar
	_show_page(0)

func _go(delta: int) -> void:
	_show_page(clampi(_page + delta, 0, PAGES.size() - 1))

func _show_page(i: int) -> void:
	_page = i
	_title.text = String(PAGES[i][0])
	_body.text = String(PAGES[i][1])
	_dots.text = "第 %d / %d 页" % [i + 1, PAGES.size()]
	_next.text = "开始执勤" if i == PAGES.size() - 1 else "下一步"
	if _bar != null:
		_bar.value = i + 1
	for c in _art.get_children():
		c.queue_free()
	_build_art(i)

func _rect(x: int, y: int, w: int, h: int, col: Color) -> ColorRect:
	var r := ColorRect.new()
	r.position = Vector2(x, y)
	r.size = Vector2(w, h)
	r.color = col
	_art.add_child(r)
	return r

func _tex(path: String, x: int, y: int, w: int, h: int) -> void:
	if not ResourceLoader.exists(path):
		return
	var t := TextureRect.new()
	t.texture = load(path)
	t.position = Vector2(x, y)
	t.size = Vector2(w, h)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_art.add_child(t)

func _build_art(i: int) -> void:
	match i:
		0:
			_rect(20, 20, 290, 260, Color("#39443f"))
			_rect(34, 34, 262, 200, Color("#4d5f54"))
			_rect(34, 240, 262, 12, Color("#2b332e"))
			_rect(120, 90, 60, 60, Color("#2b332e"))
			_rect(104, 150, 92, 84, Color("#2b332e"))
			var card := ColorRect.new()
			card.color = Color("#e4dbc2")
			card.position = Vector2(196, 128)
			card.size = Vector2(86, 116)
			card.rotation = -0.2
			_art.add_child(card)
		1:
			_rect(10, 40, 140, 190, Color("#e4dbc2"))
			_rect(180, 40, 140, 190, Color("#e4dbc2"))
			_rect(20, 52, 120, 12, Color("#8d7c52"))
			_rect(190, 52, 120, 12, Color("#8d7c52"))
			for k in 4:
				_rect(20, 80 + k * 26, 110, 6, Color("#b9ad8c"))
				_rect(190, 80 + k * 26, 110, 6, Color("#b9ad8c"))
			_rect(140, 250, 16, 16, Color("#2f7a44"))
			_rect(160, 250, 16, 16, Color("#2f7a44"))
			_rect(180, 250, 16, 16, Color("#a6301f"))
		2:
			_tex("res://art/icons/compare.png", 0, 20, 56, 56)
			_tex("res://art/icons/magnifier.png", 66, 20, 56, 56)
			_tex("res://art/icons/uv.png", 132, 20, 56, 56)
			_tex("res://art/icons/phone.png", 198, 20, 56, 56)
			_tex("res://art/icons/book.png", 264, 20, 56, 56)
			_rect(0, 110, 320, 24, Color(0, 0, 0, 0.18))
			_rect(0, 110, 210, 24, Color("#a57c2a"))
		3:
			_tex("res://art/props/stamp_green.png", 0, 20, 160, 100)
			_tex("res://art/props/stamp_red.png", 170, 20, 160, 100)
			_rect(40, 170, 240, 70, Color(0, 0, 0, 0))
			var stamp := Ui.panel(Color(0, 0, 0, 0), Color(0.65, 0.16, 0.12, 0.8), 4, 2, 0)
			stamp.position = Vector2(74, 176)
			stamp.size = Vector2(172, 64)
			stamp.rotation = -0.12
			_art.add_child(stamp)
			var lab := Ui.label("拒 绝", 26, Color(0.65, 0.16, 0.12), Ui.font_serif())
			lab.position = Vector2(0, 16)
			lab.size = Vector2(172, 32)
			lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			stamp.add_child(lab)
		4:
			for d in 30:
				var col := d % 6
				var row := d / 6
				var is_event: bool = (d + 1) in [12, 19, 26, 30]
				_rect(col * 50, row * 44, 40, 34, Color("#a6301f") if is_event else Color("#cfc4a4"))
				var l := Ui.label(str(d + 1), 12, Color("#e4dbc2") if is_event else Color("#4c5257"), Ui.font_mono())
				l.position = Vector2(col * 50 + 4, row * 44 + 4)
				l.size = Vector2(32, 18)
				_art.add_child(l)