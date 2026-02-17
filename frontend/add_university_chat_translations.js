const fs = require('fs');
const path = require('path');

const localesDir = path.join(__dirname, 'locales');
const languages = {
    sk: {
        title: "AI Konzultant Univerzity",
        welcome: "Vitajte! Som AI asistent pre {university}. Ako vám môžem pomôcť?",
        error: "Prepáčte, vyskytla sa chyba. Skúste to prosím znova.",
        placeholder: "Napíšte svoju otázku...",
        send: "Odoslať"
    },
    cs: {
        title: "AI Konzultant Univerzity",
        welcome: "Vítejte! Jsem AI asistent pro {university}. Jak vám mohu pomoci?",
        error: "Omlouváme se, vyskytla se chyba. Zkuste to prosím znovu.",
        placeholder: "Napište svou otázku...",
        send: "Odeslat"
    },
    pl: {
        title: "AI Konsultant Uniwersytetu",
        welcome: "Witaj! Jestem asystentem AI dla {university}. Jak mogę pomóc?",
        error: "Przepraszamy, wystąpił błąd. Spróbuj ponownie.",
        placeholder: "Wpisz swoje pytanie...",
        send: "Wyślij"
    },
    uk: {
        title: "AI Консультант Університету",
        welcome: "Вітаю! Я AI асистент для {university}. Як я можу допомогти?",
        error: "Вибачте, сталася помилка. Спробуйте ще раз.",
        placeholder: "Введіть ваше запитання...",
        send: "Надіслати"
    },
    en: {
        title: "University AI Consultant",
        welcome: "Welcome! I'm the AI assistant for {university}. How can I help you?",
        error: "Sorry, an error occurred. Please try again.",
        placeholder: "Type your question...",
        send: "Send"
    },
    de: {
        title: "Universitäts-KI-Berater",
        welcome: "Willkommen! Ich bin der KI-Assistent für {university}. Wie kann ich helfen?",
        error: "Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.",
        placeholder: "Geben Sie Ihre Frage ein...",
        send: "Senden"
    },
    fr: {
        title: "Consultant IA Universitaire",
        welcome: "Bienvenue! Je suis l'assistant IA pour {university}. Comment puis-je vous aider?",
        error: "Désolé, une erreur s'est produite. Veuillez réessayer.",
        placeholder: "Tapez votre question...",
        send: "Envoyer"
    },
    es: {
        title: "Consultor IA Universitario",
        welcome: "¡Bienvenido! Soy el asistente IA para {university}. ¿Cómo puedo ayudarte?",
        error: "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.",
        placeholder: "Escribe tu pregunta...",
        send: "Enviar"
    },
    it: {
        title: "Consulente IA Universitario",
        welcome: "Benvenuto! Sono l'assistente IA per {university}. Come posso aiutarti?",
        error: "Spiacente, si è verificato un errore. Riprova.",
        placeholder: "Scrivi la tua domanda...",
        send: "Invia"
    },
    pt: {
        title: "Consultor IA Universitário",
        welcome: "Bem-vindo! Sou o assistente IA para {university}. Como posso ajudar?",
        error: "Desculpe, ocorreu um erro. Por favor, tente novamente.",
        placeholder: "Digite sua pergunta...",
        send: "Enviar"
    },
    ru: {
        title: "AI Консультант Университета",
        welcome: "Добро пожаловать! Я AI ассистент для {university}. Как я могу помочь?",
        error: "Извините, произошла ошибка. Пожалуйста, попробуйте снова.",
        placeholder: "Введите ваш вопрос...",
        send: "Отправить"
    }
};

console.log('🔄 Adding university chat translations...\n');

Object.keys(languages).forEach(lang => {
    const filePath = path.join(localesDir, lang, 'common.json');

    if (fs.existsSync(filePath)) {
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));

        // Add university.chat section
        if (!content.university) {
            content.university = {};
        }

        content.university.chat = languages[lang];

        fs.writeFileSync(filePath, JSON.stringify(content, null, 4), 'utf8');
        console.log(`✅ Updated ${lang}/common.json`);
    } else {
        console.log(`❌ File not found: ${lang}/common.json`);
    }
});

console.log('\n🎉 University chat translations added successfully!');
