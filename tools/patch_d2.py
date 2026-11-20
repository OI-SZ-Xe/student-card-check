# -*- coding: utf-8 -*-
import io

# 1) Terminal: exchange site
tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
t = t.replace('''	["mail", "收件箱"],
	["achv", "成就"]''', '''	["mail", "收件箱"],
	["exchange", "证券交易所"],
	["achv", "成就"]''')
t = t.replace('''		"mail":
			_site_mail()''', '''		"mail":
			_site_mail()
		"exchange":
			_site_exchange()''')
t += '''

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
			var si := i
			var sj := j
			sell.pressed.connect(func() -> void:
				State.sell_stock(si, sj, float(State.stocks[si].price))
				_show("exchange")
			)
			row.add_child(sell)
			_body.add_child(row)
	if not any:
		_body.add_child(_line("暂无持仓。", DIM, 15))
	_body.add_child(_line("保证金 = 价 × 股数 ÷ 杠杆；亏损吞掉保证金即强制平仓。", DIM, 14))
'''
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)

# 2) Bribe modal
bribe = '''class_name BribeEvent
extends Control

signal chosen(kind: String)

var visitor_name := ""

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.7)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)
	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 28)
	paper.position = Vector2(600, 280)
	paper.size = Vector2(720, 520)
	add_child(paper)
	var head := Ui.label("贿 赂", 32, Ui.INK, Ui.font_serif())
	head.position = Vector2(40, 28)
	head.size = Vector2(300, 42)
	paper.add_child(head)
	var body := Ui.rich(String(visitor_name) + " 把一张折起来的二十元推到窗口下沿。\\n\\n「检察员同学，我爸是校董。您就当没看见，行吗？」", 17, Ui.INK)
	body.position = Vector2(40, 88)
	body.size = Vector2(640, 160)
	body.scroll_active = false
	paper.add_child(body)
	var opts := [
		["accept", "收下", "+20 元　腐败 +1"],
		["refuse", "推回去", "照常罚款 −10 元"],
		["arrest", "叫校警", "+20 元　移交安全部"]
	]
	var y := 276
	for o in opts:
		var b := Ui.button("%s　—　%s" % [String(o[1]), String(o[2])], 17, Ui.INK, Ui.PAPER)
		b.position = Vector2(40, y)
		b.size = Vector2(640, 52)
		var key := String(o[0])
		b.pressed.connect(func() -> void: chosen.emit(key))
		paper.add_child(b)
		y += 62
'''
io.open(r"F:\请出示学生证\scripts\ui\BribeEvent.gd", "w", encoding="utf-8", newline="\n").write(bribe)
print("exchange page + bribe modal")
