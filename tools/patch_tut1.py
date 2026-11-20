# -*- coding: utf-8 -*-
import io

# Meta: tutorial_done
mp = r"F:\请出示学生证\scripts\autoload\Meta.gd"
m = io.open(mp, encoding="utf-8").read()
if "tutorial_done" not in m:
    m = m.replace("var best_day := 0", "var best_day := 0\nvar tutorial_done := false")
    m = m.replace('best_day = int(parsed.get("best_day", 0))', 'best_day = int(parsed.get("best_day", 0))\n\t\ttutorial_done = bool(parsed.get("tutorial_done", false))')
    m = m.replace('"best_day": best_day', '"best_day": best_day,\n\t\t"tutorial_done": tutorial_done')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

# 1) move phone from tray to right panel
d = d.replace('''	var phone_prop := TextureButton.new()
	phone_prop.texture_normal = load("res://art/props/phone.png")
	phone_prop.position = Vector2(152, 2)
	phone_prop.size = Vector2(40, 40)
	phone_prop.pressed.connect(_open_phone)
	tools.add_child(phone_prop)
''', '')

d = d.replace('''	var drawer := TextureButton.new()''', '''	var phone_prop := TextureButton.new()
	phone_prop.texture_normal = load("res://art/props/phone.png")
	phone_prop.position = Vector2(546, 214)
	phone_prop.size = Vector2(84, 84)
	phone_prop.pressed.connect(_open_phone)
	panel.add_child(phone_prop)
	var phone_label := Ui.label("电话", 12, Color("#c8c2aa"), Ui.font_serif())
	phone_label.position = Vector2(572, 298)
	phone_label.size = Vector2(60, 18)
	panel.add_child(phone_label)

	var drawer := TextureButton.new()''')

# 2) tutorial button + auto show
d = d.replace('''	var set_btn := Ui.button("设置", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))''', '''	var tut_btn := Ui.button("教学", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))
	tut_btn.position = Vector2(590, 138)
	tut_btn.size = Vector2(88, 34)
	tut_btn.pressed.connect(_open_tutorial)
	panel.add_child(tut_btn)
	var set_btn := Ui.button("设置", 14, Color(0.18, 0.22, 0.20), Color("#cfe0d0"))''')

if "func _open_tutorial(" not in d:
    d += '''

func _open_tutorial() -> void:
	_paused = true
	var tut := Tutorial.new()
	add_child(tut)
	tut.finished.connect(func() -> void:
		Meta.tutorial_done = true
		Meta.save_meta()
		tut.queue_free()
		_paused = false
	)
'''
    d = d.replace('''	Music.play("bgm_day", 2.0)''', '''	if not Meta.tutorial_done:
		_open_tutorial()
	Music.play("bgm_day", 2.0)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("tutorial + phone moved")
