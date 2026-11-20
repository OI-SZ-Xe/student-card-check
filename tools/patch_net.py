# -*- coding: utf-8 -*-
import io, json
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''			await _loading("正在打开 %s ……" % String(s[1]), 1.0)''', '''			await _loading("正在打开 %s ……" % String(s[1]), 0.5 if State.has_upgrade("fastNet") else 1.0)''')
# remove skip button
start = s.find('\tvar skip := Ui.button("跳过", 14, Color("#12281a"), GREEN)')
if start != -1:
    end = s.find('\tskip.pressed.connect(finish)', start)
    end2 = s.find('\n', end) + 1
    s = s[:start] + s[end2:]
s = s.replace('''	var tip := Ui.label("5 秒后进入，可点击跳过", 12, DIM, Ui.font_mono())''', '''	var tip := Ui.label("正在加载，请稍候", 12, DIM, Ui.font_mono())''')
s = s.replace('''	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, 5.0)
	await get_tree().create_timer(5.0).timeout''', '''	var wait := 1.0 if State.has_upgrade("fastNet") else 5.0
	var tw := create_tween()
	tw.tween_property(bar, "value", 1.0, wait)
	await get_tree().create_timer(wait).timeout''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

up = r"F:\请出示学生证\data\upgrades.json"
data = json.load(io.open(up, encoding="utf-8-sig"))
if not any(u.get("key") == "fastNet" for u in data):
    data.append({"key": "fastNet", "name": "快速流量包", "desc": "教育局系统加载 5 秒 → 1 秒，站内跳转 1 秒 → 0.5 秒。", "price": 45, "day": 2})
io.open(up, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))
print("fastNet")
