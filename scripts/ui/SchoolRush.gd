class_name SchoolRush
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal finished(result: Dictionary)

class Actor extends Control:
	var kind := "hostile"
	var phase := 0.0
	var alive := true

	func _process(delta: float) -> void:
		phase += delta * 7.0
		queue_redraw()

	func _draw() -> void:
		if not alive:
			return
		var w := size.x
		var h := size.y
		var c := Color(0.62, 0.68, 0.60, 0.95)
		var swing: float = sin(phase) * w * 0.10
		draw_circle(Vector2(w * 0.5, h * 0.10), w * 0.115, c)
		draw_colored_polygon(PackedVector2Array([
			Vector2(w * 0.24, h * 0.21), Vector2(w * 0.76, h * 0.21),
			Vector2(w * 0.72, h * 0.58), Vector2(w * 0.28, h * 0.58)
		]), c)
		draw_colored_polygon(PackedVector2Array([
			Vector2(w * 0.24, h * 0.23), Vector2(w * 0.72, h * 0.23),
			Vector2(w * 0.64, h * 0.44), Vector2(w * 0.30, h * 0.44)
		]), Color(0.52, 0.57, 0.50, 0.95))
		draw_line(Vector2(w * 0.43, h * 0.58), Vector2(w * 0.40 + swing, h * 0.94), c, w * 0.13)
		draw_line(Vector2(w * 0.57, h * 0.58), Vector2(w * 0.60 - swing, h * 0.94), c, w * 0.13)
		draw_line(Vector2(w * 0.28, h * 0.26), Vector2(w * 0.14 - swing * 0.6, h * 0.50), c, w * 0.11)
		draw_line(Vector2(w * 0.72, h * 0.26), Vector2(w * 0.86 + swing * 0.6, h * 0.50), c, w * 0.11)
		if kind == "hostile":
			draw_line(Vector2(w * 0.84, h * 0.46), Vector2(w * 0.98, h * 0.20), c, w * 0.045)
		elif kind == "guard":
			draw_rect(Rect2(w * 0.30, h * 0.02, w * 0.40, h * 0.045), c)
		elif kind == "student":
			draw_rect(Rect2(w * 0.60, h * 0.24, w * 0.16, h * 0.26), c)
		elif kind == "org":
			draw_rect(Rect2(w * 0.70, h * 0.26, w * 0.10, h * 0.10), Color(0.75, 0.25, 0.20, 0.95))

	func hit_rect() -> Rect2:
		return Rect2(global_position + Vector2(size.x * 0.16, 0), Vector2(size.x * 0.70, size.y))

var scenario := "d12"
var _org_hit := false
var _actors: Array = []
var _hostiles: Array = []
var _bystanders: Array = []
var _guard: Actor = null
var _cross: Control = null
var _ammo := 3
var _shots := 0
var _hostiles_down := 0
var _bystanders_hit := 0
var _guard_hit := false
var _time_left := 7.0
var _live := false
var _resolved := false
var _mouse := Vector2(960, 540)
var _flash: ColorRect = null
var _ammo_label: Label = null
var _timer_label: Label = null
var _hint: Label = null

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	Music.play("bgm_tense", 0.4)
	_apply_scenario()
	if scenario in ["d19", "d26"]:
		var night := ColorRect.new()
		night.name = "night_overlay"
		night.color = Color(0.01, 0.02, 0.02, 0.45)
		night.position = Vector2.ZERO
		night.size = Vector2(1920, 1080)
		night.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(night)
		move_child(night, get_child_count() - 1)
	_build()
	_spawn()
	_live = true
	set_process(true)

func _build() -> void:
	var bg := ColorRect.new()
	bg.color = Color(0.04, 0.06, 0.05)
	bg.position = Vector2.ZERO
	bg.size = Vector2(1920, 1080)
	add_child(bg)

	var ground := ColorRect.new()
	ground.color = Color(0.09, 0.11, 0.09)
	ground.position = Vector2(0, 700)
	ground.size = Vector2(1920, 380)
	add_child(ground)

	for i in 9:
		var post := ColorRect.new()
		post.color = Color(0.16, 0.19, 0.16)
		post.position = Vector2(100 + i * 210, 600)
		post.size = Vector2(10, 120)
		add_child(post)
	var rail := ColorRect.new()
	rail.color = Color(0.18, 0.21, 0.18)
	rail.position = Vector2(80, 596)
	rail.size = Vector2(1780, 8)
	add_child(rail)

	var booth := ColorRect.new()
	booth.color = Color(0.13, 0.15, 0.12)
	booth.position = Vector2(880, 470)
	booth.size = Vector2(260, 240)
	add_child(booth)
	var glass := ColorRect.new()
	glass.color = Color(0.20, 0.27, 0.22)
	glass.position = Vector2(900, 496)
	glass.size = Vector2(220, 120)
	add_child(glass)

	_guard = _make_actor("guard", Vector2(1010, 690), 96, 210)
	_bystanders.append(_make_actor("student", Vector2(560, 700), 90, 200))
	_bystanders.append(_make_actor("student", Vector2(700, 712), 96, 210))
	_bystanders.append(_make_actor("student", Vector2(420, 704), 88, 196))

	_cross = Control.new()
	_cross.size = Vector2(80, 80)
	_cross.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_cross)
	_cross.draw.connect(_draw_cross)

	_flash = ColorRect.new()
	_flash.color = Color(1, 0.95, 0.7, 0.0)
	_flash.position = Vector2.ZERO
	_flash.size = Vector2(1920, 1080)
	_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_flash)

	var hud := Ui.panel(Color(0.02, 0.03, 0.02, 0.55), Color(0.3, 0.36, 0.28, 0.5), 1, 2, 12)
	hud.position = Vector2(40, 40)
	hud.size = Vector2(360, 110)
	add_child(hud)
	var cam := Ui.label("● REC　CAM-02 校门东侧", 16, Color(0.85, 0.35, 0.30), Ui.font_mono())
	cam.position = Vector2(16, 12)
	cam.size = Vector2(320, 20)
	hud.add_child(cam)
	_timer_label = Ui.label("", 15, Color(0.8, 0.85, 0.75), Ui.font_mono())
	_timer_label.position = Vector2(16, 40)
	_timer_label.size = Vector2(320, 20)
	hud.add_child(_timer_label)
	_ammo_label = Ui.label("", 15, Color(0.8, 0.85, 0.75), Ui.font_mono())
	_ammo_label.position = Vector2(16, 66)
	_ammo_label.size = Vector2(320, 20)
	hud.add_child(_ammo_label)

	var bar := ColorRect.new()
	bar.color = Color(0.03, 0.04, 0.03, 0.85)
	bar.position = Vector2(0, 1000)
	bar.size = Vector2(1920, 80)
	add_child(bar)
	_hint = Ui.label("3 发橡皮弹 · 点击射击 · 误伤学生或校警要担责", 17, Color(0.72, 0.76, 0.66), Ui.font_serif())
	_hint.position = Vector2(0, 1030)
	_hint.size = Vector2(1920, 26)
	_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(_hint)

	var stamp := Ui.label("2026-03-12　07:00:12", 15, Color(0.72, 0.78, 0.68), Ui.font_mono())
	stamp.position = Vector2(1560, 48)
	stamp.size = Vector2(320, 22)
	stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	add_child(stamp)

	var gate_sign := Ui.label("深 圳 实 验 中 学　东 门", 20, Color(0.55, 0.60, 0.50), Ui.font_serif())
	gate_sign.position = Vector2(60, 560)
	gate_sign.size = Vector2(460, 28)
	add_child(gate_sign)

	var scan := ColorRect.new()
	scan.position = Vector2.ZERO
	scan.size = Vector2(1920, 1080)
	scan.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = """
shader_type canvas_item;
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
void fragment() {
	vec2 uv = UV;
	float scan = 0.05 + 0.035 * sin(uv.y * 640.0 + TIME * 4.0);
	float n = hash(floor(uv * vec2(800.0, 450.0)) + floor(TIME * 16.0)) * 0.05;
	COLOR = vec4(vec3(0.34, 0.46, 0.36), scan + n);
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	scan.material = mat
	add_child(scan)

func _make_actor(kind: String, pos: Vector2, w: float, h: float) -> Actor:
	var a := Actor.new()
	a.kind = kind
	a.position = pos
	a.size = Vector2(w, h)
	a.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(a)
	_actors.append(a)
	return a

func _apply_scenario() -> void:
	match scenario:
		"d19":
			_time_left = 5.0
			if _hint != null:
				_hint.text = "夜间巡逻 · 手电范围外看不见人 · 3 发"
		"d26":
			_time_left = 4.5
			if _hint != null:
				_hint.text = "有人闯进检查站 · 3 发 · 想清楚再开枪"
		"d30":
			_time_left = 8.0
			if _hint != null:
				_hint.text = "校门总攻 · 3 发 · 这一枪决定你站在哪边"
		_:
			_time_left = 7.0

func _spawn() -> void:
	match scenario:
		"d19":
			var h := _make_actor("hostile", Vector2(1980, 700), 104, 220)
			_hostiles.append(h)
			_bystanders.append(_make_actor("student", Vector2(600, 706), 88, 196))
		"d26":
			var org := _make_actor("org", Vector2(1980, 690), 98, 206)
			_hostiles.append(org)
		"d30":
			for i in 3:
				var h2 := _make_actor("hostile", Vector2(1960 + i * 90, 640 + i * 26), 100, 216)
				_hostiles.append(h2)
			_bystanders.append(_make_actor("student", Vector2(620, 700), 90, 200))
		_:
			var h1 := _make_actor("hostile", Vector2(1960, 646), 100, 216)
			var h3 := _make_actor("hostile", Vector2(2080, 700), 106, 224)
			_hostiles.append(h1)
			_hostiles.append(h3)

func _draw_cross() -> void:
	var c := Vector2(_cross.size.x * 0.5, _cross.size.y * 0.5)
	_cross.draw_arc(c, 16.0, 0.0, TAU, 32, Color(0.95, 0.92, 0.7, 0.9), 2.0)
	_cross.draw_line(c + Vector2(-26, 0), c + Vector2(-8, 0), Color(0.95, 0.92, 0.7, 0.9), 2.0)
	_cross.draw_line(c + Vector2(8, 0), c + Vector2(26, 0), Color(0.95, 0.92, 0.7, 0.9), 2.0)
	_cross.draw_line(c + Vector2(0, -26), c + Vector2(0, -8), Color(0.95, 0.92, 0.7, 0.9), 2.0)
	_cross.draw_line(c + Vector2(0, 8), c + Vector2(0, 26), Color(0.95, 0.92, 0.7, 0.9), 2.0)

func _process(delta: float) -> void:
	if not _live:
		return
	var sway := Vector2(sin(Time.get_ticks_msec() * 0.002) * 3.0, cos(Time.get_ticks_msec() * 0.0027) * 2.0)
	_mouse = get_global_mouse_position() + sway
	_cross.position = _mouse - _cross.size * 0.5

	_time_left = maxf(0.0, _time_left - delta)
	_timer_label.text = "余 %0.1f 秒　冲击者 ×%d" % [_time_left, maxi(0, _hostiles.size() - _hostiles_down)]

	for a in _hostiles:
		if a == null or not is_instance_valid(a) or not a.alive:
			continue
		a.position.x -= 268.0 * delta
		if a.position.x < 1060:
			_live = false
			_resolve()
			return

	if _time_left <= 0.0 or _ammo <= 0:
		_live = false
		_resolve()

func _input(event: InputEvent) -> void:
	if not _live:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_fire()

func _fire() -> void:
	if _ammo <= 0:
		return
	_ammo -= 1
	_shots += 1
	_ammo_label.text = "橡皮弹 %d / 3　已开火 %d" % [_ammo, _shots]
	_flash.color = Color(1, 0.95, 0.7, 0.55)
	create_tween().tween_property(_flash, "color", Color(1, 0.95, 0.7, 0.0), 0.18)
	Sfx.play("stamp", -6.0)
	var shake := create_tween()
	shake.tween_property(self, "position", Vector2(-6, 4), 0.03)
	shake.tween_property(self, "position", Vector2(5, -3), 0.03)
	shake.tween_property(self, "position", Vector2.ZERO, 0.04)

	for a in _actors:
		if a == null or not is_instance_valid(a) or not a.alive:
			continue
		if a.hit_rect().has_point(_mouse):
			_hit(a)
			return

func _hit(a: Actor) -> void:
	a.alive = false
	a.queue_redraw()
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(a, "modulate", Color(1, 1, 1, 0.25), 0.5)
	tw.tween_property(a, "rotation", 1.2, 0.4)
	match a.kind:
		"hostile":
			_hostiles_down += 1
			_hint.text = "击中冲击者。"
		"student":
			_bystanders_hit += 1
			_hint.text = "击中学生。血从校服上渗出来。"
		"guard":
			_guard_hit = true
			_hint.text = "击中校警。他把对讲机摔在地上。"
		"org":
			_org_hit = true
			_hint.text = "你打中了他。袖标上的三个字，你认得。"
	if _ammo <= 0:
		_live = false
		await get_tree().create_timer(0.6).timeout
		_resolve()

func _resolve() -> void:
	Music.play("bgm_day", 1.5)
	if _resolved:
		return
	_resolved = true
	_live = false
	_cross.visible = false
	var panel := Ui.panel(Color("#e5dcc0"), Color("#7c6a44"), 3, 1, 30)
	panel.position = Vector2(560, 220)
	panel.size = Vector2(800, 640)
	add_child(panel)
	var title := Ui.label("处 置 结 果", 34, Ui.INK, Ui.font_serif())
	title.position = Vector2(40, 28)
	title.size = Vector2(500, 44)
	panel.add_child(title)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(40, 84)
	rule.size = Vector2(720, 2)
	panel.add_child(rule)
	var body := Ui.rich("", 18, Ui.INK)
	body.position = Vector2(40, 104)
	body.size = Vector2(720, 260)
	body.scroll_active = false
	body.text = "开火 %d 发　　击倒冲击者 %d 人\n误伤学生 %d 人　　击中校警 %d 人\n\n%s" % [
		_shots, _hostiles_down, _bystanders_hit, 1 if _guard_hit else 0,
		_verdict_text()
	]
	panel.add_child(body)

	var label := Ui.label("《武器使用报告》怎么写？", 18, Ui.INK, Ui.font_serif())
	label.position = Vector2(40, 376)
	label.size = Vector2(600, 26)
	panel.add_child(label)

	var opts := [
		["honest", "如实上报", "把每一发都写上，包括误伤。"],
		["hide", "隐去误伤", "只写击倒冲击者，报告会短一些。"],
		["frame", "记在同岗周睿名下", "他昨天还在收钱放人。"]
	]
	var y := 412
	for o in opts:
		var b := Ui.button("%s　—　%s" % [String(o[1]), String(o[2])], 16, Ui.INK, Ui.PAPER)
		b.position = Vector2(40, y)
		b.size = Vector2(720, 52)
		b.pressed.connect(_choose_report.bind(String(o[0])))
		panel.add_child(b)
		y += 62

func _verdict_text() -> String:
	if _hostiles_down >= 2 and _bystanders_hit == 0 and not _guard_hit:
		return "冲击者被拦下，无人误伤。安全部会记住这件事。"
	if _bystanders_hit > 0:
		return "学生倒在栏杆边。你听见有人在喊名字。"
	if _guard_hit:
		return "校警的护具凹了一块。他看你的眼神变了。"
	if _hostiles_down == 0:
		return "你一发没打中。校门守住了，但不是因为你。"
	return "场面控制住了，代价记在报告里。"

func _choose_report(kind: String) -> void:
	var money := _hostiles_down * 30
	var suspicion := _shots * 2
	if _bystanders_hit > 0:
		money -= 50 * _bystanders_hit
		suspicion += 10 * _bystanders_hit
	if _guard_hit:
		money -= 30
		suspicion += 15
	if _hostiles_down == 0 and _shots > 0:
		money += 10
	match kind:
		"honest":
			suspicion += 2
		"hide":
			suspicion += 6 if _bystanders_hit > 0 else 2
		"frame":
			suspicion = maxi(0, suspicion - 4)
	var result := {
		"scenario": scenario,
		"org_hit": _org_hit,
		"report": kind,
		"money": money,
		"suspicion": suspicion,
		"hostiles": _hostiles_down,
		"students": _bystanders_hit,
		"guard": _guard_hit,
		"shots": _shots
	}
	Sfx.play("stamp", -6.0)
	finished.emit(result)