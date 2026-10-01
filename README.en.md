# Russian translation for Mass Effect 3 Legendary Edition mods

A Russian translation of the text that popular ME3 Legendary Edition mods add to the game. Vanilla game text is left untouched — only content the base game never had is translated.

> **Русская версия: [README.md](README.md)**

The translation matches the official Russian localisation of the trilogy. Every term was checked against the shipped Russian text (Reapers, the Crucible, C-Sec, STG, medi-gel, planet, weapon and armour names), and proper nouns were taken from the official LE1, LE2, LE3 and DLC translations rather than transliterated by ear.

---

## Contents

* [What is translated](#what-is-translated)
* [Installation](#installation)
* [Technical details](#technical-details)
* [Compatibility](#compatibility)
* [How it was made](#how-it-was-made)
* [Feedback](#feedback)
* [Licence](#licence)

---

## What is translated

| Component | Mod | Mod version | Strings |
|---|---|---|---:|
| `EGM` | [Expanded Galaxy Mod](https://www.nexusmods.com/masseffectlegendaryedition/mods/422) + Squadmate Pack | 1.0.6 | 2,841 |
| `ProjectVariety` | [Project Variety](https://www.nexusmods.com/masseffectlegendaryedition/mods/1481) (+ the shared `DLC_Shared` file) | 0.7 | 2,974 |
| `Spectre` | [Spectre Expansion Mod](https://www.nexusmods.com/masseffectlegendaryedition/mods/15) | 1.2.1 | 1,412 |
| `CommunityPatch` | [LE3 Community Patch](https://www.nexusmods.com/masseffectlegendaryedition/mods/13) | 1.7.9 | 169 |
| `AppearanceModMenu` | [Appearance Modification Menu](https://www.nexusmods.com/masseffectlegendaryedition/mods/694) | 2.2 | 161 |
| `ApartmentAdditions` | [Apartment Additions](https://www.nexusmods.com/masseffectlegendaryedition/mods/1598) | 1.0 | 53 |
| `Hairstyles` | Shepard hairstyle mods (five of them, listed below) | — | 137 |

Roughly **7,750 strings, about 1.8 million characters**: codex entries, battle reports, terminal e-mails, descriptions of weapons, armour, vehicles and squadmates, every mod settings screen, the Cerberus Daily News feed, and hairstyle and outfit names.

The `Hairstyles` component covers five mods:

| Mod | Version |
|---|---|
| [More Hair for Femshep (ME3LE)](https://www.nexusmods.com/masseffectlegendaryedition/mods/493) | 1.1 |
| [Morning's Hairstyles for FemShep LE3](https://www.nexusmods.com/masseffectlegendaryedition/mods/726) | 1.4.4 |
| [Morning's Hairstyles for FemShep LE3 PT2](https://www.nexusmods.com/masseffectlegendaryedition/mods/1075) | 1.3.1 |
| [Morning's Hairstyles for Femshep LE3 PT3](https://www.nexusmods.com/masseffectlegendaryedition/mods/1451) | 1.3.3 |
| [Morning's Versatile Hairstyles for Femshep LE3](https://www.nexusmods.com/masseffectlegendaryedition/mods/1867) | 1.0.3 |

**Style.** The text follows the official localisation of the trilogy: Commander Shepard is «капитан Шепард», and names are checked against the game.

**Male and female Shepard.** Letters and lines addressed to Shepard need grammatical gender in Russian, so the translation is built in two variants. The installer has a **Shepard: female / male** switch (female by default).

**Deliberately left in English:** the mod names themselves, credits with author names, and song titles in the music player.

**Not touched:** vanilla game text, audio, textures, models, scripts.

---

## Installation

### The simple way

**1. Download one file.** On the [releases page](../../releases), under **Assets**, pick the file with **full** in its name — `ME3LE-Russian-Mods-v1.1-full.zip`. It is the largest one in the list. The other files are only for people who want the translation for a single specific mod.

**2. Extract it.** Right-click the downloaded archive, choose **Extract All…**, then **Extract**. Anywhere is fine. Do not run the program from inside the archive — it will not find its own files.

**3. Open the extracted folder** and double-click **`ME3LE-Русификатор-модов.exe`**. The window has a Russian/English switch in the top-right corner.

If Windows shows a blue "Windows protected your PC" screen, click **More info**, then **Run anyway**. Windows says this about any program without a paid signing certificate.

**4. Check the game folder.** The top field, **"Game folder:"**, is filled in automatically. If it is empty, click **Browse…** and pick the `Mass Effect Legendary Edition` folder — the one that contains the `Game` folder.

**5. Look at the "What to translate:" list.** Everything is ticked already. Greyed-out rows marked "mod not installed" are mods you do not have, which is fine.

**6. Pick Shepard's gender** with the **Shepard: female / male** switch. Female is the default. It only affects lines addressed to Shepard in letters and dialogue.

**7. Click "Install"** and wait for the "Done" line. Close the window.

**8. The game must be set to Russian**, otherwise the translation will not show up.

That's it.

**To remove the translation**, run the same program and click **"Uninstall"** — the mods' English text comes back. A backup of every English file is made before it is replaced, so you can always roll back.

**If you reinstall a mod** through a mod manager, it puts its English file back. Just run the program again.

**Install the translation after all other mods**, not before.

### Manual copy

The archive contains a `dist/` folder that already mirrors the game's layout. Copy the contents of the component you want, overwriting, into

```
…\Mass Effect Legendary Edition\Game\ME3\BioGame\DLC\
```

For EGM, for example, `DLC_MOD_EGM_RUS.tlk` has to end up in `DLC\DLC_MOD_EGM\CookedPCConsole\`.

Next to every file there is a matching `.male.tlk` — the male Shepard variant. To install it by hand, copy that one and drop `.male` from the name.

Per-component archives named `ME3LE-Russian-EGM-v1.1.zip` are also attached to each release; their contents go straight into the `DLC` folder.

### Command line

A PowerShell version of the installer is included for scripted setups:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Components EGM,Spectre -Silent -English
powershell -ExecutionPolicy Bypass -File install.ps1 -Components all -Male -Silent -English
powershell -ExecutionPolicy Bypass -File install.ps1 -GamePath "D:\Games\Mass Effect Legendary Edition" -English
powershell -ExecutionPolicy Bypass -File uninstall.ps1 -English
```

Without parameters `install.ps1` runs interactively. `-English` switches the output language, `-Male` installs the male Shepard variant.

---

## Technical details

**What actually changes.** The translation consists entirely of replacing `<DLCName>_RUS.tlk` files — the containers holding every mod string for the Russian locale. Nothing else is added or removed. `PCConsoleTOC.bin` is left alone, since `.tlk` sizes are not tracked there.

| File | Goes into | Size | Strings |
|---|---|---:|---:|
| `DLC_MOD_EGM_RUS.tlk` | `DLC_MOD_EGM\CookedPCConsole\` | 391 KB | 2,840 |
| `DLC_MOD_EGM_Squad_RUS.tlk` | `DLC_MOD_EGM_Squad\CookedPCConsole\` | < 1 KB | 1 |
| `DLC_MOD_ProjectVariety_RUS.tlk` | `DLC_MOD_ProjectVariety\CookedPCConsole\` | 334 KB | 1,624 |
| `DLC_Shared_RUS.tlk` | `DLC_MOD_ProjectVariety\CookedPCConsole\` | 69 KB | 1,350 |
| `DLC_MOD_Spectre_RUS.tlk` | `DLC_MOD_Spectre\CookedPCConsole\` | 311 KB | 1,412 |
| `DLC_MOD_LE3Patch_RUS.tlk` | `DLC_MOD_LE3Patch\CookedPCConsole\` | 33 KB | 169 |
| `DLC_MOD_AppearanceModMenu_RUS.tlk` | `DLC_MOD_AppearanceModMenu\CookedPCConsole\` | 4 KB | 161 |
| `DLC_MOD_ApartmentAdditions_RUS.tlk` | `DLC_MOD_ApartmentAdditions\CookedPCConsole\` | 2 KB | 53 |
| 5 hairstyle files | the corresponding mod folders | < 4 KB | 137 |

**Tested against:**

| Component | Version |
|---|---|
| Mass Effect Legendary Edition | `MassEffect3.exe` 2.0.0.0 (latest patch) |
| Mod feature level (`_metacmm.txt`) | 137 |
| Windows | 11 Pro 25H2 (build 26200) |

**Requirements:**

| For | What is needed |
|---|---|
| The GUI installer | Windows 7 or newer, .NET Framework 4.x (bundled with Windows 10/11) |
| `install.ps1` / `uninstall.ps1` | Windows PowerShell 5.1 (bundled with Windows 10/11) |
| Rebuilding the translation (`tools/`) | Python 3.8+ (developed on 3.12) |
| Rebuilding the installer | `csc.exe` shipped with Windows, nothing to install |

The translation itself is just text files — the game needs no dependencies for it.

---

## Compatibility

**Install order.** Apply the translation **last**, once every mod is in place (after ME3Tweaks Mod Manager, ALOT, ALOV and so on). Reinstalling a mod through a mod manager restores its own English `_RUS.tlk`, so the installer has to be run again.

**Texture mods** (ALOT, ALOV, A Lot of Videos) do not conflict: the translation contains no textures and touches no `.pcc` files. Order relative to them does not matter.

**Other localisations.** The vanilla `BIOGame_RUS.tlk` is untouched, so this works alongside any edits to the base game's text.

**Mod versions.** The translation was built against the versions listed above. It installs fine on newer mod versions, but strings added after the build stay English — unknown string ids are simply left alone and nothing breaks. If a mod renumbers its strings (rare, and usually only during major reworks), some text may land in the wrong place; in that case use **Uninstall** and open an issue.

**Saves** are unaffected: only text changes. The translation can be added or removed at any point, including mid-playthrough.

**Multiplayer** is not touched.

---

## How it was made

`tools/` holds the Python scripts everything was built with:

* a reader and writer for the binary `.tlk` format, including the Huffman string compression;
* extraction of the official Russian text from LE1 (out of Oodle-compressed UE3 `.pcc` packages), LE2, LE3 and every DLC, producing a dictionary of roughly 100,000 "source → official Russian" pairs;
* automatic reuse of that official text by exact match, normalised match, fuzzy match, prefix match and paragraph match. Mods often take a vanilla codex entry and append their own paragraphs, so the vanilla part fills itself in and only the new text is translated by hand;
* generators for repetitive settings strings, weapon names and planet data blocks.

The translation itself lives in `translation/` as JSON files of the form `"string id": "Russian text"`. Edits go there, then the translation is rebuilt:

```bash
python tools/build.py            # build .tlk files into build/
python tools/build.py --install  # build and copy straight into the game
python tools/mkmale.py           # generate the male Shepard overrides into translation_male/
python tools/build.py --male     # build the male variant into build_male/
python tools/mkrelease.py        # build the release archives
```

The game path comes from the `ME3LE_PATH` (game root) or `ME3LE_DLC` environment variable; without them it falls back to the default at the top of `tools/build.py`.

Build priority: text from `translation/` → the mod's existing Russian string → English.

The installer is compiled from `tools/installer/Installer.cs` with the compiler shipped in Windows:

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_installer.ps1
```

Two folders are intentionally absent from the repository: `source/` (dumped mod text) and `reference/` (the official translation extracted from the game itself), because both are someone else's intellectual property. They are generated locally from your own copy of the game:

```bash
python tools/dump.py             # dump the installed mods' text into source/
python tools/build_le1_ref.py    # official LE1 translation dictionary
python tools/build_le2_ref.py    # LE2
python tools/build_dlc_ref.py    # LE3 DLC
```

---

## Feedback

Mistakes and typos can be reported in [Issues](../../issues) — please name the mod and quote the text (or attach a screenshot). Feedback, suggestions and requests for other mods are welcome there as well.

The translation and the code, however, are **maintained by the author alone.** Pull requests and other outside changes are not accepted — deliberately, so that nothing unexpected ends up in files that people download and copy into their game. Report the text and it will be fixed in the next version. See [CONTRIBUTING.md](CONTRIBUTING.md).

The translation was produced without checking every line in-game, so some strings may still be too long for their UI slot or read awkwardly.

---

## Licence

The code (`tools/`, the installer) is MIT.

The translation (`translation/`, `dist/`) is a derivative work based on mod text: free for personal use, redistribution with attribution, no selling. Mod authors may request removal of their mod's translation through Issues.

Details in [LICENSE](LICENSE).

---

## Credits

Thanks to the authors of Expanded Galaxy Mod, Project Variety, Spectre Expansion Mod, LE3 Community Patch, Appearance Modification Menu and the rest, and to the ME3Tweaks team for Legendary Explorer, without which reverse-engineering the formats would have been far harder.

This project is not affiliated with or endorsed by Electronic Arts, BioWare, or the mod authors.
