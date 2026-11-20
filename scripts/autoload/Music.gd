extends Node

var _music: AudioStreamPlayer
var _amb: AudioStreamPlayer
var _current := ""
var _current_amb := ""

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_music = AudioStreamPlayer.new()
	_music.volume_db = -80.0
	_music.bus = "Music"
	add_child(_music)
	_amb = AudioStreamPlayer.new()
	_amb.bus = "Ambience"
	_amb.volume_db = -80.0
	add_child(_amb)

func _load(path: String) -> AudioStream:
	if not ResourceLoader.exists(path):
		return null
	var st: AudioStream = load(path)
	if st is AudioStreamWAV:
		var wav := st as AudioStreamWAV
		wav.loop_mode = AudioStreamWAV.LOOP_FORWARD
		wav.loop_begin = 0
		wav.loop_end = int(wav.data.size() / 2)
	return st

func play(track: String, fade: float = 1.2, volume: float = -16.0) -> void:
	if track == _current:
		return
	_current = track
	var st := _load("res://audio/%s.wav" % track)
	var tw := create_tween()
	if _music.playing:
		tw.tween_property(_music, "volume_db", -60.0, fade * 0.5)
	tw.tween_callback(func() -> void:
		if st == null:
			_music.stop()
			return
		_music.stream = st
		_music.play()
	)
	tw.tween_property(_music, "volume_db", volume, fade)

func ambience(track: String, fade: float = 1.5, volume: float = -26.0) -> void:
	if track == _current_amb:
		return
	_current_amb = track
	var st := null if track == "" else _load("res://audio/%s.wav" % track)
	var tw := create_tween()
	if _amb.playing:
		tw.tween_property(_amb, "volume_db", -60.0, fade * 0.5)
	tw.tween_callback(func() -> void:
		if st == null:
			_amb.stop()
			return
		_amb.stream = st
		_amb.play()
	)
	tw.tween_property(_amb, "volume_db", volume, fade)

func stop_all(fade: float = 1.0) -> void:
	_current = ""
	_current_amb = ""
	var tw := create_tween()
	tw.tween_property(_music, "volume_db", -60.0, fade)
	tw.parallel().tween_property(_amb, "volume_db", -60.0, fade)
	tw.tween_callback(func() -> void:
		_music.stop()
		_amb.stop()
	)
