# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# 1) org trigger in _begin_shift
old = '''	if State.day == 12 and not State.d12_done:
		_open_gun_event()
		return
	State.running = true'''
new = '''	if State.day == 12 and not State.d12_done:
		_open_gun_event()
		return
	if not State.pending_org.is_empty():
		_open_org()
		return
	State.running = true'''
assert old in d
d = d.replace(old, new)

# 2) handlers appended
if "func _open_org(" not in d:
    d += '''

func _open_org() -> void:
	_paused = true
	State.running = false
	var ev := OrgEvent.new()
	ev.data = State.pending_org
	add_child(ev)
	ev.chosen.connect(_on_org_choice.bind(ev))

func _on_org_choice(kind: String, ev: Control) -> void:
	var data: Dictionary = State.pending_org
	var subject := String(data.get("subject", ""))
	if kind == "help":
		var cost := int(data.get("cost", 0))
		if State.money < cost:
			_msg("你拿不出这笔钱。信被退回了。", Color("#e0a080"))
		else:
			State.money -= cost
			State.add_trust(int(data.get("help", 1)))
			State.add_suspicion(int(data.get("risk", 0)))
			_unlock_ach("undercover", "暗中支持")
			_msg("你帮了他们。信任 +%d，怀疑度 +%d。" % [int(data.get("help", 1)), int(data.get("risk", 0))], Color("#a8d08a"))
	elif kind == "report":
		State.reported_count += 1
		State.money += 10
		State.add_suspicion(-2)
		_unlock_ach("whistleblower", "举报者")
		_msg("你把邮件内容报给了纪检部。嘉奖 +10 元。", Color("#e8dfae"))
	else:
		_msg("你删掉了这封邮件。", Color("#7d8a7a"))
	State.pending_org = {}
	if is_instance_valid(ev):
		ev.queue_free()
	_paused = false
	_begin_shift()

func _unlock_ach(key: String, ach_name: String) -> void:
	if State.unlock(key, ach_name):
		_msg("成就解锁：%s" % ach_name, Color("#ffd98a"))

func _try_escape() -> void:
	State.escape_ready = true
	State.running = false
	_show_ending("")
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("org wired")
