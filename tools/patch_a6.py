# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func _open_terminal(" not in d:
    d += '''

func _open_terminal(site: String) -> void:
	if _paused:
		return
	if not State.has_upgrade("quickBookmarks"):
		_browser_load_then(site)
		return
	_paused = true
	State.time_left = maxf(0.0, State.time_left - 2.0)
	var term := EduTerminal.new()
	term.visitor = _visitor
	add_child(term)
	term.time_cost.connect(_on_terminal_cost)
	term.closed.connect(_close_modal.bind(term))

func _browser_load_then(site: String) -> void:
	_paused = true
	var overlay := Control.new()
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var dim := ColorRect.new()
	dim.color = Color(0.02, 0.03, 0.02, 0.8)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	overlay.add_child(dim)
	var label := Ui.label("正在连接教育局网络……", 22, Color("#9ad7a2"), Ui.font_mono())
	label.position = Vector2(0, 520)
	label.size = Vector2(1920, 30)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	overlay.add_child(label)
	Sfx.play("click", -14.0)
	await get_tree().create_timer(1.5).timeout
	if is_instance_valid(overlay):
		overlay.queue_free()
	_paused = false
	State.time_left = maxf(0.0, State.time_left - 3.0)
	_open_terminal(site)

func _on_terminal_cost(seconds: float) -> void:
	State.time_left = maxf(0.0, State.time_left - seconds)
	_refresh_hud()

func debug_terminal(site: String) -> void:
	_paused = false
	_open_terminal(site)
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("terminal funcs appended:", "func _open_terminal(" in io.open(dp, encoding="utf-8").read())
