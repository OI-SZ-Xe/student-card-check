# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\tvar jaw_default := [0.52, 0.60, 0.68][shape]", "\tvar jaw_default: float = [0.52, 0.60, 0.68][shape]")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed inference")
