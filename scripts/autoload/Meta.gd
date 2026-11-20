extends Node

const PATH := "user://meta.json"

var runs := 0
var last_talent := ""
var endings: Dictionary = {}
var achievements: Dictionary = {}
var best_day := 0
var tutorial_done := false

func _ready() -> void:
	load_meta()

func load_meta() -> void:
	if not FileAccess.file_exists(PATH):
		return
	var raw := FileAccess.get_file_as_string(PATH)
	var parsed: Variant = JSON.parse_string(raw)
	if parsed is Dictionary:
		runs = int(parsed.get("runs", 0))
		last_talent = String(parsed.get("last_talent", ""))
		endings = parsed.get("endings", {})
		achievements = parsed.get("achievements", {})
		best_day = int(parsed.get("best_day", 0))
		tutorial_done = bool(parsed.get("tutorial_done", false))

func save_meta() -> void:
	var data := {
		"runs": runs,
		"last_talent": last_talent,
		"endings": endings,
		"achievements": achievements,
		"best_day": best_day,
		"tutorial_done": tutorial_done
	}
	var f := FileAccess.open(PATH, FileAccess.WRITE)
	if f == null:
		return
	f.store_string(JSON.stringify(data, "\t"))
	f.close()

func record_run(ending_key: String, talent: String, day: int, ach: Dictionary, seen: Dictionary) -> void:
	runs += 1
	last_talent = talent
	best_day = maxi(best_day, day)
	endings[ending_key] = true
	for k in ach.keys():
		achievements[k] = ach[k]
	for k in seen.keys():
		endings[k] = true
	save_meta()
