extends SceneTree

func _initialize() -> void:
	for p in ["res://art/fonts/pixel16.fnt", "res://art/fonts/pixel32.fnt"]:
		print(p, " exists=", ResourceLoader.exists(p))
		var f = load(p)
		if f == null:
			print("  load failed")
			continue
		print("  class=", f.get_class(), " height16=", f.get_height(16), " width=", f.get_string_size("检查站", HORIZONTAL_ALIGNMENT_LEFT, -1, 16))
	quit()
