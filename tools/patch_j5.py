# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "var _ending_active" not in d:
    d = d.replace("var _awaiting_next := false", "var _awaiting_next := false\nvar _ending_active := false")
    d = d.replace('''	_paused = true
	var k := kind''', '''	_paused = true
	_ending_active = true
	var k := kind''')
    d = d.replace('''	if State.unlock(key, ach_name):
		var cur: String = ""''', '''	if State.unlock(key, ach_name):
		if _ending_active:
			return
		var cur: String = ""''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "结局演出" not in s:
    s = s.replace("## 目录", """## 结局演出（本轮）

- 六种结局各有专属印章：隔离审查 / 开除学籍 / 执行枪决 / 准予留任 / 准予通行 / 新秩序
- 面板含绝密抬头、档案编号、统计（余额、天数、正确审核、没收数、信任、怀疑度、腐败）、结局图鉴进度
- 结局写入 `endings_seen` 并持久化，手册「结局图鉴」页显示【已解锁】/【未解锁】
- 触发结局时不再弹出成就提示条，避免和档案纸重叠
- 配额未达标累计超过 5 天，即使没帮组织也会被判「忠诚·枪毙」

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ending polish")
