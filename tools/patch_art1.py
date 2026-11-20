# -*- coding: utf-8 -*-
import io

# Portrait -> texture based
p = r"F:\请出示学生证\scripts\ui\Portrait.gd"
body = '''class_name Portrait
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
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(body)

# CRT overlay
crt = '''class_name CrtOverlay
extends CanvasLayer

func _ready() -> void:
	layer = 100
	var rect := ColorRect.new()
	rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = """
shader_type canvas_item;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear;
void fragment() {
	vec2 uv = SCREEN_UV;
	vec3 c = texture(screen_tex, uv).rgb;
	c = vec3(c.r * 0.93, c.g * 0.99, c.b * 1.03);
	float scan = 0.93 + 0.07 * sin(uv.y * 1180.0);
	c *= scan;
	float d = distance(uv, vec2(0.5, 0.5));
	c *= 1.0 - smoothstep(0.34, 0.94, d) * 0.36;
	float n = fract(sin(dot(uv * vec2(1920.0, 1080.0) + vec2(TIME * 6.0), vec2(12.9898, 78.233))) * 43758.5453);
	c += (n - 0.5) * 0.016;
	COLOR = vec4(c, 1.0);
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	add_child(rect)
'''
io.open(r"F:\请出示学生证\scripts\ui\CrtOverlay.gd", "w", encoding="utf-8", newline="\n").write(crt)

# Main: add overlay once
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "CrtOverlay" not in m:
    m = m.replace('''func _ready() -> void:
	randomize()''', '''func _ready() -> void:
	randomize()
	add_child(CrtOverlay.new())''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)

# Ui palette: colder
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()
u = u.replace('const INK := Color("#2a2622")', 'const INK := Color("#20262a")')
u = u.replace('const INK_SOFT := Color("#554e44")', 'const INK_SOFT := Color("#4c5257")')
u = u.replace('const PAPER := Color("#e8dcc0")', 'const PAPER := Color("#e4dbc2")')
u = u.replace('const PAPER_DARK := Color("#d3c39c")', 'const PAPER_DARK := Color("#cfc4a4")')
u = u.replace('const PAPER_EDGE := Color("#b8a878")', 'const PAPER_EDGE := Color("#a9a184")')
u = u.replace('const DESK := Color("#3e463c")', 'const DESK := Color("#39423f")')
u = u.replace('const DESK_DARK := Color("#22271f")', 'const DESK_DARK := Color("#1b2220")')
u = u.replace('const DESK_LIGHT := Color("#4c5548")', 'const DESK_LIGHT := Color("#454f4a")')
u = u.replace('const WHITE := Color("#f4eeda")', 'const WHITE := Color("#eef0e4")')
io.open(up, "w", encoding="utf-8", newline="\n").write(u)
print("pixel portraits + CRT + cold palette")
