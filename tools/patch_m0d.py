# -*- coding: utf-8 -*-
import io

# Portrait: hair cap + ears
portrait = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(portrait, encoding="utf-8").read()
old = "\t_ellipse(head_c, rx, ry, skin)\n\t_ellipse(head_c + Vector2(0, -ry * 0.42), rx * 1.04, ry * 0.62, hair)"
new = "\t_ellipse(head_c, rx, ry, skin)\n\tdraw_circle(Vector2(cx - rx * 0.99, head_c.y + ry * 0.06), w * 0.020, skin_dark)\n\tdraw_circle(Vector2(cx + rx * 0.99, head_c.y + ry * 0.06), w * 0.020, skin_dark)\n\t_ellipse(head_c + Vector2(0, -ry * 0.50), rx * 1.03, ry * 0.42, hair)\n\tdraw_rect(Rect2(cx - rx * 1.0, head_c.y - ry * 0.35, w * 0.018, ry * 0.55), hair)\n\tdraw_rect(Rect2(cx + rx * 1.0 - w * 0.018, head_c.y - ry * 0.35, w * 0.018, ry * 0.55), hair)"
assert old in s
s = s.replace(old, new)
s = s.replace("\tvar rx: float = w * 0.175\n\tvar ry: float = h * 0.205", "\tvar rx: float = w * 0.185\n\tvar ry: float = h * 0.215")
io.open(portrait, "w", encoding="utf-8", newline="\n").write(s)

# Desk: chinese stats + docs count in window header
desk = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(desk, encoding="utf-8").read()
old_stats = '''\t_stats_label.text = "today correct %d  wrong %d  seen %d / %d\\nall correct %d  wrong %d\\ncredits %d  suspicion %d" % [
\t\tState.correct_today, State.wrong_today, State.handled_today, State.total_today,
\t\tState.correct_total, State.wrong_total, State.money, State.suspicion
\t]'''
new_stats = '''\t_stats_label.text = "今日　正确 %d　错误 %d　已检 %d / %d\\n累计　正确 %d　错误 %d\\n余额 %d 元　　怀疑度 %d" % [
\t\tState.correct_today, State.wrong_today, State.handled_today, State.total_today,
\t\tState.correct_total, State.wrong_total, State.money, State.suspicion
\t]'''
assert old_stats in d, "stats text not found"
d = d.replace(old_stats, new_stats)

old_school = '''\t_win_school.text = "%s · %d年级%s" % [String(v.get("school", "")), int(v.get("grade", 0)), extra]'''
new_school = '''\tvar doc_count: int = Data.required_docs(State.day, v).size()
\t_win_school.text = "%s · %d年级%s　·　应交材料 %d 份" % [String(v.get("school", "")), int(v.get("grade", 0)), extra, doc_count]'''
assert old_school in d, "school label not found"
d = d.replace(old_school, new_school)

d += '''

func debug_open_manual() -> void:
	_open_manual()

func debug_open_shop() -> void:
	_open_shop()
'''
io.open(desk, "w", encoding="utf-8", newline="\n").write(d)

# Main: shot modes
main = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(main, encoding="utf-8").read()
m = m.replace('var _shot_path := ""', 'var _shot_path := ""\nvar _shot_mode := "desk"')
m = m.replace('''		if arg.begins_with("--shot="):
			_shot_path = arg.substr(7)''', '''		if arg.begins_with("--shot="):
			_shot_path = arg.substr(7)
		elif arg.begins_with("--shot-mode="):
			_shot_mode = arg.substr(12)''')
old_shot = '''	if _shot_path != "":
		_start_desk(true)
		await get_tree().create_timer(1.4).timeout
		await RenderingServer.frame_post_draw'''
new_shot = '''	if _shot_path != "":
		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			add_child(_intro)
			await get_tree().create_timer(7.5).timeout
		else:
			_start_desk(true)
			await get_tree().create_timer(1.0).timeout
			if _shot_mode == "manual":
				_desk.debug_open_manual()
			elif _shot_mode == "shop":
				_desk.debug_open_shop()
			await get_tree().create_timer(0.8).timeout
		await RenderingServer.frame_post_draw'''
assert old_shot in m, "shot block not found"
m = m.replace(old_shot, new_shot)
io.open(main, "w", encoding="utf-8", newline="\n").write(m)

print("patched round 4")
