# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Register.gd"
s = io.open(p, encoding="utf-8").read()
old = '''	if Meta.runs > 0:
		var ng := Ui.label("第 %d 周目：继承上周目天赋「%s」，伪造率 +15%%" % [Meta.runs + 1, _talent_name(Meta.last_talent)], 14, Ui.RED, Ui.font_serif())'''
new = '''	if Meta.runs > 0:
		var tname := _talent_name(Meta.last_talent)
		var ng_text := "第 %d 周目：伪造率 +15%%" % (Meta.runs + 1)
		if tname != "无":
			ng_text = "第 %d 周目：继承上周目天赋「%s」，伪造率 +15%%" % [Meta.runs + 1, tname]
		var ng := Ui.label(ng_text, 14, Ui.RED, Ui.font_serif())'''
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ng text")
