class_name StatCurve
extends Control

var values: Array = []
var line_color := Color(0.62, 0.16, 0.12)

func _draw() -> void:
	draw_line(Vector2(0, size.y - 1), Vector2(size.x, size.y - 1), Color(0, 0, 0, 0.25), 1.0)
	if values.size() < 2:
		return
	var maxv := 1.0
	for v in values:
		maxv = maxf(maxv, float(v))
	var pts := PackedVector2Array()
	for i in values.size():
		var x := size.x * float(i) / float(values.size() - 1)
		var y := size.y - size.y * float(values[i]) / maxv
		pts.append(Vector2(x, y))
	draw_polyline(pts, line_color, 2.0)
	for p in pts:
		draw_rect(Rect2(p.x - 1.5, p.y - 1.5, 3, 3), line_color)
