# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()

old_tip = '''	var tip := Ui.rich("[b]今日提示[/b]\\n· 出生年与年级对不上，是本校门最常见的问题。\\n· 照片换脸不会写在脸上，但会写在证件照里。\\n· 介绍信要看两枚签名，缺一枚也是缺。\\n· 拒签数不够，安全部会来信。", 14, Color("#c8c2aa"))
	tip.position = Vector2(18, 100)
	tip.size = Vector2(660, 240)
	tip.scroll_active = false
	panel.add_child(tip)'''
new_tip = '''	var term_label := Ui.label("教育局办公系统", 15, Color("#9ad7a2"), Ui.font_mono())
	term_label.position = Vector2(18, 100)
	term_label.size = Vector2(400, 22)
	panel.add_child(term_label)

	if State.has_upgrade("quickBookmarks"):
		var sites := [["schools", "学校信息库"], ["phone", "电话簿"], ["rules", "准入规定"], ["wanted", "协查通报"], ["archive", "档案查询"], ["mail", "收件箱"], ["achv", "成就"]]
		var sx := 18
		var sy := 130
		for i in sites.size():
			var b := Ui.button(String(sites[i][1]), 13, Color(0.10, 0.16, 0.12), Color("#9ad7a2"))
			b.position = Vector2(sx + (i % 2) * 336, sy + int(i / 2) * 42)
			b.size = Vector2(320, 36)
			var key := String(sites[i][0])
			b.pressed.connect(func() -> void: _open_terminal(key))
			panel.add_child(b)
	else:
		var open_btn := Ui.button("打开浏览器", 16, Color(0.10, 0.16, 0.12), Color("#9ad7a2"))
		open_btn.position = Vector2(18, 132)
		open_btn.size = Vector2(240, 42)
		open_btn.pressed.connect(func() -> void: _open_terminal("schools"))
		panel.add_child(open_btn)
		var hint := Ui.label("每次查资料要先进浏览器、再进收藏夹。\\n买「快捷收藏夹」可把站点钉在桌面。", 13, Color("#7d8a7a"), Ui.font_serif())
		hint.position = Vector2(18, 186)
		hint.size = Vector2(640, 60)
		panel.add_child(hint)'''
assert old_tip in d
d = d.replace(old_tip, new_tip)

# stats position lower
d = d.replace("\t_stats_label.position = Vector2(18, 360)", "\t_stats_label.position = Vector2(18, 392)")

if "_open_terminal" not in d:
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
	_open_terminal(site)
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# Main: terminal shot mode
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "debug_terminal" not in m:
    m = m.replace('''			elif _shot_mode == "gun":''', '''			elif _shot_mode == "terminal":
				_desk.debug_terminal("schools")
			elif _shot_mode == "terminal_wanted":
				_desk.debug_terminal("wanted")
			elif _shot_mode == "terminal_rules":
				_desk.debug_terminal("rules")
			elif _shot_mode == "gun":''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("terminal wired")
