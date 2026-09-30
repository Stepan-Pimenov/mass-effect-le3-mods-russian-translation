#Requires -Version 5.1
<#
    Собирает ME3LE-Русификатор-модов.exe из tools/installer/Installer.cs.
    Используется штатный компилятор .NET Framework 4.x, который есть в любой
    Windows 10/11 — ничего ставить не нужно.
#>

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$src = Join-Path $root 'tools\installer\Installer.cs'
$manifest = Join-Path $root 'tools\installer\app.manifest'
$out = Join-Path $root 'ME3LE-Русификатор-модов.exe'

$csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path $csc)) {
    $csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
}
if (-not (Test-Path $csc)) {
    throw 'Не найден csc.exe (.NET Framework 4.x). Обычно он лежит в C:\Windows\Microsoft.NET\Framework64\v4.0.30319\.'
}

& $csc -nologo -target:winexe -platform:anycpu -optimize+ `
    "-out:$out" "-win32manifest:$manifest" `
    -reference:System.dll -reference:System.Core.dll `
    -reference:System.Drawing.dll -reference:System.Windows.Forms.dll `
    $src

if ($LASTEXITCODE -ne 0) { throw "Компиляция завершилась с кодом $LASTEXITCODE" }

$size = [math]::Round((Get-Item $out).Length / 1KB)
Write-Host "Собрано: $out ($size KB)" -ForegroundColor Green
Write-Host 'Проверка: .\ME3LE-Русификатор-модов.exe -check'
