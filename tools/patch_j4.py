# -*- coding: utf-8 -*-
import io
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var confiscatedNormalLetters" not in s:
    s = s.replace("var endings_seen: Dictionary = {}", "var endings_seen: Dictionary = {}\nvar confiscatedNormalLetters := 0\nvar confiscatedItems: Array = []")
    s = s.replace("\tendings_seen = {}", "\tendings_seen = {}\n\tconfiscatedNormalLetters = 0\n\tconfiscatedItems = []")
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

mp = r"F:\请出示学生证\scripts\autoload\SaveManager.gd"
m = io.open(mp, encoding="utf-8").read()
if "confiscatedNormalLetters" not in m:
    m = m.replace('"endings_seen": State.endings_seen,', '"endings_seen": State.endings_seen,\n\t\t"confiscatedNormalLetters": State.confiscatedNormalLetters,\n\t\t"confiscatedItems": State.confiscatedItems,')
    m = m.replace('''	if raw_endings is Dictionary:
		State.endings_seen = raw_endings''', '''	if raw_endings is Dictionary:
		State.endings_seen = raw_endings
	State.confiscatedNormalLetters = int(data.get("confiscatedNormalLetters", 0))
	var raw_items: Variant = data.get("confiscatedItems", [])
	if raw_items is Array:
		State.confiscatedItems = raw_items''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("confiscation fields added")
