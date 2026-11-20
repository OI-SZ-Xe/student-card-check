# -*- coding: utf-8 -*-
import io

desk = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(desk, encoding="utf-8").read()
d += '''

func debug_judge(kind: String) -> void:
	_judge(kind)

func debug_end_day() -> void:
	_end_day()

func debug_manual_page(idx: int) -> void:
	_paused = true
	var m := Manual.new()
	add_child(m)
	m.closed.connect(_close_modal.bind(m))
	m._show(idx)
'''
io.open(desk, "w", encoding="utf-8", newline="\n").write(d)

main = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(main, encoding="utf-8").read()
old = '''		else:
			_start_desk(true)
			await get_tree().create_timer(1.0).timeout
			if _shot_mode == "manual":
				_desk.debug_open_manual()
			elif _shot_mode == "shop":
				_desk.debug_open_shop()
			await get_tree().create_timer(0.8).timeout'''
new = '''		else:
			_start_desk(_shot_mode != "briefing")
			await get_tree().create_timer(1.0).timeout
			if _shot_mode == "manual":
				_desk.debug_open_manual()
			elif _shot_mode == "shop":
				_desk.debug_open_shop()
			elif _shot_mode == "signatures":
				_desk.debug_manual_page(4)
			elif _shot_mode == "verdict":
				_desk.debug_judge("approve")
			elif _shot_mode == "settle":
				_desk.debug_end_day()
			await get_tree().create_timer(0.9).timeout'''
assert old in m
m = m.replace(old, new)
io.open(main, "w", encoding="utf-8", newline="\n").write(m)
print("debug modes added")
