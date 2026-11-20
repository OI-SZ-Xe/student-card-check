# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "道具与主题" not in s:
    s = s.replace("## 目录", """## 道具与主题（本轮）

- 桌面道具实体化：工具栏换成木质托盘（六个凹槽对准六个按钮），印章台换成两枚像素印章（木质手柄 + 绿/红印泥环），电话是托盘右上角的像素话机（点开拨号），台账右下角是抽屉（点开证物袋，列出没收记录）
- 全局主题：LineEdit / OptionButton / PopupMenu / 滚动条统一成 CRT 深绿描边样式，桌面侧不再用引擎默认皮肤
- 窗口默认改为 1920×1080 原生分辨率（此前 1280 缩放导致字发虚），配合关闭抗锯齿，小字号变清晰

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme props/theme")
