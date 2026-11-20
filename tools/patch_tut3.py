# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Tutorial.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("paper.position = Vector2(500, 200)", "paper.position = Vector2(380, 150)")
s = s.replace("paper.size = Vector2(920, 680)", "paper.size = Vector2(1160, 780)")
s = s.replace('_body.position = Vector2(40, 94)', '_body.position = Vector2(40, 100)')
s = s.replace('_body.size = Vector2(470, 340)', '_body.size = Vector2(600, 420)')
s = s.replace('_art.position = Vector2(530, 120)', '_art.position = Vector2(700, 110)')
s = s.replace('_art.size = Vector2(330, 340)', '_art.size = Vector2(420, 430)')
s = s.replace('_dots.position = Vector2(40, 520)', '_dots.position = Vector2(40, 560)')
s = s.replace('prev.position = Vector2(40, 556)', 'prev.position = Vector2(40, 600)')
s = s.replace('_next.position = Vector2(210, 556)', '_next.position = Vector2(210, 600)')
s = s.replace('skip.position = Vector2(740, 556)', 'skip.position = Vector2(980, 600)')
s = s.replace('hint.position = Vector2(40, 616)', 'hint.position = Vector2(40, 668)')
if "var bar" not in s:
    s = s.replace('''	_show_page(0)''', '''	var bar := ProgressBar.new()
	bar.position = Vector2(40, 520)
	bar.size = Vector2(600, 10)
	bar.max_value = PAGES.size()
	bar.show_percentage = false
	bar.add_theme_stylebox_override("background", Ui.style(Color(0, 0, 0, 0.12), Color(0, 0, 0, 0), 0, 0, 0))
	bar.add_theme_stylebox_override("fill", Ui.style(Color("#a57c2a"), Color(0, 0, 0, 0), 0, 0, 0))
	paper.add_child(bar)
	_bar = bar
	_show_page(0)''')
if "var _bar" not in s:
    s = s.replace("var _next: Button", "var _next: Button\nvar _bar: ProgressBar")
s = s.replace('''	_next.text = "开始执勤" if i == PAGES.size() - 1 else "下一步"''', '''	_next.text = "开始执勤" if i == PAGES.size() - 1 else "下一步"
	if _bar != null:
		_bar.value = i + 1''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("tutorial layout upgraded")
