# -*- coding: utf-8 -*-
import io, json, os, glob

for path in glob.glob(r"F:\请出示学生证\data\*.json"):
    raw = io.open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8")
    data = json.loads(text)
    if path.endswith("signatures.json"):
        slants = {"wang_ming": -5, "li_hua": 8, "zhang_li": 0, "chen_fang": 2, "zhao_qiang": -3}
        for k, v in slants.items():
            if k in data:
                data[k]["slant"] = v
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))
    print("clean", os.path.basename(path), os.path.getsize(path))

b = r"F:\请出示学生证\scripts\ui\Briefing.gd"
t = io.open(b, encoding="utf-8").read()
repl = [
    ('\tpaper.position = Vector2(560, 170)\n\tpaper.size = Vector2(800, 720)', '\tpaper.position = Vector2(560, 200)\n\tpaper.size = Vector2(800, 640)'),
    ('\tbody.position = Vector2(48, 150)\n\tbody.size = Vector2(704, 300)', '\tbody.position = Vector2(48, 150)\n\tbody.size = Vector2(704, 210)'),
    ('\tnews.position = Vector2(48, 470)\n\tnews.size = Vector2(704, 110)', '\tnews.position = Vector2(48, 380)\n\tnews.size = Vector2(704, 100)'),
    ('\tmoney.position = Vector2(48, 596)', '\tmoney.position = Vector2(48, 500)'),
    ('\tstart.position = Vector2(268, 636)\n\tstart.size = Vector2(264, 52)', '\tstart.position = Vector2(268, 546)\n\tstart.size = Vector2(264, 52)'),
    ('\tseal.position = Vector2(600, 620)', '\tseal.position = Vector2(596, 534)'),
]
for old, new in repl:
    if old in t:
        t = t.replace(old, new)
old_money = '\tvar money := Ui.label("上月结余 %d 元　·　今日房租水电已扣　·　简单模式补贴已入账" % State.money, 13, Ui.INK_SOFT, Ui.font_mono())'
new_money = ('\tvar rent_note := "首日入住临时宿舍，免扣房租水电" if day <= 1 else "房租水电已扣"\n'
             '\tvar money := Ui.label("当前余额 %d 元　·　%s　·　简单模式补贴已入账" % [State.money, rent_note], 13, Ui.INK_SOFT, Ui.font_mono())')
if old_money in t:
    t = t.replace(old_money, new_money)
io.open(b, "w", encoding="utf-8", newline="\n").write(t)
print("briefing patched")
