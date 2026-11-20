# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Manual.gd"
s = io.open(p, encoding="utf-8").read()
start = s.index("func _endings() -> Control:")
new = '''func _endings() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	var rows := [
		["负债", "任意一天余额低于 0 元，立即隔离审查。"],
		["腐败", "收受贿赂累计 3 次，被移交司法机关。"],
		["逃亡", "第 25 天后，手上有正常的转学介绍信、伪造介绍信与高铁票，顶栏出现「启动逃亡」。"],
		["革命", "帮助学生斗争委员会累计 5 次以上，终局未向他们开枪。"],
		["忠诚·枪毙", "帮助过组织但没到 5 次，或怀疑度过高，终局被校园安全部带走。"],
		["忠诚·平稳", "一次没帮组织、拒签达标、怀疑度低，继续担任科员。"]
	]
	for r in rows:
		var item := _para("[b]%s[/b]\\n%s" % [String(r[0]), String(r[1])])
		box.add_child(item)
	return box

func _achv() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	for a in State.ACHIEVEMENTS:
		var got: bool = State.achievements.has(String(a.key))
		var line := "%s　%s　—　%s" % ["■" if got else "□", String(a.name), String(a.desc)]
		box.add_child(_para(line))
	return box
'''
s = s[:start] + new
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("manual pages fixed")
