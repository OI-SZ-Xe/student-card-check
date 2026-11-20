extends Node

const PATH := "user://settings.cfg"
const BUSES := {"music": "Music", "sfx": "SFX", "ambience": "Ambience"}

var volumes := {"master": 0.85, "music": 0.7, "sfx": 0.9, "ambience": 0.6}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ensure_buses()
	load_cfg()
	apply()

func _ensure_buses() -> void:
	for key in BUSES.keys():
		var name: String = BUSES[key]
		if AudioServer.get_bus_index(name) == -1:
			var idx := AudioServer.bus_count
			AudioServer.add_bus(idx)
			AudioServer.set_bus_name(idx, name)
			AudioServer.set_bus_send(idx, "Master")

func bus(key: String) -> String:
	return String(BUSES.get(key, "Master"))

func set_volume(key: String, value: float) -> void:
	volumes[key] = clampf(value, 0.0, 1.0)
	apply()
	save_cfg()

func apply() -> void:
	var m := float(volumes.get("master", 0.85))
	AudioServer.set_bus_volume_db(0, linear_to_db(maxf(m, 0.0001)))
	for key in BUSES.keys():
		var idx := AudioServer.get_bus_index(String(BUSES[key]))
		if idx == -1:
			continue
		var v := float(volumes.get(key, 0.8)) * m
		AudioServer.set_bus_volume_db(idx, linear_to_db(maxf(v, 0.0001)))

func load_cfg() -> void:
	var cfg := ConfigFile.new()
	if cfg.load(PATH) != OK:
		return
	for key in volumes.keys():
		volumes[key] = float(cfg.get_value("audio", key, volumes[key]))

func save_cfg() -> void:
	var cfg := ConfigFile.new()
	for key in volumes.keys():
		cfg.set_value("audio", key, float(volumes[key]))
	cfg.save(PATH)
