# -*- coding: utf-8 -*-
import io

# stamp position: bottom-left of card, away from fields
c = r"F:\请出示学生证\scripts\ui\CardView.gd"
t = io.open(c, encoding="utf-8").read()
t = t.replace("\t_stamp_frame.position = Vector2(150, 210)\n\t_stamp_frame.size = Vector2(280, 84)\n\t_stamp_frame.rotation = -0.21",
              "\t_stamp_frame.position = Vector2(60, 322)\n\t_stamp_frame.size = Vector2(250, 78)\n\t_stamp_frame.rotation = -0.17")
t = t.replace('\t_stamp = Ui.label("", 38, Ui.RED, Ui.font_serif())\n\t_stamp.position = Vector2(0, 14)\n\t_stamp.size = Vector2(280, 56)',
              '\t_stamp = Ui.label("", 34, Ui.RED, Ui.font_serif())\n\t_stamp.position = Vector2(0, 12)\n\t_stamp.size = Vector2(250, 54)')
io.open(c, "w", encoding="utf-8", newline="\n").write(t)

# gate visibility
i = r"F:\请出示学生证\scripts\screens\Intro.gd"
s = io.open(i, encoding="utf-8").read()
s = s.replace("Color(0.13, 0.15, 0.12)", "Color(0.17, 0.19, 0.15)")
io.open(i, "w", encoding="utf-8", newline="\n").write(s)

# queue scan effect
d = r"F:\请出示学生证\scripts\screens\Desk.gd"
g = io.open(d, encoding="utf-8").read()
old = '''\t_update_compare_btn()
\t_refresh_hud()

func _archive_text(v: Dictionary) -> String:'''
new = '''\t_update_compare_btn()
\t_refresh_hud()
	if State.has_upgrade("queue_scan") and State.handled_today + 1 < State.total_today:
\t\tvar rng2 := RandomNumberGenerator.new()
\t\trng2.seed = State.day * 977 + (State.handled_today + 1) * 31
\t\tvar nv := VisitorFactory.make(State.day, State.date, rng2, Data.names, Data.schools, _principals, Data.doc_rules)
\t\tvar need: int = Data.required_docs(State.day, nv).size()
\t\t_queue_label.text += "\\n队列预检：下一位 %s，应交 %d 份材料" % [String(nv.get("name", "")), need]

func _archive_text(v: Dictionary) -> String:'''
assert old in g, "spawn tail missing"
g = g.replace(old, new)
io.open(d, "w", encoding="utf-8", newline="\n").write(g)
print("patched round 7")
