# -*- coding: utf-8 -*-
import io

# 1) fallback font metrics
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
u = u.replace('''		fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
		_fb_font = fb''', '''		fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
		fb.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		fb.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED
		fb.hinting = TextServer.HINTING_FULL
		_fb_font = fb''')
io.open(up, "w", encoding="utf-8", newline="\n").write(u)

# 2) ending toast clear + day phase / rain
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	_paused = true
	_ending_active = true''', '''	_paused = true
	_ending_active = true
	if _msg_label != null:
		_msg_label.text = ""''')

# corridor tint by day phase
d = d.replace('''	var tint := ColorRect.new()
	tint.color = Color(0.12, 0.20, 0.17, 0.35)''', '''	var phase := int((State.day - 1) / 10)
	var tint_col := Color(0.12, 0.20, 0.17, 0.35)
	if phase == 1:
		tint_col = Color(0.20, 0.18, 0.10, 0.30)
	elif phase >= 2:
		tint_col = Color(0.08, 0.12, 0.20, 0.40)
	var tint := ColorRect.new()
	tint.color = tint_col''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("fallback + tint")
