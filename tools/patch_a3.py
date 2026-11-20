# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\ui\Manual.gd"
s = io.open(p, encoding="utf-8").read()
start = s.index("func _signatures() -> Control:")
end = s.index("func _phones() -> Control:")
new = '''func _signatures() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	for sch in Data.schools:
		for role in ["principal", "dean"]:
			var sig_key := "sig" if role == "principal" else "dean_sig"
			var sid := String(sch.get(sig_key, ""))
			var data := Data.sig(sid)
			if data.is_empty():
				continue
			var row := Ui.panel(Color(0, 0, 0, 0.03), Color(0.35, 0.28, 0.18, 0.2), 1, 0, 10)
			row.custom_minimum_size = Vector2(1000, 104)
			var sig := Signature.new()
			sig.setup(data, 1.0)
			sig.position = Vector2(8, 4)
			sig.size = Vector2(268, 92)
			row.add_child(sig)
			var role_cn := "校长" if role == "principal" else "教导主任"
			var nm := Ui.label("%s　%s　%s" % [String(data.get("name", "")), role_cn, String(sch.get("name", ""))], 18, Ui.INK, Ui.font_serif())
			nm.position = Vector2(296, 14)
			nm.size = Vector2(520, 24)
			row.add_child(nm)
			var st := Ui.label(String(data.get("style", "")), 13, Ui.INK_SOFT, Ui.font_serif())
			st.position = Vector2(296, 42)
			st.size = Vector2(640, 40)
			st.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			row.add_child(st)
			var ink := Ui.label("墨色 %s" % String(data.get("ink", "")), 11, Ui.INK_SOFT, Ui.font_mono())
			ink.position = Vector2(296, 80)
			ink.size = Vector2(220, 18)
			row.add_child(ink)
			box.add_child(row)
	return box

'''
s = s[:start] + new + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("signatures page rebuilt")
