# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(p, encoding="utf-8").read()
# remove any partial/broken _build_docs block
start = s.find("func _build_docs() -> void:")
if start != -1:
    end = s.find("\nfunc _build_tools", start)
    if end != -1:
        s = s[:start] + s[end+1:]
s += '''

func _build_docs() -> void:
	for c in get_children():
		if c is DocCard:
			c.queue_free()
	var docs: Dictionary = _visitor.get("docs", {})
	if docs.is_empty():
		return
	var cards: Array = []
	if docs.has("campus_card"):
		cards.append(["校园卡", [["卡号", "见卡面"], ["状态", "正常 / 异常"], ["有效期", "本学期末"]]])
	if docs.has("temp_pass"):
		cards.append(["临时通行证", [["有效期至", String(docs["temp_pass"].get("valid_until", ""))], ["签发", "校门卫"]]])
	if docs.has("security_pass"):
		cards.append(["纪检部准入证", [["来意", String(docs["security_pass"].get("purpose", "（空白）"))]]])
	if docs.has("health_cert"):
		cards.append(["健康证明", [["状态", String(docs["health_cert"].get("status", ""))]]])
	if docs.has("transfer_letter"):
		cards.append(["转学介绍信", [["转出", String(docs["transfer_letter"].get("from_school", ""))], ["转入", "深圳实验中学"], ["签名", "见原件"]]])
	var i := 0
	for item in cards:
		var dc := DocCard.new()
		dc.setup(String(item[0]), item[1])
		dc.position = Vector2(380 + i * 30, 500 + i * 24)
		dc.z_index = 6
		add_child(dc)
		i += 1
'''
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("docs appended")
