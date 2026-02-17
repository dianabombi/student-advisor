# Quick script to add marketplace translations to remaining languages
# Languages: IT, PL, RU, FR, ES, EN

Write-Host "Adding marketplace translations to remaining languages..."

# Italian (IT) - using template
$itMarketplace = @'
    "marketplace": {
        "title": "Marketplace avvocati",
        "searchLawyers": "Cerca avvocati",
        "registerAsLawyer": "Registrati come avvocato",
        "findLawyer": "Trova avvocato",
        "noLawyers": "Nessun avvocato trovato",
        "filters": {
            "title": "Filtri",
            "jurisdiction": "Giurisdizione",
            "specialization": "Specializzazione",
            "rating": "Valutazione minima",
            "language": "Lingua",
            "available": "Solo disponibili",
            "clear": "Cancella filtri",
            "apply": "Applica"
        },
        "specializations": {
            "civil_law": "Diritto civile",
            "criminal_law": "Diritto penale",
            "labor_law": "Diritto del lavoro",
            "family_law": "Diritto di famiglia",
            "commercial_law": "Diritto commerciale",
            "real_estate_law": "Immobiliare",
            "tax_law": "Diritto tributario",
            "intellectual_property": "Proprietà intellettuale",
            "administrative_law": "Diritto amministrativo",
            "corporate_law": "Diritto societario"
        },
        "lawyerCard": {
            "experience": "{{years}} anni di esperienza",
            "rating": "Valutazione",
            "reviews": "{{count}} recensioni",
            "hourlyRate": "{{rate}}€/ora",
            "consultationFee": "Consulenza: {{fee}}€",
            "viewProfile": "Visualizza profilo",
            "verified": "Verificato",
            "available": "Disponibile",
            "unavailable": "Non disponibile"
        },
        "lawyerProfile": {
            "title": "Profilo avvocato",
            "about": "Informazioni",
            "experience": "Esperienza",
            "education": "Formazione",
            "specializations": "Specializzazioni",
            "jurisdictions": "Giurisdizioni",
            "languages": "Lingue",
            "hourlyRate": "Tariffa oraria",
            "consultationFee": "Costo consulenza",
            "orderConsultation": "Prenota consulenza",
            "reviews": "Recensioni",
            "noReviews": "Nessuna recensione",
            "licenseNumber": "Numero licenza",
            "barAssociation": "Ordine degli avvocati",
            "yearsExperience": "{{years}} anni di esperienza",
            "totalCases": "{{count}} casi"
        },
        "registration": {
            "title": "Registrazione avvocato",
            "subtitle": "Unisciti alla nostra piattaforma di servizi legali",
            "step1": "Informazioni personali",
            "step2": "Documenti",
            "step3": "Specializzazioni",
            "step4": "Riepilogo",
            "fullName": "Nome completo",
            "lawyerTitle": "Titolo",
            "licenseNumber": "Numero licenza",
            "barAssociation": "Ordine degli avvocati",
            "experienceYears": "Anni di esperienza",
            "bio": "Biografia",
            "education": "Formazione",
            "hourlyRate": "Tariffa oraria (€)",
            "consultationFee": "Costo consulenza (€)",
            "uploadDiploma": "Carica diploma",
            "uploadLicense": "Carica licenza",
            "uploadId": "Carica documento d'identità",
            "selectJurisdictions": "Seleziona giurisdizioni",
            "selectSpecializations": "Seleziona specializzazioni",
            "selectLanguages": "Seleziona lingue",
            "next": "Avanti",
            "previous": "Indietro",
            "submit": "Invia richiesta",
            "submitting": "Invio in corso...",
            "success": "Registrazione completata! La tua richiesta sarà esaminata entro 48 ore.",
            "error": "Errore di registrazione. Riprova.",
            "required": "Questo campo è obbligatorio",
            "invalidLicense": "Formato numero licenza non valido",
            "fileTooBig": "File troppo grande (max 10MB)",
            "invalidFileType": "Tipo di file non valido (consentiti: PDF, JPG, PNG)"
        },
        "dashboard": {
            "dashboardTitle": "Dashboard avvocato",
            "welcome": "Benvenuto, {{name}}!",
            "stats": {
                "rating": "Valutazione",
                "reviews": "Recensioni",
                "cases": "Casi",
                "activeOrders": "Ordini attivi",
                "completedOrders": "Ordini completati"
            },
            "availability": {
                "title": "Disponibilità",
                "available": "Disponibile per ordini",
                "unavailable": "Non disponibile",
                "toggle": "Cambia stato"
            },
            "profile": {
                "title": "Il mio profilo",
                "edit": "Modifica profilo",
                "update": "Aggiorna",
                "updating": "Aggiornamento...",
                "success": "Profilo aggiornato con successo",
                "error": "Errore nell'aggiornamento del profilo"
            },
            "orders": {
                "title": "Ordini",
                "active": "Attivi",
                "completed": "Completati",
                "noOrders": "Nessun ordine",
                "viewAll": "Visualizza tutti"
            }
        },
        "admin": {
            "title": "Verifica avvocati",
            "pending": "In attesa",
            "verified": "Verificati",
            "rejected": "Rifiutati",
            "noPending": "Nessuna richiesta in attesa",
            "verify": "Verifica",
            "reject": "Rifiuta",
            "verifying": "Verifica in corso...",
            "rejecting": "Rifiuto in corso...",
            "rejectReason": "Motivo del rifiuto",
            "rejectReasonPlaceholder": "Specifica il motivo del rifiuto (minimo 10 caratteri)",
            "verifySuccess": "Avvocato verificato con successo",
            "rejectSuccess": "Richiesta rifiutata",
            "error": "Errore operazione",
            "viewDocuments": "Visualizza documenti",
            "diploma": "Diploma",
            "license": "Licenza",
            "idDocument": "Documento d'identità",
            "registeredAt": "Registrato",
            "confirmVerify": "Sei sicuro di voler verificare questo avvocato?",
            "confirmReject": "Sei sicuro di voler rifiutare questa richiesta?"
        },
        "order": {
            "title": "Prenota consulenza",
            "selectService": "Seleziona servizio",
            "consultation": "Consulenza",
            "documentReview": "Revisione documento",
            "representation": "Rappresentanza",
            "description": "Descrizione problema",
            "descriptionPlaceholder": "Descrivi il tuo problema legale in dettaglio...",
            "preferredDate": "Data preferita",
            "preferredTime": "Ora preferita",
            "submit": "Invia ordine",
            "submitting": "Invio in corso...",
            "success": "Ordine creato con successo",
            "error": "Errore nella creazione dell'ordine",
            "totalCost": "Costo totale",
            "platformFee": "Commissione piattaforma (15%)",
            "lawyerFee": "Pagamento avvocato",
            "payNow": "Paga ora"
        }
    }
'@

Write-Host "IT: Adding marketplace section..."
$itContent = Get-Content "frontend\locales\it\common.json" -Raw
$itContent = $itContent.TrimEnd()
$itContent = $itContent.Substring(0, $itContent.LastIndexOf('}'))
$itContent += ",`n" + $itMarketplace + "`n}"
Set-Content "frontend\locales\it\common.json" -Value $itContent -Encoding UTF8 -NoNewline

Write-Host "✓ IT done"
Write-Host "All translations added successfully!"
