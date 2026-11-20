# -*- coding: utf-8 -*-
import io

# ---------- CardView: stamp frame ----------
p = r"F:\请出示学生证\scripts\ui\CardView.gd"
s = io.open(p, encoding="utf-8").read()
s = s.replace("var _stamp: Label = null", "var _stamp: Label = null\nvar _stamp_frame: Panel = null")
old = '''\t_stamp = Ui.label("", 44, Ui.RED, Ui.font_serif())
\t_stamp.position = Vector2(120, 170)
\t_stamp.size = Vector2(320, 70)
\t_stamp.rotation = -0.16
\t_stamp.visible = false
\t_stamp.mouse_filter = Control.MOUSE_FILTER_IGNORE
\tadd_child(_stamp)'''
new = '''\t_stamp_frame = Ui.panel(Color(0, 0, 0, 0), Color(Ui.RED, 0.9), 4, 0, 0)
\t_stamp_frame.position = Vector2(96, 168)
\t_stamp_frame.size = Vector2(368, 96)
\t_stamp_frame.rotation = -0.14
\t_stamp_frame.visible = false
\t_stamp_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
\t_stamp = Ui.label("", 46, Ui.RED, Ui.font_serif())
\t_stamp.position = Vector2(0, 16)
\t_stamp.size = Vector2(368, 64)
\t_stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t_stamp.mouse_filter = Control.MOUSE_FILTER_IGNORE
\t_stamp_frame.add_child(_stamp)
\tadd_child(_stamp_frame)'''
assert old in s, "stamp block missing"
s = s.replace(old, new)
old2 = '''func play_stamp(text: String, color: Color) -> void:
\tif _stamp == null:
\t\treturn
\t_stamp.text = text
\t_stamp.add_theme_color_override("font_color", color)
\t_stamp.visible = true
\t_stamp.scale = Vector2(2.4, 2.4)
\t_stamp.modulate = Color(1, 1, 1, 0.2)
\tvar t := create_tween()
\tt.set_parallel(true)
\tt.tween_property(_stamp, "scale", Vector2.ONE, 0.20).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
\tt.tween_property(_stamp, "modulate", Color(1, 1, 1, 1), 0.12)
\tSfx.play("stamp", -4.0)'''
new2 = '''func play_stamp(text: String, color: Color) -> void:
\tif _stamp == null or _stamp_frame == null:
\t\treturn
\t_stamp.text = text
\t_stamp.add_theme_color_override("font_color", color)
\t_stamp_frame.add_theme_stylebox_override("panel", Ui.style(Color(0, 0, 0, 0), Color(color, 0.9), 4, 0, 0))
\t_stamp_frame.visible = true
\t_stamp_frame.pivot_offset = _stamp_frame.size * 0.5
\t_stamp_frame.scale = Vector2(2.4, 2.4)
\t_stamp_frame.modulate = Color(1, 1, 1, 0.25)
\tvar t := create_tween()
\tt.set_parallel(true)
\tt.tween_property(_stamp_frame, "scale", Vector2.ONE, 0.20).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
\tt.tween_property(_stamp_frame, "modulate", Color(1, 1, 1, 1), 0.12)
\tSfx.play("stamp", -4.0)'''
assert old2 in s, "play_stamp missing"
s = s.replace(old2, new2)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# ---------- Signature: smoothing, taper, slant ----------
sig = r"F:\请出示学生证\scripts\ui\Signature.gd"
body = '''class_name Signature
extends Control

var strokes: Array = []
var ink := Color("#1b2a4a")
var progress := 1.0
var slant_deg := 0.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func setup(data: Dictionary, p_progress: float = 1.0) -> void:
	strokes = data.get("strokes", [])
	ink = Color(String(data.get("ink", "#1b2a4a")))
	slant_deg = float(data.get("slant", 0.0))
	progress = clampf(p_progress, 0.0, 1.0)
	queue_redraw()

func _catmull(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)

func _smooth(points: PackedVector2Array, steps: int = 8) -> PackedVector2Array:
	if points.size() < 3:
		return points
	var out := PackedVector2Array()
	for i in range(points.size() - 1):
		var p0 := points[maxi(i - 1, 0)]
		var p1 := points[i]
		var p2 := points[i + 1]
		var p3 := points[mini(i + 2, points.size() - 1)]
		for k in steps:
			out.append(_catmull(p0, p1, p2, p3, float(k) / float(steps)))
	out.append(points[points.size() - 1])
	return out

func _draw() -> void:
	if strokes.is_empty():
		return
	var min_p := Vector2(INF, INF)
	var max_p := Vector2(-INF, -INF)
	for st in strokes:
		for pt in st.get("pts", []):
			var v := Vector2(float(pt[0]), float(pt[1]))
			min_p.x = minf(min_p.x, v.x)
			min_p.y = minf(min_p.y, v.y)
			max_p.x = maxf(max_p.x, v.x)
			max_p.y = maxf(max_p.y, v.y)
	if min_p.x == INF:
		return
	var span := max_p - min_p
	var pad := 10.0
	var avail := size - Vector2(pad * 2.0, pad * 2.0)
	var sc: float = minf(avail.x / maxf(span.x, 1.0), avail.y / maxf(span.y, 1.0))
	var offset: Vector2 = Vector2(pad, pad) + (avail - span * sc) * 0.5 - min_p * sc

	var center := size * 0.5
	draw_set_transform(center, deg_to_rad(slant_deg), Vector2.ONE)

	var total := strokes.size()
	var limit := int(ceil(total * progress))
	for i in mini(limit, total):
		var st: Dictionary = strokes[i]
		var raw := PackedVector2Array()
		for pt in st.get("pts", []):
			raw.append(offset + Vector2(float(pt[0]), float(pt[1])) * sc - center)
		var pts := _smooth(raw, 8)
		if pts.size() < 2:
			continue
		var base_w: float = clampf(float(st.get("w", 4.0)) * sc * 0.8, 1.0, 5.5)
		for k in range(pts.size() - 1):
			var t := float(k) / float(maxi(pts.size() - 2, 1))
			var taper := 0.45 + 0.75 * math.sin(PI * clampf(t, 0.0, 1.0))
			draw_line(pts[k], pts[k + 1], ink, maxf(0.6, base_w * taper), true)

	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
'''
io.open(sig, "w", encoding="utf-8", newline="\n").write(body)

# ---------- signatures.json: add slant ----------
import json
jp = r"F:\请出示学生证\data\signatures.json"
data = json.load(io.open(jp, encoding="utf-8"))
slants = {"wang_ming": -5, "li_hua": 8, "zhang_li": 0, "chen_fang": 2, "zhao_qiang": -3}
for k, v in slants.items():
    if k in data:
        data[k]["slant"] = v
io.open(jp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

# ---------- Briefing layout ----------
b = r"F:\请出示学生证\scripts\ui\Briefing.gd"
t = io.open(b, encoding="utf-8").read()
t = t.replace('\tpaper.position = Vector2(560, 170)\n\tpaper.size = Vector2(800, 720)',
              '\tpaper.position = Vector2(560, 200)\n\tpaper.size = Vector2(800, 640)')
t = t.replace('\tbody.position = Vector2(48, 150)\n\tbody.size = Vector2(704, 300)',
              '\tbody.position = Vector2(48, 150)\n\tbody.size = Vector2(704, 210)')
t = t.replace('\tnews.position = Vector2(48, 470)\n\tnews.size = Vector2(704, 110)',
              '\tnews.position = Vector2(48, 380)\n\tnews.size = Vector2(704, 100)')
t = t.replace('\tmoney.position = Vector2(48, 596)', '\tmoney.position = Vector2(48, 500)')
t = t.replace('\tstart.position = Vector2(268, 636)\n\tstart.size = Vector2(264, 52)',
              '\tstart.position = Vector2(268, 546)\n\tstart.size = Vector2(264, 52)')
t = t.replace('\tseal.position = Vector2(600, 620)', '\tseal.position = Vector2(596, 534)')
old_money = '''\tvar money := Ui.label("上月结余 %d 元　·　今日房租水电已扣　·　简单模式补贴已入账" % State.money, 13, Ui.INK_SOFT, Ui.font_mono())'''
new_money = '''\tvar rent_note := "首日入住临时宿舍，免扣房租水电" if day <= 1 else "房租水电已扣"
\tvar money := Ui.label("当前余额 %d 元　·　%s　·　简单模式补贴已入账" % [State.money, rent_note], 13, Ui.INK_SOFT, Ui.font_mono())'''
assert old_money in t
t = t.replace(old_money, new_money)
io.open(b, "w", encoding="utf-8", newline="\n").write(t)

print("patched round 5")
