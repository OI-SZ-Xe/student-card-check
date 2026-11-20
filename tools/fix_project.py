# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\project.godot"
raw = io.open(p, "rb").read()
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError:
    text = raw.decode("utf-8", errors="replace")
lines = []
for ln in text.splitlines():
    if ln.startswith('"') and 'config_version' in ln:
        continue
    if ln.startswith('config/name='):
        ln = 'config/name="请出示学生证"'
    lines.append(ln)
out = []
for ln in lines:
    out.append(ln)
    if ln.startswith('config/name='):
        out.append('config/icon="res://icon_game.png"')
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("project.godot repaired")
