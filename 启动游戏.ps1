$ErrorActionPreference = "Stop"
$exe = "E:\steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe"
$proj = "F:\请出示学生证"
if (-not (Test-Path $exe)) { Write-Host "找不到 Godot: $exe"; Read-Host; exit 1 }
if (-not (Test-Path $proj)) { Write-Host "找不到工程: $proj"; Read-Host; exit 1 }
Start-Process -FilePath $exe -ArgumentList @("--path", $proj)
Write-Host "已启动，日志写入 $env:APPDATA\Godot\app_userdata\请出示学生证\debug.log"
Start-Sleep -Seconds 2
