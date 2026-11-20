# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
# 清理可能残留的遮罩 + 用 SceneTreeTimer(process_always) 兜底
s = s.replace('''func _boot() -> void:
	var wait := 1.0 if State.has_upgrade("fastNet") else 5.0''', '''func _boot() -> void:
	for c in get_children():
		if c is Control and c.z_index >= 60:
			c.queue_free()
	var wait := 1.0 if State.has_upgrade("fastNet") else 5.0''')
s = s.replace('''	var timer := Timer.new()
	timer.one_shot = true
	timer.wait_time = wait
	add_child(timer)
	timer.timeout.connect(func() -> void:
		layer.queue_free()
		timer.queue_free()
	)
	timer.start()''', '''	layer.process_mode = Node.PROCESS_MODE_ALWAYS
	var st := get_tree().create_timer(wait, true, false, true)
	st.timeout.connect(func() -> void:
		if is_instance_valid(layer):
			layer.queue_free()
	)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("boot hardened")
