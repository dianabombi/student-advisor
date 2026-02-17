@echo off
chcp 65001 >nul
title Stop CODEX Platform

cd /d "%~dp0"

echo ========================================
echo    Stopping CODEX Platform
echo ========================================
echo.

docker compose down

echo.
echo CODEX Platform stopped.
echo.
pause
