using System.Data;

namespace WinFormsApp5
{
    public partial class Form1 : Form
    {
        public string res = "";

        public Form1()
        {
            InitializeComponent();
            LoadLogo();
            StyleButtons();
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

        private void StyleButtons()
        {
            foreach (Control c in groupBox1.Controls)
            {
                if (c is Button b)
                {
                    b.FlatStyle = FlatStyle.Flat;
                    b.ForeColor = Color.White;
                    b.BackColor = Color.RoyalBlue;
                    b.Font = new Font("Segoe UI Semibold", 12F);
                    b.Cursor = Cursors.Hand;
                    b.UseVisualStyleBackColor = false;
                    b.FlatAppearance.BorderColor = Color.Cornsilk;
                }
            }
            button16.BackColor = Color.Firebrick; // C
            button17.BackColor = Color.SeaGreen;  // =
        }

        private void AppendInput(string s)
        {
            if (textBox1.Text == "Делить на ноль нельзя!" || textBox1.Text == "Ошибка")
                textBox1.Text = "";
            textBox1.Text += s;
        }

        private void button1_Click(object sender, EventArgs e) => AppendInput(button1.Text);
        private void button2_Click(object sender, EventArgs e) => AppendInput(button2.Text);
        private void button3_Click(object sender, EventArgs e) => AppendInput(button3.Text);
        private void button4_Click(object sender, EventArgs e) => AppendInput(button4.Text);
        private void button5_Click(object sender, EventArgs e) => AppendInput(button5.Text);
        private void button6_Click(object sender, EventArgs e) => AppendInput(button6.Text);
        private void button7_Click(object sender, EventArgs e) => AppendInput(button7.Text);
        private void button8_Click(object sender, EventArgs e) => AppendInput(button8.Text);
        private void button9_Click(object sender, EventArgs e) => AppendInput(button9.Text);
        private void button10_Click(object sender, EventArgs e) => AppendInput(button10.Text);
        private void button11_Click(object sender, EventArgs e) => AppendInput(button11.Text);
        private void button12_Click(object sender, EventArgs e) => AppendInput(button12.Text);
        private void button13_Click(object sender, EventArgs e) => AppendInput(button13.Text);
        private void button14_Click(object sender, EventArgs e) => AppendInput(button14.Text);
        private void button15_Click(object sender, EventArgs e) => AppendInput(button15.Text);

        private void button16_Click(object sender, EventArgs e)
        {
            textBox1.Text = "";
        }

        private void button17_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(textBox1.Text))
                return;
            try
            {
                object computed = new DataTable().Compute(textBox1.Text, null);
                res = Convert.ToString(computed) ?? "";
                if (double.TryParse(res, out double d) && (double.IsInfinity(d) || double.IsNaN(d)))
                    textBox1.Text = "Делить на ноль нельзя!";
                else
                    textBox1.Text = res;
            }
            catch (DivideByZeroException)
            {
                textBox1.Text = "Делить на ноль нельзя!";
            }
            catch
            {
                textBox1.Text = "Ошибка";
            }
        }
    }
}
