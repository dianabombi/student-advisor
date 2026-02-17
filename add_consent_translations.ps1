# PowerShell script to add consent translations to all 10 language files

$consentTranslations = @{
    'sk' = @{
        title = "⚠️ Povinné potvrdenie"
        ai_tool = "Rozumiem, že CODEX je AI nástroj, NIE právnik"
        no_advice = "Rozumiem, že CODEX NEPOSKYTUJE právne poradenstvo"
        no_attorney = "Rozumiem, že používanie CODEX NEVYTVÁRA vzťah klient-advokát"
        error = "Musíte potvrdiť všetky potvrdenia pre registráciu"
        required = "Všetky potvrdenia sú povinné"
    }
    'en' = @{
        title = "⚠️ Mandatory Acknowledgment"
        ai_tool = "I understand CODEX is an AI tool, NOT a lawyer"
        no_advice = "I understand CODEX does NOT provide legal advice"
        no_attorney = "I understand using CODEX does NOT create attorney-client relationship"
        error = "You must accept all acknowledgments to register"
        required = "All acknowledgments are mandatory"
    }
    'uk' = @{
        title = "⚠️ Обов'язкове підтвердження"
        ai_tool = "Я розумію, що CODEX - це AI інструмент, а НЕ юрист"
        no_advice = "Я розумію, що CODEX НЕ надає юридичних порад"
        no_attorney = "Я розумію, що використання CODEX НЕ створює відносин клієнт-адвокат"
        error = "Ви повинні прийняти всі підтвердження для реєстрації"
        required = "Всі підтвердження обов'язкові"
    }
    'ru' = @{
        title = "⚠️ Обязательное подтверждение"
        ai_tool = "Я понимаю, что CODEX - это AI инструмент, а НЕ юрист"
        no_advice = "Я понимаю, что CODEX НЕ предоставляет юридических консультаций"
        no_attorney = "Я понимаю, что использование CODEX НЕ создает отношений клиент-адвокат"
        error = "Вы должны принять все подтверждения для регистрации"
        required = "Все подтверждения обязательны"
    }
    'de' = @{
        title = "⚠️ Obligatorische Bestätigung"
        ai_tool = "Ich verstehe, dass CODEX ein KI-Tool ist, KEIN Anwalt"
        no_advice = "Ich verstehe, dass CODEX KEINE Rechtsberatung bietet"
        no_attorney = "Ich verstehe, dass die Nutzung von CODEX KEIN Mandatsverhältnis begründet"
        error = "Sie müssen alle Bestätigungen akzeptieren, um sich zu registrieren"
        required = "Alle Bestätigungen sind obligatorisch"
    }
    'it' = @{
        title = "⚠️ Riconoscimento obbligatorio"
        ai_tool = "Comprendo che CODEX è uno strumento AI, NON un avvocato"
        no_advice = "Comprendo che CODEX NON fornisce consulenza legale"
        no_attorney = "Comprendo che l'uso di CODEX NON crea un rapporto avvocato-cliente"
        error = "Devi accettare tutti i riconoscimenti per registrarti"
        required = "Tutti i riconoscimenti sono obbligatori"
    }
    'fr' = @{
        title = "⚠️ Reconnaissance obligatoire"
        ai_tool = "Je comprends que CODEX est un outil IA, PAS un avocat"
        no_advice = "Je comprends que CODEX NE fournit PAS de conseils juridiques"
        no_attorney = "Je comprends que l'utilisation de CODEX NE crée PAS de relation avocat-client"
        error = "Vous devez accepter toutes les reconnaissances pour vous inscrire"
        required = "Toutes les reconnaissances sont obligatoires"
    }
    'es' = @{
        title = "⚠️ Reconocimiento obligatorio"
        ai_tool = "Entiendo que CODEX es una herramienta de IA, NO un abogado"
        no_advice = "Entiendo que CODEX NO proporciona asesoramiento legal"
        no_attorney = "Entiendo que el uso de CODEX NO crea una relación abogado-cliente"
        error = "Debe aceptar todos los reconocimientos para registrarse"
        required = "Todos los reconocimientos son obligatorios"
    }
    'pl' = @{
        title = "⚠️ Obowiązkowe potwierdzenie"
        ai_tool = "Rozumiem, że CODEX to narzędzie AI, a NIE prawnik"
        no_advice = "Rozumiem, że CODEX NIE świadczy porad prawnych"
        no_attorney = "Rozumiem, że korzystanie z CODEX NIE tworzy relacji klient-adwokat"
        error = "Musisz zaakceptować wszystkie potwierdzenia, aby się zarejestrować"
        required = "Wszystkie potwierdzenia są obowiązkowe"
    }
    'cs' = @{
        title = "⚠️ Povinné potvrzení"
        ai_tool = "Rozumím, že CODEX je AI nástroj, NIKOLI právník"
        no_advice = "Rozumím, že CODEX NEPOSKYTUJE právní poradenství"
        no_attorney = "Rozumím, že používání CODEX NEVYTVÁŘÍ vztah klient-advokát"
        error = "Musíte přijmout všechna potvrzení k registraci"
        required = "Všechna potvrzení jsou povinná"
    }
}

$localesPath = "C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales"

foreach ($lang in $consentTranslations.Keys) {
    $filePath = Join-Path $localesPath "$lang\common.json"
    
    if (Test-Path $filePath) {
        Write-Host "Processing $lang..." -ForegroundColor Cyan
        
        # Read JSON
        $json = Get-Content $filePath -Raw | ConvertFrom-Json
        
        # Add consent section to auth.register
        if (-not $json.auth.register.consent) {
            $json.auth.register | Add-Member -MemberType NoteProperty -Name "consent" -Value ([PSCustomObject]@{
                title = $consentTranslations[$lang].title
                ai_tool = $consentTranslations[$lang].ai_tool
                no_advice = $consentTranslations[$lang].no_advice
                no_attorney = $consentTranslations[$lang].no_attorney
                error = $consentTranslations[$lang].error
                required = $consentTranslations[$lang].required
            })
            
            # Save JSON
            $json | ConvertTo-Json -Depth 10 | Set-Content $filePath -Encoding UTF8
            Write-Host "✅ Added consent translations to $lang" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Consent already exists in $lang" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    }
}

Write-Host "`n✅ All consent translations added!" -ForegroundColor Green
