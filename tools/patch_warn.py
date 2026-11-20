# -*- coding: utf-8 -*-
import io
# 1) tutorial step rects: whole tools panel for compare step
p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('"r": Rect2(758, 538, 180, 42)', '"r": Rect2(740, 496, 410, 236)')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# 2) first error = warning only
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
st = io.open(sp, encoding="utf-8").read()
if "var warned_once" not in st:
    st = st.replace("var endless := false", "var endless := false\nvar warned_once := false")
    st = st.replace("\tendless_seen = {}", "\tendless_seen = {}")
io.open(sp, "w", encoding="utf-8", newline="\n").write(st)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''		delta = -int(Data.fee("wrong", 10))'''
new = '''		if not State.warned_once:
			State.warned_once = true
			delta = 0
			_msg("这次只警告，不扣钱。下次再判错就开罚单。", Color("#e8dfae"))
			State.wrong_today += 1
			State.wrong_total += 1
			State.handled_today += 1
			card.play_stamp("警 告", Color("#a57c2a"))
			_awaiting_next = true
			_next_btn.visible = true
			_refresh_hud()
			return
		delta = -int(Data.fee("wrong", 10))'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("warning + rect")
