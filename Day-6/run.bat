@echo off
chcp 65001 >nul
REM === ЦифроКуратор — запуск (Windows) ===
REM Команда Modern Talking

cd /d "%~dp0"

echo Проверка зависимостей...
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo Устанавливаю customtkinter...
    python -m pip install --upgrade pip
    python -m pip install customtkinter
)

echo Запуск приложения...
python app.py

if errorlevel 1 (
    echo.
    echo Произошла ошибка. Убедитесь, что установлен Python 3.10+.
    pause
)
