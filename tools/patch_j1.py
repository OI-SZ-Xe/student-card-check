# -*- coding: utf-8 -*-
import io

# State: endings_seen
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "endings_seen" not in s:
    s = s.replace("var event_done: Dictionary = {}", "var event_done: Dictionary = {}\nvar endings_seen: Dictionary = {}")
    s = s.replace("\tevent_done = {}", "\tevent_done = {}\n\tendings_seen = {}")
    s += '''

func mark_ending(key: String) -> void:
	endings_seen[key] = true
'''
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Save/load endings
mp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
m = io.open(mp, encoding="utf-8").read()
if "endings_seen" not in m:
    m = m.replace('"event_done": State.event_done,', '"event_done": State.event_done,\n\t\t"endings_seen": State.endings_seen,')
    m = m.replace('''	if raw_events is Dictionary:
		State.event_done = raw_events''', '''	if raw_events is Dictionary:
		State.event_done = raw_events
	var raw_endings: Variant = data.get("endings_seen", {})
	if raw_endings is Dictionary:
		State.endings_seen = raw_endings''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Desk: new ending presentation
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
start = d.index("func _show_ending(kind: String) -> void:")
end = d.index("func _msg(")
new = '''func _show_ending(kind: String) -> void:
	State.running = false
	if State.day >= 30:
		_unlock_ach("survivalist", "老油条")
	_paused = true
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
		else:
			k = "stable"
	State.mark_ending(k)
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

	var seal := Ui.label("═════════════════════════════\\n          [ 绝 密 ]\\n═════════════════════════════", 18, Ui.INK, Ui.font_mono())
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
	body.size := Vector2(720, 220)
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

	var sign_line := Ui.label("校园安全部　签发\\n部长　李建国（印）", 15, Ui.INK, Ui.font_serif())
	sign_line.position = Vector2(660, 560)
	sign_line.size = Vector2(320, 52)
	panel.add_child(sign_line)

	var stats := Ui.label("最终余额：%d 元　　执勤天数：%d 天\\n正确审核：%d 次　　没收介绍信：%d 封\\n信任：%d　　怀疑度：%d　　腐败：%d" % [
		State.money, State.day, State.correct_total, State.confiscatedNormalLetters,
		State.trust, State.suspicion, State.corruption
	], 15, Ui.INK, Ui.font_mono())
	stats.position = Vector2(48, 452)
	stats.size = Vector2(560, 80)
	panel.add_child(stats)

	var gallery := Ui.label("结局图鉴：%d / 6" % State.endings_seen.size(), 14, Ui.INK_SOFT, Ui.font_mono())
	gallery.position = Vector2(48, 560)
	gallery.size = Vector2(400, 22)
	panel.add_child(gallery)

	var btn := Ui.button("重新入职", 20, Ui.INK, Ui.PAPER)
	btn.position = Vector2(48, 640)
	btn.size = Vector2(220, 52)
	btn.pressed.connect(_restart)
	panel.add_child(btn)
	Sfx.play("stamp", -4.0)
'''
d = d[:start] + new + d[end:]
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("ending presentation rewritten")
