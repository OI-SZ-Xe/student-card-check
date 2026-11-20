# -*- coding: utf-8 -*-
import io

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

old = '''	else:
		delta = -int(Data.fee("wrong", 10))
		State.wrong_today += 1
		State.wrong_total += 1'''
new = '''	else:
		var forged_fields: Array = _visitor.get("forged_fields", [])
		if not forged_fields.is_empty() and randf() < 0.30:
			_open_bribe()
			return
		delta = -int(Data.fee("wrong", 10))
		State.wrong_today += 1
		State.wrong_total += 1'''
assert old in d
d = d.replace(old, new)

if "func _open_bribe(" not in d:
    d += '''

func _open_bribe() -> void:
	_paused = true
	var ev := BribeEvent.new()
	ev.visitor_name = String(_visitor.get("name", ""))
	add_child(ev)
	ev.chosen.connect(_on_bribe_choice.bind(ev))

func _on_bribe_choice(kind: String, ev: Control) -> void:
	if kind == "accept":
		State.money += 20
		State.corruption += 1
		_unlock_ach("corrupt", "腐败的检察员")
		_msg("你收下了二十元。纸币很旧，边角磨得起毛。腐败 +1。", Color("#e8dfae"))
		card.play_stamp("收 下", Color("#a57c2a"))
	elif kind == "arrest":
		var bonus := 20
		if State.talent == "justice":
			bonus += 10
		State.money += bonus
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
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Save/load stocks
sp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
s = io.open(sp, encoding="utf-8").read()
if "stocks" not in s:
    s = s.replace('"d12_done": State.d12_done,', '"d12_done": State.d12_done,\n\t\t"stocks": State.stocks,\n\t\t"stock_news": State.stock_news,')
    s = s.replace('State.d12_done = bool(data.get("d12_done", false))', 'State.d12_done = bool(data.get("d12_done", false))\n\tvar raw_stocks: Variant = data.get("stocks", [])\n\tif raw_stocks is Array and not (raw_stocks as Array).is_empty():\n\t\tState.stocks = raw_stocks\n\tState.stock_news = String(data.get("stock_news", ""))')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("bribe + stock save wired")
