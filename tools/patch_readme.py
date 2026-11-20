# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("- 开场动画：教育局通告 → 天际线 → 校门 → 检查站 → 纪检部入职五项（笔试/面试/政审/体检/宣誓）→ 朱印 → 标题。可跳过。",
"""- 入职登记：开场前填写姓名与班级，写入考核表、录取通知、HUD 与存档。
- 开场（约 30 秒，可跳过）：学校第 7 号通知 → 入职考核表（笔试/面试/政审/体检/宣誓 五项逐个盖章，审核人=校长王明并附手写签名）→ 录取通知（打印玩家姓名与班级、准予入职章）→《纪检部学生指导短片》片头（3-2-1 计数）+ 三张守则字卡 → 标题。全片无人物剪影，纯排版、表单、公章与胶片颗粒。""")
s = s.replace("- 程序化签名：5 位校长各一套贝塞尔笔迹，含倾斜与笔压；平滑与变宽描边。",
"- 程序化签名：自建笔画字库（王/明/李/华/张/丽/陈/芳/赵/强），按校长设定倾斜、间距、笔压与飞白，Catmull-Rom 平滑 + 变宽描边 + 落款横线。")
s = s.replace("- `--shot=<绝对路径> --shot-mode=desk|manual|shop|signatures|verdict|settle|briefing|intro`：无交互截图，用于回归验收。",
"- `--shot=<绝对路径> --shot-mode=register|desk|manual|shop|signatures|verdict|settle|briefing|intro|afterintro|portraits`：无交互截图，用于回归验收。`--shot-delay=<秒>` 控制过场截图时点。")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")
