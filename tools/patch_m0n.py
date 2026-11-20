# -*- coding: utf-8 -*-
import io

# --- Register: fix := on assignments ---
rp = r"F:\请出示学生证\scripts\ui\Register.gd"
r = io.open(rp, encoding="utf-8").read()
r = r.replace("\tsub.size := Vector2(600, 20)", "\tsub.size = Vector2(600, 20)")
r = r.replace("\t_hint.size := Vector2(660, 22)", "\t_hint.size = Vector2(660, 22)")
r = r.replace("\tfoot.size := Vector2(500, 18)", "\tfoot.size = Vector2(500, 18)")
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# --- State: player_class ---
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
s = s.replace('var player_name := "检察员"', 'var player_name := "检察员"\nvar player_class := "八年级（3）班"')
s = s.replace('\tplayer_name = "检察员"\n\tsimple_mode = true', '\tplayer_name = "检察员"\n\tplayer_class = "八年级（3）班"\n\tsimple_mode = true')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# --- SaveManager: persist class ---
mp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
m = io.open(mp, encoding="utf-8").read()
m = m.replace('"player_name": State.player_name,', '"player_name": State.player_name,\n\t\t"player_class": State.player_class,')
m = m.replace('State.player_name = String(data.get("player_name", "检察员"))', 'State.player_name = String(data.get("player_name", "检察员"))\n\tState.player_class = String(data.get("player_class", "八年级（3）班"))')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# --- Main: register before intro ---
ap = r"F:\请出示学生证\scripts\Main.gd"
a = io.open(ap, encoding="utf-8").read()
old = '''	if _shot_path != "":
		if _shot_mode == "intro":'''
new = '''	if _shot_path == "":
		var reg := preload("res://scripts/ui/Register.gd").new()
		add_child(reg)
		reg.submitted.connect(_on_registered)
		return
	if _shot_path != "":
		if _shot_mode == "intro":'''
assert old in a
a = a.replace(old, new)
a = a.replace('''func _on_intro_finished() -> void:''', '''func _on_registered(pname: String, pclass: String) -> void:
	State.player_name = pname
	State.player_class = pclass
	for c in get_children():
		if c is Register:
			c.queue_free()
	_intro = preload("res://scripts/screens/Intro.gd").new()
	_intro.player_name = pname
	_intro.player_class = pclass
	add_child(_intro)
	_intro.finished.connect(_on_intro_finished)

func _on_intro_finished() -> void:''')
io.open(ap, "w", encoding="utf-8", newline="\n").write(a)

# --- Desk HUD: name + class ---
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old_hud = '\tvar right := Ui.label("岗位：纪检部科员　%s" % State.player_name, 16, Color(Ui.WHITE, 0.7), Ui.font_mono())'
new_hud = '\tvar right := Ui.label("纪检部科员　%s　%s" % [State.player_name, State.player_class], 16, Color(Ui.WHITE, 0.7), Ui.font_mono())'
assert old_hud in d
d = d.replace(old_hud, new_hud)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

print("patched register flow")
