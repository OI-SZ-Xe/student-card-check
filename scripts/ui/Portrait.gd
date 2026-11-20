class_name Portrait
extends Control

var seed_value := 1
var photo_mode := false
var mirrored := false
var _tex: Texture2D = null

const COUNT := 24

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	resized.connect(queue_redraw)

func setup(p_seed: int, p_photo: bool, p_mirrored: bool = false) -> void:
	seed_value = p_seed
	photo_mode = p_photo
	mirrored = p_mirrored
	var idx := absi(seed_value) % COUNT
	var suffix := "_id" if photo_mode else ""
	var path := "res://art/portraits/p%d%s.png" % [idx, suffix]
	if ResourceLoader.exists(path):
		_tex = load(path)
	else:
		_tex = null
	queue_redraw()

func _draw() -> void:
	if _tex == null:
		draw_rect(Rect2(Vector2.ZERO, size), Color("#1d2420"))
		return
	var tw := float(_tex.get_width())
	var th := float(_tex.get_height())
	var sc: float = minf(size.x / tw, size.y / th)
	var w := tw * sc
	var h := th * sc
	var dst := Rect2((size.x - w) * 0.5, (size.y - h) * 0.5, w, h)
	if mirrored:
		draw_set_transform(Vector2(size.x, 0), 0.0, Vector2(-1, 1))
	draw_texture_rect(_tex, dst, false)
	if mirrored:
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
