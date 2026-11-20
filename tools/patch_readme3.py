# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "教育局终端" not in s:
    s = s.replace("- 仿真手册（M 键）：9 章", "- 教育局终端（7 站点）：学校信息库（校长/教导主任/总机）、电话簿、准入规定（按天生成版本并保留旧版）、协查通报、档案查询（学号/姓名，计 3 秒）、收件箱（每日简报）、成就。未买「快捷收藏夹」须先进浏览器再进站点。\n- 签字体系：五校校长 + 五位教导主任双套签名；转学介绍信校验教导主任签字。\n- 仿真手册（M 键）：9 章")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")
