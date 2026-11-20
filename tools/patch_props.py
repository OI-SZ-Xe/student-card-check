# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# tools panel: tray background + ghost buttons + phone sprite
old_tools = '''	var tools := Ui.panel(Color(0.10, 0.11, 0.10, 0.55), Color(0.5, 0.48, 0.34, 0.45), 1, 3, 14)
	tools.position = Vector2(740, 496)
	tools.size = Vector2(410, 236)
	add_child(tools)
	var t := Ui.label("桌 面 工 具", 16, Color("#d8d2b8"), Ui.font_serif())
	t.position = Vector2(18, 10)
	t.size = Vector2(200, 22)
	tools.add_child(t)'''
new_tools = '''	var tools := Ui.panel(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0)
	tools.position = Vector2(740, 496)
	tools.size = Vector2(410, 236)
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
	var phone_prop := TextureButton.new()
	phone_prop.texture_normal = load("res://art/props/phone.png")
	phone_prop.position = Vector2(352, 2)
	phone_prop.size = Vector2(48, 48)
	phone_prop.pressed.connect(_open_phone)
	tools.add_child(phone_prop)'''
assert old_tools in d
d = d.replace(old_tools, new_tools)

# ghost buttons for tools
for name in ["_compare_btn", "_magnify_btn", "_uv_btn"]:
    pass
d = d.replace('''	_icon_button(_compare_btn, "compare")''', '''	_ghost_button(_compare_btn)
	_icon_button(_compare_btn, "compare")''')
d = d.replace('''	_icon_button(_magnify_btn, "magnifier")''', '''	_ghost_button(_magnify_btn)
	_icon_button(_magnify_btn, "magnifier")''')
d = d.replace('''	_icon_button(_uv_btn, "uv")''', '''	_ghost_button(_uv_btn)
	_icon_button(_uv_btn, "uv")''')
d = d.replace('''	_icon_button(phone, "phone")''', '''	_ghost_button(phone)
	_icon_button(phone, "phone")''')
d = d.replace('''	_icon_button(manual_btn, "book")''', '''	_ghost_button(manual_btn)
	_icon_button(manual_btn, "book")''')
d = d.replace('''	_icon_button(shop_btn, "shop")''', '''	_ghost_button(shop_btn)
	_icon_button(shop_btn, "shop")''')

# rebuild stamps with sprites
start = d.index("func _build_stamps() -> void:")
end = d.index("func _build_right_panel() -> void:")
new_stamps = '''func _build_stamps() -> void:
	var panel := Ui.panel(Color(0.13, 0.12, 0.10, 0.6), Color(0.55, 0.45, 0.28, 0.5), 1, 3, 14)
	panel.position = Vector2(740, 748)
	panel.size = Vector2(410, 216)
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

'''
d = d[:start] + new_stamps + d[end:]

# drawer prop in right panel
d = d.replace('''	_stats_label = Ui.label("", 13, Color("#8f9a84"), Ui.font_mono())''', '''	var drawer := TextureButton.new()
	drawer.texture_normal = load("res://art/props/drawer.png")
	drawer.position = Vector2(500, 408)
	drawer.size = Vector2(176, 72)
	drawer.pressed.connect(_open_drawer)
	panel.add_child(drawer)
	var dlabel := Ui.label("证物", 12, Color("#c8c2aa"), Ui.font_serif())
	dlabel.position = Vector2(560, 470)
	dlabel.size = Vector2(80, 18)
	panel.add_child(dlabel)

	_stats_label = Ui.label("", 13, Color("#8f9a84"), Ui.font_mono())''')

if "func _ghost_button(" not in d:
    d += '''

func _ghost_button(b: Button) -> void:
	b.add_theme_stylebox_override("normal", Ui.style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 9))
	b.add_theme_stylebox_override("hover", Ui.style(Color(1, 1, 1, 0.07), Color(1, 1, 1, 0.12), 1, 0, 9))
	b.add_theme_stylebox_override("pressed", Ui.style(Color(0, 0, 0, 0.28), Color(0, 0, 0, 0), 0, 0, 9))

func _open_drawer() -> void:
	_paused = true
	var overlay := Control.new()
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
			txt += "第 %d 天　%s　%s\\n" % [int(item.get("day", 0)), String(item.get("name", "")), "伪造" if String(item.get("kind", "")) == "forged" else "正常"]
	list.text = txt
	paper.add_child(list)
	var close := Ui.button("关上抽屉", 16, Ui.INK, Ui.PAPER)
	close.position = Vector2(212, 442)
	close.size = Vector2(216, 46)
	close.pressed.connect(func() -> void:
		overlay.queue_free()
		_paused = false)
	paper.add_child(close)
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("props wired")
