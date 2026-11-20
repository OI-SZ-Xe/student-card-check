# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(p, encoding="utf-8").read()

old_wait = '''func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout'''
new_wait = '''func _wait(t: float) -> void:
	var elapsed := 0.0
	while elapsed < t:
		if _skip or _ended:
			return
		await get_tree().process_frame
		elapsed += get_process_delta_time()'''
assert old_wait in s
s = s.replace(old_wait, new_wait)

start = s.index("func _run() -> void:")
end = s.index("func _shot_notice_header() -> void:")
new_run = '''func _run() -> void:
	var shots: Array = [
		_shot_notice_header,
		_shot_notice_body,
		_shot_assessment,
		_shot_admission,
		_shot_film_leader,
		_shot_guidance,
		_shot_title
	]
	for shot in shots:
		if _skip or _ended:
			break
		await shot.call()
	if not _ended:
		finished.emit()

'''
s = s[:start] + new_run + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("skip-aware waits")
