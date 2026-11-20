# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\tools\gen_signatures.py"
s = io.open(p, encoding="utf-8").read()
old = '''def punch(img):
    out = img.copy()
    w, h = out.size
    box = (int(w * 0.46), int(h * 0.14), int(w * 0.60), int(h * 0.50))'''
new = '''PUNCH = {
    "wang_ming": (0.54, 0.26, 0.74, 0.56),
    "li_hua": (0.52, 0.30, 0.74, 0.60),
    "zhang_li": (0.54, 0.30, 0.76, 0.62),
    "chen_fang": (0.50, 0.30, 0.72, 0.60),
    "zhao_qiang": (0.54, 0.24, 0.76, 0.56),
}

def punch(img, key):
    out = img.copy()
    w, h = out.size
    b = PUNCH.get(key, (0.45, 0.2, 0.62, 0.5))
    box = (int(w * b[0]), int(h * b[1]), int(w * b[2]), int(h * b[3]))'''
assert old in s
s = s.replace(old, new)
s = s.replace('    punch(base).save(os.path.join(OUT, spec["id"] + "_miss.png"))',
              '    punch(base, spec["id"]).save(os.path.join(OUT, spec["id"] + "_miss.png"))')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("punch boxes per principal")
