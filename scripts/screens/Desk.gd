class_name Desk
extends Control

var skip_briefing := false
var _briefing_open := false
var _reader_btn: Control = null

var card: CardView = null
var _win_portrait: Portrait = null
var _win_name: Label = null
var _win_school: Label = null
var _win_dialogue: Label = null
var _win_archive: Label = null
var _msg_label: Label = null
var _time_label: Label = null
var _money_label: Label = null
var _day_label: Label = null
var _date_label: Label = null
var _quota_label: Label = null
var _queue_label: Label = null
var _rules_box: VBoxContainer = null
var _stats_label: Label = null
var _next_btn: Button = null
var _stamp_approve: Button = null
var _stamp_reject: Button = null
var _compare_btn: Button = null
var _magnify_btn: Button = null
var _uv_btn: Button = null

var _pending := ""
var _compare_mode := false
var _first_field := ""
var _paused := false
var _visitor: Dictionary = {}
var _principals: Dictionary = {}
var _awaiting_next := false
var _called_this := false
var _db_checked_this := false
var _ending_active := false

const HEADLINES := [
	"教育局重申：校园安全是本年度的第一要务。",
	"本市五校联合开展'平安校门'专项行动。",
	"学生会对检查站工作表示肯定，呼吁同学配合。",
	"春季流感高发，健康证明查验将更加严格。",
	"有家长反映校门通行效率偏低，校方表示将增派人手。"
]

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_build_principals()
	_build()
	State.start_day()
	VisitorFactory.forgery_bonus = State.forgery_bonus
	Music.play("bgm_day", 2.0)
	Music.ambience("amb_rain" if State.day % 5 == 0 else "amb_room")
	_refresh_hud()
	if skip_briefing:
		_begin_shift()
	else:
		_show_briefing()

func _build_principals() -> void:
	_principals.clear()
	for s in Data.schools:
		_principals[String(s.get("name", ""))] = String(s.get("dean", s.get("principal", "")))

func _build() -> void:
	var bg := ColorRect.new()
	bg.color = Ui.DESK_DARK
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)

	var desk := TextureRect.new()
	desk.texture = load("res://art/tex/desk.png")
	desk.stretch_mode = TextureRect.STRETCH_TILE
	desk.position = Vector2(0, 452)
	desk.size = Vector2(1920, 628)
	desk.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(desk)
	var edge := ColorRect.new()
	edge.color = Color(0.55, 0.5, 0.36, 0.35)
	edge.position = Vector2(0, 452)
	edge.size = Vector2(1920, 3)
	edge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(edge)

	_build_hud()
	_build_window()
	_build_monitor()
	_build_desk_items()
	_build_stamps()

	_build_right_panel()
	_build_message_bar()

func _build_hud() -> void:
	var bar := ColorRect.new()
	bar.color = Color(0.08, 0.09, 0.08)
	bar.position = Vector2(0, 0)
	bar.size = Vector2(1920, 38)
	add_child(bar)
	_day_label = Ui.label("", 18, Ui.WHITE, Ui.font_mono())
	_day_label.position = Vector2(24, 8)
	_day_label.size = Vector2(140, 22)
	add_child(_day_label)
	_date_label = Ui.label("", 17, Color(Ui.WHITE, 0.8), Ui.font_mono())
	_date_label.position = Vector2(180, 8)
	_date_label.size = Vector2(320, 22)
	add_child(_date_label)
	_time_label = Ui.label("", 18, Color("#d8c07a"), Ui.font_mono())
	_time_label.position = Vector2(520, 8)
	_time_label.size = Vector2(140, 22)
	add_child(_time_label)
	_money_label = Ui.label("", 18, Color("#a8d08a"), Ui.font_mono())
	_money_label.position = Vector2(670, 8)
	_money_label.size = Vector2(160, 22)
	add_child(_money_label)
	_quota_label = Ui.label("", 16, Color("#e0a080"), Ui.font_mono())
	_quota_label.position = Vector2(860, 9)
	_quota_label.size = Vector2(300, 22)
	add_child(_quota_label)
	var right := Ui.label("纪检部科员　%s　%s" % [State.player_name, State.player_class], 16, Color(Ui.WHITE, 0.7), Ui.font_mono())
	right.position = Vector2(1620, 9)
	right.size = Vector2(280, 22)
	right.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	add_child(right)

func _build_window() -> void:
	var win := Ui.panel(Color("#26302a"), Color("#5a6b58"), 3, 2, 0)
	win.position = Vector2(40, 44)
	win.size = Vector2(820, 400)
	add_child(win)
	var glass := TextureRect.new()
	glass.texture = load("res://art/props/corridor.png")
	glass.stretch_mode = TextureRect.STRETCH_SCALE
	glass.position = Vector2(14, 14)
	glass.size = Vector2(792, 372)
	glass.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.clip_contents = true
	win.add_child(glass)
	var phase := int((State.day - 1) / 10)
	var tint_col := Color(0.12, 0.20, 0.17, 0.35)
	if phase == 1:
		tint_col = Color(0.20, 0.18, 0.10, 0.30)
	elif phase >= 2:
		tint_col = Color(0.08, 0.12, 0.20, 0.40)
	var tint := ColorRect.new()
	tint.color = tint_col
	tint.position = Vector2.ZERO
	tint.size = Vector2(792, 372)
	tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(tint)
	var flick := create_tween()
	flick.set_loops()
	flick.tween_property(tint, "color:a", 0.28, 3.4).set_trans(Tween.TRANS_SINE)
	flick.tween_property(tint, "color:a", 0.38, 3.4).set_trans(Tween.TRANS_SINE)
	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.04, 0.03, 0.45)
	shade.position = Vector2(266, 0)
	shade.size = Vector2(526, 372)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(shade)
	if State.day % 5 == 0:
		var rain := TextureRect.new()
		rain.texture = load("res://art/props/rain.png")
		rain.stretch_mode = TextureRect.STRETCH_TILE
		rain.position = Vector2.ZERO
		rain.size = Vector2(792, 372)
		rain.modulate = Color(1, 1, 1, 0.55)
		rain.mouse_filter = Control.MOUSE_FILTER_IGNORE
		glass.add_child(rain)
		var drift := create_tween()
		drift.set_loops()
		drift.tween_property(rain, "position:x", -8.0, 1.2).set_trans(Tween.TRANS_LINEAR)
		drift.tween_property(rain, "position:x", 0.0, 0.001)

	var queue_tex := TextureRect.new()
	queue_tex.texture = load("res://art/props/queue.png")
	queue_tex.position = Vector2(500, 150)
	queue_tex.size = Vector2(260, 148)
	queue_tex.modulate = Color(1.25, 1.25, 1.25, 1.0)
	queue_tex.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(queue_tex)
	var bob := create_tween()
	bob.set_loops()
	bob.tween_property(queue_tex, "position:y", 211.0, 2.4).set_trans(Tween.TRANS_SINE)
	bob.tween_property(queue_tex, "position:y", 208.0, 2.4).set_trans(Tween.TRANS_SINE)

	_win_portrait = Portrait.new()
	_win_portrait.position = Vector2(30, 34)
	_win_portrait.size = Vector2(240, 320)
	glass.add_child(_win_portrait)
	_win_name = Ui.label("", 30, Color("#e9e3cb"), Ui.font_serif())
	_win_name.position = Vector2(292, 40)
	_win_name.size = Vector2(460, 36)
	glass.add_child(_win_name)
	_win_school = Ui.label("", 17, Color("#9fb094"), Ui.font_serif())
	_win_school.position = Vector2(292, 78)
	_win_school.size = Vector2(460, 24)
	glass.add_child(_win_school)
	_win_dialogue = Ui.label("", 18, Color("#d5cfb6"), Ui.font_serif())
	_win_dialogue.position = Vector2(292, 120)
	_win_dialogue.size = Vector2(480, 130)
	_win_dialogue.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	glass.add_child(_win_dialogue)
	_win_archive = Ui.label("", 14, Color("#8a9a82"), Ui.font_mono())
	_win_archive.position = Vector2(292, 264)
	_win_archive.size = Vector2(480, 22)
	glass.add_child(_win_archive)
	var lamp := Ui.label("●", 20, Color(0.6, 0.75, 0.5, 0.8), Ui.font_mono())
	lamp.position = Vector2(748, 14)
	lamp.size = Vector2(30, 26)
	glass.add_child(lamp)

	var frame_col := Color("#39443c")
	for r in [Rect2(0, 0, 792, 12), Rect2(0, 360, 792, 12), Rect2(0, 0, 12, 372), Rect2(780, 0, 12, 372)]:
		var bar := ColorRect.new()
		bar.color = frame_col
		bar.position = r.position
		bar.size = r.size
		glass.add_child(bar)
	var mullion := ColorRect.new()
	mullion.color = frame_col
	mullion.position = Vector2(282, 12)
	mullion.size = Vector2(6, 348)
	glass.add_child(mullion)
	var transom := ColorRect.new()
	transom.color = frame_col
	transom.position = Vector2(12, 268)
	transom.size = Vector2(768, 6)
	glass.add_child(transom)
	var plate := Ui.label("检 查 站　07", 13, Color("#8d9a86"), Ui.font_serif())
	plate.position = Vector2(320, 286)
	plate.size = Vector2(200, 20)
	glass.add_child(plate)
	for i in 5:
		var dot := ColorRect.new()
		dot.color = Color(0.55, 0.6, 0.5, 0.35)
		dot.position = Vector2(700 + i * 10, 322)
		dot.size = Vector2(4, 10)
		glass.add_child(dot)
	var reflection := ColorRect.new()
	reflection.color = Color(1, 1, 1, 0.045)
	reflection.position = Vector2(60, 20)
	reflection.size = Vector2(120, 340)
	reflection.rotation = -0.18
	glass.add_child(reflection)

func _build_monitor() -> void:
	var mon := Ui.panel(Color("#191d18"), Color("#4a5444"), 3, 2, 0)
	mon.position = Vector2(900, 44)
	mon.size = Vector2(980, 400)
	add_child(mon)
	var title := Ui.label("教 育 局 办 公 系 统　v3.1", 15, Color("#9ab08c"), Ui.font_mono())
	title.position = Vector2(20, 14)
	title.size = Vector2(600, 20)
	mon.add_child(title)
	var line := ColorRect.new()
	line.color = Color(0.3, 0.36, 0.28)
	line.position = Vector2(20, 38)
	line.size = Vector2(940, 2)
	mon.add_child(line)
	var subtitle := Ui.label("NODE 07 · 校门检查站 · 在册人员 1,284 · 今日授权 %d 人" % 8, 12, Color("#6f8068"), Ui.font_mono())
	subtitle.position = Vector2(20, 46)
	subtitle.size = Vector2(900, 18)
	mon.add_child(subtitle)

	var rules_title := Ui.label("今日核验项目", 17, Color("#d8d2b8"), Ui.font_serif())
	rules_title.position = Vector2(24, 76)
	rules_title.size = Vector2(300, 24)
	mon.add_child(rules_title)
	_rules_box = VBoxContainer.new()
	_rules_box.position = Vector2(24, 106)
	_rules_box.size = Vector2(560, 260)
	_rules_box.add_theme_constant_override("separation", 6)
	mon.add_child(_rules_box)

	_queue_label = Ui.label("", 15, Color("#9ab08c"), Ui.font_mono())
	_queue_label.position = Vector2(620, 80)
	_queue_label.size = Vector2(340, 24)
	mon.add_child(_queue_label)
	var tip := Ui.rich("[color=#7f8f78]检查流程[/color]\n1. 拖动证件查看全部字段\n2. 点击「对照」逐项比对\n3. 选印章，点击证件盖下\n4. 喊下一位\n\n[color=#7f8f78]键盘[/color]\nA 通过　R 拒绝　N 下一位\nC 对照　M 手册　P 电话", 13, Color("#c9c3ab"))
	tip.position = Vector2(620, 116)
	tip.size = Vector2(336, 260)
	tip.scroll_active = false
	mon.add_child(tip)

func _build_desk_items() -> void:
	card = CardView.new()
	card.position = Vector2(120, 486)
	add_child(card)
	card.field_picked.connect(_on_field_picked)
	card.card_pressed.connect(_on_card_pressed)
	card.letter_opened.connect(_open_letter)
	card.confiscate_pressed.connect(_confiscate)

	var tools := Ui.panel(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0)
	tools.position = Vector2(740, 496)
	tools.size = Vector2(410, 236)
	tools.z_index = 10
	add_child(tools)
	var tray := TextureRect.new()
	tray.texture = load("res://art/props/tool_tray.png")
	tray.position = Vector2.ZERO
	tray.size = Vector2(410, 236)
	tray.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tools.add_child(tray)
	var t := Ui.label("桌 面 工 具", 16, Color("#d8d2b8"), Ui.font_serif())
	t.position = Vector2(18, 8)
	t.size = Vector2(200, 22)
	tools.add_child(t)

	_compare_btn = Ui.button("对照模式 (C)", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	_compare_btn.position = Vector2(18, 42)
	_compare_btn.size = Vector2(180, 42)
	_ghost_button(_compare_btn)
	_icon_button(_compare_btn, "compare")
	_compare_btn.pressed.connect(_toggle_compare)
	tools.add_child(_compare_btn)

	_magnify_btn = Ui.button("放大镜 (Z)", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	_magnify_btn.position = Vector2(212, 42)
	_magnify_btn.size = Vector2(180, 42)
	_ghost_button(_magnify_btn)
	_icon_button(_magnify_btn, "magnifier")
	_magnify_btn.pressed.connect(_use_magnifier)
	tools.add_child(_magnify_btn)

	_uv_btn = Ui.button("紫外线灯 (U)", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	_uv_btn.position = Vector2(18, 94)
	_uv_btn.size = Vector2(180, 42)
	_ghost_button(_uv_btn)
	_icon_button(_uv_btn, "uv")
	_uv_btn.pressed.connect(_use_uv)
	tools.add_child(_uv_btn)

	var phone := Ui.button("电话核实 (P)", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	phone.position = Vector2(212, 94)
	phone.size = Vector2(180, 42)
	_ghost_button(phone)
	_icon_button(phone, "phone")
	phone.pressed.connect(_open_phone)
	tools.add_child(phone)

	var manual_btn := Ui.button("仿真手册 (M)", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	manual_btn.position = Vector2(18, 146)
	manual_btn.size = Vector2(180, 42)
	_ghost_button(manual_btn)
	_icon_button(manual_btn, "book")
	manual_btn.pressed.connect(_open_manual)
	tools.add_child(manual_btn)

	var shop_btn := Ui.button("办公用品商店", 16, Color(0.20, 0.24, 0.20), Ui.WHITE)
	shop_btn.position = Vector2(212, 146)
	shop_btn.size = Vector2(180, 42)
	_ghost_button(shop_btn)
	_icon_button(shop_btn, "shop")
	shop_btn.pressed.connect(_open_shop)
	tools.add_child(shop_btn)

	var note := Ui.label("工具用一次，时间就少一点。", 12, Color(0.75, 0.72, 0.58, 0.7), Ui.font_serif())
	note.position = Vector2(18, 198)
	note.size = Vector2(360, 20)
	tools.add_child(note)

func _build_stamps() -> void:
	var panel := Ui.panel(Color(0.13, 0.12, 0.10, 0.6), Color(0.55, 0.45, 0.28, 0.5), 1, 3, 14)
	panel.position = Vector2(740, 748)
	panel.size = Vector2(410, 216)
	panel.z_index = 20
	add_child(panel)
	var t := Ui.label("印 章 台", 16, Color("#d8d2b8"), Ui.font_serif())
	t.position = Vector2(18, 4)
	t.size = Vector2(200, 22)
	panel.add_child(t)

	var approve := TextureButton.new()
	approve.texture_normal = load("res://art/props/stamp_green.png")
	approve.position = Vector2(14, 24)
	approve.size = Vector2(180, 110)
	approve.pressed.connect(_select_stamp.bind("approve"))
	panel.add_child(approve)
	var al := Ui.label("允许进入", 15, Color("#dff0d8"), Ui.font_serif())
	al.position = Vector2(14, 92)
	al.size = Vector2(180, 22)
	al.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	al.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(al)

	var reject := TextureButton.new()
	reject.texture_normal = load("res://art/props/stamp_red.png")
	reject.position = Vector2(216, 24)
	reject.size = Vector2(180, 110)
	reject.pressed.connect(_select_stamp.bind("reject"))
	panel.add_child(reject)
	var rl := Ui.label("拒绝进入", 15, Color("#f4dcd6"), Ui.font_serif())
	rl.position = Vector2(216, 92)
	rl.size = Vector2(180, 22)
	rl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	rl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(rl)

	var arrest_btn := Ui.button("逮 捕 (E)", 15, Color(0.32, 0.24, 0.16), Color("#f0e0c8"))
	arrest_btn.position = Vector2(18, 142)
	arrest_btn.size = Vector2(180, 40)
	_icon_button(arrest_btn, "arrest")
	arrest_btn.pressed.connect(_arrest)
	panel.add_child(arrest_btn)

	_next_btn = Ui.button("喊 下 一 位 (N)", 15, Color(0.20, 0.28, 0.36), Ui.WHITE)
	_next_btn.position = Vector2(212, 142)
	_next_btn.size = Vector2(180, 40)
	_next_btn.visible = false
	_next_btn.pressed.connect(_next_visitor)
	panel.add_child(_next_btn)

	var hint := Ui.label("先选印章，再点证件", 12, Color(0.72, 0.7, 0.58, 0.8), Ui.font_serif())
	hint.position = Vector2(18, 190)
	hint.size = Vector2(300, 18)
	panel.add_child(hint)

func _build_right_panel() -> void:
	var panel := Ui.panel(Color(0.09, 0.10, 0.09, 0.5), Color(0.45, 0.42, 0.30, 0.4), 1, 3, 14)
	panel.position = Vector2(1180, 470)
	panel.size = Vector2(700, 494)
	add_child(panel)
	var t := Ui.label("值 班 台 账", 16, Color("#d8d2b8"), Ui.font_serif())
	t.position = Vector2(18, 10)
	t.size = Vector2(200, 22)
	panel.add_child(t)

	var save_btn := Ui.button("保存进度", 15, Color(0.20, 0.24, 0.20), Ui.WHITE)
	save_btn.position = Vector2(18, 44)
	save_btn.size = Vector2(150, 40)
	save_btn.pressed.connect(_save_game)
	panel.add_child(save_btn)
	var load_btn := Ui.button("读取进度", 15, Color(0.20, 0.24, 0.20), Ui.WHITE)
	load_btn.position = Vector2(180, 44)
	load_btn.size = Vector2(150, 40)
	load_btn.pressed.connect(_load_game)
	panel.add_child(load_btn)
	var new_btn := Ui.button("重新入职", 15, Color(0.28, 0.18, 0.14), Ui.WHITE)
	new_btn.position = Vector2(342, 44)
	new_btn.size = Vector2(150, 40)
	new_btn.pressed.connect(_restart)
	panel.add_child(new_btn)

	var term_label := Ui.label("教育局办公系统", 15, Color("#9ad7a2"), Ui.font_mono())
	term_label.position = Vector2(18, 100)
	term_label.size = Vector2(400, 22)
	panel.add_child(term_label)

	if State.has_upgrade("quickBookmarks"):
		var sites := [["schools", "学校信息库"], ["phone", "电话簿"], ["rules", "准入规定"], ["wanted", "协查通报"], ["archive", "档案查询"], ["mail", "收件箱"], ["achv", "成就"]]
		var sx := 18
		var sy := 130
		for i in sites.size():
			var b := Ui.button(String(sites[i][1]), 13, Color(0.10, 0.16, 0.12), Color("#9ad7a2"))
			b.position = Vector2(sx + (i % 2) * 336, sy + int(i / 2) * 42)
			b.size = Vector2(320, 36)
			var key := String(sites[i][0])
			b.pressed.connect(func() -> void: _open_terminal(key))
			panel.add_child(b)
	else:
		var open_btn := Ui.button("打开浏览器", 16, Color(0.10, 0.16, 0.12), Color("#9ad7a2"))
		open_btn.position = Vector2(18, 132)
		open_btn.size = Vector2(240, 42)
		open_btn.pressed.connect(func() -> void: _open_terminal("schools"))
		panel.add_child(open_btn)
		var hint := Ui.label("每次查资料要先进浏览器、再进收藏夹。\n买「快捷收藏夹」可把站点钉在桌面。", 13, Color("#7d8a7a"), Ui.font_serif())
		hint.position = Vector2(18, 186)
		hint.size = Vector2(640, 60)
		panel.add_child(hint)

	var reader := TextureButton.new()
	reader.texture_normal = load("res://art/props/reader.png")
	reader.position = Vector2(432, 206)
	reader.size = Vector2(96, 64)
	reader.pressed.connect(_use_reader)
	panel.add_child(reader)
	_reader_btn = reader
	var phone_prop := TextureButton.new()
	phone_prop.texture_normal = load("res://art/props/phone.png")
	phone_prop.position = Vector2(546, 214)
	phone_prop.size = Vector2(84, 84)
	phone_prop.pressed.connect(_open_phone)
	panel.add_child(phone_prop)
	var phone_label := Ui.label("电话", 12, Color("#c8c2aa"), Ui.font_serif())
	phone_label.position = Vector2(572, 298)
	phone_label.size = Vector2(60, 18)
	panel.add_child(phone_label)

	var drawer := TextureButton.new()
	drawer.texture_normal = load("res://art/props/drawer.png")
	drawer.position = Vector2(500, 408)
	drawer.size = Vector2(176, 72)
	drawer.pressed.connect(_open_drawer)
	panel.add_child(drawer)
	var dlabel := Ui.label("证物", 12, Color("#c8c2aa"), Ui.font_serif())
	dlabel.position = Vector2(560, 470)
	dlabel.size = Vector2(80, 18)
	panel.add_child(dlabel)

	_stats_label = Ui.label("", 13, Color("#8f9a84"), Ui.font_mono())
	_stats_label.position = Vector2(18, 392)
	_stats_label.size = Vector2(660, 110)
	panel.add_child(_stats_label)

func _build_message_bar() -> void:
	var bar := Ui.panel(Color(0.06, 0.07, 0.06, 0.75), Color(0.4, 0.4, 0.3, 0.4), 1, 2, 12)
	bar.position = Vector2(120, 976)
	bar.size = Vector2(1560, 72)
	add_child(bar)
	_msg_label = Ui.label("", 18, Ui.WHITE, Ui.font_serif())
	_msg_label.position = Vector2(16, 10)
	_msg_label.size = Vector2(1520, 50)
	_msg_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	bar.add_child(_msg_label)
	_msg("把证件拖到面前，逐项核对。选印章，再点证件。")

func _refresh_hud() -> void:
	_day_label.text = "DAY %d / %d" % [State.day, State.TOTAL_DAYS]
	_date_label.text = "%s  %s" % [State.date, State.weekday_cn(State.date)]
	_time_label.text = "TIME " + State.fmt_time(State.time_left)
	_money_label.text = "CREDITS %d" % State.money
	if State.quota_required > 0:
		_quota_label.text = "拒签指标 %d / %d　怀疑度 %d" % [State.quota_done, State.quota_required, State.suspicion]
	else:
		_quota_label.text = "拒签指标 ——　怀疑度 %d" % State.suspicion
	_queue_label.text = "队列：%d 人待检 / 今日 %d 人" % [maxi(0, State.total_today - State.handled_today), State.total_today]
	_fill_rules()
	_fill_stats()
	var esc := get_node_or_null("EscapeBtn")
	var can_escape: bool = State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.has_fake_id and State.has_ticket and not State.escape_ready
	if can_escape and esc == null:
		var b := Ui.button("启动逃亡", 14, Color(0.35, 0.22, 0.16), Ui.WHITE)
		b.name = "EscapeBtn"
		b.position = Vector2(1608, 3)
		b.size = Vector2(120, 30)
		b.pressed.connect(_try_escape)
		add_child(b)
	elif not can_escape and esc != null:
		esc.queue_free()

func _fill_rules() -> void:
	for c in _rules_box.get_children():
		c.queue_free()
	for d in Data.doc_rules:
		var unlock := int(d.get("day", 1))
		var scope := String(d.get("scope", "all"))
		var scope_cn := "全部"
		if scope == "experiment":
			scope_cn = "实验学生"
		elif scope == "external":
			scope_cn = "外校"
		elif scope == "transfer":
			scope_cn = "转学"
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 10)
		var mark := Ui.label("■", 15, Color("#8fbf86") if unlock <= State.day else Color("#5a6355"), Ui.font_mono())
		var nm := Ui.label("%s　[%s]" % [String(d.get("name", "")), scope_cn], 15, Color("#d5cfb6") if unlock <= State.day else Color("#6b7264"), Ui.font_serif())
		nm.custom_minimum_size = Vector2(240, 0)
		var st := Ui.label("生效" if unlock <= State.day else "第 %d 天" % unlock, 12, Color("#93a58a") if unlock <= State.day else Color("#5f6858"), Ui.font_mono())
		row.add_child(mark)
		row.add_child(nm)
		row.add_child(st)
		_rules_box.add_child(row)

func _fill_stats() -> void:
	if _stats_label == null:
		return
	_stats_label.text = "今日　正确 %d　错误 %d　已检 %d / %d\n累计　正确 %d　错误 %d\n余额 %d 元　　怀疑度 %d" % [
		State.correct_today, State.wrong_today, State.handled_today, State.total_today,
		State.correct_total, State.wrong_total, State.money, State.suspicion
	]
func _begin_shift() -> void:
	if State.money < 0:
		_show_ending("debt")
		return
	if State.day in [12, 19, 26, 30] and not bool(State.event_done.get(str(State.day), false)):
		_open_gun_event()
		return
	if not State.pending_org.is_empty():
		_msg("收件箱里有一封学生斗争委员会的邮件。打开教育局系统处理。", Color("#e8dfae"))
	State.running = true
	_paused = false
	_spawn_visitor()

func _spawn_visitor() -> void:
	if State.handled_today >= State.total_today:
		_end_day()
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = State.day * 977 + State.handled_today * 31
	var v := VisitorFactory.make(State.day, State.date, rng, Data.names, Data.schools, _principals, Data.doc_rules)
	_visitor = v
	card.set_visitor(v, State.date)
	_build_docs()
	card.position = Vector2(120, 486)
	_win_portrait.setup(int(v.get("face_seed", 1)), false, false)
	_win_name.text = String(v.get("name", ""))
	var purpose := String(v.get("purpose", ""))
	var extra := ""
	if purpose != "":
		extra = "　来意：" + purpose
	var doc_count: int = Data.required_docs(State.day, v).size()
	_win_school.text = "%s · %d年级%s　·　应交材料 %d 份" % [String(v.get("school", "")), int(v.get("grade", 0)), extra, doc_count]
	_win_dialogue.text = "「%s」" % String(v.get("dialogue", ""))
	_win_archive.text = _archive_text(v)
	_refresh_suspicious()
	_awaiting_next = false
	State.called_this = false
	State.db_checked_this = false
	_next_btn.visible = false
	_pending = ""
	_first_field = ""
	if _compare_mode:
		_compare_mode = false
		card.set_compare_mode(false)
	_update_compare_btn()
	_refresh_hud()
	if State.has_upgrade("queue_scan") and State.handled_today + 1 < State.total_today:
		var rng2 := RandomNumberGenerator.new()
		rng2.seed = State.day * 977 + (State.handled_today + 1) * 31
		var nv := VisitorFactory.make(State.day, State.date, rng2, Data.names, Data.schools, _principals, Data.doc_rules)
		var need: int = Data.required_docs(State.day, nv).size()
		_queue_label.text += "\n队列预检：下一位 %s，应交 %d 份材料" % [String(nv.get("name", "")), need]

func _archive_text(v: Dictionary) -> String:
	if not State.has_upgrade("archive"):
		return ""
	var key := String(v.get("name", ""))
	var rec: Dictionary = State.archive.get(key, {})
	return "档案：来访 %d 次，被拒 %d 次" % [int(rec.get("visits", 0)), int(rec.get("stops", 0))]

func _refresh_suspicious() -> void:
	if _visitor.is_empty():
		return
	if not State.has_upgrade("stamp_checker"):
		card.set_suspicious([])
		return
	var bad: Array = []
	var grade := int(_visitor.get("grade", 0))
	if RuleEngine.birth_year_of(String(_visitor.get("birth", ""))) != RuleEngine.expected_birth_year(grade):
		bad.append("birth")
	if String(_visitor.get("student_id", "")).substr(0, 4) != RuleEngine.expected_prefix(grade):
		bad.append("id")
	card.set_suspicious(bad)

func _eval_ctx() -> Dictionary:
	var names := {}
	for d in Data.doc_rules:
		names[String(d.get("key", ""))] = String(d.get("name", ""))
	return {
		"required": Data.required_docs(State.day, _visitor),
		"doc_names": names,
		"principals": _principals,
		"check_photo": true,
		"enforce_transfer_checks": true,
		"called": State.called_this,
		"db_checked": State.db_checked_this
	}

func _judge(kind: String) -> void:
	if _awaiting_next or _visitor.is_empty():
		return
	var res := RuleEngine.evaluate(_visitor, State.date, _eval_ctx())
	var approved := kind == "approve"
	var correct := approved == bool(res.allow)
	var delta := 0
	if correct:
		delta = int(Data.fee("correct_simple", 10)) if State.simple_mode else int(Data.fee("correct_normal", 5))
		if State.talent == "justice":
			delta += 5
		State.correct_today += 1
		State.correct_total += 1
		_msg("【通过】审核正确　+%d 元。%s" % [delta, "（今日拒签指标 +1）" if not approved else ""], Color("#a8d08a"))
	else:
		var forged_fields: Array = _visitor.get("forged_fields", [])
		if not forged_fields.is_empty() and randf() < 0.30:
			_open_bribe()
			return
		if not State.warned_once:
			State.warned_once = true
			delta = 0
			_msg("这次只警告，不扣钱。下次再判错就开罚单。", Color("#e8dfae"))
			State.wrong_today += 1
			State.wrong_total += 1
			State.handled_today += 1
			card.play_stamp("警 告", Color("#a57c2a"))
			_awaiting_next = true
			_next_btn.visible = true
			_refresh_hud()
			return
		delta = -int(Data.fee("wrong", 10))
		State.wrong_today += 1
		State.wrong_total += 1
		var why := "应拒绝"
		if bool(res.allow):
			why = "应放行"
		_msg("【退回】审核错误　%d 元。%s：%s" % [delta, why, _reason_text(res.reasons)], Color("#e0a080"))
	State.money += delta
	if not approved:
		State.quota_done += 1
	State.handled_today += 1
	card.play_stamp("通  过" if approved else "拒  绝", Ui.GREEN if approved else Ui.RED)
	card.shake()
	var key := String(_visitor.get("name", ""))
	var rec: Dictionary = State.archive.get(key, {"visits": 0, "stops": 0})
	rec["visits"] = int(rec.get("visits", 0)) + 1
	if not approved:
		rec["stops"] = int(rec.get("stops", 0)) + 1
	State.archive[key] = rec
	_awaiting_next = true
	_next_btn.visible = true
	_refresh_hud()

func _reason_text(reasons: Array) -> String:
	if reasons.is_empty():
		return "未发现违规项"
	var parts: Array = []
	for r in reasons:
		parts.append(String(r))
	return "；".join(parts)

func _next_visitor() -> void:
	if not _awaiting_next:
		return
	_awaiting_next = false
	State.called_this = false
	State.db_checked_this = false
	_next_btn.visible = false
	card.clear()
	if State.handled_today >= State.total_today:
		_end_day()
	else:
		_spawn_visitor()

func _select_stamp(kind: String) -> void:
	if _awaiting_next or _visitor.is_empty() or _paused:
		return
	_pending = kind
	Sfx.play("click", -6.0)
	_msg("已取出「%s」印章，点击证件盖下。" % ("允许进入" if kind == "approve" else "拒绝进入"), Color("#e8dfae"))

func _on_card_pressed() -> void:
	if _awaiting_next or _paused:
		return
	if _pending == "":
		_msg("先选择印章，再点证件。", Color("#e0a080"))
		return
	_judge(_pending)
	_pending = ""

func _toggle_compare() -> void:
	if _awaiting_next or _paused:
		return
	_compare_mode = not _compare_mode
	card.set_compare_mode(_compare_mode)
	_first_field = ""
	_update_compare_btn()
	if _compare_mode:
		_pending = ""
		_msg("对照模式：依次点击两个字段，系统只做算术，结论仍归你。", Color("#e8dfae"))
	else:
		_msg("已收起对照尺。", Color("#c8c2aa"))

func _update_compare_btn() -> void:
	if _compare_btn == null:
		return
	_compare_btn.text = "对照模式（开）" if _compare_mode else "对照模式 (C)"

func _on_field_picked(fid: String) -> void:
	if not _compare_mode:
		return
	if _first_field == "":
		_first_field = fid
		card.set_picked(fid)
		_msg("已选：%s。再点第二个字段。" % _field_label(fid), Color("#e8dfae"))
	else:
		var hint := RuleEngine.compare_hint(_first_field, fid, _visitor, State.date)
		State.time_left = max(0.0, State.time_left - 2.0)
		card.set_picked("")
		_first_field = ""
		_msg("对照：" + hint, Color("#f0e6b8"))
		_unlock_ach("firstCompare", "第一次比对")

func _field_label(fid: String) -> String:
	var map := {
		"name": "姓名", "grade": "年级", "birth": "出生日期", "id": "学号",
		"expiry": "有效期", "school": "学校", "campus_card": "校园卡",
		"temp_pass": "临时通行证", "security_pass": "准入证", "transfer_letter_from": "转出学校",
		"transfer_letter_sig": "校长签名", "health_cert": "健康证明"
	}
	return String(map.get(fid, fid))

func _use_magnifier() -> void:
	if _paused:
		return
	if not State.has_upgrade("magnifier"):
		_msg("没有放大镜。办公用品商店 50 元一把。", Color("#e0a080"))
		return
	if _visitor.is_empty():
		return
	State.time_left = max(0.0, State.time_left - 2.0)
	_open_loupe()

func _open_loupe() -> void:
	_paused = true
	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.55)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(dim)
	var catcher := Button.new()
	catcher.set_anchors_preset(Control.PRESET_FULL_RECT)
	catcher.flat = true
	catcher.focus_mode = Control.FOCUS_NONE
	catcher.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	overlay.add_child(catcher)
	var frame := Ui.panel(Color("#c9b48c"), Color("#6d5c3a"), 4, 2, 12)
	frame.position = Vector2(700, 220)
	frame.size = Vector2(520, 640)
	overlay.add_child(frame)
	var p := Portrait.new()
	p.setup(int(_visitor.get("photo", {}).get("seed", 1)), true, bool(_visitor.get("photo_mirrored", false)))
	p.position = Vector2(16, 16)
	p.size = Vector2(488, 552)
	frame.add_child(p)
	var hint := Ui.label("点击任意处收起放大镜　·　用时 2 秒", 13, Color("#3a3428"), Ui.font_serif())
	hint.position = Vector2(16, 580)
	hint.size = Vector2(488, 20)
	frame.add_child(hint)
	catcher.pressed.connect(_close_loupe.bind(overlay))
	Sfx.play("paper", -14.0)

func _close_loupe(overlay: Control) -> void:
	if is_instance_valid(overlay):
		overlay.queue_free()
	_paused = false

func _use_uv() -> void:
	if _paused:
		return
	if not State.has_upgrade("uv_lamp"):
		_msg("没有紫外线灯。商店售价 80 元。", Color("#e0a080"))
		return
	if _visitor.is_empty():
		return
	State.time_left = max(0.0, State.time_left - 3.0)
	var lines: Array = []
	if _visitor.has("transfer_letter") and _visitor.get("transfer_letter") != null:
		var tl: Dictionary = _visitor.get("transfer_letter", {})
		var forged := bool(tl.get("forged", false))
		lines.append("介绍信钢印压痕" + ("断裂、纸面无凸起" if forged else "连续、纸面有凸起"))
		lines.append("荧光纤维" + ("分布异常" if forged else "正常"))
	else:
		lines.append("学生证钢印完整")
	if _visitor.has("health_cert") and _visitor.get("health_cert") != null:
		var hc: Dictionary = _visitor.get("health_cert", {})
		lines.append("健康证明字段" + ("墨色新于其余栏位" if bool(hc.get("forged", false)) else "墨色一致"))
	_msg("紫外线检查：" + "；".join(lines) + "。", Color("#b3c8e8"))

func _open_phone() -> void:
	if _paused:
		return
	_paused = true
	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.55)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(dim)
	var panel := Ui.panel(Color("#1b1f1a"), Color("#7a6a4a"), 2, 2, 22)
	panel.position = Vector2(640, 300)
	panel.size = Vector2(640, 460)
	overlay.add_child(panel)
	var title := Ui.label("电 话 核 实", 24, Ui.WHITE, Ui.font_serif())
	title.position = Vector2(24, 18)
	title.size = Vector2(300, 30)
	panel.add_child(title)
	var hint := Ui.label("号码见手册第八章，每日轮换。拨号消耗 6 秒。", 13, Color(0.8, 0.8, 0.7, 0.75), Ui.font_serif())
	hint.position = Vector2(24, 52)
	hint.size = Vector2(560, 20)
	panel.add_child(hint)
	var input := LineEdit.new()
	input.placeholder_text = "例如 0755-123456"
	input.position = Vector2(24, 86)
	input.size = Vector2(360, 42)
	input.add_theme_font_override("font", Ui.font_mono())
	input.add_theme_font_size_override("font_size", 18)
	input.add_theme_color_override("font_color", Color("#e8e2c8"))
	input.add_theme_stylebox_override("normal", Ui.style(Color(0.08, 0.09, 0.08), Color(0.4, 0.4, 0.3), 1, 2, 8))
	panel.add_child(input)
	var dial := Ui.button("拨 号", 17, Color(0.2, 0.3, 0.2), Ui.WHITE)
	dial.position = Vector2(400, 86)
	dial.size = Vector2(120, 42)
	dial.pressed.connect(_on_dial.bind(input, overlay))
	panel.add_child(dial)
	var close := Ui.button("挂断", 17, Color(0.3, 0.2, 0.18), Ui.WHITE)
	close.position = Vector2(534, 86)
	close.size = Vector2(80, 42)
	close.pressed.connect(_close_loupe.bind(overlay))
	panel.add_child(close)

	if State.has_upgrade("stickyNote"):
		var y := 152
		var label := Ui.label("便签纸上的号码：", 14, Color(0.85, 0.82, 0.7), Ui.font_serif())
		label.position = Vector2(24, y)
		label.size = Vector2(300, 20)
		panel.add_child(label)
		y += 28
		for key in Data.phones.keys():
			var b := Ui.button("%s　%s" % [String(key), String(Data.phones[key])], 14, Color(0.17, 0.2, 0.17), Ui.WHITE)
			b.position = Vector2(24, y)
			b.size = Vector2(300, 34)
			b.pressed.connect(_place_call.bind(String(Data.phones[key]), overlay))
			panel.add_child(b)
			y += 38
	else:
		var tip := Ui.rich("便签纸未购置，请手动输入号码。\n[color=#8f9a84]（手册第八章有当日号码）[/color]", 14, Color(0.8, 0.8, 0.7))
		tip.position = Vector2(24, 156)
		tip.size = Vector2(580, 120)
		tip.scroll_active = false
		panel.add_child(tip)

func _on_dial(input: LineEdit, overlay: Control) -> void:
	var number := input.text.strip_edges()
	if number == "":
		_msg("请输入号码。", Color("#e0a080"))
		return
	_place_call(number, overlay)

func _place_call(number: String, overlay: Control) -> void:
	State.time_left = max(0.0, State.time_left - 6.0)
	var target := ""
	for k in Data.phones.keys():
		if String(Data.phones[k]) == number:
			target = String(k)
	var reply := ""
	if target == "教育局" or target == "深圳实验中学" or target != "":
		State.called_this = true
		var forged: Array = _visitor.get("forged_fields", [])
		var truthful := randf() < 0.75
		var bad := (not forged.is_empty()) if truthful else forged.is_empty()
		reply = "%s 值班室：这位同学的档案%s。" % [target if target != "" else "学校", "对不上" if bad else "没问题"]
		_msg("电话：" + reply + "（电话核查不一定准）", Color("#cfe0f0"))
		_unlock_ach("firstCall", "第一次通话")
		Sfx.play("click", -10.0)
		if is_instance_valid(overlay):
			overlay.queue_free()
			_paused = false
		return
	if target == "教育局":
		var sid := String(_visitor.get("student_id", ""))
		var ok := sid.substr(0, 4) == RuleEngine.expected_prefix(int(_visitor.get("grade", 0)))
		reply = "教育局档案室：%s" % ("学号在册，年级匹配。" if ok else "查无此学号段，档案异常。")
	elif target == "纪检部":
		reply = "纪检部值班员：举报请携带书面材料。"
	elif target == "新人培训":
		reply = "培训热线：你已经站在窗口后面了。"
	elif target == "":
		reply = "无人接听。"
	else:
		reply = "%s 校长办公室：介绍信签名请对照手册第五章。" % target
	_msg("电话：" + reply, Color("#cfe0f0"))
	_unlock_ach("firstCall", "第一次通话")
	Sfx.play("click", -10.0)
	if is_instance_valid(overlay):
		overlay.queue_free()
	_paused = false

func _open_manual() -> void:
	if _paused:
		return
	_paused = true
	var m := Manual.new()
	add_child(m)
	m.closed.connect(_close_modal.bind(m))

func _open_shop() -> void:
	if _paused:
		return
	_paused = true
	var s := Shop.new()
	add_child(s)
	s.changed.connect(_refresh_hud)
	s.closed.connect(_close_modal.bind(s))

func _close_modal(node: Control) -> void:
	if is_instance_valid(node):
		node.queue_free()
	_paused = false
	_refresh_hud()

func _show_briefing() -> void:
	if _briefing_open:
		return
	_briefing_open = true
	_paused = true
	var b := Briefing.new()
	b.z_index = 120
	b.day = State.day
	b.date_iso = State.date
	b.quota = State.quota_required
	b.headline = String(HEADLINES[(State.day - 1) % HEADLINES.size()])
	add_child(b)
	b.closed.connect(_on_briefing_closed.bind(b))

func _on_briefing_closed(b: Briefing) -> void:
	_briefing_open = false
	if is_instance_valid(b):
		b.queue_free()
	_paused = false
	_begin_shift()
	if not Meta.tutorial_done:
		_open_guided()
	if State.flavor != "":
		_msg("今日琐事：" + State.flavor, Color("#c8c2aa"))

func _save_game() -> void:
	if SaveManager.save(State.slot):
		_msg("进度已保存至存档 %d。" % State.slot, Color("#a8d08a"))
	else:
		_msg("保存失败。", Color("#e0a080"))

func _load_game() -> void:
	if not SaveManager.load_slot(State.slot):
		_msg("没有找到存档。", Color("#e0a080"))
		return
	_paused = false
	State.running = true
	card.clear()
	_refresh_hud()
	_spawn_visitor()
	_msg("已读取存档 %d。" % State.slot, Color("#a8d08a"))

func _restart() -> void:
	State.reset()
	get_tree().reload_current_scene()

func _end_day() -> void:
	State.running = false
	if State.quota_required > 0:
		if State.quota_done >= State.quota_required:
			State.quota_met_days += 1
		else:
			State.quota_missed += 1
			State.add_suspicion(3)
			State.add_mail("校园安全部", "第 %d 天拒签未达标" % State.day, "本日应拒签 %d 人，实际 %d 人。已记录在案。" % [State.quota_required, State.quota_done], "warn")
	if State.wrong_today == 0 and State.handled_today > 0:
		_unlock_ach("perfectDay", "完美执勤")
	var s := State.finish_day()
	_paused = true
	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(dim)
	var panel := Ui.panel(Ui.PAPER, Ui.PAPER_EDGE, 2, 2, 28)
	panel.position = Vector2(620, 320)
	panel.size = Vector2(680, 440)
	overlay.add_child(panel)
	var title := Ui.label("第 %d 天 · 执勤结算" % int(s.get("day", State.day)), 28, Ui.INK, Ui.font_serif())
	title.position = Vector2(32, 24)
	title.size = Vector2(500, 34)
	panel.add_child(title)
	var line := ColorRect.new()
	line.color = Ui.PAPER_EDGE
	line.position = Vector2(32, 70)
	line.size = Vector2(616, 2)
	panel.add_child(line)
	var body := Ui.rich("", 17, Ui.INK)
	body.position = Vector2(32, 90)
	body.size = Vector2(616, 240)
	body.text = "今日受检　[b]%d[/b] 人\n正确　[b]%d[/b] 次　　错误　[b]%d[/b] 次\n拒签指标　[b]%d / %d[/b]\n当日余额　[b]%d[/b] 元\n\n%s" % [
		int(s.get("total", 0)), int(s.get("correct", 0)), int(s.get("wrong", 0)),
		int(s.get("quota_done", 0)), int(s.get("quota", 0)), int(s.get("money", 0)),
		_settle_note(s)
	]
	body.scroll_active = false
	panel.add_child(body)
	var btn := Ui.button("进入第 %d 天" % (State.day + 1), 20, Ui.INK, Ui.PAPER)
	btn.position = Vector2(196, 352)
	btn.size = Vector2(288, 54)
	btn.pressed.connect(_on_settle_continue.bind(overlay))
	panel.add_child(btn)
	Sfx.play("paper", -8.0)

func _settle_note(s: Dictionary) -> String:
	var quota := int(s.get("quota", 0))
	if quota > 0 and int(s.get("quota_done", 0)) < quota:
		return "安全部备注：拒签数未达标，已记录在案。"
	if int(s.get("wrong", 0)) == 0 and int(s.get("total", 0)) > 0:
		return "安全部备注：本日无差错，继续保持。"
	return "安全部备注：按章办事，勿徇私情。"

func _on_settle_continue(overlay: Control) -> void:
	if is_instance_valid(overlay):
		overlay.queue_free()
	_next_day()

func _next_day() -> void:
	_paused = false
	if not State.advance_day():
		_show_ending("")
		return
	State.start_day()
	card.clear()
	_refresh_hud()
	_show_briefing()

func _show_ending(kind: String) -> void:
	if State.endless and State.money >= 0:
		return
	State.running = false
	if State.day >= 30:
		_unlock_ach("survivalist", "老油条")
	_paused = true
	_ending_active = true
	Music.play("amb_room", 2.0, -20.0)
	Music.ambience("", 1.0)
	if _msg_label != null:
		_msg_label.text = ""
	var k := kind
	if k == "":
		if State.money < 0:
			k = "debt"
		elif State.corruption >= 3:
			k = "corrupt"
		elif State.escape_ready:
			k = "escape"
		elif State.shot_org:
			k = "gun"
		elif State.trust >= 5:
			k = "revolution"
		elif State.trust > 0:
			k = "gun"
		elif State.suspicion >= 70:
			k = "gun"
		elif State.quota_missed > 5:
			k = "gun"
		else:
			k = "stable"
	State.mark_ending(k)
	if State.endless and k == "debt":
		Meta.best_day = maxi(Meta.best_day, State.day)
		Meta.save_meta()
	Meta.record_run(k, State.talent, State.day, State.achievements, State.endings_seen)
	match k:
		"escape":
			_unlock_ach("fugitive", "逃亡者")
		"revolution":
			_unlock_ach("revolutionary", "革命先驱")
		"gun", "stable":
			_unlock_ach("loyalist", "忠诚卫士")

	var titles := {
		"debt": "负债结局",
		"corrupt": "腐败结局",
		"gun": "忠诚线结局（枪毙）",
		"stable": "忠诚线结局（平稳）",
		"escape": "逃亡结局",
		"revolution": "革命线结局"
	}
	var texts := {
		"escape": "你带着一封真的介绍信、一张假证和一张高铁票离开了深圳。8 小时后，浑身酸痛的你看到了新学校：河北衡水第二中学。有些迟疑的学生会干部批准你进入。喘口气吧。但是记住：「衡水二中至高无上！」",
		"revolution": "同志，您好！今天是光荣的一天。学生斗争委员会的革命成功了。校园里推行了民主改革，你被任命为新一届学生会纪检部部长。校园里充满希望，但这条路同样充满挑战。现在，光荣属于新深圳实验。",
		"debt": "由于长期负债，你被纪检部隔离审查，最终失去了学生身份……",
		"corrupt": "你因多次收受贿赂被纪检部调查，最终被开除并移交司法机关。你的名字被永久从学校名册中删除。",
		"gun": "同学你好，校园安全部对你的政治和工作情况进行了审查。经查，你与非法组织有联系，犯有颠覆学校罪。纪检部和光荣的深圳实验不会容忍背叛，所以你被除名了。现在，和我们走一趟吧。",
		"stable": "同志，您好。很高兴地通知你，你的政治审核通过，可以继续担任纪检部科员。我们和深中人达成了新协议，4 月 1 日返回你的工作岗位，祝好运。以及，光荣属于深圳实验！"
	}
	var stamps := {
		"debt": ["隔离审查", Color(0.62, 0.16, 0.12)],
		"corrupt": ["开除学籍", Color(0.62, 0.16, 0.12)],
		"gun": ["执行枪决", Color(0.55, 0.10, 0.10)],
		"stable": ["准予留任", Color(0.20, 0.42, 0.26)],
		"escape": ["准予通行", Color(0.55, 0.42, 0.16)],
		"revolution": ["新 秩 序", Color(0.62, 0.16, 0.12)]
	}

	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0.02, 0.02, 0.02, 0.88)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	overlay.add_child(dim)

	var panel := Ui.panel(Color("#e4dbc2"), Color("#7c6a44"), 3, 1, 34)
	panel.position = Vector2(430, 160)
	panel.size = Vector2(1060, 760)
	overlay.add_child(panel)

	var seal := Ui.label("═════════════════════════════\n          [ 绝 密 ]\n═════════════════════════════", 18, Ui.INK, Ui.font_mono())
	seal.position = Vector2(48, 26)
	seal.size = Vector2(640, 80)
	panel.add_child(seal)
	var head := Ui.label("档案编号：STU-%06d　　日期：%s" % [absi(hash(State.player_name + State.date)) % 999999, State.date], 14, Ui.INK_SOFT, Ui.font_mono())
	head.position = Vector2(48, 108)
	head.size = Vector2(800, 20)
	panel.add_child(head)
	var t := Ui.label("「 %s 」" % String(titles.get(k, "结局")), 36, Ui.INK, Ui.font_serif())
	t.position = Vector2(48, 144)
	t.size = Vector2(760, 46)
	panel.add_child(t)
	var body := Ui.rich(String(texts.get(k, "")), 18, Ui.INK)
	body.position = Vector2(48, 202)
	body.size = Vector2(720, 220)
	body.scroll_active = false
	panel.add_child(body)

	var stamp_data: Array = stamps.get(k, ["结案", Ui.RED])
	var stamp := Ui.panel(Color(0, 0, 0, 0), Color(stamp_data[1], 0.82), 5, 2, 0)
	stamp.position = Vector2(650, 430)
	stamp.size = Vector2(320, 110)
	stamp.rotation = -0.14
	panel.add_child(stamp)
	var stamp_text := Ui.label(String(stamp_data[0]), 40, stamp_data[1], Ui.font_serif())
	stamp_text.position = Vector2(0, 26)
	stamp_text.size = Vector2(320, 56)
	stamp_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stamp.add_child(stamp_text)

	var sign_line := Ui.label("校园安全部　签发\n部长　李建国（印）", 15, Ui.INK, Ui.font_serif())
	sign_line.position = Vector2(660, 560)
	sign_line.size = Vector2(320, 52)
	panel.add_child(sign_line)

	var stats := Ui.label("最终余额：%d 元　　执勤天数：%d 天\n正确审核：%d 次　　没收介绍信：%d 封\n信任：%d　　怀疑度：%d　　腐败：%d" % [
		State.money, State.day, State.correct_total, State.confiscatedNormalLetters,
		State.trust, State.suspicion, State.corruption
	], 15, Ui.INK, Ui.font_mono())
	stats.position = Vector2(48, 452)
	stats.size = Vector2(560, 80)
	panel.add_child(stats)

	var minutes := int((Time.get_unix_time_from_system() - State.run_start_msec) / 60.0)
	var verdicts := State.correct_total + State.wrong_total
	var rate := 0.0 if verdicts == 0 else float(State.wrong_total) / float(verdicts) * 100.0
	var extra := Ui.label("本周目用时：%d 分钟　　误判率：%.1f%%　　收贿：%d 次　　逮捕：%d 次" % [minutes, rate, State.bribe_count, State.arrest_count], 14, Ui.INK_SOFT, Ui.font_mono())
	extra.position = Vector2(48, 536)
	extra.size = Vector2(700, 20)
	panel.add_child(extra)
	var curve := StatCurve.new()
	curve.values = State.daily_wrong
	curve.position = Vector2(48, 572)
	curve.size = Vector2(300, 64)
	panel.add_child(curve)
	var curve_label := Ui.label("每日误判曲线", 12, Ui.INK_SOFT, Ui.font_mono())
	curve_label.position = Vector2(48, 640)
	curve_label.size = Vector2(200, 18)
	panel.add_child(curve_label)
	var gallery := Ui.label("结局图鉴：%d / 6" % State.endings_seen.size(), 14, Ui.INK_SOFT, Ui.font_mono())
	gallery.position = Vector2(380, 610)
	gallery.size = Vector2(400, 22)
	panel.add_child(gallery)

	var btn := Ui.button("重新入职", 20, Ui.INK, Ui.PAPER)
	btn.position = Vector2(48, 676)
	btn.size = Vector2(220, 50)
	btn.pressed.connect(_restart)
	panel.add_child(btn)
	Sfx.play("stamp", -4.0)
func _msg(text: String, color: Color = Ui.WHITE) -> void:
	if _msg_label == null:
		return
	_msg_label.text = text
	_msg_label.add_theme_color_override("font_color", color)

func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey):
		return
	var key_event := event as InputEventKey
	if not key_event.pressed or key_event.echo:
		return
	if _paused:
		return
	match key_event.keycode:
		KEY_A:
			_select_stamp("approve")
		KEY_R:
			_select_stamp("reject")
		KEY_N:
			_next_visitor()
		KEY_C:
			_toggle_compare()
		KEY_M:
			_open_manual()
		KEY_P:
			_open_phone()
		KEY_Z:
			_use_magnifier()
		KEY_U:
			_use_uv()
		KEY_ESCAPE:
			if _compare_mode:
				_toggle_compare()

func _process(delta: float) -> void:
	if not State.running or _paused:
		return
	if _time_label == null:
		return
	if not State.time_frozen:
		State.time_left = max(0.0, State.time_left - delta)
	_time_label.text = "TIME " + State.fmt_time(State.time_left)
	if State.time_left <= 0.0:
		State.running = false
		_end_day()


func debug_open_manual() -> void:
	_open_manual()

func debug_open_shop() -> void:
	_open_shop()


func debug_judge(kind: String) -> void:
	_judge(kind)

func debug_end_day() -> void:
	_end_day()

func debug_manual_page(idx: int) -> void:
	_paused = true
	var m := Manual.new()
	add_child(m)
	m.closed.connect(_close_modal.bind(m))
	m._show(idx)


func debug_save_load() -> void:
	_save_game()
	_load_game()


func _open_letter() -> void:
	if _visitor.is_empty() or not _visitor.has("transfer_letter"):
		return
	var tl: Dictionary = _visitor.get("transfer_letter", {})
	var data := {
		"student_name": String(_visitor.get("name", "")),
		"student_id": String(_visitor.get("student_id", "")),
		"from_school": String(tl.get("from_school", "")),
		"to_school": String(tl.get("to_school", "")),
		"from_sig_id": String(tl.get("from_sig_id", "")),
		"to_sig_id": String(tl.get("to_sig_id", "")),
		"variant_from": String(tl.get("variant_from", "genuine")),
		"variant_to": String(tl.get("variant_to", "genuine"))
	}
	_paused = true
	var view := LetterView.new()
	view.letter = data
	add_child(view)
	view.closed.connect(_close_modal.bind(view))


func debug_letter() -> void:
	var data := {
		"student_name": "苏念",
		"student_id": "20231188",
		"from_school": "深圳中学",
		"to_school": "深圳实验中学",
		"from_sig_id": "li_hua",
		"to_sig_id": "wang_ming",
		"variant_from": "miss",
		"variant_to": "genuine"
	}
	_paused = true
	var view := LetterView.new()
	view.letter = data
	add_child(view)
	view.closed.connect(_close_modal.bind(view))


func _open_gun_event() -> void:
	_paused = true
	State.running = false
	var ev := SchoolRush.new()
	ev.scenario = "d%d" % State.day
	add_child(ev)
	ev.finished.connect(_on_gun_finished.bind(ev))

func _on_gun_finished(res: Dictionary, ev: Control) -> void:
	State.event_done[str(State.day)] = true
	var sc := String(res.get("scenario", "d12"))
	var money := int(res.get("money", 0))
	var susp := int(res.get("suspicion", 0))
	if sc == "d26":
		if bool(res.get("org_hit", false)):
			State.add_trust(-3)
			susp += 15
			_msg("你打中了他。袖标上写着学生斗争委员会。信任 -3，怀疑度 +15。", Color("#e0a080"))
		else:
			State.add_trust(1)
			susp += 2
			_msg("你没有开枪。他退了出去。信任 +1。", Color("#a8d08a"))
		money = 0
	else:
		State.money += money
		_msg("处置：击倒 %d 人，误伤学生 %d 人，校警%s。报告：%s。余额 %+d，怀疑度 %+d。" % [
			int(res.get("hostiles", 0)), int(res.get("students", 0)),
			"受伤" if bool(res.get("guard", false)) else "无碍",
			_report_cn(String(res.get("report", "honest"))), money, susp
		], Color("#e8dfae"))
	State.add_suspicion(susp)
	Music.play("bgm_day", 1.0)
	if sc == "d30":
		State.shot_org = bool(res.get("org_hit", false))
		if is_instance_valid(ev):
			ev.queue_free()
		_paused = false
		_refresh_hud()
		_show_ending("")
		return
	if is_instance_valid(ev):
		ev.queue_free()
	_paused = false
	_refresh_hud()
	_begin_shift()

func _report_cn(k: String) -> String:
	if k == "hide":
		return "隐去误伤"
	if k == "frame":
		return "记在周睿名下"
	return "如实上报"

func debug_gun(auto_resolve: bool = false) -> void:
	_open_gun_event()
	if auto_resolve:
		for c in get_children():
			if c is SchoolRush:
				c._resolve()


func _dbg(msg: String) -> void:
	var f := FileAccess.open("user://debug.log", FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open("user://debug.log", FileAccess.WRITE)
	if f != null:
		f.seek_end()
		f.store_line("%s %s" % [Time.get_time_string_from_system(), msg])
		f.close()

func _open_terminal(site: String) -> void:
	if _paused:
		return
	if not State.has_upgrade("quickBookmarks"):
		_browser_load_then(site)
		return
	_spawn_terminal(site)

func _spawn_terminal(site: String) -> void:
	_paused = true
	State.time_left = maxf(0.0, State.time_left - 2.0)
	var term := EduTerminal.new()
	term.visitor = _visitor
	add_child(term)
	term.time_cost.connect(_on_terminal_cost)
	if not term.org_requested.is_connected(_on_org_requested):
		term.org_requested.connect(_on_org_requested)
	term.closed.connect(_close_modal.bind(term))

func _browser_load_then(site: String) -> void:
	_paused = true
	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0.02, 0.03, 0.02, 0.8)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	overlay.add_child(dim)
	var label := Ui.label("正在连接教育局网络……", 22, Color("#9ad7a2"), Ui.font_mono())
	label.position = Vector2(0, 520)
	label.size = Vector2(1920, 30)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	overlay.add_child(label)
	Sfx.play("click", -14.0)
	await get_tree().create_timer(1.5).timeout
	if is_instance_valid(overlay):
		overlay.queue_free()
	_paused = false
	State.time_left = maxf(0.0, State.time_left - 3.0)
	_spawn_terminal(site)

func _on_terminal_cost(seconds: float) -> void:
	State.time_left = maxf(0.0, State.time_left - seconds)
	_refresh_hud()

func debug_terminal(site: String) -> void:
	_paused = false
	State.time_left = 600.0
	var term := EduTerminal.new()
	term.visitor = _visitor
	term.start_site = site
	add_child(term)
	term.z_index = 200
	term.visible = true
	term.size = Vector2(1920, 1080)
	term.time_cost.connect(_on_terminal_cost)
	if not term.org_requested.is_connected(_on_org_requested):
		term.org_requested.connect(_on_org_requested)
	if not term.org_requested.is_connected(_on_org_requested):
		term.org_requested.connect(_on_org_requested)
	term.closed.connect(_close_modal.bind(term))


func _confiscate() -> void:
	if _awaiting_next or _paused or _visitor.is_empty():
		return
	if not _visitor.has("transfer_letter") or _visitor.get("transfer_letter") == null:
		_msg("当前没有可没收的介绍信。", Color("#e0a080"))
		return
	var tl: Dictionary = _visitor.get("transfer_letter", {})
	var variant := String(tl.get("variant_from", "genuine"))
	var forged := bool(tl.get("forged", false)) or variant != "genuine"
	if forged:
		State.confiscatedItems.append({"day": State.day, "name": String(_visitor.get("name", "")), "kind": "forged"})
		_visitor["transfer_letter"] = null
		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_unlock_ach("firstConfiscation", "铁面无私")
		_msg("已没收伪造的转学介绍信。没有罚款，也没有嘉奖。", Color("#a8d08a"))
	else:
		if State.money < 25:
			_msg("余额不足 25 元，无法办理没收。", Color("#e0a080"))
			return
		State.money -= 25
		State.confiscatedNormalLetters += 1
		_unlock_ach("confiscator", "铁面无私·改")
		State.confiscatedItems.append({"day": State.day, "name": String(_visitor.get("name", "")), "kind": "normal"})
		_visitor["transfer_letter"] = null
		State.suspicion = clampi(State.suspicion + 2, 0, 100)
		State.handled_today += 1
		_msg("没收了一封正常介绍信，罚款 25 元。登记簿上留下一条谁都看得见的记录。", Color("#e0a080"))
	card.set_visitor(_visitor, State.date)
	_awaiting_next = true
	_next_btn.visible = true
	_refresh_hud()

func _arrest() -> void:
	if _awaiting_next or _paused or _visitor.is_empty():
		return
	var forged_fields: Array = _visitor.get("forged_fields", [])
	if forged_fields.is_empty():
		State.money -= 30
		State.suspicion = clampi(State.suspicion + 10, 0, 100)
		State.wrong_today += 1
		State.wrong_total += 1
		State.handled_today += 1
		_msg("误捕。该生材料齐全，家长已经在校门外等着。罚款 30 元，怀疑度 +10。", Color("#e0a080"))
	else:
		var bonus := 20
		if State.talent == "justice":
			bonus += 10
		State.money += bonus
		State.correct_today += 1
		State.correct_total += 1
		State.handled_today += 1
		State.quota_done += 1
		_unlock_ach("firstArrest", "执法如山")
		_msg("逮捕完成，嘉奖 +%d 元。他只是被带走，档案还在。" % bonus, Color("#a8d08a"))
	card.play_stamp("逮 捕", Color("#c8963a"))
	card.shake()
	_awaiting_next = true
	_next_btn.visible = true
	_refresh_hud()


func _open_org(mail_id: int = -1) -> void:
	_paused = true
	State.set_meta("org_mail_id", mail_id)
	State.running = false
	var ev := OrgEvent.new()
	ev.data = State.pending_org
	add_child(ev)
	ev.chosen.connect(_on_org_choice.bind(ev))

func _on_org_choice(kind: String, ev: Control) -> void:
	var data: Dictionary = State.pending_org
	var subject := String(data.get("subject", ""))
	if kind == "help":
		var cost := int(data.get("cost", 0))
		if State.money < cost:
			_msg("你拿不出这笔钱。信被退回了。", Color("#e0a080"))
		else:
			State.money -= cost
			State.add_trust(int(data.get("help", 1)))
			State.add_suspicion(int(data.get("risk", 0)))
			_unlock_ach("undercover", "暗中支持")
			_msg("你帮了他们。信任 +%d，怀疑度 +%d。" % [int(data.get("help", 1)), int(data.get("risk", 0))], Color("#a8d08a"))
	elif kind == "report":
		State.reported_count += 1
		State.money += 10
		State.add_suspicion(-2)
		_unlock_ach("whistleblower", "举报者")
		_msg("你把邮件内容报给了纪检部。嘉奖 +10 元。", Color("#e8dfae"))
	else:
		_msg("你删掉了这封邮件。", Color("#7d8a7a"))
	var mail_id: int = int(State.get_meta("org_mail_id", -1))
	if mail_id >= 0:
		var keep: Array = []
		for m in State.mails:
			if int(m.get("id", 0)) != mail_id:
				keep.append(m)
		State.mails = keep
	State.pending_org = {}
	if is_instance_valid(ev):
		ev.queue_free()
	_paused = false
	_begin_shift()
	if not Meta.tutorial_done:
		_open_guided()

func _unlock_ach(key: String, ach_name: String) -> void:
	if State.unlock(key, ach_name):
		if _ending_active:
			return
		var cur: String = ""
		if _msg_label != null:
			cur = _msg_label.text
		var line := "成就解锁：%s" % ach_name
		_msg((line if cur == "" else cur + "　｜　" + line), Color("#ffd98a"))

func _try_escape() -> void:
	State.escape_ready = true
	State.running = false
	_show_ending("")


func debug_org() -> void:
	State.pending_org = {
		"subject": "印刷费",
		"body": "检察员同学：\n\n我们要印一批刊物，缺五十元。\n你可以不出面，钱放在窗台上就行。\n\n——学生斗争委员会",
		"cost": 50, "help": 1, "risk": 4
	}
	_paused = false
	_open_org()


func _open_bribe() -> void:
	_paused = true
	var ev := BribeEvent.new()
	ev.visitor_name = String(_visitor.get("name", ""))
	add_child(ev)
	ev.chosen.connect(_on_bribe_choice.bind(ev))

func _on_bribe_choice(kind: String, ev: Control) -> void:
	if kind == "accept":
		State.money += 20
		State.bribe_count += 1
		State.corruption += 1
		_unlock_ach("corrupt", "腐败的检察员")
		_msg("你收下了二十元。纸币很旧，边角磨得起毛。腐败 +1。", Color("#e8dfae"))
		card.play_stamp("收 下", Color("#a57c2a"))
	elif kind == "arrest":
		var bonus := 20
		if State.talent == "justice":
			bonus += 10
		State.money += bonus
		State.arrest_count += 1
		_unlock_ach("firstArrest", "执法如山")
		_msg("你把钱推回去，按下了对讲机。嘉奖 +%d 元。" % bonus, Color("#a8d08a"))
		card.play_stamp("逮 捕", Color("#c8963a"))
	else:
		State.money -= 10
		_msg("你把钱推回去，照章罚款 10 元。他没再说话。", Color("#e0a080"))
		card.play_stamp("拒 收", Color("#a6301f"))
	State.wrong_today += 1
	State.wrong_total += 1
	State.handled_today += 1
	if is_instance_valid(ev):
		ev.queue_free()
	_paused = false
	_awaiting_next = true
	_next_btn.visible = true
	_refresh_hud()


func debug_bribe() -> void:
	_paused = false
	_open_bribe()


func _on_org_requested(mail_id: int) -> void:
	for c in get_children():
		if c is EduTerminal:
			c.queue_free()
	_paused = false
	if State.pending_org.is_empty():
		_msg("这封邮件已经处理过了。", Color("#7d8a7a"))
		return
	_open_org(mail_id)

func _check_achievements() -> void:
	if State.correct_total >= 10:
		_unlock_ach("tenCorrect", "十连正确")
	if State.reported_count >= 3:
		_unlock_ach("whistleblower", "举报者")
	if State.trust >= 5:
		_unlock_ach("undercover", "地下工作者")


func _icon_button(btn: Button, icon_name: String) -> void:
	var path := "res://art/icons/%s.png" % icon_name
	if ResourceLoader.exists(path):
		btn.icon = load(path)
		btn.expand_icon = false
		btn.add_theme_constant_override("icon_max_width", 22)


func _ghost_button(b: Button) -> void:
	b.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 9))
	b.add_theme_stylebox_override("hover", Ui.style(Color(1, 1, 1, 0.07), Color(1, 1, 1, 0.12), 1, 0, 9))
	b.add_theme_stylebox_override("pressed", Ui.style(Color(0, 0, 0, 0.28), Color(0, 0, 0, 0), 0, 0, 9))

func _open_drawer() -> void:
	_paused = true
	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	overlay.add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 24)
	paper.position = Vector2(640, 280)
	paper.size = Vector2(640, 520)
	overlay.add_child(paper)
	var head := Ui.label("证 物 袋", 28, Ui.INK, Ui.font_serif())
	head.position = Vector2(36, 26)
	head.size = Vector2(300, 34)
	paper.add_child(head)
	var sub := Ui.label("没收登记：伪造 %d 件　正常介绍信 %d 封" % [State.confiscatedItems.size(), State.confiscatedNormalLetters], 14, Ui.INK_SOFT, Ui.font_mono())
	sub.position = Vector2(36, 68)
	sub.size = Vector2(560, 20)
	paper.add_child(sub)
	var list := Ui.rich("", 15, Ui.INK)
	list.position = Vector2(36, 100)
	list.size = Vector2(568, 320)
	list.scroll_active = false
	var txt := ""
	if State.confiscatedItems.is_empty():
		txt = "抽屉是空的。"
	else:
		for item in State.confiscatedItems:
			txt += "第 %d 天　%s　%s\n" % [int(item.get("day", 0)), String(item.get("name", "")), "伪造" if String(item.get("kind", "")) == "forged" else "正常"]
	list.text = txt
	paper.add_child(list)
	var close := Ui.button("关上抽屉", 16, Ui.INK, Ui.PAPER)
	close.position = Vector2(212, 442)
	close.size = Vector2(216, 46)
	close.pressed.connect(func() -> void:
		overlay.queue_free()
		_paused = false)
	paper.add_child(close)


func debug_gun_at(sc: String) -> void:
	_paused = true
	State.running = false
	var ev := SchoolRush.new()
	ev.scenario = sc
	add_child(ev)
	ev.finished.connect(func(_r: Dictionary) -> void: ev.queue_free())


func debug_black() -> void:
	State.day = 20
	State.money = 400
	debug_terminal("black")


func debug_ending() -> void:
	State.day = 30
	State.money = 245
	State.correct_total = 176
	State.confiscatedNormalLetters = 1
	State.trust = 0
	State.suspicion = 18
	State.corruption = 0
	_show_ending("stable")


func _open_settings() -> void:
	var sp := SettingsPanel.new()
	add_child(sp)
	sp.closed.connect(func() -> void: sp.queue_free())


func handle_back() -> bool:
	for c in get_children():
		if c is EduTerminal or c is Manual or c is Shop or c is LetterView or c is OrgEvent or c is BribeEvent or c is SettingsPanel:
			c.queue_free()
			_paused = false
			return true
		if c is Control and c.has_meta("modal"):
			c.queue_free()
			_paused = false
			return true
	return false


func _open_guided() -> void:
	var g := GuidedTutorial.new()
	add_child(g)
	g.finished.connect(func() -> void:
		Meta.tutorial_done = true
		Meta.save_meta()
		g.queue_free()
	)

func _open_tutorial() -> void:
	_paused = true
	var tut := Tutorial.new()
	add_child(tut)
	tut.finished.connect(func() -> void:
		Meta.tutorial_done = true
		Meta.save_meta()
		tut.queue_free()
		_paused = false
	)


func _open_interrogation() -> void:
	if _visitor.is_empty() or _awaiting_next:
		return
	_paused = true
	var dlg := Interrogation.new()
	dlg.visitor = _visitor
	dlg.today = State.date
	add_child(dlg)
	dlg.supplied.connect(func() -> void:
		_build_docs()
		card.set_visitor(_visitor, State.date)
	)
	dlg.spend.connect(func(sec: float) -> void:
		State.time_left = maxf(0.0, State.time_left - sec)
	)
	dlg.action.connect(func(kind: String) -> void:
		_called_this = dlg.called
		_db_checked_this = dlg.db_checked
		dlg.queue_free()
		_paused = false
		match kind:
			"approve":
				_judge("approve")
			"reject":
				_judge("reject")
			"arrest":
				_arrest()
			_:
				pass
	)


func _cheats_allowed() -> bool:
	return OS.has_feature("dev") or OS.is_debug_build() or "--cheat" in OS.get_cmdline_user_args()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F2:
		if not _visitor.is_empty():
			_open_face()
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:
		if _cheats_allowed():
			_toggle_cheats()

func _toggle_cheats() -> void:
	for c in get_children():
		if c is CheatMenu:
			c.queue_free()
			return
	var m := CheatMenu.new()
	add_child(m)
	m.cmd.connect(_cheat)

func _cheat(id: String) -> void:
	match id:
		"money+":
			State.money += 200
		"money-":
			State.money -= 200
		"time+":
			State.time_left += 180.0
		"freeze":
			State.time_frozen = not State.time_frozen
		"susp0":
			State.suspicion = 0
		"trust+":
			State.trust += 3
		"upgrades":
			for u in Data.upgrades:
				var key := String(u.get("key", ""))
				if key != "" and not State.has_upgrade(key):
					State.upgrades.append(key)
		"nextday":
			State.time_left = 1.0
			State.time_frozen = false
		"gun12", "gun19", "gun26", "gun30":
			var sc := "d" + id.substr(3)
			_paused = true
			State.running = false
			var ev := SchoolRush.new()
			ev.scenario = sc
			add_child(ev)
			ev.finished.connect(func(r: Dictionary) -> void:
				ev.queue_free()
				_paused = false
			)
		"end_debt", "end_corrupt", "end_escape", "end_revolution", "end_gun", "end_stable":
			_show_ending(id.substr(4))
		"endless":
			State.endless = not State.endless
		"normal", "forged":
			_spawn_visitor()
	_refresh_hud()


func _open_face() -> void:
	var fc := FaceCompare.new()
	fc.visitor = _visitor
	add_child(fc)
	fc.closed.connect(func() -> void: fc.queue_free())


func _build_docs() -> void:
	for c in get_children():
		if c is DocCard:
			c.queue_free()
	var docs: Dictionary = _visitor.get("docs", {})
	if docs.is_empty():
		return
	var cards: Array = []
	var today := State.date
	if docs.has("campus_card") and not bool(docs["campus_card"].get("missing", false)):
		var cc: Dictionary = docs["campus_card"]
		cards.append(["校园卡", [["卡号", String(cc.get("card_no", ""))], ["持卡人", String(cc.get("holder", ""))], ["有效期", String(cc.get("valid_until", ""))]]])
	if docs.has("temp_pass") and not bool(docs["temp_pass"].get("missing", false)):
		var tp: Dictionary = docs["temp_pass"]
		var until := String(tp.get("valid_until", ""))
		cards.append(["临时通行证", [["有效期至", until], ["签发", "校门卫"]]])
	if docs.has("security_pass") and not bool(docs["security_pass"].get("missing", false)):
		var sp: Dictionary = docs["security_pass"]
		var purpose := String(sp.get("purpose", ""))
		cards.append(["纪检部准入证", [["来意", purpose if purpose != "" else "（空白）"]]])
	if docs.has("health_cert") and not bool(docs["health_cert"].get("missing", false)):
		var hc: Dictionary = docs["health_cert"]
		cards.append(["健康证明", [["结论", String(hc.get("status", ""))], ["盖章", "校医务室"]]])
	if docs.has("transfer_letter") and not bool(docs["transfer_letter"].get("missing", false)):
		var tl: Dictionary = docs["transfer_letter"]
		cards.append(["转学介绍信", [["转出", String(tl.get("from_school", ""))], ["转入", String(tl.get("to_school", ""))], ["签名", "见原件（L 键）"]]])
	for k3 in docs.keys():
		if bool(docs[k3].get("missing", false)):
			cards.append(["缺少材料", [["项目", k3], ["说明", "学生未提交"]]])
	var i := 0
	for item in cards:
		var dc := DocCard.new()
		dc.setup(String(item[0]), item[1])
		dc.position = Vector2(380 + i * 30, 500 + i * 24)
		dc.z_index = 6
		dc.dropped.connect(_on_doc_dropped)
		add_child(dc)
		i += 1


func _use_reader() -> void:
	if not State.has_upgrade("reader"):
		_msg("还没买读卡器。办公用品商店有售。", Color("#e0a080"))
		return
	if _visitor.is_empty() or _awaiting_next:
		return
	State.time_left = maxf(0.0, State.time_left - 5.0)
	var cc: Dictionary = _visitor.get("campus_card", {})
	if cc.is_empty():
		_msg("读卡器：没有检测到校园卡。", Color("#cfe0f0"))
	else:
		var ok := bool(cc.get("valid", true))
		_msg("读卡器：校园卡%s。" % ("有效" if ok else "无效 / 已挂失"), Color("#cfe0f0") if ok else Color("#e0a080"))
	_refresh_hud()


func _mirror_stamp(text: String, color: Color) -> void:
	for c in get_children():
		if c is DocCard:
			c.play_stamp(text, color)

func _on_doc_dropped(card: Control) -> void:
	if _reader_btn == null or not is_instance_valid(_reader_btn):
		return
	if card.name != "" and not (card is DocCard):
		return
	var r: Rect2 = _reader_btn.get_global_rect()
	if r.intersects(Rect2(card.global_position, card.size)):
		if card is DocCard and String(card.title) != "校园卡":
			_msg("读卡器只读校园卡。", Color("#e0a080"))
			return
		_use_reader()
		card.play_stamp("已核验", Color(0.2, 0.45, 0.26))
