#Requires -Version 5.1
<#
    Откат русификатора: возвращает *_RUS.tlk.bak на место, а если копии не было — удаляет наш файл.
    Revert: restores *_RUS.tlk.bak, or deletes our file when there was no backup.
#>

[CmdletBinding()]
param(
    [string] $GamePath,
    [switch] $Silent,
    [switch] $English
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$distRoot = Join-Path $root 'dist'

$ru = @{
    title    = 'Откат русификатора модов ME3 LE'
    askGame  = 'Укажи путь к папке игры (в ней есть подпапка Game\ME3)'
    badGame  = 'По этому пути нет Game\ME3\BioGame\DLC. Проверь путь.'
    restored = 'восстановлен из копии'
    removed  = 'удалён'
    none     = 'Нечего откатывать — наших файлов в игре не найдено.'
    done     = 'Готово. Затронуто файлов:'
    err      = 'ОШИБКА:'
}
$en = @{
    title    = 'Revert the ME3 LE mod translation'
    askGame  = 'Enter the path to the game folder (the one containing Game\ME3)'
    badGame  = 'There is no Game\ME3\BioGame\DLC under that path. Check it.'
    restored = 'restored from backup'
    removed  = 'removed'
    none     = 'Nothing to revert - none of our files were found.'
    done     = 'Done. Files touched:'
    err      = 'ERROR:'
}
$L = if ($English) { $en } else { $ru }

function Test-GameRoot([string] $path) {
    if ([string]::IsNullOrWhiteSpace($path)) { return $false }
    return Test-Path (Join-Path $path 'Game\ME3\BioGame\DLC')
}

try {
    Write-Host ''
    Write-Host $L.title -ForegroundColor Cyan

    if (-not (Test-GameRoot $GamePath)) {
        # тот же поиск, что в install.ps1, но короче: спросим, если не нашли
        $guess = $null
        foreach ($key in @(
                'HKLM:\SOFTWARE\WOW6432Node\BioWare\Mass Effect Legendary Edition',
                'HKLM:\SOFTWARE\BioWare\Mass Effect Legendary Edition')) {
            try { $guess = (Get-ItemProperty -Path $key -ErrorAction Stop).'Install Dir' } catch { }
            if (Test-GameRoot $guess) { break }
        }
        if (Test-GameRoot $guess) { $GamePath = $guess }
    }
    while (-not (Test-GameRoot $GamePath)) {
        if ($Silent) { throw $L.badGame }
        if ($GamePath) { Write-Host $L.badGame -ForegroundColor Yellow }
        $GamePath = (Read-Host $L.askGame).Trim('"', ' ')
        if (-not $GamePath) { throw $L.badGame }
    }
    $dlcRoot = Join-Path $GamePath 'Game\ME3\BioGame\DLC'

    $touched = 0
    foreach ($file in (Get-ChildItem -Path $distRoot -Recurse -Filter '*_RUS.tlk')) {
        $comp = $file.FullName.Substring($distRoot.Length).TrimStart('\')
        $rel = ($comp -split '\\', 2)[1]
        $target = Join-Path $dlcRoot $rel
        $bak = "$target.bak"
        if (Test-Path $bak) {
            Move-Item $bak $target -Force
            Write-Host ("  ~ {0} ({1})" -f $rel, $L.restored) -ForegroundColor Green
            $touched++
        } elseif (Test-Path $target) {
            Remove-Item $target -Force
            Write-Host ("  - {0} ({1})" -f $rel, $L.removed) -ForegroundColor Yellow
            $touched++
        }
    }

    Write-Host ''
    if ($touched -eq 0) { Write-Host $L.none } else { Write-Host "$($L.done) $touched" -ForegroundColor Green }
} catch {
    Write-Host ''
    Write-Host "$($L.err) $($_.Exception.Message)" -ForegroundColor Red
    if (-not $Silent) { Write-Host ''; Read-Host 'Enter' | Out-Null }
    exit 1
}

if (-not $Silent) { Write-Host ''; Read-Host 'Enter' | Out-Null }
