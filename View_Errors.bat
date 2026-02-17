@echo off
title CODEX Error Logs

echo ========================================
echo    CODEX Error Logs (Last 20)
echo ========================================
echo.

docker exec -it codex-backend-1 grep "\"level\": \"error\"" /app/logs/codex.log | tail -20
echo.
pause
