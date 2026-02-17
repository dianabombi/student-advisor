#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Amsterdam city detection - remove 'adam' variant (CORRECT VERSION)
"""

file_path = '/app/services/housing_chat_service.py'

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 415 and replace it
for i, line in enumerate(lines):
    if i == 414:  # Line 415 (0-indexed)
        print(f"Old line {i+1}: {line.strip()}")
        # Replace the line
        lines[i] = "                'amsterdam', 'ams', 'a\\'dam',\n"
        print(f"New line {i+1}: {lines[i].strip()}")
        break

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ File updated successfully - 'adam' removed from Amsterdam variants")
