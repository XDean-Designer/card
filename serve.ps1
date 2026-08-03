# 价目表 / RTB 原型 · 手机局域网预览
# 用法：在 PowerShell 中执行  .\serve.ps1
$ErrorActionPreference = 'Stop'
$port = 8765
$root = $PSScriptRoot

# 释放占用端口的旧进程
Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
  ForEach-Object {
    try { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } catch {}
  }
Start-Sleep -Milliseconds 400

$pyCmd = Get-Command python -ErrorAction SilentlyContinue
$py = if ($pyCmd) { $pyCmd.Source } else { $null }
if (-not $py) { throw '未找到 python，请先安装并加入 PATH' }

$ip = (Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object { $_.IPAddress -like '172.*' -or $_.IPAddress -like '192.168.*' -or $_.IPAddress -like '10.*' } |
  Select-Object -First 1 -ExpandProperty IPAddress)
if (-not $ip) { $ip = '本机局域网IP' }

# 使用 ASCII 文件名，避免部分手机浏览器对中文路径解析失败；窄屏会自动真机预览，?device=1 仍可强制
Write-Host "Serving: $root"
Write-Host "本机:   http://127.0.0.1:$port/demo.html"
Write-Host "手机:   http://${ip}:$port/demo.html"
Write-Host "价目表: http://${ip}:$port/demo.html?flow=price-list-filled"
Write-Host '按 Ctrl+C 结束'
Set-Location $root
& $py -m http.server $port --bind 0.0.0.0
