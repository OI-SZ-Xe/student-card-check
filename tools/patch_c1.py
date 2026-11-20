# -*- coding: utf-8 -*-
import io

# State: organization fields + events
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
if "var help_count" not in s:
    s = s.replace("var achievements: Dictionary = {}", "var achievements: Dictionary = {}\nvar help_count := 0\nvar reported_count := 0\nvar pending_org: Dictionary = {}\nvar quota_missed := 0\nvar quota_met_days := 0\nvar escape_ready := false")
    s = s.replace("\tachievements = {}", "\tachievements = {}\n\thelp_count = 0\n\treported_count = 0\n\tpending_org = {}\n\tquota_missed = 0\n\tquota_met_days = 0\n\tescape_ready = false")
    s = s.replace("\t_generate_wanted()\n\t_push_briefing_mail()", "\t_generate_wanted()\n\t_push_briefing_mail()\n\t_queue_org_event()")
    s += '''

func _queue_org_event() -> void:
	pending_org = {}
	var events := {
		3: {"subject": "我们需要你的帮助", "body": "检察员同学：\\n\\n我们知道你在校门执勤。今晚七点，校门口小卖部后面。\\n有些东西，只有你能带进来。\\n\\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 2},
		7: {"subject": "一封联名信", "body": "检察员同学：\\n\\n走廊尽头，有个女生把一封联名信塞给你。\\n信上有四十三个签名，要求学校取消夜间查寝。\\n请把它带进办公楼。\\n\\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 3},
		12: {"subject": "印刷费", "body": "检察员同学：\\n\\n我们要印一批刊物，缺五十元。\\n你可以不出面，钱放在窗台上就行。\\n\\n——学生斗争委员会", "cost": 50, "help": 1, "risk": 4},
		18: {"subject": "校警突击检查", "body": "检察员同学：\\n\\n今晚校警会查教室。有个同学在你检查站的隔间里。\\n让他待到换班，别登记。\\n\\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 8},
		22: {"subject": "处分记录", "body": "检察员同学：\\n\\n教育局系统里有一份学生处分记录。\\n凌晨两点，档案科的终端不会有人盯着。\\n拷出来，我们会记住这件事。\\n\\n——学生斗争委员会", "cost": 0, "help": 2, "risk": 12},
		28: {"subject": "革命前夜", "body": "检察员同学：\\n\\n明天，全校会动起来。\\n你只需要做一件事：在七点整，把校门打开。\\n\\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 10}
	}
	pending_org = events.get(day, {})

func add_trust(amount: int) -> void:
	trust = clampi(trust + amount, 0, 10)
	help_count += amount
'''
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# OrgEvent modal
org = '''class_name OrgEvent
extends Control

signal chosen(kind: String)

var data: Dictionary = {}

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	size = Vector2(1920, 1080)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.72)
	dim.position = Vector2.ZERO
	dim.size = Vector2(1920, 1080)
	add_child(dim)

	var paper := Ui.panel(Color("#e4dbc2"), Color("#8d7c52"), 2, 1, 30)
	paper.position = Vector2(500, 210)
	paper.size = Vector2(920, 640)
	add_child(paper)

	var head := Ui.label("学 生 斗 争 委 员 会", 26, Ui.INK, Ui.font_serif())
	head.position = Vector2(44, 30)
	head.size = Vector2(600, 34)
	paper.add_child(head)
	var sub := Ui.label("主题：%s" % String(data.get("subject", "")), 15, Ui.INK_SOFT, Ui.font_mono())
	sub.position = Vector2(44, 70)
	sub.size = Vector2(700, 22)
	paper.add_child(sub)
	var rule := ColorRect.new()
	rule.color = Ui.INK
	rule.position = Vector2(44, 102)
	rule.size = Vector2(832, 2)
	paper.add_child(rule)

	var body := Ui.rich(String(data.get("body", "")), 17, Ui.INK)
	body.position = Vector2(44, 124)
	body.size = Vector2(832, 300)
	body.scroll_active = false
	paper.add_child(body)

	var opts := [
		["help", "帮他们", "信任 +%d" % int(data.get("help", 1))],
		["report", "举报给纪检部", "怀疑度 -2，嘉奖 +10"],
		["delete", "删除邮件", "什么都不做"]
	]
	if int(data.get("cost", 0)) > 0:
		opts[0][2] = "花费 %d 元，信任 +%d" % [int(data.get("cost", 0)), int(data.get("help", 1))]
	var y := 452
	for o in opts:
		var b := Ui.button("%s　—　%s" % [String(o[1]), String(o[2])], 17, Ui.INK, Ui.PAPER)
		b.position = Vector2(44, y)
		b.size = Vector2(832, 52)
		var key := String(o[0])
		b.pressed.connect(func() -> void: chosen.emit(key))
		paper.add_child(b)
		y += 60
'''
io.open(r"F:\请出示学生证\scripts\ui\OrgEvent.gd", "w", encoding="utf-8", newline="\n").write(org)
print("state org + modal written")
