# -*- coding: utf-8 -*-
import io

# 1) font: keep up to 48 only
gp = r"F:\请出示学生证\tools\gen_font.py"
g = io.open(gp, encoding="utf-8").read()
g = g.replace("SIZES = [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]",
              "SIZES = [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48]")
io.open(gp, "w", encoding="utf-8", newline="\n").write(g)

up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
u = u.replace("for sz in [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]:",
              "for sz in [11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48]:")
u = u.replace('''static func _pick(font: Font, size: int) -> Font:
	if _bitmaps.has(size):
		return _bitmaps[size]''', '''static func _pick(font: Font, size: int) -> Font:
	if size > 48:
		size = 48
	if _bitmaps.has(size):
		return _bitmaps[size]''')
io.open(up, "w", encoding="utf-8", newline="\n").write(u)

# 2) shot waits
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
m = m.replace('''			_start_desk(_shot_mode != "briefing")
			await get_tree().create_timer(1.0).timeout''', '''			_start_desk(_shot_mode != "briefing")
			await get_tree().create_timer(2.0).timeout''')
m = m.replace('''			await get_tree().create_timer(0.9).timeout''', '''			await get_tree().create_timer(2.0).timeout''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# 3) quota affects stable ending
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''		elif State.suspicion >= 70:
			k = "gun"
		else:
			k = "stable"''', '''		elif State.suspicion >= 70:
			k = "gun"
		elif State.quota_missed > 5:
			k = "gun"
		else:
			k = "stable"''')

# 4) debug ending
if "func debug_ending(" not in d:
    d += '''

func debug_ending() -> void:
	State.day = 30
	State.money = 245
	State.correct_total = 176
	State.confiscatedNormalLetters = 1
	State.trust = 0
	State.suspicion = 18
	State.corruption = 0
	_show_ending("stable")
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp2 = r"F:\请出示学生证\scripts\Main.gd"
m2 = io.open(mp2, encoding="utf-8").read()
if 'shot-mode == "ending"' not in m2:
    m2 = m2.replace('''			elif _shot_mode == "gun19":''', '''			elif _shot_mode == "ending":
				_desk.debug_ending()
			elif _shot_mode == "gun19":''')
io.open(mp2, "w", encoding="utf-8", newline="\n").write(m2)

# 5) manual endings show unlocked
mp3 = r"F:\请出示学生证\scripts\ui\Manual.gd"
m3 = io.open(mp3, encoding="utf-8").read()
m3 = m3.replace('''	var rows := [
		["负债", "任意一天余额低于 0 元，立即隔离审查。"],
		["腐败", "收受贿赂累计 3 次，被移交司法机关。"],
		["逃亡", "第 25 天后，手上有正常的转学介绍信、伪造介绍信与高铁票，顶栏出现「启动逃亡」。"],
		["革命", "帮助学生斗争委员会累计 5 次以上，终局未向他们开枪。"],
		["忠诚·枪毙", "帮助过组织但没到 5 次，或怀疑度过高，终局被校园安全部带走。"],
		["忠诚·平稳", "一次没帮组织、拒签达标、怀疑度低，继续担任科员。"]
	]''', '''	var rows := [
		["debt", "负债", "任意一天余额低于 0 元，立即隔离审查。"],
		["corrupt", "腐败", "收受贿赂累计 3 次，被移交司法机关。"],
		["escape", "逃亡", "第 25 天后，手上有正常的转学介绍信、伪造介绍信与高铁票，顶栏出现「启动逃亡」。"],
		["revolution", "革命", "帮助学生斗争委员会累计 5 次以上，终局未向他们开枪。"],
		["gun", "忠诚·枪毙", "帮助过组织但没到 5 次，或怀疑度过高，终局被校园安全部带走。"],
		["stable", "忠诚·平稳", "一次没帮组织、拒签达标、怀疑度低，继续担任科员。"]
	]''')
m3 = m3.replace('''	for r in rows:
		var item := _para("[b]%s[/b]\\n%s" % [String(r[0]), String(r[1])])
		box.add_child(item)''', '''	for r in rows:
		var got: bool = State.endings_seen.has(String(r[0]))
		var tag := "　【已解锁】" if got else "　【未解锁】"
		var item := _para("[b]%s[/b]%s\\n%s" % [String(r[1]), tag, String(r[2])])
		box.add_child(item)''')
io.open(mp3, "w", encoding="utf-8", newline="\n").write(m3)
print("round B/C patches")
