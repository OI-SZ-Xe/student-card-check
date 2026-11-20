# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "flick" not in d:
    d = d.replace('''	glass.add_child(tint)''', '''	glass.add_child(tint)
	var flick := create_tween()
	flick.set_loops()
	flick.tween_property(tint, "color:a", 0.28, 3.4).set_trans(Tween.TRANS_SINE)
	flick.tween_property(tint, "color:a", 0.38, 3.4).set_trans(Tween.TRANS_SINE)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "排队剪影" not in s:
    s = s.replace("## 目录", """## 窗外（本轮）

- 走廊里加了排队学生的像素剪影（四个，带书包），站在玻璃后，轻微上下浮动
- 玻璃暗色层做 3.4 秒循环的呼吸明暗，模拟走廊灯管的工作状态

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("flicker + readme")
