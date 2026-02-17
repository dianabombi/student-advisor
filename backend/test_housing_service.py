#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test housing chat service directly"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.housing_chat_service import HousingChatService
from main import get_db

# Create service
service = HousingChatService()

# Get database session
db = next(get_db())

# Test city extraction
print("Testing city extraction...")
test_messages = [
    ("Ищу общежитие в Лондоне", "GB"),
    ("Шукаю гуртожиток в Лондоні", "GB"),
    ("Hľadám byt v Londine", "GB"),
    ("Looking for housing in Liverpool", "GB"),
]

for message, country in test_messages:
    city = service._extract_city_from_message(message, country)
    print(f"  '{message}' -> {city}")

# Test agencies context
print("\n\nTesting agencies context for London...")
try:
    context = service._get_agencies_context(db, "London", "GB")
    print(f"Context length: {len(context)} chars")
    print(f"First 500 chars:\n{context[:500]}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

db.close()
