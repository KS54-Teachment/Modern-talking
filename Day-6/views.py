"""
Экраны (разделы) приложения ЦифроКуратор.
Каждый раздел — это отдельный Frame, который переключается в app.py.
"""

import datetime as dt
import customtkinter as ctk

import theme as T
import logic as L
from widgets import (Card, StatCard, StrengthMeter, SectionTitle,
                     accent_button, ghost_button)


class BaseView(ctk.CTkScrollableFrame):
    """Базовый прокручиваемый экран."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.fonts = app.fonts
        self.grid_columnconfigure(0, weight=1)

    def on_show(self):
        """Вызывается при каждом открытии экрана."""
        pass


# ---------------------------------------------------------------------------
# ГЛАВНАЯ / ДАШБОРД (Задание 1: приветствие, имя, дата)
# ---------------------------------------------------------------------------
class DashboardView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)

        # Приветственный баннер
        hero = Card(self, fg_color=T.CARD)
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hero.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hero, text="Центр цифровой поддержки", font=self.fonts.small,
                     text_color=T.ACCENT).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 0))
        self.greet_lbl = ctk.CTkLabel(hero, text="", font=self.fonts.display, text_color=T.TEXT)
        self.greet_lbl.grid(row=1, column=0, sticky="w", padx=24, pady=(2, 0))
        self.date_lbl = ctk.CTkLabel(hero, text="", font=self.fonts.body, text_color=T.MUTED)
        self.date_lbl.grid(row=2, column=0, sticky="w", padx=24, pady=(2, 20))

        # Поле имени
        name_row = ctk.CTkFrame(hero, fg_color="transparent")
        name_row.grid(row=3, column=0, sticky="w", padx=24, pady=(0, 20))
        ctk.CTkLabel(name_row, text="Имя куратора:", font=self.fonts.small,
                     text_color=T.MUTED).pack(side="left", padx=(0, 10))
        self.name_entry = ctk.CTkEntry(name_row, width=220, height=36, corner_radius=10,
                                       fg_color=T.ELEV, border_color=T.BORDER,
                                       font=self.fonts.body, text_color=T.TEXT)
        self.name_entry.pack(side="left", padx=(0, 10))
        accent_button(name_row, "Сохранить", self._save_name, self.fonts, width=110).pack(side="left")

        # Статистика
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1, uniform="stat")
        self.stat_total = StatCard(stats, self.fonts, 0, "Всего обращений", "✉", T.BLUE)
        self.stat_total.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.stat_work = StatCard(stats, self.fonts, 0, "В работе", "⚡", T.YELLOW)
        self.stat_work.grid(row=0, column=1, sticky="ew", padx=8)
        self.stat_done = StatCard(stats, self.fonts, 0, "Решено", "✓", T.GREEN)
        self.stat_done.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        # Быстрые действия
        SectionTitle(self, self.fonts, "Быстрые действия",
                     "Инструменты цифрового куратора").grid(
            row=2, column=0, sticky="ew", pady=(0, 12))
        quick = ctk.CTkFrame(self, fg_color="transparent")
        quick.grid(row=3, column=0, sticky="ew")
        actions = [
            ("🤖  Консультант", "consultant"),
            ("🔐  Генератор паролей", "password"),
            ("🗂  База обращений", "appeals"),
            ("📄  Отчёт", "report"),
        ]
        for i, (label, key) in enumerate(actions):
            quick.grid_columnconfigure(i % 2, weight=1, uniform="q")
            btn = ghost_button(quick, label, lambda k=key: self.app.show_view(k),
                               self.fonts, height=56)
            btn.configure(anchor="w")
            btn.grid(row=i // 2, column=i % 2, sticky="ew",
                     padx=(0 if i % 2 == 0 else 8, 8 if i % 2 == 0 else 0),
                     pady=6)

    def _save_name(self):
        name = self.name_entry.get().strip() or L.default_user_name()
        L.set_user_name(name)
        self._refresh_greeting()
        self.app.toast.show("Имя сохранено", "success")

    def _refresh_greeting(self):
        name = L.get_user_name()
        self.greet_lbl.configure(text=L.greeting_for_now(name))
        days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        now = dt.datetime.now()
        self.date_lbl.configure(
            text=f"Сегодня {days[now.weekday()]}, {now.strftime('%d.%m.%Y')} · {now.strftime('%H:%M')}")

    def on_show(self):
        if not self.name_entry.get():
            self.name_entry.insert(0, L.get_user_name())
        self._refresh_greeting()
        store = self.app.store
        self.stat_total.set_value(len(store.all()))
        self.stat_work.set_value(store.count_by_status("В работе"))
        self.stat_done.set_value(store.count_by_status("Решено"))


# ---------------------------------------------------------------------------
# КОНСУЛЬТАНТ (Задание 2)
# ---------------------------------------------------------------------------
class ConsultantView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "🤖  Цифровой помощник «Консультант»",
                     "Выберите проблему — помощник предложит решение").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        picker = Card(self)
        picker.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        picker.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(picker, text="Проблема пользователя", font=self.fonts.h3,
                     text_color=T.TEXT).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 8))
        self.menu = ctk.CTkOptionMenu(
            picker, values=L.consultant_problems(), command=self._on_pick,
            font=self.fonts.body, dropdown_font=self.fonts.body,
            fg_color=T.ELEV, button_color=T.ACCENT_DIM, button_hover_color=T.ACCENT,
            text_color=T.TEXT, dropdown_fg_color=T.ELEV, dropdown_hover_color=T.CARD_HOVER,
            corner_radius=10, height=40)
        self.menu.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 18))

        # Карточка решения
        self.answer_card = Card(self, fg_color=T.CARD)
        self.answer_card.grid(row=2, column=0, sticky="ew")
        self.answer_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.answer_card, text="✅  Решение", font=self.fonts.h3,
                     text_color=T.ACCENT).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 6))
        self.solution_lbl = ctk.CTkLabel(self.answer_card, text="", font=self.fonts.body,
                                         text_color=T.TEXT, wraplength=620, justify="left")
        self.solution_lbl.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))
        ctk.CTkLabel(self.answer_card, text="Рекомендации:", font=self.fonts.body_bold,
                     text_color=T.MINT).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 4))
        self.recs_lbl = ctk.CTkLabel(self.answer_card, text="", font=self.fonts.body,
                                     text_color=T.TEXT_SOFT, wraplength=620, justify="left")
        self.recs_lbl.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 18))

        # Кнопка: занести в журнал
        accent_button(self.answer_card, "+ Занести в журнал обращений",
                      self._log_appeal, self.fonts, width=260).grid(
            row=4, column=0, sticky="w", padx=20, pady=(0, 18))

    def _on_pick(self, problem):
        sol, recs = L.consultant_answer(problem)
        self.solution_lbl.configure(text=sol)
        self.recs_lbl.configure(text="\n".join(f"•  {r}" for r in recs))

    def _log_appeal(self):
        problem = self.menu.get()
        self.app.store.add("Анонимный пользователь", problem, "Новое")
        self.app.toast.show("Обращение добавлено в журнал", "success")

    def on_show(self):
        self._on_pick(self.menu.get())


# ---------------------------------------------------------------------------
# ГЕНЕРАТОР ПАРОЛЕЙ (Задание 3)
# ---------------------------------------------------------------------------
class PasswordView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "🔐  Генератор надёжных паролей",
                     "Настройте параметры и создайте криптостойкий пароль").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        # Дисплей пароля
        disp = Card(self, fg_color=T.ELEV)
        disp.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        disp.grid_columnconfigure(0, weight=1)
        self.pwd_var = ctk.StringVar(value="—")
        self.pwd_lbl = ctk.CTkLabel(disp, textvariable=self.pwd_var, font=self.fonts.mono,
                                    text_color=T.ACCENT, anchor="w")
        self.pwd_lbl.grid(row=0, column=0, sticky="w", padx=20, pady=18)
        ghost_button(disp, "⧉ Копировать", self._copy, self.fonts, width=130).grid(
            row=0, column=1, padx=(0, 16), pady=18)

        # Индикатор надёжности
        self.meter = StrengthMeter(self, self.fonts)
        self.meter.grid(row=2, column=0, sticky="ew", pady=(0, 16))

        # Настройки
        opts = Card(self)
        opts.grid(row=3, column=0, sticky="ew", pady=(0, 16))
        opts.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(opts, text="Параметры", font=self.fonts.h3, text_color=T.TEXT).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))

        # Длина
        self.len_lbl = ctk.CTkLabel(opts, text="Длина: 16", font=self.fonts.body,
                                    text_color=T.TEXT_SOFT)
        self.len_lbl.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 4))
        self.length = ctk.CTkSlider(opts, from_=6, to=40, number_of_steps=34,
                                    command=self._on_len, progress_color=T.ACCENT,
                                    button_color=T.ACCENT, button_hover_color=T.MINT)
        self.length.set(16)
        self.length.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 14))

        # Чекбоксы
        self.use_upper = ctk.BooleanVar(value=True)
        self.use_lower = ctk.BooleanVar(value=True)
        self.use_digits = ctk.BooleanVar(value=True)
        self.use_special = ctk.BooleanVar(value=True)
        self.no_ambig = ctk.BooleanVar(value=False)
        checks = [
            ("Заглавные (A-Z)", self.use_upper),
            ("Строчные (a-z)", self.use_lower),
            ("Цифры (0-9)", self.use_digits),
            ("Спецсимволы (!@#)", self.use_special),
            ("Без похожих символов (Il1O0)", self.no_ambig),
        ]
        for i, (label, var) in enumerate(checks):
            ctk.CTkCheckBox(opts, text=label, variable=var, font=self.fonts.body,
                            text_color=T.TEXT_SOFT, fg_color=T.ACCENT,
                            hover_color=T.ACCENT_HOVER, checkmark_color="#06241f",
                            corner_radius=6).grid(
                row=3 + i // 2, column=i % 2, sticky="w", padx=20, pady=6)

        accent_button(opts, "⚡  Сгенерировать пароль", self._generate, self.fonts,
                      width=240, height=46).grid(row=7, column=0, columnspan=2,
                                                  sticky="w", padx=20, pady=(14, 20))


    def _on_len(self, value):
        self.len_lbl.configure(text=f"Длина: {int(float(value))}")

    def _generate(self):
        pwd = L.generate_password(
            int(self.length.get()), self.use_lower.get(), self.use_upper.get(),
            self.use_digits.get(), self.use_special.get(), self.no_ambig.get())
        self.pwd_var.set(pwd)
        self.meter.update_strength(L.password_strength(pwd))
        self.app.toast.show("Пароль сгенерирован", "success")

    def _copy(self):
        pwd = self.pwd_var.get()
        if pwd and pwd != "—":
            self.app.copy_to_clipboard(pwd)
            self.app.toast.show("Скопировано в буфер обмена", "info")

    def on_show(self):
        if self.pwd_var.get() == "—":
            self._generate()


# ---------------------------------------------------------------------------
# ПРОВЕРКА ПАРОЛЯ (отдельный раздел)
# ---------------------------------------------------------------------------
class PasswordCheckView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "🔎  Проверка надёжности пароля",
                     "Введите пароль — приложение оценит его стойкость").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        # Поле ввода пароля
        card = Card(self)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text="Пароль для проверки", font=self.fonts.h3,
                     text_color=T.TEXT).grid(row=0, column=0, sticky="w",
                                             padx=20, pady=(18, 8))
        self.entry = ctk.CTkEntry(card, height=40, corner_radius=10, fg_color=T.ELEV,
                                  border_color=T.BORDER, font=self.fonts.body,
                                  text_color=T.TEXT, show="•",
                                  placeholder_text="Введите пароль для проверки...")
        self.entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.entry.bind("<KeyRelease>", lambda e: self._check())
        self.show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(card, text="Показывать символы", variable=self.show_var,
                        command=self._toggle_show, font=self.fonts.small,
                        text_color=T.TEXT_SOFT, fg_color=T.ACCENT,
                        hover_color=T.ACCENT_HOVER, checkmark_color="#06241f",
                        corner_radius=6).grid(row=2, column=0, sticky="w",
                                              padx=20, pady=(0, 18))

        # Индикатор надёжности (собственный для этого раздела)
        self.meter = StrengthMeter(self, self.fonts)
        self.meter.grid(row=2, column=0, sticky="ew", pady=(0, 16))

        # Рекомендации
        tips_card = Card(self, fg_color=T.CARD)
        tips_card.grid(row=3, column=0, sticky="ew")
        tips_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tips_card, text="💡  Рекомендации", font=self.fonts.h3,
                     text_color=T.MINT).grid(row=0, column=0, sticky="w",
                                             padx=20, pady=(18, 6))
        self.tips = ctk.CTkLabel(tips_card, text="", font=self.fonts.body,
                                 text_color=T.TEXT_SOFT, wraplength=620, justify="left")
        self.tips.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))

    def _toggle_show(self):
        self.entry.configure(show="" if self.show_var.get() else "•")

    def _check(self):
        info = L.password_strength(self.entry.get())
        self.meter.update_strength(info)
        tips = info.get("tips") or []
        self.tips.configure(
            text="\n".join(f"•  {t}" for t in tips) if tips
            else "Отличный пароль — дополнительных рекомендаций нет.")

    def on_show(self):
        self._check()


# ---------------------------------------------------------------------------
# БАЗА ОБРАЩЕНИЙ (Задание 4)
# ---------------------------------------------------------------------------
class AppealsView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "🗂  База обращений",
                     "Добавляйте, ищите и удаляйте обращения граждан").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        # Форма добавления
        form = Card(self)
        form.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        form.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(form, text="Новое обращение", font=self.fonts.h3, text_color=T.TEXT).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))
        self.name_e = ctk.CTkEntry(form, height=40, corner_radius=10, fg_color=T.ELEV,
                                   border_color=T.BORDER, font=self.fonts.body,
                                   text_color=T.TEXT, placeholder_text="Имя гражданина")
        self.name_e.grid(row=1, column=0, sticky="ew", padx=(20, 8), pady=(0, 10))
        self.problem_e = ctk.CTkEntry(form, height=40, corner_radius=10, fg_color=T.ELEV,
                                      border_color=T.BORDER, font=self.fonts.body,
                                      text_color=T.TEXT, placeholder_text="Описание проблемы")
        self.problem_e.grid(row=1, column=1, sticky="ew", padx=(8, 20), pady=(0, 10))
        self.status_m = ctk.CTkOptionMenu(form, values=L.STATUSES, font=self.fonts.body,
                                          fg_color=T.ELEV, button_color=T.ACCENT_DIM,
                                          button_hover_color=T.ACCENT, text_color=T.TEXT,
                                          dropdown_fg_color=T.ELEV,
                                          dropdown_hover_color=T.CARD_HOVER,
                                          corner_radius=10, height=40, width=160)
        self.status_m.grid(row=2, column=0, sticky="w", padx=(20, 8), pady=(0, 18))
        accent_button(form, "+ Добавить", self._add, self.fonts, width=160).grid(
            row=2, column=1, sticky="e", padx=(8, 20), pady=(0, 18))

        # Поиск
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        search_row.grid_columnconfigure(0, weight=1)
        self.search_e = ctk.CTkEntry(search_row, height=40, corner_radius=10, fg_color=T.CARD,
                                     border_color=T.BORDER, font=self.fonts.body,
                                     text_color=T.TEXT,
                                     placeholder_text="🔍  Поиск по имени, проблеме или статусу")
        self.search_e.grid(row=0, column=0, sticky="ew")
        self.search_e.bind("<KeyRelease>", lambda e: self._render())

        # Список обращений
        self.list_box = ctk.CTkFrame(self, fg_color="transparent")
        self.list_box.grid(row=3, column=0, sticky="ew")
        self.list_box.grid_columnconfigure(0, weight=1)

    def _add(self):
        name = self.name_e.get().strip()
        problem = self.problem_e.get().strip()
        if not name or not problem:
            self.app.toast.show("Заполните имя и проблему", "warn")
            return
        self.app.store.add(name, problem, self.status_m.get())
        self.name_e.delete(0, "end")
        self.problem_e.delete(0, "end")
        self.app.toast.show("Обращение добавлено", "success")
        self._render()

    def _delete(self, appeal_id):
        self.app.store.delete(appeal_id)
        self.app.toast.show("Обращение удалено", "info")
        self._render()

    def _render(self):
        for w in self.list_box.winfo_children():
            w.destroy()
        items = self.app.store.search(self.search_e.get())
        if not items:
            empty = Card(self.list_box)
            empty.grid(row=0, column=0, sticky="ew")
            ctk.CTkLabel(empty, text="Обращений пока нет", font=self.fonts.body,
                         text_color=T.MUTED).pack(padx=20, pady=24)
            return
        for i, a in enumerate(reversed(items)):
            row = Card(self.list_box, fg_color=T.CARD)
            row.grid(row=i, column=0, sticky="ew", pady=4)
            row.grid_columnconfigure(1, weight=1)
            color = T.STATUS_COLORS.get(a.status, T.MUTED)
            ctk.CTkLabel(row, text="●", font=self.fonts.body, text_color=color).grid(
                row=0, column=0, padx=(16, 8), pady=14)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.grid(row=0, column=1, sticky="ew", pady=10)
            info.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(info, text=a.name, font=self.fonts.body_bold, text_color=T.TEXT,
                         anchor="w").grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(info, text=a.problem, font=self.fonts.small, text_color=T.TEXT_SOFT,
                         anchor="w", wraplength=420, justify="left").grid(row=1, column=0, sticky="w")
            ctk.CTkLabel(info, text=f"{a.status}  ·  {a.created}", font=self.fonts.tiny,
                         text_color=T.MUTED, anchor="w").grid(row=2, column=0, sticky="w")
            ctk.CTkButton(row, text="✕", width=36, height=36, corner_radius=8,
                          font=self.fonts.body_bold, fg_color="transparent",
                          hover_color="#3a1518", text_color=T.RED,
                          command=lambda aid=a.id: self._delete(aid)).grid(
                row=0, column=2, padx=(8, 14))

    def on_show(self):
        self._render()


# ---------------------------------------------------------------------------
# ОТЧЁТ (Задание 5)
# ---------------------------------------------------------------------------
class ReportView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "📄  Отчёт о работе",
                     "Сформируйте и сохраните отчёт в файл report.txt").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        accent_button(btns, "🔄  Сформировать", self._preview, self.fonts, width=180).pack(
            side="left", padx=(0, 10))
        ghost_button(btns, "💾  Сохранить report.txt", self._save, self.fonts, width=220).pack(
            side="left")

        card = Card(self, fg_color=T.ELEV)
        card.grid(row=2, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)
        self.textbox = ctk.CTkTextbox(card, height=360, font=self.fonts.mono_small,
                                      fg_color=T.ELEV, text_color=T.TEXT_SOFT,
                                      border_width=0, wrap="none")
        self.textbox.grid(row=0, column=0, sticky="ew", padx=14, pady=14)

    def _preview(self):
        text = L.build_report(self.app.store.all())
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)

    def _save(self):
        path = L.save_report(self.app.store.all())
        self._preview()
        self.app.toast.show("Отчёт сохранён: report.txt", "success")

    def on_show(self):
        self._preview()


# ---------------------------------------------------------------------------
# КИБЕРБЕЗОПАСНОСТЬ (Проект 6 / FAQ)
# ---------------------------------------------------------------------------
class SecurityView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "🛡  Справочник по кибербезопасности",
                     "Памятки и рекомендации для безопасной работы в сети").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        self.search_e = ctk.CTkEntry(self, height=40, corner_radius=10, fg_color=T.CARD,
                                     border_color=T.BORDER, font=self.fonts.body,
                                     text_color=T.TEXT, placeholder_text="🔍  Поиск по справочнику")
        self.search_e.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.search_e.bind("<KeyRelease>", lambda e: self._render())

        self.box = ctk.CTkFrame(self, fg_color="transparent")
        self.box.grid(row=2, column=0, sticky="ew")
        self.box.grid_columnconfigure(0, weight=1)

    def _render(self):
        for w in self.box.winfo_children():
            w.destroy()
        hits = L.security_search(self.search_e.get())
        if not hits:
            ctk.CTkLabel(self.box, text="Ничего не найдено", font=self.fonts.body,
                         text_color=T.MUTED).grid(row=0, column=0, pady=20)
            return
        for i, (title, body) in enumerate(hits):
            card = Card(self.box, fg_color=T.CARD)
            card.grid(row=i, column=0, sticky="ew", pady=4)
            card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(card, text=f"🔒  {title}", font=self.fonts.body_bold,
                         text_color=T.ACCENT, anchor="w").grid(
                row=0, column=0, sticky="w", padx=18, pady=(14, 2))
            ctk.CTkLabel(card, text=body, font=self.fonts.small, text_color=T.TEXT_SOFT,
                         anchor="w", wraplength=640, justify="left").grid(
                row=1, column=0, sticky="w", padx=18, pady=(0, 14))

    def on_show(self):
        self._render()


# ---------------------------------------------------------------------------
# О КОМАНДЕ
# ---------------------------------------------------------------------------
class AboutView(BaseView):
    def __init__(self, master, app):
        super().__init__(master, app)
        SectionTitle(self, self.fonts, "ℹ  О команде",
                     f"{L.APP_NAME} — командный проект «{L.TEAM_NAME}»").grid(
            row=0, column=0, sticky="ew", pady=(0, 16))

        banner = Card(self, fg_color=T.CARD)
        banner.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        banner.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(banner, text="Modern Talking", font=self.fonts.display,
                     text_color=T.ACCENT).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 2))
        ctk.CTkLabel(banner, text="Центр цифровой поддержки граждан · День 6: Python",
                     font=self.fonts.body, text_color=T.MUTED).grid(
            row=1, column=0, sticky="w", padx=24, pady=(0, 20))

        roster = ctk.CTkFrame(self, fg_color="transparent")
        roster.grid(row=2, column=0, sticky="ew")
        roster.grid_columnconfigure(0, weight=1)
        for i, (name, role) in enumerate(L.TEAM):
            card = Card(roster, fg_color=T.CARD)
            card.grid(row=i, column=0, sticky="ew", pady=4)
            card.grid_columnconfigure(1, weight=1)
            initials = "".join(p[0] for p in name.split()[:2])
            badge = ctk.CTkLabel(card, text=initials, font=self.fonts.body_bold,
                                 text_color="#06241f", fg_color=T.ACCENT,
                                 corner_radius=18, width=40, height=40)
            badge.grid(row=0, column=0, padx=(16, 14), pady=12)
            ctk.CTkLabel(card, text=name, font=self.fonts.body_bold, text_color=T.TEXT,
                         anchor="w").grid(row=0, column=1, sticky="w")
            tag = T.ACCENT if "лидер" in role.lower() else T.MUTED
            ctk.CTkLabel(card, text=role, font=self.fonts.small, text_color=tag,
                         anchor="e").grid(row=0, column=2, sticky="e", padx=18)


# Реестр экранов: ключ -> (иконка, название, класс)
VIEW_REGISTRY = [
    ("dashboard", "🏠", "Главная", DashboardView),
    ("consultant", "🤖", "Консультант", ConsultantView),
    ("password", "🔐", "Пароли", PasswordView),
    ("check", "🔎", "Проверка пароля", PasswordCheckView),
    ("appeals", "🗂", "Обращения", AppealsView),
    ("report", "📄", "Отчёт", ReportView),
    ("security", "🛡", "Кибербезопасность", SecurityView),
    ("about", "ℹ", "О команде", AboutView),
]
