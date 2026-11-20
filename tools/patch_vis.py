# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
if "func _ready() -> void:" in s:
    s = s.replace("func _ready() -> void:", "func _ready() -> void:\n\tset_anchors_preset(Control.PRESET_FULL_RECT)\n\tsize = Vector2(1920, 1080)\n\tz_index = 150\n\tvisible = true", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("terminal forced visible")
