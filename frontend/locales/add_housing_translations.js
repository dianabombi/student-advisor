const fs = require('fs');
const path = require('path');

// Housing search button translations for all 10 languages
const housingTranslations = {
    sk: {
        "student": {
            "hero": {
                "searchHousing": "Hľadať Ubytovanie"
            }
        }
    },
    cs: {
        "student": {
            "hero": {
                "searchHousing": "Hledat Ubytování"
            }
        }
    },
    en: {
        "student": {
            "hero": {
                "searchHousing": "Search Housing"
            }
        }
    },
    uk: {
        "student": {
            "hero": {
                "searchHousing": "Шукати Житло"
            }
        }
    },
    pl: {
        "student": {
            "hero": {
                "searchHousing": "Szukaj Zakwaterowania"
            }
        }
    },
    de: {
        "student": {
            "hero": {
                "searchHousing": "Unterkunft Suchen"
            }
        }
    },
    fr: {
        "student": {
            "hero": {
                "searchHousing": "Chercher Logement"
            }
        }
    },
    es: {
        "student": {
            "hero": {
                "searchHousing": "Buscar Alojamiento"
            }
        }
    },
    it: {
        "student": {
            "hero": {
                "searchHousing": "Cerca Alloggio"
            }
        }
    },
    ru: {
        "student": {
            "hero": {
                "searchHousing": "Искать Жилье"
            }
        }
    }
};

// Function to deep merge objects
function deepMerge(target, source) {
    for (const key in source) {
        if (source[key] instanceof Object && key in target) {
            Object.assign(source[key], deepMerge(target[key], source[key]));
        }
    }
    Object.assign(target || {}, source);
    return target;
}

// Update each language file
Object.keys(housingTranslations).forEach(lang => {
    const filePath = path.join(__dirname, lang, 'common.json');

    try {
        // Read existing file
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const existingData = JSON.parse(fileContent);

        // Merge new translations
        const updatedData = deepMerge(existingData, housingTranslations[lang]);

        // Write back to file
        fs.writeFileSync(filePath, JSON.stringify(updatedData, null, 2), 'utf8');

        console.log(`✅ Updated ${lang}/common.json with housing search translations`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n🎉 All language files updated successfully!');
