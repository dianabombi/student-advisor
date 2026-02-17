$translations = @{
    'en' = @{ login = 'Login'; register = 'Register' }
    'sk' = @{ login = 'Prihlásenie'; register = 'Registrácia' }
    'cs' = @{ login = 'Přihlášení'; register = 'Registrace' }
    'pl' = @{ login = 'Logowanie'; register = 'Rejestracja' }
    'de' = @{ login = 'Anmelden'; register = 'Registrieren' }
    'fr' = @{ login = 'Connexion'; register = 'Inscription' }
    'es' = @{ login = 'Iniciar Sesión'; register = 'Registrarse' }
    'it' = @{ login = 'Accedi'; register = 'Registrati' }
    'uk' = @{ login = 'Вхід'; register = 'Реєстрація' }
    'ru' = @{ login = 'Вход'; register = 'Регистрация' }
}

foreach ($lang in $translations.Keys) {
    $file = "C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales\$lang\common.json"
    $content = Get-Content $file -Raw | ConvertFrom-Json
    
    # Add simple auth keys
    $content.auth | Add-Member -NotePropertyName 'loginButton' -NotePropertyValue $translations[$lang].login -Force
    $content.auth | Add-Member -NotePropertyName 'registerButton' -NotePropertyValue $translations[$lang].register -Force
    
    # Save back
    $content | ConvertTo-Json -Depth 10 | Set-Content $file -Encoding UTF8
}

Write-Host "✅ Added auth.loginButton and auth.registerButton to all 10 languages!"
