# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
old = '''	var stock_opt := OptionButton.new()'''
new = '''	for ctrl_name in []:
		pass
	var stock_opt := OptionButton.new()'''
# style helper applied after creation
old2 = '''	var buy := Ui.button("买入", 15, Color("#12281a"), GREEN)'''
new2 = '''	for ctrl in [stock_opt, lev_opt]:
		ctrl.add_theme_color_override("font_color", GREEN)
		ctrl.add_theme_stylebox_override("normal", Ui.style(Color(0.05, 0.1, 0.07), EDGE, 1, 0, 6))
		ctrl.add_theme_stylebox_override("hover", Ui.style(Color(0.07, 0.13, 0.09), AMBER, 1, 0, 6))
		ctrl.add_theme_stylebox_override("pressed", Ui.style(Color(0.07, 0.13, 0.09), AMBER, 1, 0, 6))
	for ctrl in [price_in, shares_in]:
		ctrl.add_theme_font_override("font", Ui.font_mono())
		ctrl.add_theme_font_size_override("font_size", 16)
		ctrl.add_theme_color_override("font_color", GREEN)
		ctrl.add_theme_stylebox_override("normal", Ui.style(Color(0.05, 0.1, 0.07), EDGE, 1, 0, 6))
	var buy := Ui.button("买入", 15, Color("#12281a"), GREEN)'''
assert old2 in s
s = s.replace(old2, new2)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("exchange controls styled")
