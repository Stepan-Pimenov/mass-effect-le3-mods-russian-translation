Русский перевод текста, который добавляют моды Mass Effect 3 Legendary Edition. Ванильный текст игры, озвучка и текстуры не затронуты.

Переведено около **7 750 строк (~1,8 млн знаков)**: кодекс, сводки боёв, письма на терминал, описания оружия, брони, машин и напарников, все окна настроек модов, новости «Ежедневника Цербера», названия причёсок и одежды. Терминология сверена с официальным русским переводом трилогии — из LE1, LE2, LE3 и всех DLC извлечён словарь примерно на 100 000 пар «оригинал → официальный русский».

### Что нового в 1.2.1

**Сплошная вычитка окон настроек.** Описания настроек проверены по одному и приведены к единому виду: они отвечают на вопрос, что делает мод, а не что сделать игроку.

- Подписи «ВКЛЮЧЕНО / ВЫКЛЮЧЕНО» в Community Patch приведены к общему для всей сборки виду «ВКЛ / ВЫКЛ» — 38 строк.
- «Дает послу свой наряд» заменено на «особый наряд»: в оригинале речь об отдельном наряде, а не о его собственном — 46 строк.
- Советники приведены к игровым названиям: «советник азари», «советник турианцев», «советник саларианцев».
- Задания в журнале переписаны по образцу игры, без обращений: «Отправиться на Тессию и провести разведку» вместо «Отправляйся… проведи».
- В «Дополнениях квартиры» описания говорят, что делает настройка: «Ставит на стол портрет партнера» вместо «Включить или выключить портрет».

**Исправлены ошибки самих модов, из-за которых игра показывала неправду:**

- У настройки наряда Рива оба состояния были подписаны «включено».
- У настройки наряда лейтенанта Курина состояния были перепутаны местами.
- Подпись «Майкл и Ребекка Петровские» потеряла слово «Внешность», и пара настроек выглядела разной.
- Подпись «Без разговора об эмблемах» не совпадала с описанием и заменена на «Без объявлений на Цитадели».

**Непонятные настройки стали понятными:**

- «Танцовщицы клуба» прямо говорит, что выбирается: женщины, мужчины или вперемешку.
- «Кадры со спины» превратились в «Кадры со спины Миранды», а заголовок раздела объясняет, что это возврат вырезанного из игры.
- «Сцены романа» стали «Настройками сцен романа».
- «Стыковка на Цитадели: дверь кабины» — теперь «дверь рубки», как в описании.

**Пунктуация и грамматика:** восстановлена потерянная кавычка в досье на Кая Лена, убраны лишние кавычки в двух новостных заметках, выправлено «Аттический Траверс».

### Что нового в 1.2

Версия целиком про вычитку: новых модов не добавилось, зато выправлено всё, что нашлось при сплошной проверке.

**Окна настроек больше не разговаривают с игроком.** Описание настройки теперь говорит, что делает опция, а не что сделать человеку: «Убедись, что…» → «Стоит проверить, что…», «Задай…» → «Задает…», «Настрой письма…» → «Сортирует письма…». Выправлено 43 описания в EGM, Project Variety, Community Patch и Apartment Additions. В письмах и репликах персонажей обращения сохранены — там так задумано авторами.

**Кавычки везде прямые,** как в официальной локализации. Заменены угловые «…» в 23 строках настроек и типографские „…“ в 12 строках.

**В новостях «Ежедневника Цербера» убраны кавычки в кавычках.** Статья целиком была взята в кавычки, и названия внутри — в такие же; читалось со спотыканием. Снято 337 лишних пар.

**Подписи в блоках данных о планетах приведены к игровым:** «Тяготение на поверхности» → «Сила тяжести», «Основание колонии» → «Дата основания колонии», «Сутки» → «Продолжительность суток». Выправлено 42 строки.

**Переведены варианты настройки «Танцовщицы клуба»** — раньше два из трёх были подписаны по-английски, и настройка выглядела непонятной.

**Мелочи, которые режут глаз:** латинская буква в слове «Силовая», пробел перед двоеточием, «1, 17 G» вместо «1,17 G», лишние пробелы в 25 строках, пустые строки из одного пробела, оборванные переносы в конце 72 строк. В титрах убраны кавычки, которые туда попали при переносе, и возвращены адреса в угловых скобках в досье на Кая Лена.

### Состав

| Компонент | Мод | Версия мода | Строк |
|---|---|---|---:|
| `EGM` | Expanded Galaxy Mod + Squadmate Pack | 1.0.6 | 2 841 |
| `ProjectVariety` | Project Variety (+ `DLC_Shared`) | 0.7 | 2 976 |
| `Spectre` | Spectre Expansion Mod | 1.2.1 | 1 412 |
| `CommunityPatch` | LE3 Community Patch | 1.7.9 | 169 |
| `AppearanceModMenu` | Appearance Modification Menu | 2.2 | 161 |
| `ApartmentAdditions` | Apartment Additions | 1.0 | 53 |
| `Hairstyles` | More Hair for Femshep 1.1, Morning's Hairstyles 1.4.4 / PT2 1.3.1 / PT3 1.3.3, Morning's Versatile 1.0.3 | — | 137 |

### Мужской и женский Шепард

Письма и реплики, обращённые к Шепард, по-русски требуют рода, поэтому перевод собирается в двух вариантах. В окне установщика есть переключатель **Шепард: женский / мужской** (по умолчанию женский), у `install.ps1` — ключ `-Male`.

### Установка

Ниже, в разделе **Assets**, нужно скачать один файл — **`ME3LE-Russian-Mods-v1.2.1-full.zip`** (тот, в имени которого есть `full`). Распаковать его в любую папку и запустить **`ME3LE-Русификатор-модов.exe`**. Программа сама находит игру и показывает список модов с галочками; там же выбирается пол Шепард. Остаётся нажать «Установить». Откат — кнопкой «Удалить перевод» в том же окне.

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

### What's new in 1.2.1

Every settings screen was proofread line by line. Descriptions now answer what the mod does rather than telling the player what to do: the Community Patch labels match the rest of the pack, the journal objectives follow the game's own wording, and the Apartment Additions descriptions explain the setting instead of instructing. Mistakes in the mods themselves are fixed too — one option showed "enabled" for both states, another had its two states swapped, and two labels did not match their descriptions. Unclear options were made clear: "Club Dancers" now says what is being chosen, and the Miranda camera options say whose shots they restore.

### What's new in 1.2

A proofreading release — no new mods, but everything a full pass turned up has been fixed.

**Settings screens no longer address the player.** Option descriptions now say what the option does rather than what to do: 43 descriptions reworded across EGM, Project Variety, Community Patch and Apartment Additions. Characters' letters and lines keep their forms of address, as the authors intended.

**Quotation marks are straight everywhere**, matching the official localisation: 23 strings with guillemets and 12 with typographic quotes fixed.

**Cerberus Daily News no longer has quotes inside quotes** — 337 stray pairs removed.

**Planet data labels matched to the game's own wording** in 42 strings.

**The "Club Dancers" options are translated** — two of the three used to be labelled in English.

**Small things:** a Latin letter inside a Russian word, a space before a colon, stray double spaces in 25 strings, blank lines made of a single space, trailing line breaks in 72 strings, stray quotes in the credits, and the angle-bracketed addresses restored in Kai Leng's dossier.

**Download one file:** `ME3LE-Russian-Mods-v1.2.1-full.zip` (the one with `full` in its name). Extract it, run `ME3LE-Русификатор-модов.exe` — the window has an English switch — tick the components, pick Shepard's gender, click Install. Apply after all other mods. Step-by-step guide: [README.en.md](https://github.com/Stepan-Pimenov/mass-effect-le3-mods-russian-translation/blob/main/README.en.md#installation).

Tested on `MassEffect3.exe` 2.0.0.0, mod feature level 137, Windows 11 25H2. The installer needs .NET Framework 4.x (bundled with Windows 10/11).
