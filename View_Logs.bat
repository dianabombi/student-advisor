@echo off
title CODEX Logs Viewer

echo ========================================
echo    CODEX Platform Logs
echo ========================================
echo.
echo Recent logs (press Ctrl+C to exit):
echo.

docker exec -it codex-backend-1 tail -f /app/logs/codex.log
