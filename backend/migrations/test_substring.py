#!/usr/bin/env python3
# -*- coding: utf-8 -*-

message = "Шукаю роботу в Bendern"
message_lower = message.lower()

variants = ['bendern', 'бендерн', 'бендерні']

print(f"Message: '{message}'")
print(f"Message lower: '{message_lower}'")
print()

for variant in variants:
    found = variant in message_lower
    print(f"'{variant}' in message_lower: {found}")
