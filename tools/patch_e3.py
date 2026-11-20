# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

d = d.replace('''	_paused = false
	_begin_shift()

func _save_game''', '''	_paused = false
	_begin_shift()
	if State.flavor != "":
		_msg("今日琐事：" + State.flavor, Color("#c8c2aa"))

func _save_game''')

d = d.replace('''	_msg("电话：" + reply, Color("#cfe0f0"))''', '''	_msg("电话：" + reply, Color("#cfe0f0"))
	_unlock_ach("firstCall", "第一次通话")''')

d = d.replace('''		_msg("对照：" + hint, Color("#f0e6b8"))''', '''		_msg("对照：" + hint, Color("#f0e6b8"))
		_unlock_ach("firstCompare", "第一次比对")''')

d = d.replace('''	var s := State.finish_day()''', '''	if State.wrong_today == 0 and State.handled_today > 0:
		_unlock_ach("perfectDay", "完美执勤")
	var s := State.finish_day()''')

d = d.replace('''func _show_ending(kind: String) -> void:
	State.running = false''', '''func _show_ending(kind: String) -> void:
	State.running = false
	if State.day >= 30:
		_unlock_ach("survivalist", "老油条")''')

d = d.replace('''		State.confiscatedNormalLetters += 1''', '''		State.confiscatedNormalLetters += 1
		_unlock_ach("confiscator", "铁面无私·改")''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("achievement hooks + flavor")
