# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\DocCard.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''func setup(t: String, r: Array) -> void:''', '''func setup(t: String, r: Array) -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP''')
s = s.replace('''	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 14)
	paper.size = size''', '''	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 14)
	paper.mouse_filter = Control.MOUSE_FILTER_IGNORE
	paper.size = size''')
s = s.replace('''	var h := Ui.label(title, 17, Ui.INK, Ui.font_serif())''', '''	var h := Ui.label(title, 17, Ui.INK, Ui.font_serif())
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE''')
s = s.replace('''		var line := Ui.label("%s：%s" % [String(r[0]), String(r[1])], 13, Ui.INK_SOFT, Ui.font_mono())''', '''		var line := Ui.label("%s：%s" % [String(r[0]), String(r[1])], 13, Ui.INK_SOFT, Ui.font_mono())
		line.mouse_filter = Control.MOUSE_FILTER_IGNORE''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("doc drag fix")
