# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Signature.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\t\t\tvar taper := 0.45 + 0.75 * math.sin(PI * clampf(t, 0.0, 1.0))",
              "\t\t\tvar taper: float = 0.45 + 0.75 * sin(PI * clampf(t, 0.0, 1.0))")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed sin")
