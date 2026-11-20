# -*- coding: utf-8 -*-
import io
p = r"F:\请出示学生证\README.md"
s = io.open(p, encoding="utf-8").read()
if "导出" not in s:
    s = s.replace("## 目录", """## 导出（本轮）

- `export_presets.cfg`：Windows Desktop / x86_64 / 单文件（`embed_pck=true`），排除 `legacy-html`、`docs`、`tools`、`tests`
- 游戏图标 `icon_game.png` 由脚本生成（学生证 + 红章「证」），写入 exe 资源
- 产物：`build/请出示学生证.exe`（约 113 MB）、`build/说明.txt`
- 重新导出命令：
  ```
  & 'E:\\steam\\steamapps\\common\\Godot Engine\\godot.windows.opt.tools.64.exe' --headless --path . --export-release "Windows Desktop" "build\\请出示学生证.exe"
  ```

## 目录""")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme export")
