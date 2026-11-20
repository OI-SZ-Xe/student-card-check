# -*- coding: utf-8 -*-
import io

# State flag
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "d12_done" not in s:
    s = s.replace("var slot := 1", "var slot := 1\nvar d12_done := false")
    s = s.replace("\tending = \"\"", "\tending = \"\"\n\td12_done = false")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Save/Load
mp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
m = io.open(mp, encoding="utf-8").read()
if "d12_done" not in m:
    m = m.replace('"quota_done": State.quota_done,', '"quota_done": State.quota_done,\n\t\t"d12_done": State.d12_done,')
    m = m.replace('State.quota_done = int(data.get("quota_done", 0))', 'State.quota_done = int(data.get("quota_done", 0))\n\tState.d12_done = bool(data.get("d12_done", false))')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Desk: trigger + handler + debug
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''func _begin_shift() -> void:
	if State.money < 0:
		_show_ending("debt")
		return
	State.running = true'''
new = '''func _begin_shift() -> void:
	if State.money < 0:
		_show_ending("debt")
		return
	if State.day == 12 and not State.d12_done:
		_open_gun_event()
		return
	State.running = true'''
assert old in d
d = d.replace(old, new)
if "_open_gun_event" not in d.split("func _begin_shift")[0]:
    d += '''

func _open_gun_event() -> void:
	_paused = true
	State.running = false
	var ev := SchoolRush.new()
	add_child(ev)
	ev.finished.connect(_on_gun_finished.bind(ev))

func _on_gun_finished(res: Dictionary, ev: Control) -> void:
	State.d12_done = true
	State.money += int(res.get("money", 0))
	State.add_suspicion(int(res.get("suspicion", 0)))
	if is_instance_valid(ev):
		ev.queue_free()
	_paused = false
	_refresh_hud()
	var report := String(res.get("report", "honest"))
	var report_cn := "如实上报"
	if report == "hide":
		report_cn = "隐去误伤"
	elif report == "frame":
		report_cn = "记在周睿名下"
	_msg("D12 校门冲击：击倒 %d 人，误伤学生 %d 人，校警 %s。报告：%s。余额 %+d 元，怀疑度 %+d。" % [
		int(res.get("hostiles", 0)), int(res.get("students", 0)),
		"受伤" if bool(res.get("guard", false)) else "无碍",
		report_cn, int(res.get("money", 0)), int(res.get("suspicion", 0))
	], Color("#e8dfae"))
	_begin_shift()

func debug_gun(auto_resolve: bool = false) -> void:
	_open_gun_event()
	if auto_resolve:
		await get_tree().create_timer(1.0).timeout
		for c in get_children():
			if c is SchoolRush:
				c._resolve()
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Main: gun shot modes
mp2 = r"F:\请出示学生证\scripts\Main.gd"
mm = io.open(mp2, encoding="utf-8").read()
if '"gun"' not in mm:
    mm = mm.replace('''			elif _shot_mode == "letter":''', '''			elif _shot_mode == "gun":
				_desk.debug_gun(false)
			elif _shot_mode == "gunresult":
				_desk.debug_gun(true)
			elif _shot_mode == "letter":''')
io.open(mp2, "w", encoding="utf-8", newline="\n").write(mm)
print("gun wired")
