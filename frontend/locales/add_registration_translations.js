const fs = require('fs');
const path = require('path');

// Registration form translations for firstName and lastName
const registrationTranslations = {
    sk: {
        "auth": {
            "register": {
                "firstName": "Meno",
                "lastName": "Priezvisko",
                "placeholder_firstName": "Vaše meno",
                "placeholder_lastName": "Vaše priezvisko",
                "placeholder_confirm_password": "Potvrďte heslo"
            }
        }
    },
    cs: {
        "auth": {
            "register": {
                "firstName": "Jméno",
                "lastName": "Příjmení",
                "placeholder_firstName": "Vaše jméno",
                "placeholder_lastName": "Vaše příjmení",
                "placeholder_confirm_password": "Potvrďte heslo"
            }
        }
    },
    en: {
        "auth": {
            "register": {
                "firstName": "First Name",
                "lastName": "Last Name",
                "placeholder_firstName": "Your first name",
                "placeholder_lastName": "Your last name",
                "placeholder_confirm_password": "Confirm password"
            }
        }
    },
    uk: {
        "auth": {
            "register": {
                "firstName": "Ім'я",
                "lastName": "Прізвище",
                "placeholder_firstName": "Ваше ім'я",
                "placeholder_lastName": "Ваше прізвище",
                "placeholder_confirm_password": "Підтвердіть пароль"
            }
        }
    },
    pl: {
        "auth": {
            "register": {
                "firstName": "Imię",
                "lastName": "Nazwisko",
                "placeholder_firstName": "Twoje imię",
                "placeholder_lastName": "Twoje nazwisko",
                "placeholder_confirm_password": "Potwierdź hasło"
            }
        }
    },
    de: {
        "auth": {
            "register": {
                "firstName": "Vorname",
                "lastName": "Nachname",
                "placeholder_firstName": "Ihr Vorname",
                "placeholder_lastName": "Ihr Nachname",
                "placeholder_confirm_password": "Passwort bestätigen"
            }
        }
    },
    fr: {
        "auth": {
            "register": {
                "firstName": "Prénom",
                "lastName": "Nom",
                "placeholder_firstName": "Votre prénom",
                "placeholder_lastName": "Votre nom",
                "placeholder_confirm_password": "Confirmez le mot de passe"
            }
        }
    },
    es: {
        "auth": {
            "register": {
                "firstName": "Nombre",
                "lastName": "Apellido",
                "placeholder_firstName": "Tu nombre",
                "placeholder_lastName": "Tu apellido",
                "placeholder_confirm_password": "Confirmar contraseña"
            }
        }
    },
    it: {
        "auth": {
            "register": {
                "firstName": "Nome",
                "lastName": "Cognome",
                "placeholder_firstName": "Il tuo nome",
                "placeholder_lastName": "Il tuo cognome",
                "placeholder_confirm_password": "Conferma password"
            }
        }
    },
    ru: {
        "auth": {
            "register": {
                "firstName": "Имя",
                "lastName": "Фамилия",
                "placeholder_firstName": "Ваше имя",
                "placeholder_lastName": "Ваша фамилия",
                "placeholder_confirm_password": "Подтвердите пароль"
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
Object.keys(registrationTranslations).forEach(lang => {
    const filePath = path.join(__dirname, lang, 'common.json');

    try {
        // Read existing file
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const existingData = JSON.parse(fileContent);

        // Merge new translations
        const updatedData = deepMerge(existingData, registrationTranslations[lang]);

        // Write back to file
        fs.writeFileSync(filePath, JSON.stringify(updatedData, null, 2), 'utf8');

        console.log(`✅ Updated ${lang}/common.json with registration form translations`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n🎉 All registration translations added successfully!');
