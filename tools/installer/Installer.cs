// Установщик русификатора модов Mass Effect 3 Legendary Edition.
// Собирается штатным компилятором .NET Framework (csc.exe), внешних зависимостей нет.
// Сборка: tools/build_installer.ps1

using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using Microsoft.Win32;
using System.Windows.Forms;

namespace Le3RuInstaller
{
    // ------------------------------------------------------------------ строки
    internal static class Str
    {
        public static bool En = false;

        static string P(string ru, string en) { return En ? en : ru; }

        public static string Title { get { return P("Русификатор модов Mass Effect 3 Legendary Edition",
                                                    "Russian translation for Mass Effect 3 Legendary Edition mods"); } }
        public static string GameLabel { get { return P("Папка с игрой:", "Game folder:"); } }
        public static string Browse { get { return P("Обзор…", "Browse…"); } }
        public static string BrowseHint { get { return P("Выберите папку Mass Effect Legendary Edition",
                                                        "Select the Mass Effect Legendary Edition folder"); } }
        public static string Components { get { return P("Что перевести:", "What to translate:"); } }
        public static string Install { get { return P("Установить", "Install"); } }
        public static string Uninstall { get { return P("Удалить перевод", "Uninstall"); } }
        public static string Close { get { return P("Закрыть", "Close"); } }
        public static string SelectAll { get { return P("Отметить все", "Select all"); } }
        public static string NotInstalled { get { return P("мод не установлен", "mod not installed"); } }
        public static string NoDist { get { return P("Рядом с программой нет папки dist. Нужно распаковать архив целиком.",
                                                     "The dist folder is missing next to the program. Extract the whole archive."); } }
        public static string BadGame { get { return P("В этой папке нет Game\\ME3\\BioGame\\DLC. Укажите корень игры.",
                                                      "There is no Game\\ME3\\BioGame\\DLC here. Point to the game root."); } }
        public static string GameNotFound { get { return P("Игра не найдена автоматически — укажите папку вручную.",
                                                           "The game was not found automatically - select the folder manually."); } }
        public static string NothingChecked { get { return P("Не отмечено ни одного компонента.", "No components selected."); } }
        public static string NoMods { get { return P("Ни один из поддерживаемых модов не установлен.",
                                                     "None of the supported mods are installed."); } }
        public static string DoneInstall { get { return P("Готово. Установлено файлов: {0}", "Done. Files installed: {0}"); } }
        public static string DoneUninstall { get { return P("Готово. Затронуто файлов: {0}", "Done. Files touched: {0}"); } }
        public static string AfterInstall { get { return P("В игре должен быть выбран русский язык.",
                                                           "Make sure the game language is set to Russian."); } }
        public static string Backup { get { return P("сохранена копия", "backup saved"); } }
        public static string Restored { get { return P("восстановлен из копии", "restored from backup"); } }
        public static string Removed { get { return P("удалён", "removed"); } }
        public static string Error { get { return P("Ошибка: ", "Error: "); } }
        public static string ConfirmUninstall { get { return P("Убрать перевод у отмеченных модов и вернуть их английский текст?",
                                                               "Remove the translation from the selected mods and restore their English text?"); } }
        public static string ShepardLabel { get { return P("Шепард:", "Shepard:"); } }
        public static string ShepardF { get { return P("женский", "female"); } }
        public static string ShepardM { get { return P("мужской", "male"); } }
        public static string VariantF { get { return P("Вариант перевода: женский Шепард.", "Translation variant: female Shepard."); } }
        public static string VariantM { get { return P("Вариант перевода: мужской Шепард.", "Translation variant: male Shepard."); } }
    }

    // ------------------------------------------------------------- компоненты
    internal class Component
    {
        public string Id;
        public string TitleRu;
        public string TitleEn;
        public List<string> DlcFolders = new List<string>();
        public List<string> Files = new List<string>();   // пути относительно папки компонента
        public bool Present;

        public string Display
        {
            get
            {
                string name = Str.En ? TitleEn : TitleRu;
                return Present ? name : name + "  (" + Str.NotInstalled + ")";
            }
        }
    }

    internal static class Catalog
    {
        static readonly Dictionary<string, string[]> Names = new Dictionary<string, string[]>
        {
            { "EGM",                new[] { "Expanded Galaxy Mod (+ Squad Pack)", "Expanded Galaxy Mod (+ Squad Pack)" } },
            { "ProjectVariety",     new[] { "Project Variety", "Project Variety" } },
            { "Spectre",            new[] { "Spectre Expansion Mod", "Spectre Expansion Mod" } },
            { "CommunityPatch",     new[] { "LE3 Community Patch", "LE3 Community Patch" } },
            { "AppearanceModMenu",  new[] { "Appearance Mod Menu (меню внешности)", "Appearance Mod Menu" } },
            { "ApartmentAdditions", new[] { "Apartment Additions (квартира)", "Apartment Additions" } },
            { "Hairstyles",         new[] { "Причёски для Шепард (набор модов)", "Shepard hairstyle mods (bundle)" } },
        };

        public static List<Component> Load(string distRoot)
        {
            var list = new List<Component>();
            if (!Directory.Exists(distRoot)) return list;

            foreach (var dir in Directory.GetDirectories(distRoot).OrderBy(d => d))
            {
                string id = Path.GetFileName(dir);
                var c = new Component { Id = id };
                if (Names.ContainsKey(id)) { c.TitleRu = Names[id][0]; c.TitleEn = Names[id][1]; }
                else { c.TitleRu = id; c.TitleEn = id; }

                foreach (var sub in Directory.GetDirectories(dir))
                    c.DlcFolders.Add(Path.GetFileName(sub));

                foreach (var f in Directory.GetFiles(dir, "*_RUS.tlk", SearchOption.AllDirectories))
                    c.Files.Add(f.Substring(dir.Length).TrimStart('\\'));

                if (c.Files.Count > 0) list.Add(c);
            }
            // порядок как в каталоге, незнакомые — в конец
            var order = Names.Keys.ToList();
            return list.OrderBy(c => { int i = order.IndexOf(c.Id); return i < 0 ? 999 : i; }).ToList();
        }
    }

    // ----------------------------------------------------------------- логика
    internal static class Engine
    {
        public static bool IsGameRoot(string path)
        {
            if (string.IsNullOrWhiteSpace(path)) return false;
            try { return Directory.Exists(Path.Combine(path, @"Game\ME3\BioGame\DLC")); }
            catch { return false; }
        }

        public static string DlcRoot(string gameRoot)
        {
            return Path.Combine(gameRoot, @"Game\ME3\BioGame\DLC");
        }

        public static string FindGame()
        {
            var candidates = new List<string>();

            foreach (var key in new[] { @"SOFTWARE\WOW6432Node\BioWare\Mass Effect Legendary Edition",
                                        @"SOFTWARE\BioWare\Mass Effect Legendary Edition" })
                try
                {
                    using (var k = Registry.LocalMachine.OpenSubKey(key))
                        if (k != null)
                        {
                            var v = k.GetValue("Install Dir") as string;
                            if (!string.IsNullOrEmpty(v)) candidates.Add(v);
                        }
                }
                catch { }

            string steam = null;
            foreach (var key in new[] { @"SOFTWARE\WOW6432Node\Valve\Steam", @"SOFTWARE\Valve\Steam" })
                try
                {
                    using (var k = Registry.LocalMachine.OpenSubKey(key))
                        if (k != null) steam = steam ?? k.GetValue("InstallPath") as string;
                }
                catch { }

            if (!string.IsNullOrEmpty(steam))
            {
                string vdf = Path.Combine(steam, @"steamapps\libraryfolders.vdf");
                if (File.Exists(vdf))
                    try
                    {
                        foreach (Match m in Regex.Matches(File.ReadAllText(vdf), "\"path\"\\s*\"([^\"]+)\""))
                            candidates.Add(Path.Combine(m.Groups[1].Value.Replace(@"\\", @"\"),
                                                        @"steamapps\common\Mass Effect Legendary Edition"));
                    }
                    catch { }
                candidates.Add(Path.Combine(steam, @"steamapps\common\Mass Effect Legendary Edition"));
            }

            string[] tails =
            {
                @"SteamLibrary\steamapps\common\Mass Effect Legendary Edition",
                @"Program Files (x86)\Steam\steamapps\common\Mass Effect Legendary Edition",
                @"Program Files\EA Games\Mass Effect Legendary Edition",
                @"Program Files (x86)\EA Games\Mass Effect Legendary Edition",
                @"Program Files\Epic Games\MassEffectLegendaryEdition",
                @"Games\Mass Effect Legendary Edition",
            };
            foreach (var d in DriveInfo.GetDrives())
            {
                if (!d.IsReady) continue;
                foreach (var t in tails) candidates.Add(Path.Combine(d.RootDirectory.FullName, t));
            }

            foreach (var c in candidates)
                if (IsGameRoot(c)) return Path.GetFullPath(c);
            return null;
        }

        public static void MarkPresence(List<Component> comps, string gameRoot)
        {
            string dlc = DlcRoot(gameRoot);
            foreach (var c in comps)
                c.Present = c.DlcFolders.Any(f => Directory.Exists(Path.Combine(dlc, f)));
        }

        public static int Install(IEnumerable<Component> comps, string distRoot, string gameRoot,
                                  bool male, Action<string> log)
        {
            string dlc = DlcRoot(gameRoot);
            int n = 0;
            foreach (var c in comps)
            {
                string compDir = Path.Combine(distRoot, c.Id);
                foreach (var rel in c.Files)
                {
                    string target = Path.Combine(dlc, rel);
                    string dir = Path.GetDirectoryName(target);
                    if (!Directory.Exists(dir)) continue;      // мод не установлен — пропускаем

                    string bak = target + ".bak";
                    if (File.Exists(target) && !File.Exists(bak))
                    {
                        File.Copy(target, bak);
                        log("      " + Path.GetFileName(bak) + " — " + Str.Backup);
                    }
                    string source = Path.Combine(compDir, rel);
                    if (male)
                    {
                        string maleSrc = source.Substring(0, source.Length - 4) + ".male.tlk";
                        if (File.Exists(maleSrc)) source = maleSrc;
                    }
                    File.Copy(source, target, true);
                    log("  + " + rel);
                    n++;
                }
            }
            return n;
        }

        public static int Uninstall(IEnumerable<Component> comps, string distRoot, string gameRoot, Action<string> log)
        {
            string dlc = DlcRoot(gameRoot);
            int n = 0;
            foreach (var c in comps)
                foreach (var rel in c.Files)
                {
                    string target = Path.Combine(dlc, rel);
                    string bak = target + ".bak";
                    if (File.Exists(bak))
                    {
                        File.Copy(bak, target, true);
                        File.Delete(bak);
                        log("  ~ " + rel + " — " + Str.Restored);
                        n++;
                    }
                    else if (File.Exists(target))
                    {
                        File.Delete(target);
                        log("  - " + rel + " — " + Str.Removed);
                        n++;
                    }
                }
            return n;
        }
    }

    // ------------------------------------------------------------------- окно
    internal class MainForm : Form
    {
        readonly string _distRoot;
        List<Component> _comps;

        ComboBox _lang;
        Label _lblGame, _lblComp;
        TextBox _game;
        Button _browse, _install, _uninstall, _close;
        CheckedListBox _list;
        CheckBox _all;
        Label _lblShep;
        RadioButton _shepF, _shepM;
        TextBox _log;

        public MainForm(string distRoot)
        {
            _distRoot = distRoot;
            _comps = Catalog.Load(distRoot);

            Font = new Font("Segoe UI", 9f);
            StartPosition = FormStartPosition.CenterScreen;
            FormBorderStyle = FormBorderStyle.FixedSingle;
            MaximizeBox = false;
            ClientSize = new Size(660, 560);

            _lang = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Left = 570, Top = 12, Width = 70 };
            _lang.Items.AddRange(new object[] { "Русский", "English" });
            _lang.SelectedIndex = 0;
            _lang.SelectedIndexChanged += (s, e) => { Str.En = _lang.SelectedIndex == 1; Retext(); };

            _lblGame = new Label { Left = 14, Top = 16, Width = 540, AutoSize = true };
            _game = new TextBox { Left = 14, Top = 40, Width = 530, ReadOnly = false };
            _browse = new Button { Left = 552, Top = 38, Width = 88, Height = 26 };
            _browse.Click += (s, e) => BrowseGame();

            _lblComp = new Label { Left = 14, Top = 82, AutoSize = true };
            _list = new CheckedListBox
            {
                Left = 14, Top = 104, Width = 626, Height = 150,
                CheckOnClick = true, IntegralHeight = false, BorderStyle = BorderStyle.FixedSingle
            };
            _list.ItemCheck += (s, e) =>
            {
                if (!_comps[e.Index].Present) e.NewValue = CheckState.Unchecked;
            };

            _all = new CheckBox { Left = 14, Top = 262, AutoSize = true };
            _all.CheckedChanged += (s, e) =>
            {
                for (int i = 0; i < _comps.Count; i++)
                    if (_comps[i].Present) _list.SetItemChecked(i, _all.Checked);
            };

            _lblShep = new Label { Left = 286, Top = 263, AutoSize = true };
            _shepF = new RadioButton { Left = 352, Top = 261, Width = 100, Checked = true };
            _shepM = new RadioButton { Left = 456, Top = 261, Width = 100 };

            _install = new Button { Left = 14, Top = 292, Width = 150, Height = 32 };
            _install.Click += (s, e) => DoInstall();
            _uninstall = new Button { Left = 174, Top = 292, Width = 150, Height = 32 };
            _uninstall.Click += (s, e) => DoUninstall();
            _close = new Button { Left = 550, Top = 292, Width = 90, Height = 32 };
            _close.Click += (s, e) => Close();

            _log = new TextBox
            {
                Left = 14, Top = 336, Width = 626, Height = 210,
                Multiline = true, ReadOnly = true, ScrollBars = ScrollBars.Vertical,
                BackColor = SystemColors.Window, Font = new Font("Consolas", 8.5f)
            };

            Controls.AddRange(new Control[] { _lang, _lblGame, _game, _browse, _lblComp, _list,
                                              _all, _lblShep, _shepF, _shepM,
                                              _install, _uninstall, _close, _log });

            Retext();

            if (_comps.Count == 0)
            {
                Log(Str.NoDist);
                _install.Enabled = _uninstall.Enabled = false;
                return;
            }

            string found = Engine.FindGame();
            if (found != null) SetGame(found);
            else Log(Str.GameNotFound);
        }

        void Retext()
        {
            Text = Str.Title;
            _lblGame.Text = Str.GameLabel;
            _browse.Text = Str.Browse;
            _lblComp.Text = Str.Components;
            _all.Text = Str.SelectAll;
            _lblShep.Text = Str.ShepardLabel;
            _shepF.Text = Str.ShepardF;
            _shepM.Text = Str.ShepardM;
            _install.Text = Str.Install;
            _uninstall.Text = Str.Uninstall;
            _close.Text = Str.Close;

            var checks = new bool[_comps.Count];
            for (int i = 0; i < _list.Items.Count && i < checks.Length; i++) checks[i] = _list.GetItemChecked(i);
            _list.BeginUpdate();
            _list.Items.Clear();
            for (int i = 0; i < _comps.Count; i++) _list.Items.Add(_comps[i].Display, checks[i]);
            _list.EndUpdate();
        }

        void SetGame(string path)
        {
            _game.Text = path;
            Engine.MarkPresence(_comps, path);
            _list.BeginUpdate();
            _list.Items.Clear();
            foreach (var c in _comps) _list.Items.Add(c.Display, c.Present);
            _list.EndUpdate();
            _all.Checked = _comps.Any(c => c.Present);
            if (!_comps.Any(c => c.Present)) Log(Str.NoMods);
        }

        void BrowseGame()
        {
            using (var d = new FolderBrowserDialog { Description = Str.BrowseHint, ShowNewFolderButton = false })
            {
                if (Engine.IsGameRoot(_game.Text)) d.SelectedPath = _game.Text;
                if (d.ShowDialog(this) != DialogResult.OK) return;
                if (!Engine.IsGameRoot(d.SelectedPath))
                {
                    MessageBox.Show(this, Str.BadGame, Str.Title, MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
                SetGame(d.SelectedPath);
            }
        }

        List<Component> Checked()
        {
            var r = new List<Component>();
            for (int i = 0; i < _comps.Count; i++)
                if (_list.GetItemChecked(i) && _comps[i].Present) r.Add(_comps[i]);
            return r;
        }

        void Log(string s) { _log.AppendText(s + Environment.NewLine); }

        bool Ready()
        {
            if (!Engine.IsGameRoot(_game.Text))
            {
                MessageBox.Show(this, Str.BadGame, Str.Title, MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }
            if (Checked().Count == 0)
            {
                MessageBox.Show(this, Str.NothingChecked, Str.Title, MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }
            return true;
        }

        void DoInstall()
        {
            if (!Ready()) return;
            try
            {
                _log.Clear();
                int n = Engine.Install(Checked(), _distRoot, _game.Text, _shepM.Checked, Log);
                Log("");
                Log(string.Format(Str.DoneInstall, n));
                Log(_shepM.Checked ? Str.VariantM : Str.VariantF);
                Log(Str.AfterInstall);
            }
            catch (Exception ex)
            {
                Log(Str.Error + ex.Message);
                MessageBox.Show(this, Str.Error + ex.Message, Str.Title, MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        void DoUninstall()
        {
            if (!Ready()) return;
            if (MessageBox.Show(this, Str.ConfirmUninstall, Str.Title,
                                MessageBoxButtons.YesNo, MessageBoxIcon.Question) != DialogResult.Yes) return;
            try
            {
                _log.Clear();
                int n = Engine.Uninstall(Checked(), _distRoot, _game.Text, Log);
                Log("");
                Log(string.Format(Str.DoneUninstall, n));
            }
            catch (Exception ex)
            {
                Log(Str.Error + ex.Message);
                MessageBox.Show(this, Str.Error + ex.Message, Str.Title, MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }

    // ------------------------------------------------------------------ вход
    internal static class Program
    {
        // Программа собрана как оконная, поэтому для режима -check консоль
        // родительского процесса приходится подключать вручную.
        [System.Runtime.InteropServices.DllImport("kernel32.dll")]
        static extern bool AttachConsole(int processId);

        [STAThread]
        static int Main(string[] args)
        {
            string exeDir = Path.GetDirectoryName(Application.ExecutablePath);
            string dist = Path.Combine(exeDir, "dist");

            // Консольный режим для автоматизации и проверки: -check [путь к игре]
            if (args.Length > 0 && args[0] == "-check")
            {
                AttachConsole(-1);
                var comps = Catalog.Load(dist);
                string game = args.Length > 1 ? args[1] : Engine.FindGame();
                Console.WriteLine("dist: " + dist + "  (" + comps.Count + " компонентов)");
                Console.WriteLine("игра: " + (game ?? "не найдена"));
                if (game != null)
                {
                    Engine.MarkPresence(comps, game);
                    foreach (var c in comps)
                        Console.WriteLine(string.Format("  [{0}] {1} — файлов {2}",
                            c.Present ? "x" : " ", c.Id, c.Files.Count));
                }
                return 0;
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm(dist));
            return 0;
        }
    }
}
