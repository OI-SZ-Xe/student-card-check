# -*- coding: utf-8 -*-
import io, json
up = r"F:\请出示学生证\data\manual.json"
data = json.load(io.open(up, encoding="utf-8-sig"))
for page in data:
    if page.get("type") == "forgery":
        page["body"] = page.get("body", "") + "\n\n注意：校园卡、通行证、准入证、介绍信、健康证明现在都是单独一张卡片，会叠在窗口前。买了读卡器可以把校园卡直接插机读取，不用手工比对卡号。"
io.open(up, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('"d": "点一下证件，它会被抽到窗口前。",', '"d": "点一下证件，它会被抽到窗口前；其它材料是一张张单独的卡片，可以拖开看。",')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("texts updated")
