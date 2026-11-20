# -*- coding: utf-8 -*-
import io

def patch(path, pairs, asserts=True):
    s = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if asserts:
            assert old in s, "MISSING in %s: %r" % (path, old[:70])
        s = s.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)

patch(r"F:\请出示学生证\scripts\ui\Portrait.gd", [
    ("\t\tvar step := max(3.0, w / 44.0)\n\t\tvar y := step * 0.5",
     "\t\tvar step: float = maxf(3.0, w / 44.0)\n\t\tvar y: float = step * 0.5"),
    ("\t\t\tvar x := step * 0.5", "\t\t\tvar x: float = step * 0.5"),
    ("\tvar cx := w * 0.5", "\tvar cx: float = w * 0.5"),
    ("\tvar rx := w * 0.215", "\tvar rx: float = w * 0.215"),
    ("\tvar ry := h * 0.245", "\tvar ry: float = h * 0.245"),
    ("\tvar eye_y := h * 0.385", "\tvar eye_y: float = h * 0.385"),
    ("\tvar eye_dx := w * 0.082", "\tvar eye_dx: float = w * 0.082"),
])

patch(r"F:\请出示学生证\scripts\ui\Signature.gd", [
    ("\tvar sc := min(avail.x / max(span.x, 1.0), avail.y / max(span.y, 1.0))\n\tvar offset := Vector2(pad, pad) + (avail - span * sc) * 0.5 - min_p * sc",
     "\tvar sc: float = minf(avail.x / maxf(span.x, 1.0), avail.y / maxf(span.y, 1.0))\n\tvar offset: Vector2 = Vector2(pad, pad) + (avail - span * sc) * 0.5 - min_p * sc"),
])

patch(r"F:\请出示学生证\scripts\autoload\State.gd", [
    ('\tvar wd := Time.get_datetime_dict_from_unix_time(int(unix)).get("weekday", 0)',
     '\tvar wd: int = int(Time.get_datetime_dict_from_unix_time(int(unix)).get("weekday", 0))'),
])

old_reload = '''func reload() -> void:
	schools = _json("res://data/schools.json", [])
	rules = _json("res://data/rules.json", {})
	doc_rules = rules.get("docs", [])
	upgrades = _json("res://data/upgrades.json", [])
	manual = _json("res://data/manual.json", [])
	signatures = _json("res://data/signatures.json", {})
	names = _json("res://data/names.json", {})
	roll_phones()'''
new_reload = '''func reload() -> void:
	var raw_schools: Variant = _json("res://data/schools.json", [])
	schools = raw_schools if raw_schools is Array else []
	var raw_rules: Variant = _json("res://data/rules.json", {})
	rules = raw_rules if raw_rules is Dictionary else {}
	var raw_docs: Variant = rules.get("docs", [])
	doc_rules = raw_docs if raw_docs is Array else []
	var raw_up: Variant = _json("res://data/upgrades.json", [])
	upgrades = raw_up if raw_up is Array else []
	var raw_manual: Variant = _json("res://data/manual.json", [])
	manual = raw_manual if raw_manual is Array else []
	var raw_sig: Variant = _json("res://data/signatures.json", {})
	signatures = raw_sig if raw_sig is Dictionary else {}
	var raw_names: Variant = _json("res://data/names.json", {})
	names = raw_names if raw_names is Dictionary else {}
	roll_phones()'''
patch(r"F:\请出示学生证\scripts\autoload\Data.gd", [(old_reload, new_reload)])

patch(r"F:\请出示学生证\scripts\screens\Desk.gd", [
    ("var _paused_by_modal := false\n", ""),
])

print("patched round 2")
