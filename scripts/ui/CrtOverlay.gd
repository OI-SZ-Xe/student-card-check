class_name CrtOverlay
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
	float scan = 0.985 + 0.015 * sin(uv.y * 420.0);
	c *= scan;
	float d = distance(uv, vec2(0.5, 0.5));
	c *= 1.0 - smoothstep(0.36, 0.96, d) * 0.30;
	float n = fract(sin(dot(uv * vec2(1920.0, 1080.0) + vec2(TIME * 6.0), vec2(12.9898, 78.233))) * 43758.5453);
	c += (n - 0.5) * 0.012;
	COLOR = vec4(c, 1.0);
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	add_child(rect)
