# -*- coding: utf-8 -*-
import io, json

# Terminal: black market site
tp = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
t = io.open(tp, encoding="utf-8").read()
t = t.replace('''	["exchange", "证券交易所"],''', '''	["exchange", "证券交易所"],
	["black", "黑市"],''')
t = t.replace('''		"exchange":
			_site_exchange()''', '''		"exchange":
			_site_exchange()
		"black":
			_site_black()''')
t += '''

func _site_black() -> void:
	if State.day < 20:
		_body.add_child(_line("黑市尚未开张。第 20 天后再来。", DIM, 17))
		return
	_body.add_child(_line("校园东侧 · 旧器材室 · 现金交易，不问来路", AMBER, 16))
	_body.add_child(_line("余额 %d 元" % State.money, GREEN, 15))
	var items := [
		["fake_id", "伪造介绍信", 50, "一套足以骗过新学校的介绍信，字迹是仿的。"],
		["ticket", "高铁票", 100, "深圳北 → 衡水北。后天 05:40，站票。"]
	]
	for it in items:
		var key := String(it[0])
		var owned: bool = State.has_fake_id if key == "fake_id" else State.has_ticket
		var vb := _block(Color(0.07, 0.1, 0.08, 0.85))
		vb.add_child(_line("%s　—　%d 元%s" % [String(it[1]), int(it[2]), "（已购买）" if owned else ""], GREEN if not owned else DIM, 17))
		vb.add_child(_line(String(it[3]), DIM, 14))
		if not owned:
			var b := Ui.button("购买", 15, Color("#12281a"), GREEN)
			b.custom_minimum_size = Vector2(160, 38)
			var price := int(it[2])
			b.pressed.connect(func() -> void:
				if State.money < price:
					_status.text = "钱不够。"
					return
				State.money -= price
				if key == "fake_id":
					State.has_fake_id = true
				else:
					State.has_ticket = true
				_status.text = "成交。东西在器材室第三排柜子里。"
				Sfx.play("paper", -12.0)
				_show("black")
			)
			vb.add_child(b)
	_body.add_child(_line("逃出去还差一封正常的转学介绍信——得顶着 25 元罚款，从检查站里收走。", DIM, 14))
'''
io.open(tp, "w", encoding="utf-8", newline="\n").write(t)

# Manual: two new pages + renderers
mp = r"F:\请出示学生证\data\manual.json"
data = json.load(io.open(mp, encoding="utf-8-sig"))
if not any(p.get("type") == "endings" for p in data):
    data.append({"title": "十 · 结局图鉴", "type": "endings"})
    data.append({"title": "十一 · 成就", "type": "achv"})
io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

gp = r"F:\请出示学生证\scripts\ui\Manual.gd"
g = io.open(gp, encoding="utf-8").read()
if "_endings()" not in g:
    g = g.replace('''		"forgery":''', '''		"endings":
			_body.add_child(_endings())
		"achv":
			_body.add_child(_achv())
		"forgery":''')
    g += '''

func _endings() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	var rows := [
		["负债", "任意一天余额低于 0 元，立即隔离审查。"],
		["腐败", "收受贿赂累计 3 次，被移交司法机关。"],
		["逃亡", "第 25 天后，手上有正常的转学介绍信、伪造介绍信与高铁票，顶栏出现「启动逃亡」。"],
		["革命", "帮助学生斗争委员会累计 5 次以上，终局未向他们开枪。"],
		["忠诚·枪毙", "帮助过组织但没到 5 次，或怀疑度过高，终局被校园安全部带走。"],
		["忠诚·平稳", "一次没帮组织、拒签达标、怀疑度低，继续担任科员。"]
	]
	for r in rows:
		var vb := _block(Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.2))
		vb.add_child(_line(String(r[0]), AMBER, 17))
		vb.add_child(_line(String(r[1]), GREEN, 14))
	return box

func _achv() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	for a in State.ACHIEVEMENTS:
		var got: bool = State.achievements.has(String(a.key))
		var line := "%s　%s　—　%s" % ["■" if got else "□", String(a.name), String(a.desc)]
		box.add_child(_line(line, GREEN if got else DIM, 15))
	return box
'''
io.open(gp, "w", encoding="utf-8", newline="\n").write(g)

# debug gun scenario
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func debug_gun_at(" not in d:
    d += '''

func debug_gun_at(sc: String) -> void:
	_paused = true
	State.running = false
	var ev := SchoolRush.new()
	ev.scenario = sc
	add_child(ev)
	ev.finished.connect(func(_r: Dictionary) -> void: ev.queue_free())
'''
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

mp2 = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp2, encoding="utf-8").read()
if 'gun19' not in m:
    m = m.replace('''			elif _shot_mode == "gun":''', '''			elif _shot_mode == "gun19":
				_desk.debug_gun_at("d19")
			elif _shot_mode == "gun26":
				_desk.debug_gun_at("d26")
			elif _shot_mode == "black":
				_desk.debug_terminal("black")
			elif _shot_mode == "gun":''')
io.open(mp2, "w", encoding="utf-8", newline="\n").write(m)
print("black market + manual pages + debug")
