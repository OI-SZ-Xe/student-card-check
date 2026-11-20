# -*- coding: utf-8 -*-
import io
# Desk: textured surface
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	var desk := ColorRect.new()
	desk.color = Ui.DESK
	desk.position = Vector2(0, 452)
	desk.size = Vector2(1920, 628)
	desk.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(desk)'''
new = '''	var desk := TextureRect.new()
	desk.texture = load("res://art/tex/desk.png")
	desk.stretch_mode = TextureRect.STRETCH_TILE
	desk.position = Vector2(0, 452)
	desk.size = Vector2(1920, 628)
	desk.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(desk)'''
assert old in d
d = d.replace(old, new)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

# CardView: paper fiber overlay as first child
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
old2 = '''	for c in get_children():
		c.queue_free()
	if visitor.is_empty():
		return'''
new2 = '''	for c in get_children():
		c.queue_free()
	if visitor.is_empty():
		return
	var paper_tex := TextureRect.new()
	paper_tex.texture = load("res://art/tex/paper.png")
	paper_tex.stretch_mode = TextureRect.STRETCH_TILE
	paper_tex.position = Vector2.ZERO
	paper_tex.size = Vector2(CARD_W, CARD_H)
	paper_tex.modulate = Color(1, 1, 1, 0.55)
	paper_tex.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(paper_tex)'''
assert old2 in c
c = c.replace(old2, new2)
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)
print("textures wired")
