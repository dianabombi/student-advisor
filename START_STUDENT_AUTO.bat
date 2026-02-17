@echo off
chcp 65001 >nul
color 0A
title CODEX Platform Launcher

REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo    CODEX Platform - Auto Launch
echo ========================================
echo.

REM Step 1: Check Docker
echo [1/4] Checking Docker Desktop...
docker ps >nul 2>&1
if errorlevel 1 (
    echo    Docker is not running!
    echo.
    echo    Starting Docker Desktop...
    
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if not exist "%DOCKER_PATH%" (
        set "DOCKER_PATH=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    )
    if not exist "%DOCKER_PATH%" (
        set "DOCKER_PATH=%LOCALAPPDATA%\Programs\Docker\Docker\Docker Desktop.exe"
    )
    
    if not exist "%DOCKER_PATH%" (
        echo    Cannot find Docker Desktop!
        echo.
        echo    Please install Docker Desktop from:
        echo    https://www.docker.com/products/docker-desktop
        echo.
        goto :end
    )
    
    start "" "%DOCKER_PATH%"
    echo    Waiting for Docker to start...
    
    set /a counter=0
    :wait_docker
    timeout /t 5 /nobreak >nul
    docker ps >nul 2>&1
    if not errorlevel 1 goto :docker_ok
    
    set /a counter+=1
    if %counter% lss 24 (
        echo       ... waiting
        goto :wait_docker
    )
    
    echo    Docker did not start in 2 minutes
    echo    Try starting Docker manually and run this again
    goto :end
)

:docker_ok
echo    Docker is running!

REM Step 2: Check .env file
echo.
echo [2/4] Checking configuration...
if not exist ".env" (
    echo    .env file not found
    if exist ".env.example" (
        echo    Creating from .env.example...
        copy .env.example .env >nul
    ) else (
        echo    ERROR: .env.example not found!
        echo    Cannot create configuration file.
        goto :end
    )
)

findstr /C:"your_openai_key_here" .env >nul
if not errorlevel 1 (
    echo    WARNING: OpenAI API key not configured!
    echo    Edit .env and replace your_openai_key_here
    echo.
)

echo    Checking security keys...
findstr /C:"generate_random" .env >nul
if not errorlevel 1 (
    echo.
    echo    ⚠️  SECURITY WARNING: Using default keys!
    echo    Generate secure keys with:
    echo    openssl rand -hex 32
    echo.
)

echo    Security keys OK

REM Step 3: Start services
echo.
echo [3/4] Starting services...
docker compose up -d

if errorlevel 1 (
    echo    Error starting services!
    echo.
    echo    Try to fix:
    echo    1. Restart Docker Desktop
    echo    2. Run "docker compose down" and try again
    goto :end
)

echo    Services started!

REM Step 4: Wait for services
echo.
echo [4/4] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check status
docker compose ps

echo.
echo ========================================
echo    CODEX Platform is ready!
echo ========================================
echo.
echo Links:
echo    Frontend:  http://localhost:3001
echo    Backend:   http://localhost:8001/docs
echo    MinIO:     http://localhost:9003
echo.
echo Detailed instructions: README.md
echo.

REM Open browser
echo Opening browser...
start http://localhost:3001

echo.
echo Done! You can close this window.
echo.

:end
echo ========================================
echo Press any key to exit...
pause >nul
