# -*- coding: utf-8 -*-
import io

# --- Portrait: rewrite drawing for a proper head/shoulders composition ---
portrait = r"F:\请出示学生证\scripts\ui\Portrait.gd"
p = '''class_name Portrait
extends Control

var seed_value := 1
var photo_mode := false
var mirrored := false
var highlight := false

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	resized.connect(queue_redraw)

func setup(p_seed: int, p_photo: bool, p_mirrored: bool = false) -> void:
	seed_value = p_seed
	photo_mode = p_photo
	mirrored = p_mirrored
	queue_redraw()

func _ellipse(center: Vector2, rx: float, ry: float, col: Color, seg: int = 28) -> void:
	var pts := PackedVector2Array()
	for i in seg:
		var a := TAU * float(i) / float(seg)
		pts.append(center + Vector2(cos(a) * rx, sin(a) * ry))
	draw_colored_polygon(pts, col)

func _draw() -> void:
	var w := size.x
	var h := size.y
	if w < 8.0 or h < 8.0:
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value

	draw_rect(Rect2(Vector2.ZERO, size), Color("#c9b48c") if photo_mode else Color("#2f3a34"))
	if photo_mode:
		var dot := Color(0.25, 0.2, 0.14, 0.09)
		var step: float = maxf(3.5, w / 42.0)
		var y: float = step * 0.5
		while y < h:
			var x: float = step * 0.5
			while x < w:
				draw_circle(Vector2(x, y), 0.9, dot)
				x += step
			y += step

	if mirrored:
		draw_set_transform(Vector2(w, 0), 0.0, Vector2(-1, 1))

	var skin := Color("#d8b48c")
	var skin_dark := Color("#bf9a74")
	var hair := Color("#241d18")
	var r := rng.randf()
	if r < 0.25:
		hair = Color("#3a2c20")
	elif r < 0.33:
		hair = Color("#6b6259")
	var uniform := Color("#2b3a2f")
	if rng.randf() < 0.3:
		uniform = Color("#33414a")

	var cx: float = w * 0.5
	var head_c := Vector2(cx, h * 0.37)
	var rx: float = w * 0.175
	var ry: float = h * 0.205
	var shoulder_top: float = h * 0.685

	var shoulders := PackedVector2Array([
		Vector2(-w * 0.02, h),
		Vector2(w * 0.14, shoulder_top + h * 0.10),
		Vector2(cx - w * 0.12, shoulder_top),
		Vector2(cx + w * 0.12, shoulder_top),
		Vector2(w * 0.86, shoulder_top + h * 0.10),
		Vector2(w * 1.02, h)
	])
	draw_colored_polygon(shoulders, uniform)
	var shirt := PackedVector2Array([
		Vector2(cx - w * 0.105, shoulder_top),
		Vector2(cx + w * 0.105, shoulder_top),
		Vector2(cx + w * 0.02, shoulder_top + h * 0.20),
		Vector2(cx - w * 0.02, shoulder_top + h * 0.20)
	])
	draw_colored_polygon(shirt, Color("#e7e2d2"))
	draw_rect(Rect2(cx - w * 0.017, shoulder_top + h * 0.005, w * 0.034, h * 0.15), Color("#8f2f22"))
	draw_rect(Rect2(cx - w * 0.055, h * 0.52, w * 0.11, h * 0.18), skin_dark)

	_ellipse(head_c, rx, ry, skin)
	_ellipse(head_c + Vector2(0, -ry * 0.42), rx * 1.04, ry * 0.62, hair)

	var eye_y: float = h * 0.355
	var eye_dx: float = w * 0.068
	draw_circle(Vector2(cx - eye_dx, eye_y), w * 0.019, Color("#201a15"))
	draw_circle(Vector2(cx + eye_dx, eye_y), w * 0.019, Color("#201a15"))
	draw_line(Vector2(cx - eye_dx - w * 0.03, eye_y - h * 0.035), Vector2(cx - eye_dx + w * 0.028, eye_y - h * 0.04), hair, maxf(1.5, w * 0.010))
	draw_line(Vector2(cx + eye_dx - w * 0.028, eye_y - h * 0.04), Vector2(cx + eye_dx + w * 0.03, eye_y - h * 0.035), hair, maxf(1.5, w * 0.010))
	draw_line(Vector2(cx, eye_y + h * 0.01), Vector2(cx - w * 0.008, eye_y + h * 0.05), skin_dark, maxf(1.5, w * 0.009))
	draw_line(Vector2(cx - w * 0.032, h * 0.455), Vector2(cx + w * 0.032, h * 0.455), Color("#8c5a4a"), maxf(1.5, w * 0.012))

	if rng.randf() < 0.3:
		draw_arc(Vector2(cx - eye_dx, eye_y), w * 0.038, 0.0, TAU, 20, Color("#3d3327"), maxf(1.5, w * 0.007))
		draw_arc(Vector2(cx + eye_dx, eye_y), w * 0.038, 0.0, TAU, 20, Color("#3d3327"), maxf(1.5, w * 0.007))
		draw_line(Vector2(cx - w * 0.018, eye_y), Vector2(cx + w * 0.018, eye_y), Color("#3d3327"), maxf(1.5, w * 0.007))

	if rng.randf() < 0.4:
		draw_circle(Vector2(cx + rx * 0.55, h * 0.41), maxf(1.0, w * 0.007), Color("#7a5344"))

	if mirrored:
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

	if photo_mode:
		draw_rect(Rect2(Vector2.ZERO, size), Color(0.45, 0.32, 0.16, 0.10))
	draw_rect(Rect2(Vector2.ZERO, size), Color("#8e7a54") if photo_mode else Color("#1d1a15"), false, maxf(1.0, w * 0.008))
'''
io.open(portrait, "w", encoding="utf-8", newline="\n").write(p)

# --- Signature: thinner strokes ---
sig = r"F:\请出示学生证\scripts\ui\Signature.gd"
s = io.open(sig, encoding="utf-8").read()
old = '\t\t\tvar wdt: float = maxf(1.0, float(s.get("w", 4.0)) * sc * 1.5)'
new = '\t\t\tvar wdt: float = clampf(float(s.get("w", 4.0)) * sc * 0.85, 1.2, 6.0)'
assert old in s
s = s.replace(old, new)
io.open(sig, "w", encoding="utf-8", newline="\n").write(s)

# --- State: no rent on day 1 ---
st = r"F:\请出示学生证\scripts\autoload\State.gd"
t = io.open(st, encoding="utf-8").read()
old2 = '''	var rent: int = int(Data.rules.get("rent", 10)) + int(Data.rules.get("utilities", 20))
	money -= rent
	if simple_mode:
		money += int(Data.rules.get("simple_bonus", 20))'''
new2 = '''	if day > 1:
		var rent: int = int(Data.rules.get("rent", 10)) + int(Data.rules.get("utilities", 20))
		money -= rent
	if simple_mode:
		money += int(Data.rules.get("simple_bonus", 20))'''
assert old2 in t
t = t.replace(old2, new2)
io.open(st, "w", encoding="utf-8", newline="\n").write(t)

# --- HUD label wording ---
desk = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(desk, encoding="utf-8").read()
old3 = '\tvar right := Ui.label("检察员 %s" % State.player_name, 16, Color(Ui.WHITE, 0.7), Ui.font_mono())'
new3 = '\tvar right := Ui.label("岗位：纪检部科员　%s" % State.player_name, 16, Color(Ui.WHITE, 0.7), Ui.font_mono())'
assert old3 in d
d = d.replace(old3, new3)
io.open(desk, "w", encoding="utf-8", newline="\n").write(d)

print("patched round 3")
