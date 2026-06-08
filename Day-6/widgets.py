"""
Переиспользуемые виджеты и анимации для приложения ЦифроКуратор.
Всё на базе customtkinter — современные скруглённые элементы.
"""

import customtkinter as ctk
import theme as T


class NavButton(ctk.CTkButton):
    """Кнопка бокового меню с активным/неактивным состоянием."""

    def __init__(self, master, text, icon, command, font):
        super().__init__(
            master,
            text=f"  {icon}   {text}",
            command=command,
            font=font,
            anchor="w",
            height=44,
            corner_radius=10,
            fg_color="transparent",
            text_color=T.MUTED,
            hover_color=T.CARD_HOVER,
        )
        self._active = False

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.configure(fg_color=T.ELEV, text_color=T.ACCENT)
        else:
            self.configure(fg_color="transparent", text_color=T.MUTED)


class Card(ctk.CTkFrame):
    """Карточка-контейнер с мягкими углами и границей."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", T.CARD)
        kwargs.setdefault("corner_radius", 16)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", T.BORDER)
        super().__init__(master, **kwargs)


class StatCard(ctk.CTkFrame):
    """Карточка со статистикой (большое число + подпись)."""

    def __init__(self, master, fonts, value, label, icon, color=T.ACCENT):
        super().__init__(master, fg_color=T.CARD, corner_radius=16,
                         border_width=1, border_color=T.BORDER)
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text=icon, font=fonts.h1, text_color=color).grid(
            row=0, column=0, sticky="w", padx=18, pady=(16, 0))
        self.value_lbl = ctk.CTkLabel(self, text=str(value), font=fonts.display, text_color=T.TEXT)
        self.value_lbl.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 0))
        ctk.CTkLabel(self, text=label, font=fonts.small, text_color=T.MUTED).grid(
            row=2, column=0, sticky="w", padx=18, pady=(0, 16))

    def set_value(self, value):
        self.value_lbl.configure(text=str(value))


class StrengthMeter(ctk.CTkFrame):
    """Анимированный индикатор надёжности пароля."""

    def __init__(self, master, fonts):
        super().__init__(master, fg_color="transparent")
        self.fonts = fonts
        self.grid_columnconfigure(0, weight=1)
        self.bar = ctk.CTkProgressBar(self, height=10, corner_radius=6,
                                      fg_color=T.ELEV, progress_color=T.ACCENT)
        self.bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self.bar.set(0)
        self.label = ctk.CTkLabel(self, text="—", font=fonts.body_bold, text_color=T.MUTED)
        self.label.grid(row=1, column=0, sticky="w")
        self._target = 0.0
        self._current = 0.0
        self._anim = None

    def update_strength(self, info: dict):
        color = T.STRENGTH_COLORS.get(info["level"], T.ACCENT)
        self.bar.configure(progress_color=color)
        self.label.configure(text=f"{info['label']}  ·  {info['score']}/5", text_color=color)
        self._target = info["percent"]
        self._animate()

    def _animate(self):
        if self._anim is not None:
            self.after_cancel(self._anim)
        step = (self._target - self._current)
        if abs(step) < 0.02:
            self._current = self._target
            self.bar.set(self._current)
            self._anim = None
            return
        self._current += step * 0.25
        self.bar.set(self._current)
        self._anim = self.after(16, self._animate)


class Toast:
    """Всплывающее уведомление, которое плавно въезжает и исчезает."""

    def __init__(self, app, fonts):
        self.app = app
        self.fonts = fonts
        self.frame = None
        self._hide_job = None

    def show(self, message, kind="success"):
        colors = {
            "success": T.GREEN,
            "info": T.ACCENT,
            "warn": T.YELLOW,
            "error": T.RED,
        }
        icons = {"success": "✓", "info": "ℹ", "warn": "⚠", "error": "✕"}
        color = colors.get(kind, T.ACCENT)
        if self.frame is not None:
            self.frame.destroy()
        if self._hide_job is not None:
            self.app.after_cancel(self._hide_job)

        self.frame = ctk.CTkFrame(self.app, fg_color=T.ELEV, corner_radius=12,
                                  border_width=1, border_color=color)
        ctk.CTkLabel(self.frame, text=icons.get(kind, "ℹ"), font=self.fonts.h3,
                     text_color=color).pack(side="left", padx=(14, 6), pady=12)
        ctk.CTkLabel(self.frame, text=message, font=self.fonts.body,
                     text_color=T.TEXT).pack(side="left", padx=(0, 16), pady=12)

        # плавное появление снизу
        self._y = 1.12
        self._slide_in()
        self._hide_job = self.app.after(2600, self._slide_out)

    def _slide_in(self):
        if self.frame is None:
            return
        self._y -= (self._y - 0.93) * 0.25
        self.frame.place(relx=0.5, rely=self._y, anchor="center")
        if abs(self._y - 0.93) > 0.005:
            self.app.after(16, self._slide_in)
        else:
            self.frame.place(relx=0.5, rely=0.93, anchor="center")

    def _slide_out(self):
        if self.frame is None:
            return
        self._y += 0.02 + (self._y - 0.93) * 0.3
        self.frame.place(relx=0.5, rely=self._y, anchor="center")
        if self._y < 1.15:
            self.app.after(16, self._slide_out)
        else:
            self.frame.destroy()
            self.frame = None


class SectionTitle(ctk.CTkFrame):
    """Заголовок раздела: крупный заголовок + подзаголовок."""

    def __init__(self, master, fonts, title, subtitle=""):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text=title, font=fonts.h1, text_color=T.TEXT,
                     anchor="w").grid(row=0, column=0, sticky="w")
        if subtitle:
            ctk.CTkLabel(self, text=subtitle, font=fonts.small, text_color=T.MUTED,
                         anchor="w").grid(row=1, column=0, sticky="w", pady=(2, 0))


def accent_button(master, text, command, fonts, color=T.ACCENT, hover=T.ACCENT_HOVER,
                  text_color="#06241f", width=140, height=42):
    """Яркая акцентная кнопка."""
    return ctk.CTkButton(master, text=text, command=command, font=fonts.body_bold,
                         fg_color=color, hover_color=hover, text_color=text_color,
                         corner_radius=10, width=width, height=height)


def ghost_button(master, text, command, fonts, width=140, height=42):
    """Вторичная кнопка с прозрачным фоном и границей."""
    return ctk.CTkButton(master, text=text, command=command, font=fonts.body_bold,
                         fg_color="transparent", hover_color=T.CARD_HOVER,
                         text_color=T.TEXT, border_width=1, border_color=T.BORDER,
                         corner_radius=10, width=width, height=height)
