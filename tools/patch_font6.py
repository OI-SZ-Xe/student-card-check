# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Ui.gd"
s = io.open(p, encoding="utf-8").read()
start = s.index("static func _ensure_bitmap() -> void:")
new = '''static func _ensure_bitmap() -> void:
	if _bmp_ready:
		return
	_bmp_ready = true
	var fb := SystemFont.new()
	fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
	for sz in [13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 30, 32, 34, 46, 48, 62, 76, 96]:
		var path := "res://art/fonts/pixel%d.fnt" % sz
		if ResourceLoader.exists(path):
			var f: Font = load(path)
			f.fallbacks = [fb]
			_bitmaps[sz] = f

static func _pick(font: Font, size: int) -> Font:
	_ensure_bitmap()
	if _bitmaps.has(size):
		return _bitmaps[size]
	return font if font != null else font_ui()
'''
s = s[:start] + new
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("Ui fonts fixed")
