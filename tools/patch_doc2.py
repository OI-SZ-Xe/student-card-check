# -*- coding: utf-8 -*-
import io
# CardView: stop merging extras
cp = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(cp, encoding="utf-8").read()
start = c.find("func _extra_rows() -> Array:")
if start != -1:
    end = c.find("\nfunc ", start + 10)
    c = c[:start] + "func _extra_rows() -> Array:\n\treturn []\n" + (c[end+1:] if end != -1 else "")
io.open(cp, "w", encoding="utf-8", newline="\n").write(c)

# Desk: add doc stack
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "func _build_docs(" not in d:
    d = d.replace('''func _build_tools() -> void:''', '''func _build_docs() -> void:
	for c in get_children():
		if c is DocCard:
			c.queue_free()
	var docs: Dictionary = _visitor.get("docs", {})
	var meta := {
		"campus_card": ["校园卡", [["卡号", "见卡面"], ["状态", "正常/异常"], ["有效期", "至本学期末"]]],
		"temp_pass": ["临时通行证", [["有效期至", String(docs.get("temp_pass", {}).get("valid_until", ""))], ["签发", "校门卫"]], ],
		"security_pass": ["纪检部准入证", [["来意", String(docs.get("security_pass", {}).get("purpose", "（空白）"))]]],
		"health_cert": ["健康证明", [["状态", String(docs.get("health_cert", {}).get("status", ""))]]],
		"transfer_letter": ["转学介绍信", [["转出", String(docs.get("transfer_letter", {}).get("from_school", ""))], ["转入", "深圳实验中学"], ["签名", "见原件"]]]
	}
	var i := 0
	for key in ["campus_card", "temp_pass", "security_pass", "health_cert", "transfer_letter"]:
		if not docs.has(key):
			continue
		var m: Array = meta[key]
		var dc := DocCard.new()
		dc.setup(String(m[0]), m[1])
		dc.position = Vector2(360 + i * 34, 470 + i * 26)
		dc.z_index = 6
		add_child(dc)
		i += 1

func _build_tools() -> void:''')
    d = d.replace('''	_build_stamps()''', '''	_build_stamps()
	_build_docs()''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("doc cards")
