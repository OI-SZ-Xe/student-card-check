# -*- coding: utf-8 -*-
import io
# queue native 300x170
qp = r"F:\请出示学生证\tools\gen_queue.py"
q = io.open(qp, encoding="utf-8").read()
q = q.replace("img = img.resize((W * 2, H * 2), Image.NEAREST)\n", "")
io.open(qp, "w", encoding="utf-8", newline="\n").write(q)

# desk: clip + position + softer shade
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	glass.mouse_filter = Control.MOUSE_FILTER_IGNORE
	win.add_child(glass)''', '''	glass.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.clip_contents = true
	win.add_child(glass)''')
d = d.replace('''	queue_tex.position = Vector2(468, 208)
	queue_tex.size = Vector2(300, 170)''', '''	queue_tex.position = Vector2(496, 176)
	queue_tex.size = Vector2(260, 148)''')
d = d.replace('''	shade.color = Color(0.02, 0.04, 0.03, 0.55)''', '''	shade.color = Color(0.02, 0.04, 0.03, 0.45)''')
# remove debug prints
d = d.replace('\tprint("DBG desk ready start")\n', '')
d = d.replace('\tprint("DBG desk build done")\n', '')
d = d.replace('\tprint("DBG day done")\n', '')
d = d.replace('\tprint("DBG hud done")\n', '')
d = d.replace('\tprint("DBG pre shift")\n', '')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("queue fixed, debug removed")
