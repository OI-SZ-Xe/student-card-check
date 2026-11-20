# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace("queue_tex.position = Vector2(496, 176)", "queue_tex.position = Vector2(500, 150)")
d = d.replace('queue_tex.modulate = Color(1, 1, 1, 0.9)', 'queue_tex.modulate = Color(1.25, 1.25, 1.25, 1.0)')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("queue raised")
