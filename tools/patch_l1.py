# -*- coding: utf-8 -*-
import io
# register Meta autoload
p = r"F:\请出示学生证\project.godot"
s = io.open(p, encoding="utf-8").read()
if "Meta=" not in s:
    s = s.replace('Sfx="*res://scripts/autoload/Sfx.gd"', 'Sfx="*res://scripts/autoload/Sfx.gd"\nMeta="*res://scripts/autoload/Meta.gd"')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# State: forgery bonus from NG+
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "forgery_bonus" not in s:
    s = s.replace("var talent := \"\"", "var talent := \"\"\nvar forgery_bonus := 0.0")
    s = s.replace("\ttalent = \"\"", "\ttalent = \"\"\n\tforgery_bonus = 0.0")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# VisitorFactory: apply bonus
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
f = f.replace("if rng.randf() < 0.09:", "if rng.randf() < 0.09 * (1.0 + State.forgery_bonus):")
f = f.replace("if rng.randf() < 0.07:", "if rng.randf() < 0.07 * (1.0 + State.forgery_bonus):")
f = f.replace("if day >= 5 and rng.randf() < 0.10:", "if day >= 5 and rng.randf() < 0.10 * (1.0 + State.forgery_bonus):")
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)

# Register: NG+ hint + preselect
rp = r"F:\请出示学生证\scripts\ui\Register.gd"
r = io.open(rp, encoding="utf-8").read()
if "Meta.runs" not in r:
    r = r.replace('''	var note := Ui.rich("此表信息将打印在《纪检部入职考核表》与《录取通知》上。''', '''	if Meta.runs > 0:
		var ng := Ui.label("第 %d 周目：继承上周目天赋「%s」，伪造率 +15%%" % [Meta.runs + 1, _talent_name(Meta.last_talent)], 14, Ui.RED, Ui.font_serif())
		ng.position = Vector2(48, 336)
		ng.size = Vector2(660, 22)
		paper.add_child(ng)
		_talent = Meta.last_talent if Meta.last_talent != "" else _talent
	var note := Ui.rich("此表信息将打印在《纪检部入职考核表》与《录取通知》上。''')
    r += '''

func _talent_name(key: String) -> String:
	if key == "justice":
		return "正义感"
	if key == "insight":
		return "洞察力"
	if key == "economic":
		return "经济头脑"
	return "无"
'''
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# Main: set bonus at registration
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "forgery_bonus" not in m:
    m = m.replace("\tState.talent = talent", "\tState.talent = talent\n\tState.forgery_bonus = 0.15 if Meta.runs > 0 else 0.0")
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Desk: record meta at ending
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "Meta.record_run" not in d:
    d = d.replace("\tState.mark_ending(k)", "\tState.mark_ending(k)\n\tMeta.record_run(k, State.talent, State.day, State.achievements, State.endings_seen)")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("meta / NG+ wired")
