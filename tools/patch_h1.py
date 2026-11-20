# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
old = '''	var shade := ColorRect.new()'''
new = '''	var queue_tex := TextureRect.new()
	queue_tex.texture = load("res://art/props/queue.png")
	queue_tex.position = Vector2(468, 208)
	queue_tex.size = Vector2(300, 170)
	queue_tex.modulate = Color(1, 1, 1, 0.9)
	queue_tex.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glass.add_child(queue_tex)
	var bob := create_tween()
	bob.set_loops()
	bob.tween_property(queue_tex, "position:y", 211.0, 2.4).set_trans(Tween.TRANS_SINE)
	bob.tween_property(queue_tex, "position:y", 208.0, 2.4).set_trans(Tween.TRANS_SINE)

	var shade := ColorRect.new()'''
assert old in d
d = d.replace(old, new, 1)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("queue wired")
