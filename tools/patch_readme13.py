# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "多周目" not in s:
    s = s.replace("## 目录", """## 多周目与音频（本轮）

- `Meta` 自动加载：把 `runs`、上周目天赋、已解锁结局、成就、最高天数写进 `user://meta.json`
- 第二周目起：入职登记页提示「第 N 周目：继承上周目天赋 …… 伪造率 +15%」，天赋自动预选，伪造率通过 `VisitorFactory.forgery_bonus` 生效（单测默认 0，不受影响）
- 音频：程序生成 4 段循环——`bgm_day`（32 秒小调铺底）、`bgm_tense`（24 秒脉冲）、`amb_room`（20 秒房间底噪 + 挂钟）、`amb_rain`（15 秒雨声）
- `Music` 自动加载负责交叉淡入淡出：桌面播 day，枪械事件切 tense，事件结束切回，结局切到房间底噪；雨天日环境层换成雨声

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme meta/audio")
