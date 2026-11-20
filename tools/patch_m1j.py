# -*- coding: utf-8 -*-
import io
# Manual forgery: use Signature control
mp = r"F:\请出示学生证\scripts\ui\Manual.gd"
m = io.open(mp, encoding="utf-8").read()
old = '''		var path := "res://art/signatures/wang_ming%s.png" % String(item[0])
		if ResourceLoader.exists(path):
			var tr := TextureRect.new()
			tr.texture = load(path)
			tr.position = Vector2(8, 4)
			tr.size = Vector2(240, 88)
			tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			row.add_child(tr)'''
new = '''		var path := "res://art/signatures/wang_ming%s.png" % String(item[0])
		if ResourceLoader.exists(path):
			var sg := Signature.new()
			sg.setup({"img": path}, 1.0)
			sg.position = Vector2(8, 4)
			sg.size = Vector2(240, 84)
			row.add_child(sg)'''
assert old in m
m = m.replace(old, new)
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# LetterView: Signature instead of TextureRect, transparent frame
lp = r"F:\请出示学生证\scripts\ui\LetterView.gd"
l = io.open(lp, encoding="utf-8").read()
old2 = '''	var frame := Ui.panel(Color(1, 1, 1, 0.35), Color(0.4, 0.34, 0.24, 0.35), 1, 2, 6)
	frame.position = Vector2(x, y + 48)
	frame.size = Vector2(400, 150)
	parent.add_child(frame)
	var tr := TextureRect.new()
	tr.texture = tex
	tr.position = Vector2(8, 8)
	tr.size = Vector2(384, 134)
	tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	frame.add_child(tr)'''
new2 = '''	var frame := Ui.panel(Color(0, 0, 0, 0), Color(0.4, 0.34, 0.24, 0.25), 1, 2, 6)
	frame.position = Vector2(x, y + 48)
	frame.size = Vector2(400, 150)
	parent.add_child(frame)
	var sg := Signature.new()
	sg.setup({"img": path}, 1.0)
	sg.position = Vector2(8, 8)
	sg.size = Vector2(384, 134)
	frame.add_child(sg)'''
assert old2 in l
l = l.replace(old2, new2)
l = l.replace("\tif not ResourceLoader.exists(path):\n\t\treturn\n\tvar tex := load(path)\n", "\tif not ResourceLoader.exists(path):\n\t\treturn\n")
io.open(lp, "w", encoding="utf-8", newline="\n").write(l)
print("using Signature control")
