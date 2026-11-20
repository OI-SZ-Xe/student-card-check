# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\t_boot()\n", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("boot disabled")
