# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
lines = io.open(p, encoding="utf-8").read().splitlines()
out = []
for ln in lines:
    if "finish" in ln or "done[0]" in ln:
        continue
    out.append(ln)
s = "\n".join(out)
s = s.replace('''	await get_tree().create_timer(wait).timeout
''', '''	await get_tree().create_timer(wait).timeout
	layer.queue_free()
''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("cleaned finish refs")
