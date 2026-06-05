# project/ — исходный код ИТ-продукта

**DIGITAL SUPPORT** — настольное приложение цифрового куратора (команда Modern Talking).

## Запуск

```bash
python digital_support.py
```

Требования: Python 3.8+ (tkinter — в стандартной библиотеке).

## Функции

1. Генератор надёжных паролей (модуль `secrets`).
2. Анализатор надёжности пароля (6 критериев).
3. Журнал обращений (хранение в `requests.json`).

## Исправление ошибки (changelog)

### Было
```python
self._w, self._h = width, height   # ⛔ self._w — служебный атрибут tkinter!
...
round_rect(self, 2, 2, self._w - 2, self._h - 2, 12, ...)
self.create_text(self._w / 2, self._h / 2, ...)
```
В tkinter `self._w` — это внутреннее имя (Tcl-путь) виджета. Присваивая
`self._w = 170`, мы затирали это имя. При вызове `self.delete("all")` tkinter
выполняет `self.tk.call((self._w, 'delete', 'all'))`, то есть обращается
к команде с именем `170`, которой не существует →
`_tkinter.TclError: invalid command name "170"`.

### Стало
```python
self._cw, self._ch = width, height   # ✅ собственные имена, не конфликтуют
round_rect(self, 2, 2, self._cw - 2, self._ch - 2, 12, ...)
self.create_text(self._cw / 2, self._ch / 2, ...)
```

Вывод: никогда не используйте имя `_w` (и другие служебные атрибуты)
для собственных данных в классах-наследниках виджетов tkinter.
