# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var time_frozen" not in s:
    s = s.replace("var endless := false", "var endless := false\nvar time_frozen := false")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func _toggle_cheats" not in d:
    d = d.replace('''func _notification(what: int) -> void:''', '''func _notification(what: int) -> void:''')
    d += '''

func _cheats_allowed() -> bool:
	return OS.has_feature("dev") or OS.is_debug_build() or "--cheat" in OS.get_cmdline_user_args()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F1:
		if _cheats_allowed():
			_toggle_cheats()

func _toggle_cheats() -> void:
	for c in get_children():
		if c is CheatMenu:
			c.queue_free()
			return
	var m := CheatMenu.new()
	add_child(m)
	m.cmd.connect(_cheat)

func _cheat(id: String) -> void:
	match id:
		"money+":
			State.money += 200
		"money-":
			State.money -= 200
		"time+":
			State.time_left += 180.0
		"freeze":
			State.time_frozen = not State.time_frozen
		"susp0":
			State.suspicion = 0
		"trust+":
			State.trust += 3
		"upgrades":
			for u in Data.upgrades:
				var key := String(u.get("key", ""))
				if key != "" and not State.has_upgrade(key):
					State.unlock(key)
		"nextday":
			State.time_left = 1.0
			State.time_frozen = false
		"gun12", "gun19", "gun26", "gun30":
			var sc := "d" + id.substr(3)
			_paused = true
			State.running = false
			var ev := SchoolRush.new()
			ev.scenario = sc
			add_child(ev)
			ev.finished.connect(func(r: Dictionary) -> void:
				ev.queue_free()
				_paused = false
			)
		"end_debt", "end_corrupt", "end_escape", "end_revolution", "end_gun", "end_stable":
			_show_ending(id.substr(4))
		"endless":
			State.endless = not State.endless
		"normal", "forged":
			_spawn_visitor()
	_refresh_hud()
'''
# time freeze in process
d = d.replace("State.time_left -= delta", "if not State.time_frozen:\n\t\t\tState.time_left -= delta")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("cheat menu wired")
