"""
Цветовая палитра и шрифты приложения.
Стиль: тёмная тема в духе massgrave.dev — почти чёрный фон и мятно-бирюзовый акцент.
"""

# --- Палитра -----------------------------------------------------------------
BG = "#0a0e13"          # основной фон окна
SIDEBAR = "#0d1219"     # фон боковой панели
CARD = "#111a23"        # карточки
CARD_HOVER = "#16212c"  # карточка при наведении
ELEV = "#172230"        # приподнятый элемент
BORDER = "#1e2b38"      # границы

ACCENT = "#2dd4bf"      # мятно-бирюзовый акцент
ACCENT_HOVER = "#14b8a6"
ACCENT_DIM = "#0f766e"
MINT = "#5eead4"

TEXT = "#e6edf3"        # основной текст
TEXT_SOFT = "#c9d4df"
MUTED = "#7d8896"       # второстепенный текст
FAINT = "#4b5563"

GREEN = "#22c55e"
YELLOW = "#eab308"
ORANGE = "#f97316"
RED = "#ef4444"
BLUE = "#38bdf8"

# Цвета уровней надёжности пароля
STRENGTH_COLORS = {
    "empty": MUTED,
    "very_weak": RED,
    "weak": ORANGE,
    "medium": YELLOW,
    "good": "#84cc16",
    "strong": GREEN,
    "excellent": ACCENT,
}

# Цвета статусов обращений
STATUS_COLORS = {
    "Новое": BLUE,
    "В работе": YELLOW,
    "Решено": GREEN,
}

# --- Шрифты -----------------------------------------------------------------
# CTkFont нужно создавать ПОСЛЕ создания корневого окна, поэтому
# здесь храним только параметры, а объекты строятся в Fonts.build().
UI_FAMILY = "Segoe UI"      # есть на Windows; иначе берётся системный шрифт
MONO_FAMILY = "Consolas"    # моноширинный для паролей/отчёта


class Fonts:
    """Набор шрифтов, создаётся после инициализации окна."""

    def __init__(self, ctk):
        self.display = ctk.CTkFont(UI_FAMILY, size=30, weight="bold")
        self.h1 = ctk.CTkFont(UI_FAMILY, size=24, weight="bold")
        self.h2 = ctk.CTkFont(UI_FAMILY, size=18, weight="bold")
        self.h3 = ctk.CTkFont(UI_FAMILY, size=15, weight="bold")
        self.body = ctk.CTkFont(UI_FAMILY, size=14)
        self.body_bold = ctk.CTkFont(UI_FAMILY, size=14, weight="bold")
        self.small = ctk.CTkFont(UI_FAMILY, size=12)
        self.tiny = ctk.CTkFont(UI_FAMILY, size=11)
        self.nav = ctk.CTkFont(UI_FAMILY, size=14, weight="bold")
        self.mono = ctk.CTkFont(MONO_FAMILY, size=20, weight="bold")
        self.mono_small = ctk.CTkFont(MONO_FAMILY, size=12)
