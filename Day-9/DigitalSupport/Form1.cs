using System.IO;

namespace WinFormsApp7
{
    public partial class Form1 : Form
    {
        private readonly string dataFile =
            Path.Combine(AppContext.BaseDirectory, "data.txt");

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            dataGridView1.DefaultCellStyle.ForeColor = Color.Black;
            dataGridView1.DefaultCellStyle.BackColor = Color.White;
            dataGridView1.AllowUserToAddRows = false;
            dataGridView1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.ReadOnly = true;

            comboBox1.Items.Add("Новое");
            comboBox1.Items.Add("В работе");
            comboBox1.Items.Add("Закрыто");

            dataGridView1.ColumnCount = 4;
            dataGridView1.Columns[0].Name = "ФИО";
            dataGridView1.Columns[1].Name = "Проблема";
            dataGridView1.Columns[2].Name = "Статус";
            dataGridView1.Columns[3].Name = "Дата";

            LoadData();
        }

        private bool ValidateInput()
        {
            if (textBox1.Text.Trim().Length == 0)
            {
                MessageBox.Show("Введите ФИО пользователя.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }
            if (textBox2.Text.Trim().Length == 0)
            {
                MessageBox.Show("Введите описание проблемы.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }
            if (comboBox1.SelectedIndex < 0)
            {
                MessageBox.Show("Выберите статус обращения.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }
            return true;
        }

        private void ClearInputs()
        {
            textBox1.Text = "";
            textBox2.Text = "";
            comboBox1.SelectedIndex = -1;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ActiveControl = null;
            if (!ValidateInput())
                return;

            dataGridView1.Rows.Add(
                textBox1.Text.Trim(),
                textBox2.Text.Trim(),
                comboBox1.Text,
                dateTimePicker1.Value.ToShortDateString());

            SaveData();
            ClearInputs();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            ActiveControl = null;
            if (dataGridView1.CurrentRow == null || dataGridView1.CurrentRow.IsNewRow)
            {
                MessageBox.Show("Выберите запись в таблице для изменения.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            if (!ValidateInput())
                return;

            var row = dataGridView1.CurrentRow;
            row.Cells[0].Value = textBox1.Text.Trim();
            row.Cells[1].Value = textBox2.Text.Trim();
            row.Cells[2].Value = comboBox1.Text;
            row.Cells[3].Value = dateTimePicker1.Value.ToShortDateString();

            SaveData();
            ClearInputs();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ActiveControl = null;
            if (dataGridView1.CurrentRow != null && !dataGridView1.CurrentRow.IsNewRow)
            {
                dataGridView1.Rows.Remove(dataGridView1.CurrentRow);
                SaveData();
                ClearInputs();
            }
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            var row = dataGridView1.Rows[e.RowIndex];
            textBox1.Text = Convert.ToString(row.Cells[0].Value);
            textBox2.Text = Convert.ToString(row.Cells[1].Value);
            comboBox1.Text = Convert.ToString(row.Cells[2].Value);

            if (DateTime.TryParse(Convert.ToString(row.Cells[3].Value), out DateTime dt))
                dateTimePicker1.Value = dt;
        }

        private void SaveData()
        {
            using StreamWriter sw = new StreamWriter(dataFile, false);
            foreach (DataGridViewRow row in dataGridView1.Rows)
            {
                if (row.IsNewRow)
                    continue;

                sw.WriteLine(
                    Clean(row.Cells[0].Value) + ";" +
                    Clean(row.Cells[1].Value) + ";" +
                    Clean(row.Cells[2].Value) + ";" +
                    Clean(row.Cells[3].Value));
            }
        }

        private static string Clean(object? value)
        {
            // Убираем разделитель и переносы строк, чтобы не ломать CSV.
            string s = Convert.ToString(value) ?? "";
            return s.Replace(";", ",").Replace("\r", " ").Replace("\n", " ");
        }

        private void LoadData()
        {
            if (!File.Exists(dataFile))
                return;

            foreach (string line in File.ReadAllLines(dataFile))
            {
                if (string.IsNullOrWhiteSpace(line))
                    continue;

                string[] a = line.Split(';');
                dataGridView1.Rows.Add(
                    Field(a, 0),
                    Field(a, 1),
                    Field(a, 2),
                    Field(a, 3));
            }
        }

        private static string Field(string[] parts, int i)
        {
            return i < parts.Length ? parts[i] : "";
        }
    }
}
