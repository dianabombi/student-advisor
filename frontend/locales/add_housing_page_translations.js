const fs = require('fs');
const path = require('path');

// Housing page translations for all 10 languages
const housingTranslations = {
    sk: {
        "housing": {
            "title": "Hľadanie Ubytovania",
            "subtitle": "Nájdite ideálne ubytovanie pre vaše štúdium",
            "welcome": "Ahoj {{name}}! 👋 Som váš konzultant pre hľadanie ubytovania. Pomôžem vám nájsť perfektné miesto na bývanie počas štúdia. V akom meste hľadáte ubytovanie?",
            "placeholder": "Napíšte správu...",
            "send": "Odoslať",
            "error": "Prepáčte, nastala chyba. Skúste to prosím znova.",
            "info": "Tento konzultant vám pomôže nájsť ubytovanie. Poskytuje len overené informácie a odkazy. Ak niečo nevie, povie vám to priamo a poradí vám vyhľadať cez Google."
        }
    },
    cs: {
        "housing": {
            "title": "Hledání Ubytování",
            "subtitle": "Najděte ideální ubytování pro vaše studium",
            "welcome": "Ahoj {{name}}! 👋 Jsem váš konzultant pro hledání ubytování. Pomůžu vám najít perfektní místo k bydlení během studia. Ve kterém městě hledáte ubytování?",
            "placeholder": "Napište zprávu...",
            "send": "Odeslat",
            "error": "Promiňte, nastala chyba. Zkuste to prosím znovu.",
            "info": "Tento konzultant vám pomůže najít ubytování. Poskytuje pouze ověřené informace a odkazy. Pokud něco neví, řekne vám to přímo a poradí vám vyhledat přes Google."
        }
    },
    en: {
        "housing": {
            "title": "Housing Search",
            "subtitle": "Find the perfect accommodation for your studies",
            "welcome": "Hi {{name}}! 👋 I'm your housing consultant. I'll help you find the perfect place to live during your studies. Which city are you looking for accommodation in?",
            "placeholder": "Type a message...",
            "send": "Send",
            "error": "Sorry, an error occurred. Please try again.",
            "info": "This consultant helps you find housing. It provides only verified information and links. If it doesn't know something, it will tell you directly and suggest searching via Google."
        }
    },
    uk: {
        "housing": {
            "title": "Пошук Житла",
            "subtitle": "Знайдіть ідеальне житло для навчання",
            "welcome": "Привіт {{name}}! 👋 Я ваш консультант з пошуку житла. Допоможу знайти ідеальне місце для проживання під час навчання. В якому місті ви шукаєте житло?",
            "placeholder": "Напишіть повідомлення...",
            "send": "Надіслати",
            "error": "Вибачте, сталася помилка. Спробуйте ще раз.",
            "info": "Цей консультант допоможе знайти житло. Надає лише перевірену інформацію та посилання. Якщо чогось не знає, скаже вам прямо і порадить пошукати через Google."
        }
    },
    pl: {
        "housing": {
            "title": "Wyszukiwanie Zakwaterowania",
            "subtitle": "Znajdź idealne zakwaterowanie na czas studiów",
            "welcome": "Cześć {{name}}! 👋 Jestem twoim konsultantem w poszukiwaniu zakwaterowania. Pomogę ci znaleźć idealne miejsce do życia podczas studiów. W jakim mieście szukasz zakwaterowania?",
            "placeholder": "Wpisz wiadomość...",
            "send": "Wyślij",
            "error": "Przepraszamy, wystąpił błąd. Spróbuj ponownie.",
            "info": "Ten konsultant pomoże ci znaleźć zakwaterowanie. Dostarcza tylko zweryfikowane informacje i linki. Jeśli czegoś nie wie, powie ci to wprost i zasugeruje wyszukanie przez Google."
        }
    },
    de: {
        "housing": {
            "title": "Wohnungssuche",
            "subtitle": "Finden Sie die perfekte Unterkunft für Ihr Studium",
            "welcome": "Hallo {{name}}! 👋 Ich bin Ihr Berater für die Wohnungssuche. Ich helfe Ihnen, den perfekten Ort zum Leben während Ihres Studiums zu finden. In welcher Stadt suchen Sie eine Unterkunft?",
            "placeholder": "Nachricht eingeben...",
            "send": "Senden",
            "error": "Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.",
            "info": "Dieser Berater hilft Ihnen bei der Wohnungssuche. Er liefert nur verifizierte Informationen und Links. Wenn er etwas nicht weiß, wird er es Ihnen direkt sagen und vorschlagen, über Google zu suchen."
        }
    },
    fr: {
        "housing": {
            "title": "Recherche de Logement",
            "subtitle": "Trouvez le logement parfait pour vos études",
            "welcome": "Bonjour {{name}}! 👋 Je suis votre consultant en recherche de logement. Je vous aiderai à trouver l'endroit parfait pour vivre pendant vos études. Dans quelle ville cherchez-vous un logement?",
            "placeholder": "Tapez un message...",
            "send": "Envoyer",
            "error": "Désolé, une erreur s'est produite. Veuillez réessayer.",
            "info": "Ce consultant vous aide à trouver un logement. Il ne fournit que des informations et des liens vérifiés. S'il ne sait pas quelque chose, il vous le dira directement et vous suggérera de rechercher via Google."
        }
    },
    es: {
        "housing": {
            "title": "Búsqueda de Alojamiento",
            "subtitle": "Encuentra el alojamiento perfecto para tus estudios",
            "welcome": "¡Hola {{name}}! 👋 Soy tu consultor de búsqueda de alojamiento. Te ayudaré a encontrar el lugar perfecto para vivir durante tus estudios. ¿En qué ciudad buscas alojamiento?",
            "placeholder": "Escribe un mensaje...",
            "send": "Enviar",
            "error": "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.",
            "info": "Este consultor te ayuda a encontrar alojamiento. Solo proporciona información y enlaces verificados. Si no sabe algo, te lo dirá directamente y te sugerirá buscar a través de Google."
        }
    },
    it: {
        "housing": {
            "title": "Ricerca Alloggio",
            "subtitle": "Trova l'alloggio perfetto per i tuoi studi",
            "welcome": "Ciao {{name}}! 👋 Sono il tuo consulente per la ricerca di alloggi. Ti aiuterò a trovare il posto perfetto dove vivere durante i tuoi studi. In quale città cerchi un alloggio?",
            "placeholder": "Scrivi un messaggio...",
            "send": "Invia",
            "error": "Spiacente, si è verificato un errore. Riprova.",
            "info": "Questo consulente ti aiuta a trovare un alloggio. Fornisce solo informazioni e link verificati. Se non sa qualcosa, te lo dirà direttamente e ti suggerirà di cercare tramite Google."
        }
    },
    ru: {
        "housing": {
            "title": "Поиск Жилья",
            "subtitle": "Найдите идеальное жилье для учебы",
            "welcome": "Привет {{name}}! 👋 Я ваш консультант по поиску жилья. Помогу найти идеальное место для проживания во время учебы. В каком городе вы ищете жилье?",
            "placeholder": "Напишите сообщение...",
            "send": "Отправить",
            "error": "Извините, произошла ошибка. Пожалуйста, попробуйте снова.",
            "info": "Этот консультант поможет найти жилье. Предоставляет только проверенную информацию и ссылки. Если чего-то не знает, скажет вам прямо и посоветует поискать через Google."
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

        console.log(`✅ Updated ${lang}/common.json with housing page translations`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n🎉 All housing translations added successfully!');
