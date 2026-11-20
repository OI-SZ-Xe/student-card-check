extends Control

var _intro: Control = null
var _desk: Control = null
var _shot_path := ""
var _shot_mode := "desk"
var _shot_delay := -1.0
var _shot_page := 0

func _ready() -> void:
	randomize()
	theme = Ui.app_theme()
	add_child(CrtOverlay.new())
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--shot="):
			_shot_path = arg.substr(7)
		elif arg.begins_with("--shot-mode="):
			_shot_mode = arg.substr(12)
		elif arg.begins_with("--shot-delay="):
			_shot_delay = float(arg.substr(13))
		elif arg.begins_with("--shot-page="):
			_shot_page = int(arg.substr(12))
	if _shot_path == "":
		_show_menu()
		return
	if _shot_path != "":
		if _shot_mode == "register":
			var reg_shot := preload("res://scripts/ui/Register.gd").new()
			add_child(reg_shot)
			await get_tree().create_timer(1.0).timeout
			await RenderingServer.frame_post_draw
			var reg_img := get_viewport().get_texture().get_image()
			reg_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "portraits":
			var grid := Control.new()
			grid.size = Vector2(1920, 1080)
			add_child(grid)
			var bgp := ColorRect.new()
			bgp.color = Color(0.10, 0.11, 0.10)
			bgp.size = Vector2(1920, 1080)
			grid.add_child(bgp)
			for i in 8:
				var pr := Portrait.new()
				pr.setup(1000 + i * 37, false, false)
				pr.position = Vector2(120 + (i % 4) * 440, 150 + (i / 4) * 400)
				pr.size = Vector2(240, 320)
				grid.add_child(pr)
				var pr2 := Portrait.new()
				pr2.setup(1000 + i * 37, true, false)
				pr2.position = Vector2(380 + (i % 4) * 440, 150 + (i / 4) * 400)
				pr2.size = Vector2(160, 200)
				grid.add_child(pr2)
			await get_tree().create_timer(0.8).timeout
			await RenderingServer.frame_post_draw
			var pi_img := get_viewport().get_texture().get_image()
			pi_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "afterintro":
			_on_registered("周予安", "八年级（2）班", "insight")
			await get_tree().create_timer(0.6).timeout
			for c in get_children():
				if c is Intro:
					c._do_skip()
			await get_tree().create_timer(1.6).timeout
			await RenderingServer.frame_post_draw
			var ai_img := get_viewport().get_texture().get_image()
			ai_img.save_png(_shot_path)
			print("shot saved: ", _shot_path)
			get_tree().quit()
			return
		if _shot_mode == "intro":
			_intro = preload("res://scripts/screens/Intro.gd").new()
			_intro.player_name = "周予安"
			_intro.player_class = "八年级（2）班"
			add_child(_intro)
			await get_tree().create_timer(_shot_delay if _shot_delay > 0.0 else 7.5).timeout
		else:
			_start_desk(_shot_mode != "briefing")
			await get_tree().create_timer(2.0).timeout
			if _shot_mode == "manual":
				_desk.debug_manual_page(_shot_page)
			elif _shot_mode == "shop":
				_desk.debug_open_shop()
			elif _shot_mode == "signatures":
				_desk.debug_manual_page(4)
			elif _shot_mode == "verdict":
				_desk.debug_judge("approve")
			elif _shot_mode == "terminal_achv":
				_desk.debug_terminal("achv")
			elif _shot_mode == "terminal_mail":
				_desk.debug_terminal("mail")
			elif _shot_mode == "exchange":
				_desk.debug_terminal("exchange")
			elif _shot_mode == "bribe":
				_desk.debug_bribe()
			elif _shot_mode == "org":
				_desk.debug_org()
			elif _shot_mode == "terminal":
				_desk.debug_terminal("schools")
			elif _shot_mode == "terminal_wanted":
				_desk.debug_terminal("wanted")
			elif _shot_mode == "terminal_rules":
				_desk.debug_terminal("rules")
			elif _shot_mode == "interrogate":
				_desk._open_interrogation()
			elif _shot_mode == "tutorial":
				_desk._open_tutorial()
			elif _shot_mode == "settings":
				_desk._open_settings()
			elif _shot_mode == "ending":
				_desk.debug_ending()
			elif _shot_mode == "gun19":
				_desk.debug_gun_at("d19")
			elif _shot_mode == "gun26":
				_desk.debug_gun_at("d26")
			elif _shot_mode == "black20":
				_desk.debug_black()
			elif _shot_mode == "black":
				_desk.debug_terminal("black")
			elif _shot_mode == "gun":
				_desk.debug_gun(false)
			elif _shot_mode == "gunresult":
				_desk.debug_gun(true)
			elif _shot_mode == "letter":
				_desk.debug_letter()
			elif _shot_mode == "settle":
				_desk.debug_end_day()
			elif _shot_mode == "saveload":
				_desk.debug_save_load()
			await get_tree().create_timer(2.0).timeout
		await RenderingServer.frame_post_draw
		var img := get_viewport().get_texture().get_image()
		var err := img.save_png(_shot_path)
		print("shot saved: ", _shot_path, " err=", err)
		get_tree().quit()
		return
	_intro = preload("res://scripts/screens/Intro.gd").new()
	add_child(_intro)
	_intro.finished.connect(_on_intro_finished)

func _on_registered(pname: String, pclass: String, talent: String = "") -> void:
	State.player_name = pname
	State.player_class = pclass
	State.talent = talent
	State.forgery_bonus = 0.15 if Meta.runs > 0 else 0.0
	for c in get_children():
		if c is Register:
			c.queue_free()
	_intro = preload("res://scripts/screens/Intro.gd").new()
	_intro.player_name = pname
	_intro.player_class = pclass
	add_child(_intro)
	_intro.finished.connect(_on_intro_finished)

func _on_intro_finished() -> void:
	if is_instance_valid(_intro):
		var old := _intro
		_intro = null
		old.visible = false
		old.process_mode = Node.PROCESS_MODE_DISABLED
		get_tree().create_timer(1.0).timeout.connect(func() -> void:
			if is_instance_valid(old):
				old.queue_free()
		)
	_start_desk(false)

func _show_menu() -> void:
	var menu := StartMenu.new()
	add_child(menu)
	menu.choice.connect(func(kind: String) -> void:
		match kind:
			"quit":
				get_tree().quit()
			"settings":
				pass
			"new":
				menu.queue_free()
				Meta.tutorial_done = false
				var reg := preload("res://scripts/ui/Register.gd").new()
				add_child(reg)
				reg.submitted.connect(_on_registered)
			"continue":
				if SaveManager.load_slot(1):
					menu.queue_free()
					_clear_screens()
					State.endless = false
					_start_desk(true)
			"endless":
				menu.queue_free()
				_clear_screens()
				State.endless = true
				State.day = 30
				State.money = 300
				State.player_name = "科员"
				_start_desk(true)
	)

func _clear_screens() -> void:
	for c in get_children():
		if c is StartMenu or c is CrtOverlay:
			continue
		if c is Control:
			c.queue_free()

func _start_desk(skip_briefing: bool) -> void:
	var desk := preload("res://scripts/screens/Desk.gd").new()
	desk.skip_briefing = skip_briefing
	add_child(desk)
	_desk = desk


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		if _desk != null and is_instance_valid(_desk) and _desk.handle_back():
			return
		get_tree().quit()
