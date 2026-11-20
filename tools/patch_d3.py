# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\t\t\tvar si := i\n\t\t\tvar sj := j", "\t\t\tvar si: int = i\n\t\t\tvar sj: int = j")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("typed loops")
