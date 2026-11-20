# -*- coding: utf-8 -*-
import io, json
up = r"F:\请出示学生证\data\upgrades.json"
data = json.load(io.open(up, encoding="utf-8-sig"))
if not any(u.get("key") == "reader" for u in data):
    data.append({"key": "reader", "name": "读卡器", "desc": "把校园卡插进读卡器，5 秒读出有效/无效/挂失，不用手工核对。", "price": 60})
io.open(up, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func _use_reader(" not in d:
    d = d.replace('''	var phone_prop := TextureButton.new()''', '''	var reader := Ui.button("读卡器", 13, Color(0.16, 0.20, 0.18), Color("#cfe0d0"))
	reader.position = Vector2(590, 222)
	reader.size = Vector2(88, 34)
	reader.pressed.connect(_use_reader)
	panel.add_child(reader)
	var phone_prop := TextureButton.new()''')
    d += '''

func _use_reader() -> void:
	if not State.has_upgrade("reader"):
		_msg("还没买读卡器。办公用品商店有售。", Color("#e0a080"))
		return
	if _visitor.is_empty() or _awaiting_next:
		return
	State.time_left = maxf(0.0, State.time_left - 5.0)
	var cc: Dictionary = _visitor.get("campus_card", {})
	if cc.is_empty():
		_msg("读卡器：没有检测到校园卡。", Color("#cfe0f0"))
	else:
		var ok := bool(cc.get("valid", true))
		_msg("读卡器：校园卡%s。" % ("有效" if ok else "无效 / 已挂失"), Color("#cfe0f0") if ok else Color("#e0a080"))
	_refresh_hud()
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("reader added")
