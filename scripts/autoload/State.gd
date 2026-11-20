extends Node

signal day_started
signal day_finished(summary: Dictionary)

const START_DATE := "2026-03-01"
const TOTAL_DAYS := 30
const SAVE_VERSION := 1

var day := 1
var date := START_DATE
var money := 0
var time_left := 300.0
var suspicion := 0
var trust := 0
var corruption := 0
var player_name := "检察员"
var player_class := "八年级（3）班"
var talent := ""
var forgery_bonus := 0.0
var endless := false
var warned_once := false
var time_frozen := false
var called_this := false
var db_checked_this := false
var simple_mode := true
var upgrades: Array = []
var archive: Dictionary = {}
var total_today := 0
var handled_today := 0
var correct_today := 0
var wrong_today := 0
var correct_total := 0
var wrong_total := 0
var quota_required := 0
var quota_done := 0
var running := false
var finished := false
var ending := ""
var slot := 1
var d12_done := false
var wanted: Array = []
var mails: Array = []
var mail_seq := 1
var achievements: Dictionary = {}
var help_count := 0
var reported_count := 0
var pending_org: Dictionary = {}
var quota_missed := 0
var quota_met_days := 0
var escape_ready := false
const ACHIEVEMENTS := [
	{"key": "firstArrest", "name": "执法如山", "desc": "首次逮捕伪造者"},
	{"key": "firstCall", "name": "第一次通话", "desc": "首次使用电话核实"},
	{"key": "firstCompare", "name": "第一次比对", "desc": "首次使用对照模式"},
	{"key": "firstConfiscation", "name": "铁面无私", "desc": "首次没收伪造介绍信"},
	{"key": "confiscator", "name": "铁面无私·改", "desc": "没收一封正常介绍信"},
	{"key": "tenCorrect", "name": "十连正确", "desc": "累计正确审核 10 次"},
	{"key": "perfectDay", "name": "完美执勤", "desc": "某天零差错"},
	{"key": "corrupt", "name": "腐败的检察员", "desc": "第一次收受贿赂"},
	{"key": "undercover", "name": "暗中支持", "desc": "第一次帮助学生斗争委员会"},
	{"key": "whistleblower", "name": "举报者", "desc": "累计举报 3 次"},
	{"key": "survivalist", "name": "老油条", "desc": "活到第 30 天"},
	{"key": "fugitive", "name": "逃亡者", "desc": "触发逃亡结局"},
	{"key": "revolutionary", "name": "革命先驱", "desc": "触发革命结局"},
	{"key": "loyalist", "name": "忠诚卫士", "desc": "触发忠诚结局"}
]

var flavor := ""
var event_done: Dictionary = {}
var endings_seen: Dictionary = {}
var bribe_count := 0
var arrest_count := 0
var run_start_msec := 0
var daily_wrong: Array = []
var confiscatedNormalLetters := 0
var confiscatedItems: Array = []
var shot_org := false
var has_fake_id := false
var has_ticket := false

var stocks: Array = []
var stock_news := ""

func reset() -> void:
	day = 1
	date = START_DATE
	money = 0
	time_left = 600.0
	var frng := RandomNumberGenerator.new()
	frng.randomize()
	var flavors := [
		"一只橘猫跑进检查站，被你用水杯赶了出去。",
		"一个低年级学生递给你一瓶水，说「辛苦了」。",
		"窗外下起雨，你想起自己没带伞。",
		"广播里在念校长的讲话，声音有点失真。",
		"食堂阿姨给你留了一份午饭，已经凉了。",
		"有个学生对你敬礼，说「谢谢检察员」。"
	]
	flavor = ""
	event_done = {}
	endings_seen = {}
	bribe_count = 0
	arrest_count = 0
	run_start_msec = Time.get_unix_time_from_system()
	daily_wrong = []
	confiscatedNormalLetters = 0
	confiscatedItems = []
	shot_org = false
	has_fake_id = false
	has_ticket = false
	if frng.randf() < 0.5:
		flavor = String(flavors[frng.randi() % flavors.size()])
	suspicion = 0
	trust = 0
	corruption = 0
	player_name = "检察员"
	player_class = "八年级（3）班"
	talent = ""
	forgery_bonus = 0.0
	simple_mode = true
	upgrades = []
	archive = {}
	total_today = 0
	handled_today = 0
	correct_today = 0
	wrong_today = 0
	correct_total = 0
	wrong_total = 0
	quota_required = 0
	quota_done = 0
	running = false
	finished = false
	ending = ""
	d12_done = false
	wanted = []
	mails = []
	mail_seq = 1
	achievements = {}
	help_count = 0
	reported_count = 0
	pending_org = {}
	quota_missed = 0
	quota_met_days = 0
	escape_ready = false
	_init_market()

func start_day() -> void:
	finished = false
	running = false
	handled_today = 0
	correct_today = 0
	wrong_today = 0
	quota_done = 0
	total_today = 10
	quota_required = maxi(0, day - 5)
	update_market()
	_generate_wanted()
	_push_briefing_mail()
	_queue_org_event()
	if day == 1:
		money += 30
	if day > 1:
		var rent: int = int(Data.rules.get("rent", 10))
		var utilities: int = int(Data.rules.get("utilities", 20))
		if has_upgrade("advancedDorm"):
			utilities = 0
		if talent == "economic":
			rent = int(rent * 0.5)
			utilities = int(utilities * 0.5)
		money -= rent + utilities
	if simple_mode:
		var bonus: int = int(Data.rules.get("simple_bonus", 20))
		if talent == "economic":
			bonus += 10
		money += bonus
	time_left = 600.0
	var frng := RandomNumberGenerator.new()
	frng.randomize()
	var flavors := [
		"一只橘猫跑进检查站，被你用水杯赶了出去。",
		"一个低年级学生递给你一瓶水，说「辛苦了」。",
		"窗外下起雨，你想起自己没带伞。",
		"广播里在念校长的讲话，声音有点失真。",
		"食堂阿姨给你留了一份午饭，已经凉了。",
		"有个学生对你敬礼，说「谢谢检察员」。"
	]
	flavor = ""
	event_done = {}
	endings_seen = {}
	bribe_count = 0
	arrest_count = 0
	run_start_msec = Time.get_unix_time_from_system()
	daily_wrong = []
	confiscatedNormalLetters = 0
	confiscatedItems = []
	shot_org = false
	has_fake_id = false
	has_ticket = false
	if frng.randf() < 0.5:
		flavor = String(flavors[frng.randi() % flavors.size()])
	if has_upgrade("clock"):
		time_left += 30.0

func has_upgrade(upgrade_id: String) -> bool:
	return upgrades.has(upgrade_id)

func buy(upgrade_id: String) -> bool:
	var u: Dictionary = Data.upgrade(upgrade_id)
	if u.is_empty():
		return false
	if has_upgrade(upgrade_id):
		return false
	var price := int(u.get("price", 0))
	if money < price:
		return false
	money -= price
	upgrades.append(upgrade_id)
	return true

func earn(amount: int) -> void:
	money += amount

func spend(amount: int) -> bool:
	if money < amount:
		return false
	money -= amount
	return true

func add_suspicion(amount: int) -> void:
	suspicion = clampi(suspicion + amount, 0, 100)

func iso_add_days(iso: String, days: int) -> String:
	var unix := Time.get_unix_time_from_datetime_string(iso + "T00:00:00")
	return Time.get_datetime_string_from_unix_time(int(unix) + days * 86400).substr(0, 10)

func weekday_cn(iso: String) -> String:
	var unix := Time.get_unix_time_from_datetime_string(iso + "T00:00:00")
	var wd: int = int(Time.get_datetime_dict_from_unix_time(int(unix)).get("weekday", 0))
	return ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][int(wd) % 7]

func fmt_time(seconds: float) -> String:
	var s := int(max(0.0, seconds))
	return "%02d:%02d" % [int(s / 60.0), s % 60]

func finish_day() -> Dictionary:
	daily_wrong.append(wrong_today)
	running = false
	var summary := {
		"day": day,
		"correct": correct_today,
		"wrong": wrong_today,
		"total": handled_today,
		"money": money,
		"quota": quota_required,
		"quota_done": quota_done
	}
	day_finished.emit(summary)
	return summary

func advance_day() -> bool:
	day += 1
	date = iso_add_days(date, 1)
	if day > TOTAL_DAYS:
		finished = true
		ending = "day30"
		return false
	return true


func _generate_wanted() -> void:
	wanted = []
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	var count := rng.randi_range(1, 2)
	var surnames: Array = Data.names.get("surnames", ["陈"])
	var given: Array = Data.names.get("given", ["明"])
	for i in count:
		var nm := String(surnames[rng.randi() % surnames.size()]) + String(given[rng.randi() % given.size()])
		var grade := rng.randi_range(7, 9)
		wanted.append({"name": nm, "id": RuleEngine.expected_prefix(grade) + "%04d" % rng.randi_range(0, 9999)})

func is_wanted(v: Dictionary) -> bool:
	for w in wanted:
		if String(w.get("name", "")) == String(v.get("name", "")) and String(w.get("id", "")) == String(v.get("student_id", "")):
			return true
	return false

func rules_versions() -> Array:
	var out: Array = []
	out.append({"v": 1, "day": 1, "title": "第 1 版", "lines": [
		"学生证须在有效期内，过期即拒。",
		"出生年份须与年级对应：七年级 2013、八年级 2012、九年级 2011。",
		"学号前四位须为入学年份：七年级 2025、八年级 2024、九年级 2023。"
	]})
	if day >= 3:
		out.append({"v": 2, "day": 3, "title": "第 2 版", "lines": [
			"实验学生须出示校园卡，状态须为有效。",
			"外校学生须出示一次性通行证，须在有效期内。"
		]})
	if day >= 8:
		out.append({"v": 3, "day": 8, "title": "第 3 版", "lines": [
			"一次性通行证作废。",
			"外校学生须出示纪检部准入证，须含学号、姓名、学校与来意。"
		]})
	if day >= 15:
		out.append({"v": 4, "day": 15, "title": "第 4 版", "lines": [
			"转学目的须提供转学介绍信。",
			"介绍信须有转出、转入双方教导主任签字。"
		]})
	if day >= 20:
		out.append({"v": 5, "day": 20, "title": "第 5 版", "lines": [
			"全体人员须出示健康证明。",
			"健康状态非「健康」者一律拒绝。"
		]})
	if day >= 25:
		out.append({"v": 6, "day": 25, "title": "第 6 版", "lines": [
			"伪造介绍信一律没收，不予退还。",
			"没收正常介绍信罚款 25 元，须登记在案。"
		]})
	return out

func _push_briefing_mail() -> void:
	var docs: Array = []
	for d in Data.doc_rules:
		if day >= int(d.get("day", 1)):
			docs.append(String(d.get("name", "")))
	var body := "第 %d 天执勤简报\n余额：%d 元\n今日核验：%s\n拒签指标：%s" % [
		day, money, "、".join(docs),
		("至少拒绝 %d 人" % quota_required) if quota_required > 0 else "无"
	]
	mails.append({"id": mail_seq, "day": day, "kind": "brief", "from": "学生会纪检部", "subject": "第 %d 天执勤简报" % day, "body": body})
	mail_seq += 1
	if mails.size() > 12:
		mails = mails.slice(mails.size() - 12, mails.size())

func add_mail(from_who: String, subject: String, body: String, kind: String = "info") -> void:
	mails.append({"id": mail_seq, "day": day, "kind": kind, "from": from_who, "subject": subject, "body": body})
	mail_seq += 1

func unlock(ach_key: String, ach_name: String) -> bool:
	if achievements.has(ach_key):
		return false
	achievements[ach_key] = ach_name
	return true


func _queue_org_event() -> void:
	pending_org = {}
	var events := {
		3: {"subject": "我们需要你的帮助", "body": "检察员同学：\n\n我们知道你在校门执勤。今晚七点，校门口小卖部后面。\n有些东西，只有你能带进来。\n\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 2},
		7: {"subject": "一封联名信", "body": "检察员同学：\n\n走廊尽头，有个女生把一封联名信塞给你。\n信上有四十三个签名，要求学校取消夜间查寝。\n请把它带进办公楼。\n\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 3},
		12: {"subject": "印刷费", "body": "检察员同学：\n\n我们要印一批刊物，缺五十元。\n你可以不出面，钱放在窗台上就行。\n\n——学生斗争委员会", "cost": 50, "help": 1, "risk": 4},
		18: {"subject": "校警突击检查", "body": "检察员同学：\n\n今晚校警会查教室。有个同学在你检查站的隔间里。\n让他待到换班，别登记。\n\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 8},
		22: {"subject": "处分记录", "body": "检察员同学：\n\n教育局系统里有一份学生处分记录。\n凌晨两点，档案科的终端不会有人盯着。\n拷出来，我们会记住这件事。\n\n——学生斗争委员会", "cost": 0, "help": 2, "risk": 12},
		28: {"subject": "革命前夜", "body": "检察员同学：\n\n明天，全校会动起来。\n你只需要做一件事：在七点整，把校门打开。\n\n——学生斗争委员会", "cost": 0, "help": 1, "risk": 10}
	}
	pending_org = events.get(day, {})
	if not pending_org.is_empty():
		add_mail("学生斗争委员会", String(pending_org.get("subject", "")), String(pending_org.get("body", "")), "org")

func add_trust(amount: int) -> void:
	trust = clampi(trust + amount, 0, 10)
	help_count += amount


func _init_market() -> void:
	stocks = [
		{"name": "实验科技", "code": "SY001", "base": 5.0, "price": 5.0, "prev": 5.0, "positions": []},
		{"name": "深中贸易", "code": "SZ002", "base": 8.5, "price": 8.5, "prev": 8.5, "positions": []},
		{"name": "深高级制造", "code": "SG003", "base": 12.0, "price": 12.0, "prev": 12.0, "positions": []},
		{"name": "实验金融", "code": "SY004", "base": 9.5, "price": 9.5, "prev": 9.5, "positions": []},
		{"name": "深外基建", "code": "SW005", "base": 7.5, "price": 7.5, "prev": 7.5, "positions": []}
	]
	stock_news = ""

func update_market() -> void:
	if stocks.is_empty():
		_init_market()
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	for st in stocks:
		st.prev = st.price
		var drift := rng.randf_range(-0.05, 0.05)
		if talent == "insight":
			drift *= 0.7
		var new_price: float = st.price * (1.0 + drift)
		new_price = clampf(new_price, float(st.base) * 0.5, float(st.base) * 2.0)
		st.price = snappedf(new_price, 0.01)
	stock_news = "今日无重大财经消息。"
	if rng.randf() < 0.4:
		var idx := rng.randi_range(0, stocks.size() - 1)
		var up := rng.randf() < 0.55
		var factor := 1.08 if up else 0.93
		stocks[idx].price = clampf(snappedf(float(stocks[idx].price) * factor, 0.01), float(stocks[idx].base) * 0.5, float(stocks[idx].base) * 2.0)
		stock_news = "%s%s，股价%s。" % [String(stocks[idx].name), "发布新产品" if up else "被曝资金链紧张", "上涨" if up else "下跌"]
	var blown := 0
	for st in stocks:
		var keep: Array = []
		for pos in st.positions:
			var pnl: float = (float(st.price) - float(pos.buy)) * int(pos.shares)
			if pnl + float(pos.margin) <= 0.0:
				blown += 1
			else:
				keep.append(pos)
		st.positions = keep
	if blown > 0:
		stock_news += "　（强制平仓 %d 笔）" % blown

func market_change(st: Dictionary) -> float:
	var prev := float(st.get("prev", 0.0))
	if prev <= 0.0:
		return 0.0
	return (float(st.price) - prev) / prev * 100.0

func buy_stock(idx: int, shares: int, leverage: int, price: float) -> Dictionary:
	if idx < 0 or idx >= stocks.size():
		return {"ok": false, "msg": "无效标的"}
	if shares <= 0 or leverage <= 0:
		return {"ok": false, "msg": "数量或杠杆无效"}
	var notional := price * float(shares)
	var margin := notional / float(leverage)
	if money < int(ceil(margin)):
		return {"ok": false, "msg": "保证金不足"}
	money -= int(ceil(margin))
	stocks[idx].positions.append({"shares": shares, "buy": price, "leverage": leverage, "margin": margin})
	return {"ok": true, "msg": "买入 %d 股 @ %.2f（%dx）" % [shares, price, leverage]}

func sell_stock(idx: int, pos_idx: int, price: float) -> Dictionary:
	if idx < 0 or idx >= stocks.size():
		return {"ok": false, "msg": "无效标的"}
	var positions: Array = stocks[idx].positions
	if pos_idx < 0 or pos_idx >= positions.size():
		return {"ok": false, "msg": "无效持仓"}
	var pos: Dictionary = positions[pos_idx]
	var pnl: float = (price - float(pos.buy)) * int(pos.shares)
	money += int(round(float(pos.margin) + pnl))
	positions.remove_at(pos_idx)
	return {"ok": true, "msg": "平仓：%+.2f 元" % pnl}

func position_pnl(st: Dictionary, pos: Dictionary) -> float:
	return (float(st.price) - float(pos.buy)) * int(pos.shares)


func mark_ending(key: String) -> void:
	endings_seen[key] = true
