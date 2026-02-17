# -*- coding: utf-8 -*-
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Скрипт для додавання перекладів підписок для всіх мов

# Польська (pl)
$plTranslations = @'
        "subscription": {
            "title": "Wybierz subskrypcję",
            "monthly": "1 miesiąc",
            "sixMonths": "6 miesięcy",
            "yearly": "1 rok",
            "perMonth": "za miesiąc",
            "save40": "Oszczędź 40€",
            "save240": "Oszczędź 240€",
            "popular": "NAJPOPULARNIEJSZY",
            "included": "Zawiera:",
            "requests": "zapytań AI",
            "requestsPerMonth": "za miesiąc",
            "requestsMonthly": "miesięcznie",
            "requestsPerDay": "zapytań dziennie",
            "totalRequests6": "Łącznie 3000 zapytań przez 6 mies",
            "totalRequests12": "Łącznie 6000 zapytań rocznie",
            "documents": "Przesyłanie do 100 dokumentów",
            "savings": "Oszczędność",
            "perMonthPrice": "€25/miesiąc",
            "perMonthPrice12": "€22.50/miesiąc",
            "infoTitle": "Ważne informacje:",
            "infoReset": "Limit zapytań odnawia się 1. dnia każdego miesiąca",
            "infoBonus": "Przy subskrypcji otrzymujesz pełny limit natychmiast (bonus!)",
            "infoLimit": "Po wykorzystaniu wszystkich zapytań dostęp jest zawieszony do następnego miesiąca",
            "infoUpgrade": "Zawsze możesz ulepszyć plan lub kupić dodatkowe zapytania"
        }
'@

Write-Host "Переклади для польської мови готові"
Write-Host $plTranslations
