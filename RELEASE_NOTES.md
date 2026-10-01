Русский перевод текста, который добавляют моды Mass Effect 3 Legendary Edition. Ванильный текст игры, озвучка и текстуры не затронуты.

Переведено около **7 750 строк (~1,8 млн знаков)**: кодекс, сводки боёв, письма на терминал, описания оружия, брони, машин и напарников, все окна настроек модов, новости «Ежедневника Цербера», названия причёсок и одежды. Терминология сверена с официальным русским переводом трилогии — из LE1, LE2, LE3 и всех DLC извлечён словарь примерно на 100 000 пар «оригинал → официальный русский».

### Что нового в 1.1

**Spectre Expansion Mod переведён полностью** — было 919 строк, стало 1 412. Мод хранил в своём русском файле не перевод, а устаревшую английскую редакцию строк, из-за чего почти 500 строк (описания планет и систем, задания, сводки, текстовые приключения) считались готовыми и оставались английскими. Теперь сборка принимает за перевод только текст, в котором действительно есть кириллица.

**Выбор пола Шепард.** Письма и реплики, обращённые к Шепард, по-русски требуют рода, поэтому перевод собирается в двух вариантах. В окне установщика появился переключатель **Шепард: женский / мужской** (по умолчанию женский).

**Стиль приведён к официальной локализации.** «Коммандер» заменён на «капитан», выправлены имена: Хакет, Ариа, Гуэрта, «Синие светила», «Серый посредник».


**Перекрыт собственный русский Community Patch:** «Конрад Не Извиняется» → «Конрад не извиняется», «Вермайрский выживший» → «выживший на Вермайре», «Рональд Трейнор» → «Рональд Тейлор», три одинаковые подписи «Судьба Рональда Тейлора 1» → 1, 2 и 3.

### Состав

| Компонент | Мод | Версия мода | Строк |
|---|---|---|---:|
| `EGM` | Expanded Galaxy Mod + Squadmate Pack | 1.0.6 | 2 841 |
| `ProjectVariety` | Project Variety (+ `DLC_Shared`) | 0.7 | 2 974 |
| `Spectre` | Spectre Expansion Mod | 1.2.1 | 1 412 |
| `CommunityPatch` | LE3 Community Patch | 1.7.9 | 169 |
| `AppearanceModMenu` | Appearance Modification Menu | 2.2 | 161 |
| `ApartmentAdditions` | Apartment Additions | 1.0 | 53 |
| `Hairstyles` | More Hair for Femshep 1.1, Morning's Hairstyles 1.4.4 / PT2 1.3.1 / PT3 1.3.3, Morning's Versatile 1.0.3 | — | 137 |

### Установка

Ниже, в разделе **Assets**, нужно скачать один файл — **`ME3LE-Russian-Mods-v1.1-full.zip`** (тот, в имени которого есть `full`). Распаковать его в любую папку и запустить **`ME3LE-Русификатор-модов.exe`**. Программа сама находит игру и показывает список модов с галочками; там же выбирается пол Шепард. Остаётся нажать «Установить». Откат — кнопкой «Удалить перевод» в том же окне.

Подробная пошаговая инструкция — в [README](https://github.com/Stepan-Pimenov/mass-effect-le3-mods-russian-translation#установка).

Остальные архивы — отдельные компоненты для ручной установки: содержимое распаковывается в `…\Mass Effect Legendary Edition\Game\ME3\BioGame\DLC\` с заменой. Файлы с `.male.tlk` — вариант под мужского Шепарда: нужно скопировать такой файл и убрать из имени `.male`.

Ставить **после** всех модов. Переустановка мода через менеджер возвращает его английский файл — тогда установщик запускается ещё раз.

### Проверено

`MassEffect3.exe` 2.0.0.0, уровень совместимости модов 137, Windows 11 25H2. Для установщика нужен .NET Framework 4.x (входит в Windows 10/11), права администратора не требуются, если игра лежит не в `Program Files`.

### Известные ограничения

Перевод делался без проверки каждой строки в игре, поэтому где-то возможны шероховатости в длине строк и падежах. Намеренно оставлены по-английски названия самих модов, титры с именами авторов и названия песен в плеере.

---

A Russian translation of the text that Mass Effect 3 Legendary Edition mods add to the game. Vanilla text, audio and textures are untouched.

About **7,750 strings (~1.8M characters)**: codex entries, battle reports, terminal e-mails, weapon, armour, vehicle and squadmate descriptions, every mod settings screen, the Cerberus Daily News feed, hairstyle and outfit names.

### What's new in 1.1

**Spectre Expansion Mod is now fully translated** — 1,412 strings instead of 919. The mod keeps an outdated English revision of its strings in its own Russian file, so nearly 500 strings were counted as done and stayed English. The build now only accepts text that actually contains Cyrillic as a translation.

**Male/female Shepard.** Lines addressed to Shepard need grammatical gender in Russian, so the translation ships in two variants. The installer has a **Shepard: female / male** switch (female by default); `install.ps1` takes `-Male`.

**Style matched to the official localisation:** «коммандер» replaced with «капитан», names fixed (Хакет, Ариа, Гуэрта, «Синие светила»).


Covers Expanded Galaxy Mod 1.0.6, Project Variety 0.7, Spectre Expansion Mod 1.2.1, LE3 Community Patch 1.7.9, Appearance Modification Menu 2.2, Apartment Additions 1.0 and five Shepard hairstyle mods.

**Install:** download `ME3LE-Russian-Mods-v1.1-full.zip`, extract, run `ME3LE-Русификатор-модов.exe` (the window has an English switch), tick the components, pick Shepard's gender. Uninstall from the same window. Apply after all other mods; reinstalling a mod through a mod manager restores its English text, so just run the installer again.

Tested on `MassEffect3.exe` 2.0.0.0, mod feature level 137, Windows 11 25H2. The installer needs .NET Framework 4.x (bundled with Windows 10/11).
