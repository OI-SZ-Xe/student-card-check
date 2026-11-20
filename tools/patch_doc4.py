# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\DocCard.gd"
s = io.open(p, encoding="utf-8").read()
if "signal dropped" not in s:
    s = s.replace("extends Control", "extends Control\n\nsignal dropped(card: Control)\n\nvar _stamp: Label = null")
    s += '''

func play_stamp(text: String, color: Color) -> void:
	if _stamp == null:
		_stamp = Ui.label("", 24, color, Ui.font_serif())
		_stamp.position = Vector2(40, 40)
		_stamp.size = Vector2(240, 40)
		_stamp.rotation = -0.16
		add_child(_stamp)
	_stamp.text = text
	_stamp.add_theme_color_override("font_color", color)
	_stamp.modulate = Color(1, 1, 1, 0.2)
	var t := create_tween()
	t.tween_property(_stamp, "modulate", Color(1, 1, 1, 1), 0.15)
	Sfx.play("stamp", -6.0)
'''
    s = s.replace('''		else:
			_dragging = false''', '''		else:
			_dragging = false
			dropped.emit(self)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
# reader as texture prop
d = d.replace('''	var reader := Ui.button("读卡器", 13, Color(0.16, 0.20, 0.18), Color("#cfe0d0"))
	reader.position = Vector2(590, 222)
	reader.size = Vector2(88, 34)
	reader.pressed.connect(_use_reader)
	panel.add_child(reader)''', '''	var reader := TextureButton.new()
	reader.texture_normal = load("res://art/props/reader.png")
	reader.position = Vector2(590, 206)
	reader.size = Vector2(96, 64)
	reader.pressed.connect(_use_reader)
	panel.add_child(reader)
	_reader_btn = reader''')
if "var _reader_btn" not in d:
    d = d.replace("var _briefing_open := false", "var _briefing_open := false\nvar _reader_btn: Control = null")
# connect doc drops
d = d.replace('''		add_child(dc)
		i += 1''', '''		dc.dropped.connect(_on_doc_dropped)
		add_child(dc)
		i += 1''')
if "func _on_doc_dropped(" not in d:
    d += '''

func _on_doc_dropped(card: Control) -> void:
	if _reader_btn == null or not is_instance_valid(_reader_btn):
		return
	if card.name != "" and not (card is DocCard):
		return
	var r: Rect2 = _reader_btn.get_global_rect()
	if r.intersects(Rect2(card.global_position, card.size)):
		_use_reader()
		card.play_stamp("已核验", Color(0.2, 0.45, 0.26))
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("reader prop + doc stamp")
