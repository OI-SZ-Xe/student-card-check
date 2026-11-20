# -*- coding: utf-8 -*-
import io
fp = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
f = io.open(fp, encoding="utf-8").read()
f = f.replace("State.forgery_bonus", "forgery_bonus")
if "static var forgery_bonus" not in f:
    # insert after class/extends line
    lines = f.splitlines()
    idx = 0
    for i, ln in enumerate(lines[:6]):
        if ln.startswith("extends ") or ln.startswith("class_name "):
            idx = i + 1
    lines.insert(idx, "\nstatic var forgery_bonus := 0.0")
    f = "\n".join(lines)
io.open(fp, "w", encoding="utf-8", newline="\n").write(f)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "VisitorFactory.forgery_bonus" not in d:
    d = d.replace('''	Music.play("bgm_day", 2.0)''', '''	VisitorFactory.forgery_bonus = State.forgery_bonus
	Music.play("bgm_day", 2.0)''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("factory bonus decoupled")
