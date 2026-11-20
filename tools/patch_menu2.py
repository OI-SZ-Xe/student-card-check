# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''func _show_ending(kind: String) -> void:
	State.running = false''', '''func _show_ending(kind: String) -> void:
	if State.endless and State.money >= 0:
		return
	State.running = false''')
d = d.replace('''	State.mark_ending(k)''', '''	State.mark_ending(k)
	if State.endless and k == "debt":
		Meta.best_day = maxi(Meta.best_day, State.day)
		Meta.save_meta()''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
if '"browser"' not in t:
    t = t.replace('''	["black", "黑市"],''', '''	["black", "黑市"],
	["browser", "浏览器"],''')
    t = t.replace('''		"black":
			_site_black()''', '''		"black":
			_site_black()
		"browser":
			_site_browser()''')
    t += '''

func _site_browser() -> void:
	_body.add_child(_line("校门检查站 · 内部浏览器", AMBER, 16))
	_body.add_child(_line("书签栏：%s" % ("教育局档案" if State.has_upgrade("fastBookmark") else "（未购买快速收藏夹）"), DIM, 14))
	var sites := [
		["archive", "教育局档案", "调阅学生备案，准确但慢"],
		["schools", "学校信息库", "校长与教导主任名单"],
		["rules", "准入规定", "今日核验项目"]
	]
	for s in sites:
		var b := Ui.button("%s　—　%s" % [String(s[1]), String(s[2])], 16, Color("#12281a"), GREEN)
		b.custom_minimum_size = Vector2(520, 44)
		var key := String(s[0])
		b.pressed.connect(func() -> void:
			_body.add_child(_line("正在打开 %s ……" % String(s[1]), AMBER, 16))
			await get_tree().create_timer(1.6).timeout
			_show(key)
		)
		_body.add_child(b)
'''
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)
print("endless guard + browser")
