using System.Security.Cryptography;
using System.Linq;

namespace WinFormsApp6
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            LoadLogo();
        }

        private void LoadLogo()
        {
            try
            {
                string path = System.IO.Path.Combine(AppContext.BaseDirectory, "logo1.png");
                if (System.IO.File.Exists(path))
                    pictureBoxLogo.Image = Image.FromFile(path);
            }
            catch { }
        }

        private void buttonGenerate_Click(object sender, EventArgs e)
        {
            if (!cbUpper.Checked && !cbLower.Checked && !cbDigits.Checked && !cbSymbols.Checked)
            {
                MessageBox.Show("Выберите хотя бы один набор символов.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            int length = (int)numericUpDownLength.Value;
            textBox1.Text = GeneratePassword(
                length,
                cbUpper.Checked,
                cbLower.Checked,
                cbDigits.Checked,
                cbSymbols.Checked,
                cbExclude.Checked);
        }

        private void buttonCopy_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(textBox1.Text))
            {
                MessageBox.Show("Сначала сгенерируйте пароль.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            Clipboard.SetText(textBox1.Text);
            MessageBox.Show("Пароль скопирован в буфер обмена.", "Готово",
                MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            UpdateStrength();
        }

        private void UpdateStrength()
        {
            if (string.IsNullOrEmpty(textBox1.Text))
            {
                progressBarStrength.Value = 0;
                labelStrength.Text = "—";
                labelStrength.ForeColor = Color.Cornsilk;
                return;
            }

            var (score, label, color, _) = EvaluateStrength(textBox1.Text);
            progressBarStrength.Value = Math.Max(0, Math.Min(100, score));
            labelStrength.Text = label + " (" + score + "%)";
            labelStrength.ForeColor = color switch
            {
                "danger" => Color.Firebrick,
                "warn" => Color.Goldenrod,
                _ => Color.LightGreen,
            };
        }

        public static string GeneratePassword(
            int length = 16,
            bool useUpper = true,
            bool useLower = true,
            bool useDigits = true,
            bool useSymbols = true,
            bool excludeSimilar = false)
        {
            if (length < 4 || length > 64)
                throw new ArgumentException("Длина пароля должна быть от 4 до 64 символов.");

            List<string> pools = new List<string>();

            string lower = excludeSimilar
                ? "abcdefghijkmnopqrstuvwxyz"      // без l
                : "abcdefghijklmnopqrstuvwxyz";

            string upper = excludeSimilar
                ? "ABCDEFGHJKLMNPQRSTUVWXYZ"       // без I и O
                : "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

            string digits = excludeSimilar
                ? "234789"                         // без 0,1,5,6
                : "0123456789";

            string symbols = "!@#$%^&*()-_=+[]{};:,.?/";

            if (useLower)
                pools.Add(lower);
            if (useUpper)
                pools.Add(upper);
            if (useDigits)
                pools.Add(digits);
            if (useSymbols)
                pools.Add(symbols);

            if (pools.Count == 0)
                throw new ArgumentException("Выберите хотя бы один набор символов.");

            List<char> chars = new List<char>();

            // Гарантируем хотя бы один символ из каждого выбранного набора
            foreach (string pool in pools)
            {
                chars.Add(pool[RandomNumberGenerator.GetInt32(pool.Length)]);
            }

            string allChars = string.Concat(pools);

            while (chars.Count < length)
            {
                chars.Add(allChars[RandomNumberGenerator.GetInt32(allChars.Length)]);
            }

            // Перемешиваем символы (Fisher-Yates)
            for (int i = chars.Count - 1; i > 0; i--)
            {
                int j = RandomNumberGenerator.GetInt32(i + 1);
                (chars[i], chars[j]) = (chars[j], chars[i]);
            }

            return new string(chars.ToArray());
        }

        public static (int Score, string Label, string Color,
                       Dictionary<string, bool> Criteria)
            EvaluateStrength(string password)
        {
            if (string.IsNullOrEmpty(password))
                throw new ArgumentException("Введите пароль для проверки.");

            var criteria = new Dictionary<string, bool>
            {
                { "Не менее 8 символов", password.Length >= 8 },
                { "Не менее 12 символов", password.Length >= 12 },
                { "Строчные буквы (a-z)", password.Any(char.IsLower) },
                { "Прописные буквы (A-Z)", password.Any(char.IsUpper) },
                { "Цифры (0-9)", password.Any(char.IsDigit) },
                { "Спецсимволы (!@#$)", password.Any(c => !char.IsLetterOrDigit(c)) }
            };

            int score = (int)((double)criteria.Values.Count(v => v) / criteria.Count * 100);

            string label;
            string color;

            if (score <= 33)
            {
                label = "Слабый";
                color = "danger";
            }
            else if (score <= 66)
            {
                label = "Средний";
                color = "warn";
            }
            else if (score < 100)
            {
                label = "Надёжный";
                color = "accent";
            }
            else
            {
                label = "Отличный";
                color = "accent";
            }

            return (score, label, color, criteria);
        }
    }
}
