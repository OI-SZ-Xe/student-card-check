# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Ui.gd"
s = io.open(p, encoding="utf-8").read()
start = s.index("static func _ensure_bitmap() -> void:")
new = '''static func _fallback_font() -> Font:
	if _fb_font == null:
		var fb := SystemFont.new()
		fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
		_fb_font = fb
	return _fb_font

static func _pick(font: Font, size: int) -> Font:
	if _bitmaps.has(size):
		return _bitmaps[size]
	var path := "res://art/fonts/pixel%d.fnt" % size
	if ResourceLoader.exists(path):
		var f: Font = load(path)
		f.fallbacks = [_fallback_font()]
		_bitmaps[size] = f
		return f
	return font if font != null else font_ui()
'''
s = s[:start] + new
s = s.replace("static var _bitmaps: Dictionary = {}", "static var _bitmaps: Dictionary = {}\nstatic var _fb_font: Font = null")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("lazy font loading")
