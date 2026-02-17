@echo off
chcp 65001 >nul
title CODEX Health Monitor

echo ========================================
echo    🤖 CODEX Health Monitor Lite
echo ========================================
echo.

REM Перевірка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.8+
    pause
    exit /b 1
)

REM Встановлення залежностей
echo 📦 Installing dependencies...
pip install psutil requests >nul 2>&1

echo.
echo ========================================
echo    Monitor Starting
echo ========================================
echo.
echo 📊 Dashboard will be at:
echo    http://localhost:8000/monitor
echo.
echo 📝 Logs saved to: monitor_logs.json
echo.
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

REM Запуск монітора
python health_monitor_lite.py

pause
