#Requires -Version 5.1
<#
    LE3 Russian Mod Translation — installer / установщик
    Ставит русские .tlk в папки установленных модов Mass Effect 3 Legendary Edition.
    Copies Russian .tlk files into the folders of installed Mass Effect 3 LE mods.
#>

[CmdletBinding()]
param(
    # Путь к папке игры (…\Mass Effect Legendary Edition). Если не задан — ищем сами.
    [string] $GamePath,
    # Список компонентов через запятую, напр. -Components EGM,Spectre. "all" — все доступные.
    [string] $Components,
    # Не задавать вопросов (для скриптов и CI).
    [switch] $Silent,
    # Английский интерфейс установщика.
    [switch] $English,
    # Вариант перевода под мужского Шепарда.
    [switch] $Male
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$distRoot = Join-Path $root 'dist'

# ---------------------------------------------------------------- локализация
$ru = @{
    title       = 'Русификатор модов Mass Effect 3 Legendary Edition'
    noDist      = 'Не найдена папка "dist" рядом с установщиком. Распакуй архив целиком.'
    findGame    = 'Ищу установленную игру...'
    foundGame   = 'Игра найдена:'
    askGame     = 'Укажи путь к папке игры (в ней есть подпапка Game\ME3)'
    badGame     = 'По этому пути нет Game\ME3\BioGame\DLC. Проверь путь.'
    noMods      = 'В игре не найдено ни одного мода из тех, что мы переводим. Сначала установи моды.'
    available   = 'Доступные компоненты (мод установлен в игре):'
    missing     = 'Пропущены — соответствующий мод не установлен:'
    prompt      = 'Что поставить? Введи номера через пробел, "0" — все, Enter — отмена'
    nothing     = 'Ничего не выбрано. Выходим.'
    installing  = 'Устанавливаю...'
    backup      = 'резервная копия'
    done        = 'Готово. Установлено компонентов:'
    donePost    = 'Запусти игру с русским языком — текст модов будет по-русски.'
    variantF    = 'Вариант перевода: женский Шепард.'
    variantM    = 'Вариант перевода: мужской Шепард.'
    undo        = 'Чтобы откатить, запусти uninstall.ps1 или удали файлы *_RUS.tlk из папок модов.'
    err         = 'ОШИБКА:'
}
$en = @{
    title       = 'Mass Effect 3 Legendary Edition mod translation (Russian)'
    noDist      = 'The "dist" folder was not found next to the installer. Extract the whole archive.'
    findGame    = 'Looking for the installed game...'
    foundGame   = 'Game found:'
    askGame     = 'Enter the path to the game folder (the one containing Game\ME3)'
    badGame     = 'There is no Game\ME3\BioGame\DLC under that path. Check it.'
    noMods      = 'None of the supported mods are installed. Install the mods first.'
    available   = 'Available components (mod is installed):'
    missing     = 'Skipped - the corresponding mod is not installed:'
    prompt      = 'What to install? Enter numbers separated by spaces, "0" for all, Enter to cancel'
    nothing     = 'Nothing selected. Exiting.'
    installing  = 'Installing...'
    backup      = 'backup'
    done        = 'Done. Components installed:'
    donePost    = 'Start the game with Russian language selected - mod text will be in Russian.'
    variantF    = 'Translation variant: female Shepard.'
    variantM    = 'Translation variant: male Shepard.'
    undo        = 'To revert, run uninstall.ps1 or delete the *_RUS.tlk files from the mod folders.'
    err         = 'ERROR:'
}
$L = if ($English) { $en } else { $ru }

# ------------------------------------------------------------------ описания
$componentInfo = [ordered]@{
    'EGM'                = @{ ru = 'Expanded Galaxy Mod (+ Squad pack)'; en = 'Expanded Galaxy Mod (+ Squad pack)' }
    'ProjectVariety'     = @{ ru = 'Project Variety'; en = 'Project Variety' }
    'Spectre'            = @{ ru = 'Spectre Expansion Mod'; en = 'Spectre Expansion Mod' }
    'CommunityPatch'     = @{ ru = 'LE3 Community Patch'; en = 'LE3 Community Patch' }
    'AppearanceModMenu'  = @{ ru = 'Appearance Mod Menu (меню внешности)'; en = 'Appearance Mod Menu' }
    'ApartmentAdditions' = @{ ru = 'Apartment Additions (квартира)'; en = 'Apartment Additions' }
    'Hairstyles'         = @{ ru = 'Причёски для Шепард (набор модов)'; en = 'Shepard hairstyle mods (bundle)' }
}

function Write-Head([string] $text) {
    Write-Host ''
    Write-Host ('=' * 72) -ForegroundColor DarkGray
    Write-Host " $text" -ForegroundColor Cyan
    Write-Host ('=' * 72) -ForegroundColor DarkGray
}

function Test-GameRoot([string] $path) {
    if ([string]::IsNullOrWhiteSpace($path)) { return $false }
    return Test-Path (Join-Path $path 'Game\ME3\BioGame\DLC')
}

function Find-GameRoot {
    $candidates = New-Object System.Collections.Generic.List[string]

    # 1. Реестр: официальный ключ Legendary Edition
    foreach ($key in @(
            'HKLM:\SOFTWARE\WOW6432Node\BioWare\Mass Effect Legendary Edition',
            'HKLM:\SOFTWARE\BioWare\Mass Effect Legendary Edition')) {
        try {
            $v = (Get-ItemProperty -Path $key -ErrorAction Stop).'Install Dir'
            if ($v) { $candidates.Add($v) }
        } catch { }
    }

    # 2. Все библиотеки Steam из libraryfolders.vdf
    $steam = $null
    foreach ($key in @('HKLM:\SOFTWARE\WOW6432Node\Valve\Steam', 'HKLM:\SOFTWARE\Valve\Steam')) {
        try { $steam = (Get-ItemProperty -Path $key -ErrorAction Stop).InstallPath } catch { }
        if ($steam) { break }
    }
    if ($steam) {
        $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
        if (Test-Path $vdf) {
            foreach ($m in [regex]::Matches((Get-Content $vdf -Raw), '"path"\s*"([^"]+)"')) {
                $lib = $m.Groups[1].Value -replace '\\\\', '\'
                $candidates.Add((Join-Path $lib 'steamapps\common\Mass Effect Legendary Edition'))
            }
        }
        $candidates.Add((Join-Path $steam 'steamapps\common\Mass Effect Legendary Edition'))
    }

    # 3. Обычные места для Steam / EA App / Epic на всех дисках
    foreach ($drive in (Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Free -ne $null })) {
        foreach ($tail in @(
                'SteamLibrary\steamapps\common\Mass Effect Legendary Edition',
                'Program Files (x86)\Steam\steamapps\common\Mass Effect Legendary Edition',
                'Program Files\EA Games\Mass Effect Legendary Edition',
                'Program Files (x86)\EA Games\Mass Effect Legendary Edition',
                'Program Files\Epic Games\MassEffectLegendaryEdition',
                'Games\Mass Effect Legendary Edition')) {
            $candidates.Add((Join-Path ($drive.Root) $tail))
        }
    }

    foreach ($c in $candidates) { if (Test-GameRoot $c) { return (Resolve-Path $c).Path } }
    return $null
}

function Get-Components {
    $result = New-Object System.Collections.Generic.List[object]
    foreach ($name in $componentInfo.Keys) {
        $dir = Join-Path $distRoot $name
        if (-not (Test-Path $dir)) { continue }
        $folders = Get-ChildItem -Path $dir -Directory | Select-Object -ExpandProperty Name
        $files = Get-ChildItem -Path $dir -Recurse -Filter '*_RUS.tlk'
        $result.Add([pscustomobject]@{
                Name        = $name
                Description = if ($English) { $componentInfo[$name].en } else { $componentInfo[$name].ru }
                Folders     = $folders
                Files       = $files
            })
    }
    return $result
}

# ------------------------------------------------------------------- начало
try {
    Write-Head $L.title

    if (-not (Test-Path $distRoot)) { throw $L.noDist }

    if (-not (Test-GameRoot $GamePath)) {
        Write-Host $L.findGame
        $GamePath = Find-GameRoot
    }
    while (-not (Test-GameRoot $GamePath)) {
        if ($Silent) { throw $L.badGame }
        if ($GamePath) { Write-Host "$($L.badGame)" -ForegroundColor Yellow }
        $GamePath = (Read-Host $L.askGame).Trim('"', ' ')
        if (-not $GamePath) { throw $L.badGame }
    }
    $dlcRoot = Join-Path $GamePath 'Game\ME3\BioGame\DLC'
    Write-Host "$($L.foundGame) $GamePath" -ForegroundColor Green

    $all = Get-Components
    $present = @($all | Where-Object {
            $c = $_
            @($c.Folders | Where-Object { Test-Path (Join-Path $dlcRoot $_) }).Count -gt 0
        })
    $absent = @($all | Where-Object { $present -notcontains $_ })

    if ($present.Count -eq 0) { throw $L.noMods }

    Write-Host ''
    Write-Host $L.available -ForegroundColor White
    for ($i = 0; $i -lt $present.Count; $i++) {
        Write-Host ("  [{0}] {1}" -f ($i + 1), $present[$i].Description)
    }
    if ($absent.Count -gt 0) {
        Write-Host ''
        Write-Host $L.missing -ForegroundColor DarkGray
        foreach ($a in $absent) { Write-Host ("      - " + $a.Description) -ForegroundColor DarkGray }
    }

    # ------------------------------------------------------------- выбор
    $chosen = $null
    if ($Components) {
        if ($Components.Trim().ToLower() -eq 'all') {
            $chosen = $present
        } else {
            $want = $Components -split '[,;\s]+' | Where-Object { $_ }
            $chosen = @($present | Where-Object { $want -contains $_.Name })
        }
    } elseif ($Silent) {
        $chosen = $present
    } else {
        Write-Host ''
        $answer = (Read-Host $L.prompt).Trim()
        if ($answer -eq '') { Write-Host $L.nothing; exit 0 }
        if ($answer -eq '0') {
            $chosen = $present
        } else {
            $idx = $answer -split '[,;\s]+' | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
            $chosen = @($idx | Where-Object { $_ -ge 1 -and $_ -le $present.Count } | ForEach-Object { $present[$_ - 1] })
        }
    }
    $chosen = @($chosen | Group-Object -Property Name | ForEach-Object { $_.Group[0] })
    if ($chosen.Count -eq 0) { Write-Host $L.nothing; exit 0 }

    # --------------------------------------------------------- установка
    Write-Host ''
    Write-Host $L.installing -ForegroundColor White
    $installed = 0
    foreach ($c in $chosen) {
        $compDir = Join-Path $distRoot $c.Name
        $any = $false
        foreach ($file in $c.Files) {
            $rel = $file.FullName.Substring($compDir.Length).TrimStart('\')
            $target = Join-Path $dlcRoot $rel
            $targetDir = Split-Path -Parent $target
            if (-not (Test-Path $targetDir)) { continue }   # мод не установлен — молча пропускаем
            if (Test-Path $target) {
                $bak = "$target.bak"
                if (-not (Test-Path $bak)) {
                    Copy-Item $target $bak
                    Write-Host ("      {0}: {1}" -f $L.backup, (Split-Path -Leaf $bak)) -ForegroundColor DarkGray
                }
            }
            $source = $file.FullName
            if ($Male) {
                $maleSource = $source -replace '_RUS\.tlk$', '_RUS.male.tlk'
                if (Test-Path $maleSource) { $source = $maleSource }
            }
            Copy-Item $source $target -Force
            Write-Host ("  + " + $rel) -ForegroundColor Green
            $any = $true
        }
        if ($any) { $installed++ }
    }

    Write-Host ''
    Write-Host "$($L.done) $installed" -ForegroundColor Green
    $variantNote = if ($Male) { $L.variantM } else { $L.variantF }
    Write-Host $variantNote
    Write-Host $L.donePost
    Write-Host $L.undo -ForegroundColor DarkGray
} catch {
    Write-Host ''
    Write-Host "$($L.err) $($_.Exception.Message)" -ForegroundColor Red
    if (-not $Silent) { Write-Host ''; Read-Host 'Enter' | Out-Null }
    exit 1
}

if (-not $Silent) { Write-Host ''; Read-Host 'Enter' | Out-Null }
