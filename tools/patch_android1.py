# -*- coding: utf-8 -*-
import io

mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "NOTIFICATION_WM_GO_BACK_REQUEST" not in m:
    m += '''

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		if _desk != null and is_instance_valid(_desk) and _desk.handle_back():
			return
		get_tree().quit()
'''
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func handle_back(" not in d:
    d += '''

func handle_back() -> bool:
	for c in get_children():
		if c is EduTerminal or c is Manual or c is Shop or c is LetterView or c is OrgEvent or c is BribeEvent or c is SettingsPanel:
			c.queue_free()
			_paused = false
			return true
		if c is Control and c.has_meta("modal"):
			c.queue_free()
			_paused = false
			return true
	return false
'''
    d = d.replace('''	var overlay := Control.new()
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)''', '''	var overlay := Control.new()
	overlay.set_meta("modal", true)
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

pp = r"F:\请出示学生证\project.godot"
p = io.open(pp, encoding="utf-8").read()
if "emulate_mouse_from_touch" not in p:
    p = p.replace("[input_devices]", "[input_devices]\n\npointing/emulate_mouse_from_touch=true\npointing/emulate_touch_from_mouse=false")
io.open(pp, "w", encoding="utf-8", newline="\n").write(p)
print("back handling + touch settings")
