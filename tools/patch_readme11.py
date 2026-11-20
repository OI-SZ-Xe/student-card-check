# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "稳定性" not in s:
    s = s.replace("## 目录", """## 稳定性（本轮）

- 字库只保留 11–48 共 17 档；62/76/96 一律映射到 48 档（最近邻放大，仍是像素块），图集数量与显存下降
- `--shot` 截图等待从 1.9 秒延长到 4 秒，冷启动不再偶发截空
- 实测冷启动到截图 9.2 秒（含 4 秒固定等待），连续三次稳定
- 修掉一个真 bug：`State.confiscatedNormalLetters` 与 `confiscatedItems` 从未声明，没收正常介绍信会在运行时抛错；已补字段并纳入存档

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme stability")
