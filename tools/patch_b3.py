# -*- coding: utf-8 -*-
import io

# CardView: confiscate button + signal
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
if "confiscate_pressed" not in c:
    c = c.replace("signal letter_opened()", "signal letter_opened()\nsignal confiscate_pressed()")
    c = c.replace('''	if visitor.has("transfer_letter"):
		var lbtn := Ui.button("查看介绍信", 13, Ui.PAPER_DARK, Ui.INK)
		lbtn.position = Vector2(392, 286)
		lbtn.size = Vector2(136, 32)
		lbtn.pressed.connect(func() -> void: letter_opened.emit())
		add_child(lbtn)''', '''	if visitor.has("transfer_letter"):
		var lbtn := Ui.button("查看介绍信", 13, Ui.PAPER_DARK, Ui.INK)
		lbtn.position = Vector2(392, 286)
		lbtn.size = Vector2(136, 32)
		lbtn.pressed.connect(func() -> void: letter_opened.emit())
		add_child(lbtn)
		if State.day >= 25:
			var cbtn := Ui.button("没收介绍信", 13, Color("#c8a24a"), Ui.INK)
			cbtn.position = Vector2(392, 324)
			cbtn.size = Vector2(136, 32)
			cbtn.pressed.connect(func() -> void: confiscate_pressed.emit())
			add_child(cbtn)''')
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

# Desk: connect, confiscate, arrest, escape button
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace("\tcard.letter_opened.connect(_open_letter)", "\tcard.letter_opened.connect(_open_letter)\n\tcard.confiscate_pressed.connect(_confiscate)")

# arrest button in stamps panel
old_stamps = '''	_next_btn = Ui.button("喊 下 一 位 (N)", 18, Color(0.20, 0.28, 0.36), Ui.WHITE)'''
new_stamps = '''	var arrest_btn := Ui.button("逮 捕 (E)", 16, Color(0.32, 0.24, 0.16), Color("#f0e0c8"))
	arrest_btn.position = Vector2(18, 164)
	arrest_btn.size = Vector2(180, 42)
	arrest_btn.pressed.connect(_arrest)
	panel.add_child(arrest_btn)

	_next_btn = Ui.button("喊 下 一 位 (N)", 18, Color(0.20, 0.28, 0.36), Ui.WHITE)'''
assert old_stamps in d
d = d.replace(old_stamps, new_stamps)
d = d.replace('\t_next_btn.position = Vector2(18, 164)\n\t_next_btn.size = Vector2(374, 42)', '\t_next_btn.position = Vector2(212, 164)\n\t_next_btn.size = Vector2(180, 42)')

if "func _confiscate(" not in d:
    d += '''

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
		_msg("已没收伪造的转学介绍信。没有罚款，也没有嘉奖。", Color("#a8d08a"))
	else:
		if State.money < 25:
			_msg("余额不足 25 元，无法办理没收。", Color("#e0a080"))
			return
		State.money -= 25
		State.confiscatedNormalLetters += 1
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
		_msg("逮捕完成，嘉奖 +%d 元。他只是被带走，档案还在。" % bonus, Color("#a8d08a"))
	card.play_stamp("逮 捕", Color("#c8963a"))
	card.shake()
	_awaiting_next = true
	_next_btn.visible = true
	_refresh_hud()
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("confiscate + arrest wired")
