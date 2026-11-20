# -*- coding: utf-8 -*-
import io

desk = r"F:\请出示学生证\scripts\screens\Desk.gd"
s = io.open(desk, encoding="utf-8").read()
s = s.replace("var _msg: Label = null", "var _msg_label: Label = null")
s = s.replace('\t_msg = Ui.label("", 18, Ui.WHITE, Ui.font_serif())', '\t_msg_label = Ui.label("", 18, Ui.WHITE, Ui.font_serif())')
s = s.replace("\t_msg.position = Vector2(16, 10)", "\t_msg_label.position = Vector2(16, 10)")
s = s.replace("\t_msg.size = Vector2(1520, 50)", "\t_msg_label.size = Vector2(1520, 50)")
s = s.replace("\t_msg.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART", "\t_msg_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART")
s = s.replace("\tbar.add_child(_msg)", "\tbar.add_child(_msg_label)")
s = s.replace("var _rules_box: VBoxContainer = null", "var _rules_box: VBoxContainer = null\nvar _stats_label: Label = null")
old_block = '\tvar stat := Ui.label("", 13, Color("#8f9a84"), Ui.font_mono())\n\tstat.name = "StatsLabel"\n\tstat.position = Vector2(18, 360)\n\tstat.size = Vector2(660, 110)\n\tpanel.add_child(stat)'
new_block = '\t_stats_label = Ui.label("", 13, Color("#8f9a84"), Ui.font_mono())\n\t_stats_label.position = Vector2(18, 360)\n\t_stats_label.size = Vector2(660, 110)\n\tpanel.add_child(_stats_label)'
assert old_block in s, "stats block not found"
s = s.replace(old_block, new_block)
start = s.index("func _fill_stats() -> void:")
end = s.index("\nfunc ", start + 10)
newfn = '''func _fill_stats() -> void:
\tif _stats_label == null:
\t\treturn
\t_stats_label.text = "today correct %d  wrong %d  seen %d / %d\\nall correct %d  wrong %d\\ncredits %d  suspicion %d" % [
\t\tState.correct_today, State.wrong_today, State.handled_today, State.total_today,
\t\tState.correct_total, State.wrong_total, State.money, State.suspicion
\t]'''
s = s[:start] + newfn + s[end:]
io.open(desk, "w", encoding="utf-8", newline="\n").write(s)

shop = r"F:\请出示学生证\scripts\ui\Shop.gd"
t = io.open(shop, encoding="utf-8").read()
t = t.replace("var _grid: GridContainer = null", "var _grid: GridContainer = null\nvar _balance: Label = null")
old = '\tvar hint := Ui.label("余额 %d 元　·　所有工具一经售出概不退换" % State.money, 14, Color(Ui.WHITE, 0.65), Ui.font_mono())\n\thint.name = "BalanceLabel"\n\thint.position = Vector2(30, 58)\n\thint.size = Vector2(700, 20)\n\tpanel.add_child(hint)'
new = '\t_balance = Ui.label("余额 %d 元　·　所有工具一经售出概不退换" % State.money, 14, Color(Ui.WHITE, 0.65), Ui.font_mono())\n\t_balance.position = Vector2(30, 58)\n\t_balance.size = Vector2(700, 20)\n\tpanel.add_child(_balance)'
assert old in t, "shop balance block not found"
t = t.replace(old, new)
old2 = '''\t\t\tvar bal := get_node_or_null("Panel/BalanceLabel")
\t\t\tif bal != null:
\t\t\t\tbal.text = "余额 %d 元　·　所有工具一经售出概不退换" % State.money'''
new2 = '''\t\t\tif _balance != null:
\t\t\t\t_balance.text = "余额 %d 元　·　所有工具一经售出概不退换" % State.money'''
assert old2 in t, "shop buy block not found"
t = t.replace(old2, new2)
io.open(shop, "w", encoding="utf-8", newline="\n").write(t)

card = r"F:\请出示学生证\scripts\ui\CardView.gd"
c = io.open(card, encoding="utf-8").read()
old3 = '\tvar serial := Ui.label("NO. %s-%04d" % [String(visitor.get("student_id", "0000")).substr(0, 4), int(visitor.get("student_id", "0").substr(4, 4)) if String(visitor.get("student_id", "")).length() >= 8 else 0], 11, Ui.INK_SOFT, Ui.font_mono())'
new3 = '\tvar sid_text := String(visitor.get("student_id", "0000"))\n\tvar serial := Ui.label("NO. %s" % sid_text, 11, Ui.INK_SOFT, Ui.font_mono())'
assert old3 in c, "card serial block not found"
c = c.replace(old3, new3)
io.open(card, "w", encoding="utf-8", newline="\n").write(c)

print("patched")
