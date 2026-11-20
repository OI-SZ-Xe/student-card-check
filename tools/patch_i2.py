# -*- coding: utf-8 -*-
import io

# State fields
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var event_done" not in s:
    s = s.replace("var flavor := \"\"", "var flavor := \"\"\nvar event_done: Dictionary = {}\nvar shot_org := false\nvar has_fake_id := false\nvar has_ticket := false")
    s = s.replace("\tflavor = \"\"", "\tflavor = \"\"\n\tevent_done = {}\n\tshot_org = false\n\thas_fake_id = false\n\thas_ticket = false")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Save/load
mp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
m = io.open(mp, encoding="utf-8").read()
if "event_done" not in m:
    m = m.replace('"stocks": State.stocks,', '"stocks": State.stocks,\n\t\t"event_done": State.event_done,\n\t\t"shot_org": State.shot_org,\n\t\t"has_fake_id": State.has_fake_id,\n\t\t"has_ticket": State.has_ticket,')
    m = m.replace('State.stock_news = String(data.get("stock_news", ""))', '''State.stock_news = String(data.get("stock_news", ""))
	var raw_events: Variant = data.get("event_done", {})
	if raw_events is Dictionary:
		State.event_done = raw_events
	State.shot_org = bool(data.get("shot_org", false))
	State.has_fake_id = bool(data.get("has_fake_id", false))
	State.has_ticket = bool(data.get("has_ticket", false))''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Desk: triggers + result effects
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	if State.day == 12 and not State.d12_done:
		_open_gun_event()
		return''', '''	if State.day in [12, 19, 26, 30] and not bool(State.event_done.get(str(State.day), false)):
		_open_gun_event()
		return''')
d = d.replace('''	var ev := SchoolRush.new()
	add_child(ev)''', '''	var ev := SchoolRush.new()
	ev.scenario = "d%d" % State.day
	add_child(ev)''')

start = d.index("func _on_gun_finished(")
end = d.index("func debug_gun(")
new_handler = '''func _on_gun_finished(res: Dictionary, ev: Control) -> void:
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

'''
d = d[:start] + new_handler + d[end:]

# ending: shot_org forces gun ending
d = d.replace('''		elif State.trust >= 5:
			k = "revolution"''', '''		elif State.shot_org:
			k = "gun"
		elif State.trust >= 5:
			k = "revolution"''')

# escape requires items
d = d.replace("var can_escape: bool = State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.money >= 150 and not State.escape_ready",
              "var can_escape: bool = State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.has_fake_id and State.has_ticket and not State.escape_ready")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("event triggers + escape conditions")
