@echo off
title CODEX Health Check

echo ========================================
echo    CODEX Health Check
echo ========================================
echo.

echo Basic health:
curl -s http://localhost:8001/health | python -m json.tool
echo.
echo.

echo Detailed health:
curl -s http://localhost:8001/health/detailed | python -m json.tool

echo.
pause
