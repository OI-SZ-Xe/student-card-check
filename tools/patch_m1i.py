# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "debug_letter" not in d:
    d += '''

func debug_letter() -> void:
	var data := {
		"student_name": "苏念",
		"student_id": "20231188",
		"from_school": "深圳中学",
		"to_school": "深圳实验中学",
		"from_sig_id": "li_hua",
		"to_sig_id": "wang_ming",
		"variant_from": "miss",
		"variant_to": "genuine"
	}
	_paused = true
	var view := LetterView.new()
	view.letter = data
	add_child(view)
	view.closed.connect(_close_modal.bind(view))
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if '"letter"' not in m:
    m = m.replace('''			elif _shot_mode == "settle":''', '''			elif _shot_mode == "letter":
				_desk.debug_letter()
			elif _shot_mode == "settle":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("letter debug mode")
