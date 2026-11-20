# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Manual.gd"
s = io.open(p, encoding="utf-8").read()

start = s.index("func _cell(")
end = s.index("func _signatures() -> void:")
new = '''func _cell(text: String, header: bool, width: int) -> Panel:
	var p := Ui.panel(Color(0.4, 0.33, 0.2, 0.16) if header else Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.28), 1, 0, 8)
	p.custom_minimum_size = Vector2(width, 40)
	var l := Ui.label(text, 15, Ui.INK if header else Ui.INK_SOFT, Ui.font_serif() if header else Ui.font_mono())
	l.position = Vector2(10, 9)
	l.size = Vector2(width - 20, 22)
	l.autowrap_mode = TextServer.AUTOWRAP_ARBITRARY
	l.clip_text = true
	p.add_child(l)
	return p

func _table(page: Dictionary) -> Control:
	var head: Array = page.get("head", [])
	var cols := maxi(1, head.size())
	var col_w := int(980.0 / float(cols))
	var grid := GridContainer.new()
	grid.columns = cols
	grid.add_theme_constant_override("h_separation", 2)
	grid.add_theme_constant_override("v_separation", 2)
	for h in head:
		grid.add_child(_cell(String(h), true, col_w))
	for row in page.get("rows", []):
		for cell in row:
			grid.add_child(_cell(String(cell), false, col_w))
	return grid

'''
s = s[:start] + new + s[end:]

s = s.replace('''		var row := Ui.rich("[b]%s[/b]　%d 元%s\\n%s" % [String(u.get("name", "")), int(u.get("price", 0)), "（已装备）" if owned else "", String(u.get("desc", ""))], 15, Ui.INK)''',
'''		var row := Ui.rich("[b]%s[/b]　%d 元%s\\n%s\\n" % [String(u.get("name", "")), int(u.get("price", 0)), "（已装备）" if owned else "", String(u.get("desc", ""))], 15, Ui.INK)''')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("manual table fixed")
