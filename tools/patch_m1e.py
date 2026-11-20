# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Manual.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("\t\trow.custom_minimum_size = Vector2(1000, 120)", "\t\trow.custom_minimum_size = Vector2(1000, 104)")
s = s.replace("\t\tsig.position = Vector2(10, 6)\n\t\tsig.size = Vector2(300, 108)", "\t\tsig.position = Vector2(8, 4)\n\t\tsig.size = Vector2(268, 92)")
s = s.replace("\t\tnm.position = Vector2(330, 18)", "\t\tnm.position = Vector2(296, 14)")
s = s.replace("\t\tst.position = Vector2(330, 48)", "\t\tst.position = Vector2(296, 42)")
s = s.replace("\t\tink.position = Vector2(330, 92)", "\t\tink.position = Vector2(296, 80)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("signature rows tightened")
