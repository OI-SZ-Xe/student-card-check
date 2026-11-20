extends Node

func slot_path(slot: int) -> String:
	return "user://save_%d.json" % slot

func has(slot: int) -> bool:
	return FileAccess.file_exists(slot_path(slot))

func summary(slot: int) -> Dictionary:
	if not has(slot):
		return {}
	var txt := FileAccess.get_file_as_string(slot_path(slot))
	var parsed: Variant = JSON.parse_string(txt)
	if parsed is Dictionary:
		return parsed
	return {}

func save(slot: int) -> bool:
	var d := {
		"version": State.SAVE_VERSION,
		"day": State.day,
		"date": State.date,
		"money": State.money,
		"time_left": State.time_left,
		"suspicion": State.suspicion,
		"trust": State.trust,
		"corruption": State.corruption,
		"player_name": State.player_name,
		"player_class": State.player_class,
		"simple_mode": State.simple_mode,
		"upgrades": State.upgrades,
		"archive": State.archive,
		"correct_total": State.correct_total,
		"wrong_total": State.wrong_total,
		"quota_required": State.quota_required,
		"quota_done": State.quota_done,
		"d12_done": State.d12_done,
		"stocks": State.stocks,
		"event_done": State.event_done,
		"endings_seen": State.endings_seen,
		"confiscatedNormalLetters": State.confiscatedNormalLetters,
		"confiscatedItems": State.confiscatedItems,
		"shot_org": State.shot_org,
		"has_fake_id": State.has_fake_id,
		"has_ticket": State.has_ticket,
		"stock_news": State.stock_news,
		"saved_at": Time.get_datetime_string_from_system()
	}
	var f := FileAccess.open(slot_path(slot), FileAccess.WRITE)
	if f == null:
		return false
	f.store_string(JSON.stringify(d, "\t"))
	f.close()
	return true

func load_slot(slot: int) -> bool:
	if not has(slot):
		return false
	var txt := FileAccess.get_file_as_string(slot_path(slot))
	var parsed: Variant = JSON.parse_string(txt)
	if not parsed is Dictionary:
		return false
	var data: Dictionary = _migrate(parsed, int(parsed.get("version", 0)))
	State.day = int(data.get("day", 1))
	State.date = String(data.get("date", State.START_DATE))
	State.money = int(data.get("money", 0))
	State.time_left = float(data.get("time_left", 300.0))
	State.suspicion = int(data.get("suspicion", 0))
	State.trust = int(data.get("trust", 0))
	State.corruption = int(data.get("corruption", 0))
	State.player_name = String(data.get("player_name", "检察员"))
	State.player_class = String(data.get("player_class", "八年级（3）班"))
	State.simple_mode = bool(data.get("simple_mode", true))
	State.upgrades = data.get("upgrades", [])
	if not State.upgrades is Array:
		State.upgrades = []
	State.archive = data.get("archive", {})
	if not State.archive is Dictionary:
		State.archive = {}
	State.correct_total = int(data.get("correct_total", 0))
	State.wrong_total = int(data.get("wrong_total", 0))
	State.quota_required = int(data.get("quota_required", 0))
	State.quota_done = int(data.get("quota_done", 0))
	State.d12_done = bool(data.get("d12_done", false))
	var raw_stocks: Variant = data.get("stocks", [])
	if raw_stocks is Array and not (raw_stocks as Array).is_empty():
		State.stocks = raw_stocks
	State.stock_news = String(data.get("stock_news", ""))
	var raw_events: Variant = data.get("event_done", {})
	if raw_events is Dictionary:
		State.event_done = raw_events
	var raw_endings: Variant = data.get("endings_seen", {})
	if raw_endings is Dictionary:
		State.endings_seen = raw_endings
	State.confiscatedNormalLetters = int(data.get("confiscatedNormalLetters", 0))
	var raw_items: Variant = data.get("confiscatedItems", [])
	if raw_items is Array:
		State.confiscatedItems = raw_items
	State.shot_org = bool(data.get("shot_org", false))
	State.has_fake_id = bool(data.get("has_fake_id", false))
	State.has_ticket = bool(data.get("has_ticket", false))
	State.running = false
	State.finished = false
	return true

func _migrate(data: Dictionary, version: int) -> Dictionary:
	var out := data.duplicate(true)
	if version < 1:
		out["suspicion"] = int(out.get("suspicion", 0))
		out["upgrades"] = out.get("upgrades", [])
		out["archive"] = out.get("archive", {})
	out["version"] = State.SAVE_VERSION
	return out

func erase(slot: int) -> void:
	var path := slot_path(slot)
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
