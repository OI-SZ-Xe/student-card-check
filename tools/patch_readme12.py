# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "收尾（本轮）" not in s:
    s = s.replace("## 目录", """## 收尾（本轮）

- 黑市购买页验证通过：两件商品、价格、说明、购买按钮与「还差一封正常介绍信」提示
- 回退字体关闭抗锯齿与次像素定位、开启正常 hinting，减少生僻字与像素字混排时的宽度豁口
- 结局开始时清空消息栏，档案纸不再压着成就提示
- 走廊按时段变色：第 1–10 天清晨（冷绿）、11–20 天午后（偏暖）、21–30 天黄昏（偏蓝）；每逢 5 的倍数日下斜雨并轻微横向漂移

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme final")
