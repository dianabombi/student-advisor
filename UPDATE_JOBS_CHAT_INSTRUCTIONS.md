# Інструкції для оновлення jobs_chat_service.py

## Що потрібно змінити

У методі `_get_agencies_context` (рядки 203-248) додати інструкції для кожного порталу.

### Старий код (рядок 230-242):
```python
# Format agencies data for AI context
context = f"VERIFIED JOB AGENCIES IN {city.upper()}:\n\n"
for agency in agencies:
    context += f"• {agency.name}\n"
    context += f"  Website: {agency.website_url}\n"
    if agency.description:
        context += f"  Description: {agency.description}\n"
    if agency.specialization:
        context += f"  Specialization: {agency.specialization}\n"
    if agency.phone:
        context += f"  Phone: {agency.phone}\n"
    if agency.email:
        context += f"  Email: {agency.email}\n"
    context += "\n"
```

### Новий код:
```python
# Format agencies data for AI context WITH INSTRUCTIONS
context = f"VERIFIED JOB AGENCIES IN {city.upper()}:\n\n"
context += "IMPORTANT: These are main portal pages. Users must search on the portal themselves.\n\n"

for agency in agencies:
    context += f"• {agency.name}\n"
    context += f"  Website: {agency.website_url}\n"
    
    # Add search instructions based on portal type
    portal_name = agency.name.lower()
    if 'profesia' in portal_name:
        context += f"  Instructions: Open the website, enter '{city}' in location field, select 'Brigáda/Dohoda' filter\n"
    elif 'studentjob' in portal_name or 'brigada' in portal_name:
        context += f"  Instructions: Open the website, search for '{city}', browse available student jobs\n"
    elif 'kariera' in portal_name:
        context += f"  Instructions: Open the website, select region '{city}', filter by 'Part-time/Brigáda'\n"
    elif 'grafton' in portal_name or 'manpower' in portal_name:
        context += f"  Instructions: Open the website, use search to find jobs in '{city}'\n"
    else:
        context += f"  Instructions: Open the website and search for jobs in '{city}'\n"
    
    if agency.description:
        context += f"  Description: {agency.description}\n"
    if agency.specialization:
        context += f"  Specialization: {agency.specialization}\n"
    context += "\n"

context += "\nREMINDER: Tell users they need to search on the portal themselves after opening the link.\n"
```

## Як застосувати

Відкрий файл `backend/services/jobs_chat_service.py` та замін рядки 230-242 на новий код вище.
