class_name LetterView
extends Control

var _modal_z := 100

# 模态层永远压住桌面元素

signal closed

var letter: Dictionary = {}
var _uv: Label = null
var _mag: Label = null

func _ready() -> void:
	z_index = _modal_z
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0.04, 0.05, 0.04, 0.72)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dim)

	var paper := Ui.panel(Color("#ece2c6"), Color("#8d7c52"), 2, 1, 26)
	paper.position = Vector2(430, 170)
	paper.size = Vector2(1060, 740)
	add_child(paper)

	var head := Ui.label("转 学 介 绍 信", 34, Ui.INK, Ui.font_serif())
	head.position = Vector2(44, 28)
	head.size = Vector2(600, 44)
	paper.add_child(head)
	var meta := Ui.label("学生：%s　　学号：%s" % [String(letter.get("student_name", "")), String(letter.get("student_id", ""))], 15, Ui.INK_SOFT, Ui.font_mono())
	meta.position = Vector2(44, 76)
	meta.size = Vector2(700, 22)
	paper.add_child(meta)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(44, 108)
	rule.size = Vector2(972, 2)
	paper.add_child(rule)

	var body := Ui.rich("", 17, Ui.INK)
	body.position = Vector2(44, 132)
	body.size = Vector2(972, 90)
	body.scroll_active = false
	body.text = "兹证明　%s　同学因家庭搬迁，申请转入　%s　就读。\n双方校长已签字盖章，请予办理。" % [String(letter.get("student_name", "")), String(letter.get("to_school", ""))]
	paper.add_child(body)

	_add_block(paper, 44, 250, "转出校长签字", String(letter.get("from_school", "")), String(letter.get("from_sig_id", "")), String(letter.get("variant_from", "genuine")))
	_add_block(paper, 540, 250, "转入校长签字", String(letter.get("to_school", "")), String(letter.get("to_sig_id", "")), String(letter.get("variant_to", "genuine")))

	_uv = Ui.label("", 15, Color(0.20, 0.30, 0.55), Ui.font_mono())
	_uv.position = Vector2(44, 470)
	_uv.size = Vector2(972, 24)
	paper.add_child(_uv)
	_mag = Ui.label("", 15, Color(0.20, 0.30, 0.55), Ui.font_mono())
	_mag.position = Vector2(44, 500)
	_mag.size = Vector2(972, 24)
	paper.add_child(_mag)

	var hint := Ui.label("对照样本见《仿真手册》第五章。紫外线看压痕，放大镜看墨色。", 13, Ui.INK_SOFT, Ui.font_serif())
	hint.position = Vector2(44, 540)
	hint.size = Vector2(700, 20)
	paper.add_child(hint)

	var uv_btn := Ui.button("紫外线灯 (U)", 16, Ui.INK_SOFT, Ui.PAPER)
	uv_btn.position = Vector2(44, 590)
	uv_btn.size = Vector2(220, 46)
	uv_btn.disabled = not State.has_upgrade("uv_lamp")
	uv_btn.pressed.connect(_use_uv)
	paper.add_child(uv_btn)

	var mag_btn := Ui.button("放大镜 (Z)", 16, Ui.INK_SOFT, Ui.PAPER)
	mag_btn.position = Vector2(284, 590)
	mag_btn.size = Vector2(220, 46)
	mag_btn.disabled = not State.has_upgrade("magnifier")
	mag_btn.pressed.connect(_use_mag)
	paper.add_child(mag_btn)

	var close := Ui.button("还给他，继续核查", 16, Ui.INK, Ui.PAPER)
	close.position = Vector2(724, 590)
	close.size = Vector2(292, 46)
	close.pressed.connect(func() -> void: closed.emit())
	paper.add_child(close)

func _add_block(parent: Control, x: float, y: float, caption: String, school: String, sig_id: String, variant: String) -> void:
	var cap := Ui.label(caption, 15, Ui.INK, Ui.font_serif())
	cap.position = Vector2(x, y)
	cap.size = Vector2(420, 22)
	parent.add_child(cap)
	var sub := Ui.label(school, 13, Ui.INK_SOFT, Ui.font_serif())
	sub.position = Vector2(x, y + 22)
	sub.size = Vector2(420, 20)
	parent.add_child(sub)
	var path := "res://art/signatures/%s.png" % sig_id
	if variant != "" and variant != "genuine":
		path = "res://art/signatures/%s_%s.png" % [sig_id, variant]
	if not ResourceLoader.exists(path):
		return
	var frame := Ui.panel(Color(0, 0, 0, 0), Color(0.4, 0.34, 0.24, 0.25), 1, 2, 6)
	frame.position = Vector2(x, y + 48)
	frame.size = Vector2(400, 150)
	parent.add_child(frame)
	var sg := Signature.new()
	sg.setup({"img": path}, 1.0)
	sg.position = Vector2(8, 8)
	sg.size = Vector2(384, 134)
	frame.add_child(sg)

func _use_uv() -> void:
	var v := String(letter.get("variant_from", "genuine"))
	var txt := "紫外线：压痕连续，纸面有轻微凸起。"
	match v:
		"plain":
			txt = "紫外线：纸面平整，没有钢印压痕。"
		"miss":
			txt = "紫外线：压痕在第三笔处中断，断口过于整齐。"
		"light":
			txt = "紫外线：压痕正常，但墨层过薄，荧光偏淡。"
		"mirror":
			txt = "紫外线：压痕方向与样本相反。"
	_uv.text = txt
	Sfx.play("click", -10.0)

func _use_mag() -> void:
	var v := String(letter.get("variant_from", "genuine"))
	var txt := "放大镜：墨色均匀，笔锋清晰。"
	match v:
		"light":
			txt = "放大镜：墨色偏灰，网点稀疏，像复印两遍。"
		"miss":
			txt = "放大镜：第三笔缺失，断口没有洇墨。"
		"mirror":
			txt = "放大镜：字形左右相反，与样本不符。"
		"plain":
			txt = "放大镜：墨色正常，但边缘发虚，没有压痕阴影。"
	_mag.text = txt
	Sfx.play("paper", -14.0)