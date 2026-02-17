@echo off
chcp 65001 >nul
color 0B
title Student Platform Launcher

REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo    Student Platform - Quick Launch
echo ========================================
echo.

REM Check if Docker is running
echo Checking Docker...
docker ps >nul 2>&1
if errorlevel 1 (
    echo Docker is not running!
    echo Please start Docker Desktop first.
    echo.
    pause
    exit /b 1
)

echo Docker is running!
echo.

REM Start services
echo Starting Student platform...
docker compose up -d

if errorlevel 1 (
    echo Error starting services!
    pause
    exit /b 1
)

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo    Student Platform is ready!
echo ========================================
echo.
echo Open in browser: http://localhost:3001
echo.

REM Open browser
start http://localhost:3002

echo.
echo Platform is running!
echo Close this window when done.
echo.
pause
