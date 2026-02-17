import json
import os

# Complete auth.login translations for all languages
auth_login_translations = {
    'ru': {
        "welcome": "Добро пожаловать",
        "subtitle": "Войдите в свой аккаунт",
        "success_registered": "Регистрация успешна! Теперь вы можете войти.",
        "error_invalid": "Неверный email или пароль",
        "error_connection": "Ошибка соединения. Проверьте, работает ли сервер.",
        "email": "Email",
        "placeholder_email": "your@email.com",
        "password": "Пароль",
        "placeholder_password": "Введите пароль",
        "button": "Войти",
        "button_loading": "Вход...",
        "no_account": "Нет аккаунта?",
        "register_link": "Зарегистрироваться",
        "title": "Вход",
        "submit": "Войти"
    },
    'en': {
        "welcome": "Welcome",
        "subtitle": "Sign in to your account",
        "success_registered": "Registration successful! You can now log in.",
        "error_invalid": "Invalid email or password",
        "error_connection": "Connection error. Please check if the server is running.",
        "email": "Email",
        "placeholder_email": "your@email.com",
        "password": "Password",
        "placeholder_password": "Enter password",
        "button": "Sign In",
        "button_loading": "Signing in...",
        "no_account": "Don't have an account?",
        "register_link": "Register",
        "title": "Login",
        "submit": "Sign In"
    },
    'sk': {
        "welcome": "Vitajte",
        "subtitle": "Prihláste sa do svojho účtu",
        "success_registered": "Registrácia úspešná! Teraz sa môžete prihlásiť.",
        "error_invalid": "Neplatný email alebo heslo",
        "error_connection": "Chyba pripojenia. Skontrolujte, či server beží.",
        "email": "Email",
        "placeholder_email": "your@email.com",
        "password": "Heslo",
        "placeholder_password": "Zadajte heslo",
        "button": "Prihlásiť sa",
        "button_loading": "Prihlasovanie...",
        "no_account": "Nemáte účet?",
        "register_link": "Zaregistrovať sa",
        "title": "Prihlásenie",
        "submit": "Prihlásiť sa"
    }
}

# Update only ru, en, sk (the 3 other languages in admin panel)
for lang_code in ['ru', 'en', 'sk']:
    file_path = f'frontend/locales/{lang_code}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update auth.login section
        if 'auth' not in data:
            data['auth'] = {}
        data['auth']['login'] = auth_login_translations[lang_code]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

print("\nAuth login translations updated for ru, en, sk!")
