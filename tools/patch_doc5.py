# -*- coding: utf-8 -*-
import io
# CardView: emit stamped
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
if "signal stamped" not in c:
    c = c.replace("signal field_picked(field_id: String)", "signal field_picked(field_id: String)\nsignal stamped(text: String, color: Color)")
c = c.replace('''func play_stamp(text: String, color: Color) -> void:
	if _stamp == null or _stamp_frame == null:
		return''', '''func play_stamp(text: String, color: Color) -> void:
	stamped.emit(text, color)
	if _stamp == null or _stamp_frame == null:
		return''')
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
# mirror stamp to docs
if "func _mirror_stamp(" not in d:
    d = d.replace('''func _on_doc_dropped(card: Control) -> void:''', '''func _mirror_stamp(text: String, color: Color) -> void:
	for c in get_children():
		if c is DocCard:
			c.play_stamp(text, color)

func _on_doc_dropped(card: Control) -> void:''')
# connect card signal when creating card view
d = d.replace('''	var card := CardView.new()''', '''	var card := CardView.new()
	card.stamped.connect(_mirror_stamp)''')
# restrict reader to campus card
d = d.replace('''	if r.intersects(Rect2(card.global_position, card.size)):
		_use_reader()''', '''	if r.intersects(Rect2(card.global_position, card.size)):
		if card is DocCard and String(card.title) != "校园卡":
			_msg("读卡器只读校园卡。", Color("#e0a080"))
			return
		_use_reader()''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp = r"F:\请出示学生证\data\manual.json"
import json
data = json.load(io.open(mp, encoding="utf-8-sig"))
for page in data:
    if "读卡器" in page.get("body", "") and "按钮" in page.get("body", ""):
        page["body"] = page["body"].replace("买了读卡器可以把校园卡直接插机读取，不用手工比对卡号。", "买了读卡器后，把校园卡拖到台账上的读卡器上，5 秒读出结果，不用手工比对卡号。")
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))
print("mirror + restrict + text")
