#!/usr/bin/env bash
# Массовое создание GitHub Issues для команды Modern Talking.
# Требуется GitHub CLI: https://cli.github.com/  ->  gh auth login
# Запуск:  bash scripts/create-issues.sh
set -e

REPO="KS54-Teachment/Modern-talking"

# Создаём метки приоритетов (игнорируем ошибку, если уже есть)
gh label create "priority:high"   --color FF0000 --repo "$REPO" 2>/dev/null || true
gh label create "priority:medium" --color FFCC00 --repo "$REPO" 2>/dev/null || true
gh label create "priority:low"    --color00CC00 --repo "$REPO" 2>/dev/null || true

create () {
  # $1 title, $2 body, $3 label
  gh issue create --repo "$REPO" --title "$1" --body "$2" --label "$3"
}

create "Создать структуру репозитория" "Папки: docs, excel, reports, presentations, security, python, design, knowledge-base. Срок: 03.06." "priority:high"
create "Оформить README.md" "Название команды, участники, роли, описание, технологии. Срок: 03.06." "priority:high"
create "Подготовить теорию по Git" "Определения 11 терминов. Срок: 04.06." "priority:medium"
create "Создать инструкцию по безопасности" "Памятка по ИБ и вредоносному ПО. Срок: 05.06." "priority:high"
create "Провести анализ угроз" "Анализ угроз вредоносного ПО. Срок: 06.06." "priority:high"
create "Подготовить FAQ" "Минимум 20 вопросов-ответов в knowledge-base. Срок: 05.06." "priority:medium"
create "Подготовить журнал обращений" "Excel-журнал обращений пользователей. Срок: 06.06." "priority:medium"
create "Создать логотип команды" "Логотип в PNG и SVG + описание идеи. Срок: 04.06." "priority:medium"
create "Подготовить кейс пользователя" "Кейс 3: случайное удаление данных. Срок: 05.06." "priority:high"
create "Оформить презентацию к защите" "5-7 минут, все пункты защиты. Срок: 06.06." "priority:medium"
create "Настроить GitHub Pages" "Опубликовать сайт проекта из /docs. Срок: 06.06." "priority:low"
create "Написать скрипт проверки пароля" "Python-скрипт password_checker.py. Срок: 04.06." "priority:low"

echo "Готово: создано 12 issues."
