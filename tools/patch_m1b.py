# -*- coding: utf-8 -*-
import io, json

# 1) signatures.json: strip BOM, add img
p = r"F:\请出示学生证\data\signatures.json"
raw = io.open(p, "rb").read()
if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]
data = json.loads(raw.decode("utf-8"))
for k in data:
    data[k]["img"] = "res://art/signatures/%s.png" % k
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2))

# 2) Signature.gd png path
sp = r"F:\请出示学生证\scripts\ui\Signature.gd"
s = io.open(sp, encoding="utf-8").read()
if "_tex" not in s:
    s = s.replace("var progress := 1.0", "var progress := 1.0\nvar _tex: Texture2D = null")
    s = s.replace('''	data = p_data
	progress = clampf(p_progress, 0.0, 1.0)
	queue_redraw()''', '''	data = p_data
	progress = clampf(p_progress, 0.0, 1.0)
	var path := String(data.get("img", ""))
	if path != "" and ResourceLoader.exists(path):
		_tex = load(path)
	else:
		_tex = null
	queue_redraw()''')
    s = s.replace('''func _draw() -> void:
	if data.is_empty():
		return''', '''func _draw() -> void:
	if data.is_empty():
		return
	if _tex != null:
		var tw := float(_tex.get_width())
		var th := float(_tex.get_height())
		var sc: float = minf(size.x / tw, size.y / th)
		var dw := tw * sc
		var dh := th * sc
		draw_texture_rect(_tex, Rect2((size.x - dw) * 0.5, (size.y - dh) * 0.5, dw, dh), false)
		return''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(s)

# 3) Main: shot page arg
mp = r"F:\请出示学生证\scripts\Main.gd"
m = io.open(mp, encoding="utf-8").read()
if "_shot_page" not in m:
    m = m.replace('var _shot_delay := -1.0', 'var _shot_delay := -1.0\nvar _shot_page := 0')
    m = m.replace('''		elif arg.begins_with("--shot-delay="):
			_shot_delay = float(arg.substr(13))''', '''		elif arg.begins_with("--shot-delay="):
			_shot_delay = float(arg.substr(13))
		elif arg.begins_with("--shot-page="):
			_shot_page = int(arg.substr(12))''')
    m = m.replace('''			if _shot_mode == "manual":
				_desk.debug_open_manual()''', '''			if _shot_mode == "manual":
				_desk.debug_manual_page(_shot_page)''')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("done", "_tex" in io.open(sp, encoding="utf-8").read(), "_shot_page" in io.open(mp, encoding="utf-8").read())
