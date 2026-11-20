# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()

if "var stocks" not in s:
    s = s.replace("var escape_ready := false", "var escape_ready := false\nvar stocks: Array = []\nvar stock_news := \"\"")

    s = s.replace("\tescape_ready = false", "\tescape_ready = false\n\t_init_market()")

    s = s.replace("\t_generate_wanted()", "\tupdate_market()\n\t_generate_wanted()")

    s += '''

func _init_market() -> void:
	stocks = [
		{"name": "实验科技", "code": "SY001", "base": 5.0, "price": 5.0, "prev": 5.0, "positions": []},
		{"name": "深中贸易", "code": "SZ002", "base": 8.5, "price": 8.5, "prev": 8.5, "positions": []},
		{"name": "深高级制造", "code": "SG003", "base": 12.0, "price": 12.0, "prev": 12.0, "positions": []},
		{"name": "实验金融", "code": "SY004", "base": 9.5, "price": 9.5, "prev": 9.5, "positions": []},
		{"name": "深外基建", "code": "SW005", "base": 7.5, "price": 7.5, "prev": 7.5, "positions": []}
	]
	stock_news = ""

func update_market() -> void:
	if stocks.is_empty():
		_init_market()
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	for st in stocks:
		st.prev = st.price
		var drift := rng.randf_range(-0.05, 0.05)
		if talent == "insight":
			drift *= 0.7
		var new_price: float = st.price * (1.0 + drift)
		new_price = clampf(new_price, float(st.base) * 0.5, float(st.base) * 2.0)
		st.price = snappedf(new_price, 0.01)
	stock_news = "今日无重大财经消息。"
	if rng.randf() < 0.4:
		var idx := rng.randi_range(0, stocks.size() - 1)
		var up := rng.randf() < 0.55
		var factor := 1.08 if up else 0.93
		stocks[idx].price = clampf(snappedf(float(stocks[idx].price) * factor, 0.01), float(stocks[idx].base) * 0.5, float(stocks[idx].base) * 2.0)
		stock_news = "%s%s，股价%s。" % [String(stocks[idx].name), "发布新产品" if up else "被曝资金链紧张", "上涨" if up else "下跌"]
	var blown := 0
	for st in stocks:
		var keep: Array = []
		for pos in st.positions:
			var pnl: float = (float(st.price) - float(pos.buy)) * int(pos.shares)
			if pnl + float(pos.margin) <= 0.0:
				blown += 1
			else:
				keep.append(pos)
		st.positions = keep
	if blown > 0:
		stock_news += "　（强制平仓 %d 笔）" % blown

func market_change(st: Dictionary) -> float:
	var prev := float(st.get("prev", 0.0))
	if prev <= 0.0:
		return 0.0
	return (float(st.price) - prev) / prev * 100.0

func buy_stock(idx: int, shares: int, leverage: int, price: float) -> Dictionary:
	if idx < 0 or idx >= stocks.size():
		return {"ok": false, "msg": "无效标的"}
	if shares <= 0 or leverage <= 0:
		return {"ok": false, "msg": "数量或杠杆无效"}
	var notional := price * float(shares)
	var margin := notional / float(leverage)
	if money < int(ceil(margin)):
		return {"ok": false, "msg": "保证金不足"}
	money -= int(ceil(margin))
	stocks[idx].positions.append({"shares": shares, "buy": price, "leverage": leverage, "margin": margin})
	return {"ok": true, "msg": "买入 %d 股 @ %.2f（%dx）" % [shares, price, leverage]}

func sell_stock(idx: int, pos_idx: int, price: float) -> Dictionary:
	if idx < 0 or idx >= stocks.size():
		return {"ok": false, "msg": "无效标的"}
	var positions: Array = stocks[idx].positions
	if pos_idx < 0 or pos_idx >= positions.size():
		return {"ok": false, "msg": "无效持仓"}
	var pos: Dictionary = positions[pos_idx]
	var pnl: float = (price - float(pos.buy)) * int(pos.shares)
	money += int(round(float(pos.margin) + pnl))
	positions.remove_at(pos_idx)
	return {"ok": true, "msg": "平仓：%+.2f 元" % pnl}

func position_pnl(st: Dictionary, pos: Dictionary) -> float:
	return (float(st.price) - float(pos.buy)) * int(pos.shares)
'''
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("market state added")
