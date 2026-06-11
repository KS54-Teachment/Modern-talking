using System.Collections.Generic;
using System.IO;

namespace CyberSecurityCenter
{
    public partial class MainForm : Form
    {
        private readonly List<Threat> _threats = new List<Threat>();
        private readonly List<Question> _questions = new List<Question>();
        private readonly List<RadioButton[]> _answerButtons = new List<RadioButton[]>();

        public MainForm()
        {
            InitializeComponent();
            LoadLogo();
            StyleButtons();
            LoadThreats();
            LoadRecommendations();
            BuildQuiz();
        }

        // ============ Общее ============
        private void LoadLogo()
        {
            try
            {
                string path = Path.Combine(AppContext.BaseDirectory, "logo1.png");
                if (File.Exists(path))
                    pictureBoxLogo.Image = Image.FromFile(path);
            }
            catch
            {
            }
        }

        private void StyleButtons()
        {
            StyleButton(buttonResetRecs);
            StyleButton(buttonCheck);
        }

        private void StyleButton(Button b)
        {
            b.FlatStyle = FlatStyle.Flat;
            b.BackColor = Color.RoyalBlue;
            b.ForeColor = Color.White;
            b.FlatAppearance.BorderColor = Color.Cornsilk;
            b.Font = new Font("Segoe UI Semibold", 9F);
            b.Cursor = Cursors.Hand;
            b.UseVisualStyleBackColor = false;
        }

        // ============ Справочник угроз ============
        private void LoadThreats()
        {
            _threats.Add(new Threat("Фишинг", "Высокий",
                "Мошенники рассылают поддельные письма, сообщения и сайты, имитирующие банки, госуслуги или известные сервисы, чтобы выманить логины, пароли и данные карт.",
                "Проверяйте адрес отправителя и ссылки, не вводите данные по ссылкам из писем, заходите на сайты вручную и включите двухфакторную аутентификацию."));

            _threats.Add(new Threat("Вредоносное ПО (вирусы)", "Высокий",
                "Программы, которые проникают на устройство и повреждают файлы, крадут данные или мешают работе системы. Распространяются через вложения, пиратские программы и флешки.",
                "Установите антивирус и регулярно его обновляйте, не скачивайте программы из непроверенных источников, обновляйте ОС и проверяйте флешки."));

            _threats.Add(new Threat("Программы-вымогатели (Ransomware)", "Критический",
                "Вредоносное ПО, которое шифрует файлы на компьютере и требует деньги за их расшифровку. Часто даже после оплаты данные не возвращают.",
                "Регулярно делайте резервные копии на отдельный носитель, не открывайте подозрительные вложения, обновляйте систему и не платите выкуп."));

            _threats.Add(new Threat("Социальная инженерия", "Высокий",
                "Психологические манипуляции: злоумышленники выдают себя за сотрудников банка, техподдержку или знакомых и давят на эмоции (страх, срочность), чтобы получить данные или деньги.",
                "Не сообщайте пароли и коды из СМС, не принимайте решения под давлением, перезванивайте в организацию по официальному номеру."));

            _threats.Add(new Threat("Слабые и повторяющиеся пароли", "Средний",
                "Простые пароли (123456, дата рождения) легко подбираются. Если один пароль используется везде, то при утечке одного сайта страдают все аккаунты.",
                "Используйте длинные (от 12 символов) уникальные пароли, менеджер паролей и двухфакторную аутентификацию."));

            _threats.Add(new Threat("Незащищённый публичный Wi-Fi", "Средний",
                "В открытых сетях (кафе, аэропорты) злоумышленник может перехватить трафик (атака «человек посередине») и увидеть логины и пароли.",
                "Не вводите важные данные в открытых сетях, используйте VPN или мобильный интернет для оплат и входа в банк."));

            _threats.Add(new Threat("Шпионское ПО (Spyware)", "Высокий",
                "Программы, которые скрыто следят за действиями пользователя: записывают нажатия клавиш, собирают пароли и личные данные.",
                "Скачивайте приложения только из официальных магазинов, проверяйте разрешения приложений и используйте антивирус."));

            _threats.Add(new Threat("Утечка персональных данных", "Высокий",
                "Утечки баз данных сервисов приводят к тому, что ваши данные (почта, телефон, пароли) попадают в руки злоумышленников и используются для взлома и спама.",
                "Используйте разные пароли, проверяйте утечки (например, через haveibeenpwned), не публикуйте лишние данные и настройте приватность."));

            foreach (var t in _threats)
                listBoxThreats.Items.Add(t.Name);

            if (listBoxThreats.Items.Count > 0)
                listBoxThreats.SelectedIndex = 0;
        }

        private void listBoxThreats_SelectedIndexChanged(object sender, EventArgs e)
        {
            int i = listBoxThreats.SelectedIndex;
            if (i < 0 || i >= _threats.Count)
                return;

            ShowThreat(_threats[i]);
        }

        private void ShowThreat(Threat t)
        {
            richTextBoxThreat.Clear();
            AppendText(t.Name, 14F, FontStyle.Bold, Color.RoyalBlue);
            AppendText("Уровень опасности: " + t.Level, 10F, FontStyle.Bold, LevelColor(t.Level));
            AppendText("", 5F, FontStyle.Regular, Color.Black);
            AppendText("Описание", 11F, FontStyle.Bold, Color.Black);
            AppendText(t.Description, 10.5F, FontStyle.Regular, Color.Black);
            AppendText("", 5F, FontStyle.Regular, Color.Black);
            AppendText("Как защититься", 11F, FontStyle.Bold, Color.Black);
            AppendText(t.Protection, 10.5F, FontStyle.Regular, Color.Black);
        }

        private void AppendText(string text, float size, FontStyle style, Color color)
        {
            richTextBoxThreat.SelectionStart = richTextBoxThreat.TextLength;
            richTextBoxThreat.SelectionLength = 0;
            richTextBoxThreat.SelectionColor = color;
            richTextBoxThreat.SelectionFont = new Font("Segoe UI", size, style);
            richTextBoxThreat.AppendText(text + Environment.NewLine);
        }

        private Color LevelColor(string level)
        {
            switch (level)
            {
                case "Критический": return Color.DarkRed;
                case "Высокий": return Color.Firebrick;
                case "Средний": return Color.DarkGoldenrod;
                default: return Color.DimGray;
            }
        }

        // ============ Рекомендации ============
        private void LoadRecommendations()
        {
            string[] recs =
            {
                "Использую сложные и уникальные пароли для разных сайтов",
                "Включил(а) двухфакторную аутентификацию (2FA)",
                "Регулярно обновляю операционную систему и программы",
                "Не открываю подозрительные ссылки и вложения",
                "Использую антивирус и брандмауэр",
                "Делаю резервные копии важных данных",
                "Проверяю адрес сайта (https и правильное доменное имя)",
                "Не ввожу личные данные в публичных сетях Wi-Fi / использую VPN",
                "Не сообщаю пароли и коды из СМС третьим лицам",
                "Настроил(а) приватность в социальных сетях"
            };

            checkedListBoxRecs.Items.AddRange(recs);
            UpdateProgress();
        }

        private void checkedListBoxRecs_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            // Состояние элемента обновляется после события, поэтому считаем через BeginInvoke.
            BeginInvoke(new Action(UpdateProgress));
        }

        private void UpdateProgress()
        {
            int done = checkedListBoxRecs.CheckedItems.Count;
            int total = checkedListBoxRecs.Items.Count;
            labelProgress.Text = "Соблюдается: " + done + " из " + total;
        }

        private void buttonResetRecs_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < checkedListBoxRecs.Items.Count; i++)
                checkedListBoxRecs.SetItemChecked(i, false);
            UpdateProgress();
        }

        // ============ Тест безопасности ============
        private void BuildQuiz()
        {
            _questions.Add(new Question("Что такое фишинг?",
                new[]
                {
                    "Вид компьютерного вируса",
                    "Выманивание данных через поддельные письма и сайты",
                    "Программа для резервного копирования",
                    "Способ ускорения интернета"
                }, 1));

            _questions.Add(new Question("Каким должен быть надёжный пароль?",
                new[]
                {
                    "1234 или дата рождения",
                    "Короткое слово из словаря",
                    "Длинный (от 12 символов), с буквами, цифрами и спецсимволами",
                    "Одинаковым на всех сайтах"
                }, 2));

            _questions.Add(new Question("Пришло письмо от «банка» с просьбой срочно перейти по ссылке и ввести данные. Что делать?",
                new[]
                {
                    "Сразу перейти и ввести данные",
                    "Перезвонить в банк по официальному номеру и не переходить по ссылке",
                    "Переслать письмо друзьям",
                    "Ответить на письмо своими данными"
                }, 1));

            _questions.Add(new Question("Зачем нужна двухфакторная аутентификация (2FA)?",
                new[]
                {
                    "Чтобы быстрее входить в аккаунт",
                    "Чтобы защитить аккаунт, даже если пароль украли",
                    "Чтобы не вводить пароль вообще",
                    "Это просто реклама"
                }, 1));

            _questions.Add(new Question("Можно ли использовать один пароль для всех сайтов?",
                new[]
                {
                    "Да, так удобнее",
                    "Нет, при утечке пострадают все аккаунты",
                    "Да, если он сложный",
                    "Только для почты"
                }, 1));

            _questions.Add(new Question("Что такое программа-вымогатель (ransomware)?",
                new[]
                {
                    "Программа для ускорения ПК",
                    "Вирус, который шифрует файлы и требует выкуп",
                    "Антивирус",
                    "Менеджер паролей"
                }, 1));

            _questions.Add(new Question("Безопасно ли вводить данные карты в открытой Wi-Fi сети кафе?",
                new[]
                {
                    "Да, это безопасно",
                    "Нет, лучше использовать мобильный интернет или VPN",
                    "Да, если сеть с паролем",
                    "Без разницы"
                }, 1));

            int number = 1;
            foreach (var q in _questions)
            {
                int boxWidth = flowQuiz.ClientSize.Width - 28;
                if (boxWidth < 200) boxWidth = 820;

                var gb = new GroupBox
                {
                    Text = number + ". " + q.Text,
                    ForeColor = Color.Cornsilk,
                    Font = new Font("Segoe UI Semibold", 10F),
                    Width = boxWidth,
                    AutoSize = false,
                    Margin = new Padding(3, 3, 3, 12)
                };

                int y = 30;
                var rbs = new RadioButton[q.Options.Length];
                for (int i = 0; i < q.Options.Length; i++)
                {
                    var rb = new RadioButton
                    {
                        Text = q.Options[i],
                        ForeColor = Color.White,
                        Font = new Font("Segoe UI", 10F),
                        AutoSize = true,
                        Location = new Point(16, y),
                        MaximumSize = new Size(boxWidth - 36, 0)
                    };
                    gb.Controls.Add(rb);
                    rbs[i] = rb;
                    y += 30;
                }

                gb.Height = y + 10;
                _answerButtons.Add(rbs);
                flowQuiz.Controls.Add(gb);
                number++;
            }
        }

        private void buttonCheck_Click(object sender, EventArgs e)
        {
            int correct = 0;
            int answered = 0;

            for (int i = 0; i < _questions.Count; i++)
            {
                RadioButton[] rbs = _answerButtons[i];
                int selected = -1;
                for (int j = 0; j < rbs.Length; j++)
                {
                    if (rbs[j].Checked)
                    {
                        selected = j;
                        break;
                    }
                }

                if (selected >= 0) answered++;
                if (selected == _questions[i].Correct) correct++;
            }

            if (answered < _questions.Count)
            {
                var dr = MessageBox.Show(
                    "Вы ответили не на все вопросы. Показать результат всё равно?",
                    "Тест безопасности",
                    MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (dr == DialogResult.No)
                    return;
            }

            int total = _questions.Count;
            int percent = (int)Math.Round(correct * 100.0 / total);

            string verdict;
            Color color;
            if (percent < 50)
            {
                verdict = "Низкий уровень — стоит подтянуть знания.";
                color = Color.Firebrick;
            }
            else if (percent < 75)
            {
                verdict = "Средний уровень — есть над чем поработать.";
                color = Color.Gold;
            }
            else if (percent < 100)
            {
                verdict = "Хороший уровень безопасности.";
                color = Color.LightGreen;
            }
            else
            {
                verdict = "Отличный уровень! Вы хорошо защищены.";
                color = Color.LightGreen;
            }

            labelResult.ForeColor = color;
            labelResult.Text = "Результат: " + correct + " из " + total + " (" + percent + "%). " + verdict;
        }

        // ============ Модели данных ============
        private class Threat
        {
            public string Name { get; }
            public string Level { get; }
            public string Description { get; }
            public string Protection { get; }

            public Threat(string name, string level, string description, string protection)
            {
                Name = name;
                Level = level;
                Description = description;
                Protection = protection;
            }
        }

        private class Question
        {
            public string Text { get; }
            public string[] Options { get; }
            public int Correct { get; }

            public Question(string text, string[] options, int correct)
            {
                Text = text;
                Options = options;
                Correct = correct;
            }
        }
    }
}
