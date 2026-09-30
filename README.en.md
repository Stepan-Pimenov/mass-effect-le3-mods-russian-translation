# Russian translation for Mass Effect 3 Legendary Edition mods

A Russian translation of the text that popular ME3 Legendary Edition mods add to the game. Vanilla game text is left untouched — only content the base game never had is translated.

> **Русская версия: [README.md](README.md)**

The translation matches the official Russian localisation of the trilogy. Every term was checked against the shipped Russian text (Reapers, the Crucible, C-Sec, STG, medi-gel, planet names, weapon and armour names), and proper nouns were taken from the official LE1, LE2, LE3 and DLC translations rather than transliterated by ear.

---

## What is translated

| Component | Mod | Strings |
|---|---|---:|
| **EGM** | [Expanded Galaxy Mod](https://www.nexusmods.com/masseffectlegendaryedition/mods/136) + Squad Pack | 2,841 |
| **ProjectVariety** | [Project Variety](https://www.nexusmods.com/masseffectlegendaryedition/mods/819) (+ shared file) | 2,974 |
| **Spectre** | [Spectre Expansion Mod](https://www.nexusmods.com/masseffectlegendaryedition/mods/1213) | 915 |
| **CommunityPatch** | [LE3 Community Patch](https://www.nexusmods.com/masseffectlegendaryedition/mods/9) | 98 |
| **AppearanceModMenu** | [Appearance Mod Menu](https://www.nexusmods.com/masseffectlegendaryedition/mods/1130) | 161 |
| **ApartmentAdditions** | Apartment Additions | 53 |
| **Hairstyles** | Shepard hairstyle mod bundle | 137 |

Roughly **7,200 strings, about 1.4 million characters**: codex entries, battle reports, terminal e-mails, descriptions of weapons, armour, vehicles and squadmates, every mod settings screen, the Cerberus Daily News feed, and hairstyle and outfit names.

**Deliberately left in English:** the mod names themselves, credits with author names, and song titles in the music player.

**Not touched:** vanilla game text, audio and textures.

---

## Installation

### Option 1: the installer (easiest)

1. Download the archive from [Releases](../../releases) and extract it anywhere.
2. Run **`Install.bat`**.
3. The installer finds the game, lists the components and installs the ones you pick.

Components whose mod is not installed never show up in the list, so nothing unnecessary gets copied.

To install specific components without any prompts:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Components EGM,Spectre -Silent -English
```

If the game lives somewhere unusual, point the installer at it:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -GamePath "D:\Games\Mass Effect Legendary Edition" -English
```

### Option 2: manual copy

`dist/<Component>/` already mirrors the game's folder layout. Copy the contents of the component you want into

```
…\Mass Effect Legendary Edition\Game\ME3\BioGame\DLC\
```

and overwrite. For EGM, for example, `DLC_MOD_EGM_RUS.tlk` has to end up in
`DLC\DLC_MOD_EGM\CookedPCConsole\`.

### Uninstalling

Run **`Uninstall.bat`** — it restores the `*_RUS.tlk.bak` backups the installer made before overwriting anything. You can also just delete the `*_RUS.tlk` files by hand, but then the mod will fall back to English text.

---

## Requirements

* Mass Effect Legendary Edition, the **ME3** part
* The mods you want translated, already installed
* The game language set to **Russian**
* Windows PowerShell 5.1 (ships with every Windows 10/11) — for the installer only

The translation does not depend on any modding-tool version: it simply replaces a text file. If a mod author ships a major update with new strings, those strings stay English until the translation is updated.

---

## Order relative to your mod manager

Install this **after** all your mods are in place (after ME3Tweaks Mod Manager, ALOT and so on). If you later reinstall a mod through the manager it will put its own English `_RUS.tlk` back — just run the installer again.

---

## How it was made

`tools/` holds the Python scripts everything was built with:

* a reader and writer for the binary `.tlk` format, including the Huffman string compression;
* extraction of the official Russian text from LE1 (out of Oodle-compressed UE3 `.pcc` packages), LE2, LE3 and every DLC, producing a dictionary of roughly 100,000 "source → official Russian" pairs;
* automatic reuse of that official text by exact match, normalised match, fuzzy match, prefix match and paragraph match. Mods often take a vanilla codex entry and append their own paragraphs, so the vanilla part fills itself in and only the new text is translated by hand;
* generators for repetitive settings strings, weapon names and planet data blocks.

The translation itself lives in `translation/` as JSON files of the form `"string id": "Russian text"`. Edit them there and rebuild:

```bash
python tools/build.py            # build .tlk files into build/
python tools/build.py --install  # build and copy straight into the game
```

The game path comes from the `ME3LE_PATH` (game root) or `ME3LE_DLC` environment variable; without them it falls back to the default at the top of `tools/build.py`.

Build priority: text from `translation/` → the mod's existing Russian string → English.

Two folders are intentionally absent from the repository: `source/` (dumped mod text) and `reference/` (the official translation extracted from the game itself), because both are someone else's intellectual property. You generate them locally from your own copy of the game:

```bash
python tools/dump.py             # dump the installed mods' text into source/
python tools/build_le1_ref.py    # official LE1 translation dictionary
python tools/build_le2_ref.py    # LE2
python tools/build_dlc_ref.py    # LE3 DLC
```

---

## Found a mistake?

Open an [Issue](../../issues) with the mod, the text you saw (or a screenshot). Pull requests are welcome too: edit the relevant file in `translation/` and the translation rebuilds from it.

The translation was produced without checking every line in-game, so some strings may still be too long for their UI slot or read awkwardly. Reports are appreciated.

---

## Rights and credits

This is a derivative work based on mod text. All rights to the mods themselves belong to their authors; this repository contains only the translated text and the tooling — no mod or game content. If you are a mod author and would like the translation taken down or moved, just open an issue.

Thanks to the authors of Expanded Galaxy Mod, Project Variety, Spectre Expansion Mod, LE3 Community Patch, Appearance Mod Menu and the rest, and to the ME3Tweaks team for Legendary Explorer, without which reverse-engineering the formats would have been far harder.
