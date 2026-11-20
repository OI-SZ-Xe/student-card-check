# -*- coding: utf-8 -*-
import io
up = r"F:\请出示学生证\scripts\ui\Ui.gd"
u = io.open(up, encoding="utf-8").read()

if "_bmp16" not in u:
    u = u.replace("static var _f_mono: Font = null", """static var _f_mono: Font = null
static var _bmp16: Font = null
static var _bmp24: Font = null
static var _bmp32: Font = null
static var _bmp_ready := false""")
    u += '''

static func _ensure_bitmap() -> void:
	if _bmp_ready:
		return
	_bmp_ready = true
	if ResourceLoader.exists("res://art/fonts/pixel16.fnt"):
		_bmp16 = load("res://art/fonts/pixel16.fnt")
	if ResourceLoader.exists("res://art/fonts/pixel24.fnt"):
		_bmp24 = load("res://art/fonts/pixel24.fnt")
	if ResourceLoader.exists("res://art/fonts/pixel32.fnt"):
		_bmp32 = load("res://art/fonts/pixel32.fnt")
	var fb := SystemFont.new()
	fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
	for f in [_bmp16, _bmp24, _bmp32]:
		if f != null:
			f.fallbacks = [fb]

static func _pick(font: Font, size: int) -> Font:
	_ensure_bitmap()
	var bmp: Font = null
	if size <= 18:
		bmp = _bmp16
	elif size <= 26:
		bmp = _bmp24
	else:
		bmp = _bmp32
	if bmp != null:
		return bmp
	return font if font != null else font_ui()
'''
    # label
    u = u.replace('\tl.add_theme_font_override("font", font if font != null else font_ui())', '\tl.add_theme_font_override("font", _pick(font, size))')
    # rich
    u = u.replace('\tr.add_theme_font_override("normal_font", font_serif())\n\tr.add_theme_font_override("bold_font", font_serif())',
                  '\tr.add_theme_font_override("normal_font", _pick(font_serif(), size))\n\tr.add_theme_font_override("bold_font", _pick(font_serif(), size))')
    # button
    u = u.replace('\tb.add_theme_font_override("font", font_ui())', '\tb.add_theme_font_override("font", _pick(font_ui(), size))')
io.open(up, "w", encoding="utf-8", newline="\n").write(u)
print("bitmap fonts wired")
