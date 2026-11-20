extends Node

var schools: Array = []
var rules: Dictionary = {}
var doc_rules: Array = []
var upgrades: Array = []
var manual: Array = []
var signatures: Dictionary = {}
var names: Dictionary = {}
var phones: Dictionary = {}

func _ready() -> void:
	reload()

func reload() -> void:
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
	roll_phones()

func _json(path: String, fallback: Variant) -> Variant:
	if not FileAccess.file_exists(path):
		push_warning("data missing: " + path)
		return fallback
	var txt := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(txt)
	if parsed == null:
		push_error("bad json: " + path)
		return fallback
	return parsed

func roll_phones() -> void:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	phones.clear()
	for s in schools:
		phones[String(s.get("name", ""))] = "0755-%06d" % rng.randi_range(100000, 999999)
	phones["教育局"] = "0755-%06d" % rng.randi_range(100000, 999999)
	phones["纪检部"] = "0755-%06d" % rng.randi_range(100000, 999999)
	phones["新人培训"] = "0755-00000000"

func school(school_name: String) -> Dictionary:
	for s in schools:
		if String(s.get("name", "")) == school_name:
			return s
	return {}

func principal_of(school_name: String) -> String:
	return String(school(school_name).get("principal", ""))

func sig(sig_id: String) -> Dictionary:
	return signatures.get(sig_id, {})

func upgrade(upgrade_id: String) -> Dictionary:
	for u in upgrades:
		if String(u.get("id", "")) == upgrade_id:
			return u
	return {}

func doc_name(key: String) -> String:
	for d in doc_rules:
		if String(d.get("key", "")) == key:
			return String(d.get("name", key))
	return key

func required_docs(day: int, visitor: Dictionary) -> Array:
	var out: Array = []
	var is_exp: bool = bool(visitor.get("experiment", false))
	var purpose := String(visitor.get("purpose", ""))
	for d in doc_rules:
		if day < int(d.get("day", 1)):
			continue
		var scope := String(d.get("scope", "all"))
		if scope == "experiment" and not is_exp:
			continue
		if scope == "external" and is_exp:
			continue
		if scope == "transfer" and purpose != "转学":
			continue
		out.append(String(d.get("key", "")))
	return out

func fee(key: String, fallback: int) -> int:
	var fees: Dictionary = rules.get("fees", {})
	return int(fees.get(key, fallback))
