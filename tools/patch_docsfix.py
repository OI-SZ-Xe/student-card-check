# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
# rebuild docs whenever a visitor is displayed
s = s.replace('''	_build_docs()''', '''''')
for anchor in ['\t_refresh_hud()\n', '\tcard.visitor = _visitor\n']:
    pass
if "_rebuild_docs_for_visitor" not in s:
    s = s.replace('''	card.visitor = _visitor''', '''	card.visitor = _visitor
	_build_docs()''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("docs rebuild on visitor")
