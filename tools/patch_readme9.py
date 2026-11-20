# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "窗口外走廊" not in s:
    s = s.replace("## 目录", """## 窗口与字库修补（本轮）

- 检查亭窗口换成像素走廊背景：卷帘门、公告栏、挂钟、海报、地脚线，玻璃后面再压一层暗色玻璃与文字底衬，人物立绘站在玻璃后
- 字库补了 11/12 两档，共 20 档；按字号懒加载（之前一次性加载全部 20 套导致启动 30 秒无响应，已修）
- 富文本改为按词智能换行，中文断行不再从词中间劈开
- 隐藏了未购置档案卡时的占位提示，窗口文字不再和背景打架

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme window/font")
