# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "点阵字库" not in s:
    s = s.replace("## 目录", """## 点阵字库（本轮）

- `tools/gen_font.py` 扫描全部脚本与 JSON，收集 1052 个字符（汉字 + ASCII + 标点）
- 用 SimSun 在 18 个字号（13/14/15/16/17/18/20/22/24/26/30/32/34/46/48/62/76/96）逐字烘焙，阈值二值化，货架算法打包成图集，输出 BMFont `.fnt` + PNG
- 运行时 `Ui._pick(font, size)` 按字号精确命中对应字库（不做缩放），未命中的字号与缺字回退到系统字体
- 效果：UI 文字与标题都是硬边像素字，不再有抗锯齿发虚

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme font")
