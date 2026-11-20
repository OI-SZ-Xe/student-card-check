# -*- coding: utf-8 -*-
import io

sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var bribe_count" not in s:
    s = s.replace("var endings_seen: Dictionary = {}", "var endings_seen: Dictionary = {}\nvar bribe_count := 0\nvar arrest_count := 0\nvar run_start_msec := 0\nvar daily_wrong: Array = []")
    s = s.replace("\tendings_seen = {}", "\tendings_seen = {}\n\tbribe_count = 0\n\tarrest_count = 0\n\trun_start_msec = Time.get_unix_time_from_system()\n\tdaily_wrong = []")
    s = s.replace("\tquota_missed += 1", "\tquota_missed += 1")
# record daily wrong at finish_day
if "daily_wrong.append" not in s:
    s = s.replace('''func finish_day() -> Dictionary:''', '''func finish_day() -> Dictionary:
	daily_wrong.append(wrong_today)''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "_open_settings" not in d:
    # settings button in right panel row
    d = d.replace('''	var reset := Ui.button("重新入职", 15, Color(0.32, 0.18, 0.16), Color("#f0d8c8"))''', '''	var set_btn := Ui.button("设置", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))
	set_btn.position = Vector2(600, 40)
	set_btn.size = Vector2(96, 42)
	set_btn.pressed.connect(_open_settings)
	panel.add_child(set_btn)
	var reset := Ui.button("重新入职", 15, Color(0.32, 0.18, 0.16), Color("#f0d8c8"))''')
    d += '''

func _open_settings() -> void:
	var sp := SettingsPanel.new()
	add_child(sp)
	sp.closed.connect(func() -> void: sp.queue_free())
'''
# bribe count
d = d.replace('''	if kind == "accept":
		State.money += 20''', '''	if kind == "accept":
		State.money += 20
		State.bribe_count += 1''')
# arrest count
d = d.replace('''		State.money += bonus
		_unlock_ach("firstArrest", "执法如山")''', '''		State.money += bonus
		State.arrest_count += 1
		_unlock_ach("firstArrest", "执法如山")''')
# ending stats additions
d = d.replace('''	var gallery := Ui.label("结局图鉴：%d / 6" % State.endings_seen.size(), 14, Ui.INK_SOFT, Ui.font_mono())''', '''	var minutes := int((Time.get_unix_time_from_system() - State.run_start_msec) / 60.0)
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
	var gallery := Ui.label("结局图鉴：%d / 6" % State.endings_seen.size(), 14, Ui.INK_SOFT, Ui.font_mono())''')
# move gallery/button down to avoid overlap
d = d.replace('''	gallery.position = Vector2(48, 560)''', '''	gallery.position = Vector2(380, 610)''')
d = d.replace('''	btn.position = Vector2(48, 640)
	btn.size = Vector2(220, 52)''', '''	btn.position = Vector2(48, 676)
	btn.size = Vector2(220, 50)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("settings button + run stats")
