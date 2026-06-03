# Modern Talking — День 3

### Совместная работа команды через Git и GitHub

![day3](https://img.shields.io/badge/Задание-День_3-blue) ![git](https://img.shields.io/badge/Git-GitHub-orange) ![case](https://img.shields.io/badge/Кейс_3-Случайное_удаление_данных-red)

Репозиторий команды **Modern Talking** для задания 3 дня: отработка командной работы через Git и GitHub: ветки, пул-реквесты, Issues, база знаний и страница проекта.

---

## 👥 Состав команды

| Участник | Роль | Ветка |
|----------|------|-------|
| Комиссаров Илья | 🧭 Лидер команды | `feature-lead` |
| Госани Айдар | 🛠️ Технический специалист | `feature-tech` |
| Чернов Матвей | 🛡️ Специалист по ИБ | `feature-security` |
| Яноха Денис | 🎧 Консультант | `feature-consultant` |
| Чирков Костя | 📝 Документатор | `feature-documentation` |

---

## 📁 Структура папки Day-3

```
Day-3/
├── README.md                  — этот файл (описание проекта)
├── ISSUES.md                  — список задач для GitHub Issues
├── docs/                      — документация и страница проекта
│   ├── index.html             — страница для GitHub Pages
│   ├── roles.md               — роли и зоны ответственности (RACI)
│   └── theory.md              — теория по Git и GitHub
├── knowledge-base/            — база знаний
│   └── README.md              — 22 вопроса-ответа (FAQ)
├── reports/                   — отчёты и разбор кейса
│   └── case-report.md         — Кейс 3: случайное удаление данных
├── security/                  — инструкции по безопасности
│   └── security-instructions.md
├── python/                    — код
│   └── password_checker.py    — проверка надёжности пароля
├── excel/                     — таблицы (журнал, источники)
├── presentations/             — презентация и план защиты
│   └── defense-plan.md
├── design/                    — логотип команды
│   └── logo.png
└── scripts/                   — вспомогательные скрипты
    └── create-issues.sh
```

---

## 🌿 Работа с ветками

Каждый участник работает в **своей ветке** и вливает изменения в `main` через Pull Request.

```bash
# создать свою ветку от main
git checkout main
git checkout -b feature-tech

# внести изменения, зафиксировать и отправить
git add .
git commit -m "Описание изменений"
git push -u origin feature-tech
```

Затем на GitHub: **Pull requests → New pull request** → base `main`, compare своя ветка → **Merge**.

---

## 🌐 Страница проекта (GitHub Pages)

Страница собрана в `docs/index.html`. Чтобы опубликовать:

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, папка `/Day-3/docs` (или перенесите `index.html` в корень `/docs`)
4. Страница откроется по адресу: `https://ks54-teachment.github.io/Modern-talking/`

---

## 💻 Запуск кода

```bash
cd Day-3/python
python3 password_checker.py
```

---

## 🎯 Кейс команды

**Кейс 3 — случайное удаление данных.** Разбор ситуации, причины, пошаговые действия по восстановлению и профилактика — в файле [`reports/case-report.md`](reports/case-report.md).

> Материалы по теме «Вредоносное ПО» относятся к Дню 2 и хранятся в папке `Day-2/`.

---

## ✅ Чек-лист задания

- [x] Структура репозитория по папкам
- [x] Ветки для каждого участника
- [x] База знаний (FAQ)
- [x] Разбор кейса
- [x] Логотип команды
- [x] Страница проекта (GitHub Pages)
- [ ] Issues созданы во вкладке Issues
- [ ] Pull-реквесты от каждого участника

---

*Команда Modern Talking · Центр цифровой поддержки · День 3*
