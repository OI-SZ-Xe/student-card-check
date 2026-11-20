# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
start = s.index("func start_day() -> void:")
end = s.index("func has_upgrade(")
print(s[start:end][:1800])
