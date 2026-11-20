# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\project.godot"
s = io.open(p, encoding="utf-8").read()
if "Settings=" not in s:
    s = s.replace('Music="*res://scripts/autoload/Music.gd"', 'Music="*res://scripts/autoload/Music.gd"\nSettings="*res://scripts/autoload/Settings.gd"')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# Sfx bus
sp = r"F:\请出示学生证\scripts\autoload\Sfx.gd"
sf = io.open(sp, encoding="utf-8").read()
if 'bus = "SFX"' not in sf:
    sf = sf.replace("p.finished.connect(p.queue_free)", "p.finished.connect(p.queue_free)\n\tp.bus = \"SFX\"")
io.open(sp, "w", encoding="utf-8", newline="\n").write(sf)

# Music buses
mp = r"F:\请出示学生证\scripts\autoload\Music.gd"
m = io.open(mp, encoding="utf-8").read()
m = m.replace('_music.bus = "Master"', '_music.bus = "Music"')
m = m.replace('_amb = AudioStreamPlayer.new()\n\t_amb.volume_db = -80.0', '_amb = AudioStreamPlayer.new()\n\t_amb.bus = "Ambience"\n\t_amb.volume_db = -80.0')
io.open(mp, "w", encoding="utf-8", newline="\n").write(m)
print("settings + buses")
