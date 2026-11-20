# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace("\tvar can_escape := State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.money >= 150 and not State.escape_ready",
              "\tvar can_escape: bool = State.day >= 25 and State.confiscatedNormalLetters >= 1 and State.money >= 150 and not State.escape_ready")
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("typed")
