"""
ЦифроКуратор — настольное приложение цифрового куратора.
Команда Modern Talking · День 6 (Python).

Современный GUI на customtkinter: боковое меню, скруглённые карточки,
анимации (заставка, всплывающие уведомления, индикатор надёжности).

Запуск:  python app.py
"""

import sys

# --- Проверка зависимостей до импорта GUI -------------------------------
try:
    import customtkinter as ctk
except ImportError:
    msg = (
        "Для запуска нужна библиотека customtkinter.\n\n"
        "Установите её командой:\n    pip install customtkinter\n\n"
        "Затем снова запустите:  python app.py"
    )
    print(msg)
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Не хватает библиотеки", msg)
    except Exception:
        pass
    sys.exit(1)

import theme as T
import logic as L
from theme import Fonts
from widgets import NavButton, Toast
from views import VIEW_REGISTRY


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title(f"{L.APP_NAME} — {L.TEAM_NAME}")
        self.geometry("1060x720")
        self.minsize(900, 600)
        self.configure(fg_color=T.BG)

        self.fonts = Fonts(ctk)
        self.store = L.AppealsStore()
        self.toast = Toast(self, self.fonts)
        self.nav_buttons = {}
        self.views = {}
        self.current = None

        # Скрываем главное окно и показываем заставку
        self.withdraw()
        self._build_layout()
        self._show_splash()

    # ----------------------------------------------------------------- Макет
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель
        sidebar = ctk.CTkFrame(self, fg_color=T.SIDEBAR, corner_radius=0, width=240)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(99, weight=1)

        # Логотип
        logo = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 18))
        ctk.CTkLabel(logo, text="◈", font=self.fonts.h1, text_color=T.ACCENT).pack(side="left")
        title_box = ctk.CTkFrame(logo, fg_color="transparent")
        title_box.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(title_box, text=L.APP_NAME, font=self.fonts.h2,
                     text_color=T.TEXT).pack(anchor="w")
        ctk.CTkLabel(title_box, text=L.TEAM_NAME, font=self.fonts.tiny,
                     text_color=T.ACCENT).pack(anchor="w")

        # Кнопки навигации
        for i, (key, icon, label, _cls) in enumerate(VIEW_REGISTRY):
            btn = NavButton(sidebar, label, icon, lambda k=key: self.show_view(k), self.fonts.nav)
            btn.grid(row=1 + i, column=0, sticky="ew", padx=12, pady=2)
            self.nav_buttons[key] = btn

        # Нижняя подпись
        ctk.CTkLabel(sidebar, text=f"v{L.APP_VERSION} · День 6 Python", font=self.fonts.tiny,
                     text_color=T.FAINT).grid(row=100, column=0, sticky="w", padx=24, pady=16)

        # Область контента
        self.content = ctk.CTkFrame(self, fg_color=T.BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=28, pady=24)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    # --------------------------------------------------------------- Заставка
    def _show_splash(self):
        splash = ctk.CTkToplevel(self)
        splash.overrideredirect(True)
        splash.configure(fg_color=T.BG)
        w, h = 460, 300
        sw = splash.winfo_screenwidth()
        sh = splash.winfo_screenheight()
        splash.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        try:
            splash.attributes("-alpha", 0.0)
        except Exception:
            pass

        frame = ctk.CTkFrame(splash, fg_color=T.CARD, corner_radius=20,
                             border_width=1, border_color=T.BORDER)
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(frame, text="◈", font=ctk.CTkFont(T.UI_FAMILY, size=64, weight="bold"),
                     text_color=T.ACCENT).pack(pady=(54, 6))
        ctk.CTkLabel(frame, text=L.APP_NAME, font=ctk.CTkFont(T.UI_FAMILY, size=30, weight="bold"),
                     text_color=T.TEXT).pack()
        ctk.CTkLabel(frame, text=f"Команда {L.TEAM_NAME}", font=self.fonts.body,
                     text_color=T.MUTED).pack(pady=(2, 22))
        bar = ctk.CTkProgressBar(frame, width=300, height=6, corner_radius=4,
                                 fg_color=T.ELEV, progress_color=T.ACCENT)
        bar.pack()
        bar.set(0)

        state = {"alpha": 0.0, "progress": 0.0}

        def fade_in():
            state["alpha"] = min(1.0, state["alpha"] + 0.08)
            try:
                splash.attributes("-alpha", state["alpha"])
            except Exception:
                pass
            if state["alpha"] < 1.0:
                self.after(16, fade_in)
            else:
                load()

        def load():
            state["progress"] = min(1.0, state["progress"] + 0.025)
            bar.set(state["progress"])
            if state["progress"] < 1.0:
                self.after(16, load)
            else:
                self.after(250, fade_out)

        def fade_out():
            state["alpha"] = max(0.0, state["alpha"] - 0.1)
            try:
                splash.attributes("-alpha", state["alpha"])
            except Exception:
                pass
            if state["alpha"] > 0:
                self.after(16, fade_out)
            else:
                splash.destroy()
                self._reveal_main()

        self.after(60, fade_in)

    def _reveal_main(self):
        self.deiconify()
        self.show_view("dashboard")
        try:
            self.attributes("-alpha", 0.0)
            a = {"v": 0.0}

            def fade():
                a["v"] = min(1.0, a["v"] + 0.1)
                self.attributes("-alpha", a["v"])
                if a["v"] < 1.0:
                    self.after(16, fade)
            fade()
        except Exception:
            pass

    # ------------------------------------------------------- Переключение экранов
    def show_view(self, key):
        if key not in self.views:
            cls = dict((k, c) for k, _i, _l, c in VIEW_REGISTRY)[key]
            self.views[key] = cls(self.content, self)
        view = self.views[key]

        if self.current is not None and self.current is not view:
            self.current.grid_forget()
        view.grid(row=0, column=0, sticky="nsew")
        self.current = view

        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)

        if hasattr(view, "on_show"):
            view.on_show()
        self._animate_view_in(view)

    def _animate_view_in(self, view):
        """Лёгкое появление экрана (fade через шаги)."""
        # Смягчённая имитация появления: сдвигаем отступ сверху.
        steps = [18, 12, 7, 3, 0]
        def step(i=0):
            if i < len(steps):
                view.grid_configure(pady=(steps[i], 0))
                self.after(16, lambda: step(i + 1))
        step()

    # ----------------------------------------------------------------- Утилиты
    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
