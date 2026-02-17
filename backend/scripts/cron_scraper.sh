#!/bin/bash
# Weekly University Scraper Cron Job
# Runs every Sunday at 2:00 AM

# Set environment
export PYTHONIOENCODING=utf-8
export DATABASE_URL="${DATABASE_URL:-postgresql://user:password@db:5432/codex_db}"

# Log file
LOG_FILE="/var/log/university_scraper.log"

# Run scraper
echo "=== University Scraper Started: $(date) ===" >> "$LOG_FILE"
cd /app/backend/scripts
python scrape_universities.py --all >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "=== Scraper Completed Successfully: $(date) ===" >> "$LOG_FILE"
else
    echo "=== Scraper Failed with exit code $EXIT_CODE: $(date) ===" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
