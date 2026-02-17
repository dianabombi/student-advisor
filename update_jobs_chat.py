#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update jobs_chat_service.py - add instructions to agency context
"""

import re
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Read file
with open('backend/services/jobs_chat_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Old code to replace
old_code = '''            # Format agencies data for AI context
            context = f"VERIFIED JOB AGENCIES IN {city.upper()}:\\n\\n"
            for agency in agencies:
                context += f"• {agency.name}\\n"
                context += f"  Website: {agency.website_url}\\n"
                if agency.description:
                    context += f"  Description: {agency.description}\\n"
                if agency.specialization:
                    context += f"  Specialization: {agency.specialization}\\n"
                if agency.phone:
                    context += f"  Phone: {agency.phone}\\n"
                if agency.email:
                    context += f"  Email: {agency.email}\\n"
                context += "\\n"'''

# New code
new_code = '''            # Format agencies data for AI context WITH INSTRUCTIONS
            context = f"VERIFIED JOB AGENCIES IN {city.upper()}:\\n\\n"
            context += "IMPORTANT: These are main portal pages. Users must search on the portal themselves.\\n\\n"
            
            for agency in agencies:
                context += f"• {agency.name}\\n"
                context += f"  Website: {agency.website_url}\\n"
                
                # Add search instructions based on portal type
                portal_name = agency.name.lower()
                if 'profesia' in portal_name:
                    context += f"  Instructions: Open the website, enter '{city}' in location field, select 'Brigada/Dohoda' filter\\n"
                elif 'studentjob' in portal_name or 'brigada' in portal_name:
                    context += f"  Instructions: Open the website, search for '{city}', browse available student jobs\\n"
                elif 'kariera' in portal_name:
                    context += f"  Instructions: Open the website, select region '{city}', filter by 'Part-time/Brigada'\\n"
                elif 'grafton' in portal_name or 'manpower' in portal_name:
                    context += f"  Instructions: Open the website, use search to find jobs in '{city}'\\n"
                else:
                    context += f"  Instructions: Open the website and search for jobs in '{city}'\\n"
                
                if agency.description:
                    context += f"  Description: {agency.description}\\n"
                if agency.specialization:
                    context += f"  Specialization: {agency.specialization}\\n"
                context += "\\n"
            
            context += "\\nREMINDER: Tell users they need to search on the portal themselves after opening the link.\\n"'''

# Replace
if old_code in content:
    content = content.replace(old_code, new_code)
    print("SUCCESS: Code replaced!")
else:
    print("ERROR: Old code not found. Trying alternative approach...")
    # Alternative approach - search by pattern
    pattern = r'# Format agencies data for AI context\s+context = f"VERIFIED JOB AGENCIES.*?context \+= "\\n"'
    if re.search(pattern, content, re.DOTALL):
        print("SUCCESS: Pattern found for replacement")
        content = re.sub(pattern, new_code.strip(), content, flags=re.DOTALL)
    else:
        print("ERROR: Could not find code to replace")
        sys.exit(1)

# Write back
with open('backend/services/jobs_chat_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: File updated!")
print("Now restart backend: docker restart student-backend-1")
