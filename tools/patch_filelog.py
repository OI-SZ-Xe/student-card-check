# -*- coding: utf-8 -*-
import io
dp = r"F:\请出示学生证\scripts\screens\Desk.gd"
d = io.open(dp, encoding="utf-8").read()
if "debug.log" not in d:
    d = d.replace('''func _open_terminal(site: String) -> void:''', '''func _dbg(msg: String) -> void:
	var f := FileAccess.open("user://debug.log", FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open("user://debug.log", FileAccess.WRITE)
	if f != null:
		f.seek_end()
		f.store_line("%s %s" % [Time.get_time_string_from_system(), msg])
		f.close()

func _open_terminal(site: String) -> void:
	_dbg("open_terminal site=%s paused=%s visitor_empty=%s" % [site, _paused, _visitor.is_empty()])''')
io.open(dp, "w", encoding="utf-8", newline="\n").write(d)

ep = r"F:\请出示学生证\scripts\ui\EduTerminal.gd"
e = io.open(ep, encoding="utf-8").read()
e = e.replace('''func _ready() -> void:
	set_anchors_preset''', '''func _ready() -> void:
	var lf := FileAccess.open("user://debug.log", FileAccess.READ_WRITE)
	if lf == null:
		lf = FileAccess.open("user://debug.log", FileAccess.WRITE)
	if lf != null:
		lf.seek_end()
		lf.store_line("terminal ready site=%s" % start_site)
		lf.close()
	set_anchors_preset''')
io.open(ep, "w", encoding="utf-8", newline="\n").write(e)
print("file logging")
