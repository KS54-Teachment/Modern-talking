# Инструкция по работе с Git (Задание 2)

Каждый участник выполняет полный цикл: clone → branch → изменения → commit → push → Pull Request.

## 0. Подготовка (один раз)

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "you@example.com"
```

## 1. Клонировать репозиторий

```bash
git clone https://github.com/KS54-Teachment/Modern-talking.git
cd Modern-talking
```

## 2. Создать собственную ветку

Название ветки — по роли участника:

```bash
git checkout -b feature-security      # Security-инженер
# git checkout -b feature-consultant  # Консультант
# git checkout -b feature-documentation
# git checkout -b feature-excel
# git checkout -b feature-design
```

## 3. Внести изменения

Отредактируйте или добавьте файлы в свою папку (например, `security/`).

## 4. Commit

```bash
git add .
git commit -m "feat(security): добавлена инструкция по защите от вредоносного ПО"
```

Хороший commit: короткий смысл в заголовке, настоящее время, по делу.

## 5. Push

```bash
git push origin feature-security
```

## 6. Pull Request

1. Откройте репозиторий на GitHub — появится кнопка **Compare & pull request**.
2. Базовая ветка: `main`, сравниваемая: ваша `feature-…`.
3. Заполните заголовок и описание, назначьте reviewer'а.
4. После одобрения — **Merge pull request**.

## Полезные команды

```bash
git status            # текущее состояние
git log --oneline     # история коммитов
git pull origin main  # подтянуть изменения из main
git branch            # список веток
git merge main        # влить main в свою ветку (разрешить конфликты)
```

## Разрешение конфликтов

1. После `git merge`/`git pull` Git помечает конфликтные участки `<<<<<<<`, `=======`, `>>>>>>>`.
2. Вручную выберите нужный вариант, удалите маркеры.
3. `git add <файл>` → `git commit`.
