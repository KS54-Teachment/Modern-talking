#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Простой проверщик надёжности пароля.
Вспомогательный скрипт команды Modern Talking (Центр цифровой поддержки).

Использование:
    python3 password_checker.py "МойПароль123!"
"""
import sys
import re


def check_strength(password: str):
    score = 0
    notes = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        notes.append("Желательно не менее 12 символов")
    else:
        notes.append("Пароль слишком короткий")

    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    else:
        notes.append("Добавьте заглавные и строчные буквы")

    if re.search(r"\d", password):
        score += 1
    else:
        notes.append("Добавьте цифры")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        notes.append("Добавьте спецсимволы")

    levels = {0: "Очень слабый", 1: "Слабый", 2: "Средний",
              3: "Хороший", 4: "Надёжный", 5: "Очень надёжный"}
    return levels.get(score, "Надёжный"), notes


def main():
    if len(sys.argv) < 2:
        print("Укажите пароль аргументом.")
        sys.exit(1)
    pwd = sys.argv[1]
    level, notes = check_strength(pwd)
    print(f"Надёжность: {level}")
    for n in notes:
        print(f" - {n}")


if __name__ == "__main__":
    main()
