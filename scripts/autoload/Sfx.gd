extends Node

var enabled := true
var _streams: Dictionary = {}
var _players: Array[AudioStreamPlayer] = []

func _ready() -> void:
	for i in 8:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_players.append(p)
	for key in ["click", "stamp", "paper", "error", "type", "chime"]:
		var path := "res://audio/%s.wav" % key
		if ResourceLoader.exists(path):
			_streams[key] = load(path)

func play(key: String, volume_db: float = -8.0) -> void:
	if not enabled:
		return
	var stream: AudioStream = _streams.get(key, null)
	if stream == null:
		return
	for p in _players:
		if not p.playing:
			p.stream = stream
			p.volume_db = volume_db
			p.play()
			return
