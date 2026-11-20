# -*- coding: utf-8 -*-
import io
# State: talent
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var talent" not in s:
    s = s.replace("var player_class := \"八年级（3）班\"", "var player_class := \"八年级（3）班\"\nvar talent := \"\"")
    s = s.replace("\tplayer_class = \"八年级（3）班\"", "\tplayer_class = \"八年级（3）班\"\n\ttalent = \"\"")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# Register: talent buttons
rp = r"F:\请出示学生证\scripts\ui\Register.gd"
r = io.open(rp, encoding="utf-8").read()
if "talent" not in r:
    r = r.replace("signal submitted(player_name: String, player_class: String)",
                  "signal submitted(player_name: String, player_class: String, talent: String)")
    r = r.replace("var _hint: Label = null", "var _hint: Label = null\nvar _talent := \"economic\"\nvar _talent_btns: Array = []")
    r = r.replace('''	var btn := Ui.button("确认并提交", 20, Ui.INK, Ui.PAPER)''', '''	var talent_label := Ui.label("入职特长（三选一）", 18, Ui.INK, Ui.font_serif())
	talent_label.position = Vector2(48, 372)
	talent_label.size = Vector2(300, 24)
	paper.add_child(talent_label)
	var talents := [["economic", "经济头脑"], ["justice", "正义感"], ["insight", "洞察力"]]
	for i in talents.size():
		var tb := Ui.button(String(talents[i][1]), 15, Ui.PAPER_DARK, Ui.INK)
		tb.position = Vector2(48 + i * 210, 402)
		tb.size = Vector2(196, 40)
		var key := String(talents[i][0])
		tb.pressed.connect(func() -> void: _pick_talent(key))
		paper.add_child(tb)
		_talent_btns.append(tb)

	var btn := Ui.button("确认并提交", 20, Ui.INK, Ui.PAPER)''')
    r = r.replace('\tbtn.position = Vector2(250, 384)', '\tbtn.position = Vector2(250, 462)')
    r = r.replace('\tfoot.position = Vector2(48, 474)', '\tfoot.position = Vector2(48, 540)')
    r = r.replace('\tpaper.size = Vector2(760, 540)', '\tpaper.size = Vector2(760, 600)')
    r = r.replace('''	Sfx.play("stamp", -8.0)
	submitted.emit(pname, pclass)''', '''	Sfx.play("stamp", -8.0)
	submitted.emit(pname, pclass, _talent)''')
    r += '''

func _pick_talent(key: String) -> void:
	_talent = key
	_refresh_talent()

func _refresh_talent() -> void:
	var keys := ["economic", "justice", "insight"]
	for i in _talent_btns.size():
		var b: Button = _talent_btns[i]
		var on: bool = keys[i] == _talent
		b.add_theme_stylebox_override("normal", Ui.style(Ui.RED if on else Ui.PAPER_DARK, Color(0, 0, 0, 0), 0, 0, 9))
		b.add_theme_color_override("font_color", Ui.PAPER if on else Ui.INK)
'''
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# Main: 3-arg handler
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
m = m.replace("func _on_registered(pname: String, pclass: String) -> void:", "func _on_registered(pname: String, pclass: String, talent: String = \"\") -> void:")
m = m.replace("\tState.player_name = pname\n\tState.player_class = pclass", "\tState.player_name = pname\n\tState.player_class = pclass\n\tState.talent = talent")
m = m.replace('_on_registered("周予安", "八年级（2）班")', '_on_registered("周予安", "八年级（2）班", "insight")')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Desk: justice reward + insight free first compare
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''		delta = int(Data.fee("correct_simple", 10)) if State.simple_mode else int(Data.fee("correct_normal", 5))''',
'''		delta = int(Data.fee("correct_simple", 10)) if State.simple_mode else int(Data.fee("correct_normal", 5))
		if State.talent == "justice":
			delta += 5''')
d = d.replace('''		var hint := RuleEngine.compare_hint(_first_field, fid, _visitor, State.date)
		State.time_left = maxf(0.0, State.time_left - 2.0)''',
'''		var hint := RuleEngine.compare_hint(_first_field, fid, _visitor, State.date)
		if State.talent == "insight" and not State.has_meta("compare_used"):
			State.set_meta("compare_used", true)
		else:
			State.time_left = maxf(0.0, State.time_left - 2.0)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("talent wired")
