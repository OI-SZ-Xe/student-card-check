# -*- coding: utf-8 -*-
import io, glob
files = [
 r"F:\请出示学生证\scripts\ui\Interrogation.gd",
 r"F:\请出示学生证\scripts\ui\Tutorial.gd",
 r"F:\请出示学生证\scripts\ui\SettingsPanel.gd",
 r"F:\请出示学生证\scripts\ui\BribeEvent.gd",
 r"F:\请出示学生证\scripts\ui\OrgEvent.gd",
 r"F:\请出示学生证\scripts\ui\LetterView.gd",
 r"F:\请出示学生证\scripts\ui\Shop.gd",
 r"F:\请出示学生证\scripts\ui\Manual.gd",
 r"F:\请出示学生证\scripts\ui\EduTerminal.gd",
 r"F:\请出示学生证\scripts\ui\SchoolRush.gd",
]
for p in files:
    try:
        s = io.open(p, encoding="utf-8").read()
    except FileNotFoundError:
        continue
    if "z_index = 100" in s:
        continue
    s = s.replace("extends Control\n", "extends Control\n\n# 模态层永远压住桌面元素\n", 1)
    # insert after class_name/extends block
    lines = s.splitlines()
    idx = 0
    for i, ln in enumerate(lines[:6]):
        if ln.startswith("extends "):
            idx = i + 1
    lines.insert(idx, "")
    lines.insert(idx + 1, "var _modal_z := 100")
    s = "\n".join(lines)
    s = s.replace("func _ready() -> void:", "func _ready() -> void:\n\tz_index = _modal_z", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("modal z-index")
