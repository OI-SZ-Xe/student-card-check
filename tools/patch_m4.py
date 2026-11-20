# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	set_btn.position = Vector2(600, 40)
	set_btn.size = Vector2(96, 42)''', '''	set_btn.position = Vector2(590, 96)
	set_btn.size = Vector2(88, 34)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "音量总线" not in s:
    s = s.replace("## 目录", """## 音量与统计（本轮）

- 音频拆成 Master / Music / SFX / Ambience 四条总线，`Settings` 自动加载负责创建、加载与持久化（`user://settings.cfg`）
- 桌面台账右上角「设置」打开四路音量滑杆，实时生效
- 结局档案新增本周目统计：用时（分钟）、误判率、收贿次数、逮捕次数，以及每日误判折线（`StatCurve` 自绘）

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("settings pos + readme")
