# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# org: notify instead of modal
d = d.replace('''	if not State.pending_org.is_empty():
		_open_org()
		return
	State.running = true''', '''	if not State.pending_org.is_empty():
		_msg("收件箱里有一封学生斗争委员会的邮件。打开教育局系统处理。", Color("#e8dfae"))
	State.running = true''')

# open org accepts mail id
d = d.replace('''func _open_org() -> void:
	_paused = true''', '''func _open_org(mail_id: int = -1) -> void:
	_paused = true
	State.set_meta("org_mail_id", mail_id)''')

# on org choice: drop mail
d = d.replace('''	State.pending_org = {}
	if is_instance_valid(ev):''', '''	var mail_id: int = int(State.get_meta("org_mail_id", -1))
	if mail_id >= 0:
		var keep: Array = []
		for m in State.mails:
			if int(m.get("id", 0)) != mail_id:
				keep.append(m)
		State.mails = keep
	State.pending_org = {}
	if is_instance_valid(ev):''')

# connect terminal signal in both open paths
d = d.replace('''	term.time_cost.connect(_on_terminal_cost)
	term.closed.connect(_close_modal.bind(term))''', '''	term.time_cost.connect(_on_terminal_cost)
	term.org_requested.connect(_on_org_requested)
	term.closed.connect(_close_modal.bind(term))''')

if "func _on_org_requested(" not in d:
    d += '''

func _on_org_requested(mail_id: int) -> void:
	for c in get_children():
		if c is EduTerminal:
			c.queue_free()
	_paused = false
	if State.pending_org.is_empty():
		_msg("这封邮件已经处理过了。", Color("#7d8a7a"))
		return
	_open_org(mail_id)

func _check_achievements() -> void:
	if State.correct_total >= 10:
		_unlock_ach("tenCorrect", "十连正确")
	if State.reported_count >= 3:
		_unlock_ach("whistleblower", "举报者")
	if State.trust >= 5:
		_unlock_ach("undercover", "地下工作者")
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Terminal signal exists in both constructions? debug_terminal also connects
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	term.start_site = site
	add_child(term)
	term.time_cost.connect(_on_terminal_cost)''', '''	term.start_site = site
	add_child(term)
	term.time_cost.connect(_on_terminal_cost)
	term.org_requested.connect(_on_org_requested)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# flavor in State.start_day
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var flavor" in s and "flavor =" not in s.split("func start_day")[1].split("func ")[0]:
    s = s.replace('''	time_left = 600.0''', '''	time_left = 600.0
	var frng := RandomNumberGenerator.new()
	frng.randomize()
	var flavors := [
		"一只橘猫跑进检查站，被你用水杯赶了出去。",
		"一个低年级学生递给你一瓶水，说「辛苦了」。",
		"窗外下起雨，你想起自己没带伞。",
		"广播里在念校长的讲话，声音有点失真。",
		"食堂阿姨给你留了一份午饭，已经凉了。",
		"有个学生对你敬礼，说「谢谢检察员」。"
	]
	flavor = ""
	if frng.randf() < 0.5:
		flavor = String(flavors[frng.randi() % flavors.size()])''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)
print("E wiring done")
