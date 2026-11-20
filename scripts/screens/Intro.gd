class_name Intro
extends Control

signal finished

var _skip := false
var _ended := false
var _scene: Control = null
var _overlay: ColorRect = null
var _skip_btn: Button = null
var _weave_time := 0.0
var _film_mode := false
var _rng := RandomNumberGenerator.new()
var player_name := "检察员"
var player_class := "八年级（3）班"

class Leader extends Control:
	var number := 3
	var ink := Color("#e6e0c8")

	func set_number(n: int) -> void:
		number = n
		queue_redraw()

	func _draw() -> void:
		var c := size * 0.5
		var r: float = minf(size.x, size.y) * 0.36
		draw_arc(c, r, 0.0, TAU, 96, ink, 3.0, true)
		draw_arc(c, r * 0.62, 0.0, TAU, 64, Color(ink, 0.55), 2.0, true)
		draw_line(Vector2(c.x - r * 1.25, c.y), Vector2(c.x + r * 1.25, c.y), Color(ink, 0.7), 2.0)
		draw_line(Vector2(c.x, c.y - r * 1.25), Vector2(c.x, c.y + r * 1.25), Color(ink, 0.7), 2.0)
		var font := Ui.font_mono()
		draw_string(font, Vector2(c.x - 90.0, c.y + 70.0), str(number), HORIZONTAL_ALIGNMENT_CENTER, 180.0, 150, ink)

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_rng.randomize()
	_build()
	_run()

func _build() -> void:
	var bg := ColorRect.new()
	bg.color = Color("#070806")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)

	_scene = Control.new()
	_scene.size = Vector2(1920, 1080)
	add_child(_scene)

	var frame := Control.new()
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(frame)
	var border := ReferenceRect.new()
	border.border_color = Color(0.85, 0.83, 0.72, 0.10)
	border.border_width = 2.0
	border.position = Vector2(48, 48)
	border.size = Vector2(1824, 984)
	border.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_child(border)

	_overlay = ColorRect.new()
	_overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = """
shader_type canvas_item;
uniform float grain : hint_range(0.0, 0.3) = 0.065;
uniform float vig : hint_range(0.0, 1.0) = 0.52;
uniform float scratch : hint_range(0.0, 1.0) = 0.55;
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
void fragment() {
	vec2 uv = UV;
	float n = hash(floor(uv * vec2(960.0, 540.0)) + vec2(floor(TIME * 24.0)));
	float d = distance(uv, vec2(0.5, 0.5));
	float v = smoothstep(0.30, 0.86, d) * vig;
	float sx = floor(uv.x * 720.0);
	float s = step(0.996, hash(vec2(sx, floor(TIME * 9.0)))) * step(0.55, hash(vec2(sx, 7.0)));
	COLOR = vec4(vec3(1.0), n * grain + v * 0.55 + s * 0.05 * scratch);
}
"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	_overlay.material = mat
	add_child(_overlay)

	_skip_btn = Ui.button("跳过 (Esc)", 15, Color(0.06, 0.07, 0.06), Color(0.6, 0.62, 0.54))
	_skip_btn.position = Vector2(1730, 22)
	_skip_btn.size = Vector2(150, 38)
	_skip_btn.pressed.connect(_do_skip)
	add_child(_skip_btn)

func _do_skip() -> void:
	_skip = true

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		_do_skip()

func _exit_tree() -> void:
	_ended = true

func _process(delta: float) -> void:
	if not _film_mode:
		return
	_weave_time += delta
	if _weave_time > 0.18:
		_weave_time = 0.0
		_scene.position = Vector2(_rng.randf_range(-1.6, 1.6), _rng.randf_range(-1.4, 1.4))

func _wait(t: float) -> void:
	var elapsed := 0.0
	while elapsed < t:
		if _skip or _ended:
			return
		await get_tree().process_frame
		elapsed += get_process_delta_time()

func _clear() -> void:
	for c in _scene.get_children():
		c.queue_free()
	_scene.position = Vector2.ZERO

func _black() -> void:
	var r := ColorRect.new()
	r.color = Color("#070806")
	r.position = Vector2.ZERO
	r.size = Vector2(1920, 1080)
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_scene.add_child(r)

func _paper(rect: Rect2, tint: Color = Color("#e9dfc2")) -> Panel:
	var p := Ui.panel(tint, Color("#8d7c52"), 2, 1, 0)
	p.position = rect.position
	p.size = rect.size
	p.rotation = -0.004
	_scene.add_child(p)
	return p

func _type(label: Label, text: String, cps: float = 0.03) -> void:
	if _skip or _ended:
		label.text = text
		return
	label.text = ""
	for i in text.length():
		if _skip or _ended:
			label.text = text
			return
		label.text = text.substr(0, i + 1)
		if i % 3 == 0:
			Sfx.play("type", -24.0)
		await _wait(cps)
	await get_tree().create_timer(0.0001).timeout

func _run() -> void:
	var shots: Array = [
		_shot_notice_header,
		_shot_notice_body,
		_shot_assessment,
		_shot_admission,
		_shot_film_leader,
		_shot_guidance,
		_shot_title
	]
	for shot in shots:
		if _skip or _ended:
			break
		await shot.call()
	if not _ended:
		finished.emit()

func _stamp_badge(text: String, color: Color) -> Control:
	var holder := Control.new()
	holder.custom_minimum_size = Vector2(140, 44)
	var box := Ui.panel(Color(0, 0, 0, 0), Color(color, 0.85), 2, 1, 0)
	box.size = Vector2(126, 42)
	box.rotation = -0.05
	holder.add_child(box)
	var l := Ui.label(text, 17, color, Ui.font_serif())
	l.position = Vector2(0, 8)
	l.size = Vector2(126, 26)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(l)
	return holder

func _film_frame() -> void:
	var col := Color(0.86, 0.84, 0.72, 0.22)
	for yy in [74.0, 1002.0]:
		var bar := ColorRect.new()
		bar.color = col
		bar.position = Vector2(100, yy)
		bar.size = Vector2(1720, 3)
		bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_scene.add_child(bar)
	for i in 13:
		var y := 96.0 + float(i) * 70.0
		for xx in [62.0, 1838.0]:
			var hole := ColorRect.new()
			hole.color = Color(0.84, 0.82, 0.70, 0.14)
			hole.position = Vector2(xx, y)
			hole.size = Vector2(14, 30)
			hole.mouse_filter = Control.MOUSE_FILTER_IGNORE
			_scene.add_child(hole)

func _shot_notice_header() -> void:
	_clear()
	_black()
	await _wait(0.7)
	var top := Ui.label("深 圳 实 验 中 学", 34, Color("#efe8cf"), Ui.font_serif())
	top.position = Vector2(0, 380)
	top.size = Vector2(1920, 48)
	top.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	top.modulate = Color(1, 1, 1, 0)
	_scene.add_child(top)
	create_tween().tween_property(top, "modulate", Color(1, 1, 1, 1), 0.5)
	await _wait(0.8)
	var sub := Ui.label("2026 年第 7 号通知", 22, Color(0.62, 0.62, 0.52), Ui.font_mono())
	sub.position = Vector2(0, 448)
	sub.size = Vector2(1920, 32)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.modulate = Color(1, 1, 1, 0)
	_scene.add_child(sub)
	await _type(sub, "2026 年第 7 号通知", 0.03)
	create_tween().tween_property(sub, "modulate", Color(1, 1, 1, 1), 0.3)
	await _wait(1.6)

func _shot_notice_body() -> void:
	_clear()
	_black()
	var paper := _paper(Rect2(460, 150, 1000, 780))
	var head := Ui.label("关于招募学生会纪检部检查员的通知", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(60, 52)
	head.size = Vector2(880, 40)
	paper.add_child(head)
	var meta := Ui.label("各年级组、各班：", 15, Ui.INK_SOFT, Ui.font_mono())
	meta.position = Vector2(60, 104)
	meta.size = Vector2(880, 22)
	paper.add_child(meta)
	var rule := ColorRect.new()
	rule.color = Ui.PAPER_EDGE
	rule.position = Vector2(60, 134)
	rule.size = Vector2(880, 2)
	paper.add_child(rule)

	var body := Ui.rich("", 19, Ui.INK)
	body.position = Vector2(60, 168)
	body.size = Vector2(880, 300)
	body.scroll_active = false
	paper.add_child(body)
	var lines := [
		"为加强校门通行管理，现面向八年级招募学生会纪检部检查员 1 名。",
		"报名者须通过笔试、面试、政审、体检、宣誓五项考核。",
		"考核合格者，分配至校门检查站执勤，负责核验进出人员证件。"
	]
	for line in lines:
		if _skip or _ended: return
		body.text += String(line) + "\n"
		Sfx.play("type", -22.0)
		await _wait(0.6)
	if _skip or _ended: return
	var foot := Ui.label("深圳实验中学 学生会\n2026 年 2 月 24 日", 16, Ui.INK, Ui.font_serif())
	foot.position = Vector2(560, 620)
	foot.size = Vector2(380, 60)
	foot.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	paper.add_child(foot)
	var seal := Ui.label("学生\n会印", 22, Color(0.72, 0.16, 0.12, 0.85), Ui.font_serif())
	seal.position = Vector2(770, 610)
	seal.size = Vector2(110, 90)
	seal.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	seal.rotation = -0.18
	paper.add_child(seal)
	Sfx.play("stamp", -12.0)
	await _wait(2.4)

func _shot_assessment() -> void:
	_clear()
	_black()
	var paper := _paper(Rect2(400, 150, 1120, 760))
	var head := Ui.label("纪检部入职考核表", 30, Ui.INK, Ui.font_serif())
	head.position = Vector2(64, 42)
	head.size = Vector2(600, 40)
	paper.add_child(head)
	var no := Ui.label("编号 JD-2026-047　　姓名：%s　　班级：%s" % [player_name, player_class], 15, Ui.INK, Ui.font_mono())
	no.position = Vector2(64, 88)
	no.size = Vector2(900, 22)
	paper.add_child(no)
	var rule := ColorRect.new()
	rule.color = Ui.PAPER_EDGE
	rule.position = Vector2(64, 118)
	rule.size = Vector2(992, 2)
	paper.add_child(rule)

	var rows := VBoxContainer.new()
	rows.position = Vector2(64, 142)
	rows.size = Vector2(992, 520)
	rows.add_theme_constant_override("separation", 14)
	paper.add_child(rows)

	var items := [
		["01", "笔试", "教育法规 · 校园安全条例 · 纪检部工作守则"],
		["02", "面试", "校园安全部主持 · 临场判断与政治觉悟"],
		["03", "政审", "本人及直系亲属无违纪记录"],
		["04", "体检", "色觉正常 · 可长时间注视证件细节"],
		["05", "宣誓", "面向校门宣读《检查员守则》全文"]
	]
	for item in items:
		if _skip or _ended: return
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 18)
		var idx := Ui.label(String(item[0]), 18, Color(0.55, 0.48, 0.36), Ui.font_mono())
		idx.custom_minimum_size = Vector2(44, 0)
		var nm := Ui.label(String(item[1]), 24, Ui.INK, Ui.font_serif())
		nm.custom_minimum_size = Vector2(96, 0)
		var desc := Ui.label(String(item[2]), 15, Ui.INK_SOFT, Ui.font_serif())
		desc.custom_minimum_size = Vector2(560, 0)
		var status := Control.new()
		status.custom_minimum_size = Vector2(140, 44)
		var wait_label := Ui.label("待　核", 17, Ui.INK_SOFT, Ui.font_mono())
		wait_label.position = Vector2(4, 10)
		status.add_child(wait_label)
		row.add_child(idx)
		row.add_child(nm)
		row.add_child(desc)
		row.add_child(status)
		rows.add_child(row)
		await _wait(0.5)
		if _ended: return
		wait_label.text = ""
		var badge := _stamp_badge("合 格", Color(0.66, 0.17, 0.13))
		badge.scale = Vector2(1.7, 1.7)
		badge.modulate = Color(1, 1, 1, 0)
		status.add_child(badge)
		var bt := create_tween()
		bt.set_parallel(true)
		bt.tween_property(badge, "scale", Vector2.ONE, 0.16)
		bt.tween_property(badge, "modulate", Color(1, 1, 1, 1), 0.10)
		Sfx.play("stamp", -14.0)
		await _wait(0.5)

	var foot := Ui.label("审查结论：准予录用　　审核人：校长　王明", 17, Ui.INK, Ui.font_serif())
	foot.position = Vector2(64, 566)
	foot.size = Vector2(700, 26)
	paper.add_child(foot)
	var sig := Signature.new()
	sig.setup(Data.sig("wang_ming"), 1.0)
	sig.position = Vector2(690, 540)
	sig.size = Vector2(300, 110)
	paper.add_child(sig)
	var sig_line := Ui.label("（校长签字）", 12, Ui.INK_SOFT, Ui.font_mono())
	sig_line.position = Vector2(710, 648)
	sig_line.size = Vector2(240, 18)
	paper.add_child(sig_line)
	await _wait(2.4)

func _shot_admission() -> void:
	_clear()
	_black()
	await _wait(0.25)
	var card := _paper(Rect2(520, 260, 880, 580), Color("#ece2c6"))
	var small := Ui.label("深 圳 实 验 中 学", 18, Color(0.4, 0.36, 0.28), Ui.font_serif())
	small.position = Vector2(56, 44)
	small.size = Vector2(500, 24)
	card.add_child(small)
	var title := Ui.label("录 取 通 知", 46, Ui.INK, Ui.font_serif())
	title.position = Vector2(56, 82)
	title.size = Vector2(700, 60)
	card.add_child(title)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(56, 152)
	rule.size = Vector2(768, 3)
	card.add_child(rule)
	var body := Ui.rich("", 19, Ui.INK)
	body.position = Vector2(56, 186)
	body.size = Vector2(768, 250)
	body.scroll_active = false
	body.text = "兹录取　[b]%s[/b]（%s）为学生会纪检部检查员。\n\n请于 2026 年 3 月 1 日 07:00 到校门检查站报到，\n携带本通知与学生证，着校服，不得迟到。" % [player_name, player_class]
	card.add_child(body)
	var foot := Ui.label("校长　王明", 16, Ui.INK, Ui.font_serif())
	foot.position = Vector2(520, 470)
	foot.size = Vector2(220, 22)
	foot.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	card.add_child(foot)
	var sig := Signature.new()
	sig.setup(Data.sig("wang_ming"), 1.0)
	sig.position = Vector2(430, 366)
	sig.size = Vector2(300, 110)
	card.add_child(sig)

	var stamp := Ui.label("准 予 入 职", 62, Color(0.72, 0.16, 0.12, 0.9), Ui.font_serif())
	stamp.position = Vector2(64, 360)
	stamp.size = Vector2(470, 96)
	stamp.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stamp.rotation = -0.13
	stamp.scale = Vector2(2.8, 2.8)
	stamp.pivot_offset = stamp.size * 0.5
	stamp.modulate = Color(1, 1, 1, 0)
	card.add_child(stamp)
	await _wait(0.5)
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(stamp, "scale", Vector2.ONE, 0.24).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(stamp, "modulate", Color(1, 1, 1, 1), 0.14)
	Sfx.play("stamp", -3.0)
	await _wait(0.32)
	var shake := create_tween()
	shake.tween_property(_scene, "position", Vector2(10, -6), 0.05)
	shake.tween_property(_scene, "position", Vector2(-8, 4), 0.05)
	shake.tween_property(_scene, "position", Vector2.ZERO, 0.07)
	await _wait(2.4)

func _shot_film_leader() -> void:
	_clear()
	_black()
	_film_mode = true
	var wash := ColorRect.new()
	wash.color = Color(0.09, 0.09, 0.08)
	wash.size = Vector2(1920, 1080)
	_scene.add_child(wash)
	_film_frame()
	var leader_tag := Ui.label("纪检部学生指导短片", 22, Color(0.6, 0.62, 0.54), Ui.font_mono())
	leader_tag.position = Vector2(0, 96)
	leader_tag.size = Vector2(1920, 30)
	leader_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_scene.add_child(leader_tag)
	var leader := Leader.new()
	leader.position = Vector2(760, 250)
	leader.size = Vector2(400, 400)
	_scene.add_child(leader)
	for n in [3, 2, 1]:
		if _skip or _ended: return
		leader.set_number(int(n))
		Sfx.play("click", -16.0)
		await _wait(0.85)
	if _skip or _ended: return
	var prod := Ui.label("深圳实验中学 学生会纪检部　出品\n2026 · 16mm · 校内放映", 16, Color(0.55, 0.56, 0.48), Ui.font_mono())
	prod.position = Vector2(0, 760)
	prod.size = Vector2(1920, 60)
	prod.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_scene.add_child(prod)
	await _wait(1.4)

func _shot_guidance() -> void:
	var cards := [
		["01", "先看有效期，再抬头看人。", "证件是死的，站在窗口前的人是活的。"],
		["02", "称呼同学，不要称呼编号。", "你手里的是学生证，不是档案。"],
		["03", "遇到冲突，先退回窗口，再按对讲机。", "你的职责是核验，不是制服。"]
	]
	for i in cards.size():
		var c: Array = cards[i]
		if _skip or _ended: return
		_clear()
		var bg := ColorRect.new()
		bg.color = Color(0.075, 0.075, 0.07)
		bg.size = Vector2(1920, 1080)
		_scene.add_child(bg)
		_film_frame()
		var num := Ui.label(String(c[0]), 112, Color(0.60, 0.16, 0.12, 0.9), Ui.font_mono())
		num.position = Vector2(196, 396)
		num.size = Vector2(180, 130)
		_scene.add_child(num)
		var main := Ui.label(String(c[1]), 48, Color(0.93, 0.90, 0.79), Ui.font_serif())
		main.position = Vector2(392, 408)
		main.size = Vector2(1330, 80)
		_scene.add_child(main)
		var sub := Ui.label(String(c[2]), 23, Color(0.60, 0.60, 0.52), Ui.font_serif())
		sub.position = Vector2(396, 500)
		sub.size = Vector2(1200, 40)
		_scene.add_child(sub)
		var seal := Ui.panel(Color(0, 0, 0, 0), Color(0.62, 0.16, 0.12, 0.75), 3, 1, 0)
		seal.position = Vector2(1560, 700)
		seal.size = Vector2(150, 150)
		seal.rotation = -0.10
		_scene.add_child(seal)
		var seal_text := Ui.label("纪检部\n审片", 22, Color(0.66, 0.18, 0.13, 0.85), Ui.font_serif())
		seal_text.position = Vector2(18, 44)
		seal_text.size = Vector2(114, 66)
		seal_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		seal.add_child(seal_text)
		var tag := Ui.label("第 %d 讲 / 共 3 讲　　纪检部学生指导短片" % (i + 1), 15, Color(0.42, 0.44, 0.38), Ui.font_mono())
		tag.position = Vector2(196, 946)
		tag.size = Vector2(900, 22)
		_scene.add_child(tag)
		await _wait(2.4)
		if _skip or _ended: return
	await _wait(0.2)

func _shot_title() -> void:
	_clear()
	_film_mode = false
	_black()
	await _wait(0.4)
	var title := Ui.label("请 出 示 学 生 证", 96, Color("#efe7cd"), Ui.font_serif())
	title.position = Vector2(0, 400)
	title.size = Vector2(1920, 130)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.modulate = Color(1, 1, 1, 0)
	_scene.add_child(title)
	var sub := Ui.label("深圳实验中学 · 2026 春季执勤 · 学生会纪检部", 24, Color("#9aa08c"), Ui.font_serif())
	sub.position = Vector2(0, 546)
	sub.size = Vector2(1920, 36)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.modulate = Color(1, 1, 1, 0)
	_scene.add_child(sub)
	create_tween().tween_property(title, "modulate", Color(1, 1, 1, 1), 0.9)
	create_tween().tween_property(sub, "modulate", Color(1, 1, 1, 1), 1.2)
	Sfx.play("chime", -8.0)
	await _wait(2.6)
	if _ended: return
	finished.emit()
