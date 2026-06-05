# -*- coding: utf-8 -*-
"""
██████   DIGITAL SUPPORT  —  Центр цифровой поддержки граждан
Автор: команда Modern Talking  ·  Направление 1: Python и автоматизация

Минималистичное настольное приложение (tkinter) в тёмной теме
в стиле massgrave.dev. Объединяет три инструмента цифрового куратора:
    • Генератор надёжных паролей
    • Анализатор надёжности пароля
    • Журнал обращений граждан

Запуск:   python digital_support.py
Требования: Python 3.8+ (tkinter входит в стандартную библиотеку)
"""

import json
import os
import random
import secrets
import string
import datetime
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

# ─────────────────────────────────────────────────────────
#  ПАЛИТРА (тёмный минимализм + зелёный акцент, стиль massgrave.dev)
# ─────────────────────────────────────────────────────────
COL = {
    "bg":       "#0E0F11",   # основной фон
    "sidebar":  "#0B0C0E",   # боковая панель
    "surface":  "#16181C",   # карточки
    "surface2": "#1C1F24",   # поля ввода
    "border":   "#262A30",
    "text":     "#E8EAED",
    "muted":    "#8A8F98",
    "accent":   "#3DDC84",   # фирменный зелёный
    "accent2":  "#2BB673",   # зелёный hover
    "accentInk":"#06231A",   # текст на зелёной кнопке
    "danger":   "#FF5C5C",
    "warn":     "#FFB454",
}

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "requests.json")


# ─────────────────────────────────────────────────────────
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────
def round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Рисует прямоугольник со скруглёнными углами на Canvas."""
    pts = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


def pick_font(prefs, size, weight="normal"):
    """Выбирает первый доступный шрифт из списка предпочтений."""
    available = set(tkfont.families())
    for fam in prefs:
        if fam in available:
            return tkfont.Font(family=fam, size=size, weight=weight)
    return tkfont.Font(size=size, weight=weight)


# ─────────────────────────────────────────────────────────
#  БИЗНЕС-ЛОГИКА (функции — одно из минимальных требований)
# ─────────────────────────────────────────────────────────
def generate_password(length=16, use_upper=True, use_lower=True,
                      use_digits=True, use_symbols=True):
    """Генерирует криптостойкий пароль.

    Вызывает ValueError при некорректных входных данных (обработка ошибок).
    """
    if not isinstance(length, int):
        raise ValueError("Длина должна быть целым числом.")
    if length < 4 or length > 64:
        raise ValueError("Длина пароля должна быть от 4 до 64 символов.")

    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.?/")

    if not pools:
        raise ValueError("Выберите хотя бы один набор символов.")

    # Гарантируем по одному символу из каждого выбранного набора.
    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def evaluate_strength(password):
    """Оценивает надёжность пароля.

    Возвращает (score 0..100, метка, цвет, словарь критериев).
    """
    if not password:
        raise ValueError("Введите пароль для проверки.")

    criteria = {
        "Не менее 8 символов": len(password) >= 8,
        "Не менее 12 символов": len(password) >= 12,
        "Строчные буквы (a-z)": any(c.islower() for c in password),
        "Прописные буквы (A-Z)": any(c.isupper() for c in password),
        "Цифры (0-9)": any(c.isdigit() for c in password),
        "Спецсимволы (!@#$)": any(not c.isalnum() for c in password),
    }
    score = int(sum(criteria.values()) / len(criteria) * 100)

    if score <= 33:
        label, color = "Слабый", COL["danger"]
    elif score <= 66:
        label, color = "Средний", COL["warn"]
    elif score < 100:
        label, color = "Надёжный", COL["accent"]
    else:
        label, color = "Отличный", COL["accent"]
    return score, label, color, criteria


def load_requests():
    """Загружает журнал обращений из JSON (с обработкой ошибок ввода-вывода)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_requests(items):
    """Сохраняет журнал обращений в JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise IOError("Не удалось сохранить журнал: " + str(e))


# ─────────────────────────────────────────────────────────
#  ВИДЖЕТЫ
# ─────────────────────────────────────────────────────────
class GButton(tk.Canvas):
    """Скруглённая кнопка с эффектом наведения."""
    def __init__(self, parent, text, command=None, kind="primary",
                 width=170, height=46, font=None, bg=None):
        bg = bg or parent["bg"]
        super().__init__(parent, width=width, height=height, bg=bg,
                         highlightthickness=0, bd=0)
        self.text = text
        self.command = command
        self.kind = kind
        self.font = font
        self._cw, self._ch = width, height  # ширина/высота холста (НЕ трогаем self._w — это внутр. путь tkinter)
        self._draw(False)
        self.bind("<Enter>", lambda e: self._draw(True))
        self.bind("<Leave>", lambda e: self._draw(False))
        self.bind("<Button-1>", self._on_click)
        self.configure(cursor="hand2")

    def _palette(self, hover):
        if self.kind == "primary":
            return (COL["accent2"] if hover else COL["accent"]), COL["accentInk"], None
        if self.kind == "ghost":
            return (COL["surface2"] if hover else COL["surface"]), COL["text"], COL["border"]
        return (COL["surface2"] if hover else COL["surface"]), COL["text"], None

    def _draw(self, hover):
        self.delete("all")
        fill, fg, outline = self._palette(hover)
        round_rect(self, 2, 2, self._cw - 2, self._ch - 2, 12,
                   fill=fill, outline=outline or fill,
                   width=1 if outline else 0)
        self.create_text(self._cw / 2, self._ch / 2, text=self.text,
                         fill=fg, font=self.font)

    def _on_click(self, _):
        if self.command:
            self.command()


def make_entry(parent, font, width=20, show=None):
    """Создаёт тёмное поле ввода в едином стиле."""
    e = tk.Entry(parent, font=font, width=width, show=show,
                 bg=COL["surface2"], fg=COL["text"],
                 insertbackground=COL["accent"], relief="flat",
                 highlightthickness=1, highlightbackground=COL["border"],
                 highlightcolor=COL["accent"], disabledbackground=COL["surface2"])
    return e


class Toggle(tk.Canvas):
    """Кастомный переключатель (чекбокс) со скруглённым индикатором."""
    def __init__(self, parent, text, font, initial=True, bg=None):
        bg = bg or parent["bg"]
        super().__init__(parent, width=260, height=34, bg=bg,
                         highlightthickness=0, bd=0)
        self.var = tk.BooleanVar(value=initial)
        self.text = text
        self.font = font
        self._draw()
        self.bind("<Button-1>", self._toggle)
        self.configure(cursor="hand2")

    def _draw(self):
        self.delete("all")
        on = self.var.get()
        track = COL["accent"] if on else COL["surface2"]
        round_rect(self, 2, 7, 42, 27, 10, fill=track, outline=COL["border"], width=1)
        knob_x = 30 if on else 12
        self.create_oval(knob_x - 8, 9, knob_x + 8, 25,
                         fill=COL["accentInk"] if on else COL["muted"], outline="")
        self.create_text(54, 17, text=self.text, anchor="w",
                         fill=COL["text"], font=self.font)

    def _toggle(self, _):
        self.var.set(not self.var.get())
        self._draw()

    def get(self):
        return self.var.get()


# ─────────────────────────────────────────────────────────
#  ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ─────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DIGITAL SUPPORT — Центр цифровой поддержки")
        self.geometry("1000x660")
        self.minsize(900, 600)
        self.configure(bg=COL["bg"])

        # Шрифты (кросс-платформенный подбор)
        mono = ["JetBrains Mono", "Cascadia Code", "Consolas",
                "DejaVu Sans Mono", "Liberation Mono", "Courier New"]
        sans = ["Segoe UI", "Inter", "DejaVu Sans", "Liberation Sans", "Arial"]
        self.f_logo  = pick_font(mono, 15, "bold")
        self.f_nav   = pick_font(sans, 11)
        self.f_h1    = pick_font(sans, 20, "bold")
        self.f_sub   = pick_font(sans, 10)
        self.f_body  = pick_font(sans, 11)
        self.f_btn   = pick_font(sans, 11, "bold")
        self.f_mono  = pick_font(mono, 18, "bold")
        self.f_monoS = pick_font(mono, 10)

        self.requests = load_requests()
        self._build_sidebar()
        self._build_content()
        self.show_view("gen")

    # ─── БОКОВАЯ ПАНЕЛЬ ───
    def _build_sidebar(self):
        bar = tk.Frame(self, bg=COL["sidebar"], width=240)
        bar.pack(side="left", fill="y")
        bar.pack_propagate(False)

        # Логотип
        head = tk.Frame(bar, bg=COL["sidebar"])
        head.pack(fill="x", padx=22, pady=(26, 30))
        dot = tk.Canvas(head, width=12, height=12, bg=COL["sidebar"],
                        highlightthickness=0)
        dot.create_oval(1, 1, 11, 11, fill=COL["accent"], outline="")
        dot.pack(side="left")
        tk.Label(head, text="  DIGITAL SUPPORT", bg=COL["sidebar"],
                 fg=COL["text"], font=self.f_logo).pack(side="left")

        self.nav_buttons = {}
        items = [
            ("gen",    "■  Генератор паролей"),
            ("check",  "■  Проверка пароля"),
            ("journal","■  Журнал обращений"),
            ("about",  "■  О проекте"),
        ]
        for key, label in items:
            f = tk.Frame(bar, bg=COL["sidebar"], height=44)
            f.pack(fill="x", padx=12, pady=2)
            f.pack_propagate(False)
            barmark = tk.Frame(f, bg=COL["sidebar"], width=3)
            barmark.pack(side="left", fill="y")
            lbl = tk.Label(f, text=label, bg=COL["sidebar"], fg=COL["muted"],
                           font=self.f_nav, anchor="w", padx=12)
            lbl.pack(side="left", fill="both", expand=True)
            for w in (f, lbl):
                w.bind("<Button-1>", lambda e, k=key: self.show_view(k))
                w.configure(cursor="hand2")
            self.nav_buttons[key] = (f, lbl, barmark)

        # Нижняя подпись
        tk.Label(bar, text="Modern Talking · v1.0", bg=COL["sidebar"],
                 fg=COL["muted"], font=self.f_monoS).pack(side="bottom", pady=18)

    def _set_active_nav(self, key):
        for k, (f, lbl, mark) in self.nav_buttons.items():
            active = (k == key)
            lbl.configure(fg=COL["text"] if active else COL["muted"])
            mark.configure(bg=COL["accent"] if active else COL["sidebar"])
            f.configure(bg=COL["surface"] if active else COL["sidebar"])
            lbl.configure(bg=COL["surface"] if active else COL["sidebar"])

    # ─── КОНТЕНТ ───
    def _build_content(self):
        self.content = tk.Frame(self, bg=COL["bg"])
        self.content.pack(side="left", fill="both", expand=True)
        self.views = {}
        for key, builder in (("gen", self._view_gen),
                             ("check", self._view_check),
                             ("journal", self._view_journal),
                             ("about", self._view_about)):
            frame = tk.Frame(self.content, bg=COL["bg"])
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            builder(frame)
            self.views[key] = frame

    def show_view(self, key):
        self.views[key].tkraise()
        self._set_active_nav(key)
        if key == "journal":
            self._refresh_journal()

    def _header(self, parent, title, subtitle):
        wrap = tk.Frame(parent, bg=COL["bg"])
        wrap.pack(fill="x", padx=40, pady=(36, 18))
        tk.Label(wrap, text=title, bg=COL["bg"], fg=COL["text"],
                 font=self.f_h1, anchor="w").pack(anchor="w")
        tk.Label(wrap, text=subtitle, bg=COL["bg"], fg=COL["muted"],
                 font=self.f_sub, anchor="w").pack(anchor="w", pady=(4, 0))

    def _card(self, parent):
        c = tk.Frame(parent, bg=COL["surface"], highlightthickness=1,
                     highlightbackground=COL["border"])
        return c

    # ═══ ВИД: ГЕНЕРАТОР ПАРОЛЕЙ ═══
    def _view_gen(self, root):
        self._header(root, "Генератор паролей",
                     "Криптостойкие пароли на основе модуля secrets")
        card = self._card(root)
        card.pack(fill="x", padx=40, pady=8)

        # Поле результата
        out = tk.Frame(card, bg=COL["surface2"], highlightthickness=1,
                       highlightbackground=COL["border"])
        out.pack(fill="x", padx=24, pady=(24, 16))
        self.gen_result = tk.Label(out, text="—", bg=COL["surface2"],
                                   fg=COL["accent"], font=self.f_mono, anchor="w")
        self.gen_result.pack(side="left", fill="x", expand=True, padx=18, pady=16)

        # Настройки
        opts = tk.Frame(card, bg=COL["surface"])
        opts.pack(fill="x", padx=24, pady=(0, 8))
        line = tk.Frame(opts, bg=COL["surface"])
        line.pack(fill="x", pady=6)
        tk.Label(line, text="Длина пароля", bg=COL["surface"], fg=COL["muted"],
                 font=self.f_body).pack(side="left")
        self.gen_len = make_entry(line, self.f_body, width=6)
        self.gen_len.insert(0, "16")
        self.gen_len.pack(side="left", padx=12, ipady=4, ipadx=4)

        self.t_upper = Toggle(opts, "Прописные A-Z", self.f_body, True, bg=COL["surface"])
        self.t_lower = Toggle(opts, "Строчные a-z", self.f_body, True, bg=COL["surface"])
        self.t_digit = Toggle(opts, "Цифры 0-9", self.f_body, True, bg=COL["surface"])
        self.t_sym   = Toggle(opts, "Спецсимволы !@#", self.f_body, True, bg=COL["surface"])
        for t in (self.t_upper, self.t_lower, self.t_digit, self.t_sym):
            t.pack(anchor="w", pady=1)

        # Кнопки
        actions = tk.Frame(card, bg=COL["surface"])
        actions.pack(fill="x", padx=24, pady=(8, 24))
        GButton(actions, "СГЕНЕРИРОВАТЬ", command=self._do_generate,
                kind="primary", font=self.f_btn, bg=COL["surface"]).pack(side="left")
        GButton(actions, "КОПИРОВАТЬ", command=self._do_copy,
                kind="ghost", font=self.f_btn, bg=COL["surface"]).pack(side="left", padx=12)

    def _do_generate(self):
        try:
            length = int(self.gen_len.get())
            pwd = generate_password(length, self.t_upper.get(), self.t_lower.get(),
                                    self.t_digit.get(), self.t_sym.get())
            self.gen_result.configure(text=pwd)
        except ValueError as e:
            messagebox.showwarning("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _do_copy(self):
        text = self.gen_result.cget("text")
        if text and text != "—":
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Готово", "Пароль скопирован в буфер обмена.")
        else:
            messagebox.showwarning("Нечего копировать", "Сначала сгенерируйте пароль.")

    # ═══ ВИД: ПРОВЕРКА ПАРОЛЯ ═══
    def _view_check(self, root):
        self._header(root, "Проверка надёжности пароля",
                     "Оценка по 6 критериям безопасности")
        card = self._card(root)
        card.pack(fill="x", padx=40, pady=8)

        row = tk.Frame(card, bg=COL["surface"])
        row.pack(fill="x", padx=24, pady=(24, 12))
        self.chk_entry = make_entry(row, self.f_body, width=34)
        self.chk_entry.pack(side="left", fill="x", expand=True, ipady=6, ipadx=6)
        self.chk_entry.bind("<KeyRelease>", lambda e: self._do_check())
        GButton(row, "ПРОВЕРИТЬ", command=self._do_check, kind="primary",
                font=self.f_btn, width=140, bg=COL["surface"]).pack(side="left", padx=12)

        # Прогресс-бар
        self.bar_canvas = tk.Canvas(card, height=14, bg=COL["surface"],
                                    highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=24, pady=(6, 4))
        self.chk_label = tk.Label(card, text="Введите пароль…", bg=COL["surface"],
                                  fg=COL["muted"], font=self.f_btn, anchor="w")
        self.chk_label.pack(anchor="w", padx=24, pady=(0, 8))

        self.crit_frame = tk.Frame(card, bg=COL["surface"])
        self.crit_frame.pack(fill="x", padx=24, pady=(0, 24))

    def _do_check(self):
        pwd = self.chk_entry.get()
        self.bar_canvas.delete("all")
        for w in self.crit_frame.winfo_children():
            w.destroy()
        if not pwd:
            self.chk_label.configure(text="Введите пароль…", fg=COL["muted"])
            return
        try:
            score, label, color, criteria = evaluate_strength(pwd)
        except ValueError as e:
            self.chk_label.configure(text=str(e), fg=COL["warn"])
            return
        w = max(self.bar_canvas.winfo_width(), 400)
        round_rect(self.bar_canvas, 0, 0, w, 14, 7, fill=COL["surface2"], outline="")
        if score > 0:
            round_rect(self.bar_canvas, 0, 0, max(14, w * score / 100), 14, 7,
                       fill=color, outline="")
        self.chk_label.configure(text=f"{label}  ·  {score}/100", fg=color)
        for name, ok in criteria.items():
            row = tk.Frame(self.crit_frame, bg=COL["surface"])
            row.pack(anchor="w", pady=2)
            tk.Label(row, text="✔" if ok else "✘", bg=COL["surface"],
                     fg=COL["accent"] if ok else COL["danger"],
                     font=self.f_body, width=2).pack(side="left")
            tk.Label(row, text=name, bg=COL["surface"],
                     fg=COL["text"] if ok else COL["muted"],
                     font=self.f_body).pack(side="left")

    # ═══ ВИД: ЖУРНАЛ ОБРАЩЕНИЙ ═══
    def _view_journal(self, root):
        self._header(root, "Журнал обращений граждан",
                     "Регистрация и хранение обращений (requests.json)")
        body = tk.Frame(root, bg=COL["bg"])
        body.pack(fill="both", expand=True, padx=40, pady=8)

        # Форма слева
        form = self._card(body)
        form.pack(side="left", fill="y", padx=(0, 16))
        inner = tk.Frame(form, bg=COL["surface"])
        inner.pack(padx=20, pady=20)
        tk.Label(inner, text="НОВОЕ ОБРАЩЕНИЕ", bg=COL["surface"], fg=COL["accent"],
                 font=self.f_monoS).pack(anchor="w", pady=(0, 10))
        tk.Label(inner, text="ФИО гражданина", bg=COL["surface"], fg=COL["muted"],
                 font=self.f_sub).pack(anchor="w")
        self.j_fio = make_entry(inner, self.f_body, width=28)
        self.j_fio.pack(pady=(2, 10), ipady=5, ipadx=4)
        tk.Label(inner, text="Тема обращения", bg=COL["surface"], fg=COL["muted"],
                 font=self.f_sub).pack(anchor="w")
        self.j_topic = make_entry(inner, self.f_body, width=28)
        self.j_topic.pack(pady=(2, 10), ipady=5, ipadx=4)
        tk.Label(inner, text="Описание", bg=COL["surface"], fg=COL["muted"],
                 font=self.f_sub).pack(anchor="w")
        self.j_desc = tk.Text(inner, width=30, height=4, font=self.f_body,
                              bg=COL["surface2"], fg=COL["text"],
                              insertbackground=COL["accent"], relief="flat",
                              highlightthickness=1, highlightbackground=COL["border"],
                              highlightcolor=COL["accent"])
        self.j_desc.pack(pady=(2, 14))
        GButton(inner, "ДОБАВИТЬ В ЖУРНАЛ", command=self._add_request,
                kind="primary", font=self.f_btn, width=240, bg=COL["surface"]).pack()

        # Список справа
        listwrap = self._card(body)
        listwrap.pack(side="left", fill="both", expand=True)
        bar = tk.Frame(listwrap, bg=COL["surface"])
        bar.pack(fill="x", padx=16, pady=(14, 6))
        self.j_count = tk.Label(bar, text="Обращений: 0", bg=COL["surface"],
                                fg=COL["muted"], font=self.f_monoS)
        self.j_count.pack(side="left")
        GButton(bar, "УДАЛИТЬ", command=self._del_request, kind="ghost",
                font=self.f_btn, width=110, height=34, bg=COL["surface"]).pack(side="right")

        self.j_list = tk.Listbox(listwrap, bg=COL["surface2"], fg=COL["text"],
                                 font=self.f_monoS, relief="flat",
                                 selectbackground=COL["accent"],
                                 selectforeground=COL["accentInk"],
                                 highlightthickness=0, activestyle="none", bd=0)
        self.j_list.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _refresh_journal(self):
        if not hasattr(self, "j_list"):
            return
        self.j_list.delete(0, "end")
        for r in self.requests:
            self.j_list.insert("end",
                f"[{r.get('date','')}]  {r.get('fio','')}  —  {r.get('topic','')}")
        self.j_count.configure(text=f"Обращений: {len(self.requests)}")

    def _add_request(self):
        fio = self.j_fio.get().strip()
        topic = self.j_topic.get().strip()
        desc = self.j_desc.get("1.0", "end").strip()
        if not fio or not topic:
            messagebox.showwarning("Заполните поля",
                                   "Поля «ФИО» и «Тема» обязательны.")
            return
        self.requests.append({
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "fio": fio, "topic": topic, "desc": desc,
        })
        try:
            save_requests(self.requests)
        except IOError as e:
            messagebox.showerror("Ошибка сохранения", str(e))
            return
        self.j_fio.delete(0, "end")
        self.j_topic.delete(0, "end")
        self.j_desc.delete("1.0", "end")
        self._refresh_journal()

    def _del_request(self):
        sel = self.j_list.curselection()
        if not sel:
            messagebox.showinfo("Выберите запись", "Выделите обращение в списке.")
            return
        idx = sel[0]
        del self.requests[idx]
        try:
            save_requests(self.requests)
        except IOError as e:
            messagebox.showerror("Ошибка", str(e))
        self._refresh_journal()

    # ═══ ВИД: О ПРОЕКТЕ ═══
    def _view_about(self, root):
        self._header(root, "О проекте",
                     "Центр цифровой поддержки граждан")
        card = self._card(root)
        card.pack(fill="both", expand=True, padx=40, pady=8)
        text = (
            "Команда:  Modern Talking — Digital Curators Team\n"
            "Направление:  Python и автоматизация\n\n"
            "Состав команды:\n"
            "  • Комиссаров Илья — Лидер команды\n"
            "  • Госани Айдар — Технический специалист\n"
            "  • Чернов Матвей — Специалист по ИБ\n"
            "  • Яноха Денис — Консультант\n"
            "  • Чирков Костя — Документатор\n\n"
            "Функции приложения:\n"
            "  1. Генератор криптостойких паролей (модуль secrets)\n"
            "  2. Анализатор надёжности пароля по 6 критериям\n"
            "  3. Журнал обращений с сохранением в JSON\n\n"
            "Технологии:  Python 3 · tkinter · secrets · json\n"
            "Соответствие требованиям: ввод данных · функции · обработка ошибок"
        )
        tk.Label(card, text=text, bg=COL["surface"], fg=COL["text"],
                 font=self.f_body, justify="left", anchor="nw").pack(
                 anchor="nw", padx=28, pady=24)


if __name__ == "__main__":
    App().mainloop()
