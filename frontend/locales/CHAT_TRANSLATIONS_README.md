# Chat Translations - Manual Integration Guide

## Overview
This file contains chat translations for all supported languages that need to be manually added to the respective `common.json` files.

## Instructions

### For each language file (`sk/common.json`, `en/common.json`, `uk/common.json`, `ru/common.json`):

1. Open the file
2. Find the `"common"` section (usually at the end)
3. **Before** the `"common"` section, add the `"chat"` section from `chat_translations.json`
4. Ensure proper JSON formatting (commas between sections)

## Example Structure

```json
{
    "menu": { ... },
    "auth": { ... },
    "dashboard": { ... },
    "upload": { ... },
    "ai": { ... },
    "footer": { ... },
    "landing": { ... },
    "chat": {
        "title": "...",
        "welcome": "...",
        ...
    },
    "common": {
        "back": "...",
        "loading": "...",
        ...
    }
}
```

## Files to Update

1. `frontend/locales/sk/common.json` - Add Slovak chat translations
2. `frontend/locales/en/common.json` - Add English chat translations
3. `frontend/locales/uk/common.json` - Add Ukrainian chat translations
4. `frontend/locales/ru/common.json` - Add Russian chat translations

## Verification

After adding translations, verify:
- ✅ JSON is valid (no syntax errors)
- ✅ All translations are present
- ✅ Chat interface displays translated text
- ✅ Language switcher works correctly

## Alternative: Automated Script

You can also use this Node.js script to automatically merge translations:

```javascript
const fs = require('fs');
const path = require('path');

const chatTranslations = require('./chat_translations.json');
const languages = ['sk', 'en', 'uk', 'ru'];

languages.forEach(lang => {
    const filePath = path.join(__dirname, lang, 'common.json');
    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    
    // Add chat translations
    content.chat = chatTranslations[lang].chat;
    
    // Write back
    fs.writeFileSync(filePath, JSON.stringify(content, null, 4));
    console.log(`✅ Updated ${lang}/common.json`);
});
```

## Current Status

- ✅ Translations created for all 4 languages
- ⏳ Manual integration needed
- ⏳ Testing required after integration
