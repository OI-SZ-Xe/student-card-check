# -*- coding: utf-8 -*-
import io, re, glob
fnt = r"F:\请出示学生证\art\fonts\pixel18.fnt"
lines = io.open(fnt, encoding="utf-8").read().splitlines()
ids = set()
for ln in lines:
    if ln.startswith("char id="):
        ids.add(int(ln.split()[1].split("=")[1]))
print("glyphs:", len(ids))
samples = []
for path in glob.glob(r"F:\请出示学生证\data\*.json"):
    samples.append(io.open(path, encoding="utf-8-sig").read())
for path in glob.glob(r"F:\请出示学生证\scripts\**\*.gd", recursive=True):
    samples.append(io.open(path, encoding="utf-8").read())
text = "".join(samples)
missing = sorted({ch for ch in text if ord(ch) > 127 and ord(ch) not in ids})
print("missing count:", len(missing))
print("missing sample:", "".join(missing[:40]))
for s in ["第一节是数学。", "检察员同学，我的材料都在这儿了。", "档案索引卡：未购置"]:
    bad = [c for c in s if ord(c) > 127 and ord(c) not in ids]
    print(repr(s), "missing:", bad)
