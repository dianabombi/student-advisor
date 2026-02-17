@echo off
chcp 65001 >nul
title View CODEX Logs

cd /d "%~dp0"

echo ========================================
echo    CODEX Platform Logs
echo ========================================
echo.
echo Press Ctrl+C to exit logs view
echo.

docker compose logs -f
