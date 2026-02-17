@echo off
title CODEX OpenAI Costs

echo ========================================
echo    OpenAI API Calls (Last 50)
echo ========================================
echo.

docker exec -it codex-backend-1 grep "\"event\": \"openai" /app/logs/codex.log | tail -50
echo.
pause
