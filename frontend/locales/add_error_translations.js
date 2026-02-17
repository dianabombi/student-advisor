const fs = require('fs');
const path = require('path');

// Error message translations
const errorTranslations = {
    sk: {
        "auth": {
            "register": {
                "error_name_required": "Prosím, zadajte vaše celé meno (meno a priezvisko)",
                "error_email_required": "Prosím, zadajte váš email",
                "error_password_required": "Prosím, zadajte heslo"
            }
        }
    },
    cs: {
        "auth": {
            "register": {
                "error_name_required": "Prosím, zadejte vaše celé jméno (jméno a příjmení)",
                "error_email_required": "Prosím, zadejte váš email",
                "error_password_required": "Prosím, zadejte heslo"
            }
        }
    },
    en: {
        "auth": {
            "register": {
                "error_name_required": "Please enter your full name (first and last name)",
                "error_email_required": "Please enter your email",
                "error_password_required": "Please enter a password"
            }
        }
    },
    uk: {
        "auth": {
            "register": {
                "error_name_required": "Будь ласка, введіть ваше повне ім'я (ім'я та прізвище)",
                "error_email_required": "Будь ласка, введіть ваш email",
                "error_password_required": "Будь ласка, введіть пароль"
            }
        }
    },
    pl: {
        "auth": {
            "register": {
                "error_name_required": "Proszę podać pełne imię i nazwisko",
                "error_email_required": "Proszę podać email",
                "error_password_required": "Proszę podać hasło"
            }
        }
    },
    de: {
        "auth": {
            "register": {
                "error_name_required": "Bitte geben Sie Ihren vollständigen Namen ein (Vor- und Nachname)",
                "error_email_required": "Bitte geben Sie Ihre E-Mail ein",
                "error_password_required": "Bitte geben Sie ein Passwort ein"
            }
        }
    },
    fr: {
        "auth": {
            "register": {
                "error_name_required": "Veuillez entrer votre nom complet (prénom et nom)",
                "error_email_required": "Veuillez entrer votre email",
                "error_password_required": "Veuillez entrer un mot de passe"
            }
        }
    },
    es: {
        "auth": {
            "register": {
                "error_name_required": "Por favor, ingrese su nombre completo (nombre y apellido)",
                "error_email_required": "Por favor, ingrese su email",
                "error_password_required": "Por favor, ingrese una contraseña"
            }
        }
    },
    it: {
        "auth": {
            "register": {
                "error_name_required": "Si prega di inserire il nome completo (nome e cognome)",
                "error_email_required": "Si prega di inserire l'email",
                "error_password_required": "Si prega di inserire una password"
            }
        }
    },
    ru: {
        "auth": {
            "register": {
                "error_name_required": "Пожалуйста, введите ваше полное имя (имя и фамилию)",
                "error_email_required": "Пожалуйста, введите ваш email",
                "error_password_required": "Пожалуйста, введите пароль"
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
Object.keys(errorTranslations).forEach(lang => {
    const filePath = path.join(__dirname, lang, 'common.json');

    try {
        // Read existing file
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const existingData = JSON.parse(fileContent);

        // Merge new translations
        const updatedData = deepMerge(existingData, errorTranslations[lang]);

        // Write back to file
        fs.writeFileSync(filePath, JSON.stringify(updatedData, null, 2), 'utf8');

        console.log(`✅ Updated ${lang}/common.json with error messages`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n🎉 All error message translations added successfully!');
