# -*- coding: utf-8 -*-
import io
# CardView: letter button
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
if "letter_opened" not in c:
    c = c.replace("signal card_pressed()", "signal card_pressed()\nsignal letter_opened()")
    old = '''	if visitor.has("transfer_letter"):
		var tl: Dictionary = visitor.get("transfer_letter", {})
		out.append(["transfer_letter_from", "转出学校", String(tl.get("from_school", ""))])
		out.append(["transfer_letter_sig", "校长签名", "%s / %s" % [String(tl.get("sig_from", "")), String(tl.get("sig_to", ""))]])'''
    new = '''	if visitor.has("transfer_letter"):
		var tl: Dictionary = visitor.get("transfer_letter", {})
		out.append(["transfer_letter_from", "转出学校", String(tl.get("from_school", ""))])
		out.append(["transfer_letter_sig", "校长签名", "%s / %s" % [String(tl.get("sig_from", "")), String(tl.get("sig_to", ""))]])'''
    c = c.replace(old, new)
    # add button creation before stamp block
    old2 = '''	_stamp_frame = Ui.panel(Color(0, 0, 0, 0), Color(Ui.RED, 0.9), 4, 0, 0)'''
    new2 = '''	if visitor.has("transfer_letter"):
		var lbtn := Ui.button("查看介绍信", 13, Ui.PAPER_DARK, Ui.INK)
		lbtn.position = Vector2(392, 286)
		lbtn.size = Vector2(136, 32)
		lbtn.pressed.connect(func() -> void: letter_opened.emit())
		add_child(lbtn)

	_stamp_frame = Ui.panel(Color(0, 0, 0, 0), Color(Ui.RED, 0.9), 4, 0, 0)'''
    c = c.replace(old2, new2, 1)
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

# Desk: open letter
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "LetterView" not in d:
    d = d.replace('''	card.field_picked.connect(_on_field_picked)
	card.card_pressed.connect(_on_card_pressed)''', '''	card.field_picked.connect(_on_field_picked)
	card.card_pressed.connect(_on_card_pressed)
	card.letter_opened.connect(_open_letter)''')
    d += '''

func _open_letter() -> void:
	if _visitor.is_empty() or not _visitor.has("transfer_letter"):
		return
	var tl: Dictionary = _visitor.get("transfer_letter", {})
	var data := {
		"student_name": String(_visitor.get("name", "")),
		"student_id": String(_visitor.get("student_id", "")),
		"from_school": String(tl.get("from_school", "")),
		"to_school": String(tl.get("to_school", "")),
		"from_sig_id": String(tl.get("from_sig_id", "")),
		"to_sig_id": String(tl.get("to_sig_id", "")),
		"variant_from": String(tl.get("variant_from", "genuine")),
		"variant_to": String(tl.get("variant_to", "genuine"))
	}
	_paused = true
	var view := LetterView.new()
	view.letter = data
	add_child(view)
	view.closed.connect(_close_modal.bind(view))
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Manual: forgery page type
mp = r"F:\请出示学生证\scripts\ui\Manual.gd"
m = io.open(mp, encoding="utf-8").read()
if "_forgery()" not in m:
    m = m.replace('''		"upgrades":
			_body.add_child(_upgrades())''', '''		"forgery":
			_body.add_child(_forgery())
			if page.has("note"):
				_body.add_child(_note(String(page.get("note", ""))))
		"upgrades":
			_body.add_child(_upgrades())''')
    m += '''

func _forgery() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	var variants := [
		["", "真迹：墨色均匀，压痕连续"],
		["_miss", "缺笔：第三笔断裂，断口整齐"],
		["_light", "浅墨：墨色偏灰，网点稀疏"],
		["_plain", "无钢印：纸面无凸起压痕"],
		["_mirror", "镜像：字形左右相反"]
	]
	for item in variants:
		var row := Ui.panel(Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.2), 1, 0, 8)
		row.custom_minimum_size = Vector2(1000, 96)
		var path := "res://art/signatures/wang_ming%s.png" % String(item[0])
		if ResourceLoader.exists(path):
			var tr := TextureRect.new()
			tr.texture = load(path)
			tr.position = Vector2(8, 4)
			tr.size = Vector2(240, 88)
			tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			row.add_child(tr)
		var l := Ui.label(String(item[1]), 15, Ui.INK, Ui.font_serif())
		l.position = Vector2(272, 34)
		l.size = Vector2(700, 26)
		row.add_child(l)
		box.add_child(row)
	return box
'''
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("letter view wired")
