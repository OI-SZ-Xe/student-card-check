# -*- coding: utf-8 -*-
import io, json

# 1) upgrades: core three at D3/D6/D9, tools at D12, autoTrade D15
up = r"F:\请出示学生证\data\upgrades.json"
data = [
 {"id":"quickBookmarks","name":"快捷收藏夹","price":20,"day":3,"desc":"教育局网站钉在桌面。没买之前，查资料要先开浏览器、再进收藏夹。"},
 {"id":"advancedDorm","name":"高级宿舍","price":100,"day":6,"desc":"搬出临时宿舍。此后只付房租 10 元，免水电 20 元。"},
 {"id":"stickyNote","name":"便签","price":30,"day":9,"desc":"把电话号码和当日要点抄在桌角，可一键拨号。"},
 {"id":"magnifier","name":"放大镜","price":50,"day":12,"desc":"教研室外借：放大查看证件照网点与换脸痕迹。"},
 {"id":"uv_lamp","name":"紫外线灯","price":80,"day":12,"desc":"教研室外借：验签名压痕与钢印荧光。"},
 {"id":"archive","name":"档案索引卡","price":60,"day":12,"desc":"窗口显示该生在校门口的历史记录。"},
 {"id":"queue_scan","name":"队列预检单","price":70,"day":12,"desc":"提前看到下一位访客的姓名与材料数。"},
 {"id":"clock","name":"电子钟校准器","price":30,"day":12,"desc":"每日执勤时间 +30 秒。"},
 {"id":"stamp_checker","name":"印章识别器","price":120,"day":12,"desc":"自动比对年级、出生年与学号前缀。"},
 {"id":"autoTrade","name":"一键填写交割单","price":30,"day":15,"desc":"股票下单自动填入现价与 1 份。"}
]
io.open(up, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

# 2) State: day length, 10 visitors, advance, dorm rent, sticky rename not needed
sp = r"F:\请出示学生证\scripts\autoload\State.gd"
s = io.open(sp, encoding="utf-8").read()
s = s.replace("\ttotal_today = clampi(6 + int(day / 5.0), 6, 18)", "\ttotal_today = 10")
s = s.replace("\ttime_left = 300.0", "\ttime_left = 600.0")
old_rent = '''	if day > 1:
		var rent: int = int(Data.rules.get("rent", 10)) + int(Data.rules.get("utilities", 20))
		money -= rent
	if simple_mode:
		money += int(Data.rules.get("simple_bonus", 20))'''
new_rent = '''	if day == 1:
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
		money += bonus'''
assert old_rent in s
s = s.replace(old_rent, new_rent)
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# 3) Ui button disabled style already; Shop: filter by day and show lock
shp = r"F:\请出示学生证\scripts\ui\Shop.gd"
sh = io.open(shp, encoding="utf-8").read()
sh = sh.replace('''	for u in Data.upgrades:
		_grid.add_child(_make_card(u))''', '''	for u in Data.upgrades:
		if int(u.get("day", 1)) > State.day:
			continue
		_grid.add_child(_make_card(u))''')
io.open(shp, "w", encoding="utf-8", newline="\n").write(sh)

# 4) Desk: notepad -> stickyNote
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
d = d.replace('State.has_upgrade("notepad")', 'State.has_upgrade("stickyNote")')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("B1 economy/upgrades done")
