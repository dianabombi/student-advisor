#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Amsterdam city detection - remove 'adam' variant
"""

import re

file_path = '/app/services/housing_chat_service.py'

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the line with 'adam'
# Old: 'amsterdam', 'ams', 'a\'dam', 'adam',
# New: 'amsterdam', 'ams', 'a\'dam',

old_pattern = r"'amsterdam', 'ams', 'a\\'dam', 'adam',"
new_pattern = "'amsterdam', 'ams', 'a\\'dam',"

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("✅ Found and replaced 'adam' variant")
else:
    print("⚠️ Pattern not found, trying alternative...")
    # Try without escaped quote
    old_pattern2 = "'amsterdam', 'ams', 'a'dam', 'adam',"
    new_pattern2 = "'amsterdam', 'ams', 'a'dam',"
    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
        print("✅ Found and replaced 'adam' variant (alternative)")
    else:
        print("❌ Could not find pattern")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File updated successfully")
