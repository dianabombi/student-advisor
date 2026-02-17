import json
import os

# Auth translations for all languages
auth_translations = {
    'uk': {
        "auth": {
            "login": {
                "title": "Вхід",
                "subtitle": "Увійдіть до свого облікового запису",
                "submit": "Увійти"
            }
        }
    },
    'ru': {
        "auth": {
            "login": {
                "title": "Вход",
                "subtitle": "Войдите в свой аккаунт",
                "submit": "Войти"
            }
        }
    },
    'en': {
        "auth": {
            "login": {
                "title": "Login",
                "subtitle": "Sign in to your account",
                "submit": "Sign In"
            }
        }
    },
    'de': {
        "auth": {
            "login": {
                "title": "Anmelden",
                "subtitle": "Melden Sie sich bei Ihrem Konto an",
                "submit": "Anmelden"
            }
        }
    },
    'fr': {
        "auth": {
            "login": {
                "title": "Connexion",
                "subtitle": "Connectez-vous à votre compte",
                "submit": "Se connecter"
            }
        }
    },
    'es': {
        "auth": {
            "login": {
                "title": "Iniciar sesión",
                "subtitle": "Inicie sesión en su cuenta",
                "submit": "Iniciar sesión"
            }
        }
    },
    'it': {
        "auth": {
            "login": {
                "title": "Accedi",
                "subtitle": "Accedi al tuo account",
                "submit": "Accedi"
            }
        }
    },
    'pl': {
        "auth": {
            "login": {
                "title": "Logowanie",
                "subtitle": "Zaloguj się do swojego konta",
                "submit": "Zaloguj się"
            }
        }
    },
    'cs': {
        "auth": {
            "login": {
                "title": "Přihlášení",
                "subtitle": "Přihlaste se ke svému účtu",
                "submit": "Přihlásit se"
            }
        }
    },
    'sk': {
        "auth": {
            "login": {
                "title": "Prihlásenie",
                "subtitle": "Prihláste sa do svojho účtu",
                "submit": "Prihlásiť sa"
            }
        }
    },
    'pt': {
        "auth": {
            "login": {
                "title": "Entrar",
                "subtitle": "Entre na sua conta",
                "submit": "Entrar"
            }
        }
    }
}

# Update all language files
locales_dir = 'frontend/locales'

for lang_code, translations in auth_translations.items():
    file_path = os.path.join(locales_dir, lang_code, 'common.json')
    
    try:
        # Read existing translations
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add auth section
        data['auth'] = translations['auth']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

print("\nAll auth translations added!")
