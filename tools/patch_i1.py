# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\SchoolRush.gd"
s = io.open(p, encoding="utf-8").read()

if "var scenario" not in s:
    s = s.replace("var _actors: Array = []", "var scenario := \"d12\"\nvar _org_hit := false\nvar _actors: Array = []")

# scenario config in _ready before build
s = s.replace('''	_build()
	_spawn()''', '''	_apply_scenario()
	_build()
	_spawn()''')

# spawn by scenario
old_spawn = '''func _spawn() -> void:
	var h1 := _make_actor("hostile", Vector2(1960, 646), 100, 216)
	var h2 := _make_actor("hostile", Vector2(2080, 700), 106, 224)
	_hostiles.append(h1)
	_hostiles.append(h2)'''
new_spawn = '''func _apply_scenario() -> void:
	match scenario:
		"d19":
			_time_left = 5.0
			_hint.text = "夜间巡逻 · 手电范围外看不见人 · 3 发"
		"d26":
			_time_left = 4.5
			_hint.text = "有人闯进检查站 · 3 发 · 想清楚再开枪"
		"d30":
			_time_left = 8.0
			_hint.text = "校门总攻 · 3 发 · 这一枪决定你站在哪边"
		_:
			_time_left = 7.0

func _spawn() -> void:
	match scenario:
		"d19":
			var h := _make_actor("hostile", Vector2(1980, 700), 104, 220)
			_hostiles.append(h)
			_bystanders.append(_make_actor("student", Vector2(600, 860), 88, 196))
		"d26":
			var org := _make_actor("org", Vector2(1980, 690), 98, 206)
			_hostiles.append(org)
		"d30":
			for i in 3:
				var h2 := _make_actor("hostile", Vector2(1960 + i * 90, 640 + i * 26), 100, 216)
				_hostiles.append(h2)
			_bystanders.append(_make_actor("student", Vector2(620, 850), 90, 200))
		_:
			var h1 := _make_actor("hostile", Vector2(1960, 646), 100, 216)
			var h3 := _make_actor("hostile", Vector2(2080, 700), 106, 224)
			_hostiles.append(h1)
			_hostiles.append(h3)'''
assert old_spawn in s
s = s.replace(old_spawn, new_spawn)

# draw org armband
s = s.replace('''		elif kind == "student":
			draw_rect(Rect2(w * 0.60, h * 0.24, w * 0.16, h * 0.26), c)''', '''		elif kind == "student":
			draw_rect(Rect2(w * 0.60, h * 0.24, w * 0.16, h * 0.26), c)
		elif kind == "org":
			draw_rect(Rect2(w * 0.70, h * 0.26, w * 0.10, h * 0.10), Color(0.75, 0.25, 0.20, 0.95))''')

# hit handling for org
s = s.replace('''		"guard":
			_guard_hit = true
			_hint.text = "击中校警。他把对讲机摔在地上。"''', '''		"guard":
			_guard_hit = true
			_hint.text = "击中校警。他把对讲机摔在地上。"
		"org":
			_org_hit = true
			_hint.text = "你打中了他。袖标上的三个字，你认得。"''')

# result carries scenario + org
s = s.replace('''	var result := {
		"report": kind,''', '''	var result := {
		"scenario": scenario,
		"org_hit": _org_hit,
		"report": kind,''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("school rush scenarios")
