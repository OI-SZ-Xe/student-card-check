class_name CheatMenu
extends Control

signal cmd(id: String)

func _ready() -> void:
	z_index = 300
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bg := ColorRect.new()
	bg.color = Color(0.02, 0.05, 0.03, 0.92)
	bg.size = Vector2(560, 780)
	add_child(bg)
	var title := Ui.label("DEVELOPER MENU", 20, Color("#8ce0a0"), Ui.font_mono())
	title.position = Vector2(20, 14)
	title.size = Vector2(400, 26)
	add_child(title)
	var hint := Ui.label("F1 关闭　仅开发版可用", 12, Color("#5f7a64"), Ui.font_mono())
	hint.position = Vector2(20, 42)
	hint.size = Vector2(400, 18)
	add_child(hint)
	var items := [
		["money+", "金钱 +200"], ["money-", "金钱 -200"],
		["time+", "时间 +180 秒"], ["freeze", "时间冻结 开/关"],
		["susp0", "怀疑度归零"], ["trust+", "信任 +3"],
		["upgrades", "解锁全部升级"], ["nextday", "直接进入下一天"],
		["gun12", "枪械事件 D12"], ["gun19", "枪械事件 D19"], ["gun26", "枪械事件 D26"], ["gun30", "枪械事件 D30"],
		["end_debt", "结局：负债"], ["end_corrupt", "结局：腐败"], ["end_escape", "结局：逃亡"],
		["end_revolution", "结局：革命"], ["end_gun", "结局：枪毙"], ["end_stable", "结局：平稳"],
		["endless", "无尽模式 开/关"], ["normal", "生成一个新的普通访客"], ["forged", "生成一个伪造访客"]
	]
	var y := 70
	for it in items:
		var b := Ui.button(String(it[1]), 14, Color("#12281a"), Color("#9ad7a2"))
		b.position = Vector2(20, y)
		b.size = Vector2(520, 30)
		var key := String(it[0])
		b.pressed.connect(func() -> void: cmd.emit(key))
		add_child(b)
		y += 33
