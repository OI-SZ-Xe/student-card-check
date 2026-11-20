class_name Ui
extends RefCounted

const PAPER := Color("#e4dbc2")
const PAPER_DARK := Color("#cfc4a4")
const PAPER_EDGE := Color("#a9a184")
const INK := Color("#20262a")
const INK_SOFT := Color("#4c5257")
const RED := Color("#a6301f")
const GREEN := Color("#2f5d3a")
const GOLD := Color("#a57c2a")
const DESK := Color("#39423f")
const DESK_DARK := Color("#1b2220")
const DESK_LIGHT := Color("#454f4a")
const GLASS := Color("#3b4b43")
const WHITE := Color("#eef0e4")

static var _f_ui: Font = null
static var _f_serif: Font = null
static var _f_mono: Font = null
static var _bitmaps: Dictionary = {}
static var _fb_font: Font = null
static var _bmp_ready := false

static func font_ui() -> Font:
	if _f_ui == null:
		var f := SystemFont.new()
		f.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"])
		f.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		_f_ui = f
	return _f_ui

static func font_serif() -> Font:
	if _f_serif == null:
		var f := SystemFont.new()
		f.font_names = PackedStringArray(["SimSun", "Songti SC", "Noto Serif CJK SC", "serif"])
		f.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		_f_serif = f
	return _f_serif

static func font_mono() -> Font:
	if _f_mono == null:
		var f := SystemFont.new()
		f.font_names = PackedStringArray(["Consolas", "Courier New", "Noto Sans Mono CJK SC", "monospace"])
		f.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		_f_mono = f
	return _f_mono

static func label(text: String, size: int = 18, color: Color = INK, font: Font = null) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_override("font", _pick(font, size))
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	return l

static func rich(text: String, size: int = 16, color: Color = INK) -> RichTextLabel:
	var r := RichTextLabel.new()
	r.bbcode_enabled = true
	r.fit_content = true
	r.scroll_active = false
	r.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	r.text = text
	r.add_theme_font_override("normal_font", _pick(font_serif(), size))
	r.add_theme_font_override("bold_font", _pick(font_serif(), size))
	r.add_theme_font_size_override("normal_font_size", size)
	r.add_theme_font_size_override("bold_font_size", size)
	r.add_theme_color_override("default_color", color)
	return r

static func style(bg: Color, border: Color = Color(0, 0, 0, 0), bw: int = 2, radius: int = 2, pad: int = 10) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(bw)
	s.set_corner_radius_all(radius)
	s.content_margin_left = pad
	s.content_margin_right = pad
	s.content_margin_top = int(pad * 0.6)
	s.content_margin_bottom = int(pad * 0.6)
	return s

static func panel(bg: Color, border: Color = Color(0, 0, 0, 0), bw: int = 2, radius: int = 2, pad: int = 10) -> Panel:
	var p := Panel.new()
	var sb := style(bg, border, bw, radius, pad)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(2, 3)
	p.add_theme_stylebox_override("panel", sb)
	return p

static func button(text: String, size: int = 18, bg: Color = DESK_LIGHT, fg: Color = WHITE) -> Button:
	var b := Button.new()
	b.text = text
	b.add_theme_font_override("font", _pick(font_ui(), size))
	b.add_theme_font_size_override("font_size", size)
	b.add_theme_color_override("font_color", fg)
	b.add_theme_color_override("font_hover_color", fg)
	b.add_theme_color_override("font_pressed_color", fg)
	b.add_theme_color_override("font_disabled_color", Color(fg, 0.35))
	var normal := style(bg, bg.lightened(0.22), 1, 0, 9)
	normal.shadow_color = Color(0, 0, 0, 0.45)
	normal.shadow_size = 2
	normal.shadow_offset = Vector2(1, 2)
	var hover := style(bg.lightened(0.10), bg.lightened(0.34), 1, 0, 9)
	hover.shadow_color = Color(0, 0, 0, 0.40)
	hover.shadow_size = 2
	hover.shadow_offset = Vector2(1, 2)
	var pressed := style(bg.darkened(0.22), bg.darkened(0.05), 1, 0, 9)
	var disabled := style(Color(bg, 0.35), Color(bg, 0.22), 1, 0, 9)
	b.add_theme_stylebox_override("normal", normal)
	b.add_theme_stylebox_override("hover", hover)
	b.add_theme_stylebox_override("pressed", pressed)
	b.add_theme_stylebox_override("disabled", disabled)
	b.add_theme_stylebox_override("focus", style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	return b

static func place(c: Control, x: int, y: int, w: int, h: int) -> Control:
	c.position = Vector2(x, y)
	c.size = Vector2(w, h)
	return c

static func sep(color: Color = Color(0, 0, 0, 0.25), h: int = 2) -> Control:
	var r := ColorRect.new()
	r.color = color
	r.custom_minimum_size = Vector2(0, h)
	return r


static func app_theme() -> Theme:
	var t := Theme.new()
	var mono := font_mono()
	var dark := Color("#0b120d")
	var edge := Color("#2e5a3a")
	t.set_stylebox("normal", "LineEdit", style(dark, edge, 1, 0, 8))
	t.set_stylebox("focus", "LineEdit", style(Color("#0e1711"), Color("#d9b45c"), 1, 0, 8))
	t.set_stylebox("read_only", "LineEdit", style(Color("#0a0f0b"), edge, 1, 0, 8))
	t.set_color("font_color", "LineEdit", Color("#9ad7a2"))
	t.set_color("font_placeholder_color", "LineEdit", Color(0.6, 0.72, 0.62, 0.55))
	t.set_color("caret_color", "LineEdit", Color("#d9b45c"))
	t.set_font("font", "LineEdit", mono)
	t.set_font_size("font_size", "LineEdit", 16)

	t.set_stylebox("normal", "OptionButton", style(dark, edge, 1, 0, 6))
	t.set_stylebox("hover", "OptionButton", style(Color("#102016"), Color("#d9b45c"), 1, 0, 6))
	t.set_stylebox("pressed", "OptionButton", style(Color("#102016"), Color("#d9b45c"), 1, 0, 6))
	t.set_stylebox("focus", "OptionButton", style(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	t.set_color("font_color", "OptionButton", Color("#9ad7a2"))
	t.set_color("font_hover_color", "OptionButton", Color("#d9b45c"))
	t.set_font("font", "OptionButton", mono)
	t.set_font_size("font_size", "OptionButton", 15)

	t.set_stylebox("panel", "PopupMenu", style(Color("#0b120d"), edge, 1, 0, 6))
	t.set_stylebox("hover", "PopupMenu", style(Color("#13251a"), Color(0, 0, 0, 0), 0, 0, 6))
	t.set_color("font_color", "PopupMenu", Color("#9ad7a2"))
	t.set_color("font_hover_color", "PopupMenu", Color("#d9b45c"))
	t.set_font("font", "PopupMenu", mono)
	t.set_font_size("font_size", "PopupMenu", 15)

	for bar in ["VScrollBar", "HScrollBar"]:
		t.set_stylebox("scroll", bar, style(Color(0, 0, 0, 0.30), Color(0, 0, 0, 0), 0, 0, 0))
		t.set_stylebox("grabber", bar, style(Color("#3d5a44"), Color("#5a7a5e"), 1, 0, 0))
		t.set_stylebox("grabber_highlight", bar, style(Color("#4d6a54"), Color("#7a9a7e"), 1, 0, 0))
		t.set_stylebox("grabber_pressed", bar, style(Color("#2d4a34"), Color("#5a7a5e"), 1, 0, 0))
	return t


static func _fallback_font() -> Font:
	if _fb_font == null:
		var fb := SystemFont.new()
		fb.font_names = PackedStringArray(["SimSun", "Microsoft YaHei", "Noto Sans CJK SC"])
		fb.antialiasing = TextServer.FONT_ANTIALIASING_NONE
		fb.subpixel_positioning = TextServer.SUBPIXEL_POSITIONING_DISABLED
		fb.hinting = TextServer.HINTING_NORMAL
		_fb_font = fb
	return _fb_font

static func _pick(font: Font, size: int) -> Font:
	if size > 48:
		size = 48
	if _bitmaps.has(size):
		return _bitmaps[size]
	var path := "res://art/fonts/pixel%d.fnt" % size
	if ResourceLoader.exists(path):
		var f: Font = load(path)
		f.fallbacks = [_fallback_font()]
		_bitmaps[size] = f
		return f
	return font if font != null else font_ui()
