class_name Shop
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal closed
signal changed

var _grid: GridContainer = null
var _balance: Label = null

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.05, 0.06, 0.05, 0.66)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	var panel := Ui.panel(Ui.DESK_DARK, Ui.GOLD, 2, 2, 20)
	panel.position = Vector2(300, 120)
	panel.size = Vector2(1320, 820)
	add_child(panel)

	var title := Ui.label("教 育 局 办 公 用 品 商 店", 26, Ui.WHITE, Ui.font_serif())
	title.position = Vector2(30, 18)
	title.size = Vector2(700, 34)
	panel.add_child(title)
	_balance = Ui.label("余额 %d 元　·　所有工具一经售出概不退换" % State.money, 14, Color(Ui.WHITE, 0.65), Ui.font_mono())
	_balance.position = Vector2(30, 54)
	_balance.size = Vector2(700, 20)
	panel.add_child(_balance)

	var scroll := ScrollContainer.new()
	scroll.position = Vector2(30, 92)
	scroll.size = Vector2(1260, 640)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel.add_child(scroll)
	_grid = GridContainer.new()
	_grid.columns = 3
	_grid.add_theme_constant_override("h_separation", 16)
	_grid.add_theme_constant_override("v_separation", 16)
	scroll.add_child(_grid)

	var close := Ui.button("关闭", 18, Ui.DESK_LIGHT, Ui.WHITE)
	close.position = Vector2(1128, 748)
	close.size = Vector2(160, 46)
	close.pressed.connect(func() -> void: closed.emit())
	panel.add_child(close)

	_refresh()

func _refresh() -> void:
	for c in _grid.get_children():
		c.queue_free()
	var shown := 0
	for u in Data.upgrades:
		_grid.add_child(_make_card(u))
		shown += 1
	if shown == 0:
		var empty := Ui.label("暂无在售商品。第一批外借工具将在第 3 天到货。", 16, Color(0.8, 0.84, 0.76), Ui.font_serif())
		empty.position = Vector2(10, 20)
		empty.size = Vector2(900, 30)
		_grid.add_child(empty)

func _make_card(u: Dictionary) -> Control:
	var uid := String(u.get("id", ""))
	var owned := State.has_upgrade(uid)
	var card := Ui.panel(Color(0.12, 0.14, 0.12), Color(Ui.GOLD, 0.4), 1, 2, 14)
	card.custom_minimum_size = Vector2(408, 232)
	var nm := Ui.label(String(u.get("name", "")), 20, Ui.WHITE, Ui.font_serif())
	nm.position = Vector2(16, 12)
	nm.size = Vector2(360, 26)
	card.add_child(nm)
	var price := Ui.label(("已装备" if owned else "%d 元" % int(u.get("price", 0))), 16, Color(0.6, 0.9, 0.6) if owned else Ui.GOLD, Ui.font_mono())
	price.position = Vector2(16, 42)
	price.size = Vector2(360, 22)
	card.add_child(price)
	var desc := Ui.rich(String(u.get("desc", "")), 14, Color(Ui.WHITE, 0.8))
	desc.position = Vector2(16, 70)
	desc.size = Vector2(376, 96)
	desc.scroll_active = false
	card.add_child(desc)
	var btn := Ui.button("购买" if not owned else "已装备", 16, Ui.DESK_LIGHT, Ui.WHITE)
	btn.position = Vector2(16, 176)
	btn.size = Vector2(150, 40)
	btn.disabled = owned or State.money < int(u.get("price", 0))
	btn.pressed.connect(_on_buy.bind(uid))
	card.add_child(btn)
	return card

func _on_buy(uid: String) -> void:
	if State.buy(uid):
		Sfx.play("chime", -6.0)
		if _balance != null:
			_balance.text = "余额 %d 元　·　所有工具一经售出概不退换" % State.money
		changed.emit()
		_refresh()
	else:
		Sfx.play("error", -8.0)