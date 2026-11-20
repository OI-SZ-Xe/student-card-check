class_name SignatureFont
extends RefCounted

const GLYPHS := {
	"王": [
		[[18, 26], [40, 24], [62, 25], [84, 26]],
		[[24, 46], [46, 45], [68, 46], [80, 45]],
		[[52, 24], [51, 45], [52, 66], [51, 78]],
		[[14, 76], [38, 74], [64, 76], [88, 74]]
	],
	"明": [
		[[18, 22], [18, 60]],
		[[18, 22], [46, 21], [46, 60]],
		[[20, 40], [44, 39]],
		[[18, 60], [46, 59]],
		[[58, 18], [57, 62], [62, 70]],
		[[57, 18], [74, 20], [76, 34]],
		[[76, 24], [75, 62], [70, 72]],
		[[60, 42], [74, 41]],
		[[60, 52], [74, 51]]
	],
	"李": [
		[[16, 26], [52, 25]],
		[[34, 12], [33, 54]],
		[[33, 30], [18, 52]],
		[[33, 30], [48, 50]],
		[[24, 60], [50, 58], [48, 70], [36, 80]],
		[[22, 70], [56, 68]]
	],
	"华": [
		[[20, 20], [16, 44], [10, 60]],
		[[22, 22], [30, 36]],
		[[40, 30], [80, 28]],
		[[58, 14], [57, 72]],
		[[44, 50], [52, 62], [44, 74]],
		[[56, 52], [64, 50], [66, 64]]
	],
	"张": [
		[[14, 22], [24, 18], [30, 26], [20, 34], [30, 42], [16, 44]],
		[[14, 56], [28, 54]],
		[[40, 16], [38, 62]],
		[[40, 34], [56, 28]],
		[[40, 46], [58, 42]],
		[[44, 58], [64, 70]]
	],
	"丽": [
		[[14, 20], [86, 18]],
		[[26, 32], [24, 62]],
		[[24, 32], [44, 31], [44, 62]],
		[[56, 32], [54, 62]],
		[[54, 32], [74, 31], [74, 62]],
		[[30, 44], [40, 43]],
		[[60, 44], [70, 43]]
	],
	"陈": [
		[[18, 18], [16, 56]],
		[[16, 30], [26, 24], [28, 34], [18, 40]],
		[[38, 22], [72, 20]],
		[[54, 10], [53, 66]],
		[[53, 34], [40, 54]],
		[[53, 34], [68, 52]],
		[[58, 58], [66, 64]]
	],
	"芳": [
		[[22, 14], [24, 26]],
		[[46, 12], [48, 25]],
		[[16, 24], [56, 22]],
		[[36, 30], [34, 52]],
		[[34, 30], [52, 28]],
		[[50, 32], [40, 46], [36, 58]],
		[[40, 44], [52, 56]]
	],
	"赵": [
		[[18, 30], [44, 28]],
		[[30, 18], [34, 46], [46, 58]],
		[[26, 44], [48, 42]],
		[[16, 60], [38, 58], [52, 50]],
		[[58, 26], [54, 44]],
		[[62, 28], [76, 22]],
		[[52, 50], [72, 40]],
		[[66, 40], [78, 52]]
	],
	"强": [
		[[16, 20], [26, 16], [32, 24], [22, 32], [32, 40], [18, 44]],
		[[16, 54], [30, 52]],
		[[46, 26], [68, 24], [68, 42], [46, 44], [46, 26]],
		[[56, 44], [55, 66]],
		[[44, 56], [68, 54], [68, 66], [44, 68], [44, 56]],
		[[56, 70], [60, 76]]
	]
}

static func glyph(ch: String) -> Array:
	return GLYPHS.get(ch, [])

static func build(text: String, data: Dictionary) -> Array:
	var out: Array = []
	var slant := deg_to_rad(float(data.get("slant", 0.0)))
	var spacing := float(data.get("spacing", 0.94))
	var jitter := float(data.get("jitter", 0.8))
	var weight := float(data.get("weight", 4.5))
	var rng := RandomNumberGenerator.new()
	rng.seed = int(data.get("seed", 17))
	var x_off := 0.0
	var pen_end := Vector2.ZERO
	for i in text.length():
		var ch := text.substr(i, 1)
		var g := glyph(ch)
		if g.is_empty():
			x_off += 90.0 * spacing
			continue
		var dy := rng.randf_range(-0.9, 0.9) * jitter
		var rot := rng.randf_range(-0.012, 0.012) * jitter
		var first := true
		for stroke in g:
			var pts := PackedVector2Array()
			for p in stroke:
				var x := x_off + float(p[0])
				var y := float(p[1]) + dy
				var dx := (x - x_off - 50.0) * rot
				x += -(y - 50.0) * tan(slant) + dx
				pts.append(Vector2(x, y))
			if first and data.get("link", false) and pen_end != Vector2.ZERO and pts.size() > 0:
				var link := PackedVector2Array([pen_end, Vector2((pen_end.x + pts[0].x) * 0.5, minf(pen_end.y, pts[0].y) - 6.0), pts[0]])
				out.append({"pts": link, "w": weight * 0.55})
			first = false
			out.append({"pts": pts, "w": weight * rng.randf_range(0.92, 1.08)})
			pen_end = pts[pts.size() - 1]
		x_off += 100.0 * spacing
	if String(data.get("flourish", "")) == "underline":
		var total := maxf(x_off, 100.0)
		var line := PackedVector2Array()
		for k in 16:
			var t := float(k) / 15.0
			line.append(Vector2(-10.0 + total * t, 112.0 - 6.0 * t + sin(t * PI * 1.4) * 4.0))
		out.append({"pts": line, "w": weight * 0.62})
	return out
