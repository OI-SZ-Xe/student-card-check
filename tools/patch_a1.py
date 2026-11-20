# -*- coding: utf-8 -*-
import io, json

# 1) generator: add dean signatures
gp = r"F:\请出示学生证\tools\gen_signatures.py"
g = io.open(gp, encoding="utf-8").read()
if "dean_sy" not in g:
    g = g.replace('''for spec in SPECS:
    base = ink_wash(compose(spec), spec["ink"], True)''', '''DEANS = [
    dict(id="dean_sy", text="周慧", font="kaiti", size=142, ink="#243044",
         slant=-2, gap=2, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
    dict(id="dean_sz", text="吴敏", font="simkai", size=146, ink="#2b3038",
         slant=4, gap=0, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
    dict(id="dean_sg", text="何静", font="kaiti", size=138, ink="#1f2a33",
         slant=-3, gap=3, rot=(-1, 1), dy=(-2, 2), flourish=False, weight=1),
    dict(id="dean_wgy", text="许强", font="xingkai", size=176, ink="#151c26",
         slant=-4, gap=-6, rot=(-2, 2), dy=(-4, 4), flourish=True, weight=2),
    dict(id="dean_jyj", text="谢岚", font="kaiti", size=140, ink="#2a2f36",
         slant=2, gap=1, rot=(-1, 2), dy=(-3, 3), flourish=False, weight=1),
]

SPECS = SPECS + DEANS

for spec in SPECS:
    base = ink_wash(compose(spec), spec["ink"], True)''')
io.open(gp, "w", encoding="utf-8", newline="\n").write(g)

# 2) signatures.json: add dean entries
sp = r"F:\请出示学生证\data\signatures.json"
raw = io.open(sp, "rb").read()
if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]
data = json.loads(raw.decode("utf-8"))
deans = {
    "dean_sy": ("周慧", "深圳实验中学", "楷书端正，字距偏松，落款像在批作业"),
    "dean_sz": ("吴敏", "深圳中学", "细硬笔，笔画轻，习惯性右倾"),
    "dean_sg": ("何静", "深圳高级中学", "小字收紧，第二字收笔上挑"),
    "dean_wgy": ("许强", "深圳外国语学校", "行楷带草，落款拖一道横"),
    "dean_jyj": ("谢岚", "教育局直属中学", "字形偏扁，横画压得低"),
}
for k, v in deans.items():
    data[k] = {
        "name": v[0], "school": v[1], "text": v[0],
        "ink": "#1f2630", "slant": 0, "spacing": 1.0, "weight": 4.0,
        "jitter": 0.6, "flourish": "", "style": v[2],
        "img": "res://art/signatures/%s.png" % k
    }
io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

# 3) schools.json: dean fields
sch = r"F:\请出示学生证\data\schools.json"
raw2 = io.open(sch, "rb").read()
if raw2.startswith(b"\xef\xbb\xbf"):
    raw2 = raw2[3:]
schools = json.loads(raw2.decode("utf-8"))
deans_by_school = {
    "深圳实验中学": ("周慧", "dean_sy"),
    "深圳中学": ("吴敏", "dean_sz"),
    "深圳高级中学": ("何静", "dean_sg"),
    "深圳外国语学校": ("许强", "dean_wgy"),
    "教育局直属中学": ("谢岚", "dean_jyj"),
}
for s in schools:
    d = deans_by_school.get(s["name"])
    if d:
        s["dean"] = d[0]
        s["dean_sig"] = d[1]
io.open(sch, "w", encoding="utf-8", newline="\n").write(json.dumps(schools, ensure_ascii=False, indent=2))
print("deans added")
