"""
ЦифроКуратор — бизнес-логика (без графического интерфейса).
Команда Modern Talking.

Здесь собрана вся "начинка" приложения: генерация паролей, база обращений,
консультант, формирование отчёта и справочник по кибербезопасности.
Интерфейс (app.py / views.py) только вызывает эти функции, поэтому логику
можно тестировать отдельно от GUI.
"""

from __future__ import annotations

import getpass
import json
import os
import secrets
import string
import sys
import datetime as dt
from dataclasses import dataclass, asdict, field

# --- Пути к файлам данных -------------------------------------------------
# В обычном запуске — рядом с модулем; в собранном .exe (PyInstaller)
# — рядом с исполняемым файлом, чтобы обращения/настройки/отчёт
# сохранялись рядом с программой, а не во временной папке.
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPEALS_FILE = os.path.join(BASE_DIR, "appeals.json")
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

TEAM_NAME = "Modern Talking"
APP_NAME = "DigitalSupportV2"
APP_VERSION = "1.0"

# Состав команды: (имя, роль)
TEAM = [
    ("Комиссаров Илья", "Лидер команды"),
    ("Госани Айдар", "Технический специалист"),
    ("Чернов Матвей", "Специалист по информационной безопасности"),
    ("Яноха Денис", "Консультант"),
    ("Чирков Костя", "Документатор приложения"),
]

STATUSES = ["Новое", "В работе", "Решено"]


# ===========================================================================
# Задание 2. Консультант — база типовых проблем и решений
# ===========================================================================
CONSULTANT_DB = {
    "Забыл пароль": (
        "Восстановить пароль через электронную почту или телефон.",
        [
            "Откройте страницу входа и нажмите «Забыли пароль?».",
            "Введите e-mail или телефон, привязанный к аккаунту.",
            "Перейдите по ссылке из письма и задайте новый надёжный пароль.",
        ],
    ),
    "Не приходит SMS-код": (
        "Проверить сигнал сети и запросить код повторно.",
        [
            "Убедитесь, что телефон в зоне действия сети.",
            "Подождите 1-2 минуты и запросите код ещё раз.",
            "Если код не приходит — используйте вход по e-mail.",
        ],
    ),
    "Не открывается Госуслуги": (
        "Очистить кэш браузера и проверить подключение к интернету.",
        [
            "Проверьте интернет-соединение.",
            "Очистите кэш и cookie браузера.",
            "Попробуйте другой браузер или мобильное приложение.",
        ],
    ),
    "Подозрение на мошенничество": (
        "Не передавать данные, сменить пароли и обратиться в банк.",
        [
            "Никому не сообщайте коды из SMS и пароли.",
            "Срочно смените пароли на важных сервисах.",
            "Позвоните в банк по номеру с обратной стороны карты.",
        ],
    ),
    "Не приходит электронная почта": (
        "Проверить папку «Спам» и настройки фильтров.",
        [
            "Загляните в папки «Спам» и «Промоакции».",
            "Проверьте правильность адреса отправителя.",
            "Добавьте отправителя в список доверенных.",
        ],
    ),
    "Заблокирован аккаунт": (
        "Пройти процедуру восстановления и подтвердить личность.",
        [
            "Воспользуйтесь формой восстановления доступа.",
            "Подготовьте документы для подтверждения личности.",
            "При необходимости обратитесь в поддержку сервиса.",
        ],
    ),
}


def consultant_problems() -> list[str]:
    """Список всех известных проблем."""
    return list(CONSULTANT_DB.keys())


def consultant_answer(problem: str):
    """Вернуть (решение, [рекомендации]) для выбранной проблемы."""
    return CONSULTANT_DB.get(
        problem,
        (
            "Проблема не найдена в базе. Зафиксируйте обращение вручную.",
            ["Уточните детали у пользователя.", "Создайте новое обращение в журнале."],
        ),
    )


# ===========================================================================
# Задание 3. Генератор паролей + проверка надёжности
# ===========================================================================
AMBIGUOUS = "Il1O0"  # похожие символы, которые лучше исключать


def generate_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    avoid_ambiguous: bool = False,
) -> str:
    """Сгенерировать криптостойкий пароль из выбранных наборов символов."""
    length = max(4, min(int(length), 64))
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_special:
        pools.append("!@#$%^&*()-_=+[]{};:,.?/")
    if not pools:
        pools.append(string.ascii_letters)

    if avoid_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) or pool for pool in pools]

    # Гарантируем хотя бы один символ из каждого выбранного набора
    password_chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_chars))

    # Перемешиваем криптостойким образом
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars[:length])


# ---------------------------------------------------------------------------
# "Умная" оценка надёжности пароля (по мотивам zxcvbn).
# Вместо простого подсчёта критериев мы оцениваем реальное число попыток
# подбора: ищем словарные пароли, последовательности, клавиатурные
# дорожки, повторы и leet-замены, а остаток считаем честным перебором.
# ---------------------------------------------------------------------------

# Фрагмент топ-списков самых популярных паролей из утечек (по возрастанию ранга).
COMMON_PASSWORDS = [
    "password", "123456", "123456789", "12345678", "12345", "qwerty",
    "qwerty123", "qwerty1234", "1234567890", "1234567", "111111", "000000",
    "123123", "abc123", "password1", "passw0rd", "iloveyou", "admin",
    "welcome", "monkey", "dragon", "letmein", "login", "princess", "master",
    "hello", "freedom", "whatever", "qazwsx", "trustno1", "superman",
    "football", "baseball", "starwars", "ninja", "azerty", "zxcvbn",
    "qwertyuiop", "qwe123", "1q2w3e", "1q2w3e4r", "qweqwe", "123qwe",
    "пароль", "йцукен", "привет", "люблю", "россия",
]
# Частые слова-основы (их подбирают по словарю, пусть и чуть дольше).
COMMON_WORDS = [
    "password", "qwerty", "admin", "welcome", "love", "god", "money",
    "test", "user", "root", "secret", "summer", "winter", "spring",
    "autumn", "january", "company", "google", "apple", "samsung", "moscow",
    "russia", "name", "phone", "email", "computer", "internet", "system",
    "server", "hello", "dragon", "monkey", "master", "shadow", "football",
]
# Раскладки клавиатуры — для поиска "клавиатурных дорожек".
_KEYBOARD_ROWS = [
    "1234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "йцукенгшщзхъ", "фывапролджэ", "ячсмитьбю",
]
# Самые ходовые leet-замены (символ -> буква).
_LEET = {"@": "a", "4": "a", "8": "b", "(": "c", "3": "e", "6": "g",
         "1": "l", "0": "o", "$": "s", "5": "s", "7": "t", "+": "t"}
# Скорость перебора при офлайн-атаке с быстрым хешированием (попыток/сек).
_GUESSES_PER_SECOND = 1e10


def _char_pool(password: str) -> int:
    """Размер алфавита для перебора (мощность набора символов)."""
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 33
    return max(pool, 1)


def _deleet(s: str) -> str:
    return "".join(_LEET.get(c, c) for c in s)


def _is_sequence(s: str) -> bool:
    """abc / cba / 123 / 321 — подряд идущие символы."""
    if len(s) < 3:
        return False
    deltas = {ord(s[i + 1]) - ord(s[i]) for i in range(len(s) - 1)}
    return deltas == {1} or deltas == {-1}


def _in_keyboard_row(s: str) -> bool:
    low = s.lower()
    if len(low) < 3:
        return False
    for row in _KEYBOARD_ROWS:
        if low in row or low[::-1] in row:
            return True
    return False


def _match_guesses(token: str, pool: int) -> float:
    """Оценка: сколько примерно попыток нужно для этого фрагмента."""
    low = token.lower()
    de = _deleet(low)
    # 1. Готовый пароль из словаря утечек — подбирается мгновенно
    for i, common in enumerate(COMMON_PASSWORDS):
        if low == common or de == common:
            return (i + 1) * 4.0
    # 2. Словарное слово (возможны вариации регистра/leet)
    for i, word in enumerate(COMMON_WORDS):
        if low == word or de == word:
            return (i + 1) * 30.0
    # 3. Числовая/буквенная последовательность (1234, abcd)
    if _is_sequence(low):
        return float(max(len(low) * 12, 25))
    # 4. Клавиатурная дорожка (qwerty, asdf, йцукен)
    if _in_keyboard_row(low):
        return float(max(len(low) * 18, 30))
    # 5. Повтор одного символа (aaaa, 1111)
    if len(set(low)) == 1:
        return float(pool * len(low))
    # 6. Повтор короткого блока (abcabc, 121212)
    for unit in range(1, len(low) // 2 + 1):
        if len(low) % unit == 0 and low[:unit] * (len(low) // unit) == low:
            return _match_guesses(low[:unit], pool) * (len(low) // unit)
    # 7. Иначе — честный перебор по алфавиту
    return float(pool) ** len(token)


def _estimate_guesses(password: str) -> float:
    """Минимальное число попыток подбора (динамика по разбиениям, как в zxcvbn)."""
    n = len(password)
    pool = _char_pool(password)
    inf = float("inf")
    dp = [inf] * (n + 1)
    dp[0] = 1.0
    for k in range(1, n + 1):
        # вариант 1: очередной символ перебираем "в лоб"
        dp[k] = min(dp[k], dp[k - 1] * pool)
        # вариант 2: фрагмент-паттерн, заканчивающийся на позиции k
        for j in range(0, k - 1):
            cand = dp[j] * _match_guesses(password[j:k], pool)
            if cand < dp[k]:
                dp[k] = cand
    return max(dp[n], 1.0)


def _crack_time_text(seconds: float) -> str:
    """Человекопонятное время взлома."""
    minute, hour, day = 60, 3600, 86400
    month, year = day * 30, day * 365
    century = year * 100
    if seconds < 1:
        return "мгновенно"
    if seconds < minute:
        return f"{int(seconds)} сек."
    if seconds < hour:
        return f"{int(seconds // minute)} мин."
    if seconds < day:
        return f"{int(seconds // hour)} ч."
    if seconds < month:
        return f"{int(seconds // day)} дн."
    if seconds < year:
        return f"{int(seconds // month)} мес."
    if seconds < century:
        return f"{int(seconds // year)} лет"
    if seconds < century * 1000:
        return f"{int(seconds // century)} веков"
    return "практически невозможно"


def password_strength(password: str) -> dict:
    """Умная оценка надёжности пароля (по мотивам zxcvbn): учитывает
    словарные пароли, последовательности, клавиатурные дорожки, повторы
    и leet-замены, оценивая реальное число попыток подбора и время взлома."""
    if not password:
        return {"score": 0, "label": "Пусто", "percent": 0.0, "level": "empty",
                "guesses": 0, "crack_time": "—", "tips": ["Введите пароль."]}

    guesses = _estimate_guesses(password)
    seconds = guesses / _GUESSES_PER_SECOND
    crack = _crack_time_text(seconds)

    # Оценка 0..5 по числу попыток подбора (логарифмическая шкала)
    if guesses < 1e3:
        score = 0
    elif guesses < 1e6:
        score = 1
    elif guesses < 1e9:
        score = 2
    elif guesses < 1e12:
        score = 3
    elif guesses < 1e15:
        score = 4
    else:
        score = 5

    labels = {
        0: ("Очень слабый", "very_weak"),
        1: ("Слабый", "weak"),
        2: ("Средний", "medium"),
        3: ("Хороший", "good"),
        4: ("Сильный", "strong"),
        5: ("Отличный", "excellent"),
    }
    label, level = labels[score]

    # Содержательные подсказки на основе найденных слабостей
    tips = [f"⏱ Подбор перебором: ~{crack}"]
    low = password.lower()
    de = _deleet(low)
    if low in COMMON_PASSWORDS or de in COMMON_PASSWORDS:
        tips.append("Это один из самых популярных паролей — он есть в словарях утечек.")
    if any(_is_sequence(password[i:i + 4]) for i in range(max(len(password) - 3, 1))):
        tips.append("Уберите последовательности вроде 1234 или abcd.")
    if any(_in_keyboard_row(password[i:i + 4]) for i in range(max(len(password) - 3, 1))):
        tips.append("Уберите клавиатурные дорожки (qwerty, asdf, йцукен).")
    if any(password[i] == password[i + 1] == password[i + 2] for i in range(len(password) - 2)):
        tips.append("Избегайте повторов одного символа подряд.")
    if len(password) < 12:
        tips.append("Используйте не менее 12–16 символов.")
    classes = sum([any(c.islower() for c in password), any(c.isupper() for c in password),
                   any(c.isdigit() for c in password), any(not c.isalnum() for c in password)])
    if classes < 3:
        tips.append("Смешивайте буквы разных регистров, цифры и спецсимволы.")
    if score >= 4 and len(tips) == 1:
        tips.append("Надёжный пароль. Не используйте его повторно на разных сайтах.")

    return {
        "score": score,
        "label": label,
        "level": level,
        "percent": score / 5.0,
        "guesses": guesses,
        "crack_time": crack,
        "tips": tips,
    }


# ===========================================================================
# Задание 4. База обращений (с сохранением в JSON-файл)
# ===========================================================================
@dataclass
class Appeal:
    id: int
    name: str
    problem: str
    status: str = "Новое"
    created: str = field(default_factory=lambda: dt.datetime.now().strftime("%Y-%m-%d %H:%M"))


class AppealsStore:
    """Журнал обращений граждан. Хранит данные в appeals.json."""

    def __init__(self, path: str = APPEALS_FILE):
        self.path = path
        self.items: list[Appeal] = []
        self.load()

    def load(self) -> None:
        self.items = []
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for row in data:
                    self.items.append(Appeal(**row))
            except (json.JSONDecodeError, TypeError, ValueError):
                self.items = []

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(a) for a in self.items], f, ensure_ascii=False, indent=2)

    def _next_id(self) -> int:
        return (max((a.id for a in self.items), default=0)) + 1

    def add(self, name: str, problem: str, status: str = "Новое") -> Appeal:
        appeal = Appeal(id=self._next_id(), name=name.strip(), problem=problem.strip(), status=status)
        self.items.append(appeal)
        self.save()
        return appeal

    def delete(self, appeal_id: int) -> bool:
        before = len(self.items)
        self.items = [a for a in self.items if a.id != appeal_id]
        if len(self.items) != before:
            self.save()
            return True
        return False

    def update_status(self, appeal_id: int, status: str) -> bool:
        for a in self.items:
            if a.id == appeal_id:
                a.status = status
                self.save()
                return True
        return False

    def search(self, query: str) -> list[Appeal]:
        q = query.strip().lower()
        if not q:
            return list(self.items)
        return [
            a for a in self.items
            if q in a.name.lower() or q in a.problem.lower() or q in a.status.lower()
        ]

    def all(self) -> list[Appeal]:
        return list(self.items)

    def count_by_status(self, status: str) -> int:
        return sum(1 for a in self.items if a.status == status)


# ===========================================================================
# Задание 5. Формирование и сохранение отчёта report.txt
# ===========================================================================
def build_report(appeals: list[Appeal], team: str = TEAM_NAME) -> str:
    """Собрать текст отчёта о работе центра поддержки."""
    now = dt.datetime.now()
    solved = sum(1 for a in appeals if a.status == "Решено")
    lines = []
    lines.append("=" * 56)
    lines.append("  ОТЧЁТ ЦЕНТРА ЦИФРОВОЙ ПОДДЕРЖКИ")
    lines.append("=" * 56)
    lines.append(f"Команда:            {team}")
    lines.append(f"Дата формирования:  {now.strftime('%d.%m.%Y %H:%M')}")
    lines.append(f"Всего обращений:    {len(appeals)}")
    lines.append(f"Обработано (Решено): {solved}")
    lines.append("-" * 56)
    lines.append("Список обращений:")
    if not appeals:
        lines.append("  (обращений пока нет)")
    else:
        for i, a in enumerate(appeals, 1):
            lines.append(f"  {i}. [{a.status}] {a.name} — {a.problem} ({a.created})")
    lines.append("=" * 56)
    lines.append(f"Подготовлено приложением {APP_NAME} v{APP_VERSION}")
    return "\n".join(lines)


def save_report(appeals: list[Appeal], path: str = REPORT_FILE, team: str = TEAM_NAME) -> str:
    text = build_report(appeals, team)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# ===========================================================================
# Проект 6. Справочник по кибербезопасности
# ===========================================================================
SECURITY_KB = [
    ("Надёжные пароли", "Используйте пароли длиной 12+ символов с буквами, цифрами и спецсимволами. Не повторяйте пароли на разных сайтах."),
    ("Двухфакторная аутентификация", "Включайте 2FA везде, где можно. Даже при утечке пароля злоумышленник не войдёт без второго фактора."),
    ("Фишинг", "Проверяйте адрес сайта и отправителя письма. Не переходите по подозрительным ссылкам и не вводите данные на незнакомых страницах."),
    ("Мошеннические звонки", "Сотрудники банка никогда не просят коды из SMS, CVV и пароли. При сомнении положите трубку и перезвоните в банк сами."),
    ("Обновления ПО", "Своевременно обновляйте операционную систему и программы — обновления закрывают уязвимости."),
    ("Публичный Wi-Fi", "В открытых сетях не вводите пароли и не делайте покупки. Используйте VPN или мобильный интернет."),
    ("Резервные копии", "Регулярно делайте резервные копии важных данных, чтобы не потерять их при сбое или атаке вируса."),
    ("Вредоносное ПО", "Не скачивайте программы из непроверенных источников. Используйте антивирус и проверяйте вложения."),
]


def security_search(query: str) -> list[tuple[str, str]]:
    q = query.strip().lower()
    if not q:
        return list(SECURITY_KB)
    return [(t, b) for t, b in SECURITY_KB if q in t.lower() or q in b.lower()]


# ===========================================================================
# Настройки (имя цифрового куратора для приветствия — Задание 1)
# ===========================================================================
def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def save_settings(data: dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def default_user_name() -> str:
    """Имя текущего пользователя ОС (логин Windows); запасной вариант — общее имя."""
    try:
        name = getpass.getuser()
    except Exception:
        name = ""
    return name.strip() or "Цифровой куратор"


def get_user_name(default: str | None = None) -> str:
    if default is None:
        default = default_user_name()
    return load_settings().get("user_name", default)


def set_user_name(name: str) -> None:
    data = load_settings()
    data["user_name"] = name.strip()
    save_settings(data)


def greeting_for_now(name: str) -> str:
    """Приветствие в зависимости от времени суток (Задание 1)."""
    hour = dt.datetime.now().hour
    if 5 <= hour < 12:
        part = "Доброе утро"
    elif 12 <= hour < 18:
        part = "Добрый день"
    elif 18 <= hour < 23:
        part = "Добрый вечер"
    else:
        part = "Доброй ночи"
    return f"{part}, {name}!"
