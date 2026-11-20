# -*- coding: utf-8 -*-
import io
# 1) factory: sometimes a doc is not brought
p = r"F:\请出示学生证\scripts\systems\VisitorFactory.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''	v["docs"] = docs''', '''	if rng.randf() < 0.12:
		var pool: Array = []
		for k2 in docs.keys():
			if k2 != "student_card":
				pool.append(k2)
		if pool.size() > 0:
			var miss := String(pool[rng.randi() % pool.size()])
			docs[miss]["missing"] = true
			docs[miss]["can_supply"] = rng.randf() < 0.6
	v["docs"] = docs''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# 2) rule engine: missing doc = reject reason
rp = r"F:\请出示学生证\scripts\systems\RuleEngine.gd"
r = io.open(rp, encoding="utf-8").read()
r = r.replace('''	for key in required:
		var k := String(key)''', '''	for key in required:
		var k := String(key)
		var dv: Dictionary = v.get("docs", {})
		if dv.has(k) and bool(dv[k].get("missing", false)):
			reasons.append("未提交%s" % String(doc_names.get(k, k)))
			fields.append(k)
			continue''')
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# 3) interrogation: ask to supply
ip = r"F:\请出示学生证\scripts\ui\Interrogation.gd"
it = io.open(ip, encoding="utf-8").read()
it = it.replace("signal spend(seconds: float)", "signal spend(seconds: float)\nsignal supplied")
if "要求补交" not in it:
    it = it.replace('''	var guide := Ui.rich("核实手段要自己动手''', '''	var docs: Dictionary = visitor.get("docs", {})
	for k in docs.keys():
		if bool(docs[k].get("missing", false)):
			var sup := Ui.button("要求补交材料", 16, Color(0.24, 0.28, 0.18), Ui.WHITE)
			sup.position = Vector2(528, 512)
			sup.size = Vector2(230, 48)
			var key := String(k)
			sup.pressed.connect(func() -> void:
				spend.emit(5.0)
				if bool(docs[key].get("can_supply", false)):
					docs[key]["missing"] = false
					_log.text += "\\n他翻了翻书包，把材料补上了。"
					supplied.emit()
				else:
					_log.text += "\\n他拿不出来：「真的没带，我明天再来。」"
			)
			paper.add_child(sup)

	var guide := Ui.rich("核实手段要自己动手''')
io.open(ip, "w", encoding="utf-8", newline="\n").write(it)

# 4) desk: rebuild docs on supplied; also interrogation button
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('''	dlg.spend.connect(func(sec: float) -> void:''', '''	dlg.supplied.connect(func() -> void:
		_build_docs()
		card.set_visitor(_visitor, State.date)
	)
	dlg.spend.connect(func(sec: float) -> void:''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("missing docs + supply")
