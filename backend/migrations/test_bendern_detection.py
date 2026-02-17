#!/usr/bin/env python3
import sys
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

service = JobsChatService()

# Test city detection
messages = [
    "Шукаю роботу в Bendern",
    "Job in Bendern",
    "Bendern job",
    "work in bendern"
]

for msg in messages:
    city = service._extract_city_from_message(msg, 'LI')
    print(f"Message: '{msg}' -> City: {city}")
