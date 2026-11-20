# -*- coding: utf-8 -*-
import io, glob, os
bad = []
for root in [r"F:\请出示学生证\scripts", r"F:\请出示学生证\data"]:
    for path in glob.glob(os.path.join(root, "**", "*.*"), recursive=True):
        if not path.endswith((".gd", ".json", ".md", ".cfg", ".godot")):
            continue
        raw = io.open(path, "rb").read()
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as e:
            text = raw.decode("utf-8", errors="replace")
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)
            bad.append((path, str(e)))
print("fixed:", len(bad))
for p, e in bad[:10]:
    print(" ", p, e)
