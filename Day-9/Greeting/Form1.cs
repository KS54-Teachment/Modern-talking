namespace WinFormsApp4
{
    public partial class MyApp : Form
    {
        public MyApp()
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

        private void button1_Click(object sender, EventArgs e)
        {
            string name = textBox1.Text.Trim();
            if (name.Length == 0)
            {
                MessageBox.Show("Введите имя.", "Внимание",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            label1.Text = "Здравствуйте, " + name + "!";
        }
    }
}
