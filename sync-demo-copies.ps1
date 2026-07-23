# Sync card/demo.html -> Chinese mirror copies (byte-identical).
$ErrorActionPreference = 'Stop'
$src = 'd:\RTB优化工程\card\demo.html'
$dst1 = 'd:\RTB优化工程\card\剑琅联盟-RTB重构.html'
$dst2 = 'd:\RTB优化工程\剑琅联盟-卡模板演示包\剑琅联盟-RTB重构.html'

if (-not (Test-Path -LiteralPath $src)) { throw "Missing source: $src" }
$dst2Dir = Split-Path -LiteralPath $dst2 -Parent
if (-not (Test-Path -LiteralPath $dst2Dir)) { New-Item -ItemType Directory -Path $dst2Dir -Force | Out-Null }

[System.IO.File]::Copy($src, $dst1, $true)
[System.IO.File]::Copy($src, $dst2, $true)

$hashes = (Get-FileHash -LiteralPath @($src, $dst1, $dst2)).Hash | Select-Object -Unique
if ($hashes.Count -ne 1) {
  Write-Error 'Sync failed: hash mismatch after copy.'
  exit 1
}
Write-Host "Synced demo.html -> 2 mirrors OK"
