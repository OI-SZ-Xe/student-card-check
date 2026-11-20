# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("- 程序化签名：自建笔画字库（王/明/李/华/张/丽/陈/芳/赵/强），按校长设定倾斜、间距、笔压与飞白，Catmull-Rom 平滑 + 变宽描边 + 落款横线。",
"""- 签名资产：系统书法字库（华文行楷 / 楷体 / 仿宋）逐字渲染，按校长参数做倾斜、错位、墨晕、飞白与落款横线，输出为 `art/signatures/*.png`；可直接替换为真人扫描件。
- 伪造签名：真迹 / 缺笔 / 浅墨 / 无钢印 / 镜像 五种变体，转学介绍信随机选用；点证件上的「查看介绍信」可看双签原件，用紫外线灯验压痕、放大镜验墨色与方向。""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")
