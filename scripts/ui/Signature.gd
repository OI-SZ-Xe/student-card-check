class_name Signature
extends Control

var data: Dictionary = {}
var progress := 1.0
var _tex: Texture2D = null

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func setup(p_data: Dictionary, p_progress: float = 1.0) -> void:
	data = p_data
	progress = clampf(p_progress, 0.0, 1.0)
	var path := String(data.get("img", ""))
	if path != "" and ResourceLoader.exists(path):
		_tex = load(path)
	else:
		_tex = null
	queue_redraw()

func _smooth(points: PackedVector2Array, steps: int = 10) -> PackedVector2Array:
	if points.size() < 3:
		return points
	var out := PackedVector2Array()
	for i in range(points.size() - 1):
		var p0 := points[maxi(i - 1, 0)]
		var p1 := points[i]
		var p2 := points[i + 1]
		var p3 := points[mini(i + 2, points.size() - 1)]
		for k in steps:
			var t := float(k) / float(steps)
			var t2 := t * t
			var t3 := t2 * t
			out.append(0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3))
	out.append(points[points.size() - 1])
	return out

func _draw_stroke(pts: PackedVector2Array, base_w: float, ink: Color) -> void:
	var n := pts.size()
	if n < 2:
		return
	for i in range(n - 1):
		var t0 := float(i) / float(maxi(n - 1, 1))
		var t1 := float(i + 1) / float(maxi(n - 1, 1))
		var w0: float = base_w * (0.30 + 0.82 * pow(sin(PI * t0), 0.55))
		var w1: float = base_w * (0.30 + 0.82 * pow(sin(PI * t1), 0.55))
		var a := pts[i]
		var b := pts[i + 1]
		var d := b - a
		if d.length() < 0.01:
			continue
		d = d.normalized()
		var nrm := Vector2(-d.y, d.x)
		var quad := PackedVector2Array([
			a + nrm * w0 * 0.5,
			b + nrm * w1 * 0.5,
			b - nrm * w1 * 0.5,
			a - nrm * w0 * 0.5
		])
		draw_colored_polygon(quad, ink)
	draw_circle(pts[0], base_w * 0.16, ink)
	draw_circle(pts[n - 1], base_w * 0.16, ink)

func _draw() -> void:
	if data.is_empty():
		return
	if _tex != null:
		var tw := float(_tex.get_width())
		var th := float(_tex.get_height())
		var sc: float = minf(size.x / tw, size.y / th)
		var dw := tw * sc
		var dh := th * sc
		draw_texture_rect(_tex, Rect2((size.x - dw) * 0.5, (size.y - dh) * 0.5, dw, dh), false)
		return
	var text := String(data.get("text", ""))
	if text == "":
		return
	var ink := Color(String(data.get("ink", "#1b2a4a")))
	var raw := SignatureFont.build(text, data)
	if raw.is_empty():
		return

	var min_p := Vector2(INF, INF)
	var max_p := Vector2(-INF, -INF)
	for s in raw:
		var pts: PackedVector2Array = s.get("pts", PackedVector2Array())
		for p in pts:
			min_p.x = minf(min_p.x, p.x)
			min_p.y = minf(min_p.y, p.y)
			max_p.x = maxf(max_p.x, p.x)
			max_p.y = maxf(max_p.y, p.y)
	if min_p.x == INF:
		return
	var span := max_p - min_p
	var pad := 12.0
	var avail := size - Vector2(pad * 2.0, pad * 2.0)
	if avail.x <= 4.0 or avail.y <= 4.0:
		return
	var sc: float = minf(avail.x / maxf(span.x, 1.0), avail.y / maxf(span.y, 1.0))
	var offset: Vector2 = Vector2(pad, pad) + (avail - span * sc) * 0.5 - min_p * sc

	var total := raw.size()
	var limit := int(ceil(float(total) * progress))
	for i in mini(limit, total):
		var s: Dictionary = raw[i]
		var pts := PackedVector2Array()
		var src: PackedVector2Array = s.get("pts", PackedVector2Array())
		for p in src:
			pts.append(offset + p * sc)
		var smooth := _smooth(pts, 8)
		var w: float = clampf(float(s.get("w", 4.0)) * sc, 1.1, 9.0)
		_draw_stroke(smooth, w, Color(ink.r, ink.g, ink.b, 0.16))
		_draw_stroke(smooth, w * 0.72, ink)
