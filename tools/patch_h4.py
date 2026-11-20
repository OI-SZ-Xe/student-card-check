# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
start = d.index("\tvar queue_tex := TextureRect.new()")
end = d.index("\tvar shade := ColorRect.new()")
block = d[start:end]
d = d[:start] + d[end:]
anchor = "\tglass.add_child(shade)\n"
assert anchor in d
d = d.replace(anchor, anchor + block, 1)
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("queue above shade")
