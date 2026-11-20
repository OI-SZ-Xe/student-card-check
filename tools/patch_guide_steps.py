# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\GuidedTutorial.gd"
s = io.open(p, encoding="utf-8").read()
# 第三步覆盖证件与印章整片区域；去掉第四步
s = s.replace('"r": Rect2(740, 748, 410, 216), "t": "第三步：盖章", "d": "核对完选一枚印章，再点证件，章才盖下去。", "p": Vector2(300, 520)},', '"r": Rect2(120, 486, 1030, 478), "t": "第三步：盖章", "d": "先点一枚印章，再点一下证件，章就盖下去了。", "p": Vector2(300, 520)},')
s = s.replace('''	{"r": Rect2(1500, 904, 176, 72), "t": "第四步：抽屉", "d": "没收的伪造证件会进这里的证物袋。", "p": Vector2(1100, 560)}''', '')
s = s.replace('''func _advance() -> void:
	if _i >= STEPS.size() - 1:
		finished.emit()
		return''', '''var _done := false

func _advance() -> void:
	if _done:
		return
	if _i >= STEPS.size() - 1:
		_done = true
		finished.emit()
		return''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guide steps fixed")
