@echo off
chcp 65001 >nul
color 0E
title Launch CODEX Platform

cd /d "%~dp0"

echo ========================================
echo    CODEX Platform Launcher
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo.
    echo Please start Docker Desktop first.
    echo.
    pause
    exit /b 1
)

echo Starting CODEX Platform...
echo.

docker compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    CODEX Platform Started!
    echo ========================================
    echo.
    echo Access the platform at:
    echo    http://localhost:3001
    echo.
    echo Opening browser...
    timeout /t 3 /nobreak >nul
    start http://localhost:3001
) else (
    echo.
    echo ERROR: Failed to start platform!
    echo Check the logs for details.
)

echo.
pause
